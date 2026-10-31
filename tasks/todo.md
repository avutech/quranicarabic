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
- [~] Phase 5: level exams (sampler only) + Master Exam pool (462 questions written; slice reviews in progress; cross-provider final audit planned, see testbank_pipeline.md 'Accuracy comes first')
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

## Scholar review section (admin) — plan, 2026-10-31
Goal: an admin-side screen where a scholar can go through every practice question (left: Level > Chapter tree; right: all questions of the selected chapter with the correct answer and every option's explanation), then per question mark **Approved** or leave **comments**. Comments are captured for us to act on; approved questions can later be shown to students as "scholar approved".

Design
- Storage (users.db, created by `init_tables`): `question_reviews(qid PK, status approved|none, content_hash, reviewer_id, updated_at)` and `question_comments(id, qid, user_id, body, content_hash, status open|resolved, created_at, resolved_at)`. `content_hash` = hash of the question as reviewed, so an approval/comment is flagged "question changed since" after we edit it (an approval never silently carries over to new text).
- API (`tests_api.py`, all admin only, `/api/tests/review/...`): `tree` (levels > chapters + Master, with counts total/approved/open comments), `chapter/<id>` (all questions with answers, explanations, status, comments), `<qid>/approve` + `<qid>/unapprove`, `<qid>/comment`, `comment/<id>/resolve`, `export` (CSV/JSON of all comments, used to drive the edits).
- UI (`portal/review.js`, new, hooked like tests.js): admin-only sidebar item "Question Review" (REFERENCE_TOPICS, like Content Manager) plus a button in the admin panel; two-pane layout (tree left with counts and filters: all / unreviewed / has open comments / approved; question cards right with an Approve toggle and a comment box + thread).
- Not in this step: editing question text from the screen, and the student-facing "scholar approved" badge (the status is stored so the badge is a small follow-up).
- Tests: extend `test_tests_api.py` (admin-only access, approve/unapprove, comment/resolve, stale-hash flag, export); browser check of the screen on a local server.
- Deploy: staging only, built in a separate git worktree from origin/staging (the main tree has another session's uncommitted edits). Nothing to production.

Open decision: who logs in as the scholar — an existing admin account (full admin powers) or a new limited "scholar" role that only sees this section.

### Scholar review section — result (2026-10-31)
- Built and pushed to staging (a25862b): `tests_api.py` review endpoints + tables, `portal/review.js`, admin-only "Scholar Question Review" item (data.js/index.html/server.py hooks). Scholar logs in with an admin account (owner's choice).
- Verified: 21 backend tests pass (6 new for review); browser run (Playwright) of the whole flow: tree, 100 cards for L1W1, approve, comment, filters, Master 462, CSV export, no JS errors.
- Next: collect the scholar's comments (Export open comments CSV), edit the banks, re-review; then show an "approved by scholar" mark to students (status already stored; approvals auto-void when a question's text changes).

---

# Word-by-word grammar roles (started 2026-10-31)

Call out mübteda / haber / hâl / şart / cevâb-ı şart on each word in the library's word-by-word grid.
Source decision (user): option 1 — extract from the classical books, **al-I'rāb al-Muyassar** (`muyesser-irab`) as primary, **Da'ās** (`daas-irab`) as cross-check. Treebank rejected (download is morphology only; GPL verbatim-copy terms; ~11k words annotated). No AI tagging, no paid API: deterministic rule-based extraction.

- [x] Extractor `portal/build_word_roles.py`: align each ﴿head﴾ of a Muyassar entry to the ayah's words (skeleton match), detect role terms in its line, write `irab_library/roles/sNNN.json` — per tag: role, word index, scope (word/clause), alt flag, source book + entry key + the quoted line (provenance rule)
- [x] Cross-check with Da'ās by the same method; mark each tag `both` / `single`; report agreement + unaligned lines
- [x] Server: merge roles into `/api/irab-library/<s>/<a>` response (`roles`)
- [x] Frontend: role chips on each word box (EN/TR/AR labels), tooltip with source line, source note in the words footer
- [ ] Verify on sample ayahs (2:146, 2:2, 2:255, 1:1-7, conditionals), push to staging, scholar-review sheet of low-agreement tags

**Result (2026-10-31, pushed to staging 5096e8a):** 98.3% of book lines align to ayah words. Published tags: mübteda 2,774 · haber 5,163 · hâl 1,989 · şart 1,443 · cevâb-ı şart 619 (about 25% confirmed by both books). Only high-confidence or two-book tags are published; bare "والجملة … خبر" lines (sentence start unknown) are withheld. Hand-checked samples (7 per role): mübteda/şart 7/7, haber/hâl ~6/7, cevâb-ı şart ~4/7 — cevap is the weak one.
- [ ] Verify (still open): scholar review sheet of a random 200 tags per role; widen coverage with a third book (Ṣāfī / Muyassar-style) if wanted

**Round 2 (2026-10-31, staging 3356336):** added Ṣāfī (`safi-cedvel`) and the corpus' COND/RSLT particle tags as sources; a fixed color per book (role dots, legend, book cards); `portal/pair_check.py` + `irab_library/roles/PAIRING.md` check mübteda→haber, şart→cevap, cevap→şart (window: this + next 3 ayahs) and contradictions (a word is never both subject and predicate / şart and cevap; ties show neither → `CONFLICTS.json`). A single-source cevap with no şart in the 3 ayahs before is dropped.

**Round 3 (2026-10-31, staging 6dd2fa0):** 397 tags contradicted by corpus grammar hidden (`irab_library/roles/HIDDEN.json`); sentence-level tags that two books anchor on neighbouring words merged (1,013); corpus wāw al-ḥāl as a hâl source (96% of 293 covered); Da'ās/Ṣāfī range-entry alignment fixed. Scholar workbook: `scholar_review/Word_Roles_Scholar_Review_2026-10-31.xlsx` (built by `portal/word_roles_review.py`) — awaiting scholar results; then set the publish rule per role × agreement tier.
- [ ] Open: far-apart book disagreements (3,844 cases; 300 in the sheet), 3+ roles on one word (see QUALITY_suspects.json), nominal-sentence structure tags (not decided)
