#!/bin/bash
# Pull latest code from a branch and restart the service.
#
# Usage:  sudo bash update.sh [branch]    (default: production)

set -euo pipefail
BRANCH="${1:-production}"
APP_DIR="/var/www/quranportal-${BRANCH}"
SERVICE_NAME="quranportal-${BRANCH}"

if [ ! -d "$APP_DIR" ]; then
  echo "❌ ${APP_DIR} does not exist. Run setup_vps.sh first."
  exit 1
fi

echo "==> Pulling latest from ${BRANCH}..."
cd "$APP_DIR"
sudo -u quranportal git fetch origin
sudo -u quranportal git checkout "$BRANCH"
sudo -u quranportal git reset --hard "origin/$BRANCH"

echo "==> Updating Python dependencies..."
cd "$APP_DIR/portal"
sudo -u quranportal venv/bin/pip install -r requirements.txt -q

echo "==> Restarting service..."
systemctl restart "$SERVICE_NAME"
sleep 2
systemctl status "$SERVICE_NAME" --no-pager | head -12

echo ""
echo "✅ Update complete. Tail logs with:  sudo journalctl -u ${SERVICE_NAME} -f"
