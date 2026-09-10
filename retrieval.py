# retrieval.py
# Turns text into embedding vectors and finds the most relevant chunks by
# cosine similarity.

import math

from config import EMBEDDING_MODEL_ALIAS, TOP_K, ensure_model_ready, get_openai_client
from database import get_all_documents


def get_embedding(text: str) -> list[float]:
    """Convert the given text into a vector using Foundry Local's embedding model."""
    ensure_model_ready(EMBEDDING_MODEL_ALIAS)
    client = get_openai_client()

    response = client.embeddings.create(model=EMBEDDING_MODEL_ALIAS, input=text)
    return response.data[0].embedding


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """Cosine similarity between two vectors: (A . B) / (|A| * |B|), range -1 to 1.

    Higher means the vectors point in a more similar direction, i.e. the
    texts are closer in meaning.
    """
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def get_top_chunks(query: str, top_k: int = TOP_K) -> list[dict]:
    """Return the top_k stored chunks most similar to the query.

    Embeds the query, scores every stored chunk by cosine similarity, and
    returns the highest-scoring top_k.
    """
    query_embedding = get_embedding(query)
    documents = get_all_documents()

    for document in documents:
        document["similarity"] = cosine_similarity(query_embedding, document["embedding"])

    documents.sort(key=lambda document: document["similarity"], reverse=True)
    return documents[:top_k]
