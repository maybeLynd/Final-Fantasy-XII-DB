"""S-32 LU-6 and LU-5's second shape (OPUS, 2026-09-26), over block 348's harness (check.py, imported: its own cases run first,
unchanged).

LU-6: 'The null test guards the FIRST resolve; the pointer actually used comes from the SECOND, untested ... If the second resolve
ever returned null where the first did not, ebp would be stride x id - not a null pointer but a small wild address, which LU-5's
four reads would then dereference past.' LU-5: 'The record resolve has TWO failure shapes' - shape 1 (slot null) is lu5.py's;
shape 2 is the first resolve 0020E600 returning null.
Section 14 asks whether the two resolves can disagree. 0020E600 is three instructions (mov eax, ecx / add rax, [01F83530] / ret)
and is executed here: the trace records every instruction and memory write between the two calls.

Fixtures (all disclosed, each restored after its run; everything else is block 348's shipped, bound world):
  D0 (every run, control included)  the record's character byte +0x04 is set to 3 at 0030C650's entry (advance() plants 0,
             for which stride x id is 0 and the wild address would coincide with null);
  D1 (LU-6)  at the second call site 0030C706 - after the first resolve's null test passed - the base global [01F83530] is set to
             2^64 - key and restored at that call's return 0030C70B, so ONLY the second call returns 0;
  D2 (LU-5 shape 2)  the same, scoped to the first call (set at 0030C6F2, restored at 0030C6F7), so the FIRST call returns 0;
  D3 (observation)  the base global is raised by 2^32 before the run.
Evidence class: NATIVE-REPLAY (unicorn), live_game false; no application stub. Faults are observables. Writes lu6_result.json.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RBP, UC_X86_REG_RCX, UC_X86_REG_RIP, UC_X86_REG_RSP

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc, S = C.uc, C.S
SLOT, BASE = 0x2EBF130, 0x1F83530
M64 = (1 << 64) - 1
T = {"calls": [], "rbp": None, "writes": [], "window": False, "branch_6FA": None, "trace": [], "rsp": None}
PERT = {"site": None, "value": None}
ID = 3
# the two call sites of 0020E600 in 0030C650: call -> return address
SITES = {0x30C6F2: 0x30C6F7, 0x30C706: 0x30C70B}


def code(u, a, n, _):
    if a == 0x30C650:
        u.mem_write(C.REC + 4, bytes([ID]))
    if a in SITES:
        T["calls"].append({"site": "%08X" % a, "ecx": u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, "ret": None})
        if PERT["site"] == a:
            u.mem_write(BASE, struct.pack("<Q", PERT["value"]))
    elif a in SITES.values() and T["calls"] and T["calls"][-1]["ret"] is None:
        T["calls"][-1]["ret"] = u.reg_read(UC_X86_REG_RAX)
        if PERT["site"] is not None and SITES[PERT["site"]] == a:
            u.mem_write(BASE, struct.pack("<Q", base0))
    if a == 0x30C6F2:
        T["window"], T["rsp"] = True, u.reg_read(UC_X86_REG_RSP)
    elif a == 0x30C70B:
        T["window"] = False
    elif a == 0x30C6FC:
        T["branch_6FA"] = "fallthrough"
    elif a == 0x30C721 and T["branch_6FA"] is None and len(T["calls"]) == 1:
        T["branch_6FA"] = "taken (je 0030C721)"
    elif a == 0x30C723:
        T["rbp"] = u.reg_read(UC_X86_REG_RBP)
    if T["window"]:
        T["trace"].append(a)


def mw(u, acc, a, size, v, _):
    if T["window"]:
        T["writes"].append({"addr": "%X" % a, "size": size, "call_push": a == T["rsp"] - 8 and size == 8})


h1 = uc.hook_add(UC_HOOK_CODE, code)
h2 = uc.hook_add(UC_HOOK_MEM_WRITE, mw)
uc.ctl_flush_tb()
base0 = C.r(BASE, "<Q")[0]
slotp = C.r(SLOT, "<Q")[0]
key = C.r(slotp + 0xC, "<I")[0]
stride = C.r(slotp + 8, "<H")[0]


def run(pre_base=None, site=None, value=None):
    for k in ("calls", "writes", "trace"):
        T[k] = []
    T.update(rbp=None, window=False, branch_6FA=None)
    PERT.update(site=site, value=value)
    if pre_base is not None:
        C.w(BASE, "<Q", pre_base)
    out = C.advance(10, 11, flags=C.QUIET, seed=4537)
    rip = uc.reg_read(UC_X86_REG_RIP)
    faults = list(S.st["faults"])
    C.w(BASE, "<Q", base0)
    rec = {**out, "rip_at_stop": "%08X" % rip, "faults": faults, "calls": [{"site": c["site"], "ecx": "%X" % c["ecx"], "ret": "%X" % (c["ret"] or 0)} for c in T["calls"]],
           "rbp_at_0030C723": None if T["rbp"] is None else "%X" % T["rbp"], "branch_at_0030C6FA": T["branch_6FA"],
           "writes_between_calls": T["writes"], "instructions_between_calls": ["%08X" % a for a in T["trace"]]}
    return rec, rip, faults


ctrl, _, _ = run()
d1, rip1, f1 = run(site=0x30C706, value=(-key) & M64)
d2, rip2, f2 = run(site=0x30C6F2, value=(-key) & M64)
d3, rip3, f3 = run(pre_base=(base0 + (1 << 32)) & M64)
after, _, _ = run()
idrow = ID
ret0 = (key + base0) & M64
exp_rbp = (stride * idrow + ret0) & 0xFFFFFFFF
wild = (stride * idrow) & 0xFFFFFFFF

cases = {
    "control_two_calls_same_key_same_value": len(ctrl["calls"]) == 2 and ctrl["calls"][0]["ecx"] == ctrl["calls"][1]["ecx"]
        and ctrl["calls"][0]["ret"] == ctrl["calls"][1]["ret"] and ctrl["calls"][0]["ecx"] == "%X" % key and ctrl["calls"][0]["ret"] == "%X" % ret0,
    "control_only_the_two_call_pushes_write_across_both_resolves": all(x["call_push"] for x in ctrl["writes_between_calls"])
        and len(ctrl["writes_between_calls"]) == 2,
    "control_used_pointer_is_stride_x_id_plus_second_value_32bit": ctrl["rbp_at_0030C723"] == "%X" % exp_rbp,
    "control_reaches_floats_and_level_store": ctrl["returned"] and ctrl["counts"]["float"] == 4 and ctrl["level"] == 11,
    "LU6_second_resolve_null_first_not_passes_the_guard": d1["branch_at_0030C6FA"] == "fallthrough" and len(d1["calls"]) == 2
        and d1["calls"][0]["ret"] == "%X" % ret0 and d1["calls"][1]["ret"] == "0",
    "LU6_used_pointer_is_the_small_wild_address_stride_x_id": d1["rbp_at_0030C723"] == "%X" % wild,
    "LU6_HP_MP_stored_then_fault_at_0030C757_past_the_wild_address": not d1["returned"] and rip1 == 0x30C757
        and f1[:1] == ["%08X" % (wild + 0x1F)] and (d1["hp"], d1["mp"]) == (ctrl["hp"], ctrl["mp"]) and d1["counts"]["float"] == 0,
    "LU5_shape2_first_resolve_null_takes_0030C6FA": d2["branch_at_0030C6FA"] == "taken (je 0030C721)" and len(d2["calls"]) == 1
        and d2["calls"][0]["ret"] == "0" and d2["rbp_at_0030C723"] == "0",
    "LU5_shape2_HP_MP_stored_then_fault_on_0x1F": not d2["returned"] and rip2 == 0x30C757 and f2[:1] == ["0000001F"]
        and (d2["hp"], d2["mp"]) == (ctrl["hp"], ctrl["mp"]) and d2["counts"]["float"] == 0 and d2["level"] == 10,
    "restored_run_matches_control": (after["hp"], after["mp"], after["floats"], after["level"]) == (ctrl["hp"], ctrl["mp"], ctrl["floats"], ctrl["level"]),
}
obs = {"D3_base_plus_4GiB": {"returned": d3["returned"], "rip_at_stop": d3["rip_at_stop"], "faults": d3["faults"][:2], "calls": d3["calls"],
                             "rbp_at_0030C723": d3["rbp_at_0030C723"], "floats": d3["floats"], "level": d3["level"],
                             "same_as_control": (d3["hp"], d3["mp"], d3["floats"], d3["level"]) == (ctrl["hp"], ctrl["mp"], ctrl["floats"], ctrl["level"])}}
res = {"ok": all(cases.values()), "cases": cases, "world": {"base": "%X" % base0, "slot": "%X" % slotp, "key": "%X" % key, "stride": stride, "id": idrow},
       "control": ctrl, "D1_lu6": d1, "D2_lu5_shape2": d2, "observation": obs, "restored": after}
json.dump(res, open(os.path.join(HERE, "lu6_result.json"), "w"), indent=1, sort_keys=True, default=str)
print("world", res["world"])
for k, v in cases.items():
    print("%-66s %s" % (k, "PASS" if v else "FAIL"))
print("D3", json.dumps(obs["D3_base_plus_4GiB"]))
print("ALL PASS" if res["ok"] else "FAILED")
