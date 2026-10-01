"""render_substates.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
The sub-objects RenderContext02CC0410's constructor 00615840 (rbp = this) builds inside its +0x480 span, typed by the
constructors that build them.

  T  two PRenderTarget: rbx = this + 0x480 / + 0x4D0 is handed with rdx = this + 0x170 / + 0x2F8 (the two in-place
     PTexture2DD3D11) to 005DC1C0, which stores [rcx] = rdx, word [rcx + 8] = 0, dword [rcx + 0xC] = 1 and ORs 0x100 into
     the texture's +0x18 (the PRenderTargetBase layout: target at +0, targetKind at +8); the constructor then clears
     +0x10 / +0x18 / +0x20 / +0x28 (qword), +0x30 (dword), +0x38 (qword), +0x40 (dword), +0x48 (qword) - exactly
     PRenderTargetD3D11's rows after its 0x10-byte base, to its 0x50 end. PRenderTarget (0x50) derives from
     PRenderTargetD3D11 and its class descriptor has no default constructor: it is built from a texture, as here
  S  PShaderPassStateD3D11's class-descriptor vtable 00D50688 has 00611420 at +0x50, the placement default constructor
     (`if (rdx) T::T(rdx); return 1`), which calls 00615ED0; so 00615ED0 is PShaderPassStateD3D11::PShaderPassStateD3D11.
     Its stores match the store's rows: m_rasterDesc at +4 (fill 3, cull 3 then 1, depth-clip 1, multisample 1),
     m_depthDesc at +0x2C (1, 1, 2, stencil masks 0xFFFF, both face ops from 00D56070 = 1 1 1 8), m_blendDesc at +0x60
     (eight 0x20-byte targets from +0x68: 0 2 1 1 / 2 1 1 mask 0xF), +0x168..+0x187 zeroed, m_stencilRef +0x188 = 0
  P  00615840 calls 00615ED0 on this + 0x830 and this + 0x9C0, and 00615720 on this + 0xB50. 00615720 clears ten qwords at
     +0x00..+0x48 and runs 00808FE4 (the vector constructor iterator: rcx = first, rdx = stride, r8 = count, r9 = ctor)
     with rcx + 0x50, 0x190, 8, 00615ED0 - eight PShaderPassStateD3D11 from +0x50, ending at +0xCD0 = this + 0x1820
  W  REGRESSION (FAILS before): the rows are in the store; RenderContextPassStateBlock exists and tiles; the context's
     declared rows still end at +0x18C0
Not claimed: the roles of these objects; the 005DBF30 pair at +0x520 / +0x548, the 8 x 0x18 array at +0x570 and the
005DC190 object at +0x630 stay in spans (their extents are not fixed by their constructors); the 0x28-byte object at
+0x1820 (005DC400).
Usage: python render_substates.py [--patch]
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
    return all(A.get(a) == v for a, v in pairs)
RT_STORES = [("qword", 0x10), ("qword", 0x18), ("qword", 0x20), ("qword", 0x28), ("dword", 0x30), ("qword", 0x38), ("dword", 0x40), ("qword", 0x48)]
def rt_block(start):
    L = [x for x in cs.disasm(d[off(start):off(start) + 0x40], start)][:8]
    return [(x.op_str.split(" ptr")[0], int(x.op_str.split("+ ")[1].split("]")[0], 16)) for x in L if x.mnemonic == "mov" and "[rbx +" in x.op_str]
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
rtd = sorted((int(c[1], 16), int(c[2])) for c in F if c[0] == "PRenderTargetD3D11" and int(c[1], 16) >= 0x10 and not c[3].startswith("unobserved"))
check("T", has(0x615840, 0x615950, [(0x615860, ("mov", "rbp, rcx")), (0x615881, ("lea", "rdi, [rbp + 0x170]")), (0x6158A6, ("lea", "rsi, [rbp + 0x2f8]")),
                                     (0x6158CB, ("lea", "rbx, [rbp + 0x480]")), (0x6158D7, ("mov", "rdx, rdi")), (0x6158DA, ("mov", "rcx, rbx")), (0x6158DD, ("call", "0x5dc1c0")),
                                     (0x615902, ("lea", "rbx, [rbp + 0x4d0]")), (0x61590E, ("mov", "rdx, rsi")), (0x615911, ("mov", "rcx, rbx")), (0x615914, ("call", "0x5dc1c0"))])
      and rt_block(0x6158E2) == RT_STORES and rt_block(0x615919) == RT_STORES
      and rtd == [(o, 8 if w == "qword" else 4) for w, o in RT_STORES]
      and has(0x5DC1C0, 0x5DC1FB, [(0x5DC1C0, ("mov", "word ptr [rcx + 8], 0")), (0x5DC1C6, ("mov", "dword ptr [rcx + 0xc], 1")), (0x5DC1CD, ("mov", "qword ptr [rcx], rdx")),
                                   (0x5DC1D0, ("or", "dword ptr [rdx + 0x18], 0x100")), (0x5DC1D7, ("mov", "rax, qword ptr [rdx + 0x20]")), (0x5DC1F3, ("mov", "qword ptr [rdx + 0x20], rcx"))]),
      "this + 0x480 / + 0x4D0: 005DC1C0(texture170 / texture2F8) then the eight PRenderTargetD3D11 fields +0x10..+0x48 (store rows %s)" % ["+0x%X/%d" % r for r in rtd])
slot50 = struct.unpack_from("<Q", d, off(0xD50688 + 0x50))[0] - IB + B
check("S", slot50 == 0x611420 and has(0x611420, 0x611438, [(0x611424, ("test", "rdx, rdx")), (0x611429, ("mov", "rcx, rdx")), (0x61142C, ("call", "0x615ed0")), (0x611431, ("mov", "al, 1"))])
      and has(0x615ED0, 0x615FF6, [(0x615EEB, ("mov", "dword ptr [rcx + 4], 3")), (0x615F01, ("mov", "qword ptr [rcx + 0x1c], 1")), (0x615F0D, ("mov", "dword ptr [rcx + 0x2c], 1")),
                                   (0x615F1B, ("mov", "qword ptr [rcx + 0x34], 2")), (0x615F23, ("mov", "word ptr [rcx + 0x3c], 0xffff")), (0x615F29, ("movups", "xmmword ptr [rcx + 0x40], xmm1")),
                                   (0x615F35, ("movups", "xmmword ptr [rcx + 0x50], xmm1")), (0x615F3D, ("movups", "xmmword ptr [rcx + 0x68], xmm3")), (0x615F8C, ("movups", "xmmword ptr [rcx + 0x78], xmm2")),
                                   (0x615FBA, ("movups", "xmmword ptr [rcx + 0x158], xmm2")), (0x615FC1, ("mov", "qword ptr [rcx + 0x168], rdx")), (0x615FDD, ("mov", "byte ptr [rcx + 0x188], dl")),
                                   (0x615FE3, ("mov", "dword ptr [rcx + 8], 1")), (0x615FEA, ("mov", "dword ptr [rcx + 0x24], 1"))])
      and struct.unpack_from("<4I", d, off(0xD56070)) == (1, 1, 1, 8) and struct.unpack_from("<4I", d, off(0xD56060)) == (0, 2, 1, 1),
      "descriptor slot +0x50 = 00611420 -> 00615ED0, the default constructor; its stores are the D3D11 default raster / depth-stencil / blend state")
check("P", has(0x615AA9, 0x615AD4, [(0x615AA9, ("lea", "rcx, [rbp + 0x830]")), (0x615AB0, ("call", "0x615ed0")), (0x615ABC, ("lea", "rcx, [rbp + 0x9c0]")),
                                     (0x615AC3, ("call", "0x615ed0")), (0x615AC8, ("lea", "rcx, [rbp + 0xb50]")), (0x615ACF, ("call", "0x615720"))])
      and has(0x615720, 0x615789, [(0x615733, ("mov", "rbx, rcx")), (0x615736, ("mov", "qword ptr [rcx], rdi")), (0x615739, ("mov", "qword ptr [rcx + 8], rdi")),
                                   (0x61573D, ("lea", "r9, [rip + 0x78c]")), (0x615744, ("add", "rcx, 0x50")), (0x61574D, ("lea", "r8d, [rdi + 8]")), (0x615751, ("mov", "edx, 0x190")),
                                   (0x615756, ("call", "0x808fe4")), (0x61577A, ("mov", "qword ptr [rbx + 0x48], rdi"))])
      and 0x61573D + 7 + 0x78C == 0x615ED0
      and has(0x808FE4, 0x809052, [(0x809000, ("mov", "rsi, r9")), (0x809003, ("mov", "r15, r8")), (0x809006, ("mov", "r14, rdx")), (0x809009, ("mov", "rdi, rcx")),
                                   (0x809015, ("cmp", "rbx, r15")), (0x809022, ("mov", "rcx, rdi")), (0x809025, ("call", "rsi")), (0x809027, ("add", "rdi, r14"))]),
      "this + 0x830 / + 0x9C0: PShaderPassStateD3D11; this + 0xB50: ten qwords then 8 x 0x190 PShaderPassStateD3D11 through the vector constructor iterator")

REC = "_index/candidates/render-context-02cc0410/render_substates.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RC, BLK, PS = "RenderContext02CC0410", "RenderContextPassStateBlock", "PShaderPassStateD3D11"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def ev(tag, was): return "CARVED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was="-", w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
def cut(w):
    return [r(RC, 0x480, 0x50, "renderTarget480", "PRenderTarget", "a PRenderTarget built in place on texture170 (005DC1C0 links it into the texture's +0x20 list)", P, "T", w),
            r(RC, 0x4D0, 0x50, "renderTarget4D0", "PRenderTarget", "a PRenderTarget built in place on texture2F8", P, "T", w),
            r(RC, 0x520, 784, "unobservedSpan0520", "u8[784]", "initialised by the constructor - 005DBF30 on +0x520 and +0x548, an 8 x 0x18 array at +0x570 (00808FE4 with 005DC1B0), 005DC190 on +0x630, cleared fields +0x6F0..+0x828 and 1.0f at +0x7D0 - but not typed here", U, "T P", w),
            r(RC, 0x830, 0x190, "passState830", PS, "a PShaderPassStateD3D11 default-constructed in place (00615ED0)", P, "S P", w),
            r(RC, 0x9C0, 0x190, "passState9C0", PS, "a second PShaderPassStateD3D11 default-constructed in place", P, "S P", w),
            r(RC, 0xB50, 0xCD0, "passStateBlockB50", BLK, "ten qwords and eight PShaderPassStateD3D11, built by 00615720", P, "S P", w),
            r(RC, 0x1820, 44, "unobservedSpan1820", "u8[44]", "005DC400's object at +0x1820 (it writes +0..+0x1F; the constructor then clears +0x20) and a word at +0x1848; not typed here", U, "P", w)]
BLKROWS = [r(BLK, 0x00, 80, "unobservedSpan0000", "u8[80]", "ten qwords 00615720 clears; not read here", U, "P"),
           r(BLK, 0x50, 0xC80, "passStates", PS + "[8]", "eight PShaderPassStateD3D11 built by the vector constructor iterator with 00615ED0", P, "S P")]
NEWT = [BLK, "0xCD0", "17-Presentation-Rendering", "one at RenderContext02CC0410 +0xB50", "EMBEDDED in RenderContext02CC0410", "00615720", "not read here", P[0], P[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s P). Extent: 0x50 + 8 x 0x190, ending at the context's +0x1820 where 005DC400's object begins. %s" % (REC, EXE),
        "17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md", "EMBED RenderContext02CC0410 +0x0B50"]
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]; out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == RC and c[1] == "0x0480" and c[2] == "5068":
            out += ["\t".join(x) + e for x in cut("%s %s (%s)" % (c[3], c[4], c[5][:160]))]; continue
        out.append(l)
    if not any(cells(l)[0] == BLK for l in out):
        idx = max(i for i, l in enumerate(out) if cells(l)[0] == RC); out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in BLKROWS]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == BLK for l in tl):
        ti = max(i for i, l in enumerate(tl) if cells(l)[0] == RC); tl[ti + 1:ti + 1] = ["\t".join(NEWT) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
R = {int(c[1], 16): c for c in F if c[0] == RC}
names = {o: R[o][3:5] for o in (0x480, 0x4D0, 0x830, 0x9C0, 0xB50) if o in R}
end = max(o + int(c[2]) for o, c in R.items()) if R else 0
blk_ok = BLK in T and sum(int(c[2]) for c in F if c[0] == BLK) == int(T[BLK][1], 16)
# the +0x830 pass state is later the +0x58 of RenderPrimitivePass1E8 at +0x7D8 (render_buffers.py P: its release 0062B290 releases it)
moved = 0x830 not in names and 0x7D8 in R and R[0x7D8][4] == "RenderPrimitivePass1E8" and "render_buffers.py" in R[0x7D8][8]
if moved: names[0x830] = ["passState830", PS]
check("W", names == {0x480: ["renderTarget480", "PRenderTarget"], 0x4D0: ["renderTarget4D0", "PRenderTarget"], 0x830: ["passState830", PS], 0x9C0: ["passState9C0", PS],
                     0xB50: ["passStateBlockB50", BLK]} and blk_ok and (end == 0x18C0 or (end == 0x221F8 and "render_primitive.py" in R[0x18C0][8])),   # extended past +0x18C0 by render_primitive.py
      "the sub-object rows are in the store; RenderContextPassStateBlock tiles; the context's rows end at +0x18C0, or at +0x221F8 once render_primitive.py adds the renderer")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
