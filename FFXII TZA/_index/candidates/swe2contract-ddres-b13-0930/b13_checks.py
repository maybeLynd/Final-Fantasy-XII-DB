"""DD residue batch 13 (SWE2-CONTRACT for OPUS, 2026-09-30): the checks behind the residue answered on three pages.

Run: python -B b13_checks.py   (last line FAILS n; must be FAILS 0)
Inputs: the certified image through retool.py (sha 73461d08...); the US text files of the game extract
(D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile) with the US file-size table of a test client,
resolved by the method of _index/candidates/gi-0929-dialogs/gi13_saveload_states.py (002F9860: id / 1000 -> group,
01E09F68 -> loader id, FileSizeTable size -> the st2e file); the shipped myoshiok/us/worldmap/menumap_world.bin and
test_battle/us/binaryfile/menu_mapname.bin, read the way Tools/work/DATA/menumap/decode_menumap.py reads them; the
register _index/OPEN-QUESTIONS.md and the SECTION-02 review, for the boundary checks.

Page 1  16-UI/Request-Router/ui-request-router.md
  R1  who clears the request word: 00252D90 zeroes 02092730 and 02092734 after the stop-registry cancel (00225CD0)
      or, for id 11 without a handle, 002260A0; 16 call sites; the reset 00252DE0 (one caller, the area unload
      002628B0) zeroes both too. Control: 02092734's writers image-wide are exactly these two and the setter 00252B46
  R2  request 24's widget 0035D6B0 (shared with request 3 through 0035D080): message 1 posts the word and, for 24,
      sets capability row 8 bits 0 and 20; message 2 counts +0xC0 down from 24 and then opens the caption once;
      message 12 with 0x8100 closes it; message 18 for 24 clears the word, clears the two bits and posts request 2
      with parameter 0 to the mailbox; for 3 it runs 0035BC50 and the party-focus refresh instead
  R3  the caption 0035C660: text 0x86E for request 3 and 0x86F otherwise, through 00241C90; the texts resolved.
      Control: 0x87E and 0x82E reproduce the strings their own records give
  R4  request 11's widget family 003EF750..003EFCC0 asks for no text id (no 002F9860 call, no text-id immediate).
      Control: the same scan finds 002F9860 calls in the spattack window's family
  R5  world-map kind 7: every writer of the kind and every reader that branches on it; kind 7 is compared only at
      002817B3, where closing the map (code 0x418) ends the fullscreen request like kinds 2 and 3 instead of
      returning to the field menu like kind 1
  R6  the airship nodes: nodes 1, 3, 12, 20, 34 of menumap_world.bin are Rabanastre, Nalbina Fortress, Archades,
      Bhujerba and Balfonheim Port, and routes 1-14 are the seven legs between them
  R7  request 2's parameter: 0 goes to 00280D20, non-zero to 0027F540; there 1..0x20 open the airship-route page,
      0x42 the map tutorial and anything else (0x21 included) the location map 0028E660(1)
  R8  the reader of +0x10F60 / +0x10F68 bit 0x10: 00290CF0 (update-gate group 0x2000) builds the 0x61F0-byte
      battle menu through 00276650 when no request word is up
  R9  +0x598 of the save/load controller: the slot selector's 0058052A is the only byte store in the save/load
      band, the controller only compares it, and the factory zeroes every widget at construction
  R10 bit 12 of the battle-system flag dword [02EBF190]+4 (the image-B selector): its three writer functions
  R11 the text stepper 002ABF70 has one call site, in the drawer slot 002A8C50
  R12 the spattack window's text ids are control-code templates, not a title
Page 2  16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md
  N1  +0xA6 is the glyph sheet's font-variant slot, 1..7 of 02AEE810 (0 when not registered); 7 installs the
      alternate sheet pointer [02AEE808] and sets +0x44 bit 11
  N2  +0xB8 is the glyph run's pixel-test word: drawers pass it to the run begin 0017FA10, and two emitters write it
      as the data of command code 0x47
  N3  the general glyph loop 002A9F00 re-derives the spacing block for every character (002AC2F0 in the loop, from
      that glyph's own advance field); the number formatter does it once. Control: 002AE610's single call before its digits
  N4  002D14E0's list widget (procedure 002D2DB0) is the +0xC0 child of both 002A5590's owner and the shared dialog
      0057C480
  N5  002D89E0 hands 002B3400 its own stack block, so the kind-2 stamp is on a fresh state
  N6  the three 002B3xxx readers of +0x9E start the target +0x90 at minus the lag bound
  N7  register states the page's stale sentences predate (UQ-164, UQ-166, UQ-168, UQ-173, UQ-383, AC-9, AC-10)
Page 3  02-Resource-And-Asset-Pipeline/the-resource-request-queue.md
  Q1  the path copy's lifetime: done, error and cancel each free a kind-0xFF path once; the state-4 completion frees
      nothing; the cancel frees before it tests the state, so a second cancel of an in-flight path request frees again
  Q2  the four bounds of the status clause: EO-3, OV-19, OV-33, OV-36 states, the SECTION-02 review's sentences,
      the carrier requests; the chunk gate 003EB0D0
"""
import collections, hashlib, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TZA = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DB = os.path.abspath(os.path.join(TZA, ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

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


def rng(a, b):
    return [i for i in T.R.md.disasm(T.R.at(a, b - a), a) if i.address < b]


def u32(a):
    return struct.unpack("<I", T.R.at(a, 4))[0]


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
            cells = l.split("|")
            return cells[-2].strip()
    return None


def grep(pattern, lo=0, hi=1 << 40):
    rx = re.compile(pattern)
    out = []
    for f, n in sorted(SZ.items()):
        if not lo <= f < hi:
            continue
        d = T.R.at(f, n)
        if not d:
            continue
        for i in T.R.md.disasm(d, f):
            if rx.search("%s %s" % (i.mnemonic, i.op_str)):
                out.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str)))
    return out


# ------------------------------------------------------------------ text resolution (the gi13 method)
EXE = T.R.b.EXE
FST = os.environ.get("FF12_FST", r"D:/FFXII MP Mod/FFXII_TestClient1/FileSizeTables/FileSizeTable_US.fst")
BIN = r"D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile"
fst = open(FST, "rb").read()
SIZES = {}
for _f in os.listdir(BIN):
    SIZES.setdefault(os.path.getsize(os.path.join(BIN, _f)), []).append(_f)


def dec(s):
    o = ""
    for c in s:
        if 0x20 <= c <= 0x39:
            o += chr(65 + c - 0x20)
        elif 0x3A <= c <= 0x53:
            o += chr(97 + c - 0x3A)
        elif 0x54 <= c <= 0x5D:
            o += chr(48 + c - 0x54)
        elif c == 4:
            o += " "
        elif c == 2:
            o += " / "
        elif c == 0xA8:
            o += "."
        elif c == 0xA7:
            o += ","
        elif c == 0x9A:
            o += "?"
        elif c == 0x99:
            o += "!"
        else:
            o += "{%02X}" % c
    return o


def text(tid):
    g, row = divmod(tid, 1000)
    lid = struct.unpack("<b", T.R.at(0x01E09F68 + g, 1))[0]
    size = struct.unpack_from("<i", fst, 4 * (2 * 5000 + lid))[0]
    out = []
    for f in SIZES.get(size, []):
        t = open(os.path.join(BIN, f), "rb").read()
        tab = struct.unpack_from("<I", t, 0x14)[0]
        cnt = struct.unpack_from("<I", t, tab + 12)[0]
        if row < cnt:
            o = struct.unpack_from("<I", t, tab + 16 + 4 * row)[0]
            st = tab + 12 + o
            out.append((f, dec(t[st:t.index(b"\0", st)])))
    return out


def text1(tid):
    t = text(tid)
    return t[0] if len(t) == 1 else (None, repr(t))


# ============================================================ page 1: the request router
# R1 who clears the request word
pin("R1 00252D90 reads the word", 0x00252D96, "mov ebx, dword ptr [rip + 0x1e3f994]")
pin("R1 00252D90 asks the stop-registry handle", 0x00252DA4, "call 0x255290")
pin("R1 00252D90 cancels the handle through 00225CD0", 0x00252DBE, "call 0x225cd0")
pin("R1 00252D90: without a handle, id 11 goes to 002260A0", 0x00252DAD, "cmp ebx, 0xb")
pin("R1 00252D90 zeroes 02092730", 0x00252DC5, "mov dword ptr [rip + 0x1e3f965], eax")
pin("R1 00252D90 zeroes 02092734", 0x00252DCB, "mov dword ptr [rip + 0x1e3f963], eax")
c = callers(0x00252D90)
sites = [s for _, s in c]
check("R1 00252D90 has 16 direct call sites", len(c) == 16, " ".join("%08X@%08X" % x for x in c))
for s, who in ((0x00280286, "the generic route's area controller 00280140 (message 18)"), (0x0035D731, "request 24's widget"),
               (0x0028E9A2, "request 12's arm 0028E970"), (0x0035DAA8, "0035DA80, of the 0035D6B0 / 0035D8D0 / 0035D980 / 0035DA80 quartet")):
    check("R1 00252D90 is called from %08X, %s" % (s, who), s in sites)
pin("R1 the reset 00252DE0 zeroes 02092730", 0x00252DFF, "mov dword ptr [rip + 0x1e3f92b], eax")
pin("R1 the reset 00252DE0 zeroes 02092734", 0x00252E05, "mov dword ptr [rip + 0x1e3f929], eax")
check("R1 00252DE0's one caller is the area unload 002628B0", callers(0x00252DE0) == [(0x002628B0, 0x00262DCE)], str(callers(0x00252DE0)))
w = sorted(ad for f, ad, k in refs(0x02092734) if k == "W")
check("R1 control: 02092734's writers are exactly 00252B46 (the setter), 00252DCB and 00252E05",
      w == [0x00252B46, 0x00252DCB, 0x00252E05], " ".join("%08X" % x for x in w))
check("R1 control: the router's gate reads 02092734 at 00254B71", any(ad == 0x00254B71 for f, ad, k in refs(0x02092734)))

# R2 request 24's widget
check("R2 0035D6B0 is installed only by 0035D080 (lea at 0035D0B5)", refs(0x0035D6B0) == [(0x0035D080, 0x0035D0B5, "lea")], str(refs(0x0035D6B0)))
pin("R2 request 3's route builds the same widget when 022C83E8 bit 6 is set", 0x0035DA02, "call 0x35d080")
pin("R2 message 1 posts the word with flag 1", 0x0035D825, "call 0x252b40")
pin("R2 message 1, id 24: row 8 bit 0 set (ecx = 0x18 - 0x10)", 0x0035D83C, "lea ecx, [rax - 0x10]")
pin("R2 message 1, id 24: 002E1C20", 0x0035D83F, "call 0x2e1c20")
pin("R2 message 1, id 24: bit 0x14 = 20", 0x0035D844, "mov edx, 0x14")
pin("R2 message 1, id 24: row 8 again (ecx = 0x14 - 0xC)", 0x0035D849, "lea ecx, [rdx - 0xc]")
pin("R2 message 1 publishes the singleton 022CA428", 0x0035D869, "mov qword ptr [rip + 0x1f6cbb8], rbx")
pin("R2 message 1 sets the countdown +0xC0 = 24", 0x0035D89C, "mov dword ptr [rbx + 0xc0], 0x18")
pin("R2 message 2 decrements +0xC0", 0x0035D7DE, "mov dword ptr [rbx + 0xc0], eax")
pin("R2 message 2 at zero opens the caption once", 0x0035D803, "call 0x35c660")
pin("R2 message 2 marks +0xC4 bit 0", 0x0035D808, "or dword ptr [rbx + 0xc4], 1")
pin("R2 message 12 reacts to 0x8100", 0x0035D79C, "cmp qword ptr [rdx + 8], 0x8100")
pin("R2 message 12 closes the widget", 0x0035D7AD, "call 0x244f00")
pin("R2 message 18, id 24: clears the word", 0x0035D731, "call 0x252d90")
pin("R2 message 18, id 24: 002E1CA0 clears the row-8 bits", 0x0035D746, "call 0x2e1ca0")
pin("R2 message 18, id 24: request id 24 - 22 = 2", 0x0035D74D, "lea ecx, [rdi - 0x16]")
pin("R2 message 18, id 24: parameter 0", 0x0035D74B, "xor edx, edx")
pin("R2 message 18, id 24: posted to the mailbox", 0x0035D750, "call 0x2e1b10")
pin("R2 message 18, id 3: 0035BC50 (the selection state) is on the id-3 arm", 0x0035D771, "call 0x35bc50")
pin("R2 the id-3 arm is chosen by cmp edi, 3", 0x0035D723, "cmp edi, 3")
check("R2 002E1C20 is the row setter (or [0215F1C0 + row*4], 1 << bit)", ins(0x002E1C3C) == "or dword ptr [r8], eax" and "0x1e7d591" in ins(0x002E1C28))

# R3 the caption and its texts
pin("R3 0035C660 tests the word against 3", 0x0035C66B, "cmp dword ptr [rip + 0x1d360be], 3")
pin("R3 text 0x86E for request 3", 0x0035C672, "mov ecx, 0x86e")
pin("R3 text 0x86F otherwise", 0x0035C697, "mov ecx, 0x86f")
pin("R3 the text lookup", 0x0035C69C, "call 0x2f9860")
pin("R3 the dialog builder 00241C90", 0x0035C6D6, "call 0x241c90")
f86f = text1(0x86F)
check("R3 0x86F is menu_message.bin's 'All members of the party have fallen. Reform the / party with one or more reserve members.'",
      f86f == ("menu_message.bin", "All members of the party have fallen. Reform the / party with one or more reserve members."), str(f86f))
f86e = text1(0x86E)
check("R3 0x86E is 'Select a new party leader.'", f86e == ("menu_message.bin", "Select a new party leader."), str(f86e))
check("R3 control: 0x87E is 'Save complete.' (gi13's control)", text1(0x87E) == ("menu_message.bin", "Save complete."), str(text1(0x87E)))
check("R3 control: 0x82E is the disc text (UQ-299's control)", text1(0x82E) == ("menu_message.bin", "The FINAL FANTASY XII disc cannot be found."), str(text1(0x82E)))
check("R3 control: 0xC03 is 'Choose your destination.' (this page's own help_menu reading)", text1(0xC03) == ("help_menu.bin", "Choose your destination."), str(text1(0xC03)))

# R4 request 11's widget asks for no text
pin("R4 request 11's arm 003EF750 builds the 0x108 widget 003EF830", 0x003EF753, "lea rdx, [rip + 0xd6]")
g4 = grep(r"call 0x2f9860", 0x003EE000, 0x003F0000)
check("R4 no 002F9860 call in 003EE000..003F0000 (the game-over family)", not g4, str(g4))
imm = [x for x in grep(r", 0x([89a-f][0-9a-f]{2}|[1-9][0-9a-f]{3})$", 0x003EEE00, 0x003EFCD0) if "rsp" not in x[2] and "rbp" not in x[2] and "[r" not in x[2]]
check("R4 the only wide immediates in the family are 0x8001 and 0x7fee (no text id)", sorted(x[2] for x in imm) == ["cmp rax, 0x7fee", "mov edx, 0x8001"], str(imm))
g4c = grep(r"call 0x2f9860", 0x002D5000, 0x002D7000)
check("R4 control: the same scan finds 002F9860 calls in 002D5000..002D7000", len(g4c) >= 2, str([("%08X" % a) for _, a, _ in g4c]))

# R5 world-map kind 7
wk = sorted((f, ad, t) for f, ad, t in grep(r"0x10fa2\]"))
writers = [(f, ad) for f, ad, t in wk if t.startswith("mov byte ptr")]
check("R5 the kind byte +0x10FA2 is written at 0028E6F6 (1), 002903FC (the argument) and 002917D3 (1)",
      writers == [(0x0028E690, 0x0028E6F6), (0x002903F0, 0x002903FC), (0x00291750, 0x002917D3)], str(writers))
check("R5 002903F0's callers: 0027F5D0 (0027FA27), 002804E0, 00281ED0",
      sorted(f for f, _ in callers(0x002903F0)) == [0x0027F5D0, 0x002804E0, 0x00281ED0], str(callers(0x002903F0)))
pin("R5 request 17 passes kind 2", 0x0027F993, "mov ecx, 2")
pin("R5 request 15 passes kind 3", 0x0027FA22, "mov ecx, 3")
pin("R5 request 18 passes kind 7", 0x0027F9A2, "mov ecx, 7")
pin("R5 002804E0 passes kind 6", 0x00280558, "mov ecx, 6")
pin("R5 00281ED0 passes edi", 0x002823B1, "mov ecx, edi")
pin("R5 ... which is 1 (lea edi, [rbp + 1], rbp = 0)", 0x00282352, "lea edi, [rbp + 1]")
reads = [(f, ad, t) for f, ad, t in wk if not t.startswith("mov byte ptr")]
check("R5 its readers: 0028E704 (installer), 0028E7AF (cmp 3, keeps the route word), 0028E7C8, 0028F862 (the getter)",
      [ad for _, ad, _ in reads] == [0x0028E704, 0x0028E7AF, 0x0028E7C8, 0x0028F862], str(reads))
check("R5 the getter 0028F850 has one caller, 002814E0 (0028179B)", callers(0x0028F850) == [(0x002814E0, 0x0028179B)], str(callers(0x0028F850)))
pin("R5 002814E0's kind arm: 2 and 3 close the fullscreen request", 0x002817A8, "jle 0x28153c")
pin("R5 002814E0's kind arm: 6 apart", 0x002817AE, "cmp eax, 6")
pin("R5 002814E0's kind arm: 7 closes the fullscreen request too", 0x002817B3, "cmp eax, 7")
pin("R5 ... jump to 0028153C", 0x002817B6, "je 0x28153c")
pin("R5 other kinds reinstall the field menu's world map 0028E690", 0x002817CA, "call 0x28e690")
pin("R5 0028153C closes context +0x100 (00244F00)", 0x00281558, "jmp 0x244f00")
idx = T.R.at(0x120000 + 0x161914, 0xEE)
arm = 0x120000 + u32(0x120000 + 0x1618F0 + 4 * idx[0x418 - 0x418])
check("R5 close code 0x418 dispatches to the kind arm 0028179B", arm == 0x0028179B, "%08X" % arm)
pin("R5 the world-map host's close passes 0x418", 0x00552230, "mov ecx, 0x418")
check("R5 00552230 is the host's (lea in 00552250)", refs(0x00552230) == [(0x00552250, 0x0055229B, "lea")], str(refs(0x00552230)))
hk = [(ad, t) for f, ad, t in grep(r"0x172\]", 0x00550000, 0x00554000)]
hcmp = [(ad, t) for ad, t in hk if t.startswith("cmp")]
check("R5 in the host band 00550000..00554000 the kind word +0x172 is compared only with 6 (00552386)",
      hcmp == [(0x00552386, "cmp word ptr [rbx + 0x172], 6")], str(hcmp))
pin("R5 the host's title switch: kind 2 -> 0xC03", 0x00552421, "mov ecx, 0xc03")
pin("R5 the host's title switch: kind 3 -> 0xC04", 0x0055241A, "mov ecx, 0xc04")
pin("R5 the host's title switch: kind 5 -> 0xBFA", 0x00552413, "mov ecx, 0xbfa")
ck = [(ad, t) for f, ad, t in grep(r"0xca\]", 0x003B0000, 0x003D0000) if t.startswith(("cmp", "movzx"))]
cks = sorted(t.split(", ")[-1] for ad, t in ck if t.startswith("cmp"))
check("R5 the map widget's kind +0xCA is compared only with 0 (2 sites) and 6 (4 sites)", cks == ["0", "0", "6", "6", "6", "6"], str(ck))
sw = [i for i in rng(0x003C0955, 0x003C0975)]
subs = [i.op_str for i in sw if i.mnemonic in ("sub", "cmp")]
check("R5 the node predicate's switch on +0xCA picks 0, 2, 3, 4 and 6 (sub 2 / sub 1 / sub 1 / cmp 2) and nothing for 1, 5 or 7",
      subs == ["edx, 2", "edx, 1", "edx, 1", "edx, 2"], str(subs))
k7 = [x for x in grep(r"cmp .*(0x172|0xca|0x10fa2)\], 7$")]
check("R5 nothing compares +0x172, +0xCA or +0x10FA2 with 7", not k7, str(k7))
k7c = grep(r"^cmp eax, 7$", 0x002814E0, 0x002814E1)
check("R5 control: the getter-result compare at 002817B3 is found by the same instruction scan", any(ad == 0x002817B3 for _, ad, _ in k7c), str(k7c))

# R6 the airship nodes and legs
MW = r"D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok/us/worldmap/menumap_world.bin"
MN = r"D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile/menu_mapname.bin"
w = open(MW, "rb").read()
mn = open(MN, "rb").read()
U32 = lambda b, o: struct.unpack("<I", b[o:o + 4])[0]
cnt = U32(mn, 4)
ids = [U32(mn, 0x20 + i * 4) for i in range(cnt)]
hb = U32(mn, 0x14)
base = U32(mn, hb + 4)
n2 = U32(mn, hb + 12)
offs = [U32(mn, hb + 16 + i * 4) for i in range(n2 + 1)]
sys.path.insert(0, os.path.join(DB, "Tools", "work", "repos-2d"))
from ff12text import dec as tdec  # noqa: E402


def mname(x):
    i = ids.index(x)
    return tdec(mn[hb + base + offs[i]:hb + base + offs[i + 1]])


ao = struct.unpack_from("<H", w, 0xA)[0]
nn = U32(w, ao)
check("R6 menumap_world.bin: 'wmap', 39 node records of 0x1C at word[+0xA]", w[:4] == b"wmap" and nn == 39, "%r %d" % (w[:4], nn))
want = {1: "Rabanastre", 3: "Nalbina Fortress", 12: "Archades", 20: "Bhujerba", 34: "Balfonheim Port"}
for n, nm in want.items():
    v = U32(w, ao + 4 + n * 28 + 16)
    got = mname(v) if v in ids else None
    check("R6 node %d's name id %d is %r" % (n, v, nm), got == nm, repr(got))
check("R6 control: node 1's id 60100 is 'Rabanastre', as decode_menumap.out.txt records", U32(w, ao + 4 + 28 + 16) == 60100)
check("R6 control: node 22 (the route-15 self-link) is 'Ogir-Yensa Sandsea'", mname(U32(w, ao + 4 + 22 * 28 + 16)) == "Ogir-Yensa Sandsea")
qo = struct.unpack_from("<H", w, 0xC)[0]
nq = U32(w, qo)
legs = {}
for i in range(nq):
    o = qo + 4 + i * 8
    a, b, ty = w[o], w[o + 1], struct.unpack_from("<H", w, o + 2)[0]
    if ty:
        legs[ty] = (a, b)
check("R6 the link table has 60 entries and routes 1..15", nq == 60 and sorted(legs) == list(range(1, 16)), str(sorted(legs)))
exp = {1: (1, 12), 2: (12, 1), 3: (1, 3), 4: (3, 1), 5: (1, 20), 6: (20, 1), 7: (3, 12), 8: (12, 3), 9: (3, 34), 10: (34, 3),
       11: (20, 34), 12: (34, 20), 13: (12, 34), 14: (34, 12), 15: (22, 22)}
check("R6 routes 1..14 are the seven legs, each once per direction (route 15 the self-link at node 22)", legs == exp, str(legs))

# R7 request 2's parameter
tbl = [0x120000 + u32(0x00280048 + 4 * i) for i in range(18)]
check("R7 the close table 00280048: id 2 -> 0027FC9C; 6, 15, 17, 18, 19 -> 0027FD0A",
      tbl[0] == 0x0027FC9C and all(tbl[i - 2] == 0x0027FD0A for i in (6, 15, 17, 18, 19)), " ".join("%08X" % x for x in tbl))
pin("R7 id 2: parameter tested", 0x0027FCA2, "test edx, edx")
pin("R7 id 2: non-zero parameter goes on to 0027FD10", 0x0027FCA4, "jne 0x27fd10")
pin("R7 id 2: parameter 0 opens the 0x288 menu widget 00280D20", 0x0027FCAE, "call 0x280d20")
pin("R7 non-zero: the fullscreen procedure's opener 0027F540", 0x0027FD17, "call 0x27f540")
pin("R7 00280D20 builds a 0x288-byte widget with procedure 00280DE0", 0x00280D59, "lea rdx, [rip + 0x80]")


def arm22(p):
    """0027F9C1..0027F9F1: the fullscreen procedure's shared 2 / 22 arm, emulated on its own instructions."""
    ecx = p & 0xFFFFFFFF
    if ((ecx - 1) & 0xFFFFFFFF) <= 0x1F:
        ecx = 1
    ecx = (ecx - 1) & 0xFFFFFFFF
    if ecx == 0:
        return "airship"
    ecx = (ecx - 0x1F) & 0xFFFFFFFF
    if ecx == 0:
        return "airship"
    if ecx == 0x22:
        return "tutorial"
    return "location map"


seq = [i.mnemonic + " " + i.op_str for i in rng(0x0027F9C1, 0x0027F9F3)]
check("R7 the arm's instructions are the ones the emulation follows",
      seq == ["mov ecx, dword ptr [rbx + 0xd4]", "mov edi, 1", "lea eax, [rcx - 1]", "cmp eax, 0x1f", "cmovbe ecx, edi",
              "sub ecx, edi", "je 0x27fa11", "sub ecx, 0x1f", "je 0x27fa11", "cmp ecx, 0x22", "je 0x27f9f3", "xor ecx, ecx",
              "call 0x27ef00", "mov ecx, edi", "call 0x28e660", "jmp 0x27fa31"], str(seq))
res = {p: arm22(p) for p in (0, 1, 0x14, 0x20, 0x21, 0x40, 0x41, 0x42, 0x7FFF)}
check("R7 1..0x20 -> airship page; 0x42 -> tutorial; 0, 0x21, 0x40, 0x41 and others -> location map",
      res == {0: "location map", 1: "airship", 0x14: "airship", 0x20: "airship", 0x21: "location map", 0x40: "location map",
              0x41: "location map", 0x42: "tutorial", 0x7FFF: "location map"}, str(res))
pin("R7 the airship target 0027FA11 stores the word (002901B0) and kind 3", 0x0027FA1D, "call 0x2901b0")
pin("R7 the tutorial target 0027F9F3 calls 002B9FD0", 0x0027F9F3, "call 0x2b9fd0")
pin("R7 control: 0028E660 opens the location map, 002B9D30(x, 5) (the map-screens page)", 0x0028E664, "mov edx, 5")

# R8 the reader of +0x10F60 / bit 0x10
pin("R8 00290CF0 tests +0x10F68 bit 0x10", 0x00290D37, "test al, 0x10")
pin("R8 ... only while no request word is up", 0x00290D3F, "cmp dword ptr [rip + 0x1e019ea], 0")
pin("R8 ... reads the stored id +0x10F60", 0x00290D8F, "movzx eax, word ptr [rbx + 0x10f60]")
pin("R8 ... calls 00276650", 0x00290DC0, "call 0x276650")
pin("R8 00276650 builds a 0x61F0-byte widget", 0x002766D8, "mov edx, 0x61f0")
pin("R8 ... with procedure 00279E20", 0x002766D1, "lea r8, [rip + 0x3748]")
check("R8 00290CF0's one caller is the update gate 0028E290", callers(0x00290CF0) == [(0x0028E290, 0x0028E480)], str(callers(0x00290CF0)))
pin("R8 control: 0028FD50 writes +0x10F60 (the page's request 1 / 4 action)", 0x0028FD65, "mov word ptr [rax + 0x10f60], cx")

# R9 +0x598
st598 = [(f, ad, t) for f, ad, t in grep(r"^mov byte ptr \[r[a-z0-9]+ \+ 0x598\]")]
check("R9 byte stores at +0x598 image-wide: 0056BADA, 0056C01F (the gambit-screen bodies 0056B4D0 / 0056BE40) and 0058052A",
      [ad for _, ad, _ in st598] == [0x0056BADA, 0x0056C01F, 0x0058052A], str(st598))
check("R9 0058052A is in the slot selector 0057FE80", st598[-1][0] == 0x0057FE80 if st598 else False)
acc = [(ad, t) for f, ad, t in grep(r"0x598\]", 0x00582860, 0x00582861)]
check("R9 the controller 00582860 only compares +0x598 (00582E8A)", acc == [(0x00582E8A, "cmp byte ptr [rbx + 0x598], 0")], str(acc))
pin("R9 the widget factory's initialiser zeroes the object (memset)", 0x00246626, "call 0x861ec0")

# R10 bit 12 of [02EBF190]+4
b12 = [(f, ad) for f, ad, t in grep(r"^(or|and) dword ptr \[r[a-z0-9]+ \+ 4\], (0x1000|0xffffefff)$")]
check("R10 bit 12 of a +4 dword is set or cleared only in 00233C10, 00239960 and 0023A390",
      sorted(set(f for f, _ in b12)) == [0x00233C10, 0x00239960, 0x0023A390], str(b12))
check("R10 0023A390's callers: the verb handler 0050F500 and the load normaliser 00584210",
      sorted(f for f, _ in callers(0x0023A390)) == [0x0050F500, 0x00584210], str(callers(0x0023A390)))
pin("R10 0050F500 pops an int and tail-jumps 0023A390", 0x0050F512, "jmp 0x23a390")
pin("R10 control: the getter 00236760 reads bit 12", 0x0023676A, "shr eax, 0xc")
vt = os.path.join(TZA, "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
row = [l for l in open(vt, encoding="utf-8") if "\t0050F500\t" in l]
check("R10 the verb table binds 0050F500 to verb 0x308D, unnamed", len(row) == 1 and row[0].startswith("308D\t") and "DERIVED-UNNAMED" in row[0], row[0][:80] if row else "")

# R11 the stepper's call sites
check("R11 002ABF70 has one call site, 002A9945 in 002A8C50", callers(0x002ABF70) == [(0x002A8C50, 0x002A9945)], str(callers(0x002ABF70)))
check("R11 002A8C50 has no direct caller (a drawer slot)", callers(0x002A8C50) == [])
check("R11 control: 009164C8 holds 002A8C50 (the drawer table, slot 1 of kind 0)", struct.unpack("<Q", T.R.at(0x009164C8, 8))[0] == 0x002A8C50)

# R12 the spattack window
pin("R12 0028E970's builder 002D5030 makes the 0x760 widget with procedure 002D5EB0", 0x002D5039, "lea rdx, [rip + 0xe70]")
check("R12 002D5170 (called by 002D5EB0) is the window's only text lookup", sorted(set(f for f, _ in callers(0x002D5170))) == [0x002D5EB0])
for a, tid in ((0x002D519B, 0x4669), (0x002D51A3, 0x466A), (0x002D51AB, 0x466C)):
    pin("R12 002D5170 selects text %#x" % tid, a, hex(tid))
pin("R12 002D5170's other text is 0x46B4", 0x002D5200, "mov ecx, 0x46b4")
for tid in (0x4669, 0x466A, 0x466C, 0x46B4):
    f_, s_ = text1(tid)
    check("R12 %#x is a control-code template in menu_command_template.bin (starts with {0F})" % tid,
          f_ == "menu_command_template.bin" and s_.startswith("{0F}"), "%s %s" % (f_, s_))

# R13 no native producer of 15, 18 or 19
check("R13 the translator 002E0DA0 has one caller, 002E1A60", callers(0x002E0DA0) == [(0x002E1A60, 0x002E1A6F)], str(callers(0x002E0DA0)))
check("R13 002E1A60's callers are 003462D0 and 003470D0", sorted(f for f, _ in callers(0x002E1A60)) == [0x003462D0, 0x003470D0], str(callers(0x002E1A60)))
vrows = {l.split("\t")[0]: l.split("\t")[3] for l in open(vt, encoding="utf-8") if l.split("\t")[0] in ("0472", "048D")}
vh = {l.split("\t")[0]: l.split("\t")[10] for l in open(vt, encoding="utf-8") if l.split("\t")[0] in ("0472", "048D")}
check("R13 ... the begin handlers of verbs 0x472 and 0x48D, both openfullscreenmenu",
      vh == {"0472": "003470D0", "048D": "003462D0"} and all(v.startswith("openfullscreenmenu") for v in vrows.values()), "%s %s" % (vh, vrows))
mbw = sorted(ad for f, ad, k in refs(0x0215F1A4) if k == "W")
check("R13 control: the request word 0215F1A4 has the five writers the page lists (two resets, 002E1A60, 002E1AE0, the mailbox)",
      len(mbw) == 5, " ".join("%08X" % x for x in mbw))

# R14 answers cited on other pages are present there
DOCS = [("10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md", "It returns the heavy-node count (`r12d`), or `-1`"),
        ("16-UI/CONTRACT-text-control-codes-and-dyngeo-draw.md", "to the constant control code `0F 23` (`&0x230F` at `00916548`) by `002ABB20`"),
        ("02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/himg-handbook-image-bundles.md", "the generic batch-commit this page already"),
        ("16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md", "`00394400` is called only from the message-18 arm"),
        ("11-Party/the-setsavedata-presets-test-battle-scenarios.md", "`002CFD10` (28 B) calls `002527B0(6, 4, 0)` then tail-jumps `0028E880`")]
for pth, s in DOCS:
    check("R14 %s carries %r" % (pth.split("/")[-1], s[:50]), s in open(os.path.join(TZA, pth), encoding="utf-8").read())
check("R14 control: L-13 reads SUPERSEDED in the register", (row_status("L-13") or "").lstrip("*").startswith("SUPERSEDED"))

# ============================================================ page 2: numeric formatting
pin("N1 002B3400 stores 0039BAD0's return at +0xA6", 0x002B3425, "mov byte ptr [rdi + 0xa6], al")
pin("N1 0039BAD0 scans the table 02AEE810", 0x0039BADD, "lea r8, [rip + 0x2752d2c]")
pin("N1 ... from slot 1", 0x0039BAD8, "mov eax, 1")
pin("N1 ... comparing each entry with the argument", 0x0039BAE7, "cmp dword ptr [r8 + rcx*8], edx")
pin("N1 ... up to slot 7", 0x0039BAEF, "cmp eax, 8")
pin("N1 ... and returns 0 when no slot matches", 0x0039BAF4, "xor al, al")
pin("N1 002B3400: kind 7 only when 00254A10() is 0", 0x002B3432, "jne 0x2b3456")
pin("N1 002B3400: the compare with 7", 0x002B3434, "cmp byte ptr [rdi + 0xa6], 7")
pin("N1 002B3400: 7 sets +0x44 bit 11", 0x002B343D, "or dword ptr [rdi + 0x44], 0x800")
pin("N1 002B3400: and stores 0039C4A0(1) at +0x60", 0x002B3452, "mov qword ptr [rdi + 0x60], rax")
pin("N1 0039C4A0(1) returns [02AEE808] when it is bound", 0x0039C4A4, "mov rax, qword ptr [rip + 0x275235d]")
pin("N1 control: 0039C4A0(0) returns [02AEE800]", 0x0039C4B0, "mov rax, qword ptr [rip + 0x2752349]")
pin("N1 control: the run builder 002B32D0 has the same compare", 0x002B3328, "cmp byte ptr [rdi + 0xa6], 7")
pin("N1 control: the drawer 002AC2F0 hands +0xA6 to the slot getter 0039BA30", 0x002AC429, "call 0x39ba30")

check("N1 slot 7 of 02AEE810 is the qword at 02AEE848", 0x02AEE810 + 7 * 8 == 0x02AEE848)
lb = open(os.path.join(TZA, "02-Resource-And-Asset-Pipeline", "PS2-Image-Data-Formats", "loader-bound-bin-families.md"), encoding="utf-8").read()
check("N1 the loader page names 02AEE848 fontVariant[7], a sentinel in all shipped files",
      "| 6 | `02AEE848` | `fontVariant[7]` — alternate TIM2 slot | **sentinel in all shipped files**" in lb)
check("N1 the loader page: the pointer in 02AEE808 is the one in 02AEE848 plus 0x40 (past the header)", "`02AEE808 = 02AEE848+0x40`" in lb)
pin("N2 002AF960 copies +0xB8 into the command stream", 0x002AFBDA, "mov rax, qword ptr [rbx + 0xb8]")
pin("N2 ... as the data of code 0x47", 0x002AFBE5, "mov qword ptr [rcx + 0x28], 0x47")
pin("N2 002B1D20 does the same", 0x002B1D84, "mov rax, qword ptr [r8 + 0xb8]")
pin("N2 ... code 0x47", 0x002B1D8F, "mov qword ptr [rcx + 0x18], 0x47")
pin("N2 the drawer 002A9F00 passes +0xB8 to the run begin", 0x002AA51A, "mov rcx, qword ptr [rdi + 0xb8]")
pin("N2 ... 0017FA10", 0x002AA52A, "call 0x17fa10")
for a in (0x002D860E, 0x002D877F, 0x002D88BF):
    pin("N2 the helper writes 0x3001 at %08X" % a, a, "0x3001")
pin("N2 the initialiser 002AC1E0 writes 0x30000", 0x002AC249, "mov qword ptr [rbx + 0xb8], 0x30000")
pin("N2 control: the record before it is code 6 (the texture descriptor)", 0x002AFBD2, "mov qword ptr [rcx + 0x18], 6")

pin("N3 002A9F00's loop head reads the next byte", 0x002AA053, "cmp byte ptr [rax], 0xf")
pin("N3 ... and the loop tail jumps back to it", 0x002AA74C, "jmp 0x2aa050")
pin("N3 inside the loop each character goes through 002AC2F0", 0x002AA0CD, "call 0x2ac2f0")
pin("N3 ... before the pre-glyph advance is read", 0x002AA0D2, "movss xmm0, dword ptr [rip + 0x1df2b92]")
pin("N3 ... and before the post-glyph advance is read", 0x002AA734, "movss xmm0, dword ptr [rip + 0x1df252c]")
check("N3 ... the two rip operands resolve to 0209CC6C and 0209CC68", 0x002AA0DA + 0x1DF2B92 == 0x0209CC6C and 0x002AA73C + 0x1DF252C == 0x0209CC68)
pin("N3 002AC2F0 takes the glyph's own advance field (0017F9C0 on its glyph entry's +0x1C)", 0x002AC4EF, "call 0x17f9c0")
pin("N3 ... or bits 32-36 of its 8-byte record", 0x002AC4FD, "and eax, 0x1f")
pin("N3 ... adds the spacing float +0x4C", 0x002AC507, "addss xmm0, dword ptr [rdi + 0x4c]")
pin("N3 ... stores it at 0209CC78", 0x002AC510, "movss dword ptr [rip + 0x1df0760], xmm0")
pin("N3 ... scales the 16-byte block 0209CC70 by +0x34", 0x002AC55C, "mulps xmm2, xmmword ptr [rip + 0x1df070d]")
pin("N3 ... into the spacing block 0209CC60..0209CC6F", 0x002AC56A, "movaps xmmword ptr [rip + 0x1df06ef], xmm2")
pin("N3 ... and a one-shot +0xA9 overrides 0209CC68", 0x002AC5C3, "movss dword ptr [rip + 0x1df069d], xmm0")
nf = [s for f, s in callers(0x002AC2F0) if f == 0x002AE610]
check("N3 control: the number formatter 002AE610 calls 002AC2F0 once (002AE7D7), before its digit loop", nf == [0x002AE7D7], str(nf))

pin("N4 002D14E0 builds a 0x150-byte widget", 0x002D14F4, "mov ecx, 0x150")
pin("N4 ... with procedure 002D2DB0", 0x002D14ED, "lea rdx, [rip + 0x18bc]")
for call, store in ((0x0057C73C, 0x0057C745), (0x002A5845, 0x002A5855)):
    pin("N4 %08X calls 002D14E0" % call, call, "call 0x2d14e0")
    pin("N4 ... and stores it at owner +0xC0 (%08X)" % store, store, "mov qword ptr [rsi + 0xc0], rax")
check("N4 control: 002D14E0's callers include 00241D40, 002A5590 and 0057C480",
      {0x00241D40, 0x002A5590, 0x0057C480} <= set(f for f, _ in callers(0x002D14E0)), str(callers(0x002D14E0)))

pin("N5 002D89E0 points rcx at its own stack block", 0x002D8A25, "lea rcx, [rsp + 0x40]")
pin("N5 ... branches to the 002B3400 path", 0x002D8A2C, "je 0x2d8a75")
seq5 = [i.mnemonic + " " + i.op_str for i in rng(0x002D8A75, 0x002D8A80)]
check("N5 ... where rcx is not reloaded before 002B3400", seq5 == ["mov r8, r15", "mov rdx, r14", "call 0x2b3400"], str(seq5))

for rd, st in ((0x002B33B1, 0x002B33DC), (0x002B3CE9, 0x002B3CF8), (0x002B3D84, 0x002B3DB4)):
    pin("N6 %08X reads the lag bound +0x9E" % rd, rd, "movsx")
    pin("N6 ... and stores minus it in the target +0x90 (%08X)" % st, st, "mov word ptr [r")
    seqn = [i.mnemonic for i in rng(rd, st + 1)]
    check("N6 ... negated in between (%08X..%08X)" % (rd, st), "neg" in seqn)
pin("N6 control: the stepper reads +0x9E (002AC0FE)", 0x002AC0FE, "movzx eax, byte ptr [rbx + 0x9e]")

# N7 register states
for rid, word in (("UQ-164", "CLOSED"), ("UQ-166", "ANSWERED"), ("UQ-168", "ANSWERED"), ("UQ-173", "ANSWERED 2026-09-26"),
                  ("UQ-383", "ANSWERED"), ("AC-9", "ANSWERED"), ("AC-10", "ANSWERED"), ("UQ-381", "ANSWERED")):
    s = row_status(rid)
    check("N7 register %s reads %s" % (rid, word), s is not None and word in s[:80], (s or "")[:80])
check("N7 control: an unknown id has no row", row_status("UQ-99999") is None)

# ============================================================ page 3: the resource request queue
pin("Q1 the cancel 0032E590 tests kind 0xFF", 0x0032E5B9, "cmp byte ptr [rbx + 0x21], 0xff")
pin("Q1 ... and frees the path +0x24", 0x0032E5CB, "call 0x3697f0")
pin("Q1 ... before it reads the state", 0x0032E5D0, "movzx eax, byte ptr [rbx + 0x20]")
pin("Q1 ... state 4 returns without anything else", 0x0032E5DE, "je 0x32e5f9")
pin("Q1 ... states 2 and 3 become state 4", 0x0032E603, "mov byte ptr [rbx + 0x20], 4")
pin("Q1 the done helper 0032E330 frees a kind-0xFF path", 0x0032E360, "jmp 0x3697f0")
pin("Q1 the error helper 0032E370 frees a kind-0xFF path", 0x0032E3A3, "jmp 0x3697f0")
s4 = [i.mnemonic + " " + i.op_str for i in rng(0x0032E170, 0x0032E19C)]
check("Q1 the pump's state-4 completion calls +0x48 and releases, and frees nothing",
      "call rax" in s4 and "call 0x32ec40" in s4 and not any("3697f0" in x or "0x32e330" in x or "0x32e370" in x for x in s4), str(s4))
st = [hex(0x120000 + u32(0x0032E2D0 + 4 * i)) for i in range(6)]
check("Q1 the pump's state table: 1 issue, 2 counter, 3 and 4 share 0032E163, 5 and 6 share 0032E1AB",
      st == ["0x32e0bd", "0x32e149", "0x32e163", "0x32e163", "0x32e1ab", "0x32e1ab"], str(st))
fr = sorted(set(f for f, _ in callers(0x003697F0) if 0x0032E000 <= f < 0x0032ED00))
check("Q1 in the slot code 0032E000..0032ED00 only 0032E330, 0032E370 and 0032E590 free", fr == [0x0032E330, 0x0032E370, 0x0032E590], str(fr))
p24 = [(f, ad) for f, ad, t in grep(r"0x24\]", 0x0032E000, 0x0032F000) if "rsp" not in t]
check("Q1 control: +0x24 is touched only by the issue (0032E0DB, 0032E105), the three frees and the builder's store (0032E902)",
      [ad for _, ad in p24] == [0x0032E0DB, 0x0032E105, 0x0032E357, 0x0032E39A, 0x0032E5C7, 0x0032E902], str(p24))
rp = sorted(set(f for f, _ in callers(0x0032E7B0)))
cn = sorted(set(f for f, _ in callers(0x0032E590)))
check("Q1 the raw-path users (003306E0, 003319D0, 00377DC0) are not direct callers of the cancel", rp == [0x003306E0, 0x003319D0, 0x00377DC0] and not set(rp) & set(cn),
      "%s / %s" % (rp, cn))

for rid, word in (("EO-3", "SUPERSEDED"), ("OV-19", "PARTLY ANSWERED"), ("OV-33", "PARTLY ANSWERED"), ("OV-36", "ANSWERED")):
    s = row_status(rid)
    check("Q2 register %s reads %s" % (rid, word), s is not None and s.lstrip("*").startswith(word), (s or "")[:60])
check("Q2 OV-19 keeps actual IO issuance/completion timing open as RT", "Still OPEN: actual IO issuance/completion timing (RT)" in (row_status("OV-19") or ""))
check("Q2 OV-33 keeps service issuance and loading-state timing open as RT", "Still OPEN: actual service issuance/status-production and loading-state timing (RT)" in (row_status("OV-33") or ""))
rv = open(os.path.join(TZA, "_experiments", "evidence", "continuation-section02-resource-queue", "REVIEW.md"), encoding="utf-8").read()
for s in ("Live elapsed time and actual scheduler/concurrency behavior remain unresolved by these fixtures.",
          "Path ownership, repeated cancellation safety and real allocator effects",
          "That producer/reachability\nquestion remains separate.",
          "this section does not newly\nexecute those implementations."):
    check("Q2 SECTION-02 review says %r" % s[:60], s in rv)
tj = open(os.path.join(TZA, "_index", "_inbox", "TEAM.json"), encoding="utf-8").read()
for rq in ("FABLE-REQ-ASTRA-RT-REMAINDERS-0929", "FABLE-REQ-ASTRA-EO3-PATH-POINTER"):
    check("Q2 the carrier %s is on the board" % rq, rq in tj)
check("Q2 control: an invented carrier is not", "FABLE-REQ-ASTRA-NO-SUCH-0000" not in tj)
pin("Q2 the chunk gate: 0032E620 asks 003EB0D0", 0x0032E656, "call 0x3eb0d0")
pin("Q2 ... and takes the whole-request path when no stream is active", 0x0032E665, "je 0x32e742")

print("PASSES", PASSES)
print("FAILS", FAILS)
