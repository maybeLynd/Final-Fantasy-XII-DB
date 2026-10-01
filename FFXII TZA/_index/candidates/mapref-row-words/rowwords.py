"""MapRefFieldRow +0x04 / +0x06: two uint16 words read through the row's own route (OPUS, 2026-09-27). Control. Static.
  R1 ROUTE PROOF: 00264ED0 and 00264F90 load the header from the slot 02099D88 - the same slot the route's own site
     0026D910 (0026D998) loads - and form the row as header + *(int32*)(header + 4) + id * 8, the route's RELOFF
     array with stride 8
  R2 00264ED0 reads word [row + 4] and 00264F90 word [row + 6] (movzx); 0026DB30 forms the row the same way and reads
     word [row + 6] (0026DBB2)
  R3 STORE REGRESSION: +0x04 and +0x06 are 2-byte rows and no unobserved row covers them
Not claimed: what the words mean (the shipped image holds 0x0000 / 0x0001 in row 0 and 0x0001 / 0x0001 in row 1).
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
def slot(xs, upto):
    s = None
    for x in xs:
        if x.address > upto: break
        m = re.match(r"r\w+, qword ptr \[rip \+ (0x[0-9a-f]+)\]$", x.op_str)
        if x.mnemonic == "mov" and m: s = x.address + x.size + int(m.group(1), 16)
    return s
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
A, B, R = D(0x264ED0, 49), D(0x264F90, 49), D(0x26D910, 0xA0)
IA = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in A}; IB = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in B}
check("R1 both getters form the row from the route's header slot and RELOFF array (stride 8)",
      slot(A, 0x264EE9) == slot(B, 0x264FA9) == slot(R, 0x26D998) == 0x2099D88
      and IA.get(0x264EE9) == "movsxd rcx, dword ptr [r8 + 4]" and IA.get(0x264EED) == "add rcx, r8" and IA.get(0x264EF0) == "lea rax, [rcx + rdx*8]"
      and IB.get(0x264FA9) == "movsxd rcx, dword ptr [r8 + 4]" and IB.get(0x264FB0) == "lea rax, [rcx + rdx*8]")
C = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x26DB30, 0xA0)}
check("R2 word reads at row + 4 and row + 6",
      IA.get(0x264EF9) == "movzx eax, word ptr [rax + 4]" and IB.get(0x264FB9) == "movzx eax, word ptr [rax + 6]"
      and C.get(0x26DBA9) == "lea rax, [rcx + rdx*8]" and C.get(0x26DBB2) == "movzx edi, word ptr [rax + 6]")
rows = []
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "MapRefFieldRow": rows.append((int(c[1], 16), int(c[2]), c[3]))
check("R3 STORE REGRESSION: 2-byte rows at +0x04 and +0x06, not inside an unobserved row",
      all(any(r[0] == o and r[1] == 2 for r in rows) for o in (4, 6))
      and not [r for r in rows if r[2].lower().startswith("unobserved") and r[0] <= 4 < r[0] + r[1]], str(rows))
print("FAILS", fails)
sys.exit(1 if fails else 0)
