import os
import shutil
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_PATH = "data"
DB_PATH = "chroma_db"

if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)
    print("Old ChromaDB deleted")

documents = []

for file in os.listdir(DOCS_PATH):
    if file.endswith(".txt"):
        file_path = os.path.join(DOCS_PATH, file)
        loader = TextLoader(file_path, encoding="utf-8")
        documents.extend(loader.load())

print("Documents loaded:", len(documents))

if not documents:
    raise ValueError("No .txt files found in data folder")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(documents)

print("Chunks created:", len(chunks))

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DB_PATH
)

print("ChromaDB created successfully")
print("Saved at:", DB_PATH)