#!/usr/bin/env python3
from src.ingestion.pipeline import run_pipeline

if __name__ == "__main__":
    import sys

    sources = sys.argv[1:] if len(sys.argv) > 1 else ["data/sample.txt"]
    run_pipeline(
        sources=sources,
        source_name="Clinical Reference",
        source_date="2024-06",
        document_type="guideline",
    )
