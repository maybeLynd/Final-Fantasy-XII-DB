"""vp8_dequant.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
The dequantizer tables of Vp8DecoderInstance (libvpx common.Y1dequant / Y2dequant / UVdequant) and the per-macroblock
copies in Vp8MacroblockDecoder, from their writer, their reader and the receivers of both.

  A  0016F2A0 (create_decompressor): the instance is allocated as 0x44A7 bytes, aligned to 32 ((p + 0x27) & ~0x1F, the
     original pointer stored at p - 8), zeroed for 0x4480 bytes, and kept at [rsp + 0x20]; after the setjmp it is reloaded
     into rsi, and 00174540 is called with rcx = rsi
  Q  00174540 (vp8cx_init_de_quantizer, pbi in rcx = r9): for Q = 0..127 (edx, r8 advancing 4 from pbi + 0x1620):
     [r8 - 0x200] and [r8 - 0x1FE] are the two int16 of Y1dequant[Q] (+0x1420), [r8] and [r8 + 2] of Y2dequant[Q] (+0x1620),
     [r8 + 0x200] and [r8 + 0x202] of UVdequant[Q] (+0x1820). Each DC entry is looked up at Q + a delta field, clamped to
     0..127: y1dcDeltaQ (+0x1E94), y2dcDeltaQ (+0x1E98, doubled), uvdcDeltaQ (+0x1EA0, capped at 0x84); the AC entries use
     Q, y2acDeltaQ (+0x1E9C, times 0x18CCD >> 16, at least 8) and uvacDeltaQ (+0x1EA4)
  M  001746B0 (vp8_mb_init_dequantizer(pbi, xd)): Q = baseQIndex (+0x1E90), or, when segmentationEnabled (xd + 0xF60),
     segmentFeatureData[segmentId] (xd + 0xF67 + [[xd + 0xF00] + 0xB]) plus baseQIndex unless mbSegmentAbsDelta
     (xd + 0xF63) is 1, clamped 0..127. Then xd + 0x800 = 1, xd + 0x7E0 / + 0x820 / + 0x840 = the [Q][0] entries of the
     three tables, and for i = 1..15 the [Q][1] entries fill xd + 0x7E0 + 2i and xd + 0x800 + 2i (Y1), xd + 0x820 + 2i (Y2)
     and xd + 0x840 + 2i (UV). 00175EF0 calls 00174540(pbi) and 001746B0(pbi, pbi) with r12 = pbi reloaded from its slot,
     so xd is the embedded Vp8MacroblockDecoder at +0x0000
  P  REGRESSION (FAILS before): the rows are in the store and both types still tile
Usage: python vp8_dequant.py [--patch]
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
check("A", has(0x16F2A0, 0x16F372, [(0x16F2BC, ("mov", "ecx, 0x44a7")), (0x16F2D8, ("lea", "rbx, [rax + 0x27]")), (0x16F2DC, ("and", "rbx, 0xffffffffffffffe0")),
                                     (0x16F2E5, ("mov", "qword ptr [rbx - 8], rax")), (0x16F2E9, ("mov", "qword ptr [rsp + 0x20], rbx")), (0x16F2F5, ("mov", "r8d, 0x4480")),
                                     (0x16F2FB, ("mov", "rcx, rbx")), (0x16F2FE, ("call", "0x861ec0")), (0x16F33E, ("mov", "rsi, qword ptr [rsp + 0x20]")),
                                     (0x16F362, ("mov", "rcx, rsi")), (0x16F36C, ("call", "0x174540"))]),
      "0016F2A0: 0x44A7-byte allocation aligned to 32, 0x4480 bytes zeroed, then 00174540(pbi)")
check("Q", has(0x174540, 0x1746AE, [(0x174552, ("lea", "r8, [rcx + 0x1620]")), (0x174565, ("mov", "r9, rcx")), (0x174571, ("mov", "ecx, dword ptr [r9 + 0x1e94]")),
                                     (0x17457A, ("cmp", "ecx, 0x7f")), (0x174597, ("mov", "word ptr [r8 - 0x200], ax")), (0x17459F, ("mov", "ecx, dword ptr [r9 + 0x1e98]")),
                                     (0x1745C5, ("add", "ax, ax")), (0x1745C8, ("mov", "word ptr [r8], ax")), (0x1745CC, ("mov", "ecx, dword ptr [r9 + 0x1ea0]")),
                                     (0x1745F3, ("cmovg", "ecx, edi")), (0x1745F6, ("mov", "word ptr [r8 + 0x200], cx")), (0x174559, ("mov", "edi, 0x84")),
                                     (0x17461D, ("mov", "word ptr [r8 - 0x1fe], ax")), (0x174625, ("mov", "ecx, dword ptr [r9 + 0x1e9c]")),
                                     (0x174643, ("imul", "ecx, dword ptr [rbx + rax*4 + 0x1bbcd30], 0x18ccd")), (0x174656, ("mov", "word ptr [r8 + 2], cx")),
                                     (0x17465B, ("mov", "ecx, dword ptr [r9 + 0x1ea4]")), (0x174686, ("mov", "word ptr [r8 + 0x202], ax")),
                                     (0x17468E, ("add", "r8, 4")), (0x174692, ("cmp", "edx, 0x80")), (0x174698, ("jl", "0x174571"))]),
      "00174540: Y1dequant +0x1420, Y2dequant +0x1620, UVdequant +0x1820, 128 x 4 bytes each, from the five delta-q fields")
check("M", has(0x1746B0, 0x17478F, [(0x1746B0, ("mov", "rax, qword ptr [rdx + 0xf00]")), (0x1746B7, ("mov", "r8, rdx")), (0x1746BA, ("lea", "rdx, [rcx + 0x12c0]")),
                                     (0x1746C1, ("cmp", "byte ptr [r8 + 0xf60], 0")), (0x1746CB, ("cmp", "byte ptr [r8 + 0xf63], 1")), (0x1746D3, ("movzx", "eax, byte ptr [rax + 0xb]")),
                                     (0x1746D7, ("movsx", "ecx, byte ptr [rax + r8 + 0xf67]")), (0x1746E2, ("add", "ecx, dword ptr [rdx + 0xbd0]")),
                                     (0x1746FC, ("mov", "eax, dword ptr [rdx + 0xbd0]")), (0x174707, ("mov", "word ptr [r8 + 0x800], cx")),
                                     (0x174712, ("movzx", "eax, word ptr [rdx + rcx*4 + 0x160]")), (0x17471A, ("mov", "word ptr [r8 + 0x7e0], ax")),
                                     (0x174722, ("movzx", "eax, word ptr [rdx + rcx*4 + 0x360]")), (0x17472A, ("mov", "word ptr [r8 + 0x820], ax")),
                                     (0x174732, ("movzx", "eax, word ptr [rdx + rcx*4 + 0x560]")), (0x17473E, ("mov", "word ptr [r8 + 0x840], ax")),
                                     (0x174746, ("lea", "rax, [r8 + 0x802]")), (0x17474D, ("mov", "r8d, 0xf")), (0x174760, ("movzx", "ecx, word ptr [rdx + 0x162]")),
                                     (0x174767, ("mov", "word ptr [rax - 0x20], cx")), (0x17476B, ("mov", "word ptr [rax], cx")), (0x174779, ("mov", "word ptr [rax + 0x1e], cx")),
                                     (0x174784, ("mov", "word ptr [rax + 0x3e], cx"))])
      and has(0x176CE1, 0x176D07, [(0x176CE1, ("mov", "r12, qword ptr [rsp + 0x28]")), (0x176CF4, ("mov", "rcx, r12")), (0x176CF7, ("call", "0x174540")),
                                   (0x176CFC, ("mov", "rdx, r12")), (0x176CFF, ("mov", "rcx, r12")), (0x176D02, ("call", "0x1746b0"))]),
      "001746B0(pbi, xd = pbi): Q from baseQIndex or the segment path; xd +0x7E0 / +0x800 / +0x820 / +0x840 filled from the three tables")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/vp8-macroblock-decoder/vp8_dequant.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
INST, MBD = "Vp8DecoderInstance", "Vp8MacroblockDecoder"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "READ 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was, w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
NR = "not read by 00174540 or 001746B0"
def cut(t, o, was):
    if t == INST and o == 0x1420:
        return [r(INST, 0x1420, 512, "y1Dequant", "int16[256]", "common.Y1dequant[128][2]: [Q][0] the luma DC and [Q][1] the luma AC factor for q-index Q, built by 00174540 and copied per macroblock by 001746B0", P, "Q M", was),
                r(INST, 0x1620, 512, "y2Dequant", "int16[256]", "common.Y2dequant[128][2]: the second-order luma factors (DC doubled; AC scaled by 0x18CCD >> 16, at least 8)", P, "Q M", was),
                r(INST, 0x1820, 512, "uvDequant", "int16[256]", "common.UVdequant[128][2]: the chroma factors (DC capped at 0x84)", P, "Q M", was)]
    if t == MBD and o == 0x04A0:
        return [r(MBD, 0x04A0, 832, "unobservedSpan04A0", "u8[832]", NR, U, "M", was),
                r(MBD, 0x07E0, 32, "dequantY1", "int16[16]", "the macroblock's luma factors: [0] = y1Dequant[Q][0], [1..15] = y1Dequant[Q][1] (001746B0)", P, "M", was),
                r(MBD, 0x0800, 32, "dequantY1Dc", "int16[16]", "[0] = 1, [1..15] = y1Dequant[Q][1]: the luma table used when the DC comes from the second-order block (001746B0)", P, "M", was),
                r(MBD, 0x0820, 32, "dequantY2", "int16[16]", "the second-order factors: [0] = y2Dequant[Q][0], [1..15] = y2Dequant[Q][1] (001746B0)", P, "M", was),
                r(MBD, 0x0840, 32, "dequantUv", "int16[16]", "the chroma factors: [0] = uvDequant[Q][0], [1..15] = uvDequant[Q][1] (001746B0)", P, "M", was),
                r(MBD, 0x0860, 32, "unobservedSpan0860", "u8[32]", NR, U, "M", was)]
    if t == MBD and o == 0x0F00:
        return [r(MBD, 0x0F00, 8, "modeInfoContext", "Vp8ModeInfo*", "the current macroblock's mode-info entry: 001746B0 reads its segmentId (+0xB) to index segmentFeatureData", P, "M", was),
                r(MBD, 0x0F08, 88, "unobservedSpanF08", "u8[88]", NR, U, "M", was)]
APPEND = {(MBD, 0x0F63): " 001746B0: when it is 1 the segment's q-index is absolute, otherwise baseQIndex is added (M).",
          (MBD, 0x0F67): " 001746B0 reads entry segmentId (the first four entries are the per-segment q-index values) as the macroblock's q-index (M).",
          (INST, 0x1E90): " 001746B0 uses it as the q-index when segmentation is off, and adds it on the relative segment path (M)."}
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in (INST, MBD) and REC not in c[8]:
            o = int(c[1], 16)
            rows = cut(c[0], o, "%s %s (%s)" % (c[3], c[4], c[5][:160])) if c[3].startswith("unobservedSpan") else None
            if rows and sum(int(x[2]) for x in rows) == int(c[2]):
                out += ["\t".join(x) + e for x in rows]; continue
            if (c[0], o) in APPEND:
                c[5] += APPEND[(c[0], o)]; c[8] += " || EXTENDED 2026-09-28 (OPUS, %s M)" % REC; out.append("\t".join(c) + e); continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def tiles(t): return t in T and sum(int(c[2]) for c in F if c[0] == t) == int(T[t][1], 16)
I = {int(c[1], 16): c for c in F if c[0] == INST}; M = {int(c[1], 16): c for c in F if c[0] == MBD}
check("P", [I.get(o, [0] * 4)[3] for o in (0x1420, 0x1620, 0x1820)] == ["y1Dequant", "y2Dequant", "uvDequant"]
      and [M.get(o, [0] * 4)[3] for o in (0x7E0, 0x800, 0x820, 0x840, 0xF00)] == ["dequantY1", "dequantY1Dc", "dequantY2", "dequantUv", "modeInfoContext"]
      and all(REC in x[8] for x in (M[0xF63], M[0xF67], I[0x1E90])) and tiles(INST) and tiles(MBD),
      "the three instance tables, the four macroblock tables and modeInfoContext are in the store; both types tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
