#!/usr/bin/env python3
"""Run a tiny deterministic example experiment and emit a JSON artifact.

Usage:
    python experiments/run_example.py --emit-json archive/perf/example.json --cycles 10 --seed 0
"""
import argparse
import json
import os
import time
import random


def run_experiment(cycles: int, seed: int):
    random.seed(seed)
    measurements = []
    for i in range(cycles):
        # deterministic pseudo-measurement
        measurements.append({
            "step": i,
            "value": round(random.random() + 0.1 * i, 6),
        })
    metrics = {
        "name": "example-experiment",
        "cycles": cycles,
        "seed": seed,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "measurements": measurements,
    }
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-json", required=True, help="Path to write JSON artifact")
    parser.add_argument("--cycles", type=int, default=10)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    out_path = args.emit_json
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    metrics = run_experiment(args.cycles, args.seed)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(out_path)


if __name__ == "__main__":
    main()
