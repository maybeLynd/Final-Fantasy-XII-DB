"""FCP section 4: the trail descriptors. Census of the 0x50-byte descriptor read by 0051CC30 / 0051C3C0 / 0051BC70.

Read from code (2026-09-19, FABLE):
  section 4 = u32 count (capped at 4 by 003E6770), descriptors from +0x10, 0x50 bytes each.
  descriptor  +0x00 u8  ownImage   (0051BE6A: non-zero -> bind the image that follows the descriptors)
              +0x02 u16 bone       (0051C504 -> 00422170)
              +0x04 u16 ownerRecord (written by the builder at run time; expected 0 or filler in the file)
              +0x08 f32 -> uploaded at parameter +0x10 (0051C18F)
              +0x0C f32 -> entry +0x14 each update (0051CA67), uploaded at parameter +0x08
              +0x10 4 x f32[4] -> uploaded (0051C19F..0051C1DE)
  image header at section + 0x10 + n x 0x50 when ownImage: u16 +2 pixel offset, u16 +4 second offset,
              bytes +9..+0xF format / log2 sizes (0051BEDE..0051BF80)

Predictions that could fail:
  Q1  bone < 256 in every descriptor
  Q2  floats +8, +0xC finite and the four vectors finite
  Q3  when any descriptor has ownImage != 0, bytes remain after the descriptors inside the payload for a header
"""
import os, struct, glob, math, collections

ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
files = glob.glob(os.path.join(ROOT, "**", "*.cm"), recursive=True)
blocks = have4 = descs = 0
own = collections.Counter(); bones = collections.Counter(); w4 = collections.Counter()
f8 = collections.Counter(); fC = collections.Counter(); vecs = [collections.Counter() for _ in range(4)]
bad = 0; pad = collections.Counter(); q3_need = q3_ok = 0; nextsec = collections.Counter()
hdr = collections.Counter(); folder_own = collections.Counter()
for path in files:
    d = open(path, "rb").read()
    i = d.find(b"@FCP")
    if i < 0:
        continue
    size = struct.unpack_from("<I", d, i + 8)[0]
    pay = d[i + 0x30: i + size]
    if len(pay) < 0x40:
        continue
    blocks += 1
    offs = list(struct.unpack_from("<18H", pay, 0))
    o4 = offs[4]
    if not o4:
        continue
    have4 += 1
    n = min(struct.unpack_from("<I", pay, o4)[0], 4)
    pad[pay[o4 + 4: o4 + 0x10].hex()] += 1
    any_own = False
    for k in range(n):
        b = o4 + 0x10 + k * 0x50
        descs += 1
        o = pay[b]; any_own |= bool(o)
        own[o] += 1
        bone = struct.unpack_from("<H", pay, b + 2)[0]
        bones[bone] += 1
        w4[struct.unpack_from("<H", pay, b + 4)[0]] += 1
        a, c = struct.unpack_from("<2f", pay, b + 8)
        f8[round(a, 3)] += 1; fC[round(c, 3)] += 1
        v = struct.unpack_from("<16f", pay, b + 0x10)
        if not all(math.isfinite(x) and abs(x) < 1e5 for x in (a, c) + v):
            bad += 1
        for j in range(4):
            vecs[j][tuple(round(x, 2) for x in v[4 * j: 4 * j + 4])] += 1
    end = o4 + 0x10 + n * 0x50
    later = sorted((o, k) for k, o in enumerate(offs) if k != 4 and o >= end)
    nextsec[later[0][1] if later and later[0][0] == end else ("none-adjacent" if later else "end")] += 1
    if any_own:
        q3_need += 1
        q3_ok += (len(pay) - end >= 0x10)
        hdr[pay[end + 9: end + 0x10].hex()] += 1
        folder_own[os.path.relpath(path, ROOT).replace(os.sep, "/").split("/")[3]] += 1

top = lambda c, k=8: sorted(c.items(), key=lambda kv: -kv[1])[:k]
print("control: FCP blocks", blocks, "(published 1,066); with a section 4:", have4, "(published 216); descriptors:", descs)
print("header bytes +4..+0xF of the section (hex -> blocks):", top(pad, 4))
print("ownImage byte +0 (value -> descriptors):", sorted(own.items()))
print("Q1  bone word +2 (value -> descriptors):", sorted(bones.items()), "; max", max(bones))
print("    word +4 in the file (value -> descriptors):", top(w4, 6))
print("Q2  descriptors with a non-finite or huge float:", bad)
print("    float +8  (value -> descriptors):", top(f8))
print("    float +0xC (value -> descriptors):", top(fC))
for j in range(4):
    print("    vector", j, "at +0x%02X (value -> descriptors):" % (0x10 + 0x10 * j), top(vecs[j], 5))
print("Q3  blocks with an ownImage descriptor:", q3_need, "; of those with >= 0x10 bytes after the descriptors:", q3_ok, "; by folder:", top(folder_own))
print("    section that starts exactly where the descriptors end (index -> blocks):", sorted(nextsec.items(), key=lambda kv: str(kv[0])))
print("    image header bytes +9..+0xF where ownImage (hex -> blocks):", top(hdr, 6))

# who carries them: (folder, bones, float +0xC) -> models
seen = collections.defaultdict(set)
for path in files:
    d = open(path, "rb").read()
    i = d.find(b"@FCP")
    if i < 0:
        continue
    size = struct.unpack_from("<I", d, i + 8)[0]
    pay = d[i + 0x30: i + size]
    if len(pay) < 0x40:
        continue
    o4 = struct.unpack_from("<18H", pay, 0)[4]
    if not o4:
        continue
    n = min(struct.unpack_from("<I", pay, o4)[0], 4)
    bs = tuple(struct.unpack_from("<H", pay, o4 + 0x10 + k * 0x50 + 2)[0] for k in range(n))
    fs = tuple(round(struct.unpack_from("<f", pay, o4 + 0x10 + k * 0x50 + 0xC)[0], 2) for k in range(n))
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/").split("/")
    seen[(rel[3], bs, fs)].add(rel[-1])
print("who carries them - (folder, bones, float +0xC) -> models, first six names:")
for k, v in sorted(seen.items(), key=lambda kv: -len(kv[1])):
    print("   ", k, len(v), sorted(v)[:6])
