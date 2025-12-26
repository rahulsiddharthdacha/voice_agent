import numpy as np
import re
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

with open("data/raw/where_is_my_money_links.json") as f:
    links = json.load(f)


CANONICAL_ALLOWED_QUERIES = [item['title'] for item in links]


SIMILARITY_THRESHOLD = 0.72


def normalize(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec)
    return vec if norm == 0 else vec / norm


def preprocess(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text


class IntentGate:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        # Preprocess canonical queries
        canonical = [preprocess(q) for q in CANONICAL_ALLOWED_QUERIES]

        raw_embeddings = self.embeddings.embed_documents(canonical)

        # Normalize once
        self.allowed_embeddings = np.array(
            [normalize(np.array(e)) for e in raw_embeddings]
        )

    def is_supported(self, query: str) -> bool:
        if not query or len(query.strip()) < 3:
            return False

        query = preprocess(query)

        query_embedding = normalize(
            np.array(self.embeddings.embed_query(query))
        )

        scores = self.allowed_embeddings @ query_embedding

        return float(np.max(scores)) >= SIMILARITY_THRESHOLD
