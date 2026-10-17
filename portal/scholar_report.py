"""Scholar-review workbook (Excel) for the i'rab library.

  venv/bin/python scholar_report.py <out.xlsx> [baseline-git-commit]

Sheets: README, Guardrail warnings (TR+EN), Misplaced entries, Cases for a scholar, Translation changes (old vs new).
Everything is read from the repository: current readings from irab_library/{tr,en}_parts, the audit ledger and the
adjudication records from irab_library/audit_full, the old versions from git (default baseline: the last commit before the
full-fidelity audit). The Arabic book text is shown as published and is never altered.
"""
import difflib
import json
import subprocess
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).parent))
import adjudicate_tool as ad  # noqa: E402
import faith_tool as ft  # noqa: E402
import guardrails as gr  # noqa: E402

ROOT = Path(__file__).parent.parent
LIB = ROOT / "irab_library"
CAP = 32000                                   # Excel cell limit is 32,767 characters
BOOKS = {b["id"]: b for b in json.loads((LIB / "books.json").read_text("utf-8"))["books"] if b.get("kind") == "irab"}
DIM = {"tr": "Turkish reading", "en": "English reading", "fit": "Placement (which ayah it is listed under)"}


def cap(s):
    s = s or ""
    return s if len(s) <= CAP else s[:CAP] + "\n[… cut for Excel; full text is in the repository]"


def bname(b):
    x = BOOKS.get(b, {})
    d = f" (d. {x['death_h']} H)" if x.get("death_h") else ""
    return f"{x.get('title', {}).get('en', b)} — {x.get('author', {}).get('en', '')}{d}"


def src_entry(book, s, key):
    for e in json.loads((LIB / f"s{int(s):03d}.json").read_text("utf-8"))["entries"]:
        if f"{e['b']}:{e['s']}-{e['e']}" == key:
            return e
    return None


def part(lang, book, s, key):
    f = LIB / f"{lang}_parts" / book / f"s{int(s):03d}.json"
    return json.loads(f.read_text("utf-8")).get(key, {}) if f.exists() else {}


def ayah_label(key, s):
    a, z = key.split(":")[1].split("-")
    return f"{s}:{a}" if a == z else f"{s}:{a}-{z}"


def sheet(wb, title, header, rows, widths):
    ws = wb.create_sheet(title)
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E78")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append([cap(x) if isinstance(x, str) else x for x in r])
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    return ws


def warnings_rows():
    rows = []
    for lang in ("tr", "en"):
        for f in sorted((LIB / f"{lang}_parts").glob("*/s*.json")):
            book, s = f.parent.name, int(f.stem[1:])
            src = {f"{e['b']}:{e['s']}-{e['e']}": e for e in json.loads((LIB / f.name).read_text("utf-8"))["entries"]}
            for key, r in json.loads(f.read_text("utf-8")).items():
                if key not in src:
                    continue
                _, warns = gr.check_entry(lang, src[key]["t"], r["t"])
                for w in warns:
                    rows.append([lang.upper(), bname(book), s, ayah_label(key, s), key, w, src[key]["t"], r["t"]])
    return rows


def cases_rows():
    human, misplaced = [], []
    for b, s, k, rec in ad.records(None):
        e = src_entry(b, s, k)
        cur = ft.current(b, s)
        led = ft.led_read(b, s).get(k, {})
        for d, dm in rec["dims"].items():
            st, c = ad.status_of(dm, d)
            votes = "\n\n".join(f"{j}: {v['class']}" + (f" (range {v.get('ayahs')})" if v.get("ayahs") else "") + f"\n{v['evidence']}" for j, v in dm["votes"].items())
            if c == "MISPLACED":
                rng = sorted({v.get("ayahs") for v in dm["votes"].values()})
                misplaced.append([bname(b), s, k, ayah_label(k, s), f"{s}:{rng[0].replace('-', '–')}" if rng and rng[0] else "", votes, e["t"] if e else ""])
            elif c == "HUMAN":
                notes = []
                for pn in ("p1", "p2"):
                    r = led.get(pn) or {}
                    key = {"tr": "trv", "en": "env", "fit": "fit"}[d]
                    if r.get(key) not in (None, "OK"):
                        notes.append(f"{pn} reviewer ({r.get(key)}): {r.get('note', '')}")
                tr = part("tr", b, s, k).get("t", "")
                en = part("en", b, s, k).get("t", "")
                human.append([DIM[d], bname(b), s, ayah_label(k, s), k, votes, "\n".join(notes), e["t"] if e else "", tr, en])
    human.sort(key=lambda r: (r[1], r[2], r[3]))
    misplaced.sort(key=lambda r: (r[0], r[1], r[3]))
    return misplaced, human


def changed_rows(base):
    names = subprocess.check_output(["git", "diff", "--name-only", base, "HEAD", "--", "irab_library/tr_parts", "irab_library/en_parts"],
                                    cwd=ROOT, text=True).split()
    rows = []
    for n in sorted(names):
        lang = "tr" if "/tr_parts/" in n else "en"
        book, s = Path(n).parent.name, int(Path(n).stem[1:])
        try:
            old = json.loads(subprocess.check_output(["git", "show", f"{base}:{n}"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL))
        except subprocess.CalledProcessError:
            old = {}
        new = json.loads((ROOT / n).read_text("utf-8"))
        led = ft.led_read(book, s)
        adj = ad.read(book, s)
        src = {f"{e['b']}:{e['s']}-{e['e']}": e for e in json.loads((LIB / f"s{s:03d}.json").read_text("utf-8"))["entries"]}
        for key, r in new.items():
            o = (old.get(key) or {}).get("t")
            if o is None or o == r["t"]:
                continue
            ow, nw = o.split(), r["t"].split()
            sm = difflib.SequenceMatcher(None, ow, nw, autojunk=False)
            rem, add = [], []
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag in ("replace", "delete"):
                    rem.append(" ".join(ow[i1:i2]))
                if tag in ("replace", "insert"):
                    add.append(" ".join(nw[j1:j2]))
            why = []
            for pn in ("p1", "p2"):
                x = (led.get(key, {}).get(pn)) or {}
                dimkey = "trv" if lang == "tr" else "env"
                if x.get(dimkey) in ("FIXED", "WRONG", "OMISSION", "ADDITION", "UNSURE") or (x.get("fixed") and x.get("note")):
                    why.append(f"{pn} {x.get('by', '')}: {x.get(dimkey)} — {x.get('note', '')}")
            for dname, dm in (adj.get(key, {}).get("dims", {})).items():
                if dname == lang and dm.get("fixed_note"):
                    why.append(f"adjudication fix: {dm['fixed_note']}")
            e = src.get(key)
            rows.append([lang.upper(), bname(book), s, ayah_label(key, s), key, " | ".join(rem)[:3000], " | ".join(add)[:3000], "\n".join(why) or "(fix made during the audit; no note recorded)",
                         o, r["t"], (e or {}).get("t", ""), r.get("by", ""), r.get("at", "")])
    return rows


def main():
    out = sys.argv[1]
    base = sys.argv[2] if len(sys.argv) > 2 else "1d219f5"
    wb = Workbook()
    readme = wb.active
    readme.title = "README"
    warn = warnings_rows()
    mis, hum = cases_rows()
    chg = changed_rows(base)
    mp = LIB / "audit_full" / "meal_pairs" / "result.json"
    mrows = []
    if mp.exists():
        for cid, c in json.loads(mp.read_text("utf-8"))["cases"].items():
            if c["status"] == "CLEAR":
                continue
            mrows.append([c["meal"], c["first"], c["second"], c["status"] + (f" ({c['class']})" if c.get("class") else ""),
                          "\n\n".join(f"{j}: {v}\n{c['notes'].get(j, '')}" for j, v in c["votes"].items()), c["repeated_text"],
                          "\n".join(f"{k}: {v}" for k, v in c["arabic"].items())])
        mrows.sort(key=lambda r: (int(r[1].split(":")[0]), int(r[1].split(":")[1])))
    lines = [
        ["Quranic Arabic i'rab library — scholar review workbook"],
        [f"Baseline for 'old version': git commit {base} (the last state before the full-fidelity audit). 'New' = the current published readings."],
        [""],
        ["Sheet", "What it contains", "Rows"],
        ["Guardrail warnings", "Readings the automatic checker marked for attention (reading unusually short, Quranic quotation not found verbatim, footnote count differs). Warnings are signals, not errors: no check found a wrong reading, but a human should look.", len(warn)],
        ["Misplaced entries", "Entries that two independent judges (and a tie-break where needed) found to be listed under the wrong ayah(s), or to also cover further ayahs. The Arabic book text is never changed: only the ayah range it is LISTED under would change. Nothing has been moved yet — it awaits the owner's approval. 'Proposed listing' is the range the judges agreed on.", len(mis)],
        ["Cases for a scholar", "Cases the judges could not settle, or that need scholarly judgement (obscure/corrupt poetry lines, disputed glosses, unmarked additions in verses). Each shows both judges' evidence, the reviewers' notes, the Arabic and both current readings. Please give a ruling per row.", len(hum)],
        ["Meal text repeats", "Turkish meals (translations) that print identical text under two consecutive ayahs: all 902 such pairs were audited (892 are legitimate merged renderings); the rows here are the 9 confirmed errors (the text under one ayah belongs to its neighbour, i.e. the source meal is shifted or corrupted) and 1 split decision. Meals are unmodified; a scholar should decide whether to withhold, as was done for 87:14.", len(mrows)],
        ["Translation changes", "Every Turkish/English reading that the audit changed, with the old text, the new text, the words removed / added, why it was changed, and the Arabic source for checking. Changes were made only to the translations, never to the Arabic.", len(chg)],
        [""],
        ["How the audit worked", "Every one of 51,211 entries was read in full against its Turkish and English reading by two independent reviewers (second pass: a stronger model with a checklist for negations, numbers, exceptions, conditions, attributions, quotations, endings). Deliberately damaged copies were planted to measure the reviewers: 96.9% were caught (237 of 7,580 missed), so the audit is strong but not infallible — hence this scholar review."],
        ["Standards", "Unmarked additions must sit in «[Translator's note: …]» / «[Mütercim notu: …]». Quranic words stay in Arabic script. The source is never silently corrected."],
        ["Known open items", "Meal (Turkish translation) 'Dar Al-Salam Center' at 87:14 repeats the 87:13 text at the source (the live quran.com API returns the same); it is withheld from the portal because the true text could not be sourced. All Quran text and book text are unmodified."],
    ]
    for r in lines:
        readme.append(r)
    readme["A1"].font = Font(bold=True, size=14)
    for c in readme[4]:
        c.font = Font(bold=True)
    readme.column_dimensions["A"].width = 26
    readme.column_dimensions["B"].width = 110
    readme.column_dimensions["C"].width = 8
    for row in readme.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    sheet(wb, "Meal text repeats", ["Meal", "Ayah 1", "Ayah 2", "Outcome", "Judges' votes and evidence", "Repeated meal text", "Arabic (context)"], mrows, [14, 8, 8, 22, 90, 70, 80])
    sheet(wb, "Guardrail warnings", ["Lang", "Book", "Surah", "Ayah(s)", "Entry key", "Warning", "Arabic source", "Reading (as published)"], warn, [6, 38, 7, 10, 18, 50, 70, 70])
    sheet(wb, "Misplaced entries", ["Book", "Surah", "Entry key", "Currently listed under", "Proposed listing", "Judges' evidence", "Arabic source (unchanged)"], mis, [38, 7, 18, 14, 14, 90, 80])
    sheet(wb, "Cases for a scholar", ["Question about", "Book", "Surah", "Ayah(s)", "Entry key", "Judges' evidence", "Reviewers' notes", "Arabic source", "Turkish reading", "English reading"], hum, [22, 38, 7, 10, 18, 90, 60, 70, 60, 60])
    sheet(wb, "Translation changes", ["Lang", "Book", "Surah", "Ayah(s)", "Entry key", "Words removed (old)", "Words added (new)", "Why it was changed", "OLD reading", "NEW reading", "Arabic source", "Changed by", "Changed at"], chg, [6, 38, 7, 10, 18, 45, 45, 55, 70, 70, 60, 20, 22])
    wb.save(out)
    print(out, {"warnings": len(warn), "misplaced": len(mis), "human": len(hum), "changes": len(chg)})


if __name__ == "__main__":
    main()
