"""Helper for preparing Turkish readings of i'rab library entries.

    venv/bin/python tr_tool.py list <book> <surah> [first-last]  # entries + status
    venv/bin/python tr_tool.py show <book> <surah> <key>      # one entry's Arabic text
    venv/bin/python tr_tool.py put  <book> <surah> <key> <txt-file>
    venv/bin/python tr_tool.py status                         # counts per book
    venv/bin/python tr_tool.py --lang en <command> …          # English readings (en_parts/); default is Turkish

<key> is "<first>-<last>" (e.g. 2-2). Translations are stored in
irab_library/tr_parts/<book>/sNNN.json as {"<book>:<first>-<last>":
{"t": ..., "reviewed": false}}; build_irab_library.py merges them into
irab_library/tr/sNNN.json. Style rules: irab_library/glossary_tr.md.
"""

import datetime
import fcntl
import hashlib
import json
import sys
from pathlib import Path

import guardrails

LIB = Path(__file__).parent.parent / "irab_library"


def entries(book, surah):
    data = json.loads((LIB / f"s{int(surah):03d}.json").read_text("utf-8"))
    return {f"{e['s']}-{e['e']}": e["t"] for e in data["entries"] if e["b"] == book}


LANG = "tr"   # set by --lang; "en" readings live in en_parts/ with the same layout
PARTS = {"tr": "tr_parts", "en": "en_parts"}
BY = {"tr": "Claude (makine çevirisi)", "en": "Claude (machine translation)"}


def part_path(book, surah):
    return LIB / PARTS[LANG] / book / f"s{int(surah):03d}.json"


def load_part(book, surah):
    p = part_path(book, surah)
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def main(cmd, *args):
    if cmd == "list":
        book, surah = args[:2]
        lo, hi = (int(x) for x in args[2].split("-")) if len(args) > 2 else (1, 10**4)
        done = load_part(book, surah)
        for key, text in entries(book, surah).items():
            first, last = (int(x) for x in key.split("-"))
            if last < lo or first > hi:
                continue
            mark = "✓" if f"{book}:{key}" in done else " "
            print(f"[{mark}] {key:>9}  {len(text):6} chars")
    elif cmd == "show":
        book, surah, key = args
        print(entries(book, surah)[key])
    elif cmd == "put":
        book, surah, key, txt = args
        if key not in entries(book, surah):
            sys.exit(f"unknown key {key} for {book} s{surah}")
        text = Path(txt).read_text("utf-8").strip()
        if key not in entries(book, surah):
            sys.exit(f"unknown key {key} for {book} s{surah}")
        # guardrails: hard errors block the save, warnings are shown so they can be fixed
        errors, warnings = guardrails.check_entry(LANG, entries(book, surah)[key], text)
        for w in warnings:
            print(f"WARNING {book}:{key}: {w}")
        if errors:
            sys.exit("NOT SAVED — fix and put again:\n  " + "\n  ".join(errors))
        part_path(book, surah).parent.mkdir(parents=True, exist_ok=True)
        # several agents may save the same (book, surah) concurrently: lock around read-modify-write
        lock = open(part_path(book, surah).with_suffix(".lock"), "w")
        fcntl.flock(lock, fcntl.LOCK_EX)
        part = load_part(book, surah)
        first, last = (int(x) for x in key.split("-"))
        part[f"{book}:{key}"] = {
            "t": text,
            "reviewed": False,
            # Provenance: exactly which source entry (and which version of its
            # Arabic text) this reading was made from.
            "src": {"book": book, "sure": int(surah), "ayet_bas": first, "ayet_son": last,
                    "sha1": hashlib.sha1(entries(book, surah)[key].encode("utf-8")).hexdigest()},
            "by": BY[LANG],
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        }
        p = part_path(book, surah)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(part, ensure_ascii=False, indent=1), "utf-8")
        tmp.replace(p)
        fcntl.flock(lock, fcntl.LOCK_UN)
        print(f"saved {book}:{key} ({len(text)} chars)")
    elif cmd == "status":
        for d in sorted((LIB / "tr_parts").glob("*")):
            n = sum(len(json.loads(f.read_text("utf-8"))) for f in d.glob("s*.json"))
            print(f"{d.name:16} {n} entries")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv[:1] == ["--lang"]:
        LANG, argv = argv[1], argv[2:]
        if LANG not in PARTS:
            sys.exit(f"unknown language {LANG}")
    main(*argv) if argv else sys.exit(__doc__)
