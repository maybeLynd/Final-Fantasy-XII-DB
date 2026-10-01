"""shader_programs.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The D3D11 shader-program destructors read
bytes the store keeps as unregistered spans.

  F  the fragment and geometry destructors 00616880 / 00616900 (their descriptors' destroy slots 00611670 / 00611C30 call them)
     share one body: release +0x78 through vtable slot +0x10 and null it; release +0x00 the same way and null it; free [+0x10]
     through 00584730 when the dword at +0x08 is non-zero and its bit 31 is clear, null both; tail-jump to 00616B40
  B  00616B40, PShaderProgramD3D11's destructor: frees [+0x20] (m_compiledCode's data, count +0x18) and [+0x10] (count +0x08)
     through 00584730 unless the count's bit 31 is set, nulling each pair
  V  the vertex program's 0062BAB0 also releases +0x00 and frees +0x10 (count +0x08) - the same base fields
  So PShaderFragmentProgramD3D11 / PShaderGeometryProgramD3D11 +0x78 is a released object, and PShaderProgramD3D11 has an
  unregistered counted array at +0x08 / +0x10 (count u32 with bit 31 the keep flag, pointer) and a released object at +0x00.
  THE +0x00 QWORD CONFLICTS WITH THE STORE: the row there is 'baseClass_PShaderProgramBase', 1 byte (the reflection's instance
  size of an empty class), followed by unobservedSpan0001. With the empty base taking no bytes, the qword at +0x00 is the D3D11
  class's own member. The base row is not changed here; bytes +0x01..+0x07 are described as the rest of that qword, and the
  representation of the empty base is asked of FABLE (OPUS-REQ-FABLE-EMPTY-BASE-ROW).
  S  REGRESSION: the three spans are re-cut, tiling kept (FAILS before)
Usage: python shader_programs.py [--patch]
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
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
A = lambda pairs: all(at(a) == v for a, v in pairs)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def body(f):
    return A([(f + 0x17, ("mov", "rcx, qword ptr [rcx + 0x78]")), (f + 0x25, ("call", "qword ptr [rax + 0x10]")), (f + 0x29, ("mov", "qword ptr [rbx + 0x78], rdi")),
              (f + 0x2D, ("mov", "rcx, qword ptr [rbx]")), (f + 0x38, ("call", "qword ptr [rax + 0x10]")), (f + 0x3C, ("mov", "qword ptr [rbx], rdi")),
              (f + 0x3F, ("mov", "eax, dword ptr [rbx + 8]")), (f + 0x46, ("mov", "rcx, qword ptr [rbx + 0x10]")), (f + 0x4F, ("shr", "eax, 0x1f")),
              (f + 0x58, ("call", "0x584730")), (f + 0x5E, ("mov", "qword ptr [rbx + 0x10], rdi")), (f + 0x62, ("mov", "dword ptr [rbx + 8], edi")),
              (f + 0x72, ("jmp", "0x616b40"))])
check("F", body(0x616880) and body(0x616900) and A([(0x611677, ("call", "0x616880")), (0x611C37, ("call", "0x616900"))]),
      "00616880 / 00616900: release +0x78 and +0x00, free +0x10 (count +0x08), then 00616B40")
check("B", A([(0x616B57, ("mov", "eax, dword ptr [rcx + 0x18]")), (0x616B63, ("mov", "rcx, qword ptr [rcx + 0x20]")), (0x616B6C, ("call", "0x584730")),
              (0x616B7B, ("mov", "eax, dword ptr [rbx + 8]")), (0x616B87, ("mov", "rcx, qword ptr [rbx + 0x10]")), (0x616B90, ("call", "0x584730")),
              (0x616B96, ("mov", "qword ptr [rbx + 0x10], rdi")), (0x616B9A, ("mov", "dword ptr [rbx + 8], edi"))]),
      "00616B40 frees m_compiledCode's data (+0x20 / +0x18) and the +0x10 array (+0x08)")
check("V", A([(0x62BAD8, ("mov", "rcx, qword ptr [rbx]")), (0x62BAE3, ("call", "qword ptr [rax + 0x10]")), (0x62BAE6, ("mov", "qword ptr [rbx], rdi")),
              (0x62BAE9, ("mov", "eax, dword ptr [rbx + 8]")), (0x62BAF0, ("mov", "rcx, qword ptr [rbx + 0x10]")), (0x62BB02, ("call", "0x584730"))]),
      "the vertex program's 0062BAB0 releases +0x00 and frees +0x10 (count +0x08)")
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/d3d11-element-release/shader_programs.py"
EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def cells(l): return l.rstrip("\r\n").split("\t")
def ev(was, tag): return "RE-CUT 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def cut(t, rd, was):
    if t != "PShaderProgramD3D11":
        return [[t, "0x0078", "8", "releasedObject78", "void*", "an object released like the D3D11 views: this class's destructor (00616880 fragment / 00616900 geometry) calls its vtable slot +0x10 (the IUnknown Release position) and nulls it. Which object it is is not established", "TYPE RESOLVED", "PROVEN", ev(was, "F")]]
    return [[t, "0x0001", "7", "unobservedSpan0001", "u8[7]", "bytes 1..7 of the qword at +0x00 that the D3D11 shader destructors (00616880, 00616900, 0062BAB0) load, release through its vtable slot +0x10 and null - an object pointer occupying +0x00..+0x07. The store's +0x00 row is the 1-byte empty base PShaderProgramBase; how an empty base that takes no bytes is represented is asked of FABLE (OPUS-REQ-FABLE-EMPTY-BASE-ROW)", rd, "PROVEN", ev(was, "F V")],
            [t, "0x0008", "4", "arrayCount08", "uint32", "the element count of the array at +0x10 (bit 31 set keeps it): 00616B40 and the derived destructors free the array through 00584730 when it is non-zero and bit 31 is clear, then zero it; the same count / pointer layout as m_compiledCode at +0x18 / +0x20", "TYPE RESOLVED", "PROVEN", ev(was, "F B V")],
            [t, "0x000C", "4", "unobservedSpan000C", "u8[4]", "four bytes after the count; not read by the destructors", rd, "UNKNOWN", ev(was, "F B")],
            [t, "0x0010", "8", "array10", "void*", "a heap array freed through 00584730 by 00616B40 and the derived destructors (count at +0x08, bit 31 keeps it), then nulled; its elements are not read here", "TYPE RESOLVED", "PROVEN", ev(was, "F B V")]]
SPAN = {("PShaderFragmentProgramD3D11", "0x0078", "8"), ("PShaderGeometryProgramD3D11", "0x0078", "8"), ("PShaderProgramD3D11", "0x0001", "23")}
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if (c[0], c[1], c[2]) in SPAN and c[3].startswith("unobservedSpan"):
            out += ["\t".join(r) + e for r in cut(c[0], c[6], "%s %s (%s)" % (c[3], c[4], c[5][:200]))]; continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
T = {cells(l)[0]: cells(l) for l in open(os.path.join(DB, "_types", "types.tsv"), "rb").read().decode("utf-8").splitlines()}
TY = [s[0] for s in SPAN]
F = {(cells(l)[0], int(cells(l)[1], 16)): cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] in TY}
ok = (F.get(("PShaderFragmentProgramD3D11", 0x78), [0, 0, 0, ""])[3] == "releasedObject78" and F.get(("PShaderGeometryProgramD3D11", 0x78), [0, 0, 0, ""])[3] == "releasedObject78"
      and F.get(("PShaderProgramD3D11", 8), [0, 0, 0, ""])[3] == "arrayCount08" and F.get(("PShaderProgramD3D11", 0x10), [0, 0, 0, ""])[3] == "array10"
      and all(sum(int(r[2]) for k, r in F.items() if k[0] == t) == int(T[t][1], 16) for t in TY))
check("S", ok, "fragment / geometry +0x78 and PShaderProgramD3D11 +0x01..+0x17 re-cut; tiling kept")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
