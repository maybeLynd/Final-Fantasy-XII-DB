"""btm_font_census.py - RC-26 / RC-27 / RC-28 (SWE2-DATA, 2026-09-30): the .btm exfont texel packing, the file that
supplies the font_stf glyph tables, and the glyph coverage against the f1 (stf) kerning pairs.

Static only: the certified image (Database/Tools/work/exe/FFXII_TZA.exe) and the full extract D:/FFXII_TZA_extract.
Every check prints PASS/FAIL; the last line is 'FAILS N'.

Image (I):
  I1  00D10C98 = {130..135, 218..223}; the only reference to it is 00365810's lea.
  I2  00365810 is reached from one site: raw E8/E9/0F8x rel32 + rip-disp scan of .text, positive control 00364210
      (known caller 00364BA6 found by the same scan).
  I3  that site's loop (0053EC90-0053ECA4) passes ecx = 7..12, so 00365810 uses table rows 6..11 = ids 218..223 and
      stores into bitmap slots 6..11 ([022CBE00 + 0x110 + slot*8]).
  I4  every kind-7 path array in 002DF9A0 (10 arrays, one per language arm): ids 130..135 are NULL, ids 218..223 are the
      six ExFont .btm, id 210 is fontpack_fs.bin (control). Which directory each array names is printed.
  I5  00364210 indexes the glyph table [+0x10 + f*8] and the bitmap [+0x110 + f*8] with the same font index.
  I6  003643A0 (completion of 003658F0's request for id 0xD2 = fontpack_fs.bin) sets [+8] = pack + dword[pack+0] and
      calls 00366080, which fills every glyph-table slot [+0x10 + i*8], i < s16[blob+0]; it fills bitmap slots
      0, 2, 3, 4 from the pack and none of slots 6..11.
  I7  the cell upload: 003649A0 passes PSM 0x14 (r9d) to 00474650 -> 003A22A0, whose transfer size is
      003A1F20(w, h, psm) / 4 qwords; 003A1F20's jump table sends 0x14 to the w*h/8 case (4 bits per texel);
      controls: 0x13 -> w*h/4 (8 bpp), 0x00 -> w*h (32 bpp).
Corpus (C):
  C1  in every fontpack_fs.bin copy, tables 6..11: records sorted by pixelOffset tile back to back under 4 bpp
      (pow2(cellW) * pow2(cellH) / 2 bytes per cell, 00364210's rounding); under 8 bpp none do (control).
  C2  the in/ch tables end exactly at the in/ch .btm size under 4 bpp; under 8 bpp they overrun by one cell (control).
  C3  nibble order: texels outside the authored cellW x cellH inside the pow2 cell are zero under low-nibble-first
      (GS PSMT4 order) and not under high-nibble-first (control).
  C4  glyph counts per face, per fontpack copy, and the pairing each kind-7 array makes; the us-copy b/c tables
      (127 glyphs) against the in .btm they are paired with.
  C5  the 1,237 .ker pairs of the PC stf fonts against the PS2 faces' and the PC .dat faces' character sets.
"""
import os, re, struct, collections, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
EXT = r"D:\FFXII_TZA_extract"
PS2 = os.path.join(EXT, "ps2data", "image", "ff12", "myoshiok")
PCF = os.path.join(EXT, "gamedata", "d3d11", "artdata", "font")
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
ns = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(ns):
    h = pe + 24 + opt + i * 40
    secs.append((d[h:h + 8].rstrip(b"\0").decode(), struct.unpack_from("<I", d, h + 12)[0],
                 struct.unpack_from("<I", d, h + 8)[0], struct.unpack_from("<I", d, h + 20)[0],
                 struct.unpack_from("<I", d, h + 16)[0]))


def off(va):
    r = va - BASE
    for n, a, vs, ro, rs in secs:
        if a <= r < a + min(vs, rs):
            return ro + r - a
    return None


def va_of(o):
    for n, a, vs, ro, rs in secs:
        if ro <= o < ro + rs:
            return BASE + a + o - ro
    return None


def q(va):
    o = off(va)
    return struct.unpack_from("<Q", d, o)[0] if o is not None else None


def cstr(va):
    o = off(va)
    if o is None:
        return None
    s = d[o:d.index(b"\0", o)]
    return s.decode("latin1") if s and all(32 <= c < 127 for c in s) else None


md = Cs(CS_ARCH_X86, CS_MODE_64)


def ins_at(va, n=1):
    o = off(va)
    return [(x.address, x.mnemonic, x.op_str) for x in md.disasm(d[o:o + 16 * n], va, count=n)]


FAILS = 0


def check(tag, ok, msg):
    global FAILS
    if not ok:
        FAILS += 1
    print("%-4s %s  %s" % (tag, "PASS" if ok else "FAIL", msg))


text = [s for s in secs if s[0] == ".text"][0]
TV, TSZ, TRO = BASE + text[1], text[4], text[3]
blob = d[TRO:TRO + TSZ]


def raw_refs(target):
    """every rel32 in .text that resolves to target: E8/E9 (end = i+5), 0F 8x (end = i+6), and any 4-byte
    displacement whose end-of-field + disp = target (rip-relative operands without an immediate)."""
    calls, jcc, rip = [], [], []
    for i in range(len(blob) - 6):
        b = blob[i]
        if b in (0xE8, 0xE9):
            if TV + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] == target:
                calls.append(TV + i)
        if b == 0x0F and 0x80 <= blob[i + 1] <= 0x8F:
            if TV + i + 6 + struct.unpack_from("<i", blob, i + 2)[0] == target:
                jcc.append(TV + i)
    fields = set(a + 1 for a in calls) | set(a + 2 for a in jcc)  # the rel32 fields just counted
    for i in range(len(blob) - 4):
        if TV + i + 4 + struct.unpack_from("<i", blob, i)[0] == target and TV + i not in fields:
            rip.append(TV + i)
    return calls, jcc, rip


def data_qword_refs(target):
    pat = struct.pack("<Q", target)
    return [va_of(m.start()) for m in re.finditer(re.escape(pat), d) if m.start() % 8 == 0]


# ---------------------------------------------------------------- I1
tab = [struct.unpack_from("<i", d, off(0xD10C98) + 4 * k)[0] for k in range(12)]
check("I1", tab == list(range(130, 136)) + list(range(218, 224)), "00D10C98 = %s" % tab)
c, j, r = raw_refs(0xD10C98)
rip_ins = [a for a in r if any(x[1] == "lea" for x in ins_at(a - 3, 1))]
check("I1", len(r) == 1 and 0x365849 <= r[0] < 0x365850 and not data_qword_refs(0xD10C98),
      "rip references to 00D10C98: %s (data qwords %d)" % (["%08X" % a for a in r], len(data_qword_refs(0xD10C98))))

# ---------------------------------------------------------------- I2
c, j, r = raw_refs(0x365810)
dq = data_qword_refs(0x365810)
check("I2", c == [0x53EC9A] and not j and not r and not dq,
      "00365810: call/jmp sites %s, jcc %d, rip-disp %d, data qwords %d" % (["%08X" % a for a in c], len(j), len(r), len(dq)))
c2, j2, r2 = raw_refs(0x364210)
check("I2", 0x364BA6 in c2, "positive control: the same scan finds 00364210's caller 00364BA6 (%s)" % ["%08X" % a for a in c2])

# ---------------------------------------------------------------- I3
loop = ins_at(0x53EC90, 6)
txt = " | ".join("%08X %s %s" % x for x in loop)
ok = (loop[0][1:] == ("xor", "ebx, ebx") and loop[1][1:] == ("lea", "ecx, [rbx + 7]") and loop[3][1] == "call"
      and loop[4][1:] == ("inc", "ebx") and loop[5][1:] == ("cmp", "ebx, 6"))
check("I3", ok, "caller loop: " + txt)
body = ins_at(0x365810, 50)
bt = [" ".join(x[1:]) for x in body]
check("I3", "dec ecx" in bt and "movsxd rbp, dword ptr [rax + rdi*4]" in bt
      and "mov qword ptr [rax + rdi*8 + 0x110], r8" in bt,
      "00365810: row = ecx-1 -> table[row] = id, bitmap slot = row; ecx 7..12 -> rows 6..11 -> ids %s" % tab[6:12])

# ---------------------------------------------------------------- I4
# the language arms: every lea of a kind-7 array in 002DF9A0 = every qword array whose id-218 entry names ExFont
arrays = []
for m in re.finditer(re.escape(b"ExFont\\font_stf_a_normal.btm\x00"), d):
    s0 = d.rfind(b"\x00", 0, m.start()) + 1
    for ref in data_qword_refs(va_of(s0)):
        arrays.append(ref - 218 * 8)
arrays = sorted(set(arrays))
allnull = True
rows = []
for a in arrays:
    ids130 = [q(a + 8 * i) for i in range(130, 136)]
    btm = [cstr(q(a + 8 * i)) for i in range(218, 224)]
    fp = cstr(q(a + 8 * 210))
    dirs = collections.Counter()
    for i in range(0, 300):
        p = q(a + 8 * i)
        s = cstr(p) if p else None
        if s and "myoshiok\\" in s:
            dirs[s.split("myoshiok\\")[1].split("\\")[0]] += 1
    lang = [k for k, v in dirs.most_common() if k != "in" and v > 2][:1] or ["in"]
    allnull &= all(v == 0 for v in ids130) and all(b and b.endswith(".btm") for b in btm) and fp.endswith("fontpack_fs.bin")
    rows.append((a, lang[0], fp.split("myoshiok\\")[1].split("\\")[0], btm[0].split("myoshiok\\")[1].split("\\")[0],
                 btm[4].rsplit("\\", 1)[1]))
c, j, r = raw_refs(0x2DF9A0)
check("I4", len(arrays) == 10 and allnull,
      "%d kind-7 path arrays: ids 130..135 NULL in all, 218..223 = .btm and 210 = fontpack_fs.bin in all" % len(arrays))
for a, lang, fpd, btd, c222 in rows:
    print("       array %08X  majority-dir %-3s  fontpack_fs from %-3s  .btm from %-3s  id 222 = %s" % (a, lang, fpd, btd, c222))

# ---------------------------------------------------------------- I5
f5 = {a: "%s %s" % (m, o) for a, m, o in ins_at(0x364276, 3) + ins_at(0x364346, 1)}
ok = (f5.get(0x364276) == "mov rax, qword ptr [r11 + rbx*8 + 0x10]" and f5.get(0x36427B) == "mov rdi, rbx"
      and f5.get(0x364346) == "mov rdx, qword ptr [r11 + rdi*8 + 0x110]")
check("I5", ok, "00364210: glyph table [r11+rbx*8+0x10], rdi = rbx, bitmap [r11+rdi*8+0x110] - one font index")

# ---------------------------------------------------------------- I6
b6 = [(a, "%s %s" % (m, o)) for a, m, o in ins_at(0x3643A0, 70)]
t6 = [s for a, s in b6]
stores = sorted(set(int(mm.group(1), 16) for s in t6 for mm in [re.search(r"mov qword ptr \[r(?:11|dx) \+ (0x[0-9a-f]+)\], rcx", s)] if mm))
check("I6", "mov qword ptr [r11 + 8], rax" in t6 and "call 0x366080" in t6 and stores == [0x110, 0x120, 0x128, 0x130],
      "003643A0: [+8] = pack + dword[pack], call 00366080; bitmap slots stored from the pack: %s (slots 0,2,3,4; none of 6..11)" % [hex(x) for x in stores])
b8 = [" ".join(x[1:]) for x in ins_at(0x366080, 12)]
check("I6", "movsx eax, word ptr [rdx + 2]" in b8 and "mov qword ptr [r10 + 0x10], rdx" in b8,
      "00366080: table 0 at blob+4 -> [+0x10]; tables chained by their dword +0 into [+0x10 + i*8] for i < s16[blob+0]")
b9 = [" ".join(x[1:]) for x in ins_at(0x3658F0, 30)]
check("I6", "mov edx, 0xd2" in b9 and "mov qword ptr [r8], rax" in b9 and any("0x3643a0" in s or "rip - 0x1569" in s for s in b9),
      "003658F0: requests kind 7 id 0xD2 (fontpack_fs.bin) into [022CBE00+0], completion 003643A0")

# ---------------------------------------------------------------- I7
up = {a: "%s %s" % (m, o) for a, m, o in ins_at(0x364BDB, 9)}
check("I7", up.get(0x364BE0) == "mov r9d, 0x14" and up.get(0x364BF9) == "mov r8d, 0x3440" and up.get(0x364BFF) == "call 0x474650",
      "003649A0 cell upload: 00474650(dst, texels=[node+0x18], dbp 0x3440, psm 0x14, w=[node+0x14], h=[node+0x15])")
check("I7", ins_at(0x47466E, 1)[0][1:] == ("jmp", "0x3a22a0"), "00474650 tail-jumps to 003A22A0 (the transfer builder)")
IDX, TAB = 0x3A1FA4, 0x3A1F90


def case(psm):
    i = psm - 1
    if i < 0 or i > 0x39:
        return 0x3A1F89
    return struct.unpack_from("<I", d, off(TAB) + 4 * d[off(IDX) + i])[0] + BASE


shape = {0x3A1F4E: "w*h*3/2", 0x3A1F5B: "w*h/2", 0x3A1F67: "w*h/4", 0x3A1F7A: "w*h/8", 0x3A1F89: "w*h"}
c14, c13, c00 = shape[case(0x14)], shape[case(0x13)], shape[case(0x00)]
check("I7", c14 == "w*h/8" and c13 == "w*h/4" and c00 == "w*h",
      "003A1F20 transfer words: psm 0x14 -> %s (4 bpp); controls psm 0x13 -> %s (8 bpp), psm 0 -> %s (32 bpp)" % (c14, c13, c00))


# ---------------------------------------------------------------- corpus
def p2(v):
    for s in (8, 16, 32, 64):
        if v <= s:
            return s
    return 128


def tables(path):
    b = open(path, "rb").read()
    g = struct.unpack_from("<I", b, 0)[0]
    n = struct.unpack_from("<h", b, g)[0]
    t = g + 4
    out = []
    for i in range(n):
        if i:
            t += struct.unpack_from("<i", b, t)[0]
        cnt = struct.unpack_from("<i", b, t + 4)[0]
        out.append([struct.unpack_from("<HBBBBBBI", b, t + 16 + 12 * k) for k in range(cnt)])
    return n, out


BTM = ["font_stf_a_normal", "font_stf_a_shadow", "font_stf_b_normal", "font_stf_b_shadow", "font_stfc_normal", "font_stf_c_shadow"]
langs = sorted(l for l in os.listdir(PS2) if os.path.exists(os.path.join(PS2, l, "packfiles", "fontpack_fs.bin")))
packs = {l: tables(os.path.join(PS2, l, "packfiles", "fontpack_fs.bin")) for l in langs}
btms = {}
for l in os.listdir(PS2):
    for k, nm in enumerate(BTM):
        p = os.path.join(PS2, l, "exfont", nm + ".btm")
        if os.path.exists(p):
            btms[(l, 6 + k)] = open(p, "rb").read()
print("       fontpack_fs.bin copies: %s; .btm copies: %s" % (langs, sorted(set(l for l, s in btms))))

c4 = c8 = tot = 0
for l in langs:
    n, tb = packs[l]
    for s in range(6, 12):
        seq = sorted(tb[s], key=lambda r: r[7])
        tot += len(seq) - 1
        c4 += sum(1 for a, b in zip(seq, seq[1:]) if a[7] + p2(a[1]) * p2(a[2]) // 2 == b[7])
        c8 += sum(1 for a, b in zip(seq, seq[1:]) if a[7] + p2(a[1]) * p2(a[2]) == b[7])
        if seq[0][7] != 0:
            c4 = -10 ** 9
check("C1", c4 == tot and c8 == 0, "tables 6..11 of %d copies: %d/%d neighbours contiguous at 4 bpp, %d at 8 bpp; every table starts at offset 0"
      % (len(langs), c4, tot, c8))

ok2 = True
for l in ("in", "ch"):
    n, tb = packs[l]
    for s in range(6, 12):
        end4 = max(r[7] + p2(r[1]) * p2(r[2]) // 2 for r in tb[s])
        end8 = max(r[7] + p2(r[1]) * p2(r[2]) for r in tb[s])
        size = len(btms[(l, s)])
        ok2 &= end4 == size and end8 > size
        print("       %s slot %2d %-18s  n %3d  end(4bpp) %6d  end(8bpp) %6d  .btm %6d" % (l, s, BTM[s - 6], len(tb[s]), end4, end8, size))
check("C2", ok2, "in/ch tables 6..11 end exactly at their .btm size at 4 bpp and overrun it at 8 bpp")

pad_lo = pad_hi = ink = 0
hist = collections.Counter()
for l in ("in", "ch"):
    n, tb = packs[l]
    for s in range(6, 12):
        bm = btms[(l, s)]
        for r in tb[s]:
            code, w, h, adv, u5, u6, u7, po = r
            W, H = p2(w), p2(h)
            for y in range(H):
                for x in range(0, W, 2):
                    byte = bm[po + (y * W + x) // 2]
                    lo, hi = byte & 15, byte >> 4
                    hist[lo] += 1
                    hist[hi] += 1
                    for xx, vlo, vhi in ((x, lo, hi), (x + 1, hi, lo)):
                        outside = xx >= w or y >= h
                        if vlo:
                            ink += 1
                        if outside and vlo:
                            pad_lo += 1
                        if outside and vhi:
                            pad_hi += 1
check("C3", pad_lo == 0 and pad_hi > 0,
      "texels outside cellW x cellH: %d non-zero under low-nibble-first, %d under high-nibble-first (control); ink texels %d" % (pad_lo, pad_hi, ink))
print("       nibble histogram (in/ch, all cells):", dict(sorted(hist.items())))

# C4 glyph counts and pairing
for l in langs:
    n, tb = packs[l]
    print("       fontpack_fs %-3s: %d tables; glyphs per table %s" % (l, n, [len(t) for t in tb]))
us_n, us_tb = packs["us"]
in_n, in_tb = packs["in"]
same78 = all(us_tb[s][:78] == in_tb[s] for s in range(6, 12))
over = []
for s in range(8, 12):
    size = len(btms[("in", s)])
    past = [r for r in us_tb[s] if r[7] + p2(r[1]) * p2(r[2]) // 2 > size]
    over.append((s, len(us_tb[s]), size, len(past), "".join(chr(r[0]) for r in past)))
check("C4", same78 and all(o[3] == 49 for o in over),
      "us tables 6..11 begin with the in tables' 78 records unchanged; us tables 8..11 add 49 glyphs whose cells lie past the end of the in .btm")
for s, nn, size, npast, chars in over:
    print("       us slot %d: %d glyphs vs in .btm %d B -> %d cells past the end: %s" % (s, nn, size, npast, chars.encode("ascii", "backslashreplace").decode()))
usarr = [r for r in rows if r[2] == "us"]
check("C4", len(usarr) == 6 and all(r[3] == "in" for r in usarr),
      "%d kind-7 arrays pair us\\PackFiles\\fontpack_fs.bin with in\\ExFont .btm (majority dirs %s)" % (len(usarr), [r[1] for r in usarr]))
missing = [r for r in rows if not os.path.exists(os.path.join(PS2, r[3], "exfont"))]
print("       arrays whose .btm directory ships no ExFont: %s" % [(("%08X" % r[0]), r[1], r[3]) for r in missing])

# C5 kerning pairs
ker = {}
dat = {}
for L in sorted(os.listdir(PCF)):
    p = os.path.join(PCF, L)
    if not os.path.isdir(p):
        continue
    for f in ("font_stf_a", "font_stf_as", "font_stf_b", "font_stf_bs", "font_stf_c", "font_stf_cs"):
        kp = os.path.join(p, f + ".ker")
        dp = os.path.join(p, f + ".dat")
        if os.path.exists(kp):
            kb = open(kp, "rb").read()
            ker[(L, f)] = [struct.unpack_from("<Iii", kb, 12 * i) for i in range(len(kb) // 12)] if len(kb) % 12 == 0 else None
        if os.path.exists(dp):
            db = open(dp, "rb").read()
            cps = set()
            for k in range((len(db) - 0x28) // 0x24):
                u = struct.unpack_from("<I", db, 0x28 + 0x24 * k + 4)[0]
                try:
                    cps.add(ord(u.to_bytes(4, "little").rstrip(b"\0").decode("utf-8")))
                except (UnicodeDecodeError, TypeError):
                    cps.add(-1)
            dat[(L, f)] = cps
counts = sorted(set(len(v) for v in ker.values() if v))
check("C5", counts == [1237] and len(ker) == 12, "%d stf .ker files (us, jp), pair counts %s" % (len(ker), counts))
pairs = ker[("us", "font_stf_a")]
kset = set(a for a, b, c in pairs) | set(b for a, b, c in pairs)
ps2_78 = set(r[0] for r in in_tb[6])
ps2_127 = set(r[0] for r in us_tb[8])
pc = dat[("us", "font_stf_a")]
both78 = sum(1 for a, b, c in pairs if a in ps2_78 and b in ps2_78)
both127 = sum(1 for a, b, c in pairs if a in ps2_127 and b in ps2_127)
bothpc = sum(1 for a, b, c in pairs if a in pc and b in pc)
same_pairs = all(ker[k] == pairs for k in ker)
print("       .ker distinct codes %d; PS2 78-glyph face %d codes, 127-glyph face %d, PC us/font_stf_a.dat %d glyphs (%d codes)"
      % (len(kset), len(ps2_78), len(ps2_127), len(pc), len(pc)))
print("       pairs with both codes in: PS2 78-glyph face %d/1237, PS2 127-glyph face %d/1237, PC .dat %d/1237; all 12 .ker identical: %s"
      % (both78, both127, bothpc, same_pairs))
print("       .ker codes absent from the PS2 78-glyph face: %s" % "".join(chr(c) for c in sorted(kset - ps2_78)).encode("ascii", "backslashreplace").decode())
check("C5", both78 == bothpc, "control: the PS2 78-glyph face and the PC .dat face cover the same pairs (%d, %d)" % (both78, bothpc))
print("FAILS %d" % FAILS)
