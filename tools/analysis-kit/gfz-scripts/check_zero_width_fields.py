#!/usr/bin/env python3
"""check_zero_width_fields.py - a field that declares zero bytes is invisible to every other check.

THE HOLE THIS FILLS IS IN THE STORE'S OWN VALIDATION. The sum invariant - a type's field rows must
total its declared size - is the check that keeps layouts honest, and **a row of size 0 contributes
nothing to it**. So a field can sit in `fields.tsv` with a real name, a real ctype and a real
offset, declare zero bytes, and every validator will report the store clean.

It is not a hypothetical. **269 rows across 117 types declare size 0**, and they were found by
accident, while reading a census for something else. `PPhysicsRigidBodyBase` has 14 of them,
`PPhysicsCharacterControllerBase` 10, `PShaderPassD3D11` 9. Their ctypes are real - `VPString`,
`sce::Vectormath::Scalar::Aos::VVector3`, `PWorldMatrix` - so these are not placeholders; they are
reflection-derived rows whose importer had no width for the type and wrote zero.

WHY THAT MATTERS BEYOND TIDINESS. A reconstruction reading this store lays out a type from its
field rows. A zero-width field occupies nothing, so every field after it lands at the wrong place
unless the offsets are taken as authoritative - and if the offsets are authoritative, the widths
are decoration and the sum invariant proves nothing. Either way the store is asserting a layout it
has not checked.

WHAT THIS REPORTS, in three buckets, because they need different work:

  RESOLVABLE   the ctype names a type this store declares with a size, so the width is already
               known and the row can simply be filled. This is the store's own PASS 2 rule from
               check_embed_parent_fields.py, applied to the rows that rule skips because a zero
               size trivially "matches" nothing.
  PHYRE        the ctype names a class in the recovered Phyre size table but not in the store.
  UNRESOLVED   everything else - mostly `VPString`, the vector types and `VP<X>` pointer spellings
               whose widths this store has never established.

It writes nothing. A width is a measurement, and the RESOLVABLE bucket is the only one where the
measurement already exists.

    python check_zero_width_fields.py
"""
import argparse
import collections
import csv
import io
import os
import sys

import kit_paths as KP

PHYRE = os.path.join("22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                     "members", "phyre-class-instance-sizes.tsv")


def leaf(c):
    return c.strip().rstrip("*& ").split("::")[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    a = ap.parse_args()

    declared = {}
    with io.open(os.path.join(a.db, "_types", "types.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if f and f[0]:
                try:
                    declared[f[0]] = int(f[1], 0)
                except (ValueError, IndexError):
                    pass
    phyre = {}
    p = os.path.join(a.db, PHYRE)
    if os.path.exists(p):
        for f in csv.reader(io.open(p, encoding="utf-8", newline=""), delimiter="\t"):
            if f and not f[0].startswith("#") and f[0] != "class_leaf":
                phyre[f[0]] = int(f[2], 16)

    rows = []
    with io.open(os.path.join(a.db, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) >= 9 and f[2].strip() == "0":
                rows.append(f)

    res, ph, un = [], [], []
    for f in rows:
        l = leaf(f[4])
        if l in declared and declared[l]:
            res.append((f, l, declared[l]))
        elif l in phyre:
            ph.append((f, l, phyre[l]))
        else:
            un.append(f)

    print("field rows declaring size 0: %d, across %d type(s)"
          % (len(rows), len({f[0] for f in rows})))
    print()
    print("RESOLVABLE - the ctype names a declared type with a size: %d" % len(res))
    for f, l, s in res[:12]:
        print("   %-34s %-8s %-22s %s -> 0x%X" % (f[0][:34], f[1], f[3][:22], l, s))
    if len(res) > 12:
        print("   ... %d more" % (len(res) - 12))
    print()
    print("PHYRE - the ctype is in the recovered size table but not declared here: %d" % len(ph))
    for f, l, s in ph[:6]:
        print("   %-34s %-8s %s -> 0x%X" % (f[0][:34], f[1], l, s))
    print()
    print("UNRESOLVED: %d" % len(un))
    for c, n in collections.Counter(leaf(f[4]) for f in un).most_common(8):
        print("   %-46s %d" % (c[:46], n))
    print()
    print("A zero-width row contributes 0 to the sum invariant, so no other checker here can see")
    print("it. That is why these went unnoticed while the store reported 0 sum mismatches.")
    return 1 if rows else 0


if __name__ == "__main__":
    sys.exit(main())
