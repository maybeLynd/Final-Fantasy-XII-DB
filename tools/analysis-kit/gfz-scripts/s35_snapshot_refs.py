#!/usr/bin/env python3
"""s35_snapshot_refs.py - every rip-relative reference into the gameplay input snapshot band.

OPUS, 2026-09-25, for S-35's types cell. CONTRACT-input-subsystem.md section 2 names one piece of
state, the snapshot 02F97360..02F9739B, and the store had no type for it. This lists every
rip-relative memory operand in every listed body whose target falls in [LO, HI), grouped by
(target, access width), with the access direction from reg_tracking.op_kind (access flags, not
operand position; 0 disagreements against iced-x86 over the whole image). Read-only.

    s35_snapshot_refs.py [--lo 0x02F97340] [--hi 0x02F973D0]
"""
import argparse
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_default_instance_writers as W  # noqa: E402
import reg_tracking as RT  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_REG_RIP  # noqa: E402

BASE = 0x02F97360


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lo", type=lambda s: int(s, 16), default=0x02F97340)
    ap.add_argument("--hi", type=lambda s: int(s, 16), default=0x02F973D0)
    a = ap.parse_args()
    img = W.Image()
    rows = []
    for e in sorted(img.sizes):
        n = img.sizes[e]
        if not 0 < n <= 0x20000:
            continue
        b = img.read(e, n)
        if not b:
            continue
        for i in img.md.disasm(b, e):
            for k, op in enumerate(i.operands):
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    t = i.address + i.size + op.mem.disp
                    if a.lo <= t < a.hi:
                        rows.append((t, op.size, RT.op_kind(i, op, k), e))
    kinds = collections.defaultdict(collections.Counter)
    fns = collections.defaultdict(set)
    for t, s, kd, e in rows:
        kinds[(t, s)][kd] += 1
        fns[(t, s)].add(e)
    for (t, s) in sorted(kinds):
        print("%08X %+5X w%-2d %-24s fns=%-3d %s" % (
            t, t - BASE, s, dict(kinds[(t, s)]), len(fns[(t, s)]),
            " ".join("%08X" % x for x in sorted(fns[(t, s)])[:6])))
    print("total %d references in %d functions" % (len(rows), len({r[3] for r in rows})))
    return 0


if __name__ == "__main__":
    sys.exit(main())
