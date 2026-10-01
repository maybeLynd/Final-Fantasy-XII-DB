"""S-25 (OPUS, 2026-09-26): can a matched gambit line be refused by the commit? No, over the shipped action table - measured.

CONTRACT-gambit-walk section 7 (FABLE's qualification, 2026-09-25): "Whether the unit arm or the slot combiner can still make a
real commit refuse is open". The commit 0030F760 refuses (returns 0) only outside its two bands, 0..0x21E and 0x4000..0x4166. This
check shows that every action id the evaluator lets through lies inside one of them.
STATIC (from the image):
 T1  the evaluator 003014C0 has one success exit (003017E9, mov eax, 1), and its action slot `out` is written at one place,
     00301500 (the decode). The walk writes its slot [rsp+0x70] only at 00305CD6 (the 0xFFFF init) and hands it only to the
     evaluator (00305DCA), then reads it for the commit (00305DE3) and the third call (00305E44).
 T2  the evaluator reaches 003017E9 only through the condition arm (003015D4, taken when id - 0x4000 <= 0x166) or the unit arm
     (003015EA), whose availability check 002FFCF0 must return 0 (00301604 / 00301606).
 T3  the commit's only return-0 site is 0030F981 (xor eax, eax), and its only branch source is the band test 0030F7EC.
NATIVE-REPLAY over block 332's world (the shipped battle_pack bound by shipped code):
 D1  BattleEncodedId_IsValidForClass(20, id) (00322C50) accepts exactly 0..0x21E over 0..0x7FFF: the action table [02EBF138] has
     543 rows.
 D2  002FFCF0 on an eligible unit returns reason 4 (002FFD94) for 0x21F, 0x3FFF, 0x4167 and 0x7FFF - an id outside class 20 is
     refused before any target selector - and 0 for 0x96 (Attack).
 D3  control, the band is real: the commit called directly refuses 0x21F and 0x4167 (returns 0) and accepts 0x21E and 0x4166.
So with the shipped table, a line whose condition matched always carries an id the commit accepts. The bound holds for this
table: a pack whose action table had more than 0x21F rows would open 0x21F.. to the unit arm and the commit would refuse them.
Evidence classes: STATIC (T1-T3), NATIVE-REPLAY (D1-D3), live_game false. Writes result.json.
"""
import contextlib
import io
import json
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn.x86_const import UC_X86_REG_RAX

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, "..", "s21-opus-replay-applier-stub-free"))
sys.path.insert(0, BASE)
cwd = os.getcwd(); os.chdir(BASE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as C                                     # block 332 (its cases run first, unchanged)
os.chdir(cwd)
W, uc, S = C.W, C.uc, C.S
EVAL, WALK, COMMIT, AVAIL, VALID = 0x3014C0, 0x305CC0, 0x30F760, 0x2FFCF0, 0x322C50
md = Cs(CS_ARCH_X86, CS_MODE_64)
sizes = {int(l.split("\t")[0], 16): int(l.split("\t")[2]) for l in open(os.path.join(W.GRAPH, "functions.tsv"), encoding="utf-8", errors="replace")
         if l[:1] in "0123456789ABCDEF" and l.split("\t")[0] in ("003014C0", "00305CC0", "0030F760")}


def body(f):
    code = bytes(uc.mem_read(f, sizes[f]))
    return list(md.disasm(code, f))


ev, wk, cm = body(EVAL), body(WALK), body(COMMIT)
T = {
    "eval_success_exits": ["%08X" % i.address for i in ev if i.mnemonic == "mov" and i.op_str == "eax, 1"],
    "eval_out_writers": ["%08X" % i.address for i in ev if i.mnemonic == "mov" and i.op_str.startswith("word ptr [r12]")],
    "walk_slot_refs": ["%08X %s" % (i.address, i.mnemonic) for i in wk if "rsp + 0x70" in i.op_str],
    "eval_arm_sites": {"condition_arm": [("%08X" % i.address, i.op_str) for i in ev if i.address in (0x3015CE, 0x3015D2, 0x3015DA)],
                       "unit_arm": [("%08X" % i.address, i.op_str) for i in ev if i.address in (0x3015FF, 0x301604, 0x301606)]},
    "commit_return0_sites": ["%08X" % i.address for i in cm if i.mnemonic == "xor" and i.op_str == "eax, eax"],
    "commit_branches_to_return0": ["%08X" % i.address for i in cm if i.mnemonic.startswith("j") and i.op_str == "0x30f981"],
}
W.ALLOWED |= W.closure(VALID) | {VALID} | W.closure(AVAIL) | {AVAIL} | W.closure(COMMIT) | {COMMIT}
uc.ctl_flush_tb()
valid, runs = [], []
for i in range(0x8000):
    S.call(VALID, 20, i, 1)
    if uc.reg_read(UC_X86_REG_RAX) & 0xFF:
        valid.append(i)
for v in valid:
    if runs and v == runs[-1][1] + 1:
        runs[-1][1] = v
    else:
        runs.append([v, v])
table = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF138, 8)))[0]
rows = struct.unpack("<I", bytes(uc.mem_read(table + 4, 4)))[0]
C.reset()
UNIT = C.POOL
uc.mem_write(UNIT, bytes([uc.mem_read(UNIT, 1)[0] | 0x10]))
avail = {}
for aid in (0x96, 0x21F, 0x3FFF, 0x4167, 0x7FFF):
    ok = S.call(AVAIL, aid, UNIT)
    avail["%X" % aid] = {"ok": ok, "reason": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF}
commit = {}
for aid in (0x21E, 0x21F, 0x4166, 0x4167):
    C.reset()
    uc.mem_write(UNIT + 0x700, bytes(0x50))
    ok = S.call(COMMIT, UNIT, 0xABCDEF, aid, 0x00120034, stack=(0,))
    commit["%X" % aid] = {"ok": ok, "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF}
R = {"static": T, "class20_valid_runs": ["%X-%X" % tuple(r) for r in runs], "action_table_rows": rows, "availability": avail, "commit": commit}
cases = {
    "T1_one_success_exit_one_out_writer_walk_slot_only_to_the_evaluator": T["eval_success_exits"] == ["003017E9"] and T["eval_out_writers"] == ["00301500"]
        and T["walk_slot_refs"] == ["00305CD6 mov", "00305DCA lea", "00305DE3 movzx", "00305E44 movzx"],
    "T2_two_arms_condition_band_and_availability": T["eval_arm_sites"]["condition_arm"] == [("003015CE", "cx, r8w"), ("003015D2", "0x3015ea"), ("003015DA", "0x301830")]
        and T["eval_arm_sites"]["unit_arm"] == [("003015FF", "0x2ffcf0"), ("00301604", "eax, eax"), ("00301606", "0x3015e3")],
    "T3_commit_returns_0_only_from_the_band_test": T["commit_return0_sites"] == ["0030F981"] and T["commit_branches_to_return0"] == ["0030F7EC"],
    "D1_class20_is_exactly_0_to_21E": R["class20_valid_runs"] == ["0-21E"] and rows == 0x21F,
    "D2_availability_refuses_ids_outside_class20_with_reason_4": all(avail[k]["ok"] and avail[k]["reason"] == 4 for k in ("21F", "3FFF", "4167", "7FFF"))
        and avail["96"]["ok"] and avail["96"]["reason"] == 0,
    "D3_the_commit_band_is_real": all(commit[k]["ok"] for k in commit) and commit["21E"]["ret"] == 1 and commit["4166"]["ret"] == 1
        and commit["21F"]["ret"] == 0 and commit["4167"]["ret"] == 0,
}
res = {"live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-70s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps(R, default=str)[:1800])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
