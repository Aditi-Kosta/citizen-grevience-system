import hashlib
import numpy as np
from pathlib import Path
from backend.app.config import DATA_DIR

CACHE = DATA_DIR / "embeddings"
CACHE.mkdir(parents=True, exist_ok=True)


def text_hash(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def embed(text: str):
    """Optional real embedding service. Falls back to deterministic token hashing for mock mode."""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        return model.encode([text], normalize_embeddings=True)[0]
    except Exception:
        vec = np.zeros(128, dtype=np.float32)
        for token in text.lower().split():
            vec[hash(token) % 128] += 1
        norm = np.linalg.norm(vec)
        return vec / norm if norm else vec


def cosine(a, b):
    a, b = np.asarray(a), np.asarray(b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom else 0.0
