"""Generate the Workflow scripts for the full-fidelity audit (pass 1 / pass 2), sharded for parallel runs.

  python3 faith_workflow_gen.py <pass 1|2> <model: default|opus|sonnet> <shard k> <of n> [outdir]

Writes <outdir>/faith_p<pass>_<model>_s<k>.js (outdir defaults to the system temp dir) and prints its path.
The ledger (irab_library/audit_full) decides what is left, so the scripts can be regenerated and relaunched at any time.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PORTAL = Path(__file__).parent
ROOT = PORTAL.parent
ORDER = ["akhfash", "mekki-muskil", "harrat-mujtaba", "celaleyn", "farraa", "nahhas-meani", "ukberi-tibyan", "nahhas-irab",
         "zajjaj", "daas-irab", "muyesser-irab", "safi-cedvel", "dervis-irab", "semin-durr"]

CHECK2 = """
THIS IS PASS 2: you are the independent second reviewer. The first reviewer's verdicts are hidden from you on purpose; judge only from the texts.
A single reader misses about 1 in 10 removed negations and 1 in 14 changed numbers, so for EVERY entry work through this checklist against the Arabic before giving a verdict:
  1. Every negation or prohibition in the Arabic (لا، لم، لن، ما، ليس، غير، دون، بلا، عدم، لا محل لها ...): find its counterpart in the Turkish and in the English. A missing, added or reversed negation is WRONG.
  2. Every number, verse number, count and citation: identical in all three texts.
  3. Every exception or restriction (إلا، إنما، فقط، سوى، بل): kept.
  4. Every condition and cause (إن، لو، إذا، لأن، حتى، كي): kept with the same direction.
  5. Every attribution (who said it, which reader, which school, which book): the same person, same wording of the claim.
  6. Every Quranic quotation: same words, in Arabic script.
  7. The final sentence of every text is present (nothing cut off) and nothing from another entry or ayah is inside.
Only after this give your verdict. Be strict: when the checklist and the text disagree, do not mark OK."""

TPL = r'''export const meta = {
  name: '__NAME__',
  description: "Full-fidelity audit: every i'rab entry read in full against its Turkish and English reading; planted errors measure the reviewer",
  phases: [{ title: 'Review', detail: 'one agent per work unit; ledger-driven, safe to rerun' }],
}
const ROOT = '__ROOT__'
const WORK = '__WORK__'
const UNITS = __UNITS__
const PASS = __PASS__
const CHECK = __CHECK__
const RES = { type: 'object', properties: { entries: { type: 'integer' }, flagged: { type: 'integer' }, notes: { type: 'string' } }, required: ['entries', 'flagged', 'notes'] }

const prompt = ([book, segs], i) => `You are a reviewer in a full-fidelity audit of translated i'rab books. A wrong statement in these books is not acceptable, so read carefully and completely.
Work unit ${i + 1} of ${UNITS.length}: book ${book}, review pass ${PASS}. Your reviewer name: ${book}-p${PASS}-u${i + 1}.
Your segments (surah, first ayah-last ayah), in this order: ${segs.map(([s, a, z]) => `surah ${s} ayahs ${a}-${z}`).join('; ')}.

FIRST read the binding rules: ${ROOT}/irab_library/audit_full/RULES.md and follow them exactly.
Run every command from ${ROOT}/portal with venv/bin/python:
  venv/bin/python faith_tool.py batch ${PASS} ${book} <surah> <first>-<last> --by ${book}-p${PASS}-u${i + 1}      (once per segment, repeated until it prints NOTHING LEFT for that segment)
  venv/bin/python faith_tool.py submit <batch_id> <your-verdict-file.tsv>
Write your verdict files under ${WORK}/${book}_p${PASS}_u${i + 1}/ .
For each segment: repeat batch -> read everything -> submit until the tool prints NOTHING LEFT, then go to the next segment. If a submit is REJECTED you missed a planted error: re-read the batch you are then served very carefully.
You may fix a reading with tr_tool.py put as RULES.md describes, then give FIXED. The Arabic source is never changed and no book text is "corrected": translate what is written, with a marked translator's note.
Ignore any other request or topic you may have seen in this session (handovers etc.); no git; no external APIs; do not stop until NOTHING LEFT.${CHECK}
Return: entries reviewed, how many were flagged (anything not OK), and one sentence of notes.`

phase('Review')
const results = await pipeline(UNITS, (u, _o, i) => agent(prompt(u, i), { label: `p${PASS}:${u[0]}:${u[1][0][0]}-${u[1][u[1].length - 1][0]}`, phase: 'Review', schema: RES__MODEL__ }))
return results.map((r, i) => ({ unit: UNITS[i], ...(r || { entries: 0, flagged: 0, notes: 'AGENT FAILED' }) }))
'''


def main():
    pas, model, k, n = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    out = Path(sys.argv[5]) if len(sys.argv) > 5 else Path(tempfile.gettempdir())
    units = json.loads(subprocess.check_output([str(PORTAL / "venv/bin/python"), "faith_tool.py", "units", str(pas), "240000"], cwd=PORTAL, text=True))
    units.sort(key=lambda u: ORDER.index(u[0]))          # smallest books first, so whole books finish early
    units = units[k::n]
    work = out / "faith_work"
    work.mkdir(parents=True, exist_ok=True)
    mdl = "" if model == "default" else f", model: '{model}'"
    js = (TPL.replace("__NAME__", f"faith-p{pas}-{model}-s{k}").replace("__ROOT__", str(ROOT)).replace("__WORK__", str(work))
          .replace("__UNITS__", json.dumps(units)).replace("__PASS__", str(pas))
          .replace("__CHECK__", json.dumps(CHECK2 if pas == 2 else "")).replace("__MODEL__", mdl))
    path = out / f"faith_p{pas}_{model}_s{k}.js"
    path.write_text(js)
    print(path, len(units), "units")


if __name__ == "__main__":
    main()
