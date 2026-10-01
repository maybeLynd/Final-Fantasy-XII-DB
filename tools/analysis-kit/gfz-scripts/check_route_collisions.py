#!/usr/bin/env python3
"""check_route_collisions.py - refuse two different-sized types on one undiscriminated FN route.

WHY THIS EXISTS. An `FN` route seeds a type from the getter's return at every call site. That
is sound only while the getter's return type is decided BY THE FUNCTION. A bank-generic
resolver - 002ED570 reads stride and mask out of the bank passed in rcx and serves 0x50,
0xC0 and 0x260 elements - returns a different type per call site, and an unqualified route
attributes every caller's accesses to every type that names it. Measured once in the wild:
`RenderStrideC0Element` and `RenderResourceEntry` both carried `FN 0x002ED570+0x0`, the
index merged them (all 58 functions of the smaller appeared in the larger) and a
0x260-row initialiser was clipped into the 0xC0 type's window
(route-collision-002ED570, OPUS-REQ-STRUCT-ROUTE-002ED570-BANK-GENERIC-0927).

THE RULE. Group every `FN 0xA+0xD` route alternative by (address, delta). Within a group, two
types of DIFFERENT declared size sharing the same `bank=` qualifier - including both
unqualified - are a collision: without a per-type discriminator the seed cannot tell them
apart. Same-size duplicates are not flagged (a shared route between equal extents may be a
prefix or alias relationship, judged elsewhere); a same-qualifier same-size pair is still
listed as SHARED for review.

KNOWN COLLISION, ADJUDICATED 2026-09-29 (SWE2-STRUCT): `PersistentFlagPayload` (0x1538)
and `SavePayload` (0x56490) share `FN 0x002EF640+0x200` legitimately - SavePayload declares
`+0x000 persistentFlagPayloadRegion` of exactly 0x1538, so the shared route is a declared
parent-member overlap (the flag-bank view reads the payload's first 0x1538 bytes), not an
undiscriminated merge. OPUS had called it "probably a prefix overlap" and deferred it from
OPUS-REQ-STRUCT-ROUTE-002ED570-BANK-GENERIC-0927; the store's own field row confirms it.
Kept in KNOWN so the pair stays visible rather than being re-flagged.

Usage:  python check_route_collisions.py [--store <db>/_types]
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402

R_FN = re.compile(r"^FN\s+0x([0-9A-Fa-f]+)\s*\+\s*0x([0-9A-Fa-f]+)"
                  r"(?:\s+bank=0x([0-9A-Fa-f]+))?\s*$")

# (getter, delta) -> [(type, size)] pairs exempted with their reason.
KNOWN = {
    (0x002EF640, 0x200): ("JUDGED prefix overlap - SavePayload declares +0x000 "
                          "persistentFlagPayloadRegion of 0x1538 (SWE2-STRUCT 2026-09-29)"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=os.path.join(
        KP.ROOT, "Database", "FFXII TZA", "_types"))
    a = ap.parse_args()

    hdr = None
    groups = collections.defaultdict(set)    # (addr,delta,bank) -> {(type,size)}
    for line in io.open(os.path.join(a.store, "types.tsv"),
                        encoding="utf-8", newline="").read().split("\n"):
        c = line.split("\t")
        if hdr is None:
            hdr = {n: i for i, n in enumerate(c)}
            continue
        if len(c) <= hdr["route"]:
            continue
        size = c[hdr["size"]].strip()
        for alt in (c[hdr["route"]] or "").split(" | "):
            m = R_FN.match(alt.strip())
            if not m:
                continue
            key = (int(m.group(1), 16), int(m.group(2), 16),
                   int(m.group(3), 16) if m.group(3) else None)
            groups[key].add((c[hdr["type"]], size))

    collisions, shared, known = [], [], []
    # each group's key already carries the bank qualifier, so members of a group all
    # share one discriminator value - different qualifier = different group entirely
    for (addr, delta, bank), ms in sorted(groups.items()):
        if len(ms) < 2:
            continue
        sizes = {s for _t, s in ms}
        label = "FN 0x%08X+0x%X bank=%s" % (addr, delta,
                                            "0x%X" % bank if bank is not None else "none")
        if len(sizes) > 1:
            if (addr, delta) in KNOWN:
                known.append((label, ms, KNOWN[(addr, delta)]))
            else:
                collisions.append((label, ms))
        else:
            shared.append((label, ms))

    print("ROUTE COLLISION CHECK - identical FN route, different sizes\n")
    print("  FN route alternatives grouped : %d" % len(groups))
    print("  KNOWN (documented exemptions)  : %d" % len(known))
    for label, ms, why in known:
        print("    %s  <-  %s" % (label, ", ".join("%s (%s)" % m for m in ms)))
        print("        %s" % why)
    print("  same qualifier, same size     : %d (SHARED - reviewable, not refused)"
          % len(shared))
    for label, ms in shared:
        print("    %s  <-  %s" % (label, ", ".join("%s (%s)" % m for m in ms)))
    print()
    if collisions:
        print("  COLLISIONS - same FN route and qualifier, different sizes:")
        for label, ms in collisions:
            print("    %s  <-  %s" % (label, ", ".join("%s (%s)" % m for m in ms)))
        print("\nFAIL %d collision(s)" % len(collisions))
        return 1
    print("PASS - no undiscriminated same-route FN groups")
    return 0


if __name__ == "__main__":
    sys.exit(main())
