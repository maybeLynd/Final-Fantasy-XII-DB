"""gr17_jccfix.py - the jcc-edge variant of the reach set with the leaf attribution fixed.

gr17_graph2's jcc variant attributed a jcc in a no-.pdata leaf to the nearest preceding CALL TARGET (GG.fn), so the
je at 002E70C9 (leaf 002E70C0, named only by two rip leas) became an edge of 002E6EB0 and pulled 6 functions in.
Here a no-.pdata jcc site is attributed to its own leaf: the nearest start p <= site such that p follows an int3 byte
or a .pdata chunk end (or is a direct call target), and a linear decode from p lands on the site. The leaf is then a
graph node of its own, joined to callers only by the E8/E9 edges that target it. Controls: the misattributed edge must
now sit on node 002E70C0; the six additions must disappear unless another real edge brings them in.
Also counts cross-function jcc sites inside .pdata code (a jcc tail in a framed function)."""
import sys, os, re, struct, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import gr17_graph2 as G2
GG = G2.GG; T = G2.T; P = G2.P; G = GG.G
raw = T.raw
PDENDS = sorted(T.IB + e for b, e, u in G.PD)
CT = set(int(k, 16) for k in GG.RC)


def leaf_start(s):
    j = bisect.bisect_right(PDENDS, s) - 1
    floor = PDENDS[j] if j >= 0 else s - 0x1000
    cands = []
    for p in range(s, max(floor, s - 0x800) - 1, -1):
        o = T.off(p)
        if o is None:
            break
        if p == floor or raw[o - 1] == 0xCC or p in CT:
            cands.append(p)
    for p in cands:  # nearest first
        a = p
        for i in T.md.disasm(T.rd(p, s - p + 16), p):
            if i.address >= s:
                a = i.address
                break
        if a == s:
            return p
    return None


ed0, _, _ = G2.build(False)
R0 = P.reach(ed0)
ed = {a: dict(bs) for a, bs in ed0.items()}
nj = 0
unattr = 0
moved = []
for n, v, vs, p, rs in T.TEXT:
    blob = raw[p:p + min(vs, rs)]
    for m in re.finditer(rb"\x0f[\x80-\x8f]", blob):
        k = m.start()
        if k + 6 > len(blob):
            continue
        s = v + k
        if G2.in_pdata(s):
            continue
        t = s + 6 + struct.unpack_from("<i", blob, k + 2)[0]
        if not (T.IB < t < T.IB + 0x3000000) or not G2.ok_target(t):
            continue
        if not G2.in_pdata(t) and ("%X" % t) not in GG.RC:
            continue
        a = leaf_start(s)
        if a is None:
            unattr += 1
            continue
        b = GG.tfn(t)
        if a == b or (a <= t < s + 6):
            continue
        ins = list(T.md.disasm(blob[k:k + 6], s, 1))
        if not ins or ins[0].size != 6:
            continue
        if GG.fn(s) != a:
            moved.append((s, GG.fn(s), a, t))
        ed.setdefault(a, {}).setdefault(b, s)
        nj += 1
R1 = P.reach(ed)
print("no-.pdata cross-function jcc edges kept: %d (unattributable sites %d); attribution changed vs gr17_graph2 for %d"
      % (nj, unattr, len(moved)))
for s, old, new, t in moved:
    if t in R1 or GG.tfn(t) in R1:
        print("   %08X: gr17_graph2 said %08X, leaf is %08X, target %08X (reaches)" % (s, old, new, t))
print("reach set with fixed jcc edges: %d (R0 %d); added %s" % (len(R1), len(R0), sorted("%08X" % x for x in R1 - R0)))
print("control: edge 002E70C9 now on node %s; 002E6EB0 in R1: %s; 002E65A0 in R1: %s; 002E70C0 in R1: %s"
      % ("%08X" % leaf_start(0x002E70C9), 0x002E6EB0 in R1, 0x002E65A0 in R1, 0x002E70C0 in R1))
for x in sorted(R1 - R0):
    q = P.path(ed, x)
    print("   %08X via %s" % (x, " | ".join("%08X@%08X" % (b, s) for a, s, b in q)))
