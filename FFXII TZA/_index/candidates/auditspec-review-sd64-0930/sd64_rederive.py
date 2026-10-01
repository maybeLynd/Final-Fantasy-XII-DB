"""sd64_rederive.py - SWE2-AUDIT-SPEC independent checks for SD-64 (2026-09-30). Read-only on the corpus.
1. "In no namespace pool": the author's checker skips an occurrence whose name is in THAT file's pool, so a name that is
   a pool name in file A but data in file B would still be reported. Test the union of all 169 files' pools.
2. Sensitivity of control C1: re-place the c1004 PAssetReference / PString arrays under the rejected layout (all
   lists' objects first, then all lists' arrays) and under the accepted one; the control must separate them.
3. Placement under the rejected layout: do the 21 names still land only in array data of the same classes?"""
import collections, os, re, struct

ROOT = "D:/FFXII MP Mod/extracted"
NAMES = ("POSITION POSITION_MORPH PROCEDURAL_TEXTURE_ENABLED PS2FogVec PS2HSMatrix PS2MatLight PS2PLColor PS2PLPos "
         "PS2WHMatrix PS2WHSMatrix PS2ZBias PS2ZBiasEnabled PS2ZBiasInstance PS2ZBiasNoGS PS2ZBiasOriginal PS_BlendCombine "
         "PS_Blur PS_BufferRender PS_Combine PS_RenderRGBL PTAlphaThreshold").split()

def parse(d):
    hsz, nssz, _, nL = struct.unpack_from("<IIII", d, 4)
    ns = d[hsz:hsz + nssz]
    nT, nC, nM = struct.unpack_from("<III", ns, 8)
    coff = 0x20 + 4 * nT; poff = coff + 36 * nC + 24 * nM
    pool = set(x.decode("latin-1") for x in ns[poff:].split(b"\0") if x)
    def nm(o): return ns[poff + o:ns.index(b"\0", poff + o)].decode("latin-1")
    cls = [nm(struct.unpack_from("<9I", ns, coff + 36 * c)[2]) for c in range(nC)]
    L = [struct.unpack_from("<9I", d, hsz + nssz + 36 * k) for k in range(nL)]
    names = [cls[x[0] - 1] if 0 < x[0] <= nC else "?" for x in L]
    start = hsz + nssz + 36 * nL
    acc, a = [], start                     # accepted: per list objects then arrays
    for n, x in zip(names, L):
        acc.append((n, "objects", a, a + x[3])); acc.append((n, "arrays", a + x[3], a + x[3] + x[4])); a += x[3] + x[4]
    rej, a = [], start                     # rejected: all objects, then all arrays
    for n, x in zip(names, L): rej.append((n, "objects", a, a + x[3])); a += x[3]
    for n, x in zip(names, L): rej.append((n, "arrays", a, a + x[4])); a += x[4]
    return pool, acc, rej

pools = collections.Counter(); files = 0
place = {"accepted": collections.Counter(), "rejected": collections.Counter()}
c1 = {}
for dp, dn, fn in os.walk(ROOT):
    for f in sorted(fn):
        if not f.lower().endswith(".phyre"): continue
        d = open(os.path.join(dp, f), "rb").read(); files += 1
        pool, acc, rej = parse(d)
        for s in NAMES:
            if s in pool: pools[s] += 1
        if f == "c1004.dae.phyre":
            for lay, sp in (("accepted", acc), ("rejected", rej)):
                for n, part, o0, o1 in sp:
                    if part == "arrays" and n in ("PAssetReference", "PString"):
                        c1[(lay, n)] = [x.decode("latin-1") for x in re.findall(rb"[\x20-\x7e]{4,}", d[o0:o1])][:2]
        for m in re.finditer(rb"(?<=\x00)(" + b"|".join(s.encode() for s in NAMES) + rb")(?=\x00)", d):
            i = m.start()
            for lay, sp in (("accepted", acc), ("rejected", rej)):
                own = next(("%s %s" % (n, part) for n, part, o0, o1 in sp if o0 <= i < o1), "outside the lists")
                place[lay][own] += 1
print("files", files)
print("the 21 names found in ANY file's namespace pool:", dict(pools) or "none")
for k in sorted(c1): print("C1 %-8s %-16s arrays -> %s" % (k[0], k[1], c1[k]))
for lay in ("accepted", "rejected"):
    print("placement under %s layout:" % lay)
    for k, v in place[lay].most_common(): print("   %6d  %s" % (v, k))
