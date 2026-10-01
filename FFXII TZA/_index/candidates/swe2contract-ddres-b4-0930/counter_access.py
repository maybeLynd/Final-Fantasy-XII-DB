"""counter_access.py - every instruction, over every listed function body, whose memory operand reaches the event-slot
pending counters 01F832B0 .. 01F832C3 (5 x dword), in either addressing form: rip-relative, or image-base-relative
(a non-rip base register plus the RVA 0x01E632B0 .. as the displacement). SWE2-CONTRACT, 2026-09-30. Static. Reads only.

Usage: python counter_access.py

Answers the event-slot page's display-side counter row (SWE2-AUDIT-SPEC narrowing of the batch-1 review): which of
001D0190, 001D0390, 001D5260, 001D5520 touch the counters, and how.

Controls, always run:
  C1  the rip form re-finds the lea of the array base at 001CC648 (rip_refs_01F832B0.out, batch-1 record);
  C2  the image-base-relative form re-finds 001CD0E0's jump-table base use at 001CD1CB (disp 0xAFCEC), the reference
      SWE2-DATA's manifest_walker.py R2 uses as its own control, so a zero for a function below is not a blind sweep.
Blind spot, stated: a pointer formed once (lea) and then indexed through another register is listed as the lea only.
"""
import os
import sys

import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "swe2contract-ddres-b1-0930"))
import block_writer_disjoint as b  # noqa: E402  (the batch-1 loader: functions.tsv extents + the shipped EXE)

BASE = 0x120000
LO, HI = 0x01F832B0, 0x01F832C4
ASKED = [0x001D0190, 0x001D0390, 0x001D5260, 0x001D5520]


def kind(ins, i):
    if ins.mnemonic == "lea":
        return "lea"
    if ins.mnemonic.startswith(("cmp", "test")):
        return "r"
    if ins.mnemonic in ("inc", "dec", "add", "sub") and i == 0:
        return "rw"
    return "w" if i == 0 and len(ins.operands) > 1 else "r"


def sweep(ext, at, want):
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    hits = []
    for entry, size in sorted(ext.items()):
        code = at(entry, size)
        if not code:
            continue
        for ins in md.disasm(code, entry):
            for i, op in enumerate(ins.operands):
                if op.type != capstone.x86.X86_OP_MEM:
                    continue
                if op.mem.base == capstone.x86.X86_REG_RIP:
                    t, form = ins.address + ins.size + op.mem.disp, "rip"
                elif op.mem.base != 0 or op.mem.index != 0:
                    t, form = BASE + op.mem.disp, "ibr"
                else:
                    continue
                if want(t, form, ins):
                    hits.append((entry, ins.address, form, kind(ins, i), ins.mnemonic, ins.op_str, t))
    return hits


def main():
    at, ext = b.load(), b.extents()
    hits = sweep(ext, at, lambda t, f, ins: LO <= t < HI or (f == "ibr" and ins.address == 0x001CD1CB))
    c1 = any(a == 0x001CC648 and fm == "rip" for _, a, fm, _, _, _, _ in hits)
    c2 = any(a == 0x001CD1CB and fm == "ibr" and t == BASE + 0xAFCEC for _, a, fm, _, _, _, t in hits)
    print("%s  C1 rip form re-finds the base lea at 001CC648" % ("PASS" if c1 else "FAIL"))
    print("%s  C2 image-base-relative form re-finds 001CD1CB disp 0xAFCEC" % ("PASS" if c2 else "FAIL"))
    counter = [h for h in hits if LO <= h[6] < HI]
    for fn, a, fm, k, m, ops, t in counter:
        print("%08X  %08X  %-3s  %-3s  %-5s %-44s -> %08X" % (fn, a, fm, k, m, ops, t))
    by_fn = {}
    for fn, *_ in counter:
        by_fn[fn] = by_fn.get(fn, 0) + 1
    for fn in ASKED:
        print("ASKED %08X  direct accesses: %d" % (fn, by_fn.get(fn, 0)))
    return 0 if (c1 and c2) else 1


if __name__ == "__main__":
    sys.exit(main())
