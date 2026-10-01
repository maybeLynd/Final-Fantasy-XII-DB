"""UQ-70: logicpack.bin's record layout (OPUS, 2026-09-27). Control..

  L1 frame: u32 count (1,310), u32 offset[count]; records are contiguous in offset order and the last runs to the file end
  L2 every record is a 32-byte header of u8 group counts followed by (sum of the counts) x 24-byte entries - the length
     rule holds for all 1,310 records
  L3 the cn and kr copies are byte-identical
  L4 the format is the .ard AI block's (header 0x20 whose first 12 bytes are u8 counts, 24-byte records - the walk
     gb2-env-class-4/gb2_env_class.py E4 uses): 1,147 of the 1,310 records are byte-identical to AI blocks of the 166
     shipped .ard files, and 38,820 of the 41,197 entries occur among their entries
Entry meaning is not claimed (the executable never reads the file, UQ-380).
"""
import struct, sys, collections
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle")
b = (ROOT / "cn/binaryfile/logicpack.bin").read_bytes()
fails = 0


def check(nm, ok, d=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, d)); fails += (not ok)


n = struct.unpack_from("<I", b, 0)[0]
offs = list(struct.unpack_from("<%dI" % n, b, 4)) + [len(b)]
check("L1 1,310 records, contiguous, first after the table", n == 1310 and offs[0] >= 4 + 4 * n and all(offs[i] < offs[i + 1] for i in range(n)))
bad = []; groups = collections.Counter(); entries = 0
for k in range(n):
    r = b[offs[k]:offs[k + 1]]
    cnt = sum(r[:32]); groups[sum(1 for x in r[:32] if x)] += 1; entries += cnt
    if len(r) != 32 + 24 * cnt:
        bad.append((k, len(r), cnt))
check("L2 every record = 32-byte u8 count header + sum(counts) x 24", not bad, "(%d entries; nonzero groups per record %s; bad %s)"
      % (entries, dict(sorted(groups.items())), bad[:3]))
check("L3 cn and kr identical", (ROOT / "kr/binaryfile/logicpack.bin").read_bytes() == b)
import glob
ARD = sys.argv[2] if len(sys.argv) > 2 else r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/repos-3f/ard/ard"
u32 = lambda x, o: struct.unpack_from("<I", x, o)[0]; u16 = lambda x, o: struct.unpack_from("<H", x, o)[0]
blocks = set(); ents = set(); nard = 0
for f in sorted(glob.glob(ARD + "/*.ard")):
    a = open(f, "rb").read(); nard += 1; s1 = u32(a, 0x14)
    if not s1:
        continue
    c = u16(a, s1); so = [u32(a, s1 + 4 + 4 * i) for i in range(c + 1)]
    for k in range(c):
        base = s1 + so[k]; blk = a[base:base + 0x20 + 24 * sum(a[base:base + 12])]; blocks.add(blk)
        ents.update(blk[i:i + 24] for i in range(0x20, len(blk), 24))
recs = [b[offs[k]:offs[k + 1]] for k in range(n)]
exact = sum(1 for r in recs if r in blocks)
le = [r[i:i + 24] for r in recs for i in range(0x20, len(r), 24)]
check("L4 logicpack records are .ard AI blocks: 1,147 / 1,310 byte-identical; 38,820 / 41,197 entries shared",
      nard == 166 and exact == 1147 and sum(1 for e in le if e in ents) == 38820 and max(sum(1 for x in r[:32] if x) for r in recs) <= 12)
print("FAILS", fails)
sys.exit(1 if fails else 0)
