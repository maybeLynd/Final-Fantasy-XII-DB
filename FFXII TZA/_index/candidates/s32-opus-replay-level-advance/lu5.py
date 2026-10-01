"""S-32 LU-5 (OPUS, 2026-09-26): 'The record resolve has TWO failure shapes, and the float growth calls dereference both ... It
does not fail closed - it fails on the third growth call, after HP and MP have already been written.'
(CONTRACT-level-advance-and-growth.md LU-5), executed for the first shape over block 348's harness (check.py, imported: its own
cases run first, unchanged).

Shape 1 = the growth-row registry slot [02EBF130] is null (0030C6EA-0030C6ED -> 0030C721 xor ebp, ebp). The fixture nulls that
one cell for one run and restores it; everything else is the shipped, bound world. Observables: the HP call 002F9A60 and the
MP call 002F9B20 run and their results are stored (+0x08, +0x0C); the next instruction, 0030C757 movzx edx, byte [rbp + 0x1F],
faults on the unmapped address 0x1F; no float growth call and no level store happen. Control: the identical run with the slot
bound reaches all four float calls and the level store.
Shape 2 (the first resolve 0020E600 returning null: eax + [01F83530] == 0) is not executed - no shipped key yields it - and
LU-6 (the tested value is not the one used) is structural; both stay static.
Evidence class: NATIVE-REPLAY (unicorn), live_game false; no application stub. The fault is the observable, not a failure of
the run. Writes lu5_result.json.
"""
import json
import os
import struct

from unicorn.x86_const import UC_X86_REG_RIP

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc, S = C.uc, C.S
SLOT = 0x2EBF130
saved = C.r(SLOT, "<Q")[0]

ctrl = C.advance(10, 11, flags=C.QUIET, seed=4537)
C.w(SLOT, "<Q", 0)
f = C.advance(10, 11, flags=C.QUIET, seed=4537)
rip = uc.reg_read(UC_X86_REG_RIP)
faults = list(S.st["faults"])
C.w(SLOT, "<Q", saved)
after = C.advance(10, 11, flags=C.QUIET, seed=4537)

cases = {
    "control_slot_bound_reaches_floats_and_level_store": ctrl["returned"] and ctrl["counts"]["float"] == 4
        and ctrl["counts"]["level store"] == 1 and ctrl["level"] == 11,
    "shape1_HP_and_MP_run_and_are_stored_first": [x for x in f["order"] if x != "MT draw"] == ["HP 002F9A60", "MP 002F9B20"]
        and (f["hp"], f["mp"]) == (ctrl["hp"], ctrl["mp"]) and (f["hp"], f["mp"]) != (500, 50),
    "shape1_faults_at_0030C757_on_address_0x1F": not f["returned"] and rip == 0x30C757 and faults[:1] == ["0000001F"],
    "shape1_no_float_growth_and_no_level_store": f["counts"]["float"] == 0 and f["counts"]["level store"] == 0
        and f["floats"] == [10.0, 10.0, 10.0, 10.0] and f["level"] == 10,
    "slot_restored_run_matches_control": (after["hp"], after["mp"], after["floats"], after["level"]) == (ctrl["hp"], ctrl["mp"], ctrl["floats"], ctrl["level"]),
}
res = {"ok": all(cases.values()), "cases": cases, "control": ctrl, "shape1": {**f, "rip_at_stop": "%08X" % rip, "faults": faults},
       "restored": after}
json.dump(res, open(os.path.join(HERE, "lu5_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-56s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
