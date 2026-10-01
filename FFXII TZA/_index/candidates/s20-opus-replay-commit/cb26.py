"""S-20 CB-2 / CB-6 (OPUS, 2026-09-26): the combo continuation 0030FA00 (CONTRACT-combo-continuation.md) executed with the real gate
0030C010, the real commit 0030F760 and the real cancel 003105D0 inside it, over block 332's world (loaded through check.py next
to this file, under its own module name; block 332's cases and check.py's run first, unchanged).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub. ALLOWED += 0030FA00's closure.
Planted data only, so the gate 0030C010 passes: [01E0C2B8] = 1 (00253B90 then reports 0), the unit's target-buffer entry 0 = a
non-null qword with +0x788 bit 0x400, [022C2160] = 0, and a target handle (1 << 20) that resolves - the leader gate [02089340]
bit 0x10 set, descriptor 0 at 02098E10 (count 1, slot array, flag bit 0, bound 1) pointing at an object whose +0x16 generation is 1
and whose +0x30 is unit 1 (with its stats record). The unit's committed block: context 0xABC, target (1 << 20), action 0x10.
Cases:
 A  success: 0030FA00 calls the commit with the unit's OWN +0x708 / +0x710 / +0x714 and cancel-first 1; the cancel runs inside it
    and clears +0x6B7/+0x6B8 (the word store at 003106EB); the commit succeeds; then the partner byte is written back (0x77),
    the counter becomes old + 1 (2 -> 3), +0x6B4 = 5, return 1.
 F  a failing re-commit (the unit's +0x714 = 0x21F, refused by CM-2): the commit returns 0 AFTER its cancel ran, so 0030FA00
    returns 0 without restoring - measured: counter and partner as the cancel left them.
 G  the gate refuses ([01E0C2B8] = 0, attacker stats flags clear): return 0 before any commit or cancel; counter and partner
    untouched.
Writes cb26_result.json.
"""
import contextlib
import importlib.util
import io
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RAX

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("s20commit", os.path.join(HERE, "check.py"))
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)
C, W, S, uc, w, r = T.C, T.W, T.S, T.uc, T.w, T.r
CONT = 0x30FA00
W.ALLOWED |= W.closure(CONT) | {CONT}
U, U1 = T.UNIT, C.POOL + 0xF50
H = 0x76E00000
try:
    uc.mem_map(H, 0x10000)
except Exception:
    pass
ev = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.append(["commit", "%X" % u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8) & 0xFFFF,
                                                        "%X" % (u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF),
                                                        struct.unpack("<I", bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP) + 0x28, 4)))[0]]),
            begin=T.COMMIT, end=T.COMMIT)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.append(["cancel"]), begin=T.CANCEL, end=T.CANCEL)
bw = []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: bw.append(["%08X" % u.reg_read(UC_X86_REG_RIP), "+%X" % (a - U), n, v]),
            begin=U + 0x6B7, end=U + 0x6B8)
uc.ctl_flush_tb()


def plant(aid=0x10, gate=True):
    T.setup()
    uc.mem_write(H, bytes(0x10000))
    w(0x2089340, "<B", 0x10)
    w(0x1E0C2B8, "<I", 1 if gate else 0)
    w(0x22C2160, "<I", 0)
    arr, obj = H, H + 0x100
    w(arr, "<I", 1)
    w(arr + 8, "<Q", obj)
    w(obj + 0x16, "<H", 1)
    w(obj + 0x30, "<Q", U1)
    w(0x2098E10, "<Q", 1)
    w(0x2098E18, "<Q", arr)
    w(0x2098E20, "<B", r(0x2098E20, "<B") | 1)
    w(0x2098E30, "<I", 1)
    w(U + 0x780, "<Q", 0x1234)
    w(U + 0x788, "<I", 0x400)
    w(U + 0x708, "<Q", 0xABC)
    w(U + 0x710, "<I", 1 << 20)
    w(U + 0x714, "<H", aid)
    w(U + 0x6B4, "<B", 0)
    w(U + 0x6B7, "<BB", 2, 0x77)


def run():
    del ev[:], bw[:]
    ok = S.call(CONT, U)
    return {"ok": ok, "halt": (S.st["bad"] or S.st["faults"])[:2], "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, "events": list(ev),
            "writes_6B7_6B8": list(bw), "counter": r(U + 0x6B7, "<B"), "partner": r(U + 0x6B8, "<B"), "b6B4": r(U + 0x6B4, "<B")}


plant()
a = run()
plant(aid=0x21F)
f = run()
plant(gate=False)
g = run()
commits = [e for e in a["events"] if e[0] == "commit"]
cases = {
    "A_success_recommits_its_own_action_and_advances": a["ok"] and a["ret"] == 1 and commits == [["commit", "ABC", 0x10, "100000", 1]]
        and ["cancel"] in a["events"] and a["counter"] == 3 and a["partner"] == 0x77 and a["b6B4"] == 5
        and any(x[0] == "003106EB" for x in a["writes_6B7_6B8"]),
    "F_failed_recommit_returns_0_after_the_cancel_ran": f["ok"] and f["ret"] == 0 and ["cancel"] in f["events"]
        and any(x[0] == "003106EB" for x in f["writes_6B7_6B8"]) and f["b6B4"] == 0,
    "G_gate_refusal_touches_nothing": g["ok"] and g["ret"] == 0 and g["events"] == [] and g["writes_6B7_6B8"] == [] and g["counter"] == 2
        and g["partner"] == 0x77,
}
res = {"ok": all(cases.values()), "cases": cases, "success": a, "failed_recommit": f, "gate_refused": g,
       "failed_recommit_counter_after": f["counter"], "failed_recommit_partner_after": f["partner"]}
json.dump(res, open(os.path.join(HERE, "cb26_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-54s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", json.dumps({"A": a, "F": f, "G": g}, default=str)[:1800])
