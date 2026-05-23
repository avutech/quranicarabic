#!/usr/bin/env bash
# Server-side deploy: pull a branch and restart its service.
# Invoked by .github/workflows/deploy.yml over SSH. Arg: staging | production
#
# Safe by design: `git reset --hard` only touches TRACKED files, so the
# server's gitignored data (.env, users.db, uploads/, PDFs, *_cache.json)
# is never altered or deleted.
set -euo pipefail

BRANCH="${1:?usage: update.sh <staging|production>}"
case "$BRANCH" in
  production) DIR=/srv/quran;         SVC=quran ;;
  staging)    DIR=/srv/quran-staging; SVC=quran-staging ;;
  *) echo "unknown branch: $BRANCH" >&2; exit 1 ;;
esac

cd "$DIR"
git fetch --prune origin
git reset --hard "origin/$BRANCH"

cd "$DIR/portal"
venv/bin/pip install -q -r requirements.txt gunicorn
systemctl restart "$SVC"
echo "✓ deployed $BRANCH → $SVC ($(git -C "$DIR" rev-parse --short HEAD))"
