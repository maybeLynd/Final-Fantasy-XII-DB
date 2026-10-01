"""vp8_mb_rows.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
The per-frame setup 00175CA0 (libvpx init_frame(pbi)) and the macroblock row loop 00175070 (decode_mb_rows(pbi)), which
between them read or write the remaining named fields of the embedded Vp8MacroblockDecoder, the frame-context interior and
the frame-buffer plane fields.

  C  receivers: 00175EF0 calls 00175CA0 with rcx = r12 = pbi (00176262) and 00175070 with rcx = rbx = pbi (001773E4);
     vp8_decode_frame.py D proves both registers hold pbi there
  D  in 00175CA0 rcx is never written; in 00175070 rbx is written once (00175070 + 0x47: rbx = rcx), rdi once
     (rdi = rcx + 0x12C0) and rsi = [rbx + 0x12A0] (decFbRef[0]) is not rewritten before the last T site
  I  00175CA0 on a key frame (frameType == 0): frameContext +0x433 (pbi + 0x34B5) gets 16 + 16 + 4 + 2 = 38 bytes; +0x9
     gets 4, +0xD 3 (word + byte), +0x10 3; +0x13 gets 8 x 0x80 + 0x20 = 1056 bytes from a table; the macroblock decoder's
     segmentFeatureData, mbSegmentAbsDelta, the dwords at +0xF75 and +0xF7D are cleared; refreshGoldenFrame = 1, the qword at
     +0x2BF4 = 1 (refreshAltRefFrame 1, copyBufferToGf 0), copyBufferToArf = 0, the qword at +0x2C0C = 0 (both sign-bias
     ints). On an inter frame: +0x1E88 == 0 selects one set of four function pointers for the macroblock decoder's
     +0xF98 / +0xFA0 / +0xFA8 / +0xFB0, otherwise another; then if decodedKeyFrame and [pbi + 0x4448] and not ecActive,
     ecActive = 1. Always: +0xF58 = pbi + 0x2C20; +0xF00 = modeInfo and its first byte = 0; +0xF0C = frameType;
     +0xF08 = modeInfoStride (+0x1E7C); +0xDD8 = -1, or -8 when [pbi + 0x1E8C] != 0; corrupted = 0
  M  00175070 per row: +0xF10 (0 on the first row, 1 after each), currentBc = pbi + (0x15C + i) * 0x30 = partitionBoolDecoders[i];
     +0xF50 = aboveContext; the 9 bytes at [+0xF58] cleared; +0xF14 = 0 then 1 after each macroblock; +0xF8C / +0xF90 /
     +0xF84 / +0xF88 the top / bottom / left / right edge distances in 1/8 pixels ((rows or cols - 1 - i) << 7); three plane
     pointers at +0xF18 / +0xF20 / +0xF28, each minus the plane stride, and +0xF30 / +0xF38 / +0xF40 = those minus 1 (one
     column left); +0xF48 / +0xF4C = the luma / chroma strides of dstFrameBuffer (+0xE80 / +0xE94); per macroblock the
     plane pointers advance 16 / 8 / 8, +0xF00 by 0x4C (one Vp8ModeInfo) and +0xF50 by 9; corrupted |= each macroblock's
     and the bool decoder's error; dstFrameBuffer's plane pointers are at +0xEA8 / +0xEB0 / +0xEB8
  T  00175070 before the rows: for decFbRef[0] (rsi) three memsets of 0x7F: at [rsi + 0x38] - [rsi + 0x10] - 1 for
     [rsi] + 5 bytes, and at [rsi + 0x40] / [rsi + 0x48] - [rsi + 0x24] - 1 for [rsi + 0x14] + 5 bytes - the border row
     above each plane. So Vp8FrameBuffer +0x00 / +0x14 are the luma / chroma widths and +0x38 / +0x40 / +0x48 the plane pointers
  P  REGRESSION (FAILS before): the rows are in the store; Vp8FrameContext exists; all touched types tile
Names follow libvpx vocabulary; a field's meaning is only what the cited instructions do with it.
Usage: python vp8_mb_rows.py [--patch]
"""
import hashlib, os, re, sys
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
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
SITES = {
    'C': [(0x17625A, 0x176262, 0x17625A, ('mov', 'rcx, r12')), (0x17625A, 0x176262, 0x17625D, ('call', '0x175ca0')), (0x1773E1, 0x1773E9, 0x1773E1, ('mov', 'rcx, rbx')), (0x1773E1, 0x1773E9, 0x1773E4, ('call', '0x175070'))],
    'I': [(0x175CA0, 0x175EE1, 0x175CA3, ('cmp', 'dword ptr [rcx + 0x1e64], r9d')), (0x175CA0, 0x175EE1, 0x175CC2, ('movups', 'xmmword ptr [rcx + 0x34b5], xmm0')), (0x175CA0, 0x175EE1, 0x175CD0, ('movups', 'xmmword ptr [rcx + 0x34c5], xmm1')), (0x175CA0, 0x175EE1, 0x175CDD, ('mov', 'dword ptr [rcx + 0x34d5], eax')), (0x175CA0, 0x175EE1, 0x175CEA, ('mov', 'word ptr [rcx + 0x34d9], ax')), (0x175CA0, 0x175EE1, 0x175CF7, ('mov', 'dword ptr [rcx + 0x308b], eax')), (0x175CA0, 0x175EE1, 0x175D04, ('mov', 'word ptr [rcx + 0x308f], ax')), (0x175CA0, 0x175EE1, 0x175D12, ('mov', 'byte ptr [rcx + 0x3091], al')), (0x175CA0, 0x175EE1, 0x175D1F, ('mov', 'word ptr [rcx + 0x3092], ax')), (0x175CA0, 0x175EE1, 0x175D2D, ('mov', 'byte ptr [rcx + 0x3094], al')), (0x175CA0, 0x175EE1, 0x175D33, ('lea', 'rax, [rcx + 0x3095]')), (0x175CA0, 0x175EE1, 0x175D8D, ('sub', 'r8, 1')), (0x175CA0, 0x175EE1, 0x175D96, ('movups', 'xmmword ptr [rax], xmm0')), (0x175CA0, 0x175EE1, 0x175D9D, ('movups', 'xmmword ptr [rax + 0x10], xmm1')), (0x175CA0, 0x175EE1, 0x175DA3, ('mov', 'qword ptr [rcx + 0xf67], rax')), (0x175CA0, 0x175EE1, 0x175DAA, ('mov', 'byte ptr [rcx + 0xf63], al')), (0x175CA0, 0x175EE1, 0x175DB0, ('mov', 'dword ptr [rcx + 0xf75], eax')), (0x175CA0, 0x175EE1, 0x175DB6, ('mov', 'dword ptr [rcx + 0xf7d], eax')), (0x175CA0, 0x175EE1, 0x175DBC, ('mov', 'dword ptr [rcx + 0x2bf0], 1')), (0x175CA0, 0x175EE1, 0x175DC6, ('mov', 'qword ptr [rcx + 0x2bf4], 1')), (0x175CA0, 0x175EE1, 0x175DD1, ('mov', 'dword ptr [rcx + 0x2bfc], r9d')), (0x175CA0, 0x175EE1, 0x175DD8, ('mov', 'qword ptr [rcx + 0x2c0c], r9')), (0x175CA0, 0x175EE1, 0x175DE4, ('cmp', 'dword ptr [rcx + 0x1e88], r9d')), (0x175CA0, 0x175EE1, 0x175DF4, ('mov', 'qword ptr [rcx + 0xf98], rax')), (0x175CA0, 0x175EE1, 0x175E02, ('mov', 'qword ptr [rcx + 0xfa0], rax')), (0x175CA0, 0x175EE1, 0x175E10, ('mov', 'qword ptr [rcx + 0xfa8], rax')), (0x175CA0, 0x175EE1, 0x175E27, ('mov', 'qword ptr [rcx + 0xf98], rax')), (0x175CA0, 0x175EE1, 0x175E35, ('mov', 'qword ptr [rcx + 0xfa0], rax')), (0x175CA0, 0x175EE1, 0x175E43, ('mov', 'qword ptr [rcx + 0xfa8], rax')), (0x175CA0, 0x175EE1, 0x175E51, ('mov', 'qword ptr [rcx + 0xfb0], rax')), (0x175CA0, 0x175EE1, 0x175E58, ('cmp', 'dword ptr [rcx + 0x4450], r9d')), (0x175CA0, 0x175EE1, 0x175E61, ('cmp', 'dword ptr [rcx + 0x4448], r9d')), (0x175CA0, 0x175EE1, 0x175E6A, ('cmp', 'dword ptr [rcx + 0x444c], r9d')), (0x175CA0, 0x175EE1, 0x175E73, ('mov', 'dword ptr [rcx + 0x444c], 1')), (0x175CA0, 0x175EE1, 0x175E7D, ('lea', 'rax, [rcx + 0x2c20]')), (0x175CA0, 0x175EE1, 0x175E84, ('mov', 'qword ptr [rcx + 0xf58], rax')), (0x175CA0, 0x175EE1, 0x175E8B, ('mov', 'rdx, qword ptr [rcx + 0x1eb0]')), (0x175CA0, 0x175EE1, 0x175E92, ('mov', 'qword ptr [rcx + 0xf00], rdx')), (0x175CA0, 0x175EE1, 0x175E99, ('mov', 'eax, dword ptr [rcx + 0x1e64]')), (0x175CA0, 0x175EE1, 0x175E9F, ('mov', 'dword ptr [rcx + 0xf0c], eax')), (0x175CA0, 0x175EE1, 0x175EA5, ('mov', 'byte ptr [rdx], r9b')), (0x175CA0, 0x175EE1, 0x175EAD, ('mov', 'eax, dword ptr [rcx + 0x1e7c]')), (0x175CA0, 0x175EE1, 0x175EB3, ('mov', 'dword ptr [rcx + 0xf08], eax')), (0x175CA0, 0x175EE1, 0x175EB9, ('mov', 'dword ptr [rcx + 0xdd8], 0xffffffff')), (0x175CA0, 0x175EE1, 0x175EC9, ('mov', 'dword ptr [rcx + 0xfc0], r9d')), (0x175CA0, 0x175EE1, 0x175ED0, ('cmp', 'dword ptr [rcx + 0x1e8c], r9d')), (0x175CA0, 0x175EE1, 0x175ED7, ('cmovne', 'eax, edx')), (0x175CA0, 0x175EE1, 0x175EDA, ('mov', 'dword ptr [rcx + 0xdd8], eax'))],
    'M': [(0x175070, 0x175650, 0x1750A1, ('mov', 'rax, qword ptr [rcx + 0xf00]')), (0x175070, 0x175650, 0x1750A8, ('lea', 'rdi, [rcx + 0x12c0]')), (0x175070, 0x175650, 0x1750B7, ('mov', 'rbx, rcx')), (0x175070, 0x175650, 0x1750D3, ('mov', 'rsi, qword ptr [rbx + 0x12a0]')), (0x175070, 0x175650, 0x1751C9, ('mov', 'dword ptr [rbx + 0xf10], edx')), (0x175070, 0x175650, 0x1752AD, ('add', 'rax, 0x15c')), (0x175070, 0x175650, 0x1752B3, ('lea', 'rcx, [rax + rax*2]')), (0x175070, 0x175650, 0x1752B7, ('shl', 'rcx, 4')), (0x175070, 0x175650, 0x1752BB, ('add', 'rcx, rbx')), (0x175070, 0x175650, 0x1752C1, ('mov', 'qword ptr [rbx + 0xfb8], rcx')), (0x175070, 0x175650, 0x1752D4, ('mov', 'rax, qword ptr [rdi + 0x1958]')), (0x175070, 0x175650, 0x1752DD, ('mov', 'qword ptr [rbx + 0xf50], rax')), (0x175070, 0x175650, 0x1752E7, ('mov', 'rax, qword ptr [rbx + 0xf58]')), (0x175070, 0x175650, 0x1752F1, ('mov', 'qword ptr [rax], rcx')), (0x175070, 0x175650, 0x1752F4, ('mov', 'byte ptr [rax + 8], cl')), (0x175070, 0x175650, 0x1752F7, ('mov', 'dword ptr [rbx + 0xf14], r11d')), (0x175070, 0x175650, 0x1752FE, ('mov', 'dword ptr [rbx + 0xf8c], r9d')), (0x175070, 0x175650, 0x175305, ('mov', 'eax, dword ptr [rdi + 0xbb4]')), (0x175070, 0x175650, 0x175313, ('shl', 'eax, 7')), (0x175070, 0x175650, 0x175316, ('mov', 'dword ptr [rbx + 0xf90], eax')), (0x175070, 0x175650, 0x175327, ('mov', 'qword ptr [rbx + 0xf18], rax')), (0x175070, 0x175650, 0x175339, ('mov', 'qword ptr [rbx + 0xf20], rax')), (0x175070, 0x175650, 0x17534B, ('mov', 'qword ptr [rbx + 0xf28], rax')), (0x175070, 0x175650, 0x17536B, ('mov', 'qword ptr [rbx + 0xf30], rax')), (0x175070, 0x175650, 0x175376, ('mov', 'qword ptr [rbx + 0xf38], rax')), (0x175070, 0x175650, 0x175388, ('mov', 'qword ptr [rbx + 0xf40], rax')), (0x175070, 0x175650, 0x17538F, ('movsxd', 'rax, dword ptr [rbx + 0xe80]')), (0x175070, 0x175650, 0x1753A0, ('mov', 'qword ptr [rbx + 0xf18], rcx')), (0x175070, 0x175650, 0x1753AC, ('movsxd', 'rax, dword ptr [rbx + 0xe94]')), (0x175070, 0x175650, 0x1753B6, ('mov', 'qword ptr [rbx + 0xf20], rdx')), (0x175070, 0x175650, 0x1753C7, ('mov', 'qword ptr [rbx + 0xf28], r8')), (0x175070, 0x175650, 0x1753D4, ('mov', 'dword ptr [rbx + 0xf48], eax')), (0x175070, 0x175650, 0x1753E0, ('mov', 'dword ptr [rbx + 0xf4c], eax')), (0x175070, 0x175650, 0x1754A7, ('mov', 'dword ptr [rbx + 0xf84], ebp')), (0x175070, 0x175650, 0x1754AD, ('mov', 'eax, dword ptr [rdi + 0xbb8]')), (0x175070, 0x175650, 0x1754C0, ('mov', 'dword ptr [rbx + 0xf88], eax')), (0x175070, 0x175650, 0x1754CA, ('mov', 'qword ptr [rbx + 0xea8], rax')), (0x175070, 0x175650, 0x175569, ('or', 'dword ptr [rbx + 0xfc0], ecx')), (0x175070, 0x175650, 0x17557E, ('mov', 'dword ptr [rbx + 0xf14], 1')), (0x175070, 0x175650, 0x17559E, ('or', 'dword ptr [rbx + 0xfc0], eax')), (0x175070, 0x175650, 0x1755A8, ('add', 'qword ptr [rbx + 0xf18], 0x10')), (0x175070, 0x175650, 0x1755B2, ('add', 'qword ptr [rbx + 0xf20], 8')), (0x175070, 0x175650, 0x1755BD, ('add', 'qword ptr [rbx + 0xf28], 8')), (0x175070, 0x175650, 0x1755C5, ('add', 'qword ptr [rbx + 0xf30], 0x10')), (0x175070, 0x175650, 0x1755CD, ('add', 'qword ptr [rbx + 0xf38], 8')), (0x175070, 0x175650, 0x1755D5, ('add', 'qword ptr [rbx + 0xf40], 8')), (0x175070, 0x175650, 0x1755DD, ('add', 'qword ptr [rbx + 0xf00], 0x4c')), (0x175070, 0x175650, 0x1755E5, ('add', 'qword ptr [rbx + 0xf50], 9')), (0x175070, 0x175650, 0x1755ED, ('cmp', 'esi, dword ptr [rdi + 0xbb8]')), (0x175070, 0x175650, 0x1755FE, ('mov', 'r9, qword ptr [rbx + 0xeb8]')), (0x175070, 0x175650, 0x175605, ('mov', 'r8, qword ptr [rbx + 0xeb0]')), (0x175070, 0x175650, 0x175610, ('mov', 'rdx, qword ptr [rbx + 0xea8]')), (0x175070, 0x175650, 0x17562F, ('add', 'qword ptr [rbx + 0xf00], 0x4c')), (0x175070, 0x175650, 0x175637, ('mov', 'dword ptr [rbx + 0xf10], 1'))],
    'T': [(0x175070, 0x175650, 0x1751B4, ('mov', 'rax, qword ptr [rsi + 0x48]')), (0x175070, 0x175650, 0x1751EB, ('mov', 'eax, dword ptr [rsi]')), (0x175070, 0x175650, 0x1751F2, ('mov', 'rcx, qword ptr [rsi + 0x38]')), (0x175070, 0x175650, 0x1751F6, ('add', 'eax, 5')), (0x175070, 0x175650, 0x1751FC, ('movsxd', 'rax, dword ptr [rsi + 0x10]')), (0x175070, 0x175650, 0x175200, ('sub', 'rcx, rax')), (0x175070, 0x175650, 0x175203, ('dec', 'rcx')), (0x175070, 0x175650, 0x175206, ('call', '0x861ec0')), (0x175070, 0x175650, 0x17520B, ('mov', 'eax, dword ptr [rsi + 0x14]')), (0x175070, 0x175650, 0x175213, ('mov', 'rcx, qword ptr [rsi + 0x40]')), (0x175070, 0x175650, 0x17521D, ('movsxd', 'rax, dword ptr [rsi + 0x24]')), (0x175070, 0x175650, 0x175227, ('call', '0x861ec0')), (0x175070, 0x175650, 0x17522C, ('mov', 'eax, dword ptr [rsi + 0x14]')), (0x175070, 0x175650, 0x175234, ('mov', 'rcx, qword ptr [rsi + 0x48]')), (0x175070, 0x175650, 0x17523E, ('movsxd', 'rax, dword ptr [rsi + 0x24]')), (0x175070, 0x175650, 0x175248, ('call', '0x861ec0'))],
}
CACHE = {}
def listing(lo, hi):
    if (lo, hi) not in CACHE: CACHE[(lo, hi)] = list(cs.disasm(d[off(lo):off(hi)], lo))
    return CACHE[(lo, hi)]
def match(tag): return all(any(x.address == a and (x.mnemonic, x.op_str) == v for x in listing(lo, hi)) for lo, hi, a, v in SITES[tag])
def writes(lo, hi, reg, until=None):
    out = []
    for x in listing(lo, hi):
        if until and x.address >= until: break
        if x.mnemonic in ("push", "pop"): continue
        _, w = x.regs_access()
        if reg in {x.reg_name(r) for r in w} or ("e" + reg[1:] if reg[0] == "r" and len(reg) == 3 else "") in {x.reg_name(r) for r in w}: out.append(x.address)
    return out
check("C", match("C"), "00175EF0 calls init_frame with rcx = r12 and decode_mb_rows with rcx = rbx")
check("D", writes(0x175CA0, 0x175EE1, "rcx") == [] and writes(0x175070, 0x175650, "rbx") == [0x1750B7] and writes(0x175070, 0x175650, "rdi") == [0x1750A8]
      and writes(0x175070, 0x175650, "rsi", until=0x175249) == [0x1750D3],
      "rcx unwritten in 00175CA0; rbx / rdi written once in 00175070 (pbi / pbi + 0x12C0); rsi = decFbRef[0] through the T sites")
check("I", match("I"), "init_frame: key-frame context defaults and resets, the inter-frame filter pointers, ecActive, and the per-frame macroblock-decoder fields")
check("M", match("M"), "decode_mb_rows: availability flags, currentBc, contexts, edges, plane pointers and strides, per-macroblock advances")
check("T", match("T"), "decode_mb_rows: the 0x7F border rows above the three planes of decFbRef[0]")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/vp8-macroblock-decoder/vp8_mb_rows.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
INST, MBD, FB, FC = "Vp8DecoderInstance", "Vp8MacroblockDecoder", "Vp8FrameBuffer", "Vp8FrameContext"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "READ 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was="-", w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
NR = "not read by 00175CA0 or 00175070"
CUT = {
 (INST, 0x1E84): lambda w: [r(INST, 0x1E84, 4, "unobservedSpan1E84", "u8[4]", NR, U, "I", w),
                            r(INST, 0x1E88, 4, "useBilinearMcFilter", "int32", "common.use_bilinear_mc_filter: 0 selects the first set of the macroblock decoder's four prediction function pointers, non-zero the second (00175CA0)", P, "I", w),
                            r(INST, 0x1E8C, 4, "fullPixel", "int32", "common.full_pixel: non-zero makes 00175CA0 set the macroblock decoder's fullpixelMask to -8 instead of -1", P, "I", w)],
 (INST, 0x2C20): lambda w: [r(INST, 0x2C20, 9, "leftContext", "u8[9]", "common.left_context: 00175CA0 points the macroblock decoder's leftContext here; 00175070 clears its 9 bytes at each row start", P, "I M", w)],
 (INST, 0x4448): lambda w: [r(INST, 0x4448, 4, "ecEnabled", "int32", "error concealment enabled: with decodedKeyFrame set and ecActive clear, 00175CA0 sets ecActive on an inter frame", P, "I", w)],
 (MBD, 0x0DD8): lambda w: [r(MBD, 0x0DD8, 4, "fullpixelMask", "int32", "-1, or -8 (0xFFFFFFF8) when fullPixel is set (00175CA0)", P, "I", w),
                           r(MBD, 0x0DDC, 4, "unobservedSpanDDC", "u8[4]", NR, U, "I", w)],
 (MBD, 0x0F08): lambda w: [r(MBD, 0x0F08, 4, "modeInfoStride", "int32", "copied from the instance's modeInfoStride each frame (00175CA0)", P, "I", w),
                           r(MBD, 0x0F0C, 4, "frameType", "int32", "copied from the instance's frameType each frame (00175CA0)", P, "I", w),
                           r(MBD, 0x0F10, 4, "upAvailable", "int32", "0 on the first macroblock row, 1 after (00175070)", P, "M", w),
                           r(MBD, 0x0F14, 4, "leftAvailable", "int32", "0 at each row start, 1 after each macroblock (00175070)", P, "M", w),
                           r(MBD, 0x0F18, 24, "reconAbove", "uint8*[3]", "per plane (Y, U, V), the reconstruction row above the current macroblock: the destination plane pointer minus its stride, advanced 16 / 8 / 8 per macroblock (00175070)", P, "M", w),
                           r(MBD, 0x0F30, 24, "reconLeft", "uint8*[3]", "per plane, the column left of the current macroblock (reconAbove's first value minus 1), advanced 16 / 8 / 8 (00175070)", P, "M", w),
                           r(MBD, 0x0F48, 8, "reconLeftStride", "int32[2]", "the luma and chroma strides of dstFrameBuffer (00175070)", P, "M", w),
                           r(MBD, 0x0F50, 8, "aboveContext", "uint8*", "the instance's aboveContext at each row start, advanced 9 bytes per macroblock (00175070)", P, "M", w),
                           r(MBD, 0x0F58, 8, "leftContext", "uint8*", "points at the instance's leftContext (00175CA0); 00175070 clears 9 bytes through it per row", P, "I M", w)],
 (MBD, 0x0F71): lambda w: [r(MBD, 0x0F71, 4, "unobservedSpanF71", "u8[4]", NR, U, "I", w),
                           r(MBD, 0x0F75, 4, "refLfDeltas", "int8[4]", "the per-reference loop-filter deltas: cleared on a key frame (00175CA0); the frame header updates them bytewise (00175EF0)", P, "I", w),
                           r(MBD, 0x0F79, 4, "unobservedSpanF79", "u8[4]", NR, U, "I", w),
                           r(MBD, 0x0F7D, 4, "modeLfDeltas", "int8[4]", "the per-mode loop-filter deltas: cleared on a key frame (00175CA0); updated bytewise by the frame header", P, "I", w),
                           r(MBD, 0x0F81, 3, "unobservedSpanF81", "u8[3]", NR, U, "I", w)],
 (MBD, 0x0F94): lambda w: [r(MBD, 0x0F94, 4, "unobservedSpanF94", "u8[4]", NR, U, "I", w),
                           r(MBD, 0x0F98, 8, "subpixelPredict", "void*", "a prediction function pointer, one of two set per inter frame by useBilinearMcFilter (00175CA0)", P, "I", w),
                           r(MBD, 0x0FA0, 8, "subpixelPredict8x4", "void*", "as subpixelPredict, the second of the four", P, "I", w),
                           r(MBD, 0x0FA8, 8, "subpixelPredict8x8", "void*", "as subpixelPredict, the third of the four", P, "I", w),
                           r(MBD, 0x0FB0, 8, "subpixelPredict16x16", "void*", "as subpixelPredict, the fourth of the four", P, "I", w)],
 (FB, 0x0000): lambda w: [r(FB, 0x0000, 4, "yWidth", "int32", "the luma width: 00175070's border memset above the luma plane is yWidth + 5 bytes", P, "T", w),
                          r(FB, 0x0004, 12, "unobservedSpan0004", "u8[12]", NR, U, "T", w)],
 (FB, 0x0014): lambda w: [r(FB, 0x0014, 4, "uvWidth", "int32", "the chroma width: the two chroma border memsets are uvWidth + 5 bytes", P, "T", w),
                          r(FB, 0x0018, 12, "unobservedSpan0018", "u8[12]", NR, U, "T", w)],
 (FB, 0x0028): lambda w: [r(FB, 0x0028, 16, "unobservedSpan0028", "u8[16]", NR, U, "T", w),
                          r(FB, 0x0038, 8, "yBuffer", "uint8*", "the luma plane: the border memset starts at yBuffer - yStride - 1; decode_mb_rows builds its reconstruction pointers from it", P, "T M", w),
                          r(FB, 0x0040, 8, "uBuffer", "uint8*", "the first chroma plane (border memset at uBuffer - uvStride - 1)", P, "T M", w),
                          r(FB, 0x0048, 8, "vBuffer", "uint8*", "the second chroma plane (border memset at vBuffer - uvStride - 1)", P, "T M", w),
                          r(FB, 0x0050, 8, "unobservedSpan0050", "u8[8]", NR, U, "T", w)]}
FCROWS = [r(FC, 0x000, 9, "unobservedSpan0000", "u8[9]", "not written by 00175CA0", U, "I"),
          r(FC, 0x009, 4, "ymodeProb", "uint8[4]", "reset from a table on a key frame (00175CA0, a dword store)", P, "I"),
          r(FC, 0x00D, 3, "uvModeProb", "uint8[3]", "reset from a table on a key frame (a word and a byte store)", P, "I"),
          r(FC, 0x010, 3, "subMvRefProb", "uint8[3]", "reset from a table on a key frame (a word and a byte store)", P, "I"),
          r(FC, 0x013, 1056, "coefProbs", "uint8[1056]", "the coefficient probabilities (libvpx [4][8][3][11]): reset on a key frame, 8 x 0x80 + 0x20 bytes from a table", P, "I"),
          r(FC, 0x433, 38, "mvc", "uint8[38]", "the two motion-vector contexts (libvpx 2 x 19): reset on a key frame, 16 + 16 + 4 + 2 bytes", P, "I")]
NEWT = [FC, "0x459", "23-Third-Party-Libraries", "two at Vp8DecoderInstance: lastFrameContext +0x2C29 and frameContext +0x3082 (libvpx FRAME_CONTEXT)", "EMBEDDED in Vp8DecoderInstance",
        "00175CA0 resets frameContext's tables on a key frame", "none - part of its owner", P[0], P[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s I). Extent 0x459 from vp8_decode_frame.py's 8 x 0x80 + 0x59 copy; the interior from 00175CA0's key-frame resets, which end at +0x459. %s" % (REC, EXE),
        "23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md", "EMBED Vp8DecoderInstance +0x3082"]
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]; out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        key = (c[0], int(c[1], 16)) if c[0] in (INST, MBD, FB) else None
        if key in CUT and REC not in c[8] and c[3].startswith("unobservedSpan"):
            rows = CUT[key]("%s %s (%s)" % (c[3], c[4], c[5][:160]))
            if sum(int(x[2]) for x in rows) == int(c[2]): out += ["\t".join(x) + e for x in rows]; continue
        if c[0] == INST and c[3] in ("lastFrameContext", "frameContext") and c[4] == "u8[1113]":
            c[4] = FC; c[8] += " || RETYPED 2026-09-28 (OPUS, %s I): u8[1113] -> Vp8FrameContext" % REC; out.append("\t".join(c) + e); continue
        out.append(l)
    if not any(cells(l)[0] == FC for l in out):
        idx = max(i for i, l in enumerate(out) if cells(l)[0] == INST); out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in FCROWS]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == FC for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == INST); tl[ti + 1:ti + 1] = ["\t".join(NEWT) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def tiles(t): return t in T and sum(int(c[2]) for c in F if c[0] == t) == int(T[t][1], 16)
def name(t, o): return next((c[3] for c in F if c[0] == t and int(c[1], 16) == o), None)
want = [(INST, 0x1E88, "useBilinearMcFilter"), (INST, 0x2C20, "leftContext"), (INST, 0x4448, "ecEnabled"), (MBD, 0xDD8, "fullpixelMask"), (MBD, 0xF08, "modeInfoStride"),
        (MBD, 0xF18, "reconAbove"), (MBD, 0xF58, "leftContext"), (MBD, 0xF75, "refLfDeltas"), (MBD, 0xFB0, "subpixelPredict16x16"), (FB, 0, "yWidth"), (FB, 0x38, "yBuffer"),
        (FC, 0x13, "coefProbs"), (FC, 0x433, "mvc")]
fcs = [c[4] for c in F if c[0] == INST and c[3] in ("lastFrameContext", "frameContext")]
check("P", all(name(t, o) == n for t, o, n in want) and fcs == [FC, FC] and all(tiles(t) for t in (INST, MBD, FB, FC)),
      "the rows are in the store; lastFrameContext / frameContext are Vp8FrameContext; the four types tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
