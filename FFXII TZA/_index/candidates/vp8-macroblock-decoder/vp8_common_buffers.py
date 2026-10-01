"""vp8_common_buffers.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The frame-buffer release 00172750 (called
by vp8_destroy with inst + 0x12C0) and vp8_decode's thread loop place Vp8FrameBuffer records and three owned buffers inside
Vp8DecoderInstance spans the store kept unread. All offsets below are Vp8DecoderInstance offsets (base + 0x12C0 + the code's
displacement).

  R  00172750 releases, each as a Vp8FrameBuffer (free [[+0x58]-8] when [+0x60] > 0, then zero 0x90 bytes):
       four records from +0x1A40 (stride 0x90, esi = 4), one at +0x1CA0, one at +0x1D30, and one at +0x1DC0 only when the dword at
       +0x1E50 is non-zero (00172814 cmp / 0017281B je)
  O  it then frees three owned buffers through the CRT free import (IAT 008C2B48) on the pointer stored 8 bytes before each (the
     vpx_memalign original) and nulls the cells: +0x1E58 (00172852), +0x2C18 (00172868), +0x1EA8 (00172887)
  I  vp8_decode reads the frame-buffer index as a sign-extended dword at +0x1C90 (0016E8A2 movsxd rax, [rbx + 0x9d0], rbx = inst +
     0x12C0) and copies record +0x1A40 + idx*0x90 into each thread's Vp8MacroblockDecoder (vp8_mbd_carve.py T1-T2)
  S  REGRESSION: the three spans are re-cut as generated, tiling kept (FAILS before)
Usage: python vp8_common_buffers.py [--patch]
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
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)   # capstone prints small displacements in decimal
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0)) if m else None
A = lambda pairs: all(at(a)[:2] == v for a, v in pairs)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
C = 0x12C0
check("R", A([(0x16E252, ("lea", "rcx, [rbx + 0x12c0]")), (0x172762, ("lea", "rbx, [rcx + 0x780]")), (0x172769, ("mov", "esi, 4")), (0x17279E, ("add", "rbx, 0x90")),
              (0x1727AB, ("lea", "rbx, [rdi + 0x9e0]")), (0x1727DF, ("lea", "rbx, [rdi + 0xa70]")), (0x172814, ("cmp", "dword ptr [rdi + 0xb90], 0")),
              (0x17281B, ("je", "0x172852")), (0x17281D, ("lea", "rbx, [rdi + 0xb00]")), (0x172829, ("cmp", "dword ptr [rbx + 0x60], 0")),
              (0x17282F, ("mov", "rcx, qword ptr [rbx + 0x58]")), (0x172844, ("mov", "r8d, 0x90")), (0x17284D, ("call", "0x861ec0"))])
      and (C + 0x780, C + 0x9E0, C + 0xA70, C + 0xB00, C + 0xB90) == (0x1A40, 0x1CA0, 0x1D30, 0x1DC0, 0x1E50),
      "four records from +0x1A40, then +0x1CA0, +0x1D30, and +0x1DC0 only when +0x1E50 != 0")
check("O", A([(0x172852, ("mov", "rcx, qword ptr [rdi + 0xb98]")), (0x17285E, ("mov", "rcx, qword ptr [rcx - 8]")), (0x172871, ("mov", "qword ptr [rdi + 0xb98], rbx")),
              (0x172868, ("mov", "rcx, qword ptr [rdi + 0x1958]")), (0x17287D, ("mov", "rcx, qword ptr [rcx - 8]")), (0x1728A9, ("mov", "qword ptr [rdi + 0x1958], rbx")),
              (0x172887, ("mov", "rcx, qword ptr [rdi + 0xbe8]")), (0x172893, ("mov", "rcx, qword ptr [rcx - 8]")), (0x1728A2, ("mov", "qword ptr [rdi + 0xbe8], rbx"))])
      and all(at(a)[2] == 0x8C2B48 for a in (0x172862, 0x172881, 0x172897)) and (C + 0xB98, C + 0x1958, C + 0xBE8) == (0x1E58, 0x2C18, 0x1EA8),
      "owned buffers at +0x1E58, +0x2C18, +0x1EA8: free [p-8] through the CRT free import, then null")
check("I", A([(0x16E8A2, ("movsxd", "rax, dword ptr [rbx + 0x9d0]")), (0x16E6DA, ("mov", "rbx, qword ptr [rbp - 0x28]"))]) and C + 0x9D0 == 0x1C90,
      "the frame-buffer index at +0x1C90, sign-extended")
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/vp8-macroblock-decoder/vp8_common_buffers.py"
EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"; INST = "Vp8DecoderInstance"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def row(o, sz, nm, ct, mean, rd, tag, was): return [INST, "0x%X" % o, str(sz), nm, ct, mean, rd[0], rd[1], "RE-CUT 2026-09-28 (OPUS, %s %s). was part of %s. %s" % (REC, tag, was, EXE)]
FBM = "a Vp8FrameBuffer: 00172750 frees its bufferAlloc when bufferAllocSize > 0 and zeroes the record"
OWN = "an owned buffer: 00172750 frees the vpx_memalign original pointer stored 8 bytes before it through the CRT free import and nulls this cell; its content is not read here"
def cut(start, was):
    if start == 0x1A40:
        return [row(0x1A40, 0x240, "frameBuffers", "Vp8FrameBuffer[4]", "four frame-buffer records (stride 0x90): %s; vp8_decode copies the one +0x1C90 selects into each thread's decoder record" % FBM, P, "R I", was),
                row(0x1C80, 16, "unobservedSpan1C80", "u8[16]", "not read here", U, "R I", was),
                row(0x1C90, 4, "frameBufferIndex", "int32", "the index vp8_decode reads with movsxd (0016E8A2) to select the frame-buffer record it copies into each thread's decoder record", P, "I", was),
                row(0x1C94, 12, "unobservedSpan1C94", "u8[12]", "not read here", U, "R I", was),
                row(0x1CA0, 0x90, "frameBuffer1CA0", "Vp8FrameBuffer", FBM, P, "R", was),
                row(0x1D30, 0x90, "frameBuffer1D30", "Vp8FrameBuffer", FBM, P, "R", was),
                row(0x1DC0, 0x90, "frameBuffer1DC0", "Vp8FrameBuffer", FBM + " - only when +0x1E50 is non-zero", P, "R", was),
                row(0x1E50, 4, "frameBuffer1DC0Present", "uint32", "00172750 releases frameBuffer1DC0 only when this dword is non-zero (cmp / je)", P, "R", was),
                row(0x1E54, 4, "unobservedSpan1E54", "u8[4]", "not read here", U, "R", was),
                row(0x1E58, 8, "ownedBuffer1E58", "void*", OWN, P, "O", was),
                row(0x1E60, 4, "unobservedSpan1E60", "u8[4]", "not read here", U, "O", was)]
    if start == 0x1E84:
        return [row(0x1E84, 36, "unobservedSpan1E84", "u8[36]", "not read here", U, "O", was), row(0x1EA8, 8, "ownedBuffer1EA8", "void*", OWN, P, "O", was)]
    return [row(0x2BF8, 32, "unobservedSpan2BF8", "u8[32]", "not read here", U, "O", was), row(0x2C18, 8, "ownedBuffer2C18", "void*", OWN, P, "O", was),
            row(0x2C20, 5792, "unobservedSpan2C20", "u8[5792]", "not read here", U, "O", was)]
SPAN = {"0x1A40": (0x1A40, "1060"), "0x1E84": (0x1E84, "44"), "0x2BF8": (0x2BF8, "5832")}
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == INST and c[1] in SPAN and c[2] == SPAN[c[1]][1] and c[3].startswith("unobservedSpan"):
            out += ["\t".join(x) + e for x in cut(SPAN[c[1]][0], "%s %s" % (c[3], c[4]))]; continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = {cells(l)[1]: cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == INST}
T = {cells(l)[0]: cells(l) for l in open(os.path.join(DB, "_types", "types.tsv"), "rb").read().decode("utf-8").splitlines()}
gen = [x for s in (0x1A40, 0x1E84, 0x2BF8) for x in cut(s, "")]
# a row a later record re-cut (its evidence names vp8_pbi_names.py) passes if the successor's rows still cover it exactly
# a later record in this package that re-cut or renamed a row names itself in the row's evidence
SUCC_RE = re.compile(r"vp8-macroblock-decoder/(vp8_\w+\.py)")
def by_successor(c): return any(m != os.path.basename(__file__) for m in SUCC_RE.findall(c[8]))
def kept(g):
    if g[1] in F and F[g[1]][3:6] == g[3:6]: return True
    lo = int(g[1], 16); hi = lo + int(g[2]); cov = [c for c in F.values() if lo <= int(c[1], 16) < hi]
    return bool(cov) and all(by_successor(c) for c in cov) and sum(int(c[2]) for c in cov) == int(g[2])
ok = all(kept(g) for g in gen) and sum(int(c[2]) for c in F.values()) == int(T[INST][1], 16)
check("S", ok, "the three spans re-cut as generated (name, ctype, meaning; or re-cut since by a later record of this package, covering the same bytes); Vp8DecoderInstance still tiles 0x4480")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
