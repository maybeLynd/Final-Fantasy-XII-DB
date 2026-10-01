"""vp8_postproc.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
The post-processing state embedded in Vp8DecoderInstance at +0x34F0 (libvpx common.postproc_state), from the frame
post-processor 00177A70 and its noise builder 00177850.

  G  0016EA80 (vp8_get_frame) hands pbi + 0x12C0 to 00177A70 (vp8_pbi_names.py G), so 00177A70's rcx / rsi is pc = pbi + 0x12C0
  N  00177A70 with no flags: copies frameToShow's record to the caller, then pc + 0x2E3C (pbi + 0x40FC) = 1 and
     pc + 0x2E38 (pbi + 0x40F8) = baseQIndex; the flagged path sets pc + 0xB90 (pbi + 0x1E50) = 1 and repeats both stores
  A  the add-noise branch (flag bit 2): state = pc + 0x2230 (pbi + 0x34F0); when [state] != q or [state + 4] != the noise
     level, 00177850(state, 63 - q, level) runs; then 00149610 gets the post-processed frame's luma buffer, state + 8,
     pc + 0x2E40 / 0x2E50 / 0x2E60 (pbi + 0x4100 / 0x4110 / 0x4120) and the frame's width, height and stride
  F  00177850 (fillrd(state, q, a)): 0xC00 bytes from state + 8 filled from a table of rand() picks; 16 bytes each at
     state + 0xC10 / 0xC20 / 0xC30 (the negated first entry, the same, and twice it negated); [state] = q, [state + 4] = a
  P  REGRESSION (FAILS before): Vp8PostprocState exists and tiles, the instance embeds it at +0x34F0
Usage: python vp8_postproc.py [--patch]
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
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.skipdata = True   # sweep whole functions; data bytes inside them are skipped
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
    return all(A.get(a) == v for a, v in pairs)
check("G", has(0x16EA80, 0x16EB2A, [(0x16EA9E, ("mov", "rcx, qword ptr [rcx + 0x1b0]")), (0x16EB11, ("add", "rcx, 0x12c0")), (0x16EB25, ("call", "0x177a70"))]),
      "0016EA80 calls 00177A70 with pbi + 0x12C0")
check("N", has(0x177A70, 0x177B70, [(0x177A8A, ("mov", "rsi, rcx")), (0x177AA4, ("mov", "rax, qword ptr [rcx + 0x778]")), (0x177B50, ("mov", "dword ptr [rcx + 0x2e3c], 1")),
                                     (0x177B60, ("mov", "eax, dword ptr [rcx + 0xbd0]")), (0x177B66, ("mov", "dword ptr [rcx + 0x2e38], eax"))])
      and has(0x177A70, 0x177E75, [(0x177BE4, ("mov", "dword ptr [rsi + 0xb90], 1")), (0x177D44, ("mov", "eax, dword ptr [rsi + 0xbd0]")),
                                   (0x177D4A, ("mov", "dword ptr [rsi + 0x2e38], eax")), (0x177D58, ("mov", "dword ptr [rsi + 0x2e3c], 1"))]),
      "00177A70: lastFrameValid (+0x40FC) = 1 and lastBaseQIndex (+0x40F8) = baseQIndex on both paths; +0x1E50 = 1 on the flagged path")
check("A", has(0x177A70, 0x177E75, [(0x177D62, ("test", "bpl, 4")), (0x177D68, ("lea", "rcx, [rsi + 0x2230]")), (0x177D6F, ("cmp", "dword ptr [rcx], r14d")),
                                     (0x177D74, ("cmp", "dword ptr [rsi + 0x2234], r12d")), (0x177D86, ("call", "0x177850")), (0x177D91, ("lea", "rcx, [rsi + 0x2e60]")),
                                     (0x177D9C, ("lea", "r9, [rsi + 0x2e50]")), (0x177DA9, ("lea", "r8, [rsi + 0x2e40]")), (0x177DB4, ("lea", "rdx, [rsi + 0x2238]")),
                                     (0x177DCA, ("mov", "rcx, qword ptr [rsi + 0xaa8]")), (0x177DD1, ("call", "0x149610"))]),
      "00177A70 add-noise: fillrd(pbi + 0x34F0, ...) when q or the level changed; the noise at +0x34F8 and the clamps at +0x4100 / +0x4110 / +0x4120 go to 00149610")
check("F", has(0x177850, 0x177A66, [(0x177881, ("mov", "r15d, edx")), (0x177879, ("mov", "ebp, r8d")), (0x177889, ("mov", "r14, rcx")), (0x1779E2, ("mov", "ebx, 0xc00")),
                                     (0x1779F9, ("mov", "byte ptr [rdi - 1], al")), (0x177A07, ("lea", "rax, [r14 + 0xc20]")), (0x177A11, ("lea", "edi, [rbx + 0x10]")),
                                     (0x177A20, ("mov", "byte ptr [rax - 0x10], cl")), (0x177A23, ("mov", "byte ptr [rax], cl")), (0x177A25, ("mov", "byte ptr [rax + 0x10], dl")),
                                     (0x177A3A, ("mov", "dword ptr [r14], r15d")), (0x177A3D, ("mov", "dword ptr [r14 + 4], ebp"))])
      and d[off(0x1779DE):off(0x1779DE) + 4] == bytes.fromhex("498d7e08"),   # 001779DE lea rdi, [r14 + 8]: the noise fill's start (a linear sweep desynchronises just before it)
      "00177850: 0xC00 noise bytes from state + 8; three 16-byte clamps at +0xC10 / +0xC20 / +0xC30; last q and level at +0 / +4")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/vp8-macroblock-decoder/vp8_postproc.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
INST, PP = "Vp8DecoderInstance", "Vp8PostprocState"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "READ 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was="-", w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
F_PP = [r(PP, 0x000, 4, "lastQ", "int32", "the q the noise was last built for: 00177850 stores it; 00177A70 rebuilds when it differs", P, "A F"),
        r(PP, 0x004, 4, "lastNoise", "int32", "the noise level the noise was last built for, compared the same way", P, "A F"),
        r(PP, 0x008, 3072, "noise", "int8[3072]", "0xC00 noise bytes 00177850 draws from a table by rand(); the add-noise call reads them", P, "A F"),
        r(PP, 0xC08, 4, "lastBaseQIndex", "int32", "baseQIndex at the last post-processed frame (00177A70, both paths)", P, "N"),
        r(PP, 0xC0C, 4, "lastFrameValid", "int32", "set to 1 by 00177A70 after each post-processed frame", P, "N"),
        r(PP, 0xC10, 16, "blackClamp", "uint8[16]", "16 copies of the negated first noise-table entry (00177850); an add-noise argument", P, "A F"),
        r(PP, 0xC20, 16, "whiteClamp", "uint8[16]", "16 copies of the same value (00177850); an add-noise argument", P, "A F"),
        r(PP, 0xC30, 16, "bothClamp", "uint8[16]", "16 copies of twice the negated value (00177850); an add-noise argument", P, "A F")]
NEWT = [PP, "0xC40", "23-Third-Party-Libraries", "one at Vp8DecoderInstance +0x34F0 (libvpx common.postproc_state)", "EMBEDDED in Vp8DecoderInstance",
        "00177850 (the noise and clamps) and 00177A70 (the last-frame fields)", "none - part of its owner", P[0], P[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s G N A F). Extent: through bothClamp, the last byte 00177850 writes; the 16 bytes to partitionBoolDecoders (+0x4140) are not read here. %s" % (REC, EXE),
        "23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md", "EMBED Vp8DecoderInstance +0x34F0"]
def cutI(o, was):
    if o == 0x34EC:
        return [r(INST, 0x34EC, 4, "unobservedSpan34EC", "u8[4]", "between processorCoreCount and the post-processing state; not read here", U, "N", was),
                r(INST, 0x34F0, 0xC40, "postprocState", PP, "common.postproc_state: the noise and clamp tables and the last post-processed frame's q / validity (00177A70, 00177850)", P, "G N A F", was),
                r(INST, 0x4130, 16, "unobservedSpan4130", "u8[16]", "between the post-processing state and partitionBoolDecoders; not read here", U, "N", was)]
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
    if not any(cells(l)[0] == PP for l in out):
        idx = max(i for i, l in enumerate(out) if cells(l)[0] == INST); out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in F_PP]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == PP for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == INST); tl[ti + 1:ti + 1] = ["\t".join(NEWT) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
def tiles(t): return t in T and sum(int(c[2]) for c in F if c[0] == t) == int(T[t][1], 16)
I = {int(c[1], 16): c for c in F if c[0] == INST}
check("P", tiles(PP) and tiles(INST) and I.get(0x34F0, [0] * 5)[4] == PP,"Vp8PostprocState (0xC40) tiles and is embedded at +0x34F0; the instance tiles")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
