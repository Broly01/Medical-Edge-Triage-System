from typing import List

from src.models import CounterfactualResult, RetrievedChunk, TriageResult
from src.reasoning.uncertainty import multi_pass_inference


def compute_counterfactual(
    symptoms: str, remove_symptom: str, chunks: List[RetrievedChunk]
) -> CounterfactualResult:
    original: TriageResult = multi_pass_inference(symptoms, chunks)

    modified_symptoms = _remove_symptom(symptoms, remove_symptom)
    counterfactual: TriageResult = multi_pass_inference(modified_symptoms, chunks)

    reasoning = (
        f"Original: {original.triage_level} (confidence: {original.confidence})\n"
        f"Without '{remove_symptom}': {counterfactual.triage_level} "
        f"(confidence: {counterfactual.confidence})\n\n"
        f"This shows the symptom '{remove_symptom}' was "
        f"{'critical' if original.triage_level != counterfactual.triage_level else 'not critical'} "
        f"to the triage decision."
    )

    return CounterfactualResult(
        original_level=original.triage_level,
        counterfactual_level=counterfactual.triage_level,
        removed_symptom=remove_symptom,
        reasoning=reasoning,
    )


def _remove_symptom(symptoms: str, symptom: str) -> str:
    words = symptoms.split()
    filtered = [w for w in words if w.lower() != symptom.lower()]
    return " ".join(filtered)
