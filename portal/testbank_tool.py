"""Validate and snap the multiple-choice question banks in portal/testbank/.

    python3 testbank_tool.py validate [L1W1 ...]   # check structure + ayah quotes
    python3 testbank_tool.py snap [L1W1 ...]       # rewrite each quote in exact Uthmani spelling
    python3 testbank_tool.py part <file>           # validate+snap one topic file\n    python3 testbank_tool.py check <chapter>       # assemble + validate + acceptance statistics (JSON)\n    python3 testbank_tool.py assemble L1W1         # merge parts/<ch>/*.json into <ch>.json\n    python3 testbank_tool.py report                # counts per chapter / topic

Bank file (testbank/<L#W#>.json, assembled from testbank/parts/<L#W#>/*.json):
  {"chapter": "L1W1",
   "topics": [{"id": "t1", "section": 0, "title": {en,tr}, "rule": {en,tr}}],
   "questions": [{"id": "L1W1-t1-01", "topic": "t1", "difficulty": 1|2|3,
                  "ref": "1:2" | "2:255-256", "quote": "<arabic taken from the ayah>",
                  "stem": {en,tr}, "options": [{"text": {en,tr}|"ar": str, "why": {en,tr}} x4],
                  "correct": 0-3}]}
The quote must be words of the cited ayah(s): that is how "all examples are from the Quran" is enforced.
"""
import json, re, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).parent
BANK = HERE / "testbank"
QURAN = HERE.parent / "Irab Kitaplari" / "_kelime" / "qurancom.json"
LANGS = ("en", "tr")

_DROP = re.compile("[ؐ-ًؚ-ٰٟۖ-ۭـ‌‍࣓-ࣿ]")
_MAP = str.maketrans({"ٱ": "ا", "أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ؤ": "و", "ئ": "ي", "ء": "", "ة": "ه"})


def norm(word):
    w = unicodedata.normalize("NFC", word).replace("\u0648\u0670", "")   # صَلَوٰة (waw + dagger alef) = صلاة
    w = _DROP.sub("", w).translate(_MAP)
    return re.sub("[اي ]", "", w)       # alef/ya are spelled differently in Uthmani vs plain spelling        # alef is written differently in Uthmani vs plain spelling


def load_quran():
    return json.loads(QURAN.read_text("utf-8"))["ayahs"]


def ayah_words(quran, ref):
    """Uthmani words of a ref like '2:255' or '2:255-256'."""
    s, a = ref.split(":")
    lo, _, hi = a.partition("-")
    out = []
    for n in range(int(lo), int(hi or lo) + 1):
        out += [w[0] for w in quran[f"{s}:{n}"]["w"]]
    return out


def find_span(words, quote):
    """Match quote words against the ayah, ignoring stop-mark tokens (e.g. a lone ۚ) that normalise to nothing."""
    q = [t for t in (norm(t) for t in quote.split()) if t]
    kept = [(norm(w), w) for w in words]
    kept = [(n, w) for n, w in kept if n]
    nw = [n for n, _ in kept]
    for i in range(len(nw) - len(q) + 1):
        if nw[i:i + len(q)] == q:
            return " ".join(w for _, w in kept[i:i + len(q)])
    return None


def check_bank(bank, quran, snap=False):
    errs = []
    topics = {t["id"]: t for t in bank.get("topics", [])}
    for t in topics.values():
        for k in ("title", "rule"):
            if not all(t.get(k, {}).get(l) for l in LANGS):
                errs.append(f"topic {t['id']}: missing {k} in en/tr")
    seen_stems = set()
    for q in bank["questions"]:
        qid = q.get("id", "?")
        def bad(m): errs.append(f"{qid}: {m}")
        if q.get("topic") not in topics: bad("unknown topic")
        if q.get("difficulty") not in (1, 2, 3): bad("difficulty must be 1-3")
        if not all(q.get("stem", {}).get(l) for l in LANGS): bad("stem needs en+tr")
        opts = q.get("options", [])
        if len(opts) != 4: bad("needs exactly 4 options")
        if q.get("correct") not in (0, 1, 2, 3): bad("correct must be 0-3")
        labels = []
        for i, o in enumerate(opts):
            if not all(o.get("why", {}).get(l) for l in LANGS): bad(f"option {i} needs why en+tr")
            t = o.get("text")
            ok = (isinstance(o.get("ar"), str) and o["ar"].strip()) or (isinstance(t, dict) and all(t.get(l) for l in LANGS))
            if not ok: bad(f"option {i} needs text en+tr or ar")
            labels.append(json.dumps([o.get("ar"), t], ensure_ascii=False, sort_keys=True))
        if len(set(labels)) != len(labels): bad("duplicate options")
        key = re.sub(r"\W+", "", q.get("stem", {}).get("en", "").lower()) + "|" + q.get("quote", "")
        if key in seen_stems: bad("duplicate stem+quote")
        seen_stems.add(key)
        try:
            span = find_span(ayah_words(quran, q["ref"]), q["quote"])
        except Exception as e:
            span = None; bad(f"bad ref {q.get('ref')!r}: {e}")
        else:
            if span is None: bad(f"quote not found in {q['ref']}: {q.get('quote')!r}")
            elif snap: q["quote"] = span
    return errs


def chapters(args):
    return [BANK / f"{a}.json" for a in args] if args else sorted(BANK.glob("L?W*.json"))


def main(cmd, *args):
    quran = load_quran()
    if cmd in ("validate", "snap"):
        total = 0
        for p in chapters(args):
            bank = json.loads(p.read_text("utf-8"))
            errs = check_bank(bank, quran, snap=cmd == "snap")
            if cmd == "snap" and not errs:
                p.write_text(json.dumps(bank, ensure_ascii=False, indent=1), "utf-8")
            print(f"{p.stem}: {len(bank['questions'])} questions, {len(errs)} errors")
            for e in errs[:40]: print("   ", e)
            total += len(errs)
        sys.exit(1 if total else 0)
    elif cmd == "part":     # part <file>: validate one topic file and snap its quotes in place
        p = Path(args[0]); x = json.loads(p.read_text("utf-8"))
        bank = {"topics": [x["topic"]], "questions": x["questions"]}
        errs = check_bank(bank, quran, snap=True)
        if not errs: p.write_text(json.dumps(x, ensure_ascii=False, indent=1), "utf-8")
        print(f"{p.name}: {len(x['questions'])} questions, {len(errs)} errors")
        for e in errs[:60]: print("   ", e)
        sys.exit(1 if errs else 0)
    elif cmd == "check":    # check <chapter>: assemble (if parts exist) + validate + acceptance statistics, JSON on stdout
        ch = args[0]
        if (BANK / "parts" / ch).exists() and list((BANK / "parts" / ch).glob("*.json")):
            parts = [json.loads(f.read_text("utf-8")) for f in sorted((BANK / "parts" / ch).glob("*.json"))]
            topics = {}
            for x in parts: topics.setdefault(x["topic"]["id"], x["topic"])
            (BANK / f"{ch}.json").write_text(json.dumps({"chapter": ch, "topics": list(topics.values()),
                "questions": [q for x in parts for q in x["questions"]]}, ensure_ascii=False, indent=1), "utf-8")
        bank = json.loads((BANK / f"{ch}.json").read_text("utf-8"))
        errs = check_bank(bank, quran, snap=True)
        if not errs: (BANK / f"{ch}.json").write_text(json.dumps(bank, ensure_ascii=False, indent=1), "utf-8")
        qs = bank["questions"]
        per_topic, ayahs, pos = {}, {}, [0, 0, 0, 0]
        for q in qs:
            per_topic[q["topic"]] = per_topic.get(q["topic"], 0) + 1
            ayahs[q["ref"]] = ayahs.get(q["ref"], 0) + 1
            pos[q["correct"]] += 1
        problems = list(errs)
        if not 100 <= len(qs) <= 200: problems.append(f"pool size {len(qs)} is outside 100-200")
        for t in bank["topics"]:
            if per_topic.get(t["id"], 0) < 15: problems.append(f"topic {t['id']} has only {per_topic.get(t['id'], 0)} questions (min 15)")
        for ref, n in sorted(ayahs.items()):
            if n > 2: problems.append(f"ayah {ref} is used {n} times (max 2)")
        if qs and max(pos) / len(qs) > 0.35: problems.append(f"correct answer positions unbalanced {pos}")
        print(json.dumps({"chapter": ch, "ok": not problems, "pool": len(qs), "perTopic": per_topic, "positions": pos,
                          "problems": problems[:60]}, ensure_ascii=False))
        sys.exit(0)
    elif cmd == "parts":    # parts <chapter>: JSON {"files": {name: question count}, "used": [ayah refs]} for resuming authoring
        ch = args[0]; files, used = {}, []
        for f in sorted((BANK / "parts" / ch).glob("*.json")) if (BANK / "parts" / ch).exists() else []:
            try:
                x = json.loads(f.read_text("utf-8")); files[f.name] = len(x["questions"]); used += [q["ref"] for q in x["questions"]]
            except Exception: files[f.name] = -1
        revs = [int(m.group(1)) for f in (BANK / "reviews").glob(f"{ch}_review*.txt") if (m := re.search(r"_review(\d+)\.txt$", f.name))]
        print(json.dumps({"chapter": ch, "files": files, "used": used, "reviews": max(revs, default=0)}, ensure_ascii=False))
    elif cmd == "assemble":
        for ch in args:
            parts = [json.loads(f.read_text("utf-8")) for f in sorted((BANK / "parts" / ch).glob("*.json"))]
            topics = {}
            for x in parts:                      # a topic may be written in several batch files (t1a.json, t1b.json)
                topics.setdefault(x["topic"]["id"], x["topic"])
            bank = {"chapter": ch, "topics": list(topics.values()),
                    "questions": [q for x in parts for q in x["questions"]]}
            (BANK / f"{ch}.json").write_text(json.dumps(bank, ensure_ascii=False, indent=1), "utf-8")
            print(ch, len(bank["topics"]), "topics", len(bank["questions"]), "questions")
    elif cmd == "report":
        for p in chapters(args):
            bank = json.loads(p.read_text("utf-8"))
            by = {}
            for q in bank["questions"]:
                by.setdefault(q["topic"], [0, 0, 0, 0])[q["difficulty"]] += 1
            print(p.stem, len(bank["questions"]), {k: v[1:] for k, v in sorted(by.items())})


if __name__ == "__main__":
    main(*sys.argv[1:])
