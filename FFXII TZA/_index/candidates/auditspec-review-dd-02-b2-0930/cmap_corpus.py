"""cmap_corpus.py - SWE2-AUDIT-SPEC re-derivation of a sample of the cmap page's corpus claims from the shipped files
(D:/FFXII_TZA_extract, all nine locale copies), without the page's untracked decoder. Reads only.

  size, magic, fileId, offDir / offSec2, directory count 48 (stride 8), sec2 u16 count 369 and its value histogram,
  sec3 start = offSec2 + 2 + 2*count rounded up to 4, sec3 count 77 closing at EOF, entry +1 nonzero entries,
  entry +2 non -1 values, and whether the nine copies are byte-identical.
"""
import collections, glob, hashlib, struct

files = sorted(glob.glob(r"D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok/*/worldmap/menumap_common.bin"))
print("files", len(files))
hs = {}
for f in files:
    b = open(f, "rb").read()
    hs.setdefault(hashlib.sha256(b).hexdigest(), []).append(f.split("/")[-3] if "/" in f else f)
print("distinct contents", len(hs), {k[:10]: v for k, v in hs.items()})
b = open(files[0], "rb").read()
print("size 0x%X (%d)" % (len(b), len(b)), "magic", b[:4], "fileId 0x%08X" % struct.unpack_from("<I", b, 4)[0])
od, o2 = struct.unpack_from("<HH", b, 8)
print("offDir 0x%X offSec2 0x%X" % (od, o2))
n = struct.unpack_from("<I", b, od)[0]
ents = [struct.unpack_from("<BBhI", b, od + 4 + 8 * i) for i in range(n)]
print("dir count", n, "ends 0x%X" % (od + 4 + 8 * n))
print("entry +1 nonzero:", [(i, e[1]) for i, e in enumerate(ents) if e[1]])
print("entry +2 not -1:", [(i, e[2]) for i, e in enumerate(ents) if e[2] != -1])
print("nameId range", min(e[3] for e in ents), max(e[3] for e in ents))
groups = collections.Counter(e[0] for e in ents)
print("distinct groups", len(groups), "doubled", [g for g, c in groups.items() if c > 1])
c2 = struct.unpack_from("<H", b, o2)[0]
vals = struct.unpack_from("<%dh" % c2, b, o2 + 2)
print("sec2 count", c2, "histogram", dict(collections.Counter(vals)))
s3 = (o2 + 2 + 2 * c2 + 3) & ~3
c3 = struct.unpack_from("<I", b, s3)[0]
print("sec3 start 0x%X count %d end 0x%X EOF 0x%X" % (s3, c3, s3 + 4 + 8 * c3, len(b)))
recs = [struct.unpack_from("<HHHH", b, s3 + 4 + 8 * i) for i in range(c3)]
print("sec3 pad all 0:", all(r[2] == 0 for r in recs), " seq 0..%d sequential:" % (c3 - 1), [r[3] for r in recs] == list(range(c3)))
