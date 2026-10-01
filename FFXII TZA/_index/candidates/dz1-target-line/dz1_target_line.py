"""dz1_target_line.py - DZ-1 closed by propagation: the +0xD70 list holds target-line objects (FABLE, Claude Opus 5.5,
2026-09-27; the answer is UQ-25's on one-word-decides-which-fifteen-subsystems-tick.md, FABLE 2026-09-17). Static.

  D1 the only builder 002917E0 takes 0xD80 bytes from the HUD object's allocator [0209BE80]+0x10FC0 through 00273A30
     (00291981..00291997) and zeroes them twice (00275550).
  D2 the block's +0xD00 is the image looked up by the name at 01E0C1E0, which is the string "targetline_p"
     (002919E7..00291A01).
  D3 the block is linked at the list head [0209BE80]+0x10F00 or after the last +0xD70 (00291B17..00291B56), the link
     the per-node walk 0028C4C0 follows.
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
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
a = dis(0x291981, 0x2919C2)
check("D1 0xD80 bytes from the HUD allocator, zeroed",
      a.get(0x291988) == "mov r8d, 0xd80" and a.get(0x291990) == "mov rdx, qword ptr [rdx + 0x10fc0]"
      and a.get(0x291997) == "call 0x273a30" and a.get(0x2919B0) == "call 0x275550" and a.get(0x2919A8) == "mov edx, 0xd80")
b = dis(0x2919E7, 0x291A08)
q = struct.unpack_from("<Q", d, off(0x01E0C1E0))[0]; s = d[off(q):d.find(b"\0", off(q))]
check("D2 +0xD00 is the image named targetline_p",
      b.get(0x2919E7, "").startswith("mov rcx, qword ptr [rip + ") and b.get(0x2919EE) == "call 0x24a5a0"
      and b.get(0x291A01) == "mov qword ptr [rbx + 0xd00], rcx" and s == b"targetline_p", s.decode())
c = dis(0x291B17, 0x291B5D)
w = dis(0x28C4C0, 0x28C4E9)
check("D3 linked through +0xD70 from the head +0x10F00, the link the walk follows",
      c.get(0x291B17) == "mov rcx, qword ptr [rdi + 0x10f00]" and c.get(0x291B4F) == "mov qword ptr [rcx + 0xd70], rbx"
      and w.get(0x28C4D8) == "mov rbx, qword ptr [rbx + 0xd70]")
print("FAILS", fails)
sys.exit(1 if fails else 0)
