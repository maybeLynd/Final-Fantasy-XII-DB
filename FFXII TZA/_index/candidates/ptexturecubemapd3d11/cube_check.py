"""PTextureCubeMapD3D11 (0x350) past its 0x30 base (OPUS, 2026-09-27). Static, certified EXE. No reflected members.
  C0 slot 10 of PClassDescriptorConcrete<PTextureCubeMapD3D11> (00D51E90) is 00612D00, which calls 006161A0 on the object
  C1 006161A0 (after the base 005DCC40) clears the count at +0x30, resizes it to one element (00627800), zeroes +0x78..+0xA7
  C2 00627800 is the PSharray resize shape (bit 31 spares adopted storage, the inline address is never released); its
     allocator 0061CFA0 has stride 0x40 and builds each element: q 0/8/0x10/0x18, d 0x20, the
     TAsyncUpdate<PTextureCubeMapD3D11> vtable 00D54358 at +0x28
  C3 the device creates, per element (index << 6): CreateTexture2D (+0x28) into +0x00 (00620630), a shader-resource view
     (+0x38) on it into +0x08 (0061FC50), an unordered-access view (+0x40) into +0x10 (00620E10); element 0's texture
     reports its description (vtable +0x50) into the class's +0x78 (00620630)
  C4 the scheduler 0062C820 writes element +0x30 := the cube map, +0x38 := the index, and queues element +0x28
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
col = struct.unpack_from("<Q", d, off(0xD51E90 - 8))[0]; td = B + struct.unpack_from("<I", d, off(col) + 12)[0]
cname = d[off(td) + 16:off(td) + 120].split(b"\0")[0]
check("C0 00612D00 (slot 10 of the class descriptor's vtable) calls 006161A0 on the object",
      cname == b".?AV?$PClassDescriptorConcrete@VPTextureCubeMapD3D11@PRendering@Phyre@@@Phyre@@"
      and struct.unpack_from("<Q", d, off(0xD51E90 + 80))[0] == 0x612D00 and ("call", "0x6161a0") in ops(0x612D00, 44), cname.decode())
check("C1 006161A0: count at +0x30 cleared then resized to one; +0x78..+0xA7 zeroed",
      {("call", "0x5dcc40"), ("lea", "rcx, [rbx + 0x30]"), ("mov", "dword ptr [rcx], 0"), ("mov", "edx, 1"), ("call", "0x627800"),
       ("mov", "qword ptr [rbx + 0xa0], 0"), ("mov", "qword ptr [rbx + 0x78], rax"), ("mov", "qword ptr [rbx + 0x98], rax")} <= ops(0x6161A0, 102))
R = ops(0x627800, 164); A = ins(0x61CFA0, 130)
vt = [x for x in A if x.mnemonic == "lea" and "rip" in x.op_str][0]; vta = vt.address + vt.size + int(vt.op_str.split("+ ")[1].rstrip("]"), 16)
st = {}
for x in A:
    m = re.match(r"(qword|dword) ptr \[(rax|rcx)(?: ([+-]) (0x[0-9a-f]+|\d+))?\], ", x.op_str)
    if x.mnemonic == "mov" and m:
        o = (int(m.group(4), 0) * (-1 if m.group(3) == "-" else 1) if m.group(4) else 0) + (0x10 if m.group(2) == "rcx" else 0)
        st[o] = m.group(1)
check("C2 00627800 is the PSharray resize shape; 0061CFA0 builds 0x40-byte elements with the vtable at +0x28",
      {("btr", "ecx, 0x1f"), ("lea", "rdi, [rbx + 8]"), ("call", "0x61cfa0"), ("call", "0x584730"), ("mov", "dword ptr [rbx], ebp")} <= R
      and ("shl", "rcx, 6") in {(x.mnemonic, x.op_str) for x in A} and ("add", "rcx, 0x40") in {(x.mnemonic, x.op_str) for x in A}
      and st == {0: "qword", 8: "qword", 0x10: "qword", 0x18: "qword", 0x20: "dword", 0x28: "qword"} and vta == 0xD54358, "%X %s" % (vta, st))
check("C3 device calls: texture into +0x00, SRV into +0x08, UAV into +0x10, GetDesc into class +0x78",
      at(0x6208CF) == ("shl", "rdi, 6") and at(0x6208D6) == ("lea", "r9, [rdi + rcx]") and at(0x6208DD) == ("call", "qword ptr [rax + 0x28]")
      and at(0x620909) == ("lea", "rdx, [rbx + 0x78]") and at(0x620910) == ("call", "qword ptr [rax + 0x50]")
      and at(0x61FD0F) == ("lea", "r9, [rcx + 8]") and at(0x61FD1A) == ("shl", "rdi, 6") and at(0x61FD28) == ("call", "qword ptr [rax + 0x38]")
      and at(0x620ECF) == ("lea", "r9, [rcx + 0x10]") and at(0x620EDA) == ("shl", "rdi, 6") and at(0x620EE8) == ("call", "qword ptr [rax + 0x40]"))
check("C4 scheduler 0062C820: element +0x30 := the cube map, +0x38 := the index, element +0x28 queued",
      at(0x62C888) == ("shl", "rsi, 6") and at(0x62C944) == ("lea", "rdx, [rsi + 0x28]") and at(0x62C94B) == ("mov", "qword ptr [rdx + 8], rdi")
      and at(0x62C94F) == ("mov", "dword ptr [rdx + 0x10], ebp") and at(0x62C960) == ("call", "0x62eb90") and at(0x62C928) == ("mov", "ecx, dword ptr [rdi + 0x30]"))
check("C5 +0xA4 is the resources-created flag: 1 after 00620630, 0 in the release 0062C100, tested by 00625F20",
      at(0x61E319) == ("call", "0x620630") and at(0x61E31E) == ("mov", "dword ptr [rbx + 0xa4], 1")
      and at(0x62C117) == ("xor", "r14d, r14d") and at(0x62C11A) == ("mov", "dword ptr [rbx + 0xa4], r14d")
      and at(0x625F20) == ("cmp", "dword ptr [rcx + 0xa4], 0") and at(0x6505DE) == ("call", "0x625f20") and at(0x6505F3) == ("jmp", "0x62c100"))
F = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")]
T = {l.split("\t")[0]: l.split("\t") for l in open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8")}
rows = {int(r[1], 16): r for r in F if r[0] == "PTextureCubeMapD3D11"}
elr = {int(r[1], 16): r for r in F if r[0] == "TextureCubeMapD3D11Element"}
check("S the class rows and the element type exist and tile their extents",
      rows.get(0x30, [0, 0, "", ""])[2:4] == ["72", "elements"] and rows.get(0x78, [0, 0, "", ""])[2:4] == ["44", "textureDesc"] and rows.get(0xA4, [0, 0, "", ""])[2:4] == ["4", "resourcesCreated"]
      and sum(int(r[2]) for r in rows.values()) == 0x350 and T.get("TextureCubeMapD3D11Element", ["", ""])[1] == "0x40"
      and all(elr.get(o, [0, 0, 0, ""])[3] == nm for o, nm in {0: "texture", 8: "shaderResourceView", 0x10: "unorderedAccessView",
              0x28: "asyncUpdateVtable", 0x30: "asyncUpdateCubeMap", 0x38: "asyncUpdateIndex"}.items())
      and sum(int(r[2]) for r in elr.values()) == 0x40)
print("FAILS", fails)
sys.exit(1 if fails else 0)
