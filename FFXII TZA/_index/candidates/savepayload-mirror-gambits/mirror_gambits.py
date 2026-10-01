"""SavePayload +0x7B12..+0x7FFF = the battle-state mirror's gambit banks (OPUS, 2026-09-27). Control, from the store alone.

  G1 the store's own rows: BattleSystemState gambitBanks GambitConfig[120] at +0x5B10 (6,240 B, so 0x34 per bank) and
     GambitConfig = slots uint16[24] +0x00, enableMask +0x30, filledCount +0x32, tail +0x33 (0x34 bytes)
  G2 the four SavePayload rows at +0x7B12 / +0x7B14 / +0x7B42 / +0x7B43 map, through payload +0x2000 + k = block +k, onto
     bank 0 slot 0's action word, bank 0 +0x04..+0x31, bank 0 filledCount, and bank 0 tail + banks 1-23 + bank 24's first
     0x10 bytes, ending at block +0x6000 (the mirror's extent)
"""
import sys
from pathlib import Path
DB = Path(__file__).resolve().parents[3]
rows = {}
for l in open(DB / "_types" / "fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if c[0] in ("BattleSystemState", "GambitConfig", "SavePayload"):
        try: rows[(c[0], int(c[1], 16))] = c
        except ValueError: pass
fails = 0
def check(nm, ok, d=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, d)); fails += (not ok)
g = rows.get(("BattleSystemState", 0x5B10))
gc = {o: rows.get(("GambitConfig", o)) for o in (0x0, 0x30, 0x32, 0x33)}
check("G1 gambitBanks GambitConfig[120] at +0x5B10, 0x34 per bank; GambitConfig slots / enableMask / filledCount / tail",
      g and g[3] == "gambitBanks" and g[4] == "GambitConfig[120]" and int(g[2]) == 120 * 0x34
      and gc[0x0] and gc[0x0][3] == "slots" and gc[0x30] and gc[0x30][3] == "enableMask"
      and gc[0x32] and gc[0x32][3] == "filledCount" and gc[0x33] and int(gc[0x33][2]) == 1)
def blk(p): return p - 0x2000
sp = {o: rows.get(("SavePayload", o)) for o in (0x7B12, 0x7B14, 0x7B42, 0x7B43)}
ok = all(sp.values())
if ok:
    b12, b14, b42, b43 = (blk(o) for o in (0x7B12, 0x7B14, 0x7B42, 0x7B43))
    ok = (b12 - 0x5B10 == 2 and int(sp[0x7B12][2]) == 2                                  # slot 0 word 1
          and b14 - 0x5B10 == 4 and b14 + int(sp[0x7B14][2]) == 0x5B10 + 0x32 and True   # +0x04..+0x31
          and b42 - 0x5B10 == 0x32 and int(sp[0x7B42][2]) == 1                             # filledCount
          and b43 - 0x5B10 == 0x33 and b43 + int(sp[0x7B43][2]) == 0x6000                   # to the mirror's end
          and (0x6000 - (0x5B10 + 24 * 0x34)) == 0x10)                                      # bank 24's first 0x10 bytes
check("G2 the four SavePayload rows map onto bank 0 and banks 1-24 as stated, ending at block +0x6000", ok)
print("FAILS", fails)
sys.exit(1 if fails else 0)
