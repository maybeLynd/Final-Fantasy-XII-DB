"""S-36 R-4 / R-5 (OPUS, 2026-09-26): CONTRACT-ui-request-router.md's latch invariant and the drain's guard, executed over block
327's world (check.py, imported: its eight cases run first, unchanged).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub. ALLOWED += the static closures of the release
00252D90 and the hard reset 00252DE0, and the tail-jump targets the call graph lacks: 00226BA0 (from 0036D830) and 0028F2A0
(from 00252DE0). Block 327's two stop boundaries stay (001DBA90 audio, 002909F0 widget internals): a drain that dispatches
ends inside the router's mount at 002909F0, after the router's entry has been recorded with its arguments. One more recorded
stop: 0036C000, the `jmp $` of 0036BFE0 when bit ecx of [022D89B8] is clear, which request 12's mount reaches here.
Planted data only: the mailbox 0215F1A0.. (pending byte, blocked byte, id, parameter), the request word / latch 02092730 /
02092734, the eight 0x68-byte slot records at 0215F200, and the two words 020D46A0 / 020D46B8 that 0036D830 -> 00226BA0
reads ("a transition is running" = their AND != -1).
Cases:
 C4   census from the image: 02092734 has exactly three readers (00254B71 router, 00253FE3 arbiter, 003F4FD7 mirror) and three
      writers (00252B46 the setter, 00252DCB the release, 00252E05 the hard reset).
 L4   the release 00252D90 and the hard reset 00252DE0 each clear the latch and the request word.
 D0   the drain 002E09A0 with a pending request (id 7, parameter 0x22), request word 0, empty slots: it calls the router
      00254B50(7, 0x22, 0).
 DW   request word 5 -> dispatched; request word 3 -> not dispatched.
 DP   pending byte 0 -> not dispatched.
 DS   a live slot (+0x00 non-null, +0x08 = 7 so the per-slot pass leaves it alone) with +0x38 set -> not dispatched; with
      +0x3E = 0x01 -> not dispatched; with +0x3E = 0x80 -> DISPATCHED (the test is +0x3E bit 0: 002E0C8D..002E0C99,
      movzx / shl al,7 / sar al,7 / or +0x38).
 DM   NOT IN THE CONTRACT: 00267360(0) - manager slot 0 (02098E10) +0x10 bit 0 clear, or +0x11 bit 0 / +0x10 bit 7 set - makes
      the drain ZERO the four mailbox cells (002E0B94..002E0BA3): the request is discarded, not deferred, and the router
      is not called. The other cases plant slot 0 as ready (+0x10 = 1, +0x11 = 0).
 DT   for id 7 (outside {12, 15, 17, 18, 19}) the drain dispatches whether or not a transition is running: the clause
      blocks only when a transition runs AND 0053DD10 returns 0, and 0053DD10 is `mov eax, 1; ret` in this build.
Writes r45_result.json.
"""
import json
import os
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

import check as C
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
uc, S, w, r = C.uc, C.S, C.w, C.r
RELEASE, HARD = 0x252D90, 0x252DE0
W.ALLOWED |= W.closure(RELEASE) | {RELEASE} | W.closure(HARD) | {HARD} | W.closure(0x226BA0) | {0x226BA0} | \
             W.closure(0x28F2A0) | {0x28F2A0}
PEND, BLOCKED, MID, MPARAM, SLOTS, TA, TB = 0x215F1A0, 0x215F1A1, 0x215F1A4, 0x215F1A8, 0x215F200, 0x20D46A0, 0x20D46B8
MSLOT0 = 0x2098E10                                      # manager slot 0 (stride 0x288), read by 00267360(0) at +0x10 / +0x11
# A third recorded stop (disclosed): 0036BFE0 spins forever at 0036C000 (`jmp 0036C000`) when bit ecx of [022D89B8] is clear;
# request 12's mount reaches it in this world. The run ends there, after the router's entry.
from unicorn import UC_HOOK_CODE
C.STOPS[0x36C000] = "0036C000 jmp-self (bit of [022D89B8] clear)"
uc.hook_add(UC_HOOK_CODE, C.on_stop, begin=0x36C000, end=0x36C000)
uc.ctl_flush_tb()
DUMMY = 0x76600000
uc.mem_map(DUMMY, 0x1000)

# ---- C4: the census ----
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
acc = []
for line in open(os.path.join(W.GRAPH, "functions.tsv"), encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    if not p[0][:1] or p[0][:1] not in "0123456789ABCDEF" or len(p) < 3 or not p[2].isdigit():
        continue
    fa, n = int(p[0], 16), int(p[2])
    try:
        code = C.pe.get_data(fa - 0x120000, n) if hasattr(C, "pe") else None
    except Exception:
        code = None
    if code is None:
        code = bytes(uc.mem_read(fa, n))
    for i in md.disasm(code, fa):
        for k, op in enumerate(i.operands):
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and i.address + i.size + op.mem.disp == C.LATCH:
                acc.append(["%08X" % fa, "%08X" % i.address, "W" if k == 0 and i.mnemonic == "mov" else "R", i.mnemonic])
readers = sorted(x[1] for x in acc if x[2] == "R")
writers = sorted(x[1] for x in acc if x[2] == "W")


def mailbox(pending=1, mid=7, param=0x22, word=0, slot=None, trans=False, ms=(0x01, 0x00)):
    C.reset()
    w(MSLOT0 + 0x10, "<BB", *ms)
    w(PEND, "<BBxxII", pending, 0, mid, param)
    w(C.WORD, "<I", word)
    uc.mem_write(SLOTS, bytes(8 * 0x68))
    if slot is not None:
        w(SLOTS, "<QI", DUMMY, 7)
        w(SLOTS + 0x38, "<B", slot.get("38", 0))
        w(SLOTS + 0x3E, "<B", slot.get("3E", 0))
    w(TA, "<Q", 0 if trans else 0xFFFFFFFFFFFFFFFF)
    w(TB, "<Q", 0 if trans else 0xFFFFFFFFFFFFFFFF)


def drain(**kw):
    mailbox(**kw)
    ok, _ = C.call(C.DRAIN)
    routed = [s for s in C.seen if s[0] == "router"]
    return {"returned": ok, "stop": C.stop.get("at"), "faults": (S.st["bad"] or S.st["faults"])[:2],
            "router": [[s[1], "%X" % s[2]] for s in routed], "pending_after": r(PEND, "<B")[0]}


res, cases = {"census": {"accesses": acc, "readers": readers, "writers": writers}}, {}
cases["C4_latch_three_readers_three_writers"] = readers == ["003F4FD7", "00253FE3", "00254B71"][::-1][::-1] and False or \
    (sorted(readers) == ["00253FE3", "00254B71", "003F4FD7"] and sorted(writers) == ["00252B46", "00252DCB", "00252E05"])

# ---- L4: the two clears ----
clr = {}
for nm, fn in (("release_00252D90", RELEASE), ("hard_reset_00252DE0", HARD)):
    C.reset(latch=1)
    w(C.WORD, "<I", 7)
    ok, _ = C.call(fn)
    clr[nm] = {"returned": ok, "stop": C.stop.get("at"), "faults": (S.st["bad"] or S.st["faults"])[:2],
               "latch_after": r(C.LATCH, "<I")[0], "word_after": r(C.WORD, "<I")[0]}
res["clears"] = clr
cases["L4_release_and_hard_reset_clear_latch_and_word"] = all(v["latch_after"] == 0 and v["word_after"] == 0 for v in clr.values())

# ---- R-5: the drain ----
d = {
    "base": drain(),
    "word5": drain(word=5),
    "word3": drain(word=3),
    "pending0": drain(pending=0),
    "slot_38": drain(slot={"38": 1}),
    "slot_3E_01": drain(slot={"3E": 0x01}),
    "slot_3E_80": drain(slot={"3E": 0x80}),
    "id7_transition_running": drain(trans=True),
    "id12_transition_running": drain(mid=12, trans=True),
    "mslot0_inactive": drain(ms=(0x00, 0x00)),
    "mslot0_busy_11": drain(ms=(0x01, 0x01)),
    "mslot0_busy_10bit7": drain(ms=(0x81, 0x00)),
}
for k in ("mslot0_inactive", "mslot0_busy_11", "mslot0_busy_10bit7"):
    mailbox(ms={"mslot0_inactive": (0, 0), "mslot0_busy_11": (1, 1), "mslot0_busy_10bit7": (0x81, 0)}[k])
    C.call(C.DRAIN)
    d[k]["mailbox_after"] = list(r(PEND, "<BBxxII"))
res["drain"] = d
routed = lambda k: d[k]["router"][:1] == [[d[k]["router"][0][0], "22"]] if d[k]["router"] else False
cases["D0_drain_dispatches_the_pending_request_to_the_router"] = d["base"]["router"][:1] == [[7, "22"]]
cases["DW_request_word_must_be_0_or_5"] = d["word5"]["router"][:1] == [[7, "22"]] and d["word3"]["router"] == []
cases["DP_no_pending_no_dispatch"] = d["pending0"]["router"] == []
cases["DS_slot_guard_is_38_or_3E_bit0"] = d["slot_38"]["router"] == [] and d["slot_3E_01"]["router"] == [] \
    and d["slot_3E_80"]["router"][:1] == [[7, "22"]]
cases["DT_transition_clause_never_blocks_here"] = d["id7_transition_running"]["router"][:1] == [[7, "22"]] \
    and d["id12_transition_running"]["router"][:1] == [[12, "22"]] and bytes(uc.mem_read(0x53DD10, 6)) == bytes.fromhex("b801000000c3")

cases["DM_manager_slot0_not_ready_discards_the_request"] = all(d[k]["router"] == [] and d[k]["mailbox_after"] == [0, 0, 0, 0]
    for k in ("mslot0_inactive", "mslot0_busy_11", "mslot0_busy_10bit7"))
out = {"ok": all(cases.values()), "cases": cases, "allowed_functions": len(W.ALLOWED), **res}
json.dump(out, open(os.path.join(HERE, "r45_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-58s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
print(json.dumps(clr))
for k, v in d.items():
    print(k, v)
