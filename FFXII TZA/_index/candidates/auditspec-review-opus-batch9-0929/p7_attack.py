"""p7_attack.py - SWE2-AUDIT-SPEC (batch-9 review, 2026-09-29). Attack on CON-198's P7 ("the upward closure of every
vtable-stamping body leaves the family band at exactly three sites, all this PFXAA").

P7 closes over DIRECT calls (raw E8/E9) only and asserts the three exits' shapes, not what they construct. This:
  A  re-imports the falsifier's own class set / stampers / closure (its module globals; its printed checks are captured)
  B  for every body in the in-band closure, every NON-direct reference from outside the band: rip-relative lea/mov
     (window scan over the band, confirmed by decode), aligned/unaligned abs64 and rva32 in every section except .pdata
     and unwind data; a positive control: the PFXAA vtable itself must be found by the same rip scan
  C  what 00646770 and 00646AB0 are: the stamping bodies below each exit (in-band callee closure) and the vtables they stamp
"""
import contextlib, io, os, struct, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
GS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, GS)
import ov31_indep as T  # noqa: E402

buf = io.StringIO()
cwd = os.getcwd()
with contextlib.redirect_stdout(buf):
    os.chdir(GS)
    import types
    src = os.path.join(GS, "falsify_posteffect_family.py")
    ns = {"__name__": "falsify_posteffect_family", "__file__": src}
    try:
        exec(compile(open(src, encoding="utf-8").read(), src, "exec"), ns)
    except SystemExit:  # the falsifier raises SystemExit at module end; its globals are complete by then
        pass
    F = types.SimpleNamespace(**ns)
    os.chdir(cwd)
print("falsifier imported; its tail:", buf.getvalue().strip().splitlines()[-1])
LO, HI = 0x0063E000, 0x00648200
inb = lambda a: a is not None and LO <= a < HI
vname = {v: n for n, v in F.vt.items()}

# the in-band closure (recomputed exactly as P7 does, keeping the whole seen set)
seen, fr = set(F.stampers), list(F.stampers)
edges = collections.defaultdict(set)   # callee body -> in-band caller bodies
while fr:
    x = fr.pop()
    for c in F.callers[x]:
        o = F.owner(c)
        if inb(o):
            edges[x].add(o)
            if o not in seen:
                seen.add(o); fr.append(o)
print("A  stamping bodies %d; in-band closure %d bodies" % (len(F.stampers), len(seen)))

# B  non-direct references to closure bodies from outside the band
rip = T.rip_refs(LO, HI)
ctrl = [h for h in T.rip_refs(F.vt["PFXAA"], F.vt["PFXAA"] + 1)]
print("B  control: rip references to the PFXAA vtable %08X: %d (%s)" % (F.vt["PFXAA"], len(ctrl),
      ", ".join("%08X" % h[0] for h in ctrl)))
pdata = [s for s in T.SECS if s[0] == ".pdata"][0]
hits = []
for a, mn, op, sz in rip:
    i = T.dis(a, count=1)[0]
    for m, _ in T.mem_ops(i):
        if m.base == T.X86_REG_RIP:
            tgt = a + i.size + m.disp
            if tgt in seen and not inb(F.owner(a)):
                hits.append(("rip", a, F.owner(a), tgt, "%s %s" % (mn, op)))
for tgt in sorted(seen):
    d = T.data_refs(tgt)
    for kind in ("abs64", "rva32"):
        for s in d[kind]:
            va = int(s[:8], 16)
            if "(.pdata" in s:
                continue
            hits.append((kind, va, None, tgt, s))
print("B  non-direct references to closure bodies from outside the band (excluding .pdata): %d" % len(hits))
for h in hits:
    print("   %-5s %08X owner %s -> %08X (%s) %s" % (h[0], h[1], "%08X" % h[2] if h[2] else "-", h[3],
          "stamper" if h[3] in F.stampers else "in-band caller", h[4]))

# C  what each exit constructs
def below(root):
    out, st = set(), [root]
    rev = collections.defaultdict(set)
    for callee, cs in edges.items():
        for c in cs:
            rev[c].add(callee)
    while st:
        x = st.pop()
        if x in out:
            continue
        out.add(x); st.extend(rev.get(x, ()))
    return out
for ex in (0x00645DB0, 0x00646770, 0x00646AB0):
    b = below(ex)
    classes = sorted(set(n for n, s in F.leas.items() for x in s if x in b))
    print("C  exit target %08X: %d in-band bodies below it; stamps %s" % (ex, len(b), classes))

# D  classify every section-B hit: inside one of the 37 vtables' slot arrays (a virtual slot on an existing object,
#    not a construction route), inside unwind info (the RVA range .pdata's unwind pointers cover), or other
vt_ranges = []
for n, v in F.vt.items():
    k = 0
    while True:
        q = struct.unpack("<Q", T.rd(v + 8 * k, 8))[0]
        if not (0x00120000 <= q < 0x00900000):
            break
        k += 1
    vt_ranges.append((v, v + 8 * k, n))
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(T.IB + dd.VirtualAddress)
uw = [struct.unpack_from("<III", T.raw, o + 12 * j)[2] + T.IB for j in range(dd.Size // 12)]
ulo, uhi = min(uw), max(uw) + 0x100
cls = collections.Counter(); other = []
for h in hits:
    va = h[1]
    if h[0] == "abs64" and any(a <= va < b for a, b, n in vt_ranges):
        cls["abs64 in a family vtable slot array"] += 1
    elif h[0] == "rva32" and ulo <= va < uhi:
        cls["rva32 inside unwind info"] += 1
    else:
        cls["other"] += 1; other.append(h)
print("D  classification:", dict(cls), "(unwind info range %08X..%08X)" % (ulo, uhi))
for h in other:
    raw = T.rd(h[1] - 8, 24).hex()
    print("   other %-5s %08X -> %08X  bytes[-8..+16] %s" % (h[0], h[1], h[3], raw))

# E  the third exit 0089E870: whose EH data references it, and what that owner builds
print("E  stamper classes of 006458A0:", sorted(n for n, s in F.leas.items() if 0x006458A0 in s),
      "| of 00645DB0:", sorted(n for n, s in F.leas.items() if 0x00645DB0 in s))
for a in range(0x01DACB00, 0x01DACB30, 4):
    v = struct.unpack("<I", T.rd(a, 4))[0]
    print("   %08X  %08X  -> %08X" % (a, v, v + T.IB))
# .pdata entries whose unwind info lies just before 01DACB14 (the handler data follows UNWIND_INFO)
cand = [(b + T.IB, e + T.IB, u + T.IB) for b, e, u in (struct.unpack_from("<III", T.raw, o + 12 * j) for j in range(dd.Size // 12))
        if 0x01DACA80 <= u + T.IB <= 0x01DACB14]
print("   .pdata entries with unwind info in 01DACA80..01DACB14:", ["%08X-%08X uw %08X" % c for c in cand])
