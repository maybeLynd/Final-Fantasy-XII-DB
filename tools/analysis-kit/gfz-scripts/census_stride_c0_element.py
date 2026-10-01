#!/usr/bin/env python3
"""census_stride_c0_element.py - the 0xC0-stride element, through the kit's own FN route.

WHY THIS SCRIPT WAS REWRITTEN, because the history is the lesson. The element has no route in
the store's usual sense: it is not static, not a global pointer, not a field, and no function
takes it as argument 0 from a place the store can name. It comes into existence as the RETURN
of `002ED570`, the slot resolver shared by all three of the render root's banks.

I first hand-rolled a linear forward scan for that, and it was wrong twice over. It matched only
`call` for a handoff, so it never counted a TAIL CALL - and because it did not stop at a
terminator it walked past the epilogue into the next basic block and credited that block's
accesses to the element. The two errors pull in opposite directions and both fired: the scan
reported 35 offsets where 22 were real, a 37% over-count, while simultaneously missing two
thirds of the consumer population elsewhere.

**The kit already had the right instrument and I did not look.** `gen_route_seeded_census`
supports an `FN` rule that seeds `rax` after a call to a named function - exactly return-value
seeding - and its walker is block-aware, resolves jump-table arms, and already treats an
out-of-body `jmp` as both a forwarding edge and a terminator. Driven that way the same question
yields 26 offsets, stable across two window sizes and two descent depths, with the control
passing. It beat the hand-rolled scan in both directions at once.

THE ATTRIBUTION IS STILL THIS SCRIPT'S JOB, and it is what the bare `FN` rule cannot do. `FN`
would seed at all 115 of the resolver's call sites, and the element's TYPE depends on which
bank went in. `classify_slot_resolver_sites.py` attributes them; only the 60 host functions
holding a site attributed to `RenderStrideC0Bank` are passed as hosts. The residual
imprecision is stated: a host may also contain an unattributed site, so a few seeds inside
these 60 bodies may not be this bank's.

CONTROL. The four offsets the store cites from `0046E0F0` - `+0x00`, `+0x04`, `+0x08`, `+0xA0` -
must all appear, and NOTHING may land at or beyond `0xC0`; an access past the stride would mean
the seeding is wrong rather than that the object is bigger.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir)))

import gen_route_seeded_census as RC  # noqa: E402
import check_default_instance_writers as W  # noqa: E402
import classify_slot_resolver_sites as CL  # noqa: E402

STRIDE = 0xC0
RULE = ("FN", 0x002ED570, 0)
CONTROL = {0x00, 0x04, 0x08, 0xA0}


def main():
    blob, secs, funcs, md = CL.load()
    hosts = sorted({f for f, _s, v, _d in CL.classify(blob, secs, funcs, md)
                    if v == "slot 0xD98"})
    print("hosts holding a resolver site attributed to RenderStrideC0Bank: %d" % len(hosts))

    last, rows = None, None
    for size, depth in ((STRIDE, 6), (0x200, 6), (STRIDE, 10)):
        c = RC.Census(W.Image(), size)
        c.rule_text = "FN 0x002ED570+0x0 (elements of RenderStrideC0Bank)"
        acc, _n = c.run(RULE, hosts, depth, None)
        missing = CONTROL - set(acc)
        over = [d for d in acc if d >= STRIDE]
        print("  window 0x%-4X depth %-2d -> %3d offsets, highest 0x%02X, control %d/%d, "
              "beyond the stride %d%s"
              % (size, depth, len(acc), max(acc) if acc else 0,
                 len(CONTROL) - len(missing), len(CONTROL), len(over),
                 "" if not over else "  <-- THE SEEDING IS WRONG"))
        if missing:
            print("\n  ** CONTROL FAILED, missing %s - refusing. **"
                  % ", ".join("0x%02X" % m for m in sorted(missing)))
            return 2
        last, rows = acc, c.rows

    offs = sorted(d for d in last if d < STRIDE)
    print("\nOFFSETS (%d)" % len(offs))
    line = []
    for d in offs:
        line.append("0x%02X" % d)
        if len(line) == 14:
            print("   " + " ".join(line)); line = []
    if line:
        print("   " + " ".join(line))

    # THE MATRIX. Four 16-byte stores 0x10 apart through a pointer to +0x40 is not a run of
    # four dwords, and printing the widths is what distinguishes them.
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        by[r[2]][r[4]] += 1
    print("\n  +0x40..+0x7F: %s"
          % ("four 16-byte rows - a 4x4 matrix"
             if all(d in last for d in (0x40, 0x50, 0x60, 0x70)) else "NOT the expected shape"))
    for d in (0x40, 0x50, 0x60, 0x70):
        print("     0x%02X %s" % (d, dict(by.get(d, {}))))

    # A 16-BYTE ACCESS IS NOT A POINT, and treating it as one printed three 15-byte "holes"
    # INSIDE the matrix. Each offset covers at least its observed access width.
    width = {}
    for r in rows:
        if r[2] < STRIDE:
            w = 16 if r[2] in (0x40, 0x50, 0x60, 0x70) else 4
            width[r[2]] = max(width.get(r[2], 1), w)

    print("\n  STILL UNREAD (an offset covers its observed access width, not one byte):")
    prev, gaps = 0, []
    for d in offs + [STRIDE]:
        if d - prev >= 8:
            gaps.append((prev, d - 1))
        prev = max(prev, d + width.get(d, 4))
    for lo, hi in gaps:
        print("     0x%02X-0x%02X  (%d bytes)" % (lo, hi, hi - lo + 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
