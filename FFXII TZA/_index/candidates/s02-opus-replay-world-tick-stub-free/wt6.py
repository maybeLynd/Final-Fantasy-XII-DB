"""S-02 WT-6 (OPUS, 2026-09-25): in a mode-0 world tick, measure how much work each of the three per-slot calls of the loop
003141C3..003141EC does for each slot - 00234590 (003141D4), 0025D9E0 (003141DB) and 00234520 (003141E2) - by counting the
instructions executed between each call and its return. WT-6 (CONTRACT-world-simulation-tick.md): two of the three calls do
real work only for slot 0; the actor drive pass runs for all five.

Evidence class: NATIVE-REPLAY, live_game false. Same world and run as check.py (world.py's W.run, mode 0, NO application stub).
The counting hooks are added in the tick hook and the translation cache is then flushed (uc.ctl_flush_tb()), so code
translated during the world build cannot escape the count. Writes wt6_result.json.
"""
import collections
import json
import os

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RBX

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
SITES = {0x3141D4: "00234590", 0x3141DB: "0025D9E0", 0x3141E2: "00234520"}   # call sites -> callee
RETURNS = {a + 5: c for a, c in SITES.items()}                                # each call is 5 bytes (E8 rel32)
counts = collections.defaultdict(list)                                         # (callee, slot) -> [instructions per call]
cur = {"callee": None, "slot": None, "n": 0, "body": False}
BODY = {"00234590": 0x2345B9, "00234520": 0x234533}          # first instruction after each `test ecx, ecx / jne epilogue` guard
body_hit = collections.defaultdict(list)


def hook(uc, st):
    def every(u, a, n, _):
        if cur["callee"] is not None:
            if a in RETURNS and RETURNS[a] == cur["callee"]:
                counts[(cur["callee"], cur["slot"])].append(cur["n"])
                body_hit[(cur["callee"], cur["slot"])].append(cur["body"])
                cur["callee"] = None
            else:
                cur["n"] += 1
                if BODY.get(cur["callee"]) == a:
                    cur["body"] = True
        if a in SITES:
            cur.update(callee=SITES[a], slot=u.reg_read(UC_X86_REG_RBX) & 0xFFFFFFFF, n=0, body=False)
    uc.hook_add(UC_HOOK_CODE, every)
    uc.ctl_flush_tb()


ok, st, uc = W.run(0, 0, FX["fixes"], trace_n=8, count=40000000, inits=FX["inits"], tick_hook=hook)
table = {c: {s: {"calls": len(counts[(c, s)]), "min": min(counts[(c, s)]), "max": max(counts[(c, s)])}
             for s in range(5) if counts[(c, s)]} for c in SITES.values()}
# WT-6 as stated, structurally: the guarded body of 00234590 / 00234520 runs for slot 0 and for no other slot (the
# `test ecx, ecx / jne epilogue` exit); the drive pass 0025D9E0 has no slot guard and runs the same path for all five
guarded = {c: {s: body_hit[(c, s)] for s in range(5)} for c in BODY}
drive = [table["0025D9E0"][s]["min"] for s in range(5)] if all(s in table["0025D9E0"] for s in range(5)) else None
wt6 = (ok and all(guarded[c][0] and all(guarded[c][0]) for c in BODY)
       and all(guarded[c][s] and not any(guarded[c][s]) for c in BODY for s in (1, 2, 3, 4))
       and drive is not None and len(set(drive)) == 1 and all(len(counts[("0025D9E0", s)]) >= 1 for s in range(5)))
res = {"ok": wt6, "tick_returned": ok, "stopped_at": (st["bad"] or st["faults"])[:1], "guarded_body_entered": {c: {str(k): v for k, v in d.items()} for c, d in guarded.items()},
       "per_callee_per_slot": table}
json.dump(res, open(os.path.join(HERE, "wt6_result.json"), "w"), indent=1, sort_keys=True)
print("WT6", "PASS" if wt6 else "FAIL", json.dumps(table))
