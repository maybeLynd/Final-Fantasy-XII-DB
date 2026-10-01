"""WidgetSingleton02CA8F38 +0x148: a dword set to -1 through the embedded object at +0xC0 (OPUS, 2026-09-27).
Control. Static.
  W1 00550540 loads the singleton from its slot 02CA8F38 (005505BC) and calls 00562F90 with rcx = singleton + 0xC0
     (005505C6 add rcx, 0xc0; 005505D0)
  W2 00562F90 keeps rcx in r14 and writes [r14 + 0x10], [r14 + 0x18] (the singleton's existing qword00D0 / qword00D8
     rows - the base checks out) and dword [r14 + 0x88] = -1 (00563065), i.e. the singleton's +0x148
  W3 STORE REGRESSION: +0x148 is a 4-byte row and no unobserved row covers it
Not claimed: what the value means.
"""
import os, re, struct, sys
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
def D(f, n): return list(cs.disasm(d[off(f):off(f) + n], f))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
C = D(0x550540, 0xA0); CI = {x.address: x for x in C}
x = CI.get(0x5505BC)
slot = x.address + x.size + int(re.search(r"\+ (0x[0-9a-f]+)\]", x.op_str).group(1), 16) if x else None
check("W1 the caller passes singleton + 0xC0 from slot 02CA8F38",
      slot == 0x2CA8F38 and CI[0x5505C6].mnemonic == "add" and CI[0x5505C6].op_str == "rcx, 0xc0" and CI[0x5505D0].op_str == "0x562f90")
S = {y.address: "%s %s" % (y.mnemonic, y.op_str) for y in D(0x562F90, 0xE8)}
check("W2 00562F90 writes +0x10 / +0x18 / dword +0x88 = -1 of the object it gets",
      S.get(0x562FAF) == "mov r14, rcx" and S.get(0x562FDA) == "mov qword ptr [r14 + 0x10], r8"
      and S.get(0x563061) == "mov qword ptr [r14 + 0x18], rax" and S.get(0x563065) == "mov dword ptr [r14 + 0x88], 0xffffffff")
rows = []
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "WidgetSingleton02CA8F38": rows.append((int(c[1], 16), int(c[2]), c[3]))
check("W3 STORE REGRESSION: a 4-byte row at +0x148, not inside an unobserved row",
      any(r[0] == 0x148 and r[1] == 4 for r in rows) and not [r for r in rows if r[2].lower().startswith("unobserved") and r[0] <= 0x148 < r[0] + r[1]],
      str([r for r in rows if 0x138 <= r[0] <= 0x150]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
