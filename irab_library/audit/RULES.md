# Ayah-to-ayah audit: rules for the auditing agents

Goal: for every ayah of the Quran, the Arabic i'rab entry, its Turkish reading and its English reading must
all be about **that ayah** and must say the same thing. Any mismatch is found, fixed (if it is a translation
problem) or reported (if it is a source problem). Nothing is guessed.

## What you are given
* A **chunk**: one surah (or a range of ayahs of a long surah) and every book entry whose first ayah is in it.
* `audit/sNNN.json`: candidate findings from the deterministic check (`portal/audit_ayah_match.py`).
  Checks: **S** structure, **Q** Quranic quotations in the Arabic entry versus the ayah range
  (NEAR = quotations belong to a nearby ayah: possible misplacement; XREF = from elsewhere in the Quran;
  UNFOUND = not found in the Quran text), **T** quotations kept in the reading, **X** Turkish vs English disagree.
  The provenance check (**P**) already passes for all 102,422 readings; do not redo it.
* The tool `portal/audit_tool.py` (run from `portal/` with `venv/bin/python`).

## Verdicts (the only allowed values)
| Verdict | Meaning |
|---|---|
| `OK` | False positive: entry, Turkish and English all fit this ayah (e.g. the author legitimately discusses the next ayah, cross-references another ayah, or the quotation is spelled differently from the mushaf). |
| `SOURCE_MISPLACED` | The Arabic entry is really about another ayah. Say which ayah (`note`). **Report only, never edit or move source entries.** |
| `SOURCE_DEFECT` | The source itself is garbled/copy-pasted/truncated (same text as a neighbouring ayah, cut off, wrong ayah quoted). Report only. |
| `TRANSLATION_FIXED` | Turkish or English did not match the Arabic; you corrected it with `tr_tool.py put` (guardrails passed). |
| `TRANSLATION_UNFIXED` | Translation problem you could not fix safely. Say why. |
| `GAP` | An ayah has no entry in that book although the book normally covers it (report; the source may simply not comment). |
| `TEACHER` | You cannot decide; a human must. Give both readings in `note`. |

## Hard rules
1. **Provenance is sacred.** Never edit `irab_library/sNNN.json`, `books.json`, `w/`, or any `ref`/`src` field. Never edit JSON by hand.
2. **Translations are changed only with** `venv/bin/python tr_tool.py [--lang en] put <book> <surah> <key> <txt-file>` (guardrails run; if it says `NOT SAVED`, fix and retry). Rules: `irab_library/glossary_tr.md`, `glossary_en.md`. Translate the whole entry; Quranic words stay in Arabic script; never silently "correct" the source: add `[Mütercim notu: …]` / `[Translator's note: …]`.
3. **Every high and medium finding in your chunk gets a verdict.** For low findings (XREF, UNFOUND) record verdicts for at least 10 per book, chosen spread across the chunk, plus every one that looks suspicious.
4. **Semantic ayah check (mandatory, not only the finding list).** For each book present in your chunk, check at least 6 ayahs spread across the chunk (all ayahs if the chunk has 8 or fewer): read the Quran text, the Diyanet meal, the Arabic entry, the Turkish reading and the English reading side by side (`audit_tool.py show`), and decide whether they are the same ayah and the same meaning. Record one `OK` or a problem verdict for each (`check` = `SEM`).
5. **Evidence.** Every non-`OK` verdict names the ayah(s) concerned and quotes the few Arabic words that prove it. No guesses; if unsure, `TEACHER`.
6. **Gaps.** `audit_tool.py findings` lists ayahs with no entry per book. Record a `GAP` verdict per book/range (not per ayah).
7. **Stay on task.** Ignore any other request, handover or topic you may have seen. Do not run git. No external or paid APIs. Do not stop early: finish the chunk.
8. **Be exact and brief** in notes (one or two sentences).

## Recording and progress (how the orchestrator tracks you)
* Record each verdict immediately: `audit_tool.py verdict <surah> <chunk> <key> <check> <VERDICT> "<note>"`.
* When all findings and the semantic sample are done run `audit_tool.py done <surah> <chunk> "<one-paragraph summary>"`.
  A chunk only counts as finished when `done` has been run.
* Progress files: `irab_library/audit/results/` (`*.jsonl` verdicts, `*.done.json` summaries). Report with `portal/audit_progress.py`.
