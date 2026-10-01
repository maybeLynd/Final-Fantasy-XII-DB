#!/usr/bin/env python3
"""EC-7's .as7 role corrections (SWE2-EC7, 2026-09-30) - the byte facts the corrected layout-page lines rest on, read
from the shipping EXE (Database/Tools/work/exe/FFXII_TZA.exe, gitignored). Each assertion can fail:

  A1  00248500 takes its second argument (rdx, the tail block) into rdi, reads the mode from byte [rdx] and k from
      byte [rdi + 1]: `mov rdi, rdx`, `movzx edx, byte ptr [rdx]`, `movzx r9d, byte ptr [rdi + 1]`.
  A2  00248500 builds the dictionary-offset mask as 0xFFFF >> (k + 1): `lea ecx, [r9 + 1]` then `shr r15w, cl`.
  A3  0024AA00 calls 00248500 exactly once (one call site, per page, inside its loop).
  A4  002CEFD0 calls 0024AA00 exactly twice (the two 0x102-page runs).
  A5  sensitivity: A1's `movzx r9d, byte ptr [rdi + 1]` is not in 0024AA00, so A1 is not a pattern every body matches.
Exit 0 when all hold, 1 otherwise.
"""
import os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
for _ in range(8):
    if os.path.isdir(os.path.join(ROOT, "Database", "Tools")):
        break
    ROOT = os.path.dirname(ROOT)
EXE = os.environ.get("FF12_EXE") or os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
secs = []
off = pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
    secs.append((va, vs, ra, rs))
    off += 40
md = Cs(CS_ARCH_X86, CS_MODE_64)


def insns(va, size):
    rva = va - base
    for sva, svs, sra, srs in secs:
        if sva <= rva < sva + max(svs, srs):
            o = sra + (rva - sva)
            return list(md.disasm(d[o:o + size], va))
    raise SystemExit("unmapped %08X" % va)


def has(ins, mn, ops):
    return any(i.mnemonic == mn and i.op_str == ops for i in ins)


ok = True
c = insns(0x00248500, 430)
a1 = has(c, "mov", "rdi, rdx") and has(c, "movzx", "edx, byte ptr [rdx]") and has(c, "movzx", "r9d, byte ptr [rdi + 1]")
print("A1 00248500 mode from [rdx], k from [rdi + 1]:", a1)
a2 = any(x.mnemonic == "lea" and x.op_str == "ecx, [r9 + 1]" and y.mnemonic == "shr" and y.op_str == "r15w, cl"
         for x, y in zip(c, c[1:]))
print("A2 00248500 offset mask 0xFFFF >> (k + 1):", a2)
w = insns(0x0024AA00, 293)
n3 = sum(1 for i in w if i.mnemonic == "call" and i.op_str == "0x248500")
print("A3 0024AA00 calls to 00248500:", n3)
s = insns(0x002CEFD0, 1005)
n4 = sum(1 for i in s if i.mnemonic == "call" and i.op_str == "0x24aa00")
print("A4 002CEFD0 calls to 0024AA00:", n4)
a5 = not has(w, "movzx", "r9d, byte ptr [rdi + 1]")
print("A5 sensitivity, the A1 load absent from 0024AA00:", a5)
ok = a1 and a2 and n3 == 1 and n4 == 2 and a5
print("ALL HOLD" if ok else "FAILED")
sys.exit(0 if ok else 1)
