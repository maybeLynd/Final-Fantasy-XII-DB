"""platform_destroys.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The platform-level Phyre classes that
derive from the D3D11 classes had destroy cells 'descriptor destroy slot +0x58, form not reduced'; PIndirectArgsBuffer's release
also reads the unregistered bytes of its bases.

  P1 PTexture2D 005D3020, PTexture3D 005CF750, PTextureCubeMap 005D6060, PConstantBuffer 005D14C0, PStructuredBuffer 005D3750:
     destroy(descriptor, obj) calls the created-flag getter (00625F00 / 00625F10 / 00625F20 / 00625EC0 / 00625EF0), runs the
     D3D11 release pass (0062BCB0 / 0062BF40 / 0062C100 / 0062B7B0 / 0062BB40) only when it answers non-zero, then calls the D3D11
     class's destructor body (00616C60 / 00616CC0 / 00616D20 / 00616420 / 00616C00), which is the D3D11 destroy's own sequence -
     drain, release pass, free the external element array when count > 1 and bit 31 clear, then tail-jump to the base destructor
     (005DE290 / 005DE310 / 005DE390 / 0016D6A0 / 0016D6A0)
  P2 PRenderTarget 005D2F80: when 00625ED0 answers non-zero (+0x28 or +0x18 non-null) it runs 0062B890, then 005DDB00 (the
     PRenderTargetD3D11 destructor: frees +0x48 unless +0x40 bit 31 is set, then +0x38 unless +0x30 bit 31 is set, nulls the four
     cells, tail-jumps to 006108C0). The render-target fields are left to render_target_link.py
  P3 PIndirectArgsBuffer 005D7720: calls Sleep(1) (005CCB80) while the dword at +0x04 is above 0, then 006164B0 (the
     PIndirectArgsBufferD3D11 destructor): releases +0x18, +0x10 and +0x08 through vtable slot +0x10, nulling each, and
     tail-jumps to 0016D6A0
  So PIndirectArgsBufferBase +0x04 is a count the destroy waits on and PIndirectArgsBufferD3D11 +0x08/+0x10/+0x18 are objects
  released like views; which objects, and who raises the count, are not established.
  S  REGRESSION: the destroy cells are reduced and the base spans re-cut (FAILS before)
Usage: python platform_destroys.py [--patch]
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
def body(a, lim=0x200):
    out = []
    for x in cs.disasm(d[off(a):off(a) + lim], a):
        if x.mnemonic == "nop": continue
        out.append((x.mnemonic, x.op_str))
        if x.mnemonic in ("ret", "int3") or (x.mnemonic == "jmp" and x.op_str.startswith("0x") and not (a <= int(x.op_str, 16) < a + lim)): break
    return out
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
W = [("PTexture2D", 0x5D3020, 0x625F00, 0x62BCB0, 0x616C60, 0x62B100, 0x30, 0x38, 0x5DE290),
     ("PTexture3D", 0x5CF750, 0x625F10, 0x62BF40, 0x616CC0, 0x62B170, 0x38, 0x40, 0x5DE310),
     ("PTextureCubeMap", 0x5D6060, 0x625F20, 0x62C100, 0x616D20, 0x62B1E0, 0x30, 0x38, 0x5DE390),
     ("PConstantBuffer", 0x5D14C0, 0x625EC0, 0x62B7B0, 0x616420, 0x62B020, 0x18, 0x20, 0x16D6A0),
     ("PStructuredBuffer", 0x5D3750, 0x625EF0, 0x62BB40, 0x616C00, 0x62B090, 0x18, 0x20, 0x16D6A0)]
def wrap(dt, g, rp, bd):
    s = body(dt); c = [o for m, o in s if m == "call"]
    return c == ["0x%x" % g, "0x%x" % rp, "0x%x" % bd] and ("test", "al, al") in s and s[s.index(("test", "al, al")) + 1][0] == "je"
def dbody(bd, dr, rp, cnt, arr, base):
    s = body(bd); c = [o for m, o in s if m == "call"]
    return (c == ["0x%x" % dr, "0x%x" % rp, "0x584730"] and s[-1] == ("jmp", "0x%x" % base) and ("mov", "ecx, dword ptr [rbx + 0x%x]" % cnt) in s
            and ("btr", "ecx, 0x1f") in s and ("cmp", "ecx, 1") in s and ("mov", "rcx, qword ptr [rbx + 0x%x]" % arr) in s)
bad = [t for t, dt, g, rp, bd, dr, cnt, arr, base in W if not (wrap(dt, g, rp, bd) and dbody(bd, dr, rp, cnt, arr, base))]
check("P1", not bad, "five wrappers: flag-gated release pass, then the D3D11 destructor body%s" % ("" if not bad else " FAILED %s" % bad))
s = body(0x5D2F80); r = body(0x5DDB00, 0x80); g = body(0x625ED0, 0x20)
p2 = ([o for m, o in s if m == "call"] == ["0x625ed0", "0x62b890", "0x5ddb00"] and ("test", "al, al") in s
      and g[:4] == [("cmp", "qword ptr [rcx + 0x28], 0"), ("jne", "0x625ee1"), ("cmp", "qword ptr [rcx + 0x18], 0"), ("jne", "0x625ee1")]
      and ("mov", "rcx, qword ptr [rcx + 0x48]") in r and ("mov", "rcx, qword ptr [rbx + 0x38]") in r
      and [o for m, o in r if m == "call"] == ["0x584730", "0x584730"] and r[-1] == ("jmp", "0x6108c0"))
check("P2", p2, "PRenderTarget: 00625ED0-gated 0062B890, then 005DDB00 frees +0x48 / +0x38 and tail-jumps to 006108C0")
s = body(0x5D7720); t = body(0x6164B0)
p3 = (("mov", "eax, dword ptr [rdx + 4]") in s and ("mov", "eax, dword ptr [rbx + 4]") in s and ("call", "0x5ccb80") in s
      and any(m == "jle" for m, o in s) and any(m == "jg" for m, o in s) and [o for m, o in s if m == "call"] == ["0x5ccb80", "0x6164b0"]
      and [o for m, o in t if m == "mov" and (o.startswith("rcx, qword ptr [rcx + ") or o.startswith("rcx, qword ptr [rbx + "))]
          == ["rcx, qword ptr [rcx + 0x18]", "rcx, qword ptr [rbx + 0x10]", "rcx, qword ptr [rbx + 8]"]
      and [o for m, o in t if m == "call"] == ["qword ptr [rax + 0x10]"] * 3 and t[-1] == ("jmp", "0x16d6a0"))
check("P3", p3, "PIndirectArgsBuffer: Sleep(1) while +0x04 > 0, then 006164B0 releases +0x18 +0x10 +0x08")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/d3d11-element-release/platform_destroys.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def cells(l): return l.rstrip("\r\n").split("\t")
def ev(was, tag): return "RE-CUT 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def cut(t, was):
    if t == "PIndirectArgsBufferBase":
        return [[t, "0x0000", "4", "unobservedSpan0000", "u8[4]", "four bytes of the base with no reader in the destroy path; the Phyre reflection schema recovered no member for this class", "DISCOVERED", "UNKNOWN", ev(was, "P3")],
                [t, "0x0004", "4", "pendingCount", "uint32", "a count the destroy waits on: PIndirectArgsBuffer's destroy 005D7720 calls Sleep(1) while it is above 0 (a signed test, jle / jg) before the D3D11 destructor runs. Who raises and lowers it is not established", "TYPE RESOLVED", "PROVEN", ev(was, "P3")]]
    return [[t, "0x%04X" % o, "8", "releasedObject%02X" % o, "void*", "an object released like the D3D11 views: the destructor 006164B0 calls its vtable slot +0x10 (the IUnknown Release position) and nulls it; which object it is and who stores it are not established", "TYPE RESOLVED", "PROVEN", ev(was, "P3")] for o in (8, 0x10, 0x18)] + \
           [[t, "0x0020", "8", "unobservedSpan0020", "u8[8]", "this class's last eight bytes; not read by the destroy path, and the Phyre reflection schema recovered no member for them", "DISCOVERED", "UNKNOWN", ev(was, "P3")]]
SPAN = {("PIndirectArgsBufferBase", "0x0000", "8"), ("PIndirectArgsBufferD3D11", "0x0008", "32")}
DT = {t: "%08X: when the created-flag getter %08X answers non-zero it runs the D3D11 release pass %08X, then the D3D11 destructor body %08X (drain %08X, the same release pass, the external element array freed when count > 1 and bit 31 clear, tail-jump to the base destructor %08X)" % (dt, g, rp, bd, dr, base)
      for t, dt, g, rp, bd, dr, cnt, arr, base in W}
DT["PRenderTarget"] = "005D2F80: when 00625ED0 answers non-zero (+0x28 or +0x18 non-null) it runs 0062B890, then the PRenderTargetD3D11 destructor 005DDB00 (frees the +0x48 and +0x38 arrays unless their counts' bit 31 is set, nulls them, tail-jumps to the unlink 006108C0)"
DT["PIndirectArgsBuffer"] = "005D7720: calls Sleep(1) while +0x04 is above 0, then the PIndirectArgsBufferD3D11 destructor 006164B0 (releases +0x18, +0x10, +0x08 through vtable +0x10, tail-jumps to 0016D6A0)"
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if (c[0], c[1], c[2]) in SPAN and c[3].startswith("unobservedSpan"):
            out += ["\t".join(r) + e for r in cut(c[0], "%s %s (%s)" % (c[3], c[4], c[5][:200]))]; continue
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
have = {(r[0], int(r[1], 16)): r for r in F if r[0] in ("PIndirectArgsBufferBase", "PIndirectArgsBufferD3D11")}
ok = (have.get(("PIndirectArgsBufferBase", 4), [0, 0, 0, ""])[3] == "pendingCount"
      and all(have.get(("PIndirectArgsBufferD3D11", o), [0, 0, 0, ""])[3] == "releasedObject%02X" % o for o in (8, 0x10, 0x18))
      and all(sum(int(r[2]) for k, r in have.items() if k[0] == t) == int(T[t][1], 16) for t in ("PIndirectArgsBufferBase", "PIndirectArgsBufferD3D11"))
      and all(REC in T[t][6] and not re.sub(r"~~.*?~~", "", T[t][6]).strip().endswith("form not reduced") for t in DT))
check("S", ok, "seven destroy cells reduced; PIndirectArgsBuffer base spans re-cut, tiling kept")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
