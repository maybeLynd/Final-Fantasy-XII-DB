"""comparator.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only; nothing executed.
For ASTRA-REQ-OPUS-SCRIPT-COMPARISON-UNORDERED (_experiments/evidence/script-comparison-unordered/). Written without
ASTRA's code. The float path of the ScriptVM comparator 0025D740 and its six consumers, read from the bytes, and a small
executable specification that keeps the unordered result.

  S  THE COMPARATOR: edi = 1 at entry (0025D74F); the first pop (the right operand, top of stack) goes to xmm7 and the second
     (the left) to xmm6. ucomiss xmm6, xmm7 (0025D8B2); jp (0025D8B5) skips the equality test; jne; equal -> xor eax, eax,
     return 0. Otherwise or eax, -1; comiss xmm7, xmm6 (0025D8D3); cmova edi, eax (0025D8D6); return edi. cmova needs CF = 0
     and ZF = 0, which an unordered comiss never gives, so ANY NaN returns +1; ordered: right > left -> -1, else +1
  K  THE CONSUMERS: OPEQ .. OPLSE (0025EA18 .. 0025EA90) each call 0025D740, test eax, eax and set cl with sete / setne / setg
     / sets / setns / setle
  M  THE SPECIFICATION (model below): 1 vs 2 -> -1, 1 vs 1 -> 0, 2 vs 1 -> +1; NaN on the left, right or both -> +1; so with
     a NaN, EQ 0, NE 1, GT 1, LS 0, GTE 1, LSE 0 - not the host's IEEE operators (NaN > x, NaN >= x and NaN != x would differ
     from EQ/GT/GTE here: host gives GT False and GTE False)
  I  THE INTEGER FAST PATH (for ASTRA-REQ-OPUS-SCRIPT-COMPARISON-MIXED): only when depth >= 2 (0025D754 cmp edx, 2 / jge) and
     both tags are equal and 1 (0025D7B8 / 0025D7BD); the top pops to ebp, the lower to esi, then cmp esi, ebp - equal 0,
     else cmovl edi, -1: a SIGNED integer compare, lower < top -> -1, else +1. No conversion
  X  EVERY OTHER TAG PAIR takes the float path: an int operand is converted with cvtdq2ps (top 0025D869, lower 0025D8A6), a
     float is copied (movss 0025D793 / 0025D892), then S applies. So a mixed compare rounds the int by the thread's MXCSR RC
  P  PRECISION (conditional arithmetic, not execution): int 16777217 vs int 16777216 -> +1 under any RC (fast path); int
     16777217 (lower) vs float 16777216 (top) -> 0 under nearest-even, +1 under round-up; reversed -> 0 and -1; int 123 vs
     int 124 -> -1. Rejected models: all-float (the both-int case would give 0 under nearest-even), always-nearest (the
     mixed case under round-up would give 0), reversed operand order (16777217 vs 16777216 would give -1)
Not claimed: native flags or unmasked exceptions, the game's MXCSR, bad tags, underflow, authored values, which scripts
compare NaNs or mixed operands, or reachability.
Usage: python comparator.py
"""
import hashlib, math, os, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x25D740):off(0x25D8DD)], 0x25D740)}
check("S", A.get(0x25D74F) == ("mov", "edi, 1") and A.get(0x25D793) == ("movss", "xmm7, dword ptr [rbx + rdx*4 + 0x184]")
      and A.get(0x25D892) == ("movss", "xmm6, dword ptr [rbx + rdx*4 + 0x184]") and A.get(0x25D8B2) == ("ucomiss", "xmm6, xmm7")
      and A.get(0x25D8B5) == ("jp", "0x25d8d0") and A.get(0x25D8B7) == ("jne", "0x25d8d0") and A.get(0x25D8B9) == ("xor", "eax, eax")
      and A.get(0x25D8D0) == ("or", "eax, 0xffffffff") and A.get(0x25D8D3) == ("comiss", "xmm7, xmm6") and A.get(0x25D8D6) == ("cmova", "edi, eax")
      and A.get(0x25D8D9) == ("mov", "eax, edi"),
      "edi = 1; xmm7 = first pop (right), xmm6 = second (left); ucomiss / jp / jne -> 0; else comiss xmm7, xmm6 / cmova edi, -1")
SET = ["sete", "setne", "setg", "sets", "setns", "setle"]
kok = []
for j, base in enumerate(range(0x25EA18, 0x25EAA8, 0x18)):
    K = [(x.mnemonic, x.op_str) for x in cs.disasm(d[off(base):off(base + 0x18)], base)]
    kok.append(K[:5] == [("mov", "rcx, r10"), ("call", "0x25d740"), ("xor", "r11d, r11d"), ("test", "eax, eax"), ("mov", "ecx, r11d")] and K[5] == (SET[j], "cl"))
check("K", all(kok), "OPEQ..OPLSE: call 0025D740, test eax, eax, then %s cl" % " / ".join(SET))
def cmp(left, right):                       # 0025D740's float path, as read in S
    if not (math.isnan(left) or math.isnan(right)) and left == right: return 0
    ordered_above = not (math.isnan(left) or math.isnan(right)) and right > left      # comiss xmm7, xmm6: CF = 0 and ZF = 0
    return -1 if ordered_above else 1
def ops(r): return {"EQ": int(r == 0), "NE": int(r != 0), "GT": int(r > 0), "LS": int(r < 0), "GTE": int(r >= 0), "LSE": int(r <= 0)}
nan = float("nan")
fin = (cmp(1.0, 2.0), cmp(1.0, 1.0), cmp(2.0, 1.0))
nans = (cmp(nan, 1.0), cmp(1.0, nan), cmp(nan, nan))
host = {"GT": int(nan > 1.0), "GTE": int(nan >= 1.0)}
check("M", fin == (-1, 0, 1) and nans == (1, 1, 1) and ops(1) == {"EQ": 0, "NE": 1, "GT": 1, "LS": 0, "GTE": 1, "LSE": 0} and host == {"GT": 0, "GTE": 0},
      "finite %s, NaN left/right/both %s; NaN decisions %s; the host's NaN > x and NaN >= x give %s" % (fin, nans, ops(1), host))
A2 = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x25D740):off(0x25D8B2)], 0x25D740)}
check("I", A2.get(0x25D754) == ("cmp", "edx, 2") and A2.get(0x25D757) == ("jge", "0x25d7a1") and A2.get(0x25D7B8) == ("cmp", "r8d, eax")
      and A2.get(0x25D7BB) == ("jne", "0x25d760") and A2.get(0x25D7BD) == ("cmp", "r8d, edi") and A2.get(0x25D7C0) == ("jne", "0x25d760")
      and A2.get(0x25D81E) == ("mov", "ebp, dword ptr [rbx + rdx*4 + 0x184]") and A2.get(0x25D832) == ("mov", "esi, dword ptr [rbx + rdx*4 + 0x184]")
      and A2.get(0x25D839) == ("cmp", "esi, ebp") and A2.get(0x25D83D) == ("xor", "eax, eax") and A2.get(0x25D857) == ("cmp", "esi, ebp")
      and A2.get(0x25D859) == ("cmovl", "edi, eax"),
      "depth >= 2 and both tags 1: top -> ebp, lower -> esi, signed cmp esi, ebp; equal 0, cmovl -1 when lower < top, else +1")
check("X", A2.get(0x25D860) == ("movd", "xmm7, dword ptr [rbx + rdx*4 + 0x184]") and A2.get(0x25D869) == ("cvtdq2ps", "xmm7, xmm7")
      and A2.get(0x25D89D) == ("movd", "xmm6, dword ptr [rbx + rdx*4 + 0x184]") and A2.get(0x25D8A6) == ("cvtdq2ps", "xmm6, xmm6")
      and A2.get(0x25D793) == ("movss", "xmm7, dword ptr [rbx + rdx*4 + 0x184]") and A2.get(0x25D892) == ("movss", "xmm6, dword ptr [rbx + rdx*4 + 0x184]")
      and A2.get(0x25D7BB)[1] == "0x25d760" and A2.get(0x25D7C0)[1] == "0x25d760",
      "any other tag pair: int operands cvtdq2ps (top 0025D869, lower 0025D8A6), floats movss, then the float compare")
import struct
def f32(v, ru):                                         # cvtdq2ps of an int under RN or RU (sign-aware), as a Python float
    lo = struct.unpack("<I", struct.pack("<f", float(v)))[0]; x = struct.unpack("<f", struct.pack("<I", lo))[0]
    if ru and x < v: lo = lo - 1 if lo & 0x80000000 else lo + 1
    return struct.unpack("<f", struct.pack("<I", lo))[0]
def compare(lower, top, ru):                            # (value, tag) pairs; tag 1 int, 2 float
    if lower[1] == top[1] == 1: return 0 if lower[0] == top[0] else (-1 if lower[0] < top[0] else 1)
    l = f32(lower[0], ru) if lower[1] == 1 else lower[0]; t = f32(top[0], ru) if top[1] == 1 else top[0]
    return cmp(l, t)
def all_float(lower, top, ru): return cmp(f32(lower[0], ru) if lower[1] == 1 else lower[0], f32(top[0], ru) if top[1] == 1 else top[0])
def always_nearest(lower, top, ru): return compare(lower, top, False)
def reversed_order(lower, top, ru): return compare(top, lower, ru)
C = [(((16777217, 1), (16777216, 1)), (1, 1)), (((16777217, 1), (16777216.0, 2)), (0, 1)), (((16777216.0, 2), (16777217, 1)), (0, -1)), (((123, 1), (124, 1)), (-1, -1))]
got = [(compare(a, b, False), compare(a, b, True)) for (a, b), _ in C]
check("P", got == [v for _, v in C] and all_float((16777217, 1), (16777216, 1), False) == 0 and always_nearest((16777217, 1), (16777216.0, 2), True) == 0
      and reversed_order((16777217, 1), (16777216, 1), False) == -1,
      "(RN, RU): both-int 16777217/16777216 %s, mixed %s, reversed %s, 123/124 %s; all-float, always-nearest and reversed-order models rejected" % tuple(got))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
