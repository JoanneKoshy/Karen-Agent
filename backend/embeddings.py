from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np

# Load the embedding model once globally to avoid reloading each time
_model = None

def get_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> SentenceTransformer:
    """Load and cache the embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model


def create_embeddings(texts: Union[str, List[str]]) -> np.ndarray:
    """Generate embeddings for one or multiple text inputs.

    Args:
        texts: a single string or list of strings.

    Returns:
        np.ndarray: Embedding vector(s)
    """
    model = get_embedding_model()

    # Convert single string to list for consistency
    if isinstance(texts, str):
        texts = [texts]

    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if a.ndim > 1:
        a = a.flatten()
    if b.ndim > 1:
        b = b.flatten()
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


if __name__ == "__main__":
    sample_texts = [
        "Experienced data scientist skilled in Python and machine learning.",
        "Frontend developer proficient in React and TypeScript.",
    ]
    embs = create_embeddings(sample_texts)
    print("Embeddings shape:", embs.shape)
    print("Cosine similarity:", cosine_similarity(embs[0], embs[1]))
