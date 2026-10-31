# Monitoring the question-bank pipeline without Claude

The two runner loops are ordinary background processes. They keep working when a Claude session is out of limit.
Run everything from the project folder:

```bash
cd "/Users/ahmedugur/Documents/Claude/Projects/Quran Arabic"
```

## Check progress

```bash
# Where every chapter stands (accepted / needs-fix / needs-review ...)
python3 portal/testbank_status.py

# What the runner will do next, and which chapters are locked (in progress)
python3 portal/pipeline_runner.py plan

# Weekly usage of Claude and Codex, and whether each is usable or paused (85% cap)
python3 portal/pipeline_runner.py usage

# Live feed of both loops (Ctrl-C to stop watching)
tail -f tasks/runner.log tasks/runner_codex.log

# Are the loops alive?
ps aux | grep "pipeline_runner.py loop" | grep -v grep
```

Reading the log:
* `running with codex` = a job started
* `review N by codex: written` = a review finished
* `-> L2W7: adjudicate` = the next step chosen
* `all providers paused` = both are limited or at 85% weekly; it resumes by itself after the reset

## If the loops died (reboot, closed terminal)

The watchdog that restarts them is a Claude session cron, so it does not run while Claude is out of limit. Restart by hand:

```bash
cd portal
# Claude-first loop on all chapters
nohup python3 pipeline_runner.py loop --provider auto --jobs 8 >> ../tasks/runner.log 2>&1 &
# Codex-only loop (list the chapters you want it to take, comma separated)
nohup python3 pipeline_runner.py loop --provider codex --jobs 6 --chapters L2W1,L2W2,L3W1,MASTER-L1 >> ../tasks/runner_codex.log 2>&1 &
```

Per-chapter locks in `portal/testbank/.locks` stop the two loops from working on the same chapter.

## Publish accepted chapters to STAGING

```bash
python3 portal/testbank_publish.py
```

It pushes only accepted banks to origin/staging (via local branch `staging-tests`). Never production or main.

## Keep the Mac awake

Plug in the charger and keep the lid open. If the keep-awake stopped: `caffeinate -dimsu -t 172800 &`.

## Rules

* Staging only; production only when the owner says so.
* No paid API calls.
* A chapter is accepted only after a fresh independent review (or adjudication) has no real blocking findings.
* Do not edit `portal/testbank/<chapter>.json` by hand; it is generated from `portal/testbank/parts/`.

More detail: `tasks/ORCHESTRATOR.md`, `tasks/testbank_pipeline.md`.
