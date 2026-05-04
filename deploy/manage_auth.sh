#!/bin/bash
# Manage HTTP Basic Auth users for the staging portal.
#
# Usage:
#   sudo bash manage_auth.sh add <username>      # prompts for password
#   sudo bash manage_auth.sh remove <username>
#   sudo bash manage_auth.sh list
#
# (Production is public — auth file isn't used there.)

set -euo pipefail

BRANCH="${BRANCH:-staging}"
HTPASSWD_FILE="/etc/nginx/htpasswd-quranportal-${BRANCH}"
ACTION="${1:-}"
USERNAME="${2:-}"

if [ "$EUID" -ne 0 ]; then
  echo "Run as root: sudo bash $0 ..."
  exit 1
fi

if [ ! -f "$HTPASSWD_FILE" ] && [ "$ACTION" != "add" ]; then
  echo "❌ No password file at $HTPASSWD_FILE yet. Add a user first:"
  echo "   sudo bash $0 add <username>"
  exit 1
fi

case "$ACTION" in
  add)
    [ -z "$USERNAME" ] && { echo "Usage: $0 add <username>"; exit 1; }
    if [ -f "$HTPASSWD_FILE" ]; then
      htpasswd "$HTPASSWD_FILE" "$USERNAME"
    else
      htpasswd -c "$HTPASSWD_FILE" "$USERNAME"
      chown root:www-data "$HTPASSWD_FILE"
      chmod 640 "$HTPASSWD_FILE"
    fi
    echo "✅ User '$USERNAME' added/updated."
    ;;

  remove)
    [ -z "$USERNAME" ] && { echo "Usage: $0 remove <username>"; exit 1; }
    htpasswd -D "$HTPASSWD_FILE" "$USERNAME"
    echo "✅ User '$USERNAME' removed."
    ;;

  list)
    echo "Users in $HTPASSWD_FILE:"
    cut -d: -f1 "$HTPASSWD_FILE" | sed 's/^/  - /'
    ;;

  *)
    echo "Usage: $0 {add|remove|list} [<username>]"
    exit 1
    ;;
esac
