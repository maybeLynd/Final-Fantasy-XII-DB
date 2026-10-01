"""PDeferredLightingSlot0080: its "unobserved" spans are read, field by field, by the slot evaluator 0065A960
(OPUS, 2026-09-27). Control. Static.
  P1 RECEIVER: 00659EC0 calls 0065A960 with r8 = base + 0x50 + (i << 7) for each slot and with r8 = base + 0x4050
     (slot 128); 0065A960 moves r8 into rbx (0065A9D1), so [rbx + d] is the slot's +d
  P2 0065A960 reads floats (movss / mulss) at +0x00, +0x04, +0x08, +0x0C, +0x10, +0x14, +0x18, +0x1C, +0x20, +0x24,
     +0x28, +0x2C, +0x54, +0x58, +0x5C, +0x60; integer dwords at +0x50 (cmp / mov), +0x64 (cmp), +0x68 (mov); and takes
     +0x30's address (0065AF32)
  P3 STORE REGRESSION: no DISCOVERED unobserved row covers an offset P2 reads
Not claimed: meanings; +0x40..+0x4F and +0x74..+0x7F (no read found); writers (the defaults are CLASSIFIED from the
live buffer on the existing rows).
"""
import os, re, struct, sys, collections
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

C, E = I(0x659EC0), I(0x65A960)
check("P1 the caller passes slot addresses in r8 and the evaluator keeps them in rbx",
      C.get(0x65A46C) == "lea r8, [rbx + 0x4050]" and C.get(0x65A479) == "call 0x65a960"
      and C.get(0x65A493) == "shl rax, 7" and C.get(0x65A497) == "lea r8, [rbx + 0x50]" and C.get(0x65A49B) == "add r8, rax"
      and C.get(0x65A4A4) == "call 0x65a960" and E.get(0x65A9D1) == "mov rbx, r8" and 0x50 + 128 * 0x80 == 0x4050)
acc = collections.defaultdict(set)
for a, s in E.items():
    m = re.search(r"dword ptr \[rbx(?: \+ (0x[0-9a-f]+|\d+))?\]", s)
    if m: acc[int(m.group(1), 0) if m.group(1) else 0].add(s.split()[0])
FL = [0x00, 0x04, 0x08, 0x0C, 0x10, 0x14, 0x18, 0x1C, 0x20, 0x24, 0x28, 0x2C, 0x54, 0x58, 0x5C, 0x60]
INT = {0x50: {"cmp", "mov"}, 0x64: {"cmp"}, 0x68: {"mov"}}
check("P2 floats at the sixteen offsets, integer dwords at +0x50 / +0x64 / +0x68, +0x30 address-taken",
      all(acc[o] and acc[o] <= {"movss", "mulss"} for o in FL) and all(acc[o] == k for o, k in INT.items())
      and E.get(0x65AF32) == "lea r10, [rbx + 0x30]",
      str({hex(o): sorted(v) for o, v in sorted(acc.items())}))
rows = []
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "PDeferredLightingSlot0080": rows.append((int(c[1], 16), int(c[2]), c[3], c[6]))
read = FL + list(INT)
bad = [r[2] for r in rows if r[3] == "DISCOVERED" and r[2].lower().startswith("unobserved") and any(r[0] <= o < r[0] + r[1] for o in read)]
check("P3 STORE REGRESSION: no unobserved row covers a read offset", not bad and rows, str(bad))
print("FAILS", fails)
sys.exit(1 if fails else 0)
