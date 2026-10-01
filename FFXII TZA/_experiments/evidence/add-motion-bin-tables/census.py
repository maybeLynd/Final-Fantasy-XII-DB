"""The two .bin tables in ps2data/add_motion, walked by their loaders' rules.

Read-only over FFXII_TZA.vbf (set FF12_VBF).
- skeletonmapping.bin, AddMotion_LoadSkeletonMapping (0036FFF0): i32 count; per record 32 name bytes (copied with a
  0x20-byte string copy), i32 n, then n i32 values (00370086-0037013B).
- highmodelreplace.bin, AddMotion_LoadHighModelReplace (0037CCC0): records until a leading -1; each record is
  i32 a, i32 b, i32 c, then i32 pairs {x, y} until a -1, then the next record (0037CD44-0037CE49). The parsed record is
  0x30 bytes with x values from +0x10 and y values from +0x20, four slots each, and no count check.
Reports whether each walk ends exactly at the file size and the value distributions.
Positive control: the archive index lists both files.
FABLE, 2026-09-13.
"""
import sys, os, io, struct, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../Tools/analysis-kit/gfz-scripts"))
from census_format_magics import load_index

BLOCK = 0x10000
f = io.open(os.environ["FF12_VBF"], "rb")
names, blocks = load_index(f)


def read_all(path):
    sb, size, off = names[path]
    n = (size + BLOCK - 1) // BLOCK
    out = b""
    f.seek(off)
    for i in range(n):
        csize = blocks[sb + i] or BLOCK
        expected = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        chunk = f.read(csize)
        if csize != expected:
            chunk = zlib.decompress(chunk)
        out += chunk
    assert len(out) == size
    return out


SK = "ps2data/add_motion/skeletonmapping.bin"
HM = "ps2data/add_motion/highmodelreplace.bin"
print("control: both entries present:", SK in names, HM in names)

d = read_all(SK)
count = struct.unpack_from("<i", d, 0)[0]; pos = 4
print("%s: %d bytes, count %d" % (SK, len(d), count))
for r in range(count):
    name = d[pos:pos + 32].split(bytes(1))[0].decode("latin1"); n = struct.unpack_from("<i", d, pos + 32)[0]
    vals = struct.unpack_from("<%di" % n, d, pos + 36); pos += 36 + 4 * n
    print("  record %d: name %r, n %d, values %s" % (r, name, n, list(vals)))
print("  walk ends at the file size:", pos == len(d))

d = read_all(HM)
pos = 0; recs = []
while struct.unpack_from("<i", d, pos)[0] != -1:
    a, b, c = struct.unpack_from("<iii", d, pos); pos += 12
    pairs = []
    while struct.unpack_from("<i", d, pos)[0] != -1:
        pairs.append(struct.unpack_from("<ii", d, pos)); pos += 8
    pos += 4
    recs.append((a, b, c, pairs))
pos += 4
print("%s: %d bytes, %d records, walk (through the final -1) ends at the file size: %s" % (HM, len(d), len(recs), pos == len(d)))
C = collections.Counter
print("  pairs per record:", sorted(C(len(r[3]) for r in recs).items()), "; more than 4 (would overrun the 0x30 record):", sum(1 for r in recs if len(r[3]) > 4))
print("  a as (u16 low, u16 high):", sorted(C((r[0] >> 16) & 0xFFFF for r in recs).items()), "; b values:", sorted(C(r[1] for r in recs).items()), "; c values:", sorted(C(r[2] for r in recs).items()))
print("  x high words:", sorted(C((p[0] >> 16) & 0xFFFF for r in recs for p in r[3]).items()), "; y values:", sorted(C(p[1] for r in recs for p in r[3]).items()))
print("  (a, b, c) keys distinct:", len({r[:3] for r in recs}) == len(recs))
for r in recs[:6]:
    print("  ", "a=%08X b=%d c=%d" % (r[0] & 0xFFFFFFFF, r[1], r[2]), ["x=%08X y=%d" % (x & 0xFFFFFFFF, y) for x, y in r[3]])
