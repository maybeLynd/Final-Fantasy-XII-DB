#!/usr/bin/env python3
"""next_question_id.py - report which OPEN-QUESTIONS id prefixes are free.

Why this exists
---------------
On 2026-09-02 the coordinator opened six new question sections (BC, BD, BE, BG, BH, BI) after
checking that those prefixes were free AS SECTION HEADERS (`## XX.`).  They were.  But every one
of them was already in use AS A ROW ID inside a *different* section -- BC-1 belonged to DynGeo,
BD-3 to the audio bank family, BE-1/BE-2 to GameApplication, BG-1 to the Gi render commands,
BH-3 to the float-table builders, BI-1..BI-16 to a dispatcher analysis cited ~25 times in
AUDIT-LOG.  The result was 23 duplicate ids across the ledger.

The mistake was not carelessness: it was VERIFYING THE WRONG PROPERTY and getting a clean answer
to a question nobody had asked.  A second collision (BL) happened the next tick between two
parallel sessions filing at the same time.

So: check the thing that actually matters -- row ids -- and check it mechanically.

Usage
-----
    python next_question_id.py --db "Database/FFXII TZA"          # next free prefix
    python next_question_id.py --db "Database/FFXII TZA" --list   # full used/free listing
    python next_question_id.py --db "Database/FFXII TZA" --check BC BD   # are these free?

Exit code is 1 if --check names a prefix that is already taken, so it can gate a merge.
"""
import argparse
import io
import os
import re
import string
import sys

# A row id is what a document cites.  Match it wherever it appears as a table row id, with or
# without strikethrough, which is how superseded rows are written.
ROW_ID = re.compile(r"^\|\s*~{0,2}\s*([A-Z]{1,2})-(\d+)\s*~{0,2}\s*\|")
SECTION = re.compile(r"^##\s+([A-Z]{1,2})\.\s")


def prefixes_in_use(path):
    """Every prefix used as a ROW ID, and separately every one used as a section header."""
    rows, sections = {}, {}
    with io.open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            m = ROW_ID.match(line)
            if m:
                rows.setdefault(m.group(1), []).append(n)
            m = SECTION.match(line)
            if m:
                sections.setdefault(m.group(1), []).append(n)
    return rows, sections


def all_prefixes():
    """A, B, ... Z, AA, AB, ... ZZ -- the order the ledger has grown in."""
    for c in string.ascii_uppercase:
        yield c
    for a in string.ascii_uppercase:
        for b in string.ascii_uppercase:
            yield a + b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--check", nargs="*", default=None)
    a = ap.parse_args()

    path = os.path.join(a.db, "_index", "OPEN-QUESTIONS.md")
    if not os.path.exists(path):
        sys.exit("not found: %s" % path)

    rows, sections = prefixes_in_use(path)
    used = set(rows) | set(sections)

    # Positive control: this file has grown past 'Z', so a run that finds only single letters
    # has failed to parse the table rows and must not be trusted.
    if not any(len(p) == 2 for p in rows):
        sys.exit("REFUSING TO ANSWER: no two-letter row ids found, so the row parse failed. "
                 "A 'free' answer from a parser that saw nothing is worthless.")

    if a.check is not None:
        bad = False
        for p in [x.upper() for x in a.check]:
            where = []
            if p in rows:
                where.append("%d row(s), first at line %d" % (len(rows[p]), rows[p][0]))
            if p in sections:
                where.append("section header at line %d" % sections[p][0])
            if where:
                print("%-3s TAKEN  - %s" % (p, "; ".join(where)))
                bad = True
            else:
                print("%-3s free" % p)
        return 1 if bad else 0

    free = [p for p in all_prefixes() if p not in used]
    if a.list:
        print("row-id prefixes in use (%d): %s" % (len(rows), " ".join(sorted(rows))))
        hdr_only = sorted(set(sections) - set(rows))
        if hdr_only:
            print("section header but no rows yet: %s" % " ".join(hdr_only))
        print()
        print("next 12 free: %s" % " ".join(free[:12]))
    else:
        print(free[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
