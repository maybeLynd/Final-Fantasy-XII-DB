"""gr17_jccctrl.py - image-wide: rel32 jcc (0F 8x) inside .pdata code on an instruction boundary, and how many target a different function root."""
import sys, os, re, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\auditspec-review-gr17-0930")
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import gr17_graph2 as G2
T = G2.T; G = G2.GG.G
n_in = n_cross = n_bound = n_tpd = 0
ex = []
for n, v, vs, p, rs in T.TEXT:
    blob = T.raw[p:p + min(vs, rs)]
    for m in re.finditer(rb"\x0f[\x80-\x8f]", blob):
        k = m.start()
        if k + 6 > len(blob): continue
        s = v + k
        if not G2.in_pdata(s): continue
        n_in += 1
        if s not in G2.BOUND: continue
        n_bound += 1
        t = s + 6 + struct.unpack_from("<i", blob, k + 2)[0]
        if G.root(t) != G.root(s):
            n_cross += 1
            if t in G2.PDE: n_tpd += 1
            if len(ex) < 12: ex.append("%08X -> %08X root(s) %s root(t) %s" % (s, t, G.root(s) and "%08X" % G.root(s), G.root(t) and "%08X" % G.root(t)))
print("jcc byte pairs inside .pdata %d; on an instruction boundary %d; target in another function %d; of which at a .pdata chunk start %d" % (n_in, n_bound, n_cross, n_tpd))
print("\n".join(ex))
