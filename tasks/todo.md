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
| Da'âs et al. | tafsir.app | ⏳ downloading |
| el-Harrât, el-Müctebâ | tafsir.app | ⏳ downloading |
| el-İ'râbu'l-Müyesser | tafsir.app | ⏳ queued; author to be confirmed from the PDF |

Provenance: every entry carries `ref` (site, code, file, URL; page numbers where they exist).

### Phase 3: Turkish readings (agents, glossary `irab_library/glossary_tr.md`)
- [x] Wave 1: Fatiha (6 books) + Juz 'Amma (Ferrâ, Ahfeş, Zeccâc, Nahhâs): 1142 entries
- [x] Wave 2: Derviş + Celâleyn, Fatiha + Juz 'Amma: 619 entries
- [x] Wave 3: Semîn, Juz 'Amma: 337 entries
- [ ] Wave 4: el-Cedvel + Ukberî + Mekkî, Fatiha + Juz 'Amma (running)
- [ ] Wave 5: Da'âs + el-Harrât + el-Müyesser, Fatiha + Juz 'Amma (after download)
- [ ] Teacher review: `irab_library/tr_review_wave*.md`, then set `reviewed: true`
- [ ] Next scope after Juz 'Amma: to be decided by the owner

## Owner actions pending
1. `git push origin production-fix:production` (security fix)
2. `git push origin staging-ready:staging`
3. Rotate the keys in `portal/.env`; ask users to change their passwords
4. On staging, enable the `irab` module if it is hidden
