from typing import List
import ollama

from src.config import config


def generate_embedding(text: str) -> List[float]:
    response = ollama.embeddings(
        model=config.embedding_model,
        prompt=text,
    )
    return response["embedding"]


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    return [generate_embedding(t) for t in texts]
