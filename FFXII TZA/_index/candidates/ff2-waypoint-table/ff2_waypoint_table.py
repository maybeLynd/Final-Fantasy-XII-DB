"""ff2_waypoint_table.py - FF-2: the battle unit's +0x298..+0x68F is the rest of the navigation path record's
waypoint table (FABLE, Claude Opus 5.5, 2026-09-26; the join first made by a delegated read-only pass, re-checked
here). The path record at unit + 0x200 and its +0x90 xz[128] field are published on the navigation-mesh page (§3).

  W1 the writers are index-form: the path builder 00382FF0 (rsi = its r8, the record) stores a qword at
     [rsi + idx*8 + 0x90] (00383096, 0038310D, 0038352A, 003835BD). A displacement sweep cannot see these stores.
  W2 the reader takes each entry as two floats: 00383670 loads [rdi + rcx*8 + 0x90] (003836F8), spills it (00383702),
     and stores the low dword as x and the high dword as z (00383707..00383718). So the entries are not pointers.
  W3 the region bound is 128: the builder's next[] reset loop runs `cmp eax, 0x80` (00383149). So the table is
     128 x 8 = 0x400 bytes at record +0x90, which is unit +0x290..+0x68F.
  W4 the extent agrees: the unit-reuse reset zeroes unit+0x80 for 0x610 bytes (00236B12, 00236B28), up to +0x690.
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
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
W = {0x383096: "mov qword ptr [rsi + r13*8 + 0x90], rax", 0x38310D: "mov qword ptr [rsi + r13*8 + 0x90], rax",
     0x38352A: "mov qword ptr [rsi + r15*8 + 0x90], rax", 0x3835BD: "mov qword ptr [rsi + r13*8 + 0x90], rax"}
check("W1 the path builder writes the table by index: [rsi + idx*8 + 0x90], rsi = its r8 (0038301C)",
      all(at(a) == s for a, s in W.items()) and at(0x38301C) == "mov rsi, r8", str({"%08X" % a: at(a) for a in W}))
check("W2 the waypoint reader takes each entry as {f32 x, f32 z}",
      at(0x3836F8) == "mov rdx, qword ptr [rdi + rcx*8 + 0x90]" and at(0x383702) == "mov qword ptr [rsp + 0x28], rdx"
      and at(0x383707) == "movss xmm0, dword ptr [rsp + 0x28]" and at(0x38370D) == "movss xmm1, dword ptr [rsp + 0x2c]"
      and at(0x383713) == "movss dword ptr [rbp], xmm0" and at(0x383718) == "movss dword ptr [rbp + 8], xmm1")
check("W3 the region bound is 128 (the next[] reset loop)",
      at(0x383142) == "mov byte ptr [rcx], 0xff" and at(0x383149) == "cmp eax, 0x80" and at(0x38314E) == "jb 0x383140")
check("W4 the unit-reuse reset zeroes unit+0x80 for 0x610 bytes, to +0x690",
      at(0x236B12) == "lea rcx, [rdi + 0x80]" and at(0x236B28) == "mov r8d, 0x610" and 0x80 + 0x610 == 0x200 + 0x90 + 128 * 8)
print("FAILS", fails)
sys.exit(1 if fails else 0)
