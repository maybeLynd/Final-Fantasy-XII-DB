"""The one sead.win.config in the archive, walked as the sead chunk accessors walk it.

Read-only over FFXII_TZA.vbf (set FF12_VBF). Container (007ADB20 / 007AD9A0 family): +0x06 u16
directory offset, +0x08 u8 chunk count, 16-byte directory entries {u32 tag, ..., +0x08 u32 offset}.
Chunk (007ADF60): +0x02 u16 table offset, element i at chunk + u32 table[i]; the element count is
taken from chunk +0x04 here and reported with the element sizes and any printable name.
Positive control: the archive lists exactly one .config (ps2data/sound/sead.win.config, 1,264 B).
FABLE, 2026-09-12.
"""
import sys, os, io, struct, zlib
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
    return out


cfgs = [p for p in names if p.lower().endswith(".config")]
print("control: .config entries:", cfgs, [names[p][1] for p in cfgs])
d = read_all(cfgs[0])
tag, ver, diroff, count, size = struct.unpack_from("<4sHHB3xI", d, 0)
print("header: tag %r  +0x04 %d  dirOffset 0x%X  chunkCount %d  +0x0C %d (file %d)" % (tag, ver, diroff, count, size, len(d)))
ents = []
for i in range(count):
    t, a, b, off, z = struct.unpack_from("<4sHHII", d, diroff + 16 * i)
    ents.append((off, t))
    print("dir %2d  %r  +4 %d  +6 0x%X  offset 0x%03X  +0xC %d" % (i, t, a, b, off, z))
ends = sorted(o for o, _ in ents) + [len(d)]
for off, t in sorted(ents):
    end = ends[ends.index(off) + 1]
    v, hdr, cnt = struct.unpack_from("<HHI", d, off)
    tbl = list(struct.unpack_from("<%dI" % cnt, d, off + hdr)) if cnt < 64 else []
    print("chunk %r at 0x%03X..0x%03X  +0 %d  tableOffset 0x%X  count %d  elements at %s" % (t, off, end, v, hdr, cnt, [hex(x) for x in tbl]))
    for k, e in enumerate(tbl):
        eo = off + e
        nxt = off + tbl[k + 1] if k + 1 < len(tbl) else end
        blob = d[eo:nxt]
        txt = [s for s in blob.split(b"\0") if len(s) >= 2 and all(32 <= c < 127 for c in s)]
        print("    element %d  0x%03X size %d  head %s  names %s" % (k, eo, len(blob), blob[:16].hex(" "), txt))
