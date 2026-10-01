"""S-20 (OPUS, 2026-09-26): the resolved-target continuation of a fresh commit executed - the relation classifier 0030AB40 and the
group propagation walk (CONTRACT-commit-action "The propagation", 0030F8C5..0030F931), stub-free.

S-20's runtime cell names one remaining item: "the resolved-target continuation 0030AB40". This script loads cb26.py (which loads
check.py, which loads block 332's world: all their cases run first, unchanged), plants cb26's resolving target (handle 1 << 20 ->
unit 1) and runs the commit 0030F760 with that target. No application stub.
Planted data per case (disclosed): both units' byte +0 bit 0x10 (the classifier's eligibility bit, 0030ABA6/0030ABAF); the target's
stats kind byte +5 (0 = the actor's side, 1 = the other side); the actor's status word +0x3C bit 5; the units' group dword +0x24 and
the actor's +0x08; a unit's status mask bits (+0x3C & 0x80000003).
The classifier, read whole (0030AB40..0030AC48): 0 if either unit is null, either class 00263C20(+0x10) is 5, or either lacks bit
0x10; else 1 + (bit5(actor status) == same_side), with same_side decided by the two stats kind bytes (and class 3) - so 2 for an
opposite-side pair with the actor unconfused, or a same-side pair with the actor confused. The commit walks only when it is > 1.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes resolved_result.json.
"""
import contextlib
import importlib.util
import io
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
cwd = os.getcwd(); os.chdir(HERE)
spec = importlib.util.spec_from_file_location("cb26mod", os.path.join(HERE, "cb26.py"))
K = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(K)
os.chdir(cwd)
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_R8, UC_X86_REG_RIP

T, C, W, S, uc, w, r, U, U1 = K.T, K.C, K.W, K.S, K.uc, K.w, K.r, K.U, K.U1
rels, pw = [], []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: rels.append(u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF), begin=0x30F8CA, end=0x30F8CA)
for base in (U, U1):
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _, b=base: pw.append(("U" if b == U else "U1", "+%X" % (a - b), "%X" % v,
                "%08X" % u.reg_read(UC_X86_REG_RIP))), begin=base + 0x750, end=base + 0x757)
uc.ctl_flush_tb()
TGT = 1 << 20


def case(target_side=1, confused=False, grp=(0, 0), actor_handle=0, u1_mask=0):
    K.plant()
    w(U, "<B", r(U, "<B") | 0x10); w(U1, "<B", r(U1, "<B") | 0x10)
    sa, st = r(U + 0x698, "<Q"), r(U1 + 0x698, "<Q")
    w(sa + 5, "<B", 0); w(st + 5, "<B", target_side)
    w(sa + 0x3C, "<I", 0x20 if confused else 0); w(sa + 0x64, "<I", 0)
    w(st + 0x3C, "<I", u1_mask); w(st + 0x64, "<I", 0)
    w(U + 0x24, "<I", grp[0]); w(U1 + 0x24, "<I", grp[1]); w(U + 0x08, "<I", actor_handle)
    for b in (U, U1):
        uc.mem_write(b + 0x750, bytes(8))
    del rels[:], pw[:]
    ok = S.call(T.COMMIT, U, 0xABC, 0x10, TGT, stack=(0,))
    return {"ok": ok, "halt": (S.st["bad"] or S.st["faults"])[:2], "relation": rels[:1], "writes": list(pw),
            "U750": "%X" % r(U + 0x750, "<I"), "U754": "%X" % r(U + 0x754, "<I"), "U1_754": "%X" % r(U1 + 0x754, "<I")}


R = {
    "opposite_side": case(),
    "same_side_unconfused": case(target_side=0),
    "same_side_confused": case(target_side=0, confused=True),
    "u1_other_group": case(grp=(0, 7)),
    "actor_handle_not_its_group": case(actor_handle=5),
    "u1_status_masked": case(u1_mask=0x1),
}
wr = lambda x: sorted({(a, b) for a, b, c, d in x["writes"]})
cases = {
    "R1_relation_2_walks_the_group_writes_754_then_750": R["opposite_side"]["relation"] == [2] and wr(R["opposite_side"]) == [("U", "+750"), ("U", "+754"), ("U1", "+754")]
        and R["opposite_side"]["U750"] == "%X" % TGT and R["opposite_side"]["U1_754"] == "%X" % TGT,
    "R2_relation_1_skips_the_whole_walk": R["same_side_unconfused"]["relation"] == [1] and R["same_side_unconfused"]["writes"] == [],
    "R3_confused_actor_on_same_side_is_relation_2": R["same_side_confused"]["relation"] == [2] and ("U1", "+754") in wr(R["same_side_confused"]),
    "R4_only_the_actors_group_is_written": R["u1_other_group"]["relation"] == [2] and ("U1", "+754") not in wr(R["u1_other_group"])
        and ("U", "+750") in wr(R["u1_other_group"]),
    "R5_actor_handle_not_equal_group_skips_the_walk_after_the_first_store": R["actor_handle_not_its_group"]["relation"] == [2]
        and ("U1", "+754") not in wr(R["actor_handle_not_its_group"]) and ("U", "+754") in wr(R["actor_handle_not_its_group"]),
    "R6_status_masked_unit_skipped": R["u1_status_masked"]["relation"] == [2] and ("U1", "+754") not in wr(R["u1_status_masked"]),
    "no_fault": all(x["ok"] and not x["halt"] for x in R.values()),
}
res = {"live_game": False, "runs": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "resolved_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print({k: (v["relation"], wr(v)) for k, v in R.items()})
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
