"""element_release.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The five PhyreEngine D3D11 resource classes
declared 2026-09-27 had owner release cells reading 'descriptor destroy slot +0x58, form not reduced' and EMPTY element release
cells, and each element type kept a span 'no reader found in reach'. The release path reads those spans:

  O  the five destroys share one form, destroy(descriptor, obj): drain(obj); releasePass(obj); free the external element
     array through 00584730 only when the count (bit 31 masked) is above 1 and bit 31 (keep-buffer) is clear; null the
     array pointer and count; then the base destructor
       PTexture2DD3D11 00611F80: 0062B100 / 0062BCB0 / count +0x30, array +0x38 / base 005DE290
       PTexture3DD3D11 00610EC0: 0062B170 / 0062BF40 / +0x38, +0x40 / 005DE310
       PTextureCubeMapD3D11 00612B20: 0062B1E0 / 0062C100 / +0x30, +0x38 / 005DE390
       PConstantBufferD3D11 00611AD0: 0062B020 / 0062B7B0 / +0x18, +0x20 / 0016D6A0
       PStructuredBufferD3D11 006122D0: 0062B090 / 0062BB40 / +0x18, +0x20 / 0016D6A0
  W  each drain loops over the elements and, while the dword its getter addresses is > 0 (test / jle, a signed test),
     calls Sleep(1) (005CCB80 = jmp [008C21B0], KERNEL32 Sleep) and re-reads it. The getters' external-array arm addresses
     element +0x38 (2D, 00623DF0), +0x20 (3D 00623E30, cube 00623E70, structured 00623DB0) and +0x0C (constant 00623D70)
  R  each release pass walks every element and releases through vtable slot +0x10, nulling the slot:
       2D (stride 0x58, 0062BD2F): +0x10 +0x18 +0x20 +0x00 +0x08 AND +0x30; and when +0x28 is non-null it removes the
          element's embedded async-update object (+0x40) from the scheduler (0062EC70, 0062BD75), frees +0x28 through
          00584730 (0062BD9C) and nulls it
       3D (stride 0x28): +0x08 +0x10 +0x00; frees +0x18 through 00584730 (0062C0A1)
       cube (stride 0x40, 0062C18F): when +0x18 is non-null, removes +0x28 from the scheduler (0062C1D5), frees +0x18
          (0062C1FC); releases +0x08 +0x10 +0x00
       constant (stride 0x10, 0062B80F): +0x00; then frees the OWNER's +0x10 (cpuData) through 00584730 (0062B851)
       structured (stride 0x28): +0x08 +0x10 +0x00 AND +0x18
  So: 2D +0x28 and 3D / cube +0x18 are owned heap blocks, 2D +0x30 and structured +0x18 are objects released like the views
  (slot +0x10, the IUnknown Release position; which object is not established), and 2D +0x38, 3D / cube / structured +0x20
  and constant +0x0C are counts the release waits on. Who raises and lowers the counts, and what the blocks hold, is not
  established here.
  S  REGRESSION: the spans are re-cut, the element release cells are filled and the owner cells reduced (FAILS before)
Usage: python element_release.py [--patch]
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
def body(a, lim=0x800):
    out = []
    for x in cs.disasm(d[off(a):off(a) + lim], a):
        out.append((x.address, x.mnemonic, x.op_str))
        if x.mnemonic in ("ret", "int3") and x.address > a + 0x10: break
    return out
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
# O
OWN = [("PTexture2DD3D11", 0x611F80, 0x62B100, 0x62BCB0, 0x30, 0x38, 0x5DE290), ("PTexture3DD3D11", 0x610EC0, 0x62B170, 0x62BF40, 0x38, 0x40, 0x5DE310),
       ("PTextureCubeMapD3D11", 0x612B20, 0x62B1E0, 0x62C100, 0x30, 0x38, 0x5DE390), ("PConstantBufferD3D11", 0x611AD0, 0x62B020, 0x62B7B0, 0x18, 0x20, 0x16D6A0),
       ("PStructuredBufferD3D11", 0x6122D0, 0x62B090, 0x62BB40, 0x18, 0x20, 0x16D6A0)]
def form(dt, dr, rp, cnt, arr, base):
    b = body(dt); s = [(m, o) for a, m, o in b if m != "nop"]
    calls = [o for m, o in s if m == "call"]
    return (calls == ["0x%x" % dr, "0x%x" % rp, "0x584730", "0x%x" % base]
            and ("mov", "ecx, dword ptr [rbx + 0x%x]" % cnt) in s and ("btr", "ecx, 0x1f") in s and ("cmp", "ecx, 1") in s
            and ("shr", "eax, 0x1f") in s and ("mov", "rcx, qword ptr [rbx + 0x%x]" % arr) in s
            and ("mov", "qword ptr [rbx + 0x%x], rax" % arr) in s and ("mov", "dword ptr [rbx + 0x%x], eax" % cnt) in s)
bad = [t for t, *r in OWN if not form(*r)]
check("O", not bad, "the five destroys: drain, release pass, external array freed when count > 1 and bit 31 clear, base dtor%s" % ("" if not bad else " - FAILED %s" % bad))
# W
GET = {0x62B100: (0x623DF0, "0x58", 0x38), 0x62B170: (0x623E30, "5x8", 0x20), 0x62B1E0: (0x623E70, "<<6", 0x20),
       0x62B020: (0x623D70, "<<4", 0x0C), 0x62B090: (0x623DB0, "5x8", 0x20)}
def getter_off(g):
    s = [(m, o) for a, m, o in body(g, 0x40)]
    if ("imul", "rax, rax, 0x58") in s: return [int(o.split(", ")[1], 16) for m, o in s if m == "add" and o.startswith("rax, 0x")][0]
    if ("shl", "rax, 6") in s or ("shl", "rax, 4") in s: return [int(o.split(", ")[1], 16) for m, o in s if m == "add" and o.startswith("rax, 0x")][0]
    if ("lea", "rax, [rax + rax*4]") in s: return 8 * int([o for m, o in s if m == "lea" and o.startswith("rax, [rax + ") and "*" not in o][0].split("+ ")[1].rstrip("]"), 0)
ok = True; seen = []
for dr, (g, st, want) in GET.items():
    s = [(m, o) for a, m, o in body(dr, 0x80)]
    calls = [o for m, o in s if m == "call"]
    ok &= (calls.count("0x%x" % g) == 2 and "0x5ccb80" in calls and ("mov", "ecx, dword ptr [rax]") in s and ("test", "ecx, ecx") in s
           and any(m == "jle" for m, o in s) and ("mov", "ecx, 1") in s and getter_off(g) == want)
    seen.append("%08X:+0x%X" % (g, getter_off(g) or -1))
ok &= at(0x5CCB80)[0] == "jmp" and at(0x5CCB80)[2] == 0x8C21B0
check("W", ok, "drains Sleep(1) while the addressed dword > 0; getters %s; 005CCB80 -> [008C21B0]" % seen)
# R
def rel(a, disp, via=None):
    """a: address of the `mov rcx, qword ptr [.. + disp]` (or `mov rcx, qword ptr [rdi]` after an add/lea of the element base) and
    the vcall [rax + 0x10] that follows within 6 instructions (test, je, mov rax, [rcx])"""
    b = body(a, 0x30)[:6]
    m0, o0 = b[0][1], b[0][2]
    dm = re.search(r"\+ (0x[0-9a-f]+|\d+)\]$", o0)   # capstone prints displacements below 10 in decimal
    head = (m0 == "mov" and o0.startswith("rcx, qword ptr [") and ((dm is not None and int(dm.group(1), 0) == disp) if disp else (o0 == via)))
    return head and any(m == "call" and o == "qword ptr [rax + 0x10]" for x, m, o in b)
R2 = (at(0x62BD2F)[:2] == ("imul", "rsi, rax, 0x58") and at(0x62BD33)[:2] == ("cmp", "qword ptr [rsi + rcx + 0x28], r14")
      and at(0x62BD6E)[:2] == ("lea", "rdx, [rax + 0x40]") and at(0x62BD75)[:2] == ("call", "0x62ec70")
      and at(0x62BD97)[:2] == ("mov", "rcx, qword ptr [rsi + rcx + 0x28]") and at(0x62BD9C)[:2] == ("call", "0x584730")
      and at(0x62BDBE)[:2] == ("mov", "qword ptr [rsi + rax + 0x28], r14")
      and all(rel(a, o) for a, o in ((0x62BDE0, 0x10), (0x62BE15, 0x18), (0x62BE4A, 0x20), (0x62BEB2, 8), (0x62BEE7, 0x30)))
      and at(0x62BE89)[:2] == ("mov", "rcx, qword ptr [rdi]") and at(0x62BE83)[:2] == ("lea", "rdi, [rsi + rax]") and at(0x62BE8F)[:2] == ("call", "qword ptr [rax + 0x10]"))
R3 = (at(0x62BFCF)[:2] == ("lea", "rcx, [rax + rax*4]") and at(0x62BFD3)[:2] == ("lea", "rsi, [rcx*8]")
      and rel(0x62BFDB, 8) and rel(0x62C010, 0x10) and at(0x62C04F)[:2] == ("mov", "rcx, qword ptr [rdi]") and at(0x62C049)[:2] == ("lea", "rdi, [rsi + rax]")
      and at(0x62C078)[:2] == ("cmp", "qword ptr [rsi + rax + 0x18], r14") and at(0x62C09C)[:2] == ("mov", "rcx, qword ptr [rsi + rcx + 0x18]")
      and at(0x62C0A1)[:2] == ("call", "0x584730"))
RC = (at(0x62C18F)[:2] == ("shl", "rdi, 6") and at(0x62C193)[:2] == ("cmp", "qword ptr [rdi + rax + 0x18], r14")
      and at(0x62C1CE)[:2] == ("lea", "rdx, [rax + 0x28]") and at(0x62C1D5)[:2] == ("call", "0x62ec70")
      and at(0x62C1F7)[:2] == ("mov", "rcx, qword ptr [rdi + rcx + 0x18]") and at(0x62C1FC)[:2] == ("call", "0x584730")
      and rel(0x62C240, 8) and rel(0x62C275, 0x10) and at(0x62C2AA)[:2] == ("add", "rdi, rax") and rel(0x62C2B2, 0, "rcx, qword ptr [rdi]"))
RK = (at(0x62B80F)[:2] == ("shl", "rdi, 4") and at(0x62B813)[:2] == ("add", "rdi, rcx") and rel(0x62B81B, 0, "rcx, qword ptr [rdi]")
      and at(0x62B843)[:2] == ("mov", "rcx, qword ptr [rbx + 0x10]") and at(0x62B851)[:2] == ("call", "0x584730"))
RS = (at(0x62BBAF)[:2] == ("lea", "rcx, [rax + rax*4]") and at(0x62BBB3)[:2] == ("lea", "rsi, [rcx*8]") and rel(0x62BBBB, 8)
      and rel(0x62BBF0, 0x10) and at(0x62BC29)[:2] == ("lea", "rdi, [rsi + rax]") and rel(0x62BC2F, 0, "rcx, qword ptr [rdi]") and rel(0x62BC58, 0x18))
check("R", R2 and R3 and RC and RK and RS, "release passes: 2D %s, 3D %s, cube %s, constant %s, structured %s" % (R2, R3, RC, RK, RS))
# store
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/d3d11-element-release/element_release.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def cells(l): return l.rstrip("\r\n").split("\t")
def row(t, o, sz, nm, ct, mean, rd, cf, ev): return [t, "0x%04X" % o, str(sz), nm, ct, mean, rd, cf, "RE-CUT 2026-09-28 (OPUS, %s %s). %s. %s" % (REC, ev, "was part of %s", EXE)]
P = "TYPE RESOLVED"
NEW = {
 ("Texture2DD3D11Element", 0x28): [
   row("Texture2DD3D11Element", 0x28, 8, "ownedBlock", "void*", "a heap block the element owns: the release pass 0062BCB0 frees it through 00584730 (0062BD9C) and nulls it, after removing the element's queued async update (+0x40) from the scheduler (0062EC70, 0062BD75) - the removal runs only when this is non-null. Its content is not read here", P, "PROVEN", "R"),
   row("Texture2DD3D11Element", 0x30, 8, "releasedObject30", "void*", "an object released like the views: 0062BCB0 calls its vtable slot +0x10 (the IUnknown Release position) and nulls it (0062BEE7 / 0062BEF8); which object it is and who stores it are not established", P, "PROVEN", "R")],
 ("Texture2DD3D11Element", 0x38): [
   row("Texture2DD3D11Element", 0x38, 4, "pendingCount", "uint32", "a count the release waits on: the drain 0062B100 reads it through 00623DF0 and calls Sleep(1) while it is above 0 (a signed test, jle), before the release pass runs. Who raises and lowers it is not established", P, "PROVEN", "W")],
 ("Texture3DD3D11Element", 0x18): [
   row("Texture3DD3D11Element", 0x18, 8, "ownedBlock", "void*", "a heap block the element owns: the release pass 0062BF40 frees it through 00584730 (0062C0A1) when non-null and nulls it. Its content is not read here", P, "PROVEN", "R"),
   row("Texture3DD3D11Element", 0x20, 4, "pendingCount", "uint32", "a count the release waits on: the drain 0062B170 reads it through 00623E30 and calls Sleep(1) while it is above 0 (a signed test, jle). Who raises and lowers it is not established", P, "PROVEN", "W"),
   row("Texture3DD3D11Element", 0x24, 4, "unobservedSpan0024", "u8[4]", "four bytes the allocator does not write; no reader found in the release path", "DISCOVERED", "UNKNOWN", "O W R")],
 ("TextureCubeMapD3D11Element", 0x18): [
   row("TextureCubeMapD3D11Element", 0x18, 8, "ownedBlock", "void*", "a heap block the element owns: when it is non-null the release pass 0062C100 removes the element's queued async update (+0x28) from the scheduler (0062EC70, 0062C1D5), frees the block through 00584730 (0062C1FC) and nulls it. Its content is not read here", P, "PROVEN", "R")],
 ("TextureCubeMapD3D11Element", 0x20): [
   row("TextureCubeMapD3D11Element", 0x20, 4, "pendingCount", "uint32", "a count the release waits on: the drain 0062B1E0 reads it through 00623E70 and calls Sleep(1) while it is above 0 (a signed test, jle). Who raises and lowers it is not established", P, "PROVEN", "W"),
   row("TextureCubeMapD3D11Element", 0x24, 4, "unobservedSpan0024", "u8[4]", "four bytes the allocator does not write; no reader found in the release path", "DISCOVERED", "UNKNOWN", "O W R")],
 ("ConstantBufferD3D11Element", 0x0C): [
   row("ConstantBufferD3D11Element", 0x0C, 4, "pendingCount", "uint32", "a count the release waits on: the drain 0062B020 reads it through 00623D70 and calls Sleep(1) while it is above 0 (a signed test, jle). The constructor zeroes it with +0x08; who raises and lowers it is not established", P, "PROVEN", "W")],
 ("StructuredBufferD3D11Element", 0x18): [
   row("StructuredBufferD3D11Element", 0x18, 8, "releasedObject18", "void*", "an object released like the views: the release pass 0062BB40 calls its vtable slot +0x10 (the IUnknown Release position) and nulls it (0062BC58 / 0062BC69); which object it is and who stores it are not established", P, "PROVEN", "R"),
   row("StructuredBufferD3D11Element", 0x20, 4, "pendingCount", "uint32", "a count the release waits on: the drain 0062B090 reads it through 00623DB0 and calls Sleep(1) while it is above 0 (a signed test, jle). Who raises and lowers it is not established", P, "PROVEN", "W"),
   row("StructuredBufferD3D11Element", 0x24, 4, "unobservedSpan0024", "u8[4]", "four bytes the allocator 0061CF20 does not write; no reader found in the release path", "DISCOVERED", "UNKNOWN", "O W R")],
}
ELEM = {"Texture2DD3D11Element": ("PTexture2DD3D11", "00611F80", "0062B100", "0062BCB0", "releases +0x00 +0x08 +0x10 +0x18 +0x20 +0x30 through vtable +0x10 and frees +0x28 after cancelling its queued async update"),
        "Texture3DD3D11Element": ("PTexture3DD3D11", "00610EC0", "0062B170", "0062BF40", "releases +0x00 +0x08 +0x10 and frees +0x18"),
        "TextureCubeMapD3D11Element": ("PTextureCubeMapD3D11", "00612B20", "0062B1E0", "0062C100", "frees +0x18 after cancelling its queued async update, and releases +0x00 +0x08 +0x10"),
        "ConstantBufferD3D11Element": ("PConstantBufferD3D11", "00611AD0", "0062B020", "0062B7B0", "releases +0x00 (the owner's +0x10 cpuData is freed after the loop)"),
        "StructuredBufferD3D11Element": ("PStructuredBufferD3D11", "006122D0", "0062B090", "0062BB40", "releases +0x00 +0x08 +0x10 +0x18")}
BASE = {"PTexture2DD3D11": ("+0x30", "+0x38", "005DE290"), "PTexture3DD3D11": ("+0x38", "+0x40", "005DE310"), "PTextureCubeMapD3D11": ("+0x30", "+0x38", "005DE390"),
        "PConstantBufferD3D11": ("+0x18", "+0x20", "0016D6A0"), "PStructuredBufferD3D11": ("+0x18", "+0x20", "0016D6A0")}
def ecell(t):
    o, dt, dr, rp, what = ELEM[t]
    return ("released in place by its owner's destroy %s (%s, READ 2026-09-28, OPUS, %s O W R): the drain %s first waits (Sleep(1)) until the "
            "element's pendingCount is not above 0, then the release pass %s %s, nulling each; the external array holding more than one "
            "element is then freed through 00584730 unless the count's bit 31 (keep-buffer) is set. When the owner is destroyed is not "
            "established" % (dt, o, REC, dr, rp, what))
def ocell(t, old):
    e = next(k for k, v in ELEM.items() if v[0] == t); o, dt, dr, rp, what = ELEM[e]; cnt, arr, base = BASE[t]
    return ("~~%s~~ %s - READ 2026-09-28 (OPUS, %s O): destroy(descriptor, obj) runs the drain %s, the release pass %s over every %s, frees the "
            "element array at %s through 00584730 when the count at %s (bit 31 masked) is above 1 and bit 31 is clear, nulls both, then "
            "the base destructor %s" % (old, dt, REC, dr, rp, e, arr, cnt, base))
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        k = (c[0], int(c[1], 16)) if c[0] in ELEM and c[1].startswith("0x") else None
        if k in NEW and c[3].startswith("unobservedSpan"):
            for r in NEW[k]:
                r = list(r); r[8] = r[8] % ("%s %s (%s)" % (c[3], c[4], c[5][:160]))
                out.append("\t".join(r) + e)
            continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in ELEM and c[6] == "": c[6] = ecell(c[0]); tl[i] = "\t".join(c) + e
        if c[0] in BASE and c[6].endswith("descriptor destroy slot +0x58, form not reduced"): c[6] = ocell(c[0], c[6]); tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
have = {(r[0], int(r[1], 16)): r for r in F if r[0] in ELEM}
ok = all((r[0], int(r[1], 16)) in have and have[(r[0], int(r[1], 16))][3] == r[3] and have[(r[0], int(r[1], 16))][2] == r[2] for v in NEW.values() for r in v)
ok &= all(sum(int(r[2]) for k, r in have.items() if k[0] == t) == int(T[t][1], 16) for t in ELEM)
ok &= all(REC in T[t][6] for t in list(ELEM) + list(BASE)) and not any(T[t][6].endswith("form not reduced") for t in BASE)
check("S", ok, "the spans are re-cut (tiling kept), the element release cells are filled and the owner cells reduced")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
