"""S-03 invariant 1's mechanism (OPUS, 2026-09-26): "every consumer testing == 2 is silently false whenever a higher condition
holds, and that is the mechanism behind per-area waivable control suppression" - executed on the consumer the contract names for
it, PartyControl_RecomputeSuppressionFromLeaderBattleState 0023B040, over block 348's world (check.py, imported: its ten cases
run first, unchanged).

0023B040 asks 00303EC0 (ladder() == 2) first (0023B065); when true it jumps straight to the emit at 0023B1C0 with only the
global mask, and the leader-derived suppression (the leader getter 003272A0 at 0023B084 and everything after it) never runs.
Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub. ALLOWED += the static closure of 0023B040 plus
its tail-jump target 0026BD40 (the call graph has no tail-jump edges) and 00377C20 (reached through the jump thunk 00313F60).
Cases (the emit's three calls are recorded with their arguments: 003592C0(1, b2), 00359200(b0, 1), 0026BD40(~b1 & 1)):
 T2  flags = 2 (ladder 2, the chocobo): 00303EC0 returns 1, the leader getter is NOT entered, the emit runs.
 T4  flags = 2|4 (ladder 4 - the chocobo bit still set, a higher condition over it): 00303EC0 returns 0 and the leader
     getter IS entered - the == 2 test is silently false and the leader-derived path runs instead.
 T5  flags = 2|8 (ladder 5): as T4.
 T0  flags = 0: as T4 (reported: the leader path is the default).
LIMIT (disclosed): this world has no party leader, so 003272A0 returns 0 and the leader path ends at once; the emitted values
therefore coincide across the runs. The cases show which PATH runs - the pre-emption - not a different suppression result.
Writes consumers_result.json.
"""
import json
import os

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX

import check as C
import probe as P

HERE = os.path.dirname(os.path.abspath(__file__))
uc, STATE, w, r = P.uc, P.STATE, P.w, P.r
SUPP, LEADER, EMIT = 0x23B040, 0x3272A0, 0x23B1C0
P.W.ALLOWED |= P.W.closure(SUPP) | {SUPP} | P.W.closure(0x26BD40) | {0x26BD40} | P.W.closure(0x377C20) | {0x377C20}
ev = []
for a, nm in ((LEADER, "leader 003272A0"), (EMIT, "emit 0023B1C0"), (0x3592C0, "003592C0"), (0x359200, "00359200"),
              (0x26BD40, "0026BD40")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev.append([nm, u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF]),
                begin=a, end=a)
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: ev.append(["00303EC0 returned", u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, 0]),
            begin=0x23B06A, end=0x23B06A)
uc.ctl_flush_tb()


def run(flags):
    w(STATE + 0x5B04, "<I", flags)
    del ev[:]
    ok = P.S.call(SUPP)
    return {"returned": ok, "stopped_at": (P.S.st["bad"] or P.S.st["faults"])[:2], "events": list(ev)}


t = {f: run(f) for f in (2, 6, 10, 0)}
nm = lambda x: [e[0] for e in x["events"]]
wrapper = lambda x: [e[1] for e in x["events"] if e[0] == "00303EC0 returned"]
cases = {
    "T2_ladder2_skips_the_leader_path": t[2]["returned"] and wrapper(t[2]) == [1] and "leader 003272A0" not in nm(t[2])
        and "emit 0023B1C0" in nm(t[2]),
    "T4_higher_condition_makes_eq2_false_leader_path_runs": t[6]["returned"] and wrapper(t[6]) == [0] and "leader 003272A0" in nm(t[6]),
    "T5_higher_condition_makes_eq2_false_leader_path_runs": t[10]["returned"] and wrapper(t[10]) == [0] and "leader 003272A0" in nm(t[10]),
}
res = {"ok": all(cases.values()), "cases": cases, "flags_2": t[2], "flags_6": t[6], "flags_10": t[10], "flags_0": t[0]}
json.dump(res, open(os.path.join(HERE, "consumers_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-60s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
for f, x in t.items():
    print(f, x["returned"], x["stopped_at"], x["events"])
