from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def chunk_dataset(records):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=str(record)) for record in records]
    return splitter.split_documents(docs)
