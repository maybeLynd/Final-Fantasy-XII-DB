#!/usr/bin/env python3
"""check_counts.py - EC-5: does a document state a count and then tabulate a different one?

Why
---
`one-word-decides-which-fifteen-subsystems-tick.md` said *"fifteen distinct masks"* directly above a
table of **fourteen** rows, and carried that contradiction in plain sight until someone happened to
count. The missing row was the one update group reached by `jmp` instead of `call` — so the
mismatch was not cosmetic. **It was the only surviving evidence that a call-only census had been
used**, and the four-instrument rule had failed.

No existing gate compares those two numbers. `check_consistency` compares addresses *across*
documents; `check_denominators` checks that ratios declare a population; `verify_doc_addresses`
checks citations. A number introducing the table beneath it is checked by nobody.

That defect was found by eye. This finds it by sweep.

What counts as a finding
------------------------
A **stated count** — a digit or a number word from `two` to `ninety-nine` — appearing either in the
paragraph line immediately above a table, or in the nearest preceding heading, where the table's
data-row count differs.

**This is advisory, and the reason matters.** Prose near a table legitimately contains numbers that
are not the row count: *"the fifteen groups, six of which are UI-owned"* has two numbers and one of
them is not the table's length. So a finding is a **pair worth a human's eye**, not a defect. The
tool prints the sentence so that judgement is cheap.

To keep the noise honest rather than merely low:

- only the **last non-empty line** before the table is read as an introducer, plus the nearest
  heading, and each is reported with its source;
- a line with several numbers yields one candidate per number, and **a table matching any of them
  is clean** — which is exactly the "fifteen groups, six UI-owned" case;
- counts outside 2..200 are ignored, and so are lines that are themselves table rows.

Reach, stated plainly
---------------------
It compares a number to a row count. It cannot tell whether the number was *about* the table, and it
says so by calling every hit advisory. What it can do is guarantee the arithmetic in the page is
self-consistent wherever a count introduces an enumeration — which is where the update gate lost a
group.
"""
import argparse
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")

WORDS = {
    "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}
NUM = re.compile(r"(?<![A-Za-z0-9_])(\d{1,3})(?![0-9A-Fa-f]*[A-Za-z0-9_])")
WORD = re.compile(r"(?<![A-Za-z])(" + "|".join(sorted(WORDS, key=len, reverse=True)) + r")(?![A-Za-z])",
                  re.I)
SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")


# A count that introduces an enumeration is followed by what it counts: "fifteen distinct masks",
# "seven groups", "four authorities". A number that is a VALUE is not: "an 8-byte getter",
# "modes 4 and 5", "it is not 53". Requiring a plural noun within two adjectives is what separates
# them, and it took the sweep from 24 % of all tables to something a person can actually read.
_N = r"(?<![\w.])(?P<n>\d{1,3}|" + "|".join(sorted(WORDS, key=len, reverse=True)) + r")"
COUNTED = re.compile(_N + r"(?![-\w])\s+"
                     r"(?:[A-Za-z][\w`*'-]*\s+){0,2}"
                     r"[A-Za-z][\w`*'-]*s\b",
                     re.I)

EMPH = re.compile(r"[*_`]")

SECNUM = re.compile(r"^#+\s*\d+[a-z]*\.")        # "## 3.", "### 2b." - a section label
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
GROUPED = re.compile(r"\d{1,3}(?:,\d{3})+")        # 33,346 - never a small row count


def numbers_in(line):
    """-> set of plausible counts stated on this line.

    The first run of this sweep hit 1,114 of 2,431 tables. That was a measurement of the tool, not
    of the database: `## 3. The registry` contributed a "3" and `33,346` contributed a "33". A
    section label is not a count, a date is not a count, and a thousands-grouped number is never a
    row count -- so all three are removed before anything is read as one.
    """
    line = SECNUM.sub("", line)
    line = DATE.sub(" ", line)
    line = GROUPED.sub(" ", line)
    # Emphasis sits BETWEEN a count and what it counts -- "**fifteen** distinct masks" -- and the
    # positive control caught that the moment the plural-noun rule went in: the control itself was
    # written in bold and stopped being found. Strip emphasis before reading the sentence.
    line = EMPH.sub("", line)
    out = set()
    for m in COUNTED.finditer(line):
        tok = m.group("n")
        v = WORDS.get(tok.lower()) if not tok.isdigit() else int(tok)
        if v is not None and 2 <= v <= 200:
            out.add(v)
    return out


def tables(lines):
    """-> [(header_index, separator_index, data_row_count)] for every markdown table."""
    out = []
    i = 0
    while i < len(lines) - 1:
        if lines[i].lstrip().startswith("|") and SEP.match(lines[i + 1]):
            j = i + 2
            n = 0
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                n += 1
                j += 1
            out.append((i, i + 1, n))
            i = j
        else:
            i += 1
    return out


def introducers(lines, header_i):
    """-> [(kind, line_no, text)] the prose line above the table, and the nearest heading."""
    out = []
    k = header_i - 1
    while k >= 0 and not lines[k].strip():
        k -= 1
    if k >= 0 and not lines[k].lstrip().startswith("|"):
        # A heading can be the line directly above a table; do not count it twice, the
        # "heading" entry below covers it.
        if not lines[k].startswith("#"):
            out.append(("above", k + 1, lines[k].strip()))
    h = header_i - 1
    while h >= 0:
        if lines[h].startswith("#"):
            out.append(("heading", h + 1, lines[h].strip()))
            break
        h -= 1
    return out


def consistent(stated, rows):
    """Is a stated count reconcilable with this many table rows?

    Not every enumeration puts one item per row. `vtable-method-index.md` heads each section
    "N methods" and lays them out **two per row**: 47 -> 24 rows, 39 -> 20, 31 -> 16, 3067 -> 1534.
    That is `ceil(N/2)` in every case, and it is a formatting choice, not a miscount -- reporting it
    would be the tool telling the author their own layout is a defect.

    So a count is consistent when it equals the row count, or when the rows would hold it at 2, 3 or
    4 items each (exactly, or one short for a final half-full row).
    """
    if stated == rows:
        return True
    for k in (2, 3, 4):
        if stated == rows * k or stated == rows * k - (k - 1):
            return True
    return False


def scan(path, rel):
    text = io.open(path, encoding="utf-8", errors="replace").read()
    lines = text.split(chr(10))
    found = []
    for header_i, _sep, rows in tables(lines):
        if rows == 0:
            continue
        cands = []
        for kind, ln, txt in introducers(lines, header_i):
            for v in numbers_in(txt):
                cands.append((kind, ln, txt, v))
        if not cands:
            continue
        # A table matching ANY stated number is clean: "the fifteen groups, six UI-owned".
        if any(consistent(v, rows) for _k, _l, _t, v in cands):
            continue
        found.append((rel, header_i + 1, rows, cands))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--control", action="store_true",
                    help="positive control: a planted mismatch this sweep MUST flag")
    ap.add_argument("--limit", type=int, default=40)
    # A count in a HEADING is far more likely to be about the table under it than one in a
    # passing sentence: "Twelve float fields" heads an enumeration, while "all nine slices
    # included" merely mentions a number on the way to a different table. Splitting the two
    # is what turns 327 advisory lines into a list a person can actually work through.
    ap.add_argument("--source", choices=("heading", "above", "both"), default="both")
    a = ap.parse_args()

    paths = []
    for root, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if d not in ("_templates",)]
        for f in sorted(files):
            if f.endswith(".md"):
                paths.append(os.path.join(root, f))

    control_path = None
    if a.control:
        # The expected result is a short list, and a broken parser prints the same short list.
        control_path = os.path.join(a.db, "_EC5_POSITIVE_CONTROL.md")
        io.open(control_path, "w", encoding="utf-8", newline=chr(10)).write(
            "# control - delete me" + chr(10) * 2
            + "There are **seven** groups, enumerated here:" + chr(10) * 2
            + "| bit | call |" + chr(10) + "|---|---|" + chr(10)
            + chr(10).join("| `0x%04X` | `00000000` |" % (1 << i) for i in range(6)) + chr(10))
        paths.append(control_path)

    all_found = []
    for p in paths:
        rel = os.path.relpath(p, a.db).replace(os.sep, "/")
        try:
            all_found.extend(scan(p, rel))
        except OSError:
            continue
    if a.source != "both":
        keep = []
        for rel, ln, rows, cands in all_found:
            c = [x for x in cands if x[0] == a.source]
            if c and not any(consistent(v, rows) for _k, _l, _t, v in c):
                keep.append((rel, ln, rows, c))
        all_found = keep

    ctrl = [f for f in all_found if f[0].startswith("_EC5_POSITIVE_CONTROL")]
    all_found = [f for f in all_found if not f[0].startswith("_EC5_POSITIVE_CONTROL")]
    if control_path:
        os.remove(control_path)
        if ctrl:
            print("CONTROL: FOUND (said seven, tabulated six) -- the sweep can see a mismatch.")
        else:
            print("CONTROL: **NOT FOUND** -- the parser sees nothing; every result below is void.")
            return 2
        print()

    tot_tables = 0
    for p in paths:
        if control_path and p == control_path:
            continue
        try:
            tot_tables += len(tables(io.open(p, encoding="utf-8",
                                             errors="replace").read().split(chr(10))))
        except OSError:
            pass

    print("documents scanned : %d" % len([p for p in paths if p != control_path]))
    print("tables found      : %d" % tot_tables)
    print("count/table pairs that disagree : %d  (advisory -- a number near a table"
          " need not be its length)" % len(all_found))
    if a.source != "both":
        print("  restricted to counts stated in a %s" % a.source)
    print()
    for rel, ln, rows, cands in all_found[:a.limit]:
        stated = sorted({v for _k, _l, _t, v in cands})
        print("  %s  table at line %d has %d row(s); stated nearby: %s"
              % (rel, ln, rows, ", ".join(str(v) for v in stated)))
        for kind, cl, txt, v in cands[:2]:
            print("      %-7s line %d: %s" % (kind, cl, txt[:110]))
    if len(all_found) > a.limit:
        print()
        print("  ...%d more, pass --limit" % (len(all_found) - a.limit))
    print()
    print("A finding is a pair worth a human's eye, not a defect. The tool cannot tell whether the")
    print("number was ABOUT the table; it guarantees only that where a count introduces an")
    print("enumeration, the arithmetic on the page agrees with itself.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
