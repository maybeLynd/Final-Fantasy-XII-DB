"""rc29_review.py - RC-29..RC-34: an independent ORACLE check of SWE2-DATA's answers (../rc22-34-resource-readers-0930,
commit 1261e2044), plus a further narrowing of RC-30's three unbounded request sites. ORACLE, 2026-09-30. Static.

Every check re-derives its fact from the image or the shipped files with this record's own code (helpers:
../rc22-as7-pages-0930/arc.py; kind-7 rows: ../rc6-console-map-codes-0930/rc5_paths.py).
"""
import contextlib, io, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-as7-pages-0930"))
import arc  # noqa: E402
img = arc.img
sys.path.insert(0, os.path.join(HERE, "..", "rc6-console-map-codes-0930"))
with contextlib.redirect_stdout(io.StringIO()):
    import rc5_paths as R  # noqa: E402
FAILS = []


def check(ok, name):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def at(a, n=0x20):
    return {x.address: (x.mnemonic, x.op_str) for x in img.dis(a, n)}


# ---------------- RC-29: the block 008FCE00..008FD2D0 ----------------
LO, HI = 0x008FCE00, 0x008FD2D0
rip_sites = []
for r in sorted(img.ROOTS):
    for x in img.fn_ins(r):
        t = img.ripmem(x)
        if t is not None and LO <= t < HI:
            rip_sites.append((x.address, r, t, x.mnemonic, x.op_str))
imgrel = []
t = img.blob[img.TR:img.TR + img.TN]
for m in re.finditer(re.escape(struct.pack("<I", LO - img.BASE)), t):
    for back in range(3, 6):
        a = img.T0 + m.start() - back
        xs = img.dis(a, 15)
        if xs and xs[0].address == a and any(o.type == 3 and o.mem.disp == LO - img.BASE for o in xs[0].operands):
            imgrel.append((a, xs[0].mnemonic, xs[0].op_str, img.owner(a)))
print("RC-29 rip-relative references into the block: %s" % ["%08X in %08X -> %08X" % (a, r, tt) for a, r, tt, _m, _o in rip_sites])
print("RC-29 image-base-relative references (disp 0x%X): %s" % (LO - img.BASE, ["%08X %s %s" % i[:3] for i in imgrel]))
check(sorted(a for a, *_ in rip_sites) == [0x001D150F, 0x001D537D, 0x001D542A] and [i[0] for i in imgrel] == [0x001CD186],
      "K29a three rip-relative references (001D150F, 001D537D, 001D542A) and one image-base-relative read (001CD186)")
pages = [x for x in img.fn_ins(0x001D5260) if x.mnemonic == "mov" and x.op_str == "dword ptr [rbx + 0xa88], 0xe"]
check(bool(pages) and (HI - LO) == 14 * 0x58, "K29b 001D5260 sets 14 pages (+0xA88 = 0xE); the block is 14 x 0x58 bytes = 14 pages x 22 u32")
ids = struct.unpack("<%dI" % ((HI - LO) // 4), img.rd(LO, HI - LO))
check(max(ids) <= 0x126, "K29c every u32 in the block is a console command id <= 0x126 (max %s)" % hex(max(ids)))

# ---------------- RC-30: the three computed-id sites SWE2-DATA left unbounded ----------------
# site 2: 003C9950 requests 0xE + byte[obj+0xC1]; the writers of +0xC1 in the widget module
c1_writers = {0x003C95F9: "word [+0xC0] = 0x0507 -> +0xC1 = 5", 0x003C9611: "word [+0xC1] = 0x0A02 -> 2",
              0x003C974F: "table 00D11720[+0xC1]", 0x003C9D28: "dl, loop index 0..6 (7 excluded)",
              0x003C9D46: "dl, loop index 0..6 (7 excluded)"}
tab = list(img.rd(0x00D11720, 8))
a1 = at(0x003C95F9, 12); a2 = at(0x003C9611, 12); a3 = at(0x003C9731, 0x30); a4 = at(0x003C9BDD, 0x20)
check(a1.get(0x003C95F9) == ("mov", "word ptr [rbx + 0xc0], 0x507") and a2.get(0x003C9611) == ("mov", "word ptr [rbx + 0xc1], 0xa02")
      and a3.get(0x003C9747) == ("movzx", "edx, byte ptr [rcx + rdx + 0xbf1720]") and a4.get(0x003C9BDF) == ("mov", "edx, edi") and a4.get(0x003C9BF4) == ("cmp", "rcx, 7")
      and a4.get(0x003C9BFA) == ("mov", "dl, 7") and max(tab) <= 6,
      "K30a 003C9950's byte +0xC1 takes only 5, 2, 00D11720[.] = %s, or the 003C9A30 loop index 0..6: id 0x0E..0x14" % tab)
# site 1: 002CEAE0 requests 0x10 + byte[[0209AC30]+0xB2D], gated by +0xD3C bit 1
b = at(0x002CEAE4, 0x20)
w = at(0x002833E6, 0x24)
check(b.get(0x002CEAEB) == ("test", "byte ptr [rax + 0xd3c], 2") and b.get(0x002CEAF4) == ("movzx", "r8d, byte ptr [rax + 0xb2d]")
      and w.get(0x002833ED) == ("or", "dword ptr [rax + 0xd3c], 2") and w.get(0x00283400) == ("mov", "byte ptr [rax + 0xb2d], cl")
      and w.get(0x002833FB) == ("movzx", "ecx, byte ptr [r9 + 0x60]"),
      "K30b 002CEAE0's byte +0xB2D is set (with the gate bit) only from a guest member's id word +0x60 = its "
      "BattleStatsRecord definitionRowIndex (00283400); otherwise 0xFF with the gate clear (002832C7, 002832D5)")
# site 3: 00575C30 requests u16 00D23740[arg[0]] + word[obj+0xCA] (+ word arg[2])
v = struct.unpack("<8H", img.rd(0x00D23740, 16))
print("K30c 00D23740[0..7] = %s ; 00575C30 is called only from %s" % (list(v), ["%08X" % a for a, _k in img.calls_to(0x00575C30)]))
check(min(v[:6]) >= 0xE5 and v[6] == 0 and v[7] == 0,
      "K30c for arg[0] 0..5 the id is >= 0x228 + unsigned words, so 0xE2..0xE4 is unreachable; arg[0] 6 or 7 gives 0 + the words")

# ---------------- RC-31: menuquest.lst ----------------
L = at(0x0037EFC0, 0x80)
check(L.get(0x0037EFD9) == ("movzx", "r10d, word ptr [r8 + 0xe]") and L.get(0x0037EFE8) == ("lea", "rcx, [r8 + 0x10]")
      and L.get(0x0037EFFC) == ("add", "rcx, 8") and L.get(0x0037F02A) == ("movzx", "ecx, word ptr [r8 + 8]"),
      "K31a 0037EFC0: count u16 +0x0E, entries at +0x10 stride 8, first match, string = lst + u16 [+8] + u16 [entry+2]")
hdr4, uniq, e4 = set(), True, set()
for pth in arc.find("menuquest.lst"):
    d = arc.get(pth)
    n = struct.unpack("<H", d[0xE:0x10])[0]
    ent = [struct.unpack("<HHHH", d[0x10 + 8 * k:0x18 + 8 * k]) for k in range(n)]
    hdr4.add(struct.unpack("<I", d[4:8])[0])
    uniq &= len(set(e[0] for e in ent)) == n
    e4 |= set(e[2] for e in ent)
check(hdr4 == {100} and uniq and e4 <= {0, 3, 4},
      "K31b all %d files: header +4 = %s; directory ids unique; entry +4 words %s" % (len(arc.find("menuquest.lst")), sorted(hdr4), sorted(e4)))

# ---------------- RC-32..34: meshdata.mg ----------------
g = at(0x00274780, 0x0A)
d = arc.get(arc.find("in/worldmap/meshdata.mg")[0])
o0, s0, o1, s1 = struct.unpack("<4i", d[:16])
check(g.get(0x00274783) == ("mov", "eax, dword ptr [rcx + rax*8]") and o0 == 0x10 and o0 + s0 == o1 and o1 + s1 == len(d),
      "K32 00274780 returns buf + s32[buf + 8i]; the file is two {offset, size} entries (0x%X+0x%X, 0x%X+0x%X) filling its %d bytes"
      % (o0, s0, o1, s1, len(d)))
names = []
for k in range((0x00D232D0 - 0x00D23270) // 16):
    pn, pt = struct.unpack("<QQ", img.rd(0x00D23270 + 16 * k, 16))
    names.append((R.cstr(pn) if pn else None, R.cstr(pt) if pt else None))
print("K34 00D23270 name table: %s" % names)
arr = R.regions[1][0][7]
rows = {i: R.row(arr, i) for i in range(0xA8, 0xAF)}
print("K34 kind-7 rows 0xA8..0xAE (region 1): %s" % rows)
check(("main0.psd", "w_main0") in names and rows[0xA8] and rows[0xA8].lower().endswith("meshdata.mg")
      and all(rows[0xAB + i] and rows[0xAB + i].lower().endswith("w_main%d.tm2" % i) for i in range(4)),
      "K34 main0..3.psd -> w_main0..3 in 00D23270, and kind 7 0xAB..0xAE = Tm2_Menu w_main0..3.tm2, 0xA8 = meshdata.mg")
print("\nFAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
