"""S-21 I4 on the numeric path (OPUS, 2026-09-26): "a pure numeric result has no outer-tail FED0 call"
(CONTRACT-apply-result-to-target.md I4) - executed with the whole applier 003112F0 and its real callees over block 332's world
(check.py, imported: its cases run first, unchanged), with block 332's display boundary LIFTED so the numeric write runs to the
applier's end.

Harness change, disclosed: block 332 stops every numeric write at the damage display 002B4090 (check.on_display). For this file
that hook is neutralised and 002B4090's static closure joins ALLOWED, so the display body runs as shipped over the world's
idle battle-text object. No application stub.
Evidence class: NATIVE-REPLAY (unicorn), live_game false.
Cases (caller flags 0x10, arg5 0):
 N1  target HP only (A bit 8, value 40): the setter 00300530 runs, the display runs, the applier returns - and the outer
     recompute 0030FED0 at 00311AC5 is NOT called.
 N2  target MP only (A bit 14): the same, through 00300CE0.
 C   control, same world: a status result (+0x54 bit 5) DOES reach the outer recompute (block 332's I1/I3 shape).
Not executed: a source-HP numeric result, whose display reaches the text interpreter and the font (S-37's not-covered).
Writes i4_numeric_result.json.
"""
import json
import os

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
C.on_display.__code__ = (lambda u, a, n, _: None).__code__
C.W.ALLOWED |= C.W.closure(C.DISPLAY) | {C.DISPLAY}
C.uc.ctl_flush_tb()


def run(A=0, status_bit=None):
    C.reset()
    C.w(C.TGT + 0x48, "<i", 500)
    C.w(C.TGT + 0x24, "<i", 1000)
    C.w(C.TGT + 0x4C, "<h", 100)
    C.w(C.TGT + 0x28, "<h", 300)
    if A:
        C.w(C.REC + 0x2C, "<I", A)
        C.w(C.REC + 0x24, "<i", 40)
    if status_bit is not None:
        C.w(C.REC + 0x54, "<I", 1 << status_bit)
    ok = C.apply()
    return {"ok": ok, "halt": (C.S.st["bad"] or C.S.st["faults"])[:2],
            "setters": {k: len(C.ev.get(k, [])) for k in ("target_hp", "target_mp", "source_hp", "source_mp")},
            "status_calls": len(C.ev.get("status", [])), "outer_recompute": C.ev.get("outer_recompute", []),
            "hp": C.r(C.TGT + 0x48, "<i")[0], "mp": C.r(C.TGT + 0x4C, "<h")[0]}


n1, n2, c = run(A=1 << 8), run(A=1 << 14), run(status_bit=5)
cases = {
    "N1_target_hp_numeric_no_outer_recompute": n1["ok"] and n1["setters"]["target_hp"] == 1 and n1["outer_recompute"] == [],
    "N2_target_mp_numeric_no_outer_recompute": n2["ok"] and n2["setters"]["target_mp"] == 1 and n2["outer_recompute"] == [],
    "C_status_result_reaches_the_outer_recompute": c["ok"] and c["status_calls"] >= 1 and len(c["outer_recompute"]) == 1,
}
res = {"ok": all(cases.values()), "cases": cases, "target_hp": n1, "target_mp": n2, "status_control": c}
json.dump(res, open(os.path.join(HERE, "i4_numeric_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-48s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", json.dumps(res)[:1200])
