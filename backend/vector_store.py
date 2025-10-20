import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict

from backend.embeddings import create_embeddings

# Initialize Chroma client (persistent)
def get_chroma_client(persist_dir: str = "chroma_db"):
    os.makedirs(persist_dir, exist_ok=True)
    client = chromadb.Client(Settings(persist_directory=persist_dir, anonymized_telemetry=False))
    return client


def get_or_create_collection(client, name: str = "resumes"):
    """Create or load a Chroma collection for resumes."""
    return client.get_or_create_collection(name=name)


def add_resumes_to_db(collection, resume_texts: List[str], resume_ids: List[str]):
    """Add parsed resumes to Chroma vector database with embeddings and metadata."""
    if len(resume_texts) != len(resume_ids):
        raise ValueError("resume_texts and resume_ids must have the same length")

    embeddings = create_embeddings(resume_texts)
    embeddings_list = [emb.tolist() for emb in embeddings]

    # Metadata can store the same IDs for easier retrieval
    metadatas = [{"id": rid} for rid in resume_ids]

    collection.add(
        ids=resume_ids,              # required
        embeddings=embeddings_list,
        documents=resume_texts,
        metadatas=metadatas
    )

def search_top_k(collection, query_text: str, k: int = 3) -> List[Dict[str, str]]:
    """Return top K most similar resumes given a job description query."""
    query_embedding = create_embeddings(query_text)[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "distances", "metadatas"]
    )

    if not results or not results.get("documents"):
        return []

    top_results = []
    for i in range(len(results["documents"][0])):
        top_results.append({
            "id": results["metadatas"][0][i].get("id", f"resume_{i}"),
            "distance": results["distances"][0][i],
            "document": results["documents"][0][i]
        })

    return top_results


if __name__ == "__main__":
    # Test vector store pipeline
    client = get_chroma_client()
    collection = get_or_create_collection(client)

    resumes = [
        "Data scientist with strong skills in Python and TensorFlow.",
        "Software engineer experienced in backend development using Node.js.",
        "Frontend developer skilled in React and TypeScript.",
    ]

    ids = ["r1", "r2", "r3"]

    add_resumes_to_db(collection, resumes, ids)

    query = "Looking for a Python developer experienced in ML."
    results = search_top_k(collection, query)
    for r in results:
        print(r)
