"""OrderedCommandList +0x29: a byte flag set and cleared around a class-filtered walk (OPUS, 2026-09-27). Control. Static.
  O1 RECEIVER: 0018B4E0 returns [01F7F5E0] - the route's lazily created singleton slot (it creates it on demand via
     0016D6A0) - and every access below goes through its return value
  O2 001F3570 sets byte [obj + 0x29] = 1 on entry (001F3582), runs the class-filtered walk 0018B1B0 (001F361B) and then
     clears it (001F3628); 001E2AF0 reads it (001E2D2C movzx) - a byte, not the word the old row named
  O3 STORE REGRESSION: +0x29 is a 1-byte row and no unobserved row covers it
Not claimed: what the flag guards beyond its placement around the walk.
"""
import os, re, struct, sys
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
def D(f, n): return list(cs.disasm(d[off(f):off(f) + n], f))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
G = D(0x18B4E0, 33)
tgt = [x.address + x.size + int(re.search(r"\+ (0x[0-9a-f]+)\]", x.op_str).group(1), 16) for x in G if "rip +" in x.op_str]
check("O1 0018B4E0 returns [01F7F5E0], the route's singleton slot",
      tgt == [0x1F7F5E0, 0x1F7F5E0] and any(x.mnemonic == "mov" and x.op_str.startswith("rax, qword ptr [rip") for x in G)
      and any(x.op_str == "0x16d6a0" for x in G))
S = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x1F3570, 0xD0)}
R = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x1E2AF0, 0x260)}
check("O2 set 1 before the walk, cleared after, read as a byte",
      S.get(0x1F357D) == "call 0x18b4e0" and S.get(0x1F3582) == "mov byte ptr [rax + 0x29], 1"
      and S.get(0x1F361B) == "call 0x18b1b0" and S.get(0x1F3620) == "call 0x18b4e0" and S.get(0x1F3628) == "mov byte ptr [rax + 0x29], 0"
      and R.get(0x1E2D27) == "call 0x18b4e0" and R.get(0x1E2D2C) == "movzx r8d, byte ptr [rax + 0x29]")
rows = []
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "OrderedCommandList": rows.append((int(c[1], 16), int(c[2]), c[3]))
check("O3 STORE REGRESSION: a 1-byte row at +0x29, not inside an unobserved row",
      any(r[0] == 0x29 and r[1] == 1 and not r[2].lower().startswith("unobserved") for r in rows)
      and not [r for r in rows if r[2].lower().startswith("unobserved") and r[0] <= 0x29 < r[0] + r[1]], str([r for r in rows if 0x28 <= r[0] <= 0x2C]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
