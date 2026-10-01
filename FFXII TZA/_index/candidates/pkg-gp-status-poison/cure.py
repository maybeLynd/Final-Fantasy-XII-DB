"""cure.py - PKG-GP-STATUS-POISON Q8: how a cure removes Poison, and who writes the remove mask (FABLE, Claude Opus 5.5,
2026-09-29). STATIC (image) + DATA (battle_pack.bin, status_data.bin from the extract).

  R  THE REMOVE SLOT 0038FC10: m = 003851F0(...); on a target whose current statuses ([ctx+8]) include KO, Stone or bit 31,
     m survives only if it removes one of those (Phoenix-Down-like cures), else m = 0; then for each status i in m that the
     target has and that is NOT in its word 2 (+0x3C, the held layer): record +0x5C[i] = 0xFF and record +0x58 |= bit i. If
     nothing was removed, two globals are set to 1
  B  THE CANDIDATE BUILDER 003851F0: (a) with the first argument's byte +8 set and action row +0x2C bit 9, one random bit
     of row +0x18 (RNG); (b) for action 0x62 (Remedy) the statuses (the status-definition bank 02EBF118) whose status_data row word +6 has 0x400, plus 0x4000 /
     0x1000 / 0x800 when context byte +0x28 bit 4 / 5 / 6 is set; (c) otherwise 00384C30
  O  00384C30: an action row with a non-zero recipe (+0x08) gives its authored status mask +0x18 (a zero recipe takes the
     weapon's status through the equipment table instead)
  D  DATA: Poisona (0x03, recipe 1) and Antidote (0x5B, recipe 34) carry +0x18 = 0x100 = Poison only; Remedy's base set
     (flag 0x400) is Blind, Poison, Silence, Slow; the three context bits add {Stop, Doom, Disease}, {Petrify, Confuse, Oil},
     {Sleep, Sap, Disable, Immobilize}. The four shipped status_data.bin copies are byte-identical
  W  THE REMOVE MASK HAS A SECOND WRITER: the periodic builder's stage 2 (00386C70) ORs +0x58 at 00386F55 (expired
     statuses) and 00386FF3 (HP Critical, bit 29)
  Not claimed: which context bit is which Remedy Lore license (the ids 116-118 are the evaluation context's); the random
  path's users; the first argument's identity beyond its byte +8.
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
r = dis(0x38FC10, 0x38FCBA)
check("R", at(r, {0x38FC27: "call 0x3851f0", 0x38FC2C: "mov ecx, dword ptr [rbx + 8]", 0x38FC32: "test ecx, 0x80000003",
                  0x38FC3A: "and ecx, eax", 0x38FC4A: "cmovae r8d, edi", 0x38FC60: "test r8d, eax",
                  0x38FC65: "test dword ptr [rsi + 0x3c], eax", 0x38FC6A: "test dword ptr [rbx + 8], eax",
                  0x38FC78: "mov dword ptr [rdx + rcx], 0xff", 0x38FC83: "or dword ptr [rcx + 0x58], eax",
                  0x38FC96: "mov dword ptr [rip + 0x275e31c], 1"}),
      "remove slot: candidates & present & not held in +0x3C -> +0x58 bit and +0x5C[i] = 0xFF")
b = dis(0x3851F0, 0x385561)
check("B", at(b, {0x3852A6: "mov eax, 0x200", 0x3852AB: "test word ptr [rcx + 0x2c], ax", 0x385307: "mov ecx, dword ptr [rcx + 0x18]",
                  0x385321: "call 0x379cd0", 0x3853AD: "cmp dx, 0x62", 0x3853C5: "mov r14d, 0x400",
                  0x38541E: "test byte ptr [r15 + 0x28], 0x10", 0x385429: "mov r14d, 0x4000",
                  0x38547E: "test byte ptr [r15 + 0x28], 0x20", 0x385489: "mov r14d, 0x1000",
                  0x3854DE: "test byte ptr [r15 + 0x28], 0x40", 0x3854E7: "mov ebp, 0x800",
                  0x38540C: "test word ptr [rcx + 6], r14w", 0x385544: "call 0x384c30"})
      and b.get(0x3853B7) == "mov rdx, qword ptr [rip + 0x2b39d5a]" and 0x3853BE + 0x2B39D5A == 0x2EBF118,
      "builder: random-one (row +0x2C bit 9), Remedy 0x62 from status +6 flags 0x400 / 0x4000 / 0x1000 / 0x800, else 00384C30")
o = dis(0x384C30, 0x384E4E)
check("O", at(o, {0x384C90: "cmp byte ptr [rcx + 8], bl", 0x384C93: "jne 0x384e06", 0x384E3B: "mov eax, dword ptr [rbx + 0x18]",
                  0x384DB2: "mov ebx, dword ptr [rbx + 0x20]"}),
      "non-zero recipe -> row +0x18; zero recipe -> equipment row +0x20")
NAMES = ["KO", "Stone", "Petrify", "Stop", "Sleep", "Confuse", "Doom", "Blind", "Poison", "Silence", "Sap", "Oil", "Reverse",
         "Disable", "Immobilize", "Slow", "Disease", "Lure", "Protect", "Shell", "Haste", "Bravery", "Faith", "Reflect",
         "Vanish", "Regen", "Float", "Berserk", "Bubble", "HP Critical", "Libra", "X-Zone"]
bp = open(os.path.join(EXT, "us", "binaryfile", "battle_pack.bin"), "rb").read()
so = struct.unpack_from("<I", bp, 0x3C)[0]; cnt, stride, rows = struct.unpack_from("<III", bp, so + 4)
row = lambda i: bp[so + rows + i * stride:so + rows + (i + 1) * stride]
sd_paths = sorted(glob.glob(os.path.join(EXT, "*", "binaryfile", "status_data.bin")))
sds = [open(p, "rb").read() for p in sd_paths]
sd = sds[0]; c2, st2, rp2 = struct.unpack_from("<III", sd, 4)
flagset = lambda f: [NAMES[k] for k in range(c2) if struct.unpack_from("<H", sd, rp2 + k * st2 + 6)[0] & f]
dd = {0x03: row(0x03), 0x5B: row(0x5B)}
D = bp[so:so + 4] == b"st2e" and cnt == 543 and stride == 60 \
    and all(dd[i][8] != 0 and struct.unpack_from("<I", dd[i], 0x18)[0] == 0x100 for i in dd) \
    and flagset(0x400) == ["Blind", "Poison", "Silence", "Slow"] and flagset(0x4000) == ["Stop", "Doom", "Disease"] \
    and flagset(0x1000) == ["Petrify", "Confuse", "Oil"] and flagset(0x800) == ["Sleep", "Sap", "Disable", "Immobilize"] \
    and len(sds) == 4 and all(x == sd for x in sds)
check("D", D, "Poisona/Antidote +0x18 = 0x100 (Poison); Remedy base %s; +bit4 %s; +bit5 %s; +bit6 %s; %d identical status_data copies"
      % (flagset(0x400), flagset(0x4000), flagset(0x1000), flagset(0x800), len(sds)))
w = dis(0x386F40, 0x386FFA)
check("W", w.get(0x386F55) == "or dword ptr [rbx + 0x58], ebp" and w.get(0x386FF3) == "or dword ptr [rbx + 0x58], 0x20000000",
      "stage 2 also writes the remove mask (expired statuses; HP Critical bit 29)")
def cure(mask, present, held, terminal=0x80000003):
    if present & terminal and not (mask & present & terminal): mask = 0
    return mask & present & ~held
check("M", cure(0x100, 0x100, 0) == 0x100 and cure(0x100, 0x100, 0x100) == 0 and cure(0x100, 0x101, 0) == 0
      and cure(0x101, 0x101, 0) == 0x101,
      "model: Antidote cures Poison; not a held Poison; not on a KO'd target unless the cure also lifts KO")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
