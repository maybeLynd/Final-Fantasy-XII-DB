"""empty_base_apply.py - OPUS (Claude Opus 5.5), 2026-09-28. Applies FABLE's ruling on OPUS-REQ-FABLE-EMPTY-BASE-ROW
(_index/candidates/empty-base-row-ruling/, 5e83431b8) to PShaderProgramD3D11 +0x0000 in _types/fields.tsv.

  E  the premise, re-derived from the certified image with OPUS's own decode (not FABLE's code): 00616880, 00616900 and
     0062BAB0 each load the qword at [this+0], call [vtable+0x10] on it and store 0 back - so +0x00..+0x07 is one pointer
     member of this class, released at the IUnknown Release slot
  R  REGRESSION (FAILS before): the base row is size 0, ctype PShaderProgramBase[0], meaning opens 'EMPTY BASE', name kept;
     the 8-byte member releasedObject00 (void*) sits at +0x0000; the old 1-byte base + unobservedSpan0001 u8[7] form is gone
  V  the live store validates for the type: types_index --validate reports no overlap / overrun / gap for PShaderProgramD3D11,
     and check_embed_parent_fields reports no ctype disagreement for it
The member's ctype is void* (as releasedObject78 of the fragment / geometry programs): the Release slot shows a COM-shaped
object, but which interface it is is not established.
Usage: python empty_base_apply.py [--patch]
"""
import hashlib, os, re, struct, subprocess, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
KIT = os.path.join(ROOT, "Tools", "analysis-kit", "gfz-scripts")
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

def releases_plus0(f):
    # within the first 0x80 bytes: some register R is loaded from [S] (S = a register holding this), R's vtable is loaded,
    # [vt + 0x10] is called, then a zero register is stored to [S]
    ins = list(cs.disasm(d[off(f):off(f) + 0x80], f)); held = {}; load = call = store = False
    for x in ins:
        m = re.fullmatch(r"(\w+), qword ptr \[(\w+)\]", x.op_str)
        if x.mnemonic == "mov" and m and m.group(2) in ("rcx", "rbx", "rdi", "rsi"): held[m.group(1)] = m.group(2); load = True
        if x.mnemonic == "call" and x.op_str == "qword ptr [rax + 0x10]" and load: call = True
        m = re.fullmatch(r"qword ptr \[(\w+)\], (\w+)", x.op_str)
        if x.mnemonic == "mov" and m and call and m.group(1) in held.values(): store = True; break
    return load and call and store
E = {"%08X" % a: releases_plus0(a) for a in (0x616880, 0x616900, 0x62BAB0)}
check("E", all(E.values()), "each D3D11 shader destructor loads [this+0], calls its slot +0x10 and stores back: %s" % E)

FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/d3d11-element-release/empty_base_apply.py"
RUL = "_index/candidates/empty-base-row-ruling/ (FABLE, 5e83431b8)"
EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
T = "PShaderProgramD3D11"
BASE_MEAN = ("EMPTY BASE (zero bytes here by the MSVC empty-base optimization): this class derives from PShaderProgramBase, whose "
             "complete-object size is 0x1, but as a base subobject it takes no storage - its offset is shared with the pointer member "
             "releasedObject00 at +0x0000. Ruled in %s; applied 2026-09-28 by OPUS (%s)" % (RUL, REC))
MEMBER = [T, "0x0000", "8", "releasedObject00", "void*",
          "an object released like the D3D11 views: the shader destructors 00616880 (fragment), 00616900 (geometry) and 0062BAB0 "
          "(vertex) load this qword, call its vtable slot +0x10 (the IUnknown Release position) and null it. Which object it is "
          "is not established",
          "TYPE RESOLVED", "PROVEN",
          "PLACED 2026-09-28 (OPUS, %s E; empty-base ruling %s; destructors from shader_programs.py F V). Replaces unobservedSpan0001 "
          "u8[7] at +0x0001, which held bytes 1..7 of this qword while the base row took byte 0. %s" % (REC, RUL, EXE)]
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == T and c[1] == "0x0000" and c[3] == "baseClass_PShaderProgramBase" and c[2] == "1":
            c[2], c[4] = "0", "PShaderProgramBase[0]"; c[5] = BASE_MEAN + ". WAS: " + c[5]
            c[8] += " || EMPTY BASE 2026-09-28 (OPUS, %s): size 1 -> 0, ctype PShaderProgramBase -> PShaderProgramBase[0] per %s" % (REC, RUL)
            out += ["\t".join(c) + e, "\t".join(MEMBER) + e]; continue
        if c[0] == T and c[1] == "0x0001" and c[3] == "unobservedSpan0001" and c[4] == "u8[7]": continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == T]
base = [r for r in F if r[3] == "baseClass_PShaderProgramBase"]
mem = [r for r in F if r[1] == "0x0000" and r[3] == "releasedObject00"]
check("R", len(base) == 1 and base[0][1:3] == ["0x0000", "0"] and base[0][4] == "PShaderProgramBase[0]" and base[0][5].startswith("EMPTY BASE")
      and len(mem) == 1 and mem[0][2:5] == ["8", "releasedObject00", "void*"]
      and not any(r[1] == "0x0001" for r in F),
      "base row 0x0000 / size 0 / PShaderProgramBase[0] / 'EMPTY BASE'; releasedObject00 void* at +0x0000; no +0x0001 row")
v = subprocess.run([sys.executable, os.path.join(KIT, "types_index.py"), "--store", os.path.join(DB, "_types"), "--validate"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
e = subprocess.run([sys.executable, os.path.join(KIT, "check_embed_parent_fields.py"), "--types", os.path.join(DB, "_types", "types.tsv"), "--fields", FI],
                   capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
errs = [l for l in v.splitlines() if T + " " in l and ("overlap" in l or "overrun" in l or "gap" in l)]
mism = [l for l in e.splitlines() if T in l and "ctype" in l]
check("V", not errs and not mism, "types_index errors for the type: %d; PASS 2 disagreements: %d" % (len(errs), len(mism)))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
