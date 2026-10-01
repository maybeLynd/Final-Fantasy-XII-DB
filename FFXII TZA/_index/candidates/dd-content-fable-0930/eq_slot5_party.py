"""eq_slot5_party.py - the party half of the N = 5 question. GambitRuntime_RebuildOrderSetFromConfig (00328140) fills the
order record's three selector entries from a gambit target-condition row (battle_pack.bin directory +0x20, the table behind
02EBF0D8): entry +0 (the operand word) from row bytes +0x10/+0x11/+0x12 and entry +2 (a word: low byte = the slot operand
00301B1A reads, high byte = the switch selector 00301B14 reads) from row words +8/+0xA/+0xC (Z-2).
Count rows whose word at +8/+0xA/+0xC has high byte 0x1A/0x1B, and among them low byte 5.
Control: 256 rows; row +0x10 takes only 1, 2 and 4 (Z-15)."""
import sys, struct, collections
sys.path.insert(0, r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/dashboard")
import ff12_content as F

bp = open(r"D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin", "rb").read()
rows = F.st2e_rows(bp, 0x20)
print("rows", len(rows), "row size", len(rows[0]))
print("control +0x10 values:", sorted(collections.Counter(r[0x10] for r in rows).items()))
hi = collections.Counter()
hits = []
for i, r in enumerate(rows):
    for k, off in enumerate((8, 0xA, 0xC)):
        w = struct.unpack_from("<H", r, off)[0]
        hi[w >> 8] += 1
        if (w >> 8) in (0x1A, 0x1B):
            hits.append((i, k, "%#06x" % w, r[0x10 + k]))
print("high-byte (selector) histogram:", sorted(hi.items()))
print("0x1A/0x1B selector words:", len(hits), hits[:20])
print("with slot operand 5:", [h for h in hits if int(h[2], 16) & 0xFF == 5])
