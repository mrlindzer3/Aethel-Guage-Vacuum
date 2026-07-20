# Aethel Gauge Vacuum — Academy‑grade Solid‑State Isomorphic Quantum Optomechanics Laboratory

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mrlindzer3/Aethel-Guage-Vacuum/HEAD?labpath=notebooks/01-intro.ipynb) [![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://mrlindzer3.github.io/Aethel-Guage-Vacuum/)

This branch adds an academy‑grade scaffolding for a reproducible solid‑state, isomorphic, quantum optomechanics laboratory repository.

Goals
- Provide a deterministic, testable Python core library for lightweight simulations and experiment orchestration.
- Include reproducible experiment scripts and a small notebook demo.
- Provide documentation, a provenance ingestion script to convert perf JSON artifacts into machine‑readable theory records, and CI-friendly test harnesses.

Structure added in this branch
- core/solid_state_lab/ — Python package (stubs, typed docstrings, unit‑testable)
- experiments/ — runnable experiment scripts that emit archival JSON
- notebooks/ — illustrative Jupyter demo (placeholder)
- archive/theories/ — machine‑readable theory records (YAML)
- scripts/ingest_artifact.py — converts perf JSON -> archive/theories/*.yaml
- tests/ — unit test skeletons
- docs/LAB_MANUAL.md — lab manual and grading rubric
- THEORIES.md remains for human curation; archive/theories/ holds machine entries

Quickstart
1) Create a virtualenv and install requirements-dev.txt (if present).
2) Run unit tests: pytest -q
3) Run an example experiment to produce an artifact JSON: python experiments/run_example.py --emit-json archive/perf/example.json
4) Use scripts/ingest_artifact.py to convert artifact JSON into archive/theories/ example YAML record.

Next steps
- I can open a PR for this branch and prepare a detailed PR body, or modify the scaffolding (add higher‑fidelity physics, hardware drivers, CI integration) on request.
