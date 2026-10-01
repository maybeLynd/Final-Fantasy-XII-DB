"""DD residue batch 11 (SWE2-STRUCT for OPUS, 2026-09-30): checks behind the two residue sentences this batch answers.

Run: python -B b11_struct.py [--png DIR]   (FAILS 0)      archive: $FF12_VBF, else the Steam install path below
     --png DIR also writes the label crops (one per language pack) and the digit strips as PNGs, for a visual read.

Page 1 - 07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md, section 8 GR-3: "Which glyph the label is
stays unread."
  C1  00280750 registers ten atlas names into [0209AC30]+0x338..+0x380, step 8, from a stack array it fills from the
      name block 01E0C1E0..; slot +0x338 = battle_4_c, slot +0x360 = partytop_4_c (control: +0x368 = partytop_8_c,
      the _00A0 block's texture in the hud-blocks record)
  C2  00280670 binds tex2pack_ys directory entry i to slot +0x338 + 8i (0024A1D0), in lockstep
  C3  the getters: 0035D460 -> +0x338, 0035D470 -> +0x360, 0035D480 -> +0x368
  C4  0028AAA0's label: the atlas from 0035D460, T = [atlas+0x20] + 0x30, page = u16[T+0x14], entry =
      u16[T+0x16+page*2] (code 0x0001), record = T + u16[T+0x10] + entry*8, then +0x70 (frame 14); +0x74 read as w/h
  C5  0028AAA0's digits: the atlas from 0035D470, code = 1 at the cap (count >= 0x12) else 2, frame = the digit
  C6  control: the types 2/9 constructor 0029F4C0 uses the same two-level lookup
  D1  the ten tex2pack_ys.bin packs in the archive: 11 directory slots, entries 0..9 TIM2, entry 0 = the 1024x512
      battle_4_c picture (in_sdver: its own low-resolution pack)
  D2  code 0x0001 frame 14 of entry 0 is the 130x60 cell at (120, 0) in all nine full-resolution packs; in_sdver's is
      37x17 at (126, 38)
  D3  control: partytop_4_c (entry 5) codes 1 and 2 are strips of ten equal digit cells (36x50 at y 273, 28x38 at
      y 331), which only a correct lookup produces; frame 13 of the label code is a 16x16 placeholder at (0, 0)
  D4  the label pixels differ by language group: us, de, fr, es, it, and one shared picture for in/kr/ch/cn (six
      full-resolution pictures; the index bytes are hashed); the words are read visually from the --png crops

Page 3 - 12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md, crossings: "The transaction driver
calls the family's counter updater after a transaction (0056D4D2); this page does not read what it counts."
  S1  the sale arm of 0056D370: after Shop_CommitSaleItemAndGil 00310870, counter 14 with the quantity word +0xDC,
      only when (+0xE4 & 0x3FC0) == 0x1C0
  S2  the purchase arm: after Shop_CommitPurchaseItemAndGil 002FEEB0, counter 19 with the bought row's id word +8,
      on every purchase (the 0x2C0 test guards only the 0030B630 call)
  S3  00316A50: bound 30, kind-0 trigger path, mode 1 fires only when the amount equals the threshold, then sets the
      award bit at block +0x3844
  S4  descriptors 00D10460: 19 = {kind 0, mode 1, threshold 53375 = 0xD07F}; 14 = {kind 2, offset 0x0C, mode 0}
  S5  the achievement records 01DFE410 + slot*0x198: counter 14 = ACH_COUNT_SELL_EVITEM "Privateer", counter 19 =
      ACH_SPECIAL_HORIDASHI "Collector" (control: slot 19 = {13, ACH_COMPLETE_YUGOU, "Mist Walker"}, as the
      catalogue page records)
"""
import hashlib, os, struct, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

VBF = os.environ.get("FF12_VBF", r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf")
PNG = sys.argv[sys.argv.index("--png") + 1] if "--png" in sys.argv else None
FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


_bodies = {}


def body(f):
    if f not in _bodies:
        _bodies[f] = {i.address: i for i in T.R.md.disasm(T.R.at(f, T.sizes()[f]), f)}
    return _bodies[f]


def txt(f, a):
    i = body(f).get(a)
    return "%s %s" % (i.mnemonic, i.op_str) if i else "<no instruction at %08X>" % a


def pin(name, f, a, text):
    got = txt(f, a)
    check(name, text in got, "%08X  %s" % (a, got))


def q(a):
    return struct.unpack("<Q", T.R.at(a, 8))[0]


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")

# ------------------------------------------------------------------ C1: the ten names and their slots (00280750)
F = 0x00280750
pin("C1 loop start: slot offset 0x338", F, 0x002807E8, "mov ebx, 0x338")
pin("C1 name array base r11-0x68", F, 0x002807F1, "lea rdi, [r11 - 0x68]")
pin("C1 name array indexed by the slot offset", F, 0x002807F9, "sub rdi, rbx")
pin("C1 name i loaded", F, 0x0028080E, "mov rcx, qword ptr [rdi + rbx]")
pin("C1 registry kind 2", F, 0x00280812, "mov edx, 2")
pin("C1 registered by 0024A4E0", F, 0x00280817, "call 0x24a4e0")
pin("C1 slot stored at [0209AC30]+offset", F, 0x00280823, "mov qword ptr [rbx + rcx], rax")
pin("C1 step 8", F, 0x0028082E, "add rbx, 8")
pin("C1 bound 0x388 (ten slots)", F, 0x00280832, "cmp rbx, 0x388")
# the stack array: pair each rip load of rax with the next store of rax to [r11 + d]
names = {}
pend = None
for a in sorted(body(F)):
    i = body(F)[a]
    if a > 0x00280807:
        break
    if i.mnemonic == "mov" and i.op_str.startswith("rax, qword ptr [rip"):
        g = a + i.size + i.operands[1].mem.disp
        pend = T.cstr(q(g), 64)
    elif i.mnemonic == "mov" and i.op_str.startswith("qword ptr [r11 - ") and i.op_str.endswith("], rax") and pend:
        d = -int(i.op_str.split("- ")[1].split("]")[0], 16)
        names[0x338 + (d + 0x68)] = pend
        pend = None
print("   slot names: " + ", ".join("+0x%X %s" % (k, names[k]) for k in sorted(names)))
check("C1 ten slots named, +0x338..+0x380", sorted(names) == list(range(0x338, 0x388, 8)), str(len(names)))
check("C1 slot +0x338 = battle_4_c", names.get(0x338) == "battle_4_c", str(names.get(0x338)))
check("C1 slot +0x360 = partytop_4_c", names.get(0x360) == "partytop_4_c", str(names.get(0x360)))
check("C1 control: slot +0x368 = partytop_8_c (the _00A0 texture of the hud-blocks record)",
      names.get(0x368) == "partytop_8_c", str(names.get(0x368)))
check("C1 control: the set is the loader-bound page's ten tex2pack names",
      set(names.values()) == {"targetline_p", "battle_4_c", "battle_4_p", "partytop_4_c", "partytop_8_c", "icons_c",
                              "extra_c", "s_font_c", "mini_face_c", "party_grd_2"})
ORDER = [names[k] for k in sorted(names)]

# ------------------------------------------------------------------ C2: the binder's lockstep (00280670)
F = 0x00280670
pin("C2 slot offset 0x338", F, 0x0028068E, "mov ebx, 0x338")
pin("C2 directory index 0", F, 0x00280698, "xor edi, edi")
pin("C2 slot read", F, 0x002806A0, "mov rcx, qword ptr [rbx + rdx]")
pin("C2 the tex2pack blob +0x3D8", F, 0x002806A9, "mov rax, qword ptr [rdx + 0x3d8]")
pin("C2 directory entry i", F, 0x002806B0, "mov edx, dword ptr [rdi + rax]")
pin("C2 bound by 0024A1D0", F, 0x002806B6, "call 0x24a1d0")
pin("C2 slot step 8", F, 0x002806C2, "add rbx, 8")
pin("C2 directory step 4", F, 0x002806C6, "add rdi, 4")
pin("C2 same bound 0x388", F, 0x002806CA, "cmp rbx, 0x388")
pin("C2 0024A1D0 puts the picture header (TIM2 +0x10) at atlas +0x20", 0x0024A1D0, 0x0024A238,
    "mov qword ptr [rbx + 0x20], rsi")
pin("C2 rsi = TIM2 + 0x10", 0x0024A1D0, 0x0024A1EB, "lea rsi, [rdx + 0x10]")

# ------------------------------------------------------------------ C3: the getters
for g, off in ((0x0035D460, 0x338), (0x0035D470, 0x360), (0x0035D480, 0x368)):
    d = list(T.R.md.disasm(T.R.at(g, 16), g, 3))
    ok = ("0209AC30" in T.fmt(d[0])) and d[1].op_str == "rax, qword ptr [rax + 0x%x]" % off and d[2].mnemonic == "ret"
    check("C3 %08X returns [0209AC30]+0x%X" % (g, off), ok, " / ".join("%s %s" % (x.mnemonic, x.op_str) for x in d))

# ------------------------------------------------------------------ C4 / C5: the popup draw (0028AAA0)
F = 0x0028AAA0
pin("C4 the label atlas", F, 0x0028AC17, "call 0x35d460")
pin("C4 atlas kept in rbx", F, 0x0028AC2A, "mov rbx, rax")
pin("C4 picture header", F, 0x0028AC36, "mov rdx, qword ptr [rbx + 0x20]")
pin("C4 T = header + 0x30", F, 0x0028AC44, "add rdx, 0x30")
pin("C4 page = u16[T+0x14] (code high byte 0)", F, 0x0028AC48, "movzx ecx, word ptr [rdx + 0x14]")
pin("C4 entry = u16[T+0x16+page*2] (code low byte 1)", F, 0x0028AC4C, "movzx r8d, word ptr [rdx + rcx*2 + 0x16]")
pin("C4 record table offset u16[T+0x10]", F, 0x0028AC52, "movzx ecx, word ptr [rdx + 0x10]")
pin("C4 record = T + off + entry*8", F, 0x0028AC5D, "lea rsi, [rdx + r8*8]")
pin("C4 frame 14: record + 0x70", F, 0x0028AC68, "lea rdx, [rsi + 0x70]")
pin("C4 frame 14's size dword (+0x74)", F, 0x0028AD83, "mov r8d, dword ptr [rsi + 0x74]")
pin("C5 cap test (packed count >= 0x12)", F, 0x0028AE49, "cmp word ptr [r14 + 0x14], 0x12")
pin("C5 below the cap: next arm", F, 0x0028AE4F, "jl 0x28ae69")
pin("C5 at the cap: code 1", F, 0x0028AE5F, "mov dword ptr [rsp + 0x28], 1")
pin("C5 below the cap: code 2", F, 0x0028AE77, "mov dword ptr [rsp + 0x28], 2")
pin("C5 the digit atlas", F, 0x0028AE7F, "call 0x35d470")
pin("C5 digit = nibble of the packed count", F, 0x0028AE9E, "and edi, 0xf")
pin("C5 page from the code's high byte", F, 0x0028AEFC, "movzx ecx, word ptr [r8 + rax*2 + 0x14]")
pin("C5 plus the code's low byte", F, 0x0028AF02, "add ecx, edx")
pin("C5 entry", F, 0x0028AF07, "movzx edx, word ptr [r8 + rcx*2 + 0x14]")
pin("C5 frame = entry + digit", F, 0x0028AF12, "add rdx, rax")
pin("C5 record = T + off + frame*8", F, 0x0028AF24, "lea rdi, [rcx + rdx*8]")

# ------------------------------------------------------------------ C6: control, the same lookup in types 2/9
F = 0x0029F4C0
pin("C6 T = [atlas+0x20] + 0x30", F, 0x0029F4F1, "add r8, 0x30")
pin("C6 page = u16[T+0x14+(code>>8)*2]", F, 0x0029F4F5, "movzx ecx, word ptr [r8 + rax*2 + 0x14]")
pin("C6 entry = u16[T+0x14+(page+(code&0xFF))*2]", F, 0x0029F505, "movzx edx, word ptr [r8 + rcx*2 + 0x14]")
pin("C6 record = T + u16[T+0x10] + entry*8", F, 0x0029F50F, "lea r8, [rcx + rdx*8]")


# ------------------------------------------------------------------ D: the shipped packs
def load_index(f):
    magic, hlen = struct.unpack("<4sI", f.read(8))
    assert magic == b"SRYK"
    (n,) = struct.unpack("<Q", f.read(8))
    eoff = 0x10 + n * 16
    f.seek(eoff)
    raw = f.read(0x20 * n)
    ents = [struct.unpack_from("<IIQQQ", raw, i * 0x20) for i in range(n)]
    f.seek(eoff + 0x20 * n)
    (slen,) = struct.unpack("<I", f.read(4))
    st = f.read(slen - 4)                      # the length counts its own 4-byte prefix
    f.seek(eoff + 0x20 * n + slen)
    bl = f.read(hlen - (eoff + 0x20 * n + slen))
    blocks = struct.unpack("<%dH" % (len(bl) // 2), bl)
    out = {}
    for sb, _sb2, size, off, noff in ents:
        out[st[noff:st.index(b"\0", noff)].decode()] = (sb, size, off)
    return out, blocks


def read_entry(f, idx, blocks, path):
    sb, size, off = idx[path]
    nb = (size + 0xFFFF) // 0x10000
    out = bytearray()
    pos = off
    for i in range(nb):
        cs = blocks[sb + i] or 0x10000
        exp = 0x10000 if i < nb - 1 else size - 0x10000 * (nb - 1)
        f.seek(pos)
        d = f.read(cs)
        out += d if cs == exp else zlib.decompress(d)
        pos += cs
    assert len(out) == size
    return bytes(out)


class Tim:
    def __init__(self, b, off):
        self.t = b[off:]
        assert self.t[:4] == b"TIM2"
        (self.tot, self.clsz, self.imsz, self.hsz, self.cc, _f, _m, self.clt, self.imt, self.w,
         self.h) = struct.unpack_from("<IIIHHBBBBHH", self.t, 0x10)
        self.T = 0x40

    def u16(self, a):
        return struct.unpack_from("<H", self.t, a)[0]

    def rec(self, code, frame):
        page = self.u16(self.T + 0x14 + (code >> 8) * 2)
        entry = self.u16(self.T + 0x14 + (page + (code & 0xFF)) * 2)
        r = self.T + self.u16(self.T + 0x10) + (entry + frame) * 8
        x, y, d = struct.unpack_from("<HHI", self.t, r)
        return x, y, d & 0xFFF, (d >> 12) & 0xFFF

    def indices(self, x0, y0, w, h):
        img = self.t[0x10 + self.hsz:0x10 + self.hsz + self.imsz]
        return bytes(img[y * self.w + x] for y in range(y0, y0 + h) for x in range(x0, x0 + w))

    def png(self, path, x0, y0, w, h, scale=3):
        clut = self.t[0x10 + self.hsz + self.imsz:]
        pal = [struct.unpack_from("<BBBB", clut, i * 4) for i in range(256)]
        pal = [pal[(i & 0xE7) | ((i & 0x08) << 1) | ((i & 0x10) >> 1)] for i in range(256)]  # CSM1 order
        px = self.indices(x0, y0, w, h)
        rows = []
        for y in range(h):
            row = bytearray()
            for x in range(w):
                r, g, b, a = pal[px[y * w + x]]
                a = min(255, a * 2)
                row += bytes(((r * a + 40 * (255 - a)) // 255, (g * a + 40 * (255 - a)) // 255,
                              (b * a + 40 * (255 - a)) // 255)) * scale
            rows += [bytes(row)] * scale

        def ch(t, d):
            return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
        raw = b"".join(b"\0" + r for r in rows)
        open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w * scale, h * scale, 8, 2, 0,
                                                                               0, 0)) + ch(b"IDAT", zlib.compress(raw))
                               + ch(b"IEND", b""))


LANGS = ["us", "de", "fr", "es", "it", "in", "kr", "ch", "cn", "in_sdver"]
with open(VBF, "rb") as f:
    idx, blocks = load_index(f)
    packs = {}
    for lg in LANGS:
        p = "ps2data/image/ff12/myoshiok/%s/packfiles/tex2pack_ys.bin" % lg
        check("D1 %s tex2pack_ys.bin in the archive" % lg, p in idx)
        packs[lg] = read_entry(f, idx, blocks, p)
hashes = {}
for lg in LANGS:
    b = packs[lg]
    d = struct.unpack_from("<16I", b, 0)
    live = [x for x in d if x != 0xFFFFFFFF]
    check("D1 %s: 11 directory slots, entries 0..9 are TIM2" % lg,
          len(live) == 11 and all(b[x:x + 4] == b"TIM2" for x in d[:10]), "%d live" % len(live))
    t0 = Tim(b, d[0])
    if lg != "in_sdver":
        check("D1 %s: entry 0 (battle_4_c) is 1024x512, 8-bit indexed" % lg, (t0.w, t0.h, t0.imt) == (1024, 512, 5),
              "%dx%d type %d" % (t0.w, t0.h, t0.imt))
    lab = t0.rec(1, 14)
    want = (126, 38, 37, 17) if lg == "in_sdver" else (120, 0, 130, 60)
    check("D2 %s: code 0x0001 frame 14 of battle_4_c = %dx%d at (%d, %d)" % (lg, want[2], want[3], want[0], want[1]),
          lab == want, str(lab))
    ph = hashlib.sha256(t0.indices(*lab)).hexdigest()[:16]
    hashes[lg] = ph
    print("   %s label index bytes sha256/16 = %s" % (lg, ph))
    if lg == "us":
        t5 = Tim(b, d[5])
        c1 = [t5.rec(1, k) for k in range(10)]
        c2 = [t5.rec(2, k) for k in range(10)]
        check("D3 control: partytop_4_c code 1 = ten 36x50 digit cells at y 273, x = 36k",
              c1 == [(36 * k, 273, 36, 50) for k in range(10)], str(c1[:3]))
        check("D3 control: partytop_4_c code 2 = ten 28x38 digit cells at y 331, x = 28k",
              c2 == [(28 * k, 331, 28, 38) for k in range(10)], str(c2[:3]))
        check("D3 control: frame 13 of the label code is a 16x16 placeholder at (0, 0)", t0.rec(1, 13) == (0, 0, 16, 16),
              str(t0.rec(1, 13)))
        if PNG:
            os.makedirs(PNG, exist_ok=True)
            t5.png(os.path.join(PNG, "digits_code1_us.png"), 0, 273, 360, 50, 2)
            t5.png(os.path.join(PNG, "digits_code2_us.png"), 0, 331, 280, 38, 2)
    if PNG:
        t0.png(os.path.join(PNG, "label_%s.png" % lg), *lab)
full = [lg for lg in LANGS if lg != "in_sdver"]
groups = {}
for lg in full:
    groups.setdefault(hashes[lg], []).append(lg)
gl = sorted(sorted(v) for v in groups.values())
print("   label picture groups: %s" % gl)
check("D4 six distinct label pictures: us, de, fr, es, it, and in/kr/ch/cn shared",
      gl == sorted([["us"], ["de"], ["fr"], ["es"], ["it"], sorted(["in", "kr", "ch", "cn"])]), str(gl))

# ------------------------------------------------------------------ S: what the shop driver counts (0056D370)
F = 0x0056D370
pin("S1 sale / purchase split on +0xE4 bit 0", F, 0x0056D46F, "test r8b, 1")
pin("S1 bit 0 clear: the purchase arm", F, 0x0056D476, "je 0x56d49a")
pin("S1 sale commit Shop_CommitSaleItemAndGil", F, 0x0056D478, "call 0x310870")
pin("S1 sale: field +0xE4 & 0x3FC0", F, 0x0056D483, "and eax, 0x3fc0")
pin("S1 sale: == 0x1C0", F, 0x0056D488, "cmp eax, 0x1c0")
pin("S1 sale: otherwise no counter", F, 0x0056D48D, "jne 0x56d4d7")
pin("S1 sale: amount = the quantity word +0xDC", F, 0x0056D48F, "movzx edx, word ptr [rdi + 0xdc]")
pin("S1 sale: counter 14", F, 0x0056D496, "mov cl, 0xe")
pin("S1 sale: joins the update call", F, 0x0056D498, "jmp 0x56d4d2")
pin("S2 purchase commit Shop_CommitPurchaseItemAndGil", F, 0x0056D49A, "call 0x2feeb0")
pin("S2 purchase: field == 0x2C0", F, 0x0056D4AC, "cmp eax, 0x2c0")
pin("S2 purchase: the test skips only 0030B630", F, 0x0056D4B1, "jne 0x56d4c5")
pin("S2 purchase: 0030B630 (guarded)", F, 0x0056D4C0, "call 0x30b630")
pin("S2 purchase: selected row", F, 0x0056D4C5, "mov rax, qword ptr [rdi + 0xd0]")
pin("S2 purchase: counter 19", F, 0x0056D4CC, "mov cl, 0x13")
pin("S2 purchase: amount = the row's id word +8", F, 0x0056D4CE, "movzx edx, word ptr [rax + 8]")
pin("S2 the update call", F, 0x0056D4D2, "call 0x316a50")
F = 0x00316A50
pin("S3 id bound 30", F, 0x00316A50, "cmp cl, 0x1e")
pin("S3 kind byte 0 selects the trigger path", F, 0x00316A81, "cmp byte ptr [r14 + rbp*8 + 0xbf0460], 0")
pin("S3 mode byte", F, 0x00316A90, "movzx ecx, byte ptr [r14 + rbp*8 + 0xbf0462]")
pin("S3 mode 1", F, 0x00316A9D, "cmp ecx, 1")
pin("S3 mode 1 fires only when amount == threshold", F, 0x00316AA6, "cmp edx, dword ptr [r14 + rbp*8 + 0xbf0464]")
pin("S3 not equal: return", F, 0x00316AAE, "jne 0x316bd1")
pin("S3 then the award bitmap +0x3844", F, 0x00316ACB, "movzx ebx, byte ptr [rax + rdi + 0x3844]")
pin("S3 bit set", F, 0x00316AD3, "bts ebx, esi")
d19 = T.R.at(0x00D10460 + 19 * 8, 8)
d14 = T.R.at(0x00D10460 + 14 * 8, 8)
check("S4 descriptor 19 = kind 0, mode 1, threshold 53375 (0xD07F)",
      d19[0] == 0 and d19[2] == 1 and struct.unpack_from("<I", d19, 4)[0] == 0xD07F, d19.hex())
check("S4 descriptor 14 = kind 2 (a 2-byte counter), offset 0x0C, mode 0", (d14[0], d14[1], d14[2]) == (2, 0x0C, 0),
      d14.hex())
recs = {}
for slot in range(41):
    r = 0x01DFE410 + slot * 0x198
    recs[q(r)] = recs.get(q(r), []) + [(slot, T.cstr(q(r + 8), 64), T.cstr(r + 0x10, 64))]
print("   counter 14: %s; counter 19: %s" % (recs.get(14), recs.get(19)))
check("S5 counter 14 = ACH_COUNT_SELL_EVITEM, Privateer", recs.get(14) == [(11, "ACH_COUNT_SELL_EVITEM", "Privateer")])
check("S5 counter 19 = ACH_SPECIAL_HORIDASHI, Collector", recs.get(19) == [(17, "ACH_SPECIAL_HORIDASHI", "Collector")])
r19 = 0x01DFE410 + 19 * 0x198
check("S5 control: slot 19 (01E00258) = {13, ACH_COMPLETE_YUGOU, Mist Walker}, as the catalogue records",
      r19 == 0x01E00258 and (q(r19), T.cstr(q(r19 + 8), 64), T.cstr(r19 + 0x10, 64)) == (13, "ACH_COMPLETE_YUGOU",
                                                                                         "Mist Walker"))

print("FAILS %d" % FAILS)
