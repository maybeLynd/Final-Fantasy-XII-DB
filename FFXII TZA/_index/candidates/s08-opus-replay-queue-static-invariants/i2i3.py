"""S-08 I2 / I3 (OPUS, 2026-09-26), executed with no application stub over block 330's world (check.py, imported: its cases run
first, unchanged) - the constructor 0032E450, the requester 0032E870 and the recycler 0032EC40 as shipped; for I3 the pump
0032E070 and everything the requester's stall reaches run as shipped too.

I2 - list ownership is explicit: every slot is on exactly one of the free list (head 022C51D0) or the pending list (head
     022C51C0, tail 022C51C8; links +0x10 next / +0x18 prev), walked after construction, after enqueues at the head (flag 0)
     and at the tail (flag 1), and after recycling a middle, the head and the last pending slot.
I3 - no slot means a blocking retry, not an error return: with all 64 slots holding zero-byte requests, a 65th request enters
     the stall (pump -> in-flight getter -> pacer), which drains the pending zero-byte requests itself, and returns a valid id
     in the same invocation.
Evidence class: NATIVE-REPLAY (unicorn), live_game false. Writes i2i3_result.json.
"""
import json
import os

from unicorn import UC_HOOK_CODE

import check as C
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
uc, S = C.uc, C.S
PEND_H, PEND_T = 0x22C51C0, 0x22C51C8
W.ALLOWED |= W.closure(C.PUMP) | {C.PUMP}
# Named OS bridges for the pacer, each with its documented Win32 return and no blocking (declared, like world.py's OSRET):
# GetCurrentThread -> the pseudo-handle (HANDLE)-2; SetThreadPriority / GetThreadPriority / SwitchToThread / Sleep as listed.
PACER_OS = {"GetCurrentThread": 0xFFFFFFFFFFFFFFFE, "GetThreadPriority": 0, "SetThreadPriority": 1, "SwitchToThread": 0, "Sleep": 0,
            "SleepEx": 0}
for _k, _v in PACER_OS.items():
    W.OSRET[_k] = _v
    W.BRIDGED.add(_k)
entered = []
for a, nm in ((C.PUMP, "pump 0032E070"), (0x32E990, "acquire 0032E990")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: entered.append(nm), begin=a, end=a)
uc.ctl_flush_tb()


def walk(head):
    out, p, guard = [], C.r(head, "<Q")[0], 0
    while p and guard < 200:
        out.append((p - C.POOL) // 0x80)
        p = C.r(p + 0x10, "<Q")[0]
        guard += 1
    return out


def lists():
    f, pnd = walk(C.FREE), walk(PEND_H)
    return {"free": len(f), "pending": pnd, "disjoint_cover": sorted(f + pnd) == list(range(64)) and not (set(f) & set(pnd))}


def req(flag=0, nbytes=0x1000):
    C.w(C.DESC, "<iIIIQQ", 0x1000, 0, 0x55, 0, 0, 0)
    return C.run(C.REQ, 0x24, 3, C.DEST, nbytes, stack=(C.DESC, flag)) & 0xFFFFFFFF


steps = {}
uc.mem_write(C.POOL, bytes(0x2000))
C.run(C.CTOR)
steps["constructed"] = lists()
ids = [req(0) for _ in range(3)]
steps["three_head_enqueues"] = lists()
ids.append(req(1))
steps["one_tail_enqueue"] = lists()
pend = steps["one_tail_enqueue"]["pending"]
C.run(C.RECYCLE, C.POOL + pend[1] * 0x80)
steps["recycle_middle"] = lists()
pend = steps["recycle_middle"]["pending"]
C.run(C.RECYCLE, C.POOL + pend[0] * 0x80)
steps["recycle_head"] = lists()
pend = steps["recycle_head"]["pending"]
C.run(C.RECYCLE, C.POOL + pend[-1] * 0x80)
steps["recycle_last"] = lists()
i2 = all(v["disjoint_cover"] for v in steps.values()) and [len(steps[k]["pending"]) for k in
      ("constructed", "three_head_enqueues", "one_tail_enqueue", "recycle_middle", "recycle_head", "recycle_last")] == [0, 3, 4, 3, 2, 1] \
     and steps["one_tail_enqueue"]["pending"][-1] == (ids[3] & 0x3F) and steps["three_head_enqueues"]["pending"] == [ids[2] & 0x3F, ids[1] & 0x3F, ids[0] & 0x3F]

# I3: fill every slot with a zero-byte request, then a 65th.
# CONCURRENT-PRODUCER FIXTURE (declared): the pacer 0035EA30 -> 0035EB70 spins at 0035EBB0 until the frame counter [022CA5E0]
# reaches a target; in the game another thread (the frame thread) advances it. This world has no second thread, so a hook at the
# poll advances the counter by one per poll - the other thread's effect, not a change to any shipped instruction.
FRAME = 0x22CA5E0
polls = {"n": 0}
def _tick(u, a, n, _):
    polls["n"] += 1
    u.mem_write(FRAME, (int.from_bytes(bytes(u.mem_read(FRAME, 8)), "little") + 1).to_bytes(8, "little"))
uc.hook_add(UC_HOOK_CODE, _tick, begin=0x35EBB0, end=0x35EBB0)
uc.ctl_flush_tb()
uc.mem_write(C.POOL, bytes(0x2000))
C.run(C.CTOR)
fill = [req(0, nbytes=0) for _ in range(64)]
full = lists()
entered.clear()
ok65 = S.call(C.REQ, 0x24, 3, C.DEST, 0, stack=(C.DESC, 0))
from unicorn.x86_const import UC_X86_REG_RAX
rid65 = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
after = lists()
i3 = {"returned": ok65, "stopped_at": (S.st["bad"] or S.st["faults"])[:2], "id": "%X" % rid65, "pacer_polls": polls["n"], "pump_entered": entered.count("pump 0032E070"),
      "full_before": {"free": full["free"], "pending": len(full["pending"])}, "after": {"free": after["free"], "pending": len(after["pending"]),
      "disjoint_cover": after["disjoint_cover"]}}
cases = {
    "I2_every_slot_on_exactly_one_list_through_enqueues_and_recycles": i2,
    "I3_65th_request_stalls_through_the_pump_and_returns_a_slot": ok65 and full["free"] == 0 and len(full["pending"]) == 64
        and i3["pump_entered"] >= 1 and rid65 != 0 and after["disjoint_cover"],
}
res = {"ok": all(cases.values()), "cases": cases, "i2_steps": steps, "i3": i3}
json.dump(res, open(os.path.join(HERE, "i2i3_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-68s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", json.dumps(i3))
