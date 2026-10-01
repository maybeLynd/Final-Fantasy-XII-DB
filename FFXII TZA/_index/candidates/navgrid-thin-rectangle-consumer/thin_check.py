"""thin_check.py - the nav grid builder's refinement divides by trunc(side / c0), which is 0 for a side shorter than c0
(FABLE, Claude Opus 5.5, 2026-09-28). Static binding plus binary32 arithmetic.
  N1  003924B0: nx = cvttss2si(w / c0) at 003925A9, ny = cvttss2si(h / c0) at 003925CE, then w / float(nx) at 003925E9,
      h / float(ny) at 003925FC, maxss at 00392600, and the floorf call at 00392607 (w in xmm10, h in xmm11)
  N2  ASTRA's thin case: w = 1, h = 400, c0 = 3F9A5FB2 (the supplied sqrtf boundary) gives nx = 0, ny = 331, and the
      refinement +infinity (7F800000) as floorf's argument
  C   control: the 16 x 16 case gives nx = ny = 16 and a finite refinement
"""
import os, struct, sys, math
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
B = {int(p[0], 16): p[2].split(" ;")[0] for p in (l.rstrip("\n").split(None, 2) for l in open(CACHE, encoding="utf-8", errors="replace")) if len(p) == 3 and p[1] == "003924B0"}
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
want = {0x0039258C: "movaps xmm1, xmm10", 0x00392598: "divss xmm1, xmm0", 0x003925A9: "cvttss2si eax, xmm1", 0x003925AD: "movaps xmm1, xmm11",
        0x003925B9: "divss xmm1, xmm0", 0x003925CE: "cvttss2si eax, xmm1", 0x003925E9: "divss xmm4, xmm2", 0x003925FC: "divss xmm3, xmm2",
        0x00392600: "maxss xmm4, xmm3", 0x00392604: "movaps xmm0, xmm4", 0x00392607: "call 0x861f86"}
ok("N1", all(B.get(a) == s for a, s in want.items()), "refinement sequence bound at %d instructions" % len(want))
f = lambda x: struct.unpack("<f", struct.pack("<f", x))[0]
fl = lambda u: struct.unpack("<f", struct.pack("<I", u))[0]
bits = lambda x: struct.unpack("<I", struct.pack("<f", x))[0]
def fdiv(a, b):
    if b == 0.0: return math.copysign(math.inf, a) if a != 0.0 else math.nan    # masked divide-by-zero
    return f(a / b)
def refine(w, h, c0):
    nx = int(fdiv(w, c0)); ny = int(fdiv(h, c0))                                  # cvttss2si truncates toward zero
    a = fdiv(w, float(nx)); b = fdiv(h, float(ny))
    return nx, ny, (b if (math.isnan(a) or math.isnan(b)) else max(a, b))      # maxss returns the second operand on NaN
nx, ny, r = refine(1.0, 400.0, fl(0x3F9A5FB2))
ok("N2", nx == 0 and ny == 331 and bits(r) == 0x7F800000, "w = 1, h = 400, c0 = 3F9A5FB2: nx %d, ny %d, refinement %08X" % (nx, ny, bits(r)))
c16 = f(math.sqrt(f(f(16.0 * 16.0) / 275.0)))
nx2, ny2, r2 = refine(16.0, 16.0, c16)
ok("C", nx2 == ny2 == 16 and math.isfinite(r2), "16 x 16: c0 %08X, nx %d, ny %d, refinement %08X (finite)" % (bits(c16), nx2, ny2, bits(r2)))
print("FAILS", fails); sys.exit(1 if fails else 0)
