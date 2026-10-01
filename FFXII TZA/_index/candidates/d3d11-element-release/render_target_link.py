"""render_target_link.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The render target's link to its
texture, read from the construct / release / unlink code. It replaces three unregistered spans: PRenderTargetBase +0x00..+0x08,
PTextureCommonBase +0x1C..+0x27 and PRenderTargetD3D11 +0x10..+0x4F.

  K1 the kind switch: 006505A0 reads byte [rt+8] and, for 0 / 1 / 2, passes [rt+0] to the 2D / 3D / cube release pass
     (0062BCB0 / 0062BF40 / 0062C100) behind that class's created-flag getter; the unlink 006108C0 switches on the same byte and,
     when [rt+0] is non-null and [[rt+0]+0x20] == rt, clears bit 8 of [[rt+0]+0x18], nulls [[rt+0]+0x20] (when its render target
     of the same kind targets it) and nulls [rt+0]. So rt+0x00 is the target texture (the three kinds share PTextureCommonBase's
     +0x18 / +0x20) and rt+0x08 is the target's kind byte: 0 = 2D, 1 = 3D, 2 = cube map
  K2 the kind-0 constructor 005DC1C0 (called at 006158DD, 00615914, 00615C99) stores word [rt+8] = 0, [rt+0xC] = 1, [rt+0] =
     the texture, sets bit 8 of texture+0x18, and stores rt at texture+0x20 when that cell is null or its render target is kind 0
     and targets the same texture. So texture+0x20 is the render target bound to it and bit 8 of m_textureFlags is set with it
  K3 the release 0062B890: for i below [rt+0x30] (bit 31 masked) releases [[rt+0x38]+8i] through vtable +0x10 and nulls it, then
     frees [rt+0x38] through 00584730 unless the count's bit 31 is set, and nulls it and the count; the same for +0x40 / +0x48;
     then releases +0x28, +0x20, +0x18, +0x10 through vtable +0x10; then, for kind 0 with a target whose created flag +0xBC is
     set, runs the target's release pass 0062BCB0. 005DDB00 frees the two arrays again (they are null by then when 0062B890 ran)
     and tail-jumps to 006108C0
  Not established: the kind-1 / kind-2 constructors (none sets bit 8 with `or` in 005C0000-00680000), which objects the four
  cells and the two arrays hold (views, by their release, not by a creator read here).
  S  REGRESSION: the three spans are re-cut, m_textureFlags carries bit 8, the D3D11 destructor cell reads the release (FAILS before)
Usage: python render_target_link.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
A = lambda pairs: all(at(a) == v for a, v in pairs)
k1 = A([(0x6505AD, ("movzx", "r8d, byte ptr [rcx + 8]")), (0x6505D3, ("mov", "rbx, qword ptr [rcx]")), (0x6505DE, ("call", "0x625f20")), (0x6505F3, ("jmp", "0x62c100")),
        (0x6505FE, ("mov", "rbx, qword ptr [rcx]")), (0x650609, ("call", "0x625f10")), (0x65061E, ("jmp", "0x62bf40")),
        (0x650628, ("mov", "rbx, qword ptr [rcx]")), (0x650633, ("call", "0x625f00")), (0x650648, ("jmp", "0x62bcb0")),
        (0x6108C0, ("movzx", "r8d, byte ptr [rcx + 8]")), (0x6108DB, ("cmp", "r8b, 2")), (0x610918, ("cmp", "r8b, 1")), (0x610949, ("test", "r8b, r8b")),
        (0x6108F1, ("mov", "r8, qword ptr [rdx + 0x20]")), (0x6108F5, ("cmp", "r8, rcx")), (0x6108FE, ("and", "dword ptr [rdx + 0x18], 0xfffffeff")),
        (0x61092F, ("and", "dword ptr [rdx + 0x18], 0xfffffeff")), (0x61095F, ("and", "dword ptr [rdx + 0x18], 0xfffffeff")),
        (0x610980, ("mov", "qword ptr [rdx + 0x20], rax")), (0x610984, ("mov", "qword ptr [rcx], rax"))])
check("K1", k1, "006505A0 and 006108C0 switch on byte rt+8 (0 2D, 1 3D, 2 cube) over the target at rt+0; the unlink clears target+0x18 bit 8 and +0x20")
text = next(s for s in SECS if s[0] == b".text"); tlo = B + text[2]; callers = []
for i in range(off(tlo), off(tlo) + text[3] - 5):
    if d[i] == 0xE8 and tlo + i - off(tlo) + 5 + struct.unpack_from("<i", d, i + 1)[0] == 0x5DC1C0: callers.append(tlo + i - off(tlo))
k2 = (A([(0x5DC1C0, ("mov", "word ptr [rcx + 8], 0")), (0x5DC1C6, ("mov", "dword ptr [rcx + 0xc], 1")), (0x5DC1CD, ("mov", "qword ptr [rcx], rdx")),
         (0x5DC1D0, ("or", "dword ptr [rdx + 0x18], 0x100")), (0x5DC1D7, ("mov", "rax, qword ptr [rdx + 0x20]")), (0x5DC1E0, ("cmp", "byte ptr [rax + 8], 0")),
         (0x5DC1EE, ("cmp", "r8, rdx")), (0x5DC1F3, ("mov", "qword ptr [rdx + 0x20], rcx"))]) and callers == [0x6158DD, 0x615914, 0x615C99])
check("K2", k2, "005DC1C0 links a kind-0 render target and its texture (callers %s)" % ["%08X" % c for c in callers])
k3 = A([(0x62B8A5, ("test", "dword ptr [rcx + 0x30], 0x7fffffff")), (0x62B8C0, ("mov", "rax, qword ptr [rbx + 0x38]")), (0x62B8C6, ("mov", "rcx, qword ptr [rax + rdx*8]")),
        (0x62B8D6, ("call", "qword ptr [rax + 0x10]")), (0x62B8F0, ("mov", "rcx, qword ptr [rbx + 0x38]")), (0x62B902, ("call", "0x584730")),
        (0x62B907, ("mov", "qword ptr [rbx + 0x38], rbp")), (0x62B90B, ("mov", "dword ptr [rbx + 0x30], ebp")),
        (0x62B90E, ("test", "dword ptr [rbx + 0x40], 0x7fffffff")), (0x62B92A, ("mov", "rcx, qword ptr [rax + rcx*8]")), (0x62B936, ("call", "qword ptr [rax + 0x10]")),
        (0x62B96C, ("call", "0x584730")), (0x62B971, ("mov", "qword ptr [rbx + 0x48], rbp")), (0x62B975, ("mov", "dword ptr [rbx + 0x40], ebp")),
        (0x62B978, ("mov", "rcx, qword ptr [rbx + 0x28]")), (0x62B984, ("call", "qword ptr [rax + 0x10]")), (0x62B98B, ("mov", "rcx, qword ptr [rbx + 0x20]")),
        (0x62B997, ("call", "qword ptr [rax + 0x10]")), (0x62B99E, ("mov", "rcx, qword ptr [rbx + 0x18]")), (0x62B9AA, ("call", "qword ptr [rax + 0x10]")),
        (0x62B9B1, ("mov", "rcx, qword ptr [rbx + 0x10]")), (0x62B9BD, ("call", "qword ptr [rax + 0x10]")),
        (0x62B9C4, ("cmp", "byte ptr [rbx + 8], 0")), (0x62B9D7, ("cmp", "dword ptr [rcx + 0xbc], 0")), (0x62B9E0, ("call", "0x62bcb0"))])
check("K3", k3, "0062B890 releases the two counted object arrays (+0x30/+0x38, +0x40/+0x48) and +0x28 +0x20 +0x18 +0x10, then a created kind-0 target")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/d3d11-element-release/render_target_link.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def cells(l): return l.rstrip("\r\n").split("\t")
def ev(was, tag): return "RE-CUT 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
P, U = "TYPE RESOLVED", "PROVEN"
def cut(t, rd, was):
    if t == "PRenderTargetBase":
        return [[t, "0x0000", "8", "target", "PTextureCommonBase*", "the texture this render target draws into: the kind-0 constructor 005DC1C0 stores it; the release route 006505A0 passes it to the 2D / 3D / cube release pass by the kind at +0x08; the unlink 006108C0 detaches it (clears its +0x18 bit 8 and its +0x20 back pointer) and nulls this cell", P, U, ev(was, "K1 K2")],
                [t, "0x0008", "1", "targetKind", "uint8", "the target's kind: 0 = 2D, 1 = 3D, 2 = cube map (the switch in 006505A0 and 006108C0); 005DC1C0 stores 0 with a word store that also zeroes m_msaaType", P, U, ev(was, "K1 K2")]]
    if t == "PTextureCommonBase":
        return [[t, "0x001C", "4", "unobservedSpan001C", "u8[4]", "four bytes with no reader in the render-target code; declared gap span - no Phyre reflection member registration covers it", rd, "UNKNOWN", ev(was, "K1 K2")],
                [t, "0x0020", "8", "boundRenderTarget", "PRenderTargetBase*", "the render target bound to this texture: the kind-0 constructor 005DC1C0 stores it (when the cell is null or its render target targets this texture) and sets m_textureFlags bit 8; the unlink 006108C0 nulls it and clears bit 8 when it points at the render target being unlinked. The 2D release pass 0062BCB0 hands it to 0062B870 / 0062B890", P, U, ev(was, "K1 K2")]]
    rows = [[t, "0x%04X" % o, "8", "releasedObject%02X" % o, "void*", "an object released like the views: 0062B890 calls its vtable slot +0x10 (the IUnknown Release position) and nulls it; 00625ED0 reports the render target live while +0x28 or +0x18 is non-null. Which object it is is not established", P, U, ev(was, "K3")] for o in (0x10, 0x18, 0x20, 0x28)]
    for c0, a0 in ((0x30, 0x38), (0x40, 0x48)):
        rows += [[t, "0x%04X" % c0, "4", "objectCount%02X" % c0, "uint32", "the element count of the object array at +0x%02X (bit 31 masked; bit 31 set keeps the array from being freed): 0062B890 walks and releases that many, then zeroes it" % a0, P, U, ev(was, "K3")],
                 [t, "0x%04X" % (c0 + 4), "4", "unobservedSpan%04X" % (c0 + 4), "u8[4]", "four bytes after the count; not read by the release, free or unlink", "DISCOVERED", "UNKNOWN", ev(was, "K3")],
                 [t, "0x%04X" % a0, "8", "objectArray%02X" % a0, "void**", "a heap array of object pointers: 0062B890 releases each through its vtable slot +0x10 and frees the array through 00584730 unless the count's bit 31 is set; 005DDB00 frees it the same way" % (), P, U, ev(was, "K3")]]
    return rows
SPAN = {("PRenderTargetBase", "0x0000", "9"), ("PTextureCommonBase", "0x001C", "12"), ("PRenderTargetD3D11", "0x0010", "64")}
FLAG = (" || BIT 8 (2026-09-28, OPUS, %s K1 K2): set by the kind-0 render-target constructor 005DC1C0 when it binds a render target "
        "to this texture (+0x20), and cleared by the unlink 006108C0 with that link" % REC)
DTC = (" || READ 2026-09-28 (OPUS, %s K3): 005DDB00 frees the object arrays +0x48 and +0x38 through 00584730 unless their counts' bit "
       "31 is set, nulls them and tail-jumps to the unlink 006108C0; the objects themselves are released by 0062B890, which "
       "PRenderTarget's destroy runs first when 00625ED0 answers non-zero" % REC)
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if (c[0], c[1], c[2]) in SPAN and c[3].startswith("unobservedSpan"):
            out += ["\t".join(r) + e for r in cut(c[0], c[6], "%s %s (%s)" % (c[3], c[4], c[5][:200]))]; continue
        if c[0] == "PTextureCommonBase" and c[3] == "m_textureFlags" and REC not in c[5]:
            c[5] += FLAG; l = "\t".join(c) + e
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "PRenderTargetD3D11" and REC not in c[6]: c[6] += DTC; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
TYPES = ("PRenderTargetBase", "PTextureCommonBase", "PRenderTargetD3D11")
have = {(r[0], int(r[1], 16)): r for r in F if r[0] in TYPES}
want = {("PRenderTargetBase", 0): "target", ("PRenderTargetBase", 8): "targetKind", ("PTextureCommonBase", 0x20): "boundRenderTarget",
        ("PRenderTargetD3D11", 0x10): "releasedObject10", ("PRenderTargetD3D11", 0x30): "objectCount30", ("PRenderTargetD3D11", 0x38): "objectArray38",
        ("PRenderTargetD3D11", 0x48): "objectArray48"}
ok = all(have.get(k, [0, 0, 0, ""])[3] == v for k, v in want.items())
ok &= all(sum(int(r[2]) for k, r in have.items() if k[0] == t) == int(T[t][1], 16) for t in TYPES)
ok &= REC in have[("PTextureCommonBase", 0x18)][5] and REC in T["PRenderTargetD3D11"][6]
check("S", ok, "three spans re-cut with tiling kept, m_textureFlags bit 8, PRenderTargetD3D11 release cell")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
