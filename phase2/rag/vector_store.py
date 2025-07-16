from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def save_vector_store(docs, path="rag/vector_index"):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(path)

def load_vector_store(path="rag/vector_index"):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(path, embeddings)
