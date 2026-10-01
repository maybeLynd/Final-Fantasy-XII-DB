"""Reviewer's independent check for UQ-36 / UQ-39 (OPUS, 2026-09-27): does any EE/VU0 bank member match a Sony libvu0
routine's register allocation, under the linear map vf n = row n, or as a permutation-invariant shape?
Reuses ee_register_census.py's own address classification and member population (the functions its census lists).
  V1 the population is the census's 267 members (ee-register-census.tsv)
  V2 linear fingerprints, per member read / write row sets:
       sceVu0MulMatrix    reads vf4-7 and vf8-11, writes vf12-15 and ACC
       sceVu0ApplyMatrix  reads vf4-7 and vf8, writes vf9
       sceVu0Normalize    uses vf1 and vf2, reads vf00, writes Q
  V3 permutation-invariant MulMatrix shape: >= 8 rows read and not written, exactly 4 rows written and not read, ACC
     written - under ANY naming of the rows
  C  CONTROL: a synthetic member built with the MulMatrix allocation is detected by V2 and V3, and the same member with
     one row renamed is still detected by V3 (so V3 is naming-invariant)
"""
import os, re, struct, collections, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read(); B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
Q, ACC, VF00 = 0x022D9198, 0x022D91A0, 0x01EF93F0
def cls(t):                                       # the census's own VU classification
    if Q <= t < Q + 4: return "Q"
    if ACC <= t < ACC + 16: return "ACC"
    if ACC + 16 <= t < ACC + 32 * 16: return "vf%d" % ((t - ACC) // 16)
    if VF00 <= t < VF00 + 16: return "vf00"
READONLY = {"cmp", "test", "comiss", "ucomiss", "bt", "push", "lea"}
SZ = {}
for l in open(os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv"), encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: SZ[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
tsv = os.path.join(DB, "00-Engine-Core-Runtime", "Shared-Transform-Workbench", "members", "ee-register-census.tsv")
MEMBERS = [int(l.split("\t")[0], 16) for l in open(tsv, encoding="utf-8").read().splitlines()[1:] if l.strip()]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
def rw(e):
    R, W = set(), set()
    for x in md.disasm(d[off(e):off(e) + SZ[e]], e):
        for k, op in enumerate(x.operands):
            if op.type == X86_OP_MEM and op.mem.base and x.reg_name(op.mem.base) == "rip":
                c = cls(x.address + x.size + op.mem.disp)
                if not c: continue
                if k == 0 and x.mnemonic not in READONLY and len(x.operands) > 1: W.add(c)
                else: R.add(c)
    return R, W
def rows(s): return {c for c in s if re.match(r"vf\d+$", c) and c != "vf00"}
# EXACT: a member that IS the routine has the routine's row allocation (rows only; ACC / Q / vf00 as stated)
def mul_linear(R, W): return rows(R) - rows(W) == {"vf%d" % i for i in range(4, 12)} and rows(W) == {"vf%d" % i for i in range(12, 16)} and "ACC" in W
def apply_linear(R, W): return rows(R) - rows(W) == {"vf%d" % i for i in range(4, 9)} and rows(W) == {"vf9"}
def norm_linear(R, W): return rows(R) | rows(W) == {"vf1", "vf2"} and "vf00" in R and "Q" in W
# CONTAINMENT (disclosed, not a fingerprint): the routine's rows appear among a larger member's
def mul_contains(R, W): return {"vf%d" % i for i in range(4, 12)} <= R and {"vf%d" % i for i in range(12, 16)} <= W and "ACC" in W
def apply_contains(R, W): return {"vf%d" % i for i in range(4, 9)} <= R and "vf9" in W
def mul_shape(R, W):
    return len(rows(R) - rows(W)) >= 8 and len(rows(W) - rows(R)) == 4 and "ACC" in W
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
check("V1 population = the census's members", len(MEMBERS) == 267, str(len(MEMBERS)))
hits = collections.defaultdict(list); size = {}
for e in MEMBERS:
    R, W = rw(e); size[e] = (len(rows(R)), len(rows(W)))
    for nm, f in (("MulMatrix", mul_linear), ("ApplyMatrix", apply_linear), ("Normalize", norm_linear), ("MulMatrix-shape", mul_shape),
                  ("contains-MulMatrix", mul_contains), ("contains-ApplyMatrix", apply_contains)):
        if f(R, W): hits[nm].append("%08X" % e)
check("V2 no member carries a libvu0 allocation exactly (linear map)", not hits["MulMatrix"] and not hits["ApplyMatrix"] and not hits["Normalize"],
      str({k: v for k, v in hits.items() if k in ("MulMatrix", "ApplyMatrix", "Normalize")}))
big = {h: size[int(h, 16)] for h in hits["contains-MulMatrix"] + hits["contains-ApplyMatrix"]}
print("INFO containment (a larger member's rows include the routine's; not a fingerprint): MulMatrix %s, ApplyMatrix %s; (rows read, rows written) %s"
      % (hits["contains-MulMatrix"], hits["contains-ApplyMatrix"], big))
check("V3 no member has the MulMatrix shape under any row naming", not hits["MulMatrix-shape"], str(hits.get("MulMatrix-shape")))
R0 = {"vf%d" % i for i in range(4, 12)}; W0 = {"vf%d" % i for i in range(12, 16)} | {"ACC"}
R1 = (R0 - {"vf4"}) | {"vf20"}
check("C control: a planted MulMatrix allocation is found by V2 and V3; a renamed copy is still found by V3",
      mul_linear(R0, W0) and mul_shape(R0, W0) and not mul_linear(R1, W0) and mul_shape(R1, W0))
print("FAILS", fails)
sys.exit(1 if fails else 0)
