export const meta = {
  name: 'testbank-resume',
  description: 'Design, author, independently review and fix the multiple-choice question pools for chapters of Levels 1-3 (quality-gated)',
  whenToUse: 'Build or rebuild the chapter question banks under portal/testbank',
  phases: [
    { title: 'Design', detail: 'topic design per chapter' },
    { title: 'Author', detail: 'question batches per topic' },
    { title: 'Check', detail: 'assemble + validate + acceptance statistics' },
    { title: 'Review', detail: 'fresh independent reviewer per round' },
    { title: 'Fix', detail: 'fix every finding, then re-review' },
  ],
}

const ROOT = '/Users/ahmedugur/Documents/Claude/Projects/Quran Arabic'
const PORTAL = ROOT + '/portal'
const SCRATCH = '/private/tmp/claude-501/-Users-ahmedugur-Documents-Claude-Projects-Quran-Arabic/3d39aad2-2f86-47f5-bedc-112d70e8f82a/scratchpad'
const BLOCKING = ['wrong-answer', 'ambiguous', 'explanation-error', 'out-of-scope', 'hint-leak', 'turkish', 'duplicate']
const MAX_ROUNDS = 6

const ALL = []
for (let L = 1; L <= 3; L++) for (let W = 1; W <= 14; W++) ALL.push(`L${L}W${W}`)
const CHAPTERS = (args && args.chapters) ? args.chapters : ALL.filter(c => c !== 'L1W1')
const idx = c => ALL.indexOf(c)

const DESIGN = {
  type: 'object',
  properties: {
    topics: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, section: { type: 'integer' },
      title: { type: 'object', properties: { en: { type: 'string' }, tr: { type: 'string' } }, required: ['en', 'tr'] },
      rule: { type: 'object', properties: { en: { type: 'string' }, tr: { type: 'string' } }, required: ['en', 'tr'] },
      scope: { type: 'string' }, types: { type: 'array', items: { type: 'string' } }, target: { type: 'integer' } },
      required: ['id', 'section', 'title', 'rule', 'scope', 'types', 'target'] } },
    caveats: { type: 'array', items: { type: 'string' } },
    taughtBefore: { type: 'string' }, forbidden: { type: 'string' }, policy: { type: 'string' },
  },
  required: ['topics', 'caveats', 'taughtBefore', 'forbidden', 'policy'],
}
const AUTHORED = { type: 'object', properties: { file: { type: 'string' }, count: { type: 'integer' }, ayahs: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } }, required: ['file', 'count', 'ayahs'] }
const CHECKED = { type: 'object', properties: { raw: { type: 'string' } }, required: ['raw'] }
const REVIEW = { type: 'object', properties: {
  findings: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'problem', 'fix'] } },
  sound: { type: 'integer' }, verdict: { type: 'string' } }, required: ['findings', 'sound', 'verdict'] }
const FIXED = { type: 'object', properties: { changed: { type: 'array', items: { type: 'string' } }, disagreements: { type: 'array', items: { type: 'string' } } }, required: ['changed', 'disagreements'] }

const COMMON = `Project root: ${ROOT} (code in portal/). Work in ${PORTAL}. No paid APIs: you write all content yourself. Before anything else read, fully: ${ROOT}/tasks/testbank_brief.md (authoring rules 1-19 and quality bar), ${ROOT}/tasks/testbank_pipeline.md, and the docstring at the top of ${PORTAL}/testbank_tool.py (question file format). The finished pilot ${PORTAL}/testbank/L1W1.json shows the expected shape and quality.`

function designPrompt(ch) {
  const earlier = ALL.slice(0, idx(ch)).join(', ') || '(none: this is the first chapter)'
  return `${COMMON}

TASK (Step 0 of the pipeline): design the topics for chapter ${ch}. Read this chapter's lecture: cd ${PORTAL} && python3 -c "import json;print(json.dumps(json.load(open('lectures.json'))['${ch}'],ensure_ascii=False,indent=1))". Earlier chapters (the only grammar a question may rely on, besides this chapter): ${earlier}. Skim their lectures (same command with their keys) so you know what is already taught. If the file ${SCRATCH}/l3/specs/${ch}.md exists, read it too: an earlier lead's draft design with lecture caveats; use it as a starting point, you may improve it.

Produce 4-6 topics from the lecture sections (section = the lecture section index the student will be linked to; fold 'why this matters' intro sections into the next real topic; keep the final recognition/exercise section as its own mixed-recognition topic). For each topic give: id (t1..t6), section index, title en+tr (take from the lecture section title; Turkish must be correct standard Turkish), rule en+tr (THE HINT: the lesson's rule for that topic in plain words, 2-4 sentences, taught accurately, without example words or distractor cues used in questions, never a phrase that is itself an answer), a scope sentence, 6-10 question types to cover, and target = number of questions for the topic (24-30; the chapter total must land between 110 and 150, more for dense chapters). Also return: caveats (any imprecise/wrong claims in the lecture, or contested words, that authors and reviewers must avoid or handle with care), taughtBefore (one paragraph: what earlier chapters + this chapter teach, that questions may use), forbidden (what later chapters teach and must not be needed), policy (chapter conventions that must be applied consistently in every question, e.g. how fused prefixes are counted). Do not write any question files. Reply only with the structured result.`
}

function authorPrompt(ch, d, topic, batch, first, count, used) {
  return `${COMMON}

TASK: write exactly ${count} multiple-choice questions for chapter ${ch}, topic ${topic.id}, batch '${batch}'. Output file: ${PORTAL}/testbank/parts/${ch}/${topic.id}${batch}.json = {"topic": <the topic object below, copied EXACTLY, same in every batch>, "questions": [...]}. Create the folder if needed. Question ids: ${ch}-${topic.id}-NN numbered from ${String(first).padStart(2, '0')} to ${String(first + count - 1).padStart(2, '0')}.

TOPIC OBJECT (copy exactly): ${JSON.stringify({ id: topic.id, section: topic.section, title: topic.title, rule: topic.rule })}
Topic scope: ${topic.scope}
Question types to cover (mix them, vary the ask and the distractors): ${topic.types.join(' | ')}
Read the lecture section first: cd ${PORTAL} && python3 -c "import json;print(json.dumps(json.load(open('lectures.json'))['${ch}']['sections'][${topic.section}],ensure_ascii=False,indent=1))" and skim the other sections of this chapter.
Allowed knowledge: ${d.taughtBefore}
Must NOT be needed (taught later): ${d.forbidden}
Chapter policy to apply consistently: ${d.policy}
Lecture caveats / contested points to avoid or handle with care: ${d.caveats.join(' || ') || 'none'}
Ayahs ALREADY used in this chapter (do not reuse these; any other ayah max 2 uses in the whole chapter): ${used.join(', ') || 'none yet'}

Requirements (all from the brief, restated): every question is on a real Qur'anic ayah (ref 'surah:ayah', quote = contiguous Arabic words of that ayah, not starting or ending mid-word; the tool snaps the quote to exact Uthmani text). Exactly 4 options, one correct, distractors reflect real student confusions. EVERY option has a 'why' in en and tr (correct: why it is right and which rule decides; wrong: specifically why it is wrong). Difficulty about 40/40/20 percent of levels 1/2/3. Correct answer position balanced across 0-3. Every Arabic word the stem or options refer to is inside the quote. Turkish natural and correct (brief rule 11). Accuracy beats quantity: double-check each grammatical claim; if a word is debatable do not use it. Run: cd ${PORTAL} && python3 testbank_tool.py part testbank/parts/${ch}/${topic.id}${batch}.json  until 0 errors. Reply with the structured result (file, count, every ayah ref you used, notes on anything you were unsure about).`
}

function reviewPrompt(ch, d, n) {
  return `You are an expert reviewer of classical Arabic grammar (nahw) and Quranic i'rab, and a fluent Turkish editor. You have NEVER seen any earlier review of this chapter: do not open any file under ${PORTAL}/testbank/reviews/ other than the one you write. Read first: ${ROOT}/tasks/testbank_brief.md (rules 1-19) and the section 'Defining duplicate' of ${ROOT}/tasks/testbank_pipeline.md, and the docstring of ${PORTAL}/testbank_tool.py.

Review ${PORTAL}/testbank/${ch}.json (read-only: do NOT edit it). Allowed knowledge for questions: ${d.taughtBefore}. Must not be needed (taught later): ${d.forbidden}. Chapter policy: ${d.policy}. Known lecture caveats: ${d.caveats.join(' || ') || 'none'}. The lecture: portal/lectures.json key '${ch}' (earlier chapters likewise).

For EVERY question check: (1) the marked-correct option is correct and is the ONLY defensible answer (report words scholars read differently, any second defensible option); (2) every wrong option's 'why' is true and specific, the correct 'why' states the right rule, nothing contradicts the stem or the lesson, 'next word'/position claims are true for this ayah; (3) every Arabic word the stem/options refer to is inside 'quote'; the ayah reference is right (check ${ROOT}/Irab Kitaplari/_kelime/qurancom.json) and the stem's glosses are right; (4) no knowledge from a LATER chapter is needed; (5) Turkish is natural standard Turkish with correct terms and the same meaning as the English (check genitives like ismin, consistent terms); (6) the topic 'rule' hints are accurate and do not leak answers; (7) stem type matches option type; (8) duplicates by the definition in the pipeline doc; (9) within the chapter the same grammatical point is treated the same way everywhere; (10) difficulty labels plausible.
Severity values (use exactly): wrong-answer, ambiguous, explanation-error, out-of-scope, hint-leak, turkish, duplicate, minor. Use 'minor' only for real but harmless polish. Report only real problems; for a topic-hint problem use the id of the topic's first question. Write the list to ${PORTAL}/testbank/reviews/${ch}_review${n}.txt (one line per finding: id | severity | problem | fix) and return the same findings in the structured result, plus 'sound' (number of fully sound questions) and a one-line verdict.`
}

function fixPrompt(ch, d, group, findings, files) {
  return `${COMMON}

TASK: fix review findings in chapter ${ch}, ${group === 'CHAPTER' ? 'chapter-level problems' : 'topic ' + group}. Edit only these source files (never testbank/${ch}.json, it is regenerated): ${files}. Fix EVERY finding below, including minor ones. Where a question changes, rewrite ALL four 'why' texts in en and tr so they stay coherent; replacement questions must be new questions on different words/ayahs/asks (keep the id) and must follow every brief rule; no ayah used more than twice in the chapter and the correct-answer position stays balanced. If you disagree with a finding, do not ignore it silently: list it under disagreements with your reason (the next reviewer will judge). A topic 'rule' (hint) fix must be applied identically in every batch file of that topic.
Allowed knowledge: ${d.taughtBefore}. Must not be needed: ${d.forbidden}. Chapter policy: ${d.policy}. Caveats: ${d.caveats.join(' || ') || 'none'}.
Findings:
${findings.map(f => `- ${f.id} | ${f.severity} | ${f.problem} | suggested fix: ${f.fix}`).join('\n')}
After editing run: cd ${PORTAL} && for f in ${files}; do python3 testbank_tool.py part $f; done  (0 errors required; the quote matcher ignores pause marks). Reply with the structured result (ids you changed, disagreements).`
}

async function runChapter(ch) {
  try {
    phase('Design')
    // The design already exists on disk (testbank/designs/<ch>.json); load it verbatim.
    const d = await agent(`Read the JSON file ${PORTAL}/testbank/designs/${ch}.json and return its content EXACTLY (do not change, reorder or summarize anything) as the structured result.`, { label: `load design ${ch}`, phase: 'Design', schema: DESIGN, effort: 'low' })
    const info0 = await agent(`Run exactly this command and return its complete stdout in 'raw': cd ${PORTAL} && python3 testbank_tool.py parts ${ch}`, { label: `parts ${ch}`, phase: 'Design', schema: CHECKED, effort: 'low' })
    let info = { files: {}, used: [], reviews: 0 }
    try { info = JSON.parse(info0.raw.trim().split('\n').filter(l => l.startsWith('{')).pop()) } catch (e) { /* treat as nothing authored */ }
    const base = info.reviews || 0
    if (base >= 12) return { chapter: ch, status: 'exhausted-needs-human', rounds: base }
    const used = [...info.used]
    const expA = t => Math.min(15, t.target)
    const expB = t => t.target - 15
    const needA = d.topics.filter(t => info.files[t.id + 'a.json'] !== expA(t))
    const needB = d.topics.filter(t => t.target > 15 && info.files[t.id + 'b.json'] !== expB(t))
    log(`${ch}: ${needA.length} batch-a and ${needB.length} batch-b files to author (the rest already exist)`)
    const doneA = await parallel(needA.map(t => () =>
      agent(authorPrompt(ch, d, t, 'a', 1, expA(t), used), { label: `author ${ch} ${t.id}a`, phase: 'Author', schema: AUTHORED })))
    doneA.filter(Boolean).forEach(r => used.push(...r.ayahs))
    const doneB = await parallel(needB.map(t => () =>
      agent(authorPrompt(ch, d, t, 'b', 16, expB(t), used), { label: `author ${ch} ${t.id}b`, phase: 'Author', schema: AUTHORED })))
    if ([...doneA, ...doneB].some(r => !r)) log(`${ch}: some author batches failed; review will report the gap`)

    const history = []
    let status = 'stopped'
    let pool = 0
    for (let round = 1; round <= MAX_ROUNDS; round++) {
      const chk = await agent(`Run exactly this command and return its complete stdout in 'raw': cd ${PORTAL} && python3 testbank_tool.py check ${ch}`, { label: `check ${ch} r${round}`, phase: 'Check', schema: CHECKED, effort: 'low' })
      let c = { ok: false, problems: ['check failed to run'], pool: 0 }
      try { c = JSON.parse(chk.raw.trim().split('\n').filter(l => l.startsWith('{')).pop()) } catch (e) { /* keep default */ }
      pool = c.pool
      const rev = await agent(reviewPrompt(ch, d, base + round), { label: `review ${ch} r${base + round}`, phase: 'Review', schema: REVIEW })
      if (!rev) { log(`${ch}: review agent failed (limit?); stopping this run, resume later`); return { chapter: ch, status: 'interrupted', rounds: base + round - 1 } }
      const blocking = rev.findings.filter(f => BLOCKING.includes(f.severity))
      const minor = rev.findings.filter(f => !BLOCKING.includes(f.severity))
      history.push({ round, blocking: blocking.length, minor: minor.length, sound: rev.sound, problems: c.problems.length })
      log(`${ch} round ${round}: pool ${c.pool}, ${blocking.length} blocking, ${minor.length} minor findings, ${c.problems.length} check problems, ${rev.sound} sound`)
      if (!blocking.length && c.ok) { status = 'accepted'; history[history.length - 1].openMinor = minor.map(f => `${f.id}: ${f.problem}`); break }
      if (round === MAX_ROUNDS) break
      // fix: per-topic fixers in parallel, then a chapter-level fixer for statistics problems
      const groups = {}
      for (const f of rev.findings) { const m = f.id.match(/-(t\d+)-/); (groups[m ? m[1] : 'CHAPTER'] = groups[m ? m[1] : 'CHAPTER'] || []).push(f) }
      const topicIds = Object.keys(groups).filter(g => g !== 'CHAPTER')
      await parallel(topicIds.map(g => () =>
        agent(fixPrompt(ch, d, g, groups[g], `${PORTAL}/testbank/parts/${ch}/${g}a.json ${PORTAL}/testbank/parts/${ch}/${g}b.json`), { label: `fix ${ch} ${g} r${round}`, phase: 'Fix', schema: FIXED })))
      const chapterLevel = [...(groups.CHAPTER || []), ...c.problems.map(p => ({ id: ch, severity: 'check', problem: p, fix: 'bring the chapter within the acceptance statistics' }))]
      if (chapterLevel.length) {
        await agent(fixPrompt(ch, d, 'CHAPTER', chapterLevel, `${PORTAL}/testbank/parts/${ch}/*.json`), { label: `fix ${ch} chapter r${round}`, phase: 'Fix', schema: FIXED })
      }
    }
    return { chapter: ch, status, pool, rounds: history.length, history }
  } catch (e) {
    return { chapter: ch, status: 'error', error: String(e && e.message || e) }
  }
}

const results = await pipeline(CHAPTERS, ch => runChapter(ch))
return results.filter(Boolean)
