"""domain_check.py - ASTRA-REQ-FABLE-RETURN-DOMAIN-QUALIFIERS (FABLE, Claude Opus 5.5, 2026-09-28).

  W1 the reference round trip's domain is modular: with D(u) = (B + u) mod 2^64 and E(p) = (p - B) mod 2^32 (low dwords),
     D(E(p)) = p exactly when (p - B) mod 2^64 < 2^32. For a B within 4 GiB of the top (B = 2^64 - 2^31) the window wraps:
     p = 5 round-trips although it is below B, which the interval reading B <= p < B + 2^32 excludes. For the non-wrapping
     example B = 0x140000000 (three_check_bound.py's I1) the two readings agree on every sample
  Q1 each consumer carries its qualifier: the three rate pages say the NaN is kept only when the comiss completes (invalid
     masked; unmasked raises #XM and the continuation is the handler's; MXCSR not established), and the 0020E620 row says the
     window is modular
  C  controls: a page copy with the clause removed fails Q1; with the modular test replaced by the interval test W1 fails
"""
import os, re, sys
DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
M64, M32 = 1 << 64, 1 << 32
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def rt(B, p):
    E = ((p & 0xFFFFFFFF) - (B & 0xFFFFFFFF)) % M32
    return (B + E) % M64 == p
modular = lambda B, p: (p - B) % M64 < M32
interval = lambda B, p: B <= p < B + M32
def w1(pred):
    hi, lo = M64 - (1 << 31), 0x140000000
    s_hi = [hi, hi + 1, M64 - 1, 0, 5, (1 << 31) - 1, 1 << 31, hi - 1, 0x140000000]
    s_lo = [lo, lo + 1, lo + M32 - 1, lo + M32, lo - 1, 0, M64 - 1]
    return all(rt(hi, p) == pred(hi, p) for p in s_hi) and all(rt(lo, p) == pred(lo, p) for p in s_lo), rt(hi, 5), interval(hi, 5)
good, r5, i5 = w1(modular)
ok("W1", good and r5 and not i5 and all(modular(0x140000000, p) == interval(0x140000000, p) for p in [0x140000000, 0x13FFFFFFF, 0x240000000, 0x23FFFFFFF]),
   "the modular predicate matches the round trip for a wrapping and a non-wrapping B; p = 5 round-trips at B = 2^64 - 2^31 (interval reading: %s)" % i5)
P = {"shared": "00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md",
     "contract": "16-UI/Widget-Object-Model/CONTRACT-widget-object.md",
     "anim": "16-UI/Widget-Object-Model/starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md"}
T = {k: open(os.path.join(DB, v), encoding="utf-8").read() for k, v in P.items()}
CL = "the NaN is kept only when the `comiss` completes"
def q1(T):
    rate = all(T[k].count(CL) == 1 and "raises #XM" in T[k] and "MXCSR at this site is not established" in T[k] for k in P)
    row = next((l for l in T["shared"].split("\n") if l.startswith("| `0020E620` |")), "")
    return rate and "(p − B) mod 2^64 < 2^32" in row
ok("Q1", q1(T), "three rate consumers carry the completion clause; the 0020E620 row carries the modular window")
T2 = dict(T); T2["anim"] = T["anim"].replace(CL, "the NaN is kept")
ok("C", not q1(T2) and not w1(interval)[0], "a page without the clause fails Q1; the interval test fails W1")
print("FAILS", fails); sys.exit(1 if fails else 0)
