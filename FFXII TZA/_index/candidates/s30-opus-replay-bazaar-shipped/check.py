"""S-30 (OPUS, 2026-09-26): CONTRACT-bazaar-unlock-and-purchase section 4 / 7 executed over the SHIPPED goods table and the
storage bound by the shipped rebase, stub-free.

S-30's cell reads "the bit-0 invariant and FZ-3 rest on the refresh execution + EXP-092's stubbed callees". EXP-092's own header
says "STUBBED (disclosed): none" - it plants the registry, the family tables and the flag array. This closer goes further: it runs
over block 348's world (../s32-opus-replay-level-advance/check.py, imported: its cases run first, unchanged), where the shipped
battle_pack binding supplies the bazaar registry [02EBF058] (128 goods rows, stride 0x24) and the battle-state block [02EBF190]; the
inventory descriptors are bound by the shipped rebase 0030B6A0 over that block, and every tally is written through the real
mutate 003008A0 (the byte channel r9 = 3). Nothing of the goods table is planted. No application stub.
Rows used (shipped): 0 = one-time, loot 0x205C x2; 87 = repeatable, loots 0x20CA x2 + 0x20C8 x3; 99 = script-only (+0x14 bit 1),
all-zero thresholds. The shipped table holds 106 one-time rows, 15 repeatable, 7 script-only with zero thresholds.
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
from unicorn.x86_const import UC_X86_REG_RAX

W, uc, S = C.W, C.uc, C.S
REFRESH, PURCHASE, SCRIPT, REBASE, MUTATE, GATE = 0x30B270, 0x30B180, 0x30B570, 0x30B6A0, 0x3008A0, 0x322C50
for f in (REFRESH, PURCHASE, SCRIPT, REBASE, MUTATE, GATE, 0x2FD150, 0x2FD420, 0x2FD8D0, 0x2FD970, 0x2FD780, 0x2FD880):
    W.ALLOWED |= W.closure(f) | {f}
uc.ctl_flush_tb()
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
BLOCK = q(0x2EBF190)
REG = q(0x2EBF058)
NROWS = struct.unpack("<I", bytes(uc.mem_read(REG + 4, 4)))[0]
ROWS = struct.unpack("<I", bytes(uc.mem_read(REG + 0xC, 4)))[0] + q(0x1F83530)
STRIDE = struct.unpack("<H", bytes(uc.mem_read(REG + 8, 2)))[0]
FLAGS = BLOCK + 0x59C8


def call(fn, *a):
    ok = S.call(fn, *a)
    return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, (S.st["bad"] or S.st["faults"])[:2]


def flags():
    return list(uc.mem_read(FLAGS, NROWS))


def row(i):
    r = bytes(uc.mem_read(ROWS + i * STRIDE, STRIDE))
    return {"f14": r[0x14], "loots": [struct.unpack_from("<H", r, o)[0] for o in (0x16, 0x1A, 0x1E)], "thr": [r[0x18], r[0x1C], r[0x20]]}


def tally(loot):
    call(0x309F30, loot, 3)                      # the query entry, channel 3 (the byte the refresh compares)
    return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


def set_tally(loot, v):
    return call(MUTATE, loot, v, 1, 3)           # (id, value, absolute, byte channel), stack arg5 = 0
res = {"live_game": False, "rows": NROWS, "stride": STRIDE, "block": "%X" % BLOCK}
okb = call(REBASE, BLOCK)
res["rebase"] = okb
R0, R87, R99 = row(0), row(87), row(99)
res["rows_used"] = {"0": R0, "87": R87, "99": R99}
cases = {}
cases["shipped_registry_and_rebase"] = NROWS == 128 and STRIDE == 0x24 and okb[0] and R0["f14"] & 3 == 0 and R87["f14"] & 1 == 1 and R99["f14"] & 2 == 2
# refresh with every tally zero: clause 4 rejects the thresholded rows, clause 3 the zero-threshold rows
f0 = flags()
r1 = call(REFRESH)
f1 = flags()
cases["refresh_with_zero_tallies_unlocks_nothing"] = r1[0] and f1 == f0 and all(x & 3 == 0 for x in f1)
# earn row 0's thresholds through the real mutate, refresh: flag |= 3 on row 0 only
for loot, t in zip(R0["loots"], R0["thr"]):
    if t:
        set_tally(loot, t)
earned = [tally(l) for l, t in zip(R0["loots"], R0["thr"]) if t]
r2 = call(REFRESH)
f2 = flags()
cases["clause4_met_sets_both_bits_on_that_row_only"] = r2[0] and f2[0] & 3 == 3 and all(f2[i] == f1[i] for i in range(NROWS) if i != 0) \
    and earned == [t for t in R0["thr"] if t]
# clause 2: already available -> refresh leaves it
r3 = call(REFRESH)
cases["clause2_already_available_is_left_alone"] = r3[0] and flags()[0] == f2[0]
# purchase: gate, flag &= ~2 (bit 0 survives), the three recipe loots' tallies written to absolute zero
p = call(PURCHASE, 0xD000 + 0)
fp = flags()[0]
after_tally = [tally(l) for l, t in zip(R0["loots"], R0["thr"]) if t]
cases["purchase_clears_bit1_keeps_bit0_zeroes_the_tallies"] = p[0] and p[1] == 1 and fp & 3 == 1 and after_tally == [0] * len(after_tally)
# clause 1: a one-time row already unlocked is rejected even with its thresholds earned again
for loot, t in zip(R0["loots"], R0["thr"]):
    if t:
        set_tally(loot, t)
r4 = call(REFRESH)
cases["clause1_one_time_row_stays_unlocked_but_unavailable"] = r4[0] and flags()[0] & 3 == 1
# a repeatable row re-unlocks after its own purchase once its thresholds are earned again
for loot, t in zip(R87["loots"], R87["thr"]):
    if t:
        set_tally(loot, t)
call(REFRESH); rep_first = flags()[87]
call(PURCHASE, 0xD000 + 87); rep_bought = flags()[87]
for loot, t in zip(R87["loots"], R87["thr"]):
    if t:
        set_tally(loot, t)
call(REFRESH); rep_again = flags()[87]
cases["repeatable_row_re_unlocks_after_purchase"] = rep_first & 3 == 3 and rep_bought & 3 == 1 and rep_again & 3 == 3
# clause 3 + script-set: row 99 (zero thresholds) never unlocks by refresh; script-set writes bit 1 and never touches bit 0
call(REFRESH); z = flags()[99]
s1 = call(SCRIPT, 0xD000 + 99, 1); fs1 = flags()[99]
s0 = call(SCRIPT, 0xD000 + 99, 0); fs0 = flags()[99]
uc.mem_write(FLAGS + 99, bytes([fs0 | 1]))
s2 = call(SCRIPT, 0xD000 + 99, 0); fs2 = flags()[99]
s_gate = call(SCRIPT, 0xD000 + 0, 1); fs_gate = flags()[0]
cases["clause3_zero_threshold_row_never_unlocks_by_refresh"] = z & 3 == 0
cases["script_set_writes_bit1_only_and_keeps_bit0"] = s1[0] and fs1 & 3 == 2 and fs0 & 3 == 0 and fs2 & 3 == 1
cases["script_set_needs_the_rows_bit1"] = s_gate[0] and fs_gate & 3 == 1
# bit 0 is never cleared by any of the three writers across the whole sequence
cases["bit0_never_cleared_by_refresh_purchase_or_script_set"] = flags()[0] & 1 == 1 and flags()[87] & 1 == 1
# the purchase gate: an id past the table returns 0 and touches nothing
fb = flags(); pg = call(PURCHASE, 0xD000 + NROWS)
cases["purchase_gate_refuses_an_id_past_the_table"] = pg[0] and pg[1] == 0 and flags() == fb
res["cases"] = cases
res["trace"] = {"row0": [f1[0], f2[0], fp], "row87": [rep_first, rep_bought, rep_again], "row99": [z, fs1, fs0, fs2]}
res["ok"] = all(cases.values())
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print("trace", res["trace"], "rows", res["rows_used"])
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
