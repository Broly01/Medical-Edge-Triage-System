#!/usr/bin/env bash
set -e

echo "=== Medical Edge Triage ==="

if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "Starting Ollama..."
  nohup ollama serve > /tmp/ollama.log 2>&1 &
  sleep 3
fi

echo "Loading model (first load may take a few minutes)..."
curl -s http://localhost:11434/api/generate -d '{"model":"qwen2.5:3b","prompt":"hello","keep_alive":"30m"}' > /dev/null 2>&1 &

source .venv/bin/activate
echo "Starting Streamlit UI at http://localhost:8501"
streamlit run src/ui/app.py --server.port 8501
