#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <REGISTRATION_TOKEN> [OWNER] [REPO]"
  exit 1
fi

REG_TOKEN="$1"
OWNER="${2:-mrlindzer3}"
REPO="${3:-Aethel-Guage-Vacuum}"
RUNNER_USER="${RUNNER_USER:-actions-runner}"
RUNNER_HOME="/home/${RUNNER_USER}"
RUNNER_DIR="${RUNNER_HOME}/actions-runner"
ARCHIVE_URL="https://github.com/actions/runner/releases/latest/download/actions-runner-linux-x64.tar.gz"
LABELS="self-hosted,linux,cgroup"

echo "Using OWNER=${OWNER} REPO=${REPO} RUNNER_USER=${RUNNER_USER}"

# Create runner user if it doesn't exist
if ! id -u "${RUNNER_USER}" >/dev/null 2>&1; then
  echo "Creating user ${RUNNER_USER}..."
  useradd -m -s /bin/bash "${RUNNER_USER}"
fi

# Install packages
echo "Installing required packages..."
apt-get update -y
apt-get install -y curl tar git jq libicu-dev ca-certificates

# Prepare runner dir
mkdir -p "${RUNNER_DIR}"
chown "${RUNNER_USER}:${RUNNER_USER}" "${RUNNER_DIR}"

# Download and extract runner tarball
echo "Downloading runner..."
curl -fsSL "${ARCHIVE_URL}" -o /tmp/actions-runner.tar.gz
echo "Extracting to ${RUNNER_DIR}..."
tar -xzf /tmp/actions-runner.tar.gz -C "${RUNNER_DIR}"
chown -R "${RUNNER_USER}:${RUNNER_USER}" "${RUNNER_DIR}"
rm -f /tmp/actions-runner.tar.gz

# Configure the runner (run as runner user)
REPO_URL="https://github.com/${OWNER}/${REPO}"
echo "Configuring runner for ${REPO_URL} with labels ${LABELS}..."
sudo -u "${RUNNER_USER}" bash -c "cd ${RUNNER_DIR} && ./config.sh --url ${REPO_URL} --token ${REG_TOKEN} --labels \"${LABELS}\" --unattended --replace"

# Grant passwordless sudo to runner user (needed to modify /sys/fs/cgroup)
echo "Granting passwordless sudo for ${RUNNER_USER} (file: /etc/sudoers.d/${RUNNER_USER})..."
cat > /etc/sudoers.d/"${RUNNER_USER}" <<EOF
${RUNNER_USER} ALL=(ALL) NOPASSWD:ALL
EOF
chmod 440 /etc/sudoers.d/"${RUNNER_USER}"

# Install and start service
echo "Installing runner service..."
sudo -u "${RUNNER_USER}" bash -c "cd ${RUNNER_DIR} && ./svc.sh install"
sudo -u "${RUNNER_USER}" bash -c "cd ${RUNNER_DIR} && ./svc.sh start"

echo "Runner setup complete."
echo "Verify the runner appears in: https://github.com/${OWNER}/${REPO}/settings/actions/runners"
echo "If you need to remove the runner later, run as the runner user:"
echo "  cd ${RUNNER_DIR} && ./svc.sh stop && ./svc.sh uninstall && ./config.sh remove --token <REMOVE_TOKEN>"

# Post-install notes printed for operator
cat <<'NOTES'

Post-install verification:
- Check service status on VM:
  sudo -u ${RUNNER_USER} bash -c "cd ${RUNNER_DIR} && ./svc.sh status"
- Confirm GitHub shows the runner under repo Settings → Actions → Runners with labels: self-hosted, linux, cgroup
- Trigger the workflow via UI or:
  gh workflow run cgroup-throttle-smoke-test --repo ${OWNER}/${REPO}

Security notes:
- Run the runner on infrastructure you control (ephemeral VM recommended). The runner is powerful; a compromised workflow can run privileged commands.
- Use ephemeral VMs for smoke tests and destroy them after use.
- Limit who can modify workflows in the repository (branch protection / required reviews).
- If you prefer not to give NOPASSWD sudo to the runner user, run the runner as root (less recommended) or create narrowly scoped sudoers entries for only the commands needed (echo to /sys/fs/cgroup paths, service management).

Uninstall / cleanup:
# Stop & remove service (run as runner user)
# cd ${RUNNER_DIR}
# ./svc.sh stop
# ./svc.sh uninstall
# Remove registration (you may need to create a removal token via GitHub UI/gh API)
# Remove directory and sudoers
# rm -rf ${RUNNER_DIR}
# rm -f /etc/sudoers.d/${RUNNER_USER}
# userdel -r ${RUNNER_USER} || true

NOTES
