"""PTexture3DD3D11 (0x90) past its 0x38 base (OPUS, 2026-09-27). Static, certified EXE. No reflected members.
  D0 slot 10 of PClassDescriptorConcrete<PTexture3DD3D11> is 00611340, which constructs the object: base 005DCC10, count
     at +0x38 cleared then resized to one (00627750), +0x68..+0x8F zeroed
  D1 00627750's allocator 0061CF20 has stride 0x28 (rbx*5 << 3; add 0x28) and zeroes q 0/8/0x10/0x18 and d 0x20; no
     async-update object in this element
  D2 the device creates per element (index*5*8): CreateTexture3D (+0x30) into +0x00 and element 0's GetDesc (+0x50) into
     the class's +0x68 (00620250); a shader-resource view (+0x38) into +0x08 (0061FAF0); an unordered-access view (+0x40)
     into +0x10 (00620CB0)
  D3 +0x8C is the resources-created flag: 1 after 00620250 (0061E2B7), 0 in the release 0062BF40, tested by 00625F10 before
     the deferred-lighting release routes to 0062BF40 (006505A0)
  S  REGRESSION: the class rows and the element type exist and tile their extents (FAILS before)
"""
import os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
d = open(os.path.join(os.path.dirname(DB), "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read(); B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, k): return list(cs.disasm(d[off(a):off(a) + k], a))
def ops(a, k): return {(x.mnemonic, x.op_str) for x in ins(a, k)}
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return (x.mnemonic, x.op_str)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
vt = None
for l in open(os.path.join(DB, "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata", "members", "rtti-class-vtables.tsv"), encoding="utf-8"):
    r = l.rstrip("\n").split("\t")
    if r[0] == ".?AV?$PClassDescriptorConcrete@VPTexture3DD3D11@PRendering@Phyre@@@Phyre@@" and len(r) > 2: vt = int(r[2], 16)
check("D0 descriptor slot 10 00611340 constructs: base 005DCC10, count +0x38 resized to one, +0x68..+0x8F zeroed",
      vt is not None and struct.unpack_from("<Q", d, off(vt + 80))[0] == 0x611340
      and {("call", "0x5dcc10"), ("lea", "rcx, [rbx + 0x38]"), ("mov", "dword ptr [rcx], 0"), ("mov", "edx, 1"), ("call", "0x627750"),
           ("mov", "qword ptr [rbx + 0x88], 0"), ("mov", "qword ptr [rbx + 0x68], rax"), ("mov", "qword ptr [rbx + 0x80], rax")} <= ops(0x611340, 101))
A = ops(0x61CF20, 115)
check("D1 0061CF20: stride 0x28, q 0/8/0x10/0x18 and d 0x20 zeroed, no vtable",
      ("call", "0x61cf20") in ops(0x627750, 0xB0) and {("lea", "rcx, [rbx + rbx*4]"), ("shl", "rcx, 3"), ("add", "rcx, 0x28"),
      ("mov", "qword ptr [rax], r9"), ("mov", "qword ptr [rcx - 8], r9"), ("mov", "qword ptr [rcx], r9"), ("mov", "qword ptr [rcx + 8], r9"),
      ("mov", "dword ptr [rcx + 0x10], r9d")} <= A and not any(m == "lea" and "rip" in s for m, s in A))
check("D2 device calls: texture into +0x00 with GetDesc into class +0x68, SRV into +0x08, UAV into +0x10",
      at(0x620522) == ("lea", "rcx, [rax + rax*4]") and at(0x620534) == ("lea", "r9, [rdi + rdx]") and at(0x62053D) == ("call", "qword ptr [rax + 0x30]")
      and at(0x620569) == ("lea", "rdx, [rbx + 0x68]") and at(0x620570) == ("call", "qword ptr [rax + 0x50]")
      and at(0x61FBB0) == ("lea", "r9, [r8 + 8]") and at(0x61FBB4) == ("lea", "rcx, [rsi + rsi*4]") and at(0x61FBCF) == ("call", "qword ptr [rax + 0x38]")
      and at(0x620D70) == ("lea", "r9, [r8 + 0x10]") and at(0x620D74) == ("lea", "rcx, [rsi + rsi*4]") and at(0x620D8F) == ("call", "qword ptr [rax + 0x40]"))
check("D3 +0x8C is the resources-created flag",
      at(0x61E2B2) == ("call", "0x620250") and at(0x61E2B7) == ("mov", "dword ptr [rbx + 0x8c], 1")
      and at(0x62BF57) == ("xor", "r14d, r14d") and at(0x62BF5A) == ("mov", "dword ptr [rbx + 0x8c], r14d")
      and at(0x625F10) == ("cmp", "dword ptr [rcx + 0x8c], 0") and at(0x650609) == ("call", "0x625f10") and at(0x65061E) == ("jmp", "0x62bf40"))
F = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")]
T = {l.split("\t")[0]: l.split("\t") for l in open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8")}
rows = {int(r[1], 16): r for r in F if r[0] == "PTexture3DD3D11"}; elr = {int(r[1], 16): r for r in F if r[0] == "Texture3DD3D11Element"}
check("S the class rows and the element type exist and tile their extents",
      [rows.get(o, [0, 0, "", ""])[2:4] for o in (0x38, 0x68, 0x8C)] == [["48", "elements"], ["36", "textureDesc"], ["4", "resourcesCreated"]]
      and sum(int(r[2]) for r in rows.values()) == 0x90 and T.get("Texture3DD3D11Element", ["", ""])[1] == "0x28"
      and [elr.get(o, [0, 0, 0, ""])[3] for o in (0, 8, 0x10)] == ["texture", "shaderResourceView", "unorderedAccessView"]
      and sum(int(r[2]) for r in elr.values()) == 0x28)
print("FAILS", fails)
sys.exit(1 if fails else 0)
