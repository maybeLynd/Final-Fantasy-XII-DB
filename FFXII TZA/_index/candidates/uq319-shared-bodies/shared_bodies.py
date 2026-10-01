"""shared_bodies.py - UQ-319: the five shared implementations with no read body (FABLE, Claude Opus 5.5, 2026-09-26).

  S1 00633240 installs vtable 00D580B0, whose RTTI names Phyre::PClassDataMember. The body calls the owner's slot 0x48
     when the list at +8 is non-empty, destroys the member at +0x38 (006B6700), and frees +0x20 through
     00584730 when bit 0 of +0x28 is set: PClassDataMember's destructor.
  S2 006B6750 installs 00D80930 (Phyre::PAnnotation, a PSimpleDoubleListElement<PAnnotation>) and unlinks +8 from its
     list, then self-links it: PAnnotation's destructor.
  S3 006B68A0 installs 00D80970 (Phyre::PNamedSemanticDescriptor), unlinks the list element at +0x50, then installs
     00D31168 (Phyre::PType, its base): PNamedSemanticDescriptor's destructor with the base's inlined.
  S4 003844F0 is `jmp 003697F0`, the null-safe release (NULL -> ret, else 00369860(p, 0)), the validating
     deallocator already documented on the ownerless-functions page.
  S5 007DF6D0 calls the import InitializeCriticalSection on `this` (a 0x28-byte CRITICAL_SECTION on x64) and zeroes
     +0x28..+0x4B, returning `this`: the constructor of a lock plus 0x24 bytes of zeroed state.
  Planted negative: the RTTI reader must give different names for the four vtables.
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
def q(v): return struct.unpack_from("<Q", d, off(v))[0]
def u32(v): return struct.unpack_from("<I", d, off(v))[0]
def tdname(td): return d[off(td) + 16:off(td) + 120].split(b"\0")[0].decode("latin1")
def rtti(vt): return tdname(BASE + u32(q(vt - 8) + 12))
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def S(a, size): return ["%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

N = {vt: rtti(vt) for vt in (0xD580B0, 0xD80930, 0xD80970, 0xD31168)}
check("RTTI names", N == {0xD580B0: ".?AVPClassDataMember@Phyre@@", 0xD80930: ".?AVPAnnotation@Phyre@@",
                          0xD80970: ".?AVPNamedSemanticDescriptor@Phyre@@", 0xD31168: ".?AVPType@Phyre@@"}, str(N))
check("planted negative: four distinct names", len(set(N.values())) == 4)
A = S(0x633240, 0x5D)
check("S1 PClassDataMember destructor",
      "lea rax, [rip + 0x724e52]" in A and "call qword ptr [rax + 0x48]" in A and "call 0x6b6700" in A
      and "test byte ptr [rdi + 0x20], 1" in A and "mov rcx, qword ptr [rdi + 0x18]" in A and "call 0x584730" in A)
B = S(0x6B6750, 0x24)
check("S2 PAnnotation destructor: vtable, unlink +8, self-link",
      B[1] == "lea rax, [rip + 0x6ca1d5]" and B[2] == "mov qword ptr [rcx], rax"
      and B[-3:] == ["mov qword ptr [rdx], rdx", "mov qword ptr [rdx + 8], rdx", "ret "])
C = S(0x6B68A0, 0x2E)
check("S3 PNamedSemanticDescriptor destructor: own vtable, unlink +0x50, base PType vtable",
      C[0] == "lea r8, [rcx + 0x50]" and C[1] == "lea rax, [rip + 0x6ca0c5]" and C[7] == "lea rax, [rip + 0x67a8a5]"
      and C[10] == "mov qword ptr [rcx], rax")
check("S4 003844F0 -> null-safe release -> 00369860(p, 0)",
      S(0x3844F0, 5) == ["jmp 0x3697f0"]
      and S(0x3697F0, 0xD) == ["test rcx, rcx", "je 0x3697fc", "xor edx, edx", "jmp 0x369860", "ret "])
E = S(0x7DF6D0, 0x2D)
imp = d[off(BASE + u32(0x8C20B0) + 2):off(BASE + u32(0x8C20B0) + 2) + 40].split(b"\0")[0]
check("S5 InitializeCriticalSection(this), then +0x28..+0x4B zeroed",
      imp == b"InitializeCriticalSection" and E[3] == "call qword ptr [rip + 0xe29d1]"
      and E[5:10] == ["mov qword ptr [rbx + 0x28], rax", "mov qword ptr [rbx + 0x30], rax", "mov qword ptr [rbx + 0x38], rax",
                      "mov qword ptr [rbx + 0x40], rax", "mov dword ptr [rbx + 0x48], eax"], imp.decode())
print("FAILS", fails)
sys.exit(1 if fails else 0)
