# Independent mapping adjudication

Date: 2026-10-10. Scope: two existing Arabic/TR/EN records only. No library, translation, or applied-mapping files were changed. At the parent agent’s subsequent explicit request, two new independent audit vote artifacts were recorded in addition to this report. No paid API was used.

Reviewer/model: independent Codex sub-agent, instructed by this session as GPT-6. The exact backend model identifier is not exposed in my available session metadata, so I cannot honestly certify a more specific model name or claim an externally invoked stronger model. This is an independent evidence review, not proof of a model upgrade. I did not read other reviewers' reports or votes before reaching these conclusions.

## Decisions

| Current record | Verdict | Correct association | TR mapping | EN mapping | Confidence |
|---|---|---|---|---|---|
| Surah 4, `nahhas-meani:176-176` | INTRODUCTION | `[{"surah":5,"kind":"introduction"}]` | FOLLOWS_SOURCE | FOLLOWS_SOURCE | High from an externally accessible transcription of the book; original print layout not verified |
| Surah 5, `mekki-muskil:68-68` | REMAP | `[{"surah":5,"from":64,"to":64}]` | FOLLOWS_SOURCE | FOLLOWS_SOURCE | Very high: local scanned book page inspected visually plus Quran comparison |

These are proposed association decisions. Preserve all three text strings verbatim, including existing translator notes. Do not replace stable source identifiers or source-reference provenance with the corrected display association. Neither record calls for a fabricated continuous range or a disjoint association.

## Nahhas: currently 4:176

### Material inspected

- Complete current record via `python3 portal/mapping_review.py case 4 nahhas-meani:176-176`, including Arabic, Turkish, English, and hashes.
- `Irab Kitaplari/irab_kutuphane_nahaas-meanings.json`, zero-based `girdiler[395]`, with neighboring entries 4:166, 4:172, 4:174 and 5:1, 5:2.
- `irab_library/w/s004.json` for 4:1, 4:174–176 and `w/s005.json` for 5:1.
- The book transcription at [معاني القرآن للنحاس](https://www.arabic-keyboard.info/books/ar/read-book/%D9%85%D8%B9%D8%A7%D9%86%D9%8A-%D8%A7%D9%84%D9%82%D8%B1%D8%A2%D9%86-%D9%84%D9%84%D9%86%D8%AD%D8%A7%D8%B3), retrieved during this review, particularly extracted lines 911–918.

### Content and placement evidence

The entire current Arabic record is:

> رُوى عن عَلْقمة أنه قال: "كلُّ ما كان في القرآن ﴿يَا أَيُّهَا ٱلَّذِينَ آمَنُواْ﴾ فنزل بالمدينة، وكلُّ ما كان في القرآن ﴿يَا أَيُّهَا ٱلنَّاسُ﴾ فنزل بمكة".

Its subject is a reported general rule about Meccan/Medinan revelation. Quran 4:176 concerns inheritance, beginning `يستفتونك قل الله يفتيكم في الكلالة`; there is no source discussion of its inheritance terms here. A general occurrence of `يا أيها الناس` in 4:1 or 4:174 cannot establish placement: this expression occurs elsewhere and the report explicitly generalizes across the Quran.

The local downloaded JSON repeats the questionable 4:176 label and contains no chapter heading in this record. Its sequence places this record immediately before 5:1, whose commentary begins `من ذلك قوله تعالى`. This suggests introduction spillover but, taken alone, would not prove whether it belongs to surah 4, surah 5, or a general introduction.

The external book transcription resolves that ambiguity. It first includes actual 4:176 commentary, numbered 258–259, then concludes `انتهت سورة النساء`. It then has the heading `تفسير سورة المائدة`, identifies it as Medinan, and places the exact ʿAlqama report after `بسم الله الرحمن الرحيم سورة المائدة وهي مدنية` and before the numbered item `1 من ذلك قوله تعالى` for 5:1. That is explicit chapter structure, not a lexical guess. The report therefore belongs to the introduction to surah 5. It is neither a commentary entry for 4:176 nor an introduction to surah 4, and no particular verse target is necessary.

TR reproduces the attribution to Alkame and both revelation-location statements in the same order. EN does likewise with ʿAlqama. Both translate this Arabic source record; the association problem affects the whole AR/TR/EN unit rather than one translated text being drawn from another entry.

### Verification limit

No local Nahhas *Maʿānī* PDF/scan was found in the `Irab Kitaplari` file inventory; the local evidence is the downloaded JSON. Opening the stored source URL [tafsir.app/nahaas-meanings/4/176](https://tafsir.app/nahaas-meanings/4/176) through the web tool returned 503. The decisive chapter evidence above comes from a third-party-hosted transcription of the primary book, not a scan I visually checked. It is strong textual-placement evidence, but the exact printed edition page number and original-page typography remain unverified. The two online transcriptions encountered should not be assumed to have independent textual pedigrees. No claim of manuscript verification is made.

## Mekki: currently 5:68

### Material inspected

- Complete current record via `python3 portal/mapping_review.py case 5 mekki-muskil:68-68`, including Arabic, Turkish, English, and hashes.
- `Irab Kitaplari/irab_kutuphane_makki-mushkil.json`, zero-based `girdiler[402]`, and neighbors for 5:59–61, 5:69 and 5:71.
- `irab_library/w/s005.json`, particularly the complete Arabic of 5:64 and 5:68.
- Local scanned book `Irab Kitaplari/Müşkilü İ'râbi'l-Kur'ân/1.pdf`, visually rendered in memory using pypdfium2. Decisive page: **PDF page 313 (zero-based index 312), printed page 237, numbered item 713**. No OCR inference was used for the decisive reading.
- [Shamela book 5538, page 170 / volume 1 printed page 232](https://shamela.ws/book/5538/170), accessed during this review. Its paragraph matches the current source passage and sits between the end of 5:61 commentary and the `والصابئون` commentary.

### Content and layout evidence

The entire current Arabic record is:

> قَوْله {مَا أنزل} مَا فِي مَوضِع رفع بِفِعْلِهِ وَهُوَ وليزيدن وَكلما ظرف وَالْعَامِل فِيهِ أوقدوا وَفِيه معنى الشَّرْط فَلَا بُد لَهُ من جَوَاب وَجَوَابه أطفأها

The nominative `ما أنزل` governed by `وليزيدن` can describe the identical clause in either 5:64 or 5:68. That shared clause alone cannot choose a target. However, `كلما أوقدوا ... أطفأها` is in 5:64, not 5:68. Thus the entire paragraph is already coherently explained by 5:64; adding 5:68 merely because its first clause repeats would require evidence of intentional separate treatment.

The local original-page layout supplies decisive positive evidence: printed p.237 has item **713**, quoting `ما أنزل`, followed by verse number **64**. Immediately below, the author discusses `ما` and `وليزيدن`, then in the same item discusses `كلما`, `أوقدوا`, and `أطفأها`. The next independently numbered item is **714**, `والصابئون`, verse **69**; the preceding item **712** is `وقد دخلوا بالكفر`, verse **61**. There is no separate 68 heading, entry, or intervening boundary splitting the current passage. Therefore associate the complete record with 5:64 only. A disjoint `{64,68}` target is unsupported and unnecessary.

The Arabic transcription agrees in substance with the inspected scan. The local JSON metadata says verse boundaries were automatically determined (`ayet sınırları otomatik belirlendi`), consistent with the label being a segmentation artifact; the exact cause of this one incorrect label was not reconstructed.

Both TR and EN follow the Arabic grammatical discussion in order. Both already append a translator note identifying verse 64 and describing the source attachment as 68. Those notes corroborate the issue, but the decision above does not depend on trusting the translators: it is independently established by Quran text and the scanned book. Preserve the notes exactly under the content freeze.

### Verification limit and edition distinction

The stored Shamela reference is volume 1, printed page 232. The locally inspected scan has the passage on printed page 237. These are different paginations; do not silently substitute one for the other in source metadata or claim they are the same edition. The scan's passage and verse label were visually verified, but its full bibliographic edition identity was not established. The printed verse number is editorial evidence; the book paragraph itself and Quran wording independently support 5:64. Manuscripts were not consulted.

Local PDF SHA256: `d68b2f7eac5624fb624ff165bc7f04f704799f17629b918e459b3eb92894bb75`.

## Content fingerprints

These hashes were read again before writing the report and identify the unchanged reviewed content:

| Record | Language | SHA256 |
|---|---|---|
| `4 / nahhas-meani:176-176` | AR | `61ef88bb8b5bb7722e0f19b6464a7a7d2d5a4512e0e1f0d0f77b4588155c1f33` |
| `4 / nahhas-meani:176-176` | TR | `0313ce025ac23907396ae938232f1812898c0c0a69dbb0f18d69fb8a2f5fa4dc` |
| `4 / nahhas-meani:176-176` | EN | `088d0b678039eb9c512a93799588ff818f1159f5e1382da4d6b8ac085d44aecc` |
| `5 / mekki-muskil:68-68` | AR | `e4699f4313a6900597e1a7b6261db106c82a7783d5fd820507e5e08894d9fde5` |
| `5 / mekki-muskil:68-68` | TR | `cd832fe89b6880690002a2e85b5f6457fabd743bead117ed3b3737c51a9d4c8d` |
| `5 / mekki-muskil:68-68` | EN | `49b60c6c4a9d6f1b8190c03387f2995a866de7b9511e0ccc14b22906737b9f37` |

## Recorded votes

After reaching the conclusions above independently, the parent requested recording both votes with reviewer identifier `strong-adjudication-gpt6astra`. That identifier is parent-assigned and is not independent verification of the backend model; the vote model field preserves the disclosure above. Both vote commands succeeded and initially returned `NEEDS_INDEPENDENT_REVIEW`. No mapping was applied. The current case fingerprints include:

- Nahhas association: `9a2b06eaf9d4160a7a86e807e3f310d09e4fdaf794268c2f4e9f1d71b39cc22b` (current source index 567).
- Mekki association: `883fe7bec4b4bcf1878ff360bba5bded48f142ffc2e2cde8a9dc11adb01ce288` (current source index 385).
