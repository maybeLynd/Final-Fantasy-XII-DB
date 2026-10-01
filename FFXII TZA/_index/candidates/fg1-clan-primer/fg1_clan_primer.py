"""fg1_clan_primer.py - FG-1 narrowed: the Clan Primer tabs, the hunt-list tab and the rank table's minimum counts
(FABLE, Claude Opus 5.5, 2026-09-26; read by a delegated read-only pass, re-checked here).

  P1 the handbook tables in .rdata: 00D23740 u16[6] = 0x228 0x294 0x2CC 0x2F4 0x31C 0x354 (the six menuhandbook family
     resources the handbook-index page names story, world, person, knowledge, tutorial, monster), 00D23750 u8[8]
     = 0 1 2 3 4 6 5 7 (tab -> category), 00D23758 u16[8] = 160 96 64 120 56 512 48 30 (per-tab capacities).
  P2 tab 6 is the hunt list. Its family-B writer 005789D0 passes tab 6 (00578AF0) to 005779E0, which maps the tab
     through 00D23750 (005779E3) and tail-jumps 00315B50 (005779EE). There category 5 bounds the index < 0x30
     (00315BDA). The index is the row's ordinal within its row kind in the table at [02AED490]+0xC8 (0037E5BA,
     0037E658), which is the hunt list's menuquest table on the five-small-tables page.
  P3 the rank table (00D105D0.., rows {u32, u8 +4, u8 +5, u16 +6}): byte +5 is compared with the popcount of the
     30-bit set at +0x3844, and only rank 12 requires it (30, all of them). Byte +4 is the other minimum: 2 at rank 2,
     rising to 44 at rank 12.
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
def ins(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
def at(a): x = ins(a, 16)[0]; return ("%s %s" % (x.mnemonic, x.op_str)).strip()
def rip(a):
    x = ins(a, 16)[0]; s = x.op_str
    return x.address + x.size + int(s.split("rip + ")[1].split("]")[0], 16) if "rip + " in s else None
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
check("P1 the handbook family bases, tab -> category map and per-tab capacities",
      struct.unpack_from("<6H", d, off(0xD23740)) == (0x228, 0x294, 0x2CC, 0x2F4, 0x31C, 0x354)
      and list(d[off(0xD23750):off(0xD23750) + 8]) == [0, 1, 2, 3, 4, 6, 5, 7]
      and struct.unpack_from("<8H", d, off(0xD23758)) == (160, 96, 64, 120, 56, 512, 48, 30))
check("P2 tab 6's writer maps through 00D23750 into 00315B50's category 5 (index < 0x30), indexed by the hunt table at [02AED490]",
      at(0x578AF0) == "mov ecx, 6" and at(0x578AF9) == "call 0x5779e0" and rip(0x5779E3) == 0xD23750
      and at(0x5779EE) == "jmp 0x315b50" and at(0x315BDA) == "cmp esi, 0x30"
      and rip(0x37E5BA) == 0x2AED490 and rip(0x37E658) == 0x2AED490)
rows = [struct.unpack_from("<IBBH", d, off(0xD105D0 + 8 * r)) for r in range(12)]
B = [x for x in ins(0x316670, 0x80)]
reads3844 = any("+ 0x3844]" in x.op_str for x in B)
check("P3 the rank table: +5 is 0 for ranks 1-11 and 30 for rank 12 (the 30-bit +0x3844 popcount); +4 runs 0..44",
      [r[2] for r in rows] == [0] * 11 + [30] and [r[1] for r in rows] == [0, 2, 4, 8, 10, 12, 14, 16, 24, 28, 32, 44]
      and [r[3] for r in rows] == list(range(1244, 1256)) and rip(0x3153B5) == 0xD1062D and reads3844
      and at(0x316681) == "call 0x316930", str(rows[-1]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
