"""SV-1: what the shipped battle-state block's extra 6,560 bytes are, against the development save images (OPUS, 2026-09-27).

  T1 the four generation-A images (ff12savedata00..03, 57,864 B) record the block size 0x5A70 at header +0x64 (shipped 0x7410)
  T2 their battle-state mirror (payload +0x2000, which copies the block's first 0x6000 bytes) is zero from block +0x5A05 on
     in all four - consistent with a 0x5A70-byte block
  T3 in the shipped layout (the type store's BattleSystemState rows) the bytes past +0x5A70 are: the slot-map / sequence /
     transition / result-echo tail +0x5A70..+0x5B10 (160 B) and the gambit configuration - gambitBanks GambitConfig[120] at
     +0x5B10 (6,240 B) and gambitSelectedBank int32[40] at +0x7370 (160 B); 6,400 of the 6,560 extra bytes are gambits
  T4 observation: the image's CRC slots (+0x0, +0xE200) are zero in all four - the dev images were never checksummed
Not claimed: whether the development build kept gambit configuration elsewhere or not at all; generations B / C past the header.
"""
import struct, sys
from pathlib import Path

HERE = Path(__file__).resolve()
DB = HERE.parents[3]
K = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/katano")
fails = 0


def check(nm, ok, d=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, d)); fails += (not ok)


files = [(K / ("ff12savedata%02d.sav" % i)).read_bytes() for i in range(4)]
check("T1 generation A records block size 0x5A70", all(len(b) == 57864 and struct.unpack_from("<I", b, 0x64)[0] == 0x5A70 for b in files))
lasts = []
for b in files:
    mir = b[0x200 + 0x2000:0x200 + 0x8000]
    lasts.append(max(i for i in range(len(mir)) if mir[i]))
check("T2 each mirror is zero from block +0x5A05", all(x < 0x5A05 for x in lasts), str([hex(x) for x in lasts]))
rows = {}
for l in open(DB / "_types" / "fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if c[0] == "BattleSystemState":
        rows[int(c[1], 16)] = c
g = rows.get(0x5B10); s = rows.get(0x7370)
check("T3 the shipped rows past +0x5A70: gambitBanks 6,240 B at +0x5B10 and gambitSelectedBank 160 B at +0x7370, ending at 0x7410",
      g and g[3] == "gambitBanks" and int(g[2]) == 6240 and s and s[3] == "gambitSelectedBank" and int(s[2]) == 160
      and 0x7370 + 160 == 0x7410 and 0x7410 - 0x5A70 == 6560)
check("T4 CRC slots zero in all four (never checksummed)", all(struct.unpack_from("<I", b, 0)[0] == 0 and struct.unpack_from("<I", b, 0xE200)[0] == 0 for b in files))
print("FAILS", fails)
sys.exit(1 if fails else 0)
