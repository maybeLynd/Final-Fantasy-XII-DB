"""SWE2-AUDIT-SPEC: RC-35 block values re-read from the nine menumap_location.bin copies with 003BE680's own address
arithmetic (count byte +9, offset words +0xA, block = rec + 4 + 24*(cA+cB) + 20*cC), plus a control that uses a wrong
C stride (16) to show the tally is sensitive to the formula. 2026-09-30."""
import glob, struct, collections
files = sorted(glob.glob(r"D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok/*/worldmap/menumap_location.bin"))
def blocks(b, cstride):
    n = b[9]; out = []
    for i in range(n):
        ro = struct.unpack_from("<H", b, 0xA + 2 * i)[0]
        if ro == 0: out.append(None); continue
        ca, cb, cc = b[ro], b[ro + 1], b[ro + 2]
        bo = ro + 4 + 24 * (ca + cb) + cstride * cc
        out.append(struct.unpack_from("<4H", b, bo) if bo + 8 <= len(b) else "OOB")
    return out
print("copies:", len(files))
tallies = set()
for f in files:
    b = open(f, "rb").read()
    bl = blocks(b, 20)
    t = collections.Counter(x for x in bl)
    tallies.add(tuple(sorted(t.items(), key=str)))
    print("%s records=%d %s" % (f.replace(chr(92), "/").split("/")[-3], len(bl), dict(t)))
print("distinct per-copy tallies:", len(tallies))
b = open(files[0], "rb").read()
t16 = collections.Counter(blocks(b, 16))
print("CONTROL stride 16 (wrong) on", files[0].replace(chr(92), "/").split("/")[-3], ":", len(t16), "distinct values; top", t16.most_common(3))
