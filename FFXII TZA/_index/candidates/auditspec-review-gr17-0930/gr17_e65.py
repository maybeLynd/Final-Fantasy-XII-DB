"""gr17_e65.py - settle 00262AFC / 00262B12 -> 002E65A0 (flagged reaching in the jcc variant of gr17_graph2), and
compare the reach sets (382 without jcc, 388 with) against the package's 383.

For 002E65A0: decode the two window sites; is 002E65A0 in the no-jcc reach set; print its BFS path in the jcc graph with
each edge's instruction decoded at the site (call / jmp / jcc), and for every jcc edge on it, whether the jcc target is
really a different function's entry reached by a conditional tail jump (the jcc's own function extent vs the target)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import gr17_graph2 as G2
GG = G2.GG; T = GG.T; P = G2.P; G = GG.G

ed0, _, _ = G2.build(False)
ed1, _, nj = G2.build(True)
R0 = P.reach(ed0)
R1 = P.reach(ed1)
print("reach sets: no-jcc %d, jcc %d (difference %s)" % (len(R0), len(R1), sorted("%08X" % x for x in R1 - R0)))
for s in (0x00262AFC, 0x00262B12):
    i = T.dis(s, s + 15, 1)[0]
    print("%08X: %s %s (size %d)" % (s, i.mnemonic, i.op_str, i.size))
t = 0x002E65A0
print("002E65A0 in no-jcc reach set: %s; in jcc reach set: %s" % (t in R0, t in R1))
p = P.path(ed1, t)
print("BFS path 002E65A0 -> 00312280 in the jcc graph (%s edges):" % (len(p) if p else None))
for a, s, b in (p or []):
    i = T.dis(s, s + 15, 1)[0]
    kind = "call" if i.mnemonic == "call" else ("jmp" if i.mnemonic == "jmp" else "JCC")
    extra = ""
    if kind == "JCC":
        extra = " | site root %s, target root %s, target is a .pdata start: %s" % (
            "%08X" % G.root(s) if G.root(s) else "-", "%08X" % G.root(b) if G.root(b) else "-", b in G2.PDE)
    print("   %08X in %08X: %s %s -> %08X [%s]%s" % (s, a, i.mnemonic, i.op_str, b, kind, extra))
# every node of R1-R0: which jcc edge makes it reach
print("== the %d functions only the jcc variant adds, each with its first jcc edge into R0" % len(R1 - R0))
for x in sorted(R1 - R0):
    q = P.path(ed1, x)
    for a, s, b in q:
        i = T.dis(s, s + 15, 1)[0]
        if i.mnemonic not in ("call", "jmp"):
            print("   %08X: %08X in %08X %s %s -> %08X (root of target %s)" % (
                x, s, a, i.mnemonic, i.op_str, b, "%08X" % G.root(b) if G.root(b) else "-"))
            break
