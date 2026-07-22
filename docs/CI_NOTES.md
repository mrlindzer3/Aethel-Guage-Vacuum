Guard pip install -e . in CI when the repository is not a Python package.

This change prevents the CI job from failing at the install step for repositories
that do not include a pyproject.toml or setup.py. It preserves installing
requirements-dev.txt when present.
