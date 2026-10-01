"""WidgetSingleton02B457E0: +0x120..+0x26F is two 0xA8-byte records, not a 336-byte unobserved span (OPUS, 2026-09-27).
Control. Static.
  R1 the teardown 003C2210 walks two records from this + 0x120 (rbp = 2, add rdi, 0xA8): for each it releases every
     slot of the qword array at +0x18 (count byte +0x13) through 0024A680 and nulls it, zeroes the count, then releases
     the +0x00 handle through 003697F0 and nulls it
  R2 the layout closes: 0x120 + 2 * 0xA8 = 0x270, and the next declared row starts there
  R3 STORE REGRESSION: +0x120 is WidgetSingleton02B457E0Record[2] and no row starts inside it
Not claimed: what +0x08, +0x10, +0x12 hold; that the slot array is bounded by 18 anywhere but the layout
((0xA8 - 0x18) / 8); what the slots and the handle name.
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
I = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x3C2210):off(0x3C2210) + 156], 0x3C2210)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
check("R1 two 0xA8 records from +0x120: slot array +0x18 (count +0x13) released via 0024A680, handle +0x00 via 003697F0",
      I.get(0x3C222A) == "lea rdi, [rcx + 0x120]" and I.get(0x3C2231) == "mov ebp, 2" and I.get(0x3C2243) == "cmp byte ptr [rdi + 0x13], sil"
      and I.get(0x3C2249) == "lea rbx, [rdi + 0x18]" and I.get(0x3C2250) == "mov rcx, qword ptr [rbx]" and I.get(0x3C225A) == "call 0x24a680"
      and I.get(0x3C225F) == "mov qword ptr [rbx], r14" and I.get(0x3C2268) == "add rbx, 8" and I.get(0x3C2273) == "mov byte ptr [rdi + 0x13], r14b"
      and I.get(0x3C2270) == "mov rcx, qword ptr [rdi]" and I.get(0x3C227C) == "call 0x3697f0" and I.get(0x3C2281) == "mov qword ptr [rdi], r14"
      and I.get(0x3C2284) == "add rdi, 0xa8" and I.get(0x3C228B) == "sub rbp, 1")
rows = []
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "WidgetSingleton02B457E0": rows.append((int(c[1], 16), int(c[2]), c[3], c[4]))
nxt = min((r[0] for r in rows if r[0] >= 0x270), default=None)
check("R2 the layout closes at +0x270", 0x120 + 2 * 0xA8 == 0x270 and nxt == 0x270, hex(nxt or 0))
inside = [r[2] for r in rows if 0x120 < r[0] < 0x270]
check("R3 STORE REGRESSION: +0x120 is WidgetSingleton02B457E0Record[2], nothing starts inside it",
      any(r[0] == 0x120 and r[3] == "WidgetSingleton02B457E0Record[2]" for r in rows) and not inside, str(inside))
print("FAILS", fails)
sys.exit(1 if fails else 0)
