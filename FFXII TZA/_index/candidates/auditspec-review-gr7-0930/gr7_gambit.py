"""gr7_gambit.py - SWE2-AUDIT-SPEC review of GR-7 K6: player gambit rows, decoded the way the rebuild copies them
(2026-09-30). No package code.

The rebuild GambitRuntime_RebuildOrderSetFromConfig 00328140 (read in this review, 00328226..00328273) fills each
24-byte record from a target-condition row of the battle_pack directory +0x20 section: entry e (record +6+6e) gets
operand = row byte +0x10+e, the {mode, opcode} word = row word +8+2e, param = row word +0x18+2e. The evaluator
00301AD0 reads mode at entry +2 (low byte) and opcode at entry +3 (high byte). So the opcode of entry e is
row[+9+2e]. Counted over the 256 rows of every language copy of battle_pack.bin in the full extract; the operand bytes
(+0x10..+0x12) are shown as a decode control (the gambit page gives 137 / 68 / 51 rows for relation 1 / 2 / 4).
"""
import glob, struct, collections, hashlib

files = sorted(glob.glob("D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/*/binaryfile/battle_pack.bin"))
print("battle_pack copies: %d" % len(files))
for f in files:
    b = open(f, "rb").read()
    sec = struct.unpack_from("<I", b, 0x20)[0]
    cnt = struct.unpack_from("<I", b, sec + 4)[0]
    stride = struct.unpack_from("<H", b, sec + 8)[0]
    hi = struct.unpack_from("<H", b, sec + 0xA)[0]
    first = struct.unpack_from("<I", b, sec + 0xC)[0]
    rows = [b[sec + first + stride * r: sec + first + stride * (r + 1)] for r in range(cnt)]
    opc = collections.Counter()
    hit = []
    for r, row in enumerate(rows):
        for e in range(3):
            o = row[9 + 2 * e]
            opc[o] += 1
            if o in (0x36, 0x37):
                hit.append((r, e, hex(o)))
    rel = collections.Counter(row[0x10] for row in rows)
    print("%s: section 0x%X magic %r rows %d stride %d (next word %d) first +0x%X sha256 %s" % (
        f.replace(chr(92), "/").split("/")[-3], sec, b[sec:sec + 4], cnt, stride, hi, first, hashlib.sha256(b[sec:sec + first + stride * cnt]).hexdigest()[:16]))
    print("   entry opcodes 0x36/0x37: %d %s; distinct opcodes %d; entry-0 relation byte counts %s"
          % (len(hit), hit[:5], len(opc), dict(sorted(rel.items()))))
