"""The field-access index attributes one bank-generic resolver's rows to two types (OPUS, 2026-09-27).
Control. Static. REPAIRED 2026-09-27 (SWE2-STRUCT): the routes are now bank-qualified and the index
splits; C3-C5 assert the REPAIRED invariants, so this script passes post-repair and fails if the
merge ever returns.

types.tsv used to route RenderStrideC0Element (0xC0) and RenderResourceEntry (0x50) both as
`FN 0x002ED570+0x0`. The index seeded a type from that return value, so every 002ED570 caller's
accesses were written to both types, clipped to each type's size.
  C1 002ED570 is bank-generic: row = decode(chunk) + (slot & [bank+0x50]) * [bank+0x48], the stride and mask read
     from the bank passed in rcx (002ED5DF-002ED5EA)
  C2 the one shared constructor 0051F9F0 stores the stride argument at +0x48 (0051FA84), and it is called with three
     strides: 0x50 (00409F10), 0xC0 (0046E250) and 0x260 (00477EE0) - three element types behind one resolver
  C3 REPAIRED: the two types no longer share an identical route - both carry distinct `bank=` qualifiers
     (0xD98 for the C0 bank, 0xD90 for the 0x50 bank); historically both were the bare `FN 0x002ED570+0x0`
  C4 REPAIRED: the index no longer merges them - RenderResourceEntry's functions are not a subset of
     RenderStrideC0Element's (historically all 58 RES functions were inside C0's set)
  C5 REPAIRED: the third bank no longer leaks in - 005049E0, which writes its receiver out to +0x250
     (a 0x260 row), is absent from RenderStrideC0Element's index
Not claimed: which bank each formerly-shared function serves beyond what the bank= qualifier proves; the
PersistentFlagPayload / SavePayload shared route (FN 0x002EF640+0x200), which may be a legitimate prefix
overlap (known exception in check_route_collisions.py).
"""
import re, struct, sys, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def I(f): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(f):off(f) + sizes[f]], f)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

R = I(0x2ED570)
check("C1 002ED570 takes stride and mask from the bank it is given",
      R.get(0x2ED584) == "mov rbx, rcx" and R.get(0x2ED5DF) == "mov eax, dword ptr [rbx + 0x50]"
      and R.get(0x2ED5E2) == "and eax, esi" and R.get(0x2ED5E4) == "imul eax, dword ptr [rbx + 0x48]")
K = I(0x51F9F0)
strides = {}
for f, a in ((0x409F10, 0x409F23), (0x46E250, 0x46E272), (0x477EE0, 0x477EF3)):
    m = re.match(r"mov edx, (0x[0-9a-f]+)$", I(f).get(a, "")); strides[f] = int(m.group(1), 16) if m else None
check("C2 the shared bank constructor stores the stride at +0x48 and is called with 0x50, 0xC0 and 0x260",
      K.get(0x51FA84) == "mov dword ptr [rbx + 0x48], edx" and strides == {0x409F10: 0x50, 0x46E250: 0xC0, 0x477EE0: 0x260},
      str({"%08X" % f: hex(s) for f, s in strides.items() if s}))
hdr = None; routes = {}
for l in open(DB / "_types/types.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if hdr is None: hdr = c; continue
    routes[c[0]] = dict(zip(hdr, c)).get("route", "").strip()
check("C3 the two types no longer share an identical route; each carries a distinct bank= qualifier",
      routes.get("RenderStrideC0Element") != routes.get("RenderResourceEntry")
      and "bank=0xD98" in routes.get("RenderStrideC0Element", "")
      and "bank=0xD90" in routes.get("RenderResourceEntry", ""),
      "%s / %s" % (routes.get("RenderStrideC0Element"), routes.get("RenderResourceEntry")))
fns = collections.defaultdict(set)
for l in open(DB / "_types/field-access-index.tsv", encoding="utf-8"):
    c = l.rstrip("\n").split("\t")
    if c[0] in ("RenderStrideC0Element", "RenderResourceEntry"): fns[c[0]].add(c[4])
e, c0 = fns["RenderResourceEntry"], fns["RenderStrideC0Element"]
check("C4 the index no longer merges them: RenderResourceEntry's functions are not a subset of C0's",
      not e <= c0, "%d RES fns, %d shared, %d C0-only" % (len(e), len(e & c0), len(c0 - e)))
W = I(0x5049E0)
far = max(int(m.group(1), 16) for v in W.values() for m in [re.search(r"ptr \[rsi \+ (0x[0-9a-f]+)\], ", v)] if m and v.startswith("mov"))
check("C5 005049E0 (writes its receiver to +0x%X, inside a 0x260 row) is absent from RenderStrideC0Element's index" % far,
      "005049E0" not in c0 and far >= 0x250 and W.get(0x504A10) == "mov rsi, rcx")
print("FAILS", fails)
sys.exit(1 if fails else 0)
