"""sd2_check.py - SD-2: what the R2 label widget 00366B80 draws from battle_4_c (OPUS, 2026-09-30).
W1-W4 are static reads of the certified image (Database/Tools/analysis-kit/gfz-scripts/retool.py); D1-D3 read the
shipped data (FFXII_TZA.vbf through agent_flow/tools/vbfextract.py). D3 also writes battle_4_c-letters.png, the
atlas's letter cells, beside this file.
"""
import io, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, os.path.join(REPO, "agent_flow", "tools"))
import retool as T  # noqa: E402
import vbfextract as V  # noqa: E402

VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
R = T.R
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return i.address + i.size + int(i.op_str.split("rip + ")[1].split("]")[0], 16)


# W1 - the construct arm binds layout record 0xC of the package at [0209AC30]+8 (002432B0(w+0x50, pkg, 0xC, w)) and
#      looks up its atlas by the name pointer [01E0C1E8] (0024A5A0)
check("W1", rip(0x00367044) == 0x0209AC30 and txt(0x0036704B) == "lea rcx, [rdi + 0x50]" and txt(0x00367052) == "mov r8d, 0xc"
      and txt(0x00367058) == "mov rdx, qword ptr [rax + 8]" and txt(0x0036705C) == "call 0x2432b0"
      and rip(0x003670C6) == 0x01E0C1E8 and txt(0x003670DC) == "call 0x24a5a0" and T.cstr(struct.unpack("<Q", R.at(0x01E0C1E8, 8))[0]) == "battle_4_c",
      "construct: record 0xC of [[0209AC30]+8], atlas named battle_4_c")
# W2 - 002432B0 stores the record at w+0x58 (r15+8) and an item pointer array at w+0x60 (r15+0x10) for all count & 0x3FF
#      items
check("W2", txt(0x00243305) == "mov qword ptr [r15 + 8], r12" and txt(0x002432E3) == "and esi, 0x3ff"
      and txt(0x002433AA) == "mov qword ptr [r15 + 0x10], rax" and txt(0x002433E4) == "mov qword ptr [rsi + rcx], rbx",
      "binder: +0x58 = record, +0x60 = item pointers")
# W3 - the draw arm (message 4) walks items while the index is below record +0xC, revealing item i once the toggle
#      block's counter (<< 8) passes i x (threshold 022CBE08 x 128) / (+0xC + 1)
check("W3", txt(0x00366C78) == "cmp dword ptr [rax + 0xc], ebx" and txt(0x00366ED5) == "cmp esi, dword ptr [rax + 0xc]"
      and txt(0x00366ED8) == "jb 0x366cc0" and rip(0x00366CE6) == 0x022CBE08 and txt(0x00366CF0) == "shl r10d, 7"
      and txt(0x00366CFA) == "inc ecx" and txt(0x00366D01) == "div ecx" and txt(0x00366C71) == "shl ebp, 8",
      "draw: items 0 .. record+0xC-1, revealed in step with the arming counter")
# W4 - package slot +0x08 is mrppack_ys unit 1 (00280980 fills 8-byte slots from unit 0, per gen_atlas_name_census.py),
#      and tex2pack_ys directory entry 0 is bound to the name at [01E0C1E8]: 00280750 registers slot +0x338 from it and
#      00280670 binds slot +0x338 to directory offset 0
check("W4", rip(0x00280785) == 0x01E0C1E8 and txt(0x0028078C) == "mov qword ptr [r11 - 0x68], rax" and txt(0x002807E8) == "mov ebx, 0x338"
      and txt(0x002807F1) == "lea rdi, [r11 - 0x68]" and txt(0x0028068E) == "mov ebx, 0x338" and txt(0x00280698) == "xor edi, edi"
      and txt(0x002806B0) == "mov edx, dword ptr [rdi + rax]" and txt(0x002806B6) == "call 0x24a1d0",
      "battle_4_c = tex2pack_ys directory entry 0")

f = io.open(VBF, "rb")
names, blocks = V.load_index(f)
pk = V.read_entry(f, names, blocks, "ps2data/image/ff12/myoshiok/us/packfiles/mrppack_ys.bin")
offs = []
for i in range(0, 0x100, 4):
    v = U32(pk, i)
    if v == 0xFFFFFFFF:
        break
    offs.append(v)
u1 = pk[offs[1]:offs[2]]
n, toff = U32(u1, 0x1C), U32(u1, 0x20)
rec12 = toff + 20 * 12
counts = [U32(u1, toff + 20 * i) & 0x3FF for i in range(n)]
pos, items = toff + 20 * n, []
for r in range(n):
    for _ in range(counts[r]):
        if r == 12:
            items.append(u1[pos:pos + u1[pos]])
        pos += u1[pos]
na = U32(u1, 0x08)
atlas = lambda k: u1[na + 16 * k: na + 16 * k + 16].split(b"\0")[0].decode()
cells = [U16(it, 0x10) for it in items]
# D1 - us unit 1, record 12: 12 items, of which the record's +0xC draws 7
check("D1", counts[12] == 12 and U32(u1, rec12 + 0xC) == 7, "record 12: %d items, +0xC = %d" % (counts[12], U32(u1, rec12 + 0xC)))
# D2 - the seven drawn items are type 2 in atlas battle_4_c, 46 x 42 at y 14, x 390 .. 597, cells 0 1 2 2 5 6 7
check("D2", all(it[1] == 2 and atlas(U16(it, 0x0C)) == "battle_4_c" and U16(it, 8) == 46 and U16(it, 10) == 42 for it in items[:7])
      and [U16(it, 4) for it in items[:7]] == [390, 425, 460, 496, 536, 557, 597] and cells[:7] == [0, 1, 2, 2, 5, 6, 7],
      "drawn items: battle_4_c cells %s" % cells[:7])
# D3 - battle_4_c (tex2pack_ys entry 0, 1024 x 512, 8-bit indexed) carries eight letter cells in rows of three at its
#      lower left: F L E / A P I / N G. Read row-major, cells 0 1 2 2 5 6 7 are F L E E I N G. The crop is written for
#      the reader; the letter reading is by eye (inference), the cell order is the row-major reading.
tp = V.read_entry(f, names, blocks, "ps2data/image/ff12/myoshiok/us/packfiles/tex2pack_ys.bin")
o = U32(tp, 0)
ts, cs, isz, hs, cc = struct.unpack_from("<IIIHH", tp, o + 0x10)
it, w, h = tp[o + 0x23], U16(tp, o + 0x24), U16(tp, o + 0x26)
check("D3", tp[o:o + 4] == b"TIM2" and (w, h, it) == (1024, 512, 5), "battle_4_c: TIM2 %d x %d, image type %d" % (w, h, it))
try:
    from PIL import Image
    px = tp[o + 0x10 + hs: o + 0x10 + hs + isz]
    clut = tp[o + 0x10 + hs + isz: o + 0x10 + hs + isz + cs]
    pal = [struct.unpack_from("<BBBB", clut, 4 * i) for i in range(len(clut) // 4)]
    out = list(pal)
    for b in range(0, len(pal), 32):      # PS2 CSM1 palette order
        for k in range(8):
            out[b + 8 + k], out[b + 16 + k] = pal[b + 16 + k], pal[b + 8 + k]
    x0, y0, x1, y1 = 0, 384, 144, 512
    img = Image.new("RGBA", (x1 - x0, y1 - y0))
    img.putdata([(lambda c: (c[0], c[1], c[2], 255 if c[3] >= 0x40 else c[3] * 4))(out[px[y * w + x]])
                 for y in range(y0, y1) for x in range(x0, x1)])
    img.save(os.path.join(HERE, "battle_4_c-letters.png"))
    print("      wrote battle_4_c-letters.png (atlas x 0..144, y 384..512)")
except ImportError:
    print("      PIL not available; crop not written")
print("FAILS %d" % fails)
