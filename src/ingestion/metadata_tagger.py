from typing import Dict, List


def tag_source(source_name: str, source_date: str, document_type: str) -> Dict:
    return {
        "source_name": source_name,
        "source_date": source_date,
        "document_type": document_type,
    }


def tag_chunks(chunks: List[str], source_name: str, source_date: str, document_type: str) -> List[Dict]:
    metadata = tag_source(source_name, source_date, document_type)
    return [
        {"content": chunk, **metadata}
        for chunk in chunks
    ]
