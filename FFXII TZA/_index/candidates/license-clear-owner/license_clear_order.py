"""license_clear_order.py - the owner's static re-read behind the 2026-09-27 qualification of the licence-check page
(FABLE, Claude Opus 5.5; on ASTRA-RETURN-FABLE-LICENSE-CLEAR-BOUNDARY).

  L1 the builder 002F8FA0 computes the clear length in 32 bits (002F8FD3 lea r8d, [rax+7]; 002F8FD9 shr r8, 3) and calls
     memset (002F8FE0) BEFORE its signed loop gate (002F8FFC test r14d, r14d / 002F8FFF jle).
  L2 the caller 00323BB0 zeroes 46 bytes at rsp+0x20..0x4D (five qword, one dword, one word stores of the zeroed rcx)
     before the builder call at 00323BFC.
  L3 arithmetic: the 32-bit length for counts 0, 8, 0xFFFFFFF9, 0xFFFFFFF8 is 0, 1, 0, 0x1FFFFFFF (ASTRA's table);
     planted negative: a 64-bit computation would give 0x20000000 for 0xFFFFFFF9 (the 32-bit one wraps to 0), which the check must reject.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
b = dis(0x2F8FD3, 0x2F9005)
check("L1 the clear is sized in 32 bits and requested before the signed gate",
      b.get(0x2F8FD3) == "lea r8d, [rax + 7]" and b.get(0x2F8FD9) == "shr r8, 3" and b.get(0x2F8FE0) == "call 0x861ec0"
      and b.get(0x2F8FFC) == "test r14d, r14d" and b.get(0x2F8FFF) == "jle 0x2f90a3")
c = dis(0x323BCB, 0x323C01)
stores = [(a, t) for a, t in sorted(c.items()) if t.startswith("mov") and "[rsp + 0x" in t and t.endswith(("rcx", "ecx", "cx"))]
span = sum({"qword": 8, "dword": 4, "word": 2}[t.split()[1]] for a, t in stores)
check("L2 the caller zeroes 46 bytes before the builder call",
      c.get(0x323BCB) == "xor ecx, ecx" and span == 46 and all(a < 0x323BFC for a, t in stores)
      and c.get(0x323BFC) == "call 0x2f8fa0", "%d stores, %d bytes" % (len(stores), span))
L32 = lambda cnt: ((cnt + 7) & 0xFFFFFFFF) >> 3
L64 = lambda cnt: (cnt + 7) >> 3
check("L3 the 32-bit lengths match ASTRA's table; the 64-bit reading does not",
      [L32(x) for x in (0, 8, 0xFFFFFFF9, 0xFFFFFFF8)] == [0, 1, 0, 0x1FFFFFFF] and L64(0xFFFFFFF9) == 0x20000000 and L32(0xFFFFFFF9) == 0)
print("FAILS", fails)
sys.exit(1 if fails else 0)
