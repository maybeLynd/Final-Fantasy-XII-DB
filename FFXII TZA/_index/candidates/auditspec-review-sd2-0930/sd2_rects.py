"""sd2_rects.py - SWE2-AUDIT-SPEC independent decode of the SD-2 item -> atlas-rectangle mapping (2026-09-30).

Written without the package's parser. Reads the full extract tree D:/FFXII_TZA_extract (and hashes it against the
VBF copies the package read), parses mrppack_ys unit 1 record 12 by the RECORD's own row-relative +0x10 offset (the
package walks items sequentially from the end of table A instead), and resolves each type-2 item to its atlas
rectangle the way the image does it:

  constructor 0029F4C0: T = [atlas+0x20] + 0x30 ; page = u16[T+0x14+(code>>8)*2] ; entry = u16[T+0x14+(page+(code&0xFF))*2]
                        node+0x20 = T + u16[T+0x10] + entry*8 ; node+0xA = item u16 +0x10 (frame)
  draw helper 00366A30: rec = node+0x20 + (s16)node+0xA * 8 ; x = u16 rec+0, y = u16 rec+2,
                        w = u16 rec+4 & 0xFFF, h = (u32 rec+4 >> 12) & 0xFFF
  slot image  0024A1D0: [slot+0x20] = image buffer + 0x10 (the TIM2 picture header), so T = TIM2 file + 0x40.

Writes rect_<i>.png crops and rects_strip.png (drawn items in draw order) into this folder.
"""
import hashlib, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
EXT = r"D:\FFXII_TZA_extract\ps2data\image\ff12\myoshiok"
VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
S16 = lambda b, o: struct.unpack_from("<h", b, o)[0]
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]


# H - the extract tree vs the VBF copies, every language, both files
sys.path.insert(0, os.path.join(REPO, "agent_flow", "tools"))
import vbfextract as V  # noqa: E402  (read-only use of the archive reader)
f = open(VBF, "rb")
names, blocks = V.load_index(f)
langs = sorted(d for d in os.listdir(EXT) if os.path.isfile(os.path.join(EXT, d, "packfiles", "mrppack_ys.bin")))
same = 0
for lg in langs:
    for fn in ("mrppack_ys.bin", "tex2pack_ys.bin"):
        a = open(os.path.join(EXT, lg, "packfiles", fn), "rb").read()
        b = V.read_entry(f, names, blocks, "ps2data/image/ff12/myoshiok/%s/packfiles/%s" % (lg, fn))
        same += a == b
        if lg == "us":
            print("      us/%s extract %s  vbf %s  %d B" % (fn, sha(a), sha(b), len(a)))
check("H", same == 2 * len(langs), "extract == VBF copy for %d of %d files (%d languages)" % (same, 2 * len(langs), len(langs)))

pk = open(os.path.join(EXT, "us", "packfiles", "mrppack_ys.bin"), "rb").read()
tp = open(os.path.join(EXT, "us", "packfiles", "tex2pack_ys.bin"), "rb").read()

# P - unit slicing: u32 offsets at the pack head until 0xFFFFFFFF
offs = []
for i in range(0, 0x200, 4):
    v = U32(pk, i)
    if v == 0xFFFFFFFF:
        break
    offs.append(v)
u1 = pk[offs[1]:offs[2]]
check("P", u1[:3] == b"MRP", "unit 1 at 0x%X..0x%X, magic %r, %d units" % (offs[1], offs[2], u1[:4], len(offs)))

ndesc, toff, nameoff = U32(u1, 0x1C), U32(u1, 0x20), U32(u1, 0x08)
rec = toff + 20 * 12
d0, ref = U32(u1, rec), U32(u1, rec + 0x10)
cnt = d0 & 0x3FF
istart = rec + ref                      # row-relative (002A1AC3..002A1AD9)
items, p = [], istart
for _ in range(cnt):
    items.append(u1[p:p + u1[p]])
    p += u1[p]
print("      record 12: dword0 0x%08X count %d  +4 %08X +8 %08X +0xC %d  items at unit+0x%X" %
      (d0, cnt, U32(u1, rec + 4), U32(u1, rec + 8), U32(u1, rec + 0xC), istart))
check("R", cnt == 12 and U32(u1, rec + 0xC) == 7, "record 12 by its own +0x10: %d items, +0xC = %d" % (cnt, U32(u1, rec + 0xC)))

atl = lambda k: u1[nameoff + 16 * k: nameoff + 16 * k + 14].split(b"\0")[0].decode()

o = U32(tp, 0)                          # directory entry 0 (00280670: buffer = pack + u32[pack + 4k])
tim = tp[o:]
H = 0x10
tsz, csz, isz, hsz, ccol = struct.unpack_from("<IIIHH", tim, H)
w, h, itype = U16(tim, H + 0x14), U16(tim, H + 0x16), tim[H + 0x13]
T = H + 0x30
print("      tex2pack entry 0: %r at 0x%X, picture header size 0x%X, image %d x %d type %d, user data %d B" %
      (tim[:4], o, hsz, w, h, itype, hsz - 0x30))
check("T", tim[:4] == b"TIM2" and hsz > 0x30, "atlas carries user data past the 0x30 picture header (the sub-image table)")
roff = U16(tim, T + 0x10)


def rect(code, frame):
    page = U16(tim, T + 0x14 + (code >> 8) * 2)
    entry = U16(tim, T + 0x14 + (page + (code & 0xFF)) * 2)
    r = T + roff + (entry + frame) * 8
    x, y, wh = U16(tim, r), U16(tim, r + 2), U32(tim, r + 4)
    return entry, (x, y, wh & 0xFFF, (wh >> 12) & 0xFFF, tim[r + 7])


print("      i  type atlas         dst x,y   w x h   code frame  -> entry  src x,y   w x h  op")
rows = []
for i, it in enumerate(items):
    ty = it[1]
    line = "      %-2d %-4d " % (i, ty)
    if ty in (2, 9):
        code, fr = U16(it, 0xE), S16(it, 0x10)
        e, rc = rect(code, fr)
        rows.append((i, rc))
        line += "%-13s %4d,%-4d %3d x %-3d 0x%04X %-5d -> %-5d %4d,%-4d %3d x %-3d %02X" % (
            atl(U16(it, 0xC)), S16(it, 4), S16(it, 6), U16(it, 8), U16(it, 0xA), code, fr, e, *rc)
    print(line)

drawn = [rc for i, rc in rows if i < 7]
check("B", all(0 <= x and x + ww <= w and 0 <= y and y + hh <= h for x, y, ww, hh, _ in drawn),
      "the seven drawn rectangles lie inside the %d x %d atlas" % (w, h))

# L - the drawn rectangles tile the lower-left letter block; print where each sits in a 3-wide grid
xs = sorted({r[0] for r in drawn}); ys = sorted({r[1] for r in drawn})
print("      distinct src x %s, distinct src y %s" % (xs, ys))

try:
    from PIL import Image
    px = tim[H + hsz: H + hsz + isz]
    clut = tim[H + hsz + isz: H + hsz + isz + csz]
    pal = [struct.unpack_from("<BBBB", clut, 4 * i) for i in range(len(clut) // 4)]
    out = list(pal)
    for b in range(0, len(pal), 32):          # CSM1 order
        for k in range(8):
            out[b + 8 + k], out[b + 16 + k] = pal[b + 16 + k], pal[b + 8 + k]
    col = lambda c: (c[0], c[1], c[2], 255 if c[3] >= 0x40 else c[3] * 4)
    crops = []
    for i, (x, y, ww, hh, _) in rows:
        im = Image.new("RGBA", (ww, hh))
        im.putdata([col(out[px[(y + yy) * w + x + xx]]) for yy in range(hh) for xx in range(ww)])
        im.save(os.path.join(HERE, "rect_%02d.png" % i))
        crops.append((i, im))
    sel = [im for i, im in crops if i < 7]
    strip = Image.new("RGBA", (sum(im.width + 4 for im in sel), max(im.height for im in sel)), (40, 40, 40, 255))
    xx = 0
    for im in sel:
        strip.paste(im, (xx, 0), im)
        xx += im.width + 4
    strip = strip.resize((strip.width * 3, strip.height * 3))
    strip.save(os.path.join(HERE, "rects_strip.png"))
    rest = [im for i, im in crops if i >= 7]
    if rest:
        s2 = Image.new("RGBA", (sum(im.width + 4 for im in rest), max(im.height for im in rest)), (40, 40, 40, 255))
        xx = 0
        for im in rest:
            s2.paste(im, (xx, 0), im)
            xx += im.width + 4
        s2.resize((s2.width * 3, s2.height * 3)).save(os.path.join(HERE, "rects_strip_7_11.png"))
    print("      wrote rect_NN.png, rects_strip.png (items 0..6), rects_strip_7_11.png")
except ImportError:
    print("      PIL not available")
print("FAILS %d" % fails)
