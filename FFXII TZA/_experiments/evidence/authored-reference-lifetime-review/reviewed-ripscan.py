#!/usr/bin/env python3
"""ripscan.py LO HI [--range A B] - every .text instruction whose rip-relative memory operand resolves into
[LO, HI) (hex image addresses), with the function, the access kind and the target address."""
import struct, sys, bisect, argparse
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
ap = argparse.ArgumentParser()
ap.add_argument("lo"); ap.add_argument("hi"); ap.add_argument("--range", nargs=2, default=None)
a = ap.parse_args()
lo, hi = int(a.lo, 16), int(a.hi, 16)
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    if d[o:o + 8].rstrip(b"\0") == b".text":
        vs = struct.unpack_from("<I", d, o + 8)[0]; va = struct.unpack_from("<I", d, o + 12)[0]; ro = struct.unpack_from("<I", d, o + 20)[0]
funcs = []
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs.append((int(p[0], 16), p[1], int(p[2])))
    except (ValueError, IndexError): pass
funcs.sort()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
r0, r1 = (int(a.range[0], 16), int(a.range[1], 16)) if a.range else (BASE + va, BASE + va + vs)
WR = {"mov", "or", "and", "xor", "add", "sub", "inc", "dec", "bts", "btr", "movss", "movsd", "movups", "movaps", "cvtsi2ss", "setne", "sete", "setg", "setl", "seta", "setb"}
for e, n, sz in funcs:
    if e < r0 or e >= r1: continue
    off = ro + (e - BASE - va)
    for ins in md.disasm(d[off:off + sz], e):
        for k, op in enumerate(ins.operands):
            if op.type != X86_OP_MEM or not op.mem.base or ins.reg_name(op.mem.base) != "rip": continue
            tgt = ins.address + ins.size + op.mem.disp
            if not (lo <= tgt < hi): continue
            kind = "w" if (k == 0 and ins.mnemonic in WR) else "r"
            if ins.mnemonic in ("cmp", "test"): kind = "r"
            print("%08X  %08X  %s  %-8s %-44s %08X %s" % (tgt, ins.address, kind, ins.mnemonic, ins.op_str, e, n))
