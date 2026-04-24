from langchain_community.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

def create_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
    
    db.persist()
    return db


def load_vectorstore():
    embeddings = OpenAIEmbeddings()
    
    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    
    return db