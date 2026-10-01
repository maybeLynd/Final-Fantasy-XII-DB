"""render_base.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
RenderContext02CC0410's +0x000..+0x0F3, the region 005DC0E0 initialises (its only caller is the context's constructor, at
00615863, so the rows stay the context's: no base class is claimed).

  C  005DC0E0: word +0 = 0, dword +4 = 0; 00808FE4(this + 8, 0x18, 8, 005DC1B0) - eight RenderContextRecord18, the record
     render_buffers.py typed at +0x570 (same element constructor); then qwords +0xC8 / +0xD0, dword +0xD8, word +0xE0, qwords
     +0xE8 / +0xF0 / +0xF8 / +0xF4 = 0, +0xFC = 0x400000 and +0x100 = 0x100000 (the UAV pair's default sizes)
  S  0079E4A0(this, rdx, a, b): byte +0 selects which buffer pair gets the requested sizes - non-zero: +0xF4 / +0xF8 = a / b and
     +0xFC / +0x100 = 0; zero: +0xF4 / +0xF8 = 0 and +0xFC / +0x100 = a / b (one 16-byte store at +0xF4); then the initialiser
     006253D0, and byte +1 = 1 when it returns 0. 0079F4A5 copies 16 bytes into +0xF4 and sets +1 the same way; 0079F070
     tests +1 before calling the teardown 0062B5A0
  V  0061CE30, when the requested count equals +0x6F8, copies the +0x700 array pointer into +0xE8 and the count into +0xF0;
     0079F4FA tests +0xE8
  W  REGRESSION (FAILS before): the rows are in the store and tile to +0xF4
Not claimed: the fields at +0x04 and +0xC8..+0xE7 (zeroed, no reader found); what the +0xE8 copy is for.
Usage: python render_base.py [--patch]
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
    miss = [hex(a) for a, v in pairs if A.get(a) != v]
    if miss: print("   missing", miss)
    return not miss
callers = []
for s in pe.sections:
    if s.Name.startswith(b".text"):
        buf = d[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]; base = B + s.VirtualAddress
        i = buf.find(b"\xE8")
        while i >= 0:
            if base + i + 5 + struct.unpack_from("<i", buf, i + 1)[0] == 0x5DC0E0: callers.append(base + i)
            i = buf.find(b"\xE8", i + 1)
check("C", callers == [0x615863]
      and has(0x5DC0E0, 0x5DC186, [(0x5DC0F1, ("mov", "word ptr [rcx], 0")), (0x5DC0F6, ("lea", "rbx, [rcx + 8]")), (0x5DC0FA, ("mov", "dword ptr [rcx + 4], esi")),
                                   (0x5DC10F, ("lea", "edx, [rsi + 0x18]")), (0x5DC117, ("lea", "r8d, [rsi + 8]")), (0x5DC11B, ("lea", "r9, [rip + 0x8e]")), (0x5DC122, ("call", "0x808fe4")),
                                   (0x5DC127, ("mov", "qword ptr [rbx + 0xc0], rsi")), (0x5DC131, ("mov", "qword ptr [rbx + 0xc8], rsi")), (0x5DC138, ("mov", "dword ptr [rbx + 0xd0], esi")),
                                   (0x5DC13E, ("mov", "word ptr [rbx + 0xd8], si")), (0x5DC14A, ("mov", "qword ptr [rdi + 0xf0], rsi")), (0x5DC151, ("mov", "qword ptr [rdi + 0xe8], rsi")),
                                   (0x5DC15F, ("mov", "qword ptr [rdi + 0xfc], 0x400000")), (0x5DC176, ("mov", "dword ptr [rdi + 0x100], 0x100000"))])
      and 0x5DC122 + 0x8E == 0x5DC1B0,
      "005DC0E0 (one caller, 00615863): +0 word, +4, eight 0x18 records from +8 (element constructor 005DC1B0), zeroed +0xC8..+0xF3, UAV default sizes")
check("S", has(0x79E4A0, 0x79E50B, [(0x79E4B7, ("mov", "edi, r9d")), (0x79E4BF, ("mov", "esi, r8d")), (0x79E4CC, ("cmp", "byte ptr [rbx], al")),
                                     (0x79E4D0, ("mov", "dword ptr [rsp + 0x20], esi")), (0x79E4D4, ("mov", "dword ptr [rsp + 0x24], edi")), (0x79E4D8, ("mov", "qword ptr [rsp + 0x28], rax")),
                                     (0x79E4DF, ("mov", "qword ptr [rsp + 0x20], rax")), (0x79E4E4, ("mov", "dword ptr [rsp + 0x28], esi")), (0x79E4E8, ("mov", "dword ptr [rsp + 0x2c], edi")),
                                     (0x79E4F7, ("movups", "xmmword ptr [rbx + 0xf4], xmm0")), (0x79E4FE, ("call", "0x6253d0")), (0x79E507, ("mov", "byte ptr [rbx + 1], 1"))])
      and has(0x79F49E, 0x79F4BD, [(0x79F4A5, ("movups", "xmmword ptr [rax + 0xf4], xmm0")), (0x79F4AC, ("call", "0x6253d0")), (0x79F4B7, ("mov", "byte ptr [rsi + 1], 1"))])
      and has(0x79F068, 0x79F07E, [(0x79F068, ("call", "0x624670")), (0x79F070, ("cmp", "byte ptr [rax + 1], 0")), (0x79F079, ("call", "0x62b5a0"))]),
      "byte +0 routes the requested sizes to the dynamic (+0xF4) or the UAV (+0xFC) pair; byte +1 = initialised, tested before the teardown")
check("V", has(0x61CE30, 0x61CF10, [(0x61CE4B, ("cmp", "edx, dword ptr [rcx + 0x6f8]")), (0x61CE51, ("je", "0x61cef6")), (0x61CEF6, ("mov", "rax, qword ptr [rsi + 0x700]")),
                                     (0x61CEFD, ("mov", "qword ptr [rsi + 0xe8], rax")), (0x61CF04, ("mov", "dword ptr [rsi + 0xf0], edi"))])
      and has(0x79F4F0, 0x79F504, [(0x79F4FA, ("cmp", "qword ptr [rsi + 0xe8], 0"))]),
      "+0xE8 / +0xF0 = a copy of the +0x700 array pointer and its count")
REC = "_index/candidates/render-context-02cc0410/render_base.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RC = "RenderContext02CC0410"
P, U, M = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN"), ("TYPE RESOLVED", "PROBABLE")
def r(o, sz, nm, ct, mean, rd, tag, was): return [RC, "0x%04X" % o, str(sz), nm, ct, mean, rd[0], rd[1], "CARVED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)]
def rows(w):
    return [r(0x00, 1, "dynamicSizesFlag", "uint8", "selects where 0079E4A0 puts the requested buffer sizes: non-zero, the dynamic pair +0xF4 / +0xF8; zero, the UAV pair +0xFC / +0x100 (the other pair keeps 0, which its creator reads as the default)", P, "C S", w),
            r(0x01, 1, "initialised", "uint8", "set to 1 when the initialiser 006253D0 returns 0 (0079E507, 0079F4B7); 0079F070 tests it before the teardown 0062B5A0", P, "S", w),
            r(0x02, 2, "unobservedSpan0002", "u8[2]", "not written by 005DC0E0 (its word store covers +0 and +1); no access found", U, "C", w),
            r(0x04, 4, "dword04", "uint32", "zeroed by 005DC0E0; no reader found", U, "C", w),
            r(0x08, 0xC0, "records08", "RenderContextRecord18[8]", "eight 0x18 records built by 00808FE4 with 005DC1B0, the element constructor of the +0x570 array", M, "C", w),
            r(0xC8, 8, "qwordC8", "uint64", "zeroed by 005DC0E0; no reader found", U, "C", w),
            r(0xD0, 8, "qwordD0", "uint64", "zeroed by 005DC0E0; no reader found", U, "C", w),
            r(0xD8, 4, "dwordD8", "uint32", "zeroed by 005DC0E0; no reader found", U, "C", w),
            r(0xDC, 4, "unobservedSpan00DC", "u8[4]", "not written; no access found", U, "C", w),
            r(0xE0, 2, "wordE0", "uint16", "zeroed by 005DC0E0; no reader found", U, "C", w),
            r(0xE2, 6, "unobservedSpan00E2", "u8[6]", "not written; no access found", U, "C", w),
            r(0xE8, 8, "records30Copy", "void*", "a copy of the +0x700 array pointer, stored by 0061CE30 when the requested count is unchanged; 0079F4FA tests it", P, "V", w),
            r(0xF0, 4, "records30CopyCount", "uint32", "the count stored with records30Copy (0061CF04)", P, "V", w)]
FI = os.path.join(DB, "_types", "fields.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []; hit = 0
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == RC and c[1] == "0x0000" and c[2] == "244":
            out += ["\t".join(x) + e for x in rows("%s %s (%s)" % (c[3], c[4], c[5][:160]))]; hit += 1; continue
        out.append(l)
    assert hit == 1
    open(FI, "wb").write("".join(out).encode("utf-8"))
    TY = os.path.join(DB, "_types", "types.tsv"); tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "RenderContextRecord18" and c[3] == "eight at RenderContext02CC0410 +0x570":
            c[3] = "sixteen in RenderContext02CC0410: eight at +0x08 (005DC0E0) and eight at +0x570"; c[10] += " || SECOND ARRAY 2026-09-28 (OPUS, %s C)" % REC; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
R = sorted((int(c[1], 16), int(c[2]), c[3]) for c in (cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()) if c[0] == RC and int(c[1], 16) < 0xF4)
T18 = next(cells(l) for l in open(os.path.join(DB, "_types", "types.tsv"), "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "RenderContextRecord18")
check("W", "+0x08" in T18[3] and [x[2] for x in R][:2] == ["dynamicSizesFlag", "initialised"] and all(a[0] + a[1] == b[0] for a, b in zip(R, R[1:])) and R[-1][0] + R[-1][1] == 0xF4,
      "the +0x000..+0x0F3 rows are in the store and tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
