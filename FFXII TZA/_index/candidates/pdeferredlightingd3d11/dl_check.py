"""PDeferredLightingD3D11's own tail +0x41D8..+0x4330 (OPUS, 2026-09-27, OPUS-STRUCT-PDEFERREDLIGHTINGD3D11). Static.
  L0 slot 10 of the class descriptor (006414F0) calls 00645BC0, which installs the class vtable, zeroes 38 qwords
     +0x41D8..+0x4300 and four +0x4310..+0x4328, and sets word +0x4308 := 1
  L1 +0x41D8..+0x4238 are 13 record pointers: the destructor 00646600 releases each through 006505A0, which dispatches on
     record byte +8 (0 -> 0062BCB0 PTexture2DD3D11, 1 -> 0062BF40 PTexture3DD3D11, 2 -> 0062C100 PTextureCubeMapD3D11);
     0065C330 resizes the group selected by the mode dword +0x4114 (1: 3 records, 2: 4, 3: 6)
  L2 +0x4240 / +0x4248 are PConstantBufferD3D11 objects (0x50 allocation, constructor 00615550 whose stores equal the
     class descriptor's own constructor 00611D60); +0x4250 / +0x4258 / +0x4318 / +0x4320 are PStructuredBufferD3D11
     objects (0x68, constructor 00616060 = descriptor constructor 006127C0); 0065D310 / 00650D40 destroy and null them
  L3 006568D0 stores the handle 0018D240 returns for each named effect parameter: 22 names, +0x4260..+0x4300 and +0x4328
  L4 +0x4308 is ANDed with ([02CC0410+0x168] >= 0xB000), the device's feature level against 11_0 (00655634..00655646)
  S  REGRESSION: the rows exist and tile 0x41D8..+0x4330 (FAILS before)
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
    if r[0].startswith(".?AV?$PClassDescriptorConcrete@VPDeferredLightingD3D11@") and len(r) > 2: vt = int(r[2], 16)
C = ops(0x645BC0, 338)
zero = {int(m.group(1), 16) for mn, s in C for m in [re.match(r"qword ptr \[rbx \+ (0x4[0-9a-f]{3})\], rax$", s)] if mn == "mov" and m}
check("L0 constructor 00645BC0 (descriptor slot 10 006414F0): 42 zeroed qwords, word +0x4308 := 1",
      vt is not None and struct.unpack_from("<Q", d, off(vt + 80))[0] == 0x6414F0 and ("call", "0x645bc0") in ops(0x6414F0, 0x30)
      and zero == set(range(0x41D8, 0x4301, 8)) | {0x4310, 0x4318, 0x4320, 0x4328} and ("mov", "word ptr [rbx + 0x4308], 1") in C
      and ("xor", "eax, eax") in C)
dtor = [x for x in ins(0x646600, 216)]
rel = [int(re.search(r"0x4[0-9a-f]{3}", x.op_str).group(0), 16) for k, x in enumerate(dtor)
       if x.mnemonic == "mov" and x.op_str.startswith("rcx, qword ptr [rbx + 0x4") and dtor[k + 1].op_str == "0x6505a0"]
disp = [(at(a)) for a in (0x6505CD, 0x6505DE, 0x6505F3, 0x650609, 0x65061E, 0x650633, 0x650648)]
check("L1 13 record pointers released by kind (0 2D / 1 3D / 2 cube); 0065C330 resizes the mode's group",
      rel == list(range(0x41D8, 0x4239, 8)) and at(0x6505AD) == ("movzx", "r8d, byte ptr [rcx + 8]")
      and disp == [("cmp", "r8b, 2"), ("call", "0x625f20"), ("jmp", "0x62c100"), ("call", "0x625f10"), ("jmp", "0x62bf40"),
                   ("call", "0x625f00"), ("jmp", "0x62bcb0")]
      and at(0x65C345) == ("mov", "ecx, dword ptr [rcx + 0x4114]"), "%s" % [hex(r) for r in rel][:3])
def storeset(a, k):
    return [(m.group(1), m.group(2) or "0") for x in ins(a, k) for m in [re.match(r"(qword|dword) ptr \[(?:rbx|rax|rcx)(?: \+ (0x[0-9a-f]+|\d+))?\], ", x.op_str)] if x.mnemonic == "mov" and m]
check("L2 +0x4240/+0x4248 PConstantBufferD3D11, +0x4250/+0x4258/+0x4318/+0x4320 PStructuredBufferD3D11",
      storeset(0x615550, 0x54) == storeset(0x611D60, 0x70) and storeset(0x616060, 0x4E) == storeset(0x6127C0, 0x70)
      and at(0x655F31) == ("mov", "ecx, 0x50") and at(0x655F4D) == ("call", "0x615550") and at(0x655F57) == ("mov", "qword ptr [rdi + 0x4240], rbx")
      and at(0x655FC6) == ("mov", "qword ptr [rdi + 0x4248], rbx")
      and at(0x650E00) == ("mov", "ecx, 0x68") and at(0x650E1D) == ("call", "0x616060") and at(0x650E27) == ("mov", "qword ptr [rbx + 0x4250], rdi")
      and at(0x650E76)[1] == "qword ptr [rbx + 0x4258], rdi"
      and at(0x656046)[1].startswith("qword ptr [") and "0x4318" in at(0x656046)[1] and "0x4320" in at(0x656091)[1]
      and ("call", "0x5dd5e0") in ops(0x65D310, 0x200) and ("call", "0x5de210") in ops(0x65D310, 0x200))
I = ins(0x6568D0, 0x240); last = None; names = {}; q = []
for x in I:
    m = re.search(r"rip \+ (0x[0-9a-f]+)\]", x.op_str)
    if x.mnemonic == "lea" and m and x.op_str.startswith("rdx"):
        t = x.address + x.size + int(m.group(1), 16); q.append(d[off(t):off(t) + 48].split(b"\0")[0].decode())
    elif x.mnemonic == "call" and x.op_str == "0x18d240": last = q.pop(0)
    else:
        m2 = re.match(r"qword ptr \[rbx \+ (0x4[0-9a-f]{3})\], rax$", x.op_str)
        if x.mnemonic == "mov" and m2: names[int(m2.group(1), 16)] = last
PARAMS = {0x4260: "ColorBuffer", 0x4268: "ShadowBuffer", 0x4270: "LightBuffer", 0x4278: "DeferredPos", 0x4280: "DeferredDir",
          0x4288: "DeferredColor", 0x4290: "DeferredSpotAngles", 0x4298: "DeferredAttenParams", 0x42A0: "DeferredShadowMask",
          0x42A8: "DeferredAmbientColor", 0x42B0: "DeferredLightConstantBuffer", 0x42B8: "DeferredDirectionalLightConstantBuffer",
          0x42C0: "NumDeferredLights", 0x42C8: "NumDeferredDirectionalLights", 0x42D0: "LightingOutputBuffer",
          0x42D8: "RWLightingOutputBuffer", 0x42E0: "DeferredInstantIntensity", 0x42E8: "DeferredInstantScatteringIntensity",
          0x42F0: "InstantLightColorBuffer", 0x42F8: "DeferredInstantLights", 0x4300: "RWScatteredLightingOutputBuffer",
          0x4328: "DeferredLightCount"}
check("L3 22 named parameter handles from 0018D240", names == PARAMS, str(len(names)))
check("L4 +0x4308 is gated on the device feature level >= 11_0",
      at(0x655634) == ("call", "0x5fd050") and at(0x655639) == ("cmp", "dword ptr [rax + 0x168], 0xb000")
      and at(0x655643) == ("setge", "al") and at(0x655646) == ("and", "byte ptr [rbx + 0x4308], al"))
F = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")]
rows = {int(r[1], 16): r for r in F if r[0] == "PDeferredLightingD3D11"}
tail = {o: r for o, r in rows.items() if o >= 0x41D8}
check("S the tail rows exist, carry the parameter names, and tile +0x41D8..+0x4330",
      tail.get(0x41D8, [0, 0, 0, ""])[3] == "textureRecords" and all(tail.get(o, [0, 0, 0, ""])[3] == "param" + nm for o, nm in PARAMS.items())
      and sum(int(r[2]) for r in tail.values()) == 0x158)
print("FAILS", fails)
sys.exit(1 if fails else 0)
