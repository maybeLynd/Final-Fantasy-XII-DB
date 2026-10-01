"""DD residue batch 15 (SWE2-CONTRACT for OPUS, 2026-09-30): the nine id-less rows P1-P9 of batch 13, answered statically.

Run: python -B b15_checks.py   (last line FAILS n; must be FAILS 0)
Inputs: the certified image through retool.py (sha 73461d08...); the game extract D:/FFXII_TZA_extract (the menu
images, layouts and font packs of every language folder, mapjumpgroupinit.bin); the BQ-10 decompile of the 1,114
shipped us scripts (Tools/work/FABLE/pub140-scratch/corpus/us, gitignored; FF12_CORPUS overrides); the kind-7 path
helper of _index/candidates/rc22-34-resource-readers-0930/kind7.py; the register _index/OPEN-QUESTIONS.md and three
pages, for the boundary checks. Writes gameover_c_us.png (the decoded image, composited on grey) next to itself.

P1 (G)  the game-over screen: the two descriptors name kind-7 ids 0x39 (gameover_c.tm2) and 0x38 (gameover.mrp); the
        image is one 1024x256 8-bit TIM2, byte-identical in all nine full-size language folders; its pixels make two
        words, four glyphs then four (read on the rendered image as GAME OVER); the layout draws that image and
        authors one text slot with string id -1 (none); the family looks up no text id
P2 (F)  flag 0x5E: Primary-bank bit 94; set by the five aerodrome scripts before the airship map jumps and by
        rsn_z02's resident director, released by asp_a02 and rsn_z02, tested by no script; while it is set Triangle
        posts request 2 with operand word global_flag[2], or 1 when that word is 0 (not 0, as the page said)
P3 (B)  bit 12 of [02EBF190]+4: copied at load from 02089344 bit 0, which the save/load controller sets exactly when
        the load mode is 3 (the title's Trial Mode route); kept across 002370C0 by 00239960; cleared by the restore;
        the script arms (0x308D, 0x308F) are called by no shipped script; readers skip the field-menu requests
P4 (T)  field 0 is the title: 00314440 substitutes field 0xC (ttl_a01) for 0 while the debug byte 02B62DB9 is 0, and
        the only store to that byte is the reset's 0; kind-5 path 0 itself is the test map tst_a01
P5 (D)  003FFC60's five outputs in 002AE610: the argument selector (0x7F = the state's own number), the field width
        (state +0xA1, pads and keeps the low digits), bit 6 unread, bit 5 the pad character ('0' or space), bit 4
        the font's second character map
P6 (E)  bit 31 of the 8-byte glyph record: in the us and it sheets set on 0-9, A-Z, a-z and '~', clear on the space and
        every other ASCII punctuation mark; the 2.3 x (+0x34) x (+0x38) step goes before a set glyph that follows a
        clear one
P7 (H)  the pen's +8 / +0xC: the 0x0E and '*' arms only copy them into a local pen handed to 002A9F00, which reads
        +0 and +4 only; nothing on the text path reads them
P8 (S)  003BB790 dispatches on the command word 02B40E1C (0-9), not on a substate: 0 003BAC90, 1 003BA7B0, 2 003BAEB0,
        3/4/5 no handler, 6 003BA990, 7 003BA5F0 (delete the named file), 8 003BA720 (the per-slot space check), 9
        003BA680; 02B40E14 is each handler's own step, 02B40E18 the result class
P9 (C)  no: all sixteen raw-path request sites discard the returned id, nothing outside the slot module reads the slot
        table or the id counter, so no shipped code can cancel a kind-0xFF request at all
"""
import collections, hashlib, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TZA = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DB = os.path.abspath(os.path.join(TZA, ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402
from capstone import x86_const as X  # noqa: E402

FAILS = 0
PASSES = 0


def check(name, ok, detail=""):
    global FAILS, PASSES
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if ok:
        PASSES += 1
    else:
        FAILS += 1


def ins(a):
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def pin(name, a, text):
    got = ins(a)
    check(name, text in got, "%08X  %s" % (a, got))


SZ = T.sizes()


def body(f):
    return list(T.R.md.disasm(T.R.at(f, SZ[f]), f))


def u32(a):
    return struct.unpack("<I", T.R.at(a, 4))[0]


def u64(a):
    return struct.unpack("<Q", T.R.at(a, 8))[0]


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")
SC = T.scan()


def callers(f):
    return sorted(SC["calls"].get(f, ()))


def refs(g):
    return sorted(SC["refs"].get(g, ()))


OQ = open(os.path.join(TZA, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8").read().splitlines()


def row_status(rid):
    for l in OQ:
        if re.match(r"^\| *%s *\|" % re.escape(rid), l):
            return l.split("|")[-2].strip()
    return None


def page(p):
    return open(os.path.join(TZA, p), encoding="utf-8").read()


EXT = r"D:/FFXII_TZA_extract/ps2data/image/ff12"
MY = EXT + "/myoshiok"
CORPUS = os.environ.get("FF12_CORPUS", os.path.join(DB, "Tools", "work", "FABLE", "pub140-scratch", "corpus", "us"))
SCRIPTS = sorted(f for f in os.listdir(CORPUS) if f.endswith(".txt"))
LANG9 = ["ch", "cn", "de", "es", "fr", "in", "it", "kr", "us"]

# ============================================================ P1 the game-over screen
pin("G1 003EF830 points r8 at descriptor 00D11C88", 0x003EF9BD, "lea r8, [rip + 0x9222c4]")
check("G1 ... which resolves to 00D11C88", 0x003EF9C4 + 0x9222C4 == 0x00D11C88)
pin("G1 ... and hands it to 00393460", 0x003EF9C4, "call 0x393460")
pin("G1 003EF830 points r8 at descriptor 00D11CA0", 0x003EF9D7, "lea r8, [rip + 0x9222c2]")
check("G1 ... which resolves to 00D11CA0", 0x003EF9DE + 0x9222C2 == 0x00D11CA0)
pin("G1 ... and hands it to 003933F0", 0x003EF9DE, "call 0x3933f0")
pin("G1 both lists have one entry (r9d = rsi + 1, rsi = 0)", 0x003EF9D3, "lea r9d, [rsi + 1]")
pin("G1 00393460 reads the id at entry +0", 0x0039349A, "mov r8d, dword ptr [rbx - 0x10]")
pin("G1 ... and the name pointer at entry +8", 0x00393490, "mov rax, qword ptr [rbx - 8]")
pin("G1 ... and asks kind r9 + 5 = 7 (r9d = 2)", 0x003934AE, "lea edx, [r9 + 5]")
pin("G1 003933F0 asks kind 7 for each u32 id", 0x00393424, "mov edx, 7")
check("G1 00D11C88 = {id 0x39, name 'gameover_c'}", u32(0x00D11C88) == 0x39 and T.cstr(u64(0x00D11C90)) == "gameover_c",
      "%#x %r" % (u32(0x00D11C88), T.cstr(u64(0x00D11C90))))
check("G1 00D11CA0 = {id 0x38}", u32(0x00D11CA0) == 0x38, hex(u32(0x00D11CA0)))
sys.path.insert(0, os.path.join(TZA, "_index", "candidates", "rc22-34-resource-readers-0930"))
import kind7  # noqa: E402
_, K7 = kind7.paths(7)
check("G2 kind-7 id 0x39 is tm2_menu/gameover_c.tm2", K7.get(0x39, "").replace("\\", "/").lower().endswith("tm2_menu/gameover_c.tm2"), K7.get(0x39))
check("G2 kind-7 id 0x38 is mrp_menu/gameover.mrp", K7.get(0x38, "").replace("\\", "/").lower().endswith("mrp_menu/gameover.mrp"), K7.get(0x38))
check("G2 control: kind-7 id 0x3A is title.mrp (the MRP sheet's own table)", K7.get(0x3A, "").lower().endswith("title.mrp"), K7.get(0x3A))
tm = {l: open("%s/%s/tm2_menu/gameover_c.tm2" % (MY, l), "rb").read() for l in LANG9 + ["in_sdver"]}
hs = {l: hashlib.md5(b).hexdigest() for l, b in tm.items()}
check("G3 gameover_c.tm2 is byte-identical in all nine full-size language folders", len({hs[l] for l in LANG9}) == 1, str(hs))
check("G3 ... and differs only in the SD folder in_sdver", hs["in_sdver"] != hs["us"])
d = tm["us"]
o = 0x10
tot, clsz, imsz, hsz, ncol, fmt, mip, cty, ity, w, h = struct.unpack_from("<IIIHHBBBBHH", d, o)
check("G3 the image is one TIM2 picture, 1024 x 256, 8-bit indexed (type 5), 256-colour CLUT",
      d[:4] == b"TIM2" and struct.unpack_from("<H", d, 6)[0] == 1 and (w, h, ity, ncol) == (1024, 256, 5, 256),
      "%dx%d type %d clut %d" % (w, h, ity, ncol))
pix = d[o + hsz:o + hsz + imsz]
cl = d[o + hsz + imsz:o + hsz + imsz + clsz]
pal = [struct.unpack_from("<BBBB", cl, 4 * i) for i in range(ncol)]
p2 = list(pal)
for b in range(0, 256, 32):          # TIM2 CSM1 order for an 8-bit CLUT (cty bit 0x80 clear)
    for k in range(8):
        p2[b + 8 + k], p2[b + 16 + k] = pal[b + 16 + k], pal[b + 8 + k]
cols = [any(p2[pix[y * w + x]][3] >= 0x60 for y in range(h)) for x in range(w)]
runs, s0 = [], None
for x, c in enumerate(cols + [False]):
    if c and s0 is None:
        s0 = x
    if not c and s0 is not None:
        runs.append((s0, x))
        s0 = None
gaps = [runs[i + 1][0] - runs[i][1] for i in range(len(runs) - 1)]
big = [i for i, g in enumerate(gaps) if g >= 40]
check("G4 the ink (alpha >= 0x60) falls in two groups split by one gap of 40 px or more", len(big) == 1, "runs %s gaps %s" % (runs, gaps))
check("G4 ... and the first group is four separate glyphs (G, A, M, E on the render)", big == [3], str(big))
check("G4 ... spanning about 60..970 of 1024 px, centred", runs[0][0] > 40 and runs[-1][1] < 990, str((runs[0], runs[-1])))
try:
    from PIL import Image
    im = Image.new("RGB", (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = p2[pix[y * w + x]]
            a = min(255, 2 * a)
            px[x, y] = tuple(int(v * a / 255 + 40 * (255 - a) / 255) for v in (r, g, b))
    im.save(os.path.join(HERE, "gameover_c_us.png"))
    print("     wrote gameover_c_us.png (the reading of the words rests on this render)")
except ImportError:
    print("     PIL not available; gameover_c_us.png not written")


def mrp_items(b):
    n, off = struct.unpack_from("<II", b, 0x1C)
    recs = [struct.unpack_from("<IhhHH", b, off + 0x14 * i) for i in range(n)]
    p = off + 0x14 * n
    items = []
    for dw0, x, y, ww, hh in recs:
        rec = []
        for _ in range(dw0 & 0xFF):
            ln, ty = b[p], b[p + 1]
            rec.append((ty, b[p:p + ln]))
            p += ln
        items.append(((dw0 >> 10) & 0x3FFFF, x, y, ww, hh, rec))
    return items


mr = open("%s/us/mrp_menu/gameover.mrp" % MY, "rb").read()
gi = mrp_items(mr)
check("G5 gameover.mrp: three records", len(gi) == 3, str([(a, b_, c, d_, e) for a, b_, c, d_, e, _ in gi]))
r0, r1, r2 = gi
check("G5 record 0 at (474, 432), 1024 x 256, one type-2 sprite item", r0[1:5] == (474, 432, 1024, 256) and [t for t, _ in r0[5]] == [2], str(r0[:5]))
check("G5 record 1 at (1212, 878), 360 x 96, one type-8 item naming record 2", r1[1:5] == (1212, 878, 360, 96) and r1[5][0][0] == 8 and
      struct.unpack_from("<H", r1[5][0][1], 0xC)[0] == 2, str(r1[:5]))
t5 = r2[5][0][1] if r2[5] else b""
check("G5 record 2 is one type-5 text item whose string id is -1 (no string)", r2[5] and r2[5][0][0] == 5 and struct.unpack_from("<i", t5, 0x14)[0] == -1,
      t5.hex())
tcount, tail = struct.unpack_from("<II", mr, 4)          # the tail table: {count +4, offset +8}, 16-byte names
names = [mr[tail + 16 * i:tail + 16 * i + 16].split(b"\0")[0].decode() for i in range(tcount)]
check("G5 its one atlas name is gameover_c", names == ["gameover_c"], str(names))
check("G5 the nine full-size gameover.mrp copies are byte-identical",
      len({hashlib.md5(open("%s/%s/mrp_menu/gameover.mrp" % (MY, l), "rb").read()).hexdigest() for l in LANG9}) == 1)
pin("G5 control: the type-5 constructor treats string id -1 as no string", 0x0029FF45, "cmp ecx, -1")
ctl = mrp_items(open("%s/us/mrp_menu/save_load.mrp" % MY, "rb").read())
sid = [struct.unpack_from("<i", raw, 0x14)[0] for *_, rec in ctl for ty, raw in rec if ty == 5]
check("G5 control: the same walker finds type-5 items with real string ids in save_load.mrp", any(v != -1 for v in sid), str(sid[:8]))
pin("G6 the record-0 widget 003EF4A0 decodes record 0", 0x003EF4DF, "xor r8d, r8d")
pin("G6 ... through the typed-list decoder", 0x003EF4E2, "call 0x2432b0")
pin("G6 the record-1 widget 003EF050 decodes record 1", 0x003EF08F, "mov r8d, 1")
pin("G6 ... through the typed-list decoder", 0x003EF095, "call 0x2432b0")
fam = [f for f in SZ if 0x003EE000 <= f < 0x003F0000]
lk = [(f, s) for f, s in callers(0x002F9860) if f in fam] + [(f, s) for f, s in callers(0x002F9920) if f in fam]
check("G6 no function of the family 003EE000..003F0000 calls a text lookup (002F9860 / 002F9920)", not lk, str(lk))
check("G6 control: 002F9920 has callers elsewhere (the type-5 constructor 0029FF4A)", any(s == 0x0029FF4A for _, s in callers(0x002F9920)))

# ============================================================ P2 flag 0x5E
pin("F1 the gate masks the id to 14 bits", 0x0032A8A8, "and edi, 0x3fff")
pin("F1 ... and tests bit (id & 7) of payload +0x14F4 + (id >> 3)", 0x0032A900, "test byte ptr [rax + rbx + 0x14f4], dl")
check("F1 so 0x5E is byte 11 bit 6 of the Primary bank (payload +0x14FF)", (0x5E >> 3, 0x5E & 7, 0x14F4 + (0x5E >> 3)) == (11, 6, 0x14FF))
pin("F2 00253C70 asks the gate for 0x5E", 0x00253F1E, "lea ecx, [rax + 0x5e]")
pin("F2 ... (the call)", 0x00253F21, "call 0x32a8a0")
pin("F2 set: operand word 00264640(esi)", 0x00253F2C, "call 0x264640")
pin("F2 ... re-read into ebx only when non-zero", 0x00253F3D, "movsx ebx, ax")
pin("F2 ... and ebx is the parameter", 0x00253F40, "mov edx, ebx")
pin("F2 ... posted with request esi", 0x00253F44, "call 0x2e1b10")
pin("F2 clear: parameter 0x21", 0x00253F4E, "mov edx, 0x21")
pin("F2 ebx starts as 1 (edi = 0)", 0x00253D12, "xor edi, edi")
pin("F2 ... lea ebx, [rdi + 1]", 0x00253D14, "lea ebx, [rdi + 1]")
pin("F2 esi is request 2", 0x00253D88, "mov esi, 2")
T.R.md.detail = True
RB = {X.X86_REG_RBX, X.X86_REG_EBX, X.X86_REG_BX, X.X86_REG_BL, X.X86_REG_BH}
RS = {X.X86_REG_RSI, X.X86_REG_ESI, X.X86_REG_SI, X.X86_REG_SIL}
win = [i for i in body(0x00253C70) if 0x00253D14 < i.address < 0x00253F3D]
wb = [("%08X" % i.address, i.mnemonic) for i in win if i.mnemonic != "call" and set(i.regs_access()[1]) & (RB | RS) and i.address != 0x00253D88]
check("F2 nothing writes ebx or esi between 00253D14 and 00253F3D but the esi = 2 store", not wb, str(wb))
back = [("%08X" % i.address, i.op_str) for i in body(0x00253C70) if i.mnemonic.startswith("j") and i.op_str.startswith("0x")
        and 0x00253D14 < int(i.op_str, 16) <= 0x00253F44 and not 0x00253D14 <= i.address <= 0x00253F44]
check("F2 ... and no jump enters that window from outside it", not back, str(back))
check("F2 so a zero operand word posts parameter 1, which the 2 / 22 arm reads as the airship-route page (b13 R7: 1..0x20)", True)
pin("F3 00264640 reads the i16 table at 02098E58", 0x00264651, "mov rdx, qword ptr [rip + 0x1e34800]")
check("F3 ... which resolves to 02098E58", 0x00264658 + 0x1E34800 == 0x02098E58)
fm = page("19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md")
check("F3 the payload map calls 02098E58 the kind-3 authored-operand bank, i16[256] (payload +0, the scripts' global_flag[256])",
      "the kind-3 authored-operand bank, `i16[256]`" in fm and "02098E58" in fm)
gimp = collections.Counter()
for f in SCRIPTS:
    for m in re.finditer(r"import global +short +global_flag\[256\] = (0x[0-9a-f]+);", open(os.path.join(CORPUS, f), encoding="utf-8", errors="replace").read()):
        gimp[m.group(1)] += 1
check("F3 control: every script that imports global_flag[256] imports it at offset 0x00 (%d scripts)" % sum(gimp.values()),
      list(gimp) == ["0x00"] and sum(gimp.values()) > 100, str(dict(gimp)))
pat = re.compile(r"\b(set|release|is)mapjumpgroupflag\((94|0x5[eE])\)")
uses = collections.defaultdict(list)
fnre = re.compile(r"^\tfunction (\S+)\(")
for f in SCRIPTS:
    fn = None
    lines = open(os.path.join(CORPUS, f), encoding="utf-8", errors="replace").read().splitlines()
    for k, l in enumerate(lines):
        m = fnre.match(l)
        if m:
            fn = m.group(1)
        for mm in pat.finditer(l):
            nxt = " ".join(x.strip() for x in lines[k + 1:k + 3])
            uses[mm.group(1)].append((f, fn, k + 1, nxt))
cs = collections.Counter(f for f, *_ in uses["set"])
cr = collections.Counter(f for f, *_ in uses["release"])
check("F4 setmapjumpgroupflag(94): 21 sites, four in each of alc_e01, byu_b01, nac_b01, rbn_b01, var_b01 and one in rsn_z02",
      dict(cs) == {"alc_e01.txt": 4, "byu_b01.txt": 4, "nac_b01.txt": 4, "rbn_b01.txt": 4, "var_b01.txt": 4, "rsn_z02.txt": 1}, str(dict(cs)))
check("F4 releasemapjumpgroupflag(94): three in asp_a02 and one in rsn_z02", dict(cr) == {"asp_a02.txt": 3, "rsn_z02.txt": 1}, str(dict(cr)))
check("F4 ismapjumpgroupflag(94): no script tests it", not uses["is"], str(uses["is"]))
aer = [u for u in uses["set"] if u[0] != "rsn_z02.txt"]
mj = [u for u in aer if re.search(r"mapjump\((124|125),", u[3])]
check("F4 every aerodrome set is followed at once by mapjump(124 or 125, ...)", len(mj) == len(aer) == 20, str([(u[0], u[2], u[3][:40]) for u in aer if u not in mj]))
hs_fn = {u[0] for u in aer if u[1] == "高速移動時のマップジャンプ"}
check("F4 each of the five aerodrome scripts sets it in its function 高速移動時のマップジャンプ ('map jump for high-speed travel')",
      hs_fn == {"alc_e01.txt", "byu_b01.txt", "nac_b01.txt", "rbn_b01.txt", "var_b01.txt"}, str(sorted(hs_fn)))
rz = [u for u in uses["set"] if u[0] == "rsn_z02.txt"]
check("F4 rsn_z02 sets it in its resident director's init, next to global_flag[2] = 15", rz and rz[0][1] == "init" and "global_flag[2] = 15;" in rz[0][3], str(rz))
K5 = 0x01EE23A0


def k5(i):
    return T.cstr(u64(K5 + 24 * i), 160) or ""


check("F5 the map-jump targets: field 124 is asp_a01 and field 125 is asp_a02", k5(124).endswith("asp_a01.ebp") and k5(125).endswith("asp_a02.ebp"),
      "%s / %s" % (k5(124), k5(125)))
mjt = open(os.path.join(TZA, "14-Story-Event-Quest-Hunt", "members", "mapjump-flag-census.tsv"), encoding="utf-8").read().splitlines()
row = [l for l in mjt if l.startswith("0x5E\t")]
check("F5 control: mapjump-flag-census.tsv's 0x5E row reads set 21, release 4, is 0, 7 scripts", row and row[0].split("\t")[2:6] == ["21", "4", "0", "7"], str(row))
ib = open(EXT + "/us/bin/mapjumpgroupinit.bin", "rb").read()
init = set(struct.unpack_from("<%dH" % struct.unpack_from("<H", ib, 8)[0], ib, 10))
check("F5 mapjumpgroupinit.bin does not pre-set 0x5E (a new game starts with it clear)", ib[:8] == b"FLAGDEF1" and 0x5E not in init and 0x80 in init)
nat = [(f, s) for f, s in callers(0x0032AB60)]
check("F5 the Primary setter's direct callers: the two verb handlers, 0035CA70, the init walker 00379160, the thunk 0032ABE0",
      sorted(f for f, _ in nat) == [0x0032ABE0, 0x0034DD90, 0x0034EE20, 0x0035CA70, 0x00379160], str(nat))
pin("F5 ... 0035CA70's literal id is 0x73, not 0x5E", 0x0035CE76, "lea ecx, [rdx + 0x73]")
vt = os.path.join(TZA, "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
VT = [l.split("\t") for l in open(vt, encoding="utf-8").read().splitlines()]
vh = {r[3]: r[15] for r in VT[1:] if len(r) > 15 and r[3] in ("setmapjumpgroupflag", "releasemapjumpgroupflag")}
check("F5 the verb table binds setmapjumpgroupflag to 0034EE20 and releasemapjumpgroupflag to 0034DD90",
      vh == {"setmapjumpgroupflag": "0034EE20", "releasemapjumpgroupflag": "0034DD90"}, str(vh))
pin("F5 ... set passes 1", 0x0034EE2C, "mov edx, 1")
pin("F5 ... release passes 0", 0x0034DD9C, "xor edx, edx")

# ============================================================ P3 bit 12 of [02EBF190]+4
pin("B1 the save/load controller reads the load mode", 0x00582CBA, "call 0x394450")
pin("B1 ... compares it with 3", 0x00582CBF, "cmp al, 3")
pin("B1 ... mode 3: 00238A30(1)", 0x00582CC8, "call 0x238a30")
pin("B1 ... otherwise 00238A30(0)", 0x00582CDE, "call 0x238a30")
pin("B1 ... then 00285E60 (which runs 00233C10)", 0x00582CD0, "call 0x285e60")
pin("B1 00238A30 sets 02089344 bit 0 for a non-zero argument", 0x00238A40, "cmovne edx, eax")
pin("B1 00285E60 calls 00233C10", 0x00285E86, "call 0x233c10")
pin("B1 00233C10 tests 02089344 bit 0", 0x00233C65, "test byte ptr [rip + 0x1e556d8], 1")
pin("B1 ... set: block +4 bit 12 set", 0x00233C6E, "or dword ptr [rax + 4], 0x1000")
pin("B1 ... and 02089344 bit 0 consumed", 0x00233C7C, "and dword ptr [rip + 0x1e556c1], 0xfffffffe")
pin("B1 ... clear: block +4 bit 12 cleared", 0x00233CA6, "and dword ptr [rax + 4], 0xffffefff")
w344 = sorted(set(f for f, a, k in refs(0x02089344) if k == "W"))
check("B1 02089344's writers image-wide: 00233C10, 00238A20, 00238A30, 00238A50 and 00239960",
      w344 == [0x00233C10, 0x00238A20, 0x00238A30, 0x00238A50, 0x00239960], " ".join("%08X" % x for x in w344))
pin("B1 ... 00238A20 sets bit 1 only", 0x00238A20, "or dword ptr [rip + 0x1e5091d], 2")
pin("B1 ... 00238A50 sets bit 2 only", 0x00238A50, "or dword ptr [rip + 0x1e508ed], 4")
pin("B1 ... 00239960 clears bit 1", 0x00239A63, "and eax, 0xfffffffd")
pin("B1 ... and bit 2", 0x00239A7E, "and dword ptr [rip + 0x1e4f8bf], 0xfffffffb")
check("B1 so bit 0 is written only by 00238A30 and consumed by 00233C10", True)
check("B1 00238A30's callers: the controller's two calls and 0050F5A0 (verb 0x308F's callback)",
      sorted(callers(0x00238A30)) == [(0x0050F5A0, 0x0050F5A5), (0x00582860, 0x00582CC8), (0x00582860, 0x00582CDE)], str(callers(0x00238A30)))
pin("B2 00239960 saves block +4 before 002370C0", 0x002399D7, "mov ebx, dword ptr [rax + 4]")
pin("B2 ... (the rebuild call)", 0x002399E9, "call 0x2370c0")
pin("B2 ... and puts bit 12 back from the saved word", 0x00239A2F, "bt ebx, 0xc")
pin("B2 0023A390 sets or clears bit 12 by its argument", 0x0023A39B, "or dword ptr [rax + 4], 0x1000")
check("B2 0023A390's callers: verb 0x308D's handler 0050F500 and the load normaliser 00584210",
      sorted(f for f, _ in callers(0x0023A390)) == [0x0050F500, 0x00584210], str(callers(0x0023A390)))
pin("B2 the restore path clears it: 0023A390(0)", 0x00584393, "call 0x23a390")
cnt = collections.Counter()
for f in SCRIPTS:
    t = open(os.path.join(CORPUS, f), encoding="utf-8", errors="replace").read()
    for v in ("308c", "308d", "308e", "308f"):
        cnt[v] += t.count("unkCall_%s(" % v)
check("B3 no shipped us script calls verb 0x308D, 0x308E or 0x308F", cnt["308d"] == cnt["308e"] == cnt["308f"] == 0, str(dict(cnt)))
check("B3 control: their neighbour 0x308C is called 854 times", cnt["308c"] == 854, str(cnt["308c"]))
fv1 = row_status("FV-1") or ""
check("B3 register FV-1 is ANSWERED: load mode 3 is the title's Trial Mode load route", fv1.lstrip("*").startswith("ANSWERED"), fv1[:60])
fvq = [l for l in OQ if l.startswith("| FV-1 ")]
check("B3 ... the row says mode 3 drops a loaded save into the first Trial Mode field", fvq and "Trial Mode" in fvq[0])
for site, nxt, what in ((0x00253E10, 0x00253E17, "the request path at 00253E10"), (0x00253ED4, 0x00253EDB, "the 0x21 post at 00253EE6"),
                        (0x00253F11, 0x00253F18, "Triangle's flag-0x5E path")):
    pin("B4 bit 12 set skips %s" % what, site, "call 0x236760")
    check("B4 ... (jne past it at %08X)" % nxt, ins(nxt).startswith("jne"), ins(nxt))
pin("B4 the save finaliser turns bit 12 into header +0x57 bit 0", 0x00583F5A, "call 0x236760")
check("B4 the getter 00236760's direct callers include the persistence-pair capture 00584580 and restore 005843E0",
      {0x00584580, 0x005843E0} <= set(f for f, _ in callers(0x00236760)))

# ============================================================ P4 field 0
pin("T1 a bad header (00255260 non-zero is good) clears bit 9", 0x00280387, "and dword ptr [rax + 8], 0xfffffdff")
pin("T1 ... sets bit 8", 0x002803A3, "or dword ptr [rax + 8], 0x100")
pin("T1 ... edi = 0", 0x002803B1, "xor edi, edi")
pin("T1 ... target +4 = 0", 0x002803B3, "mov dword ptr [rax + 4], edi")
pin("T2 message 18's bit-8 arm compares the target with 0xC", 0x00280252, "cmp dword ptr [rcx + 4], 0xc")
pin("T2 ... 0xC goes to 003603E0", 0x0028025B, "call 0x3603e0")
pin("T2 ... anything else to 00314440(target)", 0x00280279, "mov ecx, dword ptr [rax + 4]")
pin("T2 ... (the call)", 0x0028027C, "call 0x314440")
pin("T3 00314440 asks 00408B00", 0x0031445E, "call 0x408b00")
pin("T3 ... non-zero skips the substitution", 0x00314465, "jne 0x314471")
pin("T3 ... a zero target", 0x00314467, "test ebx, ebx")
pin("T3 ... becomes 0xC", 0x00314469, "mov eax, 0xc")
pin("T3 ... (cmove)", 0x0031446E, "cmove ebx, eax")
pin("T3 00408B00 returns the byte 02B62DB9", 0x00408B00, "movzx eax, byte ptr [rip + 0x275a2b2]")
check("T3 ... (02B62DB9)", 0x00408B07 + 0x275A2B2 == 0x02B62DB9)
wdb9 = [(f, a) for f, a, k in refs(0x02B62DB9) if k == "W"]
check("T3 02B62DB9's one store image-wide is the reset 00408BA0 at 00408BBC", wdb9 == [(0x00408BA0, 0x00408BBC)], str(wdb9))
pin("T3 ... which stores al", 0x00408BBC, "mov byte ptr [rip + 0x275a1f7], al")
pin("T3 ... with eax = 0", 0x00408BA0, "xor eax, eax")
fc = page("19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md")
check("T3 the debug-global page: 02B62DB9 has no writer but the reset; 00314440 substitutes field 0xC when it is 0",
      "no writer but the reset" in fc and "substitutes field `0xC` when `02B62DB9` is 0" in fc)
check("T4 kind-5 path 12 is ttl_a01, the title map", k5(12).endswith("plan_map\\ttl_a\\ttl_a01\\global\\ttl_a01.ebp"), k5(12))
check("T4 kind-5 path 0 is the test map tst_a01 (a plan_work path)", k5(0).endswith("plan_map\\tst_a\\tst_a01\\global\\tst_a01.ebp") and "plan_work" in k5(0), k5(0))
check("T4 control: kind-5 path 0x132 is rbn_a18 (the cutscene page's live Southgate control)", k5(0x132).endswith("rbn_a18.ebp"), k5(0x132))
check("T4 control: kind-5 path 0x483 is tri_a01 (FV-1's Trial Mode field)", k5(0x483).endswith("tri_a01.ebp"), k5(0x483))
tst = open(os.path.join(CORPUS, "tst_a01.txt"), encoding="utf-8").read()
check("T4 tst_a01 places four party members and has no exit, map jump or menu call",
      tst.count("setupbattle(") == 4 and "mapjump(" not in tst and "openfullscreenmenu" not in tst and "mapExitGroup0[0]" in tst)

# ============================================================ P5 003FFC60 in the number formatter
for a, t in ((0x003FFC68, "movzx eax, byte ptr [rcx + 1]"), (0x003FFC6C, "and al, 0x7f"), (0x003FFC7E, "and cl, 0xf"),
             (0x003FFC86, "cmova eax, edx"), (0x003FFC96, "shr eax, 6"), (0x003FFCAE, "shr eax, 5"), (0x003FFCC5, "shr eax, 4")):
    pin("D1 003FFC60: %s" % t, a, t)
for a, t, what in ((0x002AE74F, "lea rdx, [rsp + 0x34]", "out1 -> [rsp+0x34]"), (0x002AE75D, "xor r8d, r8d", "out2 not asked"),
                   (0x002AE72C, "lea r9, [rsp + 0x40]", "bit 6 -> [rsp+0x40]"), (0x002AE743, "lea rax, [rsp + 0x3c]", "bit 5 -> [rsp+0x3c]"),
                   (0x002AE754, "mov qword ptr [rsp + 0x20], rax", "... as the fifth argument"),
                   (0x002AE739, "lea rax, [rsp + 0x38]", "bit 4 -> [rsp+0x38]"), (0x002AE73E, "mov qword ptr [rsp + 0x28], rax", "... as the sixth"),
                   (0x002AE760, "call 0x3ffc60", "the call")):
    pin("D2 002AE610 sets up 003FFC60: %s" % what, a, t)
pin("D3 out1 must be 0x7F", 0x002AE823, "cmp byte ptr [rsp + 0x34], 0x7f")
pin("D3 ... equal: format the number", 0x002AE83D, "je 0x2ae86a")
pin("D3 ... otherwise zero the spacing block and return, drawing nothing", 0x002AE841, "mov qword ptr [rip + 0x1dee418], rax")
pin("D3 the '.' arm hands the formatter a copy with byte 1 = 0xFF", 0x002ADB07, "mov byte ptr [rip + 0x1b5f2fb], 0xff")
pin("D3 ... after selecting argument n = out1 (16-byte entries)", 0x002AD930, "movzx edx, byte ptr [rsp + 0x4c]")
pin("D3 ... and the copy's number +0x54 is the argument's value", 0x002ADBA4, "mov dword ptr [rbp - 0x1c], eax")
pin("D4 the '-' arm asks out2 into state +0xA1", 0x002AD8B0, "lea r8, [r14 + 0xa1]")
pin("D4 the '.' arm asks out2 into [rsp+0x42]", 0x002AD8FD, "lea r8, [rsp + 0x42]")
pin("D4 ... and stores it in the copy's +0xA1", 0x002ADBAC, "mov byte ptr [rbp + 0x31], al")
check("D4 ... (rbp + 0x31 = copy rbp - 0x70, + 0xA1)", -0x70 + 0xA1 == 0x31)
pin("D4 the formatter takes max(+0xA1, +0xA2) as the width", 0x002AE7AC, "cmova ecx, eax")
pin("D4 ... into the count", 0x002AE7B4, "mov dword ptr [r14], eax")
pin("D4 width 0: the natural digit count", 0x002AE86A, "cmp dword ptr [r14], 0")
pin("D4 ... but at least +0x98 + 1", 0x002AE8A7, "cmovl ecx, eax")
pin("D4 a width keeps the low digits: subtract 10^width while the value reaches it", 0x002AE8C3, "sub ecx, dword ptr [rdx + rax*4]")
tbl = [struct.unpack("<i", T.R.at(0x00916520 + 4 * i, 4))[0] for i in range(9)]
check("D4 ... 00916520 is 10^0 .. 10^8 (the width clamp is 8)", tbl == [10 ** i for i in range(9)], str(tbl))
pin("D5 bit 5 goes to 003EFD00 as its fourth argument", 0x002AE8D1, "mov r9d, dword ptr [rsp + 0x3c]")
pin("D5 003EFD00's fill is '0'", 0x003EFD59, "mov edx, 0x30")
pin("D5 ... unless the flag is 0", 0x003EFD78, "test r9d, r9d")
pin("D5 ... then a space", 0x003EFD7D, "mov edx, 0x20")
pin("D5 ... memset over the width", 0x003EFD82, "call 0x861ec0")
pin("D6 bit 4 chooses the sheet's map at +0x18", 0x002AE861, "mov ecx, dword ptr [r15 + 0x18]")
pin("D6 ... instead of +0x14", 0x002AE77C, "mov ecx, dword ptr [r15 + 0x14]")
pin("D6 ... and is forced off on the alternate sheet (+0x44 bit 11)", 0x002AE774, "mov dword ptr [rsp + 0x38], 0")
pin("D6 ... it also picks fallback code 1 instead of 7", 0x002AE820, "cmovne eax, ecx")
pin("D6 ... and suppresses the leading step (r13d)", 0x002AEA5D, "test r8d, r8d")
r40 = [i for i in body(0x002AE610) if "rsp + 0x40]" in i.op_str]
check("D7 bit 6 ([rsp+0x40]) is only zeroed and its address taken: never read",
      [(i.address, i.mnemonic) for i in r40] == [(0x002AE680, "mov"), (0x002AE72C, "lea")], str([(hex(i.address), i.mnemonic, i.op_str) for i in r40]))
fp = open("%s/us/packfiles/fontpack_it.bin" % MY, "rb").read()
d0 = struct.unpack_from("<I", fp, 0)[0]
blk = d0 + 0x40
gt, ma, mb = (struct.unpack_from("<I", fp, blk + o)[0] for o in (0xC, 0x14, 0x18))
A = struct.unpack_from("<224H", fp, blk + ma)
Bm = struct.unpack_from("<224H", fp, blk + mb)
check("D8 us primary sheet: map +0x14 sends '0'..'9' to 0x85..0x8E", fp[d0:d0 + 4] == b"TIM2" and list(A[16:26]) == list(range(0x85, 0x8F)), str([hex(x) for x in A[16:26]]))
check("D8 ... map +0x18 sends them to the two-byte codes 0x3010..0x3910", list(Bm[16:26]) == [0x3010 + 0x100 * k for k in range(10)], str([hex(x) for x in Bm[16:26]]))
check("D8 ... and 'A' to 0x20 against 0xDC", A[0x21] == 0x20 and Bm[0x21] == 0xDC, "%#x %#x" % (A[0x21], Bm[0x21]))
pin("D8 the relocator rebases +0x14 against the block", 0x0039C00E, "mov ecx, dword ptr [rdi + 0x14]")
pin("D8 ... and +0x18", 0x0039C024, "mov ecx, dword ptr [rdi + 0x18]")
pin("D8 ... the block is the picture header + 0x30 (TIM2 + 0x40)", 0x0039BFC2, "lea rdi, [rbx + 0x30]")
pin("D8 control: 0039C4A0(0) returns [02AEE800], the sheet the loader page binds as TIM2 + 0x40", 0x0039C4B0, "mov rax, qword ptr [rip + 0x2752349]")

# ============================================================ P6 bit 31 of the glyph record
pin("E1 002A9F00's state copy is at rsp + 0x60", 0x002A9F2C, "lea r9, [rsp + 0x60]")
pin("E1 ... rbp = r11 - 0x1B8", 0x002A9F0A, "lea rbp, [r11 - 0x1b8]")
pin("E1 ... rsp = r11 - 0x28 - 0x290", 0x002A9F11, "sub rsp, 0x290")
check("E1 so rbp - 0x40 is the copy's +0x60, the sheet pointer (b13 N1)", (0x2B8 - 0x1B8) - 0x60 - 0x60 == 0x40)
pin("E1 the glyph table is sheet + [sheet + 0xC]", 0x002AA0F8, "mov ecx, dword ptr [rdi + 0xc]")
pin("E1 ... (relocated like the maps)", 0x0039BFFB, "mov ecx, dword ptr [rdi + 0xc]")
pin("E1 the record's low dword", 0x002AA117, "mov ecx, dword ptr [r12 + rbx*8]")
pin("E1 ... bit 31", 0x002AA129, "mov eax, 0x80000000")
pin("E2 set: if the class state is 2", 0x002AA13A, "cmp byte ptr [rcx + 0x10fc], 2")
pin("E2 ... add +0x34 x 2.3 x +0x38 to the pen", 0x002AA148, "mulss xmm0, xmm14")
pin("E2 ... (xmm14 = [009166F4])", 0x002AA00C, "movss xmm14, dword ptr [rip + 0x66c6df]")
check("E2 ... 009166F4 is 2.3f", abs(struct.unpack("<f", T.R.at(0x009166F4, 4))[0] - 2.3) < 1e-6)
pin("E2 ... then state 1", 0x002AA15C, "mov byte ptr [rcx + 0x10fc], 1")
pin("E2 clear: state 2", 0x002AA16C, "mov byte ptr [rax + 0x10fc], 2")


def sheet(lang):
    b = open("%s/%s/packfiles/fontpack_it.bin" % (MY, lang), "rb").read()
    z = struct.unpack_from("<I", b, 0)[0] + 0x40
    g, a_, b_ = (struct.unpack_from("<I", b, z + o)[0] for o in (0xC, 0x14, 0x18))
    n = (a_ - g) // 8
    rec = [struct.unpack_from("<II", b, z + g + 8 * i) for i in range(n)]
    amap = struct.unpack_from("<95H", b, z + a_)
    return rec, amap


pin("E3 a single-byte code c (>= 0x20) is glyph c - 0x20", 0x002AC37C, "sub esi, 0x20")
pin("E3 ... a byte below 0x20 leads a two-byte code (base table 00916570 + second byte - 0x20)", 0x002AC3B9, "add esi, -0x20")
pin("E3 ... and 002AC2F0 tests the same bit 31 on that record", 0x002AC4B8, "mov eax, 0x80000000")
SETUS = set(range(0x20, 0x8F)) | {0x93, 0x94} | set(range(0x98, 0xB7))
for lang in ("us", "it"):
    rec, amap = sheet(lang)
    on = {c for c in range(0x20, 0x100) if rec[c - 0x20][0] >> 31}
    check("E3 %s sheet: of the single-byte codes 0x20-0xFF bit 31 is set on exactly 0x20-0x8E, 0x93-0x94 and 0x98-0xB6" % lang,
          on == SETUS, " ".join("%02X" % c for c in sorted(on ^ SETUS)))
    two = [i for i in range(0xE0, len(rec)) if rec[i][0] >> 31]
    check("E3 %s sheet: and on no glyph past the single-byte block (indices 0xE0 on, the two-byte glyphs)" % lang, not two, str(two[:8]))
    asc = [chr(0x20 + k) for k in range(1, 95) if not (0x20 <= amap[k] < 0x100 and rec[amap[k] - 0x20][0] >> 31)]
    check("E3 %s sheet: every printable ASCII character but the space maps (map +0x14) to a glyph with bit 31 set" % lang, not asc, str(asc))
    adv = {rec[c - 0x20][1] & 0x1F for c in range(0x85, 0x8F)}
    check("E3 control (%s): the ten digit glyphs 0x85-0x8E share one advance (AC-10: digits monospaced)" % lang, len(adv) == 1, str(adv))
    check("E3 control (%s): 'I' (0x28) is narrower than 'W' (0x36), so the record table is the right one" % lang,
          (rec[0x08][1] & 0x1F) < (rec[0x16][1] & 0x1F), "%d %d" % (rec[0x08][1] & 0x1F, rec[0x16][1] & 0x1F))
for lang in ("kr", "cn", "ch", "in"):
    rec, amap = sheet(lang)
    n_on = sum(r[0] >> 31 for r in rec)
    check("E4 %s sheet: bit 31 is the minority (%d of %d records), one Latin block among the two-byte glyphs" % (lang, n_on, len(rec)),
          0 < n_on < len(rec) // 5, str(n_on))
# the glyph render behind the README's naming of the clear groups: x = lo & 0x3FF, y = lo >> 10 & 0x3FF, advance = hi & 0x1F
try:
    from PIL import Image, ImageDraw
    fb = open("%s/us/packfiles/fontpack_it.bin" % MY, "rb").read()
    q0 = struct.unpack_from("<I", fb, 0)[0]
    _, _, isz, hz, _, _, _, _, ity2, FW, FH = struct.unpack_from("<IIIHHBBBBHH", fb, q0 + 0x10)
    fpx = fb[q0 + 0x10 + hz:q0 + 0x10 + hz + isz]
    rec, _ = sheet("us")
    cv = Image.new("L", (40 * 30, 6 * 40), 40)
    dr = ImageDraw.Draw(cv)
    for k, c in enumerate(range(0x20, 0x100)):
        lo, hi = rec[c - 0x20]
        gx, gy, gw = lo & 0x3FF, (lo >> 10) & 0x3FF, (hi & 0x1F) + 2
        for yy in range(24):
            for xx in range(gw):
                if gx + xx < FW and gy + yy < FH:
                    v = fpx[((gy + yy) * FW + gx + xx) // 2]
                    cv.putpixel(((k % 40) * 30 + xx, (k // 40) * 40 + yy), ((v >> 4) if (gx + xx) & 1 else (v & 0xF)) * 17)
        dr.text(((k % 40) * 30, (k // 40) * 40 + 26), "%X" % c, fill=255 if lo >> 31 else 120)
    cv.resize((cv.width * 2, cv.height * 2)).save(os.path.join(HERE, "glyphs_us_20_FF.png"))
    print("     wrote glyphs_us_20_FF.png (bright code = bit 31 set, grey = clear)")
except ImportError:
    print("     PIL not available; glyphs_us_20_FF.png not written")
check("E4 control: AC-10 reads ANSWERED", (row_status("AC-10") or "").lstrip("*").startswith("ANSWERED"))

# ============================================================ P7 the pen's +8 / +0xC
for a, t in ((0x002AC8A4, "movss xmm2, dword ptr [r12 + 0xc]"), (0x002AC8DB, "movss dword ptr [rbp + 0x6c], xmm2"),
             (0x002AC8BD, "movss xmm1, dword ptr [r12 + 8]"), (0x002AC8E4, "movss dword ptr [rbp + 0x68], xmm1"),
             (0x002ACAB4, "lea r8, [rbp + 0x60]"), (0x002ACABD, "call 0x2a9f00")):
    pin("H1 the 0x0E arm: %s" % t, a, t)
for a, t in ((0x002AD690, "movss xmm0, dword ptr [r12 + 8]"), (0x002AD6A2, "movss dword ptr [rbp + 0x78], xmm0"),
             (0x002AD69B, "movss xmm1, dword ptr [r12 + 0xc]"), (0x002AD6B1, "movss dword ptr [rbp + 0x7c], xmm1"),
             (0x002AD71F, "lea r8, [rbp + 0x70]"), (0x002AD728, "call 0x2a9f00")):
    pin("H2 the '*' arm: %s" % t, a, t)
B5 = body(0x002AC5F0)
loc = [(hex(i.address), i.mnemonic, i.op_str) for i in B5 if re.search(r"\[rbp \+ 0x(68|6c|78|7c)\]", i.op_str) and not i.op_str.startswith("dword ptr [rbp")]
check("H3 002AC5F0 never reads the local slots rbp+0x68 / +0x6C / +0x78 / +0x7C (stores only)", not loc, str(loc))
v16 = [(hex(i.address), i.mnemonic) for i in B5 if re.search(r"xmm\d+, xmmword ptr \[rbp \+ 0x(60|70)\]", i.op_str)]
check("H3 ... and never loads the local pens as 16-byte vectors", not v16, str(v16))
r12 = sorted({i.op_str.split("[r12 + ")[1].split("]")[0] for i in B5 if "[r12 + 0x" in i.op_str or "[r12 + 8]" in i.op_str})
check("H3 the pen's +8 / +0xC appear in 002AC5F0 only in the four copies", [(hex(i.address)) for i in B5 if re.search(r"\[r12 \+ (8|0xc)\]", i.op_str)] ==
      ["0x2ac8a4", "0x2ac8bd", "0x2ad690", "0x2ad69b"])
r15 = sorted({i.op_str for i in body(0x002A9F00) if "r15" in i.op_str and "[r15" in i.op_str})
check("H4 002A9F00 touches its pen (r15) only at +0 and +4", all(re.search(r"\[r15( \+ 4)?\]", s) for s in r15), str(r15))
w15 = [(hex(i.address), i.op_str) for i in body(0x002A9F00) if i.mnemonic in ("mov", "lea") and i.op_str.startswith("r15,")]
check("H4 ... and r15 is set once, from r8 (002A9F37)", w15 == [("0x2a9f37", "r15, r8")], str(w15))
for f, reg in ((0x002AE450, "rsi"), (0x002AEB20, "r15")):
    ac = sorted({re.search(r"\[%s( \+ 0x[0-9a-f]+| \+ \d+)?\]" % reg, i.op_str).group(0) for i in body(f)
                 if re.search(r"\[%s( \+ 0x[0-9a-f]+| \+ \d+)?\]" % reg, i.op_str)})
    check("H4 the pen callee %08X reads its pen (%s) at +0 / +4 only" % (f, reg), all(x in ("[%s]" % reg, "[%s + 4]" % reg) for x in ac) or f == 0x002AEB20, str(ac))
pin("H4 002AEB20's pen is r15 until it is reloaded", 0x002AEB6B, "mov r15, r8")
pin("H4 ... reloaded with a table pointer at 002AEEE2", 0x002AEEE2, "mov r15, qword ptr [rbx + 0x20]")
pre = [i.op_str for i in body(0x002AEB20) if i.address < 0x002AEEE2 and "[r15" in i.op_str]
check("H4 ... and before that reads only [r15] and [r15 + 4]", sorted(set(re.search(r"\[r15[^\]]*\]", s).group(0) for s in pre)) == ["[r15 + 4]", "[r15]"], str(pre))
uq = row_status("UQ-165") or ""
check("H5 register UQ-165 reads ANSWERED (components [2] and [3] carried but unread on 002AE610's path)", uq.lstrip("*").startswith("ANSWERED"), uq[:60])

# ============================================================ P8 the storage machine
dsp = [(0x003BB809, "cmp eax, 1", 0x003BB810, "call 0x3ba7b0"), (0x003BB81F, "cmp eax, 6", 0x003BB826, "call 0x3ba990"),
       (0x003BB835, "cmp eax, 2", 0x003BB83C, "call 0x3baeb0"), (0x003BB84B, "test eax, eax", 0x003BB851, "call 0x3bac90"),
       (0x003BB888, "cmp eax, 7", 0x003BB88F, "call 0x3ba5f0"), (0x003BB89E, "cmp eax, 8", 0x003BB8A5, "call 0x3ba720"),
       (0x003BB8B0, "cmp eax, 9", 0x003BB8B7, "call 0x3ba680")]
pin("S1 003BB790 dispatches on the command word 02B40E1C", 0x003BB803, "mov eax, dword ptr [rip + 0x2785613]")
check("S1 ... (02B40E1C)", 0x003BB809 + 0x2785613 == 0x02B40E1C)
for a, t, c, ct in dsp:
    pin("S1 %s" % t, a, t)
    pin("S1 ... -> %s" % ct.split()[-1], c, ct)
for a, t in ((0x003BB860, "cmp eax, 3"), (0x003BB865, "cmp eax, 4"), (0x003BB86A, "cmp eax, 5")):
    pin("S1 command %s: no handler" % t[-1], a, t)
pin("S1 ... 3 / 4 / 5 clear 02B40E14..1B", 0x003BB876, "mov qword ptr [rip + 0x2785597], rax")
pin("S1 ... and 02B40E10 (idle)", 0x003BB87D, "mov dword ptr [rip + 0x278558d], eax")
pin("S1 the result classes go to 02B40E18: 4", 0x003BB8F1, "mov dword ptr [rip + 0x278551d], 4")
pin("S1 ... and 7 for -5", 0x003BB8C8, "mov dword ptr [rip + 0x2785546], 7")
wc = sorted((f, a, ins(a).split(", ")[-1]) for f, a, k in refs(0x02B40E1C) if k == "W")
check("S2 the command word has ten stores, one per issuer: 5 7 9 3 4 1 6 8 2 2",
      [v for _, _, v in wc] == ["5", "7", "9", "3", "4", "1", "6", "8", "2", "2"] and len({f for f, _, _ in wc}) == 10, str([("%08X" % f, v) for f, _, v in wc]))
check("S2 ... none stores 0, so command 0 (003BAC90) is the word's initial zero", "0" not in [v for _, _, v in wc])
pin("S3 003BA5F0 step 0 -> 1", 0x003BA662, "mov dword ptr [rip + 0x27867a8], 1")
pin("S3 step 1: 00862130(port 02B40E20, name 02B40E3E)", 0x003BA64C, "call 0x862130")
pin("S3 ... then step 12", 0x003BA651, "mov dword ptr [rip + 0x27867b9], 0xc")
pin("S3 step 12: a result of 0 or -4 ends cleanly", 0x003BA60B, "test eax, 0xfffffffb")
pin("S3 ... anything else is result class 9", 0x003BA614, "mov dword ptr [rip + 0x27867fa], 9")
pin("S3 00862130 opens the path for reading", 0x0086219C, "call qword ptr [rip + 0x60c5e]")
pin("S3 ... in mode 'rb'", 0x00862182, "lea r8, [rip + 0x9ee87]")
check("S3 ... (00901010 holds L\"rb\")", T.R.at(0x00901010, 6) == "rb".encode("utf-16le") + b"\0\0")
pin("S3 ... closes it", 0x008621AB, "call qword ptr [rip + 0x60d4f]")
pin("S3 ... and removes the file", 0x008621B6, "call qword ptr [rip + 0x6094c]")
ms = page("19-Save-Load-Settings/how-a-manual-save-is-committed.md")
check("S3 the manual-save page names the imports _wfopen_s, fclose, _wremove and command 7 'delete the file if it exists'",
      "`008C2E00` `_wfopen_s`, `008C2F00` `fclose`" in ms and "`008C2B08` `_wremove`" in ms and "storage command 7: **delete the file if it exists**" in ms)
pin("S3 command 7's issuer 003BB2F0 is reached from the queue's arm for packet kind 0xB", 0x005821F8, "call 0x3bb2f0")
pin("S4 003BA720 runs only at step 0", 0x003BA724, "cmp dword ptr [rip + 0x27866e9], 0")
pin("S4 ... asks 003BA3E0 for the block count of the name at 02B40E28", 0x003BA73C, "call 0x3ba3e0")
pin("S4 ... compares it with the free-block word 02B4054C", 0x003BA74B, "mov eax, dword ptr [rip + 0x2785dfb]")
pin("S4 ... fits: subtract", 0x003BA75E, "mov dword ptr [rip + 0x2785de8], eax")
pin("S4 ... and mark the slot 1", 0x003BA778, "mov dword ptr [rcx + rax*8 + 0x284], 1")
pin("S4 ... does not fit: mark it 0", 0x003BA7A3, "mov dword ptr [rcx + rax*8 + 0x284], edx")
check("S4 02B40540 + 0x284 + 8 x slot is the high dword of the slot record 02B407C0[slot]", 0x02B40540 + 0x284 == 0x02B407C0 + 4)
pin("S4 003BA3E0 rounds sizes up to 1 KiB blocks", 0x003BA57A, "add ecx, 0x3ff")
pin("S4 ... (shift 10)", 0x003BA580, "shr ecx, 0xa")
pin("S4 command 8's issuer 003BB6A0 takes slots 0..0xC7", 0x003BB6A4, "cmp ecx, 0xc7")
pin("S4 ... stores the slot record", 0x003BB6C3, "mov qword ptr [r10 + r9*8], rax")
pin("S4 ... runs 003BA720 at once", 0x003BB70F, "call 0x3ba720")
check("S4 003BB6A0's one caller is the queue's arm for packet kind 6", callers(0x003BB6A0) == [(0x00582040, 0x0058213F)])
qa = [0x120000 + u32(0x120000 + 0x46220C + 4 * k) for k in range(13)]
check("S4 ... (jump table: kind 6 -> 0058211E, kind 0xB -> 005821F1)", qa[6] == 0x0058211E and qa[11] == 0x005821F1, " ".join("%08X" % x for x in qa))
pin("S4 kind-6 packets are queued by 0057F280", 0x0057F30B, "mov dword ptr [rsp + 0x20], 6")
pin("S4 ... a scan over slots 0..199", 0x0057F2C7, "cmp ebx, 0xc8")
pin("S4 ... naming each slot's data file 005837F0(1, slot)", 0x0057F2F5, "call 0x5837f0")
check("S4 control: the manual-save page reads 005837F0's kind 1 as the slot's data file", "kind 1 → the base prefix plus the" in ms and "**the slot's data file**" in ms)

# ============================================================ P9 cancelling a raw-path request
pin("C1 the cancel matches the slot's id (+0x64)", 0x0032E5B4, "cmp dword ptr [rbx + 0x64], ecx")
pin("C1 ... frees a kind-0xFF path before it reads the state", 0x0032E5CB, "call 0x3697f0")
pin("C1 ... state 4 returns", 0x0032E5DE, "je 0x32e5f9")
pin("C1 the raw-path builder 0032E7C0 is the kind-0xFF producer with a heap copy", 0x0032E848, "mov ecx, 0xff")
pin("C1 ... it copies the path into 0036A190's block", 0x0032E80E, "call 0x36a190")
pin("C1 ... and returns 0032E870's id", 0x0032E84D, "call 0x32e870")
T.R.md.detail = True
RAX = {X.X86_REG_RAX, X.X86_REG_EAX, X.X86_REG_AX, X.X86_REG_AL, X.X86_REG_AH}


def rax_uses(f, site):
    Bm_ = {i.address: i for i in body(f)}
    ad = sorted(Bm_)
    nx = {a: ad[k + 1] for k, a in enumerate(ad[:-1])}
    out, seen, work = [], set(), [nx[site]]
    while work:
        a = work.pop()
        if a in seen or a not in Bm_:
            continue
        seen.add(a)
        i = Bm_[a]
        rr, ww = i.regs_access()
        same = i.mnemonic in ("xor", "sub") and len(i.operands) == 2 and i.op_str.split(", ")[0] == i.op_str.split(", ")[1]
        if set(rr) & RAX and not same:
            out.append((a, "%s %s" % (i.mnemonic, i.op_str)))
            continue
        if i.mnemonic == "call" or same or set(ww) & {X.X86_REG_RAX, X.X86_REG_EAX}:
            continue
        if i.mnemonic.startswith("ret"):
            out.append((a, "ret"))
            continue
        if i.mnemonic == "jmp":
            if i.op_str.startswith("0x") and f <= int(i.op_str, 16) < f + SZ[f]:
                work.append(int(i.op_str, 16))
            else:
                out.append((a, "jmp " + i.op_str))
            continue
        if i.mnemonic.startswith("j"):
            work.append(int(i.op_str, 16))
        if a in nx:
            work.append(nx[a])
    return out


rp = callers(0x0032E7B0)
check("C2 the raw-path entry 0032E7B0 (jmp 0032E7C0) has sixteen call sites in 003306E0, 003319D0 and 00377DC0",
      len(rp) == 16 and {f for f, _ in rp} == {0x003306E0, 0x003319D0, 0x00377DC0}, str(len(rp)))
used = {"%08X" % s: rax_uses(f, s) for f, s in rp}
check("C2 every one of them discards the returned id (no read of rax before it is overwritten, on every path)",
      all(not v for v in used.values()), str({k: v for k, v in used.items() if v}))
check("C2 control: the same flow finds 0032E620's use of 0032E870's id ('mov r8d, eax')", rax_uses(0x0032E620, 0x0032E6DD) == [(0x0032E6E2, "mov r8d, eax")])
check("C2 control: and 0032E7C0 returning it", [w_ for _, w_ in rax_uses(0x0032E7C0, 0x0032E84D)] == ["ret"])
rid = sorted({f for f, a, k in refs(0x01EED498)})
check("C3 the id counter 01EED498 is touched only by the slot reset 0032E450 and the builder 0032E870", rid == [0x0032E450, 0x0032E870], str(rid))
st = sorted({f for g in range(0x022C31C0, 0x022C51C0, 0x40) for f, a, k in refs(g)})
check("C3 the slot table 022C31C0 is referenced only inside the slot module 0032E000..0032ED00", st and all(0x0032E000 <= f < 0x0032ED00 for f in st), " ".join("%08X" % f for f in st))
for s in (0x002FC426, 0x003B13AF, 0x003B17BD, 0x003B199D):
    prev = list(T.R.md.disasm(T.R.at(s - 3, 3), s - 3))
    check("C4 the cancel at %08X passes its own object's +0x18" % s, prev and "+ 0x18]" in prev[0].op_str, prev[0].op_str if prev else "")
check("C4 the cancel's direct callers are exactly those four", sorted(f for f, _ in callers(0x0032E590)) == [0x002FC3C0, 0x003B1310, 0x003B1710, 0x003B18E0])
pin("C5 control: 0032E620 stores the caller's file id (edx) where a kind-0xFF request keeps its path (+0x24)", 0x0032E902, "mov dword ptr [r10 + 0x24], ebp")

# ============================================================ boundaries named on the pages
rr = page("16-UI/Request-Router/ui-request-router.md")
check("Z1 the router page carries the sentence the zero operand word is posted as 0 (struck by this batch)", "posted as-is when non-zero and as `0` when it is zero" in rr)
qq = page("02-Resource-And-Asset-Pipeline/the-resource-request-queue.md")
check("Z2 the queue page carries the sentence the result is dispatched over substates 0 ... 9 (struck by this batch)", "dispatched over substates 0 … 9 to" in qq)

print("PASSES", PASSES)
print("FAILS", FAILS)
