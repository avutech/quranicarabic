# Blind independent mapping adjudication

Reviewer: `audit-framework-blind`. Model: GPT-6, Codex session; exact backend variant is not exposed. Date: 2026-10-10. No other reviewer reports or vote files were read before deriving these conclusions. Complete current Arabic, Turkish, English and Quran/meaning context were read through `mapping_review.py case`; published translator notes were visible as immutable case content but were not treated as independent source proof.

## Nahhas meanings: current 4:176

**Vote: INTRODUCTION, target surah 5 introduction. TR/EN: FOLLOWS_SOURCE.**

The entry transmits a general statement from ʿAlqama distinguishing Quranic address formulae by place of revelation. It does not explain the inheritance ruling at 4:176. The local downloaded original has this entry between the ending al-Nisa discussion and 5:1, but its ayah metadata repeats the current error and cannot prove placement.

The [complete primary-book transcription](https://www.arabic-keyboard.info/books/ar/read-book/معاني-القرآن-للنحاس) supplies missing chapter boundaries: its al-Nisa exposition ends, then the al-Ma’idah chapter heading appears, then this statement, then the numbered exposition of 5:1. This establishes an introduction belonging to surah 5. Attaching it to 5:1 would imply verse-specific content that the source does not claim. The complete Turkish and English texts both follow the same source statement. No rewriting is needed. The old tafsir.app 4:176 URL failed with HTTP 503 during retrieval; it was not used to settle the target. Evidence here is a book transcription, not a separately inspected Nahhas printed scan.

## Mekki: current 5:68

**Vote: REMAP, target 5:64–64. TR/EN: FOLLOWS_SOURCE.**

I visually inspected the local original scan, volume 1, PDF page 313 (one-based), printed page **237**. Item **713** is explicitly labelled ayah **64**. It contains the whole current entry: the grammatical discussion of `ما أنزل` governed by `وليزيدن`, followed by `كلما`, `أوقدوا`, and `أطفأها`. Neighboring numbered items are ayah 61 above and 69 below; these are discrete commentary items, not a continuous range.

Quran 5:64 contains both discussed clauses. Ayah 5:68 repeats the first clause but has no fire-kindling/extinguishing conditional, so matching the repeated opening alone produces a wrong placement. The original printed ayah label resolves the repeated-phrase ambiguity. The current metadata says printed page 232; that metadata was not relied upon, because the directly viewed scan prints 237. Both translations follow all clauses in the same source entry. Their existing notes mention 64, but scan and Quran evidence independently establish the result.

## Recording and scope

Votes use full current SHA-256 values for Arabic, Turkish, English and association identity supplied by `mapping_review.py case`. Submitted vote payloads are `/tmp/blind_vote_4.json` and `/tmp/blind_vote_5.json`; the persistent vote tool stores its own evidence and hashes. The Mekki scan SHA-256 is recorded below. These are independent proposals only: no book text, translations, references, or served associations were edited or applied.

Mekki volume-1 PDF SHA-256: `d68b2f7eac5624fb624ff165bc7f04f704799f17629b918e459b3eb92894bb75`.
