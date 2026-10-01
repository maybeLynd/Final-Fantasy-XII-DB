r"""DD residue batch 14 (SWE2-CONTRACT for OPUS, 2026-09-30): the checks behind the answers to batch 10's proposed rows.

Run: python -B b14_checks.py   (last line FAILS n; must be FAILS 0)
Inputs: the certified image through retool.py / structflow.py (sha 73461d08...); the installed FFXII_TZA.vbf ($FF12_VBF,
else the Steam path below) for map_ref.bin, the .efb names, every archive name and the namespace-12 .cm heads; the game
extract D:/FFXII_TZA_extract for the 1,066 .cm files (control Z1 re-decodes one from the archive).

P7  efx-and-efb-effect-containers.md - the mode-0 .efb request
  Q1  00331990 issues mode 0 (00264F40, the block's aux value 0) then mode 1 (00264F10, the row's word +0); 0050D4D0
      issues mode 1 only; these three are 00378A60's only call sites
  Q2  00378A60 hands its mode to 00377DC0 (00378B2B) and also loads the pack (00378030, 00378B41); the mode-1 arm runs
      the teardown 00378230 first (00378ACF); the mode-0 arm skips the whole load when 02ADD0E0 >= 0 equals 02ADD0DC
  Q3  00377DC0 names the file: 002DF880(4, index), the stem after the last '\' or '/' minus 4 characters, prefix
      "PS2Data\efb\", suffix ".efb"; mode 1 keeps the 0x43D170-byte block at 02ADD050 (bit 0x20, completion 003788F0),
      mode 0 at 02ADD098 (bit 0x40, completion 003789A0); both request it through 0032E7B0 with size -1
  Q4  002DF880 returns -1 without writing the buffer when the name slot is null, and 00377DC0 does not test the return
  Q5  the request: 0032E7B0 -> 0032E7C0 -> 0032E870(kind 0xFF, tail flag 1); 0032E870 stores kind +0x21, size +0x28,
      block +0x38 / +0x70, callback +0x40, +0x22 = 0; 0032E990 with the flag set appends at the tail 022C51C8
  Q6  the pump 0032E070 serves only the head 022C51C0: state 1 (kind 0xFF) -> 002DF6C0, which always returns 0 -> state 2
      -> 3; state 3 waits while 0046DFE0 reports busy (status word 0215EFF4 == -1), then state = 5 + (status < 0); with
      +0x22 == 0 state 5 calls 0032E330 (callback ok = 1) and state 6 calls 0032E370 (callback ok = 0 when +0x28 == -1)
  Q7  002DF6C0's first branch needs 0017D930 (the file-cache flag +0x88), 001D6EF0 and 001D6B40 (the path's key in the
      file cache); it opens through 001D6F20 and, when that returns null, writes no status. Its other branch is 001D6D90:
      status = -1, then a type-2 job with callback 001D6D70 and the direct-callback byte set
  Q8  001A07B0 runs a type-2 job through 001A0CF0; a failed open stores 0xFFFFFFFE as the job result; 001A09E0 answers
      only for paths ending ".cm"; the job's callback gets that result, and 001D6D70 writes it to the status word
  Q9  003789A0: on ok = 0 it frees its own block and clears bit 0x40 and 02ADD098; on ok = 1 it calls the stub 0053DD10
      (mov eax, 1 / ret) and publishes the block at 02ADD088; 02ADD088's references are exactly six
  Q10 the cache key: 001D6B40 -> 0020BE50 normalises (0020C440: skip leading non-alphanumerics, '/' -> '\', '\\' -> '\',
      toupper, trailing blanks off), hashes with 00674A00 (djb2 from 0x1505, x33, bit 31 cleared) and compares the hash
      only; the cache gains keys only through 0020B680 <- 001D6A20 <- 0059A9B0, inside the file open 0059EE90
  Q11 data: map_ref.bin's 1,315 rows against the namespace-4 name table 01E5E500 and the archive: no mode-0 .efb name
      ships; mode 1 ships for 945 fields; the two indices never name the same package; null names: 34 (mode 0), 121
      (mode 1). Control: the rows' indices equal 03-World-Area-Field/Map-Pack/members/map-ref-field-packs.tsv
  Q12 the 31-bit key of every mode-0 path collides with no archive name's key. Control: unicorn runs 00674A00 itself on
      three strings and agrees with the Python hash
  Q13 the install beside the archive holds no loose PS2Data tree, so a name the archive lacks has no file to open
P1  fef-and-motion-entries.md - the embedded EFX0010 payload
  A1  00504940 stores the entry pointer at +0x230 and hands low32(entry) + 0x30 only to 0016D6A0, which is `ret 0`
  A2  003EDAD0: six direct call sites, no rip reference, no pointer to it in data
  A3  0026FB90's pointer is the EFB walk: r14 + 0x10 over the parsed block
  A4  002FC4A0 and 003B0660 pass [01FD4A30]; its one writer is the boot hub's allocation (0022A240); files are loaded
      into it by 0032E620 from 002FC860, 003B0660 and 003B2310
  A5  003B2220 passes [entry + 0x28] of the 32 x 0x30 table 02EBE5E0; over the 21 functions that address the table the
      field is written by 003B2310 ([01FD4A30]), 003B1A80 (0), the table memset and whole-entry moves only
  A6  003B29B0's three callers pass the 0057A2D0 result: 00249210(ctx, 7, 0x31 + n) +8, a fresh block (0036A100 /
      0036A190) loaded from namespace 7; the names are the three menu .efx files; +0x11F8's writers are 00572E10's
  A7  003B38B0 (from 00409FE0) gets resource + dword[r14 + roundup64(size) - 4], the model length the file layer writes
      (001A0E1B, 001A0F4E); every @FEF model's payload at +0x30 lies below its length
  A8  the namespace-12 .cm files (the only .cm a [01FD4A30] load can name) start '@FRP', not an EFX magic, and
      003EDAD0 tests the magic first
  A9  copied-pointer census (structflow from every model-instance source: the 004780B0 / 003E55B0 / 0041E590 call sites,
      the creation in 004780C0 and the binder's callback entry): +0x230 is only written (005049A7); the two other hits
      are loop aliases (005049E0's 20-dword init from +0x194, 00504BC0's 16-dword read from +0x140). Control: the census
      finds batch 10's three +0x218 / +0x21C readers 005044D0, 00504D30, 0053AB50
P4  ftr-node-table.md - the aux-pool values
  G1  the binder hands 00409300 the record's +0xC0 and 004094D0 its +0x150 (rbx = record + 0x1B8)
  G2  00409300's rich arm: +0x3C = 1.0, bits 23-25 -> +0x30 / +0x34 / +0x38 (record +0xF0..+0xF8), bits 26-28 -> 0046D560
  G3  0046D560 is the sin / cos LUT rotation (angle / 2pi x 32768, & 0x7FFF, LUT 01F004E0, cos at index - 0x2000) writing
      rows 0-2; 0046D380 (the @FMW rotation channel) uses the same LUT and scale
  G4  004094D0: bit 21's sixteen dwords -> record +0x150..+0x18F, else 0046D110 copies the identity 01F204E0
  G5  the binder copies record +0xF0..+0xFC to +0x1B0 and +0x130 and sets the scale vec4s +0x100, +0x140, +0x1D0 to 1.0
  G6  data, all 27,561 records: every index inside the pool; angles in [-pi, pi]; every bit-21 matrix's last column is
      (0, 0, 0, 1); bit 29's index is inside the pool in 1,953 / 1,953, naming a float in [0.92, 1.38], 1.0 in 1,697
P6  ftr-node-table.md - the 0x290 consumers' fields and the +0x94 readers
  C1  0041C260: +0xC0 -> +0x120 (0046D730) and +0xF0..+0x10C -> +0x130..+0x14C
  C2  00373860: parent +0x270, cross-skeleton parent +0x276, +0x280 bit 0x10, +0x27E, +0x284; the composer arm passes
      +0xC0, +0x230, +0x100, +0x150; the bit-0x10 arm reads +0x1A0, +0xF0, +0x1C0, +0x100, +0x1E0, +0x10C
  C3  00372610: parent x local x (+0x230) -> 02AD9E40, rows scaled by the four +0x100 floats, x (+0x150) -> 02AD9E80;
      00373860 then copies 02AD9E40 to +0x80 and 02AD9E80 to the +0x284 matrix
  C4  the @FMW apply driver 00418880: writes +0xF0..+0x10C, reads the staging +0x1B0.., +0x1D0.., snapshot +0x130..,
      flags +0x28A / +0x280, chain +0x278
  C5  the palette 003703A0: +0x150 (00370738) and +0x80 (0037077C) of the remapped bone
  C6  +0x94 census (structflow from the skeleton pools [root + 0xD98] and [entry + 0x330]): written by 00372820 and
      003713C0, read by 27 functions, and every read goes to ecx for 0020E600. Control: the binder's two writes
P3  ftr-node-table.md - which bones carry attachments or markers
  B1  the bind path reads only the link, the flag word and the transform stream (R1 of batch 10 re-pinned: the binder
      tests the flag word only for 0x100)
  B2  bones are named from outside by index: 003E5AD0 (ids below 0x20 through the u16 table at +0x14C, 0x104..0x106 from
      payload +0x3A / +0x3C / +0x3E), FCP section 3's slot words (0041F010 mode 0, 0041F158), and the trail resolver
      003711D0, which refuses an index at or past the skeleton's +0x88 count
P5  ftr-node-table.md - FCP section 2
  D1  the FCP page records UQ-220 ANSWERED 2026-09-26 (FABLE): section 2 is the rig of seventeen controllers
Control
  Z1  the extract's m1132.cm equals its archive entry
"""
import collections, hashlib, math, os, struct, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")
sys.path.insert(0, KIT)
import retool as T  # noqa: E402
import structflow as S  # noqa: E402

ROOT = "D:/FFXII_TZA_extract"
VBF = os.environ.get("FF12_VBF", r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf")
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
    check(name, got == text or got.startswith(text + " ") if not text.endswith("*") else got.startswith(text[:-1]),
          "%08X  %s" % (a, got))


SZ = T.sizes()
SC = T.scan()


def body(f):
    return list(T.R.md.disasm(T.R.at(f, SZ[f]), f))


def callers(f):
    return sorted(SC["calls"].get(f, ()))


def refs(g):
    return sorted(SC["refs"].get(g, ()))


def u32(a):
    return struct.unpack("<I", T.R.at(a, 4))[0]


def f32(a):
    return struct.unpack("<f", T.R.at(a, 4))[0]


def q64(a):
    return struct.unpack("<Q", T.R.at(a, 8))[0]


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")

# ------------------------------------------------------------------ the archive
vf = open(VBF, "rb")
magic, hl, cnt, hi32 = struct.unpack("<4sIII", vf.read(16))
vf.seek(0)
H = vf.read(hl)
ent = 16 + cnt * 16
st_ = ent + cnt * 32
slen = struct.unpack_from("<I", H, st_)[0]
bl = st_ + slen
E = [struct.unpack_from("<IIQQQ", H, ent + i * 32) for i in range(cnt)]
Bk = struct.unpack_from("<%dH" % ((hl - bl) // 2), H, bl)
strs = H[st_ + 4:st_ + slen]
IDX = {strs[e[4]:strs.index(b"\0", e[4])].decode(): e for e in E}
nb = lambda s: (s >> 16) + (1 if s & 0xFFFF else 0)


def decode(e):
    out, pos = bytearray(), e[3]
    n = nb(e[2])
    for k in range(n):
        s = Bk[e[0] + k]
        last = k == n - 1
        flag = 0 if (s == 0 or (last and e[2] & 0xFFFF and s == e[2] & 0xFFFF)) else 1
        vf.seek(pos)
        dd = vf.read(s or 0x10000)
        out += zlib.decompress(dd) if flag else dd
        pos += s or 0x10000
    return bytes(out)


# ================================================================== P7: the mode-0 .efb request
print("\n== P7 (efx-and-efb-effect-containers.md)")
pin("Q1 00331990 asks MapRef_GetAuxValue0 first", 0x00331998, "call 0x264f40")
pin("Q1 ... mode 0", 0x0033199D, "xor r8d, r8d")
pin("Q1 ... 00378A60(field, aux0, 0)", 0x003319A4, "call 0x378a60")
pin("Q1 then MapRef_GetPrimaryFieldValue", 0x003319AB, "call 0x264f10")
pin("Q1 ... mode 1", 0x003319B0, "mov r8d, 1")
pin("Q1 ... 00378A60(field, word +0, 1) as a tail jump", 0x003319BF, "jmp 0x378a60")
pin("Q1 0050D4D0 (mapload) passes mode 1", 0x0050D4DC, "mov r8d, 1")
pin("Q1 ... and tail-jumps 00378A60", 0x0050D4EA, "jmp 0x378a60")
check("Q1 00378A60 has exactly these three call sites", [s for f, s in callers(0x00378A60)] == [0x003319A4, 0x003319BF, 0x0050D4EA],
      str([hex(s) for f, s in callers(0x00378A60)]))
pin("Q1 00264F40 reads the block index (row word +2) ...", 0x00264F69, "movsx rax, word ptr [rax + 2]")
pin("Q1 ... and the block's first word", 0x00264F79, "movsx eax, word ptr [rcx + rax]")
pin("Q1 00264F10 returns the row's word +0", 0x00264F39, "movzx eax, word ptr [rax]")
pin("Q2 00378A60 keeps the mode in esi", 0x00378A89, "mov esi, r8d")
pin("Q2 mode-1 arm: the teardown 00378230 before the request", 0x00378ACF, "call 0x378230")
pin("Q2 mode-0 arm: skip test reads 02ADD0E0 ...", 0x00378AD6, "mov eax, dword ptr [rip + 0x2764604]")
pin("Q2 ... skips the load when it equals 02ADD0DC", 0x00378AE6, "je 0x378b56")
pin("Q2 the .efb request with the mode in ecx", 0x00378B29, "mov ecx, esi")
pin("Q2 ... 00377DC0", 0x00378B2B, "call 0x377dc0")
pin("Q2 ... and the pack load 00378030", 0x00378B41, "call 0x378030")
pin("Q3 00377DC0: namespace 4 (r9d = 4 from the caller)", 0x00378B1A, "mov r9d, 4")
pin("Q3 ... into ecx", 0x00377DFD, "mov ecx, eax")
pin("Q3 ... the name through 002DF880", 0x00377E09, "call 0x2df880")
pin("Q3 the scan stops at '\\' ...", 0x00377E69, "cmp dl, 0x5c")
pin("Q3 ... or '/'", 0x00377E6E, "cmp dl, 0x2f")
pin("Q3 stem length = length - slash - 5 (four characters off)", 0x00377E83, "sub edi, 5")
check("Q3 the prefix at 00D11110 is 'PS2Data\\efb\\'", T.R.at(0x00D11110, 13) == b"PS2Data\\efb\\\0")
check("Q3 the suffix bytes written are '.', 'e', 'f', 'b'",
      [ins(a) for a in (0x00377ED0, 0x00377EDA, 0x00377EE4, 0x00377EEE)] ==
      ["mov byte ptr [rsp + rbx + 0x50], 0x2e", "mov byte ptr [rsp + rax + 0x50], 0x65", "mov byte ptr [rsp + rax + 0x50], 0x66",
       "mov byte ptr [rsp + rax + 0x50], 0x62"])
pin("Q3 mode 1: completion 003788F0", 0x00377F26, "lea rax, [rip + 0x9c3]")
pin("Q3 ... block 0x43D170", 0x00377F41, "mov ecx, 0x43d170")
pin("Q3 ... kept at 02ADD050", 0x00377F6F, "mov qword ptr [rip + 0x27650da], rbx")
pin("Q3 ... size -1", 0x00377F76, "or r8d, 0xffffffff")
pin("Q3 ... requested", 0x00377F82, "call 0x32e7b0")
pin("Q3 ... pending bit 0x20", 0x00377F8E, "or dword ptr [rip + 0x276515b], 0x20")
pin("Q3 mode 0: completion 003789A0", 0x00377F97, "lea rax, [rip + 0xa02]")
pin("Q3 ... block 0x43D170", 0x00377FB2, "mov ecx, 0x43d170")
pin("Q3 ... kept at 02ADD098", 0x00377FE0, "mov qword ptr [rip + 0x27650b1], rbx")
pin("Q3 ... size -1", 0x00377FE7, "or r8d, 0xffffffff")
pin("Q3 ... requested", 0x00377FF3, "call 0x32e7b0")
pin("Q3 ... pending bit 0x40", 0x00377FFF, "or dword ptr [rip + 0x27650ea], 0x40")
pin("Q4 002DF880: a null name slot ...", 0x002DF89E, "jne 0x2df8a4")
pin("Q4 ... returns -1 without a write", 0x002DF8A0, "or eax, 0xffffffff")
pin("Q4 ... (ret)", 0x002DF8A3, "ret")
pin("Q4 00377DC0 does not test the return", 0x00377E0E, "xor r15d, r15d")
pin("Q5 0032E7B0 is a jump to 0032E7C0", 0x0032E7B0, "jmp 0x32e7c0")
pin("Q5 0032E7C0: tail flag 1", 0x0032E836, "mov dword ptr [rsp + 0x28], 1")
pin("Q5 ... kind 0xFF", 0x0032E848, "mov ecx, 0xff")
pin("Q5 ... 0032E870", 0x0032E84D, "call 0x32e870")
for a, t in ((0x0032E8C9, "call 0x32e990"), (0x0032E92C, "mov dword ptr [r10 + 0x28], esi"), (0x0032E943, "mov byte ptr [r10 + 0x21], r14b"),
             (0x0032E94D, "mov qword ptr [r10 + 0x38], rdi"), (0x0032E951, "mov qword ptr [r10 + 0x40], r8"),
             (0x0032E969, "mov word ptr [r10 + 0x22], 0"), (0x0032E970, "mov qword ptr [r10 + 0x70], rdi")):
    pin("Q5 0032E870 request field", a, t)
pin("Q5 0032E990: flag set -> the tail arm", 0x0032E9E9, "jne 0x32ea1a")
pin("Q5 ... the new tail 022C51C8", 0x0032EA21, "mov qword ptr [rip + 0x1f967a0], rdx")
pin("Q6 the pump serves the head 022C51C0", 0x0032E090, "mov rbx, qword ptr [rip + 0x1f97129]")
jt = [0x120000 + u32(0x0032E2D0 + 4 * k) for k in range(6)]
check("Q6 the state table: 1 -> 0032E0BD, 2 -> 0032E149, 3 and 4 -> 0032E163, 5 and 6 -> 0032E1AB",
      jt == [0x0032E0BD, 0x0032E149, 0x0032E163, 0x0032E163, 0x0032E1AB, 0x0032E1AB], str([hex(x) for x in jt]))
pin("Q6 state 1: kind 0xFF ...", 0x0032E0D7, "cmp al, 0xff")
pin("Q6 ... -> 002DF6C0", 0x0032E111, "call 0x2df6c0")
pin("Q6 ... 0 -> state 2", 0x0032E127, "mov byte ptr [rbx + 0x20], 2")
check("Q6 002DF6C0 returns 0 on both branches", ins(0x002DF747) == "xor eax, eax" and ins(0x002DF77C) == "xor eax, eax"
      and ins(0x002DF77E) == "jmp 0x2df749")
pin("Q6 state 2 -> 3", 0x0032E15A, "mov byte ptr [rbx + 0x20], 3")
pin("Q6 state 3 waits on 0046DFE0", 0x0032E163, "call 0x46dfe0")
pin("Q6 0046DFE0 reports busy while the status word is -1", 0x0046DFE7, "cmp dword ptr [rip + 0x1cf1006], -1")
pin("Q6 0046E0E0 returns the status word 0215EFF4", 0x0046E0E0, "mov eax, dword ptr [rip + 0x1cf0f0e]")
pin("Q6 state = 5 + (status < 0)", 0x0032E1A3, "sets al")
pin("Q6 ...", 0x0032E1A6, "add al, 5")
pin("Q6 +0x22 == 0 -> the whole-file arm", 0x0032E1B1, "je 0x32e266")
pin("Q6 state 5 -> 0032E330", 0x0032E26F, "call 0x32e330")
pin("Q6 otherwise -> 0032E370", 0x0032E285, "call 0x32e370")
pin("Q6 0032E330 calls back with ok = 1", 0x0032E346, "mov r8d, 1")
pin("Q6 0032E370 calls back only for a whole-file request (+0x28 == -1)", 0x0032E382, "cmp dword ptr [rcx + 0x28], -1")
pin("Q6 ... with ok = 0", 0x0032E38C, "xor r8d, r8d")
pin("Q7 first branch: 0017D930 ...", 0x002DF6E1, "call 0x17d930")
pin("Q7 ... 0017D930 tests the file-system object's +0x88", 0x001D6B7B, "cmp byte ptr [rax + 0x88], cl")
pin("Q7 ... 001D6EF0", 0x002DF6EA, "call 0x1d6ef0")
pin("Q7 ... 001D6B40(path)", 0x002DF6F6, "call 0x1d6b40")
pin("Q7 ... the open 001D6F20(path, 1)", 0x002DF70C, "call 0x1d6f20")
pin("Q7 ... a null open skips the read and writes no status", 0x002DF717, "je 0x2df742")
pin("Q7 other branch: 001D6D90", 0x002DF777, "call 0x1d6d90")
pin("Q7 001D6D90 sets the status word to -1", 0x001D6DD4, "mov dword ptr [rax], 0xffffffff")
pin("Q7 ... callback 001D6D70", 0x001D6DEF, "lea rax, [rip - 0x86]")
pin("Q7 ... direct-callback byte", 0x001D6E08, "mov byte ptr [rdi + 0x18], 1")
pin("Q7 ... job type 2", 0x001D6E0C, "mov dword ptr [rdi], 2")
pin("Q7 ... posted", 0x001D6E51, "call 0x1a0bb0")
pin("Q8 001A07B0: type 2 -> 001A0CF0", 0x001A080C, "call 0x1a0cf0")
check("Q8 001A0CF0's only caller is 001A07B0", callers(0x001A0CF0) == [(0x001A07B0, 0x001A080C)])
pin("Q8 001A0CF0: not open ...", 0x001A0D68, "je 0x1a0d80")
pin("Q8 ... result 0xFFFFFFFE", 0x001A0D80, "mov eax, 0xfffffffe")
pin("Q8 ... stored as the job result", 0x001A0D87, "mov qword ptr [rbx + 0x10], rax")
check("Q8 001A09E0 answers only for paths ending '.cm'", [ins(a) for a in (0x001A0A05, 0x001A0A0E, 0x001A0A17)] ==
      ["cmp byte ptr [rcx + rdx], 0x2e", "cmp byte ptr [rcx + rdx], 0x63", "cmp byte ptr [rcx + rdx], 0x6d"])
pin("Q8 001A07B0 calls the job callback directly when +0x18 is set", 0x001A0840, "cmp byte ptr [rdi + 0x18], 0")
pin("Q8 ... with the result", 0x001A084F, "mov rcx, qword ptr [rdi + 0x10]")
pin("Q8 001D6D70 writes it to the status word", 0x001D6D7C, "mov dword ptr [rax], ecx")
check("Q8 the status pointer 01F82CC0 is written only by 001D6D90, 001D6FB0 and its own clear",
      sorted((f, a, k) for f, a, k in refs(0x01F82CC0) if k == "W") ==
      [(0x001D6D70, 0x001D6D7E, "W"), (0x001D6D90, 0x001D6DCD, "W"), (0x001D6FB0, 0x001D6FED, "W")])
pin("Q9 003789A0: ok = 0 -> the failure arm", 0x003789C9, "je 0x378a25")
pin("Q9 ... frees its own block", 0x00378A25, "call 0x3697f0")
pin("Q9 ... clears bit 0x40", 0x00378A2A, "and dword ptr [rip + 0x27646bf], 0xffffffbf")
pin("Q9 ... clears 02ADD098", 0x00378A31, "mov qword ptr [rip + 0x276465c], 0")
pin("Q9 ok = 1 -> the stub", 0x003789EE, "call 0x53dd10")
check("Q9 0053DD10 is mov eax, 1 / ret", T.R.at(0x0053DD10, 6) == b"\xb8\x01\x00\x00\x00\xc3")
pin("Q9 ... then publishes at 02ADD088", 0x00378A0B, "mov qword ptr [rip + 0x2764676], rax")
pin("Q9 003788F0 (mode 1) publishes at 02ADD088 after 0026FF90", 0x0037895B, "mov qword ptr [rip + 0x2764726], rax")
r88 = [(f, a, k) for f, a, k in refs(0x02ADD088)]
check("Q9 02ADD088: written by 00377CC0, 003788F0, 003789A0 and the teardown, read only by the teardown",
      r88 == [(0x00377CC0, 0x00377D3A, "W"), (0x00378230, 0x003783E0, "R"), (0x00378230, 0x003783F3, "R"), (0x00378230, 0x003783FF, "W"),
              (0x003788F0, 0x0037895B, "W"), (0x003789A0, 0x00378A0B, "W")], str(r88))
r98 = sorted({f for f, a, k in refs(0x02ADD098)})
check("Q9 02ADD098 is touched only by 00377CC0, 00377DC0 and 003789A0", r98 == [0x00377CC0, 0x00377DC0, 0x003789A0], str(r98))
pin("Q10 001D6B40 -> 0020BE50", 0x001D6B54, "call 0x20be50")
pin("Q10 0020BE50 normalises through 0020C440", 0x0020BF02, "call 0x20c440")
pin("Q10 ... hashes through 00674A00", 0x0020BF13, "call 0x674a00")
pin("Q10 ... compares only the hash", 0x0020BF33, "cmp dword ptr [rdx + 0x20], ebx")
pin("Q10 0020C440: '/' -> '\\'", 0x0020C4D5, "mov byte ptr [rcx], 0x5c")
pin("Q10 ... a doubled '\\' keeps one", 0x0020C4EF, "cmp byte ptr [rdi + 1], al")
pin("Q10 ... each byte through the CRT import at 008C2FF0", 0x0020C4F7, "call qword ptr [rip + 0x6b6af3]")
pin("Q10 ... trailing blanks off", 0x0020C523, "cmp byte ptr [rbx], 0x20")
import pefile  # noqa: E402
pe = pefile.PE(T.R.b.EXE, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
IMP = {i.address: (i.name or b"").decode() for e in pe.DIRECTORY_ENTRY_IMPORT for i in e.imports}
check("Q10 008C2FF0 is toupper", IMP.get(0x008C2FF0) == "toupper", str(IMP.get(0x008C2FF0)))
pin("Q10 00674A00: djb2 seed 0x1505", 0x00674A03, "mov eax, 0x1505")
pin("Q10 ... x 33", 0x00674A10, "imul eax, eax, 0x21")
pin("Q10 ... signed bytes", 0x00674A17, "movsx edx, dl")
pin("Q10 ... bit 31 cleared", 0x00674A23, "btr eax, 0x1f")
check("Q10 the cache gains keys only through 0020B680 <- 001D6A20 <- 0059A9B0 <- 0059EE90",
      callers(0x0020B680) == [(0x001D6A20, 0x001D6A53)] and callers(0x001D6A20) == [(0x0059A9B0, 0x0059AAA4)]
      and callers(0x0059A9B0) == [(0x0059EE90, 0x0059F1B7)], str((callers(0x0020B680), callers(0x001D6A20), callers(0x0059A9B0))))
pin("Q10 0059A9B0 fills the entry by ReadFile from the open handle", 0x0059AA27, "call qword ptr [rip + 0x327713]")
check("Q10 008C2140 is ReadFile", IMP.get(0x008C2140) == "ReadFile", str(IMP.get(0x008C2140)))


def norm(p):
    s = p
    i = 0
    while i < len(s) and not ("a" <= s[i] <= "z" or "0" <= s[i] <= "9" or "A" <= s[i] <= "Z"):
        i += 1
    s = s[i:].replace("/", "\\")
    out = []
    j = 0
    while j < len(s):
        if s[j] == "\\" and j + 1 < len(s) and s[j + 1] == "\\":
            j += 1
            continue
        out.append(s[j].upper())
        j += 1
    return "".join(out).rstrip(" ")


def djb2(s):
    h = 0x1505
    for c in s.encode("latin1"):
        h = (h * 33 + (c - 256 if c >= 128 else c)) & 0xFFFFFFFF
    return h & 0x7FFFFFFF


# data
mr = decode(IDX["ps2data/image/ff12/in/common/map_ref.bin"])
check("Q11 map_ref.bin is MRF v2", mr[:4] == b"MRF\x02")
rows_off, blk_off = struct.unpack_from("<ii", mr, 4)
nrows = (blk_off - rows_off) // 8
check("Q11 1,315 rows", nrows == 1315, str(nrows))
NS4 = 0x01E5E500
pin("Q11 namespace 4's table is 01E5E500 (002DF9A0)", 0x002DF9E1, "lea rax, [rip + 0x1b7eb18]")
pin("Q11 ... stored at 0215F020 = 0215F000 + 4 x 8", 0x002DF9E8, "mov qword ptr [rip + 0x1e7f631], rax")
check("Q11 ... and nothing else writes 0215F020", [(f, a) for f, a, k in refs(0x0215F020) if k == "W"] == [(0x002DF9A0, 0x002DF9E8)])


def ns4(i):
    q = q64(NS4 + 8 * i)
    return T.cstr(q, 200) if q else None


efb = {n.lower() for n in IDX if n.lower().startswith("ps2data/efb/") and n.lower().endswith(".efb")}
check("Q11 control: 410 .efb names in the archive", len(efb) == 410, str(len(efb)))
cat = collections.Counter()
same = 0
m0paths = []
rowidx = []
for f in range(nrows):
    own, blk = struct.unpack_from("<Hh", mr, rows_off + 8 * f)
    aux0 = struct.unpack_from("<h", mr, blk_off + 16 * blk)[0]
    rowidx.append((own, blk, aux0))
    res = []
    for idx in (aux0, own):
        s = ns4(idx)
        if s is None:
            res.append(None)
            continue
        k = max(s.rfind("\\"), s.rfind("/"))
        stem = s[k + 1:len(s) - 4]
        res.append(("ps2data/efb/" + stem + ".efb").lower())
    if res[0]:
        m0paths.append("PS2Data\\efb\\" + res[0].rsplit("/", 1)[1])
    if res[0] and res[1] and res[0] == res[1]:
        same += 1
    cat[(("null" if res[0] is None else ("ships" if res[0] in efb else "absent")),
         ("null" if res[1] is None else ("ships" if res[1] in efb else "absent")))] += 1
check("Q11 no mode-0 .efb name ships (1,281 fields name one)",
      sum(v for k, v in cat.items() if k[0] == "ships") == 0 and sum(v for k, v in cat.items() if k[0] == "absent") == 1281, str(dict(cat)))
check("Q11 mode 1 ships for 945 fields, names an absent .efb for 249, and names no package for 121",
      sum(v for k, v in cat.items() if k[1] == "ships") == 945 and sum(v for k, v in cat.items() if k[1] == "absent") == 249
      and sum(v for k, v in cat.items() if k[1] == "null") == 121, str(dict(cat)))
check("Q11 34 fields' mode-0 index names no package", sum(v for k, v in cat.items() if k[0] == "null") == 34)
check("Q11 the two indices never name the same package", same == 0, str(same))
TSV = os.path.join(DB, "03-World-Area-Field", "Map-Pack", "members", "map-ref-field-packs.tsv")
trows = [l.split("\t") for l in open(TSV, encoding="utf-8").read().splitlines() if l and not l.startswith("#")][1:]
check("Q11 control: the TSV's own_idx / block / block_idx equal the decoded rows in all 1,315",
      len(trows) == 1315 and all(int(r[1]) == o and int(r[4]) == b and int(r[5]) == a for r, (o, b, a) in zip(trows, rowidx)),
      "%d rows" % len(trows))
akeys = collections.defaultdict(set)
for n in IDX:
    akeys[djb2(norm(n))].add(n)
m0keys = {djb2(norm(p)): p for p in set(m0paths)}
coll = sorted((m0keys[k], sorted(akeys[k])[:2]) for k in m0keys if k in akeys)
check("Q12 the %d distinct mode-0 paths' keys collide with none of the %d archive names' keys" % (len(m0keys), len(IDX)), not coll, str(coll[:3]))
try:
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RAX, UC_X86_REG_RSP
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(0x00674000, 0x1000)
    mu.mem_write(0x00674A00, T.R.at(0x00674A00, 0x28))
    mu.mem_map(0x10000000, 0x10000)
    got = []
    for s in ("PS2DATA\\EFB\\ALC0101.EFB", "PS2DATA\\EFB\\OUS0100.EFB", "PS2DATA\\PLAN_MASTER\\MAP_CTRL\\OUS01\\OUS0101\\BIN\\OUS0101.MPK"):
        mu.mem_write(0x10000000, s.encode() + b"\0")
        mu.reg_write(UC_X86_REG_RCX, 0x10000000)
        mu.reg_write(UC_X86_REG_RSP, 0x10008000)
        mu.emu_start(0x00674A00, 0x00674A27)
        got.append((mu.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, djb2(s)))
    check("Q12 control: 00674A00 run under unicorn equals the Python key on three strings", all(a == b for a, b in got), str(got))
except ImportError:
    check("Q12 control: unicorn available", False)

inst = os.path.dirname(VBF)
top = sorted(os.listdir(inst))
loose = [os.path.join(dp, d) for dp, dn, fn in os.walk(inst) for d in dn + fn if d.lower() == "ps2data"]
check("Q13 the installed game beside the archive has no loose PS2Data tree (top level: %s)" % ", ".join(top), not loose, str(loose[:3]))

# ================================================================== P1: the embedded EFX0010 payload
print("\n== P1 (fef-and-motion-entries.md)")
pin("A1 00504940 stores the @FEF entry pointer at +0x230", 0x005049A7, "mov qword ptr [rbx + 0x230], rax")
pin("A1 ... rdx = movsxd of its low dword ...", 0x005049B6, "movsxd rdx, eax")
pin("A1 ... + 0x30", 0x005049B9, "add rdx, 0x30")
pin("A1 ... handed to 0016D6A0", 0x005049BD, "call 0x16d6a0")
check("A1 0016D6A0 is ret 0", T.R.at(0x0016D6A0, 3) == b"\xc2\x00\x00")
pin("A1 ... and the register is not used again (next: the +0x1F8 copy)", 0x005049C2, "mov rax, qword ptr [rbx + 0x1f8]")
cs = callers(0x003EDAD0)
check("A2 003EDAD0 has exactly six direct call sites", [(f, s) for f, s in cs] ==
      [(0x0026FB90, 0x0026FCEE), (0x002FC4A0, 0x002FC5D2), (0x003B0660, 0x003B0745), (0x003B2220, 0x003B226D), (0x003B29B0, 0x003B2A75),
       (0x003B38B0, 0x003B39B3)], str([hex(s) for f, s in cs]))
check("A2 ... no rip reference to it", not refs(0x003EDAD0))
check("A2 ... and no qword in the image equals it", not T.qword_sites(0x003EDAD0), str(T.qword_sites(0x003EDAD0)[:3]))
pin("A3 0026FB90: rbp = the blob's size dword", 0x0026FCE2, "movsxd rbp, dword ptr [r14]")
pin("A3 ... r14 += 0x10", 0x0026FCE5, "add r14, 0x10")
pin("A3 ... the blob pointer", 0x0026FCE9, "mov rcx, r14")
r30 = refs(0x01FD4A30)
check("A4 01FD4A30 has one writer, the boot hub 0022A0B0", [(f, a) for f, a, k in r30 if k == "W"] == [(0x0022A0B0, 0x0022A240)],
      str([(hex(f), hex(a), k) for f, a, k in r30]))
pin("A4 ... the result of the allocation 0036D240(0x3000100)", 0x0022A22A, "mov ecx, 0x3000100")
pin("A4 ...", 0x0022A236, "call 0x36d240")
pin("A4 002FC4A0 passes [01FD4A30]", 0x002FC5B3, "mov rcx, qword ptr [rip + 0x1cd8476]")
pin("A4 003B0660 loads [01FD4A30] into rbx", 0x003B06F8, "mov rbx, qword ptr [rip + 0x1c24331]")
pin("A4 ... loads namespace 10 index 0 into it", 0x003B070A, "lea ecx, [rdx + 0xa]")
pin("A4 ...", 0x003B070D, "call 0x32e620")
pin("A4 ... and passes it", 0x003B0742, "mov rcx, rbx")
pin("A4 ... index 0", 0x003B06EE, "xor edx, edx")
pin("A4 namespace 10's table is 01E127B8 (stored at 0215F050)", 0x002DF9FD, "lea rax, [rip + 0x1b32db4]")
pin("A4 ...", 0x002DFA04, "mov qword ptr [rip + 0x1e7f645], rax")
check("A4 ... its entry 0 is c_all.efx", T.cstr(q64(0x01E127B8), 200) == "PS2Data\\effect_finish\\jp\\common\\c_all.efx", str(T.cstr(q64(0x01E127B8), 200)))
pin("A4 002FC860 loads into it", 0x002FC956, "mov r8, qword ptr [rip + 0x1cd80d3]")
pin("A4 ...", 0x002FC96F, "call 0x32e620")
pin("A4 003B2310 loads namespace 12 into it", 0x003B23F0, "mov ecx, 0xc")
pin("A4 ...", 0x003B23F5, "mov r8, qword ptr [rip + 0x1c22634]")
pin("A5 003B2310 stores [01FD4A30] at the entry's +0x28", 0x003B23EC, "mov qword ptr [rbx + 0x28], rax")
pin("A5 003B2220 passes [entry + 0x28]", 0x003B2262, "mov rcx, qword ptr [rbx + 0x28]")
pin("A5 003B25D0 walks 02EBE5E0 ...", 0x003B25FE, "lea rbx, [rip + 0x2b0bfdb]")
pin("A5 ... 0x30 a step", 0x003B2696, "add rbx, 0x30")
pin("A5 ... 32 entries", 0x003B269E, "cmp r14d, 0x20")
tf = sorted({f for g in range(0x02EBE5E0, 0x02EBEBE0) for (f, a, k) in SC["refs"].get(g, ())})
w28 = []
for f in tf:
    for i in body(f):
        if not i.operands:
            continue
        o = i.operands[0]
        if o.type == 3 and i.mnemonic not in ("cmp", "test", "push", "lea") and o.mem.disp == 0x28 and len(i.operands) == 2:
            w28.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str)))
        if i.mnemonic.startswith("rep") or (i.mnemonic == "call" and i.op_str == "0x861ec0"):
            w28.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str)))
check("A5 over the 21 functions that address the table, +0x28 stores and bulk writes are: 003B1A80's 0, two rep movsq "
      "(entry moves), the 003B16B0 memset, two stack memsets, two bit clears in other tables",
      len(tf) == 21 and [(f, a) for f, a, t in w28] == [(0x003B16B0, 0x003B16D0), (0x003B18E0, 0x003B1A06), (0x003B1A80, 0x003B1B15),
                                                        (0x003B1BA0, 0x003B1C9D), (0x003B25D0, 0x003B265B), (0x003B29B0, 0x003B29F7),
                                                        (0x003B29B0, 0x003B2A56), (0x003B2B40, 0x003B2B77)],
      "; ".join("%08X %s" % (a, t) for f, a, t in w28))
pin("A5 003B1A80 writes 0", 0x003B1B04, "xor esi, esi")
pin("A5 003B16B0's memset is the table (02EBE5E0, 0x600 bytes)", 0x003B16C3, "lea rcx, [rip + 0x2b0cf16]")
pin("A5 ...", 0x003B16CA, "mov r8d, 0x600")
pin("A5 003B25D0's move copies entry + 0x30 over entry", 0x003B264C, "mov rsi, r15")
pin("A5 003B29B0's and 003B2B40's +0x28 are bit clears in the 02EBDBE0 table", 0x003B29CD, "lea rax, [rip + 0x2b0b20c]")
pin("A6 00558FB0 stores the 0057A2D0 result at [X + 0xD8]", 0x005591BB, "mov qword ptr [rsi + 0xd8], rax")
pin("A6 ... and passes [X + 0xD8]", 0x0055920F, "mov rcx, qword ptr [rbp + 0xd8]")
pin("A6 00561390 stores it", 0x0056177B, "mov qword ptr [rsi + 0xd8], rax")
pin("A6 ... and passes it", 0x005614BE, "mov rcx, qword ptr [rbx + 0xd8]")
pin("A6 00572E10 stores it at +0x11F8", 0x00572EDF, "mov qword ptr [rdi + 0x11f8], rax")
pin("A6 ... passes it", 0x00572F36, "mov rcx, qword ptr [rdi + 0x11f8]")
pin("A6 ... then frees it", 0x00572F50, "call 0x3697f0")
check("A6 0057A2D0 has exactly those three callers", [f for f, s in callers(0x0057A2D0)] == [0x00558FB0, 0x00561390, 0x00572E10])
pin("A6 0057A2D0 = 00249210(ctx, 7, edx + 0x31, ...)", 0x0057A2DF, "lea r8d, [rdx + 0x31]")
pin("A6 ...", 0x0057A2E3, "mov edx, 7")
pin("A6 ... returns [slot + 8]", 0x0057A2ED, "mov rax, qword ptr [rax + 8]")
pin("A6 00249210 sizes the file", 0x00249296, "call 0x32e400")
pin("A6 ... allocates", 0x002492CC, "call 0x36a190")
pin("A6 ... keeps the buffer at [slot + 8]", 0x002492DE, "mov qword ptr [rbx + 8], rdi")
pin("A6 ... and loads the file into it (namespace in ecx = 7)", 0x002492F0, "mov ecx, r15d")
pin("A6 ...", 0x002492F3, "call 0x32e620")
NS7 = 0x01EDD7E0
pin("A6 namespace 7's table is 01EDD7E0", 0x002DFF78, "lea rax, [rip + 0x1bfd861]")
nm7 = [T.cstr(q64(NS7 + 8 * i), 200) for i in (0x31, 0x32, 0x33)]
check("A6 ... indices 0x31..0x33 name the three menu .efx files", nm7 == ["PS2Data\\effect_finish\\in\\menu\\m_all.efx",
      "PS2Data\\effect_finish\\jp\\menu\\m_all2.efx", "PS2Data\\effect_finish\\in\\menu\\m_all3.efx"], str(nm7))
check("A6 the three call sites pass 0, 1 and 2 (indices 0x31, 0x32, 0x33)",
      ins(0x0056176F) == "lea r8d, [rdx + 2]" and ins(0x00561763) == "xor edx, edx" and ins(0x00572EC8) == "mov edx, 1"
      and ins(0x005591A5) == "mov edx, 2")
pin("A7 00409FE0: edx = dword[r14 + roundup64(size) - 4]", 0x0040A16F, "mov edx, dword ptr [rax + r14 - 4]")
pin("A7 ... 003B38B0", 0x0040A174, "call 0x3b38b0")
pin("A7 003B38B0: rdi = offset + resolved base", 0x003B38DA, "lea rdi, [rsi + rax]")
pin("A7 ... passed to 003EDAD0", 0x003B39AD, "mov rcx, rdi")
pin("A7 the file layer writes the model's length there (001A0CF0)", 0x001A0E1B, "mov dword ptr [rax + rbp - 4], edi")
pin("A7 ... (001A0E50)", 0x001A0F4E, "mov dword ptr [rax + rbp - 4], edi")
pin("A7 ... edi = the model read's byte count", 0x001A0DB0, "mov edi, dword ptr [rbx + 0x10]")
pin("A7 ... and the companion is read at buffer + that count", 0x001A0DF0, "add rdx, qword ptr [rsi + 0x100]")
cms = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if f.lower().endswith(".cm"):
            cms.append(os.path.join(dp, f))
fefs = []
for p in cms:
    d = open(p, "rb").read()
    if d[:4] != b"@FRP":
        continue
    var, clen, cnt_ = struct.unpack_from("<III", d, 4)
    base = 0x40 if var == 1 else 0x30
    for e in range(cnt_):
        o = base + struct.unpack_from("<I", d, base + e * 4)[0]
        if d[o:o + 4] == b"@FEF":
            fefs.append((p, o, len(d), d[o + 0x30:o + 0x37]))
check("A7 144 @FEF models; in each the payload (EFX0010 at +0x30) lies below the model's length",
      len(fefs) == 144 and all(o + 0x30 < n and m == b"EFX0010" for p, o, n, m in fefs), "%d" % len(fefs))
ns12tabs = set()
for i in body(0x002DF9A0):
    if i.mnemonic == "mov" and i.operands[0].type == 3 and i.operands[0].mem.base == 41 and i.address + i.size + i.operands[0].mem.disp == 0x0215F060:
        ns12tabs.add(i.address)
leas = {}
for i in body(0x002DF9A0):
    if i.mnemonic == "lea" and i.operands[1].type == 3 and i.operands[1].mem.base == 41:
        leas[i.reg_name(i.operands[0].reg)] = i.address + i.size + i.operands[1].mem.disp
    if i.mnemonic == "mov" and i.operands[0].type == 3 and i.operands[0].mem.base == 41 and i.address + i.size + i.operands[0].mem.disp == 0x0215F060:
        ns12tabs.add(leas.get(i.reg_name(i.operands[1].reg)))
cm12 = set()
for tb in ns12tabs:
    for k in range(0x400):
        q = q64(tb + 8 * k)
        s = T.cstr(q, 200) if q else None
        if s and s.lower().endswith(".cm"):
            cm12.add(s.replace("\\", "/").lower())
heads = {n: decode(IDX[n])[:8] for n in sorted(cm12) if n in IDX}
missing = sorted(cm12 - set(heads))
check("A8 namespace 12's .cm names (%d tables, %d names): the %d that ship all start '@FRP'; the rest are not in the archive"
      % (len(ns12tabs), len(cm12), len(heads)), len(cm12) == 18 and len(heads) == 17 and all(h[:4] == b"@FRP" for h in heads.values()),
      "absent: %s" % missing)
check("A8 003EDAD0 tests the three EFX magics first", T.R.at(0x00D11C70, 24) == b"EFX0010\0EFX0009\0EFX0008\0"
      and ins(0x003EDAE4) == "lea rcx, [rip + 0x924185]" and ins(0x003EDB5D) == "jne 0x3ee24d")
CHK = 0x00808F10


class Flow(S.Flow):
    """structflow, plus: __chkstk (00808F10) preserves the argument registers (structflow's call model clobbers them)"""
    def step(self, f, x, st, depth):
        if x.mnemonic == "call" and x.operands and x.operands[0].type == 2 and x.operands[0].imm == CHK:
            st.pop("rax", None)
            return
        S.Flow.step(self, f, x, st, depth)


getters = (0x004780B0, 0x003E55B0, 0x0041E590)
seeds = {(c, g) for g in getters for c, s in SC["calls"].get(g, ())} | {(0x004780C0, 0x002ED570)}
seeds = {s for s in seeds if s[0] not in getters}
pin("A9 the model instance is 0x260 bytes (00477EE0)", 0x00477EF3, "mov edx, 0x260")
pin("A9 004780B0 resolves a model-pool entry", 0x004780B3, "jmp 0x2ed570")
pin("A9 the binder's callback 00478270 is planted by 00478030 for 0051FF30", 0x00478030, "lea rdx, [rip + 0x239]")
check("A9 0051FF30's callers: 00478030 (the model pool) and two other pools", [f for f, s in callers(0x0051FF30)] == [0x00409F70, 0x0046E3E0, 0x00478030])
g = Flow([0x230, 0x1F8, 0x218, 0x21C], 3, stride=0x260, slot=0, seed_calls=seeds)
for f in (0x00504940, 0x00504F00, 0x00478270, 0x005049E0):
    g.enqueue(f, {"rcx": {"B"}}, 3)
g.run(sorted({s[0] for s in seeds}))
h230 = sorted((a, k, form) for f, a, k, form, off, w, t in g.hits if off == 0x230)
check("A9 census (%d seed functions, %d walked): +0x230 is touched at 005049A7 (the write) and two loop aliases"
      % (len({s[0] for s in seeds}), len(g.entry)), h230 == [(0x005049A7, "w", "B"), (0x00504B8C, "w", "E560"), (0x00504C10, "r", "E560")],
      str([("%08X" % a, k, fm) for a, k, fm in h230]))
pin("A9 alias 1: 005049E0's loop starts at +0x194 ...", 0x00504B49, "lea rax, [rsi + 0x194]")
pin("A9 ... 20 dwords", 0x00504B96, "cmp rbx, 0x14")
pin("A9 alias 2: 00504BC0's loop starts at +0x140 ...", 0x00504C00, "lea rbx, [rax + 0x140]")
pin("A9 ... 16 dwords", 0x00504C07, "mov edi, 0x10")
check("A9 ... no escape, no unknown-offset access, no tagged indirect call", not g.esc and not g.unk and not g.indirect)
c218 = sorted({f for f, a, k, form, off, w, t in g.hits if off in (0x218, 0x21C) and k == "r" and form == "B"})
check("A9 control: the census finds batch 10's three +0x218 / +0x21C readers", c218 == [0x005044D0, 0x00504D30, 0x0053AB50], str([hex(x) for x in c218]))

# ================================================================== P4: the aux pool
print("\n== P4 (ftr-node-table.md)")
pin("G1 rbx = record + 0x1B8 (the 00373DC0 call passes rbx - 0x1B8)", 0x00372A98, "lea rcx, [rbx - 0x1b8]")
pin("G1 00409300's output = record + 0xC0", 0x00372BAF, "lea r8, [rbx - 0xf8]")
pin("G1 ...", 0x00372BBC, "call 0x409300")
pin("G1 004094D0's output = record + 0x150", 0x00372BC1, "lea r8, [rbx - 0x68]")
pin("G1 ...", 0x00372BCB, "call 0x4094d0")
pin("G2 00409300: +0x3C = 1.0", 0x0040936A, "mov dword ptr [rdi + 0x3c], 0x3f800000")
pin("G2 bit 23 -> +0x30", 0x004093A6, "mov dword ptr [rdi + 0x30], ecx")
pin("G2 bit 24 -> +0x34", 0x004093BD, "mov dword ptr [rdi + 0x34], ecx")
pin("G2 bit 25 -> +0x38", 0x004093D4, "mov dword ptr [rdi + 0x38], ecx")
pin("G2 bits 26-28 as floats -> 0046D560(out, x, y, z)", 0x0040941B, "call 0x46d560")
check("G3 2pi at 01CEBC78 and 32768 at 00D10820", abs(f32(0x01CEBC78) - 2 * math.pi) < 1e-6 and f32(0x00D10820) == 32768.0)
for f in (0x0046D560, 0x0046D380):
    tx = [ins(f + d) for d in (4, 0xC, 0x13)]
    check("G3 %08X: divide by 2pi, LUT 01F004E0, times 32768" % f, tx[0] == ("movss xmm5, dword ptr [rip + 0x187e70c]" if f == 0x0046D560 else "movss xmm5, dword ptr [rip + 0x187e8ec]")
          and tx[1].startswith("lea r8, [rip + ") and f + 0x13 + int(tx[1].split("+ ")[1].rstrip("]"), 16) == 0x01F004E0, str(tx))
pin("G3 0046D560 masks the index to 0x7FFF", 0x0046D5B1, "and eax, 0x7fff")
pin("G3 ... cos = index offset 0x2000", 0x0046D582, "mov ecx, 0x2000")
check("G3 ... and writes rows 0-2 only (+0x00..+0x2C)", max(i.operands[0].mem.disp for i in body(0x0046D560)
      if i.mnemonic in ("movss", "mov") and i.operands[0].type == 3 and i.reg_name(i.operands[0].mem.base) == "rdx") == 0x2C)
pin("G4 004094D0: bit 21", 0x004094FF, "bt edx, 0x15")
pin("G4 ... sixteen dwords from the output's +0", 0x00409520, "mov dword ptr [r8 - 0x28], ecx")
pin("G4 ... else 0046D110", 0x00409593, "jmp 0x46d110")
pin("G4 0046D110 copies 01F204E0", 0x0046D110, "lea rdx, [rip + 0x1ab33c9]")
check("G4 01F204E0 is the identity", struct.unpack("<16f", T.R.at(0x01F204E0, 64)) == (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))
for a, t in ((0x00372BD0, "mov eax, dword ptr [rbx - 0xc8]"), (0x00372BD6, "mov dword ptr [rbx - 8], eax"),
             (0x00372BF9, "mov dword ptr [rbx - 0x88], eax"), (0x00372C3C, "mov dword ptr [rbx - 0xb0], 0x3f800000"),
             (0x00372C61, "mov dword ptr [rbx + 0x20], 0x3f800000"), (0x00372C7D, "mov dword ptr [rbx - 0x70], 0x3f800000")):
    pin("G5 binder copy / scale seed", a, t)
Bt = lambda v, k: v >> k & 1
inpool = 0
nrec = 0
ang = []
lastcol = collections.Counter()
b29 = []
for p in cms:
    d = open(p, "rb").read()
    if d[:4] != b"@FRP":
        continue
    var, clen, cnt_ = struct.unpack_from("<III", d, 4)
    base = 0x40 if var == 1 else 0x30
    for e in range(cnt_):
        o = base + struct.unpack_from("<I", d, base + e * 4)[0]
        if d[o:o + 4] != b"@FTR":
            continue
        n = struct.unpack_from("<I", d, o + 0xC)[0]
        aux = o + struct.unpack_from("<I", d, o + 0x34)[0]
        npool = (o + struct.unpack_from("<I", d, o + 8)[0] - aux) // 4
        for k in range(n):
            ro = o + (struct.unpack_from("<I", d, o + 0x40 + 4 * k)[0] >> 12)
            fl = struct.unpack_from("<I", d, ro + 4)[0]
            q = [ro + 8]

            def take():
                v = struct.unpack_from("<H", d, q[0])[0]
                q[0] += 2
                return v
            nrec += 1
            if Bt(fl, 30):
                take()
            if Bt(fl, 31):
                take()
            m16 = [take() for _ in range(16)] if Bt(fl, 21) else []
            if Bt(fl, 22):
                take()
            t3 = [take() for b in (23, 24, 25) if Bt(fl, b)]
            r3 = [take() for b in (26, 27, 28) if Bt(fl, b)]
            x29 = take() if Bt(fl, 29) else None
            pf = lambda i: struct.unpack_from("<f", d, aux + 4 * i)[0]
            if all(i < npool for i in m16 + t3 + r3):
                inpool += 1
            ang += [pf(i) for i in r3]
            if m16:
                M = [pf(i) for i in m16]
                lastcol[(M[3], M[7], M[11], M[15])] += 1
            if x29 is not None:
                b29.append(pf(x29) if x29 < npool else None)
check("G6 27,561 records, every stream index inside the pool", nrec == 27561 and inpool == nrec, "%d %d" % (nrec, inpool))
check("G6 the 36,871 rotation values lie in [-pi, pi]", len(ang) == 36871 and all(abs(a) <= math.pi + 1e-6 for a in ang),
      "%d %.6f %.6f" % (len(ang), min(ang), max(ang)))
check("G6 every one of the 27,561 bit-21 matrices has last column (0, 0, 0, 1)", lastcol == {(0.0, 0.0, 0.0, 1.0): 27561}, str(lastcol.most_common(2)))
check("G6 bit 29: 1,953 indices, all inside the pool, floats in [0.92, 1.38], 1.0 to four places in 1,697",
      len(b29) == 1953 and None not in b29 and 0.92 < min(b29) and max(b29) < 1.38 and sum(1 for v in b29 if round(v, 4) == 1.0) == 1697,
      "%d min %.4f max %.4f ones %d" % (len(b29), min(v for v in b29 if v is not None), max(v for v in b29 if v is not None),
                                         sum(1 for v in b29 if round(v, 4) == 1.0)))

# ================================================================== P6: the 0x290 consumers and the +0x94 readers
print("\n== P6 (ftr-node-table.md)")
for a, t in ((0x0041C2E5, "imul rbx, rax, 0x290"), (0x0041C2EF, "lea rdx, [rbx + 0xc0]"), (0x0041C2F6, "lea rcx, [rbx + 0x120]"),
             (0x0041C2FD, "call 0x46d730"), (0x0041C302, "mov eax, dword ptr [rbx + 0xf0]"), (0x0041C30F, "mov dword ptr [rbx + 0x130], eax"),
             (0x0041C33B, "mov eax, dword ptr [rbx + 0x100]"), (0x0041C359, "mov dword ptr [rbx + 0x148], eax")):
    pin("C1 0041C260", a, t)
for a, t in ((0x00373974, "imul rbx, rax, 0x290"), (0x00373998, "mov dword ptr [rbx + 0x284], eax"),
             (0x0037399E, "movzx eax, word ptr [rbx + 0x270]"), (0x003739AB, "movzx eax, word ptr [rbx + 0x276]"),
             (0x003739C2, "lea rsi, [rdi + 0x80]"), (0x003739CB, "sub rsi, -0x80"), (0x003739DD, "test byte ptr [rbx + 0x280], 0x10"),
             (0x003739EA, "lea rdx, [rbx + 0x1a0]"), (0x00373A04, "lea r8, [rbx + 0xc0]"), (0x00373ACC, "lea r8, [rbx + 0x230]"),
             (0x00373B3E, "lea r8, [rbx + 0x150]"), (0x00373A3C, "lea r8, [rbx + 0x1c0]"), (0x00373A43, "lea rdx, [rbx + 0xf0]"),
             (0x00373A68, "lea r8, [rbx + 0x1e0]"), (0x00373A6F, "lea rdx, [rbx + 0x100]"), (0x00373A80, "movss xmm0, dword ptr [rbx + 0x10c]"),
             (0x00373B58, "lea r9, [rbx + 0x100]"), (0x00373B66, "lea rax, [rbx + 0x150]"), (0x00373B6D, "lea r8, [rbx + 0x230]"),
             (0x00373B79, "lea rdx, [rbx + 0xc0]"), (0x00373B85, "call 0x372610"), (0x00373BE0, "movsx rax, word ptr [rbx + 0x27e]"),
             (0x00373BF7, "movups xmm0, xmmword ptr [rcx + rdi + 0x80]"), (0x00373C26, "mov ecx, dword ptr [rcx + rdi + 0x284]")):
    pin("C2 00373860", a, t)
for a, t in ((0x0037266C, "call 0x202d70"), (0x00372679, "lea rcx, [rip + 0x27677c0]"), (0x00372680, "call 0x202d70"),
             (0x00372685, "movss xmm2, dword ptr [rsi]"), (0x003726C6, "movss xmm2, dword ptr [rsi + 0xc]"),
             (0x003726DC, "mov r8, rdi"), (0x003726E4, "lea rcx, [rip + 0x2767795]"), (0x003726EB, "call 0x202d70")):
    pin("C3 00372610", a, t)
pin("C3 00373860 copies 02AD9E40 to +0x80", 0x00373B9C, "lea rdx, [rip + 0x276629d]")
pin("C3 ... and 02AD9E80 to the +0x284 matrix", 0x00373BAE, "lea rdx, [rip + 0x27662cb]")
for a, t in ((0x0041947A, "imul r15, rax, 0x290"), (0x00419486, "movzx eax, byte ptr [r15 + 0x28a]")):
    pin("C4 00418880", a, t)
acc = collections.defaultdict(set)
st = {}
for i in body(0x00418880):
    for op in i.operands:
        if op.type == 3 and i.mnemonic != "lea" and op.mem.base and i.reg_name(op.mem.base) == "r15" and not op.mem.index:
            kind = "w" if (op is i.operands[0] and len(i.operands) > 1 and i.mnemonic not in ("cmp", "test")) else "r"
            acc[op.mem.disp].add(kind)
fmw = {k: "".join(sorted(v)) for k, v in acc.items()}
check("C4 00418880 through r15 (the bone; r15 holds the owner elsewhere in the body): writes the local matrix +0xC0..+0xFF "
      "and +0x100..+0x10C, reads the staging +0x190 / +0x1A0 / +0x1B0 / +0x1D0 groups, and +0x280 / +0x28A",
      all("w" in fmw.get(k, "") for k in (0xC0, 0xD0, 0xE0, 0xF0, 0xF4, 0xF8, 0xFC, 0x100, 0x104, 0x108, 0x10C))
      and all("r" in fmw.get(k, "") for k in (0x190, 0x194, 0x198, 0x1A0, 0x1A4, 0x1A8, 0x1B0, 0x1B4, 0x1B8, 0x1BC, 0x1D0, 0x1D4, 0x1D8, 0x1DC, 0x280, 0x28A)),
      str(sorted((hex(k), v) for k, v in fmw.items() if k < 0x290)))
for a, t in ((0x00370738, "lea rdx, [r8 + 0x150]"), (0x0037073F, "imul rcx, rax, 0x290"), (0x0037074D, "call 0x202d60"),
             (0x0037075A, "add rdx, 0x150"), (0x0037077C, "sub rdx, -0x80"), (0x00370787, "call 0x202d70"),
             (0x003707C6, "mov rcx, qword ptr [rsi + 0x6c0]")):
    pin("C5 003703A0", a, t)


def rcx_src(f, s):
    lo = max(f, s - 80)
    xs = [i for i in T.R.md.disasm(T.R.at(lo, s - lo + 5), lo) if i.address <= s]
    regs = {"rcx"}
    for i in reversed(xs[:-1]):
        if i.mnemonic in ("mov", "lea") and i.operands and i.operands[0].type == 1 and i.reg_name(i.operands[0].reg) in regs:
            o = i.operands[1]
            if o.type == 1:
                regs = {i.reg_name(o.reg)}
                continue
            return "%s %s" % (i.mnemonic, i.op_str)
    return None


sk = {(f, 0x002ED570) for f, s in SC["calls"].get(0x002ED570, ()) if (rcx_src(f, s) or "").endswith(("+ 0xd98]", "+ 0x330]"))}
sk |= {(0x0046E4D0, 0x002ED570), (0x0046E420, 0x002ED570)}
pin("C6 the skeleton pool is the render root's +0xD98 (0041F340 -> 0046E4D0 -> 00372820)", 0x0041F404, "mov rsi, qword ptr [rax + 0xd98]")
g2 = Flow([0x94], 3, stride=0x1000000, slot=0, seed_calls=sk)
for f in (0x00372820, 0x003713C0, 0x00373860, 0x003714A0):
    g2.enqueue(f, {"rcx": {"B"}}, 3)
g2.run(sorted({s[0] for s in sk}))
wr = sorted({(f, a) for f, a, k, form, off, w, t in g2.hits if off == 0x94 and k == "w"})
rd = sorted({(f, a) for f, a, k, form, off, w, t in g2.hits if off == 0x94 and k == "r"})
check("C6 control: the census finds the binder's two writes and 003713C0's two", wr == [(0x003713C0, 0x00371435), (0x003713C0, 0x00371469),
      (0x00372820, 0x00372914), (0x00372820, 0x003729A9)], str(wr))
rf = sorted({f for f, a in rd})
check("C6 +0x94 is read by 28 functions (%d sites, %d seed functions, %d walked)" % (len(rd), len({s[0] for s in sk}), len(g2.entry)),
      len(rf) == 28, " ".join("%08X" % f for f in rf))


def resolves(a, depth=1):
    """from a read into ecx: the first call / jmp on the way is 0020E600 and nothing writes rcx before it (a jcc's target too)"""
    for i in T.R.md.disasm(T.R.at(a, 64), a):
        if i.address == a:
            continue
        if i.mnemonic in ("call", "jmp"):
            return i.op_str == "0x20e600"
        if i.mnemonic.startswith("j"):
            t = int(i.op_str, 16)
            if ins(t) not in ("call 0x20e600", "jmp 0x20e600") and (depth <= 0 or not resolves(t, depth - 1)):
                return False
            continue
        try:
            w = {i.reg_name(r) for r in i.regs_access()[1]}
        except Exception:
            w = set()
        if w & {"rcx", "ecx", "cx", "cl"}:
            return False
    return False


bad = []
for f, a in rd:
    x = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    if not (x.mnemonic == "mov" and x.op_str.startswith("ecx, dword ptr [") and resolves(a)):
        bad.append("%08X %s" % (a, x.op_str))
check("C6 every read loads ecx and the next call or jump on each path is 0020E600, with rcx untouched", not bad, "; ".join(bad[:6]))
pin("C6 003713C0 hands the resolved tail to 003E1C50", 0x00371487, "call 0x3e1c50")

# ================================================================== P3 and P5
print("\n== P3 / P5 (ftr-node-table.md)")
b_ = body(0x00372820)
ft = [i for i in b_ if "[r14 + 4]" in i.op_str]
check("B1 the binder reads the authored flag word only as 'test 0x100' (twice)", [i.op_str for i in ft] == ["dword ptr [r14 + 4], 0x100"] * 2)
pin("B1 ... and the link word at +0", 0x00372B15, "mov ecx, dword ptr [r14]")
pin("B2 003E5AD0: ids below 0x20 ...", 0x003E5AE7, "cmp edx, 0x20")
pin("B2 ... index the u16 table at +0x14C", 0x003E5AEF, "movzx eax, word ptr [rcx + rax*2 + 0x14c]")
pin("B2 ... 0x104 -> payload +0x3A", 0x003E5B00, "movzx eax, word ptr [r8 + 0x3a]")
pin("B2 ... 0x105 -> +0x3C", 0x003E5B0E, "movzx eax, word ptr [r8 + 0x3c]")
pin("B2 ... 0x106 -> +0x3E", 0x003E5B1C, "movzx eax, word ptr [r8 + 0x3e]")
pin("B2 0041F010 mode 0: the slot's bone word from FCP section 3", 0x0041F158, "movzx eax, word ptr [rax + rbp*2]")
pin("B2 the trail resolver 003711D0 compares the index with the skeleton's +0x88 count", 0x00371215, "movsx ecx, word ptr [rbx + 0x88]")
pin("B2 ... and refuses one at or past it", 0x0037121F, "cmp ebp, ecx")
FCP = open(os.path.join(DB, "17-Presentation-Rendering", "Model-And-Motion-Formats", "fcp-character-parameter-block.md"),
           encoding="utf-8").read()
RIG = os.path.join(DB, "17-Presentation-Rendering", "Character-Render-Records", "the-rig-of-seventeen-controllers.md")
check("D1 the FCP page records UQ-220 ANSWERED 2026-09-26 (FABLE): section 2 is the rig of seventeen controllers",
      "**ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): section 2 is the character's rig, the table of seventeen controllers" in FCP
      and os.path.isfile(RIG))

# ================================================================== control
print("\n== control")
rel = "ps2data/obj_finish/in/monster/m11/m1132/m1132.cm"
check("Z1 extract == archive: " + rel, rel in IDX and decode(IDX[rel]) == open(os.path.join(ROOT, rel), "rb").read())
vf.close()
print("PASSES %d" % PASSES)
print("FAILS %d" % FAILS)
