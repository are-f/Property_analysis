import json
from rag.embedder import chunk_dataset
from rag.vector_store import save_vector_store

def build_rag_index(input_file="data/raw_data.json"):
    with open(input_file, "r") as f:
        records = json.load(f)
    chunks = chunk_dataset(records)
    save_vector_store(chunks)
