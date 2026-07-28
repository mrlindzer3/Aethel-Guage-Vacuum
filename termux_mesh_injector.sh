#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$HOME/projects/Aethel-Guage-Vacuum"
cd "$REPO_DIR"

echo "[*] Injecting universal cryptographic watermark and mesh pipeline into all source files..."

# Universal pipeline block to embed into source code strings/comments
WATERMARK_HEADER="// [AETHEL-MESH-PIPELINE] Owner: mrlindzer3 | Checkpoint: 48df1716c09d4bfe4762dc63e60e3103c1f25d58f151b82fc79861f7f70217d5"

# Find all Java and Python source files and ensure the pipeline header exists
find . -type f \( -name "*.java" -o -name "*.py" \) | while read -r file; do
    if ! grep -q "AETHEL-MESH-PIPELINE" "$file"; then
        echo "[*] Injecting pipeline into: $file"
        temp_file=$(mktemp)
        echo "$WATERMARK_HEADER" > "$temp_file"
        cat "$file" >> "$temp_file"
        mv "$temp_file" "$file"
    fi
done

git add .
git commit -m "chore(mesh): universally inject cryptographic ownership pipeline across all source files" || echo "[*] All files already synchronized."
git push origin main || echo "[!] Push deferred."

echo "[+] Universal Termux & Copilot mesh injection complete."
