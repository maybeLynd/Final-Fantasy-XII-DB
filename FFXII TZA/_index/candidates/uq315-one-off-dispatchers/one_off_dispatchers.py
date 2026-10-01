"""one_off_dispatchers.py - UQ-315: the nine one-off Runtime.Callback dispatchers, each read (FABLE, Claude Opus 5.5, 2026-09-26).

  N0 the nine: every functions.tsv row tagged under Runtime.Callback / Runtime.CallbackQueue / Runtime.CallbackAdapter /
     Presentation.Runtime.Callback, less the 351 return-value adapters, the 46 owned-buffer resets and the 3 Lua adapters.
  N1 0020DA50 / 0020D9F0: first-success walk of a node chain (next at +8) calling vtable slot 0 / slot 1 respectively;
     returns 1 at the first true, 0 at the end. Only caller family: the console's entry formatter.
  N2 002481C0: from the root at 0208EBC0 down the +0x10 chain while flags +0x40 have bits 0 and 3; tail-calls the root's
     proc [+0] with message record 009150F0 (= 11) if the node has bit 9, else 009150D8 (= 10).
  N3 002465F0: memsets the record, stores the proc (NULL -> the folded stub 005C5230) at +0, stamps the generation bit 17
     from 0208ED5C, and calls the proc with a stack message whose first dword is 1.
  N4 00248030: when a node's bit 17 differs from the generation at 0208ED5C (and bit 10 is clear) it sets bit 2 and,
     unless bit 18, calls the proc with message record 00915108 (= 2); then restamps bit 17.
  N5 00186230: advances the slot index +0xCB8 mod 4, calls each 16-byte {fn, arg} entry of that slot's vector
     (+0xC38 + 32k .. +0xC40 + 32k), then empties it (end = begin).
  N6 006CC860: for buffer [+0xA0], calls the member callback [+0x58] on each pointer of the vector at
     +0x60 + 32i, empties it, then flips +0xA0 (sete). Reached only through 0067AB40 (this + 0xA8).
  N7 0063DC30: tail-calls [+0x48] with the arguments shifted down one, or returns 0x15 when it is NULL.
  N8 0017ECB0: stores dword [arg + 0x10] into 01DF08F8.
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
def u32(v): return struct.unpack_from("<I", d, off(v))[0]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def S(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)}
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

rows = list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))
cb = [r for r in rows[1:] if len(r) > 8 and any(k in r[8] for k in ("Runtime.Callback", "Runtime.CallbackQueue"))]
big = {"ReturnValueAdapter": 0, "OwnedBufferResetAdapter": 0, "Lua.Runtime.CallbackAdapter": 0}
nine = []
for r in cb:
    k = next((k for k in big if r[8].endswith(k)), None)
    if k: big[k] += 1
    else: nine.append(r[0])
body = {r[0]: int(r[2]) for r in rows[1:] if len(r) > 2 and r[2].isdigit()}
check("N0 the population is 351 + 46 + 3 + 9", big == {"ReturnValueAdapter": 351, "OwnedBufferResetAdapter": 46, "Lua.Runtime.CallbackAdapter": 3}
      and sorted(nine) == ["0017ECB0", "00186230", "0020D9F0", "0020DA50", "002465F0", "00248030", "002481C0", "0063DC30", "006CC860"],
      "%s %s" % (big, sorted(nine)))
A, B = S(0x20DA50, 0x5E), S(0x20D9F0, 0x60)
check("N1 first-success chain walks: slot 0 / slot 1, next at +8",
      A[0x20DA6A] == "call qword ptr [rax]" and A[0x20DA70] == "mov rbx, qword ptr [rbx + 8]" and A[0x20DA8A] == "mov al, 1"
      and A[0x20DAA1] == "xor al, al" and B[0x20DA0A] == "call qword ptr [rax + 8]" and B[0x20DA11] == "mov rbx, qword ptr [rbx + 8]")
C = S(0x2481C0, 0x51)
check("N2 transition notice: bits 0/3 walk, bit 9 selects 11 else 10",
      C[0x2481D3] == "test dl, 1" and C[0x2481D8] == "test dl, 8" and C[0x2481DD] == "bt edx, 9"
      and C[0x2481E3] == "mov rax, qword ptr [rax + 0x10]" and u32(0x9150D8) == 10 and u32(0x9150F0) == 11
      and C[0x2481FB] == "jmp rax" and C[0x24820D] == "jmp rax")
D = S(0x2465F0, 0x18B)
check("N3 widget initialiser: memset, proc (NULL -> 005C5230), generation bit, message 1",
      D[0x246626] == "call 0x861ec0" and D[0x246635] == "cmove rbx, rax" and D[0x246641] == "mov qword ptr [rdi], rbx"
      and D[0x24660A] == "mov dword ptr [rsp + 0x20], 1" and D[0x246740] == "lea rdx, [rsp + 0x20]" and D[0x246748] == "call rax")
E = S(0x248030, 0x153)
check("N4 generation reconcile: bit 17 vs 0208ED5C, message 2 unless bit 18, restamp",
      E[0x248078] == "shr eax, 0x11" and E[0x248086] == "bt ecx, 0xa" and E[0x2480DB] == "or ecx, 4"
      and E[0x2480E1] == "bt ecx, 0x12" and u32(0x915108) == 2 and E[0x2480F9] == "call rax"
      and E[0x248101] == "and dword ptr [rbx + 0x40], 0xfffdffff")
F = S(0x186230, 0x7D)
check("N5 four-slot deferred drain",
      F[0x186248] == "inc eax" and F[0x18624A] == "and eax, 3" and F[0x186262] == "mov rbx, qword ptr [rbx + rcx + 0xc38]"
      and F[0x186273] == "mov rcx, qword ptr [rbx + 8]" and F[0x186277] == "call qword ptr [rbx]" and F[0x186279] == "add rbx, 0x10"
      and F[0x18629A] == "mov qword ptr [rcx + rsi + 0xc40], rax")
G = S(0x6CC860, 0xB6); H = S(0x67AB40, 0xC)
check("N6 double-buffered drain and flip",
      G[0x6CC871] == "mov ecx, dword ptr [rcx + 0xa0]" and G[0x6CC877] == "add rcx, 3" and G[0x6CC8C3] == "call qword ptr [rsi + 0x58]"
      and G[0x6CC8F3] == "mov qword ptr [rcx + rsi + 8], rax" and G[0x6CC8FF] == "sete r14b"
      and H == {0x67AB40: "add rcx, 0xa8", 0x67AB47: "jmp 0x6cc860"})
I = S(0x63DC30, 0x2D)
check("N7 dispatch-with-default", I[0x63DC32] == "mov rax, qword ptr [rcx + 0x48]" and I[0x63DC53] == "jmp rax" and I[0x63DC56] == "mov eax, 0x15")
J = S(0x17ECB0, 0xA)
check("N8 value store", J[0x17ECB0] == "mov eax, dword ptr [rcx + 0x10]" and 0x17ECB9 + struct.unpack_from("<i", d, off(0x17ECB3) + 2)[0] == 0x1DF08F8)
print("FAILS", fails)
sys.exit(1 if fails else 0)
