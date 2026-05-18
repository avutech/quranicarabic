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

---

## Workflow Orchestration

### 1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately — don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First** — Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan** — Check in before starting implementation
3. **Track Progress** — Mark items complete as you go
4. **Explain Changes** — High-level summary at each step
5. **Document Results** — Add review section to `tasks/todo.md`
6. **Capture Lessons** — Update `tasks/lessons.md` after corrections

## Core Principles

- **Simplicity First** — Make every change as simple as possible. Impact minimal code.
- **No Laziness** — Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact** — Changes should only touch what's necessary. Avoid introducing bugs.
