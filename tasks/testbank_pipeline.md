# Question-bank pipeline (one chapter at a time; levels run in parallel)

Owner: "quality is something we don't compromise." A chapter is accepted ONLY when a FRESH independent
reviewer finds nothing substantive (see Acceptance). Read `tasks/testbank_brief.md` (authoring rules learned
from the L1W1 pilot) before anything else. Pilot reference: `portal/testbank/L1W1.json` and `portal/testbank/parts/L1W1/`.
Working dir: `/Users/ahmedugur/Documents/Claude/Projects/Quran Arabic/portal`. No paid APIs; every agent writes its own content.

## Step 0 - Topics (lead does this, per chapter)
Read the chapter's lecture: `python3 -c "import json;print(json.dumps(json.load(open('lectures.json'))['L<n>W<k>'],ensure_ascii=False,indent=1))"`.
Topics come from the lecture sections (index = `section`). Fold "Why does this matter / introduction" sections into the
next real topic, and keep the final "Recognition / Applied exercise" section as its own mixed-recognition topic.
Target 4-6 topics. Decide a topic id (t1..t6), the section index it links to (the student gets a link to it), and a
2-sentence scope. Also read the lectures of the PRIOR chapters (all earlier weeks, and earlier levels) so you know what
a student may already be asked about (a question may use anything taught in this or an earlier chapter, never later ones).

## Step 1 - Author (parallel agents)
Pool target per chapter: 100-200 questions, i.e. about 24-30 per topic (use the higher end for dense chapters
such as case endings, weak verbs, conditionals, derived forms). One agent writes at most 15 questions: split a
topic into batches `t1a.json` (15) and `t1b.json` (the rest) so quality stays high. Each batch file is
`testbank/parts/<L#W#>/<topic><batch>.json` = `{"topic": {...same topic object in every batch of that topic...}, "questions": [...]}`.
Question ids `L#W#-<topic>-NN`, unique across batches (batch b continues numbering). The author prompt must include:
- the full format spec (docstring of `testbank_tool.py`) and `tasks/testbank_brief.md` rules, verbatim;
- the topic's lecture section text, the scope sentence, what earlier chapters taught, and the ayahs ALREADY USED in
  the chapter so far (to avoid repeats; max 2 uses of one ayah in the chapter);
- the distinct question types to cover and a difficulty split of about 40/40/20 percent;
- real Quranic ayahs only (quote is snapped to Uthmani by the tool); explanation (`why`) for EVERY option in en+tr;
  `topic.rule` en+tr = the hint = the lesson's rule in plain words WITHOUT echoing words/distractors of any question;
- the agent must run `python3 testbank_tool.py part <file>` until 0 errors;
- final reply of 3 lines max.
Run the batches of a chapter in parallel; different chapters of the level may run in parallel too (keep to ~10
concurrent agents). Then `python3 testbank_tool.py assemble <ch>` and `validate <ch>`.

## Step 2 - Independent review (fresh agent, has NEVER seen another review or the authoring prompt)
Prompt template (fill the chapter id; include the chapter policy sentence if the chapter has one):

> You are an expert reviewer of classical Arabic grammar (nahw) and Quranic i'rab, and a fluent Turkish editor.
> Review `portal/testbank/<ch>.json` (read-only; do NOT edit it). Format spec: docstring of `portal/testbank_tool.py`.
> Authoring rules it must follow: `tasks/testbank_brief.md`. Lesson content it must stay inside: `portal/lectures.json`
> key '<ch>' plus the earlier chapters (a question may use only what this and earlier chapters teach). Judge strictly.
> For EVERY question check: (1) the marked-correct option is correct and is the ONLY defensible answer (report words
> scholars read differently, and any second defensible option); (2) every wrong option's `why` is true and specific,
> the correct `why` states the right rule, nothing contradicts the stem or the lesson; (3) every Arabic word the
> stem/options refer to is inside `quote`, the ayah reference is right (check against `Irab Kitaplari/_kelime/qurancom.json`)
> and the stem's glosses are right; (4) no knowledge from a LATER chapter is needed; (5) Turkish natural, correct terms,
> same meaning as English; (6) topic `rule` hints accurate and not leaking answers; (7) stem type matches option type;
> (8) no two questions test the same word in the same way; (9) difficulty labels plausible; (10) within the chapter, the same
> grammatical point is treated the same way everywhere.
> Report only real problems, one per line: `<id> | severity (wrong-answer / ambiguous / explanation-error / out-of-scope /
> hint-leak / turkish / duplicate / minor) | problem | fix`. Finish with the count of fully sound questions and a one-line
> verdict. Write the list to `portal/testbank/reviews/<ch>_review<N>.txt` and reply with it (max 60 lines).

## Step 3 - Fix
A fixer agent (may be the author of that chapter, resumed) fixes EVERY finding (not only the severe ones), following the
rules. Replacement questions must be new questions on different words/ayahs. Then `part` on each file, assemble, validate.

## Step 4 - Fresh review again
A different, fresh reviewer (Step 2 template, next N). Rewritten questions are never trusted until a fresh reviewer
has read them. Repeat Step 3-4 until Acceptance.

## Defining `duplicate` (so review rounds converge without lowering the bar)
A duplicate is two questions that test the same word/ayah in the same way (same ask, same kind of distractors), or one
frame/word overused (more than 3 uses of one very frequent word such as لَا فِي إِلَىٰ قُلْ; 7 questions on one frame).
The frequency limit counts only questions where the word is the TARGET (the word the question is about / the
correct option). A frequent word that merely appears as a wrong option or inside a quote does not count. Re-using a word to test a different skill is NOT a duplicate. A narrow chapter will naturally touch the same words; vary
the ask and the distractors. Reviewers must apply exactly this definition.

## What a hint-leak is (reviewers must apply exactly this)
The hint is the chapter's rule (see the end of tasks/testbank_brief.md). Restating the rule is intended, so a recall
question whose correct option matches the hint is NOT a leak. Report hint-leak only when the hint names a specific word,
ayah or distractor from a question, or states the final answer to an application question.

## Acceptance
Latest fresh review has NO findings of severity wrong-answer, ambiguous, explanation-error, out-of-scope, hint-leak,
turkish or duplicate. `minor` findings are fixed too if cheap, otherwise logged. The validator must report 0 errors,
pool size must be 100-200, topics balanced (no topic under 15 questions), every ayah used at most twice, and the
correct-answer position balanced (no position over 35 percent). Record the result in
`tasks/testbank_progress_L<level>.md`: chapter, pool size, review rounds, counts of findings per round, open minor items.
If a chapter fails to converge after 4 review rounds, STOP on that chapter, log what keeps failing, and continue with the next.

## Reporting
Each lead keeps `tasks/testbank_progress_L<level>.md` current and ends with a table of all 14 chapters (status, pool,
rounds). Do not touch `server.py`, `index.html`, `tests_api.py` or other levels' files.
