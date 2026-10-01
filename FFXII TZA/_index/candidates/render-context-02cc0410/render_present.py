"""render_present.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
RenderContext02CC0410's +0x1820..+0x18BF: a sampler, the viewport and target size, and the DXGI adapter / output state.
Found from the census seeded at the getter's jmp alias 00624670; kept only where the instruction's displacement is the
context offset itself (the census over-projects the +0xB50 pass-state loop at 00624E95 one iteration, onto +0x1820..+0x187C).

  S  +0x1820 is a PSamplerStateD3D11: the context's constructor runs 005DC400 on it and clears its +0x20 (00615AE4 /
     00615AE9) - the body of PSamplerStateD3D11's constructor 00615CD0 and of its descriptor's placement constructor
     006135E0 (vtable 00D500E8 slot +0x50; slot +0x58 is its destroy 006132E0). 0061D9C0 builds a D3D11 sampler from its
     bytes and CreateSamplerState (device slot +0xB8) stores the sampler at its +0x20; the teardown releases +0x1840 and
     clears bit 7 of +0x183C exactly as 006132E0 does. Extent 0x28: +0x1848 is written separately
  M  0062AAB0(this, mode, n): mode 0 / 1 / 2 writes the word +0x1848 = 0 / 1 / 0x101 and +0x184C = n; 00625D79 stores a byte
     at +0x1848, 006257BD reads it. 00625DA7 stores clock() (00625D80, the CRT import) converted to double at +0x1850
  V  at each resize (00625CC3.. and 00627AF2..) +0x185C = 0 (one qword), +0x1864 / +0x186C = width, +0x1868 / +0x1870 =
     height; 0061D3D0(this, x, y, w, h) builds a D3D11_VIEWPORT with TopLeftY = [+0x1870] - y - h and calls
     RSSetViewports (device context +0x110, slot +0x160) - so +0x1870 is the target height the viewport is flipped against
  A  +0x1878 is the DXGI factory: 00623C10 enumerates adapters through its slot +0x38 (EnumAdapters) and hands out +0x18AC
     and +0x18B0; the adapter scan (00625590..) keeps the chosen IDXGIAdapter at +0x1880 (replacing and releasing the old
     one) with its index - 1 at +0x18AC and ORs a rotating bit into +0x18B0. 006242C0 takes output [+0x1894] through the
     adapter's slot +0x38 (EnumOutputs), GetDisplayModeList (slot +0x40, format 0x1C) and GetDesc (slot +0x38): +0x1898 =
     the output's HMONITOR (DXGI_OUTPUT_DESC +0x58), +0x18A0 = its mode count. The teardown releases +0x1880 and +0x1878
  F  +0x1890 = 1 when the swap chain (+0x118) reports full screen (GetFullscreenState, slot +0x58), else 0; 0062B250 tests
     it for 1. +0x18A8 = 8 / 0017ECE0() when 00180170 returns false (meaning not claimed)
  W  REGRESSION (FAILS before): the rows are in the store
Not claimed: what mode 0 / 1 / 2 selects; the meaning of +0x18A8; what 0017ECE0 returns.
Usage: python render_present.py [--patch]
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
pe = pefile.PE(EXEP, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
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
q = lambda va: struct.unpack_from("<Q", d, off(va))[0] - IB + B
check("S", has(0x615AD5, 0x615AF5, [(0x615AD5, ("lea", "rbx, [rbp + 0x1820]")), (0x615AE4, ("call", "0x5dc400")), (0x615AE9, ("mov", "qword ptr [rbx + 0x20], r14")),
                                     (0x615AED, ("mov", "word ptr [rbp + 0x1848], r14w"))])
      and has(0x615CD0, 0x615CEF, [(0x615CD9, ("call", "0x5dc400")), (0x615CE1, ("mov", "qword ptr [rbx + 0x20], 0"))])
      and has(0x6135E0, 0x613618, [(0x613603, ("call", "0x5dc400")), (0x613608, ("mov", "qword ptr [rbx + 0x20], 0"))])
      and q(0xD500E8 + 0x50) == 0x6135E0 and q(0xD500E8 + 0x58) == 0x6132E0
      and has(0x6132E0, 0x613321, [(0x6132F2, ("mov", "rcx, qword ptr [rdx + 0x20]")), (0x6132FE, ("call", "qword ptr [rax + 0x10]")), (0x613309, ("and", "dword ptr [rbx + 0x1c], 0xffffff7f"))])
      and has(0x62B677, 0x62B69C, [(0x62B677, ("mov", "rcx, qword ptr [rbx + 0x1840]")), (0x62B688, ("call", "qword ptr [rax + 0x10]")), (0x62B692, ("and", "dword ptr [rbx + 0x183c], 0xffffff7f"))])
      and has(0x61D9C0, 0x61DB7D, [(0x61D9DE, ("cmp", "qword ptr [rcx + 0x20], 0")), (0x61DA02, ("mov", "r11d, dword ptr [rbx + 0x1c]")), (0x61DA22, ("cvttss2si", "rbp, dword ptr [rbx + 0xc]")),
                                   (0x61DAFC, ("movss", "xmm0, dword ptr [rbx + 8]")), (0x61DB1C, ("lea", "r8, [rbx + 0x20]")), (0x61DB77, ("call", "qword ptr [rax + 0xb8]"))]),
      "+0x1820: PSamplerStateD3D11 (constructor body 005DC400 + clear +0x20, descriptor 00D500E8 slots +0x50 / +0x58), its sampler created into +0x20")
check("M", has(0x62AAB0, 0x62AAF7, [(0x62AAC0, ("mov", "word ptr [rcx + 0x1848], 0x101")), (0x62AAC9, ("mov", "dword ptr [rcx + 0x184c], r8d")),
                                     (0x62AAD1, ("mov", "word ptr [rcx + 0x1848], 1")), (0x62AAE4, ("mov", "word ptr [rcx + 0x1848], 0"))])
      and has(0x625D72, 0x625DB0, [(0x625D79, ("mov", "byte ptr [r14 + 0x1848], al")), (0x625D80, ("call", "qword ptr [rip + 0x29d2e2]")), (0x625DA3, ("cvtdq2pd", "xmm0, xmm0")),
                                   (0x625DA7, ("movsd", "qword ptr [r14 + 0x1850], xmm0"))])
      and has(0x6257B5, 0x6257D9, [(0x6257BD, ("movzx", "eax, byte ptr [rbx + 0x1848]")), (0x6257D4, ("call", "0x625830"))]),
      "+0x1848 mode bytes (0 / 1 / 0x101) with +0x184C; +0x1850 = clock() as double")
imp = [i.name for e in pefile.PE(EXEP).DIRECTORY_ENTRY_IMPORT for i in e.imports if i.address - IB + B == 0x625D86 + 0x29D2E2]
check("M2", imp == [b"clock"], "the import at 008C3068 is %s" % imp)
check("V", has(0x625CC1, 0x625CFB, [(0x625CC3, ("mov", "dword ptr [r14 + 0x186c], r13d")), (0x625CCD, ("mov", "qword ptr [r14 + 0x185c], rsi")),
                                     (0x625CD7, ("mov", "dword ptr [r14 + 0x1870], r15d")), (0x625CE0, ("mov", "dword ptr [r14 + 0x1864], r13d")),
                                     (0x625CEA, ("mov", "dword ptr [r14 + 0x1868], r15d")), (0x625CF6, ("call", "0x61d3d0"))])
      and has(0x627AEF, 0x627B1D, [(0x627AF2, ("mov", "dword ptr [rdi + 0x186c], r15d")), (0x627AFC, ("mov", "dword ptr [rdi + 0x1870], r14d")),
                                   (0x627B05, ("mov", "qword ptr [rdi + 0x185c], r13")), (0x627B0F, ("mov", "dword ptr [rdi + 0x1864], r15d")), (0x627B16, ("mov", "dword ptr [rdi + 0x1868], r14d"))])
      and has(0x61D3D0, 0x61D482, [(0x61D403, ("mov", "eax, dword ptr [rcx + 0x1870]")), (0x61D40D, ("sub", "eax, r8d")), (0x61D413, ("sub", "eax, ecx")),
                                   (0x61D43D, ("mov", "rcx, qword ptr [r10 + 0x110]")), (0x61D46A, ("call", "qword ptr [rax + 0x160]"))]),
      "+0x185C..+0x1870: the resize writes origin 0, width, height twice; 0061D3D0 flips the viewport against +0x1870 and calls RSSetViewports")
check("A", has(0x623C10, 0x623CA2, [(0x623C1A, ("mov", "eax, dword ptr [rcx + 0x18ac]")), (0x623C29, ("mov", "eax, dword ptr [rcx + 0x18b0]")),
                                     (0x623C32, ("mov", "rcx, qword ptr [rcx + 0x1878]")), (0x623C56, ("call", "qword ptr [rax + 0x38]"))])
      and has(0x625693, 0x62577F, [(0x625698, ("or", "dword ptr [rbx + 0x18b0], eax")), (0x6256F2, ("mov", "qword ptr [rbx + 0x1880], rax")),
                                   (0x62570B, ("mov", "dword ptr [rbx + 0x18ac], eax")), (0x625749, ("mov", "qword ptr [rbx + 0x1880], rax")),
                                   (0x625766, ("mov", "rcx, qword ptr [rbx + 0x1878]")), (0x625777, ("call", "qword ptr [rax + 0x38]"))])
      and has(0x6242C0, 0x624482, [(0x624307, ("mov", "rcx, qword ptr [rcx + 0x1880]")), (0x62430E, ("mov", "edx, dword ptr [rdi + 0x1894]")), (0x624317, ("call", "qword ptr [rax + 0x38]")),
                                   (0x624336, ("lea", "edx, [r8 + 0x1c]")), (0x62433A, ("call", "qword ptr [rax + 0x40]")), (0x6243DC, ("mov", "dword ptr [rcx + 0x1894], edx")),
                                   (0x62441B, ("call", "qword ptr [rax + 0x38]")), (0x62442E, ("mov", "r8, qword ptr [rsp + 0x98]")),
                                   (0x624448, ("mov", "qword ptr [rdi + 0x1898], r8")), (0x624452, ("mov", "dword ptr [rdi + 0x18a0], r9d"))])
      and has(0x62B74F, 0x62B781, [(0x62B74F, ("mov", "rcx, qword ptr [rbx + 0x1880]")), (0x62B75E, ("call", "qword ptr [rax + 0x10]")),
                                   (0x62B768, ("mov", "rcx, qword ptr [rbx + 0x1878]")), (0x62B777, ("call", "qword ptr [rax + 0x10]"))]),
      "+0x1878 factory (EnumAdapters), +0x1880 adapter (EnumOutputs), +0x1894 output index, +0x1898 HMONITOR, +0x18A0 mode count, +0x18AC / +0x18B0")
check("F", has(0x62985A, 0x629897, [(0x62985A, ("mov", "rcx, qword ptr [rdi + 0x118]")), (0x62986F, ("call", "qword ptr [rax + 0x58]")),
                                     (0x629877, ("mov", "dword ptr [rdi + 0x1890], 1")), (0x629883, ("mov", "dword ptr [rdi + 0x1890], esi"))])
      and has(0x62B250, 0x62B264, [(0x62B254, ("cmp", "dword ptr [rcx + 0x1890], 1"))])
      and has(0x6278C1, 0x6278E3, [(0x6278C4, ("call", "0x17ece0")), (0x6278CB, ("call", "0x180170")), (0x6278D6, ("mov", "eax, 8")), (0x6278DB, ("div", "ebx")),
                                   (0x6278DD, ("mov", "dword ptr [rdi + 0x18a8], eax"))]),
      "+0x1890 full-screen flag from GetFullscreenState; +0x18A8 = 8 / 0017ECE0()")

REC = "_index/candidates/render-context-02cc0410/render_present.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RC = "RenderContext02CC0410"
P, U, M = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN"), ("TYPE RESOLVED", "PROBABLE")
def ev(tag, was): return "CARVED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(o, sz, nm, ct, mean, rd, tag, was): return [RC, "0x%04X" % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
def rows1820(w):
    return [r(0x1820, 0x28, "sampler1820", "PSamplerStateD3D11", "a PSamplerStateD3D11 built in place (005DC400, then +0x20 cleared - its constructor 00615CD0's body); 0061D9C0 creates its D3D11 sampler into +0x20", P, "S", w),
            r(0x1848, 1, "modeByte1848", "uint8", "0 / 1 / 1 for modes 0 / 1 / 2 of 0062AAB0 (a word store with +0x1849); 00625D79 stores a byte here and 006257BD passes it to 00625830", P, "M", w),
            r(0x1849, 1, "modeByte1849", "uint8", "1 only for mode 2 of 0062AAB0 (the word 0x101)", P, "M", w),
            r(0x184A, 2, "unobservedSpan184A", "u8[2]", "no access found", U, "M", w)]
def rows1850(w):
    return [r(0x1850, 8, "initClock", "double", "clock() at initialisation, converted to double (00625D80 / 00625DA7)", P, "M", w),
            r(0x1858, 4, "unobservedSpan1858", "u8[4]", "no access found", U, "V", w),
            r(0x185C, 8, "viewportOrigin", "uint32[2]", "x, y: zeroed as one qword at each resize (00625CCD, 00627B05)", P, "V", w),
            r(0x1864, 4, "viewportWidth", "uint32", "the width stored at each resize, beside viewportOrigin", M, "V", w),
            r(0x1868, 4, "viewportHeight", "uint32", "the height stored at each resize", M, "V", w),
            r(0x186C, 4, "targetWidth", "uint32", "the width stored again at each resize", M, "V", w),
            r(0x1870, 4, "targetHeight", "uint32", "the height 0061D3D0 flips each viewport against (TopLeftY = targetHeight - y - h) before RSSetViewports", P, "V", w),
            r(0x1874, 4, "unobservedSpan1874", "u8[4]", "no access found", U, "V", w),
            r(0x1878, 8, "dxgiFactory", "void*", "the DXGI factory: EnumAdapters (slot +0x38) in 00623C10 and the adapter scan; released by the teardown", P, "A", w),
            r(0x1880, 8, "dxgiAdapter", "void*", "the chosen IDXGIAdapter (the scan releases and replaces it); EnumOutputs (slot +0x38) in 006242C0; released by the teardown", P, "A", w),
            r(0x1888, 8, "unobservedSpan1888", "u8[8]", "no access found", U, "A", w),
            r(0x1890, 4, "fullscreen", "uint32", "1 when the swap chain at +0x118 reports full screen (GetFullscreenState, slot +0x58), else 0; 0062B250 tests it", P, "F", w),
            r(0x1894, 4, "outputIndex", "uint32", "the output 006242C0 enumerates from the adapter (a 1-based argument stored decremented)", P, "A", w),
            r(0x1898, 8, "outputMonitor", "void*", "the output's HMONITOR (DXGI_OUTPUT_DESC +0x58, from GetDesc)", P, "A", w),
            r(0x18A0, 4, "outputModeCount", "uint32", "the output's display-mode count (GetDisplayModeList, format 0x1C)", P, "A", w)]
def rows18A8(w):
    return [r(0x18A8, 4, "value18A8", "uint32", "8 / 0017ECE0() when 00180170 returns false (006278DD); meaning not claimed", M, "F", w),
            r(0x18AC, 4, "adapterIndex", "uint32", "the chosen adapter's index (the scan stores index - 1 with the adapter); 00623C10 hands it out", P, "A", w),
            r(0x18B0, 4, "adapterMask", "uint32", "one bit per adapter the scan accepts (a rotating bit ORed in); 00623C10 hands it out", P, "A", w),
            r(0x18B4, 12, "unobservedSpan18B4", "u8[12]", "no access found; the bytes before the +0x18C0 renderer", U, "A", w)]
FI = os.path.join(DB, "_types", "fields.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []; hit = set()
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == RC and (c[1], c[2]) in (("0x1820", "44"), ("0x1850", "84"), ("0x18A8", "24")):
            was = "%s %s (%s)" % (c[3], c[4], c[5][:160])
            out += ["\t".join(x) + e for x in {"0x1820": rows1820, "0x1850": rows1850, "0x18A8": rows18A8}[c[1]](was)]; hit.add(c[1]); continue
        out.append(l)
    assert hit == {"0x1820", "0x1850", "0x18A8"}, hit
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
R = {int(c[1], 16): c for c in (cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()) if c[0] == RC}
ok = all(o in R and R[o][3] == n for o, n in ((0x1820, "sampler1820"), (0x1850, "initClock"), (0x1870, "targetHeight"), (0x1878, "dxgiFactory"), (0x1880, "dxgiAdapter"),
                                              (0x1890, "fullscreen"), (0x18AC, "adapterIndex"), (0x184C, "swapChainBufferCount"), (0x18A4, "refreshRate")))
ends = sorted((o, o + int(c[2])) for o, c in R.items() if 0x1820 <= o < 0x18C0)
check("W", ok and all(a[1] == b[0] for a, b in zip(ends, ends[1:])) and ends[0][0] == 0x1820 and ends[-1][1] == 0x18C0,
      "the +0x1820..+0x18BF rows are in the store and tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
