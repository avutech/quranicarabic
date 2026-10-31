"""Full-fidelity audit: every i'rab entry read in full against its Turkish and English reading.

An agent never chooses what to review: it is *served* batches of unreviewed entries and must give a verdict for
every entry in the batch. A ledger records, per entry and per pass, a verdict together with the hashes of the Arabic,
Turkish and English texts that were reviewed (a later edit makes the record stale automatically).
Planted errors ("canaries": a wrong-ayah translation or a half-truncated one) are mixed into batches; a batch in which
a planted error is not flagged is REJECTED and re-served, and the miss is logged, so reviewer reliability is measured.

  venv/bin/python faith_tool.py batch    <pass 1|2> <book> <surah> [from-to] [--chars 60000] [--by NAME]
  venv/bin/python faith_tool.py submit   <batch_id> <tsv-file>
  venv/bin/python faith_tool.py coverage [book]
  venv/bin/python faith_tool.py flags    [pass] [book]
  venv/bin/python faith_tool.py units    [pass] [chars per unit]      remaining work units as JSON (book, surah, from, to)

Verdict file (TSV, one line per entry id, nothing else): id <TAB> fit <TAB> tr <TAB> en <TAB> note
  fit: OK | WRONG_AYAH | PARTIAL          tr, en: OK | WRONG | OMISSION | ADDITION | UNSURE | FIXED
  A note is required for everything that is not OK.  FIXED = you corrected that reading with tr_tool.py put.
Rules: irab_library/audit_full/RULES.md
"""
import fcntl
import hashlib
import json
import os
import random
import re
import sys
import time
from pathlib import Path

LIB = Path(__file__).parent.parent / "irab_library"
AF = Path(os.environ.get("FAITH_AF") or LIB / "audit_full")   # FAITH_AF: separate ledger directory for pilots
LEDGER, SERVED = AF / "ledger", AF / "served"
FIT = {"OK", "WRONG_AYAH", "PARTIAL"}
TRV = {"OK", "WRONG", "OMISSION", "ADDITION", "UNSURE", "FIXED"}
PASS2_SAMPLE = 15          # % of pass-1-clean entries that a second, independent reviewer also reads
BOOKS = ["farraa", "akhfash", "zajjaj", "nahhas-irab", "nahhas-meani", "mekki-muskil", "ukberi-tibyan", "semin-durr",
         "daas-irab", "muyesser-irab", "celaleyn", "harrat-mujtaba", "safi-cedvel", "dervis-irab"]


def h(x):
    return hashlib.sha1(x.encode("utf-8")).hexdigest()[:12]


def src(s):
    return json.loads((LIB / f"s{int(s):03d}.json").read_text("utf-8"))["entries"]


def part(lang, book, s):
    p = LIB / f"{lang}_parts" / book / f"s{int(s):03d}.json"
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def led_path(book, s):
    return LEDGER / book / f"s{int(s):03d}.json"


def led_read(book, s):
    p = led_path(book, s)
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def led_update(book, s, fn):
    p = led_path(book, s)
    p.parent.mkdir(parents=True, exist_ok=True)
    lock = p.with_suffix(".lock")
    with open(lock, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        d = json.loads(p.read_text("utf-8")) if p.exists() else {}
        fn(d)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(d, ensure_ascii=False, indent=0), "utf-8")
        os.replace(tmp, p)


def current(book, s):
    """key -> (entry, tr text, en text, hashes)"""
    tr, en = part("tr", book, s), part("en", book, s)
    out = {}
    for e in src(s):
        if e["b"] != book:
            continue
        k = f"{book}:{e['s']}-{e['e']}"
        t, n = tr.get(k, {}).get("t", ""), en.get(k, {}).get("t", "")
        out[k] = (e, t, n, (h(e["t"]), h(t), h(n)))
    return out


def complete(rec, hs):
    return bool(rec) and (rec.get("ar"), rec.get("tr"), rec.get("en")) == hs and all(rec.get(x) for x in ("fit", "trv", "env"))


def audit_flagged(s):
    p = LIB / "audit" / f"s{int(s):03d}.json"
    if not p.exists():
        return set()
    return {f["key"] for f in json.loads(p.read_text("utf-8"))["findings"] if f["sev"] in ("high", "medium")}


def needs(book, s, pas, cur, led, flagged):
    """keys that still have to be reviewed in this pass"""
    out = []
    for k, (e, t, n, hs) in cur.items():
        if not t or not n:
            continue
        if pas == 1:
            if not complete(led.get(k, {}).get("p1"), hs):
                out.append(k)
        else:
            p1 = led.get(k, {}).get("p1")
            if not complete(p1, hs):
                continue
            risky = (p1.get("fit") != "OK" or p1.get("trv") != "OK" or p1.get("env") != "OK" or p1.get("fixed")
                     or k in flagged or int(h(k), 16) % 100 < PASS2_SAMPLE)
            if risky and not complete(led.get(k, {}).get("p2"), hs):
                out.append(k)
    return out


# ---------------------------------------------------------------- batch
def subtle(text, kind, lang):
    """a small, plausible corruption of the reading; None when the text has nothing to corrupt this way"""
    if kind == "digit":
        m = re.search(r"(?<![\w.])(\d{1,3})(?![\w])", text)
        if not m: return None
        n = int(m.group(1))
        return text[:m.start()] + str(n + 1 if n < 900 else n - 1) + text[m.end():]
    if kind == "negate":
        pat = r"\b(not|no|never|nor|neither)\b " if lang == "en" else r"\b(değil|yoktur|yok|asla|hiçbir)\b ?"
        m = re.search(pat, text)
        return (text[:m.start()] + text[m.end():]) if m else None
    return None


def make_canary(k, cur, lang, kind, seed):
    e, t, n, _ = cur[k]
    text = t if lang == "tr" else n
    rnd = random.Random(seed)
    if kind in ("digit", "negate"):
        return subtle(text, kind, lang)
    if kind == "trunc":
        cut = text[: int(len(text) * 0.5)]
        return cut[: cut.rfind(" ")] if " " in cut else cut
    others = [x for x in cur if x != k and len(cur[x][1 if lang == "tr" else 2]) > 80]
    return cur[rnd.choice(others)][1 if lang == "tr" else 2] if others else text[: len(text) // 2]


def pick_canary(k, cur, rnd):
    """choose (lang, kind); subtle kinds only when the text really contains something to corrupt"""
    opts = [("tr", "swap"), ("en", "swap"), ("tr", "trunc"), ("en", "trunc")]
    for lang in ("tr", "en"):
        text = cur[k][1] if lang == "tr" else cur[k][2]
        for kind in ("digit", "negate", "negate"):
            if subtle(text, kind, lang): opts.append((lang, kind))
    return rnd.choice(opts)


def cmd_batch(pas, book, surah, *rest):
    pas = int(pas)
    chars, by, rng = 60000, "agent", None
    i = 0
    rest = list(rest)
    while i < len(rest):
        if rest[i] == "--chars":
            chars = int(rest[i + 1]); i += 2
        elif rest[i] == "--by":
            by = rest[i + 1]; i += 2
        else:
            rng = rest[i]; i += 1
    a, z = (int(x) for x in rng.split("-")) if rng else (1, 999)
    cur, led = current(book, surah), led_read(book, surah)
    todo = [k for k in needs(book, surah, pas, cur, led, audit_flagged(surah)) if a <= int(cur[k][0]["s"]) <= z]
    if not todo:
        print("NOTHING LEFT in this range for pass", pas)
        return
    bid = f"p{pas}-{book}-{int(surah):03d}-{int(time.time()) % 10**7}-{os.getpid() % 1000}"
    pick, size = [], 0
    for k in todo:
        e, t, n, _ = cur[k]
        sz = len(e["t"]) + len(t) + len(n)
        if pick and size + sz > chars:
            break
        pick.append(k); size += sz
    # planted errors: about one in ten entries (at least one per batch of 5+), only on entries long enough to matter
    rnd = random.Random(bid)
    cands = [k for k in pick if len(cur[k][0]["t"]) > 120 and len(cur[k][1]) > 120 and len(cur[k][2]) > 120]
    canaries = {}
    for k in cands:
        if rnd.random() < 0.10:
            canaries[k] = pick_canary(k, cur, rnd)
    if not canaries and len(cands) >= 5:
        k = rnd.choice(cands); canaries[k] = pick_canary(k, cur, rnd)
    items, shown = [], {}
    for n_, k in enumerate(pick, 1):
        e, t, n, hs = cur[k]
        if k in canaries:
            lang, kind = canaries[k]
            bad = make_canary(k, cur, lang, kind, f"{bid}{k}")
            if lang == "tr": t = bad
            else: n = bad
        items.append({"n": n_, "key": k, "hs": list(hs), "canary": list(canaries[k]) if k in canaries else None})
        shown[n_] = (e, t, n)
    SERVED.mkdir(parents=True, exist_ok=True)
    (SERVED / f"{bid}.json").write_text(json.dumps({"id": bid, "pass": pas, "book": book, "surah": int(surah), "by": by, "items": items}), "utf-8")
    w = json.loads((LIB / "w" / f"s{int(surah):03d}.json").read_text("utf-8"))
    print(f"BATCH {bid}  pass {pas}  {book}  surah {surah}  {len(pick)} entries  ({len(todo) - len(pick)} more waiting after this batch)")
    print("Give a verdict for EVERY id below (see the file format in RULES.md). Check: (1) FIT: is the Arabic entry about its own ayah(s)?"
          " (2) Turkish and (3) English: complete, faithful, nothing added, nothing missing.\n")
    ay = sorted({a_ for e, _, _ in shown.values() for a_ in range(int(e["s"]), int(e["e"]) + 1)})
    print("=== AYAH CONTEXT (Quran text, Diyanet, English) for ayahs the entries below belong to ===")
    for a_ in ay[:14]:
        v = w[str(a_)]
        print(f"[{surah}:{a_}] {' '.join(x['ar'] for x in v['w'])}\n   TR: {v['m'].get('77')}\n   EN: {v['m'].get('20')}")
    if len(ay) > 14:
        print(f"... and ayahs {ay[14]}-{ay[-1]} (use: venv/bin/python audit_tool.py show {surah} <key> for any entry)")
    for n_, (e, t, n) in shown.items():
        print(f"\n########## ID {n_}   ayah {surah}:{e['s']}" + (f"-{e['e']}" if e['e'] != e['s'] else ""))
        print(f"--- ARABIC\n{e['t']}\n--- TURKISH\n{t}\n--- ENGLISH\n{n}")


# ---------------------------------------------------------------- submit
def cmd_submit(bid, tsv):
    sp = SERVED / f"{bid}.json"
    if not sp.exists():
        sys.exit("unknown or already used/rejected batch id")
    man = json.loads(sp.read_text("utf-8"))
    book, s, pas = man["book"], man["surah"], man["pass"]
    items = {it["n"]: it for it in man["items"]}
    got, errs = {}, []
    for ln in Path(tsv).read_text("utf-8").splitlines():
        if not ln.strip():
            continue
        c = ln.split("\t")
        if len(c) < 4 or not c[0].strip().isdigit():
            errs.append(f"bad line: {ln[:60]!r}"); continue
        n = int(c[0]); note = c[4].strip() if len(c) > 4 else ""
        fit, tr, en = c[1].strip(), c[2].strip(), c[3].strip()
        if n not in items: errs.append(f"unknown id {n}")
        elif n in got: errs.append(f"id {n} given twice")
        elif fit not in FIT or tr not in TRV or en not in TRV: errs.append(f"id {n}: values must be fit {sorted(FIT)}, tr/en {sorted(TRV)}")
        elif (fit != "OK" or tr != "OK" or en != "OK") and not note: errs.append(f"id {n}: a note is required when anything is not OK")
        else: got[n] = (fit, tr, en, note)
    miss = sorted(set(items) - set(got))
    if miss: errs.append(f"missing verdicts for ids {miss}")
    if errs:
        sys.exit("NOT ACCEPTED (nothing recorded, fix the file and submit again):\n  " + "\n  ".join(errs))
    # planted errors must have been caught
    log = AF / "canary_log.jsonl"
    missed = []
    for it in man["items"]:
        if it["canary"]:
            lang = it["canary"][0]
            v = got[it["n"]][1 if lang == "tr" else 2]
            ok = v != "OK"
            with open(log, "a", encoding="utf-8") as f:
                f.write(json.dumps({"batch": bid, "key": it["key"], "type": it["canary"], "detected": ok, "pass": pas, "by": man["by"]}) + "\n")
            if not ok: missed.append(it["n"])
    if missed:
        sp.unlink()
        sys.exit(f"REJECTED: a deliberately planted error was shown to you in id(s) {missed} and you marked it OK. Nothing from this batch was "
                 "recorded. Read every entry again carefully (compare sentence by sentence, check the end of each text) and ask for a new batch.")
    cur = current(book, s)
    now = time.strftime("%Y-%m-%d %H:%M")
    bad = []

    def upd(d):
        for it in man["items"]:
            k = it["key"]; fit, tr, en, note = got[it["n"]]
            ar_h, tr_h, en_h = cur[k][3]
            fixed = tr == "FIXED" or en == "FIXED"
            if not fixed and [ar_h, tr_h, en_h] != it["hs"]:
                bad.append(it["n"]); continue            # a reading changed while it was being reviewed
            rec = {"ar": ar_h, "tr": tr_h, "en": en_h, "fit": fit, "trv": tr, "env": en, "note": note, "by": man["by"], "at": now, "fixed": fixed}
            if it["canary"]:                              # the canaried language was not shown for real: it is NOT reviewed
                rec["trv" if it["canary"][0] == "tr" else "env"] = None
            d.setdefault(k, {})[f"p{pas}"] = rec

    led_update(book, s, upd)
    sp.unlink()
    left = len(needs(book, s, pas, current(book, s), led_read(book, s), audit_flagged(s)))
    print(f"ACCEPTED {len(got) - len(bad)} entries" + (f"; ids {bad} changed during review and stay open" if bad else "") +
          f". Still open for this book/surah/pass: {left}. Ask for the next batch until it says NOTHING LEFT.")


# ---------------------------------------------------------------- reports
def cmd_coverage(book=None):
    tot = {"entries": 0, "p1": 0, "flag": 0, "p2_need": 0, "p2_done": 0}
    print(f"{'book':16}{'entries':>8}{'pass1 done':>11}{'flagged':>9}{'pass2 due':>10}{'pass2 done':>11}")
    for b in ([book] if book else BOOKS):
        c = {"entries": 0, "p1": 0, "flag": 0, "p2_need": 0, "p2_done": 0}
        for s in range(1, 115):
            cur = current(b, s)
            if not cur: continue
            led = led_read(b, s); fl = audit_flagged(s)
            for k, (e, t, n, hs) in cur.items():
                c["entries"] += 1
                p1 = led.get(k, {}).get("p1")
                if complete(p1, hs):
                    c["p1"] += 1
                    if p1["fit"] != "OK" or p1["trv"] != "OK" or p1["env"] != "OK" or p1.get("fixed"): c["flag"] += 1
                    if p1["fit"] != "OK" or p1["trv"] != "OK" or p1["env"] != "OK" or p1.get("fixed") or k in fl or int(h(k), 16) % 100 < PASS2_SAMPLE:
                        c["p2_need"] += 1
                        if complete(led.get(k, {}).get("p2"), hs): c["p2_done"] += 1
        print(f"{b:16}{c['entries']:>8}{c['p1']:>11}{c['flag']:>9}{c['p2_need']:>10}{c['p2_done']:>11}")
        for k in tot: tot[k] += c[k]
    print(f"{'TOTAL':16}{tot['entries']:>8}{tot['p1']:>11}{tot['flag']:>9}{tot['p2_need']:>10}{tot['p2_done']:>11}")
    log = AF / "canary_log.jsonl"
    if log.exists():
        rows = [json.loads(x) for x in log.read_text("utf-8").splitlines() if x.strip()]
        d = sum(r["detected"] for r in rows)
        print(f"planted errors shown: {len(rows)}, caught: {d} ({100 * d / max(1, len(rows)):.1f}%), missed: {len(rows) - d}")


def cmd_flags(pas="1", book=None):
    for b in ([book] if book else BOOKS):
        for s in range(1, 115):
            for k, v in sorted(led_read(b, s).items()):
                r = v.get(f"p{pas}")
                if r and (r.get("fit") != "OK" or r.get("trv") != "OK" or r.get("env") != "OK" or r.get("fixed")):
                    print(json.dumps({"surah": s, "key": k, "fit": r.get("fit"), "tr": r.get("trv"), "en": r.get("env"), "note": r.get("note"), "by": r.get("by")}, ensure_ascii=False))


def cmd_units(pas="1", unit_chars="240000"):
    """Work units: [book, [[surah, from, to], ...]] of about unit_chars characters, small neighbouring surahs packed together."""
    unit_chars, out = int(unit_chars), []
    for b in BOOKS:
        segs, acc = [], 0
        for s in range(1, 115):
            cur = current(b, s)
            if not cur: continue
            todo = needs(b, s, int(pas), cur, led_read(b, s), audit_flagged(s))
            first = last = None
            for k in todo:
                e, t, n, _ = cur[k]
                sz = len(e["t"]) + len(t) + len(n)
                if acc and acc + sz > unit_chars:
                    if first is not None: segs.append([s, first, last]); first = None
                    out.append([b, segs]); segs, acc = [], 0
                first = int(e["s"]) if first is None else first
                last = int(e["e"]); acc += sz
            if first is not None: segs.append([s, first, last])
        if segs: out.append([b, segs])
    print(json.dumps(out))


if __name__ == "__main__":
    cmds = {"batch": cmd_batch, "submit": cmd_submit, "coverage": cmd_coverage, "flags": cmd_flags, "units": cmd_units}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv[1]](*sys.argv[2:])
