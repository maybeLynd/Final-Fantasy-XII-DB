"""Every .mpk in the archive, split exactly as the arena splitter 0036B980 splits it.

Read-only over FFXII_TZA.vbf (set FF12_VBF). Layout assumed from 0036B980 (0036BA0A-0036BA45 size
check, 0036BB26-0036BC1E carve): u32 count; u32 size[count]; the table padded to a multiple of 0x40;
then, for each nonzero size in order, a 0x40-byte slot (overwritten at load by an arena block
header) followed by `size` payload bytes. The loader refuses a file whose sizes do not add up to the
block size, so the check "layout ends exactly at the file size" is the same test the engine makes.
Also compares each embedded slot-13 EFB0 payload with the loose ps2data/efb/<stem>.efb, because the
dispatcher 00378BC0 frees slot 13 and 00377DC0 requests the loose file.
Positive control: the extension census lists 550 .mpk entries.
FABLE, 2026-09-12.
"""
import sys, os, io, struct, zlib, collections, hashlib
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


paths = sorted(p for p in names if p.lower().endswith(".mpk"))
efb = {p.split("/")[-1][:-4].lower(): p for p in names if p.lower().startswith("ps2data/efb/") and p.lower().endswith(".efb")}
print("control: .mpk entries in the archive index:", len(paths), "(published 550)")
C = collections.Counter
counts = C(); exact = 0; bad = []; present = C(); magic = collections.defaultdict(C); sizes = collections.defaultdict(list)
slot_zero = C(); combos = C(); efb_cmp = C()
for p in paths:
    d = read_all(p)
    n = struct.unpack_from("<I", d, 0)[0]
    counts[n] += 1
    sz = struct.unpack_from("<%dI" % n, d, 4)
    pos = ((n + 1) * 4 + 0x3F) & ~0x3F
    have = []
    for i, s in enumerate(sz):
        if not s:
            continue
        have.append(i)
        present[i] += 1
        slot_zero[d[pos:pos + 0x40] == bytes(0x40)] += 1
        payload = d[pos + 0x40:pos + 0x40 + s]
        magic[i][payload[:4]] += 1
        sizes[i].append(s)
        if i == 13:
            stem = p.split("/")[-1][:-4].lower()
            if stem in efb:
                loose = read_all(efb[stem])
                efb_cmp["identical to the loose .efb" if loose == payload else "differs from the loose .efb"] += 1
                efb_cmp["loose file larger" if len(loose) > len(payload) else "loose file not larger"] += 1
                efb_cmp["same 8-byte signature" if loose[:8] == payload[:8] else "different signature"] += 1
            else:
                efb_cmp["no loose .efb with this stem"] += 1
        pos += 0x40 + s
    combos[tuple(have)] += 1
    if pos == len(d):
        exact += 1
    else:
        bad.append((p, pos, len(d)))
print("count field:", dict(counts), "; layout ends exactly at the file size:", exact, bad[:3])
print("the 0x40 slot before each payload is all zero:", dict(slot_zero))
for i in sorted(present):
    ss = sorted(sizes[i])
    print("slot %2d  in %3d files  size %d..%d (median %d)  first bytes %s"
          % (i, present[i], ss[0], ss[-1], ss[len(ss) // 2], [(k.hex(), v) for k, v in magic[i].most_common(3)]))
print("slots never present:", [i for i in range(32) if i not in present])
print("embedded slot-13 EFB0 against ps2data/efb:", dict(efb_cmp), "; loose .efb files:", len(efb))
print("most common slot sets:", combos.most_common(6))
