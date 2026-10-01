"""j4_stride_path.py - J-4: the descriptor 002ED610 reaches is the render root's +0x060 one, stride 0xC0
(FABLE, Claude Opus 5.5, 2026-09-26). Regression for the J-4 correction on resource-section-addressing.md.

  P1 0041E3A0 stores root + 0x60 at root + 0xD98 (0041E3DA lea rax,[rsi+0x60]; 0041E3E5 mov [rsi+0xd98],rax), and
     root + 0xF0 at + 0xDA0 as the control of the table's layout.
  P2 002ED610 takes its descriptor from [resolved + 0xD98] (002ED65D) and passes it to ResourceTable_ResolveEntryByIndex
     002ED570 (002ED666). It then reads the returned row's +0x84 (002ED670), which lies past a 0x50-byte row.
  P3 the +0x060 descriptor's wrapper 0046E250 hands 0051F9F0 the stride 0xC0 (0x50 and 0x260 are the other two
     wrappers', 00409F10 and 00477EE0): the immediate each wrapper loads into edx before the call.
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
def S(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)}
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
R = S(0x41E3A0, 0x100)
check("P1 root + 0x60 at + 0xD98; control: root + 0xF0 at + 0xDA0",
      R.get(0x41E3DA) == "lea rax, [rsi + 0x60]" and R.get(0x41E3E5) == "mov qword ptr [rsi + 0xd98], rax"
      and R.get(0x41E3EF) == "lea rax, [rsi + 0xf0]" and R.get(0x41E3F6) == "mov qword ptr [rsi + 0xda0], rax")
Q = S(0x2ED610, 0x90)
check("P2 [resolved + 0xD98] -> 002ED570; the row's +0x84 is read",
      Q.get(0x2ED65D) == "mov rcx, qword ptr [rax + 0xd98]" and Q.get(0x2ED666) == "call 0x2ed570"
      and Q.get(0x2ED670) == "mov ecx, dword ptr [rax + 0x84]")
def stride(wrapper):
    for x in cs.disasm(d[off(wrapper):off(wrapper) + 0x60], wrapper):
        if x.mnemonic == "mov" and x.op_str.startswith("edx, 0x"): return int(x.op_str.split(", ")[1], 16)
        if x.mnemonic == "call": break
    return None
got = {w: stride(w) for w in (0x409F10, 0x46E250, 0x477EE0)}
check("P3 the three wrappers pass strides 0x50 / 0xC0 / 0x260", got == {0x409F10: 0x50, 0x46E250: 0xC0, 0x477EE0: 0x260},
      str({hex(k): (hex(v) if v else v) for k, v in got.items()}))
print("FAILS", fails)
sys.exit(1 if fails else 0)
