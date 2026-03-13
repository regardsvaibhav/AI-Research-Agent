import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sentence_transformers import SentenceTransformer
import numpy as np

# Load once, reuse everywhere
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> np.ndarray:
    """Convert list of texts into vectors."""
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings

def embed_query(query: str) -> np.ndarray:
    """Convert a single query into a vector."""
    return model.encode([query])[0]