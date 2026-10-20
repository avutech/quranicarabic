# Question-bank authoring rules (learned from the L1W1 pilot review, 2026-10-17)

Pilot result: independent review judged 74/100 sound on first draft. Every rule below prevents a flagged defect.

1. **Every word the stem or an option refers to must be inside `quote`.** (3 questions named words outside the quote.)
2. **Stay in scope.** Only use grammar the chapter (and earlier chapters) teach. No participles, relative pronouns, demonstratives, numerals or masdars as distractors in L1W1-style intro chapters; use plain nouns/verbs/particles. Later chapters may use what earlier chapters taught.
3. **One defensible answer.** Avoid words/ayahs scholars read differently (e.g. 55:6 النَّجْم, 95:1 التِّين). Prefer unambiguous words.
4. **Stem and answer type must match** ("which statement" => options are statements; "which word" => options are words).
5. **Fused clitics (وَ فَ لِ بِ كَ)**: pick ONE policy per chapter and state it in the topic rule; never treat the same fused word as separate in one question and joined in another.
6. **Topic `rule` (the hint) must teach the rule without echoing any question's words or distractors.** Do not list example words and do not list the false cues used as distractors.
7. **Explanations must not contradict the lesson or the correct option**; no loose asides about other words.
8. **Turkish**: zaman (tense) not kip (mood) for time; natural phrasing; same meaning as English.
9. Avoid pairs of questions testing the same word/ayah; max 2 uses of one ayah per topic.
10. Quote must not start/end mid-word (a prefix like وَ is part of the Uthmani word); ayah-final words are fine now (matcher fixed).

## Quality bar (owner: "quality is something we don't compromise", 2026-10-17)
Per chapter pipeline: author per topic -> `testbank_tool.py part` -> assemble/validate -> independent review -> fix -> FRESH independent review -> fix ... repeat.
A chapter is accepted ONLY when a fresh review reports no wrong-answer / ambiguous / explanation-error / out-of-scope / hint-leak / turkish / duplicate findings.
Rewritten questions are never trusted until a fresh reviewer has read them. Reviewers must not have seen earlier reviews.

## More rules from L1W1 review 3
11. **Turkish genitive/terms**: ismin (not isimin), muzâri' spelled one way throughout (use "muzâri" as the lesson does), "kelimenin türünü belirlemez" (not "kısmı belirlemez"), "Üçü/Dördü birden ... değildir" for "none of the N", no repeated words. Check every Turkish `why` reads as correct standard Turkish.
12. **Tense wording after a conditional**: a madi (past-form) verb after إِذَا / إِن etc. can carry future meaning (110:1-2). Say "past form (madi)" not "action already happened", unless the ayah is plainly narrative.
13. **"Next word" claims** in a `why` must be true for THIS ayah (check the actual neighbouring word).
14. **Hints (topic rule) must not contain a phrase that is the answer to a question** (e.g. "connective tissue of the sentence").
15. **Generic distractors** such as "both a noun and a verb" need a word-specific sentence in their `why`, not an identical sentence every time.
16. **Duplicates** (frequency counted on TARGET words only, not on distractor mentions) means the same word/ayah asked the same way with the same kind of distractors. The same word may appear again if it tests a different skill. But do not build 7 questions on one frame ("خَلَقَ ٱلْإِنسَـٰنَ"), nor more than 3 uses of one frequent word (لَا, فِي, إِلَىٰ, قُلْ) in a chapter.
17. **Frequent function words** (لَا فِي إِلَىٰ مِنْ) are tempting; spread particle questions over many different particles the lesson lists.

## Rules from the Level 3 lead (lecture defects)
18. **If the lecture is imprecise or wrong on a point** (e.g. hamza called a weak letter, 'forbidden after lā al-nāhiya', loose diptote definitions, examples outside the Qur'an), test only the safe, classical, uncontested core and avoid the defective claim. Report the defect in the author's reply so it can be fixed in lectures.json.
19. **Diptote, derived-form and pattern questions** use only unambiguous Qur'anic words whose classification every classical source agrees on.

## Hint = the rule (owner's design) - what counts as a hint leak (clarified after L1W1 review 5)
The hint IS the chapter's rule, in plain words; students pay a small score cost to see it. So a pure recall question
("what defines a noun?") may legitimately restate the hint, and a reviewer must NOT report that as a leak.
A `hint-leak` finding is only: (a) the hint names a specific Qur'anic word, ayah or distractor used in a question
(e.g. an example word, or a false cue that is the wrong option of a question), or (b) the hint states the final
answer of an APPLICATION question (one that asks the student to classify/parse a given word) instead of the general rule.
Authors should still prefer application questions over recall; at most about 15 percent of a topic's questions may be pure recall.

## Turkish suffixes on Arabic words (L1W1 review 10)
20. **Do not attach Turkish suffixes to Arabic script words** (no عَن'dan, يَعْلَمُ'nun, حَتَّىٰ'da): vowel harmony on Arabic words is error-prone for authors and reviewers alike. Write "عَن harfi", "يَعْلَمُ kelimesi", "حَتَّىٰ harfinde", or rephrase ("... harfinden sonra gelir"). Same for Latin transliterations: use "Allah'a" style only for Allah.
