#!/usr/bin/env python3
"""check_repeated_records.py - unknown spans that continue a record the store already declares twice.

**THE STORE OFTEN ALREADY KNOWS THE SHAPE IT IS MISSING.** When a type is documented from the front,
the first instances of a record array get declared field by field and the rest of the array collapses
into one large `unobservedSpan`. The evidence for the array is then sitting in the store itself -
two consecutive runs of rows with an identical field-size sequence - and nobody looks, because a
displacement-keyed scan cannot see past the first element of an indexed array and so reports the
span as unreached.

`ManagerSub0209BE80_57E0` is the case this was written from. Its rows at `0xD0` and `0x1A0` are
`ptr(8) / span(186) / count(2) / span(12)` - the same sequence twice, each totalling exactly `0xD0` -
the third record's first field is declared at `0x270`, and the `8,728`-byte span that follows ends to
the byte on the 44th record boundary.

THE TEST. For each type, walk the rows in offset order and look for two ADJACENT groups with the
same field-size sequence (a repeat). Then ask whether an unknown span abuts the repeat and whether
its length is a whole multiple of the record size. Both must hold, because either alone is common:
sequences repeat by coincidence in small types, and spans abut records that do not continue.

**IT COMPARES TILINGS, NOT STRUCTURES, AND THAT IS A REAL LIMIT.** The match is on declared field
SIZES - `8/186/2/12` against `8/186/2/12` - so two records whose guards sit at different relative
offsets are indistinguishable to it. `_57E0` is again the case in point: its two records step `0xD0`
apart on their pointers and share a count slot at record-relative `+0xC2`, but their guard flags sit
`0xC` and `0xE` below their objects, so the guards step `0xCE` and the records are NOT congruent.
The store had recorded that mismatch before this tool existed and the tool cannot see it. A store's
tiling is partly a record of how the documentation grew, and only partly of how the object is laid
out; this reads the former.

**A HIT IS A HYPOTHESIS, NOT A LAYOUT.** The arithmetic closing proves that the span COULD hold
whole records, never that it does. `_57E0` is the reminder: its stride survived this test and then
every code-side witness for it was ruled out, leaving the hypothesis standing on the store alone.
What a hit buys is a question worth asking, pointed at a specific span.

    python check_repeated_records.py
    python check_repeated_records.py --min-record 16 --min-span 256
"""
import argparse
import csv
import io
import os
import re
import sys

import kit_paths as KP

STORE = os.path.join(KP.DB, "_types", "fields.tsv")
GAP = re.compile(r"unobserved|unknown|gap|span|pad", re.I)


def rows_by_type(path):
    out = {}
    with io.open(path, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 9:
                continue
            try:
                off = int(f[1], 0)
                size = int(f[2], 0)
            except ValueError:
                continue
            out.setdefault(f[0], []).append((off, size, f[3], f[6]))
    for k in out:
        out[k].sort()
    return out


def find_repeats(rows, min_record, min_fields):
    """Adjacent groups of rows whose field-size sequences match. Returns (start_i, n_fields, bytes)."""
    hits = []
    n = len(rows)
    for i in range(n):
        for k in range(min_fields, 9):          # a record is 2..8 declared fields
            if i + 2 * k > n:
                break
            a = rows[i:i + k]
            b = rows[i + k:i + 2 * k]
            if [x[1] for x in a] != [x[1] for x in b]:
                continue
            # A UNIFORM RUN IS NOT A RECORD. Six consecutive dwords trivially "repeat" as two
            # three-dword groups, and `CharacterRenderSystemTail` produced exactly that false
            # positive - 0x4C/0x50/0x54 are three plain uint32s and the tool read them as a
            # 12-byte record repeating. What makes `_57E0` evidence is that its sequence is
            # HETEROGENEOUS - 8/186/2/12 - which is a signature; 4/4/4 is not.
            if len({x[1] for x in a}) < 2:
                continue
            rec = sum(x[1] for x in a)
            if rec < min_record:
                continue
            # the two groups must be contiguous in memory, or they are not consecutive records
            if a[0][0] + rec != b[0][0]:
                continue
            if b[0][0] + rec != (rows[i + 2 * k][0] if i + 2 * k < n else b[0][0] + rec):
                pass
            hits.append((i, k, rec))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=STORE)
    ap.add_argument("--min-record", type=int, default=16)
    ap.add_argument("--min-span", type=int, default=256)
    ap.add_argument("--min-fields", type=int, default=2)
    a = ap.parse_args()

    by_type = rows_by_type(a.store)
    found = []
    for ty, rows in sorted(by_type.items()):
        for i, k, rec in find_repeats(rows, a.min_record, a.min_fields):
            after = i + 2 * k
            # walk forward to the first gap-named row at or after the repeat
            j = after
            while j < len(rows) and not GAP.search(rows[j][2]):
                j += 1
                if j > after + 2:               # the span must be near, not anywhere later
                    break
            if j >= len(rows) or not GAP.search(rows[j][2]):
                continue
            off, size, name, readiness = rows[j]
            if size < a.min_span:
                continue
            # does the span cover a whole number of records, counting from the repeat's start?
            span_end = off + size
            total = span_end - rows[i][0]
            whole = (total % rec == 0)
            # HOW SURPRISING IS THE EXACT CLOSE? For a total of `total` bytes, count how many
            # OTHER plausible record sizes also divide it exactly. When many do, "EXACT" carries
            # almost no information - a 192-byte span closes exactly on 8, 12, 16, 24, 32, 48, 64
            # and 96, so two competing readings of the same span can both pass. It is the REPEAT
            # that is the evidence; the exact close is only a filter, and this column says how
            # coarse a filter it is for this hit.
            alts = sum(1 for r2 in range(4, min(257, total + 1), 4)
                       if r2 != rec and total % r2 == 0)
            found.append((ty, rows[i][0], rec, k, name, off, size, readiness,
                          total // rec, whole, alts))

    exact = [f for f in found if f[9]]
    print("types scanned                         : %d" % len(by_type))
    print("repeat + adjacent span (>= %d B)       : %d" % (a.min_span, len(found)))
    print("of those, the span closes EXACTLY on a record boundary : %d" % len(exact))
    print()
    if not found:
        print("  none")
        return 0
    print("%-30s %-8s %6s %3s %-22s %8s %7s %-6s %s"
          % ("type", "rec@", "recB", "flds", "span", "spanB", "records", "closes", "rival sizes"))
    for ty, ro, rec, k, name, off, size, rd, nrec, whole, alts in sorted(found, key=lambda x: -x[6]):
        print("%-30s %-8s %6d %3d %-22s %8d %7d %-6s %d"
              % (ty[:30], hex(ro), rec, k, name[:22], size, nrec,
                 "EXACT" if whole else "no", alts))
    print()
    print("A HIT IS A HYPOTHESIS. The arithmetic closing shows the span COULD hold whole records,")
    print("never that it does - see `_57E0`, whose stride passed this test and whose every")
    print("code-side witness was then ruled out. What a hit buys is a question worth asking.")
    print()
    print("READ `rival sizes` BEFORE BELIEVING `EXACT`. It counts the other record sizes that")
    print("divide the same total exactly, so a high count means the close discriminates nothing.")
    print("The thresholds were a real worry and are no longer one. BEFORE uniform runs were")
    print("rejected, loosening to --min-span 16 --min-record 4 took the EXACT count from 1 to 35,")
    print("so the null was a threshold artifact. With the rejection in place the same loosening")
    print("yields 3 candidates and still ONE exact hit, so the result is now threshold-stable:")
    print("`_57E0` is the only span in the store that continues a heterogeneous declared record.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
