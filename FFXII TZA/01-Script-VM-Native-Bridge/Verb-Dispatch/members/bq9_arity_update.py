"""bq9_arity_update.py — apply the BQ-9 answer (FABLE 2026-09-27, control
bq9_sync_arity.py 13 checks FAILS 0) to scriptvm-verb-table.tsv.

Marking decision (SWE2-DATA):

  * 33 no-callback rows (the *sync family + setnorecovertelepostatus,
    restartbattle, unkCall_5a6, fsmenu_syncopenchip, debug_meswin_3e) get
    arity=0 / net_or_sums=0. pops_int/pops_float stay EMPTY: the family has no
    pop sites at all (the executor hands the value stack only to begin/result,
    none exists), so "empty" is the measured answer, not a gap — and it keeps
    bq9_sync_arity.py's A1 signature intact.
  * 22 single-need + 11 hand-read-loop rows get their measured n in arity and
    net_or_sums. pops_* stay as observed (per-type counts are floors; the total
    is the answer).
  * 24 two-valued rows get a NEW status CONDITIONAL — distinct from GUARDED
    (early-out, only one branch reads): these handlers diverge mid-body when
    class-3 predicate 00263D00 skips one pop, so the measured arity is n for
    most actors and n-1 when the predicate holds. net_or_sums carries 'lo|hi'
    (GUARDED's 0|1 convention), guard names '00263D00', and arity carries the
    catalog value when it equals one of the pair (authored wins, 15 rows incl.
    aturny=2) else the larger.

Status rule for the 66 exact rows:
  cat_known & cat_args == measured -> CONFIRMED
  cat_known & cat_args != measured -> CONFLICT
  !cat_known & real name           -> DERIVED
  !cat_known & unkCall_* slot      -> DERIVED-UNNAMED
"""
import csv, sys
from pathlib import Path

TSV = Path(__file__).resolve().parents[1] / "scriptvm-verb-table.tsv"

ZERO = {  # 33 no-callback rows -> arity 0
    "003D","0046","0119","0170","01AD","01E5","0204","0208","023B","023F",
    "024C","02A9","0330","0342","0345","0350","0356","0369","036B","03B0",
    "0449","044B","048A","049B","04AB","04AD","04B5","0536","05A6","203E",
    "7036","705F","7060",
}
EXACT = {  # 22 single-need + 11 loops -> measured n
    "0147":0,"0148":0,"03BF":0,"03E0":0,"0411":0,"0498":0,"0554":0,"0573":0,
    "029D":1,"035B":1,"040D":1,"040E":1,"040F":1,
    "0412":0,"057A":0,"0359":1,"0410":1,"0413":1,"0555":1,"0566":1,"209C":1,"0486":3,
    "0352":6,"0360":3,"0355":3,"0357":4,"053E":1,"053F":1,"0540":2,"0541":2,
    "03E9":1,"01F9":0,"01FB":0,
}
COND = {  # 24 two-valued -> (lo, hi) through predicate 00263D00
    "0047":(2,3),"004E":(2,3),"0061":(2,3),"024F":(2,3),"0257":(2,3),
    "025D":(2,3),"0260":(2,3),"02C8":(2,3),"02CE":(2,3),"02D4":(2,3),
    "02D6":(2,3),"02DE":(2,3),
    "004A":(3,4),"004F":(3,4),"0064":(3,4),"0067":(3,4),"0250":(3,4),
    "0258":(3,4),"0278":(3,4),"027C":(3,4),"02C9":(3,4),"02CF":(3,4),
    "02D8":(3,4),"02DB":(3,4),
}

def status_for(row, measured):
    cat = row["cat_args"].strip()
    known = row["cat_known"].strip() == "True"
    if known and cat and int(cat) == measured:
        return "CONFIRMED"
    if known and cat and int(cat) != measured:
        return "CONFLICT"
    if row["verb"].startswith("unkCall_"):
        return "DERIVED-UNNAMED"
    return "DERIVED"

rows = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
changed = {"zero": 0, "exact": 0, "cond": 0}
seen = set()
for r in rows:
    cid = r["call_id"]
    if cid in ZERO:
        r["net_or_sums"], r["arity"] = "0", "0"
        r["arity_status"] = status_for(r, 0)
        changed["zero"] += 1; seen.add(cid)
    elif cid in EXACT:
        n = EXACT[cid]
        r["net_or_sums"], r["arity"] = str(n), str(n)
        r["arity_status"] = status_for(r, n)
        changed["exact"] += 1; seen.add(cid)
    elif cid in COND:
        lo, hi = COND[cid]
        cat = int(r["cat_args"] or "-1")
        r["net_or_sums"] = "%d|%d" % (lo, hi)
        r["guard"] = "00263D00"
        r["arity"] = str(cat if cat in (lo, hi) else hi)
        r["arity_status"] = "CONDITIONAL"
        changed["cond"] += 1; seen.add(cid)

missing = (ZERO | set(EXACT) | set(COND)) - seen
assert not missing, "unmatched call_ids: %s" % sorted(missing)
assert changed == {"zero": 33, "exact": 33, "cond": 24}, changed

with open(TSV, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(rows)

from collections import Counter
print("updated:", changed)
print(Counter(r["arity_status"] for r in rows if r["call_id"] in seen))
