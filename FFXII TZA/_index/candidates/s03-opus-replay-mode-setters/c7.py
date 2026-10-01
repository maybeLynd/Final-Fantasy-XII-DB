"""S-03 section 7 (OPUS, 2026-09-26): the chocobo setter's disable arm with the special-sequence bit set, executed over
block 348's world (check.py, imported: its ten cases run first, unchanged) - the arm AUDIT-SEM's review of request 368 names
open: `if (state[0x5AE0] & 2) { if (actor3) thunk_FUN_002EB030(actor3, 0x2001); toggle bit 1 }`.

Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub. The call graph has no tail-jump edges, so the
shipped targets reached by `jmp` join ALLOWED: 00263750 (from the roster getter thunk 0031ABF0) and 002EB030 (from 00329A10).
Planted data: roster slot 3 (the table 0209A1F0 read by 00263750) points at a unit block.
Cases (flags word = 2 before each disable):
 A  5AE0 bit 1 set, slot 3 filled: 002E73C0(actor3, 3), then 00329A10 -> 002EB030(actor3, 0x2001); 5AE0 bit 1 cleared, its
    other bits kept; 5AEC = 0; flags bit 1 cleared.
 B  5AE0 bit 1 set, slot 3 empty: no 002EB030, 5AE0 bit 1 still cleared (the toggle is outside the actor test).
 C  5AE0 bit 1 clear: no 002EB030 and 5AE0 unchanged.
 D  the 5AE0 test uses the value read before the roster calls (00303E03), not after: a disclosed perturbation rewrites 5AE0
    to 0xC (bit 1 clear) at 00303E28, between that read and the test at 00303E2F - the post still happens, and the toggle,
    an XOR on the CURRENT word (00303E55..00303E71), then sets bit 1 (0xC -> 0xE).
Writes c7_result.json.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX

import check as C
import probe as P

HERE = os.path.dirname(os.path.abspath(__file__))
uc, STATE, w, r = P.uc, P.STATE, P.w, P.r
ROSTER, EVT, TOUCH = 0x209A1F0, 0x2EB030, 0x2E73C0
P.W.ALLOWED |= P.W.closure(0x263750) | {0x263750} | P.W.closure(EVT) | {EVT}
UNIT = 0x76800000
uc.mem_map(UNIT, 0x10000)
calls = []
for a, nm in ((EVT, "002EB030"), (TOUCH, "002E73C0"), (0x329A10, "00329A10")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: calls.append([nm, "%X" % u.reg_read(UC_X86_REG_RCX), "%X" % (u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)]),
                begin=a, end=a)
uc.ctl_flush_tb()


def disable(seq, actor, change_during=None):
    uc.mem_write(UNIT, bytes(0x10000))
    w(STATE + 0x5B04, "<I", 2)
    w(STATE + 0x5AE0, "<Q", seq)
    w(STATE + 0x5AEC, "<I", 0x77)
    saved = r(ROSTER, "<4Q")
    w(ROSTER, "<4Q", 0, 0, 0, actor)
    del calls[:]
    hk = None
    if change_during is not None:           # D: rewrite 5AE0 between the read at 00303E03 and the test at 00303E2F
        hk = uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: u.mem_write(STATE + 0x5AE0, struct.pack("<I", change_during)),
                         begin=0x303E28, end=0x303E28)
        uc.ctl_flush_tb()
    ok = P.S.call(P.SET1, 0)
    if hk is not None:
        uc.hook_del(hk)
        uc.ctl_flush_tb()
    out = {"returned": ok, "stopped_at": (P.S.st["bad"] or P.S.st["faults"])[:2], "calls": list(calls),
           "flags": r(STATE + 0x5B04, "<I")[0], "5AE0": "%X" % r(STATE + 0x5AE0, "<I")[0], "5AEC": r(STATE + 0x5AEC, "<I")[0]}
    w(ROSTER, "<4Q", *saved)
    return out


a = disable(0xE, UNIT)
b = disable(0xE, 0)
c = disable(0xC, UNIT)
d = disable(0xE, UNIT, change_during=0xC)
names = lambda x: [k[0] for k in x["calls"]]
cases = {
    "A_bit1_set_actor3_posts_2001_and_clears_bit1": a["returned"] and names(a) == ["002E73C0", "00329A10", "002EB030"]
        and a["calls"][0][1:] == ["%X" % UNIT, "3"] and a["calls"][2][1:] == ["%X" % UNIT, "2001"]
        and a["5AE0"] == "C" and a["5AEC"] == 0 and a["flags"] == 0,
    "B_bit1_set_no_actor3_no_post_bit1_still_cleared": b["returned"] and "002EB030" not in names(b) and b["5AE0"] == "C" and b["5AEC"] == 0,
    "C_bit1_clear_no_post_5AE0_unchanged": c["returned"] and "002EB030" not in names(c) and c["5AE0"] == "C" and c["5AEC"] == 0,
    "D_test_uses_the_value_read_before_the_roster_calls": d["returned"] and "002EB030" in names(d) and d["5AE0"] == "E",
}
res = {"ok": all(cases.values()), "cases": cases, "A": a, "B": b, "C": c, "D": d}
json.dump(res, open(os.path.join(HERE, "c7_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-56s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", json.dumps([a, b, c, d])[:1500])
