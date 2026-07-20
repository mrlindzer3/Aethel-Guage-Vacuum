#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/mrlindzer3/Aethel-Guage-Vacuum.git"
CLONE_DIR="Aethel-Guage-Vacuum"
BRANCH="ci/add-pytest-workflow"
VENV_DIR=".venv"
PYTHON="${PYTHON:-python3}"
GH_CREATE_PR=${GH_CREATE_PR:-1}   # set to 0 to skip creating the PR with gh

echo "1) Ensure git, $PYTHON, and pip are installed..."
command -v git >/dev/null || { echo "git not found"; exit 1; }
command -v "$PYTHON" >/dev/null || { echo "$PYTHON not found"; exit 1; }

echo "2) Clone repository (if needed)"
if [ -d "$CLONE_DIR" ]; then
  echo "Directory $CLONE_DIR already exists — using it"
  cd "$CLONE_DIR"
  git fetch origin
else
  git clone "$REPO_URL" "$CLONE_DIR"
  cd "$CLONE_DIR"
fi

echo "3) Check out branch $BRANCH"
# Try to check it out; if it doesn't exist locally, attempt to fetch remote branch
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git checkout "$BRANCH"
else
  if git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; then
    git checkout -b "$BRANCH" "origin/$BRANCH"
  else
    echo "Remote branch $BRANCH not found. Creating new branch from default branch..."
    DEFAULT_BRANCH=$(git remote show origin | awk '/HEAD branch/ {print $NF}')
    git checkout "$DEFAULT_BRANCH"
    git pull origin "$DEFAULT_BRANCH"
    git checkout -b "$BRANCH"
  fi
fi

echo "4) Create and activate virtualenv at $VENV_DIR"
"$PYTHON" -m venv "$VENV_DIR"
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

echo "5) Upgrade pip and install dev deps"
python -m pip install --upgrade pip setuptools wheel
if [ -f requirements-dev.txt ]; then
  python -m pip install -r requirements-dev.txt
else
  python -m pip install pytest numpy
fi

echo "6) Run pytest (smoke tests)"
export PYTHONPATH=.
python -m pytest -q

echo "7) Run performance check (10 cycles, threshold 5.0 ms)"
python tests/performance_check.py --cycles 10 --threshold 5.0

echo "Performance check passed (or script exited non-zero before this line if it failed)."

if [ "${GH_CREATE_PR}" -eq 1 ]; then
  if command -v gh >/dev/null 2>&1; then
    echo "8) Creating PR with gh (if it doesn't already exist)"
    gh pr view --json number --jq '.number' --head "ci/add-pytest-workflow" >/dev/null 2>&1 || \
      gh pr create --base main --head ci/add-pytest-workflow --title "feat(tests): add lightweight pytest smoke test and CI workflow" --body "Make run_performance_benchmark test-friendly (returns timings).\n\nAdd deterministic pytest with stubs, a performance check script, a GitHub Actions workflow to run tests and a performance job, requirements-dev.txt, and CONTRIBUTING.md."
    echo "PR created or already exists. Open the compare page in your browser if you want to review before merging:"
    echo "https://github.com/mrlindzer3/Aethel-Guage-Vacuum/compare/main...ci/add-pytest-workflow?expand=1"
  else
    echo "gh CLI not installed. To create the PR manually, open:"
    echo "https://github.com/mrlindzer3/Aethel-Guage-Vacuum/compare/main...ci/add-pytest-workflow?expand=1"
  fi
fi

echo "All done."
