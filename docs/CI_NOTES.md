CI notes: reduced dependency resolution in ci-lint

To avoid environment/resolution conflicts (e.g., LibMambaUnsatisfiableError seen in some CI runs), the ci-lint workflow installs only the minimal developer/test tools (black, isort, flake8, pytest) via pip before optionally installing requirements-dev.txt. This reduces the chance of complex dependency graph resolution issues during workflow setup.

If your project requires a reproducible environment for tests that depends on a package build (pyproject.toml / setup.py), consider adding an optional matrix entry that runs a full install in a separate job rather than during every lint run.

Rerun trigger: GitHub Copilot Chat Assistant applied formatting and minimal-deps fixes and triggered a rerun on 2026-07-22T07:51:00Z.
