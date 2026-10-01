"""MapScreenContainer +0x190..+0x1AF: four qword handles filled by one loader (OPUS, 2026-09-27). Control. Static.
  M1 002BA040 and 003CB440 load the container from its route slots (0209E5F0, 02B47760) and call 00404060 with
     rdx = container + 0x190
  M2 00404060 stores the handle 002493D0 / 00249320 returns into [rdx + 8], [rdx], [rdx + 0x10] and [rdx + 0x18], each
     as a qword (0040409D, 004040CC, 004040FA, 00404111) - so +0x198 is written and +0x1A8 is a qword
  M3 STORE REGRESSION: +0x198 and +0x1A8 are 8-byte rows, and no unobserved row covers +0x190..+0x1AF
Not claimed: what the four handles name (the loader's ids are 0xB9, 0xBA, 0xB0 and 0xBF).
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
def caller(f, call):
    xs = D(f, 0x200); I = {x.address: x for x in xs}
    i = next(k for k, x in enumerate(xs) if x.address == call)
    slot = next((x.address + x.size + int(re.search(r"\+ (0x[0-9a-f]+)\]", x.op_str).group(1), 16)
                 for x in xs[max(0, i - 6):i] if x.mnemonic == "mov" and x.op_str.startswith("rdx, qword ptr [rip")), None)
    add = any(x.op_str == "rdx, 0x190" and x.mnemonic == "add" for x in xs[max(0, i - 6):i])
    return slot, add, xs[i].op_str
a, b = caller(0x2BA040, 0x2BA0D8), caller(0x3CB440, 0x3CB4B1)
check("M1 both callers pass container + 0x190 from the container's own route slots",
      a == (0x209E5F0, True, "0x404060") and b == (0x2B47760, True, "0x404060"), "%s / %s" % (a, b))
L = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x404060, 187)}
check("M2 the loader stores four qword handles at rdx + 8 / + 0 / + 0x10 / + 0x18",
      L.get(0x40406A) == "mov rdi, rdx" and L.get(0x40409D) == "mov qword ptr [rdi + 8], rax" and L.get(0x4040CC) == "mov qword ptr [rdi], rax"
      and L.get(0x4040FA) == "mov qword ptr [rdi + 0x10], rax" and L.get(0x404111) == "mov qword ptr [rdi + 0x18], rax"
      and L.get(0x404093) == "call 0x2493d0" and L.get(0x404107) == "call 0x249320")
rows = []
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "MapScreenContainer": rows.append((int(c[1], 16), int(c[2]), c[3]))
g = {r[0]: r for r in rows}
check("M3 STORE REGRESSION: 8-byte rows at +0x198 and +0x1A8, no unobserved row in +0x190..+0x1AF",
      g.get(0x198, (0, 0))[1] == 8 and not g.get(0x198, (0, 0, "unobserved"))[2].startswith("unobserved") and g.get(0x1A8, (0, 0))[1] == 8
      and not [r for r in rows if 0x190 <= r[0] < 0x1B0 and r[2].lower().startswith("unobserved")],
      str([r for r in rows if 0x190 <= r[0] < 0x1B0]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
