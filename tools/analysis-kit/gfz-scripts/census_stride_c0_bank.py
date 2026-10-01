#!/usr/bin/env python3
"""census_stride_c0_bank.py - a render-root slot bank, censused from its own entry points.

    python census_stride_c0_bank.py            # the +0x60 bank, RenderStrideC0Bank
    python census_stride_c0_bank.py --bank 50  # the +0x00 bank, RenderResourceEntryBank

WHY IT NEEDS ITS OWN SEEDS. The bank is `EMBED RenderResourceRoot +0x60`, and neither census
rule reaches it: a `STATIC` walk would look for `lea` sites of `022C6F90` and the code writes
`lea rcx, [rbx + 0x60]` off the root's register instead, while a `PTR` walk would need a global
holding the bank, and the only one is the root's own interior-pointer slot at `+0xD98`, which
is inside the object the walk is trying to enter. So the four functions that take the bank as
argument 0 are seeded directly - which is the same thing `gen_route_seeded_census.py` does for a
`ctor` column, no inference, just naming the entry points the image already has.

THE FOUR ENTRY POINTS, each verified to receive the bank rather than something else:
  0046E250  the initialiser  - called as `[rsi+0xD98]` from 0041E3A0 (0041E447/0041E450)
  0046E4B0  the constructor  - called as `[rsi+0xD98]` from 0041E3A0 (0041E410/0041E417)
  0046E3E0  the refresh      - the +0xD98 handler
  0046E0F0  UpdateFinalPoses - called as `[rbx+0xD98]` from 0041E340, its ONLY caller

  0046E420, `SkeletonModelGroup_RefreshLinkedResourceEntry`, is DELIBERATELY EXCLUDED. Two of
  its four callers pass `[rax+0xD98]` and the other two pass `[X+0x330]`, and no path from a
  `+0xD98` read to that `+0x330` exists in the image, so half its call sites may hand it a
  different bank. Including it would attribute offsets to this type that may belong to another.

CONTROL. `0046E290` and `0046E297` write the bank's `+0x60` vector and are cited in the store;
a census that cannot see them is not looking where the evidence came from, so the run refuses.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir)))

import gen_route_seeded_census as RC  # noqa: E402
import check_default_instance_writers as W  # noqa: E402

# THE +0x00 BANK CARRIES ITS OWN HAZARD and it is why that variant exists here rather than as a
# one-off: at the root's offset ZERO the child's address IS the parent's, so a census could
# absorb the ROOT's interior-pointer table at +0xD90..+0xDA8 and report a 0xDB0 object as a 0x60
# one. The run prints how many offsets land at or above 0xD90 so the absorption is visible
# rather than assumed absent. Measured 2026-09-19: none.
BANKS = {
    "c0": dict(name="RenderStrideC0Bank", embed=0x60, size=0x90,
               entries=[0x0046E250, 0x0046E4B0, 0x0046E3E0, 0x0046E0F0],
               control={0x0046E290, 0x0046E297}, windows=(0x90, 0x200, 0x1000)),
    "50": dict(name="RenderResourceEntryBank", embed=0x0, size=0x60,
               entries=[0x00409F10, 0x00409F70, 0x00409F80],
               # 0051FA84 and 0051FA8E write rowStride and bankShift through the shared
               # constructor; if the walk cannot reach them it never entered the descriptor.
               control={0x0051FA84, 0x0051FA8E}, windows=(0x60, 0x200, 0x1000)),
}
BANK = BANKS["50" if "--bank" in sys.argv and sys.argv[sys.argv.index("--bank") + 1] == "50"
             else "c0"]
ENTRIES = BANK["entries"]
CONTROL_SITES = BANK["control"]
WINDOWS = BANK["windows"]


def run(img, size, depth=6):
    c = RC.Census(img, size)
    c.rule_text = "EMBED RenderResourceRoot +0x%X" % BANK["embed"]
    acc = collections.defaultdict(set)
    for e in ENTRIES:
        if e not in img.sizes:
            print("  !! %08X unknown to this image" % e)
            continue
        fwd = set()
        c.walk(e, {W.ARG_REGS[0]: 0}, acc, fwd, None)
        for g in sorted(fwd):
            c.walk(g[0], {W.ARG_REGS[g[1] - 1]: g[2]}, acc, set(), None)
    return c, acc


def main():
    img = W.Image()
    seen = {}
    for size in WINDOWS:
        c, acc = run(img, size)
        sites = {r[1] for r in c.rows}
        seen[size] = (sorted(acc), sites)
        top = max(acc) if acc else -1
        missing = CONTROL_SITES - sites
        print("window 0x%-5X  offsets %-4d  highest 0x%X%s"
              % (size, len(acc), top,
                 "   <-- HARD AGAINST THE WINDOW, truncated" if top >= size - 8 else ""))
        print("    control sites present: %d of %d%s"
              % (len(CONTROL_SITES) - len(missing), len(CONTROL_SITES),
                 "" if not missing else "  MISSING " + ", ".join("%08X" % m
                                                                 for m in sorted(missing))))
        if missing:
            print("\n  ** CONTROL FAILED - the scan is not looking where the evidence came"
                  " from. Refused. **")
            return 2

    small, big = seen[0x200][0], seen[0x1000][0]
    gained = set(big) - set(small)
    print("\nwidening 0x200 -> 0x1000 gained %d offset(s)%s"
          % (len(gained), "" if not gained else ": "
             + ", ".join("0x%X" % g for g in sorted(gained))))
    if not gained:
        print("  stable under widening - the 0x200 window was not truncating")

    offs = seen[0x1000][0]
    print("\nOFFSETS (%d)" % len(offs))
    line = []
    for o in offs:
        line.append("0x%03X" % o)
        if len(line) == 12:
            print("   " + " ".join(line)); line = []
    if line:
        print("   " + " ".join(line))

    print("\n%s: against its declared 0x%X, and against the shared 0x00-0x5B prefix:"
          % (BANK["name"], BANK["size"]))
    pre = [o for o in offs if o < 0x5C]
    tail = [o for o in offs if o >= 0x5C]
    print("   inside the shared descriptor prefix (0x00-0x5B): %d -> %s"
          % (len(pre), ", ".join("0x%X" % o for o in pre)))
    print("   this type's own tail (0x5C and above)          : %d -> %s"
          % (len(tail), ", ".join("0x%X" % o for o in tail)))
    over = [o for o in offs if o >= BANK["size"]]
    print("   BEYOND the declared size                        : %d%s"
          % (len(over), "" if not over else " -> " + ", ".join("0x%X" % o for o in over)
             + "   <-- the bound is WRONG, not the census"))

    if BANK["embed"] == 0:
        absorbed = [o for o in offs if o >= 0xD90]
        print("   ROOT ACCESSES ABSORBED (offset >= 0xD90, the parent's slot table): %d%s"
              % (len(absorbed), "" if not absorbed else " -> " + ", ".join("0x%X" % o
                 for o in absorbed) + "   <-- the census entered the PARENT, refuse it"))

    print("\nWRITERS PER OFFSET")
    by = collections.defaultdict(set)
    for r in c.rows:
        by[r[2]].add(r[0])
    for o in offs:
        print("   0x%03X  %s" % (o, ", ".join("%08X" % f for f in sorted(by[o]))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
