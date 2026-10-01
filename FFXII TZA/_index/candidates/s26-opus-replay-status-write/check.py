"""S-26 (OPUS, 2026-09-26): CONTRACT-status-write section 4's five invariants executed with NO stubbed callee.

S-26's runtime cell: "CONTRACT-status-write's five invariants rest on EXP-086's stubbed run" (EXP-086 ret-stubbed fourteen callees:
0031B860, 0030B9B0, 0030B8E0, 00377C20, 003112F0, 00300FC0, 00312280, 00301140, 003299B0, 00300140, 00307D10, 003284D0, 0030FED0,
0046A800). This harness runs BattleStats_ChangeStatusAndProcessSideEffects 0030E360 over block 348's world
(../s32-opus-replay-level-advance/check.py, imported: its own cases run first, unchanged), with the static closure of 0030E360
allowed and NO application stub: every callee EXP-086 stubbed runs as shipped when reached. The status definition table is the
shipped battle_pack's (bound by shipped code in that world).
Signature (EXP-086, measured): rcx target, rdx source, r8b status, r9d paramA, [rsp+0x28] paramB, [rsp+0x30] flags, [rsp+0x38] mode.
Fixtures: the target is battle-state row 0 (block 348's record), zeroed per case with the named words planted; no owning unit and
no source unless stated. Instruments: the entry set per call (world.py records every function entered), the entries of 0030E360
itself with their (status, mode) and stack depth, and the heap imports / operator new 00210EC0.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import contextlib
import io
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, "..", "s32-opus-replay-level-advance"))
sys.path.insert(0, D)
cwd = os.getcwd(); os.chdir(D)
with contextlib.redirect_stdout(io.StringIO()):
    import check as C
os.chdir(cwd)
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_R8, UC_X86_REG_RIP

W, uc, S = C.W, C.uc, C.S
SW = 0x30E360
W.ALLOWED |= W.closure(SW) | {SW}
REC = C.REC
EXP086_STUBBED = {0x31B860: "0031B860", 0x30B9B0: "0030B9B0", 0x30B8E0: "0030B8E0", 0x377C20: "00377C20", 0x3112F0: "003112F0",
                  0x300FC0: "00300FC0", 0x312280: "00312280", 0x301140: "00301140", 0x3299B0: "003299B0", 0x300140: "00300140",
                  0x307D10: "00307D10", 0x3284D0: "003284D0", 0x30FED0: "0030FED0", 0x46A800: "0046A800"}
SIDE = {0x3284D0: "reaction 003284D0", 0x3299B0: "event 003299B0", 0x300FC0: "defeat cleanup 00300FC0", 0x312280: "rewards 00312280",
        0x301140: "recover 00301140", 0x30FED0: "recompute 0030FED0", 0x46A800: "extra 0046A800", 0x300140: "case-4 action 00300140",
        0x307D10: "case-4 secondary 00307D10", 0x3112F0: "applier 003112F0"}
entries = []


def on_sw(u, a, n, _):
    rsp = u.reg_read(UC_X86_REG_RSP)
    mode = struct.unpack("<Q", bytes(u.mem_read(rsp + 0x38, 8)))[0] & 0xFFFFFFFF
    entries.append({"status": u.reg_read(UC_X86_REG_R8) & 0xFF, "mode": mode, "rsp": rsp})


uc.hook_add(UC_HOOK_CODE, on_sw, begin=SW, end=SW)
new_calls = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: new_calls.append(1), begin=0x210EC0, end=0x210EC0)
uc.ctl_flush_tb()
WORDS = (0x38, 0x3C, 0x64)


def state():
    return {"%X" % o: struct.unpack("<I", bytes(uc.mem_read(REC + o, 4)))[0] for o in WORDS} | {
        "BC": bytes(uc.mem_read(REC + 0xBC, 128)).hex(), "13C": bytes(uc.mem_read(REC + 0x13C, 64)).hex()}


def run(status, mode, words=None, flags=0x200, pa=1, pb=2):
    uc.mem_write(REC, bytes(0x1C8))
    for o, v in (words or {}).items():
        uc.mem_write(REC + o, struct.pack("<I", v))
    before = state()
    entries.clear(); new_calls.clear()
    S.st["entered"] = set()
    imp0 = dict(S.st["imports"])
    ok = S.call(SW, REC, 0, status, pa & 0xFFFFFFFFFFFFFFFF, stack=(pb & 0xFFFFFFFFFFFFFFFF, flags, mode))
    after = state()
    ent = set(S.st["entered"])
    heap = {k: S.st["imports"][k] - imp0.get(k, 0) for k in ("malloc", "_aligned_malloc") if S.st["imports"][k] - imp0.get(k, 0)}
    top = entries[0]["rsp"] if entries else 0
    return {"ok": ok, "rip": "%08X" % uc.reg_read(UC_X86_REG_RIP), "bad": list(S.st["bad"])[:2], "faults": list(S.st["faults"])[:2],
            "before": {k: before[k] for k in ("38", "3C", "64")}, "after": {k: after[k] for k in ("38", "3C", "64")},
            "params_changed": before["BC"] != after["BC"] or before["13C"] != after["13C"],
            "side_effects": sorted(v for k, v in SIDE.items() if k in ent),
            "exp086_stubbed_entered": sorted(v for k, v in EXP086_STUBBED.items() if k in ent),
            "sw_entries": [{"status": e["status"], "mode": e["mode"], "depth": (top - e["rsp"]) // 8} for e in entries],
            "heap": heap, "operator_new": len(new_calls)}


res = {"live_game": False, "block348_result_md5_unchanged": None}
cases, detail = {}, {}
B = lambda s: 1 << s
# ---- I1: presence is (+0x3C | +0x64); +0x38 is not part of it ----
i1a = run(4, 5)                                    # mode 5 writes +0x38 on an absent status
i1b = run(4, 3, {0x3C: B(4)})                      # add into +0x64 while +0x3C already holds it
i1c = run(4, 4, {0x64: B(4)})                      # add into +0x3C while +0x64 already holds it
ctl = run(4, 4)                                    # control: presence changes -> side effects run (no recompute: flags 0x200)
ctl0 = run(4, 4, flags=0)                          # the same with the recompute: it rebuilds +0x24..+0x47, which includes +0x3C
detail.update(I1a_mode5_plus38=i1a, I1b_add64_while_3C=i1b, I1c_add3C_while_64=i1c, control_presence_changes=ctl,
              control_with_recompute=ctl0)
cases["I1_mode5_sets_+38_and_fires_nothing"] = i1a["ok"] and i1a["after"]["38"] == B(4) and not i1a["side_effects"] and len(i1a["sw_entries"]) == 1
cases["I1_I2_bit_written_into_the_other_word_fires_nothing"] = all(x["ok"] and not x["side_effects"] and len(x["sw_entries"]) == 1 for x in (i1b, i1c)) \
    and i1b["after"]["64"] == B(4) and i1c["after"]["3C"] == B(4)
cases["control_presence_change_fires_side_effects_with_real_callees"] = ctl["ok"] and bool(ctl["side_effects"]) and ctl["after"]["3C"] == B(4)
cases["I1_addendum_the_real_recompute_rewrites_+3C_after_the_add"] = ctl0["ok"] and "recompute 0030FED0" in ctl0["side_effects"] \
    and ctl0["after"]["3C"] != B(4)
# ---- I3: every mode refuses when the bit is already in the requested state ----
ALREADY = {0: {}, 1: {}, 2: {}, 3: {0x64: B(4)}, 4: {0x3C: B(4)}, 5: {0x38: B(4)}}   # clears on absent; adds on present
i3 = {m: run(4, m, ALREADY[m], flags=0) for m in range(6)}
detail["I3"] = i3
cases["I3_every_mode_refuses_when_already_in_the_requested_state"] = all(
    x["ok"] and x["before"] == x["after"] and not x["params_changed"] and not x["side_effects"] and len(x["sw_entries"]) == 1 for x in i3.values())
# ---- I4: the cascade is a set of mode-0 clears, each refused when absent: depth at most one level ----
c10 = run(10, 4, {0x64: B(25)})
c10a = run(10, 4)
c20 = run(20, 4, {0x64: B(15)})
ko = run(0, 4, flags=0)
detail.update(I4_status10_with_bit25=c10, I4_status10_absent=c10a, I4_status20_with_bit15=c20, I4_KO_add=ko)
def inner(x):
    return x["sw_entries"][1:]
cases["I4_cascade_calls_are_mode_0_and_one_level_deep"] = all(x["ok"] and inner(x) and all(e["mode"] == 0 for e in inner(x))
    and len({e["depth"] for e in inner(x)}) == 1 for x in (c10, c10a, c20, ko))
cases["I4_present_bit_cleared_absent_bit_refused"] = c10["after"]["64"] == 0 and [e["status"] for e in inner(c10)] == [25] \
    and [e["status"] for e in inner(c10a)] == [25] and c10a["after"]["64"] == 0 and c10a["after"]["3C"] == B(10) \
    and c20["after"]["64"] == 0 and [e["status"] for e in inner(c20)] == [15]
# ---- I5: never allocates ----
allx = [i1a, i1b, i1c, ctl, ctl0, c10, c10a, c20, ko] + list(i3.values())
cases["I5_no_heap_import_and_no_operator_new_in_any_case"] = all(not x["heap"] and x["operator_new"] == 0 for x in allx)
# ---- the callees EXP-086 stubbed: which ran real ----
ran = sorted(set().union(*[set(x["exp086_stubbed_entered"]) for x in allx]))
res["exp086_stubbed_callees_run_real"] = ran
cases["no_fence_no_fault_in_any_case"] = all(x["ok"] and not x["bad"] and not x["faults"] for x in allx)
res["cases"], res["detail"] = cases, detail
res["ok"] = all(cases.values())
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print("EXP-086-stubbed callees that ran real:", ran)
print("KO cascade:", len(inner(ko)), "inner mode-0 calls; control side effects:", ctl["side_effects"])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
