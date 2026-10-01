"""RC-30 follow-through: who reads the loaded loca_*.cl2, and which header fields (SWE2-DATA 2026-09-30), static +
shipped data.

003C1F00 keeps the requested .cl2 buffer at world-map widget +0x118 (rc30c_data_fields.py S3). The widget-module
+0x118 census (tools/dispscan.py 118 118 over 003B0000-003D0000) has one reader besides the release: 003C26C0, which
takes [widget + 0x118] (else the fallback [widget + 0x110]) as a CLUT for a location-map image:
  0024A9E0(buf, 0) returns buf + 0x10 (the picture header; the loop steps u32 sizes while k < u16 [buf + 6]);
  rdi = pic + u16 [pic + 0xC] + u32 [pic + 8]  = the palette (header size + image size);
  esi = u16 [pic + 0xE]                        = the colour count;
  0024A480(image, name, kind, palette = rdi, count = esi) registers the image with that external palette, and
  0024A1D0 later copies the palette in 64-byte groups for the upload (0024A2E0 onward).
So the CLT2 file is a TIM2-shaped container: +6 u16 picture count, picture header at +0x10 with +0x10 u32 total
size (the page's 'endOff'), +0x14 u32 CLUT size ('dataSize'), +0x18 u32 image size (0), +0x1C u16 header size
('fieldLo' = 0x30), +0x1E u16 colour count, and the palette at +0x10 + 0x30 + 0 = +0x40.
Checks: P1 the reader pins; P2 the container helper pins; D1 in all 20 shipped .cl2: u16 [+6] = 1, pic + u16[pic+0xC] +
u32[pic+8] = +0x40 and u32 [pic] = 0x30 + CLUT size; D2 +0x22 / +0x23 ('kindLo' / 'kindHi') are not read by 003C26C0
or 0024A9E0 (no access at pic + 0x12 / + 0x13). Control C1: the same TIM2 reading fits the shipped loca_00.tm2
(magic 'TIM2', u16 [+6] >= 1, picture total = header + image + CLUT).
"""
import os, re, struct, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import dis  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


r = {x.address: x for x in dis(0x003C26C0)}
pins = [(0x003C2794, "rcx, qword ptr [r13 + 0x118]"), (0x003C27A0, "rcx, qword ptr [r13 + 0x110]"),
        (0x003C27A9, "0x24a9e0"), (0x003C27B0, "ecx, word ptr [rax + 0xc]"), (0x003C27B4, "edi, dword ptr [rax + 8]"),
        (0x003C27B7, "esi, word ptr [rax + 0xe]"), (0x003C27BB, "rax, rcx"), (0x003C27C1, "rdi, rax"),
        (0x003C281D, "r9, rdi"), (0x003C2820, "dword ptr [rsp + 0x20], esi"), (0x003C2824, "0x24a480")]
for a, s in pins:
    print("   %08X %s %s" % (a, r[a].mnemonic, r[a].op_str))
check("P1 003C26C0 reads the .cl2 at widget +0x118 and hands palette / count to 0024A480",
      all(r[a].op_str == s for a, s in pins), str([hex(a) for a, s in pins if r[a].op_str != s]))
h = {x.address: x for x in dis(0x0024A9E0)}
check("P2 0024A9E0: picture 0 = buf + 0x10, count u16 [buf + 6], later pictures step u32 [pic]",
      h[0x0024A9E0].op_str == "rax, [rcx + 0x10]" and h[0x0024A9E4].op_str == "ecx, word ptr [rcx + 6]"
      and h[0x0024A9F2].op_str == "ecx, dword ptr [rax]")
allops = [x.op_str for x in dis(0x003C26C0)] + [x.op_str for x in dis(0x0024A9E0)]
check("D2 no read of pic + 0x12 / + 0x13 (the +0x22 / +0x23 bytes) in 003C26C0 or 0024A9E0",
      not any(re.search(r"\[rax \+ 0x1[23]\]", o) for o in allops))
EX = "D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok"
files = sorted(glob.glob(EX + "/*/bin_menu/loca_*.cl2"))
ok = 0
for f in files:
    b = open(f, "rb").read()
    cnt = struct.unpack_from("<H", b, 6)[0]
    pic = 0x10
    tot, clut, img = struct.unpack_from("<III", b, pic)
    hs, ncol = struct.unpack_from("<HH", b, pic + 0xC)
    pal = pic + hs + img
    ok += cnt == 1 and pal == 0x40 and tot == hs + clut and len(b) - 0x40 == clut and clut == ncol * 4
check("D1 all shipped .cl2 read as TIM2-shaped: one picture, palette at +0x40, total = header + CLUT, CLUT = count x 4",
      ok == len(files) and len(files) == 20, "%d / %d" % (ok, len(files)))
t = open(EX + "/us/worldmap/bin/areatim2/loca_00.tm2", "rb").read() if os.path.exists(
    EX + "/us/worldmap/bin/areatim2/loca_00.tm2") else open(glob.glob(EX + "/*/worldmap/bin/areatim2/loca_00.tm2")[0], "rb").read()
ttot, tclut, timg = struct.unpack_from("<III", t, 0x10)
ths = struct.unpack_from("<H", t, 0x1C)[0]
check("C1 the same picture-header reading fits a shipped TIM2 (loca_00.tm2): total = header + image + CLUT",
      t[:4] == b"TIM2" and struct.unpack_from("<H", t, 6)[0] >= 1 and ttot == ths + timg + tclut,
      "%s count %d header %#x image %#x clut %#x total %#x" % (t[:4], struct.unpack_from("<H", t, 6)[0], ths, timg, tclut, ttot))
print("FAILS %d" % FAILS)
