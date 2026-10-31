# Status verified — 2026-10-12

All three most recent agents have finished; none is currently reviewing.
Current exhaustive coverage464/182,167units with both independent reviews:
0.2547%,441agree,23ledger cases require adjudication,181,703units missing
one/both reviews.73/73surah1 book entry units have current double reviews;
335meaning units and56book/ayah lookup units have current double reviews.
The6old stale receipts remain listed as historical problems, but fresh current
receipts cover all3 affected entries; do not edit old hashes.

13resource52/surah2 disputes were adjudicated:all13correct ayah associations,
no remaps. The original disagreements concern wording adequacy. Exact printed
edition behind resource52 remains unauthenticated, original_source_verified=false.
The progress tool does not yet consume these adjudications, so23ledger cases
must not be described as23unresolved mapping errors. Reports:
`tasks/MEANINGS_52_S002_ADJUDICATION.jsonl`, `_STATUS.json`, `_SOURCES.json`.

Latest28lookup partition completed both blind passes. Findings/proposals include
Mekki missing routes at1:4 and1:6, Celaleyn1:1 intro, and source-evidence dispute
at empty Nahhas-meani1:7. No content/mapping changes or deployment.
NEXT: assign remaining42surah1 lookups in Semin/Safi/Dervis/Daas/Harrat/Muyesser
with two blind passes; resolve remaining source/evidence disagreements; continue
full surah2 remaining resources/books/lookups. Reconcile external translation
changes without accepting or silently reverting them; preserve baseline. Refresh
full_coverage status and handover after actual progress, never infer completion.

---

<!-- LIVE_CHECKPOINT_START -->
# Current continuation checkpoint — 2026-10-11

- Exhaustive current reviews:pass1=433,pass2=433;
  433/182167 units double-read
  (0.2377%).
  413 agree;
  20 require adjudication. Accuracy not certified.
- Active workers:remaining_fatiha_pass1/pass2 each ALL21 Akhfash/Zajjaj/Nahhas
  surah1 lookups, then fresh independent rerereads of stale entries1:3,1:26,1:30.
  meaning52_dispute_adjudication independently investigating all13 resource52/
  surah2 disagreement cases, distinguishing correct association from content issues.
- ROOT full current stale-case rereads saved for Mekki1:26 (disjoint1:2+1:4)
  and Ukberi1:30 (1:1). These are supporting evidence, not configured receipts.
- ROOT reread ALL7 Muyesser current book/ayah displays in AR/TR/EN, saved
  `tasks/ROOT_MUYESSER_LOOKUPS_S001_REVIEW.jsonl`:7supporting MATCH reviews,
  no omitted commentary detected from any of the7 source entries. Authenticated
  staging rendering not verified; strong-model double reviews still required.
- All102,422 current merged/part readings compared:4,027differences now,
  in `mapping_audit/reconciliation_2026-10-11/current_merged_part_discrepancies.json`.
  Never silently rebuild or treat current parts as approved content changes.
- Whole-corpus exact neighboring-entry append scan found1candidate:
  Zajjaj1:1 mergedEN = current1:1 EN(8,312chars) + blankline + current1:2
  EN(3,109chars),total11,423chars. Report
  `verbatim_neighbor_append_candidates.json` in same reconciliation directory.
  Blind lookup worker also independently flagged this served-reading mismatch.
  Needs source/association resolution; no source/reading edits applied.
- NEXT:finish three current assignments, refresh status; keep old stale evidence
  and baseline; complete missing refreshed receipts; schedule remaining70surah1
  lookups (10books*7aya) with2blind passes. Then sequential remaining surah2
  books/meanings/lookups. Read ALL units; no sampling. Printed-source verification,
  expert uncertainties and signed-in staging remain separate unfinished gates.

ROOT completed ALL3 current stale-case full AR/TR/EN supporting rereads.
Akhfash entry:1:3 original12157 AR+16031TR+18958EN chars read in consecutive
untruncated chunks; current1:1–3 retained, evidence
`tasks/ROOT_STALE_AKHFASH_S001_REVIEW.jsonl`. Mekki disjoint1:2+1:4 and Ukberi1:1
are saved separately. Configured agents now independently refreshing these3;
root supporting reviews do not replace required receipts or approve text edits.
Lookup pass1 completed all21:19MATCH,1displayedEN mismatch,1UNSURE emptyZajjaj3.
No source/reading/mapping edits. Refresh counts after pass2/checkpoints.

Latest regenerated status:433/182,167two-pass units (0.2377%),413agree,
20need adjudication,181,734missing reviews. All21 lookup cases now double-read.
Next assignments explicitly queued for BOTH book reviewers after stale3 refresh:
ALL28 Nahhas-meani/Mekki/Ukberi/Celaleyn surah1 lookups (7each), independent
blind passes. The remaining6 books'42 lookups follow afterward. Third agent
continues independent adjudication of all13 resource52 disputes.

<!-- LIVE_CHECKPOINT_END -->

# Latest active work checkpoint — 2026-10-11

Current validated exhaustive coverage412/182,167units with both reviews (0.2262%):
393agree,19require adjudication,181,755missing one/both passes. Six stale receipts
remain excluded. Refresh status before reporting because agents save incrementally.
Remaining Fatiha entry reviewers finished all17each; therefore all73 Fatiha
entries have recorded two passes, but3 changed entries remain stale (70current).
Resource52/surah2 blind pass2 finished286:273MATCH,7MISMATCH,6UNSURE; these
flagged translation semantic issues do NOT imply wrong-verse remapping. Pass1
had286MATCH, so13cases require adjudication under content freeze. Original edition
unverified; no content fixes authorized or applied.

Active reviewers `/root/remaining_fatiha_pass1` and pass2 now each reviewing
ALL21 surah1 lookups for Akhfash/Zajjaj/Nahhas-irab, blindly,7each. No sampling.
Root reread full current Mekki entry:1:26 AR/TR/EN and saved supporting stale-case
review `tasks/ROOT_STALE_MEKKI_S001_REVIEW.jsonl`: disjoint1:2+1:4 remains
proposed; stronger independent refreshed receipts required. No original receipts
or baseline hashes replaced. Continue stale Akhfash/Ukberi full rereads, then
configured refreshes; finish all remaining book/ayah lookup partitions and broader
corpus. No content, mapping or deployment changes.

---

# Active continuation — 2026-10-11

Owner said “let's continue”; audit resumed without accepting external content
changes or reverting/rebuilding/deploying anything. This block supersedes active
assignment statements below.

Three fresh blind agents requested gpt-6-astra/max, fork_turns:none:
1. `/root/remaining_fatiha_pass1`: ALL17 remaining surah1 entries,
   Semin7/Safi7/Dervis2/Daas1, independent pass1.
2. `/root/remaining_fatiha_pass2`: same ALL17, independent blind pass2.
3. `/root/meanings52_s002_pass2`: ALL286 resource52 meaning cells surah2,
   independent blind pass2; original pass1 is already complete.
They write incremental `tasks/EXHAUSTIVE_*.jsonl`, never read peer/root findings,
never alter content or mappings, and must read large entries in complete chunks.

ROOT reconciliation work: all102,422 current TR/EN records checked against
current Arabic SHA1, zero missing/stale source provenance. Snapshot of ALL2,048
changed readings saved in
`irab_library/mapping_audit/reconciliation_2026-10-11/changed_readings_snapshot.jsonl`
with previous baseline text hash, current text hash, and full current record.
`summary.json` records1,067TR and981EN changes. Original baseline preserved.
Provenance agreement does not mean external content edits are accepted or correct.
Root's attempted combined display of stale case payloads was truncated; no new
full-payload semantic review was claimed for those cases.

NEXT ROOT: fully reread current stale cases entry:1:3/Akhfash,1:26/Mekki,
1:30/Ukberi in consecutive untruncated chunks; preserve old receipts and collect
fresh independent configured reviews before closing them. Pending unresolved
source/mapping decisions remain open. After workers finish, assign all remaining
surah1 book/ayah lookups (13books*7ayahs) with two blind passes, then sequential
surah2 remaining book/meaning/lookup partitions. No sampling. Refresh counts with
`python3 portal/full_coverage.py status` and append actual checkpoint here.
Do not rerun a script that overwrites the preserved baseline manifest/inventory.

---

# 2026-10-11 reconciliation: supersedes earlier unchanged-content statements

Read `tasks/HANDOVER_CHATGPT.md` in full: unchanged original translation handover,
no git diff, not an updated account of continued audit work.
Current git HEAD remains1d219f5. Do not attribute existing uncommitted changes
solely from git status; compare the preserved audit baseline.

Evidence of external/Claude-labelled work since our baseline:
-704 protected translation-part files changed:362TR,342EN. No protected source,
 mergedTR/EN,word or catalog file differs from the baseline.
-Text SHA256 comparison against all51,211 preserved inventory entries finds
 1,067TR+981EN changed texts affecting1,763 unique entries. These records carry
 Claude labels;820 changed readings have date2026-10-11 and1,228 date2026-10-10.
 This includes content edits, conflicting with owner's current content freeze.
 Do not revert, rebaseline, rebuild or deploy automatically. Preserve evidence.
 Detail:`irab_library/mapping_audit/external_content_changes_2026-10-11.json`.
-Claude audit_full ledger now records51,211p1 and1,913p2 receipts. Its actual
 hash-current coverage is51,159p1 and1,843p2;52p1 need revalidation. This is
 older protocol evidence, not the mandatory exhaustive blind review protocol.
 `faith_tool.py` still selects pass2 by flags plus PASS2_SAMPLE; therefore this
 ledger cannot establish no-sampling two-pass completion.
-Our exhaustive current coverage:109/182,167units with two independent passes
 (0.0598%);103agree,6need adjudication.395p1,109p2 valid current receipts.
 Six stale receipts:both passes for entry:1:3,entry:1:26,entry:1:30, following
 changes to translation text. Do NOT simply update receipt hashes; reread changes.
-No new commit observed. Staging was not rechecked this turn; earlier342-file
 comparison remains historical, not a claim about newly changed translation parts.

All three previous reviewers completed assignments:book reviewers42/42each;
meaning resource52 surah2 all286p1 complete. Next: coordinate external work and
preserve frozen-content policy, revalidate changed readings and stale receipts;
assign independent pass2 for resource52/surah2; continue remaining surah1 books
Semin/Safi/Dervis/Daas and all non-Farraa lookups, then full corpus. Original-source
verification, disagreements, mapping proposals and signed-in staging remain open.
User asked for status/reconciliation; no external edits undone or authorized here.

---

# Handover to Claude: Quran book-to-ayah audit

Last updated: 2026-10-10 (America/New_York).

## Latest continuation checkpoint (supersedes older counts below)

Latest staging verification: read-only SSH SHA256 comparison of ALL114 source
files plus ALL114 merged Turkish and ALL114 merged English files (342 total)
found **zero differences** between staging and local files. Saved
`irab_library/mapping_audit/staging_content_comparison.json`. This establishes
that current deployed JSON matches audited local JSON; it does not verify the
signed-in rendered UI or resolve the1,988 local merged-vs-part differences.
No server/source files were modified.

- Valid exhaustive receipts: pass1=261, pass2=82.
- Both independent reviews: 82/182167 (0.0450%).
- Agreeing evidence: 78; adjudication: 4.
- Missing one/both passes: 182085. No accuracy certification.
- Root direct supporting reviews: **21 complete entries**, adding all1 Daas
  whole-surah entry1:1–7, MATCH in AR/TR/EN. Evidence
  `tasks/ROOT_DAAS_S001_REVIEW.jsonl`; original source byte-compared.
- Book pass1 reports initial16/16 complete, now executing additional26
  Ukberi/Celaleyn/Harrat/Muyesser units. Book pass2 and meanings52/surah2
  remain active; consult actual receipts for exact current counts.
- Protected content check: all3615 manifest files unchanged. No content,
  mapping or deployment changes.
- NEXT: continue root source review/adjudication; keep three workers busy;
  assign resource52/surah2 blind pass2 when available; complete remaining
  Semin/Safi/Dervis/Daas surah1 entry passes and all non-Farraa lookup passes.
  Regenerate status before reporting. No sampling and no pending units cleared.


**Latest binding scope clarification: NO SAMPLING.** Review every entry,
complete AR/TR/EN readings, all43,652 meaning-resource cells, and every14-book /
6,236-ayah lookup, including no-entry cases. A blind second review is required
for every unit. Batches are sequential partitions of all work, not samples.
Historical15% pass2 scheduling must not be used or counted as completion.

Exhaustive scheduler added: `python3 portal/full_coverage.py build`. Manifest
under `irab_library/mapping_audit/full_coverage/` enumerates **182,167 units**:
51,211 AR/TR/EN entry units,43,652 meaning cells,87,304 book/ayah lookups.
Every unit requires passes1 AND2:364,334 review decisions. The24,004 no-entry
lookups remain explicit review units. Census uniqueness/counts were tested.
`packet KIND SURAH [BOOK_OR_RESOURCE]` emits full whole-partition cases;
large partitions must be processed consecutively with no skipped units.

The exhaustive sweep uses requested gpt-6-astra/max in separate blind contexts.
Latest status checkpoint: **81 units with both independent receipts**,77 agreeing
and4 needing adjudication;203 pass1 decisions,81 pass2 decisions.182,086 units
still lack one or both reviews; two-pass coverage0.0445%. Counts evolve while
agents save incremental receipts. Refresh `python3 portal/full_coverage.py status`
before reporting progress. Review coverage is not source/accuracy certification.

Active parallelism: environment permits4 active agents INCLUDING root.
- `/root/parallel_books_pass1`: blind pass1, initial16 surah1 Nahhas-irab6,
  Nahhas-meani5,Mekki5. Nahhas-irab6 done, proceeding remaining partitions.
- `/root/parallel_books_pass2`: same initial16 blind pass2; Nahhas-irab6 and
  Nahhas-meani5 done, currently Mekki5.
- BOTH book reviewers were instructed to continue after initial16 with ALL
  surah1 Ukberi6,Celaleyn7,Harrat6,Muyesser7 (26 additional units each),
  sequential full partitions; no peer/root conclusions disclosed.
- `/root/parallel_meanings_s002_pass1`: all286 resource52 meaning cells surah2,
  sequential pass1. Current checkpoint120 cells saved; remaining166. Check
  actual receipts for latest. Resource52 surah2 independent pass2 still needs
  assignment when a slot opens. Full repeated context may be factored losslessly
  within a batch; no payload text omitted and every unit explicitly reviewed.
All3 agents requested gpt-6-astra/max with fork_turns:none, preserve content,
save incremental `tasks/EXHAUSTIVE_*.jsonl`. Do not infer unread completion.
Rotate finished slots into next whole partitions. Remaining surah1 books after
these42 new decisions per reviewer are Semin7,Safi7,Dervis2,Daas1; all lookup
partitions except Farraa remain open. Then continue every surah2 book/meaning/
lookup unit in manifest order, not representative samples.

ROOT is directly auditing too:20 complete supporting entry reviews saved:
- `tasks/ROOT_CELALEYN_S001_REVIEW.jsonl`: all7;6 MATCH,1 UNSURE introduction/
  basmala boundary. All7 original DOCX paragraphs byte-compared after numbered
  prefix removal. Original DOCX SHA2560829cedf29a23de64f6238d7fe1896ba24be605f293588136fc9a8b29f709a2d.
- `tasks/ROOT_HARRAT_S001_REVIEW.jsonl`: all6;5 MATCH,1 proposed MISMATCH:
  current1:6 substantively derives نستعين from1:5 after parsing1:6. Proposed
  disjoint1:5+1:6, pending blind original-source adjudication. All6 full original
  local extracted entries byte-compared.
- `tasks/ROOT_MUYESSER_S001_REVIEW.jsonl`: all7;all source/translation mappings
  MATCH. All7 original local extracted entries byte-compared. EN grammatical
  phrasing at1:2 differs but refers to same entry; not an ayah mapping correction.
Root backend model configuration is not exposed, so supporting reviews are
NOT counted as required Astra/max receipts. Configured book workers will review
these partitions blindly. Printed facsimile and signed-in staging remain open.

Next ROOT work: independently audit remaining full small partitions (e.g.Daas1),
then verify source evidence for disagreements without leaking it to blind workers;
keep handover and coverage refreshed. Compare all protected file hashes after
work. No source/mapping modifications or deployment have been performed.

Earlier findings: Farraa1:2 disjoint1:2+1:7; Akhfash1:7 disjoint1:5+1:7.
Zajjaj extra1:3 scope and Farraa lookup interpretations need adjudication.
No mapping proposal applied. Never inflate disjoint links into a continuous range.

Latest owner steering: choose the model; accuracy is the priority and guesses
are unacceptable. Selected **gpt-6-astra / max reasoning** for subsequent
semantic reviewer/adjudicator agent requests, based on current official model
documentation. See `tasks/MAPPING_AUDIT_FRAMEWORK.md` selected-model policy.
Record orchestrator configuration separately from exposed backend identity.
Earlier reviews are preliminary evidence; original-source verification and
blind independent confirmation remain required. No model can promise zero
errors, so uncertainty must remain open and expert adjudication is required
where source evidence cannot resolve a case. No paid bulk API usage authorized.

## Objective and authorization

The owner says the translation job described in `tasks/HANDOVER_CHATGPT.md` is finished. The current objective is to verify that every Arabic book entry is linked to the correct surah and ayah or ayah range, identify mismatches, and develop an audit agent framework to establish the correct mapping with evidence.

The owner initially requested an explanation before starting. They subsequently authorized the full audit: “start working on auditing the match between ayah by ayah for all books, irab, turkish and english translations for each book and ayah meanings.” They explicitly froze all content: “No book context is going to be changed or altered. only the match with ayah.” They authorized an agent decision framework and stronger-model escalation when needed. Mapping proposals and audit artifacts are authorized; no deployment has been authorized.

The owner requested this file so Claude can resume if Codex reaches its limit. Update it after meaningful progress, including unresolved questions, checks, changes, and next steps.

## Work completed by Codex

1. Read `tasks/HANDOVER_CHATGPT.md` and explained the audit scope to the owner.
2. Explained that entries legitimately covering several ayahs must map to the correct range. Not every classical book comments on every verse.
3. Checked local repository status, deployment documentation, relevant API routes, and existing audit artifacts.
4. Verified staging via HTTP and read-only SSH.
5. Created this handover. No source data, application code, branches, or deployments were changed by Codex.

## Verified staging status

Checked on 2026-10-10:

- Site: `https://staging.learnirab.com` responds with HTTP 200 using local `curl`. The web browsing tool could not open it; that was a tool access limitation, not a site outage.
- SSH access works to `root@137.184.56.77` using the existing local key `~/.ssh/quran_deploy_ci`. Do not print or copy private key material.
- Checkout: `/srv/quran-staging`, branch `staging`, tracking `origin/staging`.
- Service: `quran-staging`, active.
- Deployed commit: `1d219f5` — `I'rab library: ayah-to-ayah audit of all 14 books (Arabic/TR/EN), 43 translation fixes, report`.
- The local checkout has that same HEAD commit, but extensive uncommitted work (see below).
- Read-only scan of all 114 deployed source files found **51,211 Arabic entries**.
- Turkish: **zero missing translation part records, zero stale Arabic SHA1 hashes**.
- English: **zero missing translation part records, zero stale Arabic SHA1 hashes**.
- Both merged language directories contain 114 surah files. Their presence was checked; merged content was not exhaustively compared with translation parts.
- `/api/irab-library/1/1` returns HTTP 401 without authentication. The signed-in visual interface was not verified.
- Server checkout had untracked PDF material and a local environment backup; neither was opened or changed.

These checks establish translation record coverage and Arabic hash agreement, **not correctness of every mapping or translation**.

## Existing audit evidence

Existing files include:

- `irab_library/audit/RULES.md`
- `irab_library/audit/REPORT.md`
- `irab_library/audit/summary.json`
- `portal/audit_ayah_match.py`
- `portal/audit_tool.py`
- `portal/audit_report.py`
- `portal/audit_progress.py`

The existing report states:

| Verdict | Recorded count |
| --- | ---: |
| OK | 18,294 |
| TRANSLATION_FIXED | 43 |
| SOURCE_MISPLACED | 27 |
| SOURCE_DEFECT | 61 |
| TRANSLATION_UNFIXED | 0 |
| TEACHER | 0 |
| GAP | 1,105 |

It reports 145 audited chunks across 114 surahs and 19,530 verdicts; zero provenance mismatches in 102,422 translation records and zero guardrail errors after edits. Codex has **not independently rerun that audit or validated its methodology**. The report's detailed misplaced-entry section lists 20 items despite 27 recorded verdicts; understand aggregation/deduplication before interpreting these counts. Do not equate 19,530 verdicts with exhaustive verification of 51,211 source entries.

Examples recorded in that report include `akhfash` at 2:142 discussing 2:143, `mekki-muskil` at 5:68 discussing 5:64, and `semin-durr` at 70:9 discussing 70:10. These are prior report claims, not new independently adjudicated findings.

Some entries mix discussion of different verses or contain the introduction of the following surah. Distinguish extraction/mapping errors, source defects, cross-references, legitimate multi-ayah discussion, and surah introductions. Preserve the original book text and provenance.

## Local state to preserve

At the access check:

- Branch: `main`, reported 36 commits ahead of and 1 behind the locally known `origin/main` (no fetch was performed).
- HEAD: `1d219f5`.
- **778 changed/untracked paths** before this handover: 775 under `irab_library`, 3 under `portal`.
- Many existing Turkish/English translation part files are modified.
- Untracked items include `irab_library/audit_full/`, `portal/adjudicate_tool.py`, `portal/faith_tool.py`, and `portal/b3.tsv`.
- `irab_library/audit_full/` is absent from the staging checkout.

These are pre-existing owner/Claude changes. Do not discard, overwrite, reset, commit, or deploy them without understanding their purpose. The newer full-audit workflow has not yet been inspected by Codex.

## Proposed next steps after owner confirmation

1. Read the existing audit rules, tools, full-audit artifacts, and relevant project instructions before building anything new.
2. Establish what the earlier audit actually covered and what the uncommitted follow-up work has already accomplished.
3. Propose or extend an evidence-backed framework: structural checks, Quran quotation/reference matching, candidate destinations, original-book source verification, and explicit review/adjudication states.
4. Track every entry's review status and preserve unresolved cases. A clean automatic check alone cannot substantiate 100% accuracy.
5. Produce a mismatch register with current mapping, quoted evidence, proposed correct mapping/range, confidence, and adjudication outcome.
6. Keep this handover current throughout the work.

## Binding constraints

Carry forward `tasks/HANDOVER_CHATGPT.md`: preserve `ref` and translation provenance, never silently correct source text, never edit library JSON by hand, no paid APIs for bulk work, no scraping kuranmeali.com, and preserve Quranic Arabic Corpus data and attribution. Read language glossaries before translation work. Production promotion requires the owner's explicit instruction. No deployment was authorized in this session.

## Current audit progress after authorization

- Added `portal/mapping_audit.py`: scans all source entries and meaning cells, reruns deterministic candidate checks into a separate `irab_library/mapping_audit/deterministic/` directory, checks provenance, merged-vs-part text equality, original meal/word cache mapping, and records a protected content SHA256 manifest. It writes only new audit artifacts.
- Fresh deterministic run: 51,211 entries, 3,667 candidate findings (680 high, 88 medium, 2,899 low). These are not confirmed mismatches.
- All 43,652 meal records agree with their cached source; all 6,236 word records agree with the cache. Zero missing/provenance issues in this local scan. **1,988 merged TR/EN readings differ from current part text**, meaning a rebuild/deployment would be needed to serve the latest work, but neither has been performed.
- Protected content manifest covers 3,615 files; scan confirms identical before/after bytes. The first word comparison briefly used swapped tuple fields and falsely flagged all verses; this was corrected and the complete scan rerun. No book data was changed.
- Full-fidelity historical coverage independently measured: 28,291 current complete pass-1 records, 1,507 flagged entries, 5,865 second-pass reviews due, zero second-pass reviews complete. Historical canaries: 2,780 shown / 2,718 detected / 62 missed. Sampling is not 100% semantic certification.
- Added `portal/mapping_review.py`: queue / case / verses / vote / status. Cases expose full AR/TR/EN, reference and Quran/meanings; other judges' votes are withheld by the case command. Votes require current SHA256 hashes (including association fingerprint), reviewer/model identity, Arabic evidence, explicit TR/EN mapping verdicts, canonical-valid destinations, and distinct reviewer agreement. Disagreement/uncertainty escalates. Cross-surah, disjoint targets and surah introductions are supported. No application of proposals is implemented. Identity labels cannot cryptographically enforce blind independent reviewers; orchestrator must enforce that workflow.
- Meaningful decision checks passed: repeated reviewer does not close; disagreement/uncertainty escalates; stale hashes, invalid bounds and missing dimensions reject; cross-surah/introduction valid targets accept.
- `tasks/MAPPING_AUDIT_FRAMEWORK.md` documents agent roles, coverage gates, limitations and escalation policy.
- `tasks/mapping_independent_review.md`: all 20 unique prior misplaced entries independently examined. Five primary remaps, five introductions, two narrow ranges, six mixed entries, one ambiguous mixed entry, one unresolved generic entry. No proposals applied. Distinguish disjoint target sets from broad ranges.
- `tasks/MEAL_MAPPING_REVIEW.md` and `tasks/MEAL_MAPPING_EVIDENCE.json`: complete structural/source-cache audit of 6,236 verses / 43,652 meanings; independent Corpus/Tanzil verse/word numbering comparison. **Confirmed semantic mismatch in resource 210 at 87:14**: repeats meaning of 87:13, also present upstream in cache. Correct original 87:14 resource text has not been located; do not invent/rewrite it or move a duplicate into an occupied 87:13 slot.
- Meal scan found 903 consecutive duplicate pairs, mostly intentional combined verse translations. These are candidates; most are not individually adjudicated. Full independent semantic certification remains open.
- `tasks/daas_mapping_review.jsonl`: complete full-text mapping review of 209 Daas entries in surahs 90–114 (213 expanded ayah associations): 191 MATCH, 18 UNSURE, zero substantiated mismatches. All TR/EN follow their own AR entry. These are first independent reviews, not two-judge completed decisions.
- Added repeatable `portal/mapping_source_compare.py`: all 51,211 entries across all 14 books match original local extracted text/range records, zero differences. This does not validate upstream verse labels against the printed editions.
- Added `portal/mapping_progress.py`: aggregates current independent JSONL evidence, distinguishes pending/stale records, writes `independent_reviews.jsonl` and `progress.json`, and rechecks protected content hashes. `tasks/MAPPING_AUDIT_PROGRESS.md` is the human-readable checkpoint.
- Completed all **133 Semin entries** in surahs90–114: 100 MATCH, 32 proposed range/disjoint mapping corrections, one UNSURE (101:4), zero pending. All399 AR/TR/EN SHA256 hashes validated. Artifacts: `tasks/semin_mapping_review.jsonl`, `tasks/semin_mapping_review_summary.json`, `tasks/semin_mapping_review_notes.md`. These are first-review proposals, not applied corrections.
- Completed all **66 historical fit-flag reviews**, full current AR/TR/EN: 40 mixed-scope proposals needing original-source adjudication;12 correctly anchored fragments;4 misplaced introductions; Nahhas13:20→13:30; Ukberi28:82–83→82; other uncertainty/source-boundary cases. Source fragments are not silently rewritten.
- Strong independent source adjudication resolved **Mekki5:68→5:64 only** using a visually inspected original scan (PDF313, printed237, item713) and **Nahhas4:176→surah5 introduction** using a primary-book transcription chapter boundary. See `tasks/STRONG_MAPPING_ADJUDICATION.md`. Both full-language independent votes are recorded; at initial submission they needed a second independent review. Spawn request selected gpt-6-astra/high, but the child could not independently expose its backend model identifier; its report/votes disclose that limitation. Do not claim model identity from the reviewer label alone.

## Agents / work in progress at this update

- `review_mapping`: completed133/133 Semin pilot and prior20 source cases.
- `meal_mapping`: completed66/66 historical fit flags and all57 resource52 duplicate pairs (50 maximal combined ranges,107 verse-resource records), output `tasks/MEAL_52_DUPLICATE_REVIEW.jsonl`. All50 ranges intentional; zero mismatches/unsure within this set. Other meaning resources/singletons remain open.
- `strong_adjudication`: completed both source-based decisions/votes, report above.
- `audit_framework`: completed209/209 Daas pilot and second **blind** original-source adjudication of Nahhas4:176 and Mekki5:68, output `tasks/BLIND_MAPPING_ADJUDICATION.md` plus independent votes. Both agree exactly with the first source judge: **AGREED_PROPOSAL** for surah5 introduction and5:64 respectively. No mapping applied.
- Current new full-language review register: **408 unique entries**,50,803 without a new full review in this session. Historical28,291 pass1 records are separately preserved and must not be conflated with new independent certification. All3,615 protected file hashes remain unchanged.

## Immediate continuation point

All agents at this checkpoint have finished their assigned batches. Continue unreviewed mapping units and adjudicate32 Semin proposals,40 historical mixed-scope findings and remaining unsure cases against source context. Prioritize843 resource77 duplicate pairs and resource21087:14's missing original record. Two source-based proposals have blind agreement but are not applied. Full audit of51,211 entries and43,652 meaning cells is **not complete**. Preserve source/translation text, review history and existing uncommitted work. Never claim100% accuracy from these preliminary scans. Update this file at meaningful checkpoints.
