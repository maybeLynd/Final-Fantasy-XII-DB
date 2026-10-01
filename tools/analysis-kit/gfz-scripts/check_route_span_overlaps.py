#!/usr/bin/env python3
"""check_route_span_overlaps.py - do two declared routes claim the same bytes?

RESTORED 2026-09-27 (OPUS) under its own name. Until ffe018a49 this was check_route_collisions.py; that
commit gave the file name to a different check (undiscriminated FN routes) and this one - the ARRAY /
SLOTPTR span-overlap check with the sparse-SLOTPTR containment rule - stopped existing, which left
check_route_collisions_control.py crashing on `contained`. Its body is byte-identical to ffe018a49^.

`check_route_counts.py` asks whether a count agrees with its own document. `check_route_extents.py`
asks whether the data stops where the count says. Neither asks the question that needs no external
evidence at all: **the type store declares a base, a stride and a count for many types, and those
spans must not overlap each other.** If type A's span covers type B's base, at least one of the two
is wrong, and the store contradicts itself.

This is a pure internal-consistency check. It cannot be satisfied by a mistaken reading of the
image, because it never reads the image - it reads only what the store already asserts. That makes
it weaker in scope and stronger in kind: a finding here is a defect by construction.

KNOWN AND EXPECTED: ItemClassDescriptor and InventoryClassDescriptor both declare
`ARRAY 0x01EEBCC0 stride=0x58 count=15`. That is the already-queued contradiction
OPUS-CON-ITEMCLASS-INVENTORYCLASS-SAME-TABLE, not a new one, and it is reported separately so it
does not mask anything.
"""
import csv
import io
import os
import re
import sys
import argparse

import kit_paths as KP

ap = argparse.ArgumentParser()
ap.add_argument("--db", default=KP.DB)
ARGS = ap.parse_args()

# PARRAY IS EXCLUDED AND THE EXCLUSION IS THE POINT. The grammar in _types/README.md line 25 reads
#     PARRAY  0xADDR [+0xOFF] stride=0xS [count]   element i at *(ADDR) + OFF + i*S
# so a PARRAY names a POINTER at ADDR; the elements live wherever that pointer leads and the route
# claims no fixed span at all. Treating it as direct made CharacterRenderRecord appear to swallow
# 0x48800 bytes of .data and collide with two neighbours - two defects that do not exist.
# ARRAY claims N*S bytes at ADDR. SLOTPTR CLAIMS ITS CELLS, NOT ITS STRIDE - corrected 2026-09-21
# (OPUS) on SWE2-STRUCT-REQ-OPUS-SPARSE-SLOTPTR-SPAN-MODEL. The old model said SLOTPTR claims N*S
# bytes of pointer table, which is right only when the cell IS the stride: both dense SLOTPTRs
# here have stride 8 and 8-byte cells, so the two coincided and the model looked general. It is
# not. A SPARSE SLOTPTR - a per-element pointer living inside a record, stride 0x288 and cell 8 -
# claims 8 bytes every 0x288, and the old model claimed the 0x280 of record between them as well.
# Those bytes belong to the record, so a correct route was reported as overrunning by 3,232 bytes.
# A stride is a STEP, not an extent.
#
# AND A SPARSE SLOTPTR INSIDE AN ARRAY IS CONTAINMENT, NOT COLLISION - but only when it is
# verified, which is the useful part. Every cell must land on a DECLARED POINTER FIELD of the
# ARRAY's element type. ActorRecordPool's cells land on ActorManagerSlot +0x08 `recordPool`, which
# is declared void* and 8 bytes, so the route is confirmed by the very check that used to fail it.
# A sparse SLOTPTR whose cells land in a gap, on a non-pointer field, or straddle a field boundary
# is still a defect and is still reported.
R = re.compile(r"\b(ARRAY|SLOTPTR)\s+(0x[0-9A-Fa-f]+)\s+stride=(0x[0-9A-Fa-f]+|\d+)"
               r"\s+count=(\d+)")

CELL = 8          # a SLOTPTR cell is one pointer

def _fields(db):
    """type -> {offset: (size, ctype)} from fields.tsv."""
    out = {}
    with io.open(os.path.join(db, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh, delimiter="	")
        for f in rd:
            try:
                out.setdefault(f["type"], {})[int(f["offset"], 16)] = (int(f["size"]), f["ctype"])
            except (ValueError, KeyError, TypeError):
                continue
    return out


FIELDS = None


def contained(a, b):
    """Is one of these a SPARSE SLOTPTR living inside the other ARRAY, verifiably?

    Legal only when every cell lands on a DECLARED POINTER FIELD of the ARRAY's element type.
    Returns (True, why) for verified containment, (False, why) otherwise - `why` is printed either
    way, so a refusal says which cell failed and on what grounds.
    """
    for sp, ar in ((a, b), (b, a)):
        (sb, se, sn, sk, ss, sc) = sp
        (ab, ae, an, ak, as_, ac) = ar
        if sk != "SLOTPTR" or ak != "ARRAY":
            continue
        if ss == CELL:
            continue                     # dense: cells tile, nothing to contain
        cells = [sb + i * ss for i in range(sc)]
        if not all(ab <= c and c + CELL <= ae for c in cells):
            return False, "%s cells are not all inside %s" % (sn, an)
        offs = {(c - ab) % as_ for c in cells}
        if len(offs) != 1:
            return False, ("%s cells land at %d different offsets inside %s's element"
                           % (sn, len(offs), an))
        off = offs.pop()
        decl = (FIELDS or {}).get(an, {}).get(off)
        if decl is None:
            return False, ("%s cells land at %s +0x%03X, which %s does not declare"
                           % (sn, an, off, an))
        size, ctype = decl
        if size != CELL or "*" not in ctype:
            return False, ("%s cells land on %s +0x%03X, declared %d bytes as %s - not a pointer"
                           % (sn, an, off, size, ctype))
        return True, ("every %s cell lands on %s +0x%03X, declared %s - verified containment"
                      % (sn, an, off, ctype))
    return False, ""


rows = list(csv.reader(io.open(os.path.join(ARGS.db, "_types", "types.tsv"),
                               encoding="utf-8", newline=""), delimiter="\t"))
FIELDS = _fields(ARGS.db)
spans = []
for r in rows[1:]:
    if len(r) < 13 or not r[12]:
        continue
    for alt in r[12].split("|"):
        m = R.search(alt)
        if not m:
            continue
        kind, base, stride, count = m.group(1), int(m.group(2), 16), \
            int(m.group(3), 0), int(m.group(4))
        spans.append((base, base + (stride * count if kind == "ARRAY"
                                    else stride * (count - 1) + CELL),
                      r[0], kind, stride, count))
spans.sort()
print("routes with a literal base/stride/count: %d" % len(spans))

dup, overlap, contained_ok = [], [], []
for i in range(len(spans)):
    b1, e1, n1, k1, s1, c1 = spans[i]
    for j in range(i + 1, len(spans)):
        b2, e2, n2, k2, s2, c2 = spans[j]
        if b2 >= e1:
            break
        if b1 == b2 and e1 == e2:
            dup.append((n1, n2, b1, e1))
            continue
        ok, why = contained(spans[i], spans[j])
        if ok:
            contained_ok.append((n2, n1, why))
        else:
            overlap.append((n1, b1, e1, n2, b2, e2, why))

print()
print("IDENTICAL spans (two types claiming exactly the same table): %d" % len(dup))
for n1, n2, b, e in dup:
    print("   %-34s == %-34s  %08X..%08X" % (n1, n2, b, e))
print()
print("VERIFIED CONTAINMENT (a sparse SLOTPTR inside an ARRAY, cells on a declared pointer): %d"
      % len(contained_ok))
for inner, outer, why in contained_ok:
    print("   %s" % why)
print()
print("PARTIAL overlaps (one span running into another): %d" % len(overlap))
for n1, b1, e1, n2, b2, e2, why in overlap:
    print("   %-30s %08X..%08X  overruns into" % (n1, b1, e1))
    print("   %-30s %08X..%08X  by %d byte(s)" % (n2, b2, e2, min(e1, e2) - b2))
    if why:
        print("      containment refused: %s" % why)

print()
print("verdict: %s" % ("clean apart from the known duplicate" if not overlap
                       else "%d PARTIAL OVERLAP(S) - each is a defect by construction" % len(overlap)))

sys.exit(1 if overlap else 0)
