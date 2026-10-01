"""S-41 (OPUS, 2026-09-26): the sound-request path executed with NO scripted callee - the readiness refuser and both dispatchers real.

S-41's runtime exposure (s41-runtime-per-invariant-exposure.md): invariant 2's readiness refuser 002DEE80 was scripted in
EXP-096, and so were the dispatchers 001DBDB0 / 001DBE90 (their entry arguments were the observable). This harness runs EXP-096's
wrapper-level cases over block 355's world (../s29-opus-replay-inventory-rebase/world.py, its real initialisers built) with:
  - the audio object built by its OWN lazy initialiser 00210AF0 (operator new 0x40 + ctor 002105E0; cell 01FD36A0, getter
    00210B30) before the cases - a real initialiser, not a fixture object;
  - EXP-096's planted globals, the same addresses and meanings (its check.py): gate1 02091098, gate2 byte 022CB726, handle cells
    02AEF3FC / 02AEF400 / 02AEF404, the handle table 02AEEDC0 (64 x 24 B: +8 lo16, +0xA hi16), actor-manager slot bytes
    (liveness 02098E20 + slot*0x288, mute +0x1F1);
  - the dispatchers and the readiness test RUN AS SHIPPED; hooks at their entries only record arguments;
  - NO application stub. The allowed set is the static closures of the entries used plus the audio initialiser's.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import importlib.util
import json
import os
import struct
import sys

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9

HERE = os.path.dirname(os.path.abspath(__file__))
WD = os.path.join(HERE, "..", "s29-opus-replay-inventory-rebase")
sys.path.insert(0, WD)
spec = importlib.util.spec_from_file_location("world355", os.path.join(WD, "world.py"))
W = importlib.util.module_from_spec(spec)
spec.loader.exec_module(W)
FX = json.load(open(os.path.join(WD, "world.json")))

W_C60, W_CA0, W_1500, W_A1A0 = 0x249C60, 0x249CA0, 0x271500, 0x24A1A0
RES_A, PLAY, READY, DISP, DISPB, AUDIO_INIT = 0x3A1180, 0x2DF220, 0x2DEE80, 0x1DBDB0, 0x1DBE90, 0x210AF0
for f in (W_C60, W_CA0, W_1500, W_A1A0, RES_A, PLAY, READY, AUDIO_INIT, 0x1DBCE0):
    W.ALLOWED |= W.closure(f) | {f}
W.ALLOWED |= {0x16D6A0}
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
G1, G2B, SLOTS, HDLA, HDLGB, HDLB, TBL = 0x02091098, 0x022CB726, 0x02098E20, 0x02AEF3FC, 0x02AEF400, 0x02AEF404, 0x02AEEDC0
log = {"disp": [], "dispb": [], "ready": []}


def grab(key):
    def h(u, a, n, _):
        log[key].append(tuple(u.reg_read(r) & 0xFFFFFFFF for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9)))
    return h


uc.hook_add(UC_HOOK_CODE, grab("disp"), begin=DISP, end=DISP)
uc.hook_add(UC_HOOK_CODE, grab("dispb"), begin=DISPB, end=DISPB)
uc.hook_add(UC_HOOK_CODE, grab("ready"), begin=READY, end=READY)
uc.ctl_flush_tb()
okA = S.call(AUDIO_INIT)
AUDIO = struct.unpack("<Q", bytes(uc.mem_read(0x01FD36A0, 8)))[0]


def mk_handle(hi, slot, flag31=0):
    return ((hi << 16) | slot | (flag31 << 31)) & 0xFFFFFFFF


def w(a, f, v):
    uc.mem_write(a, struct.pack(f, v))


def run(entry, rcx, g1=0, g2=0, hdlA=0xFFFFFFFF, hdlGB=0xFFFFFFFF, hdlB=0xFFFFFFFF, tbl=(), live=None, mute=None, rax_in=0x0BADF00D):
    w(G1, "<I", g1); w(G2B, "<B", g2)
    w(HDLA, "<I", hdlA); w(HDLGB, "<I", hdlGB); w(HDLB, "<I", hdlB)
    uc.mem_write(TBL, bytes(64 * 24))
    for slot, lo, hi in tbl:
        w(TBL + slot * 24 + 8, "<H", lo); w(TBL + slot * 24 + 0xA, "<H", hi)
    w(SLOTS, "<B", 0 if live is None else live)
    w(SLOTS + 0x1F1, "<B", 0 if mute is None else mute)
    for k in log:
        log[k].clear()
    S.st["entered"] = set()
    uc.reg_write(UC_X86_REG_RAX, rax_in)
    ok = S.call(entry, rcx)
    return {"ok": ok, "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, "bad": list(S.st["bad"])[:2], "faults": list(S.st["faults"])[:2],
            "disp": ["(%X, %X, %X, %X)" % a for a in log["disp"]], "dispb": ["(%X, %X, %X, %X)" % a for a in log["dispb"]],
            "ready": ["%X" % a[0] for a in log["ready"]], "functions": len(S.st["entered"])}


GOOD_A = dict(hdlA=mk_handle(7, 3), tbl=[(3, 3, 7)], live=0x01)
res = {"live_game": False, "audio_init": {"ok": okA, "object": "%X" % AUDIO}}
c = {
    "w_c60_ok": run(W_C60, 5, **GOOD_A),
    "w_ca0_ok": run(W_CA0, 5, **GOOD_A),
    "w_1500_gate1_set": run(W_1500, 5, g1=1, **GOOD_A),
    "w_c60_gate1_set": run(W_C60, 5, g1=1, **GOOD_A),
    "w_ca0_gate1_set": run(W_CA0, 5, g1=1, **GOOD_A),
    "w_a1a0_gate1_set": run(W_A1A0, 5, g1=1),
    "w_a1a0_gate1_set_sentinel2": run(W_A1A0, 5, g1=1, rax_in=0x5A5A5A5A),
    "w_c60_resolver_refuses": run(W_C60, 5, live=0x01),                         # handle -1
    "w_c60_liveness_refuses": run(W_C60, 5, hdlA=mk_handle(7, 3), tbl=[(3, 3, 7)], live=0x00),
    "w_c60_gate2_set": run(W_C60, 5, g2=1, **GOOD_A),
    "w_a1a0_ready_path": run(W_A1A0, 5),
    "ready_ecx0": run(READY, 0),
    "ready_ecx5": run(READY, 5),
    "w_c60_other_index": run(W_C60, 0x1FF, **GOOD_A),
}
res["runs"] = c
cases = {}
cases["audio_object_built_by_its_own_initialiser"] = okA and AUDIO != 0
ok_all = all(x["ok"] and not x["bad"] and not x["faults"] for x in c.values())
cases["no_fence_no_fault_in_any_run"] = ok_all
# the dispatch arguments (EXP-096's observable) with the dispatcher REAL: (0, id, pan 0x40, vol 0x7F), id = lo<<9 + index
cases["I3_wrappers_dispatch_pan_0x40_vol_0x7F_with_the_dispatcher_real"] = c["w_c60_ok"]["disp"] == ["(0, 605, 40, 7F)"] and c["w_ca0_ok"]["disp"] == ["(0, 605, 40, 7F)"]
cases["I4_bank_owns_a_512_id_block_id_is_lo_shl_9_plus_index"] = c["w_c60_other_index"]["disp"] == ["(0, 7FF, 40, 7F)"]
# I5: gate1 protects the three wrappers, not the path - 00271500 proceeds
cases["I5_gate1_refuses_three_wrappers_not_00271500"] = c["w_c60_gate1_set"]["ret"] == 0xFFFFFFFF and c["w_ca0_gate1_set"]["ret"] == 0xFFFFFFFF \
    and not c["w_c60_gate1_set"]["disp"] and not c["w_a1a0_gate1_set"]["dispb"] and c["w_1500_gate1_set"]["disp"] == ["(0, 605, 40, 7F)"]
# 0024A1A0's gate1 refusal writes no return value: eax comes back as it was on entry (0024A1AF jne 0024A1C8 -> ret)
cases["I2_0024A1A0_gate1_refusal_returns_no_defined_value_eax_passes_through"] = c["w_a1a0_gate1_set"]["ret"] == 0x0BADF00D     and c["w_a1a0_gate1_set_sentinel2"]["ret"] == 0x5A5A5A5A and not c["w_a1a0_gate1_set"]["ready"]
# I2: independent refusers, none says which, and they disagree on what failure looks like
refusals = {k: c[k]["ret"] for k in ("w_c60_gate1_set", "w_c60_resolver_refuses", "w_c60_liveness_refuses", "w_c60_gate2_set", "ready_ecx0", "w_a1a0_ready_path")}
res["refusal_values"] = {k: "%X" % v for k, v in refusals.items()}
cases["I2_refusers_report_only_failure_and_disagree_on_its_value"] = all(not c[k]["disp"] for k in ("w_c60_gate1_set", "w_c60_resolver_refuses",
    "w_c60_liveness_refuses", "w_c60_gate2_set")) and len({refusals["w_c60_gate1_set"], refusals["w_c60_resolver_refuses"],
    refusals["w_c60_liveness_refuses"]}) == 1 and refusals["w_c60_gate2_set"] != refusals["w_c60_gate1_set"] and refusals["ready_ecx0"] == 0
cases["I2_readiness_refuser_002DEE80_runs_real_both_arms"] = c["ready_ecx0"]["ret"] == 0 and c["ready_ecx0"]["functions"] == 1 \
    and c["ready_ecx5"]["ok"] and c["ready_ecx5"]["functions"] > 1
# I1: a receipt does not mean a sound is playing - the real dispatcher returns a receipt with no bank loaded in this world
res["receipts"] = {k: "%X" % c[k]["ret"] for k in ("w_c60_ok", "w_ca0_ok", "w_1500_gate1_set")}
cases["I2_0024A1A0_real_readiness_refuses_before_the_reshape"] = c["w_a1a0_ready_path"]["ret"] == 0 and c["w_a1a0_ready_path"]["ready"] == ["5"]     and not c["w_a1a0_ready_path"]["dispb"]
cases["I1_receipt_returned_with_no_bank_loaded"] = c["w_c60_ok"]["ret"] not in (0, 0xFFFFFFFF) and bool(c["w_c60_ok"]["disp"])
res["cases"] = cases
res["ok"] = all(cases.values())
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print("refusals:", res["refusal_values"], "receipts:", res["receipts"])
print("a1a0 ready path:", c["w_a1a0_ready_path"])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
