"""The range bytes of the action row and the equipment row, tallied the way the range-band code reads them.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract), us battle_pack.bin.
What the code reads (002FEB80, 00309300, 00320D70):
  action row +0x0C bit 26  -> the reach comes from the WEAPON (equipment row +0x18 / 10) and the two inner bands from
                              the character's parameter block, by the equipment row's kind byte +0x25 (0-5, 2 excluded)
  otherwise                -> reach = action row +0x05 / 10, inner bands = action row +0x02 / 10 and +0x03 / 10
Predictions the reading makes, each of which the data could refute:
  P1  equipment kind 2 - the one kind the code gives no per-character bands - is the long-range kind
  P2  the other kinds' +0x18 are short (melee reach)
  P3  the action rows with non-zero +0x02 / +0x03 do NOT have bit 26 (their bytes would never be read)
Control: the action table has 543 rows of 60 bytes and the equipment table 557 rows of 52 (published).
FABLE, 2026-09-19.
"""
import os, struct, collections

ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
d = open(os.path.join(ROOT, "ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin"), "rb").read()


def rows(diroff):
    o = struct.unpack_from("<I", d, diroff)[0]
    n, stride, first = struct.unpack_from("<III", d, o + 4)
    return stride, [d[o + first + i * stride: o + first + (i + 1) * stride] for i in range(n)]


sa, A = rows(0x3C)
se, E = rows(0x38)
print("control: action rows %d x %d (published 543 x 60); equipment rows %d x %d (published 557 x 52)" % (len(A), sa, len(E), se))
bit26 = [i for i, r in enumerate(A) if struct.unpack_from("<I", r, 0xC)[0] & 0x4000000]
rest = [i for i in range(len(A)) if i not in bit26]
print("action rows with +0x0C bit 26:", len(bit26))
print("  their +0x05 (NOT read for these rows):", collections.Counter(A[i][5] for i in bit26).most_common())
print("  their (+0x02, +0x03):", collections.Counter((A[i][2], A[i][3]) for i in bit26).most_common())
print("action rows without bit 26:", len(rest))
print("  their +0x05 (reach x 10):", collections.Counter(A[i][5] for i in rest).most_common(10))
print("  their (+0x02, +0x03) (inner bands x 10):", collections.Counter((A[i][2], A[i][3]) for i in rest).most_common())
nz = [i for i in range(len(A)) if A[i][2] or A[i][3]]
print("P3  rows with non-zero +0x02 / +0x03:", [(i, A[i][2], A[i][3], A[i][5]) for i in nz], "; any with bit 26:", any(i in bit26 for i in nz))
k = collections.defaultdict(collections.Counter)
for r in E:
    k[r[0x25]][r[0x18]] += 1
for kind in sorted(k):
    v = k[kind]
    print("equipment kind %d: %3d rows, +0x18 min %3d max %3d  %s" % (kind, sum(v.values()), min(v), max(v), dict(v.most_common(6))))
k2 = [x for x in k[2]]
others = [x for kind in k if kind not in (0, 2) for x in k[kind]]
print("P1  kind 2 smallest +0x18:", min(k2), " P2  largest +0x18 among kinds 1, 3, 4, 5:", max(others))
