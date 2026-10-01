"""vp8_mbd_carve.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Vp8DecoderInstance's first 0x12A0 bytes are a
record laid out like the decoder's per-thread records, and two element types inside it are read from the bytes.

  T1 vp8_decode's thread loop (0016E8A2..0016E96E): for i < [inst+0x4390], the record at [inst+0x4410] + i*0x12A0 (0016E94A imul
     0x12a0 / 0016E951 add [rdi+0x4410]) receives a 0x90-byte copy at +0xE70..+0xEFF (nine 16-byte moves 0016E8B7..0016E93F) and
     is passed to 0016FB80 (0016E958); after the loop 0016FB80 is called on the instance itself (0016E974 mov rcx, rdi /
     0016E977). So the per-thread records are 0x12A0 apart and the instance's own +0x0000 is handed to the same routine
  T2 the copy's source: rbx = inst + 0x12C0 (0016E681 lea rcx, [rdi+0x12c0] / 0016E6A3 / 0016E6DA mov rbx, [rbp-0x28]), and the
     source row is [rbx + 0x780 + idx*0x90] with idx = [rbx+0x9D0] (0016E8A2..0016E8B7)
  T3 0016FB80 writes one dword per block record, stride 0x38 from +0x880: 16 luma records (loop 0016FB90..0016FBB7, offset =
     ((i>>2) * [+0xE80] + (i&3)) * 4) and eight chroma records at +0xC00 .. +0xD88 from 0, 4 and [+0xE94] * 4 (+ 4): 24 records,
     +0x880..+0xDBF. +0xE80 and +0xE94 are the copy's +0x10 and +0x24
  T4 00172750 (vp8_destroy passes inst + 0x12C0 at 0016E252) walks 0x90-byte records at +0x780 (4, stride 0x90), +0x9E0, +0xA70,
     +0xB00 ...: when [rec+0x60] > 0 it frees [[rec+0x58] - 8] (the vpx_memalign original pointer) and then memsets the record to 0
     for 0x90 bytes. So the 0x90 records are frame-buffer records with an owned allocation at +0x58 sized by +0x60
  Extent: the per-thread stride is 0x12A0 and the next structure in the instance starts at +0x12C0 (T2, T4), so the embedded record
  is taken as 0x12A0 with a 32-byte remainder at +0x12A0. The instance's existing +0xF84..+0xF93 rows move into the record.
  Not established: whether the thread record holds anything beyond this layout, the block records' other bytes, the frame-buffer
  record's other fields, and what +0x12A0..+0x12BF holds.
  S  REGRESSION: the carve is in the store as generated, tiling kept (FAILS before)
Usage: python vp8_mbd_carve.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
A = lambda pairs: all(at(a) == v for a, v in pairs)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
cp = all(at(0x16E8BF + 0x20 * k) == ("movups", "xmmword ptr [rax + rsi + 0x%x], xmm0" % (0xE70 + 0x20 * k)) for k in range(5)) and \
     all(at(0x16E8CF + 0x20 * k) == ("movups", "xmmword ptr [rax + rsi + 0x%x], xmm1" % (0xE80 + 0x20 * k)) for k in range(4))
check("T1", cp and A([(0x16E892, ("cmp", "dword ptr [rdi + 0x4390], r13d")), (0x16E8AD, ("mov", "rax, qword ptr [rdi + 0x4410]")),
                     (0x16E94A, ("imul", "rcx, rax, 0x12a0")), (0x16E951, ("add", "rcx, qword ptr [rdi + 0x4410]")), (0x16E958, ("call", "0x16fb80")),
                     (0x16E960, ("lea", "rsi, [rsi + 0x12a0]")), (0x16E967, ("cmp", "r11d, dword ptr [rdi + 0x4390]")),
                     (0x16E974, ("mov", "rcx, rdi")), (0x16E977, ("call", "0x16fb80"))]),
      "thread records at [inst+0x4410] + i*0x12A0 get a 0x90 copy at +0xE70 and 0016FB80; then 0016FB80(inst)")
check("T2", A([(0x16E681, ("lea", "rcx, [rdi + 0x12c0]")), (0x16E6A3, ("mov", "qword ptr [rbp - 0x28], rcx")), (0x16E6DA, ("mov", "rbx, qword ptr [rbp - 0x28]")),
               (0x16E8A2, ("movsxd", "rax, dword ptr [rbx + 0x9d0]")), (0x16E8A9, ("lea", "rcx, [rax + rax*8]")), (0x16E8B4, ("add", "rcx, rcx")),
               (0x16E8B7, ("movups", "xmm0, xmmword ptr [rbx + rcx*8 + 0x780]"))]),
      "the copy's source is [inst + 0x12C0 + 0x780 + idx*0x90]")
check("T3", A([(0x16FB83, ("lea", "r9, [rcx + 0x880]")), (0x16FB93, ("lea", "r9, [r9 + 0x38]")), (0x16FB9D, ("imul", "edx, dword ptr [rcx + 0xe80]")),
               (0x16FBAF, ("mov", "dword ptr [r9 - 0x38], edx")), (0x16FBB3, ("cmp", "r8d, 0x10")), (0x16FBB9, ("mov", "dword ptr [rcx + 0xc00], r10d")),
               (0x16FBC0, ("mov", "dword ptr [rcx + 0xce0], r10d")), (0x16FBC7, ("mov", "dword ptr [rcx + 0xc38], 4")), (0x16FBD1, ("mov", "dword ptr [rcx + 0xd18], 4")),
               (0x16FBDB, ("mov", "eax, dword ptr [rcx + 0xe94]")), (0x16FBE4, ("mov", "dword ptr [rcx + 0xc70], eax")), (0x16FBEA, ("mov", "dword ptr [rcx + 0xd50], eax")),
               (0x16FBFD, ("mov", "dword ptr [rcx + 0xca8], eax")), (0x16FC03, ("mov", "dword ptr [rcx + 0xd88], eax"))])
      and 0x880 + 16 * 0x38 == 0xC00 and 0x880 + 23 * 0x38 == 0xD88,
      "0016FB80: 24 block records of 0x38 from +0x880 (16 luma from [+0xE80], 8 chroma from [+0xE94])")
check("T4", A([(0x16E252, ("lea", "rcx, [rbx + 0x12c0]")), (0x16E259, ("call", "0x172750")), (0x172762, ("lea", "rbx, [rcx + 0x780]")),
               (0x172775, ("cmp", "dword ptr [rbx + 0x60], 0")), (0x17277B, ("mov", "rcx, qword ptr [rbx + 0x58]")), (0x172784, ("mov", "rcx, qword ptr [rcx - 8]")),
               (0x172790, ("mov", "r8d, 0x90")), (0x172799, ("call", "0x861ec0")), (0x17279E, ("add", "rbx, 0x90")),
               (0x1727AB, ("lea", "rbx, [rdi + 0x9e0]")), (0x1727DF, ("lea", "rbx, [rdi + 0xa70]")), (0x17281D, ("lea", "rbx, [rdi + 0xb00]"))]),
      "00172750(inst + 0x12C0): 0x90 records at +0x780 ... free [[rec+0x58]-8] when [rec+0x60] > 0, then zero the record")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/vp8-macroblock-decoder/vp8_mbd_carve.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
EV = lambda tag: "CARVED 2026-09-28 (OPUS, %s %s). %s" % (REC, tag, EXE)
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
MBD, BLK, FB, INST = "Vp8MacroblockDecoder", "Vp8BlockDescriptor", "Vp8FrameBuffer", "Vp8DecoderInstance"
def r(t, o, sz, nm, ct, mean, rd, ev, w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev]
NEW_TYPES = [
    [MBD, "0x12A0", "23-Third-Party-Libraries", "one embedded at Vp8DecoderInstance +0x0000, and one per decoder thread in the array at [instance+0x4410] (count [instance+0x4390]); the same routine 0016FB80 is applied to both",
     "EMBEDDED in Vp8DecoderInstance; the thread records' allocation is not read here", "none read", "none - part of its owner", "TYPE RESOLVED", "PROVEN", "L1",
     EV("T1 T3") + ". Extent from the thread-record stride 0x12A0 (0016E94A); the instance's next structure starts at +0x12C0.", "23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md", "EMBED Vp8DecoderInstance +0x0000"],
    [BLK, "0x38", "23-Third-Party-Libraries", "24 per Vp8MacroblockDecoder, from +0x880 (16 luma, then 4 + 4 chroma)", "EMBEDDED in Vp8MacroblockDecoder", "0016FB80 writes each record's +0x00", "none - part of its owner",
     "TYPE RESOLVED", "PROVEN", "L1", EV("T3") + ". Stride 0x38 from 0016FB93 (lea r9, [r9 + 0x38]) and the chroma stores at +0xC00 + k*0x38.", "23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md", "EMBED Vp8MacroblockDecoder +0x0880 stride=0x38"],
    [FB, "0x90", "23-Third-Party-Libraries", "records at Vp8DecoderInstance +0x12C0 + 0x780 (stride 0x90) and at +0x12C0 + 0x9E0 / 0xA70 / 0xB00 ...; one copied into each Vp8MacroblockDecoder at +0xE70",
     "EMBEDDED in Vp8DecoderInstance (and copied by value)", "not read here", "00172750 frees [[+0x58] - 8] when [+0x60] > 0, then zeroes the record (0x90 bytes)", "TYPE RESOLVED", "PROVEN", "L1",
     EV("T2 T4"), "23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md", ""]]
def mbd_rows(moved):
    rows = [r(MBD, 0, 0x880, "unobservedSpan0000", "u8[2176]", "not read by 0016FB80 or the thread-loop copy", U, EV("T1 T3")),
            r(MBD, 0x880, 0x540, "blocks", "Vp8BlockDescriptor[24]", "24 block records of 0x38: 0016FB80 writes each one's +0x00 offset (16 luma from the luma stride, 8 chroma from the chroma stride)", P, EV("T3")),
            r(MBD, 0xDC0, 0xB0, "unobservedSpanDC0", "u8[176]", "after the 24 block records; not read here", U, EV("T3")),
            r(MBD, 0xE70, 0x90, "dstFrameBuffer", FB, "a by-value copy of one of the instance's frame-buffer records (vp8_decode copies [inst + 0x12C0 + 0x780 + idx*0x90] here for each thread record); 0016FB80 reads its strides at +0xE80 / +0xE94", P, EV("T1 T2 T3")),
            r(MBD, 0xF00, 0x84, "unobservedSpanF00", "u8[132]", "not read here", U, EV("T1"))]
    for c in moved:
        rows.append([MBD, "0x%04X" % int(c[1], 16)] + c[2:8] + [c[8] + " || MOVED 2026-09-28 (OPUS, %s): the row was Vp8DecoderInstance +%s; the offset is the same inside the embedded Vp8MacroblockDecoder" % (REC, c[1])])
    rows.append(r(MBD, 0xF94, 0x30C, "unobservedSpanF94", "u8[780]", "not read by the bodies read here", U, EV("T1")))
    return rows
BLK_ROWS = [r(BLK, 0, 4, "offset", "uint32", "the block's byte offset in its plane: ((i>>2) * stride + (i&3)) * 4 for luma block i, 0 / 4 / stride*4 / stride*4 + 4 for the chroma blocks (0016FB80)", P, EV("T3")),
            r(BLK, 4, 0x34, "unobservedSpan0004", "u8[52]", "not read here", U, EV("T3"))]
FB_ROWS = [r(FB, 0, 0x10, "unobservedSpan0000", "u8[16]", "not read here", U, EV("T3 T4")),
           r(FB, 0x10, 4, "yStride", "uint32", "the luma stride 0016FB80 multiplies block rows by (read at the Vp8MacroblockDecoder's +0xE80)", P, EV("T3")),
           r(FB, 0x14, 0x10, "unobservedSpan0014", "u8[16]", "not read here", U, EV("T3")),
           r(FB, 0x24, 4, "uvStride", "uint32", "the chroma stride 0016FB80 reads (at the Vp8MacroblockDecoder's +0xE94)", P, EV("T3")),
           r(FB, 0x28, 0x30, "unobservedSpan0028", "u8[48]", "not read here", U, EV("T4")),
           r(FB, 0x58, 8, "bufferAlloc", "void*", "the record's owned allocation: 00172750 frees [ptr - 8] (the vpx_memalign original pointer) when bufferAllocSize is above 0 (a signed test)", P, EV("T4")),
           r(FB, 0x60, 4, "bufferAllocSize", "uint32", "tested above 0 (cmp / jle) before bufferAlloc is freed; 00172750 then zeroes the whole record", P, EV("T4")),
           r(FB, 0x64, 0x2C, "unobservedSpan0064", "u8[44]", "not read here", U, EV("T4"))]
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    eol = fl[1][len(fl[1].rstrip("\r\n")):]
    moved = [cells(l) for l in fl if cells(l)[0] == INST and cells(l)[1] in ("0xF84", "0xF88", "0xF8C", "0xF90")]
    assert len(moved) == 4, moved
    out = []; placed = False
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == INST and c[1] in ("0xF84", "0xF88", "0xF8C", "0xF90"): continue
        if c[0] == INST and c[1] == "0x00" and c[3] == "unobservedSpan0000":
            out.append("\t".join([INST, "0x00", "4768", "macroblockDecoder", MBD, "the embedded per-row decoder record (0x12A0), laid out like the per-thread records at [+0x4410]: vp8_decode hands this +0x0000 to the same routine 0016FB80 it runs on each thread record. Replaces unobservedSpan0000 and absorbs the former +0xF84..+0xF93 rows",
                                  "TYPE RESOLVED", "PROVEN", EV("T1 T3") + ". was unobservedSpan0000 uint8[3972] and the rows +0xF84..+0xF90 (now Vp8MacroblockDecoder rows)"]) + e); continue
        if c[0] == INST and c[1] == "0xF94" and c[3] == "unobservedSpan0F94":
            out.append("\t".join([INST, "0x12A0", "32", "unobservedSpan12A0", "u8[32]", "between the embedded Vp8MacroblockDecoder and the structure at +0x12C0 (the base vp8_decode and vp8_destroy use for the frame-buffer records); not read here", U[0], U[1], EV("T1 T2 T4") + ". was part of unobservedSpan0F94 uint8[2724]"]) + e)
            out.append("\t".join([INST, "0x12C0", "1912", "unobservedSpan12C0", "u8[1912]", "the start of the structure vp8_decode and vp8_destroy address as inst + 0x12C0; its frame-buffer records (Vp8FrameBuffer) begin at +0x12C0 + 0x780 = +0x1A40. Not carved here", U[0], U[1], EV("T2 T4") + ". was part of unobservedSpan0F94 uint8[2724]"]) + e)
            continue
        out.append(l)
        if not placed and c[0] == INST and c[1] == "0x1A38":
            pass
    # append the three new types' rows after the last Vp8DecoderInstance row
    idx = max(i for i, l in enumerate(out) if cells(l)[0] == INST)
    new = mbd_rows(moved) + BLK_ROWS + FB_ROWS
    out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in new]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    ti = max(i for i, l in enumerate(tl) if cells(l)[0] == INST)
    if not any(cells(l)[0] == MBD for l in tl):
        tl[ti + 1:ti + 1] = ["\t".join(x) + te for x in NEW_TYPES]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def tiles(t): return sum(int(c[2]) for c in F if c[0] == t) == int(T[t][1], 16) if t in T else False
inst = {c[1]: c for c in F if c[0] == INST}
ok = (all(t in T for t in (MBD, BLK, FB)) and all(tiles(t) for t in (MBD, BLK, FB, INST))
      and inst.get("0x00", [0, 0, 0, 0, ""])[4] == MBD and "0xF84" not in inst and "0x12A0" in inst and "0x12C0" in inst
      and [c[3] for c in F if c[0] == MBD and c[1] in ("0x0F84", "0x0F88", "0x0F8C", "0x0F90")] == ["mbToLeftEdge", "mbToRightEdge", "mbToTopEdge", "mbToBottomEdge"])
check("S", ok, "Vp8DecoderInstance +0x0000 is an embedded Vp8MacroblockDecoder (0x12A0); the three new types tile; the four edge rows moved")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
