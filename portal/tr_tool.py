"""Helper for preparing Turkish readings of i'rab library entries.

    venv/bin/python tr_tool.py list <book> <surah>            # entries + status
    venv/bin/python tr_tool.py show <book> <surah> <key>      # one entry's Arabic text
    venv/bin/python tr_tool.py put  <book> <surah> <key> <txt-file>
    venv/bin/python tr_tool.py status                         # counts per book

<key> is "<first>-<last>" (e.g. 2-2). Translations are stored in
irab_library/tr_parts/<book>/sNNN.json as {"<book>:<first>-<last>":
{"t": ..., "reviewed": false}}; build_irab_library.py merges them into
irab_library/tr/sNNN.json. Style rules: irab_library/glossary_tr.md.
"""

import datetime
import hashlib
import json
import sys
from pathlib import Path

LIB = Path(__file__).parent.parent / "irab_library"


def entries(book, surah):
    data = json.loads((LIB / f"s{int(surah):03d}.json").read_text("utf-8"))
    return {f"{e['s']}-{e['e']}": e["t"] for e in data["entries"] if e["b"] == book}


def part_path(book, surah):
    return LIB / "tr_parts" / book / f"s{int(surah):03d}.json"


def load_part(book, surah):
    p = part_path(book, surah)
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def main(cmd, *args):
    if cmd == "list":
        book, surah = args
        done = load_part(book, surah)
        for key, text in entries(book, surah).items():
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
        if not text:
            sys.exit("empty translation")
        part = load_part(book, surah)
        first, last = (int(x) for x in key.split("-"))
        part[f"{book}:{key}"] = {
            "t": text,
            "reviewed": False,
            # Provenance: exactly which source entry (and which version of its
            # Arabic text) this reading was made from.
            "src": {"book": book, "sure": int(surah), "ayet_bas": first, "ayet_son": last,
                    "sha1": hashlib.sha1(entries(book, surah)[key].encode("utf-8")).hexdigest()},
            "by": "Claude (makine çevirisi)",
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        }
        p = part_path(book, surah)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(part, ensure_ascii=False, indent=1), "utf-8")
        print(f"saved {book}:{key} ({len(text)} chars)")
    elif cmd == "status":
        for d in sorted((LIB / "tr_parts").glob("*")):
            n = sum(len(json.loads(f.read_text("utf-8"))) for f in d.glob("s*.json"))
            print(f"{d.name:16} {n} entries")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(*sys.argv[1:]) if len(sys.argv) > 1 else sys.exit(__doc__)
