"""refresh.py - PKG-GP-STATUS-POISON Q9: what re-inflicting a status on a target that has it does (FABLE, Claude Opus 5.5,
2026-09-29). STATIC (image) + DATA (status_data.bin).

  G  THE GATE in BattleFormula_ResolveCandidateStatusApplication 00387CB0: for a candidate status the target already has
     (context +8 = the target's +0x64 | +0x3C), the add continues only when the status row's word +6 has bit 5 (0x20);
     otherwise the status is skipped and counted as "no effect" (r12 = 1, 00387D85-00387DCA, 00387EB6)
  A  THE ADD 00387BB0 (AppendStatusAddOperation) does not test presence: it sets the apply bit and writes the default
     duration (00387730; 11 for ids 2 / 6) and the default beat (003876D0) into record +0x5C[s] / +0xDC[s]
  I  THE RECORD'S TIMER SLOTS start at -1: the initialiser 003848E0 fills 32 dwords from +0x5C and 32 words from +0xDC
     with -1 (edx = -1 + 0x21 = 32 iterations, 00384950-00384963)
  C  THE COPY-THROUGH, applier step 9 (003115B6-00311606), writes every non-negative record slot into the target's
     +0xBC / +0x13C, whatever step 7's status write did
  D  DATA: bit 5 of +6 is set on exactly Stop, Sleep, Confuse, Lure, Protect, Shell, Haste, Bravery, Faith, Reflect,
     Vanish, Regen, Float and Bubble; Poison's +6 is 0xA400 (clear)
  M  MODEL: re-casting Poison on a poisoned target leaves its duration and beat as they were (no apply bit, slots stay -1);
     re-casting Haste on a hasted target: the status write refuses (already present), but the copy-through installs the
     default duration and beat - a refresh
  Not claimed: the second caller of 00387BB0 (003909F1) and its gates beyond the block mask; the random single-status path.
"""
import glob, hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
EXT = "D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle"
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
g = dis(0x387CB0, 0x387F34)
check("G", at(g, {0x387D85: "test dword ptr [rsi + 8], edi", 0x387D88: "je 0x387dd0", 0x387DC6: "test byte ptr [rcx + 6], 0x20",
                  0x387DCA: "je 0x387eb6", 0x387E71: "call 0x387bb0", 0x387EB6: "mov r12d, 1"}),
      "a present status goes on only with row +6 bit 5; else 'no effect'")
a = dis(0x387BB0, 0x387CAE)
sites = [s for s in a.values() if "+ 0x64]" in s or "+ 0x3c]" in s]
check("A", at(a, {0x387C17: "or dword ptr [r8 + 0x54], eax", 0x387C66: "call 0x387730", 0x387C6B: "mov dword ptr [rdi + 0x5c], eax",
                  0x387C78: "mov dword ptr [rdi + 0x5c], 0xb", 0x387C81: "call 0x3876d0", 0x387C86: "mov word ptr [r14 + 0xdc], ax"})
      and not sites, "the add writes default timers and tests no presence word (+0x64 / +0x3C reads: %d)" % len(sites))
i = dis(0x3848E0, 0x384965)
check("I", at(i, {0x3848FA: "or r8, 0xffffffffffffffff", 0x3848FE: "lea rcx, [rbx + 0x5c]", 0x384916: "lea rax, [rbx + 0xdc]",
                  0x384925: "lea edx, [r8 + 0x21]", 0x384950: "mov dword ptr [rcx], r8d", 0x384957: "mov word ptr [rax], r8w",
                  0x38495F: "sub rdx, 1"}) and (-1 + 0x21) == 32,
      "the record's 32 + 32 timer slots start at -1")
c = dis(0x3115B6, 0x311608)
check("C", at(c, {0x3115B9: "lea rcx, [rbx + 0x5c]", 0x3115D4: "js 0x3115db", 0x3115D6: "mov dword ptr [r9 + rcx + 0x60], eax",
                  0x3115F6: "js 0x3115fe", 0x3115F8: "mov word ptr [rax + r9 + 0x60], cx"}),
      "step 9 copies non-negative slots into the target's +0xBC / +0x13C")
NAMES = ["KO", "Stone", "Petrify", "Stop", "Sleep", "Confuse", "Doom", "Blind", "Poison", "Silence", "Sap", "Oil", "Reverse",
         "Disable", "Immobilize", "Slow", "Disease", "Lure", "Protect", "Shell", "Haste", "Bravery", "Faith", "Reflect",
         "Vanish", "Regen", "Float", "Berserk", "Bubble", "HP Critical", "Libra", "X-Zone"]
sd = open(sorted(glob.glob(os.path.join(EXT, "*", "binaryfile", "status_data.bin")))[0], "rb").read()
cn, st, rp = struct.unpack_from("<III", sd, 4)
w6 = [struct.unpack_from("<H", sd, rp + k * st + 6)[0] for k in range(cn)]
refresh = [NAMES[k] for k in range(cn) if w6[k] & 0x20]
check("D", refresh == ["Stop", "Sleep", "Confuse", "Lure", "Protect", "Shell", "Haste", "Bravery", "Faith", "Reflect", "Vanish",
                       "Regen", "Float", "Bubble"] and w6[8] == 0xA400,
      "refreshable (row +6 bit 5): %s; Poison +6 = %04X" % (refresh, w6[8]))
def recast(present, flag20, cur, default):
    """(target timers after the apply) for one status s"""
    slots = (-1, -1)
    if present and not flag20: return cur              # skipped: no apply bit, slots stay -1
    slots = default                                     # 00387BB0
    # step 7: the status write refuses when present, else installs its parameters; step 9 copies non-negative slots
    return tuple(x if x >= 0 else y for x, y in zip(slots, cur))
check("M", recast(True, False, (900, 30), (3000, 120)) == (900, 30) and recast(True, True, (900, 30), (3000, 120)) == (3000, 120),
      "Poison re-cast keeps (900, 30); Haste re-cast refreshes to (3000, 120)")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
