"""widget_b8_rate.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Consumes
ASTRA-RETURN-OPUS-RATE-NORMALIZER-DOMAIN (_experiments/evidence/rate-normalizer-domain/).

Widget +0xB8 read '1.0f on every widget in the game'. That is the default, not an invariant:
  R1 00229E70 (37 B) is the shared rate normalizer: movss xmm1, [01E02820]; xorps xmm0; comiss xmm0, xmm1; jb -> return the
     rate; otherwise store [01CEBBA8] = 1.0f into 01E02820 and return 1.0. `jb` is taken when 0 < rate AND when the compare
     is unordered, so a positive fraction is kept (not floored at 1), any non-positive rate - negative, +0 or -0 - is
     reset (not only zero), and a NaN rate passes through unchanged
  R2 002468A0, when 00229DF0() != 0 and 00229EA0() == 2, stores 1.0f / 00229E70() at +0xB8 (002469C9 / 002469CE / 002469D6 /
     002469DA) over the 1.0f default (00246700, 0024699C)
  M  the model the row now states, against the two readings it replaces: floor-at-1 would keep 1.0 for a 0.5 rate and
     zero-only would keep -1.0; the byte-derived rule gives 0.5 -> +0xB8 2.0, -1.0 -> 1.0, NaN -> NaN
  L  LIMITS (2026-09-28, ASTRA-REQ-OPUS-RATE-COMPLETION-QUALIFIER): R1 and M hold for a COMPLETED comparison with masked FP
     exceptions. COMISS signals invalid for QNaN and SNaN; unmasked, the flags are not updated and continuation is unknown. DAZ
     makes a positive subnormal rate an effective zero (reset). The DIVSS result for special inputs depends on the FP state.
     M's values are a host model of ordinary masked cases, not FF12 bit-exact or native-exception evidence
  S  REGRESSION: the +0xB8 row no longer says '1.0f on every widget' unqualified, and it carries the limits (FAILS before)
Usage: python widget_b8_rate.py [--patch]
"""
import hashlib, math, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)) if m else None
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
r1 = (at(0x229E70)[0] == "movss" and at(0x229E70)[2] == 0x1E02820 and at(0x229E78)[:2] == ("xorps", "xmm0, xmm0")
      and at(0x229E7B)[:2] == ("comiss", "xmm0, xmm1") and at(0x229E7E)[:2] == ("jb", "0x229e91")
      and at(0x229E80)[2] == 0x1CEBBA8 and at(0x229E88)[2] == 0x1E02820 and at(0x229E88)[1].startswith("dword ptr")
      and at(0x229E91)[:2] == ("movaps", "xmm0, xmm1") and struct.unpack_from("<f", d, off(0x1CEBBA8))[0] == 1.0)
check("R1", r1, "00229E70: keep the rate when 0 < rate or unordered; else store and return 1.0")
r2 = (at(0x2469C9)[:2] == ("call", "0x229e70") and at(0x2469CE)[2] == 0x1CEBBA8 and at(0x2469D6)[:2] == ("divss", "xmm1, xmm0")
      and at(0x2469DA)[:2] == ("movss", "dword ptr [rbx + 0xb8], xmm1") and at(0x2469C4)[:2] == ("cmp", "eax, 2"))
check("R2", r2, "002468A0 stores 1.0 / 00229E70() at +0xB8 on the guarded arm")
def rate(r):          # the byte rule: comiss 0, r ; jb (CF=1: 0 < r or unordered) -> r ; else 1.0
    return r if (math.isnan(r) or 0.0 < r) else 1.0
floor1 = lambda r: max(r, 1.0); zero_only = lambda r: 1.0 if r == 0.0 else r
b8 = lambda f, r: 1.0 / f(r)
ok = (b8(rate, 0.5) == 2.0 and b8(rate, -1.0) == 1.0 and b8(rate, -0.0) == 1.0 and math.isnan(b8(rate, float("nan")))
      and b8(floor1, 0.5) != b8(rate, 0.5) and b8(zero_only, -1.0) != b8(rate, -1.0))
check("M", ok, "host model, masked ordinary cases: rate 0.5 -> +0xB8 2.0; -1.0 -> 1.0; -0.0 -> 1.0; NaN -> NaN (completed COMISS only); floor-at-1 and zero-only readings rejected")
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/widget-rate-b8/widget_b8_rate.py"
fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "Widget" and c[1] == "0x0B8" and c[5].startswith("1.0f on every widget in the game"):
            c[5] = ("~~1.0f on every widget in the game~~ 1.0f BY DEFAULT, not an invariant (qualified 2026-09-28, OPUS, %s; ASTRA "
                    "rate-normalizer-domain): 002468A0's guarded arm stores 1.0f / 00229E70(), and 00229E70 keeps the shared rate "
                    "01E02820 when it is positive (fractions included) or NaN, and resets it to 1.0 when it is zero or negative - so "
                    "+0xB8 is 1 / rate for a positive rate (2.0 for 0.5), 1.0 otherwise, NaN for a NaN rate. Actual game rates are "
                    "not established." % REC) + c[5][len("1.0f on every widget in the game"):]
            c[8] += " || QUALIFIED 2026-09-28 (OPUS, %s R1 R2 M)" % REC
            fl[i] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
row = next(cells(l) for l in fl if cells(l)[0] == "Widget" and cells(l)[1] == "0x0B8")
check("S", not row[5].startswith("1.0f on every widget in the game") and "COMPLETED comparison" in row[5] and "DAZ" in row[5]
      and "not established" in row[5], "the +0xB8 row states the default, the rate rule and its FP limits")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
