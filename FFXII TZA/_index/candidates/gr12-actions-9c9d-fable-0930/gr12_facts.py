"""gr12_facts.py - FABLE's GR-12 narrowing (2026-09-30): the battle menu's container-kind switch in 0027C3D0, the
instructions that issue / offer actions 0x9C / 0x9D, and the three category-13 action rows. PASS/FAIL, then FAILS n.
Controls: the kind table must send kind 11 to 0027C584 and kind 24 to 0027C613 AND every other kind elsewhere, and the
row reader must name row 0x95 'Dismount' (AT-9's control) before rows 0x9B-0x9D are read."""
import os, struct, sys
import capstone
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "Tools", "dashboard"))
import ff12_content as F
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; o = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + o + 40 * i + 8) for i in range(n)]
def off(a):
    r = a - BASE
    for vsz, va, rsz, raw in secs:
        if va <= r < va + max(vsz, rsz): return raw + r - va
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
def ins(a): i = next(md.disasm(d[off(a):off(a) + 16], a)); return ("%s %s" % (i.mnemonic, i.op_str)).strip()
fails = 0
def check(name, ok, got=""):
    global fails
    print("%s %s %s" % ("PASS" if ok else "FAIL", name, got)); fails += 0 if ok else 1

# the kind switch: kind - 6 indexes the byte table 0027C6B8 (23 kinds), which selects a dword offset at 0027C6A0
check("0027C40C add eax, -6 / 0027C40F cmp eax, 0x16", ins(0x27C40C) == "add eax, -6" and ins(0x27C40F) == "cmp eax, 0x16")
idx = d[off(0x27C6B8):off(0x27C6B8) + 23]
tab = [struct.unpack_from("<I", d, off(0x27C6A0) + 4 * k)[0] + BASE for k in range(max(idx) + 1)]
dest = {k + 6: tab[b] for k, b in enumerate(idx)}
for k in sorted(dest): print("  kind %2d -> %08X" % (k, dest[k]))
check("kind 11 -> 0027C584 and nothing else", [k for k in dest if dest[k] == 0x27C584] == [11])
check("kind 24 -> 0027C613 and nothing else", [k for k in dest if dest[k] == 0x27C613] == [24])
# kind 11: an entry whose own id is 0x9C or 0x9D is issued at once
for a, want in [(0x27C591, "movzx r10d, word ptr [rdx + 0x50]"), (0x27C596, "mov r8d, 0x9c"), (0x27C5A0, "sub ax, r8w"),
                (0x27C5A4, "cmp ax, 1"), (0x27C5A8, "jbe 0x27c5f2"), (0x27C5FA, "movzx r8d, r10w"), (0x27C5FE, "call 0x311cd0"),
                (0x27C608, "mov eax, 0x17"),
                # kind 24: the stashed-item compare
                (0x27C620, "call 0x273270"), (0x27C625, "cmp di, ax"), (0x27C637, "mov r8d, 0x9c"), (0x27C65A, "mov r8d, 0x9d"),
                # the list body offers 0x9C / 0x9D only with a stash
                (0x27D131, "mov ecx, 0x9c"), (0x27D141, "cmp ax, 1"), (0x27D14D, "call 0x273270"), (0x27D152, "cmp ax, r14w"),
                # the command-list builder names 0x9B (with 0x113)
                (0x31EFB3, "sub ecx, 0x9b"), (0x31EFBB, "sub ecx, 0x78"), (0x31F17F, "cmp ebp, 0x9b")]:
    got = ins(a); check("%08X %s" % (a, want), got == want, "-> " + got)
# the rows
bp = open(r"D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin", "rb").read()
banks = F.decode_banks(bp); act = F.st2e_rows(bp, 0x3C)
check("control: row 0x95 names Dismount", F.dec(banks[0][F.u16(act[0x95], 0x34) & 0x7FF]) == "Dismount")
cat13 = [i for i, r in enumerate(act) if r[0x1E] == 13]
check("category 13 rows are exactly 0x9B-0x9D", cat13 == [0x9B, 0x9C, 0x9D], str([hex(i) for i in cat13]))
for a in (0x9B, 0x9C, 0x9D):
    r = act[a]
    print("  row %03X %s" % (a, " ".join("%02x" % b for b in r)))
    check("row %03X +0x22 = 0xFFFF (none), +0x1C = 3" % a, F.u16(r, 0x22) == 0xFFFF and r[0x1C] == 3)
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
