"""Audit of meals (Turkish/English translations) that print the SAME text under two consecutive ayahs.

Identical neighbouring texts are a signal, not an error: translators often render two ayahs as one sentence. The question per
pair is whether the repeated text really covers BOTH ayahs. The meal data is never changed by this tool; confirmed errors are
reported for a scholar (and, if the owner approves, withheld via irab_library/meals_withheld.json).

  python3 meal_pair_audit.py gen <outdir> <n shards>     writes pairs.json + mealpair_s<k>.js workflow scripts (Opus judges J1/J2, tie-break J3)
  python3 meal_pair_audit.py report <results.json ...>    classifies the returned votes (by code) and writes meal_pairs_result.json
"""
import json
import sys
from pathlib import Path

LIB = Path(__file__).parent.parent / "irab_library"
SHOW = ["77", "52", "20"]          # other meals shown to the judge as cross-reference
NAMES = {"77": "Diyanet", "52": "Elmalılı", "20": "English (Saheeh-type)", "112": "res112", "85": "English-85", "210": "Dar Al-Salam", "124": "res124"}


def load():
    return {s: json.loads((LIB / "w" / f"s{s:03d}.json").read_text("utf-8")) for s in range(1, 115)}


def ar(w, s, a):
    v = w[s].get(str(a))
    return " ".join(x["ar"] for x in v["w"]) if v else None


def pairs(w):
    out = []
    for s in range(1, 115):
        n = len(w[s])
        for a in range(1, n):
            x, y = w[s][str(a)]["m"], w[s][str(a + 1)]["m"]
            for k in x:
                if k in y and x[k].strip() and x[k].strip() == y[k].strip():
                    out.append((k, s, a))
    return out


def case(w, k, s, a, cid):
    ctx = {}
    for d in (-1, 0, 1, 2):
        t = ar(w, s, a + d)
        if t:
            ctx[f"{s}:{a + d}"] = t
    refs = {}
    for o in SHOW:
        if o != k:
            refs[NAMES.get(o, o)] = {f"{s}:{a}": w[s][str(a)]["m"].get(o, ""), f"{s}:{a + 1}": w[s][str(a + 1)]["m"].get(o, "")}
    nb = {}
    for d in (-1, 2):
        v = w[s].get(str(a + d))
        if v:
            nb[f"{s}:{a + d}"] = v["m"].get(k, "")
    return {"id": cid, "meal": NAMES.get(k, k), "first": f"{s}:{a}", "second": f"{s}:{a + 1}", "repeated_text": w[s][str(a)]["m"][k],
            "arabic": ctx, "same_meal_neighbours": nb, "other_meals": refs}


def controls(w, k_list, count):
    """known-wrong cases: two real consecutive ayahs whose true meals differ, but shown with the first ayah's text under both"""
    import random
    rnd = random.Random(20261017)
    pool = []
    for s in range(2, 115):
        for a in range(1, len(w[s])):
            x, y = w[s][str(a)]["m"].get("77", ""), w[s][str(a + 1)]["m"].get("77", "")
            if len(x) > 40 and len(y) > 40 and x != y and ar(w, s, a) != ar(w, s, a + 1):
                pool.append((s, a))
    out = []
    for i in range(count):
        s, a = rnd.choice(pool)
        c = case(w, "77", s, a, f"CTRL{i:03d}")
        c["meal"] = "Diyanet"
        c["repeated_text"] = w[s][str(a)]["m"]["77"]       # identical text claimed for both ayahs
        out.append(c)
    return out


TPL = r'''export const meta = {
  name: 'mealpair-__K__',
  description: "Meal-pair audit: does a Turkish/English meal that prints the same text under two consecutive ayahs really cover both? Two independent Opus judges, a tie-break judge",
  phases: [{ title: 'Judge', detail: 'batches of cases; every batch holds a known-wrong control' }],
}
const BATCHES = __BATCHES__
const VERD = ['COVERS_BOTH', 'ONLY_FIRST', 'ONLY_SECOND', 'OTHER_AYAH', 'UNSURE']
const SCHEMA = { type: 'object', properties: { verdicts: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, verdict: { type: 'string', enum: VERD }, note: { type: 'string' } }, required: ['id', 'verdict', 'note'] } } }, required: ['verdicts'] }

const prompt = (cases, judge, stance) => `You are judge ${judge} in an accuracy audit of Quran meals (translations of the Quran). A wrong statement published as a translation of an ayah is not acceptable. ${stance}
Each case below is a meal (translation) that prints EXACTLY THE SAME text under two consecutive ayahs (first, second). Translators often render two ayahs in one sentence, so identical text is only a signal. For each case decide, from the Arabic, whether the repeated text really covers BOTH ayahs:
  COVERS_BOTH  - the text renders the content of the first AND the second ayah (an honest merged rendering is fine, even if loose).
  ONLY_FIRST   - the text translates only the first ayah; the second ayah's own meaning is missing, so the text under the second ayah is wrong there.
  ONLY_SECOND  - the text translates only the second ayah; it is wrong under the first.
  OTHER_AYAH   - it translates neither of them (e.g. a different ayah).
  UNSURE       - you cannot decide.
Use the Arabic (with its neighbouring ayahs, given as context) as the only authority; the other meals shown are cross-references and can themselves be loose. Quote the Arabic words that decide it in 'note'. Be careful and complete; do not skim. The data is JSON; give exactly one verdict per case id and do not look anything up outside this prompt, run no commands, no external APIs.
CASES:
${JSON.stringify(cases)}`

const run = async (cases, judge, stance, label) => {
  const ctrl = cases.filter(c => c.id.startsWith('CTRL')).map(c => c.id)
  let r = null
  for (let i = 0; i < 3; i++) {
    r = await agent(prompt(cases, judge, stance), { model: 'opus', schema: SCHEMA, phase: 'Judge', label: `${judge}:${label}${i ? ' retry' + i : ''}` })
    const by = {}
    for (const v of (r && r.verdicts) || []) by[v.id] = v.verdict
    const ok = cases.every(c => by[c.id]) && ctrl.every(id => by[id] && by[id] !== 'COVERS_BOTH')
    if (ok) return { ok: true, verdicts: r.verdicts }
  }
  return { ok: false, verdicts: (r && r.verdicts) || [] }
}

const doBatch = async (b, i) => {
  const [a, c] = await parallel([
    () => run(b, 'J1', 'Judge neutrally.', `b${i}`),
    () => run(b, 'J2', 'Be a skeptic: actively look for the second ayah content that the text omits; clear a case only if the text really covers both.', `b${i}`),
  ])
  const ja = {}, jc = {}
  for (const v of a.verdicts) ja[v.id] = v
  for (const v of c.verdicts) jc[v.id] = v
  const dis = b.filter(x => !x.id.startsWith('CTRL') && (!ja[x.id] || !jc[x.id] || ja[x.id].verdict !== jc[x.id].verdict))
  let j3 = { ok: true, verdicts: [] }
  if (dis.length) j3 = await run([...dis, ...b.filter(x => x.id.startsWith('CTRL'))], 'J3', 'You are the tie-break judge: two judges disagreed on these cases. Decide on the Arabic alone.', `b${i}`)
  return { batch: i, canary_ok: a.ok && c.ok && j3.ok, J1: a.verdicts, J2: c.verdicts, J3: j3.verdicts }
}

phase('Judge')
return await pipeline(BATCHES, (b, _o, i) => doBatch(b, i))
'''


def gen(out, n):
    w = load()
    cs = [case(w, k, s, a, f"{k}:{s}:{a}") for k, s, a in pairs(w)]
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "pairs.json").write_text(json.dumps(cs, ensure_ascii=False))
    size = 15
    ctl = controls(w, None, (len(cs) + size - 1) // size)
    batches = [cs[i:i + size] + [ctl[i // size]] for i in range(0, len(cs), size)]
    for k in range(n):
        part = batches[k::n]
        js = TPL.replace("__K__", str(k)).replace("__BATCHES__", json.dumps(part, ensure_ascii=False))
        (out / f"mealpair_s{k}.js").write_text(js)
        print(out / f"mealpair_s{k}.js", len(part), "batches")
    print(len(cs), "cases,", len(batches), "batches")


def classify(votes):
    vs = [votes[j] for j in ("J1", "J2", "J3") if j in votes]
    if len(vs) < 2:
        return "NEED_MORE", None
    if vs[0] == vs[1]:
        return ("CLEAR" if vs[0] == "COVERS_BOTH" else "ERROR" if vs[0] in ("ONLY_FIRST", "ONLY_SECOND", "OTHER_AYAH") else "HUMAN"), vs[0]
    if len(vs) < 3:
        return "NEED_J3", None
    for c in set(vs):
        if vs.count(c) >= 2:
            return ("HUMAN" if c == "COVERS_BOTH" else "ERROR" if c != "UNSURE" else "HUMAN"), c    # a 2-1 vote to clear is not good enough
    return "HUMAN", None


def report(files):
    cases = {c["id"]: c for c in json.loads((Path(files[0]).parent / "pairs.json").read_text("utf-8"))} if (Path(files[0]).parent / "pairs.json").exists() else {}
    votes, bad = {}, []
    for f in files:
        for b in json.loads(Path(f).read_text("utf-8")):
            if not b:
                continue
            if not b["canary_ok"]:
                bad.append(b["batch"])
            for j in ("J1", "J2", "J3"):
                for v in b[j]:
                    votes.setdefault(v["id"], {})[j] = v["verdict"]
                    votes[v["id"]].setdefault("notes", {})[j] = v["note"]
    res = {}
    for cid, v in votes.items():
        if cid.startswith("CTRL"):
            continue
        st, c = classify({j: v[j] for j in ("J1", "J2", "J3") if j in v})
        res[cid] = {"status": st, "class": c, "votes": {j: v[j] for j in ("J1", "J2", "J3") if j in v}, "notes": v["notes"]}
    counts = {}
    for r in res.values():
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    json.dump(res, open(Path(files[0]).parent / "meal_pairs_result.json", "w"), ensure_ascii=False, indent=1)
    print(counts, "cases judged:", len(res), "of", len(cases) or "?", "batches with a failed control:", bad)


if __name__ == "__main__":
    if sys.argv[1] == "gen":
        gen(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "report":
        report(sys.argv[2:])
    else:
        sys.exit(__doc__)
