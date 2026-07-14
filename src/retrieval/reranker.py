from typing import List

from src.config import config
from src.models import RetrievedChunk


def rerank(query: str, chunks: List[RetrievedChunk]) -> List[RetrievedChunk]:
    relevance_scores = []
    query_lower = query.lower()
    query_terms = set(query_lower.split())

    for chunk in chunks:
        content_lower = chunk.content.lower()
        term_matches = sum(1 for term in query_terms if term in content_lower)
        score = term_matches / max(len(query_terms), 1)
        relevance_scores.append(score)

    scored = list(zip(chunks, relevance_scores))
    scored.sort(key=lambda x: x[1], reverse=True)

    return [chunk for chunk, _ in scored[:config.rerank_top_k]]
