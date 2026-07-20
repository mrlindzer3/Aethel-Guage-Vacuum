# Contributing

Thanks for wanting to contribute to Aethel-Guage-Vacuum. This document covers the basic steps to run tests and the benchmark locally and how to use the provided CI.

Running tests locally

1. Create a virtual environment (recommended):
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .\.venv\Scripts\activate   # Windows (PowerShell)

2. Install dev dependencies:
   python -m pip install -r requirements-dev.txt

3. Run the test suite from the repository root:
   PYTHONPATH=. python -m pytest -q

Running the benchmark locally

- Run the benchmark script directly (from repo root so imports resolve):
  PYTHONPATH=. python test_solid_state_fabric.py

- You can run a short deterministic run for development:
  PYTHONPATH=. python -c "from test_solid_state_fabric import run_performance_benchmark; print(run_performance_benchmark(cycles=3, return_timings=True))"

CI behavior

- The repository includes a GitHub Actions workflow that runs the lightweight pytest smoke test on push and pull requests across Python 3.11 and 3.10.
- A manual performance-check workflow is provided (workflow_dispatch). Use the Actions tab to run the "Performance check" workflow manually — it will execute a short benchmark and fail if the average frame time exceeds the configured threshold (default 5.0 ms).

Notes

- The smoke test stubs heavy core/ai/ui modules so CI runs fast and deterministically. The manual performance check is available for on-demand verification on GitHub-hosted runners; for reliable performance gating use dedicated hardware or self-hosted runners.

If you want me to add reviewers, a stricter performance gate, or a different CI matrix, open an issue or add a comment to the PR.
