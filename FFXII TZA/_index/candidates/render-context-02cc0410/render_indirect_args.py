"""render_indirect_args.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
RenderContext02CC0410 +0x7B8 (com7B8): its creator, users and release - a 16-byte draw-indirect arguments buffer.

  C  CREATOR: the initialiser (00625DE3..00625E25), only when featureLevel (+0x168) >= 0xB000 (D3D_FEATURE_LEVEL_11_0), calls the
     device's CreateBuffer (slot +0x18) with a D3D11_BUFFER_DESC of ByteWidth 0x10, Usage 0 (DEFAULT), BindFlags 0, CPUAccess 0,
     MiscFlags 0x10 (DRAWINDIRECT_ARGS), StructureByteStride 4, into this + 0x7B8
  U  USE: 0061EDA4 copies a UAV's hidden structure count into it (device context +0x110, slot +0x188 = CopyStructureCount, offset
     0) and then copies it to another resource (slot +0x178 = CopyResource, source = this buffer)
  L  LIFETIME: the constructor zeroes it (00615840); the teardown releases it through slot +0x10 and zeroes it (0062B6EB..0062B6FD).
     Below feature level 11_0 it stays null
  W  REGRESSION (FAILS before): the row names the buffer and its condition
Usage: python render_indirect_args.py [--patch]
"""
import hashlib, os, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
    miss = [hex(a) for a, v in pairs if A.get(a) != v]
    if miss: print("   missing", miss)
    return not miss
check("C", has(0x625DD6, 0x625E2C, [(0x625DE3, ("cmp", "dword ptr [r14 + 0x168], 0xb000")), (0x625DEE, ("jl", "0x625e2c")), (0x625DF4, ("lea", "r9, [r14 + 0x7b8]")),
                                     (0x625DFD, ("mov", "qword ptr [rbp - 0x78], 0x10")), (0x625E0D, ("mov", "qword ptr [rbp - 0x70], rax")),
                                     (0x625E14, ("mov", "dword ptr [rbp - 0x68], 0x10")), (0x625E1B, ("mov", "dword ptr [rbp - 0x64], 4")),
                                     (0x625E25, ("call", "qword ptr [rax + 0x18]"))]),
      "feature level >= 11_0: CreateBuffer {16 B, DEFAULT, bind 0, CPU 0, misc 0x10 DRAWINDIRECT_ARGS, stride 4} into +0x7B8")
check("U", has(0x61EDA4, 0x61EE15, [(0x61EDAE, ("mov", "rdi, qword ptr [rcx + 0x110]")), (0x61EDC0, ("mov", "rdx, qword ptr [rbp + 0x7b8]")),
                                     (0x61EDCA, ("xor", "r8d, r8d")), (0x61EDD0, ("call", "qword ptr [rbx + 0x188]")), (0x61EDEB, ("mov", "r8, qword ptr [rbp + 0x7b8]")),
                                     (0x61EDF8, ("call", "qword ptr [rdi + 0x178]"))]),
      "0061EDA4: CopyStructureCount(dst = +0x7B8, 0, uav) then CopyResource(other, +0x7B8)")
check("L", has(0x62B6EB, 0x62B704, [(0x62B6EB, ("mov", "rcx, qword ptr [rbx + 0x7b8]")), (0x62B6FA, ("call", "qword ptr [rax + 0x10]")), (0x62B6FD, ("mov", "qword ptr [rbx + 0x7b8], rdi"))]),
      "the teardown releases and nulls it")
REC = "_index/candidates/render-context-02cc0410/render_indirect_args.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
M = ("an ID3D11Buffer of 16 bytes for draw-indirect arguments, created only when featureLevel (+0x168) >= 0xB000 (11_0): DEFAULT usage, "
     "no bind flags, MiscFlags 0x10 (DRAWINDIRECT_ARGS), stride 4 (00625DE3..00625E25). 0061EDA4 copies a UAV's structure count into it "
     "(CopyStructureCount, device context slot +0x188) and copies it on (CopyResource, slot +0x178); the teardown releases it; null below 11_0")
FI = os.path.join(DB, "_types", "fields.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "RenderContext02CC0410" and c[1] == "0x07B8" and c[3] == "com7B8":
            was = "%s (%s)" % (c[3], c[5])
            c[3] = "drawIndirectArgs7B8"; c[5] = M; c[6], c[7] = "TYPE RESOLVED", "PROVEN"
            c[8] += " || RESOLVED 2026-09-28 (OPUS, %s C U L). was %s" % (REC, was); fl[i] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
row = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "RenderContext02CC0410" and cells(l)[1] == "0x07B8"]
check("W", len(row) == 1 and row[0][3] == "drawIndirectArgs7B8" and "DRAWINDIRECT_ARGS" in row[0][5], "+0x7B8 names the draw-indirect buffer and its feature-level condition")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
