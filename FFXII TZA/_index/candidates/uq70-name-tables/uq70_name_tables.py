"""uq70_name_tables.py - UQ-70 narrowed: two of the five undecoded test_battle/bin families are decoded (FABLE,
Claude Opus 5.5, 2026-09-26).

  N1 basic_skill_basic_skill_name.bin (cn and kr): u32 count, then count u32 offsets, ascending and inside the file,
     each to a NUL-terminated UTF-16LE string. The count is 1,345, the row count of the sibling st2e table
     basic_skill.bin. The strings are Japanese designer labels for those rows (the first is "LEVEL-00基本値").
  N2 growth_rate_growth_rate_name.bin: the same layout, 128 names, the row count of growth_rate.bin (the first is
     "テスト成長値", test growth value).
  N3 logicpack.bin: the same count-and-offsets frame. There are 1,310 records, at ascending in-file offsets, of 56 to
     3,008 bytes, every one a multiple of 8. What a record holds is not decoded here.
  N4 the cn and kr copies of each name table are byte-identical.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
R = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract") / "ps2data/image/ff12/test_battle"
def u32(b, o): return struct.unpack_from("<I", b, o)[0]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
def table(path):
    b = path.read_bytes(); n = u32(b, 0); offs = [u32(b, 4 + 4 * i) for i in range(n)]
    framed = offs == sorted(offs) and all(4 + 4 * n <= o < len(b) for o in offs)
    names = []
    for o in offs:
        e = o
        while e + 1 < len(b) and b[e:e + 2] != b"\0\0": e += 2
        names.append(b[o:e].decode("utf-16-le"))
    return b, n, framed, names
for fam, sib, first in (("basic_skill_basic_skill_name", "basic_skill", "LEVEL-00基本値"),
                        ("growth_rate_growth_rate_name", "growth_rate", "テスト成長値")):
    b, n, framed, names = table(R / "cn/binaryfile" / (fam + ".bin"))
    s = (R / "cn/binaryfile" / (sib + ".bin")).read_bytes()
    check("N1/N2 %s: %d UTF-16 names, framed, count = %s.bin's st2e row count" % (fam, n, sib),
          framed and s[:4] == b"st2e" and n == u32(s, 4) and names[0] == first and all(names),
          "sibling count %d; first %r; last %r" % (u32(s, 4), names[0], names[-1]))
    check("N4 %s: the cn and kr copies are identical" % fam, b == (R / "kr/binaryfile" / (fam + ".bin")).read_bytes())
lp = (R / "cn/binaryfile/logicpack.bin").read_bytes(); n = u32(lp, 0)
offs = [u32(lp, 4 + 4 * i) for i in range(n)]; sizes = [b - a for a, b in zip(offs, offs[1:] + [len(lp)])]
check("N3 logicpack: 1,310 records at ascending in-file offsets, 56 to 3,008 bytes, all multiples of 8",
      n == 1310 and offs == sorted(offs) and offs[0] >= 4 + 4 * n and min(sizes) == 56 and max(sizes) == 3008 and all(z % 8 == 0 for z in sizes))
print("FAILS", fails)
sys.exit(1 if fails else 0)
