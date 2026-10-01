#!/usr/bin/env python3
"""check_route_counts.py - does a route's `count=` agree with its own document?

WHY THIS EXISTS. `count=` in the route grammar is doing two jobs, and nothing noticed until a
generator was finally written against the column. `AuthoredTableHeader` carried
`SLOTPTR 0x02EBEF70 stride=0x8 count=40`; the band is **146** qword slots and 40 is how many of them
are headers of that shape. A consumer reading the documented meaning - *N entries at stride S from
ADDR* - scans the wrong span and attributes other types' accesses to this one. That row cost 1,461
false accesses before it was corrected.

**Thirty-seven routes carry `count=` and exactly one has been checked.** This checks the rest the
only way they can be checked mechanically: by reading what the type's OWN document says about the
same address, and putting the two numbers side by side.

WHAT IT DOES NOT DO
-------------------
**It does not issue a verdict, and that is deliberate.** A document mentioning a different number
near the same address is not proof of a defect - counts legitimately differ between the table, the
populated subset and the slots one function walks. What the instrument produces is the EVIDENCE a
reader needs: the route, the document lines that name the address, and every count-shaped number in
them. Every automated verdict this kit has attempted on a shape rather than a reading has
over-reported, so this one reports and stops.

A row is worth reading when the document's number differs from the route's, and worth reading first
when the document says "of" - *"forty of them"*, *"N of the M slots"* - which is the exact phrasing
that made the `AuthoredTableHeader` route wrong.

    python check_route_counts.py
    python check_route_counts.py --type AuthoredTableHeader
"""
import argparse
import csv
import io
import os
import re
import sys

import kit_paths as KP

COUNT = re.compile(r"count=(\d+)")
ADDR = re.compile(r"(0x)?([0-9A-Fa-f]{6,8})")
STRIDE = re.compile(r"stride=(0x[0-9A-Fa-f]+|\d+)")
# a number that is being used as a quantity of things
QTY = re.compile(r"\b(\d{1,5})\s*(?:qword\s+)?(?:slots?|rows?|entries|entry|records?|elements?|"
                 r"headers?|of them|of the)\b", re.I)
OFPHRASE = re.compile(r"\b(\d{1,5})\s+of\s+(?:the\s+)?(\d{1,5})?\b", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--types", default=os.path.join(KP.DB, "_types", "types.tsv"))
    ap.add_argument("--type", default=None)
    a = ap.parse_args()

    rows = []
    with io.open(a.types, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 13 or not f[0]:
                continue
            route = f[12]
            m = COUNT.search(route)
            if not m:
                continue
            if a.type and f[0] != a.type:
                continue
            rows.append((f[0], route, f[11]))

    print("routes carrying `count=` : %d" % len(rows))
    print()
    flagged = 0
    for tname, route, docs in rows:
        m = COUNT.search(route)
        cnt = m.group(1)
        am = re.search(r"0x([0-9A-Fa-f]{6,8})", route)
        addr = am.group(1).upper() if am else None
        st = STRIDE.search(route)
        stride = st.group(1) if st else "-"

        lines = []
        for d in [x.strip() for x in (docs or "").split(";") if x.strip()]:
            p = os.path.join(KP.DB, d)
            if not os.path.exists(p):
                continue
            try:
                txt = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
            except OSError:
                continue
            for i, ln in enumerate(txt):
                if addr and addr in ln.upper():
                    lines.append((os.path.basename(d), i + 1, ln.strip()))

        nums, ofs = set(), []
        for _f, _i, ln in lines:
            for q in QTY.finditer(ln):
                nums.add(q.group(1))
            for o in OFPHRASE.finditer(ln):
                ofs.append(o.group(0))
        disagree = nums and cnt not in nums
        mark = ""
        if ofs:
            mark = "  <-- document says \"%s\"" % ofs[0][:28]
        elif disagree:
            mark = "  <-- document quantities: %s" % ",".join(sorted(nums)[:6])
        if mark:
            flagged += 1
        print("  %-30s count=%-6s stride=%-7s doc lines naming the addr: %-3d%s"
              % (tname[:30], cnt, stride, len(lines), mark))
        if mark and lines:
            for f2, i2, ln in lines[:2]:
                print("        %s:%d  %s" % (f2, i2, ln[:120]))
    print()
    print("%d row(s) where the document's own quantities differ from the route's count." % flagged)
    print("That is a READING LIST, not a defect list - counts legitimately differ between a table,")
    print("its populated subset, and the slots one function walks. The `N of M` phrasing is the one")
    print("that made AuthoredTableHeader's route wrong, so those come first.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
