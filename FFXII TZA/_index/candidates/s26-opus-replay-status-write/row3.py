"""S-26 (OPUS, 2026-09-26): the status write with an OWNING battle unit - section 10 row 3 (invariant 2's exception) and the
unit-dependent side effects check.py could not reach (the reaction, the defeat cleanup with rewards, the recovery).

check.py ran 0030E360 on a battle-state row that no unit owns. Here the row is owned: block 345's world
(s25-opus-replay-enmity/check.py, imported; its cases run first, unchanged) installs party units whose +0x698 is a battle-state
row, and the owner search 0031B860 runs as shipped. No application stub; the allowed set is the static closures of 0030E360 and
00300FC0.
The exception, read from the bytes (0030E467..0030E49C): when the owning unit's stats kind +5 is 0 and its type byte +4 is in
0x1B..0x27 (sub al, 0x1B / cmp al, 0xC / ja), a terminal status (bit & 0x80000003) calls 00300FC0(unit, 0) at 0030E497 and jumps
to the exit - before any mask write. In the shipped party table (battle_pack directory +0x44) rows 27..39 are the thirteen Espers,
so 0x1B..0x27 is exactly the Esper rows. The type byte is planted per case on block 345's party row 0 (block 345 plants it too).
Cases (KO = status 0, mode 3, flags 0x200):
 E1  type 0x1B and 0x27 (both ends of the band): 00300FC0 is called with the owning unit and 0; no reaction, no rewards; the three
     masks +0x38 / +0x3C / +0x64 are untouched.
 E2  type 0x1A and 0x28 (just outside) and 0x00 (Vaan's row): the full KO path - reaction 003284D0, defeat cleanup 00300FC0,
     rewards 00312280 - and the KO bit lands in +0x64.
 E3  a non-terminal add (status 5) on an Esper row is not the exception: the bit is written and 00300FC0 is not called.
 E4  removing KO from the Vaan row (mode 0) clears the bit (the mask write comes first) and enters the recovery 00301140. Boundary
     recorded: the recovery calls BattleUnit_RefreshActorRuntimeFromDefinition 00238BF0, which reads the unit's actor runtime -
     a zeroed fixture handle in block 345's world - and faults there. The recovery's own effects are not executed.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes row3_result.json.
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
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RIP

W, uc, S, w, r = E.W, E.uc, E.S, E.w, E.r
SW, DEFEAT, REWARDS, REACTION, RECOVER = 0x30E360, 0x300FC0, 0x312280, 0x3284D0, 0x301140
W.ALLOWED |= W.closure(SW) | {SW} | W.closure(DEFEAT) | {DEFEAT}
ev, mask_w = [], []
for a, nm in ((DEFEAT, "defeat"), (REWARDS, "rewards"), (REACTION, "reaction"), (RECOVER, "recover")):
    uc.hook_add(UC_HOOK_CODE, (lambda nm: lambda u, a, n, _: ev.append([nm, "%X" % u.reg_read(UC_X86_REG_RCX), "%X" % (u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)]))(nm),
                begin=a, end=a)
uc.ctl_flush_tb()
P0 = E.unit(E.NFOE + 0)


def run(typ, status=0, mode=3, pre64=None):
    E.world()
    row = E.row(0)
    w(row + 4, "<BB", typ, 0)
    if pre64 is not None:
        w(row + 0x64, "<I", pre64)
    before = {"%X" % o: r(row + o, "<I")[0] for o in (0x38, 0x3C, 0x64)}
    del ev[:], mask_w[:]
    h = uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: mask_w.append(["+%X" % (a - row), "%08X" % u.reg_read(UC_X86_REG_RIP)]),
                    begin=row + 0x38, end=row + 0x67)
    ok = S.call(SW, row, 0, status, 1, stack=(2, 0x200, mode))
    uc.hook_del(h)
    after = {"%X" % o: r(row + o, "<I")[0] for o in (0x38, 0x3C, 0x64)}
    trace = list(S.st["trace"])
    return {"ok": ok, "halt": (S.st["bad"] or S.st["faults"])[:1], "events": list(ev), "before": before, "after": after,
            "last_function": "%08X" % max(f for f in W.FSTARTS if f <= trace[-1]) if trace else None,
            "mask_writes": [x for x in mask_w if x[0] in ("+38", "+3C", "+64")], "unit": "%X" % P0}


R = {"type_%02X" % t: run(t) for t in (0x1B, 0x27, 0x1A, 0x28, 0x00)}
R["nonterminal_on_esper_row"] = run(0x1B, status=5)
R["remove_ko_vaan"] = run(0x00, status=0, mode=0, pre64=1)
names = lambda x: [e[0] for e in x["events"]]
unit = "%X" % P0
cases = {
    "E1_esper_rows_defeat_cleanup_only_masks_untouched": all(
        R[k]["ok"] and R[k]["events"] == [["defeat", unit, "0"]] and R[k]["after"] == R[k]["before"] and not R[k]["mask_writes"]
        for k in ("type_1B", "type_27")),
    "E2_outside_the_band_the_full_KO_path_and_the_bit": all(
        R[k]["ok"] and names(R[k]) == ["reaction", "defeat", "rewards"] and R[k]["after"]["64"] == 1 for k in ("type_1A", "type_28", "type_00")),
    "E3_nonterminal_on_an_esper_row_is_written_no_defeat": R["nonterminal_on_esper_row"]["ok"] and "defeat" not in names(R["nonterminal_on_esper_row"])
        and (R["nonterminal_on_esper_row"]["after"]["64"] | R["nonterminal_on_esper_row"]["after"]["3C"]) & (1 << 5) != 0,
    "E4_removing_KO_clears_the_bit_then_enters_the_recovery_boundary_00238BF0": "recover" in names(R["remove_ko_vaan"])
        and R["remove_ko_vaan"]["after"]["64"] & 1 == 0 and R["remove_ko_vaan"]["mask_writes"] != []
        and not R["remove_ko_vaan"]["ok"] and R["remove_ko_vaan"]["last_function"] == "00238BF0",
    "no_fault_except_the_recorded_boundary": all(x["ok"] and not x["halt"] for k, x in R.items() if k != "remove_ko_vaan"),
}
res = {"live_game": False, "runs": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "row3_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-60s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({k: (names(v), v["after"]) for k, v in R.items()}))
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
