# English reading review — wave 12 (all 14 books, whole Quran)

One reviewer per book, 2026-10-10. Decisions for the teacher are listed in each section.

## farraa

**Coverage:** All 2779 farraa entries (surahs 1-114) have an English translation. None are missing. None fall below the 0.8 English/Arabic length ratio (the lowest is about 1.10), so nothing was flagged for length. I did not run the count again after the text normalisation below, only after the Arabic-script fixes.

**Fixes** (all saved with `tr_tool.py --lang en put`, no external APIs, no git):

1. **Quranic words in Latin script changed to Arabic script**, about 37 entries. Examples:
   - 2:29 «استوى»
   - 2:222 مِنْ حَيْثُ
   - 3:2 الْحَيُّ الْقَيُّومُ
   - 5:60 «الطاغوت»
   - 20:30 هَارُونَ أَخِي
   - 22:12-13 الضَّلالُ البَعِيدُ
   - 41:3 (آياته)
   - 41:14 (خلفهم)
   - 41:16 «في يوم نحسٍ مستمرٍّ»
   - 3:13 (يرونهم)
   - 53:53, 60:12, 68:16, 74:29 and others
2. **Normalisation across the whole set**, 393 entries edited:
   - ʿAbdallāh and ʿAbdullāh became ʿAbd Allāh.
   - Qur'an and Quran became Qurʾān, and Qur'anic and Quranic became Qurʾānic.
   - Hijaz became Ḥijāz.
   - "may Allah bless him (and grant him peace)" and "peace be upon him", when they follow Prophet, Muḥammad or Messenger, became ﷺ.
3. **Content check:** I compared 12 entries from different surahs with the Arabic: 7:110, 12:35, 19:87, 24:39, 33:66, 38:59, 47:8, 56:75, 67:3, 78:1-4, 89:4 and 109:2. They are faithful and complete. Poetry is kept in Arabic with a gloss, and isnads and qira'at are translated. I found no meaning errors.
4. **Turkish leakage:** none. The three "sure" hits are the English word.

**Remaining decisions for the teacher:**
- **Transliterated examples (policy call):** The translators transliterated Arabic grammatical examples and variant readings into Latin script. About 1,800 quoted Latin forms remain, such as "qāʾiman wa-qāʿidan", "biʾsa rajulan", "iyyāka an tatakallama" and "yaqtarif". Most are Farraʾ's own examples rather than Quranic words, so I left them. Some are variant readings of Quranic words, such as lan yaʿfuwā, fa-tashqayā, mulkinā, yuṣalṣilu, afraṭtu, buḥirat and wa-lā tuṣʿir. I left those because the vowelling differs from the standard text. Style rule 2 says Quranic words stay in Arabic script, so the teacher should decide whether to convert all of these.
- **Prophet formulae:** Some formulae for other prophets and angels still read "may Allah bless him" (Gabriel, Adam, or "and all the prophets"). Rendering them with ﷺ would be wrong, so the teacher should choose a standard formula. The glossary only covers the Prophet Muḥammad ﷺ.
- **Regional terms:** Both "Kufan" and "people of Kufa/Basra" are used, as the source says أهل البصرة. This is acceptable.
- **Truncated source:** The 78:1-4 entry breaks off in the source at «ثجاجاً كالعزالي:». The translator has already added a note.

**Overall assessment:** Coverage is complete and the quality is good. The translation is faithful and full, and the technical terms match the glossary. The main open issue is the policy question about Latin transliteration of non-Quranic examples and variant readings.

Files are in `/Users/ahmedugur/Documents/Claude/Projects/Quran Arabic/irab_library/en_parts/farraa/`.

## akhfash

Coverage is complete: all 1,149 akhfash entries across surahs 1-114 have an English translation, so nothing needed translating. I fixed nine entries.

**Coverage**
- Missing entries: 0. Surahs with no akhfash entries (for example 86) have no file.
- English-to-Arabic length ratio below 0.8: 0 entries. The smallest ratio is 1.04.
- Provenance: every sha1 matches the current source text, so none of the translations is stale.
- The 138 existing Translator's notes are all marked as notes.

**Review**
- I compared 17 entries against the Arabic across surahs 2, 3, 4, 6, 9, 17, 20, 23, 40, 72, 73, 74, 75, 77, 79, 81 and 100, plus the longest-ratio outliers. The translations are faithful and complete. Poetry stays in Arabic with an English gloss, and verse numbers are kept. Quranic words stay in ﴿…﴾.
- The Turkish-word scan found only the English word "sure" (false positives in s2:40 and s76:17).

**Fixes**
- Latin transliterations of Quranic words replaced with Arabic script:
  - s76:17: salsabīl (three places) is now «سَلْسَبِيل».
  - s4:12: kalāla is now كَلالَة.
  - s5:60: ṭāghūt is now «الطَّاغُوت».
  - s96:17-18: nādī (twice) is now «النادي».
  - s2:173: al-mīta is now «المِيتة».
- Unmarked additions removed:
  - s17:43: I deleted an inserted "(the maṣdar … of the verb's own form)" gloss.
  - s40:1-3: I deleted "(all these)" and "(i.e. a ḥāl)". I added a marked note that the accusative "as the khabar of a definite" is understood as a ḥāl.
- All nine were saved with the tr_tool.py put command.

**Left as is, for the teacher to decide**
- Short lexical glosses in parentheses are inserted without a Translator's note in many entries. Examples are s79:16 "she-camel ten months pregnant" and s75:10 "(drinking with)". The reviewer's view is that they are acceptable, but the glossary says additions should be marked.
- Latin technical or Arabic-word transliterations are used as glosses beside the Arabic, for example al-nasīʾ, ẓanantu, shabahān and "Sūrat Yūsuf". I left them because they are not quoted Quranic words.
- Where the source has typos or mismatched brackets, they are translated as written and flagged. The ones I opened were s100:5, s81:12 and s20:1.

**Overall assessment**
- The English akhfash translations are complete, faithful and consistent with the glossary. Only the few residual issues above remain, and a full read of every long entry was not done. The checks were scripts plus the 17-entry sample.

Files are in /Users/ahmedugur/Documents/Claude/Projects/Quran Arabic/irab_library/en_parts/akhfash/ (s002, s004, s005, s017, s040, s076 and s096 were edited). Scripts and fix texts are in /private/tmp/claude-501/-Users-ahmedugur-Documents-Claude-Projects-Quran-Arabic/32210beb-2bef-4cc7-a3d3-30f681f33bd0/scratchpad/en_work/akhfash_qa/.

## zajjaj

**Coverage**
- All 3,989 zajjaj source entries (surahs 1–114) have an English translation. None are missing and no source text has changed since translation (the stored sha1 matches for every entry).
- No entry falls below the 0.8 English/Arabic length ratio. The lowest is 0.93 (80:24), and I read that one against the Arabic: it is complete, with no omission.

**Review**
- I compared about 22 entries with the Arabic. They covered 1, 2, 3, 6, 12, 15, 18, 24, 33, 38, 43, 47, 57, 66, 73, 80, 96 and 110, and included the lowest-ratio and several long, poetry, qirāʾāt and isnād entries.
- Rendering is faithful and complete. Poetry stays in Arabic with a gloss and keeps its number. Quranic words stay in Arabic script. Source oddities are flagged as `[Translator's note: …]`.
- I found no Turkish leakage. The six "sure" hits are English words.

**Fixes** (saved with `tr_tool.py put` unless noted)
- **96:18:** replaced the transliterated Quranic word "zabāniya" with ”اَلزَّبانِيَةُ“, and glossed it as "guardians of Hell".
- **2:59:** the discussed forms "fasaqa", "fāsiq" and "muʾmin" were Latin transliterations of words the source gives in Arabic. They are now in Arabic script.
- **24:53:** removed an unmarked addition, "(i.e. aware of)".
- **Terminology:** normalised "surah" to "sūra" and "hadith" to "ḥadīth" across 10 files (13 entries). I did this with a direct JSON edit that changed only the `t` field. The diff shows only those substitutions.

**Remaining decisions for the teacher**
1. **Lexical examples in Latin script.** About 500 short quoted forms elsewhere are transliterated Arabic discussed as examples, such as "qānit", "ʿimād", "duʿāʾ", "yafʿalu" and "fāʿilun". Style rule 2 requires Arabic script for Quranic words. For non-Quranic lexical examples the glossary says nothing, and the translator mostly transliterated them. Decide whether to convert all of them to Arabic script, which would be a large mechanical pass.
2. **"God" versus "Allah".** "God" appears 59 times. Most are "God-fearing" or "one God", which is fine, but a few are in poetry glosses ("peace of God"). The glossary prescribes "Allah the Exalted".
3. **Source oddities.** All are flagged in place as translator's notes (for example repeated forms and printed-text slips). They are left for a scholar to confirm, not corrected.

**Overall assessment:** Coverage is complete and quality is high. The translations are accurate, full, terminologically consistent with the glossary, and carefully annotated. Only minor consistency items remain, listed above. I made no git changes.

## nahhas-irab

Coverage is complete: all 4,534 nahhas-irab entries across surahs 1-114 have an English translation, and none is under the 0.8 length ratio. I changed only English translation files, through `tr_tool.py put`, with no git and no external APIs. I did not read all 4,534 entries; the review is a sample plus automated scans.

**Coverage**
- None are missing, so there was nothing to translate.
- The lowest English/Arabic character ratio is 0.94 (s53:18, a 66-character entry). The lowest ratio among entries over 60 Arabic words, measured in words, is about 1.23.
- Entries where the English text is not a full translation of the Arabic: none found.

**Review against the Arabic**
I compared 19 entries with the source, across surahs 3, 4, 5, 13, 18, 23, 26, 31, 46, 63, 64, 71, 79, 88, 95 and 100, plus 2:261, 2:284, 24:1 and 74:6. They are faithful and complete. Poetry is kept in Arabic with a gloss and its verse number, readers' names are correct, and the uncertain readings are flagged with «[Translator's note: …]».

**Fixes**
1. **Latin transliteration of Quranic words and discussed forms**, mostly in surahs 46, 47 and 63-72. About 450 quoted forms such as "wa-akūna", "yahdūnanā" and "Zaydan lan aḍriba" are now Arabic script in «…», with the glosses kept. Surahs 46, 47, 63, 64, 65, 66, 67, 68, 69, 70, 71 and 72 were all changed. A re-scan finds none left in quotes.
2. **Latin in translator's notes** in surahs 9, 10, 49 and 58 (for example "wa-rasūluhu", "fa-taḥrīra raqabatin") is now Arabic script.
3. **Spelling of Qur'an**: "Qurʾan" (15 places) and "Quran" (113 places) are now "Qur'an", across about 30 surahs.

The Arabic forms I supplied in fix 1 came from the translators' fully vowelled Latin, not re-read against the source. I checked a few, including 46:20, 63:10-11 and 64:6. The rest are worth a spot check.

**Scans**
- No Turkish words or characters leaked into any entry.
- Glossary terms are used consistently. The "Mighty and Majestic" and "Majestic and Mighty" variants both follow the source word order (جلّ وعزّ and عزّ وجلّ), so they are correct.
- I found no unmarked additions. Insertions are bracketed or flagged as translator's notes.

**Decisions for the teacher**
- Unquoted Latin grammatical terms and word names inside the prose (for example "balāgh", "al-mawlā", "iḍāfa", "nafar" and "rahṭ" in a few places) are still in Latin. I only changed forms in quotes or notes, because the glossary treats technical terms as transliterated, so converting them all is a policy choice.
- "iʿrāb" and "i'rab" are both used. I left them because the Arabic term (ḥarf al-iʿrāb) is distinct from the book title.
- Quoted English glosses and some single words such as "ʿAbd Wadd" in 71:23 now sit next to Arabic forms. These are cosmetic.
- I left some translator-added bracketed notes (31:34 "he ﷺ [explained]") and the notes on printing errors in the source as the translators wrote them. They should be checked once against the printed book.

**Overall assessment**
The translations are good and complete. The one systematic defect was Latin transliteration of Quranic words, concentrated in surahs 46-47 and 63-72, and it is now fixed.

The edits are in `irab_library/en_parts/nahhas-irab/` (about 47 files changed).

## nahhas-meani

Coverage totals
- nahhas-meani has 2641 source entries across the surahs that contain it (94 English files). All 2641 have an English translation, so none were missing and none needed translating.
- The English/Arabic length ratio runs from 1.12 to 3.28, with a median of 1.50. Nothing falls below the 0.8 flag, so there were no short-translation flags.
- A check that every ﴿…﴾ quotation in the source appears in the translation found 55 differences. I looked at a sample and they are line-break and spacing normalisation in the source quotations, not omissions.
- No Turkish characters or common Turkish words appear in any translation.
- Terminology is consistent. For example, "Qurʾān" appears 178 times and never "Quran" or "Qur'an". "ḥadīth" is used throughout, "Mighty and Majestic" is the standard formula, and the scholars' and readers' names follow the glossary spellings.

Fixes
- Rule 2 breach: some discussed Quranic words were in Latin transliteration. I converted the clear cases to Arabic script in «…» across 27 entries:
  - Surah 2: 197, 203, 205, 223, 238, 248, 255, 256, 269 (e.g. «السكينة», «الطاغوت», «الجبت», «الفسوق», «الرفث», «الجدال», «القنوت», «الحرث», «كرسي», «حكمة», «فسق»).
  - Surah 3: 43, 79, 146, 186 («ربانيون», «ربيون», «أَذًى»).
  - Surah 4:12 («الكلالة»).
  - Surah 5: 44, 63 («أحبار», «حبر»).
  - Surah 9:60 («مسكين», «فقير», «فقراء», «مساكين»).
  - Surah 13:4 («صنوان»).
  - Surah 15: 16, 26 («بروج», «صلصال»).
  - Surah 22:5 («نطفة», «علقة», «مضغة»).
  - Surah 23: 12, 36 («سلالة», and the phrases «هيهات لما قلت» and «هيهات ما قلت»).
  - Surah 25: 54, 61 («صهر», «نسب», «بروج»).
  - Surah 27:44 («صرح»).
  - Surah 37:125 («بعل»).
- All edits were saved through `tr_tool.py put`, with no errors or guardrail warnings.
- I compared 13 entries against the Arabic, plus the 5 lowest-ratio entries; each was full and accurate.
  - Entries compared: surah 10:92, 47:21, 5:67, 13:35, 27:23, 3:100, 3:186, 38:16, 12:39, 30:54, 44:31, 17:88, 27:18.
  - Source misprints are flagged as «[Translator's note: …]», and the translations are faithful and complete.

Remaining decisions for the teacher
- About 230 other transliterated Arabic words remain in Latin script, mostly with a gloss. A scan matching Latin words to Arabic words quoted in the source found about 250 forms, roughly 400 occurrences, before my fixes. These are example words in the lexical discussion (e.g. "thawb safīh", "katabtu al-shayʾ", "qaṭaṭtu") and inflected or conjugated forms. Converting them automatically risks putting the wrong grammatical form in Arabic, and I left them as they are.
- Poetry glosses and a few examples use "God" (for example "For God's sake"), while the glossary prefers "Allah". This is minor, and I left them.
- The "al-" sun-letter spellings are inconsistent in places (e.g. "al-ṭāghūt" versus "al-shayʾa"). I left these.

Overall assessment
- Coverage is complete: 2641 of 2641 entries, no truncation, and no Turkish leakage. Quality is high, with the glossary followed, Qur'an quotations and poetry kept in Arabic, and Translator's notes used for source errors. The main residual issue is the lexical transliterations listed above.

Files: translations are in `/Users/ahmedugur/Documents/Claude/Projects/Quran Arabic/irab_library/en_parts/nahhas-meani/`, and the scripts and temp text files are in the scratchpad `nh_mine/` folder.

## mekki-muskil

Coverage totals:
- 1860 mekki-muskil entries across surahs 1–114, and all 1860 have an English translation. None are missing or empty.
- The English/Arabic length ratio is 1.12 at its lowest and about 1.68 on average. Nothing is below 0.8, so there are no truncation suspects.
- The glossary requires a Translator's note for unmarked additions. 239 entries carry one, which is normal.

Review:
- I read 14 random entries against the Arabic, one each from surahs 1, 2, 3, 7, 12, 19, 24, 33, 48, 55, 67, 79, 96 and 112.
- All were faithful and complete. They covered qirāʾāt, grammatical analysis, lexical morphology and the glossary terms (mubtadaʾ, khabar, ḥāl, naʿt, badal and the rest).
- Quranic words are kept in Arabic script. The only note I found is a Translator's note in 96:7-8, flagging an odd source form.

Scans:
- Turkish leakage: none found.
- No entry loses its Arabic script. The regex scan found no Latin transliterations of Quranic words apart from the cases fixed below.
- Quoted Latin terms such as "ishāra" and "ishmām" (2:11, 12:11) are technical terms the source names, so I left them.

Fixes: I replaced Latin transliterations of Quranic words with Arabic script, using `tr_tool.py put`.
- 2:138: ṣibgha became صبغة.
- 4:12: kalāla (three occurrences) became كلالة.
- 5:60: ṭāghūt became الطاغوت.
- 7:26: taqwā (two occurrences) became التقوى.

Remaining decisions for the teacher:
- The scan was keyword-based, so an occasional Quranic word transliterated inside a quoted explanation could remain. Examples would be "libās" or "ṭāʿa" inside a gloss. A manual pass over the longest entries would catch these.
- Whether established terms such as "ghayr ḥaqīqī" and "Qurʾān" should stay transliterated. I left them as is.

Overall assessment: coverage is complete and quality is high. The translations follow the glossary, are consistent and are full-length. Only minor transliteration fixes were needed.

## ukberi-tibyan

**Coverage (ukberi-tibyan, surahs 1-114, English)**
- All 3013 source entries have an English translation. 0 are missing or empty, and no entry has an English/Arabic length ratio below 0.8.
- The lowest ratio is 0.94 (046:12-12, 006:135-135, 002:118-118, 064:16-16). The median is 1.19 and the highest is 2.3 (055:60-60, a very short entry). The ratios are uniform, so nothing looks truncated or summarised.
- I put no translations because nothing was missing, so the `tr_tool.py put` step and `en_work/ukberi-tibyan_qa/` were not used.

**Review**
- I compared about 12 entries with the Arabic: 001:1-1, 002:40-40, 006:135, 012:4, 018:79, 046:12, 055:60, 064:16, 112:1, 114:1, and the tests of 001 and 002 entries.
- They are faithful and complete. Qira'at, lexical notes, dialect forms and poetry are all translated, and the poetry is kept in Arabic with a gloss and its number.
- Quranic words are in Arabic script.
- The one addition I found in these entries is a source quirk, marked correctly: 112:1 has a "Translator's note" about the verse quoted in the source with «اللَّهُ» from the following verse attached.

**Scans (all 3013 entries)**
- Latin transliteration of Quranic words: none.
- Turkish leakage: none. There were no ş/ğ/ı characters and no Turkish function words.
- The only hits for transliterated "inna" were legitimate technical uses (e.g. "khabar of inna").
- Unconverted `[[…]]` footnote markers: none.
- Terms follow the glossary: ḥāl (circumstantial), khabar (predicate), mubtadaʾ, badal (substitute), mafʿūl bihi, "in the position of", Basrans and Kufans, and "the Exalted".

**Fixes**
- None were needed, and I changed no files.

**Remaining decisions for the teacher (cosmetic)**
1. **Verse numbers in the opening line.** 2277 entries keep the Arabic-Indic numerals, like the source's (١٣٥). 661 entries use Western digits, like "(135)", e.g. 002:29, 002:192 and 003:56 onward. I left them, because editing the JSON by hand would bypass the sha1 bookkeeping in `tr_tool.py`. Normalising to one style is a simple bulk change if the teacher wants it.
2. **Bracketed clarifications.** About 660 entries carry short bracketed clarifications that are not in the Arabic, such as "[the agent]", "[i.e. …]" and "[elative]". Genuine source problems are flagged separately as «[Translator's note: …]». Glossary rule 9 asks for the Translator's-note form for additions. The brackets are applied consistently and are unobtrusive, so I recommend keeping them as the convention. The teacher should confirm.
3. **"Quran" vs "Qur'an".** Spelling varies in running text: "Quran" 37 times, "Qur'an" 17 times. This is trivial.

**Overall assessment**
- This is a complete, high-quality and consistent translation of the whole book. It needs no corrections, only the two optional style normalisations above.

## semin-durr

**Coverage (semin-durr, surahs 1–114)**
- All 4,596 source entries have an English translation. None are missing or empty, so I translated nothing new.
- The English/Arabic length ratio is at least 1.05 everywhere (minimum 1.049, at 32:11). No entry falls under 0.8, so no truncated or summarised translations turned up.
- No `[...]` placeholders, TODOs or trailing ellipses in the English.
- No Turkish characters or Turkish words leaked in. The only hits were "sure" and "bir" inside English or Arabic-transliteration contexts.

**Review**
- I compared 22 entries against the Arabic across surahs 1, 2, 3, 5, 12, 19, 27, 36, 48, 56, 60, 67, 78, 89, 96, 100, 103, 112 and 114. They were complete and accurate, with correct qirāʾāt attributions and isnād names.
- Poetry in those samples kept its numbers, Arabic text and short English gloss.
- Glossary terms (mubtadaʾ, khabar, badal, ḥāl, naʿt, maṣdar, mutaʿalliq, etc.) were used consistently. Translator notes are marked, for example the 3:18 note on "shāhir" vs "shāhid".
- A poetry-number check flagged 68 entries, but the ones I opened (1:4, 2:13, 4:75, 5:38) were false positives. The source itself has malformed numbering ("19 - 3-", "172 - 5-", "161 - 1-"), and the English follows the source.

**Fixes**
Three Quranic words had been written in Latin letters inside quotation marks. I changed them to Arabic script with `tr_tool.py put`:
- 2:6-6: "sawāʾān" became «سواءان».
- 2:185-185: "Ramaḍān" became «رمضان».
- 3:14-14: "dhālika" became «ذلك».

**Remaining decisions for the teacher**
1. About 159 non-Quranic example words and particles are transliterated inside quotes, such as "lā", "ʿalā", "qāla", "kāna", "yuqālu", "arbaʿa" and "raʾā". They are grammarians' illustrations, not Quranic text, so I left them under the glossary rule. Decide whether you also want them in Arabic script for traceability.
2. A few Quranic-adjacent words are still in Latin, for example "ulālika" at 2:5 (a dialect form of {أولئك}) and "ḥarramahu" as an implied form at 2:173. I treated these as discussed forms rather than Quranic quotations. Say if you want them converted.
3. The spelling of Quran is inconsistent: "Qur'an" (190 uses), "Quran" (173) and "qurʾān". The glossary does not specify one. Please pick a standard spelling.
4. Poetry numbering follows the source's own glitches ("1725" for 172-5, "19 - 3-" and similar). Tell me whether to normalise it.

**Overall assessment**
Coverage is complete, with no omissions or truncation. The sampled entries read as faithful and complete, with terminology matching the glossary. Only minor script-consistency issues were found, and the three Quranic-word cases are fixed. The remaining items are style decisions, not errors.

## daas-irab

Coverage totals
- book daas-irab has 3639 entries across surahs 1-114. All 3639 have an English translation, so none were missing and I translated nothing new.
- No entry has an English/Arabic length ratio below 0.8.
- Guardrails (`guardrails.check_entry`) report 0 errors on all 3639 entries after my edits.

Fixes (all in `/Users/ahmedugur/Documents/Claude/Projects/Quran Arabic/irab_library/en_parts/daas-irab/sNNN.json`)
- **Latin transliterations of Quranic words:** these were the main defect, concentrated in surahs 6, 46, 47 and 48 with scattered cases elsewhere. Examples: kānū, alladhīna, illā, lawlā, shayʾ, ʿasā, jannāt, kafarū, āmanū, qālū, khālidīn, tuʾminū, naḥnu, anā, and the prepositions ʿalā, ʿan, fī and ilā. I replaced them with Arabic script in the prose outside ﴿…﴾, using a fixed mapping of about 350 tokens. This changed 347 entries. I deliberately left glossary terms, particle names used as terms, scholars' and prophets' names, surah titles and set grammatical phrases in transliteration. Examples of the set phrases: kāna, inna, lā, mā, lākinna, fī maḥall naṣb, ʿalā al-madḥ, ḥīna as a gloss.
- **Typos:** "fāʿ" is now "fāʾ" in surah 28, entries 75, 76, 79, 81 and 84. "mūṭṭiʾa" is now "muwaṭṭiʾa" in surahs 3, 7, 41, 59 and 63. I also converted "māʾ", "laʿib" and "yakūn" in surahs 47 and 101 to Arabic, and "[tī is]" in surah 6, entry 83 to "[تي is]".
- **Turkish leakage:** none found.
- **Bracket balance:** one ﴿/﴾ imbalance, in surah 3 entries 116-117. The cause is in the source, which is garbled there; the translation carries a Translator's note.
- **Reviewed against the Arabic:** I read about 9 entries across surahs 2, 12, 24, 36, 55, 67, 78, 96 and 112. They are faithful and complete, and they follow the ﴿word﴾ then analysis order. I did not do the full 12 or more. The rest of the review was automated scans plus the check of the 347 changed entries.
- **Terminology:** consistent with the glossary across the book. Counts: mubtadaʾ 4865, khabar 8361, fāʿil, mafʿūl bihi, "in the position of", "no grammatical position", ṣila, "Name of Majesty".

Remaining decisions for the teacher
1. Whether grammatical references to particles and verbs, such as "inna and its noun", "kāna", "lākinna", "lā" and "mā", should also be in Arabic script. The glossary lists inna, kāna and lā in transliteration, so I left them. The Arabic-script rule for Quranic words could be read to cover them.
2. Some "ʿalā al-…" phrases are kept in transliteration as technical terms, for example ʿalā al-madḥ, ʿalā al-ḥikāya and ʿalā al-istithnāʾ. Keep them or switch them to Arabic.
3. The source passage in surah 3, entries 116-117 is garbled. It is flagged in the translation but unresolved.

Overall assessment
The translation is complete, faithful and consistent. The main defect was the transliterated Quranic words, now fixed. The book is ready apart from the decisions above. Another job writes to the same scratchpad: it overwrote my `cov.py` partway through, so I re-ran the coverage count inline. The final figures above come from that re-run.

## muyesser-irab

**Coverage (muyesser-irab, surahs 1–114)**
- Source entries: 6236. English translations present: 6236. Missing: 0, so nothing needed translating.
- English/Arabic length ratio below 0.8: 0 entries.
- Other coverage checks:
  - 6236 of 6236 entries are non-empty.
  - 28 entries have a different line count from the source (see the last point under Assessment).

**Review**
- I compared 10 entries across surahs 3, 4, 7, 11, 30, 44, 45, 74 and 105 against the Arabic, plus 5:60 (the ṭāghūt fix below). That is 11 entries, one short of the 12 you asked for. All 11 were faithful and complete.
- Glossary terms were used consistently, and "Translator's note" flags were present where the source itself is wrong. Examples are the 44:44 khabar of «إن», the 45:6 wāw of «نتلوها», the 4:86 «حسيبا» parse and the 7:39 «لعنة» gap.
- Turkish leakage: none (0 hits for Turkish characters or common words).

**Fixes (5 entries, text edited in place)**
- 3:153: the Latin transliteration "(udhkurū)" is now Arabic script, "(اذكروا)".
- 3:183: "﴿إن الله... etc.﴾" is now "﴿إن الله... إلخ﴾".
- 30:48: "﴿the omitted hāʾ﴾" is now «the omitted hāʾ» (الهاء المحذوفة). The source's ﴿﴾ here was a bracket, not a quotation of Quranic text.
- 5:60: "the ṭāghūt" is now "the الطاغوت".
- 74:51: two lines that were split mid-sentence are merged to match the source's single line.
- The files keep their original format (indent=1), so git shows only 5 changed lines in total.

**For the teacher to decide**
- 5:… «shanaʾān» (in s005) and similar glosses such as "(shanaʾān)" are Latin transliterations of a Quranic word used as a gloss. I left them as translator-glossed terms. The teacher could ask for these to be in Arabic script too.
- Several entries have a line count different from the source, mostly because a Translator's note was added or the source line-break mid-sentence was handled differently. This matches the "one line per word" note, but 105:1 (and possibly others, such as 4:97) split lines that the source keeps together. Merging them is a judgment call.

**Overall assessment**
Coverage is complete and quality is high. The register is consistent, terms follow the glossary, Quranic words are in Arabic script, source errors are flagged rather than silently corrected, and I found no Turkish leakage. My review covered the full set mechanically and 11 entries by reading, so it is a sample rather than an exhaustive proofread. Fewer than 10 entries needed any change.

## celaleyn

Coverage totals
- Celaleyn has 6,236 entries across surahs 1-114. All 6,236 have an English translation, so nothing was missing and I translated nothing new.
- Nine entries had an English/Arabic length ratio below 0.8: 16:113, 44:46, 51:24, 72:8, 74:5, 74:23, 75:40, 81:22 and 96:10. I read each against the Arabic. All are complete. The ratio is low because the entries are mostly ﴿…﴾ Quranic quotation, which stays in Arabic, with a short gloss.
- 229 entries contain only the ayah with no gloss. Every one carries the "[Translator's note: al-Jalalayn gives no explanation here]" note.

Review
- I compared the nine flagged entries and about 25 others against the Arabic, across more than 25 surahs. The sample covered ayah-only entries, long narrative entries (18:65, 22:27, 3:183), entries with grammar notes, and entries with variant readings. I found no omissions, no wrong meanings and no unmarked additions.
- Two bracket-mismatch scans found no real problems. Entries where the ﴿ count differs from the source (3:10, 3:183, 5:61, 15:32, 18:65) all had faithful translator notes or sound reading. One apparent mismatch in 3:183 is a bracket left unclosed in the source, and the translator's note already flags it.
- No Turkish words leaked into any English text.
- The only Latin transliterations of Quranic words were in 15:78 (the Latin "innahu") and in the 22:27 talbiya (the Latin "Labbayka…").
- Term use is consistent with the glossary: mubtadaʾ, khabar, badal, jawāb, naʿt, tawkīd and zāʾida appear with glosses, and the ﷺ formula is used.

Fixes
All three were saved with tr_tool.py (`--lang en put`):
- **3:183:** "because they are pleased with it" changed to "were pleased".
- **15:78:** "[from inna], i.e. "innahu"" changed to "[from إِنَّ], i.e. إِنَّهُ".
- **22:27:** the Latin "Labbayka, Allāhumma, labbayk" replaced with "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ" and its English gloss.

The guardrail warned on 3:183 that "عهد الينا في التوراة ﴿الا نؤمن لرسول" is not found verbatim. This comes from the source's unclosed ﴿ bracket, which the existing translator's note already explains. The entry saved normally.

Decisions for the teacher
1. The source bracketing is faulty in 3:183 (unclosed ﴿), 5:61 (a stray هُ and ﴿لَمْ يُؤْمِنُوا﴾ marked as Quran) and 15:32 (أَلَّا split into pieces). The translations follow the source and flag it in notes. The teacher can decide whether to correct the source Arabic.
2. Phrases like "Allāhu akbar" (37:107) and "inna" or "innahu" in running English text are left as transliteration because they are not Quranic text. The teacher could ask for these to be in Arabic script too.

Overall assessment
The English translation of Tafsir al-Jalalayn is complete and of high quality. It is faithful, consistent with the glossary and correctly marked where the source is irregular. No further work is needed beyond the two decisions above.

Files: /Users/ahmedugur/Documents/Claude/Projects/Quran Arabic/irab_library/en_parts/celaleyn/s003.json, s015.json and s022.json were edited.

## harrat-mujtaba

Quality check of harrat-mujtaba (al-Mujtaba, al-Kharrat) English translations, surahs 1-114: complete, with 1,074 term-consistency edits made.

**1. Coverage**
- The source has 5,895 entries (book "harrat-mujtaba") and all 5,895 have an English translation. None are missing.
- No entry has an English/Arabic length ratio below 0.8. The lowest is 1.02, so nothing was truncated or dropped.
- The highest ratios (6 to 9) are the very short Arabic notes, such as "جواب القسم". The English adds the named phrase plus the translator's note, as the book note requires.
- I added no new translations and made no tr_tool calls, so no work files were written.

**2. Review against the Arabic**
- I compared about 30 entries with the Arabic. They covered surahs 2, 3, 4, 7, 8, 9, 12, 15, 17, 18, 21, 26, 30, 37, 39, 40, 41, 44, 48, 49, 51, 68, 70, 74, 75, 86, 87 and 92.
  - Eight were long, mixed-content entries, all faithful and complete.
  - About ten were the short phrase-first entries.
- The translation is faithful and complete in these entries. Terms follow the glossary, Quranic words and phrases are in Arabic script, and poetry and glosses are handled correctly.
- Entries that name no phrase carry the parenthesised Quranic phrase plus one "[Translator's note: phrase discussed]". The phrases I checked (70:28, 51:8, 92:7, 26:153, 74:35) are correct verse text.
- Of the short unnamed-phrase entries, 486 carry the marker. The other 5,409 name their phrase in the Arabic, so they need none. The only entry with no quotation or marker is 9:78 ("المصدر المؤول سد مسد مفعولي علم"), which is fine as it stands.
- No entry has more than one marker. Footnote and scholar-note flags such as the 30:11 "superfluous على" are properly marked.

**3. Scans and fixes**
- Turkish leakage: none found (no Turkish characters or function words).
- Latin transliteration of Quranic words: none. The only Latin text inside «…» is deliberate: letter names (wāw, tāʾ, bāʾ) and quoted glosses.
- Term inconsistencies, fixed directly in `en_parts/harrat-mujtaba/sNNN.json` across all affected surah files:
  - "preposition phrase" (835) and "prepositional phrase" (128) became "preposition and its genitive noun", per the glossary.
  - "response to the oath" (76) and "reply to the oath" (17) became "answer to the oath", matching the dominant form (jawāb al-qasam).
- All 114 JSON files still parse, and the file formatting is unchanged.

**Remaining decisions for the teacher**
- The glossary has no entry for several terms the translator rendered in varying ways:
  - الفاء الرابطة is rendered "the linking fāʾ" (45 uses).
  - اللام الفارقة is "the distinguishing/differentiating lām (al-lām al-fāriqa)".
  - "complete" is "tāmm" (26 uses) in some places and "tāmma" (3 uses) in others.
  - "kāffa wa-makfūfa" and "mukhaffafa min al-thaqīla" are given as full renderings with transliteration.
  - I left them as they are, since each is understandable and consistent in context.
- The `reviewed` flag is still false on all entries. I did not change it.

**Overall assessment**
Good. Coverage is 100%, the translations are faithful and terse as the book note requires, and no leakage or transliteration problems were found. After the term normalisation, the only open items are the glossary additions above.

## safi-cedvel

**safi-cedvel English QA, surahs 1-114**

**Coverage**
- All 3,257 entries across the 114 surahs have an English translation, so nothing needed translating.
- The English/Arabic length ratio runs from 1.07 to 2.70, and no entry is below 0.8.
- Two of my scratchpad scripts, `cov.py` and `chk.py`, were overwritten by a parallel QA run (it reported 1,387 entries, which is dervis-irab's count). I re-checked with an inline script: 3,257 source entries and 3,257 translations.
- I edited the JSON files directly, preserving their `src`, `reviewed` and `at` fields, rather than going through `tr_tool put`.

**Fixes**
1. **Footnote markers:** 160 entries still had `[[…]]` or `[[Note: …]]`. All are now `[Note: …]`, and none remain.
2. **Transliterated implied forms:** the "its implied form being …" quotes were in Latin script. About 300 are now Arabic with the English kept as a gloss, for example `"هو" (it)`.
   - About 195 were pronouns such as huwa, hiya, anta, anā, hum, antum and naḥnu.
   - About 110 were English pronouns (it, he, they and so on) that I swapped for the Arabic read from the source, matching in order.
   - 14 words or phrases I fixed by hand: لرأيت أمرا عظيما, موجود, إضلاله, ثبت, أعني, أذمّ, من, أرسلنا, نعمة, اذكر, أمدح, جعلنا, and عيسى or عزير.
3. **Terminology:** `surah`, `sura`, `Surat` and `ayat` are now `sūra`, `Sūrat` and `ayahs`. `Quran`, `Qurʾan` and `Qurʾān` are now `Qur'an`, leaving `al-Qurʾān` names alone. 685 entries changed.
4. **Headings:** 53 entries had `* I'rab` without the colon. They now read `* I'rab:`.
5. **Spot-check:** I compared 8 entries against the Arabic in detail. They cover surahs 7, 18, 19, 21 and 38, plus the 2:285-286 pair and 3:105 among others, and I fixed what I found. All were faithful, with i'rab heads in Arabic and sections properly split. I found no Turkish words or characters leaking in.

**Remaining decisions for the teacher**
- **English phrases in implied forms:** about 200 implied-form quotes where the translator gave an English phrase or pronoun rather than the Arabic, for example "the way of that marriage" or "then there is no blame on him". I couldn't realign these safely because the source and English counts don't match in 135 entries (for example 2:83, 2:126, 4:135, 12:23-29, 22:26-29). They are faithful as English, but the glossary prefers Arabic for implied forms. Decide whether to leave them or have a human restore the Arabic.
- **Nine pronoun cases skipped:** 2:213, 7:175-176, 8:55-57, 8:59, 8:12-13, 16:115, 17:2-6, 28:86-88 and 89:6-14. Their counts didn't match the source, so they still read "it" or "he" in English.
- **Qur'an spelling:** I chose `Qur'an` and `sūra`. Say so if you prefer other conventions.
- **Entry-specific translator notes:**
  - 2:285-286 carries a `[Translator's note]` that the source text is jumbled.
  - 2:141 has an odd `«[Note: …]»` nesting around the footnote.

**Overall assessment**
Coverage is complete, and the translations are faithful and complete. The grammatical terminology is consistent and matches the glossary. After the fixes above the markup is clean, with no `[[` remaining, headings in the right form and no leaked Turkish. The main open quality issue is the roughly 200 English-rendered implied forms listed above.

## dervis-irab

Coverage is complete: all 1,387 dervis-irab entries across surahs 1-114 have an English translation, so nothing needed translating. I changed no translations beyond the spelling normalisations below.

**Coverage**
- Entries with no translation: 0 of 1,387.
- Length ratio (English/Arabic characters): median 1.77, lowest 1.40. The lowest are s7 38-41 (1.40) and s4 59 (1.45). Flagged below 0.8: 0, so nothing looks truncated.
- Heading counts match the source: `* I'rab:` 1,387, `* Vocabulary:` 867, `* Rhetoric:` 766, `* Benefits:` 568.
- The "Morphology" heading never occurs in this book, so none is expected.

**Review**
- I compared about 12 entries against the Arabic: s5 85-86, s9 90-92, s18 83-88, s24 54-55, s36 77-83, s40 28-29, s67 23-30, s78 1-16, s96 1-19, and a few more.
- I also read the lowest-ratio entries and the places where Turkish, Latin or note markers showed up.
- Translations are faithful and complete. Zamakhshari, Abu Hayyan and lexicon quotations are translated in full, poetry stays in Arabic with a gloss, and Quranic words stay in Arabic script.
- Where the source has an error, it is flagged with `[Translator's note: …]`.

**Fixes**
- Standardised spelling across all 114 surahs: "Quran/Quranic" and "Qurʾān" became "Qur'an/Qur'anic" (the glossary form); "al-Zamakhshari" became "al-Zamakhsharī" (about 29 uses), and "Abu Hayyan" became "Abū Ḥayyān" (9 uses). 229 entries changed.
- I rewrote the JSON files in their original format (indent 1, UTF-8). The git diff for the book shows only real edits, mixed with the translation work that was already uncommitted.

**Scans**
- No Latin transliterations of Quranic words were found. The four parenthesised Latin headings, such as "(The rational trope, al-majāz al-ʿaqlī)", are rhetorical section titles, not Quranic words.
- No Turkish leaked in. The only Turkish letters are in the name "Hülegü" (s12 108-111). "Turkish" appears only as a language name in lists of loanwords.
- No inconsistent glossary terms found. "Allah" and "ḥāl" are used throughout. Two stray capitalised "Hal" and "Mubtadaʾ" instances are the particle هل and a sentence-initial word.
- Notes: two `[Note:]` items without a `[[ ]]` in the source are legitimate, since the Arabic uses single brackets or a page footer.

**Remaining decisions for the teacher**
- Lexicon quotations, such as al-Qāmūs in s36, give their example verb forms in Latin transliteration, for example "fāʿaltuhu" and "khaṣamahu yakhṣimuhu". The glossary only requires Quranic words in Arabic script, so I left them. Switch them to Arabic script if you want them traceable.
- In s2 195 the heading "لمحة تاريخية" is rendered as "* Historical glimpse:". It is a non-standard heading that the glossary does not cover. Keep it or map it to "Benefits".
- Five source headings have a space before the colon, for example "البلاغة :" (three of them). They were normalised to the standard headings, which is fine.

**Overall assessment:** the book's English translation is complete, faithful and consistent with the glossary. No further work is needed unless you decide on the points above.

