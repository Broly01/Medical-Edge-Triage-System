from src.models import CounterfactualResult, TriageResult
from src.retrieval.retriever import retrieve
from src.retrieval.reranker import rerank
from src.temporal import filter_fresh
from src.reasoning.uncertainty import multi_pass_inference
from src.reasoning.counterfactual import compute_counterfactual


def run_triage(symptoms: str) -> TriageResult:
    retrieved = retrieve(symptoms)
    reranked = rerank(symptoms, retrieved)
    fresh_chunks, warnings = filter_fresh(reranked)

    result = multi_pass_inference(symptoms, fresh_chunks)
    result.knowledge_warnings = warnings
    result.outdated_sources = [
        c.source_name for c in reranked if c not in fresh_chunks
    ]

    return result


def run_counterfactual(symptoms: str, remove_symptom: str) -> CounterfactualResult:
    retrieved = retrieve(symptoms)
    reranked = rerank(symptoms, retrieved)
    fresh_chunks, _ = filter_fresh(reranked)

    return compute_counterfactual(symptoms, remove_symptom, fresh_chunks)
