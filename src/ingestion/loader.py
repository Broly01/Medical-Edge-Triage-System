import json
import re
from typing import List, Dict


def chunk_text(text: str, chunk_size: int = 512, chunk_overlap: int = 64) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks


def load_medquad(filepath: str) -> List[Dict]:
    data = []
    with open(filepath, "r") as f:
        for line in f:
            entry = json.loads(line)
            data.append(entry)
    return data


def load_guidelines(filepath: str) -> List[Dict]:
    with open(filepath, "r") as f:
        content = f.read()
    sections = re.split(r"\n#{2,3}\s+", content)
    data = []
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split("\n")
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        data.append({"title": title, "content": body, "source": filepath})
    return data


def load_documents(sources: List[str]) -> List[Dict]:
    all_docs = []
    for source in sources:
        if source.endswith(".jsonl"):
            all_docs.extend(load_medquad(source))
        elif source.endswith(".md"):
            all_docs.extend(load_guidelines(source))
    return all_docs
