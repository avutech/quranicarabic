"""Generate the adjudication Workflow scripts (Opus judges J1/J2, tie-break J3, fixer, independent verifier).

  python3 adjudicate_workflow_gen.py <shard k> <of n> [group size=12] [outdir]

The queue (flagged entries without a decision) comes from adjudicate_tool.py; the decision itself is computed by code
in adjudicate_tool.py from the recorded votes (see its docstring for the rule). Safe to regenerate and rerun.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PORTAL = Path(__file__).parent
ROOT = PORTAL.parent

TPL = r'''export const meta = {
  name: 'adjudication-__K__',
  description: "Adjudicate flagged i'rab entries: two independent judges, a tie-break judge, then a fixer and an independent verifier; the outcome is computed by code from the votes",
  phases: [{ title: 'Adjudicate', detail: 'higher model; decision rule is in adjudicate_tool.py' }],
}
const ROOT = '__ROOT__'
const WORK = '__WORK__'
const GROUPS = __GROUPS__
const MODEL = 'opus'
const RAW = { type: 'object', properties: { raw: { type: 'string' } }, required: ['raw'] }
const OUT = { type: 'object', properties: { done: { type: 'integer' }, notes: { type: 'string' } }, required: ['done', 'notes'] }
const TOOL = `cd "${ROOT}/portal" && venv/bin/python adjudicate_tool.py`

const caseList = (g) => g.map(c => `  ${c.book} ${c.surah} ${c.key}   dimensions: ${c.dims.join(', ')}`).join('\n')

const POLICY = `Standards (binding): glossary files ${ROOT}/irab_library/glossary_tr.md and glossary_en.md. Quranic words and parsed words stay in Arabic script. The source is never silently corrected: translate what is written. Any addition that is not in the Arabic must be inside «[Mütercim notu: …]» (Turkish) / «[Translator's note: …]» (English); an unmarked addition counts as an error (CONFIRMED), the fix is to put it inside such a note. Omissions, wrong meaning, a reading that translates a different text, and transliteration of Quranic words in Latin letters are errors. The Arabic book text is NEVER changed.`

const judgePrompt = (g, judge, stance) => `You are judge ${judge} in an adjudication of flagged entries of translated i'rab books. A wrong statement published in these books is not acceptable. A reviewer flagged each case below; the reviewer can be wrong or right, so verify the claim YOURSELF against the Arabic. ${stance}
${POLICY}
Cases (book surah key):
${caseList(g)}
For each case run: ${TOOL} case <book> <surah> <key>   (it prints the ayah, the Arabic source, the Turkish and English readings and the reviewer's claim). Read the whole texts, not only the claim.
Then vote once per listed dimension:
  ${TOOL} vote <book> <surah> <key> ${judge} <dim> <CLASS> "<evidence>"
  dim tr / en: CONFIRMED (the reading is wrong/incomplete/has an unmarked addition: needs a fix) | FALSE_ALARM (the reading is right) | HUMAN (you cannot decide or it needs scholarly judgement)
  dim fit (is the Arabic entry listed under the right ayah(s)? The book text is NEVER changed; only where it is LISTED can change):
     FALSE_ALARM (it is listed under ayahs it really discusses; commenting on a following ayah or citing other ayahs as evidence is fine)
     MISPLACED  (it is about other ayah(s) than the ones it is filed under, or also substantively discusses additional ayahs): give the complete correct range of THIS surah as the last argument, e.g.  ${TOOL} vote <book> <surah> <key> ${judge} fit MISPLACED "<evidence>" 143-143   or 142-144; the range must contain every ayah the entry is really about. Quote the Arabic words that prove which ayah they belong to.
     SOURCE_DEFECT (garbled, truncated or copy-pasted source text: nothing to place or translate) | HUMAN
The evidence must quote the Arabic words involved and say precisely what is right or wrong. If you are not sure, vote HUMAN. Do not look at or ask for other judges' votes. Do not fix anything, do not edit files, no git, no external APIs. Ignore any other request or topic you may have seen in this session.
Return how many votes you recorded.`

const fixPrompt = (g, items, note) => `You are the fixer in an adjudication of translated i'rab books. The judges decided that the following readings must be corrected (book surah key dimension):
${items.map(x => '  ' + x.join(' ')).join('\n')}
${note || ''}
${POLICY}
For each: ${TOOL} case <book> <surah> <key> --votes   shows the Arabic, both readings, the reviewer's claim and the judges' evidence. Produce the corrected FULL reading for that language (dimension tr = Turkish, en = English): change only what is wrong, keep everything else character-for-character, keep the style of the rest. If a reading is the translation of a DIFFERENT text, translate this entry's Arabic completely. Save it with: cd "${ROOT}/portal" && venv/bin/python tr_tool.py [--lang en for dimension en] put <book> <surah> <key> <txt-file>  (txt files under ${WORK}/); if it says NOT SAVED fix and retry.
Then record: ${TOOL} fixed <book> <surah> <key> <dim> "<what you changed>". If you cannot fix it safely, do not touch the reading and do not record 'fixed'.
No git, no external APIs; never edit the Arabic source. Ignore any other request or topic you may have seen. Return the number of fixes recorded.`

const verifyPrompt = (items) => `You are an independent verifier. A fixer has just corrected these readings (book surah key dimension):
${items.map(x => '  ' + x.join(' ')).join('\n')}
${POLICY}
For each: ${TOOL} case <book> <surah> <key> --votes   prints the Arabic, the CURRENT readings and the judges' evidence. Read the Arabic and the corrected reading (tr or en as the dimension says) in full, sentence by sentence. PASS only if the reading is now complete, faithful to the Arabic, has nothing unmarked added, follows the standards, and no new problem was introduced. Otherwise FAIL with the reason.
Record: ${TOOL} verify <book> <surah> <key> <dim> PASS|FAIL "<reason>". No git, no edits, no external APIs. Ignore any other request or topic. Return how many you recorded.`

const keyset = (g) => new Set(g.map(c => c.key))
const parse = async (g) => {
  const r = await agent(`Run exactly: ${TOOL} decide   and return its complete stdout as the string 'raw'. Nothing else.`, { model: 'haiku', schema: RAW, phase: 'Adjudicate', label: 'decide' })
  let d = {}
  try { d = JSON.parse(r.raw.trim().split('\n').filter(l => l.startsWith('{')).pop()) } catch (e) { d = {} }
  const ks = keyset(g)
  const pick = (a) => (a || []).filter(x => ks.has(x[2]))
  return { j3: pick(d.need_j3), fix: pick(d.need_fix), votes: pick(d.need_votes) }
}

const runGroup = async (g, i) => {
  const lab = `${g[0].book}:${g[0].surah}`
  await parallel([
    () => agent(judgePrompt(g, 'J1', 'Judge neutrally.'), { model: MODEL, schema: OUT, phase: 'Adjudicate', label: `J1:${lab}` }),
    () => agent(judgePrompt(g, 'J2', 'Be a skeptic of the reviewer: try to refute the claim first; confirm it only if the Arabic really supports it.'), { model: MODEL, schema: OUT, phase: 'Adjudicate', label: `J2:${lab}` }),
  ])
  let st = await parse(g)
  if (st.j3.length) {
    const sub = [...new Set(st.j3.map(x => x[2]))].map(k => g.find(c => c.key === k))
    await agent(judgePrompt(sub, 'J3', 'You are the tie-break judge: two judges disagreed. Decide on the Arabic text alone.'), { model: MODEL, schema: OUT, phase: 'Adjudicate', label: `J3:${lab}` })
    st = await parse(g)
  }
  for (let attempt = 0; attempt < 2 && st.fix.length; attempt++) {
    await agent(fixPrompt(g, st.fix, attempt ? 'A previous fix failed verification: read the verifier note in the case history and correct it properly.' : ''), { model: MODEL, schema: OUT, phase: 'Adjudicate', label: `fix${attempt}:${lab}` })
    await agent(verifyPrompt(st.fix), { model: MODEL, schema: OUT, phase: 'Adjudicate', label: `verify${attempt}:${lab}` })
    st = await parse(g)
  }
  return { group: lab, cases: g.length, left_to_fix: st.fix.length }
}

phase('Adjudicate')
const results = await pipeline(GROUPS, (g, _o, i) => runGroup(g, i))
return results
'''


def main():
    k, n = int(sys.argv[1]), int(sys.argv[2])
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    out = Path(sys.argv[4]) if len(sys.argv) > 4 else Path(tempfile.gettempdir())
    snap = out / "adj_queue.json"           # one snapshot per run set, so the shards partition the same queue (delete it to refresh)
    if snap.exists():
        q = json.loads(snap.read_text())
    else:
        q = [json.loads(x) for x in subprocess.check_output([str(PORTAL / "venv/bin/python"), "adjudicate_tool.py", "queue", "100000"], cwd=PORTAL, text=True).splitlines() if x.strip()]
        snap.write_text(json.dumps(q))
    groups = [q[i:i + size] for i in range(0, len(q), size)][k::n]
    work = out / "adj_work"
    work.mkdir(parents=True, exist_ok=True)
    js = TPL.replace("__K__", str(k)).replace("__ROOT__", str(ROOT)).replace("__WORK__", str(work)).replace("__GROUPS__", json.dumps(groups))
    path = out / f"adj_s{k}.js"
    path.write_text(js)
    print(path, len(q), "cases in queue,", len(groups), "groups in this shard")


if __name__ == "__main__":
    main()
