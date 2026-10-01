"""timers.py - PKG-GP-STATUS-POISON Q2: what the eight +0x17C timers are (FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

  T  STAGE 3 (BattleFormula_AdvanceStatusLinkedAuxTimers 00385570) walks the EFFECT-LAYER ids (a bit present in +0x68 or
     +0x78), resolves each id's row in the effect table 02EBF040 (rip at 003855FD), reads the row's byte +6 as a slot
     index (0xFF = no timer), and counts +0x17C[slot] down by one, writing the new value to the result's +0x42[slot]
  B  STAGE 2 (00386C70) is the 32 statuses' timer: it addresses the target's +0xBC[s] (duration) and +0x13C[s] (beat) through computed pointers, and
     never +0x17C (no instruction in its body carries the displacement)
  So +0x17C[8] are the effect layers' eight slot timers, not "the status duration timers": Poison's duration is +0xBC[8].
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
t = dis(0x385570, 0x385676)
check("T", at(t, {0x3855CD: "test byte ptr [rax + r14 + 0x68], dl", 0x3855D4: "test byte ptr [rax + r14 + 0x78], dl",
                  0x3855FD: "mov r8, qword ptr [rip + 0x2b39a3c]", 0x385619: "movzx edx, byte ptr [rcx + 6]",
                  0x38561D: "cmp edx, 0xff", 0x385625: "movzx ecx, word ptr [r14 + rdx*2 + 0x17c]", 0x385636: "dec ecx",
                  0x385645: "mov word ptr [rsi + rdx*2 + 0x42], cx"}) and 0x385604 + 0x2B39A3C == 0x2EBF040,
      "stage 3: effect-layer id -> effect table 02EBF040 row +6 = slot -> +0x17C[slot] - 1 -> result +0x42[slot]")
b = dis(0x386C70, 0x387017)
check("B", not any("0x17c" in s for s in b.values())
      and b.get(0x386CEB) == "movsx eax, word ptr [rcx + r15]",
      "stage 2 never addresses +0x17C; it is the 32 statuses' timer")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
