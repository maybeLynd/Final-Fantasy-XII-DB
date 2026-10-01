"""stub_value.py - control for the manager-slot correction (FABLE, Claude Opus 5.5, 2026-09-26).

T1 005C5230 is exactly `xor eax, eax` / `ret` (bytes 33 C0 C3): it returns 0 and touches nothing else.
T2 side B (003DD230) on a negative fifth argument: 003DD25C test ecx,ecx / jns / call 005C5230 / mov ecx, eax.
T3 side A (003DA400) substitutes zero: xor ecx, ecx at 003DA45A and cmovns ecx, eax at 003DA46E.
Known positive: T2 must find the call to 005C5230; a decoder that finds nothing cannot pass T2.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(a, size): return {x.address: x for x in cs.disasm(d[off(a):off(a) + size], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
check("T1 005C5230 = 33 C0 C3 (xor eax,eax / ret)", d[off(0x5C5230):off(0x5C5230) + 3] == b"\x33\xC0\xC3", d[off(0x5C5230):off(0x5C5230) + 3].hex())
b = body(0x3DD230, 0x80)
seq = [b.get(a) for a in sorted(b) if 0x3DD25C <= a <= 0x3DD26C]
txt = " | ".join("%s %s" % (x.mnemonic, x.op_str) for x in seq)
check("T2 side B: test ecx,ecx / jns / call 005C5230 / mov ecx,eax", "test ecx, ecx" in txt and "jns" in txt and "call 0x5c5230" in txt
      and "mov ecx, eax" in txt, "(%s)" % txt)
a = body(0x3DA400, 0x90)
check("T3 side A: xor ecx,ecx at 003DA45A and cmovns ecx,eax at 003DA46E",
      a.get(0x3DA45A) is not None and a[0x3DA45A].op_str == "ecx, ecx" and a.get(0x3DA46E) is not None
      and a[0x3DA46E].mnemonic == "cmovns" and a[0x3DA46E].op_str == "ecx, eax")
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
