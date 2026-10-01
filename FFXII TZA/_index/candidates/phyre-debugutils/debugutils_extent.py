"""PApplication +0x10D8..+0x112F is ONE embedded PFramework::PDebugUtils (OPUS, 2026-09-27). Control. Static + store.

  D1 PDebugUtils' class descriptor states its extent: 00791C20 calls 00632D80 with r8 -> 'PDebugUtils' (01CB09D0),
     r9d = 0x58 and alignment 8 at [rsp+0x20] (00791C58-00791C70), the argument list every Phyre extent in the store uses
  D2 getDebugUtils returns that object's address: the adapter 0079CEB0 is `lea rax, [rcx+0x10d8] / ret`, and its caller
     (00794E2F, just after the getDebugUtils registration at 00794DB5 / 00794DCD) is
     PMethodCallerConcrete<PApplication, PDebugUtils *>
  D3 0x10D8 + 0x58 = 0x1130, PApplication's own extent, and the store's rows from +0x10D8 tile exactly +0x10D8..+0x112F
Not claimed: what the debug-utilities object does, or which of its members the rows' names describe.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)}
def tgt(a):
    x = next(cs.disasm(d[off(a):off(a) + 15], a)); m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
def cstr(v): return d[off(v):off(v) + 64].split(b"\0")[0].decode("latin-1")
def rtti(vt):
    col = struct.unpack_from("<Q", d, off(vt - 8))[0]
    otd = off(BASE + struct.unpack_from("<I", d, off(col) + 12)[0])
    return d[otd + 16:otd + 300].split(b"\0")[0].decode("latin-1")
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

C = ins(0x791C20, 0x60)
check("D1 PDebugUtils' descriptor: 00632D80(name 'PDebugUtils', size 0x58, align 8)",
      C.get(0x791C58) == "mov dword ptr [rsp + 0x20], 8" and C.get(0x791C60) == "mov r9d, 0x58"
      and cstr(tgt(0x791C66)) == "PDebugUtils" and C.get(0x791C70) == "call 0x632d80")
A = [v for k, v in sorted(ins(0x79CEB0, 12).items())][:2]
check("D2 getDebugUtils is lea rax, [rcx+0x10d8] / ret, returning PDebugUtils *",
      A == ["lea rax, [rcx + 0x10d8]", "ret "] and cstr(tgt(0x794DB5)) == "getDebugUtils"
      and rtti(tgt(0x794E2F)) == ".?AV?$PMethodCallerConcrete@VPApplication@PFramework@Phyre@@PEAVPDebugUtils@23@@"
                                 "PCallerImplementation0@PCallerImplementation@PInternal@Phyre@@")
size = None; spans = []
for l in open(DB / "_types" / "types.tsv", encoding="utf-8"):
    c = l.split("\t")
    if c[0] == "PApplication": size = int(c[1], 16)
for l in open(DB / "_types" / "fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if c[0] == "PApplication" and int(c[1], 16) >= 0x10D8: spans.append((int(c[1], 16), int(c[2])))
spans.sort(); cur = 0x10D8; tiled = True
for o, s in spans:
    tiled &= (o == cur); cur = o + s
check("D3 0x10D8 + 0x58 = PApplication's 0x1130 extent, and the rows tile +0x10D8..+0x112F",
      size == 0x1130 and 0x10D8 + 0x58 == size and tiled and cur == size, str([(hex(o), s) for o, s in spans]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
