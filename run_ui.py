#!/usr/bin/env python3
import subprocess
import sys

if __name__ == "__main__":
    cmd = ["streamlit", "run", "src/ui/app.py", "--server.port", "8501"]
    subprocess.run(cmd)
