"""render_primitive_state.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
PrimitiveRendererD3D11's four unobserved spans (+0x10, +0xC8, +0x848, +0x20868), from its vtable (00D86960) census and the
bodies it reaches. Only instructions whose displacement is the field itself are used.

  L  THE LATCH. 006C8920 (the renderer's frame latch) copies pending state into the copy the draw path reads: the dwords
     +0x10..+0x8C to +0x20868..+0x208E4 (the same order), +0x1A0 / +0x1A8 / +0x1B0 / +0x1B8 to +0x1C0 / +0x1C8 / +0x1D0 / +0x1D8,
     +0x1E8 / +0x1EC to +0x1E0 / +0x1E4, +0x208FC to +0x1F0, byte +0x208F7 to +0x85C, +0x208F8 to +0x870, +0x208E8 to +0x854,
     dword +0x208EC to +0x858, +0x851 to +0x850, +0x20920 to +0x20921, +0x20931 to +0x20930, the dirty bytes +0x208F1 / +0x208F3
     to +0x208F2 / +0x208F4 (then clears both), and the 16 bytes at +0x20900 to +0x20910. The map is derived from the body here
  S  THE SETTERS (vtable slots): 6 (006CAF40) copies 0x40 bytes from its argument to +0x10 and sets +0x208F3; 8 (006CAEB0) sets
     +0x1A0 / +0x1A8 / +0x1B0, +0x208FC, +0x208F7, +0x68 = (arg != 0), +0x6C = a byte argument as float, 16 bytes at +0x50 and 8
     at +0x60, and +0x208F1; 9 (006CAE90) +0x70 / +0x74 and +0x208F1; 10 (006CAC10) +0x1B8; 11 (006CAD90) byte +0x208E8 and float
     +0x208EC; 12 (006CADB0) +0x855 from a global; 15 (006CAB80) +0x7C and +0x208F1; 26 (006CAC40) floats +0x1E8 / +0x1EC; 7
     (006CAD30) +0x860 / +0x868; 32 (006CAD50) the rect +0x20900 = {x, y, x + w, y + h}, +0x20920 = (arg > 0), +0x208F0 = 1.
     Non-virtual: 006CAC30 byte +0x851 and word +0x852; 006CAE70 +0x80 / +0x84 and +0x208F1
  M  006C8920 then picks the pair +0x190 / +0x198 by +0x851 and the word +0x852: from +0x128 / +0x130, +0x140 / +0x130,
     +0x148 / +0x130 or +0x118 / +0x110
  W  REGRESSION (FAILS before): the spans are carved, the rows tile the type's first 0x208 bytes, +0x848..+0x880 and
     +0x20868..+0x20938
Not claimed: what the 0x40 block, the vec4, the pointers +0xC8..+0x200 and the bytes hold; the D3D11 objects behind the qwords
(no dereference is cited, so they stay uint64).
Usage: python render_primitive_state.py [--patch]
"""
import hashlib, os, re, struct, sys
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
def body(lo, hi): return list(cs.disasm(d[off(lo):off(hi)], lo))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in body(lo, hi)}
    miss = [hex(a) for a, v in pairs if A.get(a) != v]
    if miss: print("   missing", miss)
    return not miss
# L: derive the latch map from 006C8920 - each load from [rbx + a] followed by a store of the same register to [rbx + b]
MEM = re.compile(r"(byte|word|dword|qword|xmmword) ptr \[rbx \+ (0x[0-9a-f]+)\]")
latch = {}; last = {}
for x in body(0x6C8920, 0x6C8B54):
    if x.mnemonic in ("mov", "movzx", "movups") and "ptr [rbx +" in x.op_str:
        dst, src = [s.strip() for s in x.op_str.split(",", 1)]
        m = MEM.search(src)
        if m and not MEM.search(dst): last[dst.replace("eax", "rax").replace("xmm0", "xmm0")] = (int(m.group(2), 16), m.group(1)); continue
        m = MEM.search(dst)
        if m:
            reg = src.replace("eax", "rax").replace("al", "rax")
            if reg in last: latch[last[reg][0]] = (int(m.group(2), 16), m.group(1))
EXP = {o: (0x20868 + o - 0x10, "dword") for o in range(0x10, 0x90, 4)}
EXP.update({0x1A0: (0x1C0, "qword"), 0x1A8: (0x1C8, "qword"), 0x1B0: (0x1D0, "qword"), 0x1B8: (0x1D8, "qword"), 0x1E8: (0x1E0, "dword"),
            0x1EC: (0x1E4, "dword"), 0x208FC: (0x1F0, "dword"), 0x208F7: (0x85C, "byte"), 0x208F8: (0x870, "byte"), 0x208E8: (0x854, "byte"),
            0x208EC: (0x858, "dword"), 0x851: (0x850, "byte"), 0x20920: (0x20921, "byte"), 0x208F1: (0x208F2, "byte"), 0x208F3: (0x208F4, "byte"),
            0x20931: (0x20930, "byte"), 0x20900: (0x20910, "xmmword")})
check("L", latch == EXP and has(0x6C8B46, 0x6C8B54, [(0x6C8B46, ("mov", "byte ptr [rbx + 0x208f1], 0")), (0x6C8B4D, ("mov", "byte ptr [rbx + 0x208f3], 0"))]),
      "006C8920 latches %d fields (derived from its body); dirty bytes +0x208F1 / +0x208F3 cleared after" % len(latch))
vt = [struct.unpack_from("<Q", d, off(0xD86960) + 8 * i)[0] - IB + B for i in range(33)]
check("S", [vt[i] for i in (6, 7, 8, 9, 10, 11, 12, 15, 26, 32)] == [0x6CAF40, 0x6CAD30, 0x6CAEB0, 0x6CAE90, 0x6CAC10, 0x6CAD90, 0x6CADB0, 0x6CAB80, 0x6CAC40, 0x6CAD50]
      and has(0x6CAF40, 0x6CAFA9, [(0x6CAF42, ("mov", "dword ptr [rcx + 0x10], eax")), (0x6CAF9C, ("mov", "dword ptr [rcx + 0x4c], eax")), (0x6CAFA1, ("mov", "byte ptr [rcx + 0x208f3], 1"))])
      and has(0x6CAEB0, 0x6CAF37, [(0x6CAEB7, ("mov", "dword ptr [rcx + 0x208fc], eax")), (0x6CAEC2, ("mov", "byte ptr [rcx + 0x208f7], al")), (0x6CAECE, ("mov", "qword ptr [rcx + 0x1a0], rdx")),
                                   (0x6CAED5, ("mov", "qword ptr [rcx + 0x1b0], r9")), (0x6CAEDC, ("setne", "al")), (0x6CAEDF, ("mov", "dword ptr [rcx + 0x68], eax")),
                                   (0x6CAEE7, ("mov", "qword ptr [rcx + 0x1a8], r8")), (0x6CAEF2, ("cvtdq2ps", "xmm0, xmm0")), (0x6CAEF5, ("movss", "dword ptr [rcx + 0x6c], xmm0")),
                                   (0x6CAF01, ("mov", "dword ptr [r10 + 0x50], eax")), (0x6CAF1B, ("mov", "dword ptr [r10 + 0x5c], eax")), (0x6CAF21, ("mov", "dword ptr [r10 + 0x60], eax")),
                                   (0x6CAF28, ("mov", "dword ptr [r10 + 0x64], eax")), (0x6CAF2E, ("mov", "byte ptr [r10 + 0x208f1], 1"))])
      and has(0x6CAE90, 0x6CAEA1, [(0x6CAE90, ("mov", "dword ptr [rcx + 0x70], edx")), (0x6CAE95, ("mov", "dword ptr [rcx + 0x74], r8d")), (0x6CAE99, ("mov", "byte ptr [rcx + 0x208f1], 1"))])
      and has(0x6CAC10, 0x6CAC1A, [(0x6CAC10, ("mov", "qword ptr [rcx + 0x1b8], rdx"))])
      and has(0x6CAD90, 0x6CADA1, [(0x6CAD90, ("movss", "dword ptr [rcx + 0x208ec], xmm2")), (0x6CAD9A, ("mov", "byte ptr [rcx + 0x208e8], dl"))])
      and has(0x6CADB0, 0x6CADC9, [(0x6CADC0, ("mov", "byte ptr [rcx + 0x855], al"))])
      and has(0x6CAB80, 0x6CABB9, [(0x6CABA9, ("mov", "dword ptr [rbx + 0x7c], edx")), (0x6CABAC, ("mov", "byte ptr [rbx + 0x208f1], 1"))])
      and has(0x6CAC40, 0x6CAC8E, [(0x6CAC6F, ("movss", "dword ptr [rbx + 0x1ec], xmm6")), (0x6CAC80, ("movss", "dword ptr [rbx + 0x1e8], xmm2"))])
      and has(0x6CAD30, 0x6CAD41, [(0x6CAD30, ("mov", "qword ptr [rcx + 0x860], rdx")), (0x6CAD39, ("mov", "qword ptr [rcx + 0x868], r8"))])
      and has(0x6CAD50, 0x6CAD8A, [(0x6CAD50, ("lea", "eax, [rdx + r9]")), (0x6CAD54, ("mov", "dword ptr [rcx + 0x20900], edx")), (0x6CAD5E, ("add", "edx, r8d")),
                                   (0x6CAD61, ("mov", "dword ptr [rcx + 0x20908], eax")), (0x6CAD6C, ("mov", "dword ptr [rcx + 0x20904], r8d")), (0x6CAD73, ("seta", "al")),
                                   (0x6CAD76, ("mov", "dword ptr [rcx + 0x2090c], edx")), (0x6CAD7C, ("mov", "byte ptr [rcx + 0x20920], al")), (0x6CAD82, ("mov", "byte ptr [rcx + 0x208f0], 1"))])
      and has(0x6CAC30, 0x6CAC3F, [(0x6CAC30, ("mov", "byte ptr [rcx + 0x851], dl")), (0x6CAC36, ("mov", "word ptr [rcx + 0x852], r8w"))])
      and has(0x6CAE70, 0x6CAE84, [(0x6CAE70, ("mov", "dword ptr [rcx + 0x80], edx")), (0x6CAE76, ("mov", "dword ptr [rcx + 0x84], r8d")), (0x6CAE7D, ("mov", "byte ptr [rcx + 0x208f1], 1"))]),
      "the setters write the pending fields and mark +0x208F1 / +0x208F3 / +0x208F0")
check("M", has(0x6C8AFD, 0x6C8BEF, [(0x6C8B56, ("movzx", "ecx, word ptr [rbx + 0x852]")), (0x6C8B67, ("mov", "rax, qword ptr [rbx + 0x128]")), (0x6C8B6E, ("mov", "qword ptr [rbx + 0x190], rax")),
                                     (0x6C8B75, ("mov", "rax, qword ptr [rbx + 0x130]")), (0x6C8B7C, ("mov", "qword ptr [rbx + 0x198], rax")), (0x6C8B89, ("mov", "rax, qword ptr [rbx + 0x140]")),
                                     (0x6C8BAB, ("mov", "rax, qword ptr [rbx + 0x148]")), (0x6C8BCD, ("mov", "rax, qword ptr [rbx + 0x118]")), (0x6C8BDB, ("mov", "rax, qword ptr [rbx + 0x110]"))]),
      "+0x190 / +0x198 chosen by +0x851 / +0x852 from four pairs")

REC = "_index/candidates/render-context-02cc0410/render_primitive_state.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
T = "PrimitiveRendererD3D11"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
LAT = "latched by 006C8920 into +0x%X"
def pend(o, n, nm, ct, m, lat=None): return (o, n, nm, ct, m + ("; " + LAT % lat if lat is not None else ""), P)
def gap(o, n, why="no access found by the vtable census"): return (o, n, "unobservedSpan%X" % o, "u8[%d]" % n, why, U)
S10 = [pend(0x10, 0x40, "block10", "uint32[16]", "64 bytes vtable slot 6 (006CAF40) copies from its argument as dwords, marking +0x208F3", 0x20868),
       pend(0x50, 16, "vec50", "uint32[4]", "16 bytes slot 8 copies from a stack argument; 006CB338 reads its first byte", 0x208A8),
       pend(0x60, 8, "pair60", "uint32[2]", "8 bytes slot 8 copies from a stack argument; 006CB344 reads its first byte", 0x208B8),
       pend(0x68, 4, "flag68", "uint32", "slot 8: 1 when its fourth stack argument is non-zero; 006CB323 compares it", 0x208C0),
       pend(0x6C, 4, "value6C", "float", "slot 8: a byte argument converted to float; 006CB328 reads it as float", 0x208C4),
       pend(0x70, 4, "dword70", "uint32", "slot 9 (006CAE90) edx, marking +0x208F1", 0x208C8),
       pend(0x74, 4, "dword74", "uint32", "slot 9 r8d", 0x208CC),
       pend(0x78, 4, "dword78", "uint32", "no writer found", 0x208D0),
       pend(0x7C, 4, "dword7C", "uint32", "slot 15 (006CAB80) from a stack argument, marking +0x208F1", 0x208D4),
       pend(0x80, 4, "dword80", "uint32", "006CAE70 edx, marking +0x208F1; 006CB39D compares it", 0x208D8),
       pend(0x84, 4, "dword84", "uint32", "006CAE70 r8d", 0x208DC),
       pend(0x88, 4, "dword88", "uint32", "no writer found", 0x208E0),
       pend(0x8C, 4, "dword8C", "uint32", "written by 006CB301", 0x208E4),
       gap(0x90, 16),
       pend(0xA0, 4, "dwordA0", "uint32", "read by 006CA6F4 and 006CB5AA, zeroed at 006CB5C5"),
       gap(0xA4, 12),
       pend(0xB0, 4, "dwordB0", "uint32", "read by 006CA684 and 006CB55A, zeroed at 006CB575"),
       gap(0xB4, 4)]
def q(o, m, lat=None): return pend(o, 8, "qword%X" % o, "uint64", m, lat)
SC8 = [q(0xC8, "read by the draw body at 006C8D24 (006C9262, 006C95A3)"), q(0xD0, "read by 006C8D24 (4 sites)"), q(0xD8, "read by 006C8D24 and 006CA84C / 006CA891"),
       q(0xE0, "read by 006C8D24 (2 sites)"), q(0xE8, "read by 006C8D24 (006C963E)"), q(0xF0, "read by 006C8D24 (006C92DC)"), q(0xF8, "read by 006C8D24 (006C9635)"),
       q(0x100, "read by 006C8CA0 (006C8D57)"), q(0x108, "read by 006C8CA0 (006C8D69)"), q(0x110, "the second of the pair 006C8920 copies to +0x198 in its fourth case"),
       q(0x118, "the first of that pair (to +0x190)"), gap(0x120, 8), q(0x128, "copied to +0x190 by 006C8920 (mode case 3)"),
       q(0x130, "copied to +0x198 by 006C8920 in three cases"), q(0x138, "read by 006C8D24 (006C9688)"), q(0x140, "copied to +0x190 (mode case 2)"),
       q(0x148, "copied to +0x190 (mode case 1)"), q(0x150, "read by 006C8D24 (006C938A)"), q(0x158, "read by 006C8D24 (2 sites)"),
       q(0x160, "written by 006C8D24 at five sites and compared / read there"), q(0x168, "written and compared by 006C8D24 (8 sites)"),
       q(0x170, "written at 006C8E01, read at 006C971A"), q(0x178, "read by 006C8D24 (006C9130)"), q(0x180, "read by 006C8D24 (006C915B)"), gap(0x188, 8),
       q(0x190, "the selected first of a pair (006C8920, by +0x851 / +0x852); read by 006C8D24"), q(0x198, "the selected second of that pair"),
       q(0x1A0, "slot 8 rdx", 0x1C0), q(0x1A8, "slot 8 r8", 0x1C8), q(0x1B0, "slot 8 r9", 0x1D0), q(0x1B8, "slot 10 (006CAC10) rdx", 0x1D8),
       q(0x1C0, "the latched +0x1A0; read by 006C8D24, compared by 006CB307"), q(0x1C8, "the latched +0x1A8"), q(0x1D0, "the latched +0x1B0"), q(0x1D8, "the latched +0x1B8"),
       pend(0x1E0, 4, "latched1E8", "float", "the latched +0x1E8; 006CB411 reads it as float"), pend(0x1E4, 4, "latched1EC", "float", "the latched +0x1EC"),
       pend(0x1E8, 4, "value1E8", "float", "slot 26 (006CAC40): its float argument / (a constant / 0017FFD0())", 0x1E0), pend(0x1EC, 4, "value1EC", "float", "slot 26: its float argument / a constant", 0x1E4),
       pend(0x1F0, 4, "latched208FC", "uint32", "the latched +0x208FC; read by 006C8D24"), gap(0x1F4, 4),
       q(0x1F8, "written and read by 006C8D24"), q(0x200, "read by 006C8D24 (3 sites)")]
S848 = [q(0x848, "read at 28 sites across the renderer's methods"),
        pend(0x850, 1, "latched851", "uint8", "the latched +0x851; 006CB4B6 compares it"), pend(0x851, 1, "mode851", "uint8", "set by 006CAC30 (dl); picks the +0x190 pair with +0x852", 0x850),
        pend(0x852, 2, "mode852", "uint16", "set by 006CAC30 (r8w); 006C8920 switches on it"), pend(0x854, 1, "latched208E8", "uint8", "the latched +0x208E8; compared by 006C8D24"),
        pend(0x855, 1, "byte855", "uint8", "set by slot 12 (006CADB0) from a global; read by slot 13 (006C9C30) and 006C8D24"), gap(0x856, 2),
        pend(0x858, 4, "latched208EC", "float", "the latched +0x208EC; read as float by 006C8D24 and 006CB3E3"), pend(0x85C, 1, "latched208F7", "uint8", "the latched +0x208F7; read by 006C8D24"),
        gap(0x85D, 3), q(0x860, "slot 7 (006CAD30) rdx; read by 006C8D24"), q(0x868, "slot 7 r8; read by 006C8D24"),
        pend(0x870, 1, "latched208F8", "uint8", "the latched +0x208F8; compared by 006C8D24"), gap(0x871, 15)]
SL = [pend(0x20868, 0x40, "latched10", "uint32[16]", "the latched +0x10 block (006C8920)"), pend(0x208A8, 16, "latched50", "uint32[4]", "the latched +0x50; 006CB33C compares its first byte"),
      pend(0x208B8, 8, "latched60", "uint32[2]", "the latched +0x60; 006CB348 compares its first byte"), pend(0x208C0, 4, "latched68", "uint32", "the latched +0x68; read by 006CB31D"),
      pend(0x208C4, 4, "latched6C", "float", "the latched +0x6C; 006CB32D compares it as float"), pend(0x208C8, 4, "latched70", "uint32", "the latched +0x70"),
      pend(0x208CC, 4, "latched74", "uint32", "the latched +0x74"), pend(0x208D0, 4, "latched78", "uint32", "the latched +0x78; 006C9847 compares it, 006C98B6 overwrites it"),
      pend(0x208D4, 4, "latched7C", "uint32", "the latched +0x7C; read by 006C8D24 at five sites"), pend(0x208D8, 4, "latched80", "uint32", "the latched +0x80; compared by 006C8D24 at five sites"),
      pend(0x208DC, 4, "latched84", "uint32", "the latched +0x84"), pend(0x208E0, 4, "latched88", "float", "the latched +0x88; 006C9857 compares it as float, 006C98A7 overwrites it"),
      pend(0x208E4, 4, "latched8C", "uint32", "the latched +0x8C; compared and overwritten by 006C8D24, read by 006CB2FB"),
      pend(0x208E8, 1, "byte208E8", "uint8", "slot 11 (006CAD90) dl", 0x854), gap(0x208E9, 3),
      pend(0x208EC, 4, "value208EC", "float", "slot 11 xmm2", 0x858),
      pend(0x208F0, 1, "rectDirty", "uint8", "set to 1 by slot 32 when the rect changes; tested by 006C88B6, cleared at 006C88F8"),
      pend(0x208F1, 1, "stateDirty", "uint8", "set to 1 by slots 8 / 9 / 15 and 006CAE70; cleared by 006C8920 after latching", 0x208F2),
      pend(0x208F2, 1, "stateDirtyLatched", "uint8", "the latched +0x208F1; tested by 006C8D24"),
      pend(0x208F3, 1, "blockDirty", "uint8", "set to 1 by slot 6; cleared by 006C8920 after latching", 0x208F4),
      pend(0x208F4, 1, "blockDirtyLatched", "uint8", "the latched +0x208F3; tested and cleared by 006C8D24"), gap(0x208F5, 2),
      pend(0x208F7, 1, "byte208F7", "uint8", "slot 8 from a stack argument", 0x85C), pend(0x208F8, 1, "byte208F8", "uint8", "compared by 006CB4EB", 0x870), gap(0x208F9, 3),
      pend(0x208FC, 4, "dword208FC", "uint32", "slot 8 from a stack argument", 0x1F0),
      pend(0x20900, 16, "rect", "int32[4]", "slot 32 (006CAD50): {x, y, x + w, y + h}, the D3D11_RECT order; 006CB477 / 006CB487 read it as two qwords", 0x20910),
      pend(0x20910, 16, "rectLatched", "int32[4]", "the latched +0x20900 (one 16-byte copy); 006CB470 / 006CB480 read it as two qwords"),
      pend(0x20920, 1, "rectEnable", "uint8", "slot 32: 1 when its stack argument is positive", 0x20921), pend(0x20921, 1, "rectEnableLatched", "uint8", "the latched +0x20920; 006CB45A compares it"),
      gap(0x20922, 14), pend(0x20930, 1, "latched20931", "uint8", "the latched +0x20931; tested by 006C98FF"),
      pend(0x20931, 1, "byte20931", "uint8", "set to 1 at 006CA7C9, stored at 006CB44A", 0x20930), gap(0x20932, 2),
      pend(0x20934, 4, "dword20934", "uint32", "written by 006C8905, read by 006C9A23")]
SPANS = {0x10: (168, S10), 0xC8: (320, SC8), 0x848: (56, S848), 0x20868: (208, SL)}
FI = os.path.join(DB, "_types", "fields.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
def row(o, n, nm, ct, m, rd, was): return [T, "0x%05X" % o, str(n), nm, ct, m, rd[0], rd[1], "CARVED 2026-09-28 (OPUS, %s L S M). was %s. %s" % (REC, was, EXE)]
tiles = all(sum(r[1] for r in rows) == n and all(a[0] + a[1] == b[0] for a, b in zip(rows, rows[1:])) and rows[0][0] == o for o, (n, rows) in SPANS.items())
if "--patch" in sys.argv:
    assert tiles
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []; hit = set()
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == T and int(c[1], 16) in SPANS and c[3].startswith("unobservedSpan") and int(c[2]) == SPANS[int(c[1], 16)][0]:
            was = "%s %s (%s)" % (c[3], c[4], c[5][:120])
            out += ["\t".join(row(*r, was)) + e for r in SPANS[int(c[1], 16)][1]]; hit.add(int(c[1], 16)); continue
        out.append(l)
    assert hit == set(SPANS), hit
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
R = sorted((int(c[1], 16), int(c[2]), c[3]) for c in (cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()) if c[0] == T)
names = {o: nm for o, n, nm in R}
check("W", tiles and names.get(0x10) == "block10" and names.get(0x20900) == "rect" and names.get(0x848) == "qword848" and names.get(0x208F1) == "stateDirty"
      and all(a[0] + a[1] == b[0] for a, b in zip(R, R[1:])),
      "the four spans are carved and the type's rows tile")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
