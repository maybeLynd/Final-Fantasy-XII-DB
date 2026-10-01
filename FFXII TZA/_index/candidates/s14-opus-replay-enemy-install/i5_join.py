"""S-14 I5, the +0x50 order join (OPUS, 2026-09-26): "the +0x50 order join uses a zero-extended 16-bit count minus one and a
SIGNED jg, so zero/missing count rejects" (CONTRACT-battle-unit-construction.md I5) - executed over block 343's world (check.py,
imported: its cases run first, unchanged), the installer 0023A570 on the enemy path over the shipped rsn_b.ard.

The guard is 0023A70B..0023A726: count = word [[02EBF168]] (0 when the slot is null), then `movzx eax, word [def+0x50]`,
`dec ecx`, `cmp eax, ecx`, `jg 0023A63A` (the rejection exit). Hooks record which of the two successors runs: 0023A72C
(passed) or 0023A63A (rejected, the exit block 343's I5 row-bound case also lands on).
Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub. The slot 02EBF168 and its table are saved and
restored around each case (planted data).
Cases (definition 0, class 1):
 J0  the shipped table: the guard passes and the install returns 1 (control).
 J1  the slot null (missing count): the guard rejects at 0023A726 and the install returns 0 with no spawn initialisation.
 J2  a table whose count word is 0: the same rejection - the signed compare against -1 refuses every index, 0 included.
 J3  on the definition with the largest +0x50 index: a count equal to that index (one past the end) is rejected; a count of
     index + 1 passes. The definitions are the ones bound when this file runs: block 343's later cases rebind [02EBF120]
     to the area file's table, so the live table is read here rather than check.DEFS.
Writes i5_join_result.json.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc, r, w = C.uc, C.r, C.w
SLOT, PASSED, REJECT = 0x2EBF168, 0x23A72C, 0x23A63A
seen = []
for a, nm in ((PASSED, "passed 0023A72C"), (REJECT, "rejected 0023A63A"), (0x23A71E, "guard 0023A71E")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: seen.append(nm), begin=a, end=a)
uc.ctl_flush_tb()
TAB = 0x76900000
uc.mem_map(TAB, 0x1000)
orig_slot = r(SLOT, "<Q")[0]
LIVE = C.table(0x2EBF120)                                 # the definition table as bound NOW (block 343's later cases rebind it)
idxs = {d: r(C.row(LIVE, d) + 0x50, "<H")[0] for d in range(LIVE["count"])}
DJ3 = max(idxs, key=lambda d: (idxs[d], -d))              # the definition with the largest +0x50, for J3
idx50 = idxs[DJ3]
orig_count = r(orig_slot, "<H")[0] if orig_slot else None


def case(slot_value, count=None, d=0):
    C.world()
    if count is not None:
        uc.mem_write(TAB, bytes(0x100))
        w(TAB, "<H", count)
        slot_value = TAB
    w(SLOT, "<Q", slot_value)
    del seen[:]
    ok, v = C.install(0x0100 | d)
    out = {"ok": ok, "returned": v, "path": [s for s in seen if s != "guard 0023A71E"][:1], "guard_reached": "guard 0023A71E" in seen,
           "spawn_init": "spawn init 0023AC80" in C.ev["calls"]}
    w(SLOT, "<Q", orig_slot)
    return out


j = {"shipped": case(orig_slot), "slot_null": case(0), "count_0": case(None, 0), "count_eq_index": case(None, idx50, DJ3),
     "count_index_plus_1": case(None, idx50 + 1, DJ3)}
cases = {
    "J0_shipped_table_passes": j["shipped"]["ok"] and j["shipped"]["path"] == ["passed 0023A72C"] and j["shipped"]["returned"] == 1,
    "J1_missing_count_rejects": j["slot_null"]["ok"] and j["slot_null"]["path"] == ["rejected 0023A63A"] and j["slot_null"]["returned"] == 0
        and not j["slot_null"]["spawn_init"],
    "J2_zero_count_rejects": j["count_0"]["ok"] and j["count_0"]["path"] == ["rejected 0023A63A"] and j["count_0"]["returned"] == 0
        and not j["count_0"]["spawn_init"],
    "J3_bound_is_count_minus_one": j["count_eq_index"]["path"] == ["rejected 0023A63A"] and j["count_eq_index"]["returned"] == 0
        and j["count_index_plus_1"]["path"] == ["passed 0023A72C"],
}
res = {"ok": all(cases.values()), "cases": cases, "j3_definition": DJ3, "j3_plus50": idx50, "plus50_by_definition": idxs, "live_definitions": LIVE["count"], "shipped_count": orig_count, "slot": "%X" % orig_slot, "runs": j}
json.dump(res, open(os.path.join(HERE, "i5_join_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-40s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", json.dumps({"dj3": DJ3, "idx50": idx50, "count": orig_count, "runs": j})[:900])
