"""WidgetSingleton0209C498: +0x160 and +0x2A8 are two child widgets of 0x148 bytes built in place (OPUS, 2026-09-27).
Control. Static.
  C1 0029D4D0 loads the singleton from its slot 0209C498 and calls the in-place widget constructor 00245000 twice:
     rcx = singleton + 0x160, then + 0x2A8; edx = 0x148 both times; r8 = the same handler 0029D550
  C2 the two children tile the span exactly: 0x160 + 0x148 = 0x2A8, 0x2A8 + 0x148 = 0x3F0 (the next declared row,
     byte03F0)
  C3 STORE REGRESSION: +0x160 and +0x2A8 are embedded Widget rows of 0x148 bytes, and no row starts inside either child
Not claimed: what the children display; the handler 0029D550's behaviour.
"""
import os, struct, sys
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
cs = Cs(CS_ARCH_X86, CS_MODE_64)
X = list(cs.disasm(d[off(0x29D4D0):off(0x29D4D0) + 0x50], 0x29D4D0))
I = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in X}
sz = {x.address: x.size for x in X}
rip = lambda a: a + sz[a] + int(I[a].split("+ ")[1].rstrip("]"), 16)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
check("C1 two in-place 0x148 widgets at +0x160 and +0x2A8 of [0209C498], one handler",
      I.get(0x29D4D4, "").startswith("mov rcx, qword ptr [rip") and rip(0x29D4D4) == 0x209C498
      and I.get(0x29D4E2) == "add rcx, 0x160" and I.get(0x29D4EC) == "mov edx, 0x148" and I.get(0x29D4F1) == "call 0x245000"
      and I.get(0x29D4F6, "").startswith("mov rcx, qword ptr [rip") and rip(0x29D4F6) == 0x209C498
      and I.get(0x29D504) == "add rcx, 0x2a8" and I.get(0x29D50E) == "mov edx, 0x148" and I.get(0x29D513) == "call 0x245000"
      and rip(0x29D4DB) == rip(0x29D4FD) == 0x29D550)
check("C2 the children tile +0x160..+0x3EF", 0x160 + 0x148 == 0x2A8 and 0x2A8 + 0x148 == 0x3F0)
rows = []
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "WidgetSingleton0209C498": rows.append((int(c[1], 16), int(c[2]), c[3], c[4]))
inside = [r[2] for r in rows if 0x160 < r[0] < 0x3F0 and r[0] != 0x2A8]
check("C3 STORE REGRESSION: two embedded Widget rows of 0x148, nothing starting inside them",
      (0x160, 0x148, "childWidget160", "Widget") in rows and (0x2A8, 0x148, "childWidget2A8", "Widget") in rows and not inside, str(inside))
print("FAILS", fails)
sys.exit(1 if fails else 0)
