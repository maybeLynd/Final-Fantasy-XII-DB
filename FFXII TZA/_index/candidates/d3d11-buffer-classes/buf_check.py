"""PConstantBufferD3D11 (0x50) and PStructuredBufferD3D11 (0x68) past their bases (OPUS, 2026-09-27). Static. No reflected
members for either tail.
  K0 constructors: 00615550 == the PConstantBufferD3D11 descriptor's constructor 00611D60, and 00616060 == the
     PStructuredBufferD3D11 descriptor's constructor 006127C0 (identical store sequences; allocation sizes 0x50 / 0x68)
  K1 PConstantBufferD3D11 creator 0061F070: the description is dynamic (2), constant-buffer bind (4), CPU write
     (0x10000); +0x10 := an aligned copy buffer (the old one freed first); per element (stride 0x10, from +0x18/+0x20 by the
     PSharray rule) CreateBuffer into element +0x00, GetDesc into the class's +0x30, element +0x08 := 0
  K2 PConstantBufferD3D11 +0x48: 1 after 0061F070 returns (0061D960), 0 in the release 0062B7B0
  K3 PStructuredBufferD3D11: 0061F200 walks +0x18/+0x20 at stride 0x28, CreateBuffer into element +0x00 and GetDesc into
     the class's +0x48; 0061F710 (SRV, +0x38) into element +0x08; 006209C0 (UAV, +0x40) into element +0x10
  K4 PStructuredBufferD3D11 +0x60: written only 0 (constructor, release 0062BB40) and tested by 00625EF0; NO non-zero
     writer in reach - so it is NOT called a created flag (unlike the constant buffer and the three textures)
  S  REGRESSION: rows and element types exist and tile (FAILS before)
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
SZ = {}
for l in open(os.path.join(os.path.dirname(DB), "Tools", "work", "graph", "functions.tsv"), encoding="utf-8"):
    c = l.split("\t")
    try: SZ[int(c[0], 16)] = int(c[2])
    except: pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, k=None): return list(cs.disasm(d[off(a):off(a) + (k or SZ.get(a, 0x200))], a))
def ops(a, k=None): return {(x.mnemonic, x.op_str) for x in ins(a, k)}
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return (x.mnemonic, x.op_str)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
def storeset(a, k):
    return [(m.group(1), m.group(2) or "0") for x in ins(a, k) for m in [re.match(r"(qword|dword) ptr \[(?:rbx|rax|rcx)(?: \+ (0x[0-9a-f]+|\d+))?\], ", x.op_str)] if x.mnemonic == "mov" and m]
vts = {}
for l in open(os.path.join(DB, "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata", "members", "rtti-class-vtables.tsv"), encoding="utf-8"):
    r = l.rstrip("\n").split("\t")
    for nm in ("PConstantBufferD3D11", "PStructuredBufferD3D11"):
        if r[0].startswith(".?AV?$PClassDescriptorConcrete@V%s@" % nm) and len(r) > 2: vts[nm] = int(r[2], 16)
check("K0 the creation sites' constructors equal the class descriptors' own constructors",
      struct.unpack_from("<Q", d, off(vts["PConstantBufferD3D11"] + 80))[0] == 0x611D60
      and struct.unpack_from("<Q", d, off(vts["PStructuredBufferD3D11"] + 80))[0] == 0x6127C0
      and storeset(0x615550, 0x54) == storeset(0x611D60, 0x70) and storeset(0x616060, 0x4E) == storeset(0x6127C0, 0x70))
K = {x.address: (x.mnemonic, x.op_str) for x in ins(0x61F070)}
check("K1 constant-buffer creator 0061F070",
      K[0x61F0F1] == ("mov", "dword ptr [rsp + 0x34], 2") and K[0x61F0F9] == ("mov", "dword ptr [rsp + 0x38], 4")
      and K[0x61F101] == ("mov", "qword ptr [rsp + 0x3c], 0x10000") and K[0x61F11E] == ("call", "0x584730")
      and K[0x61F137] == ("call", "0x17d260") and K[0x61F13C] == ("mov", "qword ptr [rbx + 0x10], rax")
      and K[0x61F163] == ("btr", "eax, 0x1f") and K[0x61F174] == ("lea", "rax, [rbx + 0x20]") and K[0x61F17D] == ("lea", "rdi, [rsi + rax]")
      and K[0x61F18C] == ("mov", "r9, rdi") and K[0x61F192] == ("call", "qword ptr [rax + 0x18]")
      and K[0x61F19C] == ("lea", "rdx, [rbx + 0x30]") and K[0x61F1A3] == ("call", "qword ptr [rax + 0x50]")
      and K[0x61F0D6] == ("xor", "r13d, r13d") and K[0x61F1BC] == ("mov", "dword ptr [rdi + 8], r13d") and K[0x61F1C0] == ("add", "rsi, 0x10"))
check("K2 constant buffer +0x48 is the resources-created flag",
      at(0x61D994) == ("call", "0x61f070") and ("mov", "dword ptr [rbx + 0x48], 1") in {(x.mnemonic, x.op_str) for x in ins(0x61D994 + 5, 0x20)}
      and at(0x62B7CA) == ("xor", "ebp, ebp") and at(0x62B7D2) == ("mov", "dword ptr [rbx + 0x48], ebp") and at(0x625EC0) == ("cmp", "dword ptr [rcx + 0x48], 0"))
S2 = ops(0x61F200); V = ops(0x61F710); U = ops(0x6209C0)
check("K3 structured buffer: CreateBuffer into element +0x00 and GetDesc into +0x48; SRV into +0x08; UAV into +0x10 (stride 0x28)",
      at(0x61F4B4) == ("lea", "r9, [rcx + rdx]") and at(0x61F4C2) == ("call", "qword ptr [rax + 0x18]")
      and at(0x61F4F0) == ("lea", "rdx, [rbx + 0x48]") and at(0x61F4F4) == ("call", "qword ptr [rax + 0x50]")
      and ("lea", "rdx, [rbx + 0x20]") in S2 and ("mov", "eax, dword ptr [rbx + 0x18]") in S2
      and {("lea", "r8, [rbx + 0x20]"), ("lea", "r9, [r8 + 8]"), ("lea", "rcx, [rdi + rdi*4]"), ("call", "qword ptr [rax + 0x38]")} <= V
      and {("lea", "r8, [rbx + 0x20]"), ("lea", "r9, [r8 + 0x10]"), ("lea", "rcx, [rdi + rdi*4]"), ("call", "qword ptr [rax + 0x40]")} <= U)
w60 = []
for fa, s in SZ.items():
    if not (0x5D0000 <= fa < 0x680000) or s <= 0 or s > 20000 or off(fa) is None: continue
    for x in ins(fa, s):
        if x.mnemonic in ("mov", "or", "inc", "add") and re.match(r"dword ptr \[r\w+ \+ 0x60\], ", x.op_str) and not x.op_str.endswith((", 0", ", r14d")):
            if any(y.op_str in ("0x61f200", "0x62bb40", "0x625ef0", "0x616060") for y in ins(fa, s)): w60.append("%08X" % x.address)
check("K4 structured buffer +0x60: only zero writes and a test; no non-zero writer among the structured-buffer functions",
      at(0x616090) == ("mov", "dword ptr [rbx + 0x60], 0") and at(0x62BB64) == ("mov", "dword ptr [rbx + 0x60], r14d")
      and at(0x62BB5B) == ("xor", "r14d, r14d") and at(0x625EF0) == ("cmp", "dword ptr [rcx + 0x60], 0") and not w60, str(w60))
F = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")]
T = {l.split("\t")[0]: l.split("\t") for l in open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8")}
def rows(t): return {int(r[1], 16): r for r in F if r[0] == t}
cb, sb, ce, se = rows("PConstantBufferD3D11"), rows("PStructuredBufferD3D11"), rows("ConstantBufferD3D11Element"), rows("StructuredBufferD3D11Element")
check("S rows and element types exist and tile",
      [cb.get(o, [0, 0, 0, ""])[3] for o in (0x10, 0x18, 0x30, 0x48)] == ["cpuData", "elements", "bufferDesc", "resourcesCreated"]
      and [sb.get(o, [0, 0, 0, ""])[3] for o in (0x18, 0x48, 0x60)] == ["elements", "bufferDesc", "releaseGate60"]
      and sum(int(r[2]) for r in cb.values()) == 0x50 and sum(int(r[2]) for r in sb.values()) == 0x68
      and T.get("ConstantBufferD3D11Element", ["", ""])[1] == "0x10" and T.get("StructuredBufferD3D11Element", ["", ""])[1] == "0x28"
      and sum(int(r[2]) for r in ce.values()) == 0x10 and sum(int(r[2]) for r in se.values()) == 0x28)
print("FAILS", fails)
sys.exit(1 if fails else 0)
