"""The 0x48-byte D3D11 buffer element that PSharray m_buffers holds (PDataBlockBufferD3D11 / PIndexDataBlockBufferD3D11)
(OPUS, 2026-09-27, OPUS-STRUCT-PDATABLOCKBUFFER-D3D11). Static, certified EXE.
  E1 the device: 005FD050 (and 00624670, a jmp to it) returns the magic static 02CC0410 = R; 00625830 (receiver R, via
     006253D0 <- 0079F4AC on 00624670's return) calls D3D11CreateDeviceAndSwapChain (thunk 0080F2C8) with
     ppDevice = R+0x108 and ppImmediateContext = R+0x110
  E2 the creators 0066F970 / 0066FAB0 / 00670070 / 0066FE20 load [005FD050()+0x108] and call its vtable+0x18
     (ID3D11Device::CreateBuffer) with ppBuffer = element +0x00; 00670070 / 0066FE20 then call vtable+0x38
     (CreateShaderResourceView) with ppSRView = element +0x08; element +0x40 is stored 0
  E3 widths: the element constructors 0065F690 / 0065F340 and the copies 00661720 / 0065F700 / 00672F30 / 00673030
     move qwords at +0x00 +0x08 +0x10 +0x18 +0x30 +0x40, dwords at +0x20 +0x38, install the TAsyncUpdate vtable at
     +0x28, and never touch +0x24 or +0x3C
  E4 the schedulers 00674610 / 006747D0 write element+0x28+8 = the data block itself and element+0x28+0x10 = the
     element's index, then hand element+0x28 to 0062EB90
  E5 the update: TAsyncUpdate<PDataBlockD3D11> (00D68DD0) / <PIndexDataBlockD3D11> (00D68DE0) slot 0 = 00670570 /
     00670580: rcx = [this+8] (the block), edx = [this+0x10] (the index) -> 00670590 / 00670690, which Map through
     [R+0x110], memcpy (VCRUNTIME140) from element +0x40 for the block's m_dataSize (+0x78 / +0x70), and Unmap
     (context vtable+0x78) on element +0x00
  S  REGRESSION: both element types carry the carved rows (FAILS before)
Not claimed: +0x10..+0x23 (zeroed and copied; no reader found), +0x24 / +0x3C (never touched), what the buffers hold.
"""
import os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(os.path.dirname(DB), "Tools", "work", "exe", "FFXII_TZA.exe")
pe = pefile.PE(EXE, fast_load=True); pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
B = pe.OPTIONAL_HEADER.ImageBase; d = open(EXE, "rb").read()
IMPORTS = {i.address: (i.name or b"").decode() for e in pe.DIRECTORY_ENTRY_IMPORT for i in e.imports}
def off(v): return pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, n): return list(cs.disasm(d[off(a):off(a) + n], a))
def ops(a, n): return {(x.mnemonic, x.op_str) for x in ins(a, n)}
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return (x.mnemonic, x.op_str)
def rip(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip \+ (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + int(m.group(1), 16)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok

# E1
between = [x for x in ins(0x6253F8, 0x6257D4 - 0x6253F8) if re.match(r"(rbx|ebx)\b", x.op_str) and x.mnemonic in ("mov", "lea", "xor", "pop")]
check("E1 R = 02CC0410; D3D11CreateDeviceAndSwapChain fills R+0x108 (device) and R+0x110 (context)",
      rip(0x5FD097) == 0x2CC0410 and rip(0x5FD0C4) == 0x2CC0410 and at(0x624670) == ("jmp", "0x5fd050")
      and at(0x79F472) == ("call", "0x624670") and at(0x79F499) == ("mov", "rcx, rax") and at(0x79F4AC) == ("call", "0x6253d0")
      and at(0x6253F8) == ("mov", "rbx, rcx") and at(0x6257BA) == ("mov", "rcx, rbx") and at(0x6257D4) == ("call", "0x625830")
      and not [x for x in between if x.address != 0x6253F8 and x.op_str.startswith(("rbx", "ebx"))]
      and at(0x625861) == ("mov", "r14, rcx") and at(0x6259E8) == ("lea", "r12, [r14 + 0x108]")
      and at(0x625A40) == ("mov", "qword ptr [rsp + 0x48], r12") and at(0x625A26) == ("lea", "rax, [r14 + 0x110]")
      and at(0x625A2D) == ("mov", "qword ptr [rsp + 0x58], rax") and at(0x625A64) == ("call", "0x80f2c8")
      and IMPORTS.get(rip(0x80F2C8)) == "D3D11CreateDeviceAndSwapChain", IMPORTS.get(rip(0x80F2C8)))

# E2
C = {0x66F970: 318, 0x66FAB0: 318, 0x670070: 589, 0x66FE20: 589}
e2 = {}
for f, n in C.items():
    o = ops(f, n)
    dev = ("call", "0x5fd050") in o and any(m == "mov" and s.endswith("qword ptr [rax + 0x108]") for m, s in o)
    cb = any(m == "call" and s.endswith("+ 0x18]") for m, s in o)
    z40 = any(m == "mov" and re.match(r"qword ptr \[\w+ \+ \w+ \+ 0x40\], (r15|0)$", s) for m, s in o)
    srv = any(m == "call" and s.endswith("+ 0x38]") for m, s in o) and any(m == "lea" and s.endswith("[rcx + 8]") for m, s in o)
    e2[f] = (dev, cb, z40, srv)
check("E2 creators: CreateBuffer into +0x00 (all four), CreateShaderResourceView into +0x08 (00670070, 0066FE20), +0x40 := 0",
      all(v[0] and v[1] and v[2] for v in e2.values()) and e2[0x670070][3] and e2[0x66FE20][3]
      and at(0x670248) == ("lea", "r9, [rcx + 8]") and at(0x66FFF8) == ("lea", "r9, [rcx + 8]"),
      str({"%08X" % k: v for k, v in e2.items()}))

# E3
def stores(f, n, base):
    out = {}
    for x in ins(f, n):
        m = re.match(r"(qword|dword) ptr \[%s(?: \+ (0x[0-9a-f]+|\d+))?\], " % base, x.op_str)
        if x.mnemonic == "mov" and m: out[int(m.group(2) or "0", 0)] = m.group(1)
    return out
FULL = {0: "qword", 8: "qword", 0x10: "qword", 0x18: "qword", 0x20: "dword", 0x28: "qword", 0x30: "qword", 0x38: "dword", 0x40: "qword"}
CTOR = {k: v for k, v in FULL.items() if k <= 0x28}
ASSIGN = {k: v for k, v in FULL.items() if k != 0x28}   # assignment keeps the destination's own vtable
okc = stores(0x65F690, 39, "rdx") == CTOR and stores(0x65F340, 39, "rdx") == CTOR
okp = all(stores(f, n, b) == FULL for f, n, b in ((0x661720, 117, "rax"), (0x6618A0, 117, "rax"), (0x672F30, 243, "rdx"), (0x673030, 243, "rdx"))) \
      and stores(0x65F700, 84, "rbx") == ASSIGN and stores(0x65F3E0, 84, "rbx") == ASSIGN
check("E3 constructors, copies and assignments: q 0/8/10/18/30/40, d 20/38, vtable 28 (not on assignment); 24 and 3C never", okc and okp)

# E4
s1 = ops(0x6747D0, 129); s2 = ops(0x674610, 0x1C0)
check("E4 schedulers: element+0x30 := the block, element+0x38 := the index, element+0x28 -> 0062EB90",
      {("add", "rdx, 0x28"), ("mov", "qword ptr [rdx + 8], r8"), ("mov", "dword ptr [rdx + 0x10], r10d"), ("call", "0x62eb90")} <= s1
      and {("lea", "rdx, [rdi + 0x28]"), ("mov", "qword ptr [rdx + 8], rbx"), ("mov", "dword ptr [rdx + 0x10], esi"), ("call", "0x62eb90")} <= s2)

# E5
vt = {0xD68DD0: 0x670570, 0xD68DE0: 0x670580}
okv = all(struct.unpack_from("<Q", d, off(v))[0] == m for v, m in vt.items())
okm = all(at(m) == ("mov", "edx, dword ptr [rcx + 0x10]") and at(m + 3) == ("mov", "rcx, qword ptr [rcx + 8]") for m in vt.values())
u1 = ops(0x670590, 241); u2 = ops(0x670690, 241)
memcpy = IMPORTS.get(rip(0x861EBA)) == "memcpy"
check("E5 the update: memcpy from element +0x40 for the block's m_dataSize, Unmap on element +0x00",
      okv and okm and memcpy and at(0x670577) == ("jmp", "0x670590") and at(0x670587) == ("jmp", "0x670690")
      and {("mov", "rdx, qword ptr [rdi + rdx + 0x40]"), ("mov", "r8d, dword ptr [rbx + 0x78]"), ("call", "0x861eba"), ("call", "qword ptr [rax + 0x78]")} <= u1
      and {("mov", "rdx, qword ptr [rdi + rdx + 0x40]"), ("mov", "r8d, dword ptr [rbx + 0x70]"), ("call", "0x861eba"), ("call", "qword ptr [rax + 0x78]")} <= u2)

F = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")]
want = {0x0: ("8", "buffer"), 0x8: ("8", "shaderResourceView"), 0x28: ("8", "asyncUpdateVtable"), 0x30: ("8", "asyncUpdateBlock"),
        0x38: ("4", "asyncUpdateIndex"), 0x40: ("8", "pendingUploadSource")}
okS = True
for t in ("PDataBlockBufferD3D11", "PIndexDataBlockBufferD3D11"):
    rows = {int(r[1], 16): r for r in F if r[0] == t}
    okS &= all(o in rows and rows[o][2] == w and rows[o][3] == nm for o, (w, nm) in want.items()) and sum(int(r[2]) for r in rows.values()) == 0x48
check("S both element types carry the carved rows and still tile 0x48", okS)
print("FAILS", fails)
sys.exit(1 if fails else 0)
