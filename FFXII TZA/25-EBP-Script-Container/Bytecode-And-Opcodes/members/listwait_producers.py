# (FABLE, Claude Opus 5.5, 2026-09-26) - published copy; runs from any working directory.
"""listwait_producers.py - image-wide census of list-wait producers. A list wait (kinds 5 and 7) needs the wait slot's
kind byte +0x14 = 5 or 7 AND an encoded list at +0x1C. Lists every immediate store of ANY width to [reg+0x14] whose low
byte is 5 or 7, and every register store to [reg+0x14], each only when a store to [same reg+0x1C] lies within 40
instructions before it. Control: the interpreter's kind-5 store 00261D24 (byte 5, REQWAITALL) and kind-7 store 00261B97
(word 0x107, shared by REQALL and REQIALL) must both be listed; the script prints PASS/FAIL."""
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
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
n_imm = n_reg = 0
seen = set()
for fe, n, nm in sorted(F):
    if n <= 0 or n > 100000: continue
    o = off(fe)
    if o < ro or o + n > ro + rs: continue
    ins = list(md.disasm(d[o:o + n], fe))
    for i, x in enumerate(ins):
        ops = x.operands
        if not x.mnemonic.startswith("mov") or len(ops) != 2 or ops[0].type != X86_OP_MEM: continue
        m = ops[0].mem
        if m.disp != 0x14 or m.base == 0 or md.reg_name(m.base) in ("rsp", "rbp", "rip") or m.index != 0: continue
        if ops[1].type == X86_OP_IMM:
            if (ops[1].imm & 0xFF) not in (5, 7): continue
            val = "imm %#x/%d" % (ops[1].imm, ops[0].size)
        elif ops[1].type == X86_OP_REG:
            val = "reg %s/%d" % (md.reg_name(ops[1].reg), ops[0].size)
        else: continue
        prior = [y for y in ins[max(0, i - 40):i] if y.mnemonic.startswith("mov") and len(y.operands) == 2
                 and y.operands[0].type == X86_OP_MEM and y.operands[0].mem.base == m.base and y.operands[0].mem.disp == 0x1C]
        if not prior: continue
        seen.add(x.address)
        if ops[1].type == X86_OP_IMM: n_imm += 1
        else: n_reg += 1
        print("%08X %-36s %08X %-18s +0x1C at %s" % (fe, nm[:36], x.address, val, ",".join("%08X" % y.address for y in prior)))
print("immediate kind-5/7 stores with a +0x1C store before them: %d; register stores: %d" % (n_imm, n_reg))
print("control (00261D24 and 00261B97 listed):", "PASS" if {0x261D24, 0x261B97} <= seen else "FAIL")
