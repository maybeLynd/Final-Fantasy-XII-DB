"""PTexture2DD3D11 (0x188) past its 0x30 base (OPUS, 2026-09-27, OPUS-STRUCT-PTEXTURE2DD3D11). Static, certified EXE.
Reflection registers no member for this class, so every row rests on code.
  T1 the constructor 006160B0 (after the base 005DCBE0) sets +0x30 := 1 and builds one element in place at +0x38:
     qwords +0x38..+0x68, dword +0x70, the TAsyncUpdate<PTexture2DD3D11> vtable at +0x78; then zeroes +0x90..+0xBF
  T2 the element copy 00613770 has stride 0x58 and moves q 0..0x30, d 0x38, vtable 0x40, q 0x48, d 0x50 (never 0x3C/0x54)
  T3 +0x30 is a count with the PSharray rule: every walker strips bit 31 and takes the address +0x38 at count one,
     [+0x38] above one (0061FDA0, 0061F890, 00620B70, 0062C360); element i is base + i*0x58
  T4 the device ([02CC0410+0x108]) creates: CreateTexture2D (+0x28) into element +0x00 with initial data and into
     element +0x08 without (0061FDA0); CreateShaderResourceView (+0x38) on element +0x00 into +0x10 and on element +0x08
     into +0x18 (0061F890); CreateUnorderedAccessView (+0x40) into +0x20 (00620B70); element +0x00's vtable +0x50
     (ID3D11Resource-derived GetDesc) fills the class's +0x90 (0061FDA0)
  T5 the scheduler 0062C360 writes element +0x48 := the texture, +0x50 := the index, and queues element +0x40 (0062EB90)
  S  REGRESSION: the store carries the carve (FAILS before)
Not claimed: element +0x28 / +0x30 / +0x38 roles, the +0xC0..+0x187 tail, what the textures hold.
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
def stores(f, k, base):
    out = {}
    for x in ins(f, k):
        m = re.match(r"(qword|dword) ptr \[%s(?: \+ (0x[0-9a-f]+|\d+))?\], " % base, x.op_str)
        if x.mnemonic == "mov" and m: out[int(m.group(2) or "0", 0)] = m.group(1)
    return out
col = struct.unpack_from("<Q", d, off(0xD51510 - 8))[0]; td = B + struct.unpack_from("<I", d, off(col) + 12)[0]
cname = d[off(td) + 16:off(td) + 120].split(b"\0")[0]
check("T0 006160B0 is PTexture2DD3D11's constructor: slot 10 of PClassDescriptorConcrete<PTexture2DD3D11> (00D51510) is 006123F0, which calls it on the object",
      cname == b".?AV?$PClassDescriptorConcrete@VPTexture2DD3D11@PRendering@Phyre@@@Phyre@@"
      and struct.unpack_from("<Q", d, off(0xD51510 + 80))[0] == 0x6123F0
      and ("mov", "rcx, rdx") in ops(0x6123F0, 0x30) and ("call", "0x6160b0") in ops(0x6123F0, 0x30), cname.decode())
C = ops(0x6160B0, 139)
el = stores(0x6160B0, 139, "rax"); cls = stores(0x6160B0, 139, "rbx")
lea_vt = [x for x in ins(0x6160B0, 139) if x.mnemonic == "lea" and "rip" in x.op_str][0]
vt = lea_vt.address + lea_vt.size + int(re.search(r"0x[0-9a-f]+", lea_vt.op_str.split("+")[1]).group(0), 16)
check("T1 constructor: count 1 at +0x30, element in place at +0x38, vtable at element +0x40, +0x90..+0xBF zeroed",
      ("call", "0x5dcbe0") in C and ("lea", "rax, [rbx + 0x38]") in C and ("mov", "dword ptr [rbx + 0x30], 1") in C
      and el == {0: "qword", 8: "qword", 0x10: "qword", 0x18: "qword", 0x20: "qword", 0x28: "qword", 0x30: "qword", 0x38: "dword", 0x40: "qword"}
      and {0x90, 0x98, 0xA0, 0xA8, 0xB0, 0xB8} <= set(cls) and vt == 0xD54348, "vtable %X" % vt)
cp = stores(0x613770, 133, "rax")
check("T2 element copy: stride 0x58; q 0-0x30, d 0x38, vtable 0x40, q 0x48, d 0x50",
      ("add", "r9, 0x58") in ops(0x613770, 133) and ("add", "rdx, 0x58") in ops(0x613770, 133)
      and cp == {0: "qword", 8: "qword", 0x10: "qword", 0x18: "qword", 0x20: "qword", 0x28: "qword", 0x30: "qword", 0x38: "dword", 0x40: "qword", 0x48: "qword", 0x50: "dword"})
W = {0x61FDA0: 1190, 0x61F890: 598, 0x620B70: 317, 0x62C360: 0x210}
walk = {f: ("btr", "eax, 0x1f") in ops(f, k) and any(m == "lea" and s.endswith("[rbx + 0x38]") for m, s in ops(f, k))
        and any(m == "mov" and s.endswith("qword ptr [rbx + 0x38]") for m, s in ops(f, k)) for f, k in W.items()}
check("T3 walkers apply the PSharray rule to +0x30 / +0x38 with stride 0x58", all(walk.values())
      and at(0x6200D4) == ("imul", "rdi, rax, 0x58") and at(0x61F963) == ("imul", "rdi, rax, 0x58"), str(walk))
check("T4 device calls: textures into +0x00 / +0x08, SRVs into +0x10 / +0x18, UAV into +0x20, GetDesc into class +0x90",
      at(0x6200DE) == ("lea", "r9, [rdi + rcx]") and at(0x6200E5) == ("call", "qword ptr [rax + 0x28]")
      and at(0x620176) == ("lea", "r9, [rcx + 8]") and at(0x620182) == ("xor", "r8d, r8d") and at(0x620188) == ("call", "qword ptr [rax + 0x28]")
      and at(0x61F95D) == ("lea", "r9, [rcx + 0x10]") and at(0x61F975) == ("mov", "rdx, qword ptr [rdi + rdx]") and at(0x61F979) == ("call", "qword ptr [rax + 0x38]")
      and at(0x61FA3E) == ("mov", "rdx, qword ptr [rdi + rcx + 8]") and at(0x61FA69) == ("lea", "r9, [rcx + 0x18]") and at(0x61FA78) == ("call", "qword ptr [rax + 0x38]")
      and at(0x620C1C) == ("lea", "r9, [rcx + 0x20]") and at(0x620C38) == ("call", "qword ptr [rax + 0x40]")
      and at(0x620111) == ("lea", "rdx, [rbx + 0x90]") and at(0x62011B) == ("call", "qword ptr [rax + 0x50]"))
check("T5 scheduler: element +0x48 := the texture, +0x50 := the index, element +0x40 queued",
      at(0x62C4AA) == ("lea", "rdx, [r15 + 0x40]") and at(0x62C4B1) == ("mov", "qword ptr [rdx + 8], rbx")
      and at(0x62C4B5) == ("mov", "dword ptr [rdx + 0x10], r9d") and at(0x62C4C7) == ("call", "0x62eb90"))
check("T6 +0xBC is the resources-created flag: 1 after 0061FDA0, 0 in the release 0062BCB0, tested by 00625F00",
      at(0x61E242) == ("call", "0x61fda0") and at(0x61E247) == ("mov", "dword ptr [rbx + 0xbc], 1")
      and at(0x62BCC7) == ("xor", "r14d, r14d") and at(0x62BCCA) == ("mov", "dword ptr [rbx + 0xbc], r14d")
      and at(0x625F00) == ("cmp", "dword ptr [rcx + 0xbc], 0") and at(0x650628) == ("mov", "rbx, qword ptr [rcx]")
      and at(0x650633) == ("call", "0x625f00") and at(0x650648) == ("jmp", "0x62bcb0"))
F = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")]
rows = {int(r[1], 16): r for r in F if r[0] == "PTexture2DD3D11"}
elr = {int(r[1], 16): r for r in F if r[0] == "Texture2DD3D11Element"}
T = {l.split("\t")[0]: l.split("\t") for l in open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8")}
wantc = {0x30: ("96", "elements"), 0x90: ("44", "textureDesc"), 0xBC: ("4", "resourcesCreated")}
wante = {0x00: "texture", 0x08: "secondTexture", 0x10: "shaderResourceView", 0x18: "secondShaderResourceView",
         0x20: "unorderedAccessView", 0x40: "asyncUpdateVtable", 0x48: "asyncUpdateTexture", 0x50: "asyncUpdateIndex"}
check("S the store carries the class rows and the element type, each tiling its extent",
      all(o in rows and (rows[o][2], rows[o][3]) == v for o, v in wantc.items()) and sum(int(r[2]) for r in rows.values()) == 0x188
      and "Texture2DD3D11Element" in T and T["Texture2DD3D11Element"][1] == "0x58"
      and all(o in elr and elr[o][3] == nm for o, nm in wante.items()) and sum(int(r[2]) for r in elr.values()) == 0x58)
print("FAILS", fails)
sys.exit(1 if fails else 0)
