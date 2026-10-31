"""Helper for Turkish word meanings in the word-by-word grid.

    venv/bin/python wtr_tool.py list <surah> [first-last]  # a:w  arabic | translit | english | grammar  [✓ done]
    venv/bin/python wtr_tool.py put  <surah> <tsv-file>  # lines "a:w<TAB>turkish meaning"
    venv/bin/python wtr_tool.py status

Saves to irab_library/words_tr/sNNN.json as {"a:w": {"t", "src": {ar, en, sha1}, "by", "at"}};
build_irab_library.py merges them into the grid. Style: irab_library/glossary_tr.md.
"""

import datetime
import fcntl
import hashlib
import json
import sys
from pathlib import Path

LIB = Path(__file__).parent.parent / "irab_library"


def words(surah):
    data = json.loads((LIB / "w" / f"s{int(surah):03d}.json").read_text("utf-8"))
    return {f"{a}:{i}": w for a, v in data.items() for i, w in enumerate(v["w"], start=1)}


def path(surah):
    return LIB / "words_tr" / f"s{int(surah):03d}.json"


def load(surah):
    p = path(surah)
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def main(cmd, *args):
    if cmd == "list":
        done = load(args[0])
        lo, hi = (int(x) for x in args[1].split("-")) if len(args) > 1 else (1, 10**4)
        for k, w in words(args[0]).items():
            if not lo <= int(k.split(":")[0]) <= hi:
                continue
            print(f"[{'✓' if k in done else ' '}] {k}\t{w['ar']} | {w['tl']} | {w['en']} | {w['pt']}")
    elif cmd == "put":
        surah, tsv = args
        path(surah).parent.mkdir(parents=True, exist_ok=True)
        # several agents may save the same surah concurrently: lock around read-modify-write
        lock = open(path(surah).with_suffix(".lock"), "w")
        fcntl.flock(lock, fcntl.LOCK_EX)
        ws, out, n = words(surah), load(surah), 0
        now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        for line in Path(tsv).read_text("utf-8").splitlines():
            if not line.strip():
                continue
            key, _, tr = line.partition("\t")
            key, tr = key.strip(), tr.strip()
            if key not in ws or not tr:
                sys.exit(f"bad line: {line!r}")
            w = ws[key]
            out[key] = {"t": tr, "by": "Claude (makine çevirisi)", "at": now,
                        "src": {"ar": w["ar"], "en": w["en"],
                                "sha1": hashlib.sha1((w["ar"] + "|" + w["en"]).encode("utf-8")).hexdigest()}}
            n += 1
        tmp = path(surah).with_suffix(".tmp")
        tmp.write_text(json.dumps(out, ensure_ascii=False, indent=1), "utf-8")
        tmp.replace(path(surah))
        fcntl.flock(lock, fcntl.LOCK_UN)
        print(f"saved {n} words for surah {surah} ({len(out)}/{len(ws)} done)")
    elif cmd == "status":
        for p in sorted((LIB / "words_tr").glob("s*.json")):
            print(p.stem, len(json.loads(p.read_text("utf-8"))))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(*sys.argv[1:]) if len(sys.argv) > 1 else sys.exit(__doc__)
