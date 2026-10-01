"""SV-1: the party-stats array in all three development save generations, and where the battle-state block grew
(OPUS, 2026-09-27). Control. Data: the sixteen katano images; the type store's BattleStatsRecord / BattleSystemState rows.

The shipped battle-state block holds BattleStatsRecord[40] at block +8, stride 0x1C8, whose byte +4 is the definition
row index (type store). The discriminator is that same byte: a record array is found where byte +4 of consecutive
records runs 0, 1, 2, ... 39.
  P1 each generation holds exactly 40 records whose +4 byte equals the record index:
       A (00-03) image +0x2208 stride 0x1C4 | B (04, 05, 06, 15) image +0x2208 stride 0x190 | C (07-14) image +0x15FC
       stride 0x140; the shipped stride 0x1C8 finds no run in generation A (a 4-byte-per-record growth, not a shift)
  P2 generations A and B keep the array where the shipped layout does - block +8 of the block copy at image +0x2200
     (payload +0x2000); generation B's record ends at +0x190, where the shipped licencePoints field begins
  P3 REGRESSION (rejects OPUS's first SV-1 narrowing, a6ea12736, which put 160 B of the growth in a shipped tail
     +0x5A70..+0x5B10): in all four generation-A images the fields after the array sit 0xA0 = 40 x 4 lower than
     shipped - the slot maps (shipped +0x5A48 / +0x5A5A, uint16[9] of index-or-0xFFFF) are at +0x59A8 / +0x59BA,
     while the shipped offsets hold zeros, and the copy's last non-zero byte lies at or below +0x5A04 = shipped
     slotMapSourceFirst +0x5AA4 - 0xA0. So 0x7410 - 0x5A70 = 6,560 = 40 x 4 (the record growth) + 6,400 (gambitBanks
     6,240 + gambitSelectedBank 160); the shipped tail +0x5A70..+0x5B10 existed in development at +0x59D0..+0x5A70
  P4 (added the same day) the growth splits one byte before the level and three after it: generation A's level byte
     is +0x1C1 (a strictly increasing function of experience +0x18C in all 160 records) where shipped has +0x1C2,
     with experience and licencePoints unmoved; after the level A has 2 bytes and shipped 5 (the three board
     selectors and a pad)
Not claimed: which byte inside +0x194..+0x1C1 is the inserted one (a 45- to 46-byte licence-bit array is the simplest
reading, not shown), or the fields of B / C records past the head; generation C's block
framing (its array starts at +0x15FC) and what B and C hold after the array.
"""
import struct, sys
from pathlib import Path

HERE = Path(__file__).resolve()
DB = HERE.parents[3]
K = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/katano")
F = {i: (K / ("ff12savedata%02d.sav" % i)).read_bytes() for i in range(16)}
GEN = {"A": ([0, 1, 2, 3], 0x2208, 0x1C4), "B": ([4, 5, 6, 15], 0x2208, 0x190),
       "C": ([7, 8, 9, 10, 11, 12, 13, 14], 0x15FC, 0x140)}
fails = 0


def check(nm, ok, d=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, d)); fails += (not ok)


def run(b, base, s):
    k = 0
    while base + 4 + k * s < len(b) and b[base + 4 + k * s] == k: k += 1
    return k


runs = {g: [run(F[i], base, s) for i in files] for g, (files, base, s) in GEN.items()}
def best_run(b, s):
    return max(run(b, base, s) for base in range(0x2200, 0x2200 + s))
wrong = [best_run(F[i], 0x1C8) for i in GEN["A"][0]]
check("P1 40 records with +4 == index in every image: A stride 0x1C4, B 0x190, C 0x140; stride 0x1C8 finds no run in A",
      all(r == 40 for rs in runs.values() for r in rs) and max(wrong) < 6, "runs %s, 0x1C8 best %s" % (runs, wrong))

rows = {}
for l in open(DB / "_types" / "fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if c[0] in ("BattleStatsRecord", "BattleSystemState"):
        rows[(c[0], int(c[1], 16))] = c
arr = rows.get(("BattleSystemState", 0x8)); lp = rows.get(("BattleStatsRecord", 0x190))
check("P2 A and B keep the array at block +8 of the copy at image +0x2200; B's record ends where shipped licencePoints begins",
      GEN["A"][1] == GEN["B"][1] == 0x2200 + 8 and arr and arr[4] == "BattleStatsRecord[40]" and lp and lp[3] == "licencePoints")

def slotmap(b, o):
    w = struct.unpack_from("<9H", b, o); k = 0
    while k < 9 and w[k] <= 0x27: k += 1
    return 1 <= k < 9 and all(x == 0xFFFF for x in w[k:])  # an index list closed by 0xFFFF fill; zeros alone fail
ok = True; det = []
for i in GEN["A"][0]:
    b = F[i]; blk = b[0x2200:0x8200]
    last = max(j for j in range(len(blk)) if blk[j])
    shifted = slotmap(b, 0x2200 + 0x5A48 - 0xA0) and slotmap(b, 0x2200 + 0x5A5A - 0xA0)
    unshifted_zero = not any(blk[0x5A48:0x5AB6])
    ok &= shifted and unshifted_zero and last <= 0x5AA4 - 0xA0
    det.append((i, hex(last), shifted, unshifted_zero))
gb = rows.get(("BattleSystemState", 0x5B10)); gs = rows.get(("BattleSystemState", 0x7370))
check("P3 REGRESSION: generation A's post-array fields sit 0xA0 = 40 x 4 lower than shipped; 6,560 = 160 + 6,400 gambit",
      ok and gb and int(gb[2]) == 6240 and gs and int(gs[2]) == 160 and 0x7410 - 0x5A70 == 40 * 4 + 6240 + 160,
      str(det))

# P4 (added 2026-09-27, OPUS): where in the record the four bytes went. Experience (+0x18C) and licence points (+0x190)
# keep their shipped offsets in generation A; the level byte does not.
lv_rows = rows.get(("BattleStatsRecord", 0x1C2)); ex_rows = rows.get(("BattleStatsRecord", 0x18C))
pairs = []; zero_shipped = 0
for i in GEN["A"][0]:
    b = F[i]
    for r in range(40):
        o = 0x2208 + r * 0x1C4
        pairs.append((struct.unpack_from("<I", b, o + 0x18C)[0], b[o + 0x1C1]))
        zero_shipped += (b[o + 0x1C2] == 0 and b[o + 0x1C3] == 0)
by = {}
for e, l in pairs: by.setdefault(e, set()).add(l)
srt = sorted(set(pairs))
functional = all(len(v) == 1 for v in by.values()) and all(srt[k][1] < srt[k + 1][1] for k in range(len(srt) - 1))
check("P4 generation A's level is at +0x1C1 (shipped +0x1C2): a strictly increasing function of experience at +0x18C over "
      "all 160 records, levels 1-99, while the shipped offset +0x1C2 / +0x1C3 is zero in all 160 - so ONE byte was inserted "
      "between licencePoints +0x190..+0x193 and the level, and THREE after it",
      functional and len(by) >= 5 and all(1 <= l <= 99 for e, l in pairs) and zero_shipped == 160
      and lv_rows and lv_rows[3] == "level" and ex_rows and ex_rows[3] == "experience",
      "(%d distinct experience values: %s)" % (len(by), sorted((e, min(v)) for e, v in by.items())))
print("FAILS", fails)
sys.exit(1 if fails else 0)
