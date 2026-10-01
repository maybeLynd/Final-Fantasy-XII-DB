"""vp8_block_records.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
CORRECTION of OPUS's own carve 13ab80dcc (vp8_mbd_carve.py T3): the Vp8MacroblockDecoder block records start at +0x860, not
+0x880, there are 25 of them, not 24, and the 'offset' 0016FB80 writes is each record's +0x20, not its +0x00. The carve
saw one field per record, so any 0x38-aligned boundary fitted it; the pointer stores below fix the boundary.

  B  0016FA40 (vp8_setup_block_dptrs(xd)): a 25-pass loop (r9d = 0x19) with rax from xd + 0x868, stride 0x38, stores
     [rax - 8] = xd + 0x180 + 32b (qcoeff), [rax] = xd + 0x4A0 + 32b (dqcoeff), [rax + 0x20] = xd + 0x7C0 + b (eob). So
     record b is at xd + 0x860 + 0x38b with qword pointers at +0x00 / +0x08 / +0x28
  Q  the same routine's predictor stores land at +0x10 of those records: block 0 at xd + 0x870 = xd + 0 (luma, rows of 4
     blocks 0x40 apart), blocks 16 / 17 at xd + 0xBF0 / 0xC28 = xd + 0x100 / 0x104, blocks 20 / 21 = xd + 0x140 / 0x144
  O  0016FB80 (vp8_build_block_doffsets) stores its 16 luma offsets from xd + 0x880 at stride 0x38 and the chroma ones at
     xd + 0xC00 / 0xC38 / 0xC70 / 0xCA8 and 0xCE0 / 0xD18 / 0xD50 / 0xD88 = +0x20 of records 0..23; record 24 (the
     second-order block) gets none
  R  receivers: 0016F2A0 calls 0016FA40 with rcx = pbi (the embedded decoder at +0), and 00171480 with rcx = mb_row_di + i * 0x12A0
  W  REGRESSION rejecting the old reading (FAILS before): 'blocks' is Vp8BlockDescriptor[25] at +0x860; the record has
     qcoeff +0x00, dqcoeff +0x08, predictor +0x10, offset +0x20, eob +0x28; predictor, dqcoeff and eobs are rows of the
     macroblock decoder; and no row places a block record at +0x880
Usage: python vp8_block_records.py [--patch]
"""
import hashlib, os, sys
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
check("B", has(0x16FB29, 0x16FB79, [(0x16FB29, ("lea", "r8, [r9 + 0x7c0]")), (0x16FB30, ("lea", "rax, [r9 + 0x868]")), (0x16FB37, ("lea", "rdx, [r9 + 0x4a0]")),
                                     (0x16FB3E, ("mov", "r9d, 0x19")), (0x16FB50, ("lea", "rcx, [rdx - 0x320]")), (0x16FB57, ("mov", "qword ptr [rax], rdx")),
                                     (0x16FB5A, ("mov", "qword ptr [rax + 0x20], r8")), (0x16FB5E, ("add", "rdx, 0x20")), (0x16FB62, ("mov", "qword ptr [rax - 8], rcx")),
                                     (0x16FB66, ("lea", "rax, [rax + 0x38]")), (0x16FB6A, ("inc", "r8")), (0x16FB6D, ("sub", "r9, 1"))])
      and has(0x16FA40, 0x16FA70, [(0x16FA49, ("mov", "r11, rcx")), (0x16FA66, ("mov", "r9, rcx"))]),   # r9 = xd, the base of the loop above
      "0016FA40: 25 records from xd + 0x860, stride 0x38: +0x00 = qcoeff + 32b, +0x08 = dqcoeff + 32b, +0x28 = eobs + b")
check("Q", has(0x16FA40, 0x16FB29, [(0x16FA45, ("lea", "rdx, [rcx + 4]")), (0x16FA4F, ("lea", "r8, [rcx + 0x8a8]")), (0x16FA76, ("mov", "qword ptr [r8], rdx")),
                                     (0x16FA79, ("mov", "qword ptr [r8 - 0x38], rax")), (0x16FA7D, ("lea", "r8, [r8 + 0xe0]")), (0x16FA93, ("add", "rdx, 0x40")),
                                     (0x16FAA1, ("lea", "rcx, [r9 + 0x104]")), (0x16FAAE, ("lea", "rdx, [r9 + 0xc28]")), (0x16FAE9, ("lea", "rcx, [r9 + 0x144]")),
                                     (0x16FAF6, ("lea", "rdx, [r9 + 0xd08]"))]),
      "0016FA40: predictor pointers at record +0x10 (block 1 at xd + 0x8A8, blocks 17 / 21 at xd + 0xC28 / 0xD08)")
check("O", has(0x16FB80, 0x16FC0A, [(0x16FB83, ("lea", "r9, [rcx + 0x880]")), (0x16FB93, ("lea", "r9, [r9 + 0x38]")), (0x16FBAF, ("mov", "dword ptr [r9 - 0x38], edx")),
                                     (0x16FBB3, ("cmp", "r8d, 0x10")), (0x16FBB9, ("mov", "dword ptr [rcx + 0xc00], r10d")), (0x16FBC0, ("mov", "dword ptr [rcx + 0xce0], r10d")),
                                     (0x16FBC7, ("mov", "dword ptr [rcx + 0xc38], 4")), (0x16FBE4, ("mov", "dword ptr [rcx + 0xc70], eax")), (0x16FBFD, ("mov", "dword ptr [rcx + 0xca8], eax")),
                                     (0x16FC03, ("mov", "dword ptr [rcx + 0xd88], eax"))])
      and all((a - 0x860 - 0x20) % 0x38 == 0 for a in (0x880, 0xC00, 0xC38, 0xC70, 0xCA8, 0xCE0, 0xD18, 0xD50, 0xD88)),
      "0016FB80: every offset store is +0x20 of a record at xd + 0x860 + 0x38k (k = 0..23)")
check("R", has(0x16F3D1, 0x16F3E7, [(0x16F3D1, ("mov", "rcx, rsi")), (0x16F3E2, ("call", "0x16fa40"))])
      and has(0x17169C, 0x1716B6, [(0x17169C, ("imul", "rsi, rdi, 0x12a0")), (0x1716A7, ("mov", "rcx, qword ptr [rbx + 0x4410]")), (0x1716AE, ("add", "rcx, rsi")), (0x1716B1, ("call", "0x16fa40"))]),
      "0016FA40 runs on the embedded decoder (rcx = pbi) and on each mb_row_di record")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/vp8-macroblock-decoder/vp8_block_records.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
MBD, BLK = "Vp8MacroblockDecoder", "Vp8BlockDescriptor"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "CORRECTED 2026-09-28 (OPUS, %s %s; corrects 13ab80dcc). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was, w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
NR = "not written by 0016FA40 or 0016FB80"
def cells(l): return l.rstrip("\r\n").split("\t")
def new_mbd(old):
    w = lambda o: "%s %s %s" % (old[o][3], old[o][4], old[o][2]) if o in old else "-"
    return {0x0000: [r(MBD, 0x0000, 384, "predictor", "uint8[384]", "the prediction buffer the block records point into: luma 16 x 16 from +0x000, chroma 8 x 8 from +0x100 and +0x140 (0016FA40)", P, "Q", w(0))],
            0x04A0: [r(MBD, 0x04A0, 800, "dqcoeff", "int16[400]", "the dequantized coefficients: record b's +0x08 points at +0x4A0 + 32b (0016FA40)", P, "B", w(0x4A0)),
                     r(MBD, 0x07C0, 25, "eobs", "int8[25]", "one end-of-block byte per block: record b's +0x28 points at +0x7C0 + b (0016FA40)", P, "B", w(0x4A0)),
                     r(MBD, 0x07D9, 7, "unobservedSpan07D9", "u8[7]", NR + "; before dequantY1 at the next 16-byte boundary", U, "B", w(0x4A0))],
            0x0860: [r(MBD, 0x0860, 1400, "blocks", BLK + "[25]", "25 block records of 0x38 (16 luma, 4 + 4 chroma, 1 second-order): 0016FA40 points each at its qcoeff / dqcoeff / predictor / eob; 0016FB80 writes the offsets of the first 24", P, "B Q O", "%s; %s; %s" % (w(0x860), w(0x880), w(0xDC0))),
                     r(MBD, 0x0DD8, 8, "unobservedSpanDD8", "u8[8]", NR + "; between the last block record and preFrameBuffer", U, "B", w(0xDC0))]}
BLKROWS = [r(BLK, 0x00, 8, "qcoeff", "int16*", "the block's 16 quantized coefficients: xd + 0x180 + 32b (0016FA40)", P, "B", "offset uint32 at +0x00 and unobservedSpan0004 u8[52]"),
           r(BLK, 0x08, 8, "dqcoeff", "int16*", "the block's 16 dequantized coefficients: xd + 0x4A0 + 32b (0016FA40)", P, "B", "unobservedSpan0004"),
           r(BLK, 0x10, 8, "predictor", "uint8*", "the block's corner in the macroblock decoder's predictor buffer (0016FA40)", P, "Q", "unobservedSpan0004"),
           r(BLK, 0x18, 8, "unobservedSpan0018", "u8[8]", NR, U, "B", "unobservedSpan0004"),
           r(BLK, 0x20, 4, "offset", "uint32", "the block's byte offset in its plane: ((i>>2) * stride + (i&3)) * 4 for luma block i, 0 / 4 / stride*4 / stride*4 + 4 for the chroma blocks (0016FB80); not written for block 24", P, "O", "offset at +0x00"),
           r(BLK, 0x24, 4, "unobservedSpan0024", "u8[4]", NR, U, "B", "unobservedSpan0004"),
           r(BLK, 0x28, 8, "eob", "int8*", "the block's end-of-block byte: xd + 0x7C0 + b (0016FA40)", P, "B", "unobservedSpan0004"),
           r(BLK, 0x30, 8, "unobservedSpan0030", "u8[8]", NR, U, "B", "unobservedSpan0004")]
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]
    old = {int(cells(l)[1], 16): cells(l) for l in fl if cells(l)[0] == MBD}
    assert old[0x880][3] == "blocks" and old[0x860][2] == "32" and old[0xDC0][2] == "32" and old[0x4A0][2] == "832" and old[0][2] == "384", "unexpected starting rows"
    NEW = new_mbd(old); drop = {0x880, 0xDC0}; out = []; placedB = False
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == MBD and int(c[1], 16) in NEW: out += ["\t".join(x) + e for x in NEW[int(c[1], 16)]]; continue
        if c[0] == MBD and int(c[1], 16) in drop: continue
        if c[0] == BLK:
            if not placedB: out += ["\t".join(x) + e for x in BLKROWS]; placedB = True
            continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in tl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == BLK and "+0x0880" in c[12]:
            c[3] = "25 per Vp8MacroblockDecoder, from +0x860 (16 luma, 4 + 4 chroma, 1 second-order)"
            c[5] = "0016FA40 writes each record's pointers (+0x00 / +0x08 / +0x10 / +0x28); 0016FB80 writes the offset (+0x20) of the first 24"
            c[10] += " || CORRECTED 2026-09-28 (OPUS, %s B Q O): the records start at +0x860 and number 25; the offset is at record +0x20. was: 24 records from +0x880 with the offset at +0x00" % REC
            c[12] = "EMBED Vp8MacroblockDecoder +0x0860 stride=0x38"
            out.append("\t".join(c) + e); continue
        out.append(l)
    open(TY, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def tiles(t): return t in T and sum(int(c[2]) for c in F if c[0] == t) == int(T[t][1], 16)
M = {int(c[1], 16): c for c in F if c[0] == MBD}; K = {int(c[1], 16): c[3] for c in F if c[0] == BLK}
check("W", M.get(0x860, [0] * 5)[3:5] == ["blocks", BLK + "[25]"] and 0x880 not in M
      and [K.get(o) for o in (0, 8, 0x10, 0x20, 0x28)] == ["qcoeff", "dqcoeff", "predictor", "offset", "eob"]
      and [M.get(o, [0] * 4)[3] for o in (0, 0x4A0, 0x7C0)] == ["predictor", "dqcoeff", "eobs"] and "+0x0860" in T[BLK][12]
      and tiles(MBD) and tiles(BLK),
      "blocks = Vp8BlockDescriptor[25] at +0x860 (no record at +0x880); record qcoeff / dqcoeff / predictor / offset / eob at +0 / +8 / +0x10 / +0x20 / +0x28; both types tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
