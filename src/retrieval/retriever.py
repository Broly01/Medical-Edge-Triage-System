from typing import List, Optional
import lancedb

from src.config import config
from src.ingestion.embedder import generate_embedding
from src.models import RetrievedChunk


def get_db() -> lancedb.DBConnection:
    return lancedb.connect(config.lancedb_uri)


def get_or_create_table(db: lancedb.DBConnection):
    try:
        return db.open_table(config.collection_name)
    except Exception:
        return db.create_table(config.collection_name, data=[
            {
                "id": "init",
                "content": "initialize",
                "embedding": [0.0] * 768,
                "source_name": "system",
                "source_date": "2024-01",
                "document_type": "init",
            }
        ])


def insert_documents(db: lancedb.DBConnection, documents: List[dict]):
    table = db.open_table(config.collection_name)
    table.add(documents)


def retrieve(query: str, top_k: Optional[int] = None) -> List[RetrievedChunk]:
    if top_k is None:
        top_k = config.retrieval_top_k

    db = get_db()
    try:
        table = db.open_table(config.collection_name)
    except Exception:
        return []

    embedding = generate_embedding(query)
    results = table.search(embedding).limit(top_k).to_list()

    chunks = []
    for r in results:
        chunks.append(RetrievedChunk(
            content=r["content"],
            source_name=r.get("source_name", "Unknown"),
            source_date=r.get("source_date", "Unknown"),
            document_type=r.get("document_type", "Unknown"),
            score=r.get("_distance", 0.0),
        ))
    return chunks
