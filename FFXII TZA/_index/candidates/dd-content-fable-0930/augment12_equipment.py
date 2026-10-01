"""augment12_equipment.py - which shipped equipment rows carry augment byte +0x1A == 12, and with which category byte +9.
The auto-status rebuild reads +0x1A only on rows whose category byte +9 is 19..22 (the award page, section 9, after
08-Combat-Formula/the-auto-status-rebuild.md). Equipment table = battle_pack.bin directory +0x38; item id = 0x1000 + row.
Names: bank 1 of the battle_pack text banks, index = row (the dashboard's eq names).
Control: rows 0x168 / 0x16F / 0x171 must carry 27 / 28 / 29 with category 21 (Embroidered Tippet, Golden Amulet, Firefly)."""
import sys, hashlib
import os
# installed at Database/FFXII TZA/_index/candidates/dd-content-fable-0930/; the decoders are Database/Tools/dashboard
_HERE = os.path.dirname(os.path.abspath(__file__))
for _d in (os.path.join(_HERE, "..", "..", "..", "..", "Tools", "dashboard"),
           r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\dashboard"):
    if os.path.isfile(os.path.join(_d, "ff12_content.py")):
        sys.path.insert(0, _d)
        break
from ff12_content import st2e_rows, decode_banks, dec

bp = open(r"D:\FFXII_TZA_extract\ps2data\image\ff12\test_battle\us\binaryfile\battle_pack.bin", "rb").read()
print("battle_pack.bin sha256", hashlib.sha256(bp).hexdigest())
eq = st2e_rows(bp, 0x38)
banks = decode_banks(bp)
names = banks[1]
print("equipment rows:", len(eq), " bank-1 names:", len(names))
for row in (0x168, 0x16F, 0x171):
    r = eq[row]
    print("control 0x%04X %-22s +0x1A=%d +9=%d" % (0x1000 + row, dec(names[row]) if row < len(names) else "?", r[0x1A], r[9]))
hits = [(i, r[9]) for i, r in enumerate(eq) if r[0x1A] == 12]
print("rows with +0x1A == 12:", len(hits))
for i, c in hits:
    print("  0x%04X %-22s +9=%d %s" % (0x1000 + i, dec(names[i]) if i < len(names) else "?", c,
                                       "(rebuild category 19-22)" if 19 <= c <= 22 else "(not a rebuild category)"))
