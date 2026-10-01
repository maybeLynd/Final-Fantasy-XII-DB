"""bf1_opcodes.py - BF-1: the semantics of every ScriptVM opcode - the facts first read for this record (FABLE, Claude
Opus 5.5, 2026-09-27). Static. The rest of the table cites pages whose own controls cover them.

  K1 dispatch: 100 targets from the RVA table 00261DF8; the six invalid-equivalents (01, 02, 19, 1A, 31, 47) all land on
     0025E60A, and every handler returns through 0025E613 / 0025E651, which advance the pc by the table length.
  K2 names: opcode N's mnemonic is record N-1's +8 pointer in 01EFEA60 (spot checks 0x36 POPI0, 0x58 CALL, 0x63 REQIALL).
  K3 SYSHALT (03) sets actor +0x14 bit 6 and rewinds the pc; SYSTEM (04) pops one value and continues.
  K4 PREQ / PREQSW / PREQEW (2A-2C) pop three values and PREQWAIT (33) pops two - none submits anything.
  K5 PUSHA / POPA, PUSHX / POPX, PUSHY / POPY move ints between the stack and the context's [+0x10], [+8], [+0xC].
  K6 POPCMPY*JMP (52-56) pop v and take JMP's path when v = / > / >= / < / <= the context's Y [+0xC]; JMPINTERNAL (60)
     is JMP's own handler (002618A8), which jumps to bytecode base [actor+0x58] + jumpTable[operand].
  K7 PUSHI (4E) and PUSHF (50) push from the slot's int / float pools [slot+0x68] / [slot+0x70] by operand; PUSHII (4F)
     pushes the sign-extended operand.
  K8 REQCHG (34) pops (value, actor, slot) and calls the per-actor override setter 0025AF60; REQCANCEL (35) recycles the
     entry range above a popped index (003DB420); REQWAIT (32) parks the context as wait kind 3 on a found entry.
  K9 OPDIV (15) tests a zero divisor on both the int and float paths; OPMOD (16) divides with no test.
  K10 DVAR (46) pops a value and hands it to the ret-0 stub 0016D6A0 - a no-op.
  K11 CALL rewinds and saves the pc when the verb yields; CALLPOPA / CALLACTPOPA pop the finished verb's result into A.
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
tg = [BASE + struct.unpack_from("<I", d, off(0x261DF8) + 4 * i)[0] for i in range(100)]
def mn(op):
    if op == 0: return None
    p = struct.unpack_from("<Q", d, off(0x1EFEA60) + 24 * (op - 1) + 8)[0]
    return d[off(p):off(p) + 24].split(b"\0")[0].decode()
check("K1 100 targets; the six invalid-equivalents land on 0025E60A",
      len(tg) == 100 and [i for i in range(100) if tg[i] == 0x25E60A] == [0x01, 0x02, 0x19, 0x1A, 0x31, 0x47])
check("K2 opcode N's name is record N-1's +8 pointer",
      mn(0x36) == "POPI0" and mn(0x58) == "CALL" and mn(0x63) == "REQIALL" and mn(0x03) == "SYSHALT" and mn(0x2D) == "RET",
      "%s %s %s" % (mn(0x36), mn(0x58), mn(0x63)))
a = dis(0x25E5EA, 0x25E60A); b = dis(0x25E649, 0x25E664)
check("K3 SYSHALT sets +0x14 bit 6 and rewinds the pc; SYSTEM pops one and continues",
      tg[3] == 0x25E5EA and a.get(0x25E5EA) == "or byte ptr [r15 + 0x14], 0x40" and a.get(0x25E607) == "sub r14, rax"
      and tg[4] == 0x25E649 and b.get(0x25E64C) == "call 0x267e10" and b.get(0x25E662) == "jmp 0x25e613")
c = dis(0x26121A, 0x261239); e = dis(0x2615A6, 0x2615BA)
check("K4 PREQ x3 pop three and PREQWAIT pops two, submitting nothing",
      tg[0x2A] == tg[0x2B] == tg[0x2C] == 0x26121A and list(c.values()).count("call 0x267e10") == 2 and c.get(0x261234) == "jmp 0x25e64c"
      and tg[0x33] == 0x2615A6 and e.get(0x2615A9) == "call 0x267e10" and e.get(0x2615B5) == "jmp 0x25e64c")
r = {k: dis(tg[k], tg[k] + 0x20) for k in (0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20)}
check("K5 A / X / Y registers at the context's +0x10 / +8 / +0xC",
      r[0x1B][tg[0x1B]] == "mov ecx, dword ptr [rsi + 0x10]" and r[0x1D][tg[0x1D]] == "mov ecx, dword ptr [rsi + 8]"
      and r[0x1E][tg[0x1E]] == "mov ecx, dword ptr [rsi + 0xc]"
      and any(t == "mov dword ptr [rsi + 0x10], eax" for t in dis(tg[0x1C], tg[0x1C] + 0x73).values())
      and any(t == "mov dword ptr [rsi + 8], eax" for t in dis(tg[0x1F], tg[0x1F] + 0x73).values())
      and any(t == "mov dword ptr [rsi + 0xc], eax" for t in dis(tg[0x20], tg[0x20] + 0x73).values()))
jmp = dis(0x2618A8, 0x2618DD)
conds = {}
for op, want in ((0x53, "jle"), (0x54, "jl"), (0x55, "jge"), (0x56, "jg")):
    t = dis(tg[op], tg[op] + 0x16); conds[op] = any(v.startswith(want + " 0x25e651") for v in t.values()) and "jmp 0x2618a8" in t.values()
q52 = dis(0x261897, 0x2618A8)
check("K6 the Y-compare jumps and JMP / JMPINTERNAL share one handler",
      tg[0x51] == tg[0x60] == 0x2618A8 and jmp.get(0x2618AE) == "call 0x3589e0" and jmp.get(0x2618B3) == "mov r14, qword ptr [r15 + 0x58]"
      and q52.get(0x26189F) == "cmp eax, dword ptr [rsi + 0xc]" and q52.get(0x2618A2) == "jne 0x25e651" and all(conds.values()), str(conds))
p = dis(0x261855, 0x261892)
check("K7 PUSHI / PUSHF read the slot's pools at +0x68 / +0x70; PUSHII pushes the sign-extended operand",
      p.get(0x261855) == "mov rax, qword ptr [r13 + 0x68]" and p.get(0x26186D) == "movsx edx, bx" and p.get(0x26187D) == "mov rax, qword ptr [r13 + 0x70]"
      and p.get(0x261863) == "call 0x267f90" and p.get(0x26188D) == "call 0x267f60")
q = dis(0x2615BA, 0x26161C); w = dis(0x261539, 0x2615A6); cc = dis(0x261301, 0x26131C)
check("K8 REQCHG -> 0025AF60; REQCANCEL -> 003DB420; REQWAIT parks as wait kind 3",
      q.get(0x2615EB) == "call 0x25af60" and cc.get(0x261312) == "call 0x3db420" and tg[0x35] == 0x261301
      and w.get(0x261596) == "mov byte ptr [rsi + 0x14], 3" and w.get(0x261571) == "call 0x3dbf60")
dv = dis(0x25F0AC, 0x25F1D6); md = dis(0x25F1D6, 0x25F232)
check("K9 OPDIV tests a zero divisor (int and float); OPMOD divides with no test",
      dv.get(0x25F0D1) == "test ebx, ebx" and dv.get(0x25F0D3) == "je 0x25e682" and any(v.startswith("ucomiss xmm6, xmm7") for v in dv.values())
      and "idiv ebx" in md.values() and not any(v == "test ebx, ebx" for v in md.values()))
dvar = dis(0x261742, 0x261761)
check("K10 DVAR pops and hands the value to the ret-0 stub",
      tg[0x46] == 0x261742 and dvar.get(0x261745) == "call 0x267e10" and dvar.get(0x261757) == "call 0x16d6a0" and d[off(0x16D6A0):off(0x16D6A0) + 3] == b"\xc2\x00\x00")
cp = dis(0x261ABB, 0x261AFE); ca = dis(0x261AFE, 0x261B15); c58 = dis(0x26199D, 0x2619EF)
check("K11 CALL saves the pc to repeat when the verb yields; CALLPOPA / CALLACTPOPA pop the completed verb's result into A",
      c58.get(0x2619B6) == "call 0x2621d0" and c58.get(0x2619C6) == "je 0x25e651" and c58.get(0x2619E7) == "mov qword ptr [rsi], r14"
      and cp.get(0x261AD4) == "call 0x2621d0" and cp.get(0x261AF1) == "call 0x267e10" and cp.get(0x261AF6) == "mov dword ptr [rsi + 0x10], eax"
      and ca.get(0x261B13) == "jmp 0x261abf")
print("FAILS", fails)
sys.exit(1 if fails else 0)
