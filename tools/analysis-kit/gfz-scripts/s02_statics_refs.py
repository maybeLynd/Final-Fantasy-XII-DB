"""s02_statics_refs.py - every rip-relative reference into S-02's contract-named statics (OPUS, 2026-09-24).

Direction from the repaired reg_tracking.op_kind, width from the operand size, one decode of every
listed body. Output: site, function, target, offset-in-window, kind, width, instruction.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_default_instance_writers as W  # noqa: E402
import reg_tracking as RT  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_REG_RIP  # noqa: E402

WINDOWS = [
    ("gate-enable", 0x01E0C440, 0x01E0C4A0),
    ("registry", 0x01FD4100, 0x01FD4800),
    ("tick-deferred", 0x01EED040, 0x01EED090),
]


def main(out):
    img = W.Image()
    rows = []
    for entry in sorted(img.sizes):
        size = img.sizes[entry]
        if not 0 < size <= 0x20000:
            continue
        b = img.read(entry, size)
        if not b:
            continue
        for i in img.md.disasm(b, entry):
            for oi, op in enumerate(i.operands):
                if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP or op.mem.index:
                    continue
                t = i.address + i.size + op.mem.disp
                for name, lo, hi in WINDOWS:
                    if lo <= t < hi:
                        rows.append((name, t, i.address, entry, RT.op_kind(i, op, oi), op.size,
                                     "%s %s" % (i.mnemonic, i.op_str)))
    rows.sort()
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("window\ttarget\tsite\tfunction\tkind\twidth\tinstruction\n")
        for r in rows:
            f.write("%s\t%08X\t%08X\t%08X\t%s\t%d\t%s\n" % r)
    per = collections.defaultdict(collections.Counter)
    for name, t, site, fn, k, w, txt in rows:
        per[(name, t)][k] += 1
        per[(name, t)]["w%d" % w] += 1
    for (name, t), c in sorted(per.items()):
        print("%-14s %08X  %s" % (name, t, " ".join("%s=%d" % kv for kv in sorted(c.items()))))
    print(len(rows), "references")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "s02-statics-refs.tsv")
