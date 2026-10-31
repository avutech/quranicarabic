"""Adjudication of flagged entries by independent judges, with the decision made by *code* from the recorded votes.

Flagged = any reviewer (pass 1 or 2) gave something other than OK for fit / tr / en on the current text.
For each flagged dimension, independent judges vote; the rule below turns the votes into an outcome.

  venv/bin/python adjudicate_tool.py queue   [limit] [book]          cases that still need votes (JSON lines)
  venv/bin/python adjudicate_tool.py case    <book> <surah> <key> [--votes]   the case file (--votes: fixers/verifiers only) (Arabic, TR, EN, ayah, reviewer notes)
  venv/bin/python adjudicate_tool.py vote    <book> <surah> <key> <judge J1|J2|J3> <dim fit|tr|en> <CLASS> "<evidence>"
  venv/bin/python adjudicate_tool.py decide  [book]                  compute outcomes; prints what needs J3 / a fix / a human
  venv/bin/python adjudicate_tool.py fixed   <book> <surah> <key> <dim> "<what was changed>"
  venv/bin/python adjudicate_tool.py verify  <book> <surah> <key> <dim> PASS|FAIL "<reason>"
  venv/bin/python adjudicate_tool.py report                          outcome counts + the human list

Classes: tr / en dimension: CONFIRMED (the reading is wrong/incomplete/has an unmarked addition: needs a fix) | FALSE_ALARM | HUMAN
         fit dimension:      MISPLACED (the entry is filed under the wrong ayah(s): give the correct range "a-b" in the same surah; the book text is never
                             changed, only where it is LISTED) | SOURCE_DEFECT (garbled/truncated/copy-pasted source: report, nothing to place) | FALSE_ALARM | HUMAN
         A MISPLACED decision needs every judge to vote MISPLACED with the identical ayah range; anything else -> HUMAN.

Decision rule (code):
  any HUMAN vote                                  -> HUMAN
  first two judges agree                          -> that class (FALSE_ALARM only if every vote is FALSE_ALARM)
  first two disagree                              -> J3 is required; majority (2 of 3) wins, except
                                                     FALSE_ALARM must be unanimous, so 2-1 for FALSE_ALARM -> HUMAN
  CONFIRMED -> a fix is required: fixed + verify PASS, else after 2 failed attempts -> HUMAN
"""
import fcntl
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import faith_tool as ft  # noqa: E402

AD = ft.AF / "adjudication"
CLASSES = {"fit": {"MISPLACED", "SOURCE_DEFECT", "SOURCE_ISSUE", "FALSE_ALARM", "HUMAN"}, "tr": {"CONFIRMED", "FALSE_ALARM", "HUMAN"}, "en": {"CONFIRMED", "FALSE_ALARM", "HUMAN"}}
DIMKEY = {"fit": "fit", "tr": "trv", "en": "env"}


def path(book, s):
    return AD / book / f"s{int(s):03d}.json"


def read(book, s):
    p = path(book, s)
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def update(book, s, fn):
    p = path(book, s)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p.with_suffix(".lock"), "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        d = json.loads(p.read_text("utf-8")) if p.exists() else {}
        fn(d)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(d, ensure_ascii=False, indent=0), "utf-8")
        os.replace(tmp, p)


def flagged_dims(rec_by_pass, hs):
    """dims that some reviewer flagged on the current text -> list of (pass, note)"""
    out = {}
    for pn, r in rec_by_pass.items():
        if not r or [r.get("ar"), r.get("tr"), r.get("en")] != list(hs):
            continue
        for d, k in DIMKEY.items():
            v = r.get(k)
            if v not in (None, "OK", "FIXED"):
                out.setdefault(d, []).append((pn, v, r.get("note", ""), r.get("by", "")))
    return out


def outcome_of(dim, votes, cur_state):
    """pure function of the votes -> (status, class)"""
    vs = [votes[j]["class"] for j in ("J1", "J2", "J3") if j in votes]
    if "HUMAN" in vs:
        return "DECIDED", "HUMAN"
    if len(vs) < 2:
        return "NEED_VOTES", None
    if vs[0] == vs[1]:
        return "DECIDED", vs[0]
    if len(vs) < 3:
        return "NEED_J3", None
    for c in set(vs):
        if vs.count(c) >= 2:
            return "DECIDED", "HUMAN" if c == "FALSE_ALARM" else c      # a 2-1 vote to clear is not good enough
    return "DECIDED", "HUMAN"


def cases(book_filter=None):
    for b in ([book_filter] if book_filter else ft.BOOKS):
        for s in range(1, 115):
            cur = ft.current(b, s)
            if not cur:
                continue
            led, ad = ft.led_read(b, s), read(b, s)
            for k, (e, t, n, hs) in cur.items():
                fl = flagged_dims(led.get(k, {}), list(hs))
                if fl:
                    yield b, s, k, e, t, n, list(hs), fl, ad.get(k)


def stale(ad, hs):
    return not ad or ad.get("hs") != hs


def cmd_queue(limit="50", book=None):
    out = 0
    for b, s, k, e, t, n, hs, fl, ad in cases(book):
        if stale(ad, hs):
            need = list(fl)
        else:
            need = [d for d in fl if ad["dims"].get(d, {}).get("status") in ("NEED_VOTES", "NEED_J3", None)]
        if need:
            print(json.dumps({"book": b, "surah": s, "key": k, "dims": need}, ensure_ascii=False)); out += 1
            if out >= int(limit):
                return


def cmd_case(book, s, key, *flags):
    cur = ft.current(book, s)
    e, t, n, hs = cur[key]
    led = ft.led_read(book, s).get(key, {})
    fl = flagged_dims(led, list(hs))
    w = json.loads((ft.LIB / "w" / f"s{int(s):03d}.json").read_text("utf-8"))
    print(f"CASE {key}  (surah {s})  flagged dimensions: {', '.join(fl)}")
    for a in range(int(e["s"]), min(int(e["e"]), int(e["s"]) + 5) + 1):
        v = w[str(a)]
        print(f"[{s}:{a}] {' '.join(x['ar'] for x in v['w'])}\n   TR: {v['m'].get('77')}\n   EN: {v['m'].get('20')}")
    print(f"\n=== ARABIC SOURCE\n{e['t']}\n\n=== TURKISH READING\n{t}\n\n=== ENGLISH READING\n{n}\n\n=== REVIEWER CLAIMS (to be verified, not trusted)")
    for d, items in fl.items():
        for pn, v, note, by in items:
            print(f"- dim {d}: {v}  ({pn} by {by}): {note}")
    if "--votes" in flags:       # fixers and verifiers only: judges must never see each other's votes
        rec = read(book, s).get(key)
        print("\n=== JUDGES' VOTES AND EVIDENCE")
        for d, dm in (rec or {}).get("dims", {}).items():
            for j, v in dm["votes"].items():
                print(f"- dim {d} {j}: {v['class']}: {v['evidence']}")
            if dm.get("verify_note"):
                print(f"- dim {d} previous verifier note: {dm['verify_note']}")


def cmd_vote(book, s, key, judge, dim, cls, evidence, ayahs=""):
    if judge not in ("J1", "J2", "J3"): sys.exit("judge must be J1, J2 or J3")
    if dim not in CLASSES or cls not in CLASSES[dim]: sys.exit(f"for dim {dim} the class must be one of {sorted(CLASSES.get(dim, []))}")
    if len(evidence) < 25 and cls != "HUMAN": sys.exit("evidence required: quote the Arabic words and say what is right or wrong")
    if cls == "MISPLACED":
        import re as _re
        m = _re.fullmatch(r"(\d+)-(\d+)", ayahs.strip())
        if not m or int(m.group(1)) > int(m.group(2)): sys.exit('MISPLACED needs the correct ayah range of this surah as an 8th argument, e.g. "143-143" or "142-144"')
    cur = ft.current(book, s)
    hs = list(cur[key][3])

    def f(d):
        if d.get(key, {}).get("hs") != hs:
            d[key] = {"hs": hs, "dims": {}}
        dm = d[key]["dims"].setdefault(dim, {"votes": {}, "status": "NEED_VOTES"})
        if judge in dm["votes"]:
            print("this judge already voted on this dimension; vote ignored"); return
        dm["votes"][judge] = {"class": cls, "evidence": evidence, "at": time.strftime("%Y-%m-%d %H:%M")}
        if cls == "MISPLACED": dm["votes"][judge]["ayahs"] = ayahs.strip()
        st, c = outcome_of(dim, dm["votes"], None)
        dm["status"], dm["class"] = st, c
        if dim == "fit": dm["status"], dm["class"] = status_of(dm, "fit")
        print(f"recorded; dimension status now {st}" + (f" -> {c}" if c else ""))

    update(book, s, f)


def records(book=None):
    """every adjudication record that still applies to the current text (the hashes are kept up to date when a fix is recorded)"""
    for b in ([book] if book else ft.BOOKS):
        d = AD / b
        if not d.exists():
            continue
        for f in sorted(d.glob("s*.json")):
            s = int(f.stem[1:])
            cur = ft.current(b, s)
            for k, rec in json.loads(f.read_text("utf-8")).items():
                if k in cur and rec["hs"] == list(cur[k][3]):
                    yield b, s, k, rec


def status_of(dm, dim=None):
    if dm.get("verified") == "PASS":
        return "DONE", "FIXED_AND_VERIFIED"
    if dm.get("fix_failed", 0) >= 2:
        return "DECIDED", "HUMAN"
    st, c = outcome_of(dim, dm["votes"], None)
    if c == "SOURCE_ISSUE":
        c = "SOURCE_DEFECT"
    if c == "MISPLACED":                                     # a placement change needs identical ranges from every judge
        rngs = {v.get("ayahs") for v in dm["votes"].values()}
        if len(rngs) != 1 or None in rngs:
            return "DECIDED", "HUMAN"
    return st, c


def cmd_decide(book=None):
    counts, need3, fixes, need_votes = {}, [], [], []
    for b, s, k, rec in records(book):
        for d, dm in rec["dims"].items():
            st, c = status_of(dm, d)
            counts[f"{st}/{c}"] = counts.get(f"{st}/{c}", 0) + 1
            if st == "NEED_J3": need3.append([b, s, k, d])
            elif st == "NEED_VOTES": need_votes.append([b, s, k, d])
            elif st == "DECIDED" and c in ("CONFIRMED", "SOURCE_ISSUE") and c == "CONFIRMED": fixes.append([b, s, k, d])
    print(json.dumps({"counts": counts, "need_j3": need3, "need_fix": fixes, "need_votes": need_votes}, ensure_ascii=False))


def _dimrec(book, s, key, dim, fn):
    cur = ft.current(book, s)
    hs = list(cur[key][3])

    def f(d):
        if d.get(key, {}).get("hs") != hs or dim not in d[key]["dims"]:
            sys.exit("no current adjudication for that entry/dimension (the text may have changed)")
        fn(d[key]["dims"][dim])
    update(book, s, f)


def cmd_fixed(book, s, key, dim, what):
    def f(dm):
        dm["fixed_note"] = what
        dm.pop("verified", None)
    cur = ft.current(book, s)
    # a fix changes the reading, so the hashes move: re-key the adjudication record to the new hashes, keeping the history
    ad = read(book, s)
    old = ad.get(key)
    if not old or dim not in old["dims"]:
        sys.exit("no adjudication for that entry/dimension")
    new_hs = list(cur[key][3])

    def g(d):
        rec = d[key]
        rec["history"] = rec.get("history", []) + [{"old_hs": rec["hs"], "dim": dim, "what": what, "at": time.strftime("%Y-%m-%d %H:%M")}]
        rec["hs"] = new_hs
        rec["dims"][dim]["fixed_note"] = what
        rec["dims"][dim].pop("verified", None)
    update(book, s, g)
    print("fix recorded; now an independent verifier must check the new text")


def cmd_verify(book, s, key, dim, verdict, reason):
    if verdict not in ("PASS", "FAIL"): sys.exit("PASS or FAIL")

    def f(dm):
        dm["verified"] = verdict if verdict == "PASS" else None
        dm["verify_note"] = reason
        if verdict == "FAIL":
            dm["fix_failed"] = dm.get("fix_failed", 0) + 1
    _dimrec(book, s, key, dim, f)
    print("verify recorded:", verdict)


def cmd_placements():
    """proposed placement corrections: entry stays as published, only the ayah(s) it is LISTED under change"""
    out = []
    for b, s, k, rec in records(None):
        dm = rec["dims"].get("fit")
        if not dm: continue
        st, c = status_of(dm, "fit")
        if c == "MISPLACED":
            a, z = [int(x) for x in next(iter({v["ayahs"] for v in dm["votes"].values()})).split("-")]
            out.append({"key": k, "surah": s, "book": b, "list_under": [a, z], "judges": {j: v["evidence"][:300] for j, v in dm["votes"].items()}})
    print(json.dumps(out, ensure_ascii=False, indent=1))


def cmd_report():
    tot, human, src = {}, [], []
    for b, s, k, rec in records(None):
        for d, dm in rec["dims"].items():
            st, c = status_of(dm, d)
            key = c or st
            tot[key] = tot.get(key, 0) + 1
            if c == "HUMAN":
                human.append([b, s, k, d, [v["evidence"][:140] for v in dm["votes"].values()]])
            elif c in ("SOURCE_DEFECT", "MISPLACED"):
                src.append([b, s, k, d, c, sorted({v.get("ayahs", "") for v in dm["votes"].values()} - {""}), [v["evidence"][:140] for v in dm["votes"].values()][:1]])
    print(json.dumps(tot))
    print(f"-- {len(human)} for a human, {len(src)} source issues")
    for h in human:
        print("HUMAN", json.dumps(h, ensure_ascii=False))
    for h in src:
        print("SOURCE", json.dumps(h, ensure_ascii=False))


if __name__ == "__main__":
    cmds = {"queue": cmd_queue, "case": cmd_case, "vote": cmd_vote, "decide": cmd_decide, "fixed": cmd_fixed, "verify": cmd_verify, "report": cmd_report, "placements": cmd_placements}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv[1]](*sys.argv[2:])
