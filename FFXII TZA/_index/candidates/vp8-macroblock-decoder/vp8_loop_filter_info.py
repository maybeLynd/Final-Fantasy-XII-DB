"""vp8_loop_filter_info.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
The loop-filter tables embedded in Vp8DecoderInstance at +0x1ED0 (libvpx common.lf_info, loop_filter_info_n), from the
three routines create_decompressor 0016F2A0 runs on them.

  A  0016F2A0: pbi is reloaded into rsi from its slot (vp8_dequant.py A); rbx = rsi + 0x1ED0; 00173640(rbx, [rsi + 0x2BE8]);
     [rsi + 0x2BE4] = [rsi + 0x2BE8]; 001735C0(rbx); then rbx += 0xC00 and four 16-byte memsets store the values 0..3
  S  00173640 (vp8_loop_filter_update_sharpness(lfi, sharpness)): for 64 filter levels (r14d = 2 * level up to 0x7E), with
     rbp = lfi + 0x400 + 16 * level, memset 16 bytes at rbp + 0x400 (lim: the inside limit), at rbp (blim: 2 * level +
     the limit) and at rbp - 0x400 (mblim: 2 * (level + 2) + the limit)
  L  001735C0 (lf_init(lfi)): for level 0..63, lfi + 0xC80 + level and lfi + 0xCC0 + level get the key-frame and inter-frame
     high-edge-variance thresholds (0 / 1 / 2 and 0 / 1 / 2 / 3 at levels 15, 20, 40); lfi + 0xD00..+0xD09 get the ten
     bytes 01 01 01 01 00 02 02 01 02 03
  X  the extent: the next Vp8DecoderInstance row after lfi is filterLevel at +0x2BE0 = lfi + 0xD10; the last byte written
     here is lfi + 0xD09, so 0xD0A..0xD0F is padding to the 16-byte alignment the tables' start at +0x1ED0 keeps
  P  REGRESSION (FAILS before): Vp8LoopFilterInfo exists and tiles, the instance embeds it at +0x1ED0, lastSharpnessLevel named
lfi + 0xC40..+0xC7F (libvpx lvl[4][4][4]) is not written by these routines and stays unobserved.
Usage: python vp8_loop_filter_info.py [--patch]
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
check("A", has(0x16F33E, 0x16F3CB, [(0x16F33E, ("mov", "rsi, qword ptr [rsp + 0x20]")), (0x16F371, ("mov", "edx, dword ptr [rsi + 0x2be8]")), (0x16F377, ("lea", "rbx, [rsi + 0x1ed0]")),
                                     (0x16F37E, ("mov", "rcx, rbx")), (0x16F381, ("call", "0x173640")), (0x16F386, ("mov", "eax, dword ptr [rsi + 0x2be8]")),
                                     (0x16F38C, ("mov", "rcx, rbx")), (0x16F38F, ("mov", "dword ptr [rsi + 0x2be4], eax")), (0x16F395, ("call", "0x1735c0")),
                                     (0x16F39A, ("add", "rbx, 0xc00")), (0x16F3B0, ("mov", "r8d, 0x10")), (0x16F3B6, ("mov", "edx, edi")), (0x16F3BB, ("call", "0x861ec0")),
                                     (0x16F3C2, ("add", "rbx, 0x10")), (0x16F3C6, ("cmp", "edi, 4"))]),
      "0016F2A0: lfi = pbi + 0x1ED0 handed to 00173640 (with sharpnessLevel) and 001735C0; lastSharpnessLevel = sharpnessLevel; hevThr rows 0..3 at lfi + 0xC00")
check("S", has(0x173640, 0x17370D, [(0x17365E, ("lea", "rbp, [rcx + 0x400]")), (0x1736A0, ("lea", "rcx, [rbp + 0x400]")), (0x1736A7, ("mov", "r8d, 0x10")),
                                     (0x1736B3, ("call", "0x861ec0")), (0x1736B8, ("add", "ebx, r14d")), (0x1736C3, ("mov", "rcx, rbp")), (0x1736C6, ("call", "0x861ec0")),
                                     (0x1736CB, ("lea", "edx, [rbx + 4]")), (0x1736D4, ("lea", "rcx, [rbp - 0x400]")), (0x1736DB, ("call", "0x861ec0")),
                                     (0x1736E2, ("add", "rbp, 0x10")), (0x1736E6, ("add", "r14d, 2")), (0x1736EA, ("cmp", "r14d, 0x7e"))]),
      "00173640: 64 levels x 16 bytes of mblim (+0x000), blim (+0x400) and lim (+0x800)")
check("L", has(0x1735C0, 0x17363A, [(0x1735C7, ("lea", "rax, [rcx + 0xcc0]")), (0x1735D8, ("cmp", "rdx, 0x28")), (0x1735DE, ("mov", "byte ptr [rax - 0x40], 2")),
                                     (0x1735E2, ("mov", "byte ptr [rax], 3")), (0x1735E7, ("cmp", "rdx, 0x14")), (0x1735F6, ("cmp", "rdx, 0xf")),
                                     (0x173613, ("cmp", "rcx, 0x3f")), (0x173619, ("mov", "dword ptr [r8 + 0xd00], 0x1010101")),
                                     (0x173624, ("mov", "dword ptr [r8 + 0xd04], 0x1020200")), (0x17362F, ("mov", "word ptr [r8 + 0xd08], 0x302"))]),
      "001735C0: hevThrLut[2][64] at +0xC80 / +0xCC0 by level; modeLfLut[10] at +0xD00")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/vp8-macroblock-decoder/vp8_loop_filter_info.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
INST, LF = "Vp8DecoderInstance", "Vp8LoopFilterInfo"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "READ 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was="-", w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
F_LF = [r(LF, 0x000, 1024, "mblim", "uint8[1024]", "mblim[64][16]: per filter level, 16 copies of the macroblock-edge limit 2 * (level + 2) + the inside limit (00173640)", P, "S"),
        r(LF, 0x400, 1024, "blim", "uint8[1024]", "blim[64][16]: per level, 16 copies of the block-edge limit 2 * level + the inside limit (00173640)", P, "S"),
        r(LF, 0x800, 1024, "lim", "uint8[1024]", "lim[64][16]: per level, 16 copies of the inside limit, which the sharpness shifts down and caps (00173640)", P, "S"),
        r(LF, 0xC00, 64, "hevThr", "uint8[64]", "hev_thr[4][16]: row i is 16 bytes of the value i (0016F2A0)", P, "A"),
        r(LF, 0xC40, 64, "unobservedSpan0C40", "u8[64]", "not written by 0016F2A0, 00173640 or 001735C0", U, "A S L"),
        r(LF, 0xC80, 128, "hevThrLut", "uint8[128]", "hev_thr_lut[2][64]: per level, the row of hevThr to use - key frames 0 / 1 / 2 from level 15 / 40, inter frames 0 / 1 / 2 / 3 from level 15 / 20 / 40 (001735C0)", P, "L"),
        r(LF, 0xD00, 10, "modeLfLut", "uint8[10]", "mode_lf_lut: the ten bytes 01 01 01 01 00 02 02 01 02 03 written by 001735C0", P, "L"),
        r(LF, 0xD0A, 6, "unobservedSpan0D0A", "u8[6]", "after the last byte 001735C0 writes and before the 16-byte end the next instance row fixes (X)", U, "L X")]
NEWT = [LF, "0xD10", "23-Third-Party-Libraries", "one at Vp8DecoderInstance +0x1ED0 (libvpx common.lf_info)", "EMBEDDED in Vp8DecoderInstance",
        "0016F2A0 (00173640 + 001735C0 + the hevThr memsets)", "none - part of its owner", P[0], P[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s A S L X). Extent: filterLevel at +0x2BE0 = +0x1ED0 + 0xD10. %s" % (REC, EXE),
        "23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md", "EMBED Vp8DecoderInstance +0x1ED0"]
def cutI(o, was):
    if o == 0x1EC4:
        return [r(INST, 0x1EC4, 12, "unobservedSpan1EC4", "u8[12]", "between filterType and the loop-filter tables; not read by these routines", U, "A", was),
                r(INST, 0x1ED0, 0xD10, "loopFilterInfo", LF, "common.lf_info: the loop-filter limit and threshold tables 0016F2A0 builds through 00173640 and 001735C0", P, "A S L X", was)]
    if o == 0x2BE4:
        return [r(INST, 0x2BE4, 4, "lastSharpnessLevel", "int32", "common.last_sharpness_level: 0016F2A0 copies sharpnessLevel here after building the limits for it", P, "A", was)]
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]; out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == INST and REC not in c[8] and c[3].startswith("unobservedSpan"):
            rows = cutI(int(c[1], 16), "%s %s (%s)" % (c[3], c[4], c[5][:160]))
            if rows and sum(int(x[2]) for x in rows) == int(c[2]):
                out += ["\t".join(x) + e for x in rows]; continue
        out.append(l)
    if not any(cells(l)[0] == LF for l in out):
        idx = max(i for i, l in enumerate(out) if cells(l)[0] == INST); out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in F_LF]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == LF for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == INST); tl[ti + 1:ti + 1] = ["\t".join(NEWT) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def tiles(t): return t in T and sum(int(c[2]) for c in F if c[0] == t) == int(T[t][1], 16)
I = {int(c[1], 16): c for c in F if c[0] == INST}
check("X", 0x2BE0 in I and I[0x2BE0][3] == "filterLevel" and 0x1ED0 + 0xD10 == 0x2BE0, "the next instance row after lfi is filterLevel at +0x2BE0 = +0x1ED0 + 0xD10")
check("P", tiles(LF) and tiles(INST) and I.get(0x1ED0, [0] * 5)[4] == LF and I.get(0x2BE4, [0] * 4)[3] == "lastSharpnessLevel",
      "Vp8LoopFilterInfo (0xD10) tiles and is embedded at +0x1ED0; lastSharpnessLevel at +0x2BE4; the instance tiles")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
