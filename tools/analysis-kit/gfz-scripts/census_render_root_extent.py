#!/usr/bin/env python3
"""An extent for the render root at 022C6F30, or an honest account of why there isn't one.

TWO INSTRUMENTS HAVE ALREADY FAILED ON THIS OBJECT AND BOTH SAID SO RATHER THAN GUESSING:
`gen_static_census.py` matches ABSOLUTE addresses and every access here is `[reg + small disp]`,
so its control (three sites the store cites) reported all three ABSENT and it refused to write.
`data_xref_scan.py` with `022C7020` as a control returned zero and refused - correctly, because
that address is never named in the image at all.

So this drives `gen_route_seeded_census.Census` directly on `STATIC 0x022C6F30`, which follows
the base register rather than the address.

THE BOUND IS THE WHOLE PROBLEM AND IT IS RUN TWICE FOR THAT REASON. A census window that is too
small reports its own truncation as an absence - which is exactly how the AB30 object's `+0x61CC`
access went missing behind a `0x6000` bound earlier in this store. So the census runs at two
window sizes and the result is only trusted if the larger one finds nothing the smaller missed.
If the highest offset sits hard against the window, that is truncation and the run says so.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# the census modules resolve their inputs relative to the repository root
os.chdir(os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir)))

import gen_route_seeded_census as RC  # noqa: E402
import check_absence_claims as G  # noqa: E402
import call_graph as CG  # noqa: E402
import check_default_instance_writers as W  # noqa: E402

BASE = 0x022C6F30
RULE = ("STATIC", BASE, 0)
# The six lea sites cache the root into the pointer global 022C6F20 and RELOAD it before
# passing it on (003323E2 stores, 003323F8 reloads), so a STATIC-only walk loses the taint
# through the global round-trip. Both alternatives are real and both are seeded.
RULE2 = ("PTR", 0x022C6F20, 0)
# The three interior-pointer stores 0041E3A0 makes. The store cites them; a census that cannot
# see them is not looking where the evidence came from.
CONTROL_SITES = {0x0041E3E5, 0x0041E3F6, 0x0041E404}


def run(img, callers, size, depth=6):
    c = RC.Census(img, size)
    acc, n, nh = None, 0, 0
    for rule, text in ((RULE, "STATIC 0x%08X" % BASE), (RULE2, "PTR 0x022C6F20")):
        c.rule_text = text
        hosts = RC.hosts_for(img, rule, callers)
        acc, k = c.run(rule, hosts, depth, acc)
        n += k
        nh += len(hosts)
    return c, acc, n, nh


def main():
    img = W.Image()
    callers, _c, _s = CG.call_maps(G.EXE, G.FUNCS)

    results = {}
    for size in (0x1000, 0x11000, 0x30000):
        c, acc, n, nhosts = run(img, callers, size)
        sites = {r[1] for r in c.rows}
        results[size] = (sorted(acc), c.rows, sites)
        top = max(acc) if acc else -1
        print("window 0x%-6X  hosts %-3d  triples %-5d  offsets %-4d  highest 0x%X%s"
              % (size, nhosts, n, len(acc), top,
                 "   <-- HARD AGAINST THE WINDOW, truncated" if top >= size - 0x40 else ""))
        missing = CONTROL_SITES - sites
        print("    control sites present: %d of %d%s"
              % (len(CONTROL_SITES) - len(missing), len(CONTROL_SITES),
                 "" if not missing else "  MISSING " + ", ".join("%08X" % m for m in
                                                                 sorted(missing))))

    small, big = results[0x11000][0], results[0x30000][0]
    gained = set(big) - set(small)
    print("\nwidening 0x11000 -> 0x30000 gained %d offset(s)%s"
          % (len(gained), "" if not gained else ": "
             + ", ".join("0x%X" % g for g in sorted(gained)[:12])))
    if not gained:
        print("  the smaller window was NOT truncating - the population is stable under widening")

    offs, rows, _ = results[0x30000]
    if not offs:
        print("\nNO OFFSETS. Report as an instrument result, not as an extent.")
        return 1

    print("\nOFFSET DISTRIBUTION, to find where the object stops rather than assume it")
    buckets = collections.Counter(o // 0x100 for o in offs)
    for b in sorted(buckets):
        print("   +0x%05X..+0x%05X  %d offset(s)" % (b * 0x100, b * 0x100 + 0xFF, buckets[b]))

    print("\nTHE LARGEST GAP between consecutive offsets, which is where an extent argument"
          "\nwould have to live:")
    pairs = sorted(zip(offs, offs[1:]), key=lambda p: p[1] - p[0], reverse=True)[:5]
    for lo, hi in pairs:
        print("   0x%05X -> 0x%05X   gap 0x%X" % (lo, hi, hi - lo))

    print("\nALL OFFSETS")
    line = []
    for o in offs:
        line.append("0x%05X" % o)
        if len(line) == 10:
            print("   " + " ".join(line)); line = []
    if line:
        print("   " + " ".join(line))
    return 0


if __name__ == "__main__":
    sys.exit(main())
