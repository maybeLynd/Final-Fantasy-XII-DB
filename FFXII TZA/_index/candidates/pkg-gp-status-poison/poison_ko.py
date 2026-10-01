"""poison_ko.py - PKG-GP-STATUS-POISON Q7: can a Poison tick KO its target? (FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

  A  THE ARM (periodic builder stage 2, status 8, 00386D9B-00386E39): flag A (+0x2C) |= 0x140; the share is
     trunc(base / 16) with base = max HP (+0x24), doubled under Bubble (bit 28), or max(current HP (+0x48), 1) under
     Disease (bit 16); a share <= 0 becomes -1 (dec); the delta is added to the record's HP accumulator +0x24; flag C
     (+0x140) |= 0x4000
  S  THE APPLIER'S STEP 10 (00311608-00311668) runs on +0x2C bit 8, which 0x140 carries, and derives the HP write's flags:
     bit 10 -> 5, bit 19 -> 8, !bit 18 -> 6, !bit 6 -> 4; A bit 3 would pick the absolute writer.
     For A = 0x140 the flags are 0x40 (suppress the alive event only) and the delta writer is used
  H  THE HP WRITE clamps new HP to the unit's floor (+0x48 of the battle unit, 0030064C) and takes the lethal branch when
     the stored HP is <= that floor (0030078B); nothing on the path tests a Poison or tick flag
  M  MODEL: max HP 1000, HP 40 -> share 62, new max(40 - 62, floor 0) = 0 -> lethal. The opposite claim ("a tick leaves
     1 HP") is rejected: under the model no clamp to 1 exists outside Disease's cap, and Disease caps only the upper side
  Not claimed: the two eligibility gates' outcome for a particular unit (they can suppress any damage, not only a tick's);
  a live observation (none exists).
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
arm = dis(0x386D9B, 0x386E3E)
check("A", at(arm, {0x386D9B: "or dword ptr [rbx + 0x2c], 0x140", 0x386DAB: "and r8d, 0x10000", 0x386DB4: "mov eax, dword ptr [rsi + 0x48]",
                    0x386DC0: "mov eax, dword ptr [rsi + 0x24]", 0x386DC3: "bt ecx, 0x1c", 0x386DC9: "add eax, eax",
                    0x386DD1: "sar eax, 4", 0x386DD6: "jle 0x386e2c", 0x386E18: "neg eax", 0x386E1A: "add dword ptr [rbx + 0x24], eax",
                    0x386E1D: "or dword ptr [rbx + 0x140], 0x4000", 0x386E2C: "dec dword ptr [rbx + 0x24]"}),
      "Poison arm: flag A |= 0x140, share = trunc(base/16) or -1, flag C |= 0x4000")
st = dis(0x311608, 0x31166A)
check("S", at(st, {0x311610: "bt ecx, 8", 0x311614: "jae 0x31166a", 0x311620: "mov edx, dword ptr [rbx + 0x24]",
                   0x311628: "shr r9d, 6", 0x31162C: "and r9d, 0x2000", 0x311638: "shr eax, 0xc", 0x311641: "and eax, 0x40",
                   0x311649: "shr eax, 2", 0x31164E: "and eax, 0x10", 0x311657: "test cl, 8", 0x311668: "call rax"}),
      "step 10 applies HP on +0x2C bit 8 with flags derived from +0x2C")
hw = dis(0x300640, 0x300656); lt = dis(0x300784, 0x300792)
check("H", at(hw, {0x30064C: "cmp r14d, eax", 0x30064F: "jge 0x300656", 0x300651: "mov r14d, eax"})
      and at(lt, {0x300784: "mov eax, dword ptr [rsp + 0xb0]", 0x30078B: "cmp dword ptr [rsi + 0x48], eax"}),
      "HP write clamps to the floor and tests lethal against the same floor")
def share(maxhp, cur, bubble=False, disease=False):
    base = max(cur, 1) if disease else (maxhp * 2 if bubble else maxhp)
    q = int(base / 16)                       # cdq / and 0xf / add / sar 4 = truncation toward zero
    return -q if q > 0 else -1
def flags(a):                                # step 10's derivation, as read
    r9 = (((a >> 6) & 0x2000) | (a & 0x400)) >> 5
    return r9 | ((~(a >> 12)) & 0x40) | ((~(a >> 2)) & 0x10)
def hp_write(old, delta, floor=0):
    new = max(old + delta, floor)
    return new, new <= floor                  # (stored HP, lethal)
f = flags(0x140)
ko = hp_write(40, share(1000, 40))
check("M", share(1000, 40) == -62 and share(1000, 40, bubble=True) == -125 and share(1000, 40, disease=True) == -2
      and share(15, 15) == -1 and f == 0x40 and ko == (0, True) and hp_write(100, share(1000, 100)) == (38, False),
      "shares -62/-125/-2/-1; flags 0x%X; HP 40 -> %s (lethal); HP 100 -> 38 (alive)" % (f, ko))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
