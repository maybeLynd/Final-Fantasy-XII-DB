"""glyph_run_arrays.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
GlyphRunWidget1498's two large unread spans are index-addressed arrays - invisible to a displacement census, which is why
both censuses left them unreached. The widget's reader and appender address them with a scaled index.

  R  the handler 0053E380 (rbx = rcx) calls 0053E640 with rcx = rbx on message 2; 0053E640 (rbx = rcx) walks three
     position arrays, each while its position minus a base is below the cursor +0xEC:
       dwords at +0x290 + 4i for i from the word +0x108 to the word +0x10A, then reads the dword +0x690 + 4i
       records at +0xA90 + 0x14i for i from the word +0x1490 to the word +0x1492, then reads the record's +4 and +0x10
       dwords at +0x110 + 4i for i from the byte +0x105 to the byte +0x106, then reads the int16 +0x210 + 2i
     and on a hit stores the value at +0xF8 and a kind byte at +0xFC (5 / 6 / 2)
  A  0053EFC0 (the widget from its cell 02CA8A80) appends a record at +0xA90 + 0x14 * (int16 +0x1492): the dword +0 = the
     running offset +0xF0, int16s at +4..+0x10 (+0x10 = its first argument), then increments +0x1492 and advances +0xF0
  E  capacities by adjacency: 0x110 + 64*4 = 0x210, 0x210 + 64*2 = 0x290, 0x290 + 256*4 = 0x690, 0x690 + 256*4 = 0xA90,
     0xA90 + 128*0x14 = 0x1490 - five arrays tiling +0x110..+0x148F exactly, the last ending at the run range's first index
     word; the byte / word index widths agree (64 fits a byte range, 256 and 128 word ranges). The capacities are the
     space the layout leaves, not a bound the code checks
  W  REGRESSION (FAILS before): the arrays, the run record type and the renamed range fields are in the store; both tile
Usage: python glyph_run_arrays.py [--patch]
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
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.skipdata = True
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
    return all(A.get(a) == v for a, v in pairs)
check("R", has(0x53E380, 0x53E494, [(0x53E38F, ("mov", "rbx, rcx")), (0x53E3A0, ("je", "0x53e479")), (0x53E48C, ("mov", "rcx, rbx")), (0x53E48F, ("call", "0x53e640"))])
      and has(0x53E640, 0x53EB05, [(0x53E64F, ("mov", "rbx, rcx")), (0x53E976, ("movsx", "rcx, word ptr [rbx + 0x108]")), (0x53E97E, ("movsx", "r8d, word ptr [rbx + 0x10a]")),
                                   (0x53E992, ("lea", "rdx, [rbx + 0x290]")), (0x53E999, ("lea", "rdx, [rdx + rcx*4]")), (0x53EA61, ("mov", "ecx, dword ptr [rbx + rax*4 + 0x690]")),
                                   (0x53EA70, ("mov", "byte ptr [rbx + 0xfc], 5")), (0x53E9B9, ("movsx", "rdx, word ptr [rbx + 0x1490]")), (0x53E9C1, ("movsx", "r11d, word ptr [rbx + 0x1492]")),
                                   (0x53E9CE, ("lea", "r8, [rdx + 0xa9]")), (0x53E9D5, ("lea", "r8, [rdx + r8*4]")), (0x53E9D9, ("lea", "r8, [rbx + r8*4]")), (0x53E9F1, ("add", "r8, 0x14")),
                                   (0x53EA93, ("movsx", "edx, word ptr [r8 + 0x10]")), (0x53EAA5, ("movsx", "eax, word ptr [r8 + 4]")), (0x53EAB2, ("mov", "byte ptr [rbx + 0xfc], 6")),
                                   (0x53E9FA, ("movsx", "rcx, byte ptr [rbx + 0x105]")), (0x53EA02, ("movsx", "r10d, byte ptr [rbx + 0x106]")), (0x53EA16, ("lea", "rdx, [rbx + 0x110]")),
                                   (0x53EA1D, ("lea", "rdx, [rdx + rcx*4]")), (0x53EADD, ("movsx", "eax, word ptr [rbx + rax*2 + 0x210]")), (0x53EAED, ("mov", "byte ptr [rbx + 0xfc], 2"))]),
      "0053E640 walks +0x290 / +0x690 (by +0x108 .. +0x10A), the runs from +0xA90 (by +0x1490 .. +0x1492), +0x110 / +0x210 (by +0x105 .. +0x106)")
check("A", has(0x53EFC0, 0x53F0C6, [(0x53EFE5, ("movsx", "rax, word ptr [r11 + 0x1492]")), (0x53EFED, ("lea", "r10, [rax + rax*4]")), (0x53EFF1, ("mov", "eax, dword ptr [r11 + 0xf0]")),
                                     (0x53EFF8, ("mov", "dword ptr [r11 + r10*4 + 0xa90], eax")), (0x53F043, ("mov", "word ptr [r11 + r10*4 + 0xaa0], bx")), (0x53F0AE, ("inc", "word ptr [r11 + 0x1492]")),
                                     (0x53F0B9, ("add", "dword ptr [r11 + 0xf0], eax")), (0x53EFC5, ("mov", "r11, qword ptr [rip + 0x2769ab4]"))]) and 0x53EFCC + 0x2769AB4 == 0x2CA8A80,   # r11 = [02CA8A80], the widget's cell
      "0053EFC0 appends a 0x14 record at +0xA90 + 0x14 * runCount, then increments runCount and advances +0xF0")
check("E", 0x110 + 64 * 4 == 0x210 and 0x210 + 64 * 2 == 0x290 and 0x290 + 256 * 4 == 0x690 and 0x690 + 256 * 4 == 0xA90 and 0xA90 + 128 * 0x14 == 0x1490,
      "five arrays tile +0x110..+0x148F by adjacency (64 / 64 / 256 / 256 / 128)")

FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/glyph-run-arrays-opus/glyph_run_arrays.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
G, RR = "GlyphRunWidget1498", "GlyphRunRecord14"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "CARVED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def cells(l): return l.rstrip("\r\n").split("\t")
RENAME = {0x105: ("markRangeBFirst", "the first index of the +0x110 / +0x210 array range 0053E640 walks"), 0x106: ("markRangeBEnd", "the end index of that range"),
          0x108: ("markRangeAFirst", "the first index of the +0x290 / +0x690 array range 0053E640 walks"), 0x10A: ("markRangeAEnd", "the end index of that range"),
          0x1490: ("runRangeFirst", "the first run index 0053E640 walks from"), 0x1492: ("runCount", "the next run index: 0053EFC0 appends at it and increments it; 0053E640 walks up to it")}
def rows_110(w):
    return [[G, "0x0110", "256", "markPositionsB", "uint32[64]", "positions 0053E640 compares (minus a base) with the cursor, indexed from markRangeBFirst to markRangeBEnd", P[0], P[1], ev("R E", w)],
            [G, "0x0210", "128", "markValuesB", "int16[64]", "the value 0053E640 takes (into +0xF8, kind 2) at the matching markPositionsB index", P[0], P[1], ev("R E", w)],
            [G, "0x0290", "1024", "markPositionsA", "uint32[256]", "positions 0053E640 compares with the cursor, indexed from markRangeAFirst to markRangeAEnd", P[0], P[1], ev("R E", w)],
            [G, "0x0690", "1024", "markValuesA", "uint32[256]", "the value 0053E640 takes (into +0xF8, kind 5) at the matching markPositionsA index", P[0], P[1], ev("R E", w)]]
RRROWS = [[RR, "0x00", "4", "textOffset", "uint32", "the widget's running offset (+0xF0) when 0053EFC0 appended the run; 0053E640 compares it (minus a base) with the cursor", P[0], P[1], "CARVED 2026-09-28 (OPUS, %s A R). %s" % (REC, EXE)],
          [RR, "0x04", "2", "word04", "int16", "written by 0053EFC0; 0053E640 takes it into +0xF8 (kind 6)", P[0], P[1], "CARVED 2026-09-28 (OPUS, %s A R). %s" % (REC, EXE)]] + \
         [[RR, "0x%02X" % o, "2", "word%02X" % o, "int16", "written by 0053EFC0 from its arguments scaled by two globals", P[0], "PROBABLE", "CARVED 2026-09-28 (OPUS, %s A). %s" % (REC, EXE)] for o in (6, 8, 0xA, 0xC, 0xE)] + \
         [[RR, "0x10", "2", "length10", "int16", "the appender's first argument; 0053E640 adds it to the run's position and caps it to set the cursor", P[0], P[1], "CARVED 2026-09-28 (OPUS, %s A R). %s" % (REC, EXE)],
          [RR, "0x12", "2", "unobservedSpan12", "u8[2]", "not written by 0053EFC0 nor read by 0053E640", U[0], U[1], "CARVED 2026-09-28 (OPUS, %s A R). %s" % (REC, EXE)]]
NEWT = [RR, "0x14", "99-Unresolved-Residual", "128 at GlyphRunWidget1498 +0xA90", "EMBEDDED in GlyphRunWidget1498", "0053EFC0 (append)", "not read here", P[0], P[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s A R E). Stride 0x14 from 0053EFC0 (`lea r10, [rax + rax*4]`, `[r11 + r10*4 + 0xa90]`) and 0053E640 (`add r8, 0x14`). %s" % (REC, EXE),
        "16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md", "EMBED GlyphRunWidget1498 +0x0A90 stride=0x14 count=128"]
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]
    g = {int(cells(l)[1], 16): cells(l) for l in fl if cells(l)[0] == G}
    assert g[0x110][2] == "2432" and g[0xAA2][2] == "2542" and g[0xA90][3] == "dword0A90"
    runwas = "; ".join("+0x%X %s %s (%s)" % (o, c[3], c[4], c[5][:60]) for o, c in sorted(g.items()) if 0xA90 <= o < 0x1490)
    out = []; rdone = False
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == G:
            o = int(c[1], 16)
            if o == 0x110: out += ["\t".join(x) + e for x in rows_110("%s %s (%s)" % (c[3], c[4], c[5][:120]))]; continue
            if 0xA90 <= o < 0x1490:
                if not rdone:
                    out.append("\t".join([G, "0x0A90", "2560", "runs", RR + "[128]", "the run records 0053EFC0 appends and 0053E640 walks from runRangeFirst to runCount", P[0], P[1], ev("A R E", runwas)]) + e); rdone = True
                continue
            if o in RENAME:
                nm, mean = RENAME[o]; c[8] += " || RENAMED 2026-09-28 (OPUS, %s R A): was %s" % (REC, c[3]); c[3] = nm; c[5] = mean + ". " + c[5]
                out.append("\t".join(c) + e); continue
        out.append(l)
    idx = max(i for i, l in enumerate(out) if cells(l)[0] == G); out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in RRROWS]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == RR for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == G); tl[ti + 1:ti + 1] = ["\t".join(NEWT) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
M = {int(c[1], 16): c for c in F if c[0] == G}
check("W", [M.get(o, [0] * 4)[3] for o in (0x110, 0x210, 0x290, 0x690, 0xA90, 0x105, 0x108, 0x1490, 0x1492)] ==
      ["markPositionsB", "markValuesB", "markPositionsA", "markValuesA", "runs", "markRangeBFirst", "markRangeAFirst", "runRangeFirst", "runCount"]
      and RR in T and sum(int(c[2]) for c in F if c[0] == RR) == 0x14 and sum(int(c[2]) for c in M.values()) == 0x1498,
      "the five arrays, GlyphRunRecord14 and the range fields are in the store; both types tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
