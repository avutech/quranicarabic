# Master Exam question blueprint

The Master Exam is the capstone ("level 4"): after all three levels the student should know the topics *collectively*.
A student's attempt has 50 questions, drawn from the pool balanced across the 3 levels, then chapters, then topics.
The pool is 42 chapters x 11 questions = 462 questions, one `parts/MASTER/<chapter>.json` per primary chapter.

## What makes a question a MASTER question (vs a chapter-pool question)
1. **Integrative.** It tests the *primary chapter's* concept AND forces the student to combine it with at least one other
   concept: from the same chapter or from ANY EARLIER chapter (earlier weeks, earlier levels). A chapter-pool question asks
   one thing ("which word is a verb?"); a Master question asks the student to put several rules together.
   Examples of integration (use the primary chapter's concept as the anchor):
   - parse one word fully: category (ism/fi'l/harf) + its role in the sentence + the reason for its form/ending;
   - sentence type (nominal/verbal) + which word is mubtada'/khabar/fa'il/maf'ul + why its ending is what it is;
   - which analysis of a short ayah fragment is fully correct (each option is a different multi-part analysis);
   - find the one analysis in a list that contains an error, and why;
   - "this form looks like X but is Y because ...": two rules that pull in different directions;
   - connect a particle's effect on the following word with the case/mood it causes.
2. **Mostly application, some reasoning.** Difficulty split per chapter slice of 11: about 1 x level 1, 5 x level 2, 5 x level 3
   (Level 1 chapters may use a little more level 1/2; Level 3 chapters more level 3).
3. **Primary chapter = `chapter`; `topic` = one of THAT chapter's topic ids** (see `portal/testbank/designs/<chapter>.json`; L1W1 has t1-t5).
   Spread each chapter's 11 questions over at least 3 different topics. The topic's rule is shown as the hint, so choose
   the topic whose rule best helps with the question.
4. **Allowed knowledge** = the primary chapter and every earlier chapter (use `designs/<chapter>.json` `taughtBefore`, `forbidden`,
   `policy`, `caveats`; lectures in `portal/lectures.json`). NEVER require anything taught later than the primary chapter.
5. **Every example from the Qur'an**: real ayah in `ref`, the words in `quote` (snapped to Uthmani text by the tool). Prefer ayahs that are NOT
   already used in that chapter's own pool (`portal/testbank/<chapter>.json`); no ayah more than twice in the whole Master pool.
6. **Same quality rules as chapter questions** (`tasks/testbank_brief.md`, rules 1-20): exactly 4 options, one defensible answer,
   an explanation (`why`, en + tr) for EVERY option, distractors from real confusions, natural Turkish, no Turkish suffix on Arabic-script
   words, no contested analyses, correct answer position balanced, every Arabic word named in stem/options inside `quote`.
7. Ids are `M-<chapter>-NN` (NN = 01..11).

## File format
`portal/testbank/parts/MASTER/<chapter>.json` = `{"questions": [ ... ]}` (no `topic` object), each question:
`id, chapter, topic, difficulty, ref, quote, stem{en,tr}, options[4]{ar|text{en,tr}, why{en,tr}}, correct`.
`python3 testbank_tool.py part <file>` validates and snaps quotes; `python3 testbank_tool.py check MASTER` assembles `MASTER.json`
and prints pool statistics (400-600 questions; at least 8 per chapter).

## Review and acceptance
Per level slice (`M-L<level>W*`), a fresh independent reviewer per round; accepted when a fresh review has no wrong-answer,
ambiguous, explanation-error, out-of-scope, hint-leak, turkish or duplicate finding. Review files:
`portal/testbank/reviews/MASTER-L<level>_review<N>.txt`. The Master Exam is published to staging only when all three level slices are accepted.
