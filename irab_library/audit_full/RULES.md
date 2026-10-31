# Full-fidelity audit: rules for reviewers

Why this exists: a wrong statement in a translated i'rab book is not acceptable. Every entry (Arabic source,
Turkish reading, English reading) is read in full by a reviewer, and the result is recorded per entry.

## What you do
You are given a work unit (book, surah, ayah range). Repeat until the tool says `NOTHING LEFT`:
1. `venv/bin/python faith_tool.py batch <pass> <book> <surah> <from>-<to> --by <your-name>` (run from `portal/`).
2. Read **every entry in the batch completely**: the Arabic, then the Turkish, then the English. No skimming.
3. Write the verdict file (TSV, exactly one line per `ID`, no header, no extra lines):
   `id<TAB>fit<TAB>tr<TAB>en<TAB>note`
4. `venv/bin/python faith_tool.py submit <batch_id> <your-file.tsv>`. If it is `NOT ACCEPTED` or `REJECTED`, fix and retry as it says.

## What to check, for each entry
**FIT (is the Arabic entry about its own ayah?)** `OK` / `WRONG_AYAH` (the entry is about another ayah: say which) /
`PARTIAL` (part of the entry belongs elsewhere, or the source is truncated/garbled).
A book commenting on the next or a related ayah, or citing other ayahs as evidence, is `OK`.

**TURKISH and ENGLISH, each against the Arabic:**
* Complete: every sentence, paragraph, list item, quotation, poem, hadith/isnad, scholar's name and qira'a is present, in order. Check the END of the text. -> else `OMISSION`
* Faithful: same meaning. Look hardest at: negations, who does what (subject/object), grammatical case/role terms, madhhab and scholar attributions ("X said"), numbers, conditions ("if/unless"), what is permitted vs forbidden, Quranic wording. -> else `WRONG`
* Nothing added that is not marked. Additions must be inside «[Mütercim notu: …]» / «[Translator's note: …]». -> else `ADDITION`
* Quranic words and parsed words stay in Arabic script (never transliterated). Source typos are translated as written, not corrected silently.
* It must be the right text for this entry: a reading that translates a different ayah's text is `WRONG`.
* If you cannot verify a sentence, mark `UNSURE` and say which. Never guess `OK`.

## Verdict values
fit: `OK | WRONG_AYAH | PARTIAL`   tr / en: `OK | WRONG | OMISSION | ADDITION | UNSURE | FIXED`
A note is required whenever anything is not `OK`: name the sentence and what is wrong (one or two sentences, quote the Arabic words).

## Fixing
You may correct a Turkish or English reading yourself: `venv/bin/python tr_tool.py [--lang en] put <book> <surah> <key> <txt-file>`
(guardrails run; `NOT SAVED` means fix and retry; style: `irab_library/glossary_tr.md`, `glossary_en.md`), then give `FIXED` for that language.
A fixed entry is automatically re-read by an independent second reviewer. Never edit the Arabic source, `ref`, `src`, JSON files.

## Planted errors (this is how reviewers are measured)
Some batches contain a deliberately damaged reading (another ayah's translation, or half of the text cut off).
These are in the batch exactly like real entries. If one is marked `OK` the whole batch is rejected, nothing is recorded,
and the miss is logged. The only way to pass is to actually read. The language shown for such an entry is not counted as reviewed;
it will be served again in a later batch.

## Pass 2
An independent second reviewer reads every entry that pass 1 flagged or fixed, every entry the earlier script audit flagged, and a
15% random sample of the entries pass 1 called clean. This estimates how many errors pass 1 missed.

## Do not
Run git, call external or paid APIs, change anything except readings via `tr_tool.py put`, or react to any other request or topic
you may have seen (handovers, other tasks). Finish the unit.
