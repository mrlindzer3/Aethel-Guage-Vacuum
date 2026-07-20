#!/usr/bin/env python3
"""Ingest a perf JSON artifact and emit a YAML theory record.

This is a minimal placeholder used in CI: read JSON and write a YAML file containing a summary and the raw artifact.
"""
import argparse
import json
import os
import time

try:
    import yaml
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False


def artifact_to_record(json_path: str, out_dir: str) -> str:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    base = os.path.basename(json_path)
    name = os.path.splitext(base)[0]
    record = {
        "id": name,
        "ingested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": {
            "name": data.get("name"),
            "cycles": data.get("cycles"),
            "seed": data.get("seed"),
        },
        "artifact": data,
    }
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{name}.yaml")
    if HAVE_YAML:
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(record, f, sort_keys=False)
    else:
        # fallback simple YAML-ish writer
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"id: {record['id']}\n")
            f.write(f"ingested_at: {record['ingested_at']}\n")
            f.write("summary:\n")
            for k, v in record["summary"].items():
                f.write(f"  {k}: {v}\n")
            f.write("artifact: |\n")
            json_blob = json.dumps(record["artifact"], indent=2)
            for line in json_blob.splitlines():
                f.write("  " + line + "\n")
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", help="Path to perf JSON artifact")
    parser.add_argument("--out-dir", default="archive/theories", help="Directory to write YAML records")
    args = parser.parse_args()

    out_path = artifact_to_record(args.artifact, args.out_dir)
    print(out_path)

if __name__ == "__main__":
    main()
