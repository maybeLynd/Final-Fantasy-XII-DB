"""script_class_census.py - EB-1 / UQ-312: what the Lua loader's callers hand it, and whether any shipped asset carries
one (FABLE, Claude Opus 5.5, 2026-09-26).

  S1 the bytes. 00684D10 loads r8 = [rcx+8] and r15 = [r8+0x50]. The registered field schema names that member
     PClassCallableMethodScript::m_script, a PScripting::VPScript pointer. The function returns early when [r8+0x60],
     the tagged m_entryPoint string (VPString), is empty after its low tag bit is removed (00684D3F-00684D4E).
     It then calls 00683C30(L, r15) at 00684DD1. 00683C30 reads the PScript's source bytes at +0x18, their size as
     dword +0x10 with bit 31 cleared, and the chunk name as the tagged string at +0x48, which the schema names
     PScript::m_sourceName (00683C36-00683C4E).
  S2 the schema agrees: PClassCallableMethodScript registers m_script at 0x50 and m_entryPoint at 0x60, and PScript
     registers m_sourceName at 0x48.
  S3 the shipped data. Across the packed namespaces of all .phyre files in the full extract (every distinct string
     pool), neither PScript nor PClassCallableMethodScript is declared as a class, so no shipped asset can
     deserialise one.
     Control: the same parse finds classes the game does ship, such as PMesh and PAssetReference.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, os, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
def dis(a, n): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + n], a)}
A = dis(0x684D10, 0x250); C = dis(0x683C30, 0x67)
check("S1 00684D10 takes m_script (+0x50), gates on the tagged m_entryPoint (+0x60), and hands m_script to 00683C30",
      A.get(0x684D37) == "mov r8, qword ptr [rcx + 8]" and A.get(0x684D3B) == "mov r15, qword ptr [r8 + 0x50]"
      and A.get(0x684D3F) == "movzx eax, byte ptr [r8 + 0x60]" and A.get(0x684D47) == "mov rdi, qword ptr [r8 + 0x60]"
      and A.get(0x684DCB) == "mov rdx, r15" and A.get(0x684DD1) == "call 0x683c30")
check("S1 00683C30 reads the PScript's size (+0x10, bit 31 cleared), bytes (+0x18) and tagged name (+0x48)",
      C.get(0x683C3D) == "mov r9, qword ptr [rdx + 0x48]" and C.get(0x683C47) == "mov eax, dword ptr [rdx + 0x10]"
      and C.get(0x683C4A) == "mov rdx, qword ptr [rdx + 0x18]" and C.get(0x683C4E) == "btr eax, 0x1f")
rows = list(csv.reader(open(DB / "22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/phyre-field-schema.tsv", encoding="utf-8"), delimiter="\t"))
S = {(r[0], r[2]): r[3] for r in rows if len(r) > 3}
check("S2 the schema: PClassCallableMethodScript m_script 0x50, m_entryPoint 0x60; PScript m_sourceName 0x48",
      S.get(("PClassCallableMethodScript", "m_script")) == "0x50" and S.get(("PClassCallableMethodScript", "m_entryPoint")) == "0x60"
      and S.get(("PScript", "m_sourceName")) == "0x48")
EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
if not EX.exists():
    check("S3 extract present", False, str(EX)); print("FAILS", fails); sys.exit(1)
classes = set(); pools = set(); nfiles = 0
for p in EX.rglob("*"):
    if p.suffix.lower() != ".phyre": continue
    nfiles += 1
    with open(p, "rb") as f:
        h = f.read(12)
        if len(h) < 12: continue
        hs, ns = struct.unpack_from("<II", h, 4); f.seek(hs); b = f.read(ns)
    if len(b) < 0x20: continue
    A_, nC, nM, sp = struct.unpack_from("<IIII", b, 8)
    base = 0x20 + 4 * A_; mb = base + 36 * nC; pool = mb + 24 * nM
    P = b[pool:pool + sp]
    if P in pools: continue
    pools.add(P)
    for k in range(nC):
        o = struct.unpack_from("<9I", b, base + 36 * k)[2]
        classes.add(P[o:P.find(b"\0", o)].decode("latin-1").split("<")[0])
print("   .phyre files %d, distinct pools %d, declared classes %d" % (nfiles, len(pools), len(classes)))
check("S3 no shipped namespace declares PScript or PClassCallableMethodScript",
      "PScript" not in classes and "PClassCallableMethodScript" not in classes and len(pools) > 10)
check("S3 control: the same parse finds shipped classes (PMesh, PAssetReference)",
      "PMesh" in classes and "PAssetReference" in classes, str(sorted(classes)[:8]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
