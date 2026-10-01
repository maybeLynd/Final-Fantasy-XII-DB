"""uq156_arms.py - control for the UQ-156 arm readings (FABLE, Claude Opus 5.5, 2026-09-26).

Re-derives from the shipping image the facts the map-screens page's 2026-09-26 narrowings rest on:
  A. 00254560 case 1 lands on the default arm, which is `mov al, 1` (the constant 1).
  B. location arm 10 calls 00254560 with ecx = 1 and skips 002BB785..002BB7DC on a non-zero result; no direct
     branch in the procedure targets that range and no case-table arm starts inside it (the path never runs).
  C. arm callee sets: location arm 10 has the marker step / confirm / closer / dispatcher; track arm 10 has the
     dispatcher and closer, but no marker step; both arm 14s run 003BED70, 002B7460 and 00271CB0.
  D. the link fields: location arm 10 writes container +0x179DC/+0x179DE/+0x179D0; location arm 14 reads +0x179DE/+0x179DC.
Planted negative: check C also asserts a callee known to be ABSENT (00402DB0 in the track arm), so a matcher that
returned "present" for everything would fail. Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
EXE = ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"
BASE = 0x120000
d = EXE.read_bytes()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
    raise ValueError(hex(v))
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return list(cs.disasm(d[off(a):off(b)], a))
def u32(v): return struct.unpack_from("<I", d, off(v))[0]
def arm(idx, case, mid): return BASE + u32(case + d[off(idx) + mid - 1] * 4)
def arm_starts(idx, case): return {BASE + u32(case + d[off(idx) + m - 1] * 4) for m in range(1, 0x2B)}
def calls(ins): return {int(x.op_str, 16) for x in ins if x.mnemonic == "call" and x.op_str.startswith("0x")}

fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

# A. 00254560 case 1
tbl = 0x2546E8
c1 = BASE + u32(tbl + 4)
first = dis(c1, c1 + 2)
check("A 00254560 case 1 -> default arm, mov al,1", c1 == 0x2545B5 and first and first[0].mnemonic == "mov"
      and first[0].op_str == "al, 1", "(%08X: %s %s)" % (c1, first[0].mnemonic, first[0].op_str))

# B. location arm 10 gate and the dead range
LOC, LIDX, LCASE = 0x2BAF80, 0x2BC28C, 0x2BC24C
TRK, TIDX, TCASE = 0x2B7B80, 0x2B8EB0, 0x2B8E70
la10 = dis(0x2BB751, 0x2BBCD0)
at = {x.address: x for x in la10}
check("B arm 10 location starts 002BB751", arm(LIDX, LCASE, 0xA) == 0x2BB751)
check("B r15d = 1 then call 00254560 with ecx = r15d",
      at[0x2BB76D].op_str == "r15d, 1" and at[0x2BB773].op_str == "ecx, r15d" and at[0x2BB776].op_str == "0x254560")
check("B jne past the range on al != 0", at[0x2BB783].mnemonic == "jne" and at[0x2BB783].op_str == "0x2bb7e1")
proc = dis(LOC, 0x2BC28C)
into = [x for x in proc if x.mnemonic.startswith("j") and x.op_str.startswith("0x")
        and 0x2BB785 <= int(x.op_str, 16) <= 0x2BB7DC]
check("B no direct branch into 002BB785..002BB7DC", not into, str([hex(x.address) for x in into]))
check("B no case-table arm starts in the range", not [s for s in arm_starts(LIDX, LCASE) if 0x2BB785 <= s <= 0x2BB7DC])

# C. callee sets
lc10 = calls(la10)
tc10 = calls(dis(0x2B82D7, 0x2B8394))
for f in (0x402DB0, 0x2BA310, 0x2B9B30, 0x2BC3E0):
    check("C location arm 10 calls %08X" % f, f in lc10)
check("C track arm 10 calls 002B6DB0 and 002B6260", {0x2B6DB0, 0x2B6260} <= tc10)
check("C track arm 10 does NOT call 00402DB0 (planted negative)", 0x402DB0 not in tc10)
lc14 = calls(dis(0x2BB186, 0x2BB751)); tc14 = calls(dis(0x2B7D7E, 0x2B82D7))
for f in (0x3BED70, 0x2B7460, 0x271CB0):
    check("C both arm 14s call %08X" % f, f in lc14 and f in tc14)

# D. link fields
w10 = {m for x in la10 if x.mnemonic in ("mov", "or") for m in re.findall(r"^\w+ ptr \[r\w+ \+ (0x179d[0-9a-f])\]", x.op_str)}
r14 = {m for x in dis(0x2BB186, 0x2BB751) for m in re.findall(r"ptr \[r\w+ \+ (0x179d[0-9a-f])\]", x.op_str)}
check("D location arm 10 writes +0x179DC/+0x179DE/+0x179D0", {"0x179dc", "0x179de", "0x179d0"} <= w10, str(sorted(w10)))
check("D location arm 14 reads +0x179DE/+0x179DC", {"0x179de", "0x179dc"} <= r14, str(sorted(r14)))
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
