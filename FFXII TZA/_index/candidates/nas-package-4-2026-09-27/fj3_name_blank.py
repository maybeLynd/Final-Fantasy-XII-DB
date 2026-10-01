"""fj3_name_blank.py - FJ-3's mechanism, read whole, for NAS package 4 (FABLE, Claude Opus 5.5, 2026-09-27). Static.

  B1 the builder 00329220 stores the record's name pointer +0x10 exactly three times: null at entry (00329261, r15),
     the text-bank name in the stats-row branch (003295EE, the return of 002B58B0), and the empty string at 003298AD.
  B2 the third store is unconditional within the unit block: the only branch that skips the distance test
     (00329879 je) lands on 003298A6, the same instruction the fall-through reaches; the pointer it stores is an empty
     string (01CEB638 holds a zero byte).
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
body = list(cs.disasm(d[off(0x329220):off(0x329220) + 0x790], 0x329220))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
st = [(x.address, x.op_str) for x in body if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rdi + 0x10],")]
t = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in body}
check("B1 three stores to +0x10: null, the text-bank name, the empty string",
      [a for a, _ in st] == [0x329261, 0x3295EE, 0x3298AD] and t.get(0x3295E9) == "call 0x2b58b0"
      and t.get(0x3298A6) == "lea rax, [rip + 0x19c1d8b]", str(["%08X" % a for a, _ in st]))
check("B2 the third store is reached on both arms of the unit block, and it points at an empty string",
      t.get(0x329879) == "je 0x3298a6" and t.get(0x3298A1) == "jne 0x3298a6" and t.get(0x3298A3) == "or dword ptr [rdi], 8"
      and 0x3298AD + 0x19C1D8B == 0x1CEB638 and d[off(0x1CEB638)] == 0)
print("FAILS", fails)
sys.exit(1 if fails else 0)
