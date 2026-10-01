"""er1_table.py - ER-1 propagation check (FABLE, Claude Opus 5.5, 2026-09-27): the 0215FDA0 records are the
NameBindingEntry free list UQ-58 / EW-3 describe. Static.

  R1 the allocator 002E25E0 pops the head [0215FD60], increments the stamp +0x24, and takes the new head from +0x08.
  R2 the resolver 002E97C0 indexes 0215FDA0 by (id & 0x7FFF) << 6 and reads only +0x24 and +0x1A of the record there
     (the handle check) - not +0x04 / +0x06 / +0x08.
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
a = dis(0x2E25E0, 0x2E261F)
check("R1 pop at 0215FD60, stamp +0x24, next at +0x08",
      a.get(0x2E25E0) == "mov rdx, qword ptr [rip + 0x1e7d779]" and 0x2E25E7 + 0x1E7D779 == 0x0215FD60
      and a.get(0x2E25EC) == "inc dword ptr [rdx + 0x24]" and a.get(0x2E25F6) == "mov rax, qword ptr [rdx + 8]"
      and a.get(0x2E2618) == "mov qword ptr [rip + 0x1e7d741], rax")
r = dis(0x2E97C0, 0x2E9800)
recreads = sorted(t for t in r.values() if "[rax + " in t)
check("R2 the resolver reads only +0x24 and +0x1A of the record",
      r.get(0x2E97D8) == "shl rax, 6" and r.get(0x2E97DC, "").startswith("lea rcx, [rip + ")
      and r.get(0x2E97E8) == "mov edx, dword ptr [rax + 0x24]" and r.get(0x2E97EB) == "movzx ecx, word ptr [rax + 0x1a]"
      and not any(("[rax + 4]" in t or "[rax + 6]" in t or "[rax + 8]" in t) for t in r.values()), str(recreads))
print("FAILS", fails)
sys.exit(1 if fails else 0)
