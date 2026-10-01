"""RenderContext02CC0410: the magic-static render singleton (OPUS, 2026-09-27, OPUS-STRUCT-RENDER-CONTEXT-02CC0410).
Static, certified EXE.
  R1 005FD050 (and 00624670, a jmp to it) constructs 02CC0410 once with 00615840 and returns it
  R2 00615840 zeroes +0x108 / +0x110 / +0x118, builds PTexture2DD3D11 objects in place at +0x170 and +0x2F8 (memset 0x188,
     then 006160B0), sets +0x184C := 1, and constructs the +0x18C0 subobject (006C8750)
  R3 00625830 (receiver R) fills +0x120 as the DXGI_SWAP_CHAIN_DESC it passes to D3D11CreateDeviceAndSwapChain: zeroed as
     nine qwords, BufferCount := [+0x184C], format 0x1C, refresh 0x3C/1 then adjusted by 00623320 with +0x18A4 := num/den,
     usage 0x20, window at +0x30, windowed 1, flags 2; ppSwapChain = +0x118, ppDevice = +0x108, ppImmediateContext = +0x110
  S  REGRESSION: the type and its rows exist; size AT LEAST 0x18C0
Not claimed: the base region (005DC0E0), the extent past +0x18C0, anything the pages do not already cite.
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
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return (x.mnemonic, x.op_str)
def rip(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip \+ (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + int(m.group(1), 16)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
check("R1 005FD050 constructs 02CC0410 with 00615840 and returns it; 00624670 jumps to 005FD050",
      rip(0x5FD097) == 0x2CC0410 and at(0x5FD09E) == ("mov", "rcx, rbx") and at(0x5FD0A1) == ("call", "0x615840")
      and rip(0x5FD0C4) == 0x2CC0410 and at(0x624670) == ("jmp", "0x5fd050"))
C = {(x.mnemonic, x.op_str) for x in ins(0x615840, 887)}
check("R2 00615840: +0x108/+0x110/+0x118 zeroed, PTexture2DD3D11 in place at +0x170 and +0x2F8, +0x184C := 1, +0x18C0 built",
      {("mov", "qword ptr [rbp + 0x108], r14"), ("mov", "qword ptr [rbp + 0x110], r14"), ("mov", "qword ptr [rbp + 0x118], r14"),
       ("lea", "rdi, [rbp + 0x170]"), ("lea", "rsi, [rbp + 0x2f8]"), ("mov", "r8d, 0x188"), ("call", "0x6160b0"),
       ("mov", "dword ptr [rbp + 0x184c], 1"), ("lea", "rcx, [rbp + 0x18c0]"), ("call", "0x6c8750")} <= C
      and at(0x615893) == ("call", "0x861ec0") and at(0x6158A0) == ("call", "0x6160b0") and at(0x6158C5) == ("call", "0x6160b0"))
D = {x.address: (x.mnemonic, x.op_str) for x in ins(0x625830, 1672)}
check("R3 00625830: +0x120 is the swap-chain description; +0x108/+0x110/+0x118 are the device, context and swap chain",
      D[0x625901] == ("lea", "rsi, [r14 + 0x120]") and D[0x625938] == ("mov", "qword ptr [rsi + 0x40], rax")
      and D[0x62593C] == ("mov", "eax, dword ptr [r14 + 0x184c]") and D[0x625943] == ("mov", "dword ptr [rsi + 0x28], eax")
      and D[0x625955] == ("mov", "dword ptr [rsi + 0x10], 0x1c") and D[0x62595C] == ("mov", "dword ptr [rsi + 8], 0x3c")
      and D[0x625963] == ("mov", "dword ptr [rsi + 0xc], 1") and D[0x625992] == ("call", "0x623320")
      and D[0x62599C] == ("div", "dword ptr [rsi + 0xc]") and D[0x6259A6] == ("mov", "dword ptr [r14 + 0x18a4], eax")
      and D[0x6259E1] == ("mov", "qword ptr [rsi + 0x30], r12") and D[0x6259EF] == ("mov", "dword ptr [rsi + 0x24], 0x20")
      and D[0x625A04] == ("mov", "qword ptr [rsi + 0x38], 1") and D[0x625A0F] == ("mov", "dword ptr [rsi + 0x40], 2")
      and D[0x6259E8] == ("lea", "r12, [r14 + 0x108]") and D[0x6259F6] == ("lea", "rbx, [r14 + 0x118]") and D[0x625A26] == ("lea", "rax, [r14 + 0x110]")
      and D[0x625A2D] == ("mov", "qword ptr [rsp + 0x58], rax") and D[0x625A40] == ("mov", "qword ptr [rsp + 0x48], r12")
      and D[0x625A45] == ("mov", "qword ptr [rsp + 0x40], rbx") and D[0x625A4A] == ("mov", "qword ptr [rsp + 0x38], rsi")
      and D[0x625A64] == ("call", "0x80f2c8"))
check("R4 +0x168 is the created feature level (pFeatureLevel -> rsp+0x60 -> R+0x168)",
      D[0x625A32] == ("lea", "rax, [rsp + 0x60]") and D[0x625A37] == ("mov", "qword ptr [rsp + 0x50], rax")
      and D[0x625AF8] == ("mov", "eax, dword ptr [rsp + 0x60]") and D[0x625B0C] == ("mov", "dword ptr [r14 + 0x168], eax")
      and D[0x625DE3] == ("cmp", "dword ptr [r14 + 0x168], 0xb000"))
T = {l.split("\t")[0]: l.split("\t") for l in open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8")}
F = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")]
rows = {int(r[1], 16): r for r in F if r[0] == "RenderContext02CC0410"}
want = {0x108: "d3dDevice", 0x110: "d3dImmediateContext", 0x118: "dxgiSwapChain", 0x120: "swapChainDesc", 0x168: "featureLevel",
        0x170: "texture170", 0x2F8: "texture2F8", 0x184C: "swapChainBufferCount", 0x18A4: "refreshRate"}
check("S RenderContext02CC0410 declared (AT LEAST 0x18C0) with the proven rows, tiling to 0x18C0",
      "RenderContext02CC0410" in T
      # the extent was later raised by render_primitive.py (its evidence names it); the rows below +0x18C0 still tile it
      and (T["RenderContext02CC0410"][1].startswith("AT LEAST 0x18C0") or "render_primitive.py" in T["RenderContext02CC0410"][10])
      and all(o in rows and rows[o][3] == nm for o, nm in want.items()) and sum(int(r[2]) for o, r in rows.items() if o < 0x18C0) == 0x18C0)
print("FAILS", fails)
sys.exit(1 if fails else 0)
