"""S-39 I-2 (OPUS, 2026-09-26): 'AND THE TEARDOWN ORDER FOLLOWS FROM I-1. At all three teardown sites the non-owning list is
cleared first and the owner destroys second' (CONTRACT-render-command-list-and-graphics-handshake.md I-2), executed at the
scene-teardown site 001E0590 (001E05A9 clear, then 001E05B6 flush) over block 312's harness (check.py, imported: its cases run
first, unchanged).

Both lists are the shipped constructors' (block 312's case A); three commands are enqueued by the real enqueue 0018C610, so
both lists hold the same three pointers (I-1). 001E0590 then runs as shipped. Allowed in addition to block 312's set: the
closure of 001E0590 and the shipped command class's destroy target 001F2460 (reached indirectly inside the flush).
STOP BOUNDARY (recorded, not stubbed): 001A14D0, which 001E0590 calls last to release a global object this world does not build
(it faults reading +0x18 of null); the order under test is complete before it.
Asserted: the clear 0018B040 is entered before the flush 0018C8F0; at the flush's entry the ordered list is empty and the
owner still holds the three commands; every free of a command happens while the ordered list is empty; the freed pointers
are exactly the three enqueued commands. The other two sites (0017CD53 / 0017CD60, 00188204 / 00188211) are the same pair in
the same order statically and are not executed here.
Evidence class: NATIVE-REPLAY (unicorn), live_game false; no application stub. Writes i2_result.json.
"""
import json
import os

from unicorn import UC_HOOK_CODE

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc = C.uc
STOP = 0x1A14D0
C.ALLOWED |= C.closure(0x1E0590) | {0x1E0590} | C.closure(0x1F2460) | {0x1F2460}
C.ALLOWED.discard(STOP)
L, O = C.q(C.G_ORDERED), C.q(C.G_OWNER)


def count(lst):
    return (C.q(lst + 8) - C.q(lst)) // 8


ev = []
for a, nm in ((C.F["clear"], "clear 0018B040"), (C.F["flush"], "flush 0018C8F0"), (0x1DB620, "001DB620")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev.append([nm, count(L), count(O)]), begin=a, end=a)
uc.ctl_flush_tb()

C.call(C.F["clear"], L)
own_before = [p for p in C.entries(O)]
for arg in (1, 2, 3):
    C.call(C.F["enqueue"], O, arg)
cmds = [p for p in C.entries(O) if p not in own_before]
same_pointers = [p for p in C.entries(L)] == [p for p in C.entries(O)][-len(C.entries(L)):] and set(cmds) <= set(C.entries(L))
ev.clear()
frees_before = list(C.state.get("frees", []))
ok = C.call(0x1E0590)
stopped = C.state.get("bad", [])
freed = [p for p in C.state.get("frees", []) if p not in frees_before]
order = [e[0] for e in ev]
at_clear = next((e for e in ev if e[0] == "clear 0018B040"), None)
at_flush = next((e for e in ev if e[0] == "flush 0018C8F0"), None)
cases = {
    "both_lists_hold_the_three_enqueued_pointers": len(cmds) == 3 and same_pointers,
    "clear_entered_before_flush": "clear 0018B040" in order and "flush 0018C8F0" in order
        and order.index("clear 0018B040") < order.index("flush 0018C8F0"),
    "at_flush_entry_ordered_list_empty_owner_still_full": at_flush is not None and at_flush[1] == 0 and at_flush[2] >= 3
        and at_clear is not None and at_clear[1] >= 3,
    "every_freed_command_was_freed_after_the_ordered_list_emptied": set(cmds) <= set(freed) and count(L) == 0,
    "run_ends_at_the_recorded_boundary_001A14D0": stopped == ["%08X" % STOP] and "001DB620" in order,
}
res = {"ok": all(cases.values()), "cases": cases, "events": ev, "commands": ["%X" % p for p in cmds], "freed": ["%X" % p for p in freed],
       "stopped_at": stopped}
json.dump(res, open(os.path.join(HERE, "i2_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-62s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
