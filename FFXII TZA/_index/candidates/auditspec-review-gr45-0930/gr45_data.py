"""gr45_data.py - S8 re-derived from the shipped us battle_pack.bin without pack.py (GR-4/GR-5 review, 2026-09-30).

battle_pack.bin: dword directory at file start; entry 0x3C / 4 = 15 is the action section. Section header: +0 magic,
+4 row count (dword), +8 stride (word), +0xC row offset from the section start (the fields the binder 003845F0 and the
slot readers use: +4 count, +8 stride, +0xC rows).
"""
import struct, hashlib

PACK = "D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin"
b = open(PACK, "rb").read()
print("file %s bytes %d sha256 %s" % (PACK, len(b), hashlib.sha256(b).hexdigest()))
sec = struct.unpack_from("<I", b, 0x3C)[0]
magic = b[sec:sec + 4]
cnt = struct.unpack_from("<I", b, sec + 4)[0]
stride = struct.unpack_from("<H", b, sec + 8)[0]
roff = struct.unpack_from("<I", b, sec + 0xC)[0]
print("section 0x%X magic %r count %d stride %d rows at +0x%X" % (sec, magic, cnt, stride, roff))
rows = [b[sec + roff + i * stride: sec + roff + (i + 1) * stride] for i in range(cnt)]
nz28 = [(i, r[0x28]) for i, r in enumerate(rows) if r[0x28]]
print("+0x28 non-zero rows: %d; ids %s..%s; all in 0xD0..0xF1: %s; value == 120 + (id - 0xD0) on all: %s"
      % (len(nz28), hex(nz28[0][0]), hex(nz28[-1][0]), all(0xD0 <= i <= 0xF1 for i, v in nz28),
         all(v == 120 + i - 0xD0 for i, v in nz28)))
print("   values %s" % [v for i, v in nz28])
print("   zero inside 0xD0..0xF1: %s" % [hex(i) for i in range(0xD0, 0xF2) if not rows[i][0x28]])
print("+0x29 non-zero rows: %d" % sum(1 for r in rows if r[0x29]))
nz0b = [i for i, r in enumerate(rows) if r[0x0B]]
print("+0x0B non-zero rows: %d, range %d..%d contiguous %s; +0x0A on those rows %s"
      % (len(nz0b), nz0b[0], nz0b[-1], nz0b == list(range(nz0b[0], nz0b[-1] + 1)), sorted({rows[i][0x0A] for i in nz0b})))
pairs = [(rows[182 + 2 * k][0x0B], rows[183 + 2 * k][0x0B], rows[0x106 + k][0x0A]) for k in range(13)]
print("pairs (row 182+2k +0x0B, row 183+2k +0x0B, summon row 0x106+k +0x0A): %s" % pairs)
print("all equal: %s" % all(a == c and b_ == c for a, b_, c in pairs))
print("+0x24 word on 0xD0..0xF1: %s" % sorted({struct.unpack_from("<H", rows[i], 0x24)[0] for i in range(0xD0, 0xF2)}))
