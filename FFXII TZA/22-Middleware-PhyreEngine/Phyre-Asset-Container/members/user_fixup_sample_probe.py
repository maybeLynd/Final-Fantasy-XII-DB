# user_fixup_sample_probe.py (FABLE, Claude Opus 5.5, 2026-09-25; UQ-287) - locate the user-fixup record array in sample .phyre files by shape (count x 12 bytes:
# {typeIndex, size, offset}, offsets cumulative from 0, sizes summing to <= dataSize), print the blob before it
# and the type index -> class name through the packed namespace.
import sys, struct, collections, random
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools")
import vbfextract as V
f = open(r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf", "rb")
names, blocks = V.load_index(f)
phy = sorted(n for n in names if n.lower().endswith(".phyre"))
random.seed(7)
NAMED = ["gamedata/d3d11/artdata/chr/bg_obj/b00/b0001/mws/b0001.dae.phyre",
         "gamedata/d3d11/artdata/map/rbn50/rbn5001/rbn5001.dae.phyre"]
sample = NAMED + random.sample(phy, 40)
for p in sample:
    b = V.read_entry(f, names, blocks, p)
    w = struct.unpack_from("<21I", b)
    hsz, nssz, cnt, dsz = w[1], w[2], w[12], w[13]
    ns = b[hsz:hsz + nssz]
    nTypes, nClasses, nMembers, pool = struct.unpack_from("<IIII", ns, 8)
    coff = 0x20 + 4 * nTypes; moff = coff + 36 * nClasses; poff = moff + 24 * nMembers
    def tname(i):
        o = struct.unpack_from("<I", ns, 0x20 + 4 * i)[0]
        return ns[poff + o: ns.index(b"\0", poff + o)].decode("ascii", "replace")
    def cname(c):
        w9 = struct.unpack_from("<9I", ns, coff + 36 * c)
        return ns[poff + w9[2]: ns.index(b"\0", poff + w9[2])].decode("ascii", "replace")
    hits = []
    for pos in range(hsz + nssz, len(b) - 12 * cnt):
        if b[pos + 8:pos + 12] != bytes(4):          # the first record's offset must be 0
            continue
        recs = [struct.unpack_from("<3I", b, pos + 12 * k) for k in range(cnt)]
        if recs[0][2] != 0:
            continue
        ok = all(recs[k][2] == recs[k - 1][2] + recs[k - 1][1] for k in range(1, cnt)) and \
             recs[-1][2] + recs[-1][1] <= dsz and all(r[1] > 0 for r in recs)
        if ok:
            hits.append((pos, recs))
    print("==", p, "count", cnt, "dataSize", dsz, "types", nTypes, "classes", nClasses, "record-array hits", len(hits))
    for pos, recs in hits[:1]:
        blob = b[pos - ((dsz + 0) ):pos]
        for t, s, o in recs[:8]:
            label = ("type " + tname(t)) if t < nTypes else ("class " + cname(t - nTypes - 1) if t - nTypes - 1 < nClasses else "?")
            print("   idx %4d  %-40s size %3d  data %r" % (t, label, s, blob[o:o + s][:60]))
