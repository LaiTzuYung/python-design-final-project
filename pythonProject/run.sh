#!/bin/bash
# Launch Wordle Helper (UI.py)
# Usage: ./run.sh
set -e

cd "$(dirname "$0")"

find_python() {
    for cmd in python3 python; do
        if command -v "$cmd" >/dev/null 2>&1 && "$cmd" --version >/dev/null 2>&1; then
            echo "$cmd"
            return 0
        fi
    done
    return 1
}

PYTHON=$(find_python) || { echo "Python not found in PATH"; exit 1; }

"$PYTHON" -m pip install -q -r requirements.txt
"$PYTHON" UI.py