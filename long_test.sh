#!/bin/bash
echo "=== Starting Extended Aethel-Gauge Stress & Continuity Test ==="
COUNTER=1
while true; do
    echo "[Cycle $COUNTER] Running matrix core simulation..."
    python src/aethel_gauge_matrix_core_0x9.py
    echo "[Cycle $COUNTER] Completed. Waiting 10 seconds before next cycle..."
    sleep 10
    COUNTER=$((COUNTER + 1))
done
