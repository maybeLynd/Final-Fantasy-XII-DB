"""vif_owner_quals.py - the owner's static re-read of the five ASTRA VIF/GIF qualifications carried onto
the-vif1-vu1-layer.md (FABLE, Claude Opus 5.5, 2026-09-27). Static; ASTRA's packages hold the executed evidence.

  P1 program selection: best candidate 0 (0022CADD), empty list straight to the call (0022CAE5 -> 0022CB0E), unsigned
     skip of larger entries (0022CAF6 jb) and keep-largest (0022CAFA cmovae), 0x10000 compare after the scan
     (0022CB07), indirect call through 02068E30 with no pointer check (0022CB17/0022CB1E). The count reset is one dword
     store of 0 to 02088E44 and a ret.
  P2 callback flag: the caller stores a BYTE (001DB5B9 mov [rsp+0x20], sil), the wrapper reads a DWORD of the same
     argument slot (0022C944), the callback tests the full dword (001DB643 test r8d, r8d) and setne's a byte (001DB64C).
  P3 admission: the header load (0022C9D6) precedes the budget compare (0022CB55); the zero-WL V4-32 loop adds register
     addends and loops on ebx < num (0022C678..0022C686).
  P4 GIF size: the total is 32-bit (0020F3B8 add r10d, edx), the cursor 64-bit (0020F3C2 add r9, rax), gate byte at
     0020F316.
  P5 whole-stream strides: the inner reads are unchanged ([rax+r8*4] at 0022C2D0, word [rax+r8*8] at 0022C840) - the
     qualification narrows their consequence, not the instructions.
Each check also asserts that the wrong reading does NOT match (planted negatives: byte read at 0022C944, 64-bit total
at 0020F3B8, signed compare at 0022CAF6).
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

m = dis(0x22CAD0, 0x22CB24); r = dis(0x22C930, 0x22C93B)
check("P1 MSCAL keeps the largest eligible address, else slot 0; the count reset clears only the count",
      m.get(0x22CADD) == "xor eax, eax" and m.get(0x22CAE5) == "je 0x22cb0e" and m.get(0x22CAF6) == "jb 0x22cafd"
      and m.get(0x22CAFA) == "cmovae eax, ecx" and m.get(0x22CB07) == "cmp eax, 0x10000"
      and m.get(0x22CB0E) == "mov r9d, eax" and m.get(0x22CB1E) == "call qword ptr [rax + r9*8]"
      and 0x22CB17 in m and 0x02068E30 == 0x22CB1E + int(m[0x22CB17].split("0x")[-1].rstrip("]"), 16)
      and r.get(0x22C930) == "mov dword ptr [rip + 0x1e5c50a], 0" and 0x22C93A + 0x1E5C50A == 0x02088E44
      and r.get(0x22C93A) == "ret"
      and m.get(0x22CAF6) != "jl 0x22cafd")
a = dis(0x1DB5B9, 0x1DB5BE); w = dis(0x22C944, 0x22C94C); c = dis(0x1DB643, 0x1DB650)
check("P2 byte store, dword read, dword test",
      a.get(0x1DB5B9) == "mov byte ptr [rsp + 0x20], sil" and w.get(0x22C944) == "mov eax, dword ptr [rsp + 0x60]"
      and w.get(0x22C948) == "mov dword ptr [rsp + 0x28], eax" and c.get(0x1DB643) == "test r8d, r8d"
      and c.get(0x1DB64C) == "setne r8b" and not w.get(0x22C944, "").startswith("movzx eax, byte"))
h = dis(0x22C9D3, 0x22C9DB); b = dis(0x22CB55, 0x22CB58); u = dis(0x22C678, 0x22C688)
check("P3 header read before the budget compare; zero-WL loop adds register addends and loops",
      h.get(0x22C9D3) == "add edi, 4" and h.get(0x22C9D6) == "mov ebx, dword ptr [rax + rbp]"
      and b.get(0x22CB55) == "cmp edi, r12d" and 0x22C9D6 < 0x22CB55
      and u.get(0x22C678) == "add r10, rbp" and u.get(0x22C67B) == "add rax, r14" and u.get(0x22C67E) == "add ebx, r11d"
      and u.get(0x22C681) == "add edi, esi" and u.get(0x22C683) == "cmp ebx, r13d" and u.get(0x22C686) == "jl 0x22c630")
g = dis(0x20F316, 0x20F31D); s = dis(0x20F3B8, 0x20F3C5)
check("P4 GIF total 32-bit, cursor 64-bit, gate byte",
      g.get(0x20F316, "").startswith("cmp byte ptr [rip + ") and s.get(0x20F3B8) == "add r10d, edx"
      and s.get(0x20F3C0) == "mov eax, edx" and s.get(0x20F3C2) == "add r9, rax" and s.get(0x20F3B8) != "add r10, rdx")
v = dis(0x22C2D0, 0x22C2E2); x = dis(0x22C840, 0x22C845)
check("P5 the inner stride instructions are unchanged",
      v.get(0x22C2D0, "").endswith("[rax + r8*4]") and v.get(0x22C2DA, "").endswith("[rax + r8*4 + 4]")
      and v.get(0x22C2DF) == "inc r8" and x.get(0x22C840, "").endswith("word ptr [rax + r8*8]"),
      "%s | %s | %s" % (v.get(0x22C2D0), v.get(0x22C2DA), x.get(0x22C840)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
