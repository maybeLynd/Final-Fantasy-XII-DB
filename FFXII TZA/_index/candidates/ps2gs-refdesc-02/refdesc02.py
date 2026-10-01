"""LegacyPs2GsReferenceDescriptor +0x02: a signed word read through the context's descriptor array (OPUS, 2026-09-27).
Control. Static.
  G1 003A6FC0 loads the array base from the context's +0x178 (003A6FF8) - the route's own pointer - and forms the
     element as index * 6 * 8 = index * 0x30, the element stride (003A6FF4 lea rcx, [rax + rax*2]; 003A7006 add rcx, rcx)
  G2 it reads word [base + index*0x30 + 2] sign-extended (003A7009) and scales it by 64 (003A7013 shl rax, 6)
  G3 STORE REGRESSION: +0x02 is a 2-byte row and no unobserved row covers it
Not claimed: what the value indexes (it is scaled by 64 and used as an offset; the target is not traced here).
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
I = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x3A6FC0):off(0x3A6FC0) + 0x80], 0x3A6FC0)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
check("G1 the base is the context's +0x178 array and the element stride is 0x30",
      I.get(0x3A6FF8) == "mov rax, qword ptr [rdx + 0x178]" and I.get(0x3A6FF4) == "lea rcx, [rax + rax*2]" and I.get(0x3A7006) == "add rcx, rcx")
check("G2 a sign-extended word at element +2, scaled by 64",
      I.get(0x3A7009) == "movsx rax, word ptr [rax + rcx*8 + 2]" and I.get(0x3A7013) == "shl rax, 6")
rows = []
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "LegacyPs2GsReferenceDescriptor": rows.append((int(c[1], 16), int(c[2]), c[3]))
check("G3 STORE REGRESSION: a 2-byte row at +0x02, not inside an unobserved row",
      any(r[0] == 2 and r[1] == 2 for r in rows) and not [r for r in rows if r[2].lower().startswith("unobserved") and r[0] <= 2 < r[0] + r[1]],
      str([r for r in rows if r[0] < 8]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
