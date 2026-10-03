"""S-25: CONTRACT-gambit-walk.md executed as shipped code - the walk 00305CC0 with its REAL evaluator 003014C0 (EXP-095 scripted it
and ret-stubbed the commit and the slot resolver) (OPUS, 2026-09-26).

Runs over block 332's world (s21-opus-replay-applier-stub-free/check.py, loaded under its own module name; its cases run first,
unchanged): the image, the IAT traps with memset bridged by name, the shipped battle_pack bindings and the unit pool. No
application stub. ALLOWED += the static closure of 00305CC0 (which includes the evaluator's and the commit's).
The evaluator is kept on the path section 4a documents: with bit 5 of the battle state word [02089340] ("combat AI suspended")
set, AiOrder_EvaluateAndResolveActionTarget returns 0 at 00301511 before doing anything - so every order is offered to the real
evaluator, nothing is committed, and the walk's own logic is what is measured. Planted data only: a gambit set (count bytes at
+0.., orders of 24 bytes from +0x20) and the unit.
Signature, read from the prologue: 00305CC0(rcx = unit, rdx = set, r8d = subgroup index, r9d = flag); flag 0 here.
Cases:
 G1  section 4: for subgroups 0, 1, 2 and 4 of a set with counts [2, 3, 1, 0, 4, 5] the evaluator is offered orders starting at
     set + 0x20 + (sum of the preceding counts) * 24, one per count, each 24 bytes on (the two-accumulator loop and the odd
     leftover both exercised).
 G2  an empty subgroup (3) offers nothing and returns 0; a null set returns 0.
 G3  the count byte is RE-READ every iteration: a disclosed perturbation rewrites set[4] at the evaluator's entry - 4 -> 2 on the
     second offer stops the walk after 2; set[1] 3 -> 5 on the first offer makes it offer 5.
 G4  section 4a: with bit 5 set the evaluator returns 0 and the commit 0030F760 is never reached - but NOT "before doing
     anything": ahead of the bit-5 test at 00301511 it zeroes *param (003014ED), decodes the order through 00308EC0 and stores
     the action id into *out (00301500); 00308EC0 and the cookie check are the only functions entered below it.
Writes result.json next to this file.
"""
import importlib.util
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RDX, UC_X86_REG_RAX

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("block332", os.path.normpath(os.path.join(HERE, "..", "s21-opus-replay-applier-stub-free", "check.py")))
C = importlib.util.module_from_spec(spec)
_cwd = os.getcwd()
os.chdir(os.path.dirname(spec.origin))
import sys
sys.path.insert(0, os.path.dirname(spec.origin))
spec.loader.exec_module(C)
os.chdir(_cwd)
W, S, uc = C.W, C.S, C.uc
WALK, EVAL, COMMIT = 0x305CC0, 0x3014C0, 0x30F760
W.ALLOWED |= W.closure(WALK) | {WALK}
SET, UNIT = 0x77100000, C.POOL
uc.mem_map(SET, 0x1000)
FS = set(int(l.split("\t")[0], 16) for l in open(os.path.join(W.GRAPH, "functions.tsv"), encoding="utf-8", errors="replace")
         if l[:1] in "0123456789ABCDEF")
offers, entered, perturb = [], [], {}


def on_eval(u, a, n, _):
    offers.append(u.reg_read(UC_X86_REG_RDX) - SET)
    p = perturb.get(len(offers))
    if p:
        u.mem_write(SET + p[0], bytes([p[1]]))


uc.hook_add(UC_HOOK_CODE, on_eval, begin=EVAL, end=EVAL)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: entered.append(a) if a in FS else None)
uc.ctl_flush_tb()
COUNTS = [2, 3, 1, 0, 4, 5]


def walk(k, counts=COUNTS, pert=None, set_ptr=SET):
    C.reset()
    uc.mem_write(SET, bytes(0x1000))
    uc.mem_write(SET, bytes(counts))
    uc.mem_write(0x2089340, bytes([0x20]))                # bit 5: combat AI suspended
    del offers[:], entered[:]
    perturb.clear()
    perturb.update(pert or {})
    ok = S.call(WALK, UNIT, set_ptr, k, 0)
    return {"ok": ok, "halt": (S.st["bad"] or S.st["faults"])[:2], "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF,
            "offers": list(offers), "commit_entered": COMMIT in entered,
            "entered_below_eval": sorted({"%08X" % a for a in entered if a not in (WALK, EVAL)})}


def want(k, n=None):
    first = 0x20 + sum(COUNTS[:k]) * 24
    return [first + 24 * i for i in range(COUNTS[k] if n is None else n)]


res, cases = {}, {}
g1 = {k: walk(k) for k in (0, 1, 2, 4)}
res["G1"] = g1
cases["G1_first_order_is_the_prefix_sum_and_one_offer_per_count"] = all(g1[k]["ok"] and g1[k]["offers"] == want(k) and g1[k]["ret"] == 0 for k in g1)
g2 = {"empty_subgroup_3": walk(3), "null_set": walk(0, set_ptr=0)}
res["G2"] = g2
cases["G2_empty_subgroup_and_null_set_offer_nothing"] = all(v["ok"] and v["offers"] == [] and v["ret"] == 0 for v in g2.values())
g3 = {"shorten_4_to_2": walk(4, pert={2: (4, 2)}), "lengthen_3_to_5": walk(1, pert={1: (1, 5)})}
res["G3"] = g3
cases["G3_count_byte_reread_every_iteration"] = g3["shorten_4_to_2"]["offers"] == want(4, 2) and g3["lengthen_3_to_5"]["offers"] == want(1, 5) \
    and all(v["ok"] for v in g3.values())
cases["G4_bit5_evaluator_decodes_the_order_then_returns_no_commit"] = all(not v["commit_entered"] and v["entered_below_eval"] == ["00308EC0", "00808C40"]
                                                                        for v in g1.values())
out = {"ok": all(cases.values()), "cases": cases, **res}
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
for k2, v2 in cases.items():
    print("%-62s %s" % (k2, "PASS" if v2 else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED", json.dumps({k: {kk: [vv["ok"], vv["halt"], vv["offers"], vv["entered_below_eval"][:5]] for kk, vv in v.items()} for k, v in res.items()})[:1500])


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
