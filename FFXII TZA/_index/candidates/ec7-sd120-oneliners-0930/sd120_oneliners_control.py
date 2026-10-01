#!/usr/bin/env python3
"""SD-120 one-liner corrections (SWE2-EC7, 2026-09-30) - the byte facts the corrected lines rest on, read from the
shipping EXE (Database/Tools/work/exe/FFXII_TZA.exe, gitignored). Each assertion can fail:

  C1  0053DB50 indexes its keys with a 16-byte stride: `add rcx, rcx` followed by a `[r9 + rcx*8]` load
      (the published line said 8-byte pairs), and a `shl rax, 4` elsewhere in the body.
  C2  00507120 calls 0053DB50 exactly once (the published line said it "runs the per-item step").
  C3  0050A100 contains no call instruction (call-free, as both readings agree).
  C4  sensitivity: the same stride test on 0053DB50's own caller 00507120 finds no `add rcx, rcx` + `*8` pair,
      so C1 is not a pattern every body matches.
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


def body(va, size):
    rva = va - base
    for sva, svs, sra, srs in secs:
        if sva <= rva < sva + max(svs, srs):
            o = sra + (rva - sva)
            return d[o:o + size]
    raise SystemExit("unmapped %08X" % va)


md = Cs(CS_ARCH_X86, CS_MODE_64)


def insns(va, size):
    return list(md.disasm(body(va, size), va))


def stride16(ins):
    for a, b in zip(ins, ins[1:]):
        if a.mnemonic == "add" and a.op_str == "rcx, rcx" and "rcx*8]" in b.op_str:
            return "%08X %s %s ; %08X %s %s" % (a.address, a.mnemonic, a.op_str, b.address, b.mnemonic, b.op_str)
    return None


ok = True
db50 = insns(0x0053DB50, 437)
s = stride16(db50)
shl = [i for i in db50 if i.mnemonic == "shl" and i.op_str.endswith(", 4")]
print("C1 0053DB50 16-byte stride:", s, "| shl ..., 4 at", ["%08X" % i.address for i in shl])
ok &= bool(s) and bool(shl)
c7120 = [i for i in insns(0x00507120, 867) if i.mnemonic == "call"]
n = sum(1 for i in c7120 if i.op_str == "0x53db50")
print("C2 00507120 calls to 0053DB50:", n, "of", len(c7120), "calls")
ok &= n == 1
ca100 = [i for i in insns(0x0050A100, 2842) if i.mnemonic == "call"]
print("C3 0050A100 call instructions:", len(ca100))
ok &= len(ca100) == 0
s4 = stride16(insns(0x00507120, 867))
print("C4 sensitivity, the same stride test on 00507120:", s4)
ok &= s4 is None
print("ALL HOLD" if ok else "FAILED")
sys.exit(0 if ok else 1)
