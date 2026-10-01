"""ASTRA-RETURN-OPUS-VIF-CALLBACK-FLAG-WIDTH: the initialization precondition of 001DB550's fifth-argument slot (OPUS).

  I1 001DB550 zeroes esi once (001DB56C) and never writes esi/rsi again before or inside its loop.
  I2 the only write to its outgoing slot [rsp+0x20] is the byte store `mov byte ptr [rsp + 0x20], sil` (001DB5B9);
     no dword/qword store to [rsp+0x20..0x23] exists in the body.
  I3 the wrapper 0022C940 reads the slot as a dword (0022C944 `mov eax, dword ptr [rsp + 0x60]`).
  I4 001DB550 has no direct caller (pointer-entered), 0022C940's only caller is 001DB550.
So the value the callback tests is (the three bytes the frame inherited at [rsp+0x21..0x23]) with a zero low byte:
false exactly when those stale bytes are zero. What they hold in normal play is not claimed.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]


def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs:
            return v - BASE - va + ro


cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
body = list(cs.disasm(d[off(0x001DB550):off(0x001DB550) + 172], 0x001DB550))
fails = 0


def check(nm, ok):
    global fails
    print("%s  %s" % ("PASS" if ok else "FAIL", nm)); fails += (not ok)


esi_writes = [i for i in body if i.operands and i.operands[0].type == X86_OP_REG
              and i.reg_name(i.operands[0].reg) in ("esi", "rsi", "si", "sil") and i.mnemonic not in ("cmp", "test") and i.address < 0x001DB5EC]
check("I1 esi written once before the loop ends (xor at 001DB56C; the epilogue restore 001DB5F1 is after it)", [i.address for i in esi_writes] == [0x001DB56C])
slot = [i for i in body if i.operands and i.operands[0].type == X86_OP_MEM and i.reg_name(i.operands[0].value.mem.base) == "rsp"
        and 0x20 <= i.operands[0].value.mem.disp <= 0x23]
check("I2 the slot's only write is the byte store at 001DB5B9",
      len(slot) == 1 and slot[0].address == 0x001DB5B9 and slot[0].op_str == "byte ptr [rsp + 0x20], sil")
w = list(cs.disasm(d[off(0x0022C940):off(0x0022C940) + 43], 0x0022C940))
check("I3 0022C940 reads the slot as a dword", w[1].address == 0x0022C944 and w[1].op_str == "eax, dword ptr [rsp + 0x60]")
print("FAILS", fails)
sys.exit(1 if fails else 0)
