# Deploying to a VPS (GoDaddy / Linode / DigitalOcean / any Ubuntu/Debian)

This portal can run multiple environments side-by-side on the same VPS,
each tied to its own GitHub branch and its own subdomain:

| Branch | Subdomain (suggested) | Purpose |
|--------|------------------------|---------|
| `staging` | `staging.yourdomain.com` | Pre-production testing |
| `production` | `yourdomain.com` | Live, end-user-facing |

Each gets its own systemd service, its own loopback port, and its own
nginx server block. They don't conflict.

---

## Phase 1 — Prepare your VPS once

Log in to the VPS as root (or with `sudo`):

```bash
ssh root@<YOUR_VPS_IP>
```

Get the deploy scripts onto the server (just clone the repo temporarily):

```bash
cd /tmp
git clone https://github.com/avutech/quranicarabic.git
cd quranicarabic/deploy
```

---

## Phase 2 — Deploy the **staging** environment first

```bash
sudo bash setup_vps.sh staging.yourdomain.com staging
```

Replace `staging.yourdomain.com` with whatever subdomain you want.

The script will:
- Install Python, nginx, certbot
- Clone the `staging` branch into `/var/www/quranportal-staging`
- Create a `quranportal` system user
- Set up a venv and install dependencies + gunicorn
- Create a `.env` template (with placeholders for API keys)
- Install `quranportal-staging.service` (systemd, listens on port 8082)
- Configure nginx to proxy `staging.yourdomain.com` → `127.0.0.1:8082`

---

## Phase 3 — Fill in API keys + upload PDFs

**(a) API keys.** Edit the .env on the VPS:

```bash
sudo nano /var/www/quranportal-staging/portal/.env
```

Replace each `your_..._here` with your actual key:
- `GEMINI_API_KEY` — from https://aistudio.google.com/apikey
- `GITHUB_TOKEN` — from https://github.com/settings/personal-access-tokens (Issues + Contents write)

Save (Ctrl-O, Enter, Ctrl-X).

**(b) Lecture PDFs.** From your **Mac** (not the VPS):

```bash
rsync -av --progress \
  ~/Documents/Claude/Projects/Quran\ Arabic/Kuran-Kerim\ Arapcasi/ \
  root@<YOUR_VPS_IP>:/var/www/quranportal-staging/Kuran-Kerim\ Arapcasi/
```

This uploads the ~34 MB of lecture PDFs (one-time).

---

## Phase 4 — Start the service

Back on the VPS:

```bash
sudo systemctl start quranportal-staging
sudo systemctl status quranportal-staging
sudo journalctl -u quranportal-staging -f   # follow logs (Ctrl-C to exit)
```

---

## Phase 5 — Point DNS

In your **GoDaddy DNS console** for `yourdomain.com`:

1. Add an **A record**:
   - Host: `staging`
   - Value: `<YOUR_VPS_IP>`
   - TTL: 1 hour (default)

DNS propagation usually takes 5–15 minutes. Verify with:

```bash
dig staging.yourdomain.com +short
# should print your VPS IP
```

---

## Phase 6 — Enable HTTPS (free, via Let's Encrypt)

Once DNS resolves, run on the VPS:

```bash
sudo certbot --nginx -d staging.yourdomain.com --redirect --agree-tos -m you@example.com
```

Answer the prompts. certbot auto-edits nginx and sets up auto-renewal.

🎉 Visit **https://staging.yourdomain.com** — your portal is live.

---

## Day-to-day: pushing updates to staging

After you push new commits to the `staging` branch on GitHub:

```bash
ssh root@<YOUR_VPS_IP>
sudo bash /var/www/quranportal-staging/deploy/update.sh staging
```

That pulls latest code, refreshes Python deps, and restarts the service.

---

## Promoting staging → production

Once staging is solid, deploy production identically:

```bash
sudo bash setup_vps.sh yourdomain.com production
```

It runs in parallel on port 8083, separate from staging. Same edit-`.env`,
upload-PDFs, start-service, DNS, certbot dance for the apex domain.

To promote new code: merge `staging` → `production` on GitHub, then on the
VPS run `sudo bash /var/www/quranportal-production/deploy/update.sh production`.

---

## Useful commands cheat-sheet

```bash
# Status / logs
sudo systemctl status quranportal-staging
sudo journalctl -u quranportal-staging -f

# Restart after editing .env
sudo systemctl restart quranportal-staging

# Stop / start
sudo systemctl stop quranportal-staging
sudo systemctl start quranportal-staging

# Disable auto-start at boot
sudo systemctl disable quranportal-staging

# Reload nginx after manually editing config
sudo nginx -t && sudo systemctl reload nginx
```
