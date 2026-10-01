#!/usr/bin/env python3
"""scan_descriptor_flag_rip.py - every RIP-RELATIVE access to a static Phyre descriptor's +0xFC.

OPUS, 2026-09-25. The flag-bit census `scan_descriptor_flag_bits.py` is TIED: it seeds registers
provably holding a descriptor and follows them. That is the right defence against attribution by
displacement, and it is blind by construction to code that names a descriptor by its ABSOLUTE
address - which is how every class's static initialiser edits the flags word after the Abstract
constructor returns (`and dword [rip->desc+0xFC], ~2`, or `mov eax,[rip->desc+0xFC] ; and/or eax ;
mov [rip->desc+0xFC], eax`). It reported bit 3 "never set"; 35 initialisers set it.

This is the complement: the static descriptor objects are known exactly (the `lea rcx,[desc]` before
each call to a descriptor constructor listed in phyre-class-descriptor-vtable.tsv), so every
rip-relative operand landing on desc+0xFC..+0xFF is attributable with no taint at all. It reports
each access with its direction (reg_tracking.op_kind) and, for and/or with an immediate, the bits.
Read-only.

    scan_descriptor_flag_rip.py
"""
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402
import check_default_instance_writers as W  # noqa: E402
import reg_tracking as RT  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP  # noqa: E402

TSV = ("22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/"
       "phyre-class-descriptor-vtable.tsv")


def main():
    img = W.Image()
    rows = [l.rstrip("\r\n").split("\t") for l in io.open(os.path.join(G.DB, TSV), encoding="utf-8")
            if not l.startswith("#")]
    h = {k: i for i, k in enumerate(rows[0])}
    init = {int(r[h["static_initialiser"]], 16): r[0] for r in rows[1:] if r[h["static_initialiser"]]}
    ctor = {int(r[h["ctor_body"]], 16): r[0] for r in rows[1:]}
    objs = {}
    for e in sorted(img.sizes):
        n = img.sizes[e]
        if not 0 < n <= 0x2000:
            continue
        ins = list(img.md.disasm(img.read(e, n), e))
        for k, i in enumerate(ins):
            if (i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM
                    and i.operands[0].imm in ctor):
                for p in reversed(ins[max(0, k - 6):k]):
                    if (p.mnemonic == "lea" and p.op_str.startswith("rcx,")
                            and p.operands[1].mem.base == X86_REG_RIP):
                        objs[p.address + p.size + p.operands[1].mem.disp] = ctor[i.operands[0].imm]
                        break
    print("static descriptor objects: %d of %d classes (initialisers in the table: %d)"
          % (len(objs), len(ctor), len(init)))
    fc = {o + 0xFC + d: n for o, n in objs.items() for d in range(4)}
    tally = collections.Counter()
    bits = collections.defaultdict(set)
    where = collections.defaultdict(set)
    for e in sorted(img.sizes):
        n = img.sizes[e]
        if not 0 < n <= 0x20000:
            continue
        for i in img.md.disasm(img.read(e, n), e):
            for j, op in enumerate(i.operands):
                if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
                    continue
                t = i.address + i.size + op.mem.disp
                if t not in fc:
                    continue
                role = "initialiser" if e in init else "other"
                key = (i.mnemonic, RT.op_kind(i, op, j), role)
                tally[key] += 1
                where[key].add(e)
                if i.mnemonic in ("and", "or") and i.operands[1].type == X86_OP_IMM:
                    bits[(i.mnemonic, role)].add(i.operands[1].imm & 0xFFFFFFFF)
    for k, v in sorted(tally.items(), key=lambda kv: -kv[1]):
        print("  %-5s %-3s %-12s %4d sites in %4d functions" % (k[0], k[1], k[2], v, len(where[k])))
    for k, v in sorted(bits.items()):
        print("  %-3s immediates (%s): %s" % (k[0], k[1], " ".join("%08X" % x for x in sorted(v))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
