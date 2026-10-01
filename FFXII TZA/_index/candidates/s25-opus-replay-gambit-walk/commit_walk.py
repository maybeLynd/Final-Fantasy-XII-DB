"""S-25 (OPUS, 2026-09-26): a gambit walk that COMMITS, with the real evaluator on its bit-5-clear path, the real target-selector
evaluator 00301AD0 and the real commit 0030F760, over an AUTHORED gambit list (CONTRACT-gambit-walk sections 5, 6, 7).

Runs over block 345's world (s25-opus-replay-enmity/check.py, imported: its cases run first, unchanged): foes installed by the
shipped installer 0023A570 from a shipped area file, party units owning battle-state rows, battle_pack bound by shipped code.
The gambit list is authored, not planted: the shipped preset loader GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders
(00327CB0) reads preset 11 (id 0x500B) - "Foe: flying -> Telekinesis; Foe: party leader's target / targeting self / targeting ally
/ nearest visible / any -> Attack" - into party row 0, and the gambit screen's commit GambitConfig_CommitBankAndRebuildRuntimeOrders
(003282D0) banks those 0x34 bytes and rebuilds the runtime set 02089378 + index * 0x170 through 00328140.
The foe's grudge is written by the shipped enmity writer 00321850 (20 -> 30 with the first-grudge boost, CONTRACT-enmity E-6a).
No application stub. Disclosed fixtures and bindings:
 - [02EBF0D8] (the gambit target conditions) bound by 00238880's first call 003845F0(&[02EBF0D8], dir +0x20), as block 332 makes
   00237FC0's first call; 00238880's menu lookup (heap 6) is not built;
 - unit byte +0 bit 4 on the party unit and the foe (the evaluator's gate 0030151A);
 - each unit handle's +0x30 back-pointer (ActorWork_GetBattleUnitRaw 00263E30) and +0xC0 definition, a zeroed object, so
   002E9C00 returns its byte +0x12 = 0; the handles' matrices are zero;
 - the party unit's sighted buffer +0xBC0 = {count 1, the foe's handle}; the perception update that fills it is not run
   (range +0x6D0 = 0.0, so 0030F130 copies it);
 - 00217150, reached by the real code through the thunk 00202D70 (a tail jump the static closure does not follow), is admitted.
Cases:
 W1  the authored set: six records from preset 11, conditions 605A 6000 6004 6005 6001 6002, actions 00AA then 0096 x5.
 W2  first match wins, with real conditions: line 1 (Telekinesis) is refused by BattleAction_CheckActionAvailabilityReason 002FFCF0
     (non-zero reason) before any target selector, and lines 2-6 pass it (0); lines 2-4 reach 00301AD0 and find no target; line 5 ("Foe: nearest visible") finds one, the
     evaluator returns 1 and 0030F760 commits Attack; line 6 is never offered; the walk returns 1.
 W3  the commit's block: +0x708 = the committed record's address (set + 0x20 + 4 * 24), +0x710 = the target, +0x714 = 0x96, and
     the copy at +0x718.
 W4  control: with no grudge, lines 5 and 6 find no target and nothing is committed (walk returns 0) - a party member's "Foe"
     relation takes only a foe holding a positive grudge (0030BD6D..0030BDA7 -> BattleEnmity_HasAnyPositive 00321840).
 W5  section 6, on real committed state: a resume-mode walk (r9 1) over the same set evaluates lines 1-4, then reaches the record
     +0x708 points at and returns 1 WITHOUT evaluating it - no fifth evaluation, no commit.
 W6  section 7's third call: the same unit, resume mode, over party row 1's set (preset 11 banked the same way), with +0x714 set to
     0x4021 first (a disclosed perturbation, so the latched word differs from the action): the stale context never matches, line 5
     commits, and the success tail calls 004697C0([unit + 0x698], 0x96, 0x4021, 4) - its second argument is the ACTION word the
     evaluator decoded ([rsp+0x70], 00305E44), not the target; its third is the word latched from +0x714 at entry. W2's
     normal-mode commit makes no third call.
 Also measured (W2/W3): the walk's 0xFFFF-initialised slot [rsp+0x70] receives the evaluator's decoded action id (00301500) and is
 the commit's r8w; the 0-initialised slot [rsp+0x30] receives the target id (003017E7) and is the commit's r9d.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes commit_walk_result.json.
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
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9

W, uc, S, w, r = E.W, E.uc, E.S, E.w, E.r
WALK, EVAL, COMMIT, LOAD, BANK, NOTIFY = 0x305CC0, 0x3014C0, 0x30F760, 0x327CB0, 0x3282D0, 0x4697C0
W.ALLOWED |= set().union(*(W.closure(f) | {f} for f in (WALK, LOAD, BANK, 0x217150)))
SETS = 0x2089378
ev = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.append(["eval", u.reg_read(UC_X86_REG_RDX)]), begin=EVAL, end=EVAL)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.append(["availability", u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF]), begin=0x301604, end=0x301604)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.append(["selector", u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF]), begin=0x3016AD, end=0x3016AD)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.append(["eval_ret", u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF]), begin=0x305DD7, end=0x305DD7)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.append(["commit", "%X" % (u.reg_read(UC_X86_REG_R8) & 0xFFFF), "%X" % (u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF)]),
            begin=COMMIT, end=COMMIT)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.append(["commit_ret", u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF]), begin=0x305DF9, end=0x305DF9)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.append(["notify", "%X" % u.reg_read(UC_X86_REG_RCX), "%X" % (u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF),
                                                        "%X" % (u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF), u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF]),
            begin=NOTIFY, end=NOTIFY)
uc.ctl_flush_tb()
dir20 = struct.unpack("<i", bytes(uc.mem_read(E.SP.B + 0x20, 4)))[0]
assert S.call(0x3845F0, 0x2EBF0D8, dir20), "00238880's first call"
CFG, DEFS = 0x77200000, 0x77300000
uc.mem_map(CFG, 0x1000)
uc.mem_map(DEFS, 0x1000)
P0, F0 = E.unit(E.NFOE + 0), E.unit(0)


def authored_set(party_row):
    """preset 11 through the shipped loader into the row, then banked and rebuilt by the gambit screen's commit"""
    ok = S.call(LOAD, E.row(party_row), 0x500B)
    uc.mem_write(CFG, bytes(uc.mem_read(E.row(party_row) + 0x88, 0x34)))
    ok = ok and S.call(BANK, party_row, CFG)
    base = SETS + party_row * 0x170
    n = uc.mem_read(base, 1)[0]
    recs = [bytes(uc.mem_read(base + 0x20 + 24 * i, 24)) for i in range(n)]
    return ok, base, recs, bytes(uc.mem_read(CFG, 0x34))


def build(grudge=True):
    E.world()
    sets = [authored_set(0), authored_set(1)]
    for u in (P0, F0):
        uc.mem_write(u, bytes([uc.mem_read(u, 1)[0] | 0x10]))
        h = r(u + 0x10, "<Q")[0]
        w(h + 0x30, "<Q", u)
        w(h + 0xC0, "<Q", DEFS)
    w(P0 + 0xBC0, "<II", 0, 1)
    w(P0 + 0xBC8, "<QQ", r(F0 + 0x10, "<Q")[0], 0)
    uc.mem_write(0x2089340, bytes([uc.mem_read(0x2089340, 1)[0] & 0xDF]))
    g = S.call(0x321850, F0, 0, 20, 0) if grudge else True
    return sets, g, E.tab(0)


def walk(set_base, resume):
    del ev[:]
    ok = S.call(WALK, P0, set_base, 0, resume)
    return {"ok": ok, "halt": (S.st["bad"] or S.st["faults"])[:1], "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF,
            "events": [[e[0], "+%X" % (e[1] - set_base)] if e[0] == "eval" else e for e in ev]}


def block():
    return {"708": "%X" % r(P0 + 0x708, "<Q")[0], "710": "%X" % r(P0 + 0x710, "<I")[0], "714": "%X" % r(P0 + 0x714, "<H")[0],
            "copy_718_equals_700": bytes(uc.mem_read(P0 + 0x718, 0x18)) == bytes(uc.mem_read(P0 + 0x700, 0x18))}


sets, grudge_ok, tab = build()
base0, base1 = sets[0][1], sets[1][1]
w2 = walk(base0, 0)
b3 = block()
w5 = walk(base0, 1)
w(P0 + 0x714, "<H", 0x4021)                               # disclosed perturbation: a latched word distinct from the action
w6 = walk(base1, 1)
sets_ng, _, tab_ng = build(grudge=False)
w4 = walk(base0, 0)
R = {"W1_set": {"ok": sets[0][0], "records": [x.hex() for x in sets[0][2]], "config": sets[0][3].hex()}, "grudge": {"ok": grudge_ok, "table": tab},
     "W2": w2, "W3_block": b3, "W4_no_grudge": dict(w4, table=tab_ng), "W5_resume_same_set": w5, "W6_resume_other_set": w6}
recs = sets[0][2]
kinds = lambda x: [e[0] for e in x["events"]]
rec5 = "+%X" % (0x20 + 4 * 24)
cases = {
    "W1_authored_set_from_preset_11": sets[0][0] and len(recs) == 6 and [struct.unpack_from("<H", sets[0][3], 4 * i)[0] for i in range(6)]
        == [0x605A, 0x6000, 0x6004, 0x6005, 0x6001, 0x6002] and [struct.unpack_from("<H", x, 0)[0] for x in recs] == [0xAA] + [0x96] * 5,
    "W2_first_match_commits_with_real_conditions": w2["ok"] and w2["ret"] == 1 and kinds(w2) == [
        "eval", "availability", "eval_ret"] + ["eval", "availability", "selector", "eval_ret"] * 4 + ["commit", "commit_ret"]
        and [e[1] for e in w2["events"] if e[0] == "availability"][0] != 0 and [e[1] for e in w2["events"] if e[0] == "availability"][1:] == [0] * 4
        and [e for e in w2["events"] if e[0] == "selector"] == [["selector", 0]] * 3 + [["selector", 1]]
        and [e[1] for e in w2["events"] if e[0] == "eval"] == ["+20", "+38", "+50", "+68", rec5]
        and [e for e in w2["events"] if e[0] in ("commit", "commit_ret")][0][1] == "96" and w2["events"][-1] == ["commit_ret", 1],
    "W3_commit_block_names_the_committed_record": b3["708"] == "%X" % (base0 + 0x20 + 4 * 24) and b3["714"] == "96"
        and b3["710"] == [e for e in w2["events"] if e[0] == "commit"][0][2] and b3["copy_718_equals_700"],
    "W4_no_grudge_no_target_no_commit": w4["ok"] and w4["ret"] == 0 and "commit" not in kinds(w4)
        and [e for e in w4["events"] if e[0] == "selector"] == [["selector", 0]] * 5 and tab_ng == [0] * len(tab_ng),
    "W5_resume_reaches_its_record_and_returns_1_unevaluated": w5["ok"] and w5["ret"] == 1
        and [e[1] for e in w5["events"] if e[0] == "eval"] == ["+20", "+38", "+50", "+68"] and "commit" not in kinds(w5) and "notify" not in kinds(w5),
    "W6_resumed_commit_makes_the_third_call_with_the_latched_word": w6["ok"] and w6["ret"] == 1 and "commit" in kinds(w6)
        and [e for e in w6["events"] if e[0] == "notify"] == [["notify", "%X" % r(P0 + 0x698, "<Q")[0], "96", "4021", 4]]
        and "notify" not in kinds(w2),
}
res = {"live_game": False, "runs": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "commit_walk_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-64s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({k: R[k]["events"] for k in ("W2", "W4_no_grudge", "W5_resume_same_set", "W6_resume_other_set")}))
print("block", b3, "grudge", tab)
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
