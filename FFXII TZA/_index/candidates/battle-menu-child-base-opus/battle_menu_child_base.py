"""battle_menu_child_base.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
BattleMenuChildWidget1620's base-handler layout, and the correction of OPUS's own absence rows and of one migrated field.

  J  the installed handler 0027AD70 (both construction sites 002779FA / 00277A16 pass it) keeps this in rdi and, on every
     message it does not handle itself, tail-jumps to 003EE420 with rcx = this (0027ADB2 / 0027ADBF). The rows written on
     2026-09-20 / 09-22 read 'no access by either body installed on this object' - the tail jump was not followed, so
     003EE420's accesses below are this object's and those absence rows were wrong
  R  003EE420 (rsi = this) walks TWO 0x1E0-byte records from this + 0xC0 (loops end at `cmp r15d / r12d / r11d, 2`):
     message 1 writes each record's +0x170 / +0x178 / +0x180 and +0x1A0 / +0x1A8 / +0x1B0 and runs 002B3400 on
     record + 0xA0; message 2 runs 003EEBD0(record, record index == word [this + 0x4B0]); message 4 skips a record whose
     float +0x1D0 is not above 0, copies its +0x1D4 low byte into the target, and draws through 003EED60(this, record)
     and 003EEA80(record + 0x170) / 003EEA80(record + 0x1A0)
  T  002B3400 is one of TextDrawState's initialisers (its type row) and TextDrawState is 0xD0: record + 0xA0 + 0xD0 = +0x170
  G  003EEA80 on a 0x20-byte group: [+0] a sheet object, [+8] / [+0x10] one or two entry pointers ([+0x1C] != 0 selects
     two), [+0x18] a float scale (not above 0 skips; also multiplied into the draw)
  U  003EEBD0 moves four floats by a per-update step and clamps them to [0, 1.0]: record +0x1D0 (up when selected),
     +0x88 (by +0x1D4 bit 8), +0x188 and +0x1B8 (the two groups' scales, by bit 9)
  W  003EE420 on this: +0x480 a sheet pointer and +0x488 a layer byte, drawn at the int16 offsets +0x490 / +0x492 with the
     block at +0x494 by address, only while the float +0x48C is above 0; message 2 moves +0x4A8 / +0x4AC by bits 0 / 1 of
     the word +0x4B4 and +0x48C by bit 0 of the byte +0x4B8, each clamped to [0, 1.0]; the word +0x4B0 is the selected record
  X  the migrated row dword0340 (singleton +0xB240 = AB30 +0x710) is NOT this widget's: 00290707 builds a 0x720-byte widget
     (00296940: `mov edx, 0x720` into 00245000, handler 002985D0) at singleton + 0xAB30 when +0x10F68 bit 0x2000 is clear,
     and 00290CF0 builds the 0x61F0 battle-menu widget (00276650) in the same storage in the other mode; the +0x710
     accesses (002964BA, 0029696A, 002906FF) run behind bit 0x2000 on that storage, so they belong to the 0x720 widget,
     while inside the 0x61F0 widget the same bytes are the second record's TextDrawState
  P  REGRESSION (FAILS before): the rows are in the store; no BattleMenuChildWidget1620 row claims +0x340 as a dword; the
     0x720 widget type carries +0x710
Usage: python battle_menu_child_base.py [--patch]
"""
import hashlib, os, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
    return all(A.get(a) == v for a, v in pairs)
check("J", has(0x27AD70, 0x27ADC4, [(0x27AD80, ("mov", "rdi, rcx")), (0x27ADAF, ("mov", "rdx, rsi")), (0x27ADB2, ("mov", "rcx, rdi")), (0x27ADBF, ("jmp", "0x3ee420"))]),
      "0027AD70 tail-jumps to 003EE420 with rcx = this")
check("R", has(0x3EE420, 0x3EE8B3, [(0x3EE42A, ("mov", "rsi, rcx")), (0x3EE7D6, ("lea", "rbx, [rsi + 0x240]")), (0x3EE7E0, ("mov", "qword ptr [rbx - 0x10], rdi")),
                                     (0x3EE80A, ("mov", "qword ptr [rbx - 8], rax")), (0x3EE82A, ("mov", "qword ptr [rbx], rax")), (0x3EE82D, ("mov", "qword ptr [rbx + 0x20], rdi")),
                                     (0x3EE851, ("mov", "qword ptr [rbx + 0x28], rax")), (0x3EE876, ("mov", "qword ptr [rbx + 0x30], rax")), (0x3EE87D, ("imul", "rcx, rax, 0x1e0")),
                                     (0x3EE884, ("add", "rcx, 0x160")), (0x3EE88E, ("call", "0x2b3400")), (0x3EE896, ("lea", "rbx, [rbx + 0x1e0]")), (0x3EE89D, ("cmp", "r15d, 2")),
                                     (0x3EE680, ("movzx", "eax, word ptr [rsi + 0x4b0]")), (0x3EE693, ("imul", "rcx, rax, 0x1e0")), (0x3EE69A, ("add", "rcx, 0xc0")),
                                     (0x3EE6A4, ("call", "0x3eebd0")), (0x3EE6AC, ("cmp", "r11d, 2")), (0x3EE590, ("lea", "r14, [rsi + 0xc0]")), (0x3EE59E, ("imul", "rax, r13, 0x1e0")),
                                     (0x3EE5AF, ("comiss", "xmm6, dword ptr [r14 + 0x1d0]")), (0x3EE5BD, ("movzx", "eax, byte ptr [r14 + 0x1d4]")), (0x3EE5DE, ("call", "0x3eed60")),
                                     (0x3EE5E6, ("lea", "rcx, [r14 + 0x170]")), (0x3EE612, ("call", "0x3eea80")), (0x3EE623, ("lea", "rcx, [r14 + 0x1a0]")), (0x3EE637, ("call", "0x3eea80")),
                                     (0x3EE646, ("cmp", "r12d, 2"))]),
      "003EE420: two 0x1E0 records from +0xC0 (create / update / draw loops of 2)")
TY = os.path.join(DB, "_types", "types.tsv"); FI = os.path.join(DB, "_types", "fields.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
TT = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
check("T", "002B3400" in "\t".join(TT["TextDrawState"]) and TT["TextDrawState"][1] == "0xD0" and 0xA0 + 0xD0 == 0x170,
      "002B3400 initialises TextDrawState (0xD0), placed at record + 0xA0 and ending at + 0x170")
check("G", has(0x3EEA80, 0x3EEB88, [(0x3EEA8D, ("movss", "xmm1, dword ptr [rcx + 0x18]")), (0x3EEA95, ("comiss", "xmm0, xmm1")), (0x3EEAA4, ("jae", "0x3eebc2")),
                                     (0x3EEABA, ("lea", "r14, [rcx + 8]")), (0x3EEAEC, ("mulss", "xmm0, xmm1")), (0x3EEAFA, ("cmp", "dword ptr [rcx + 0x1c], esi")),
                                     (0x3EEAFD, ("setne", "sil")), (0x3EEB10, ("mov", "rcx, qword ptr [r14]")), (0x3EEB4D, ("mov", "rax, qword ptr [rdi]"))]),
      "003EEA80: sheet +0, one or two entries from +8 (by +0x1C), float scale +0x18")
ONE = struct.unpack_from("<f", d, off(0x3EEBDE + 8 + 0x18FCFC2))[0]
check("U", ONE == 1.0 and has(0x3EEBD0, 0x3EED5A, [(0x3EEC05, ("movss", "xmm0, dword ptr [rcx + 0x1d0]")), (0x3EEC0D, ("test", "r9d, r9d")), (0x3EEC24, ("minss", "xmm1, xmm0")),
                                     (0x3EEC2E, ("maxss", "xmm0, xmm1")), (0x3EEC35, ("movss", "dword ptr [rcx + 0x1d0], xmm0")), (0x3EEC4F, ("test", "dword ptr [r10 + 0x1d4], 0x100")),
                                     (0x3EEC90, ("movss", "dword ptr [r10 + 0x88], xmm0")), (0x3EECAB, ("test", "dword ptr [r10 + 0x1d4], 0x200")),
                                     (0x3EECEC, ("movss", "dword ptr [r10 + 0x188], xmm0")), (0x3EED07, ("test", "dword ptr [r10 + 0x1d4], 0x200")), (0x3EED1D, ("movss", "xmm0, dword ptr [r10 + 0x1b8]"))]),
      "003EEBD0: +0x1D0 / +0x88 / +0x188 / +0x1B8 stepped and clamped to [0, %.1f]" % ONE)
check("W", has(0x3EE420, 0x3EE7C7, [(0x3EE486, ("cmp", "qword ptr [rsi + 0x480], 0")), (0x3EE493, ("comiss", "xmm6, dword ptr [rsi + 0x48c]")), (0x3EE49C, ("movzx", "eax, byte ptr [rsi + 0x488]")),
                                     (0x3EE4A3, ("lea", "r8, [rsi + 0x494]")), (0x3EE4B4, ("movsx", "eax, word ptr [rsi + 0x492]")), (0x3EE4BB, ("movsx", "r9d, word ptr [rsi + 0x490]")),
                                     (0x3EE4D0, ("mov", "rdx, qword ptr [rsi + 0x480]")), (0x3EE4DB, ("call", "0x2d8cb0")), (0x3EE6CC, ("movzx", "r8d, word ptr [rsi + 0x4b4]")),
                                     (0x3EE6EF, ("test", "r8b, 1")), (0x3EE718, ("movss", "dword ptr [rsi + 0x4a8], xmm0")), (0x3EE745, ("test", "r8b, 2")),
                                     (0x3EE76B, ("movss", "dword ptr [rsi + 0x4ac], xmm0")), (0x3EE785, ("test", "byte ptr [rsi + 0x4b8], 1")), (0x3EE7B5, ("movss", "dword ptr [rsi + 0x48c], xmm3"))]),
      "003EE420 on this: sheet +0x480, layer +0x488, fades +0x48C / +0x4A8 / +0x4AC by +0x4B8 / +0x4B4 bits, offsets +0x490 / +0x492")
check("X", has(0x290707, 0x290730, [(0x290707, ("test", "dword ptr [rcx + 0x10f68], 0x2000")), (0x290711, ("jne", "0x290730")), (0x290713, ("add", "rcx, 0xab30")),
                                     (0x29071A, ("call", "0x296940")), (0x290726, ("or", "dword ptr [rax + 0x10f68], 0x2000"))])
      and has(0x296940, 0x296954, [(0x29694A, ("mov", "edx, 0x720")), (0x29694F, ("jmp", "0x245000"))]) and 0x296943 + 7 + 0x1C86 == 0x2985D0
      and has(0x290D31, 0x290DC5, [(0x290D37, ("test", "al, 0x10")), (0x290D96, ("lea", "rcx, [rbx + 0xab30]")), (0x290DC0, ("call", "0x276650"))])
      and has(0x290640, 0x290674, [(0x290640, ("test", "dword ptr [rcx + 0x10f68], 0x2000")), (0x290664, ("add", "rcx, 0xab30")), (0x29066F, ("jmp", "0x296490"))])
      and has(0x296490, 0x2964C4, [(0x29649A, ("mov", "rbx, rcx")), (0x2964BA, ("mov", "dword ptr [rbx + 0x710], 1"))])
      and has(0x296960, 0x296975, [(0x29696A, ("cmp", "dword ptr [rcx + 0x710], 0"))])
      and has(0x2906D0, 0x290710, [(0x2906E7, ("add", "rcx, 0xab30")), (0x2906FF, ("cmp", "dword ptr [rcx + 0xb240], eax"))]),
      "singleton + 0xAB30 hosts a 0x720 widget (00296940, bit 0x2000) or the 0x61F0 battle menu (00276650); +0x710 is the 0x720 widget's")

REC = "_index/candidates/battle-menu-child-base-opus/battle_menu_child_base.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BM, RC, SP, W7, AB = "BattleMenuChildWidget1620", "BattleMenuChildRecord1E0", "SpritePartsRef20", "Widget0720At0209BE80_AB30", "ManagerSub0209BE80_AB30"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "CORRECTED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was="-", w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
NR = "not reached by 003EE420 or its callees read here"
def bm_rows(was):
    return [r(BM, 0x00C0, 0x3C0, "records", RC + "[2]", "two 0x1E0 records the base handler 003EE420 (reached by 0027AD70's tail jump) creates, updates and draws", P, "J R", was),
            r(BM, 0x0480, 8, "sheet480", "void*", "a sprite sheet drawn by 003EE420 (002D8CB0) when set and while fade48C is above 0", P, "W", was),
            r(BM, 0x0488, 1, "layer488", "uint8", "copied into the draw target's +0x5C for that draw", P, "W", was),
            r(BM, 0x0489, 3, "unobservedSpan0489", "u8[3]", NR, U, "W", was),
            r(BM, 0x048C, 4, "fade48C", "float", "gates the sheet draw (above 0); stepped by message 2 toward 1.0 or 0 by bit 0 of layerFlags4B8 and clamped", P, "W", was),
            r(BM, 0x0490, 2, "drawX490", "int16", "added to a global offset for the sheet draw", P, "W", was),
            r(BM, 0x0492, 2, "drawY492", "int16", "added to a global offset for the sheet draw", P, "W", was),
            r(BM, 0x0494, 20, "unobservedSpan0494", "u8[20]", "passed by address (+0x494) to the sheet draw; its width is not fixed here", U, "W", was),
            r(BM, 0x04A8, 4, "fade4A8", "float", "stepped by message 2 by bit 0 of fadeDirections4B4 and clamped to [0, 1.0]", P, "W", was),
            r(BM, 0x04AC, 4, "fade4AC", "float", "stepped by message 2 by bit 1 of fadeDirections4B4 and clamped to [0, 1.0]", P, "W", was),
            r(BM, 0x04B0, 2, "selectedRecord", "uint16", "the record index message 2 steps up (the others step down) and message 4 draws first", P, "R W", was),
            r(BM, 0x04B2, 2, "unobservedSpan04B2", "u8[2]", NR, U, "W", was),
            r(BM, 0x04B4, 2, "fadeDirections4B4", "uint16", "bit 0 / bit 1: whether fade4A8 / fade4AC rise or fall", P, "W", was),
            r(BM, 0x04B6, 2, "unobservedSpan04B6", "u8[2]", NR, U, "W", was),
            r(BM, 0x04B8, 1, "layerFlags4B8", "uint8", "bit 0: whether fade48C rises or falls", P, "W", was),
            r(BM, 0x04B9, 7, "unobservedSpan04B9", "u8[7]", NR, U, "W", was)]
RCROWS = [r(RC, 0x000, 128, "unobservedSpan000", "u8[128]", NR, U, "R"),
          r(RC, 0x080, 8, "object80", "void*", "read by 003EED60 and stored into the text-draw state's +0x28", P, "R"),
          r(RC, 0x088, 4, "fade88", "float", "stepped by 003EEBD0 by flags1D4 bit 8, clamped to [0, 1.0]; read by 003EED60 for the text draw", P, "U R"),
          r(RC, 0x08C, 2, "word8C", "uint16", "read by 003EED60 for the text draw", P, "R"),
          r(RC, 0x08E, 18, "unobservedSpan08E", "u8[18]", NR, U, "R"),
          r(RC, 0x0A0, 0xD0, "textDraw", "TextDrawState", "initialised by 002B3400 on create; drawn through 003EED60", P, "R T"),
          r(RC, 0x170, 0x20, "partsA", SP, "a sprite-parts group written on create and drawn by 003EEA80", P, "R G"),
          r(RC, 0x190, 16, "unobservedSpan190", "u8[16]", NR, U, "R"),
          r(RC, 0x1A0, 0x20, "partsB", SP, "a second sprite-parts group, drawn after partsA", P, "R G"),
          r(RC, 0x1C0, 16, "unobservedSpan1C0", "u8[16]", NR, U, "R"),
          r(RC, 0x1D0, 4, "fade1D0", "float", "gates the record's draw (above 0); stepped up while the record is selected, down otherwise, clamped to [0, 1.0]", P, "U R"),
          r(RC, 0x1D4, 4, "flags1D4", "uint32", "low byte: the draw layer copied into the target; bit 8 drives fade88; bit 9 drives both parts' scales", P, "U R"),
          r(RC, 0x1D8, 8, "unobservedSpan1D8", "u8[8]", NR, U, "R")]
SPROWS = [r(SP, 0x00, 8, "sheet", "void*", "the sheet object 003EEA80 draws from ([sheet] -> +0x20 -> +0x30 tables)", P, "G"),
          r(SP, 0x08, 16, "entries", "void*[2]", "one or two sprite entries (each read as four words and a nibble pair)", P, "G"),
          r(SP, 0x18, 4, "scale", "float", "not above 0 skips the draw; multiplied into it; stepped by 003EEBD0 on bit 9", P, "G U"),
          r(SP, 0x1C, 4, "twoEntries", "uint32", "non-zero draws both entries", P, "G")]
NEWT = [[RC, "0x1E0", "16-UI", "two at BattleMenuChildWidget1620 +0xC0", "EMBEDDED in BattleMenuChildWidget1620", "003EE420 message 1 (fields) and 002B3400 (textDraw)", "not read here", P[0], P[1], "L1",
         "CARVED 2026-09-28 (OPUS, %s R). Stride 0x1E0 and count 2 from 003EE420's three loops. %s" % (REC, EXE), "16-UI/Widget-Object-Model/CONTRACT-widget-object.md", "EMBED BattleMenuChildWidget1620 +0x00C0 stride=0x1E0 count=2"],
        [SP, "0x20", "16-UI", "two per BattleMenuChildRecord1E0, at +0x170 and +0x1A0", "EMBEDDED", "003EE420 message 1", "not read here", P[0], P[1], "L1",
         "CARVED 2026-09-28 (OPUS, %s G). %s" % (REC, EXE), "16-UI/Widget-Object-Model/CONTRACT-widget-object.md", "EMBED BattleMenuChildRecord1E0 +0x170"],
        [W7, "0x720", "16-UI", "at ManagerSingleton0209BE80 +0xAB30 while +0x10F68 bit 0x2000 is set - the same storage the 0x61F0 battle menu (ManagerSub0209BE80_AB30) occupies in the other mode",
         "IN PLACE - 00296940 (built by 00290707 when bit 0x2000 is clear, which then sets it)", "00296940: 00245000 at 0029694F (mov edx, 0x720; handler 002985D0)", "not read here", P[0], P[1], "L1",
         "DECLARED 2026-09-28 (OPUS, %s X). %s" % (REC, EXE), "00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md", "DYNAMIC ManagerSingleton0209BE80 +0xAB30 while +0x10F68 bit 0x2000 is set"]]
def w7rows(old):
    return [r(W7, 0x000, 0xC0, "widgetBase0000", "Widget", "the shared widget base 00245000 / 002465F0 write on every constructed widget", P, "X"),
            r(W7, 0x0C0, 0x650, "unobservedSpan0C0", "u8[1616]", "reached by its methods (00296490 reads a qword at +0xC0; 00296960 reaches +0x180 / +0x414 / +0x648 per CONTRACT-per-frame-update-gate); not typed here", U, "X"),
            [W7, "0x710", "4", "dword0710", "uint32", "set to 1 by 00296490 (002964BA) and compared with 0 by 00296960 (0029696A) and 002906D0 (002906FF, as singleton +0xB240); all run behind +0x10F68 bit 0x2000. RE-HOMED 2026-09-28 (OPUS, %s X) from BattleMenuChildWidget1620 +0x340, where FABLE's rule-0 migration had placed it; the storage is shared, and inside the 0x61F0 battle menu these bytes are the second record's textDraw" % REC,
             P[0], "PROBABLE", old + " || RE-HOMED 2026-09-28 (OPUS, %s X)" % REC],
            r(W7, 0x714, 12, "unobservedSpan714", "u8[12]", "not read here", U, "X")]
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]
    old = {int(cells(l)[1], 16): cells(l) for l in fl if cells(l)[0] == BM}
    assert old[0xC0][2] == "640" and old[0x340][3] == "dword0340" and old[0x344][2] == "380", "unexpected starting rows"
    was = "unobservedSpan00C0 (640 B) 'no access by either body installed', dword0340 (MIGRATED, now re-homed to %s +0x710), unobservedSpan0344 (380 B) 'no access by either body installed'" % W7
    out = []; placed = False
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == BM and int(c[1], 16) in (0xC0, 0x340, 0x344):
            if not placed: out += ["\t".join(x) + e for x in bm_rows(was)]; placed = True
            continue
        out.append(l)
    idx = max(i for i, l in enumerate(out) if cells(l)[0] == BM)
    out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in RCROWS + SPROWS + w7rows(old[0x340][8])]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]; to = []
    for l in tl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == AB and REC not in c[10]:
            c[10] += " || SHARED STORAGE 2026-09-28 (OPUS, %s X): 00290707 builds a different 0x720-byte widget (%s, 00296940) at the same singleton + 0xAB30 while +0x10F68 bit 0x2000 is clear; this 0x61F0 widget is built by 00290CF0 in the other mode" % (REC, W7)
        to.append("\t".join(c) + e)
    ti = max(i for i, l in enumerate(to) if cells(l)[0] == BM)
    to[ti + 1:ti + 1] = ["\t".join(x) + te for x in NEWT if not any(cells(y)[0] == x[0] for y in to)]
    open(TY, "wb").write("".join(to).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
TT = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def tiles(t): return t in TT and sum(int(c[2]) for c in F if c[0] == t) == int(TT[t][1], 16)
M = {int(c[1], 16): c for c in F if c[0] == BM}
if M.get(0, [0] * 5)[4] == "BattleMenuChildBase4C0":   # the rows below +0x4C0 moved to the base type (child_base_4c0.py E)
    M.update({int(c[1], 16): c for c in F if c[0] == "BattleMenuChildBase4C0" and int(c[1], 16) > 0})
check("P", M.get(0xC0, [0] * 5)[3:5] == ["records", RC + "[2]"] and 0x340 not in M and M.get(0x4B0, [0] * 4)[3] == "selectedRecord"
      and any(c[0] == W7 and c[1] == "0x710" and c[3] == "dword0710" for c in F) and all(tiles(t) for t in (BM, RC, SP, W7)),
      "records[2] at +0xC0 and the +0x480..+0x4BF fields; no +0x340 dword on the widget; %s carries +0x710; the four types tile" % W7)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
