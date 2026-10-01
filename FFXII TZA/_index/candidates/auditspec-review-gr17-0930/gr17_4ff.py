"""gr17_4ff.py - 004FF2C0 (0046EFD0's kind-3 track launch, 0046F14B) reaches 00312280 in this review's R0 graph; the
package's E5 tests only 005372D0 for that route. Print the BFS path with each site decoded, and 004FF2C0's body."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import gr17_graph2 as G2
GG = G2.GG; T = G2.T; P = G2.P; G = GG.G
ed0, _, _ = G2.build(False)
p = P.path(ed0, 0x004FF2C0)
print("path 004FF2C0 -> 00312280 (%d edges)" % len(p))
for a, s, b in p:
    i = T.dis(s, s + 15, 1)[0]
    print("   %08X in %08X: %s %s -> %08X" % (s, a, i.mnemonic, i.op_str, b))
print("004FF2C0 direct callees: %s" % sorted("%08X" % x for x in ed0.get(0x004FF2C0, {})))
for x in sorted(ed0.get(0x004FF2C0, {})):
    print("   %08X reaches: %s" % (x, x in P.reach(ed0)))
