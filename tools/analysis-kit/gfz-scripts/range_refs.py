#!/usr/bin/env python3
"""Every reference into a VA RANGE: RIP-relative operands and image-base accesses, by function.

usage: range_refs.py <lo_hex> <hi_hex>
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402

lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
d, base, secs = G.load_pe(G.EXE)
funcs, flist = [], []
f = io.open(G.FUNCS, encoding="utf-8", errors="replace")
f.readline()
for line in f:
    p = line.split("\t")
    try:
        sz = int(p[2])
        if 0 < sz <= 0x20000:
            funcs.append((int(p[0], 16), sz))
            flist.append((int(p[0], 16), sz, p[1]))
    except (ValueError, IndexError):
        pass
flist.sort()


def owner(va):
    a, b = 0, len(flist) - 1
    while a <= b:
        m = (a + b) // 2
        e, n, nm = flist[m]
        if va < e:
            b = m - 1
        elif va >= e + n:
            a = m + 1
        else:
            return "%08X %s" % (e, nm)
    return "(unlisted)"


# rebuild the two code-side sets with their sites, which build_instruments discards
import capstone  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_REG_RIP  # noqa: E402

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
hits = {}
for entry, size in funcs:
    r = entry - base
    blob = None
    for nm, sva, vs, ra, rs in secs:
        if sva <= r < sva + max(vs, rs) and nm == ".text":
            o = r - sva
            if o < rs:
                blob = d[ra + o: ra + o + size]
            break
    if not blob:
        continue
    holders = set()
    for i in md.disasm(blob, entry):
        if i.mnemonic == "lea" and len(i.operands) == 2:
            dst, src = i.operands
            if (src.type == X86_OP_MEM and src.value.mem.base == X86_REG_RIP
                    and i.address + i.size + src.value.mem.disp == base):
                holders.add(dst.value.reg)
                continue
        if holders:
            _rd, wr = i.regs_access()
            holders -= set(wr)
        for o in i.operands:
            if o.type != X86_OP_MEM:
                continue
            tgt = None
            if o.value.mem.base == X86_REG_RIP:
                tgt = i.address + i.size + o.value.mem.disp
            elif holders and o.value.mem.base in holders and o.value.mem.disp:
                tgt = base + o.value.mem.disp
            if tgt is not None and lo <= tgt < hi:
                hits.setdefault(owner(i.address), []).append(
                    "%08X -> %08X %s %s" % (i.address, tgt, i.mnemonic, i.op_str[:44]))

print("references into %08X..%08X: %d function(s)\n" % (lo, hi, len(hits)))
for fn in sorted(hits):
    print("%s  (%d)" % (fn, len(hits[fn])))
    for s in hits[fn][:6]:
        print("    %s" % s)
