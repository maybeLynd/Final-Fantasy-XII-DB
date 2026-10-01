"""S-21 I4 on the SOURCE numeric paths, executed to the applier's end (OPUS, 2026-09-26): "numeric ... branches do not set that outer
flag. A pure numeric result has no outer-tail FED0 call" (CONTRACT-apply-result-to-target I4), for the source HP and source MP arms.

Imports check.py (block 332; its cases run first, unchanged) and lifts the display boundary 002B4090 exactly as i4_numeric.py does
(disclosed: check.on_display neutralised, the display's closure allowed). No application stub; no font and no graphics object are
needed on these paths. The source arms read their own record fields (00311700..0031177B, read from the image):
  source HP (A bit 7): value dword [rec + 0x20] (0031172F), setter r12 = 00300530, or 00300520 when A bit 1 (00311732);
  source MP (A bit 13): value word [rec + 0x28] (0031174F), setter r15 = 00300CE0, or 00300C90 when A bit 2 (00311771).
Cases:
 S1  source HP +40 (A bit 7): 00300530 is called with the source's stats record, the source's HP goes 500 -> 540, the display runs,
     the applier returns, and the outer recompute site 00311AC5 is never reached.
 S2  source MP +30 (A bit 13): 00300CE0 is called with the source's record, the source's MP goes 100 -> 130, the applier returns, no
     outer recompute.
 S3  the target is untouched by both.
 C   control, same world: a status result (+0x54 bit 5) reaches the outer recompute once.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes i4_source_result.json.
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
    for rec in (C.SRC, C.TGT):
        C.w(rec + 0x48, "<i", 500)
        C.w(rec + 0x24, "<i", 1000)
        C.w(rec + 0x4C, "<h", 100)
        C.w(rec + 0x28, "<h", 300)
    if A:
        C.w(C.REC + 0x2C, "<I", A)
        C.w(C.REC + 0x20, "<i", 40)
        C.w(C.REC + 0x28, "<h", 30)
    if status_bit is not None:
        C.w(C.REC + 0x54, "<I", 1 << status_bit)
    ok = C.apply()
    rd = lambda rec: {"hp": C.r(rec + 0x48, "<i")[0], "mp": C.r(rec + 0x4C, "<h")[0]}
    return {"ok": ok, "halt": (C.S.st["bad"] or C.S.st["faults"])[:2],
            "setters": {k: [["%X" % x for x in c[:2]] for c in C.ev.get(k, [])] for k in ("target_hp", "target_mp", "source_hp", "source_mp")},
            "status_calls": len(C.ev.get("status", [])), "outer_recompute": C.ev.get("outer_recompute", []),
            "source": rd(C.SRC), "target": rd(C.TGT)}


s1, s2, c = run(A=1 << 7), run(A=1 << 13), run(status_bit=5)
untouched = {"hp": 500, "mp": 100}
cases = {
    "S1_source_hp_numeric_runs_to_the_end_no_outer_recompute": s1["ok"] and s1["setters"]["source_hp"] == [["300530", "%X" % C.SRC]]
        and s1["source"]["hp"] == 540 and s1["outer_recompute"] == [],
    "S2_source_mp_numeric_runs_to_the_end_no_outer_recompute": s2["ok"] and s2["setters"]["source_mp"] == [["300CE0", "%X" % C.SRC]]
        and s2["source"]["mp"] == 130 and s2["outer_recompute"] == [],
    "S3_the_target_is_untouched": s1["target"] == untouched and s2["target"] == untouched and not s1["setters"]["target_hp"] and not s2["setters"]["target_mp"],
    "C_status_result_reaches_the_outer_recompute": c["ok"] and c["status_calls"] >= 1 and len(c["outer_recompute"]) == 1,
}
res = {"ok": all(cases.values()), "cases": cases, "source_hp": s1, "source_mp": s2, "status_control": c}
json.dump(res, open(os.path.join(HERE, "i4_source_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-60s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", json.dumps({"S1": s1, "S2": s2})[:1500])
