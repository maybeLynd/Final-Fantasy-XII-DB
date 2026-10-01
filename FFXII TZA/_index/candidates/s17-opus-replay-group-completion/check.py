"""S-17 (OPUS, 2026-09-26): CONTRACT-group-completion-and-respawn's invariants executed with the completion's callees REAL - the
three event locks and the dispatch EXP-011 stubbed - over units installed by the shipped installer.

World: block 345's (s25-opus-replay-enmity/check.py, imported; its cases run first, unchanged): two foes installed by 0023A570
from a shipped area file - spawn-backed (stats kind 1), each with its own spawn list at +0x40. Registration goes through the
verb's own native target 00239710(actor, mode, group) (verb 0x3030's tail), which sets the unit's group byte +0xE98 and calls
00306E60. The only planted field is each unit handle's +0x30 back-pointer (ActorWork_GetBattleUnitRaw 00263E30), as in
s25-opus-replay-gambit-walk's commit_walk.py. The group ledger is the image's BSS at 02EC13C0 (0x18 per group, 1-based).
No application stub.
Cases:
 G1  registration: two foes into group 1 set memberMask bits 0 and 1; deadMask stays 0.
 G2  a death is recorded (deadMask |= bit) and completes nothing while another member lives (returns 0).
 G3  a death is idempotent: the same member dying again changes nothing.
 G4  completion is the mask test: the last member's death returns 1, and the completion runs its callees for real -
     00307140(1), 00238B70(1), 00238AE0(1) (the event locks; 02089340 gains bits 0x20 and 0x80) and the dispatch 003299B0(unit,
     0x2005) - and the ledger flag +0x10 bit 0 rises.
 G5  a unit outside memberMask cannot complete the group: with F1 unregistered (00306E60(F1, 0)), F1's death leaves the group
     incomplete; F0's then completes it.
 G6  registration clears the member's dead bit and there is no one-shot: after a completion, re-registering F0 makes the group
     incomplete; F0 dying again completes it a second time.
 G7  the group id is 1-based: 00239710(actor, mode, 0) registers nothing and a group-0 unit's death touches no ledger.
 G8  the reset 00307090 zeroes both masks and clears flag bit 0 only (flags 0xFF -> 0xFE) for every group. (Each scenario above
     also starts with that reset, as an area entry does, so no ledger state carries between them.)
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import contextlib
import io
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "s25-opus-replay-enmity"))
sys.path.insert(0, BASE)
cwd = os.getcwd(); os.chdir(BASE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as E                                     # block 345 (its cases run first, unchanged)
os.chdir(cwd)
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX

W, uc, S, w, r = E.W, E.uc, E.S, E.w, E.r
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
REG, DEATH, RESET, SETG = 0x306E60, 0x306F00, 0x307090, 0x239710
for f in (REG, DEATH, RESET, SETG):
    W.ALLOWED |= W.closure(f) | {f}
ev = []
for a, nm in ((0x307140, "lock_00307140"), (0x238B70, "lock_00238B70"), (0x238AE0, "lock_00238AE0"), (0x3299B0, "dispatch_003299B0")):
    uc.hook_add(UC_HOOK_CODE, (lambda nm: lambda u, a, n, _: ev.append([nm, "%X" % u.reg_read(UC_X86_REG_RCX), "%X" % (u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)]))(nm),
                begin=a, end=a)
uc.ctl_flush_tb()
LEDGER = 0x2EC13C0


def ledger(g):
    b = bytes(uc.mem_read(LEDGER + (g - 1) * 0x18, 0x18))
    return {"member": struct.unpack_from("<Q", b, 0)[0], "dead": struct.unpack_from("<Q", b, 8)[0], "flags": b[0x10]}


def fresh():
    E.world()
    f0, f1 = E.unit(0), E.unit(1)
    for u in (f0, f1):
        w(q(u + 0x10) + 0x30, "<Q", u)
    uc.mem_write(0x2089340, bytes(4))
    S.call(RESET)                                          # each scenario starts as an area entry does: the ledger reset first
    return f0, f1


def setgroup(u, g):
    return S.call(SETG, q(u + 0x10), 1, g)


def death(u):
    del ev[:]
    ok = S.call(DEATH, u)
    return {"ok": ok, "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFF, "halt": (S.st["bad"] or S.st["faults"])[:1], "events": list(ev), "ledger": ledger(1),
            "state_340": "%X" % struct.unpack("<I", bytes(uc.mem_read(0x2089340, 4)))[0]}


R = {}
F0, F1 = fresh()
R["G1"] = {"ok": setgroup(F0, 1) and setgroup(F1, 1), "e98": [uc.mem_read(F0 + 0xE98, 1)[0], uc.mem_read(F1 + 0xE98, 1)[0]], "ledger": ledger(1)}
R["G2"] = death(F0)
R["G3"] = death(F0)
R["G4"] = death(F1)
F0, F1 = fresh()
setgroup(F0, 1); setgroup(F1, 1)
S.call(REG, F1, 0)
g5_after_unreg = ledger(1)
g5a = death(F1)
g5b = death(F0)
R["G5"] = {"after_unregister": g5_after_unreg, "outsider_death": g5a, "member_death": g5b}
F0, F1 = fresh()
setgroup(F0, 1); setgroup(F1, 1)
death(F0); first = death(F1)
S.call(REG, F0, 1)
g6_reg = ledger(1)
g6 = death(F0)
R["G6"] = {"first_completion": first["ret"], "after_reregister": g6_reg, "second_completion": g6}
F0, F1 = fresh()
before0 = [ledger(g) for g in range(1, 6)]
ok7 = S.call(SETG, q(F1 + 0x10), 1, 0)
g7_e98 = uc.mem_read(F1 + 0xE98, 1)[0]
g7d = death(F1)
R["G7"] = {"setgroup0_ok": ok7, "e98": g7_e98, "ledgers_unchanged": [ledger(g) for g in range(1, 6)] == before0, "death": g7d}
for g in range(1, 65):
    uc.mem_write(LEDGER + (g - 1) * 0x18, struct.pack("<QQB", 0x5, 0x3, 0xFF))
ok8 = S.call(RESET)
after8 = [ledger(g) for g in range(1, 65)]
R["G8"] = {"ok": ok8, "all_masks_zero": all(x["member"] == 0 and x["dead"] == 0 for x in after8), "flags": sorted({x["flags"] for x in after8})}
L = lambda x: x["ledger"]
cases = {
    "G1_registration_sets_member_bits": R["G1"]["ok"] and R["G1"]["e98"] == [1, 1] and R["G1"]["ledger"]["member"] == 3 and R["G1"]["ledger"]["dead"] == 0,
    "G2_death_recorded_no_completion_while_a_member_lives": R["G2"]["ok"] and R["G2"]["ret"] == 0 and L(R["G2"])["dead"] == 1 and R["G2"]["events"] == [],
    "G3_death_is_idempotent": R["G3"]["ok"] and R["G3"]["ret"] == 0 and L(R["G3"]) == L(R["G2"]) and R["G3"]["events"] == [],
    "G4_last_death_completes_with_real_locks_and_dispatch": R["G4"]["ok"] and R["G4"]["ret"] == 1 and L(R["G4"])["dead"] == 3 and L(R["G4"])["flags"] & 1 == 1
        and [e[0] for e in R["G4"]["events"]] == ["lock_00307140", "lock_00238B70", "lock_00238AE0", "dispatch_003299B0"]
        and all(e[1] == "1" for e in R["G4"]["events"][:3]) and R["G4"]["events"][3][2] == "2005"
        and int(R["G4"]["state_340"], 16) & 0xA0 == 0xA0,
    "G5_outsider_death_cannot_complete": g5_after_unreg["member"] == 1 and g5a["ret"] == 0 and g5b["ret"] == 1,
    "G6_reregistration_clears_dead_bit_no_one_shot": first["ret"] == 1 and g6_reg["member"] == 3 and g6_reg["dead"] == 2 and g6["ret"] == 1,
    "G7_group_zero_registers_nothing": ok7 and g7_e98 == 0 and R["G7"]["ledgers_unchanged"] and g7d["ret"] == 0,
    "G8_reset_zeroes_masks_clears_flag_bit0_only": ok8 and R["G8"]["all_masks_zero"] and R["G8"]["flags"] == [0xFE],
}
res = {"live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-60s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({k: R[k] for k in ("G1", "G4", "G5", "G6", "G7", "G8")}, default=str)[:1800])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
