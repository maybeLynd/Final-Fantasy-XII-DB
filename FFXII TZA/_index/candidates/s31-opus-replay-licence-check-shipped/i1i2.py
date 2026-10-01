"""S-31 I1 / I2 (OPUS, 2026-09-26), executed over block 326's world (check.py, imported: its cases run first, unchanged) - the
ask 00323EC0(rec, actionId) over the SHIPPED licence, ability and party-slot tables.

I1 - three exits before any board data is touched, in order: invalid action id -> 0 (00323ED6); rec NULL -> 1 (00323EEA);
rec[5] != 0 -> 1 (00323EF3); rec[4] > 6, unsigned -> 1 (00323EFF).
I2 - the licence system applies only to record kind 0 with slot <= 6; everything else is licensed for everything, before a
single node is read.
Board data = the licence records behind [02EBF038] and the record's 46-byte owned mask at +0x194; a read hook over both
counts every access. Control: the same unlicensed ability with kind 0, slot 6 goes past the exits and reads the board.
Evidence class: NATIVE-REPLAY (unicorn), live_game false; no application stub. Writes i1i2_result.json.
"""
import json
import os

from unicorn import UC_HOOK_MEM_READ

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc = C.uc
reads = {"n": 0}
lo, hi = C.lic_d, C.lic_d + C.lic_n * C.lic_s
uc.hook_add(UC_HOOK_MEM_READ, lambda u, ac, a, n, v, _: reads.__setitem__("n", reads["n"] + 1), begin=lo, end=hi - 1)
uc.hook_add(UC_HOOK_MEM_READ, lambda u, ac, a, n, v, _: reads.__setitem__("n", reads["n"] + 1), begin=C.REC + 0x194, end=C.REC + 0x194 + 0x2D)
uc.ctl_flush_tb()


def ask(rec, action):
    reads["n"] = 0
    v = C.run(C.ASK, rec, action)
    return v, reads["n"]


unlicensed = [a for a in range(C.ab_n) if C.run(C.ASK, C.rec(), a) == 0]
A = unlicensed[0]
out = {"unlicensed_with_empty_board": len(unlicensed), "probe_action": A}
e1 = ask(C.rec(), 0xFFFF)                 # an id outside class 0x14
e1n = ask(0, 0xFFFF)                      # invalid id AND null record: the id test comes first
e2 = ask(0, A)
e3 = ask(C.rec(kind=1), A)
e4 = ask(C.rec(slot=7), A)
e4u = ask(C.rec(slot=0xFF), A)            # unsigned compare: 0xFF is > 6
ctl = ask(C.rec(slot=6), A)
out.update(invalid_id=e1, invalid_id_null_rec=e1n, null_rec=e2, kind1=e3, slot7=e4, slot255=e4u, control_slot6=ctl)

i2_kind = [a for a in range(C.ab_n) if C.run(C.ASK, C.rec(kind=1), a) != 1]
i2_slot = [a for a in range(C.ab_n) if C.run(C.ASK, C.rec(slot=7), a) != 1]
out.update(i2_kind1_not_licensed=i2_kind, i2_slot7_not_licensed=i2_slot)

cases = {
    "I1_exit1_invalid_id_returns_0_no_board_read": e1 == (0, 0) and e1n == (0, 0),
    "I1_exit2_null_record_returns_1": e2 == (1, 0),
    "I1_exit3_kind_nonzero_returns_1_no_board_read": e3 == (1, 0),
    "I1_exit4_slot_above_6_unsigned_returns_1_no_board_read": e4 == (1, 0) and e4u == (1, 0),
    "control_kind0_slot6_reads_the_board_and_is_refused": ctl[0] == 0 and ctl[1] > 0,
    "I2_kind_nonzero_or_slot_above_6_licensed_for_every_ability": len(unlicensed) > 0 and not i2_kind and not i2_slot,
}
res = {"ok": all(cases.values()), "cases": cases, **out}
json.dump(res, open(os.path.join(HERE, "i1i2_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-60s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", "abilities", C.ab_n, "unlicensed with an empty board", len(unlicensed))
