"""eq_action_names.py - name action ids 0x9C / 0x9D (the battle-menu equip branch, 0027C637 / 0027C65A) the way AT-9
named 0x113 / 0x95: action table row (battle_pack.bin directory +0x3C) +0x34 -> text bank 0. Controls: 0x95 must read
Dismount and 0x113 Dismiss (AT-9)."""
import sys
sys.path.insert(0, r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/dashboard")
import ff12_content as F

bp = open(r"D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin", "rb").read()
banks = F.decode_banks(bp)
act = F.st2e_rows(bp, 0x3C)
print("action rows", len(act), "bank0 entries", len(banks[0]))
for aid in (0x95, 0x113, 0x9B, 0x9C, 0x9D, 0x9E):
    r = act[aid]
    w = F.u16(r, 0x34)
    print("%#05x  +0x34=%#06x  bank0[%d] = %r  +0x1E kind=%d" % (aid, w, w & 0x7FF, F.dec(banks[0][w & 0x7FF]), r[0x1E]))
