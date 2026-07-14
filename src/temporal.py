from datetime import datetime
from typing import List, Tuple

from src.config import config
from src.models import RetrievedChunk


def parse_source_date(source_date: str) -> datetime:
    try:
        return datetime.strptime(source_date, "%Y-%m")
    except ValueError:
        try:
            return datetime.strptime(source_date, "%Y")
        except ValueError:
            return datetime.now()


def get_knowledge_age(source_date: str) -> int:
    pub_date = parse_source_date(source_date)
    now = datetime.now()
    return (now.year - pub_date.year) * 12 + (now.month - pub_date.month)


def filter_fresh(chunks: List[RetrievedChunk]) -> Tuple[List[RetrievedChunk], List[str]]:
    fresh = []
    warnings = []

    for chunk in chunks:
        age_months = get_knowledge_age(chunk.source_date)
        if age_months > config.freshness_threshold_months:
            warnings.append(
                f"[KNOWLEDGE WARNING] '{chunk.source_name}' ({chunk.source_date}) "
                f"is {age_months} months old. Source may contain outdated medical information."
            )
        else:
            fresh.append(chunk)

    return fresh, warnings
