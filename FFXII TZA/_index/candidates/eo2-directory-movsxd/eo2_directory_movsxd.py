"""eo2_directory_movsxd.py - EO-2-a / EO-2-b: the second recorded crash site, 003845F0+0x10, reads a battle_pack
directory entry that was rebased in 32 bits and read back sign-extended (FABLE, Claude Opus 5.5, 2026-09-27). Static.

  D1 the pack's load callback 00238850 receives the buffer address as a 32-bit value and sign-extends it
     (movsxd rdx, ecx) before 003846F0 binds it.
  D2 003846F0 rebases every directory dword in place with a 32-bit add of the base's low half (00384780
     add dword ptr [rbx], ebp).
  D3 00236C30 reads each entry back with movsxd (00236C7B, 00236C99, ...) and passes it to
     AreaData_BindAndRebaseSectionDescriptor 003845F0, whose instruction at +0x10 is mov eax, [rdx + 0xc] - the
     recorded faulting instruction.
  D4 arithmetic: a section at 0x82AD88C0 (a buffer between 2 and 4 GiB) sign-extends to 0xFFFFFFFF82AD88C0, the recorded
     rdx; the same section below 2 GiB would not. Planted negative: 0x02AD88C0 stays positive.
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
a = dis(0x238850, 0x238874)
check("D1 the load callback sign-extends a 32-bit buffer address", a.get(0x238854) == "movsxd rdx, ecx" and a.get(0x238861) == "call 0x3846f0")
b = dis(0x3846F0, 0x3847A1)
check("D2 the directory is rebased in place in 32 bits", b.get(0x384780) == "add dword ptr [rbx], ebp" and b.get(0x3846FE) == "mov rbp, rdx")
c = dis(0x236C70, 0x236CA2); f = dis(0x3845F0, 0x384608)
check("D3 entries are read back with movsxd and handed to 003845F0, whose +0x10 is the faulting read",
      c.get(0x236C7B) == "movsxd rdx, dword ptr [rcx + 0xc]" and c.get(0x236C86) == "call 0x3845f0"
      and c.get(0x236C99) == "movsxd rdx, dword ptr [rax + 0x10]" and f.get(0x384600) == "mov eax, dword ptr [rdx + 0xc]")
sx = lambda v: v - (1 << 32) if v & 0x80000000 else v
check("D4 a section above 2 GiB sign-extends to the recorded pointer; below 2 GiB it does not",
      (sx(0x82AD88C0) & 0xFFFFFFFFFFFFFFFF) == 0xFFFFFFFF82AD88C0 and sx(0x02AD88C0) == 0x02AD88C0)
print("FAILS", fails)
sys.exit(1 if fails else 0)
