#!/usr/bin/env python3
"""check_admitted_bodies_are_switch_tables.py - are admitted unlisted "bodies" really inline switch tables?

OPUS, 2026-09-25, from UC-1 pass 2. unlisted-body-admissions.tsv admits blocks that follow a listed
function's `ret` as unlisted code bodies. Two it admits - 00277851+100 and 002FE7D0+106 - are not
code: their dwords are IMAGE-BASE-RELATIVE RVAs (value + 0x00120000) landing inside the preceding
function, i.e. that function's inline jump table, and the pages citing them call them tables.

For every admitted row, this reads the block as aligned dwords (from the first 4-aligned offset) and
counts how many, plus the image base, land inside the PRECEDING listed function's code (its listed
extent or the gap up to the block). A block whose first run of >= 3 consecutive dwords all do is
reported as a table candidate; the rest of the block after that run may be a byte index table or
code. CODE-ONLY evidence (image bytes and the listed extents); no unwind data. Read-only.

    check_admitted_bodies_are_switch_tables.py
"""
import io
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402
import check_default_instance_writers as W  # noqa: E402

ADM = "99-Unresolved-Residual/Unlisted-Code/unlisted-body-admissions.tsv"


def main():
    img = W.Image()
    rows = []
    for line in io.open(os.path.join(G.DB, ADM), encoding="utf-8"):
        c = line.rstrip("\r\n").split("\t")
        if line.startswith("#") or len(c) < 10 or not c[1].isdigit():
            continue
        rows.append((int(c[0], 16), int(c[1]), int(c[2], 16) if c[2] not in ("", "-") else None, c[8]))
    hits = []
    for s, n, prev, kind in rows:
        if prev is None or prev not in img.sizes:
            continue
        lo, hi = prev, s
        a = (s + 3) & ~3
        run = 0
        while a + 4 <= s + n:
            v = struct.unpack("<I", img.read(a, 4))[0] + img.base
            if lo <= v < hi:
                run += 1
                a += 4
                continue
            break
        if run >= 3:
            hits.append((s, n, prev, kind, run))
    print("admitted rows read: %d; table candidates (>= 3 leading RVAs into the preceding function): %d"
          % (len(rows), len(hits)))
    for s, n, prev, kind, run in hits:
        print("  %08X+%-4d %-12s prev %08X  %d leading RVAs into it" % (s, n, kind, prev, run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
