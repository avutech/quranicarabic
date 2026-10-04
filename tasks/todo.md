# I'rab Library — replace AI i'rab with classical books

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
