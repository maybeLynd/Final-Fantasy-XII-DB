"""sd123_formats.py - SWE2-AUDIT-SPEC (review of OPUS 524d5aacd, 2026-09-30). Shipped-data histogram of the kind-0x52
record's format byte, and a size control that tests the loader's field offsets against every record.

Own walker (not type_census.py): every EFX stream ('EFX0010'/'EFX0009'/'EFX0008' magic, stream size at +0xC) in every
.efx/.efb under D:/FFXII_TZA_extract/ps2data plus the embedded-stream files listed in
17-Presentation-Rendering/Effect-File-Formats/members/efx-embedded-stream-files.txt (read-only input). Chunks
{u32 length, u16 flag 0x100, u16 type} from stream +0x10. A 0xB00 chunk with kind byte +0xE == 0x52 is a kind-0x52
record; its payload is chunk+0x10 (kind-54 page s1).

Payload fields as the loader 00500C00 reads them (rbx = payload): +0 format byte, +2 palette count, +4/+6 -> +0x1CC/+0x1CE,
+8/+0xA -> +0xA8/+0xAA (copied to +0xA4/+0xA6, the pair every live surface arm sizes by), palettes from +0x10.

Size control (sensitive to wrong offsets or a wrong bytes-per-pixel reading): predicted =
  0x10 + count * (64 if fmt&0x3F == 0 else 1024 if fmt&0x3F == 1 else 0) + w*h*bpp(fmt&0x3F), bpp = 0.5,1,2,3,4 for 0..4
must lie within [payload - 15, payload] (16-byte padding). Known positive: the kind census total 13,161.
"""
import os, struct, collections

ROOT = "D:/FFXII_TZA_extract"
HERE = os.path.dirname(os.path.abspath(__file__))
EMB = os.path.join(HERE, "..", "..", "..", "17-Presentation-Rendering", "Effect-File-Formats", "members",
                   "efx-embedded-stream-files.txt")
MAGICS = (b"EFX0010", b"EFX0009", b"EFX0008")
BPP2 = {0: 1, 1: 2, 2: 4, 3: 6, 4: 8}   # bytes per pixel x2


def chunks(b, s, e):
    c = s
    while c + 8 <= e:
        ln, fl, ty = struct.unpack_from("<IHH", b, c)
        if ln < 8 or c + ln > e or fl != 0x100:
            return
        yield ty, c, ln
        c += ln


paths = []
for dp, dn, fn in os.walk(os.path.join(ROOT, "ps2data")):
    paths += [os.path.join(dp, f) for f in fn if f.lower().endswith((".efx", ".efb"))]
paths += [os.path.join(ROOT, l.strip()) for l in open(EMB) if l.strip()]

kinds = collections.Counter()
fmt = collections.Counter()
fmt_cnt = collections.Counter()
size_ok = collections.Counter()
size_bad = collections.Counter()
bad_examples = []
bit6 = collections.Counter()
examples = {}
for p in paths:
    b = open(p, "rb").read()
    rel = os.path.relpath(p, ROOT).replace("\\", "/")
    for m in MAGICS:
        i = b.find(m)
        while i >= 0:
            sz = struct.unpack_from("<I", b, i + 0xC)[0]
            e = i + sz if 0x10 <= sz and i + sz <= len(b) else len(b)
            last = i + 0x10
            for ty, c, ln in chunks(b, i + 0x10, e):
                last = c + ln
                if ty != 0xB00:
                    continue
                k = b[c + 0xE]
                kinds[k] += 1
                if k != 0x52:
                    continue
                pl = c + 0x10
                plen = ln - 0x10
                f = b[pl]
                n = b[pl + 2]
                w, h = struct.unpack_from("<HH", b, pl + 8)
                fmt[f] += 1
                fmt_cnt[(f, n)] += 1
                bit6[(f >> 6) & 1] += 1
                examples.setdefault(f, "%s @%X w=%d h=%d n=%d" % (rel, c, w, h, n))
                f6 = f & 0x3F
                if f == 0xFF:
                    pred = 1
                elif f6 in BPP2:
                    pal = n * (64 if f6 == 0 else 1024 if f6 == 1 else 0)
                    pred = 0x10 + pal + (w * h * BPP2[f6]) // 2
                else:
                    pred = None
                if pred is not None and plen - 15 <= pred <= plen:
                    size_ok[f] += 1
                else:
                    size_bad[f] += 1
                    if len(bad_examples) < 12:
                        bad_examples.append("%s @%X fmt=%02X n=%d w=%d h=%d payload=%d pred=%s" % (rel, c, f, n, w, h, plen, pred))
            i = b.find(m, max(last, i + 1))

print("files walked %d" % len(paths))
print("0xB00 kind histogram:", {"0x%X" % k: v for k, v in sorted(kinds.items())})
print("kind 0x52 records: %d" % kinds[0x52])
print("format byte histogram:", {"0x%02X" % k: v for k, v in sorted(fmt.items())})
print("(format, palette count) histogram:", {"0x%02X/%d" % k: v for k, v in sorted(fmt_cnt.items())})
print("bit 6 of format:", dict(bit6))
print("size control: ok", {"0x%02X" % k: v for k, v in sorted(size_ok.items())},
      "bad", {"0x%02X" % k: v for k, v in sorted(size_bad.items())})
for x in bad_examples:
    print("  bad:", x)
for k, v in sorted(examples.items()):
    print("  example fmt 0x%02X: %s" % (k, v))
