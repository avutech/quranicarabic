#!/bin/bash
# One-time VPS setup for the Quranic Arabic Learning Portal.
# Run as root (or via sudo) on a fresh Ubuntu/Debian VPS.
#
# Usage:
#   sudo bash setup_vps.sh <domain> [<branch>]
#
# Example:
#   sudo bash setup_vps.sh quranportal.example.com production
#   sudo bash setup_vps.sh staging.quranportal.example.com staging

set -euo pipefail

DOMAIN="${1:-}"
BRANCH="${2:-production}"
REPO_URL="https://github.com/avutech/quranicarabic.git"
APP_DIR="/var/www/quranportal-${BRANCH}"
SERVICE_NAME="quranportal-${BRANCH}"
SERVICE_USER="quranportal"
PORT_BASE=8081
# pick a unique loopback port per branch (8081 main, 8082 staging, 8083 production, etc.)
case "$BRANCH" in
  main)        PORT=8081 ;;
  staging)     PORT=8082 ;;
  production)  PORT=8083 ;;
  *)           PORT=8090 ;;
esac

if [ -z "$DOMAIN" ]; then
  echo "Usage: sudo bash setup_vps.sh <domain> [<branch>]"
  echo "  branch defaults to 'production'"
  exit 1
fi

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root: sudo bash setup_vps.sh $DOMAIN $BRANCH"
  exit 1
fi

echo "==> Installing system packages (python, git, nginx, certbot, htpasswd)..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q python3 python3-venv python3-pip git nginx certbot python3-certbot-nginx apache2-utils

echo "==> Creating service user '${SERVICE_USER}' (if missing)..."
id -u "$SERVICE_USER" >/dev/null 2>&1 || useradd -r -m -s /bin/bash "$SERVICE_USER"

echo "==> Cloning/updating repo at ${APP_DIR} (branch ${BRANCH})..."
mkdir -p /var/www
# Tell git it's safe for root to operate on a quranportal-owned worktree
git config --global --add safe.directory "$APP_DIR" 2>/dev/null || true
if [ -d "$APP_DIR/.git" ]; then
  cd "$APP_DIR"
  git fetch origin
  git checkout "$BRANCH"
  git reset --hard "origin/$BRANCH"
else
  rm -rf "$APP_DIR"
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi
chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"

echo "==> Setting up Python venv..."
cd "$APP_DIR/portal"
sudo -u "$SERVICE_USER" python3 -m venv venv
sudo -u "$SERVICE_USER" venv/bin/pip install --upgrade pip --quiet
sudo -u "$SERVICE_USER" venv/bin/pip install -r requirements.txt gunicorn --quiet

echo "==> Creating .env template (if missing)..."
if [ ! -f "$APP_DIR/portal/.env" ]; then
  sudo -u "$SERVICE_USER" tee "$APP_DIR/portal/.env" >/dev/null <<EOF
# Edit me before starting the service!
GEMINI_API_KEY=your_gemini_key_here
GITHUB_TOKEN=your_github_pat_here
GITHUB_REPO=avutech/quranicarabic
GEMINI_MODEL=gemini-2.5-flash-lite
EOF
  chmod 600 "$APP_DIR/portal/.env"
  chown "$SERVICE_USER:$SERVICE_USER" "$APP_DIR/portal/.env"
  ENV_NEEDS_EDIT=1
fi

echo "==> Creating PDF directory placeholder..."
mkdir -p "$APP_DIR/Kuran-Kerim Arapcasi"
chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR/Kuran-Kerim Arapcasi"

# Normalize any macOS-style decomposed (NFD) filenames to composed (NFC).
# Browsers send composed UTF-8, so NFD names from rsync/tar-from-Mac would 404.
python3 - "$APP_DIR/Kuran-Kerim Arapcasi" <<'PYEOF'
import os, sys, unicodedata
root = sys.argv[1]
if os.path.isdir(root):
    fixed = 0
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for name in filenames + dirnames:
            nfc = unicodedata.normalize("NFC", name)
            if name != nfc:
                old, new = os.path.join(dirpath, name), os.path.join(dirpath, nfc)
                if not os.path.exists(new):
                    os.rename(old, new); fixed += 1
    if fixed: print(f"   normalized {fixed} filename(s) to NFC")
PYEOF

echo "==> Installing systemd service ${SERVICE_NAME}..."
cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=Quranic Arabic Learning Portal (${BRANCH})
After=network.target

[Service]
Type=simple
User=${SERVICE_USER}
Group=${SERVICE_USER}
WorkingDirectory=${APP_DIR}/portal
EnvironmentFile=${APP_DIR}/portal/.env
ExecStart=${APP_DIR}/portal/venv/bin/gunicorn --bind 127.0.0.1:${PORT} --workers 2 --timeout 120 server:app
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"

echo "==> Configuring nginx for ${DOMAIN}..."

# Staging gets HTTP Basic Auth (testers only); production is public.
HTPASSWD_FILE="/etc/nginx/htpasswd-${SERVICE_NAME}"
AUTH_BLOCK=""
GENERATED_CREDS=""
if [ "$BRANCH" = "staging" ]; then
  if [ ! -f "$HTPASSWD_FILE" ]; then
    GEN_USER="tester"
    GEN_PASS=$(openssl rand -base64 12 | tr -d '/+=' | head -c 14)
    htpasswd -bc "$HTPASSWD_FILE" "$GEN_USER" "$GEN_PASS" >/dev/null 2>&1
    chown root:www-data "$HTPASSWD_FILE"
    chmod 640 "$HTPASSWD_FILE"
    GENERATED_CREDS="user: ${GEN_USER}    password: ${GEN_PASS}"
  fi
  AUTH_BLOCK="
    auth_basic \"Quran Portal — staging (private)\";
    auth_basic_user_file ${HTPASSWD_FILE};
"
fi

cat > "/etc/nginx/sites-available/${SERVICE_NAME}" <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    client_max_body_size 10m;
    proxy_read_timeout 120s;

    location / {${AUTH_BLOCK}
        proxy_pass http://127.0.0.1:${PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
ln -sf "/etc/nginx/sites-available/${SERVICE_NAME}" "/etc/nginx/sites-enabled/${SERVICE_NAME}"
nginx -t
systemctl reload nginx

if [ -n "$GENERATED_CREDS" ]; then
  echo ""
  echo "🔑 Auto-generated test credentials (saved to ${HTPASSWD_FILE}):"
  echo "   ${GENERATED_CREDS}"
  echo ""
  echo "   Add or change users any time with:"
  echo "     bash ${APP_DIR}/deploy/manage_auth.sh add <username>"
  echo "     bash ${APP_DIR}/deploy/manage_auth.sh remove <username>"
  echo "     bash ${APP_DIR}/deploy/manage_auth.sh list"
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo " ✅  Setup complete for ${DOMAIN}  (branch: ${BRANCH}, port: ${PORT})"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "Next steps (in order):"
echo ""
echo "  1️⃣   Edit your API keys:"
echo "       sudo nano ${APP_DIR}/portal/.env"
echo ""
echo "  2️⃣   Upload the PDF lecture folder (~34 MB) from your Mac:"
echo "       From your Mac, run:"
echo "       rsync -av --progress ~/Documents/Claude/Projects/Quran\\ Arabic/Kuran-Kerim\\ Arapcasi/ \\"
echo "             root@<YOUR_VPS_IP>:${APP_DIR}/Kuran-Kerim\\ Arapcasi/"
echo ""
echo "  3️⃣   Start the service:"
echo "       sudo systemctl start ${SERVICE_NAME}"
echo "       sudo systemctl status ${SERVICE_NAME} --no-pager"
echo ""
echo "  4️⃣   Point DNS A record for ${DOMAIN} → this server's public IP"
echo "       (in your GoDaddy DNS console)"
echo ""
echo "  5️⃣   After DNS resolves, get HTTPS for free:"
echo "       sudo certbot --nginx -d ${DOMAIN} --redirect --agree-tos -m you@example.com"
echo ""
echo "  ℹ️   Logs:    sudo journalctl -u ${SERVICE_NAME} -f"
echo "  ℹ️   Updates: cd ${APP_DIR} && sudo bash deploy/update.sh ${BRANCH}"
echo ""
