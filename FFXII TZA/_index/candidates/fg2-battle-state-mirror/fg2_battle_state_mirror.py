"""fg2_battle_state_mirror.py - FG-2: the save payload's +0x2081..+0x7B11 lies inside the 0x6000-byte copy of the
battle-state block at payload +0x2000 (FABLE, Claude Opus 5.5, 2026-09-26; placed by a delegated read-only pass,
re-checked here).

The payload starts at buffer + 0x200, and the battle-state block sits at buffer + 0x4E68C (payload +0x4E48C; the
save payload page §2.2).
  M1 the capture: 00229B40 copies 0xC0 x 0x80 = 0x6000 bytes from buffer + 0x4E68C (the block) to buffer + 0x2200
     (payload +0x2000). See 00229B7B (count), 00229B81 (source), 00229B88 (destination) and the back edge 00229BE2.
  M2 the restore: 002EF4A0 copies 0xC0 x 0x80 back from the static buffer's payload +0x2000 (02166480) to its block
     (021B290C).
  M3 so payload +X in +0x2000..+0x7FFF is block +(X - 0x2000), and FG-2's +0x2081..+0x7B11 is block +0x81..+0x5B11.
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
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return ("%s %s" % (x.mnemonic, x.op_str)).strip()
def rip(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); s = x.op_str
    return x.address + x.size + int(s.split("rip + ")[1].split("]")[0], 16) if "rip + " in s else None
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
check("M1 the capture copies 0xC0 x 0x80 from buffer+0x4E68C (the block) to buffer+0x2200 (payload +0x2000)",
      at(0x229B7B) == "mov r8d, 0xc0" and at(0x229B81) == "lea rdx, [rax + 0x4e68c]" and at(0x229B88) == "add rax, 0x2200"
      and at(0x229BE2) == "jne 0x229b91" and 0xC0 * 0x80 == 0x6000)
STATIC = 0x2164280
check("M2 the restore copies the same 0x6000 bytes back in the static buffer",
      rip(0x2EF4A0) == STATIC + 0x4E68C and rip(0x2EF4AC) == STATIC + 0x2200 and at(0x2EF4A7) == "mov edx, 0xc0" and at(0x2EF504) == "jne 0x2ef4b3")
check("M3 FG-2's +0x2081..+0x7B11 is block +0x81..+0x5B11, inside the copy",
      0x2000 <= 0x2081 and 0x7B11 < 0x2000 + 0x6000 and (0x2081 - 0x2000, 0x7B11 - 0x2000) == (0x81, 0x5B11))
print("FAILS", fails)
sys.exit(1 if fails else 0)
