"""bracket_count.py - UQ-38's static bracket recounted from the two instruments' columns (FABLE, Claude Opus 5.5, 2026-09-28).
  B1  ee_member_calls (column 'verdict') calls 47 members whole
  B2  both instruments call 31 members C+fragments
  B3  FRONTIER's (column 'frontier') 41 C+fragments members split 31 / 5 whole / 5 mostly under ee_member_calls
  B4  95 members are FRONTIER 'translated' and ee_member_calls 'C+fragments' (the disagreement)
"""
import os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [l.split("\t") for l in open(os.path.join(HERE, "../uq38-carry-criterion/uq38_carry.tsv"), encoding="utf-8").read().split("\n")[1:] if l.strip()]
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
c = collections.Counter((r[1], r[2]) for r in rows)
whole = sum(v for (e, f), v in c.items() if e == "whole")
both_c = c[("C+fragments", "C+fragments")]
fr_c = {e: v for (e, f), v in c.items() if f == "C+fragments"}
ok("B1", len(rows) == 267 and whole == 47, "%d members; ee_member_calls whole: %d" % (len(rows), whole))
ok("B2", both_c == 31, "C+fragments by both instruments: %d" % both_c)
ok("B3", fr_c == {"C+fragments": 31, "whole": 5, "mostly": 5}, "FRONTIER's C+fragments split under ee_member_calls: %s (total %d)" % (fr_c, sum(fr_c.values())))
ok("B4", c[("C+fragments", "translated")] == 95, "FRONTIER translated / ee C+fragments: %d" % c[("C+fragments", "translated")])
print("FAILS", fails); sys.exit(1 if fails else 0)
