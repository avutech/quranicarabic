# Practice Tests & Master Exam (started 2026-10-17)

Owner decisions: EN + TR content (Arabic UI later) · 100–200 questions per chapter ·
hint costs 25% of a point, retry earns 50% · "report this question" button for students
only (no scholar queue) · Master Exam is never locked.

| Test | Count | Length | Pool |
|---|---|---|---|
| Chapter practice test | 42 | 20 | 100–200 per chapter, balanced across the chapter's topics |
| Level exam | 3 | 20 | drawn from the 14 chapter pools of that level |
| Master Exam (all 3 levels) | 1 | 50 | own pool, 400–600 integrative questions |

Report after every test: strongest/weakest topics, link to the lecture section, 10-question drill, level summary, history.
Every question: MCQ (4 options), real ayah (snapped to the local Uthmani text), explanation for every option.
Generated in-session by subagents (no paid API). Data: `portal/testbank/<L#W#>.json`.

- [x] Phase 0: schema + `portal/testbank_tool.py` (validate / snap ayah text / coverage report); authoring rules in `tasks/testbank_brief.md`
- [x] Phase 1: pilot chapter L1W1 accepted after 11 independent review rounds (blocking findings per round: 26, 34, 26+, 15, 15, ~10, 5, 3, 2, 4, 0; no wrong answer keys in any round). Lessons are in `tasks/testbank_brief.md` (rules 1-20) and `tasks/testbank_pipeline.md`.
- [x] Phase 2 (done, 13 tests: `portal/test_tests_api.py`): backend: balanced sampler, server-side grading (answers never sent to the browser), results + per-topic history tables, question reports
- [x] Phase 3 (done; browser-tested with Playwright against a throwaway DB): frontend (`portal/tests.js` + hooks in index.html/data.js): Tests entries, test runner (hint, retry, per-option explanations), report page, drills
- [~] Phase 4 (workflow wf_e88a1ae3-94d running): generate remaining 41 chapter pools (one agent per topic batch), validate each
- [ ] Phase 5: level exams (sampler only) + Master Exam pool
- [ ] Phase 6: verify (pool validation, sampling balance over 1000 draws, UI end to end)

---

# I'rab Library — replace AI i'rab with classical books

## Mapping-only audit — authorized 2026-10-10

Owner scope: all books, Arabic i‘rab, Turkish/English readings and ayah meanings.
All content remains frozen; only associations may be proposed for correction.

- [x] Verify read-only staging access and translation record completeness.
- [x] Census all 51,211 entries / 43,652 meaning cells; preserve content hashes.
- [x] Compare all 14 books with original local extracted mappings/text: no differences.
- [x] Run fresh deterministic checks without overwriting historical reports.
- [x] Check meaning-cache extraction and independent Arabic verse numbering.
- [x] Build mapping-only queue, blind case packets, evidence-backed voting and escalation framework.
- [x] Independently revisit all 20 previously reported misplaced entries.
- [x] Escalate two ambiguous cases to a separately configured stronger model; obtain primary-source evidence.
- [ ] Complete first full semantic mapping review of every book entry and every meaning cell.
- [ ] Obtain independent second review and resolve competing target associations.
- [ ] Verify any approved association overlay preserves every text and provenance record.
- [ ] Resolve local merged-vs-parts differences and verify actual staging display after any authorized deployment.

Progress and continuation: `tasks/HANDOVER_CLAUDE.md`, `tasks/MAPPING_AUDIT_FRAMEWORK.md`,
`irab_library/mapping_audit/summary.json` and per-review JSONL artifacts. Automated
coverage is complete; exhaustive semantic certification remains open.

Goal: for any ayah, show every book in `Irab Kitaplari/` that comments on it
(title + author + traceable source), with the book's i'rab text, plus a Turkish
reading for students. AI i'rab removed. Celâleyn tafsir shown as its own line.

## Status (2026-10-03)

### Phase 1: index + UI ✅
- [x] Built per-ayah index (`portal/build_irab_library.py` → `irab_library/`)
- [x] `/api/irab-library/books`, `/api/irab-library/<s>/<a>` (login only)
- [x] Library UI: pick ayah → tafsir line + i'rab books, each with a citation
- [x] Removed `/api/irab`, `/api/irab-compare`, the compare views and the Gemini curriculum cache
- [x] Self Check turned off by default (admin toggle turns it back on)
- [x] **Security:** static route allowlist (it was leaking `.env` and `users.db`). Fix is on `production-fix`; **owner must push**

### Phase 2: books (all digital text, no OCR needed)
| Book | Source | Status |
|---|---|---|
| Ferrâ, Ahfeş, Zeccâc, Nahhâs ×2, Semîn | tafsir.app (given JSON) | ✅ indexed |
| Celâleyn (tafsir) | local .docx, 114 files | ✅ indexed |
| Derviş | tafsir.app | ✅ indexed |
| Sâfî, el-Cedvel | tafsir.app | ✅ indexed |
| Ukberî, et-Tibyân | shamela.ws/book/22928 | ✅ indexed (with print pages) |
| Mekkî, Müşkil | shamela.ws/book/5538 | ✅ indexed (with print pages) |
| Da'âs et al. | tafsir.app | ✅ indexed |
| el-Harrât, el-Müctebâ | tafsir.app | ✅ indexed |
| el-İ'râbu'l-Müyesser | tafsir.app | ✅ indexed; author not confirmed (local PDF says محمد الطيب الإبراهيم) |

Provenance: every entry carries `ref` (site, code, file, URL; page numbers where they exist).

### Phase 3: Turkish readings (agents, glossary `irab_library/glossary_tr.md`)
- [x] Wave 1: Fatiha (6 books) + Juz 'Amma (Ferrâ, Ahfeş, Zeccâc, Nahhâs): 1142 entries
- [x] Wave 2: Derviş + Celâleyn, Fatiha + Juz 'Amma: 619 entries
- [x] Wave 3: Semîn, Juz 'Amma: 337 entries
- [x] Wave 4: el-Cedvel + Ukberî + Mekkî, Fatiha + Juz 'Amma: 453 entries
- [x] Wave 5: Da'âs, Fatiha + Juz 'Amma: 435 entries
- [x] Wave 6: el-Harrât + el-Müyesser, Fatiha + Juz 'Amma: 1038 entries
- [ ] Teacher review: `irab_library/tr_review_wave*.md`, then set `reviewed: true`
- [ ] Next scope after Juz 'Amma: to be decided by the owner

## Owner actions pending
1. `git push origin production-fix:production` (security fix)
2. `git push origin staging-ready:staging`
3. Rotate the keys in `portal/.env`; ask users to change their passwords
4. On staging, enable the `irab` module if it is hidden

## Review (2026-10-03)
- Integrity check:
  - 51,211 entries, all with a source `ref`.
  - 4,024 Turkish readings, all matching an existing source entry by sha1.
  - Rendering 112:1 shows 13 books with citations and Turkish tabs.
  - Anonymous access is 401; `.env` and `users.db` return 404.
- Not verified in a real browser on staging. That needs the owner to push.
- Repo is 183 MB after the index rebuilds; the largest file is 8.9 MB.

## Overnight run 2026-10-03/04: morning summary

**On staging (staging.learnirab.com → İ'rab Kütüphanesi):**
- New layout:
  - ayah header with selectable Turkish meal (Diyanet default, plus Elmalılı and three others)
  - word-by-word grid, one box per word in ayah order: Arabic, transliteration, Turkish, English, grammar (Arabic + Turkish), root
  - book cards with line-by-line text, previous/next source, A−/A+, copy (always includes the citation) and "Kaynak hakkında"
- Turkish word meanings for **all 77,429 words** (machine translation, each with its source word and sha1).
- **Da'âs i'rab fully in Turkish** (3,639 entries); review list in `irab_library/tr_review_wave7.md`.
- Sources:
  - grammar and roots: Quranic Arabic Corpus v0.4, the original unmodified file (GPL notice in `irab_library/w/`)
  - words and meals: quran.com
  - Quran text: Tanzil
  - all credited on the page.

**Complete in Turkish for the whole Quran** (each reading verified against the sha1 of its source):
- Da'âs
- el-Müyesser
- Celâleyn
- el-Harrât
- el-Cedvel (Sâfî)
- Derviş
- all 77,429 word meanings

That is 28,428 Turkish book readings on staging. Review lists: `tr_review_wave7.md` … `tr_review_wave10.md`.

**Not started:** the classical commentaries for surahs 2–77. They are done only for Fatiha and Juz 'Amma.
- **Books:** Ferrâ, Ahfeş, Zeccâc, Nahhâs ×2, Mekkî, Ukberî, Semîn.
- **Size:** about 18M Arabic characters, roughly 270 agent packages. Semîn alone is about 7M.
- **Your decision:** whether and which.

**Biggest recurring review decision:** a policy for short bracketed completions and translator notes (see waves 7–10). One decision covers every book.

**Decisions for you:**
1. Review lists `irab_library/tr_review_wave1.md` … `wave7.md`. The main open policies:
   - how entries open («sözü» / «kavli»)
   - translator-note policy
   - term unification (lafza-i celâl / lafzatullah, nâfiye / nefy harfi)
2. Promote staging to production when you're happy.
3. el-Cedvel and Derviş for surahs 2–77 are very large (about 90 agent packages each). Do them next?
4. kuranmeali.com: not scraped (no API or licence). Ask the owner for permission if you want their word meanings.
5. Gemini appeal: AI feedback stays down until Google reinstates the project.
