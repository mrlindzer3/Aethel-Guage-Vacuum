#!/usr/bin/env bash
set -euo pipefail

echo "Installing pre-commit and hooks..."
python3 -m pip install --upgrade pip
pip install pre-commit
pre-commit install
pre-commit autoupdate || true

echo "Done. To run the hooks locally, run: pre-commit run --all-files"
