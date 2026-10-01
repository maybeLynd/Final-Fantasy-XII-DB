"""S-12 P-1 / P-2 (OPUS, 2026-09-26): the weather init core 002620E0 executed in its three arms over block 339's world (check.py,
imported: its cases run first, unchanged), with its callees real - where EXP-106 ran 002620E0 itself but scripted its external
chain (the roll 0025ACA0, the notifications 003601C0 and the rest).

P-1 - runs only from the primary manager, once per field setup: returns at once unless dword[mgr+0x28] == 0 (002620E6); skips its
      body when byte[mgr+0x10] & 4 is set (002620F3); sets that bit itself (002621A4).
P-2 - the latch does not skip everything: with the bit set, 002621A8 still runs 003601C0(0x0B) and tail-jumps 003601C0(0x0C).
Harness change, disclosed: block 339 stops every run at the apply 0026D910 (its recorded boundary, check.on_apply). For this file
that hook is neutralised, so the roll's tail jump runs the apply as shipped, over the SHIPPED map_ref.bin / gramap_weatherinfo.bin
published the way block 303 publishes them ([02099D88], guard [02099D90] = 1, [02ADD0B0]; payload +0x1044 = field 464).
Anything else the fresh arm reaches is reported, not substituted.
Evidence class: NATIVE-REPLAY (unicorn), live_game false; no application stub. Writes p12_result.json.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RIP

import check as C
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
uc, S = C.uc, C.S
C.on_apply.__code__ = (lambda u, a, n, _: None).__code__
INIT = 0x2620E0
PRESENT = 0x40AAD0
W.ALLOWED |= W.closure(INIT) | {INIT} | W.closure(C.APPLY) | {C.APPLY}
if os.environ.get("P12_PRESENT_BOUNDARY", "1") == "1":
    W.ALLOWED.discard(PRESENT)
MAPREF = r"D:\FFXII_TZA_extract\ps2data\image\ff12\in\common\map_ref.bin"
MWEATHER = r"D:\FFXII_TZA_extract\ps2data\image\ff12\in\common\gramap_weatherinfo.bin"
mrf, mwt = open(MAPREF, "rb").read(), open(MWEATHER, "rb").read()
TAB = 0x76500000
uc.mem_map(TAB, 0x100000)
MRF, MWT = TAB, TAB + ((len(mrf) + 0xFFF) & ~0xFFF)
uc.mem_write(MRF, mrf)
uc.mem_write(MWT, mwt)
MGR = 0x76400000
uc.mem_map(MGR, 0x10000)
ev = []
for a, nm in ((0x3601C0, "notify 003601C0"), (0x25ACA0, "roll 0025ACA0"), (C.APPLY, "apply 0026D910"), (0x2621A4, "set bit 002621A4"),
              (0x2621A8, "latched tail 002621A8"), (PRESENT, "presentation 0040AAD0")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev.append([nm, u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF]), begin=a, end=a)
uc.ctl_flush_tb()


def arm(f28, b10):
    uc.mem_write(MGR, bytes(0x1000))
    C.w(MGR + 0x28, "<I", f28)
    C.w(MGR + 0x10, "<B", b10)
    C.setup(0, (0, 100, 0))
    for cell, val in ((0x2099D88, MRF), (0x2099D90, 1), (0x2ADD0B0, MWT)):
        C.w(cell, "<Q", val)
    C.w(C.PAY + 0x1044, "<i", 464)
    ev.clear()
    ok = S.call(INIT, MGR)
    return {"returned": ok, "stopped_at": (S.st["bad"] or S.st["faults"])[:2], "rip": "%X" % uc.reg_read(UC_X86_REG_RIP),
            "b10_after": uc.mem_read(MGR + 0x10, 1)[0], "events": list(ev)}


np = arm(1, 0)
la = arm(0, 4)
fr = arm(0, 0)
names = lambda r: [e[0] for e in r["events"]]
cases = {
    "P1_non_primary_returns_at_once": np["returned"] and np["events"] == [] and np["b10_after"] == 0,
    "P1_latched_skips_the_body": la["returned"] and "roll 0025ACA0" not in names(la) and la["b10_after"] == 4,
    "P2_latched_still_notifies_0B_then_0C": la["events"][:1] == [["latched tail 002621A8", la["events"][0][1]]]
        and [e for e in la["events"] if e[0] == "notify 003601C0"] == [["notify 003601C0", 0xB], ["notify 003601C0", 0xC]],
    "P1_fresh_runs_the_body_roll_then_apply": names(fr)[:2] == ["roll 0025ACA0", "apply 0026D910"],
}
fresh_completed = fr["returned"] and "set bit 002621A4" in names(fr)
if fresh_completed:
    cases["P1_fresh_sets_the_bit_itself_and_notifies"] = (fr["b10_after"] & 4) == 4 and \
        [e for e in fr["events"] if e[0] == "notify 003601C0"] == [["notify 003601C0", 0xB], ["notify 003601C0", 0xC]]
res = {"ok": all(cases.values()), "cases": cases, "fresh_completed": fresh_completed, "non_primary": np, "latched": la, "fresh": fr,
       "presentation_boundary": os.environ.get("P12_PRESENT_BOUNDARY", "1") == "1"}
json.dump(res, open(os.path.join(HERE, "p12_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-56s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", "fresh completed:", fresh_completed, "stop:", fr["stopped_at"], fr["rip"])
