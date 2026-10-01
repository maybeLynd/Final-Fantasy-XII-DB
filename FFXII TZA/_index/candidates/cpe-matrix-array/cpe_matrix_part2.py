"""cpe_matrix_part2.py - OPUS (Claude Opus 5.5), 2026-09-28. Part 2 of cpe-matrix-array (part 1: cpe_matrix_array.py,
f4538d11a, under review and left unchanged). STATIC, certified EXE only.

  P1 a seventh 4x4 float matrix at CPostEffect +0x92C: 0070AED0(this, nine floats) stores the 3x3 linear part COLUMN BY
     COLUMN from its arguments (xmm1 / xmm2 / xmm3 -> +0x92C / +0x93C / +0x94C, the stack floats -> columns 1 and 2),
     zeroes column 3 and row 3 (dwords +0x938 / +0x948, qwords +0x958 / +0x960) and stores 1.0f at +0x968 (row 3 col 3)
  P2 006FE7F0 reads it as four 16-byte rows (movups +0x92C / +0x93C / +0x94C / +0x95C into xmm8..xmm11)
  P3 the per-matrix bytes act as enables in 006FE7F0: a zero byte at +0x924 replaces matrix 0's address (+0x7A4) with
     null (cmp byte / jne / mov r14, rsi); a non-zero byte at +0x925 selects matrix 1's address (+0x7E4)
  S  REGRESSION: the store has +0x92C float[4][4] (64) and nothing starting inside it; the old 16-byte mixed968 tail is
     split at +0x96C (FAILS before the patch)
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
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
W = {0x70AED8: "dword ptr [rcx + 0x92c], xmm1", 0x70AF26: "dword ptr [rcx + 0x93c], xmm2", 0x70AF2E: "dword ptr [rcx + 0x94c], xmm3",
     0x70AEF4: "dword ptr [rcx + 0x930], xmm0", 0x70AF10: "dword ptr [rcx + 0x940], xmm0", 0x70AF36: "dword ptr [rcx + 0x950], xmm0",
     0x70AEE6: "dword ptr [rcx + 0x934], xmm1", 0x70AF02: "dword ptr [rcx + 0x944], xmm1", 0x70AF1E: "dword ptr [rcx + 0x954], xmm1"}
p1 = (all(at(a) == ("movss", o) for a, o in W.items())
      and at(0x70AF4B) == ("mov", "dword ptr [rcx + 0x938], eax") and at(0x70AF45) == ("mov", "dword ptr [rcx + 0x948], eax")
      and at(0x70AF3E) == ("mov", "qword ptr [rcx + 0x958], rax") and at(0x70AF51) == ("mov", "qword ptr [rcx + 0x960], rax")
      and at(0x70AED6) == ("xor", "eax, eax") and at(0x70AF58) == ("mov", "dword ptr [rcx + 0x968], 0x3f800000"))
check("P1", p1, "0070AED0: 3x3 linear part column by column, column 3 / row 3 zeroed, 1.0f at +0x968")
p2 = all(at(a) == ("movups", o) for a, o in ((0x6FE9E5, "xmm8, xmmword ptr [rdi + 0x92c]"), (0x6FE9F3, "xmm9, xmmword ptr [rdi + 0x93c]"),
                                           (0x6FE9FB, "xmm10, xmmword ptr [rdi + 0x94c]"), (0x6FEA03, "xmm11, xmmword ptr [rdi + 0x95c]")))
check("P2", p2, "006FE7F0 reads the matrix as four 16-byte rows")
p3 = (at(0x6FE97D) == ("lea", "r14, [rdi + 0x7a4]") and at(0x6FE984) == ("cmp", "byte ptr [rdi + 0x924], sil")
      and at(0x6FE98B) == ("jne", "0x6fe990") and at(0x6FE98D) == ("mov", "r14, rsi")
      and at(0x6FE990) == ("cmp", "byte ptr [rdi + 0x925], sil") and at(0x6FE997) == ("je", "0x6fe9a0")
      and at(0x6FE999) == ("lea", "rsi, [rdi + 0x7e4]"))
check("P3", p3, "006FE7F0: a zero enable byte replaces the matrix address with null; non-zero passes it")
F = [l.split("\t") for l in open(os.path.join(ROOT, "FFXII TZA", "_types", "fields.tsv"), encoding="utf-8").read().replace("\r\n", "\n").splitlines()]
cpe = {int(r[1], 16): r for r in F if r[0] == "CPostEffect"}
s = (cpe.get(0x92C, [0, 0, "0"])[2] == "64" and cpe.get(0x92C)[4] == "float[4][4]"
     and not [o for o in cpe if 0x92C < o < 0x96C] and 0x96C in cpe)
check("S", s, "the store has +0x92C float[4][4] and the old mixed968 tail split at +0x96C")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
