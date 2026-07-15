#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Medical Edge Triage ==="

if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "Starting Ollama..."
  nohup ollama serve > /tmp/ollama.log 2>&1 &
  sleep 3
fi

echo "Loading model..."
curl -s http://localhost:11434/api/generate -d '{"model":"qwen2.5:3b","prompt":"hello","keep_alive":"30m"}' > /dev/null 2>&1 &

source "$SCRIPT_DIR/.venv/bin/activate"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

echo "Starting Streamlit UI at http://localhost:8501"
streamlit run "$SCRIPT_DIR/src/ui/app.py" --server.port 8501
