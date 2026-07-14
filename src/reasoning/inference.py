import json
from typing import List

import ollama

from src.config import config
from src.models import RetrievedChunk, TriageResult


def build_prompt(symptoms: str, chunks: List[RetrievedChunk]) -> str:
    context = "\n\n".join([
        f"[Source: {c.source_name} ({c.source_date})]\n{c.content}"
        for c in chunks
    ])

    prompt = f"""You are a medical triage assistant. Analyze the symptoms using the retrieved clinical context.

Symptoms:
{symptoms}

Retrieved Context:
{context}

Provide output as JSON only with these fields:
{{
  "triage_level": one of {config.triage_levels},
  "confidence": float between 0 and 1,
  "reasoning": "step-by-step clinical reasoning",
  "supporting_evidence": ["list of source names used"]
}}"""
    return prompt


def run_inference(symptoms: str, chunks: List[RetrievedChunk]) -> dict:
    prompt = build_prompt(symptoms, chunks)

    messages = [
        {"role": "system", "content": "You are a medical triage expert. Output only valid JSON."},
        {"role": "user", "content": prompt},
    ]

    response = ollama.chat(
        model=config.reasoning_model,
        messages=messages,
        format="json",
    )

    content = response["message"]["content"]
    return json.loads(content)
