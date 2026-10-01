# user_fixup_census.py (FABLE, Claude Opus 5.5, 2026-09-25) - UQ-287.
# Reads the 84-byte PClusterHeader of every shipped .phyre entry straight from the first VBF block (the CU-4
# method) and tabulates m_userFixupCount (+0x30) and m_userFixupDataSize (+0x34), split by the D3D11 partition
# (mesh: index/vertex buffer non-zero; texture: m_maxTextureBufferSize non-zero; neither).
# Controls: every header must carry RYHP / 84 / 11XD (CU-4's uniformity) or the run refuses; the entry count
# must be 35,984.
# Output: user-fixup-census.tsv beside this file (one row per distinct (partition, count, dataSize)).
import os, sys, struct, zlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools")
import vbfextract as V
VBF = os.environ.get("FFXII_VBF", r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf")
f = open(VBF, "rb")
names, blocks = V.load_index(f)
phy = sorted(n for n in names if n.lower().endswith(".phyre"))
def head(path):
    sb, size, off = names[path]
    csize = blocks[sb] or V.BLOCK
    f.seek(off)
    data = f.read(csize)
    expected = min(V.BLOCK, size)
    return data if csize == expected else zlib.decompress(data)
rows = collections.Counter()
examples = {}
bad = 0
for p in phy:
    h = head(p)[:84]
    w = struct.unpack("<21I", h)
    if h[:4] != b"RYHP" or w[1] != 84 or h[12:16] != b"11XD":
        bad += 1
        continue
    part = "mesh" if (w[18] or w[19]) else ("texture" if w[20] else "neither")
    key = (part, w[12], w[13])
    rows[key] += 1
    examples.setdefault(key, p)
if len(phy) != 35984 or bad:
    sys.exit("REFUSE: control failed - %d entries, %d headers off the CU-4 shape" % (len(phy), bad))
with open(os.path.join(HERE, "user-fixup-census.tsv"), "w", newline="") as out:
    out.write("partition\tuserFixupCount\tuserFixupDataSize\tfiles\texample\n")
    for k in sorted(rows):
        out.write("%s\t%d\t%d\t%d\t%s\n" % (k[0], k[1], k[2], rows[k], examples[k]))
print("entries", len(phy), "| headers off-shape", bad)
by = collections.Counter()
for (part, c, s), n in rows.items():
    by[(part, "nonzero" if c else "zero")] += n
print(dict(by))
print("distinct (count, size) with count>0:", sorted({(c, s) for (part, c, s) in rows if c})[:40])
