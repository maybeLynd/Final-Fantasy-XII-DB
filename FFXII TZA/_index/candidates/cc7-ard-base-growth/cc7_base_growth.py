"""cc7_base_growth.py - CC-7: .ard slots 5 and 6 are one layout in two roles, a base row and a per-level growth row
(FABLE, Claude Opus 5.5, 2026-09-26). Static.

  G1 BattleUnit_ApplyUnitDefinition (0023A570) binds, for the unit definition rsi, unit +0xE70 = slot-5 row
     word[def+0x22] (registry 02EBF148) and unit +0xE78 = slot-6 row word[def+0x24] (registry 02EBF140).
  G2 every reader combines them the same way: value = slot6[f] * (byte[stats+0x1C2] - byte[stats+0x88]) + slot5[f],
     with stats = [unit+0x698] and +0x1C2 the level - Reward_ComputeExperienceForRecipient (002F8C71-002F8C85,
     field +0x34) and 00317090 (field +0x00), the same shape as the other pair readers.
  G3 the licence-point reader (field +0x2F) and the defeat-reward gil (field +0x30) use the same roles; a reading
     with slot 5 as the growth row fails every check.
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
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
a = dis(0x23A965, 0x23A9FB)
check("G1 the unit binds slot 5 (def +0x22) at +0xE70 and slot 6 (def +0x24) at +0xE78",
      a.get(0x23A998) == "movzx ecx, word ptr [rsi + 0x22]" and a.get(0x23A9A5) == "mov qword ptr [rdi + 0xe70], rcx"
      and a.get(0x23A9DF) == "movzx ecx, word ptr [rsi + 0x24]" and a.get(0x23A9F4) == "mov qword ptr [rdi + 0xe78], rcx")
b = dis(0x2F8C63, 0x2F8C88); c = dis(0x3170AA, 0x3170D3)
ok_b = (b.get(0x2F8C63) == "movzx esi, byte ptr [rax + 0x1c2]" and b.get(0x2F8C71) == "sub esi, eax"
        and b.get(0x2F8C73) == "mov rax, qword ptr [r14 + 0xe78]" and b.get(0x2F8C7A) == "imul esi, dword ptr [rax + 0x34]"
        and b.get(0x2F8C7E) == "mov rax, qword ptr [r14 + 0xe70]" and b.get(0x2F8C85) == "add esi, dword ptr [rax + 0x34]")
ok_c = (c.get(0x3170AA) == "movzx edx, byte ptr [rax + 0x1c2]" and c.get(0x3170B1) == "movzx eax, byte ptr [rax + 0x88]"
        and c.get(0x3170BA) == "mov rax, qword ptr [rcx + 0xe78]" and c.get(0x3170CB) == "imul edx, ecx"
        and c.get(0x3170C4) == "mov rax, qword ptr [r8 + 0xe70]" and c.get(0x3170D1) == "add edx, ecx")
check("G2 the readers compute slot6 x (level - byte +0x88) + slot5", ok_b and ok_c)
e = dis(0x2F912B, 0x2F9146); f = dis(0x312534, 0x31254C)
check("G3 the licence-point and defeat-gil readers use the same roles (multiply slot 6, add slot 5)",
      e.get(0x2F912B) == "mov rax, qword ptr [rdi + 0xe78]" and e.get(0x2F9132) == "movzx ecx, byte ptr [rax + 0x2f]"
      and e.get(0x2F913D) == "imul edx, ecx" and e.get(0x2F9136) == "mov rax, qword ptr [rdi + 0xe70]" and e.get(0x2F9144) == "add edx, ecx"
      and f.get(0x312534) == "mov rax, qword ptr [r14 + 0xe78]" and f.get(0x31253B) == "imul edi, dword ptr [rax + 0x30]"
      and f.get(0x31253F) == "mov rax, qword ptr [r14 + 0xe70]" and f.get(0x312546) == "add edi, dword ptr [rax + 0x30]")
print("FAILS", fails)
sys.exit(1 if fails else 0)
