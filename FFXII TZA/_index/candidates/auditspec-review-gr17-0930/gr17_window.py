"""gr17_window.py - the package's S9 window re-counted with its own ranges, including the site kind its scan skips:
a conditional jump (jcc) whose target lies outside the containing function's .pdata extent (a conditional tail call).
Each outgoing site is tested against this review's boundary-checked reach set R0 (no jcc edges; gr17_graph2) and
against R1c = R0 plus every cross-function jcc edge whose SITE lies inside a .pdata chunk of the function it is
attributed to (the one leaf-misattributed edge 002E70C9 is thereby excluded)."""
import sys, os, struct, re, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import gr17_graph2 as G2
GG = G2.GG; T = G2.T; P = G2.P; G = GG.G

ed0, _, _ = G2.build(False)
R0 = P.reach(ed0)
# corrected jcc graph: keep a jcc edge only if its site is inside .pdata (so its function attribution is by unwind root)
ed1 = {a: dict(bs) for a, bs in ed0.items()}
nj = 0
for n, v, vs, p, rs in T.TEXT:
    blob = T.raw[p:p + min(vs, rs)]
    for m in re.finditer(rb"\x0f[\x80-\x8f]", blob):
        k = m.start()
        if k + 6 > len(blob):
            continue
        s = v + k
        if not G2.in_pdata(s) or s not in G2.BOUND:
            continue
        t = s + 6 + struct.unpack_from("<i", blob, k + 2)[0]
        a = G.root(s)
        if t not in G2.PDE or G.root(t) != t or a == t:
            continue
        ed1.setdefault(a, {}).setdefault(t, s)
        nj += 1
R1c = P.reach(ed1)
print("reach sets: R0 (no jcc) %d; R1c (pdata-attributed jcc edges added, %d edges) %d; added %s"
      % (len(R0), nj, len(R1c), sorted("%08X" % x for x in R1c - R0)))

W = [(0x003EA820, 0x003EA88D, 0x003EA9F8), (0x0032FC30, 0x0032FC50, 0x0032FC7B), (0x0032FCA0, 0x0032FCC2, 0x0032FCF6),
     (0x002628B0, 0x002628B0, 0x00262D34), (0x0025B070, 0x0025B070, 0x0025B249), (0x00234200, 0x00234200, 0x002342CE)]
dc = jc = 0
for f, lo, hi in W:
    ext = [(IBb, IBe) for (IBb, IBe) in ((T.IB + b, T.IB + e) for b, e, u in G.PD) if G.root(IBb) == f]
    inside = lambda t: any(b <= t < e for b, e in ext)
    for i in T.dis(lo, hi + 5):
        if i.address >= hi:
            break
        if not i.operands or i.operands[0].type != 2:
            continue
        t = i.operands[0].imm
        if i.mnemonic == "call" or (i.mnemonic == "jmp" and not inside(t)):
            dc += 1
            tf = GG.tfn(t)
            if tf in R0 or tf in R1c:
                print("  %08X %s -> %08X reaches (R0 %s, R1c %s)" % (i.address, i.mnemonic, t, tf in R0, tf in R1c))
        elif i.mnemonic.startswith("j") and i.mnemonic != "jmp" and not inside(t):
            jc += 1
            tf = GG.tfn(t)
            print("  CROSS-FUNCTION JCC %08X %s -> %08X (R0 %s, R1c %s)" % (i.address, i.mnemonic, t, tf in R0, tf in R1c))
print("window: %d direct call/tail sites (package S9 prints 174), %d cross-function jcc sites" % (dc, jc))
