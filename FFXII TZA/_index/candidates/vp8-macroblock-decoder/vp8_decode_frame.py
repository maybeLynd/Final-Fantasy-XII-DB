"""vp8_decode_frame.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
The frame-header decoder 00175EF0 (libvpx vp8_decode_frame, called as 00175EF0(pbi) by the receive path 0016F840) and the
token-partition setup 00175A00 (setup_token_decoder), read with every base register's definition checked.

  D  DEFINITIONS: 00175EF0 enters with pbi in rcx; r14 = pbi + 0x12C0 (00175F25), r12 = pbi (00175F4A), r13 = [pbi + 0x12A0]
     (decFbRef[0], 00175F43), rdi = pbi + 0x42C0 (00175F32), [rsp + 0x28] = pbi (00175F5C, its only write), [rsp + 0x50] =
     r14 (00175F64; rewritten only at 00177195). For every site below, the last linear write of its base register before
     the site is one of those definitions or a reload from those two slots (r12 / r13 / rbx = [rsp + 0x28] or [rsp + 0x50],
     r13 = r12 + 0x12C0); in 00175A00, rbx = rcx (00175A45) and r14 = rbx + 0x4140
  H2 the short-packet path: when ecActive (+0x444C) is 0 it raises; otherwise frameType (+0x1E64) = 1, version (+0x34E0) = 0,
     showFrame (+0x1E68) = 1
  H3 the key-frame header: width (+0x1A20) and height (+0x1A24) are the low 14 bits of two little-endian 16-bit words;
     horizScale (+0x1A28) and vertScale (+0x1A2C) are those words' top two bits
  H4 decodedKeyFrame (+0x4450) is tested; then the modes bool decoder at +0x42C0 is started on the first partition:
     +0x08 = the buffer, +0x00 = buffer + size, +0x10 = 0, +0x18 = -8, +0x1C = 0xFF, +0x20 = decryptCb (+0x4460),
     +0x28 = decryptState (+0x4468)
  H5 on a key frame two bits are read (00174470) and the second is stored at clampType (+0x1A30); then the macroblock
     decoder's segmentation bytes: +0xF60 enabled, +0xF61 update map, +0xF62 update data, +0xF63 abs delta, +0xF67
     eight feature bytes cleared, +0xF64 / +0xF66 the three tree probabilities, +0xF61..+0xF62 cleared when disabled
  H6 filterType (+0x1EC0, one bit), filterLevel (+0x2BE0, six bits), sharpnessLevel (+0x2BE8, three bits); the macroblock
     decoder's +0xF6F (mode/ref delta enabled) and +0xF70 (delta update)
  H7 the macroblock decoder: corrupted (+0xFC0) cleared on entry; two 0x90 copies of decFbRef[0] into +0xDE0 (pre) and
     +0xE70 (dst); currentBc (+0xFB8) = &partitionBoolDecoders[0] (+0x4140)
  H8 baseQIndex (+0x1E90) and the five delta-q fields (+0x1E94..+0x1EA4) written from the header
  H9 refreshGoldenFrame / refreshAltRefFrame (+0x2BF0 / +0x2BF4), copyBufferToGf / copyBufferToArf (+0x2BF8 / +0x2BFC), the
     golden and altref sign-bias ints (+0x2C0C / +0x2C10), refreshEntropyProbs (+0x2C00); when it is 0, frameContext
     (+0x3082) is copied to lastFrameContext (+0x2C29): 8 x 0x80 + 0x59 = 0x459 bytes; refreshLastFrame (+0x2BEC)
  H10 independentPartitions (+0x4454); qcoeff (+0x180 of the macroblock decoder) cleared, 0x320 bytes; the mode decoder
     0017B580(pbi); aboveContext (+0x2C18) cleared, mbCols (+0x1E78) * 9 bytes; frameCorruptResidual (+0x4458) = 0; the
     threaded path taken on threadsActive (+0x4380) and multiTokenPartition (+0x34E4); decodedKeyFrame set on a key frame;
     at the end, refreshEntropyProbs 0 copies lastFrameContext back and restores independentPartitions
  T  00175A00: the first partition ends at fragmentPtrs[0] (+0x4310) + fragmentSizes[0] (+0x4358); multiTokenPartition
     (+0x34E4) is two bits; fragmentCount (+0x430C) 1 splits the buffer (+0x4318, +0x4358); fragmentCount = partitions + 1;
     each partition's bool decoder, from +0x4140 at stride 0x30, is started from fragmentPtrs[i] / fragmentSizes[i]
     (indexed [rbx + i*8 + 0x4310] / [rbx + i*4 + 0x4358]) exactly as H4; decodingThreadCount (+0x438C) is clamped
  P  REGRESSION (FAILS before): the rows are in the store; Vp8BoolDecoder exists; the three types tile
Names follow libvpx vocabulary; a field's meaning is only what the cited instructions do with it.
Usage: python vp8_decode_frame.py [--patch]
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
    'H1': [(0x175F25, ('lea', 'r14, [rcx + 0x12c0]')), (0x175F43, ('mov', 'r13, qword ptr [rcx + 0x12a0]')), (0x175F4A, ('mov', 'r12, rcx')), (0x175F5C, ('mov', 'qword ptr [rsp + 0x28], rcx')), (0x1772CE, ('mov', 'rbx, qword ptr [rsp + 0x28]'))],
    'H2': [(0x175F83, ('cmp', 'dword ptr [rcx + 0x444c], r15d')), (0x175F9F, ('mov', 'dword ptr [r14 + 0xba4], 1')), (0x175FAA, ('mov', 'dword ptr [r14 + 0x2220], r15d')), (0x175FB1, ('mov', 'dword ptr [r14 + 0xba8], 1'))],
    'H3': [(0x1760EB, ('and', 'ecx, 0x3fff')), (0x1760F1, ('mov', 'dword ptr [r14 + 0x760], ecx')), (0x1760FC, ('shr', 'eax, 6')), (0x1760FF, ('mov', 'dword ptr [r14 + 0x768], eax')), (0x176113, ('and', 'ecx, 0x3fff')), (0x176119, ('mov', 'dword ptr [r14 + 0x764], ecx')), (0x176124, ('shr', 'eax, 6')), (0x176127, ('mov', 'dword ptr [r14 + 0x76c], eax'))],
    'H4': [(0x17623E, ('cmp', 'dword ptr [r12 + 0x4450], r15d')), (0x176262, ('mov', 'r10, qword ptr [r12 + 0x4468]')), (0x17626C, ('mov', 'rcx, qword ptr [r12 + 0x4460]')), (0x17627C, ('add', 'rax, rbp')), (0x17627F, ('mov', 'qword ptr [rdi + 8], rbp')), (0x176283, ('mov', 'qword ptr [rdi], rax')), (0x176286, ('mov', 'qword ptr [rdi + 0x10], r15')), (0x17628A, ('mov', 'dword ptr [rdi + 0x18], 0xfffffff8')), (0x176291, ('mov', 'dword ptr [rdi + 0x1c], 0xff')), (0x176298, ('mov', 'qword ptr [rdi + 0x20], rcx')), (0x17629C, ('mov', 'qword ptr [rdi + 0x28], r10'))],
    'H5': [(0x1762E8, ('mov', 'dword ptr [r14 + 0x770], eax')), (0x1762FC, ('mov', 'byte ptr [r12 + 0xf60], al')), (0x17631E, ('mov', 'byte ptr [r12 + 0xf61], al')), (0x17632E, ('mov', 'byte ptr [r12 + 0xf62], al')), (0x17634B, ('mov', 'byte ptr [r12 + 0xf63], al')), (0x176361, ('mov', 'qword ptr [r12 + 0xf67], rax')), (0x176545, ('mov', 'word ptr [r12 + 0xf64], ax')), (0x17654E, ('mov', 'byte ptr [r12 + 0xf66], al')), (0x17665D, ('mov', 'word ptr [r12 + 0xf61], r15w'))],
    'H6': [(0x1766CD, ('mov', 'dword ptr [r12 + 0x1ec0], esi')), (0x17674B, ('mov', 'dword ptr [r12 + 0x2be0], r14d')), (0x1767CC, ('mov', 'dword ptr [r12 + 0x2be8], ebp')), (0x1767D4, ('lea', 'r13, [r12 + 0x12c0]')), (0x1767DC, ('mov', 'byte ptr [r12 + 0xf70], r15b')), (0x176843, ('mov', 'byte ptr [r12 + 0xf6f], sil')), (0x1768B3, ('mov', 'byte ptr [r12 + 0xf70], sil'))],
    'H7': [(0x175F51, ('mov', 'dword ptr [rcx + 0xfc0], r15d')), (0x17613C, ('movups', 'xmm0, xmmword ptr [r13]')), (0x176141, ('movups', 'xmmword ptr [r12 + 0xde0], xmm0')), (0x1761BD, ('movups', 'xmm0, xmmword ptr [r13]')), (0x1761C2, ('movups', 'xmmword ptr [r12 + 0xe70], xmm0')), (0x176235, ('movups', 'xmmword ptr [r12 + 0xef0], xmm0')), (0x176BD2, ('lea', 'rax, [r12 + 0x4140]')), (0x176BDD, ('mov', 'qword ptr [r12 + 0xfb8], rax'))],
    'H8': [(0x176C64, ('mov', 'dword ptr [r13 + 0xbd0], r14d')), (0x176C84, ('mov', 'dword ptr [r13 + 0xbd4], eax')), (0x176CE6, ('mov', 'dword ptr [r13 + 0xbe4], eax'))],
    'H9': [(0x176D73, ('mov', 'dword ptr [r13 + 0x1930], esi')), (0x176DD9, ('mov', 'dword ptr [r13 + 0x1934], esi')), (0x176DE0, ('mov', 'dword ptr [r13 + 0x1938], r15d')), (0x176E72, ('mov', 'dword ptr [r13 + 0x193c], r15d')), (0x176F61, ('mov', 'dword ptr [r13 + 0x194c], esi')), (0x176FC7, ('mov', 'dword ptr [r13 + 0x1950], esi')), (0x177014, ('mov', 'r10d, 8')), (0x177033, ('mov', 'dword ptr [r13 + 0x1940], esi')), (0x177042, ('lea', 'rcx, [r13 + 0x1969]')), (0x17704C, ('lea', 'rdx, [r13 + 0x1dc2]')), (0x1770AD, ('sub', 'rax, 1')), (0x1770B1, ('jne', '0x177060')), (0x1770E5, ('mov', 'byte ptr [rcx + 0x58], al')), (0x177162, ('mov', 'dword ptr [r13 + 0x192c], eax'))],
    'H10': [(0x177173, ('mov', 'dword ptr [r12 + 0x4454], 1')), (0x1772EC, ('mov', 'dword ptr [rbx + 0x4454], r15d')), (0x177342, ('lea', 'rcx, [rbx + 0x180]')), (0x17734B, ('mov', 'r8d, 0x320')), (0x177356, ('mov', 'rcx, rbx')), (0x177359, ('call', '0x17b580')), (0x17735E, ('movsxd', 'rax, dword ptr [rbx + 0x1e78]')), (0x177365, ('lea', 'rsi, [rbx + 0x12c0]')), (0x17736C, ('mov', 'rcx, qword ptr [rsi + 0x1958]')), (0x177375, ('lea', 'r8, [rax + rax*8]')), (0x177379, ('call', '0x861ec0')), (0x17737E, ('mov', 'dword ptr [rbx + 0x4458], r15d')), (0x177385, ('cmp', 'dword ptr [rbx + 0x4380], r15d')), (0x17738E, ('cmp', 'dword ptr [rsi + 0x2224], r15d')), (0x17740D, ('cmp', 'dword ptr [rbx + 0x4450], 0')), (0x177416, ('cmp', 'dword ptr [rsi + 0xba4], 0')), (0x177424, ('mov', 'dword ptr [rbx + 0x4450], 1')), (0x177444, ('cmp', 'dword ptr [rsi + 0x1940], 0')), (0x177451, ('lea', 'rcx, [rsi + 0x1dc2]')), (0x17745D, ('lea', 'rdx, [rsi + 0x1969]')), (0x1774FC, ('mov', 'dword ptr [rbx + 0x4454], eax'))],
    'T': [(0x175A19, ('mov', 'eax, dword ptr [rcx + 0x4358]')), (0x175A1F, ('lea', 'rsi, [rcx + 0x42c0]')), (0x175A26, ('add', 'rax, qword ptr [rcx + 0x4310]')), (0x175A45, ('mov', 'rbx, rcx')), (0x175ACB, ('mov', 'dword ptr [rbx + 0x34e4], r12d')), (0x175AE0, ('cmp', 'dword ptr [rbx + 0x430c], edi')), (0x175B0A, ('mov', 'rdx, qword ptr [rbx + 0x4310]')), (0x175B2E, ('mov', 'dword ptr [rbx + 0x4358], ecx')), (0x175B34, ('mov', 'qword ptr [rbx + 0x4318], rax')), (0x175BC5, ('lea', 'r14, [rbx + 0x4140]')), (0x175BD0, ('mov', 'dword ptr [rbx + 0x430c], eax')), (0x175BE0, ('mov', 'r8, qword ptr [rbx + 0x4468]')), (0x175BE7, ('mov', 'rcx, qword ptr [rbx + 0x4460]')), (0x175BF1, ('mov', 'edx, dword ptr [rbx + rax*4 + 0x4358]')), (0x175BF8, ('mov', 'r9, qword ptr [rbx + rax*8 + 0x4310]')), (0x175C00, ('mov', 'qword ptr [r14 + 8], r9')), (0x175C04, ('mov', 'qword ptr [r14 + 0x10], 0')), (0x175C0C, ('mov', 'dword ptr [r14 + 0x18], 0xfffffff8')), (0x175C14, ('mov', 'dword ptr [r14 + 0x1c], 0xff')), (0x175C1C, ('lea', 'rax, [r9 + rdx]')), (0x175C20, ('mov', 'qword ptr [r14], rax')), (0x175C23, ('mov', 'qword ptr [r14 + 0x20], rcx')), (0x175C27, ('mov', 'qword ptr [r14 + 0x28], r8')), (0x175C59, ('add', 'r14, 0x30')), (0x175C70, ('cmp', 'dword ptr [rbx + 0x438c], r13d')), (0x175C79, ('mov', 'dword ptr [rbx + 0x438c], r13d'))],
}
FUN = {k: (0x175A00, 0x175CA0) if k == "T" else (0x175EF0, 0x177531) for k in SITES}
LIST = {r: list(cs.disasm(d[off(r[0]):off(r[1])], r[0])) for r in set(FUN.values())}
BYADDR = {r: {x.address: x for x in L} for r, L in LIST.items()}
def full(n):
    m = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
    if n in m: return m[n]
    mm = re.fullmatch(r"(r\d+)[dwb]", n); return mm.group(1) if mm else n
# the approved definitions of each base register (address -> (register, instruction))
DEFS = {0x175F25: ("r14", ("lea", "r14, [rcx + 0x12c0]")), 0x175F4A: ("r12", ("mov", "r12, rcx")), 0x175F43: ("r13", ("mov", "r13, qword ptr [rcx + 0x12a0]")),
        0x175F32: ("rdi", ("lea", "rdi, [rcx + 0x42c0]")), 0x176523: ("r12", ("mov", "r12, qword ptr [rsp + 0x28]")), 0x176650: ("r12", ("mov", "r12, qword ptr [rsp + 0x28]")),
        0x176BB6: ("r12", ("mov", "r12, qword ptr [rsp + 0x28]")), 0x176CE1: ("r12", ("mov", "r12, qword ptr [rsp + 0x28]")), 0x1767D4: ("r13", ("lea", "r13, [r12 + 0x12c0]")),
        0x176BBB: ("r13", ("mov", "r13, qword ptr [rsp + 0x50]")), 0x1772CE: ("rbx", ("mov", "rbx, qword ptr [rsp + 0x28]")), 0x177365: ("rsi", ("lea", "rsi, [rbx + 0x12c0]")),
        0x175A45: ("rbx", ("mov", "rbx, rcx")), 0x175BC5: ("r14", ("lea", "r14, [rbx + 0x4140]")),
        # the lastFrameContext copy loop: rcx = r13 + 0x1969 (00177042), then advanced 0x80 per pass
        0x177042: ("rcx", ("lea", "rcx, [r13 + 0x1969]")), 0x177060: ("rcx", ("lea", "rcx, [rcx + 0x80]"))}
SLOTS = [(0x28, 0x175F5C, "rcx", None), (0x50, 0x175F64, "r14", 0x177195)]   # slot, its defining store, source, next rewrite (after every reload)
def base_regs(x):
    # a lea of two registers or a scaled index is arithmetic, not an access through a base
    if x.mnemonic == "lea" and not re.fullmatch(r"\w+, \[\w+(?: [+-] (0x[0-9a-f]+|\d+))?\]", x.op_str): return set()
    return {full(m.group(1)) for m in re.finditer(r"\[(\w+)(?: [+*]| \])", x.op_str)} - {"rsp", "rip"}
def last_write(L, addr, reg):
    last = None
    for x in L:
        if x.address >= addr: break
        if x.mnemonic in ("push", "pop"): continue
        _, w = x.regs_access()
        if reg in {full(x.reg_name(r)) for r in w}: last = x.address
    return last
bad = []
for k, pairs in SITES.items():
    r = FUN[k]; L = LIST[r]; A = BYADDR[r]
    for a, v in pairs:
        x = A.get(a)
        if x is None or (x.mnemonic, x.op_str) != v: bad.append("%X text" % a); continue
        for reg in base_regs(x):
            lw = last_write(L, a, reg)
            ok = (lw is None and reg == "rcx") or (lw in DEFS and DEFS[lw][0] == reg and (A[lw].mnemonic, A[lw].op_str) == DEFS[lw][1])
            if not ok: bad.append("%X %s <- %s" % (a, reg, "%X" % lw if lw else "entry"))
L = LIST[(0x175EF0, 0x177531)]
def last_slot_store(addr, slot):
    last = None
    for x in L:
        if x.address >= addr: break
        if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rsp + %s], " % hex(slot)): last = x
    return last
# every approved reload of a slot must see, as the slot's last linear store, the slot's defining store of the right register
reloads = [(a, int(m.group(1), 16)) for a, (reg, (mn, op)) in DEFS.items() for m in [re.search(r"\[rsp \+ (0x[0-9a-f]+)\]", op)] if m and a < 0x177531 and a > 0x175EF0]
SLOTDEF = {s: (at, src) for s, at, src, nx in SLOTS}
sl = all((lambda st: st is not None and st.address == SLOTDEF[s][0] and st.op_str.endswith(", " + SLOTDEF[s][1]))(last_slot_store(a, s)) for a, s in reloads)
check("D", not bad and sl, "every cited instruction matches, and each base register's last linear write is an approved definition%s" % (": " + ", ".join(bad) if bad else ""))
def ok(tag): return not any(b.startswith(tuple("%X" % a for a, _ in SITES[tag])) for b in bad)
TXT = {"H2": "short packet: ecActive gate; frameType = 1, version = 0, showFrame = 1",
       "H3": "key frame: width / height 14 bits, horizScale / vertScale the top 2 bits",
       "H4": "decodedKeyFrame tested; the modes bool decoder +0x42C0 started (end, buffer, 0, -8, 0xFF, decryptCb, decryptState)",
       "H5": "clampType; segmentation bytes +0xF60..+0xF67 of the macroblock decoder",
       "H6": "filterType, filterLevel, sharpnessLevel; mode/ref delta enabled +0xF6F and update +0xF70",
       "H7": "corrupted +0xFC0 cleared; pre +0xDE0 and dst +0xE70 copied from decFbRef[0]; currentBc +0xFB8 = &partitionBoolDecoders[0]",
       "H8": "baseQIndex and the delta-q fields", "H9": "refresh / copy / sign-bias flags; lastFrameContext <- frameContext, 8 x 0x80 + 0x59 bytes; refreshLastFrame",
       "H10": "independentPartitions, qcoeff cleared (0x320), aboveContext cleared (mbCols * 9), frameCorruptResidual, threaded path, decodedKeyFrame, restore",
       "T": "fragment arrays indexed; multiTokenPartition; fragmentCount; partition bool decoders at stride 0x30; decodingThreadCount clamp"}
for k in [k for k in SITES if k != "H1"]: check(k, ok(k), TXT[k])

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/vp8-macroblock-decoder/vp8_decode_frame.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
INST, MBD, BD = "Vp8DecoderInstance", "Vp8MacroblockDecoder", "Vp8BoolDecoder"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "READ 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was="-", w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
NR = "not read by 00175EF0 or 00175A00"
def cutI(o, was):
    I = INST
    C = {0x1420: [r(I, 0x1420, 1536, "unobservedSpan1420", "u8[1536]", NR, U, "D", was),
                  r(I, 0x1A20, 4, "width", "int32", "common.Width: on a key frame, the low 14 bits of the first 16-bit size word", P, "H3", was),
                  r(I, 0x1A24, 4, "height", "int32", "common.Height: on a key frame, the low 14 bits of the second 16-bit size word", P, "H3", was),
                  r(I, 0x1A28, 4, "horizScale", "int32", "common.horiz_scale: the first size word's top two bits", P, "H3", was),
                  r(I, 0x1A2C, 4, "vertScale", "int32", "common.vert_scale: the second size word's top two bits", P, "H3", was),
                  r(I, 0x1A30, 4, "clampType", "int32", "common.clamp_type: on a key frame, the second of two header bits (the first is read and dropped)", P, "H5", was),
                  r(I, 0x1A34, 4, "unobservedSpan1A34", "u8[4]", NR, U, "D", was)],
         0x1E84: [r(I, 0x1E84, 12, "unobservedSpan1E84", "u8[12]", NR, U, "D", was),
                  r(I, 0x1E90, 4, "baseQIndex", "int32", "common.base_qindex: written from the frame header", P, "H8", was),
                  r(I, 0x1E94, 4, "y1dcDeltaQ", "int32", "common.y1dc_delta_q: a header delta, read and rewritten by the delta-q update", P, "H8", was),
                  r(I, 0x1E98, 4, "y2dcDeltaQ", "int32", "common.y2dc_delta_q: as y1dcDeltaQ", P, "H8", was),
                  r(I, 0x1E9C, 4, "y2acDeltaQ", "int32", "common.y2ac_delta_q: as y1dcDeltaQ", P, "H8", was),
                  r(I, 0x1EA0, 4, "uvdcDeltaQ", "int32", "common.uvdc_delta_q: as y1dcDeltaQ", P, "H8", was),
                  r(I, 0x1EA4, 4, "uvacDeltaQ", "int32", "common.uvac_delta_q: as y1dcDeltaQ", P, "H8", was)],
         0x1EC0: [r(I, 0x1EC0, 4, "filterType", "int32", "common.filter_type: one header bit", P, "H6", was),
                  r(I, 0x1EC4, 3356, "unobservedSpan1EC4", "u8[3356]", NR, U, "D", was),
                  r(I, 0x2BE0, 4, "filterLevel", "int32", "common.filter_level: six header bits", P, "H6", was),
                  r(I, 0x2BE4, 4, "unobservedSpan2BE4", "u8[4]", NR, U, "D", was),
                  r(I, 0x2BE8, 4, "sharpnessLevel", "int32", "common.sharpness_level: three header bits", P, "H6", was)],
         0x2BF8: [r(I, 0x2BF8, 4, "copyBufferToGf", "int32", "common.copy_buffer_to_gf: written from the header when refreshGoldenFrame is 0", P, "H9", was),
                  r(I, 0x2BFC, 4, "copyBufferToArf", "int32", "common.copy_buffer_to_arf: written from the header when refreshAltRefFrame is 0", P, "H9", was),
                  r(I, 0x2C00, 4, "refreshEntropyProbs", "int32", "common.refresh_entropy_probs: when 0, frameContext is saved to lastFrameContext before the frame and restored after it", P, "H9", was),
                  r(I, 0x2C04, 8, "unobservedSpan2C04", "u8[8]", NR, U, "D", was),
                  r(I, 0x2C0C, 4, "refFrameSignBiasGolden", "int32", "common.ref_frame_sign_bias[GOLDEN_FRAME]: one header bit", P, "H9", was),
                  r(I, 0x2C10, 4, "refFrameSignBiasAltRef", "int32", "common.ref_frame_sign_bias[ALTREF_FRAME]: one header bit", P, "H9", was),
                  r(I, 0x2C14, 4, "unobservedSpan2C14", "u8[4]", NR, U, "D", was)],
         0x2C20: [r(I, 0x2C20, 9, "unobservedSpan2C20", "u8[9]", NR, U, "D", was),
                  r(I, 0x2C29, 1113, "lastFrameContext", "u8[1113]", "common.lfc: when refreshEntropyProbs is 0, 00175EF0 copies frameContext here before the frame (8 x 0x80 + 0x59 bytes) and back after it", P, "H9 H10", was),
                  r(I, 0x3082, 1113, "frameContext", "u8[1113]", "common.fc, the frame's entropy context: the source and restore target of the lastFrameContext copies", P, "H9 H10", was),
                  r(I, 0x34DB, 1, "unobservedSpan34DB", "u8[1]", NR, U, "D", was)],
         0x34E0: [r(I, 0x34E0, 4, "version", "int32", "common.version: set 0 on the short-packet path", P, "H2", was),
                  r(I, 0x34E4, 4, "multiTokenPartition", "int32", "common.multi_token_partition: two header bits; the partition count is 1 << it; with threadsActive it selects the threaded row decoder", P, "T H10", was)],
         0x34EC: [r(I, 0x34EC, 3156, "unobservedSpan34EC", "u8[3156]", NR, U, "D", was),
                  r(I, 0x4140, 384, "partitionBoolDecoders", BD + "[8]", "mbc[0..7], the token-partition bool decoders: 00175A00 starts one per partition at stride 0x30 from fragmentPtrs[i] / fragmentSizes[i]; the macroblock decoder's currentBc points at the first", P, "T H7", was)],
         0x42F0: [r(I, 0x42F0, 28, "unobservedSpan42F0", "u8[28]", NR, U, "D", was),
                  r(I, 0x430C, 4, "fragmentCount", "uint32", "fragments.count: 1 makes 00175A00 split the one buffer into partitions; it then becomes the partition count + 1", P, "T", was),
                  r(I, 0x4310, 72, "fragmentPtrs", "void*[9]", "fragments.ptrs: indexed [pbi + i*8 + 0x4310]; [0] is the first partition 00175EF0 decodes from; nine entries end where fragmentSizes begins", P, "T H4", was),
                  r(I, 0x4358, 36, "fragmentSizes", "uint32[9]", "fragments.sizes: indexed [pbi + i*4 + 0x4358], parallel to fragmentPtrs", P, "T H4", was),
                  r(I, 0x437C, 4, "unobservedSpan437C", "u8[4]", NR, U, "D", was)],
         0x4448: [r(I, 0x4448, 4, "unobservedSpan4448", "uint8[4]", NR, U, "D", was),
                  r(I, 0x444C, 4, "ecActive", "int32", "error concealment active: when 0 a short packet or a bad partition size raises (00175EF0, 001758F0)", P, "H2", was),
                  r(I, 0x4450, 4, "decodedKeyFrame", "int32", "tested before decoding; set to 1 after a key frame", P, "H4 H10", was),
                  r(I, 0x4454, 4, "independentPartitions", "int32", "set by the header decode and restored after the frame when refreshEntropyProbs is 0", P, "H10", was),
                  r(I, 0x4458, 4, "frameCorruptResidual", "int32", "cleared before the macroblock rows are decoded", P, "H10", was),
                  r(I, 0x445C, 4, "unobservedSpan445C", "u8[4]", NR, U, "D", was),
                  r(I, 0x4460, 8, "decryptCb", "void*", "the decrypt callback: called on each partition-size read (001758F0) and stored into every bool decoder", P, "H4 T", was),
                  r(I, 0x4468, 8, "decryptState", "void*", "the decrypt callback's state: its first argument, stored into every bool decoder", P, "H4 T", was),
                  r(I, 0x4470, 16, "unobservedSpan4470", "u8[16]", NR, U, "D", was)]}
    return C.get(o)
def cutM(o, was):
    M = MBD
    C = {0x0000: [r(M, 0x0000, 384, "unobservedSpan0000", "u8[384]", NR, U, "D", was),
                  r(M, 0x0180, 800, "qcoeff", "int16[400]", "the quantized coefficients: 00175EF0 clears all 0x320 bytes before the macroblock rows", P, "H10", was),
                  r(M, 0x04A0, 992, "unobservedSpan04A0", "u8[992]", NR, U, "D", was)],
         0x0DC0: [r(M, 0x0DC0, 32, "unobservedSpanDC0", "u8[32]", NR, U, "D", was),
                  r(M, 0x0DE0, 144, "preFrameBuffer", "Vp8FrameBuffer", "xd->pre: 00175EF0 copies decFbRef[0]'s 0x90-byte record here, as it does into dstFrameBuffer", P, "H7", was)],
         0x0F00: [r(M, 0x0F00, 96, "unobservedSpanF00", "u8[96]", NR, U, "D", was),
                  r(M, 0x0F60, 1, "segmentationEnabled", "uint8", "one header bit; when 0 the update flags +0xF61 / +0xF62 are cleared", P, "H5", was),
                  r(M, 0x0F61, 1, "updateMbSegmentationMap", "uint8", "one header bit, read when segmentation is enabled", P, "H5", was),
                  r(M, 0x0F62, 1, "updateMbSegmentationData", "uint8", "one header bit; when set, the abs-delta bit and the feature data follow", P, "H5", was),
                  r(M, 0x0F63, 1, "mbSegmentAbsDelta", "uint8", "one header bit", P, "H5", was),
                  r(M, 0x0F64, 3, "mbSegmentTreeProbs", "uint8[3]", "the segment-map tree probabilities, written as a word at +0xF64 and a byte at +0xF66", P, "H5", was),
                  r(M, 0x0F67, 8, "segmentFeatureData", "int8[8]", "cleared as one qword when the segment data is updated, then filled from the header", P, "H5", was),
                  r(M, 0x0F6F, 1, "modeRefLfDeltaEnabled", "uint8", "one header bit", P, "H6", was),
                  r(M, 0x0F70, 1, "modeRefLfDeltaUpdate", "uint8", "cleared, then one header bit when the deltas are enabled", P, "H6", was),
                  r(M, 0x0F71, 19, "unobservedSpanF71", "u8[19]", NR, U, "D", was)],
         0x0F94: [r(M, 0x0F94, 36, "unobservedSpanF94", "u8[36]", NR, U, "D", was),
                  r(M, 0x0FB8, 8, "currentBc", BD + "*", "the bool decoder the token reader uses: 00175EF0 points it at partitionBoolDecoders[0] (pbi + 0x4140)", P, "H7", was),
                  r(M, 0x0FC0, 4, "corrupted", "int32", "cleared as 00175EF0 begins and read after the macroblock rows", P, "H7", was),
                  r(M, 0x0FC4, 732, "unobservedSpanFC4", "u8[732]", NR, U, "D", was)]}
    return C.get(o)
NEWT = [BD, "0x30", "23-Third-Party-Libraries", "nine per Vp8DecoderInstance: partitionBoolDecoders[8] at +0x4140 and modeBoolDecoder at +0x42C0", "EMBEDDED in Vp8DecoderInstance",
        "started by 00175EF0 (the modes decoder) and 00175A00 (each partition)", "none - part of its owner", P[0], P[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s H4 T). Stride 0x30 from 00175C59 (add r14, 0x30); the partition array ends where modeBoolDecoder starts. %s" % (REC, EXE),
        "23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md", "EMBED Vp8DecoderInstance +0x4140 stride=0x30"]
BDROWS = [r(BD, 0, 8, "userBufferEnd", "void*", "buffer + size, stored when the decoder is started", P, "H4 T"),
          r(BD, 8, 8, "userBuffer", "void*", "the partition's bytes (fragmentPtrs[i], or the first partition)", P, "H4 T"),
          r(BD, 0x10, 8, "value", "uint64", "the bit window, 0 at start; compared against the split shifted to the top byte (00175A00)", P, "H4 T"),
          r(BD, 0x18, 4, "count", "int32", "the bits left in value, -8 at start; below 0 the refill 00179ED0 runs", P, "H4 T"),
          r(BD, 0x1C, 4, "range", "uint32", "the arithmetic-decoder range, 0xFF at start; split = 1 + (((range - 1) * prob) >> 8)", P, "H4 T"),
          r(BD, 0x20, 8, "decryptCb", "void*", "copied from the instance's decryptCb", P, "H4 T"),
          r(BD, 0x28, 8, "decryptState", "void*", "copied from the instance's decryptState", P, "H4 T")]
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]
    out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in (INST, MBD) and REC not in c[8] and c[3].startswith("unobservedSpan"):
            was = "%s %s (%s)" % (c[3], c[4], c[5][:160]); o = int(c[1], 16)
            rows = cutI(o, was) if c[0] == INST else cutM(o, was)
            if rows and sum(int(x[2]) for x in rows) == int(c[2]):
                out += ["\t".join(x) + e for x in rows]; continue
        if c[0] == INST and c[1] == "0x42C0" and c[4] == "uint8[48]":
            c[4] = BD; c[8] += " || RETYPED 2026-09-28 (OPUS, %s H4): uint8[48] -> Vp8BoolDecoder" % REC; out.append("\t".join(c) + e); continue
        if c[0] == INST and c[1] == "0x2C18" and c[3] == "ownedBuffer2C18":
            c[3] = "aboveContext"; c[5] += " 00175EF0 clears it for mbCols * 9 bytes before each frame's rows - one 9-byte context per macroblock column (H10)."
            c[8] += " || RENAMED 2026-09-28 (OPUS, %s H10): was ownedBuffer2C18" % REC; out.append("\t".join(c) + e); continue
        out.append(l)
    if not any(cells(l)[0] == BD for l in out):
        idx = max(i for i, l in enumerate(out) if cells(l)[0] == INST)
        out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in BDROWS]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == BD for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == INST); tl[ti + 1:ti + 1] = ["\t".join(NEWT) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def tiles(t): return t in T and sum(int(c[2]) for c in F if c[0] == t) == int(T[t][1], 16)
I = {int(c[1], 16): c for c in F if c[0] == INST}; M = {int(c[1], 16): c for c in F if c[0] == MBD}
wantI = {0x1A20: "width", 0x1A30: "clampType", 0x1E90: "baseQIndex", 0x1EC0: "filterType", 0x2BE0: "filterLevel", 0x2C00: "refreshEntropyProbs", 0x2C18: "aboveContext",
         0x2C29: "lastFrameContext", 0x3082: "frameContext", 0x34E4: "multiTokenPartition", 0x4140: "partitionBoolDecoders", 0x4310: "fragmentPtrs", 0x4358: "fragmentSizes",
         0x444C: "ecActive", 0x4460: "decryptCb"}
wantM = {0x180: "qcoeff", 0xDE0: "preFrameBuffer", 0xF60: "segmentationEnabled", 0xF67: "segmentFeatureData", 0xFB8: "currentBc", 0xFC0: "corrupted"}
check("P", all(o in I and I[o][3] == n for o, n in wantI.items()) and all(o in M and M[o][3] == n for o, n in wantM.items()) and I[0x42C0][4] == BD
      and all(tiles(t) for t in (INST, MBD, BD)), "the rows are in the store; Vp8BoolDecoder exists; Vp8DecoderInstance, Vp8MacroblockDecoder and Vp8BoolDecoder tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
