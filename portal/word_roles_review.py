"""Scholar-review workbook for the word-by-word grammar roles (mübteda, haber, hâl, şart, cevâb-ı şart).

  venv/bin/python word_roles_review.py <out.xlsx>

Tabs: README · 1 Verify tags (a stratified random sample: role × how many books agree) · 2 Books disagree (same role,
words 2+ apart) · 3 Missing roles (every word of random ayahs, to measure what we do not mark) · 4 Hidden by grammar check.
The reviewer never has to decide the grammar alone: each row shows the book line the tag was read from.
"""
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, str(Path(__file__).parent))
import build_word_roles as B  # noqa: E402

LIB = B.LIB
CAP = 32000
ROLE_NAME = {"mubteda": "Mübteda · Mubtada’ · مبتدأ", "haber": "Haber · Khabar · خبر", "hal": "Hâl · Ḥāl · حال",
             "sart": "Şart · Sharṭ · شرط", "cevap": "Cevâb-ı şart · Jawāb al-sharṭ · جواب الشرط",
             "ismInna": "İsm-i inne · Ism of inna · اسم إنّ", "ismKana": "İsm-i kâne · Ism of kāna · اسم كان"}
BOOKS = {b["id"]: b for b in json.loads((LIB / "books.json").read_text("utf-8"))["books"]}
BOOKS["qac"] = {"title": {"en": "Quranic Arabic Corpus morphology"}, "author": {"en": "corpus.quran.com"}}
BOOKS["derived"] = {"title": {"en": "Derived from the word's own grammar (not a book)"}, "author": {"en": "sentence_structure.py"}}
PER_CELL = 25                                   # tags per role × agreement tier
seed = random.Random(20261031)


def bname(b):
    x = BOOKS.get(b, {})
    return f"{x.get('title', {}).get('en', b)} — {x.get('author', {}).get('en', '')}".strip(" —")


def cap(s):
    s = s or ""
    return s if len(s) <= CAP else s[:CAP] + " […]"


def sheet(wb, title, header, rows, widths, dropdown=None):
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
    if dropdown and rows:
        col, options = dropdown
        dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col}2:{col}{len(rows) + 1}")
        for r in range(2, len(rows) + 2):
            ws[f"{col}{r}"].fill = PatternFill("solid", fgColor="FFF2CC")
    return ws


def load():
    """All published tags with their ayah words: [(surah, ayah, idx, tag, words)], plus the words per ayah."""
    tags, ayahs = [], {}
    for s in range(1, 115):
        w = json.loads((LIB / "w" / f"s{s:03d}.json").read_text("utf-8"))
        r = json.loads((LIB / "roles" / f"s{s:03d}.json").read_text("utf-8"))
        for a, v in w.items():
            ayahs[(s, int(a))] = [x["ar"] for x in v["w"]]
        for a, byword in r.items():
            for i, ts in byword.items():
                for t in ts:
                    tags.append((s, int(a), int(i), t))
    return tags, ayahs


def tier(t):
    n = len(t["src"])
    return "1 book" if n == 1 else "2 books" if n == 2 else "3+ books"


def main(out):
    tags, ayahs = load()
    wb = Workbook()
    wb.remove(wb.active)

    # 1 — stratified sample
    cells = defaultdict(list)
    for s, a, i, t in tags:
        cells[(t["r"], tier(t))].append((s, a, i, t))
    rows, ident = [], 0
    for role in B.ROLES:
        for tr in ("1 book", "2 books", "3+ books"):
            pool = cells[(role, tr)]
            for s, a, i, t in seed.sample(pool, min(PER_CELL, len(pool))):
                ident += 1
                words = ayahs[(s, a)]
                rows.append([f"V{ident:03d}", f"{s}:{a}", " ".join(words), words[i], i + 1, ROLE_NAME[role],
                             "sentence starting here" if t["scope"] == "clause" else "this word", tr,
                             "\n\n".join(f"[{bname(x['b'])}]\n{x['q']}" for x in t["src"]), "", "", ""])
    sheet(wb, "1 Verify tags",
          ["ID", "Ayah", "Ayah (words as in the grid)", "Marked word", "Word #", "Role shown to students", "Scope", "Books agreeing",
           "Book line(s) the tag was read from", "DECISION", "If wrong: the correct word # (or the correct role)", "Notes"],
          rows, [7, 8, 55, 14, 7, 22, 16, 10, 70, 18, 22, 28],
          dropdown=("J", ["Correct", "Wrong word", "Wrong role", "Book does not say this", "Unsure"]))

    # 2 — books disagree, far apart
    rows = []
    for s in range(1, 115):
        words = json.loads((LIB / "w" / f"s{s:03d}.json").read_text("utf-8"))
        _, _, merged = B.build_surah(s)
        for a, byword in merged.items():
            per = defaultdict(lambda: defaultdict(dict))
            for i, rs in byword.items():
                for role, t in rs.items():
                    if t["alt"]:
                        continue
                    for x in t["src"]:
                        if x["b"] not in (B.QAC, B.DERIVED):
                            per[role][x["b"]][i] = x["q"]
            for role, books in per.items():
                bl = list(books.items())
                for p in range(len(bl)):
                    for q in range(p + 1, len(bl)):
                        A, C = bl[p][1], bl[q][1]
                        if set(A) & set(C):
                            continue
                        d = min(abs(i - j) for i in A for j in C)
                        if d >= 2:
                            ia, ic = min(A), min(C)
                            ws = words[str(a)]["w"]
                            rows.append((s, int(a), role, bl[p][0], ia, ws[ia]["ar"], A[ia], bl[q][0], ic, ws[ic]["ar"], C[ic], d, " ".join(w["ar"] for w in ws)))
    total = len(rows)
    rows = seed.sample(rows, min(300, total))
    rows.sort(key=lambda r: (r[0], r[1]))
    sheet(wb, "2 Books disagree",
          ["ID", "Ayah", "Role", "Ayah (words as in the grid)", "Book A", "Word # (A)", "Word (A)", "Book A line", "Book B", "Word # (B)", "Word (B)",
           "Book B line", "Words apart", "WHICH IS RIGHT?", "Notes"],
          [[f"D{n:03d}", f"{r[0]}:{r[1]}", ROLE_NAME[r[2]], r[12], bname(r[3]), r[4] + 1, r[5], r[6], bname(r[7]), r[8] + 1, r[9], r[10], r[11], "", ""]
           for n, r in enumerate(rows, 1)],
          [7, 8, 22, 50, 22, 7, 12, 55, 22, 7, 12, 55, 7, 18, 28],
          dropdown=("N", ["A is right", "B is right", "Both (two roles)", "Neither", "Unsure"]))
    disagree_total = total

    # 3 — missing roles (recall): every word of random ayahs
    pick = seed.sample([k for k, w in ayahs.items() if 5 <= len(w) <= 18], 25)
    shown = defaultdict(list)
    for s, a, i, t in tags:
        shown[(s, a, i)].append(ROLE_NAME[t["r"]].split(" · ")[0] + (" (sentence)" if t["scope"] == "clause" else ""))
    rows = []
    for s, a in sorted(pick):
        for i, w in enumerate(ayahs[(s, a)]):
            rows.append([f"M{len(rows) + 1:03d}", f"{s}:{a}", i + 1, w, "، ".join(shown.get((s, a, i), [])) or "—", "", ""])
    sheet(wb, "3 Missing roles",
          ["ID", "Ayah", "Word #", "Word", "Roles we show for this word", "ROLE IT SHOULD HAVE (if one is missing)", "Notes"],
          rows, [7, 8, 7, 18, 34, 36, 30],
          dropdown=("F", ["Mübteda", "Haber", "Hâl", "Şart", "Cevâb-ı şart", "Nothing missing"]))

    # 4 — hidden by the grammar check
    hidden = json.loads((LIB / "roles" / "HIDDEN.json").read_text("utf-8"))
    rows = []
    for n, h in enumerate(hidden, 1):
        ref, idx = h["ref"].split("#")
        s, a = map(int, ref.split(":"))
        words = ayahs[(s, a)]
        rows.append([f"H{n:03d}", ref, " ".join(words), words[int(idx)], int(idx) + 1, ROLE_NAME[h["role"]], h["why"], ", ".join(bname(b) for b in h["books"]), "", ""])
    sheet(wb, "4 Hidden by grammar check",
          ["ID", "Ayah", "Ayah (words as in the grid)", "Word", "Word #", "Role the book(s) gave", "Why it is hidden", "Books", "DECISION", "Notes"],
          rows, [7, 8, 55, 14, 7, 24, 34, 40, 20, 28],
          dropdown=("I", ["Hidden rightly", "Should be shown", "Unsure"]))

    # README (first)
    ws = wb.create_sheet("README", 0)
    lines = [
        "Word-by-word grammar roles — scholar review",
        "",
        "What is being checked: the small chips under each word in the library's word-by-word grid (Mübteda, Haber, Hâl, Şart, Cevâb-ı şart).",
        "They are NOT computed grammar: each was read by a program from a classical i'rab book, and every row below shows the book line it came from.",
        "You do not need to decide the grammar alone — first check whether the book line really says the role, and on THAT word.",
        "",
        "Sheet 1 — Verify tags: a random sample, 25 per role per level of agreement (1 book / 2 books / 3+ books). Choose DECISION in the yellow column.",
        "   Correct = the line says this role on this word.  Wrong word = the role is right but belongs to another word (give its word #).",
        "   Wrong role = the line says a different role.  Book does not say this = the program misread the line.  Unsure.",
        f"Sheet 2 — Books disagree: {len(rows) and 300} of {disagree_total} cases where two books put the same role on words 2 or more apart. Say which book is right.",
        "Sheet 3 — Missing roles: every word of 25 random ayahs. Tell us where a role is missing so we can measure how much we do not mark.",
        "Sheet 4 — Hidden by grammar check: tags a program hid because the word's own grammar contradicts them (e.g. mübteda on a verb). Say if it was right to hide.",
        "",
        "Books: " + " · ".join(f"{bname(b)}" for b in (B.MUYASSAR, B.DAAS, B.SAFI, B.QAC)),
        "Colors on the page: al-I'rāb al-Muyassar = teal, Da'ās = orange, Ṣāfī = magenta, corpus = grey.",
        "",
        "Why this matters: results decide which tags we keep showing. For example, if tags confirmed by only one book are right under 90%, we will stop showing them.",
    ]
    for ln in lines:
        ws.append([ln])
    ws["A1"].font = Font(bold=True, size=14)
    ws.column_dimensions["A"].width = 150
    for row in ws.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(out)
    print(f"saved {out}: sheet1 {ident} tags · sheet2 300 of {disagree_total} disagreements · sheet3 25 ayahs · sheet4 {len(hidden)} hidden")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "word_roles_review.xlsx")
