"""UQ-2 residue re-counted by what position 1 IS (OPUS, 2026-09-27). Control.

UQ-2 closed SUPERSEDED (cd73ae1d5) with a residue of 511 rows of derived-call-signatures.tsv whose position 1 is not
typed by the three typing tables (vtable slot, vtable store through this, typed callers). Under the Win64 ABI, position 1
is rcx or xmm0, so the derived signature itself already sorts those rows:
  R1 140 have arity 0 - there is no position 1 to type
  R2 3 take position 1 in xmm0 - it is floating-point (float vs double not claimed)
  R3 47 read later arguments but neither rcx nor xmm0 - position 1 is dead in the body, so no callee-side evidence can
     type it (UQ-1's dead-position class)
  R4 321 read rcx - an integer or pointer whose type is not derived: the real derivation residue
  S  the four classes partition the 511 exactly, and 562 - 511 = 51 typed (40 + 7 + 4)
Not claimed: any type for the 321; that the 47 are unused by callers.
"""
import os, sys, collections
DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ABI = os.path.join(DB, "00-Engine-Core-Runtime", "ABI-Recovery")
rows = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(ABI, "derived-call-signatures.tsv"), encoding="utf-8")
        if l[:1].isalnum() and not l.startswith("addr")]
typed = set()
n_tab = {}
for fn in ("derived-signatures-this-types.tsv", "derived-signatures-ctor-types.tsv"):
    s = {l.split("\t")[0] for l in open(os.path.join(ABI, fn), encoding="utf-8") if l[:1].isalnum() and not l.startswith("addr")}
    n_tab[fn] = len(s); typed |= s
CALLER = {"002FFEF0", "00306B10", "0030B8E0", "0030DA30"}   # uq2_caller_route.py C1
typed |= CALLER
un = [r for r in rows if r[0] not in typed]
c = collections.Counter()
for r in un:
    ints, flt = r[2].split(","), r[3].split(",")
    if r[1] == "0": c["R1"] += 1
    elif "rcx" in ints: c["R4"] += 1
    elif "xmm0" in flt: c["R2"] += 1
    else: c["R3"] += 1
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
check("R1 140 rows have arity 0", c["R1"] == 140, str(c["R1"]))
check("R2 3 rows take position 1 in xmm0", c["R2"] == 3, str(c["R2"]))
check("R3 47 rows never read position 1", c["R3"] == 47, str(c["R3"]))
check("R4 321 rows read rcx with no derived type", c["R4"] == 321, str(c["R4"]))
check("S the classes partition the 511, and 51 are typed", len(rows) == 562 and len(un) == 511 and sum(c.values()) == 511
      and len(rows) - len(un) == 51, "(tables %s)" % n_tab)
print("FAILS", fails)
sys.exit(1 if fails else 0)
