# Running the question-bank pipeline from the AI Orchestrator (Claude first, Codex fallback)

The pipeline (chapter pools + Master Exam pool, see `tasks/testbank_pipeline.md`, `tasks/master_blueprint.md`) has two engines.
Pick ONE engine per chapter at a time.

| Engine | How | Strength | Weakness |
|---|---|---|---|
| Claude `Workflow` tool | `tasks/testbank_workflow.js`, `tasks/master_workflow.js` (inside a Claude Code session; the watchdog restarts them) | fan-out of many agents with structured results | stalls when the Claude session/weekly usage limit is hit; needs the Claude Code session to stay open |
| **Runner** (this doc) | `python3 portal/pipeline_runner.py loop` — launched from the AI Orchestrator or a terminal | provider-neutral; runs each job with `claude -p` or `codex exec` and **switches provider when one reports a usage limit**; no session to keep open | fewer parallel agents; handles review/fix jobs (authoring stays with the Workflow engine) |

State always lives in files (`portal/testbank/…`), so any worker can pick up where another stopped:
`python3 portal/testbank_status.py` shows every chapter and Master slice (accepted / needs-review / needs-fix / needs-re-review / authoring).

## Add these tasks in the AI Orchestrator (Command Palette → "AI Orchestrator: Add Task")

**Task 1 — Pipeline loop (choose Claude or Codex as the launcher; the runner does the provider switching itself)**
```
In the repository root run:  python3 portal/pipeline_runner.py loop --provider auto --jobs 4
Leave it running until it prints "nothing left to run". Do not edit question files yourself.
If it exits early, run `python3 portal/pipeline_runner.py plan` and `python3 portal/testbank_status.py`, report what is blocked, and restart the loop.
Rules: staging only (never production), no paid APIs, never publish unreviewed banks, quality bar in tasks/testbank_pipeline.md.
```
*Variant — only some chapters (e.g. while the Workflow engine handles the rest):* add `--chapters L1W2,L1W3,MASTER-L1`.

**Task 2 — Publish accepted chapters to STAGING**
```
In the repository root run:  python3 portal/testbank_publish.py
It commits and pushes only newly accepted question banks to origin/staging (via the local branch staging-tests).
Never push to production or main. Report which chapters it published.
```

**Task 3 — Status report**
```
Run: python3 portal/testbank_status.py   and   python3 portal/pipeline_runner.py plan
Summarise: accepted count, chapters closest to acceptance (lowest blocking count), chapters with 8+ review rounds, anything stuck. Change nothing.
```

## Handoff notes (use "AI Orchestrator: Handoff Task" when switching worker)
```
Context: Quran Arabic portal, question banks. State is in portal/testbank/ (parts/, reviews/, designs/, <chapter>.json) — read it, don't trust memory.
Next step: run `python3 portal/pipeline_runner.py plan`, then `loop`.
Never: push to production/main; publish a bank whose chapter is not 'accepted'; edit testbank/<chapter>.json by hand (generated from parts/);
run two engines on the same chapter; use paid API keys.
A chapter is accepted only when a FRESH independent review has no blocking findings. A rewrite (fix) always needs a new fresh review.
```

## How the runner decides what to do
* `needs-review` / `needs-re-review` → **review job**: a fresh worker reviews `testbank/<chapter>.json` (or the Master slice) and writes `testbank/reviews/<name>_review<N>.txt`.
* `needs-fix` → **fix job**: a worker fixes every finding in the latest review by editing `testbank/parts/<chapter>/*.json`, validates, and runs `testbank_tool.py check`.
* `authoring` → not handled here (use the Workflow engine); `accepted` → nothing; 12+ review rounds → left for a human.
* Providers: `claude -p` (acceptEdits) first, `codex exec -s workspace-write` second. A usage-limit message pauses that provider for 45 minutes (`portal/testbank/runner_state.json`); a network error retries after 5 minutes. A chapter that fails 3 jobs in a row is skipped.
* `python3 portal/pipeline_runner.py selftest` proves both CLIs work (shell command + file write + reply).
* Codex binary: found in the VS Code ChatGPT extension (override with `CODEX_BIN`); Claude binary: `claude` (override with `CLAUDE_BIN`). Both must be signed in (`codex login status`).

## Weekly-usage throttle (owner, 2026-10-23)
* A provider is NOT used once its weekly usage is >= 85% (`WEEKLY_CAP` in `portal/pipeline_runner.py`); jobs go to the other provider. If both are at/above 85% every loop sleeps (checking every <= 30 min, without counting failed attempts) until the earlier weekly reset, then resumes by itself.
* Codex: exact percent and reset time via `codex app-server` (`account/rateLimits/read`). Claude: the CLI only emits a `seven_day` rate_limit_event near its limit, so no event = below the warning threshold; a non-allowed seven_day status counts as exhausted (resetsAt used as wake-up). Readings are cached 10 min in `testbank/runner_state.json`.
* `python3 portal/pipeline_runner.py usage` prints both readings and whether each provider is usable.
