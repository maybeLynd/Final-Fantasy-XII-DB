"""S-15 (OPUS, 2026-09-26): the field runtime pass 0025D9E0 executed over real actor records with no scripted callee.

S-15's runtime cell rests on EXP-106, which scripted the interpreter 0025E4C0, audio 00261F90, the deferred request 0032FC30, the
init core's external chain, the lifecycle helpers, the slot-0 post-chain, the wait predicates and arm checkers (block 299's exposure
note maps them: none reaches an S-15 invariant). This harness runs the pass with its whole static closure allowed and NO application
stub, over the world of the S-13 stub-free closer (../s13-opus-replay-record-pool-stub-free/check.py, executed first, its eleven
cases unchanged): manager slot 0 at 02098E10 holds five REAL records built by 002679F0 / 00266530 with all callees real.
Fixtures (planted data, disclosed):
  - slot 0's record-table pointer +0x08 = the pool block (its caller 0026CE60 keeps it there), and the slot flag bytes per case;
  - slot 1 (02098E10 + 0x288) is a copy of slot 0's block (same records) - the drive loop is reached for slots other than 0
    directly (0025DAC7 test r14d, r14d / jne 0025DB22); for slot 0 it is gated on the global predicate 00377DB0;
  - the party-focus cell 022C7FE0 (read by 003590D0) per case;
  - one disclosed PERTURBATION, the control for I1/I2 only: record 0's +0x14 low nibble set, which the shipped image never does.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import contextlib
import io
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
D13 = os.path.normpath(os.path.join(HERE, "..", "s13-opus-replay-record-pool-stub-free"))
ns = {"__file__": os.path.join(D13, "check.py"), "__name__": "s13_world"}
# 2026-09-29 (OPUS; migration A04, OPUS-NOTICE-ORACLE-S13-RESULT-REWRITE): S-13 writes its result to S13_RESULT, joined
# onto its own folder. Running it here used to rewrite S-13's cited result.json; an absolute path in THIS folder keeps
# S-13's published result untouched. Only the output location changes.
os.environ["S13_RESULT"] = os.path.join(HERE, "s13_world_result.json")
cwd = os.getcwd(); os.chdir(D13)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(open(os.path.join(D13, "check.py"), encoding="utf-8").read(), "s13_check", "exec"), ns)
except SystemExit:
    pass
os.chdir(cwd)
assert ns["res"]["ok"], "the S-13 world's own cases must pass first"
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RDX

W, uc, S = ns["W"], ns["uc"], ns["S"]
PASS, WRES, INIT, FOCUSCELL = 0x25D9E0, 0x25DF00, 0x2620E0, 0x22C7FE0
W.ALLOWED |= W.closure(PASS) | {PASS}
SLOT0, block, recs = ns["SLOT"], ns["block"], ns["recs"]
SLOT1 = SLOT0 + 0x288
uc.mem_write(SLOT0 + 8, struct.pack("<Q", block))
BASE = bytes(uc.mem_read(SLOT0, 0x288))
drives = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: drives.append(u.reg_read(UC_X86_REG_RDX)), begin=WRES, end=WRES)
uc.ctl_flush_tb()
EXP106_SCRIPTED = set(int(x, 16) for x in (
    "0025E4C0 00261F90 0032FC30 00259B30 003E8980 0025ACA0 0017D490 0026FAD0 00379860 00379290 003DE920 00363B40 003601C0 0025B600 "
    "0025B740 0025B820 0025C170 0025B250 0025E400 0026A5F0 00233AA0 00263660 00250960 00259FB0 00268690 003B7130 002E1C40 00254A90 "
    "00234150 002EFD20 002F1A30 00183070 002677B0 002EFA70 003EAA70 0017E7D0 001ED180 001ED130 001EDE80 001EC5C0 001EC5E0 003DBF60 "
    "003DB2A0 002674B0 00267420 002E6310 002681E0 002E5030 002E5750 003E6EF0 003E68B0 003E6A70 0026D6F0").split())


def rb(a):
    return uc.mem_read(a, 1)[0]


def rd(a, f="<I"):
    return struct.unpack(f, bytes(uc.mem_read(a, struct.calcsize(f))))[0]


def run(slot, focus=0, count=20000000, **flags):
    sb = SLOT0 + slot * 0x288
    uc.mem_write(sb, BASE)
    for k, v in flags.items():
        uc.mem_write(sb + int(k[1:], 16), bytes([v]))
    uc.mem_write(FOCUSCELL, struct.pack("<I", focus))
    uc.mem_write(0x2099D70, bytes(16))
    drives.clear(); S.st["entered"] = set(); S.count = count
    ok = S.call(PASS, slot)
    ent = set(S.st["entered"])
    return {"ok": ok, "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, "bad": list(S.st["bad"])[:2], "faults": list(S.st["faults"])[:2],
            "drives": len(drives), "driven": sorted({"%X" % r for r in drives}), "b10": rb(sb + 0x10), "b11": rb(sb + 0x11),
            "b12": rb(sb + 0x12), "d24": rd(sb + 0x24), "d38": rd(sb + 0x38), "pub70": "%X" % rd(0x2099D70, "<Q"),
            "pub78": "%X" % rd(0x2099D78, "<Q"), "init_core": INIT in ent, "functions": len(ent),
            "exp106_scripted_run_real": sorted("%08X" % a for a in EXP106_SCRIPTED if a in ent)}


cases, detail = {}, {}
# ---- postconditions: the fold path (slot 0, +0x10 < 0x80) and the drive path (slot 1, +0x10 >= 0x80) ----
fold = run(0, b10=0x01, b13=1)
drv = run(1, b10=0x81, b13=1, b12=1)
detail.update(fold_slot0=fold, drive_slot1=drv)
cases["P_fold_every_actor_driven_counters_up_publish_current"] = fold["ok"] and fold["drives"] == len(recs) and set(fold["driven"]) == {"%X" % r for r in recs} \
    and fold["d24"] == 1 and fold["d38"] == 1 and fold["pub70"] == "%X" % SLOT0 and (fold["b11"] & 1) == (fold["b10"] >> 7)
cases["P_drive_counters_up_publish_current_bit0_equals_bit7"] = drv["ok"] and drv["d24"] == 1 and drv["d38"] == 1 and drv["pub70"] == "%X" % SLOT1 \
    and (drv["b11"] & 1) == (drv["b10"] >> 7) == 1
# ---- I1: the shipped nibble is clear -> the drive repeats zero times (exit B: no +0x12 publish, no init core) ----
drv3 = run(1, b10=0x81, b13=1, b12=3)
detail["drive_b12_3"] = drv3
cases["I1_drive_loop_runs_once_repeat_zero_times_exit_B"] = all(x["ok"] and x["drives"] == 1 and not x["init_core"] for x in (drv, drv3)) \
    and drv3["b12"] == 3
# ---- I1 control / I2: the nibble set (disclosed perturbation) -> the loop repeats and nothing in it stops it ----
r0 = recs[0]
b14 = rb(r0 + 0x14)
uc.mem_write(r0 + 0x14, bytes([(b14 & 0xB0) | 1]))
per = run(1, count=3000000, b10=0x81, b13=1, b12=1)
b14_after = rb(r0 + 0x14)
uc.mem_write(r0 + 0x14, bytes([b14]))
detail["control_nibble_set"] = dict(per, b14_after="%X" % b14_after)
cases["I2_control_nibble_set_repeats_without_bound_until_the_replay_budget"] = (not per["ok"]) and not per["bad"] and not per["faults"] \
    and per["drives"] >= 1000 and (b14_after & 0x0F) == 1 and not (b14_after & 0x40)
# ---- I3: 02099D78 null two ways, indistinguishable; positive control ----
gen = rd(recs[0] + 0x16, "<H")
h_ok = (gen << 20) | (0 << 16) | 0
h_stale = (((gen + 1) & 0x7FF) << 20) | (0 << 16) | 0
nof = run(1, focus=0, b10=0x81, b13=1, b12=1)
stale = run(1, focus=h_stale, b10=0x81, b13=1, b12=1)
good = run(1, focus=h_ok, b10=0x81, b13=1, b12=1)
detail.update(I3_no_focus=nof, I3_stale_handle=stale, I3_valid_handle=good, I3_handles={"valid": "%X" % h_ok, "stale": "%X" % h_stale, "record_gen": gen})
strip = lambda x: {k: v for k, v in x.items() if k not in ("functions", "exp106_scripted_run_real")}
cases["I3_no_focus_and_unresolved_handle_both_publish_null_indistinguishably"] = nof["pub78"] == "0" and stale["pub78"] == "0" \
    and strip(nof) == strip(stale)
cases["I3_control_valid_handle_publishes_the_record"] = good["pub78"] == "%X" % recs[0]
# ---- I4: early arms report success (1) while driving nothing ----
arms = {"+0x17 bit4": run(1, b10=0x81, b13=1, b12=1, b17=0x10), "+0x11 bit2": run(1, b10=0x81, b13=1, b12=1, b11=4),
        "slot 0, +0x10>=0x80, 00377DB0 false": run(0, b10=0x81, b13=1, b12=1), "+0x10 bit0 clear": run(1, b10=0x80, b13=1, b12=1)}
detail["I4_arms"] = arms
cases["I4_success_reported_with_no_actor_driven"] = all(a["ok"] and a["ret"] == 1 and a["drives"] == 0 for a in arms.values())
allx = [fold, drv, drv3, nof, stale, good] + list(arms.values())
cases["no_fence_no_fault"] = all(x["ok"] and not x["bad"] and not x["faults"] for x in allx)
res = {"live_game": False, "cases": cases, "detail": detail,
       "exp106_scripted_run_real": sorted(set().union(*[set(x["exp106_scripted_run_real"]) for x in allx + [per]]))}
res["ok"] = all(cases.values())
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-80s %s" % (k, "PASS" if v else "FAIL"))
print("EXP-106-scripted callees that ran real:", res["exp106_scripted_run_real"])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
