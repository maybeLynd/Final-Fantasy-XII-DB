#!/usr/bin/env python3
"""EC-7 role corrections, second set (SWE2-EC7, 2026-09-30) - the byte facts the corrected lines rest on, read from the
shipping EXE (Database/Tools/work/exe/FFXII_TZA.exe, gitignored). Each assertion can fail:

  P1  each of 0043D8F0, 0043E440, 0043DB90, 0043DF80 calls the primitive allocator 008642A0 exactly once.
  P2  00438860 calls each of the four (its software-clip path's builders), 3 + 3 + 6 + 6 call sites.
  P3  sensitivity: 00438860 itself does not call 008642A0, so P1 is not a property every body in the family shares.
  T1  0024A710 builds the slot mask from bits 5, 6, 7 and the caller's bit k: `mov ebx, 0xe0` then `bts ebx, ecx`.
  T2  its walk starts at 0208F5B8 (the atlas registry's slot 0 +0x38) and steps 0x48 per slot.
  T3  its transfer base starts at 0x3520 and it queues transfers through 0024AF50 (two call sites).
  T4  it stores the packed descriptor through [r14 - 8], slot +0x30 when r14 points at slot +0x38.
  T5  sensitivity: T1's `mov ebx, 0xe0` is absent from 0024AF50, so T1 is not a pattern every body matches.
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
SIZE = {0x0043D8F0: 661, 0x0043E440: 874, 0x0043DB90: 999, 0x0043DF80: 1204, 0x0024A710: 711, 0x0024AF50: 0}


def insns(va, size):
    rva = va - base
    for sva, svs, sra, srs in secs:
        if sva <= rva < sva + max(svs, srs):
            o = sra + (rva - sva)
            return list(md.disasm(d[o:o + size], va))
    raise SystemExit("unmapped %08X" % va)


def calls(ins, tgt):
    return sum(1 for i in ins if i.mnemonic == "call" and i.op_str == "0x%x" % tgt)


def body_size(va):
    fn = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
    with open(fn, encoding="utf-8", errors="replace") as f:
        h = f.readline().rstrip("\n").split("\t")
        ia, isz = h.index("entry"), h.index("body_bytes")
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) > max(ia, isz) and p[ia].strip().upper().lstrip("0X").zfill(8) == "%08X" % va:
                return int(p[isz])
    raise SystemExit("no census row for %08X" % va)


ok = True
B = (0x0043D8F0, 0x0043E440, 0x0043DB90, 0x0043DF80)
for b in B:
    n = calls(insns(b, SIZE[b]), 0x8642A0)
    print("P1 %08X calls 008642A0: %d" % (b, n))
    ok &= n == 1
drv = insns(0x00438860, body_size(0x00438860))
want = {0x0043D8F0: 3, 0x0043E440: 3, 0x0043DB90: 6, 0x0043DF80: 6}
for b in B:
    n = calls(drv, b)
    print("P2 00438860 call sites to %08X: %d (want %d)" % (b, n, want[b]))
    ok &= n == want[b]
n = calls(drv, 0x8642A0)
print("P3 sensitivity, 00438860's own calls to 008642A0: %d (want 0)" % n)
ok &= n == 0
t = insns(0x0024A710, SIZE[0x0024A710])
t1 = any(x.mnemonic == "mov" and x.op_str == "ebx, 0xe0" for x in t) and any(x.mnemonic == "bts" and x.op_str == "ebx, ecx" for x in t)
print("T1 mask 0xE0 | 1<<k:", t1)
lea = [x for x in t if x.mnemonic == "lea" and x.op_str.startswith("r14, [rip + ")]
t2a = bool(lea) and lea[0].address + lea[0].size + int(lea[0].op_str.split("+ ")[1].rstrip("]"), 16) == 0x0208F5B8
t2b = any(x.mnemonic == "add" and x.op_str == "r14, 0x48" for x in t)
print("T2 walk from 0208F5B8, stride 0x48:", t2a, t2b)
t3a = any(x.mnemonic == "mov" and x.op_str.endswith(", 0x3520") for x in t)
t3b = calls(t, 0x24AF50)
print("T3 base 0x3520:", t3a, "; calls to 0024AF50:", t3b)
t4 = any(x.mnemonic == "mov" and x.op_str.startswith("qword ptr [r14 - 8], ") for x in t)
print("T4 descriptor store through [r14 - 8]:", t4)
q = insns(0x0024AF50, body_size(0x0024AF50))
t5 = not any(x.mnemonic == "mov" and x.op_str == "ebx, 0xe0" for x in q)
print("T5 sensitivity, T1's mask load absent from 0024AF50:", t5)
ok &= t1 and t2a and t2b and t3a and t3b == 2 and t4 and t5
print("ALL HOLD" if ok else "FAILED")
sys.exit(0 if ok else 1)
