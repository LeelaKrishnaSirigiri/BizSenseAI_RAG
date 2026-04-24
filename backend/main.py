import os
import tempfile
import hashlib

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.db import Base, engine, get_db
from backend.models import User

from langsmith import traceable
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from docx import Document as DocxDocument
from langgraph.graph import StateGraph

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "BizSenseAI"

app = FastAPI(title="BizSense AI Backend")

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

base_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

base_retriever = base_db.as_retriever(search_kwargs={"k": 5})

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=512
)

user_vector_dbs = {}


# request models
class SignupRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    question: str
    user: str
    history: list = []


# password helpers
def normalize_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def hash_password(password: str) -> str:
    return pwd_context.hash(normalize_password(password))


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(normalize_password(password), password_hash)


# basic routes
@app.get("/")
def home():
    return {"status": "BizSense AI backend running"}


@app.post("/signup")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == req.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=req.username,
        password_hash=hash_password(req.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "username": user.username
        }
    }


@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username
        }
    }


# upload route
@app.post("/upload/{user}")
async def upload_file(user: str, file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename.lower()
    text = ""

    if filename.endswith(".txt"):
        text = content.decode("utf-8")

    elif filename.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        text = "\n".join([page.page_content for page in pages])

        try:
            os.remove(tmp_path)
        except Exception:
            pass

    elif filename.endswith(".docx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        doc = DocxDocument(tmp_path)
        text = "\n".join([para.text for para in doc.paragraphs])

        try:
            os.remove(tmp_path)
        except Exception:
            pass

    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if not text.strip():
        raise HTTPException(status_code=400, detail="Uploaded file has no readable text")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.create_documents([text])

    user_vector_dbs[user] = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return {
        "message": "File uploaded and processed successfully",
        "chunks": len(chunks)
    }


# langgraph nodes
@traceable(name="Route Node")
def route_node(state: dict):
    query = state["query"]
    user = state["user"]
    history = state.get("history", [])

    docs = []
    used_source = "base_chroma_db"

    if user in user_vector_dbs:
        upload_docs = user_vector_dbs[user].similarity_search(query, k=3)
        docs.extend(upload_docs)
        used_source = "uploaded_file_and_base_chroma_db"

    base_docs = base_retriever.invoke(query)
    docs.extend(base_docs)

    return {
        "query": query,
        "user": user,
        "history": history,
        "docs": docs,
        "used_source": used_source
    }

@traceable(name="Answer Node")
def answer_node(state: dict):
    docs = state.get("docs", [])
    query = state.get("query", "")
    history = state.get("history", [])

    history_text = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in history[-6:]]
    )

    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = f"""
You are BizSense AI, an internal knowledge-base assistant for Nexora Technologies.

Rules:
1. If user greets you response to him politely.
2. Answer ONLY using the provided Context or Chat History.
3. Do NOT repeat the question like you asked.
4. Do NOT use general knowledge.
5. If the answer is not clearly present in the Context or knowledge base or Chat History, say exactly: "I don't know."


Chat History:
{history_text}

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(final_prompt)

    return {
        "answer": response.content,
        "source_count": len(docs),
        "used_source": state.get("used_source", "unknown")
    }


# build graph
graph = StateGraph(dict)
graph.add_node("route", route_node)
graph.add_node("answer", answer_node)
graph.set_entry_point("route")
graph.add_edge("route", "answer")
compiled_graph = graph.compile()


# chat route
@app.post("/chat")
def chat(req: ChatRequest):
    query = req.question.strip().lower()

    greetings = [
        "hi",
        "hello",
        "hey",
        "hii",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if query in greetings:
        return {
            "answer": "Hello! How can I help you today?",
            "source_count": 0,
            "used_source": "greeting_handler"
        }

    result = compiled_graph.invoke({
        "query": req.question,
        "user": req.user,
        "history": req.history
    })

    return {
        "answer": result["answer"],
        "source_count": result["source_count"],
        "used_source": result["used_source"]
    }