#!/usr/bin/env python3
"""check_static_spans.py - two types claiming the same static bytes.

WHY THIS EXISTS. `check_storage_class.py` checks that an `EMBED` fits its parent and that two
`EMBED`s into the same parent do not overlap. **Nothing checks the same thing for static anchors.**
An `ARRAY 0xADDR stride=0xS count=N` claims `N*S` bytes at a fixed address, a `SLOTPTR` claims a
pointer table of the same shape, and a `STATIC` claims its declared size - and until now no
instrument asked whether two of those claims land on the same bytes.

That is not hypothetical. `AuthoredTableHeader` carried
`SLOTPTR 0x02EBEF70 stride=0x8 count=40`, whose span `02EBEF70..02EBF0B0` sits inside the 146-slot
registry band that also holds `02EBF190`, the `BattleSystemState` pointer. The route read as forty
consecutive same-typed slots; the owning contract says membership is by idiom and *"never by its
address falling in the band"*. A census generator built against the column produced 1,461 accesses
of one type attributed to another before the row was corrected to `DYNAMIC`.

WHAT COUNTS AS A SPAN, and the distinction matters
--------------------------------------------------
    STATIC  0xADDR                     the OBJECT: [ADDR, ADDR + declared size)
    ARRAY   0xADDR stride=S count=N    the ELEMENTS: [ADDR, ADDR + N*S)
    SLOTPTR 0xADDR stride=S count=N    the POINTER TABLE: [ADDR, ADDR + N*S)
    PTR / PARRAY 0xADDR                only the POINTER CELL: [ADDR, ADDR + 8)

**A `PTR` collision is usually correct and is reported separately, never failed.** `AchievementState`
is `PTR 0x020927C0+0x3844` and `ImageBackedStateBlock` is `PTR 0x020927C0`: the same cell, read at
two depths, because one is interior to the other. That is the routes agreeing, not disagreeing. A
collision between two *data* spans is the one that cannot be right.

    python check_static_spans.py --self-test
    python check_static_spans.py
"""
import argparse
import csv
import io
import os
import re
import sys

import kit_paths as KP

R_STATIC = re.compile(r"^STATIC\s+(0x[0-9A-Fa-f]+)")
R_ARRAY = re.compile(r"^ARRAY\s+(0x[0-9A-Fa-f]+)(?:\s*\+\s*(0x[0-9A-Fa-f]+))?\s+stride=(0x[0-9A-Fa-f]+|\d+)\s+count=(\d+)")
R_SLOT = re.compile(r"^SLOTPTR\s+(0x[0-9A-Fa-f]+)\s+stride=(0x[0-9A-Fa-f]+|\d+)(?:\s+count=(\d+))?")
R_CELL = re.compile(r"^(PTR|PARRAY)\s+(0x[0-9A-Fa-f]+)")


def spans_from(tname, route, size):
    """[(kind, lo, hi, text)] for one route alternative."""
    out = []
    for a in route.split("|"):
        a = a.strip()
        m = R_STATIC.match(a)
        if m and size:
            lo = int(m.group(1), 0)
            out.append(("object", lo, lo + size, a))
            continue
        m = R_ARRAY.match(a)
        if m:
            lo = int(m.group(1), 0) + (int(m.group(2), 0) if m.group(2) else 0)
            out.append(("elements", lo, lo + int(m.group(3), 0) * int(m.group(4)), a))
            continue
        m = R_SLOT.match(a)
        if m and m.group(3):
            lo = int(m.group(1), 0)
            out.append(("pointer table", lo, lo + int(m.group(2), 0) * int(m.group(3)), a))
            continue
        m = R_CELL.match(a)
        if m:
            lo = int(m.group(2), 0)
            out.append(("pointer cell", lo, lo + 8, a))
            continue
    return out


def collisions(rows):
    """rows: (type, kind, lo, hi, text). Returns (data_hits, cell_hits)."""
    data = sorted([r for r in rows if r[1] != "pointer cell"], key=lambda r: r[2])
    cells = sorted([r for r in rows if r[1] == "pointer cell"], key=lambda r: r[2])
    dh, ch = [], []
    for seq, out in ((data, dh), (cells, ch)):
        for i in range(len(seq)):
            for j in range(i + 1, len(seq)):
                if seq[j][2] >= seq[i][3]:
                    break
                if seq[i][0] == seq[j][0]:
                    continue          # two alternatives of ONE type are not a collision
                out.append((seq[i], seq[j]))
    return dh, ch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--types", default=os.path.join(KP.DB, "_types", "types.tsv"))
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        ok = True
        cases = [
            ("two ARRAYs on disjoint bands",
             [("A", "elements", 0x1000, 0x1100, ""), ("B", "elements", 0x1100, 0x1200, "")], 0, 0),
            ("an ARRAY inside another ARRAY's span",
             [("A", "elements", 0x1000, 0x1200, ""), ("B", "elements", 0x1080, 0x1090, "")], 1, 0),
            ("a SLOTPTR table over a STATIC object",
             [("A", "object", 0x2000, 0x2400, ""), ("B", "pointer table", 0x2100, 0x2140, "")], 1, 0),
            ("two alternatives of ONE type are not a collision",
             [("A", "elements", 0x3000, 0x3100, ""), ("A", "elements", 0x3050, 0x3060, "")], 0, 0),
            ("two pointer CELLS at one address are reported, not failed",
             [("A", "pointer cell", 0x4000, 0x4008, ""), ("B", "pointer cell", 0x4000, 0x4008, "")],
             0, 1),
        ]
        for label, rows, nd, nc in cases:
            dh, ch = collisions(rows)
            good = (len(dh), len(ch)) == (nd, nc)
            ok = ok and good
            print("  %-52s data=%d cell=%d  %s" % (label, len(dh), len(ch), "ok" if good else "BROKEN"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    rows = []
    with io.open(a.types, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 13 or not f[0]:
                continue
            try:
                size = int(f[1], 0)
            except ValueError:
                size = None
            for kind, lo, hi, txt in spans_from(f[0], f[12], size):
                rows.append((f[0], kind, lo, hi, txt))

    dh, ch = collisions(rows)
    print("static-anchored route spans: %d" % len(rows))
    print("  data spans (object/elements/pointer table) : %d"
          % len([r for r in rows if r[1] != "pointer cell"]))
    print("  pointer cells                              : %d"
          % len([r for r in rows if r[1] == "pointer cell"]))
    print()
    print("DATA-SPAN COLLISIONS (two types claiming the same bytes): %d" % len(dh))
    for x, y in dh:
        print("  %s %s [%08X,%08X)" % (x[0], x[1], x[2], x[3]))
        print("    overlaps %s %s [%08X,%08X)" % (y[0], y[1], y[2], y[3]))
        print("      %s" % x[4])
        print("      %s" % y[4])
    print()
    print("pointer cells shared by more than one type: %d  (reported, not failed -"
          " one type interior to another reads the same cell at two depths)" % len(ch))
    for x, y in ch:
        print("  %08X  %s  and  %s" % (x[2], x[0], y[0]))
    return 1 if dh else 0


if __name__ == "__main__":
    sys.exit(main())
