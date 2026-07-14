from typing import List

from src.config import config
from src.ingestion.loader import chunk_text
from src.ingestion.embedder import generate_embedding
from src.ingestion.metadata_tagger import tag_chunks
from src.retrieval.retriever import get_db, insert_documents


def run_pipeline(sources: List[str], source_name: str, source_date: str, document_type: str):
    db = get_db()

    all_records = []
    for source in sources:
        with open(source, "r") as f:
            text = f.read()

        chunks = chunk_text(text, config.chunk_size, config.chunk_overlap)
        tagged = tag_chunks(chunks, source_name, source_date, document_type)

        for item in tagged:
            embedding = generate_embedding(item["content"])
            all_records.append({
                "id": f"{source_name}-{len(all_records)}",
                "content": item["content"],
                "embedding": embedding,
                "source_name": item["source_name"],
                "source_date": item["source_date"],
                "document_type": item["document_type"],
            })

    insert_documents(db, all_records)
    print(f"Ingested {len(all_records)} chunks from {source_name}")
