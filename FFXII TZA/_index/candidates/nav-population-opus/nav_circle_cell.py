"""nav_circle_cell.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only; no emulator, no native execution.
Independent derivation for ASTRA-REQ-OPUS-NAV-CIRCLE-CELL (_experiments/evidence/nav-circle-cell-boundary/) and
ASTRA-REQ-OPUS-MULSS-STATUS-LIMIT (_experiments/evidence/original-mulss-status-control/), written without ASTRA's code.

  D  004690B0 decoded (67 instructions, 237 B, no calls, no stores). With RCX = a rectangle {+0 minA, +8 minB, +0x10 maxA,
     +0x18 maxB} and RDX = a circle {+0 A, +8 B, +0x10 r}:
       band 1  A >= minA - r, B >= minB, r + maxA >= A, maxB >= B       (each `comiss / jb` - equality passes) -> 1
       band 2  A >= minA, B >= minB - r, maxA >= A, r + maxB >= B       (the last `jae` returns 1)            -> 1
       corners r*r > (minB - B)^2 + (minA - A)^2, then (maxB - B)^2 + (minA - A)^2, then (minB - B)^2 + (maxA - A)^2
               (each `ja`, strict), then r*r > (maxB - B)^2 + (maxA - A)^2 by `seta` (strict)                -> 1 / 0
     `comiss` sets CF on an unordered compare, so any NaN operand fails the band tests; the corner `ja` / `seta` are also
     false on unordered. The corner tests are not quadrant-selected: any corner strictly inside the disk returns 1
  F  a float32 model of that exact operation order (each ADDSS / SUBSS / MULSS rounded to binary32; double arithmetic then
     one rounding is exact for these operations) on ASTRA's ten cases with rectangle 0..10, radius 5: inside 1, far outside 0,
     edge tangency (-5, 5) 1, the four 3-4-5 corner tangencies 0, radius 0x40A00001 at the first corner 1 (r*r rounds to
     0x41C80003), radius 0x409FFFFF 0 (0x41C7FFFE); a `ja -> jae` mutant of the first corner test gives 1 on the exact tangency
  X  for the MULSS status request: 0x40A00001 * 0x40A00001 is not representable in binary32 (the exact rational product
     differs from its rounding), so IEEE 754 requires the inexact status (MXCSR PE, 0x20: 1F80 -> 1FA0 native); 5.0 * 5.0 is
     exact (no status). An emulator that leaves MXCSR at 1F80 after the first product omits a status the standard requires -
     the output bits are unaffected, the status is not evidence of native absence
  S  REGRESSION (FAILS before): NavGridParams cellBitsetArray carries the predicate rule
Usage: python nav_circle_cell.py [--patch]
"""
import hashlib, os, struct, sys
from fractions import Fraction
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
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
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
L = list(cs.disasm(d[off(0x4690B0):off(0x4690B0) + 237], 0x4690B0))
A = {x.address: (x.mnemonic, x.op_str) for x in L}
KEY = [(0x4690C0, ("subss", "xmm0, xmm2")), (0x4690C4, ("comiss", "xmm4, xmm0")), (0x4690C7, ("jb", "0x4690f1")), (0x4690CE, ("comiss", "xmm1, dword ptr [rcx + 8]")),
       (0x4690D7, ("addss", "xmm0, dword ptr [rcx + 0x10]")), (0x4690DC, ("comiss", "xmm0, xmm4")), (0x4690E6, ("comiss", "xmm0, xmm1")), (0x4690EB, ("mov", "eax, 1")),
       (0x4690F1, ("comiss", "xmm4, xmm3")), (0x469100, ("subss", "xmm0, xmm2")), (0x469104, ("comiss", "xmm1, xmm0")), (0x46910E, ("comiss", "xmm0, xmm4")),
       (0x469116, ("addss", "xmm0, dword ptr [rcx + 0x18]")), (0x46911B, ("comiss", "xmm0, xmm1")), (0x46911E, ("jae", "0x4690eb")),
       (0x469125, ("subss", "xmm3, xmm4")), (0x469129, ("subss", "xmm5, dword ptr [rdx + 8]")), (0x46912E, ("mulss", "xmm2, xmm2")), (0x469140, ("addss", "xmm1, xmm0")),
       (0x469144, ("comiss", "xmm2, xmm1")), (0x469147, ("ja", "0x4690eb")), (0x46914E, ("subss", "xmm1, dword ptr [rdx + 8]")), (0x46915E, ("addss", "xmm0, xmm3")),
       (0x469165, ("ja", "0x4690eb")), (0x46916C, ("subss", "xmm3, xmm4")), (0x46917B, ("addss", "xmm5, xmm0")), (0x469182, ("ja", "0x4690eb")),
       (0x469192, ("addss", "xmm1, xmm3")), (0x469196, ("comiss", "xmm2, xmm1")), (0x469199, ("seta", "al")), (0x46919C, ("ret", ""))]
writes = [x for x in L if x.op_str.startswith(("dword ptr", "qword ptr", "byte ptr", "word ptr")) and x.mnemonic in ("mov", "movss", "movups", "movaps")]
check("D", len(L) == 67 and all(A.get(a) == v for a, v in KEY) and not writes and not any(x.mnemonic == "call" for x in L),
      "004690B0: two inclusive bands (comiss / jb, jae) then four strict corner tests (ja x3, seta); no calls, no stores")
f32 = lambda x: struct.unpack("<f", struct.pack("<f", x))[0]
fb = lambda u: struct.unpack("<f", struct.pack("<I", u))[0]
bits = lambda x: struct.unpack("<I", struct.pack("<f", x))[0]
def model(rect, circ, strict=True):
    minA, minB, maxA, maxB = map(f32, rect); a, b, r = map(f32, circ)
    if a >= f32(minA - r) and b >= minB and f32(r + maxA) >= a and maxB >= b: return 1
    if a >= minA and b >= f32(minB - r) and maxA >= a and f32(r + maxB) >= b: return 1
    dA0, dB0, rr = f32(minA - a), f32(minB - b), f32(r * r)
    gt = (lambda x, y: x > y) if strict else (lambda x, y: x >= y)
    if gt(rr, f32(f32(dB0 * dB0) + f32(dA0 * dA0))): return 1
    dB1 = f32(maxB - b)
    if rr > f32(f32(dB1 * dB1) + f32(dA0 * dA0)): return 1
    dA1 = f32(maxA - a)
    if rr > f32(f32(dB0 * dB0) + f32(dA1 * dA1)): return 1
    return int(rr > f32(f32(dB1 * dB1) + f32(dA1 * dA1)))
R = (0.0, 0.0, 10.0, 10.0)
cases = [((5, 5, 5), 1), ((-6, 5, 5), 0), ((-5, 5, 5), 1), ((-3, -4, 5), 0), ((-3, 14, 5), 0), ((13, -4, 5), 0), ((13, 14, 5), 0),
         ((-3, -4, fb(0x40A00001)), 1), ((-3, -4, fb(0x409FFFFF)), 0)]
got = [model(R, c) for c, _ in cases]
mut = model(R, (-3, -4, 5), strict=False)
check("F", got == [e for _, e in cases] and mut == 1 and bits(f32(fb(0x40A00001) ** 2)) == 0x41C80003 and bits(f32(fb(0x409FFFFF) ** 2)) == 0x41C7FFFE,
      "ASTRA's ten cases reproduced by an independent float32 model: %s; r^2 bits 41C80003 / 41C7FFFE; the ja->jae mutant accepts the exact tangency" % got)
exact = lambda u: Fraction(fb(u))
p1 = exact(0x40A00001) * exact(0x40A00001); p0 = exact(0x40A00000) * exact(0x40A00000)
check("X", p1 != Fraction(f32(float(p1))) and p0 == Fraction(f32(float(p0))),
      "0x40A00001 squared is inexact in binary32 (IEEE inexact status required: native 1FA0); 5.0 squared is exact (no status)")
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/nav-population-opus/nav_circle_cell.py"
ADD = (" || THE OVERLAP TEST 2026-09-28 (OPUS, %s D F; ASTRA nav-circle-cell-boundary, independently derived): 004690B0, which gates each "
       "mark, returns 1 when the circle's centre lies in the rectangle widened by r along one axis only (two bands, every bound "
       "inclusive), or else when some corner is strictly inside the disk (r*r > squared distance, strict). So a circle touching a "
       "side counts, and one touching only a corner does not. The arithmetic order is the source's ADDSS / SUBSS / MULSS order; "
       "a NaN fails every test. Emulator-derived results carry no native MXCSR status (X)" % REC)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavGridParams" and c[3] == "cellBitsetArray" and REC not in c[5]: c[5] += ADD; fl[i] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
F = {cells(l)[3]: cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "NavGridParams"}
_r = F["cellBitsetArray"][5]   # the NaN sentence was later narrowed by nav_nan_domain.py; the rest of ADD must still be present
check("S", ADD in _r or (ADD.split("a NaN fails every test.")[0] in _r and "nav_nan_domain.py" in _r), "NavGridParams cellBitsetArray carries the overlap predicate rule")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
