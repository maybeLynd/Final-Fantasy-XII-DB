"""accumulation_order.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.

ASTRA's postmultiply-float-order ran the FIRST output of 003977B0 and found out[0][0] = f32(f32(f32(p1 + p0) + p2) + p3),
pk = f32(B[0][k] * A[k][0]), and asked that no whole-matrix rule be stated until the other output chains are read. This
reads all of them from the bytes:
  L  one loop body, run four times (r11d = 4 / add rax, 4 / sub r11, 1 / jne) - column j = 0..3; the snapshot column
     A[0..3][j] is loaded once per pass into xmm7 / xmm4 / xmm5 / xmm6
  R  each of the four rows i is: four separate mulss products A[k][j] * B[i][k] (B = rdx, row-major, B[i][k] at
     rdx + 0x10*i + 4*k), then three addss in the order (p0 + p1) or (p1 + p0), then + p2, then + p3, then one movss store
     to out + 0x10*i + 4*j. Rows 0 and 2 add p1 + p0 first, rows 1 and 3 p0 + p1 - bitwise the same sum (IEEE addition
     commutes; NaN payload selection aside)
  N  no fused multiply-add, no double-precision conversion, no horizontal or packed add in the body: every product and
     every partial sum is a separate binary32 operation
Whole-matrix rule (within ASTRA's stated MXCSR 1F80 / masked-nearest boundary):
  out[i][j] = f32(f32(f32(p0 + p1) + p2) + p3),  pk = f32(B[i][k] * A[k][j])
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
body = [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x3977B0):off(0x3977B0) + 349], 0x3977B0)]
at = {a: (m, o) for a, m, o in body}
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
check("L", at[0x39780A] == ("mov", "r11d, 4") and at[0x3978E0] == ("add", "rax, 4") and at[0x3978E4] == ("sub", "r11, 1")
      and at[0x3978E8] == ("jne", "0x397810"),
      "one column loop, four passes")
# symbolic evaluation of the loop body: registers hold ('A', k) snapshot values or product / sum expressions
loop = [(a, m, o) for a, m, o in body if 0x397810 <= a < 0x3978E0]
SNAP = {"r8 + rax - 0x20": 0, "r9 + rax - 0x20": 1, "r8 + rax": 2, "rax + r10": 3}
reg, stores = {}, {}
ok = True
for a, m, o in loop:
    dst, src = [s.strip() for s in o.split(",", 1)]
    if m == "movss" and dst.startswith("xmm"):
        k = SNAP[src.split("[")[1].rstrip("]")]; reg[dst] = ("A", k)
    elif m == "movaps":
        reg[dst] = reg[src]
    elif m == "mulss":
        disp = src.split("[")[1].rstrip("]").replace("rdx", "").replace("+", "").strip() or "0"
        e = int(disp, 16); i, kk = e // 16, (e % 16) // 4
        ok &= reg[dst][0] == "A" and reg[dst][1] == kk
        reg[dst] = ("P", i, kk)
    elif m == "addss":
        reg[dst] = ("S", reg[dst], reg[src])
    elif m == "movss":
        disp = {"rax - 0x20": 0, "rax - 0x10": 1, "rax": 2, "rax + 0x10": 3}[dst.split("[")[1].rstrip("]")]
        stores[disp] = reg[src]
    else:
        ok = False
def canon(e):
    if e[0] == "P": return ("P", e[1], e[2])
    l, r = canon(e[1]), canon(e[2])
    return ("S",) + tuple(sorted([l, r])) if (l[0] == "P" and r[0] == "P") else ("S", l, r)
want = lambda i: ("S", ("S", ("S", ("P", i, 0), ("P", i, 1)), ("P", i, 2)), ("P", i, 3))
got = {i: canon(stores.get(i, ("P", -1, -1))) for i in range(4)}
raw_first = {i: (stores[i][1][1][1][2], stores[i][1][1][2][2]) for i in range(4)}
check("R", ok and all(got[i] == want(i) for i in range(4)),
      "each row i: products A[k][j]*B[i][k] summed ((p0+p1)+p2)+p3; first pair order per row %s" % raw_first)
bad = [(hex(a), m) for a, m, o in body if m.startswith(("vfmadd", "vfmsub", "cvtss2sd", "cvtsd2ss", "haddps", "addps", "mulps", "dpps"))]
check("N", not bad, "no fused, widened, horizontal or packed arithmetic in the body: %s" % bad)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
