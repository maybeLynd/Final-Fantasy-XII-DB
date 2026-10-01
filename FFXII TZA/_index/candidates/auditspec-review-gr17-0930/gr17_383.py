"""gr17_383.py - the 382-vs-383 reach count. The package's Limits figure ("135 of the 383 functions that can reach
00312280") is not printed by its checker; recompute it from the package's own graph (retool CALLS, read-only use of the
kit cache) and diff it against this review's boundary-checked no-jcc graph (gr17_graph2.build(False), 382 incl. the
target). Also: who names the leaf 002E70C0 (the jcc 002E70C9 -> 00325260 that gr17_graph2 misattributed to 002E6EB0)."""
import sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import gr17_graph2 as G2
    import retool as RT
P = G2.P; T = G2.T
SC = RT.scan()
CALLS = SC["calls"]
REV = collections.defaultdict(set)
for t, cs in CALLS.items():
    for f, s in cs:
        if f != t:
            REV[t].add(f)
TGT = 0x00312280
R = {TGT}; st = [TGT]
while st:
    x = st.pop()
    for y in REV.get(x, ()):
        if y not in R:
            R.add(y); st.append(y)
ed0, _, _ = G2.build(False)
R0 = P.reach(ed0)
print("package graph (retool CALLS): %d functions in the reach set incl. 00312280 (%d excluding it)" % (len(R), len(R) - 1))
print("review graph (boundary-checked, no jcc): %d incl. 00312280" % len(R0))
print("only in package graph: %s" % sorted("%08X" % x for x in R - R0))
print("only in review graph: %s" % sorted("%08X" % x for x in R0 - R))
for x in sorted(R - R0):
    es = sorted((t, s) for t, cs in CALLS.items() for f, s in cs if f == x and t in R)
    print("   %08X -> %s" % (x, ["%08X@%08X" % e for e in es[:6]]))
print("== references to the leaf 002E70C0")
t = 0x002E70C0
print("  rel32 %s | jcc %s | rip %s | data %s" % (T.rel32_callers(t), T.jcc_callers(t),
      ["%08X %s %s" % h[:3] for h in T.rip_refs(t, t + 1)], T.data_refs(t)))
