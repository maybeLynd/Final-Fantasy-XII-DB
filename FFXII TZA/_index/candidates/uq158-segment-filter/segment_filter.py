"""segment_filter.py - control for the UQ-158 correction (FABLE, Claude Opus 5.5, 2026-09-26).

S1 00402A40 calls 004023D0 at 00402B25 and, on eax == 1, jumps to 00402BAC (next record), skipping the node build
   (memset 0xB0 at 00402B3A, 004027D0 at 00402B62, the +0x98/+0xA0 link at 00402B8F/00402B96).
S2 004023D0 returns 1 only from 00402484, reached when both ids and both endpoints match in either order (je 0x402484 at
   00402444 and 0040246F), and 0 at 00402481 after the list is exhausted.
Known positive: the skip target 00402BAC must lie AFTER the link stores, so a reversed reading (build on 1) cannot pass.
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
f = body(0x402A40, 0x1AC); g = body(0x4023D0, 0xBA)
fails = 0
def check(name, ok):
    global fails
    print("%s  %s" % ("PASS" if ok else "FAIL", name)); fails += (not ok)
check("S1 call 004023D0, cmp eax,1, je 00402BAC",
      f[0x402B25].op_str == "0x4023d0" and f[0x402B2A].op_str == "eax, 1" and f[0x402B2D].mnemonic == "je" and f[0x402B2D].op_str == "0x402bac")
check("S1 the build path: memset 0xB0, 004027D0, link +0x98/+0xA0",
      f[0x402B31].op_str == "r8d, 0xb0" and f[0x402B3A].op_str == "0x861ec0" and f[0x402B62].op_str == "0x4027d0"
      and f[0x402B8F].op_str == "qword ptr [rcx + 0x98], rbx" and f[0x402B96].op_str == "qword ptr [rbx + 0xa0], rcx")
check("known positive: the skip target lies after the link stores", 0x402BAC > 0x402B96)
check("S2 return 1 only at 00402484, reached from the two full-match je",
      g[0x402484].op_str == "eax, 1" and g[0x402444].op_str == "0x402484" and g[0x40246F].op_str == "0x402484"
      and g[0x402481].op_str == "eax, eax")
check("S2 id pair and endpoint pair compared at +0x80/+0x82 and +0x84/+0x86/+0x8C/+0x8E",
      "rcx + 0x80" in g[0x4023E0].op_str and "rcx + 0x82" in g[0x4023F2].op_str and "rcx + 0x84" in g[0x40240C].op_str
      and "rcx + 0x8c" in g[0x402430].op_str and "rcx + 0x8e" in g[0x40243D].op_str)
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
