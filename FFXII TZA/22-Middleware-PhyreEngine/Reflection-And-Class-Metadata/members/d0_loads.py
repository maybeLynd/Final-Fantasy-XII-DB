# (FABLE, Claude Opus 5.5, 2026-09-26) - published copy; runs from any working directory.
# Usage for the descriptor contract's +0xD0 note: d0_loads.py 00590000 006C0000
"""d0_loads.py LO HI [DISP] - every qword load `mov r64, [reg+DISP]` (default 0xD0) in functions inside [LO, HI), with the
function, and whether the same function also loads [reg+0xC8] (the sibling keep-mask) and [reg+0x90]/[reg+0xA0]/[reg+0x80]
(descriptor list heads) - a weak descriptor-shape signal. Control: 0063C5E0 (the +0xD0 getter) must be listed."""
import struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16); DISP = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0xD0
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
vs, va, rs, ro = struct.unpack_from("<IIII", d, pe + 24 + opt + 8)
off = lambda v: ro + v - BASE - va
F = []
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: F.append((int(p[0], 16), int(p[2]), p[1]))
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
for fe, n, nm in sorted(F):
    if not (lo <= fe < hi) or n <= 0 or n > 100000: continue
    hits = []; sib = set()
    for x in md.disasm(d[off(fe):off(fe) + n], fe):
        ops = x.operands
        if len(ops) != 2 or ops[1].type != X86_OP_MEM: continue
        m = ops[1].mem
        if m.base == 0 or md.reg_name(m.base) in ("rsp", "rbp", "rip") or m.index != 0: continue
        if x.mnemonic == "mov" and ops[0].type == X86_OP_REG and ops[1].size == 8:
            if m.disp == DISP: hits.append("%08X" % x.address)
            elif m.disp in (0xC8, 0x80, 0x90, 0xA0): sib.add(hex(m.disp))
    if hits: print("%08X %-34s %-40s %s" % (fe, nm[:34], ",".join(hits[:6]), ",".join(sorted(sib))))
