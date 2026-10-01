"""phyre_destroys2.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Seven more Phyre destroy cells
('descriptor destroy slot +0x58, form not reduced') read, and the bytes they settle.

  T  the four texture bases PTexture2DBase 005CE800, PTexture3DBase 005D4ED0, PTextureCommonBase 005D7200, PTextureCubeMapBase
     005D0CA0 share one body: when byte +0x08 is non-zero they pass 'A PTextureCommonBase object is being destroyed whilst still
     mapped' (00D4B350) to 005CDAA0 with level 3; then, when +0x20 (the bound render target) is non-null, they call the unlink
     006108C0 on it. So PTextureCommonBase +0x08 is the texture's mapped state (the engine's own message), a byte
  M  PSamplerStateD3D11 006132E0: releases +0x20 through vtable slot +0x10 and nulls it, clears bit 7 of PSamplerStateBase
     m_flags (+0x1C), then 0016D6A0
  N  PNameComponent 006AF910: +0x18 / +0x20 is an intrusive list link {next, prev}: it stores prev into next+8 and next into
     prev+0, then points both cells at the link itself; it frees m_name (+0x28) through 00584730 unless the pointer's bit 0 is
     set; then the PComponent destructor 006AAA50 (006ACA70 on [+8] with this when +8 is set)
  V  PShaderVertexProgramD3D11 006110B0: 0062BAB0 releases +0x90, +0x00 and +0x88 through vtable +0x10 and frees the +0x10 array
     (count +0x08, bit 31 keeps it); m_inputLayout's array (+0x80, count +0x78) goes to 00619070 unless bit 31 is set; then
     00616B40. So the gap +0x90 is an object released like the views
  S  REGRESSION: the seven cells are reduced and the four spans re-cut (FAILS before)
Usage: python phyre_destroys2.py [--patch]
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
MSG = b"A PTextureCommonBase object is being destroyed whilst still mapped\0"
t = d[off(0xD4B350):off(0xD4B350) + len(MSG)] == MSG
for f in (0x5CE800, 0x5D4ED0, 0x5D7200, 0x5D0CA0):
    t &= (A([(f + 0x12, ("cmp", "byte ptr [rdx + 8], 0")), (f + 0x1F, ("mov", "ecx, 3")), (f + 0x24, ("call", "0x5cdaa0")),
             (f + 0x29, ("mov", "rcx, qword ptr [rbx + 0x20]")), (f + 0x32, ("call", "0x6108c0"))]) and at(f + 0x18)[2] == 0xD4B350)
check("T", t, "texture bases: 'destroyed whilst still mapped' when byte +0x08 != 0, then unlink +0x20 through 006108C0")
check("M", A([(0x6132F2, ("mov", "rcx, qword ptr [rdx + 0x20]")), (0x6132FE, ("call", "qword ptr [rax + 0x10]")), (0x613301, ("mov", "qword ptr [rbx + 0x20], 0")),
              (0x613309, ("and", "dword ptr [rbx + 0x1c], 0xffffff7f")), (0x613313, ("call", "0x16d6a0"))]),
      "PSamplerStateD3D11: release +0x20, clear m_flags bit 7, base")
check("N", A([(0x6AF922, ("lea", "r8, [rdx + 0x18]")), (0x6AF926, ("mov", "rcx, qword ptr [r8]")), (0x6AF929, ("mov", "rax, qword ptr [r8 + 8]")),
              (0x6AF92D, ("mov", "qword ptr [rcx + 8], rax")), (0x6AF931, ("mov", "qword ptr [rax], rcx")), (0x6AF934, ("mov", "qword ptr [r8], r8")),
              (0x6AF937, ("mov", "qword ptr [r8 + 8], r8")), (0x6AF93B, ("mov", "rcx, qword ptr [rdx + 0x28]")), (0x6AF94C, ("call", "0x584730")),
              (0x6AF955, ("call", "0x6aaa50")), (0x6AAA5D, ("mov", "rax, qword ptr [rcx + 8]")), (0x6AAA6C, ("call", "0x6aca70"))]),
      "PNameComponent: unlink the {next, prev} link at +0x18, free m_name unless bit 0, PComponent destructor")
check("V", A([(0x6110C5, ("call", "0x62bab0")), (0x62BABF, ("mov", "rcx, qword ptr [rcx + 0x90]")), (0x62BACE, ("call", "qword ptr [rax + 0x10]")),
              (0x62BAD1, ("mov", "qword ptr [rbx + 0x90], rdi")), (0x62BAD8, ("mov", "rcx, qword ptr [rbx]")), (0x62BB0E, ("mov", "rcx, qword ptr [rbx + 0x88]")),
              (0x6110CB, ("mov", "edx, dword ptr [rbx + 0x78]")), (0x6110DD, ("mov", "rcx, qword ptr [rbx + 0x80]")), (0x6110E4, ("call", "0x619070")),
              (0x6110F8, ("call", "0x616b40"))]),
      "PShaderVertexProgramD3D11: 0062BAB0 releases +0x90 (and +0x00, +0x88), the input-layout array goes to 00619070, then 00616B40")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/d3d11-element-release/phyre_destroys2.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def cells(l): return l.rstrip("\r\n").split("\t")
def ev(was, tag): return "RE-CUT 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def cut(t, was):
    if t == "PTextureCommonBase":
        return [[t, "0x0008", "1", "mapped", "uint8", "the texture's mapped state: the four texture-base destroys pass 'A PTextureCommonBase object is being destroyed whilst still mapped' to 005CDAA0 (level 3) when it is non-zero. Its writers are not read here", "TYPE RESOLVED", "PROVEN", ev(was, "T")]]
    if t == "PSamplerStateD3D11":
        return [[t, "0x0020", "8", "releasedObject20", "void*", "an object released like the D3D11 views: the destroy 006132E0 calls its vtable slot +0x10 (the IUnknown Release position) and nulls it; which object it is is not established", "TYPE RESOLVED", "PROVEN", ev(was, "M")]]
    if t == "PNameComponent":
        return [[t, "0x0018", "8", "listNext", "void*", "the next link of an intrusive doubly linked list {next, prev} at +0x18: the destroy 006AF910 stores prev into next+8 and then points this cell at the link itself. Which list is not established", "TYPE RESOLVED", "PROVEN", ev(was, "N")],
                [t, "0x0020", "8", "listPrev", "void*", "the prev link of the same list: the destroy stores next into prev+0 and then points this cell at the link itself", "TYPE RESOLVED", "PROVEN", ev(was, "N")]]
    return [[t, "0x0090", "8", "releasedObject90", "void*", "an object released like the D3D11 views: 0062BAB0 (run first by the destroy 006110B0) calls its vtable slot +0x10 (the IUnknown Release position) and nulls it; which object it is is not established", "TYPE RESOLVED", "PROVEN", ev(was, "V")]]
SPAN = {("PTextureCommonBase", "0x0008", "1"), ("PSamplerStateD3D11", "0x0020", "8"), ("PNameComponent", "0x0018", "16"), ("PShaderVertexProgramD3D11", "0x0090", "8")}
DT = {t: "%s: when byte +0x08 (mapped) is non-zero it passes 'A PTextureCommonBase object is being destroyed whilst still mapped' to 005CDAA0 (level 3); then, when +0x20 (the bound render target) is set, it unlinks it through 006108C0 (T)" % f
      for t, f in (("PTexture2DBase", "005CE800"), ("PTexture3DBase", "005D4ED0"), ("PTextureCommonBase", "005D7200"), ("PTextureCubeMapBase", "005D0CA0"))}
DT["PSamplerStateD3D11"] = "006132E0: releases +0x20 through vtable +0x10 and nulls it, clears bit 7 of m_flags (+0x1C), then 0016D6A0 (M)"
DT["PNameComponent"] = "006AF910: unlinks the {next, prev} list link at +0x18 and self-links it, frees m_name (+0x28) through 00584730 unless the pointer's bit 0 is set, then the PComponent destructor 006AAA50 (006ACA70 on [+8] when set) (N)"
DT["PShaderVertexProgramD3D11"] = "006110B0: 0062BAB0 releases +0x90, +0x00 and +0x88 through vtable +0x10 and frees the +0x10 array (count +0x08); the m_inputLayout array (+0x80, count +0x78) goes to 00619070 unless bit 31 is set; then 00616B40 (V)"
FLAG7 = " || BIT 7 (2026-09-28, OPUS, %s M): PSamplerStateD3D11's destroy 006132E0 clears it after releasing its +0x20 object" % REC
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if (c[0], c[1], c[2]) in SPAN and c[3].startswith("unobservedSpan"):
            out += ["\t".join(r) + e for r in cut(c[0], "%s %s (%s)" % (c[3], c[4], c[5][:200]))]; continue
        if c[0] == "PSamplerStateBase" and c[3] == "m_flags" and REC not in c[5]: c[5] += FLAG7; l = "\t".join(c) + e
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in DT and c[6].endswith("descriptor destroy slot +0x58, form not reduced"):
            c[6] = "~~%s~~ %s - READ 2026-09-28 (OPUS, %s)" % (c[6], DT[c[0]], REC); tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
TYPES = [s[0] for s in SPAN]
have = {(r[0], int(r[1], 16)): r for r in F if r[0] in TYPES}
want = {("PTextureCommonBase", 8): "mapped", ("PSamplerStateD3D11", 0x20): "releasedObject20", ("PNameComponent", 0x18): "listNext",
        ("PNameComponent", 0x20): "listPrev", ("PShaderVertexProgramD3D11", 0x90): "releasedObject90"}
ok = all(have.get(k, [0, 0, 0, ""])[3] == v for k, v in want.items())
ok &= all(sum(int(r[2]) for k, r in have.items() if k[0] == t) == int(T[t][1], 16) for t in TYPES)
ok &= all(REC in T[t][6] for t in DT)
check("S", ok, "seven destroy cells reduced; four spans re-cut with tiling kept")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
