# I'rab Library — replace AI i'rab with classical books

Goal: for any ayah, show every book in `Irab Kitaplari/` that comments on it
(title + author), with the book's i'rab text, plus a Turkish reading for students.
Remove the AI i'rab (`/api/irab`, `/api/irab-compare`, related UI).

## Inventory (2026-10-03)

### Ready — digital text, already split by ayah (tafsir.app JSON)
| code | book | author | coverage |
|---|---|---|---|
| iraab-alnahas | إعراب القرآن | en-Nahhâs (ö. 338) | 5109 / 6236 ayahs |
| aldur-almasoon | الدر المصون | es-Semîn el-Halebî (ö. 756) | 4596 |
| zajjaj | معاني القرآن وإعرابه | ez-Zeccâc (ö. 311) | 4054 |
| farraa | معاني القرآن | el-Ferrâ (ö. 207) | 2968 |
| nahaas-meanings | معاني القرآن | en-Nahhâs (ö. 338) | 2682 (47 surahs) |
| akhfash | معاني القرآن | el-Ahfeş (ö. 215) | 1210 |

Schema: `{kod, kitap, muellif, vefat, girdiler:[{sure, ayet_bas, ayet_son, metin}]}`

### Scanned PDFs — no text layer, need OCR + ayah segmentation (~16k pages)
| folder | pages | note |
|---|---|---|
| Al Cadwal Fi Irabi Kuran (Mahmûd Sâfî) | 6,488 (15 vols) | tabular layout |
| İ'râbu'l-Kur'ân ve Beyânuhu (Derviş) | 5,503 | |
| el-İ'râbu'l-Müyesser | 630 | |
| el-Müctebâ (el-Harrât) | 1,614 | |
| et-Tibyân fî İ'râbi'l-Kur'ân (Ukberî) | 1,379 | |
| Müşkilü İ'râbi'l-Kur'ân (Mekkî) | 1,104 | |
| İ'râbu'l-Kur'âni'l-Kerîm (3 vols) | 1,418 | confirm author from title page |
| ~~et-Tibyân fî Ulûmi'l-Kur'ân (Sâbûnî)~~ | 324 | NOT an i'rab book (Turkish, Qur'anic sciences) — exclude |

## Plan

### Phase 1 — Index + ship with the 6 ready books
- [ ] `books.json` catalog: id, title (AR/TR), author, death year, source, status
- [ ] Build script → per-surah index files `irab/{surah}.json`: ayah → [{book_id, text, range}]
      (entries covering a range e.g. 1:1–3 attach to every ayah, marked as a range)
- [ ] `/api/irab-books/<surah>/<ayah>` (or static files)
- [ ] UI: pick ayah → list of books (title · author · death date) → expand to read
- [ ] Remove AI i'rab endpoints, prompts, compare view
- [ ] Verify: Fatiha + Baqara 1–10 render from all books; removed routes return 404

### Phase 2 — Bring in the PDF books
- [ ] First check whether digital text already exists (tafsir.app / Shamela) — avoids OCR
- [ ] Otherwise: OCR pilot on ~20 pages per book, measure accuracy, pick engine
- [ ] Per-book segmentation parser (surah/ayah headings) → same index format
- [ ] Spot-check 10 random ayahs per book against the scan

### Phase 3 — Turkish reading
- [ ] Fixed i'rab glossary (mübteda, haber, fâil, mef'ûlün bih, hâl, temyîz…)
- [ ] Translate with Claude, glossary enforced; cache per (book, ayah); never regenerate on view
- [ ] Priority order: ayahs used in lessons → Juz 'Amma → Fatiha/Baqara → rest
- [ ] Label as "makine çevirisi"; Arabic original always shown alongside
- [ ] Teacher review flag (reviewed / unreviewed) per entry

## Open questions
- Which site hosts it: `portal/` (Flask) or `Dersler/` (static)?
- Copyright: modern works (Sâfî, Derviş, el-Harrât, Da'âs?) — public, or login-only?
- Translation budget / scope: everything up front vs. on-demand + cache
