#!/usr/bin/env bash
set -euo pipefail

# Trigger CI workflow, wait for completion, and merge PR if CI succeeds.
# Prereqs: gh CLI authenticated, jq installed, network access to GitHub.

OWNER="mrlindzer3"
REPO="Aethel-Guage-Vacuum"
BRANCH="feat/cgroup-throttle-manager"
WORKFLOW_NAME="ci-lint"
POLL_INTERVAL=10
TIMEOUT_MIN=30
DOWNLOAD_LOGS=true

# Preconditions
if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install from https://cli.github.com/"
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "jq not found. Install via your package manager (apt/yum/brew)."
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "gh is not authenticated. Run 'gh auth login' first."
  exit 1
fi

echo "Triggering workflow ${WORKFLOW_NAME} on ${OWNER}/${REPO}@${BRANCH}..."
gh workflow run "${WORKFLOW_NAME}" --repo "${OWNER}/${REPO}" --ref "${BRANCH}"

echo "Waiting for a workflow run to appear..."
end=$((SECONDS + TIMEOUT_MIN*60))
RUN_ID=""
while [ $SECONDS -lt $end ]; do
  RUN_INFO=$(gh run list --repo "${OWNER}/${REPO}" --workflow "${WORKFLOW_NAME}" --branch "${BRANCH}" --limit 1 --json id,status,conclusion,createdAt,url --jq '.[0] // empty')
  if [ -n "$RUN_INFO" ]; then
    RUN_ID=$(echo "$RUN_INFO" | jq -r '.id')
    STATUS=$(echo "$RUN_INFO" | jq -r '.status')
    CONCLUSION=$(echo "$RUN_INFO" | jq -r '.conclusion')
    RUN_URL=$(echo "$RUN_INFO" | jq -r '.url')
    echo "Found run id: $RUN_ID (status=$STATUS, conclusion=$CONCLUSION) - $RUN_URL"
    break
  fi
  sleep 2
done

if [ -z "$RUN_ID" ]; then
  echo "Timed out waiting for a workflow run to be scheduled (timeout ${TIMEOUT_MIN}m)."
  exit 2
fi

echo "Polling run #$RUN_ID until completion (interval ${POLL_INTERVAL}s)..."
while [ $SECONDS -lt $end ]; do
  RUN_INFO=$(gh run view "$RUN_ID" --repo "${OWNER}/${REPO}" --json status,conclusion,url --jq '.')
  STATUS=$(echo "$RUN_INFO" | jq -r '.status')
  CONCLUSION=$(echo "$RUN_INFO" | jq -r '.conclusion')
  RUN_URL=$(echo "$RUN_INFO" | jq -r '.url')
  echo "$(date --iso-8601=seconds) status=$STATUS conclusion=$CONCLUSION"
  if [ "$STATUS" = "completed" ]; then
    break
  fi
  sleep "${POLL_INTERVAL}"
done

if [ "$STATUS" != "completed" ]; then
  echo "Run did not complete within timeout (${TIMEOUT_MIN}m). Current status: $STATUS"
  exit 3
fi

echo "Run completed with conclusion: $CONCLUSION"
if [ "$CONCLUSION" != "success" ]; then
  echo "Workflow failed or was cancelled. Run URL: $RUN_URL"
  if [ "$DOWNLOAD_LOGS" = true ]; then
    OUTDIR="./run-logs-${RUN_ID}"
    echo "Downloading logs to ${OUTDIR}..."
    gh run download "$RUN_ID" --repo "${OWNER}/${REPO}" --dir "${OUTDIR}"
    echo "Logs downloaded. Inspect ${OUTDIR} for step-level output."
  fi
  exit 4
fi

echo "Workflow succeeded. Finding PR for branch ${BRANCH}..."
PR_NUM=$(gh pr list --repo "${OWNER}/${REPO}" --head "${BRANCH}" --json number --jq '.[0].number')
if [ -z "$PR_NUM" ] || [ "$PR_NUM" = "null" ]; then
  echo "No open PR found for ${BRANCH}."
  exit 5
fi
echo "Found PR #$PR_NUM. Merging now..."

set +e
MERGE_OUTPUT=$(gh pr merge "$PR_NUM" --repo "${OWNER}/${REPO}" --merge --delete-branch 2>&1)
MERGE_EXIT=$?
set -e
if [ $MERGE_EXIT -ne 0 ]; then
  echo "Merge failed (exit $MERGE_EXIT). Output:"
  echo "$MERGE_OUTPUT"
  echo "If branch protection prevented merging, examine repo settings or run 'gh pr merge' manually."
  exit 6
fi

echo "Successfully merged PR #$PR_NUM and deleted branch."
exit 0
