"""uq68_kind_source.py - UQ-68: where the battle window kind (menu +0xD8) comes from (FABLE, Claude Opus 5.5, 2026-09-26).
Static.

  K1 BattleMenu_UpdateCommandSelectionAndDispatch (002778C0) keeps its second argument in r12 and stores
     menu +0xD8 = word [r12 + 8] (002791A1-002791AC).
  K2 the battle command menu's widget procedure 00276D30 dispatches on message id - 1 through its jump table, and
     message 1 lands on the arm that starts 002778C0 as the widget's task with the message payload [msg + 8] (00276DCF,
     00276DD3); per the widget message protocol, message 1's payload is the constructor caller's locals argument.
  K3 the battle UI controller's procedure 00279E20 creates that widget (handler 00276D30, 0027A402) with locals whose
     +8 is the controller's word +0x61BA (0027A3F4, 0027A40C).
  K4 the controller's message 34 (id 0x22) stores +0x61BA = word [msg + 8] (0027A7B7-0027A7BC); message 33 stores +0x61B8.
  K5 sensitivity: the jump-table decode is checked - message 1 goes to 00276D85 and 34 to 0027A7B7, and no other id
     reaches either arm.
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
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
a = dis(0x2778C0, 0x2778F0); b = dis(0x279187, 0x2791B3)
check("K1 the dispatch stores menu +0xD8 = word [arg2 + 8]", a.get(0x2778EC) == "mov r12, rdx"
      and b.get(0x2791A1) == "movzx eax, word ptr [r12 + 8]" and b.get(0x2791AC) == "mov word ptr [rsi + 0xd8], ax")
def table(bidx, tgt, count):
    return {c: BASE + struct.unpack_from("<I", d, off(tgt) + 4 * d[off(bidx) + c - 1])[0] for c in range(1, count + 1)}
t1 = table(BASE + 0x157880, BASE + 0x157854, 0x35)
c = dis(0x276DCF, 0x276DEB)
check("K2 message 1 of the menu procedure starts the dispatch with the payload [msg + 8]", t1[1] == 0x276D85
      and c.get(0x276DCF) == "mov rax, qword ptr [rbx + 8]" and c.get(0x276DD3) == "lea r8, [rip + 0xae6]")
e = dis(0x27A3E7, 0x27A432)
check("K3 the controller creates the menu widget with locals +8 = its word +0x61BA",
      e.get(0x27A3F4) == "movzx eax, word ptr [rbx + 0x61ba]" and e.get(0x27A402) == "lea r8, [rip - 0x36d9]"
      and e.get(0x27A40C) == "mov qword ptr [rbp - 0x20], rax" and e.get(0x27A3FB) == "lea r9, [rbp - 0x28]")
t2 = table(BASE + 0x15AA38, BASE + 0x15A9E0, 0x34)
f = dis(0x27A78E, 0x27A7C4)
check("K4 controller message 34 sets +0x61BA from word [msg + 8]; message 33 sets +0x61B8",
      t2[34] == 0x27A7B7 and t2[33] == 0x27A78E and f.get(0x27A7B7) == "movzx eax, word ptr [r14 + 8]"
      and f.get(0x27A7BC) == "mov word ptr [rbx + 0x61ba], ax" and f.get(0x27A793) == "mov word ptr [rbx + 0x61b8], ax")
check("K5 sensitivity: only message 1 reaches the spawn arm and only message 34 the +0x61BA store",
      [k for k, v in t1.items() if v == 0x276D85] == [1] and [k for k, v in t2.items() if v == 0x27A7B7] == [34])
print("FAILS", fails)
sys.exit(1 if fails else 0)
