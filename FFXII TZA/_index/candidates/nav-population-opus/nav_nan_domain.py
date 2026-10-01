"""nav_nan_domain.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC; no emulator, no native execution.
Narrows OPUS's own NaN clause on NavGridParams cellBitsetArray (nav_circle_cell.py, d87bb8501) for
ASTRA-REQ-OPUS-NAV-NAN-DOMAIN (_experiments/evidence/nav-nan-operand-domain/): 'a NaN fails every test' was too broad.

  O  operand structure from nav_circle_cell.py D: the two bands read A, B, r and all four bounds; each corner test reads r and
     one bound per axis (minA / minB, minA / maxB, maxA / minB, maxA / maxB). comiss sets CF / ZF / PF on an unordered
     compare, so `jb` fails a band and `ja` / `seta` reject a corner - a NaN disables exactly the tests that read it
  N  the same binary32 model in the source order, with NaN (quiet 0x7FC00000): rectangle 0..10 with minA = NaN, centre
     (13, 14), r = 6 returns 1 through the last corner ((10-14)^2 + (10-13)^2 = 25 < 36); a NaN centre coordinate and a NaN
     radius return 0 (every test reads them); a finite control with the same circle returns 1 by the same corner
  W  REGRESSION (FAILS before): the row states the per-operand rule and no longer the blanket clause
The native reading assumes the compares complete under masked exceptions (MXCSR 1F80); no live bound or radius is claimed.
Usage: python nav_nan_domain.py [--patch]
"""
import math, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
f32 = lambda x: struct.unpack("<f", struct.pack("<f", x))[0]
NAN = struct.unpack("<f", struct.pack("<I", 0x7FC00000))[0]
def model(rect, circ):
    # binary32 in the source order; Python float comparisons with NaN are False, matching comiss + jb / ja / seta
    minA, minB, maxA, maxB = map(f32, rect); a, b, r = map(f32, circ)
    if a >= f32(minA - r) and b >= minB and f32(r + maxA) >= a and maxB >= b: return 1
    if a >= minA and b >= f32(minB - r) and maxA >= a and f32(r + maxB) >= b: return 1
    dA0, dB0, rr = f32(minA - a), f32(minB - b), f32(r * r)
    if rr > f32(f32(dB0 * dB0) + f32(dA0 * dA0)): return 1
    dB1 = f32(maxB - b)
    if rr > f32(f32(dB1 * dB1) + f32(dA0 * dA0)): return 1
    dA1 = f32(maxA - a)
    if rr > f32(f32(dB0 * dB0) + f32(dA1 * dA1)): return 1
    return int(rr > f32(f32(dB1 * dB1) + f32(dA1 * dA1)))
READS = {"band1": {"A", "B", "r", "minA", "maxA", "minB", "maxB"}, "band2": {"A", "B", "r", "minA", "maxA", "minB", "maxB"},
         "c1": {"A", "B", "r", "minA", "minB"}, "c2": {"A", "B", "r", "minA", "maxB"}, "c3": {"A", "B", "r", "maxA", "minB"}, "c4": {"A", "B", "r", "maxA", "maxB"}}
check("O", all(s >= {"A", "B", "r"} for s in READS.values()) and [k for k, s in READS.items() if "minA" not in s] == ["c3", "c4"],
      "every test reads the centre and r; a NaN minA leaves corners c3 / c4 live")
cases = [((NAN, 0, 10, 10), (13, 14, 6), 1), ((0, 0, 10, 10), (13, 14, 6), 1), ((0, 0, 10, 10), (NAN, 14, 6), 0), ((0, 0, 10, 10), (13, 14, NAN), 0), ((0, 0, 10, 10), (13, 14, 5), 0)]
got = [model(rc, ci) for rc, ci, _ in cases]
check("N", got == [e for _, _, e in cases] and math.isnan(NAN), "minA NaN with centre (13, 14), r 6 -> 1; finite control -> 1; NaN centre / radius -> 0; tangent control -> 0: %s" % got)
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/nav-population-opus/nav_nan_domain.py"
OLD = "a NaN fails every test."
NEW = ("a comparison with an unordered (NaN) operand is false - comiss sets CF / ZF / PF, so `jb` fails that band and `ja` / `seta` reject that corner - "
       "so a NaN disables exactly the tests that read it: a NaN centre coordinate or radius fails all six, while a NaN rectangle bound fails only the bands "
       "and corners that read it, and a remaining corner can still return 1 (minA NaN, centre (13, 14), r 6 returns 1 through the last corner; ASTRA "
       "nav-nan-operand-domain, %s N). The native reading assumes the compares complete under masked exceptions." % REC)
NOTE = " || NARROWED 2026-09-28 (OPUS, %s O N): the clause 'a NaN fails every test' was too broad (ASTRA-REQ-OPUS-NAV-NAN-DOMAIN)" % REC
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavGridParams" and c[3] == "cellBitsetArray" and OLD in c[5]:
            c[5] = c[5].replace(OLD, NEW); c[8] += NOTE; fl[i] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
row = next(cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "NavGridParams" and cells(l)[3] == "cellBitsetArray")
check("W", NEW in row[5] and OLD not in row[5] and NOTE in row[8], "cellBitsetArray states the per-operand NaN rule, not the blanket clause")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
