# Medical Edge Triage System

AI-powered medical triage assistant that classifies patient symptoms into urgency levels (Level 1 — Resuscitation through Level 5 — Non-Urgent) using Retrieval-Augmented Generation (RAG), multi-pass reasoning with uncertainty quantification, and counterfactual explanations.

## Architecture

```
Patient Symptoms
       ↓
Ollama Embeddings (nomic-embed-text) — 768-dim vector
       ↓
LanceDB Vector Retrieval — ANN search (top-10)
       ↓
Term-Match Reranker — Jaccard-like scoring (top-5)
       ↓
Temporal Knowledge Filtering — flags sources >24 months old
       ↓
Multi-Pass Reasoning — 5 passes via Qwen 3 8B
       ↓
Variance-Based Confidence Score — 1 − σ²/4.0
       ↓
Counterfactual Explanation — remove symptom → re-run → compare
       ↓
Final Triage Decision (Level 1–5)
```

## Triage Levels

| Level | Label | Example |
|-------|-------|---------|
| Level 1 | Resuscitation | Cardiac arrest, severe trauma |
| Level 2 | Emergency | Meningitis signs, STEMI |
| Level 3 | Urgent | Pneumonia, moderate asthma |
| Level 4 | Semi-Urgent | Mild infection, stable fracture |
| Level 5 | Non-Urgent | Minor headache, common cold |

## Setup

### 1. Install Ollama

```bash
brew install ollama
```

Or via script:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Start Ollama

```bash
ollama serve
```

### 3. Pull Models

Two models are required:

```bash
ollama pull nomic-embed-text     # 274 MB — embeddings
ollama pull qwen2.5:3b           # 1.7 GB — LLM reasoning
```

> **Performance note:** qwen2.5:3b takes ~30s to load on first inference, then ~10s per inference pass.

### 4. Create Python Environment

Using `uv` (recommended):

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Or using `pip`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5. Generate Sample Data

```bash
python scripts/download_data.py
```

This creates:
- `data/sample_triage.json` — 4 sample triage cases
- `data/triage_guidelines.md` — clinical guidelines text

### 6. Ingest Data into Vector Database

```bash
python run_ingest.py data/triage_guidelines.md
```

This chunks the guidelines (512 tokens, 64 overlap), generates embeddings via `nomic-embed-text`, and stores them in `data/lancedb/`.

## Run

### Single Command (recommended)

```bash
./run.sh
```

This starts Ollama (if not running), preloads the model in background, and launches Streamlit UI at **http://localhost:8501**.

### Streamlit UI

```bash
streamlit run src/ui/app.py
```

Enter symptoms like `fever 39C headache stiff neck`, click **Analyze**, and see:
- Triage level with color-coded urgency
- Confidence score
- Step-by-step reasoning
- Supporting evidence sources
- Knowledge warnings for outdated sources
- Multi-pass vote breakdown
- Counterfactual analysis (remove a symptom to test impact)

### FastAPI Backend

```bash
python run_api.py
```

Open **http://localhost:8000/docs** for interactive Swagger docs.

#### POST /triage

```json
{ "symptoms": "fever 39C headache stiff neck" }
```

Response:

```json
{
  "triage_level": "Level 2 — Emergency",
  "confidence": 0.82,
  "reasoning": "Multi-pass consensus across 5 passes.\n  Pass 1: Level 2\n  Pass 2: Level 2\n  Pass 3: Level 3\n  Pass 4: Level 2\n  Pass 5: Level 2",
  "supporting_evidence": ["CDC Fever Guidelines"],
  "outdated_sources": [],
  "knowledge_warnings": [],
  "pass_votes": ["Level 2", "Level 2", "Level 3", "Level 2", "Level 2"]
}
```

#### POST /counterfactual

```json
{ "symptoms": "fever 39C headache stiff neck", "remove_symptom": "stiff neck" }
```

Response:

```json
{
  "original_level": "Level 2 — Emergency",
  "counterfactual_level": "Level 3 — Urgent",
  "removed_symptom": "stiff neck",
  "reasoning": "Without 'stiff neck' the classification dropped from Emergency to Urgent — this symptom was critical to the decision."
}
```

#### GET /health

```json
{ "status": "healthy", "service": "Medical Edge Triage" }
```

#### GET /metrics

```json
{
  "embedding_model": "nomic-embed-text",
  "reasoning_model": "qwen2.5:3b",
  "vector_db": "lancedb"
}
```

### Direct Python Test

```python
from src.orchestrator import run_triage
result = run_triage("fever 39C headache stiff neck")
print(result.triage_level, result.confidence)
```

## Algorithms Used

| Component | Algorithm |
|-----------|-----------|
| **Embedding** | `nomic-embed-text` — 768-dim BERT-based contrastive embedding (Matryoshka Representation Learning) |
| **Vector Search** | LanceDB — Approximate Nearest Neighbor (IVF + Product Quantization) |
| **Reranking** | Term-overlap scoring: `|query_terms ∩ chunk_terms| / |query_terms|` |
| **Temporal Filtering** | Threshold: `current_date − source_date > 24 months → flag` |
| **LLM Reasoning** | Qwen 2.5 3B — Transformer decoder, Grouped-Query Attention |
| **Uncertainty** | Variance: `1 − np.var(numeric_levels) / 4.0` |
| **Multi-pass Sampling** | Random subset + shuffle from top-k chunks (stratified per pass) |
| **Counterfactual** | Ablation: remove token → re-run full pipeline → compare |

## Project Structure

```
├── src/
│   ├── config.py                 # All configuration
│   ├── models.py                 # Data classes
│   ├── temporal.py               # Knowledge age filtering
│   ├── orchestrator.py           # Wires all stages
│   ├── ingestion/
│   │   ├── loader.py             # Chunking + file loaders
│   │   ├── embedder.py           # Ollama embeddings
│   │   ├── metadata_tagger.py    # Source provenance
│   │   └── pipeline.py           # Ingest runner
│   ├── retrieval/
│   │   ├── retriever.py          # LanceDB search
│   │   └── reranker.py           # Term-match rerank
│   ├── reasoning/
│   │   ├── inference.py          # LLM prompt + parse
│   │   ├── uncertainty.py        # Multi-pass + variance
│   │   └── counterfactual.py     # Ablation analysis
│   ├── api/
│   │   └── app.py                # FastAPI routes
│   └── ui/
│       └── app.py                # Streamlit frontend
├── scripts/
│   └── download_data.py          # Generates sample data
├── run.sh                        # Single command: Ollama + model + Streamlit
├── run_api.py                    # Start FastAPI server
├── run_ui.py                     # Start Streamlit
├── run_ingest.py                 # Ingest documents
├── data/
│   ├── sample_triage.json        # Sample test cases
│   └── triage_guidelines.md      # Clinical guidelines
├── requirements.txt
└── pyproject.toml
```

## Models

| Model | Size | Purpose |
|-------|------|---------|
| `nomic-embed-text` | 274 MB | Text → 768-dim embeddings for vector search |
| `qwen2.5:3b` | 1.7 GB | Clinical reasoning, structured JSON output |
