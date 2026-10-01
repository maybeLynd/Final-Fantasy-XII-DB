"""S-32 GL-6 (OPUS, 2026-09-26): 'Gil is an EXECUTION RESOURCE, spent in three phases ... reserve, commit, give back. ... a
reserve-then-refund pair is invisible in the balance and visible twice in the counters.' (CONTRACT-gil-storage-and-movement.md
GL-6), executed over block 347's world (check.py, imported: its cases run first, unchanged).

The three writers run as shipped code with every callee real:
  BattleAction_PrepareExecutionResources 0030EF20(unit, abilityRow)      - reserves: [unit+0xE58] = 00309060's cost, gil -= cost
  BattleAction_RefundReservedExecutionResources 00300280(unit)          - gives back [unit+0xE58], then zeroes it
  BattleAction_ConsumeExecutionResources 00305640(unit, abilityRow, 0)  - commits: zeroes the reservation, no refund
Fixtures (planted): a party unit (stats +5 = 0) whose stats +0x6C bit 0 is set - the flag BattleUnit_UsesGilActionCostChannel
002F9820 tests, which routes the ability's cost to gil; the ability is a shipped battle_pack row (the first id that 00309060
prices above zero); gil starts at 1000 through the setter.
Evidence class: NATIVE-REPLAY (unicorn), live_game false; no application stub. Writes gl6_result.json.
"""
import json
import os
import struct

import check as C
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
uc, S = C.uc, C.S
PREPARE, REFUND, CONSUME, COST, SETTER, GETTER = 0x30EF20, 0x300280, 0x305640, 0x309060, 0x254EE0, 0x253690
W.ALLOWED |= set().union(*(W.closure(f) | {f} for f in (PREPARE, REFUND, CONSUME)))
ABIL = 0x2EBF138
UNIT, STATS = 0x76280000, 0x76282000
from unicorn.x86_const import UC_X86_REG_RAX


def rd(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))[0]


def row(i):
    hdr = rd(ABIL, "<Q")
    return rd(hdr + 0xC, "<I") + rd(0x1F83530, "<Q") + i * rd(hdr + 8, "<H")


def fresh_unit():
    uc.mem_write(UNIT, bytes(0xF50))
    uc.mem_write(STATS, bytes(0x400))
    uc.mem_write(UNIT + 0x698, struct.pack("<Q", STATS))
    uc.mem_write(UNIT + 0xDC8, struct.pack("<H", 0xFFFF))
    uc.mem_write(STATS + 0x6C, bytes([1]))
    uc.mem_write(STATS + 0x24, struct.pack("<i", 1000))
    uc.mem_write(STATS + 0x28, struct.pack("<h", 500))


def cost(i):
    fresh_unit()
    S.call(COST, UNIT, i)
    return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


def state():
    return {"gil": rd(C.GIL, "<i"), "gain_counter": rd(C.COUNTERS + 0x3860, "<I"), "spend_counter": rd(C.COUNTERS + 0x3864, "<I"),
            "reserved_E58": rd(UNIT + 0xE58, "<I")}


def reset(gil):
    uc.mem_write(C.COUNTERS + 0x3860, bytes(8))
    assert S.call(SETTER, gil)
    uc.mem_write(C.COUNTERS + 0x3860, bytes(8))


n = rd(rd(ABIL, "<Q") + 4, "<I")
pick = next(i for i in range(min(n, 0x21F)) if cost(i) > 0)
c = cost(pick)
out = {"ability": pick, "cost": c, "ability_rows": n}

fresh_unit(); reset(1000)
s0 = state()
ok1 = S.call(PREPARE, UNIT, row(pick)); s1 = state()
ok2 = S.call(REFUND, UNIT); s2 = state()
out["reserve_then_refund"] = {"start": s0, "after_prepare": s1, "after_refund": s2, "ok": [ok1, ok2]}

fresh_unit(); reset(1000)
t0 = state()
ok3 = S.call(PREPARE, UNIT, row(pick)); t1 = state()
ok4 = S.call(CONSUME, UNIT, row(pick), 0); t2 = state()
ok5 = S.call(REFUND, UNIT); t3 = state()
out["reserve_then_commit"] = {"start": t0, "after_prepare": t1, "after_consume": t2, "after_late_refund": t3, "ok": [ok3, ok4, ok5]}

cases = {
    "prepare_reserves_the_cost_and_takes_it_from_gil": ok1 and s1["reserved_E58"] == c and s1["gil"] == 1000 - c
        and s1["spend_counter"] == c and s1["gain_counter"] == 0,
    "refund_gives_it_back_and_clears_the_reservation": ok2 and s2["gil"] == 1000 and s2["reserved_E58"] == 0 and s2["gain_counter"] == c,
    "reserve_then_refund_invisible_in_balance_visible_twice_in_counters": s2["gil"] == s0["gil"] and s2["spend_counter"] == c
        and s2["gain_counter"] == c,
    "commit_keeps_the_charge_and_ends_the_reservation": ok4 and t2["gil"] == 1000 - c and t2["reserved_E58"] == 0
        and t2["spend_counter"] == c and t2["gain_counter"] == 0,
    "a_refund_after_commit_gives_nothing_back": ok5 and t3["gil"] == 1000 - c and t3["gain_counter"] == 0,
}
res = {"ok": all(cases.values()), "cases": cases, **out}
json.dump(res, open(os.path.join(HERE, "gl6_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-68s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED", "ability", pick, "cost", c)
