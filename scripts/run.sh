#!/usr/bin/env bash
# Example script
set -euo pipefail
. .venv/bin/activate
python -c 'print("Hello from $(basename "$PWD")")'
