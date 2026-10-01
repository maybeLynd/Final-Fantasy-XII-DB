"""fj2_fields.py - FJ-2: the display record's +0x64 and +0x5E, as the builder 00329220 fills them (FABLE, Claude Opus 5.5,
2026-09-26).

  F1 +0x64 is the enemy's Clan Primer entry id. For a unit whose stats record has kind 1 (003298EA cmp byte [rax+5], 1)
     and whose class nibble is not 3 (003298F4 / 003298F9), the builder loads the unit's .ard class row [unit+0xE68]
     (003298FE) and stores its word +0x52 (00329905 -> 0032990D). The unit-definition page documents that word as the
     Clan Primer entry id: the installer copies it to unit +0x52, and 0031B9A0 returns it. Otherwise the store takes
     ebx.
  F2 +0x5E is the unit's issued command action id. When unit flag bit 14 is set (0032997A-00329981), the builder stores
     word [unit+0xBA0] (00329983 -> 0032998A), which the battle-unit field map names issuedCommandActionId. Otherwise
     it stores ebx.
  F3 the default in both cases is 0xFFFF: ebx is set at 00329850 and not written again before either store.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, struct, sys
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
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
L = list(cs.disasm(d[off(0x329220):off(0x329220) + 1933], 0x329220))
X = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in L}
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
check("F1 +0x64 = word [ [unit+0xE68] + 0x52 ] for a kind-1 record whose class nibble is not 3",
      X.get(0x3298EA) == "cmp byte ptr [rax + 5], 1" and X.get(0x3298F4) == "call 0x263c20" and X.get(0x3298F9) == "cmp eax, 3"
      and X.get(0x3298FE) == "mov rax, qword ptr [rsi + 0xe68]" and X.get(0x329905) == "movzx ecx, word ptr [rax + 0x52]"
      and X.get(0x32990B) == "mov ecx, ebx" and X.get(0x32990D) == "mov word ptr [rdi + 0x64], cx")
check("F2 +0x5E = word [unit+0xBA0] when unit flag bit 14 is set",
      X.get(0x32997A) == "mov eax, dword ptr [rsi]" and X.get(0x32997C) == "bt rax, 0xe"
      and X.get(0x329983) == "movzx ebx, word ptr [rsi + 0xba0]" and X.get(0x32998A) == "mov word ptr [rdi + 0x5e], bx")
wr = [x.address for x in L if 0x329850 < x.address < 0x329983 and x.mnemonic not in ("cmp", "test", "push") and
      x.op_str.split(",")[0].strip() in ("ebx", "rbx", "bx", "bl")]
check("F3 the default is 0xFFFF: ebx set at 00329850 and not written again before the stores",
      X.get(0x329850) == "mov ebx, 0xffff" and wr == [], "other ebx writes %s" % ["%08X" % a for a in wr])
print("FAILS", fails)
sys.exit(1 if fails else 0)
