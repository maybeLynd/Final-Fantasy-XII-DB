"""S-14 I2 / I3 on the ENEMY path (OPUS, 2026-09-26), executed over block 333's enemy-install world (check.py, imported: its
cases run first, unchanged) - the installer 0023A570 with class byte 1 over the shipped rsn_b.ard, every callee real.

I2 - reset precedes the master-enable rejection: with d[02089300] = 0 the reset 00236A60 runs once and the installer returns 0;
     all-ones flags (bit 2 and bit 4 clear, as block 333's party case) come out as 0xFFEF7FB9FFE7B0E1 - the conjunction the
     contract states - and +0xEAC survives (only the success path's pulse reset clears it); no rekey, no spawn initializer.
I3 - a return of 0 can follow identity changes: on class 1 the rekey 00322050 runs after the reset and before the class
     dispatch (a nonzero class byte). With the unit's +0x40 spawn index list holding count 0 the installer then returns 0
     after the rekey; with count 1 it goes on to the real spawn initializer 0023AC80 and returns 1 (control).
     (This zero-count case is the unit's +0x40 list; whether it is the contract's '+0x50 join' rejection is not claimed.)
Evidence class: NATIVE-REPLAY (unicorn), live_game false; no application stub. Writes i2i3_enemy_result.json.
"""
import json
import os

from unicorn import UC_HOOK_CODE

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc = C.uc
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: C.ev["calls"].append("rekey 00322050"), begin=0x322050, end=0x322050)
uc.ctl_flush_tb()
ALL = 0xFFFFFFFFFFFFFFEB


def run(master=1, flags=None, eac=None, lst=(1, 0), uid=0x0100):
    C.world()
    C.w(C.MASTER, "<I", master)
    if flags is not None:
        C.w(C.POOL, "<Q", flags)
    if eac is not None:
        C.w(C.POOL + 0xEAC, "<Q", eac)
    C.w(C.LIST, "<BB", *lst)
    ok, v = C.install(uid)
    return {"ok": ok, "returned": v, "flags": "%016X" % C.r(C.POOL, "<Q")[0], "EAC": "%X" % C.r(C.POOL + 0xEAC, "<Q")[0],
            "calls": list(C.ev["calls"])}


i2 = run(master=0, flags=ALL, eac=0x3333333333333333)
ctl = run()
fail = run(lst=(0, 0))
order = ctl["calls"]
cases = {
    "I2_enemy_reset_then_master_reject": i2["ok"] and i2["returned"] == 0 and i2["calls"] == ["reset 00236A60"]
        and i2["flags"] == "FFEF7FB9FFE7B0E1" and i2["EAC"] == "3333333333333333",
    "I3_enemy_rekey_after_reset_before_dispatch_control_installs": ctl["ok"] and ctl["returned"] == 1
        and order[:2] == ["reset 00236A60", "rekey 00322050"] and "spawn init 0023AC80" in order
        and order.index("rekey 00322050") < order.index("spawn init 0023AC80"),
    "I3_enemy_return_0_after_the_rekey": fail["ok"] and fail["returned"] == 0 and fail["calls"] == ["reset 00236A60", "rekey 00322050"],
}
res = {"ok": all(cases.values()), "cases": cases, "I2_master0": i2, "control": ctl, "zero_count_list": fail}
json.dump(res, open(os.path.join(HERE, "i2i3_enemy_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-62s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
