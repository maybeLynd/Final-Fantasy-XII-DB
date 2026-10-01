"""S-03 (OPUS, 2026-09-26): 'Modes 4 and 5 differ in exactly one place' (CONTRACT-battle-runtime-mode.md section 6) executed -
BattleGroup_RefreshFourActorDefinitions 003266C0 run as shipped over block 348's world (check.py, imported: its ten cases run
first, unchanged) with the mode word selecting each ladder value.

Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub; ALLOWED += the static closure of 003266C0.
Planted data: the base selector table state+0x5A48 (nine u16, 0x0101..0x0909), the leader byte state+0x5AA4 (0x03, which
matches base entry 2), and the prior content of the four mapping-class tables +0x5A5A / +0x5A6C / +0x5A7E / +0x5A90 (0xEEEE).
The contract's claim: both modes rewrite the slot map to the leader alone, but mode 4 writes entries 0, 1 and 3 while mode 5
writes 0 and 1 and RESTORES entry 3 to what it held before the refresh; entry 2 keeps all nine selectors in both.
Cases:
 M4  flags = 4 (ladder 4): tables 0 (+0x5A5A), 1 (+0x5A6C) and 3 (+0x5A90) are rewritten; table 2 (+0x5A7E) = the base nine.
 M5  flags = 8 (ladder 5): tables 0 and 1 equal mode 4's; table 3 equals its content BEFORE the call; table 2 = the base nine.
 X   the only difference between the two runs' final tables is table 3.
Other ladder values are run and reported (flags 0, 1, 2), not asserted.
Writes m45_result.json.
"""
import json
import os
import struct

import check as C
import probe as P

HERE = os.path.dirname(os.path.abspath(__file__))
uc, STATE, w, r = P.uc, P.STATE, P.w, P.r
REFRESH = 0x3266C0
P.W.ALLOWED |= P.W.closure(REFRESH) | {REFRESH}
BASE = [0x0101 * (i + 1) for i in range(9)]
TABLES = {"t0_5A5A": 0x5A5A, "t1_5A6C": 0x5A6C, "t2_5A7E": 0x5A7E, "t3_5A90": 0x5A90}


def tables():
    return {k: ["%04X" % x for x in r(STATE + off, "<9H")] for k, off in TABLES.items()}


def refresh(flags, prior3=None):
    w(STATE + 0x5A48, "<9H", *BASE)
    for off in TABLES.values():
        w(STATE + off, "<9H", *([0xEEEE] * 9))
    if prior3 is not None:
        w(STATE + 0x5A90, "<9H", *prior3)
    w(STATE + 0x5AA4, "<B", 0x03)
    w(STATE + 0x5B04, "<I", flags)
    before = tables()
    ok, lad, _ = P.call(P.LADDER)
    w(STATE + 0x5B04, "<I", flags)
    good = P.S.call(REFRESH)
    return {"ladder": lad, "returned": good, "stopped_at": (P.S.st["bad"] or P.S.st["faults"])[:2], "before": before, "after": tables()}


PRIOR3 = [0x3000 + i for i in range(9)]
m4 = refresh(4)
m5 = refresh(8)
m5p = refresh(8, prior3=PRIOR3)
m4p = refresh(4, prior3=PRIOR3)
other = {f: refresh(f) for f in (0, 1, 2)}
base9 = ["%04X" % x for x in BASE]
diff = sorted(k for k in TABLES if m4p["after"][k] != m5p["after"][k])
cases = {
    "M4_mode4_rewrites_tables_0_1_3_keeps_table2_base": m4["returned"] and m4["ladder"] == 4 and m4p["returned"]
        and m4["after"]["t2_5A7E"] == base9
        and all(m4p["after"][k] != m4p["before"][k] for k in ("t0_5A5A", "t1_5A6C", "t3_5A90"))
        and m4p["after"]["t3_5A90"] != ["%04X" % x for x in PRIOR3],
    "M5_mode5_restores_table3_to_its_prior_content": m5p["returned"] and m5p["ladder"] == 5
        and m5p["after"]["t3_5A90"] == ["%04X" % x for x in PRIOR3] and m5p["after"]["t2_5A7E"] == base9
        and m5p["after"]["t0_5A5A"] == m4p["after"]["t0_5A5A"] and m5p["after"]["t1_5A6C"] == m4p["after"]["t1_5A6C"],
    "X_modes_4_and_5_differ_only_in_table3": diff == ["t3_5A90"],
}
res = {"ok": all(cases.values()), "cases": cases, "mode4": m4, "mode5": m5, "mode5_prior3": m5p, "mode4_prior3": m4p,
       "other_flags": other, "differing_tables": diff}
json.dump(res, open(os.path.join(HERE, "m45_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-56s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
for nm, x in (("m4p", m4p), ("m5p", m5p)):
    print(nm, x["ladder"], x["returned"], x["stopped_at"], json.dumps(x["after"]))
for f, x in other.items():
    print("flags", f, x["ladder"], x["returned"], x["stopped_at"], json.dumps(x["after"]))
