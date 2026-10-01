"""S-22 WE-1 (OPUS, 2026-09-26): 'This is the PRE-AFFINITY stage, and it shares its input with the one that follows. It runs before
BattleFormula_ApplyActionElementAffinity (0038B6A0) ... and both read the same element mask at ActionDefinition + 0x13'
(CONTRACT-environmental-element-scaling.md), executed on the SHIPPED recipes through the real resolver.

Loads block 316's check.py (its cases run first, unchanged). The environment-scaling stage 0038B220 is step id 94 and the affinity
stage 0038B6A0 is step id 95 in the shipped step table 01EFA5C0. Part 1 (static, from the shipped recipe table 01EF96C0): every
recipe's committed list, and where 94 / 95 occur. Part 2 (executed): each shipped recipe whose committed list holds both is run
through the resolver 00385F60 exactly as block 316 runs recipes (planted stats / result / action row only); the loop hook records
the executed slot order, and a read hook on the action row's +0x13 byte records which function read it.
Evidence class NATIVE-REPLAY (unicorn), live_game false. No application stub. Writes we1_result.json.
"""
import bisect
import contextlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
cwd = os.getcwd(); os.chdir(HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as C
os.chdir(cwd)
from unicorn import UC_HOOK_MEM_READ
from unicorn.x86_const import UC_X86_REG_RIP

uc, state = C.uc, C.state
STARTS = sorted(C.FSTARTS)
ACTION_ID = 5
reads13 = []


def on_read(u, acc, a, n, v, _):
    if a <= C.AROWS + 0x20 * ACTION_ID + 0x13 < a + n:
        rip = u.reg_read(UC_X86_REG_RIP)
        reads13.append("%08X" % STARTS[bisect.bisect_right(STARTS, rip) - 1])


uc.hook_add(UC_HOOK_MEM_READ, on_read, begin=C.AROWS, end=C.AROWS + 0x20 * 16)
uc.ctl_flush_tb()
res = {"live_game": False, "step94": "%08X" % C.STEPS[94], "step95": "%08X" % C.STEPS[95]}
# ---- part 1: the shipped recipes ----
table = {}
for rid in range(109):
    pre, com = C.recipe(rid)
    if 94 in com or 95 in com:
        table[rid] = {"committed": com, "i94": [i for i, s in enumerate(com) if s == 94], "i95": [i for i, s in enumerate(com) if s == 95]}
res["recipes_with_94_or_95"] = {str(k): v for k, v in table.items()}
both = [rid for rid, v in table.items() if v["i94"] and v["i95"]]
only = [rid for rid, v in table.items() if not (v["i94"] and v["i95"])]
res["recipes_with_both"] = both
res["recipes_with_only_one"] = only
static_order = all(max(table[r]["i94"]) < min(table[r]["i95"]) for r in both)
# ---- part 2: executed ----
runs = {}
for rid in both:
    del reads13[:]
    ok, ret = C.run_recipe(rid, ACTION_ID)
    slots = list(state["slots"])
    runs[str(rid)] = {"ok": ok, "slots_run": slots, "halt": (state["bad"] or state["faults"])[:2], "reads_of_plus13": list(reads13)}
res["runs"] = runs
def order_ok(r):
    s = r["slots_run"]
    return 94 in s and 95 in s and s.index(94) < s.index(95)
reached = [k for k, r in runs.items() if 94 in r["slots_run"] and 95 in r["slots_run"]]
cases = {
    "static_every_recipe_with_both_lists_94_before_95": bool(both) and static_order,
    "executed_94_runs_before_95_wherever_both_run": bool(reached) and all(order_ok(runs[k]) for k in reached),
    "executed_both_stages_read_the_element_byte_plus13": bool(reached) and all(
        C.STEPS[94] in [int(x, 16) for x in runs[k]["reads_of_plus13"]] and C.STEPS[95] in [int(x, 16) for x in runs[k]["reads_of_plus13"]]
        for k in reached),
    "executed_recipes_return": all(r["ok"] for r in runs.values()),
}
res["reached_both"] = reached
res["cases"] = cases
res["ok"] = all(cases.values())
json.dump(res, open(os.path.join(HERE, "we1_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-70s %s" % (k, "PASS" if v else "FAIL"))
print("both:", both, "only one:", only)
print({k: (r["slots_run"], sorted(set(r["reads_of_plus13"])), r["halt"]) for k, r in runs.items()})
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
