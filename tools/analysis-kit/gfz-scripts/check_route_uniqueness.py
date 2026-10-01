#!/usr/bin/env python3
"""check_route_uniqueness.py - a route that does not determine a type conflates every census.

WHY THIS EXISTS. The route column says how to REACH an object, and the route-seeded censuses
seed from it. When two types share a route string the tool cannot tell them apart: it seeds
both from the same places and attributes every offset it finds to whichever type was asked
for. The result is not an error - it is a plausible, larger census, which is the dangerous
shape.

MEASURED, not hypothetical. `RenderStrideC0Element` and `RenderResourceEntry` both carry
`FN 0x002ED570+0x0`, because 002ED570 is the slot resolver SHARED by three banks and its return
is whichever bank's element went in. Running the standard tool on that route bare seeds 87
hosts and reports 43 offsets; restricting the hosts to the 60 that
`classify_slot_resolver_sites.py` attributes to one bank gives 26. **The bare run adds
seventeen offsets that belong to other banks' element types** - +0x02, +0x20, +0x24, +0x28,
+0x30, +0x38, +0x44, +0x48, +0xA4, +0xAC, +0xB2, +0xB3, +0xB6, +0xB8, +0xB9, +0xBA, +0xBB - and
nothing in the output says so.

A SHARED ROUTE IS NOT AUTOMATICALLY WRONG, and this reports rather than refuses. Two types can
legitimately be reached the same way and be told apart by context a route does not capture.
What is always true is that the ROUTE ALONE CANNOT SELECT THE TYPE, so any census seeded from
it needs an explicit restriction - and that restriction has to live somewhere a later reader
will find, which today means the evidence column.

    check_route_uniqueness.py [--self-test]
"""
import argparse
import collections
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kit_paths as KP  # noqa: E402
import tsv_io  # noqa: E402

# A route seeded by the census tools; sharing one of these is what actually conflates a run.
SEEDABLE = ("PTR ", "FN ", "STATIC ")


def scan(db):
    hdr, rows, _t = tsv_io.read(os.path.join(db, "_types", "types.tsv"))
    i = {c: n for n, c in enumerate(hdr)}
    by = collections.defaultdict(list)
    for r in rows:
        if not r or not r[0] or len(r) <= i["route"]:
            continue
        route = r[i["route"]].strip()
        if route:
            by[route].append(r[0])
    return {k: v for k, v in by.items() if len(v) > 1}


def seedable(route):
    return any(alt.strip().startswith(SEEDABLE) for alt in route.split("|"))


def self_test():
    ok = True
    cases = [("FN 0x002ED570+0x0", True), ("PTR 0x0209BE80", True),
             ("STATIC 0x022C6F30 | PTR 0x022C6F20", True),
             ("EMBED RenderResourceRoot +0x60", False),
             ("CHAIN ActorStorageRecord +0xA8 stride=0x28", False)]
    for route, want in cases:
        got = seedable(route)
        ok &= got == want
        print("  %-42s seedable=%-5s expected %s" % (route[:42], got, want))
    print("SELF-TEST", "PASSES" if ok else "FAILS")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    dups = scan(a.db)
    seed = {k: v for k, v in dups.items() if seedable(k)}
    print("ROUTE UNIQUENESS  a route that does not determine a type conflates every census")
    print("  routes shared by more than one type : %d" % len(dups))
    print("  of those, SEEDABLE by the census tools (the ones that actually conflate): %d"
          % len(seed))
    for k, v in sorted(dups.items(), key=lambda kv: (not seedable(kv[0]), kv[0])):
        print("\n  %s%s" % (k, "   <-- SEEDABLE" if seedable(k) else ""))
        for t in v:
            print("      %s" % t)
    if seed:
        print("\n  A census seeded from a shared route attributes other types' offsets to the")
        print("  one asked for, and reports a LARGER result rather than an error. Each of the")
        print("  above needs its restriction recorded where a later reader will find it.")
    return 1 if seed else 0


if __name__ == "__main__":
    sys.exit(main())
