export const meta = {
  name: 'master-exam-pool',
  description: 'Author the Master Exam pool (integrative questions, 11 per chapter) and review/fix it per level until accepted',
  whenToUse: 'Build or resume the Master Exam question pool under portal/testbank/MASTER.json',
  phases: [
    { title: 'Author', detail: '11 integrative questions per chapter, written by one agent per chapter' },
    { title: 'Check', detail: 'assemble MASTER.json + statistics' },
    { title: 'Review', detail: 'fresh independent reviewer per level per round' },
    { title: 'Fix', detail: 'fix every finding per chapter, then re-review' },
  ],
}

const ROOT = '/Users/ahmedugur/Documents/Claude/Projects/Quran Arabic'
const PORTAL = ROOT + '/portal'
const BLOCKING = ['wrong-answer', 'ambiguous', 'explanation-error', 'out-of-scope', 'hint-leak', 'turkish', 'duplicate']
const MAX_ROUNDS = 6
const ALL = []
for (let L = 1; L <= 3; L++) for (let W = 1; W <= 14; W++) ALL.push(`L${L}W${W}`)
const LEVELS = (args && args.levels) ? args.levels : [1, 2, 3]

const AUTHORED = { type: 'object', properties: { file: { type: 'string' }, count: { type: 'integer' }, notes: { type: 'string' } }, required: ['file', 'count'] }
const CHECKED = { type: 'object', properties: { raw: { type: 'string' } }, required: ['raw'] }
const REVIEW = { type: 'object', properties: {
  findings: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'problem', 'fix'] } },
  sound: { type: 'integer' }, verdict: { type: 'string' } }, required: ['findings', 'sound', 'verdict'] }
const FIXED = { type: 'object', properties: { changed: { type: 'array', items: { type: 'string' } }, disagreements: { type: 'array', items: { type: 'string' } } }, required: ['changed', 'disagreements'] }

const COMMON = `Project root: ${ROOT} (code in portal/). Work in ${PORTAL}. No paid APIs: you write all content yourself. Read first, fully: ${ROOT}/tasks/testbank_brief.md (authoring rules 1-20), ${ROOT}/tasks/master_blueprint.md (what a MASTER EXAM question is: READ IT CAREFULLY), and the docstring of ${PORTAL}/testbank_tool.py. The finished chapter bank ${PORTAL}/testbank/L1W1.json shows the expected question shape and quality.`

function authorPrompt(ch) {
  const design = ch === 'L1W1' ? 'This chapter has no design file; use portal/testbank/L1W1.json topics t1-t5 and its lecture.' : `Chapter design (topics, scope, what may be used, what must not be needed, policy, caveats): ${PORTAL}/testbank/designs/${ch}.json`
  return `${COMMON}

TASK: write exactly 11 Master Exam questions whose PRIMARY chapter is ${ch}. ${design} The chapter's own question bank (for the ayahs it already uses; prefer OTHER ayahs): ${PORTAL}/testbank/${ch}.json. The lecture: cd ${PORTAL} && python3 -c "import json;print(json.dumps(json.load(open('lectures.json'))['${ch}'],ensure_ascii=False,indent=1))" (and the lectures of earlier chapters for the earlier concepts you combine).
Output file: ${PORTAL}/testbank/parts/MASTER/${ch}.json = {"questions": [...]} (create the folder if needed; NO "topic" object). Question ids "M-${ch}-01" ... "M-${ch}-11". Every question has: id, chapter "${ch}", topic (one of the chapter's topic ids; spread over at least 3 different topics), difficulty (1/2/3; use about 2 x level 1... see blueprint), ref, quote, stem {en,tr}, 4 options each with why {en,tr}, correct 0-3 (positions balanced).
Run: cd ${PORTAL} && python3 testbank_tool.py part testbank/parts/MASTER/${ch}.json  until 0 errors. Reply with the structured result.`
}

function reviewPrompt(L, n) {
  return `You are an expert reviewer of classical Arabic grammar (nahw) and Quranic i'rab, and a fluent Turkish editor. You have NEVER seen any earlier review of this pool: do not open any file under ${PORTAL}/testbank/reviews/ other than the one you write. Read first: ${ROOT}/tasks/testbank_brief.md (rules 1-20 and 'Hint = the rule'), ${ROOT}/tasks/master_blueprint.md, the sections 'Defining duplicate' and 'What a hint-leak is' of ${ROOT}/tasks/testbank_pipeline.md, and the docstring of ${PORTAL}/testbank_tool.py.
Review ONLY the questions of ${PORTAL}/testbank/MASTER.json whose id starts with M-L${L}W (Level ${L}); read-only: do NOT edit it. Each question's allowed knowledge: its primary chapter ('chapter' field) and every EARLIER chapter (design files ${PORTAL}/testbank/designs/<chapter>.json give taughtBefore / forbidden / policy / caveats; the lectures are in ${PORTAL}/lectures.json). A Master question must be integrative (blueprint) and must never need anything taught LATER than its primary chapter.
For EVERY question check: (1) the marked-correct option is correct and is the ONLY defensible answer; (2) every wrong option's 'why' is true and specific, the correct 'why' states the right rule(s), no tense/neighbour-word claim is false for this ayah; (3) every Arabic word the stem/options refer to is inside 'quote' and the ref/glosses are right (check Irab Kitaplari/_kelime/qurancom.json); (4) nothing from a LATER chapter is needed; (5) Turkish natural standard Turkish, correct terms, same meaning as English, no Turkish suffix attached to Arabic-script words; (6) the question really integrates the primary chapter with at least one other concept (otherwise 'minor' at most, unless it is a plain duplicate of the chapter pool style); (7) stem type matches option type; (8) duplicates by the pipeline definition, also within this level's Master questions; (9) difficulty labels plausible; (10) its topic id really is a topic of its primary chapter.
Severity values (use exactly): wrong-answer, ambiguous, explanation-error, out-of-scope, hint-leak, turkish, duplicate, minor. Report only real problems. Write the list to ${PORTAL}/testbank/reviews/MASTER-L${L}_review${n}.txt (one line per finding: id | severity | problem | fix) and return the same findings in the structured result plus 'sound' and a one-line verdict.`
}

function fixPrompt(ch, findings) {
  return `${COMMON}

TASK: fix review findings for the Master Exam questions of primary chapter ${ch}. Edit ONLY ${PORTAL}/testbank/parts/MASTER/${ch}.json (never testbank/MASTER.json). Fix EVERY finding below, including minor ones. Where a question changes, rewrite ALL four 'why' texts in en and tr; replacement questions are new integrative questions (keep the id) following the blueprint. If you disagree with a finding, list it under disagreements with your reason.
Chapter design: ${PORTAL}/testbank/designs/${ch}.json (L1W1: see testbank/L1W1.json). Findings:
${findings.map(f => `- ${f.id} | ${f.severity} | ${f.problem} | suggested fix: ${f.fix}`).join('\n')}
After editing run: cd ${PORTAL} && python3 testbank_tool.py part testbank/parts/MASTER/${ch}.json  (0 errors required). Reply with the structured result.`
}

async function runLevel(L) {
  const chapters = ALL.filter(c => c.startsWith(`L${L}W`))
  try {
    phase('Author')
    const info0 = await agent(`Run exactly this command and return its complete stdout in 'raw': cd ${PORTAL} && python3 testbank_tool.py parts MASTER`, { label: `parts MASTER L${L}`, phase: 'Author', schema: CHECKED, effort: 'low' })
    let info = { files: {}, reviews: 0 }
    try { info = JSON.parse(info0.raw.trim().split('\n').filter(l => l.startsWith('{')).pop()) } catch (e) { /* nothing written yet */ }
    const todo = chapters.filter(c => info.files[c + '.json'] !== 11)
    log(`Level ${L}: ${todo.length} of ${chapters.length} chapters still need their 11 Master questions`)
    await parallel(todo.map(c => () => agent(authorPrompt(c), { label: `master author ${c}`, phase: 'Author', schema: AUTHORED })))

    const base0 = await agent(`Run exactly this command and return its complete stdout in 'raw': cd ${PORTAL} && python3 testbank_tool.py parts MASTER-L${L}`, { label: `parts MASTER-L${L}`, phase: 'Check', schema: CHECKED, effort: 'low' })
    let base = 0
    try { base = JSON.parse(base0.raw.trim().split('\n').filter(l => l.startsWith('{')).pop()).reviews || 0 } catch (e) { /* first run */ }
    if (base >= 12) return { level: L, status: 'exhausted-needs-human', rounds: base }
    const history = []
    let status = 'stopped'
    for (let round = 1; round <= MAX_ROUNDS; round++) {
      const chk = await agent(`Run exactly this command and return its complete stdout in 'raw': cd ${PORTAL} && python3 testbank_tool.py check MASTER`, { label: `check MASTER L${L} r${round}`, phase: 'Check', schema: CHECKED, effort: 'low' })
      let c = { ok: false, problems: ['check failed to run'], pool: 0 }
      try { c = JSON.parse(chk.raw.trim().split('\n').filter(l => l.startsWith('{')).pop()) } catch (e) { /* keep default */ }
      const rev = await agent(reviewPrompt(L, base + round), { label: `master review L${L} r${base + round}`, phase: 'Review', schema: REVIEW })
      if (!rev) { log(`Level ${L}: review failed (limit/network?); stopping this run, resume later`); return { level: L, status: 'interrupted', rounds: base + round - 1 } }
      const blocking = rev.findings.filter(f => BLOCKING.includes(f.severity))
      history.push({ round, blocking: blocking.length, minor: rev.findings.length - blocking.length, sound: rev.sound, problems: c.problems.length })
      log(`Master L${L} round ${round}: ${blocking.length} blocking, ${rev.findings.length - blocking.length} minor, ${c.problems.length} check problems, ${rev.sound} sound`)
      if (!blocking.length) { status = 'accepted'; break }
      if (round === MAX_ROUNDS) break
      const groups = {}
      for (const f of rev.findings) { const m = f.id.match(/^M-(L\dW\d+)-/); if (m) (groups[m[1]] = groups[m[1]] || []).push(f) }
      await parallel(Object.keys(groups).map(ch => () => agent(fixPrompt(ch, groups[ch]), { label: `master fix ${ch} r${base + round}`, phase: 'Fix', schema: FIXED })))
    }
    return { level: L, status, rounds: base + history.length, history }
  } catch (e) {
    return { level: L, status: 'error', error: String(e && e.message || e) }
  }
}

const results = await pipeline(LEVELS, L => runLevel(L))
return results.filter(Boolean)
