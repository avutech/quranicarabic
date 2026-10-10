# Handover: I'rab library translations (for ChatGPT or any other assistant)

Written 2026-10-10. Use this if Claude hits its usage limit again and you want to carry on elsewhere.
Everything below is in the git repo `avutech/quranicarabic`, folder `irab_library/` and `portal/`.

## 1. What this project is

A Quranic Arabic study portal (Flask, `portal/`). The AI i'rab feature was replaced by a **library of classical i'rab books**. For every ayah the portal shows each book (title, author) and its i'rab, with **Turkish and English translations** for students, plus a word-by-word grid and Turkish/English meals. Staging site: staging.learnirab.com (branch `staging`). Production is promoted only on the owner's decision.

## 2. Non-negotiable rules

1. **Never lose provenance.** Every entry keeps its source reference (`ref`). Every translation records the source book, surah, ayah range, the sha1 of the Arabic it was made from, who translated it and when. The tools do this for you. Never edit the JSON by hand.
2. **Translate the WHOLE entry.** No summarising. Quranic words and parsed words stay in Arabic script, never transliterated. Quotations `﴿…﴾` stay.
3. **Never correct the source silently.** Translate what is written and add `[Mütercim notu: …]` (Turkish) or `[Translator's note: …]` (English). Footnotes `[[…]]` become `[Dipnot: …]` / `[Note: …]`.
4. **Style guides are binding:** `irab_library/glossary_tr.md` and `irab_library/glossary_en.md`. Read them first.
5. **No paid APIs for bulk work** (owner's rule). Do not scrape kuranmeali.com. The Quranic Arabic Corpus data stays unaltered and credited.
6. Never push to production without the owner's say-so. Staging only.

## 3. Data layout (`irab_library/`)

| Path | What |
|---|---|
| `sNNN.json` | Source entries per surah: `{b: book id, s: first ayah, e: last ayah, t: Arabic text, ref: {...}}` |
| `books.json` | Book catalog (title, author, source), meals, word sources |
| `tr_parts/<book>/sNNN.json`, `en_parts/<book>/sNNN.json` | **The translations** (one file per book per surah). Key `book:s-e`. Each has `t`, `src{book,sure,ayet_bas,ayet_son,sha1}`, `by`, `at` |
| `tr/`, `en/` | Merged readings built from the `_parts` (rebuilt, do not edit) |
| `w/sNNN.json`, `words_tr/` | Word-by-word grid (done for the whole Quran, 77,429 Turkish word meanings) |
| `glossary_tr.md`, `glossary_en.md` | Style guides |
| `guardrails_report.json` | Latest audit |
| `tr_review_wave1.md` … `wave10.md` | Reviewer notes and open decisions for the teacher |

Book ids. **Classical:** `farraa`, `akhfash`, `zajjaj`, `nahhas-irab`, `nahhas-meani`, `mekki-muskil`, `ukberi-tibyan`, `semin-durr`. **Student books:** `daas-irab`, `muyesser-irab`, `celaleyn`, `harrat-mujtaba`, `safi-cedvel`, `dervis-irab`.

## 4. Status on 2026-10-10 (check with the script in section 6)

- **Done:** all 77,429 Turkish word meanings; Turkish for most books (farraa, akhfash, zajjaj, nahhas-irab, nahhas-meani, mekki-muskil, and the six student books); English for many books (including daas-irab, farraa, akhfash, zajjaj and others).
- **Remaining at the time of writing** (about 12,600 entries):
  - Turkish: `semin-durr` (about 4,250) and `ukberi-tibyan` (about 530)
  - English student books: `dervis-irab` (about 1,390) and `safi-cedvel` (about 1,990)
  - English classical: `semin-durr` (about 4,410)
- Claude had three workflows running for exactly these when this was written; they may have finished by the time you read this. Always re-check.
- After translation finishes: QA pass per book, guardrails audit, rebuild, commit, push to staging.

## 5. How to translate an entry (the tool does the bookkeeping)

Run from `portal/` (use `venv/bin/python`; add `--lang en` for English, omit for Turkish):

```bash
venv/bin/python tr_tool.py status                                  # overall progress
venv/bin/python tr_tool.py --lang en list semin-durr 2 1-50        # entries in a range; ✓ = already done
venv/bin/python tr_tool.py --lang en show semin-durr 2 <key>       # print the Arabic source of one entry
venv/bin/python tr_tool.py --lang en put  semin-durr 2 <key> my.txt   # save a translation (text file)
```

`put` runs the **guardrails** and refuses to save (prints `NOT SAVED`) when it finds an error:

- translation shorter than 0.45 × the Arabic (summarised or truncated)
- more than half of the `﴿…﴾` quotations missing in Arabic script
- Turkish inside an English reading, or English inside a Turkish one
- banned Turkish spellings: `müteallık`, `müteallikdir`, `mastar` (use `müteallik`, `mütealliktir`, `masdar`)

Warnings (short ratio, footnotes not carried over) are printed; fix them too. Work in mushaf order (surah 1 to 114, ayah order). `put` is safe to run in parallel (file locks, atomic writes).

Then: `venv/bin/python guardrails.py audit` (add `--lang tr|en`, `--book ID`) must report **0 errors and 0 provenance problems**.

### If your assistant has no shell access (chat only)

1. In a terminal, `show` an entry (or a few) and paste the Arabic into the chat together with the matching glossary file and the rules in section 2.
2. Save each answer to a `.txt` file and run `put`. Do not paste translations straight into JSON.
3. Keep batches small (a few entries at a time) so the model does not shorten them.

## 6. Check what is left (single command)

Save as `check_left.py` anywhere and run with `python3`:

```python
import json, hashlib
from pathlib import Path
LIB = Path("irab_library")  # run from the repo root
CLASSICAL = ["farraa","akhfash","zajjaj","nahhas-irab","nahhas-meani","mekki-muskil","ukberi-tibyan","semin-durr"]
STUDENT = ["daas-irab","muyesser-irab","celaleyn","harrat-mujtaba","safi-cedvel","dervis-irab"]
for lang, books in [("tr", CLASSICAL+STUDENT), ("en", CLASSICAL+STUDENT)]:
    left = {}
    for s in range(1, 115):
        cache = {}
        for e in json.loads((LIB/f"s{s:03d}.json").read_text("utf-8"))["entries"]:
            if e["b"] not in books: continue
            p = LIB/f"{lang}_parts"/e["b"]/f"s{s:03d}.json"
            if p not in cache: cache[p] = json.loads(p.read_text("utf-8")) if p.exists() else {}
            r = cache[p].get(f"{e['b']}:{e['s']}-{e['e']}")
            if not (r and r["src"]["sha1"] == hashlib.sha1(e["t"].encode()).hexdigest()):
                left[e["b"]] = left.get(e["b"], 0) + 1
    print(lang, left or "ALL DONE")
```

(Turkish for `daas-irab` and others may already be complete; the script shows only what is missing.)

## 7. Finish line (after all translations are in)

1. Per-book QA: coverage, length ratios, at least 12 entries per book spot-checked against the Arabic, scan for Latin transliteration of Quranic words, language leakage, unmarked additions. Write findings to a `tr_review_wave*.md`-style note for the teacher.
2. `guardrails.py audit` → 0 errors, 0 provenance problems.
3. Rebuild: `cd portal && venv/bin/python build_irab_library.py`.
4. Commit `irab_library/tr`, `tr_parts`, `en`, `en_parts` (and the review notes).
5. Push to **staging**: use the GitHub account `avutech` (`gh auth switch -u avutech`); the other account gets 403. Pushing `staging` auto-deploys via `.github/workflows/deploy.yml`.
6. Check staging in the browser: a surah, all three language tabs on a book card, blue Quranic text.

## 8. Open decisions for the owner (not for the assistant to decide)

- Glossary policies listed at the end of each `tr_review_wave*.md` file.
- Production promotion.
- Gemini Google Cloud project is suspended (appeal submitted); no Gemini work until resolved.
- Code cleanup awaiting approval: remove the ChatGPT extraction option and dead Claude code; add `login_required` to `/api/feedback-issue`.

## 9. Credentials

None are in this document or the repo. `ANTHROPIC_API_KEY` etc. live only in the server `.env`. Translation work needs no keys.
