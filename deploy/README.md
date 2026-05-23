# Deployment

The portal runs on a single VPS (`137.184.56.77`) with two independent
environments, each its own git checkout + systemd service, fronted by Caddy
(ports 80/443, automatic SSL).

| Environment | URL | Branch | Folder | Service | Port |
|-------------|-----|--------|--------|---------|------|
| Production | https://www.learnirab.com | `production` | `/srv/quran` | `quran` | 8081 |
| Staging | https://staging.learnirab.com | `staging` | `/srv/quran-staging` | `quran-staging` | 8082 |

`main` is the dev/integration branch — it does **not** auto-deploy.

## How a deploy happens

A push to `staging` or `production` triggers `.github/workflows/deploy.yml`,
which SSHes into the VPS and runs `deploy/update.sh <branch>`. That script:

1. `git reset --hard origin/<branch>` in the env's folder
2. `pip install -r requirements.txt gunicorn` in `portal/`
3. `systemctl restart <service>`

`git reset --hard` only touches **tracked** files, so server-local gitignored
data — `.env`, `users.db`, `uploads/`, the PDF folder, `*_cache.json` — is
never altered.

## Promotion flow (merge up)

```bash
# develop on main
git push origin main

# promote to staging  -> auto-deploys staging.learnirab.com
git checkout staging && git merge main && git push origin staging

# promote to production -> auto-deploys www.learnirab.com
git checkout production && git merge staging && git push origin production

git checkout main
```

Manual deploy: GitHub → Actions → "Deploy to VPS" → Run workflow, or
`gh workflow run deploy.yml -f branch=staging`.

## CI configuration

GitHub Actions secrets (Settings → Secrets and variables → Actions):
`VPS_HOST`, `VPS_USER`, `VPS_PORT`, `VPS_SSH_KEY` (a dedicated deploy key with
root SSH to the VPS).

## One-time server bootstrap (already done)

Each env folder was made a git checkout with:

```bash
cd /srv/quran            # or /srv/quran-staging
git init -q
git remote add origin https://github.com/avutech/quranicarabic.git
git fetch origin -q
git checkout -f -B production origin/production   # or staging
```

Caddy config lives in `/etc/caddy/Caddyfile`; systemd units in
`/etc/systemd/system/quran*.service`. Logs: `journalctl -u quran -f`.
