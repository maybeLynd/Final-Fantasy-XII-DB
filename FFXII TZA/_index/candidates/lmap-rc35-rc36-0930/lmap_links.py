"""lmap_links.py - RC-36 data half: where a marker's link bytes point, in every shipped menumap_location.bin (OPUS,
2026-09-30). A marker is an array-B point. 003C0F70 passes its byte +0x14 to 003BDDE0 as a point index of the same
record and hands the returned point to 003BCBA0, which reads that point's +0x0C as a field id without testing its kind.
This counts, per copy, the markers whose +0x14 is 0xFF (no link), indexes array A (kind 0), indexes array B (kind 1,
another marker), or is out of range; and the same for +0x15 (the link selector 003C2320's kind-1 arm reads)."""
import collections, hashlib, struct, sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools")
import vbfextract as V  # noqa: E402

VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
f = open(VBF, "rb")
names, blocks = V.load_index(f)
ps = sorted(p for p in names if p.replace("\\", "/").lower().endswith("menumap_location.bin"))


def H(b, o):
    return struct.unpack_from("<H", b, o)[0]


tot = collections.Counter()
for p in ps:
    b = V.read_entry(f, names, blocks, p)
    cnt = b[9]
    offs = [H(b, 0xA + 2 * i) for i in range(cnt)]
    c = collections.Counter()
    for r in offs:
        A, Bn = b[r], b[r + 1]
        for j in range(Bn):
            m = r + 4 + 24 * A + 24 * j
            for off in (0x14, 0x15):
                v = b[m + off]
                k = "FF" if v == 0xFF else "A" if v < A else "B" if v < A + Bn else "out"
                c[(off, k)] += 1
    tot.update(c)
    print("%-6s sha %s markers %d  +0x14 %s  +0x15 %s" % (
        p.replace("\\", "/").split("/")[-3], hashlib.sha256(b).hexdigest()[:8],
        sum(v for (o, k), v in c.items() if o == 0x14),
        {k: v for (o, k), v in sorted(c.items()) if o == 0x14}, {k: v for (o, k), v in sorted(c.items()) if o == 0x15}))
print("all copies: +0x14 %s; +0x15 %s" % ({k: v for (o, k), v in sorted(tot.items()) if o == 0x14},
                                           {k: v for (o, k), v in sorted(tot.items()) if o == 0x15}))
