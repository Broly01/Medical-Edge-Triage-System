import random
from typing import List

import numpy as np

from src.config import config
from src.models import RetrievedChunk, TriageResult
from src.reasoning.inference import run_inference


LEVEL_WEIGHTS = {
    "Level 1": 5,
    "Level 2": 4,
    "Level 3": 3,
    "Level 4": 2,
    "Level 5": 1,
}


def extract_level_number(level_str: str) -> int:
    for key in LEVEL_WEIGHTS:
        if key in level_str:
            return LEVEL_WEIGHTS[key]
    return 3


def multi_pass_inference(symptoms: str, chunks: List[RetrievedChunk]) -> TriageResult:
    passes = config.num_reasoning_passes
    all_outputs = []
    votes = []

    for i in range(passes):
        sampled = random.sample(chunks, min(len(chunks), max(3, len(chunks) - 1)))
        random.shuffle(sampled)

        output = run_inference(symptoms, sampled)
        level = output.get("triage_level", "Level 3 — Urgent")
        all_outputs.append(level)
        votes.append(level)

    numeric_levels = [extract_level_number(l) for l in all_outputs]
    variance = float(np.var(numeric_levels))
    max_variance = 4.0
    confidence = max(0.0, 1.0 - variance / max_variance)

    final_level = max(set(all_outputs), key=all_outputs.count)
    reasoning = f"Multi-pass consensus across {passes} passes.\n"
    for i, v in enumerate(all_outputs):
        reasoning += f"  Pass {i+1}: {v}\n"

    return TriageResult(
        triage_level=final_level,
        confidence=round(confidence, 3),
        reasoning=reasoning.strip(),
        supporting_evidence=[c.source_name for c in chunks[:3]],
        pass_votes=votes,
    )
