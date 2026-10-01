#!/usr/bin/env python3
"""check_prose_only_edges.py - pointer fields whose target is named in PROSE but not in the ctype.

WHY THIS EXISTS, and it comes from a near-miss rather than a theory. AL-8 asked for a writer of
`SpawnRecord +0x19`. Four sweeps had found none, and a fifth - seeded from the type's declared
route `PARRAY 0x0208E690 stride=0x250`, over all 20 bodies that reference the pool and their
one-hop callees, across five instruction forms - also found none. It was one step from being
recorded as an established absence.

The writer exists. `BattleEnmity_UpdatePeriodicDecay` reaches the record through
`BattleUnit + 0x6A0`, not through the pool. **A ROUTE IS A WAY IN, NOT THE ONLY WAY IN**, and a
census seeded from one bounds what it can ever say.

The alternate path was already in the store - `BattleUnit +0x6A0` is named `spawnRecord` and its
meaning reads "the owning SpawnRecord (0x250)". But its **ctype is `void*`**, so the pointer
graph does not contain the edge, and nothing that walks ctypes - a census generator, a gate, a
reconstruction - can follow it. The knowledge was present and unusable.

WHAT THIS REPORTS. Every field row whose ctype is anonymous (`void*`, `uint64`, `u8[8]`, blank)
while its NAME or MEANING names a type this store declares. Each is a candidate inbound edge
that exists in prose only.

WHAT IT DOES NOT DO. It does not rewrite ctypes. "The meaning mentions a type" is weaker than
"the field points at one" - a meaning may name a type to say the field is an INDEX into it, or
that it is one dereference away, which is exactly the LegacyPs2Gs `+0x150` case where writing
the child type would have been wrong by one indirection. Each candidate needs a person.

    python check_prose_only_edges.py --db "<db>"
"""
import argparse
import collections
import csv
import io
import os
import re
import sys

import kit_paths as KP

ANON = {"void*", "uint64", "u8[8]", "qword", "", "UNKNOWN", "void *", "uintptr"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    a = ap.parse_args()

    declared = []
    with io.open(os.path.join(a.db, "_types", "types.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if f and f[0]:
                declared.append(f[0])
    dset = set(declared)
    # longest first so `BattleStatsRecord` wins over `BattleStats` if both existed
    order = sorted(declared, key=len, reverse=True)

    rows = []
    with io.open(os.path.join(a.db, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) >= 9 and f[0]:
                rows.append(f)

    # the edges the ctype column already carries
    have = collections.defaultdict(set)
    for f in rows:
        c = re.sub(r"\[\d+\]$", "", f[4].strip().rstrip("*").strip())
        if c in dset and c != f[0]:
            have[f[0]].add(c)

    cands = []
    for f in rows:
        if f[4].strip() not in ANON:
            continue
        if int(f[2] or 0) != 8:
            continue                       # an inbound pointer is pointer-sized
        text = (f[3] or "") + "  " + (f[5] or "")
        for t in order:
            if t == f[0] or len(t) < 6:
                continue
            if re.search(r"\b%s\b" % re.escape(t), text):
                cands.append((f, t, t in have[f[0]]))
                break

    new = [c for c in cands if not c[2]]
    print("field rows whose ctype is anonymous but whose name/meaning names a declared type: %d"
          % len(cands))
    print("   of those, the owning type ALREADY has that edge via another row : %d"
          % (len(cands) - len(new)))
    print("   CANDIDATE NEW EDGES, prose only                                 : %d" % len(new))
    print()
    print("%-30s %-8s %-26s -> %s" % ("owner", "offset", "field", "target named in prose"))
    for f, t, _ in new:
        print("%-30s +0x%-5s %-26s -> %s" % (f[0][:30], f[1], f[3][:26], t))
    print()
    print("current inbound-pointer graph: %d types have at least one inbound ctype edge"
          % len({t for s in have.values() for t in s}))
    print()
    print("NOTHING IS WRITTEN. `the meaning mentions a type` is weaker than `the field points at")
    print("one`: a meaning may name a type because the field INDEXES it, or because the type is")
    print("one dereference further out - LegacyPs2GsTextureContext +0x150 is exactly that, and")
    print("writing the child type there would have been wrong by one indirection.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
