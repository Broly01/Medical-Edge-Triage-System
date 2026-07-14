#!/usr/bin/env python3
"""Download sample medical triage data for testing the system."""

import json
import os
from pathlib import Path


def create_sample_data():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    samples = [
        {
            "symptoms": "fever 39C headache stiff neck photophobia",
            "triage": "Level 2 — Emergency",
            "rationale": "Meningitis symptoms require immediate evaluation"
        },
        {
            "symptoms": "chest pain radiating to left arm shortness of breath diaphoresis",
            "triage": "Level 1 — Resuscitation",
            "rationale": "STEMI presentation needs immediate resuscitation"
        },
        {
            "symptoms": "cough productive fever 38C wheezing",
            "triage": "Level 3 — Urgent",
            "rationale": "Lower respiratory infection, urgent but stable"
        },
        {
            "symptoms": "mild headache no fever normal vitals",
            "triage": "Level 5 — Non-Urgent",
            "rationale": "Minor complaint, can wait for primary care"
        },
    ]

    output_path = data_dir / "sample_triage.json"
    with open(output_path, "w") as f:
        json.dump(samples, f, indent=2)
    print(f"Created {output_path} with {len(samples)} sample cases")

    guidelines = """# Clinical Triage Guidelines

## Meningitis Signs
- Fever
- Neck stiffness
- Headache
- Photophobia
- Altered mental status
- Petechial rash

## Cardiac Emergency Signs
- Chest pain or discomfort
- Pain radiating to arm, jaw, or back
- Shortness of breath
- Nausea or vomiting
- Diaphoresis
- Lightheadedness

## Respiratory Infection Signs
- Cough (productive or dry)
- Fever
- Shortness of breath
- Wheezing
- Sputum production

## Minor Complaints
- Mild headache
- Low-grade fever (<38C)
- Minor cuts and bruises
- Common cold symptoms
"""
    guidelines_path = data_dir / "triage_guidelines.md"
    with open(guidelines_path, "w") as f:
        f.write(guidelines)
    print(f"Created {guidelines_path}")


if __name__ == "__main__":
    create_sample_data()
