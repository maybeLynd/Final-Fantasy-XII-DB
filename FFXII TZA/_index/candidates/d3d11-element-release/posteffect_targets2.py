"""posteffect_targets2.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Three more post-effect base classes keep
render-target pointers in unregistered spans; their destructors release them (posteffect_targets.py did PDepthOfFieldD3D11 and
PMotionBlurD3D11).

  V  each class's RTTI vtable holds its deleting destructor at slot 0 (found by the destructor's address, RTTI-checked), and the
     destructor calls the body: PFXAABase 00647590 -> 00646770; PMLAABase 006479F0 -> 0065D610; PGlowGPUBase 00647820 ->
     0065D4F0
  F  00646770 passes [+0x50] to the render-target release 006505A0
  L  0065D610 passes [+0x50] to 006505A0 and nulls it, then walks two cells from +0x58 (esi = 2, stride 8) with the same kind switch
     inlined (byte [rt+8]: 0 -> 00625F00 / 0062BCB0, 1 -> 00625F10 / 0062BF40, 2 -> 00625F20 / 0062C100 on [rt+0]), nulling each
  G  0065D4F0 walks three cells from +0xA0 with the inlined switch, then passes three cells from +0xB8 and +0xD0 to 006505A0,
     nulling each: seven render targets, +0xA0..+0xD7 - the class's last 56 bytes exactly
  So these cells are PRenderTargetBase*. PFXAABase +0x58..+0x6F and PMLAABase +0x68..+0xAF stay unread by the destructors.
  S  REGRESSION: the three spans are re-cut as generated, tiling kept (FAILS before)
Usage: python posteffect_targets2.py [--patch]
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
def vtables_holding(f):
    """image VAs of qwords equal to f whose preceding qword is a complete-object locator (i.e. f is some vtable's slot 0)"""
    out, q, i = [], struct.pack("<Q", f), d.find(struct.pack("<Q", f))
    while i >= 0:
        for vs, va, rs, ro in SECS:
            if ro <= i < ro + rs:
                out.append(B + va + i - ro)
        i = d.find(q, i + 1)
    return out
def installs(f, cls, body):
    ins = list(cs.disasm(d[off(f):off(f) + 0x40], f))
    want = (".?AV%s@PPostProcessing@Phyre@@" % cls).encode()
    hits = []
    for vt in vtables_holding(f):
        try:
            if rtti(vt) == want: hits.append(vt)
        except Exception: pass
    return bool(hits) and any(x.mnemonic == "call" and x.op_str == "0x%x" % body for x in ins)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
check("V", installs(0x647590, "PFXAABase", 0x646770) and installs(0x6479F0, "PMLAABase", 0x65D610) and installs(0x647820, "PGlowGPUBase", 0x65D4F0),
      "each class's RTTI vtable has the destructor at slot 0, and the destructor calls the body")
check("F", A([(0x64678C, ("mov", "rcx, qword ptr [rcx + 0x50]")), (0x646790, ("call", "0x6505a0"))]), "00646770: [+0x50] -> 006505A0")
def switch(base):
    """the inlined kind switch at base: byte [rt+8], releases per kind, target [rt+0]"""
    ins = [(x.mnemonic, x.op_str) for x in cs.disasm(d[off(base):off(base) + 0xC0], base)][:48]
    return all(("call", "0x%x" % t) in ins for t in (0x625F20, 0x62C100, 0x625F10, 0x62BF40, 0x625F00, 0x62BCB0)) and any(o.endswith("byte ptr [rdx + 8]") or o.endswith("byte ptr [rcx + 8]") for m, o in ins if m == "movzx")
check("L", A([(0x65D627, ("mov", "rcx, qword ptr [rcx + 0x50]")), (0x65D62B, ("call", "0x6505a0")), (0x65D632, ("lea", "rdi, [rbx + 0x58]")), (0x65D636, ("mov", "qword ptr [rbx + 0x50], rbp")),
              (0x65D63A, ("lea", "esi, [rbp + 2]")), (0x65D6CC, ("mov", "qword ptr [rdi], rbp")), (0x65D6CF, ("add", "rdi, 8")), (0x65D6D3, ("sub", "rsi, 1"))]) and switch(0x65D640),
      "0065D610: [+0x50] -> 006505A0; two cells from +0x58 through the inlined kind switch")
check("G", A([(0x65D508, ("mov", "esi, 3")), (0x65D50D, ("lea", "rdi, [rcx + 0xa0]")), (0x65D514, ("mov", "ebp, esi")), (0x65D5AC, ("mov", "qword ptr [rdi], r15")),
              (0x65D5AF, ("add", "rdi, 8")), (0x65D5B3, ("sub", "rbp, 1")), (0x65D5BD, ("lea", "rbx, [r14 + 0xb8]")), (0x65D5CC, ("call", "0x6505a0")),
              (0x65D5D1, ("mov", "qword ptr [rbx], r15")), (0x65D5D4, ("add", "rbx, 8")), (0x65D5D8, ("sub", "rsi, 1")),
              (0x65D5DE, ("mov", "rcx, qword ptr [r14 + 0xd0]")), (0x65D5EA, ("call", "0x6505a0"))]) and switch(0x65D520),
      "0065D4F0: three cells from +0xA0 (inlined switch), three from +0xB8 and +0xD0 through 006505A0")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/d3d11-element-release/posteffect_targets2.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def ev(was, tag): return "RE-CUT 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def rt(t, o, how, tag, was): return [t, "0x%04X" % o, "8", "renderTarget%02X" % o, "PRenderTargetBase*", "a render target: the destructor %s and nulls it" % how, "TYPE RESOLVED", "PROVEN", ev(was, tag)]
def gap(t, o, sz, tag, was): return [t, "0x%04X" % o, str(sz), "unobservedSpan%04X" % o, "u8[%d]" % sz, "not read by the class's destructor; the Phyre reflection schema recovered no member for these bytes", "DISCOVERED", "UNKNOWN", ev(was, tag)]
SW = "releases it through the render-target kind switch inlined in %s (byte +0x08 selects the 2D / 3D / cube release of the target +0x00)"
def cut(t, was):
    if t == "PFXAABase": return [rt(t, 0x50, "00646770 passes it to the render-target release 006505A0", "V F", was), gap(t, 0x58, 24, "V F", was)]
    if t == "PMLAABase": return [rt(t, 0x50, "0065D610 passes it to the render-target release 006505A0", "V L", was)] + [rt(t, o, SW % "0065D610", "V L", was) for o in (0x58, 0x60)] + [gap(t, 0x68, 72, "V L", was)]
    return [rt(t, o, SW % "0065D4F0", "V G", was) for o in (0xA0, 0xA8, 0xB0)] + [rt(t, o, "0065D4F0 passes it to the render-target release 006505A0", "V G", was) for o in (0xB8, 0xC0, 0xC8, 0xD0)]
SPAN = {("PFXAABase", "0x0050", "32"), ("PMLAABase", "0x0050", "96"), ("PGlowGPUBase", "0x00A0", "56")}
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if (c[0], c[1], c[2]) in SPAN and c[3].startswith("unobservedSpan"):
            out += ["\t".join(r) + e for r in cut(c[0], "%s %s (%s)" % (c[3], c[4], c[5][:200]))]; continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
TYP = [s[0] for s in SPAN]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
F = {(cells(l)[0], int(cells(l)[1], 16)): cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] in TYP}
gen = {(r[0], int(r[1], 16)): r for t in TYP for r in cut(t, "")}
ok = all(k in F and F[k][3:6] == g[3:6] for k, g in gen.items()) and all(sum(int(r[2]) for k, r in F.items() if k[0] == t) == int(T[t][1], 16) for t in TYP)
check("S", ok, "the three spans re-cut as generated (name, ctype, meaning), tiling kept")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
