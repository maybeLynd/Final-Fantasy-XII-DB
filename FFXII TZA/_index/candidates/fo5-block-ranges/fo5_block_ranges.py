"""fo5_block_ranges.py - FO-5: every byte of the battle-state block's +0x2D48..+0x4747 and +0x5006..+0x59C7 placed
(FABLE, Claude Opus 5.5, 2026-09-26; placed by a delegated read-only pass, re-checked here).

  R1 +0x2D48..+0x4747 is stats records 25 (from its +0xB8) to 39: the forty 0x1C8-byte records sit at 8 + i*0x1C8,
     and 0x2D48 = 8 + 25*0x1C8 + 0xB8, 0x4748 = 8 + 40*0x1C8.
  R2 the five scan rows inside it (+0x2E5D, +0x2EA8, +0x2EAA, +0x2EC1, +0x2ED1) are record 26's fields +5, +0x50, +0x52,
     +0x69, +0x79. 00320230 forms block + 0x2E58 = record 26 (00320274) and tail-jumps 003202F0 (00320285), whose reads
     are record-relative (00320319, 0032034B, 0032035E, 00320364, 0032036A).
  R3 +0x5004..+0x534B is inventory backup B: the snapshot copies word [+0x47C8 + 2i] to [+0x5004 + 2i] (0030FCC7,
     0030FCCF), and the restore reads it back (0030FB37). Both loops are bounded by a 0x1A4 count ([01EEBD28],
     [01EEBD54]).
  R4 the restore then clears 0x83C bytes from +0x4F84 (0030FBBA, 0030FBC1, 0030FBC7). 0x83C is region A's size, and
     both backups sit at their source + 0x83C (0x4748 + 0x83C = 0x4F84, 0x47C8 + 0x83C = 0x5004). So +0x534C..+0x57BF is
     the cleared, unused remainder of that mirror.
  R5 +0x57C0 and +0x57C8 are the class descriptors' region C for items (0x57C0 at 01EEBCE8) and region B for loot
     (0x57C8 at 01EEBD88), answered on the encoded-id page.
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
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return "%s %s" % (x.mnemonic, x.op_str)
def u32(v): return struct.unpack_from("<I", d, off(v))[0]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
check("R1 +0x2D48..+0x4747 is records 25 (from +0xB8) to 39", 0x2D48 == 8 + 25 * 0x1C8 + 0xB8 and 0x4748 == 8 + 40 * 0x1C8)
R = {0x320274: "add rcx, 0x2e58", 0x320285: "jmp 0x3202f0", 0x320319: "cmp byte ptr [rcx + 5], 1",
     0x32034B: "movzx ecx, word ptr [rbx + 0x50]", 0x32035E: "cmp word ptr [rbx + 0x52], ax",
     0x320364: "test byte ptr [rbx + 0x69], 2", 0x32036A: "test byte ptr [rbx + 0x79], 2"}
check("R2 the five scan rows are record 26's +5/+0x50/+0x52/+0x69/+0x79 (block + 0x2E58 = 8 + 26*0x1C8)",
      all(at(a) == s for a, s in R.items()) and 0x2E58 == 8 + 26 * 0x1C8
      and sorted(0x2E58 + f for f in (5, 0x50, 0x52, 0x69, 0x79)) == [0x2E5D, 0x2EA8, 0x2EAA, 0x2EC1, 0x2ED1],
      str({"%08X" % a: at(a) for a in R if at(a) != R[a]}))
check("R3 +0x5004 is inventory backup B of the 0x1A4 equipment words at +0x47C8",
      at(0x30FCC7) == "movzx eax, word ptr [rcx + rdx*2 + 0x47c8]" and at(0x30FCCF) == "mov word ptr [rcx + rdx*2 + 0x5004], ax"
      and at(0x30FB37) == "movsx edx, word ptr [rax + rcx*2 + 0x5004]" and u32(0x1EEBD28) == 0x1A4 and u32(0x1EEBD54) == 0x1A4
      and 0x5004 + 2 * 0x1A4 == 0x534C)
check("R4 the restore clears 0x83C bytes from +0x4F84: the mirror of region A, whose +0x534C..+0x57BF tail is unused",
      at(0x30FBBA) == "add rcx, 0x4f84" and at(0x30FBC1) == "mov r8d, 0x83c" and at(0x30FBC7).startswith("call ")
      and 0x4748 + 0x83C == 0x4F84 and 0x47C8 + 0x83C == 0x5004 and 0x4F84 + 0x83C == 0x57C0)
check("R5 region C for items at +0x57C0 and region B for loot at +0x57C8, from the class descriptors",
      u32(0x1EEBCE8) == 0x57C0 and u32(0x1EEBCC0) == 0x4748 and u32(0x1EEBD88) == 0x57C8 and 0x57C8 + 0x200 == 0x59C8)
print("FAILS", fails)
sys.exit(1 if fails else 0)
