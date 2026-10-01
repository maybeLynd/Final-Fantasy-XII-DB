"""S-08: the pump 0032E070's state machine (CONTRACT-resource-request-queue.md section 7) executed row by row, with the external read
reduced to the one device word the pump reads (OPUS, 2026-09-26). Over block 330's world (check.py, imported: its cases run first,
unchanged).

What the pump reads of the outside world, measured from its callees: the in-flight getter 0046DFE0 returns 2 when the device word
[0215EFF4] is -1, and the result getter 0046E0E0 returns that word itself (its sign picks state 5 or 6). Issuing goes through
0046E030 -> 002DF780, the file layer (open / async read / close) - the "external read behavior" section 7 sets apart. Here the
file entry for (kind 0x24, index 3) is planted ABSENT (-1 at 02F73B6C), so 002DF780 returns at 002DF7B9 without any file call and
0046E030 still reports the issue accepted; completion is the planted device word. The other external inputs are the request's
own callbacks (+0x40 done/error, +0x48 cancel, +0x50 part), planted as small recording functions ("scripted external responses",
section 9). No application stub; nothing substitutes shipped code. ALLOWED += the pump's static closure.
Evidence class: NATIVE-REPLAY (unicorn), live_game false.
Cases (one request, kind 0x24, index 3, 0x1000 bytes, then the pump; slot fields planted where a row starts mid-flight):
 S1  state 1 with bytes -> issue (accepted), time stamped at +8 (the frame counter [022CA5E0], planted 1000), state 2 -> two
     time reads, +0 += second, state 3 -> in flight
     (device -1): the pump returns with the request still at the head in state 3 (it blocks later work).
 S5  device 0x1000 (>= 0) -> state 5, chunk byte 0: the done helper calls +0x40(id, ctx, 1); state 0; the slot is recycled.
 S6  device -5 (< 0) -> state 6: the error helper calls +0x40(id, ctx, 0) only when +0x28 == -1 (both measured); recycled.
 S4  state 4 (cancelling), device idle: the cancel callback +0x48(id) runs with +0x28 zeroed first; recycled. Without a
     callback +0x28 is NOT zeroed.
 C1  state 5, chunk byte 1, remaining > part: remaining -= part, offset / destination advance, the part callback returns 1 ->
     requeued: +0x28 = min(cap, remaining), offset aligned down to 0x800, accumulator 0, state 1, progress 0 (snapshotted when
     the pump re-issues it at 0046E030). The SAME pump call then carries the requeued part through states 1 -> 2 -> 3 -> 5
     (the device word still reports completion) and retires it - section 9's "one pump can traverse states 1->2->3->5".
 C2  the part callback returns 2: progress 2, state 5 kept; the NEXT pump re-probes the part callback first (no second
     subtraction).
 C3  the part callback returns 3: progress 3, state 5 - not a release; the next pump subtracts the previous part AGAIN.
 CE  state 5, chunk byte 1, remaining <= part: the done helper runs and the slot is recycled.
Writes pump_states_result.json.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8

import check as C
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
uc, w, r = C.uc, C.w, C.r
W.ALLOWED |= W.closure(C.PUMP) | {C.PUMP}
DEVICE, ENTRY, FRAME = 0x215EFF4, 0x2F73B6C, 0x22CA5E0
cur, issues = {}, []
PEND_H = 0x22C51C0
CB = 0x76700000                                           # recording callback fixtures: done, cancel, part
uc.mem_map(CB, 0x1000)
DONE, CANCEL, PART = CB, CB + 0x100, CB + 0x200
uc.mem_write(DONE, b"\xC3")
uc.mem_write(CANCEL, b"\xC3")
part_ret = {"v": 1}
calls = []


def on_cb(u, a, n, _):
    nm = {DONE: "done", CANCEL: "cancel", PART: "part"}[a]
    calls.append([nm, u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, "%X" % u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF])
    if nm == "part":
        u.reg_write(UC_X86_REG_RAX, part_ret["v"])


uc.mem_write(PART, b"\xC3")
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: issues.append(view(cur["slot"])), begin=0x46E030, end=0x46E030)
for a in (DONE, CANCEL, PART):
    uc.hook_add(UC_HOOK_CODE, on_cb, begin=a, end=a)
uc.ctl_flush_tb()


def fresh(nbytes=0x1000):
    uc.mem_write(C.POOL, bytes(0x2000))
    C.run(C.CTOR)
    w(C.DESC, "<iIIIQQ", 0x1000, 0, 0x55, 0, 0, 0)
    rid = C.run(C.REQ, 0x24, 3, C.DEST, nbytes, stack=(C.DESC, 0)) & 0xFFFFFFFF
    slot = C.POOL + (rid & 0x3F) * 0x80
    w(slot + 0x40, "<QQQ", DONE, CANCEL, PART)
    w(slot + 0x60, "<I", 0x77)
    w(slot + 0x70, "<Q", 0xC0FFEE)
    w(ENTRY, "<i", -1)
    w(FRAME, "<q", 1000)                                  # the time the pump stamps (0035E810 reads [022CA5E0])
    cur["slot"] = slot
    return rid, slot


def pump():
    del calls[:]
    del issues[:]
    ok = C.S.call(C.PUMP)
    return ok, (C.S.st["bad"] or C.S.st["faults"])[:2]


def view(slot):
    return {"state": r(slot + 0x20, "<B")[0], "chunk": r(slot + 0x22, "<B")[0], "progress": r(slot + 0x23, "<B")[0],
            "part_28": r(slot + 0x28, "<i")[0], "offset_2C": "%X" % r(slot + 0x2C, "<I")[0], "cap_30": "%X" % r(slot + 0x30, "<I")[0],
            "remaining_34": r(slot + 0x34, "<i")[0], "acc_00": r(slot, "<q")[0], "time_08": r(slot + 8, "<q")[0],
            "dest_38": "%X" % r(slot + 0x38, "<Q")[0], "pending_head": "%X" % r(PEND_H, "<Q")[0]}


res, cases = {}, {}
# S1
rid, slot = fresh()
w(DEVICE, "<i", -1)
ok, halt = pump()
s1 = dict(view(slot), ok=ok, halt=halt, calls=list(calls), issues=len(issues))
cases["S1_issue_stamps_time_then_2_then_3_and_waits"] = ok and s1["state"] == 3 and s1["pending_head"] == "%X" % slot and s1["time_08"] == 1000 \
    and s1["acc_00"] == 1000 and calls == [] and s1["issues"] == 1
# S5 (continues S1's slot)
w(DEVICE, "<i", 0x1000)
ok, halt = pump()
s5 = dict(view(slot), ok=ok, halt=halt, calls=list(calls))
cases["S5_delivered_calls_done_with_1_and_recycles"] = ok and calls == [["done", 0x77, "C0FFEE", 1]] and s5["state"] == 0 and s5["pending_head"] == "0"
# S6: error, with and without +0x28 == -1
s6 = {}
for label, part in (("part_minus1", -1), ("part_1000", 0x1000)):
    rid, slot = fresh()
    w(slot + 0x20, "<B", 3)
    w(slot + 0x28, "<i", part)
    w(DEVICE, "<i", -5)
    ok, halt = pump()
    s6[label] = dict(view(slot), ok=ok, halt=halt, calls=list(calls))
cases["S6_failed_reports_only_when_part_is_minus1"] = s6["part_minus1"]["ok"] and s6["part_minus1"]["calls"] == [["done", 0x77, "C0FFEE", 0]] \
    and s6["part_1000"]["ok"] and s6["part_1000"]["calls"] == [] and s6["part_minus1"]["pending_head"] == "0" and s6["part_1000"]["pending_head"] == "0"
# S4: cancel, with and without a callback
s4 = {}
for label, cb in (("with_callback", CANCEL), ("no_callback", 0)):
    rid, slot = fresh()
    w(slot + 0x48, "<Q", cb)
    w(slot + 0x20, "<B", 4)
    w(DEVICE, "<i", 0)
    ok, halt = pump()
    s4[label] = dict(view(slot), ok=ok, halt=halt, calls=list(calls))
cases["S4_cancel_zeroes_count_only_with_a_callback"] = s4["with_callback"]["ok"] and s4["with_callback"]["calls"] == [["cancel", 0x77, s4["with_callback"]["calls"][0][2] if s4["with_callback"]["calls"] else "", s4["with_callback"]["calls"][0][3] if s4["with_callback"]["calls"] else 0]] \
    and s4["with_callback"]["part_28"] == 0 and s4["no_callback"]["ok"] and s4["no_callback"]["calls"] == [] and s4["no_callback"]["part_28"] == 0x1000 \
    and s4["with_callback"]["pending_head"] == "0" and s4["no_callback"]["pending_head"] == "0"


# chunked rows
def chunked(remaining, part, ret, pumps=1):
    rid, slot = fresh()
    w(slot + 0x20, "<B", 3)
    w(slot + 0x22, "<BB", 1, 0)
    w(slot + 0x28, "<i", part)
    w(slot + 0x2C, "<I", 0x10000)
    w(slot + 0x30, "<I", 0x80000)
    w(slot + 0x34, "<i", remaining)
    w(slot + 0x38, "<Q", C.DEST)
    w(DEVICE, "<i", part)
    part_ret["v"] = ret
    out = []
    for _ in range(pumps):
        ok, halt = pump()
        v = dict(view(slot), ok=ok, halt=halt, calls=list(calls), issues=list(issues))
        out.append(v)
        w(DEVICE, "<i", -1)                               # the requeued read (if any) is in flight on the next pass
    return out


c1 = chunked(0x100000, 0x80000, 1)
rq = c1[0]["issues"][0] if c1[0]["issues"] else {}
cases["C1_part_1_requeues_with_min_cap_aligned_offset_state1"] = c1[0]["ok"] and [c[0] for c in c1[0]["calls"]] == ["part", "done"] \
    and rq.get("state") == 1 and rq.get("progress") == 0 and rq.get("remaining_34") == 0x80000 and rq.get("part_28") == 0x80000 \
    and rq.get("offset_2C") == "%X" % ((0x10000 + 0x80000) & ~0x7FF) and rq.get("dest_38") == "%X" % (C.DEST + 0x80000) and rq.get("acc_00") == 0
c2 = chunked(0x100000, 0x80000, 2, pumps=2)
cases["C2_part_2_keeps_state5_and_reprobes_without_subtracting"] = c2[0]["ok"] and c2[0]["state"] == 5 and c2[0]["progress"] == 2 \
    and c2[0]["remaining_34"] == 0x80000 and [c[0] for c in c2[1]["calls"]] == ["part"] and c2[1]["remaining_34"] == 0x80000
c3 = chunked(0x100000, 0x40000, 3, pumps=2)
cases["C3_part_3_is_not_a_release_the_next_pass_subtracts_again"] = c3[0]["ok"] and c3[0]["state"] == 5 and c3[0]["progress"] == 3 \
    and c3[0]["remaining_34"] == 0x100000 - 0x40000 and c3[1]["remaining_34"] == 0x100000 - 2 * 0x40000
ce = chunked(0x80000, 0x80000, 1)
cases["CE_last_part_calls_done_and_recycles"] = ce[0]["ok"] and [c[0] for c in ce[0]["calls"]] == ["done"] and ce[0]["pending_head"] == "0"
part_ret["v"] = 1

res = {"ok": all(cases.values()), "cases": cases, "S1": s1, "S5": s5, "S6": s6, "S4": s4, "C1": c1, "C2": c2, "C3": c3, "CE": ce}
json.dump(res, open(os.path.join(HERE, "pump_states_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-60s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
