import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    embedding_model: str = "nomic-embed-text"
    reasoning_model: str = "qwen3:8b"

    lancedb_uri: str = os.getenv("LANCEDB_URI", "data/lancedb")
    collection_name: str = "medical_triage"

    chunk_size: int = 512
    chunk_overlap: int = 64

    retrieval_top_k: int = 10
    rerank_top_k: int = 5

    num_reasoning_passes: int = 5
    freshness_threshold_months: int = 24

    counterfactual_remove_symptom: str = ""

    triage_levels: List[str] = field(default_factory=lambda: [
        "Level 1 — Resuscitation",
        "Level 2 — Emergency",
        "Level 3 — Urgent",
        "Level 4 — Semi-Urgent",
        "Level 5 — Non-Urgent",
    ])

    def __post_init__(self):
        os.makedirs(self.lancedb_uri, exist_ok=True)


config = Config()
