from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.models import TriageResult, CounterfactualResult
from src.orchestrator import run_triage, run_counterfactual

app = FastAPI(
    title="Medical Edge Triage API",
    version="1.0.0",
)


class TriageRequest(BaseModel):
    symptoms: str
    age: int | None = None
    duration_hours: int | None = None


class CounterfactualRequest(BaseModel):
    symptoms: str
    remove_symptom: str


class TriageResponse(BaseModel):
    triage_level: str
    confidence: float
    reasoning: str
    supporting_evidence: list[str]
    outdated_sources: list[str]
    knowledge_warnings: list[str]
    pass_votes: list[str]


class CounterfactualResponse(BaseModel):
    original_level: str
    counterfactual_level: str
    removed_symptom: str
    reasoning: str


@app.post("/triage", response_model=TriageResponse)
def triage_endpoint(req: TriageRequest):
    if not req.symptoms.strip():
        raise HTTPException(status_code=400, detail="Symptoms cannot be empty")
    result: TriageResult = run_triage(req.symptoms)
    return TriageResponse(
        triage_level=result.triage_level,
        confidence=result.confidence,
        reasoning=result.reasoning,
        supporting_evidence=result.supporting_evidence,
        outdated_sources=result.outdated_sources,
        knowledge_warnings=result.knowledge_warnings,
        pass_votes=result.pass_votes,
    )


@app.post("/counterfactual", response_model=CounterfactualResponse)
def counterfactual_endpoint(req: CounterfactualRequest):
    if not req.symptoms.strip():
        raise HTTPException(status_code=400, detail="Symptoms cannot be empty")
    if not req.remove_symptom.strip():
        raise HTTPException(status_code=400, detail="remove_symptom cannot be empty")
    result: CounterfactualResult = run_counterfactual(req.symptoms, req.remove_symptom)
    return CounterfactualResponse(
        original_level=result.original_level,
        counterfactual_level=result.counterfactual_level,
        removed_symptom=result.removed_symptom,
        reasoning=result.reasoning,
    )


@app.get("/health")
def health():
    return {"status": "healthy", "service": "Medical Edge Triage"}


@app.get("/metrics")
def metrics():
    return {
        "embedding_model": "nomic-embed-text",
        "reasoning_model": "qwen2.5:3b",
        "vector_db": "lancedb",
    }
