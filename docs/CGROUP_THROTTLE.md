# Cgroup throttle README

This repository contains tools to safely throttle processes using Linux cgroups.
The main utility is tools/cgroup_throttle.py (attached in this branch) and a
self-hosted smoke-test that verifies behavior on a host with cgroup access.

Quick summary
- tools/cgroup_throttle.py: attach existing PIDs or run commands under a cgroup with a target CPU percent
- .github/workflows/cgroup-throttle-smoke.yml: a smoke test that runs on a self-hosted runner with cgroup access
- scripts/setup-actions-runner-ubuntu.sh: unattended script to register a self-hosted runner with label "cgroup"
- scripts/setup-actions-runner-ubuntu.sh grants passwordless sudo to the runner user — run this only on an ephemeral VM you control

Running the smoke test (high level)
1. Provision a disposable Ubuntu VM you control.
2. Run scripts/setup-actions-runner-ubuntu.sh <REG_TOKEN> to register a runner with labels self-hosted,linux,cgroup.
3. In GitHub Actions -> Workflows -> cgroup-throttle-smoke-test -> Run workflow on branch feat/cgroup-throttle-manager.

Security checklist for reviewers / PR merging
- Ensure workflows that run on self-hosted privileged runners are only editable by trusted contributors.
- Prefer ephemeral VMs for privileged workflows; do not run this on shared infrastructure.
- Confirm smoke test runs on a runner with labels: self-hosted,linux,cgroup.
- Confirm the repo's branch protection and required review settings meet your org's policies before merging.

Local developer setup (lint/tests)
- Install dev deps (if present): python -m pip install -r requirements-dev.txt
- Install editable package: pip install -e .
- Run pre-commit hooks: scripts/install-precommit.sh
- Run tests: pytest

If you need a dockerized privileged runner example or narrower sudo scope for the runner user, open an issue or request it in this PR.
