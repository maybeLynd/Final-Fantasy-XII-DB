"""cell_access.py - every rip-relative access overlapping [cell, cell+width) , with access width and
read/write role, grouped by containing function (functions.tsv, largest entry <= site).
An access at a nearby address whose width covers the cell is reported as OVERLAP (not by name).
Usage: python cell_access.py 0x02F9736A 2
"""
import struct, sys, bisect
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
EXE = r"Database/Tools/work/exe/FFXII_TZA.exe"
FT = r"Database/Tools/work/graph/functions.tsv"
pe = pefile.PE(EXE, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
text = next(s for s in pe.sections if s.Name.rstrip(b"\0") == b".text")
data = text.get_data(); tva = IB + text.VirtualAddress
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
ents = sorted(int(l.split("\t")[0], 16) for l in open(FT, encoding="utf-8").read().splitlines()[1:] if l[:1].strip())
def fn(a):
    i = bisect.bisect_right(ents, a) - 1
    return ents[i] if i >= 0 else None
cell, width = int(sys.argv[1], 16), int(sys.argv[2])
lo, hi = cell - 16, cell + width
hits = {}
CH = 0x8000
for c0 in range(0, len(data) - 4, CH):
    c1 = min(c0 + CH, len(data) - 4)
    his = set()
    for T in (lo, hi):
        for tail in range(6):
            for p in (c0, c1 - 1):
                his.add(((T - (tva + p + 4 + tail)) & 0xFFFFFFFF) >> 16)
    for h in his:
        pat = struct.pack("<H", h)
        q = data.find(pat, c0 + 2, c1 + 4)
        while q != -1 and q < c1 + 2:
            p = q - 2
            d = struct.unpack_from("<i", data, p)[0]
            for tail in range(6):
                end = tva + p + 4 + tail
                if lo <= end + d < hi:
                    for back in range(9, 0, -1):
                        s = p - back
                        if s < 0: continue
                        ins = next(md.disasm(data[s:s + 16], tva + s), None)
                        if not ins or ins.address + ins.size != end: continue
                        if not any(op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP for op in ins.operands): continue
                        for k, op in enumerate(ins.operands):
                            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                                tgt = end + op.mem.disp
                                if tgt < cell + width and tgt + op.size > cell:
                                    role = "W" if (k == 0 and ins.mnemonic not in ("cmp", "test", "bt", "push", "call", "jmp")) else "R"
                                    if ins.mnemonic in ("lea",): role = "ADDR"
                                    if k == 0 and ins.mnemonic.startswith(("add", "sub", "inc", "dec", "or", "and", "xor", "btr", "bts")): role = "RW"
                                    hits[ins.address] = (role, op.size, tgt, ins.mnemonic + " " + ins.op_str)
                        break
            q = data.find(pat, q + 1, c1 + 4)
byfn = {}
for a, (role, sz, tgt, txt) in sorted(hits.items()):
    byfn.setdefault(fn(a), []).append((a, role, sz, tgt, txt))
readers_name = {f for f, v in byfn.items() if any(r in ("R", "RW") and t == cell for _, r, _, t, _ in v)}
readers_any = {f for f, v in byfn.items() if any(r in ("R", "RW") for _, r, _, _, _ in v)}
writers = {f for f, v in byfn.items() if any(r in ("W", "RW") for _, r, _, _, _ in v)}
print("cell %08X width %d: %d sites in %d functions" % (cell, width, len(hits), len(byfn)))
print("functions reading by exact address: %d; reading incl. overlapping wider/nearby access: %d; writing: %d" % (len(readers_name), len(readers_any), len(writers)))
for f in sorted(byfn):
    for a, r, sz, t, txt in byfn[f]:
        if r in ("W", "RW", "ADDR") or t != cell:
            print("  %08X in %s  %-4s w%d tgt %08X  %s" % (a, "%08X" % f if f else "?", r, sz, t, txt))
print("READERS_NAME", sorted("%08X" % f for f in readers_name))
print("overlap-only readers:", ["%08X" % f for f in sorted(readers_any - readers_name)])
