# Translation agent structure and guardrails

## Roles

| Role | Count | Job |
|---|---|---|
| **Orchestrator** (main Claude session) | 1 | Splits each book into mushaf-order packages of about 66k Arabic characters; launches workflows; verifies coverage and sources independently; rebuilds, commits, deploys to staging. |
| **Translator agents** | 1 per package | Translate every entry in their ayah ranges, saving each one with `tr_tool.py put`. |
| **QA agent** | 1 per book per wave | Checks coverage, length ratios, a side-by-side sample against the Arabic, and terminology; fixes problems via `put`; writes the teacher's decision list. |
| **Guardrail monitor** | 1 (background) | Runs `guardrails.py audit` every 10 minutes and alerts the orchestrator on any error. |

## Guardrails (`portal/guardrails.py`)

### 1. At save time (`tr_tool.py put`)

Hard errors **block the save**; warnings are printed so the agent can fix them.

| Check | Effect |
|---|---|
| Empty translation | error |
| Shorter than 0.45 × the vowel-stripped Arabic | error (warning below 0.8) |
| Over half of the source's ﴿…﴾ quotations missing in Arabic script | error |
| Turkish inside an English reading, or English inside a Turkish one | error |
| Glossary spelling (müteallık, müteallikdir, mastar) | error |
| `[[…]]` footnotes not carried over | warning |

### 2. Provenance

Every save records the book, surah, ayah range, the sha1 of the Arabic, the translator and the date. The build hides any reading whose Arabic source has changed.

### 3. Audit

`venv/bin/python guardrails.py audit [--lang tr|en] [--book ID]` re-checks every saved reading, including provenance, and writes `irab_library/guardrails_report.json`.

### 4. Concurrency

`put` takes a file lock and writes atomically, so many agents can save to the same surah file safely.

## Style rules

- Turkish: `irab_library/glossary_tr.md`
- English: `irab_library/glossary_en.md`

## Waves running on 2026-10-04

- Turkish: the 8 classical books, surahs 2–77 (270 packages)
- English: the 6 student books, whole Quran (316 packages)
- English: the 8 classical books, whole Quran (282 packages)
