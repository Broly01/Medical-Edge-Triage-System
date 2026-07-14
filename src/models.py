from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SymptomInput:
    text: str
    age: Optional[int] = None
    duration_hours: Optional[int] = None


@dataclass
class RetrievedChunk:
    content: str
    source_name: str
    source_date: str
    document_type: str
    score: float = 0.0


@dataclass
class TriageResult:
    triage_level: str
    confidence: float
    reasoning: str
    supporting_evidence: List[str] = field(default_factory=list)
    outdated_sources: List[str] = field(default_factory=list)
    knowledge_warnings: List[str] = field(default_factory=list)
    pass_votes: List[str] = field(default_factory=list)


@dataclass
class CounterfactualResult:
    original_level: str
    counterfactual_level: str
    removed_symptom: str
    reasoning: str
