# Quranic Arabic Learning Portal

## Project overview
A multilingual (English / Turkish / Arabic) self-study portal for Quranic Arabic grammar. Users browse 42 lessons across 3 levels, open lesson PDFs, and answer practice questions with live AI feedback powered by Claude.

## Stack
- **Backend:** Python + Flask (`portal/server.py`), port 8081
- **Frontend:** Single-page HTML/CSS/JS (`portal/index.html`) — no framework
- **Data:** `portal/data.js` — all 42 lessons, titles in EN/TR/AR, 5 practice questions each
- **AI feedback:** Anthropic Claude API (`claude-sonnet-4-6`) via `/api/feedback` POST

## Running locally
```bash
cd portal
export ANTHROPIC_API_KEY=your_key_here
venv/bin/python server.py
# → http://localhost:8081
```

## Key files
| File | Purpose |
|------|---------|
| `portal/server.py` | Flask server — serves HTML, PDFs, and Claude API proxy |
| `portal/index.html` | Full frontend — sidebar, lesson view, practice flow |
| `portal/data.js` | All lesson data: 3 levels × 14 weeks, titles, questions |
| `portal/requirements.txt` | `flask>=3.0`, `anthropic>=0.97` |

## PDF materials
Lesson PDFs live in `Kuran-Kerim Arapcasi/` (ignored by git — local only, ~34 MB).
The server serves them via `/pdfs/<path>` from that folder.

## Environment variable
`ANTHROPIC_API_KEY` must be set in the shell before starting the server.
Without it, the server starts but AI feedback returns a 500 error.
