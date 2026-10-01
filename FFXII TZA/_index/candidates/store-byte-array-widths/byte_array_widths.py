"""Type store: a byte-array ctype must agree with its row's size (OPUS, 2026-09-27). Control and regression.

  W1 STORE-WIDE: every row whose ctype is u8[N] / uint8[N] has size == N (rows carved from a larger span kept the old
     length in five places: PPhysicsCharacterCamera / PInputSource / PAnimationHierarchyNode +0x08, PPhysicsCapsuleBase
     +0x7C, PaneListWidget0B68 +0xB44)
  W2 PaneListWidget0B68 +0xB44 is the four-byte slotRequest array, not one byte followed by an unobserved span: 0029BB40
     reads [rsi + r15 + 0xB44] with the slot index in rsi (0029BBA2) under the walk bound `cmp edi, 4`, so +0xB45..+0xB47
     are elements a displacement census cannot see
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

bad = []; rows = {}
for l in open(DB / "_types" / "fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) < 5: continue
    rows[(c[0], c[1])] = c
    m = re.fullmatch(r"u(?:int)?8\[(\d+)\]", c[4])
    if m and c[2].isdigit() and int(m.group(1)) != int(c[2]): bad.append("%s %s size %s ctype %s" % (c[0], c[1], c[2], c[4]))
check("W1 every byte-array ctype matches its row size", not bad, "; ".join(bad[:6]))

d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
body = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x29BB40):off(0x29BB40) + 0x120], 0x29BB40)}
sr = rows.get(("PaneListWidget0B68", "0xB44"))
check("W2 slotRequest is four bytes: indexed read at 0029BBA2 under the bound cmp edi, 4; no separate span at +0xB45",
      "[rsi + r15 + 0xb44]" in body.get(0x29BBA2, "") and any(v == "cmp edi, 4" for v in body.values())
      and sr is not None and sr[2] == "4" and ("PaneListWidget0B68", "0xB45") not in rows,
      body.get(0x29BBA2, ""))
print("FAILS", fails)
sys.exit(1 if fails else 0)
