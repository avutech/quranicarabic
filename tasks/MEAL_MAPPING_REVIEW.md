# Ayah meanings mapping review — 2026-10-10

Scope: read-only audit of all 114 `irab_library/w/sNNN.json` files. No book, Arabic source, translation, cache, or word-grid content changed. No network calls, paid APIs, or kuranmeali.com scraping.

## Complete deterministic coverage

| Check | Coverage | Result |
|---|---:|---|
| Canonical Hafs verse-key coverage against `portal/fetch_tafsir_app.py:VERSES` | 114 surahs / 6,236 ayahs | Exact, zero gaps or extra keys |
| Seven expected meal resources per ayah | 43,652 meal records | All present and nonempty |
| Same verse and resource text against original local Quran.com cache, allowing only HTML entity decoding | 43,652 meal records | Zero differences |
| Arabic words, English word meanings, transliteration against same cache verse | 6,236 ayahs | Exact tuple equality |
| Independent Corpus/Tanzil verse and word-position coverage | 6,236 ayahs | All present; zero word-count differences |
| Arabic verse identity against Corpus after analysis-only orthographic normalization | 6,236 ayahs | 6,233 exact normalized matches; three equivalent-spelling differences reviewed |

The local independent source is `Irab Kitaplari/_kelime/quranic-corpus-morphology-0.4.txt`, Quranic Arabic Corpus v0.4, based on Tanzil verified Arabic text v1.0.2 as declared in its unchanged copyright header. The local Quran.com cache is `Irab Kitaplari/_kelime/qurancom.json`, fetched 2026-10-04. Corpus text was parsed by TAB-delimited columns (not whitespace: FORM at 37:130 contains an embedded space). Arabic was reconstructed by joining each word's segments using `portal/morph_labels.py:to_arabic`. Comparison normalized vowel/Quran marks, alif variants, hamza spelling, alif maqsura, tatweel and small pronoun letters only in memory. Remaining spellings are 11:13 افتراه / افترىٰه and 12:39, 12:41 صَـٰحِبَىِ / صَىٰحِبَىِ. These are the same verses, not numbering shifts. The corpus was not altered.

## Confirmed semantic mismatch

**Resource 210 (Dar Al-Salam Center), 87:14** has `Sonra onun içinde ne ölür, ne de yaşar.` This is the same text assigned to 87:13 and translates its Arabic `ثُمَّ لَا يَمُوتُ فِيهَا وَلَا يَحْيَىٰ`. Arabic 87:14 is `قَدْ أَفْلَحَ مَن تَزَكَّىٰ`, describing the success of one who purifies himself. The English meals and other Turkish meals at that ayah corroborate this different subject. Resource 210 at 87:15 is `Ve Rabbinin adını anıp namaz kılan.`, correctly following the purification statement; neighboring entries 87:10–19 therefore do not show a continuing offset.

This defect already exists in the original Quran.com cache; exact cache equality does not detect it. **No correction applied.** Proposed decision: classify the existing 87:14 text as a duplicated 87:13 meaning; retain its bytes and provenance, flag the 87:14 slot for source verification. Do not merely move the duplicate onto 87:13, which already contains it. A correct 87:14 original-source record must be located before any mapping replacement. No equivalent resource-210 replacement has been independently sourced in this review. A higher model is unnecessary to establish the obvious mismatch, but source retrieval/review is necessary to select the permitted correction.

## Consecutive duplicate candidates

The scan found 903 adjacent identical-meal pairs, all spanning different Arabic verse text: 843 resource 77, 57 resource 52, two resource 112, one resource 210. Duplicate pairs are signals, not automatic mismatches. Many translators intentionally combine consecutive ayahs into one sentence; preserve that context and record the full applicable range.

Manual semantic review performed here: resource 112 at 15:92–93 and 26:218–219 are legitimate combined ranges. Their printed `93:` / `219` labels describe the joined translation, not a displaced individual verse. Resource 210 at 87:13–14 is the confirmed defect above. Resource 77 at 2:26–27, 105:3–4, 106:1–2, 106:3–4, 107:2–3, 110:1–3, 111:4–5, 113:1–5 and 114:1–6, plus resource 52 at 104:8–9, also clearly combine the cited Arabic subjects. These sample verdicts do not close the other duplicate candidates. The detailed candidate inventory is in `tasks/MEAL_MAPPING_EVIDENCE.json`.

## Limits and decision framework

This pass covers 100% of deterministic meal provenance and verse keys, **not 100% independent semantic validation of the 43,652 records**. Cached upstream mistakes can survive all structural checks. The 843 duplicate pairs in resource 77 have not all been individually adjudicated; resource 52 duplicate review is now complete as recorded below. Other singleton semantic mistakes can exist without a duplicate signal. Distinguish structural pass, source-cache agreement, combined-range evidence, and independent semantic certification in the final ledger.

Recommended decision sequence: (1) validate canonical ayah and source resource IDs; (2) compare source-cache identity; (3) group identical consecutive source translations as range candidates; (4) judge whether their unchanged full text covers the whole Arabic range; (5) confirm suspicious singleton text against another meaning and original publisher source; (6) adjudicate only unresolved ambiguity using a stronger model or independent reviewer. Never change wording, split a combined translation, or silently replace a source. Persist old/proposed ayah mappings, exact text hashes, source evidence, reviewer verdict, uncertainty and immutable content identifiers. A source-defective record lacking a correct replacement stays unresolved.

## Follow-up: resource 52 duplicate review completed

All 57 adjacent duplicate pairs for resource 52 (Elmalili Hamdi Yazir), grouped into 50 maximal identical-text ranges covering 107 verse/resource records, were independently reviewed against the full unchanged Turkish text and full Arabic of every verse in each range. Neighboring verse subjects were checked using resource 20. All 50 ranges are intentional combined translations; zero wrong mappings and zero unresolved duplicate candidates in this specific set. Exact original-cache/build agreement verified for all 107 records, with SHA-1/SHA-256 content hashes retained in `tasks/MEAL_52_DUPLICATE_REVIEW.jsonl`. No original publisher edition was consulted or needed to resolve these obvious range combinations; the review concerns mapping rather than certification of the translator's interpretive choices. No content or association was changed. This does not certify resource 52 singleton meanings or resource 77 duplicate candidates.
