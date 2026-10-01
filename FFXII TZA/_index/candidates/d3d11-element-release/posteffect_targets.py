"""posteffect_targets.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Two post-effect D3D11 classes kept
render-target pointers in unregistered spans; their virtual destructors hand them to the render-target release.

  R  the RTTI vtables' slot 0 are MSVC scalar-deleting destructors: 00647470 (PDepthOfFieldD3D11) installs its vtable, runs
     006466E0, then frees through 00584730 or, with flag bit 2, the sized 0016D6A0(this, 0xD0); 00647D40 (PMotionBlurD3D11)
     runs 00646A30, then the same with size 0xD70. Both sizes equal the store's type sizes
  D  006466E0 passes [+0x80], [+0x88], [+0x90] and [+0x98] to 006505A0; 00646A30 passes [+0xD68] to 006505A0 and nulls it.
     006505A0 is the render-target release that switches on byte [rt+8] (target kind) and releases the target at [rt+0]
     (render_target_link.py K1), so each cell is a render target (PRenderTargetBase*)
  PDepthOfFieldD3D11 +0xA0..+0xCF is not read by this destructor.
  S  REGRESSION: the two spans are re-cut, tiling kept (FAILS before)
Usage: python posteffect_targets.py [--patch]
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
def rtti(v):
    col = struct.unpack_from("<Q", d, off(v - 8))[0]; td = struct.unpack_from("<I", d, off(col) + 12)[0] + B
    return d[off(td) + 16:off(td) + 90].split(bytes(1))[0]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
TY = os.path.join(DB, "_types", "types.tsv"); FI = os.path.join(DB, "_types", "fields.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
vt = at(0x647489)[2]
r = (A([(0x647490, ("mov", "qword ptr [rcx], rax")), (0x647493, ("call", "0x6466e0")), (0x6474A8, ("call", "0x584730")), (0x6474B0, ("mov", "edx, 0xd0")), (0x6474B8, ("call", "0x16d6a0")),
        (0x647D59, ("call", "0x646a30")), (0x647D6E, ("call", "0x584730")), (0x647D76, ("mov", "edx, 0xd70")), (0x647D7E, ("call", "0x16d6a0"))])
     and rtti(vt) == b".?AVPDepthOfFieldD3D11@PPostProcessing@Phyre@@" and struct.unpack_from("<Q", d, off(vt))[0] == 0x647470
     and int(T["PDepthOfFieldD3D11"][1], 16) == 0xD0 and int(T["PMotionBlurD3D11"][1], 16) == 0xD70)
check("R", r, "slot-0 deleting destructors 00647470 / 00647D40; sized deletes 0xD0 / 0xD70 = the store's sizes")
dd = (A([(0x6466FC, ("mov", "rcx, qword ptr [rcx + 0x80]")), (0x646703, ("call", "0x6505a0")), (0x646709, ("mov", "rcx, qword ptr [rbx + 0x88]")), (0x646710, ("call", "0x6505a0")),
         (0x646716, ("mov", "rcx, qword ptr [rbx + 0x90]")), (0x64671D, ("call", "0x6505a0")), (0x646723, ("mov", "rcx, qword ptr [rbx + 0x98]")), (0x64672A, ("call", "0x6505a0")),
         (0x646A4C, ("mov", "rcx, qword ptr [rcx + 0xd68]")), (0x646A53, ("call", "0x6505a0")), (0x646A59, ("mov", "qword ptr [rbx + 0xd68], 0")),
         (0x6505AD, ("movzx", "r8d, byte ptr [rcx + 8]")), (0x6505D3, ("mov", "rbx, qword ptr [rcx]"))]))
check("D", dd, "006466E0 / 00646A30 hand +0x80..+0x98 / +0xD68 to the render-target release 006505A0")
REC = "_index/candidates/d3d11-element-release/posteffect_targets.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def ev(was, tag): return "RE-CUT 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def cut(t, was):
    P = ("TYPE RESOLVED", "PROVEN")
    if t == "PMotionBlurD3D11":
        return [[t, "0x0D68", "8", "renderTargetD68", "PRenderTargetBase*", "a render target: the destructor 00646A30 passes it to the render-target release 006505A0 (which switches on its kind byte +0x08 and releases its target +0x00) and nulls it", P[0], P[1], ev(was, "R D")]]
    return [[t, "0x%04X" % o, "8", "renderTarget%02X" % o, "PRenderTargetBase*", "a render target: the destructor 006466E0 passes it to the render-target release 006505A0 (which switches on its kind byte +0x08 and releases its target +0x00)", P[0], P[1], ev(was, "R D")] for o in (0x80, 0x88, 0x90, 0x98)] + \
           [[t, "0x00A0", "48", "unobservedSpan00A0", "u8[48]", "the class's last 48 bytes; not read by its destructor, and the Phyre reflection schema recovered no member for them", "DISCOVERED", "UNKNOWN", ev(was, "D")]]
SPAN = {("PDepthOfFieldD3D11", "0x0080", "80"), ("PMotionBlurD3D11", "0x0D68", "8")}
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if (c[0], c[1], c[2]) in SPAN and c[3].startswith("unobservedSpan"):
            out += ["\t".join(r) + e for r in cut(c[0], "%s %s (%s)" % (c[3], c[4], c[5][:200]))]; continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = {(cells(l)[0], int(cells(l)[1], 16)): cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] in ("PDepthOfFieldD3D11", "PMotionBlurD3D11")}
gen = {(r[0], int(r[1], 16)): r for t in ("PDepthOfFieldD3D11", "PMotionBlurD3D11") for r in cut(t, "")}
ok = (all(k in F and F[k][3:6] == g[3:6] for k, g in gen.items())
      and all(sum(int(r[2]) for k, r in F.items() if k[0] == t) == int(T[t][1], 16) for t in ("PDepthOfFieldD3D11", "PMotionBlurD3D11")))
check("S", ok, "the two spans re-cut as generated (name, ctype, meaning), tiling kept")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
