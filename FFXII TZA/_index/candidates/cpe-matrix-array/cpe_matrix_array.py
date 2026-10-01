"""cpe_matrix_array.py - OPUS (Claude Opus 5.5), 2026-09-28. CPostEffect +0x7A4..+0x929 is SIX 4x4 float matrices and
one byte per matrix - not the 45 u64 / uint32 / 'mixed' rows the census re-cut left there. STATIC, certified EXE only.

  R1 the reset 0070FF10(this, index): index == -2 loops rcx = 0..5 (cmp rcx, 6 / jl), advancing 0x40 per matrix; each
     pass zero-fills six qwords and stores 1.0f (0x3F800000) at the four diagonal cells, i.e. relative to the matrix at
     +0x7A4 + 0x40*i: +0x00, +0x14, +0x28, +0x3C; then clears byte +0x924 + i.  Any other index resets that one matrix
     (shl rax, 6) and its byte the same way.
  R2 006FB810 moves matrices 0 and 1 by 16-byte rows (movups reads at +0x7A4/+0x7B4/+0x7C4/+0x7D4 and +0x7E4..+0x814,
     identity stores, movups writes back): the 4x4 row structure, from a second, independent body.
  R3 the per-matrix bytes are read one at a time (cmp byte ptr [.. + 0x924..0x927]) at 006FE984 / 006FE990 / 006F723B /
     006F724E.
  N  the zero-filled qwords straddle float cells (e.g. +0x7B0 covers row 0 col 3 and row 1 col 0), so an 8-byte field
     there is a fill artefact; and the census's 4-byte hits from 007145E0 are a 64-byte dword-wise matrix assignment
     whose callers pass matrix-aligned destinations (+0x5D4 in the +0x210 sub-object = +0x7E4).
  S  REGRESSION: the store has +0x7A0 float (4), +0x7A4 float[6][4][4] (384), +0x924 u8[6] (6), and no row starts
     strictly inside (+0x7A4, +0x92A) (FAILS before the patch).
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(a, sz): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + sz], a)]
def has(b, mn, op): return any(m == mn and o == op for _, m, o in b)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

R = body(0x70FF10, 226)
loop_diag = [o for a, m, o in R if 0x70FF30 <= a < 0x70FF63 and "0x3f800000" in o]
loop_zero = [o for a, m, o in R if 0x70FF30 <= a < 0x70FF63 and o.startswith("qword ptr [rax") and o.endswith("rdx")]
one_diag = [o for a, m, o in R if a >= 0x70FF7B and "0x3f800000" in o]
r1 = (has(R, "cmp", "edx, -2") and has(R, "lea", "rax, [r8 + 0x7d8]") and has(R, "lea", "rax, [rax + 0x40]")
      and has(R, "cmp", "rcx, 6") and has(R, "mov", "byte ptr [r8 + rcx + 0x924], dl") and has(R, "shl", "rax, 6")
      and has(R, "mov", "byte ptr [rcx + r8 + 0x924], dl")
      # loop base rax = +0x7D8: diagonal at +0x7E0/+0x7CC/+0x7B8/+0x7A4 = matrix+0x3C/+0x28/+0x14/+0x00
      and loop_diag == ["dword ptr [rax + 8], 0x3f800000", "dword ptr [rax - 0xc], 0x3f800000",
                        "dword ptr [rax - 0x20], 0x3f800000", "dword ptr [rax - 0x34], 0x3f800000"]
      and len(loop_zero) == 6
      and one_diag == ["dword ptr [rax + r8 + 0x7e0], 0x3f800000", "dword ptr [rax + r8 + 0x7cc], 0x3f800000",
                       "dword ptr [rax + r8 + 0x7b8], 0x3f800000", "dword ptr [rax + r8 + 0x7a4], 0x3f800000"])
check("R1", r1, "0070FF10: six matrices at +0x7A4 stride 0x40 reset to identity (diagonal +0x00/+0x14/+0x28/+0x3C), byte +0x924+i cleared")
C = body(0x6FB810, 2365)
rows = ["0x7a4", "0x7b4", "0x7c4", "0x7d4", "0x7e4", "0x7f4", "0x804", "0x814"]
r2 = all(any(m == "movups" and o.endswith("xmmword ptr [rdi + %s]" % r) for _, m, o in C) for r in rows) and \
     all(any(m == "movups" and o.startswith("xmmword ptr [rdi + %s]" % r) for _, m, o in C) for r in rows) and \
     all(has(C, "mov", "dword ptr [rdi + %s], 0x3f800000" % r) for r in ("0x7a4", "0x7b8", "0x7cc", "0x7e0", "0x7e4", "0x7f8", "0x80c", "0x820"))
check("R2", r2, "006FB810: matrices 0 and 1 moved as 16-byte rows (8 movups reads, 8 writes) with identity diagonals")
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
r3 = (at(0x6FE984)[1].startswith("byte ptr [rdi + 0x924]") and at(0x6FE990)[1].startswith("byte ptr [rdi + 0x925]")
      and at(0x6F723B)[1].startswith("byte ptr [rbx + 0x926]") and at(0x6F724E)[1].startswith("byte ptr [rbx + 0x927]")
      and all(at(a)[0] == "cmp" for a in (0x6FE984, 0x6FE990, 0x6F723B, 0x6F724E)))
check("R3", r3, "the per-matrix bytes are compared one at a time (006FE984 / 006FE990 / 006F723B / 006F724E)")
A = body(0x7145E0, 100)
callers = {0x706F7D: "rcx, 0x5d4", 0x70723D: "rcx, 0x654", 0x70A835: "rcx, 0xb38"}
n_ok = (has(A, "mov", "r9d, 2") and has(A, "lea", "r8, [r8 + 0x20]") and sum(1 for _, m, o in A if m == "mov" and o.startswith("dword ptr [r8")) == 8
        and all(at(a) == ("add", op) for a, op in callers.items()))
check("N", n_ok, "007145E0 copies 64 bytes as 16 dwords; its callers pass +0x5D4 / +0x654 / +0xB38 in their own objects")
F = [l.split("\t") for l in open(os.path.join(ROOT, "FFXII TZA", "_types", "fields.tsv"), encoding="utf-8").read().replace("\r\n", "\n").splitlines()]
cpe = {int(r[1], 16): r for r in F if r[0] == "CPostEffect"}
s = (cpe.get(0x7A0, [0, 0, "0"])[2] == "4" and cpe.get(0x7A0)[4] == "float"
     and cpe.get(0x7A4, [0, 0, "0"])[2] == "384" and cpe.get(0x7A4)[4] == "float[6][4][4]"
     and cpe.get(0x924, [0, 0, "0"])[2] == "6" and cpe.get(0x924)[4] == "u8[6]"
     and not [o for o in cpe if 0x7A4 < o < 0x924] and not [o for o in cpe if 0x924 < o < 0x92A])
check("S", s, "the store carries the matrix array and the byte array, and nothing inside them")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
