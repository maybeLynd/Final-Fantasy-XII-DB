"""S-32 LC-5 (OPUS, 2026-09-26): 'The loot stream is advanced by the PERIODIC TICK, not only by kills. 00319530 has one caller,
BattleUnit_RunPeriodicCombatMaintenance at 00311146, gated two instructions earlier on the unit's stats[+0x05] being zero'
(CONTRACT-loot-rolls-and-the-chain.md LC-5), executed over block 320's world (check.py, imported: its cases run first, unchanged).

The loot stream is the LCG at 022C256C (x = x * 0x41C64E6D + 0x3039), which 00319530 steps three times per draw and stores
back at 00319582. Each run seeds it with a known value in pre_tick, runs the whole tick 00310DB0 to its ret with no stub, and
reads it back.
Cases: stats[+5] = 0 -> 00319530 entered once from 00311146 and the stream advanced by exactly three steps; stats[+5] = 1 ->
not entered, the stream unchanged; no stats block -> not entered, unchanged (gate 1).
Evidence class: NATIVE-REPLAY (unicorn), live_game false. Writes lc5_result.json.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE

import check as C
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
LOOT, DRAW, SITE = 0x22C256C, 0x319530, 0x311146
PICK_FLAGS, PICK_POS = 0x22BE7F0, 0x22BE800          # Loot_FindOverlappingPickupIndex 002FB150: 10 slots, stride 0x20
SEED = 0x1234ABCD
# Two shipped functions the pickup path enters through indirect transfers, outside 00310DB0's static call-graph closure; found by
# running (each stopped a run when first entered) and allowed with their own closures - listed shipped targets, not stubs.
EXTRA = (0x2FD8D0, 0x2FD150)
for _e in EXTRA:
    W.ALLOWED |= W.closure(_e) | {_e}


def lcg(x, k):
    for _ in range(k):
        x = (x * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    return x


def tick(kind5=0, stats=True, pickup=True):
    ev = {"draws": [], "returns": []}

    def pre(uc):
        uc.mem_write(C.UNIT, bytes(0x2000))
        uc.mem_write(C.STATS, bytes(0x2000))
        uc.mem_write(C.ACTOR, bytes(0x1000))
        uc.mem_write(C.POS, bytes(0x100))
        uc.mem_write(C.ACTOR + 3, bytes([0x65]))
        uc.mem_write(C.ACTOR + 0xB8, struct.pack("<Q", C.POS))
        uc.mem_write(C.UNIT + 0x10, struct.pack("<Q", C.ACTOR))
        if stats:
            uc.mem_write(C.UNIT + 0x698, struct.pack("<Q", C.STATS))
            uc.mem_write(C.STATS + 5, bytes([kind5]))
        uc.mem_write(C.COUNTER, struct.pack("<I", 0))
        uc.mem_write(C.MODE, struct.pack("<i", 0))
        uc.mem_write(0x2098E20, bytes([1, 0, 0, 0, 1, 1, 1, 3]))
        uc.mem_write(LOOT, struct.pack("<I", SEED))
        uc.mem_write(0x208E688, struct.pack("<Q", C.UNIT))    # the battle-unit pool: this unit is its one unit, owning STATS
        uc.mem_write(0x208E6A0, struct.pack("<I", 1))         # (002F9400's owner lookup 0031B860 needs it for a foe-kind record)
        if pickup:
            uc.mem_write(PICK_FLAGS, bytes([1]))          # pickup slot 0 active (flag byte, 002FB1E0)
            uc.mem_write(PICK_POS, bytes(0x10))           # at the origin, where the actor's position block also is
            uc.mem_write(C.UNIT + 0x714, struct.pack("<H", 0x4165))   # the 003110E8 alternative to 003273B0 (party focus)

    def hook(uc, st):
        def on_draw(u, a, n, _):
            ret = struct.unpack("<Q", bytes(u.mem_read(u.reg_read(W.UC_X86_REG_RSP), 8)))[0]
            ev["draws"].append("%08X" % (ret - 5))
        uc.hook_add(UC_HOOK_CODE, on_draw, begin=DRAW, end=DRAW)

    ok, st, uc = W.run(C.UNIT, 0, C.FX["fixes"], trace_n=8, inits=C.FX["inits"], pre_tick=pre, tick_hook=hook)
    after = struct.unpack("<I", bytes(uc.mem_read(LOOT, 4)))[0]
    return {"ok": ok, "stopped_at": (st["bad"] or st["faults"])[:1], "draw_call_sites": ev["draws"], "loot_after": "%08X" % after,
            "steps": next((k for k in range(0, 16) if lcg(SEED, k) == after), None)}


a = tick(0)
b = tick(1)
c = tick(stats=False)
d = tick(0, pickup=False)
cases = {
    "stats5_zero_the_tick_draws_once_from_00311146": a["ok"] and a["draw_call_sites"] == ["%08X" % SITE] and a["steps"] == 3,
    "stats5_one_no_draw_stream_unchanged": b["ok"] and b["draw_call_sites"] == [] and b["steps"] == 0,
    "no_stats_block_no_draw_stream_unchanged": c["ok"] and c["draw_call_sites"] == [] and c["steps"] == 0,
    "no_overlapping_pickup_no_draw_stream_unchanged": d["ok"] and d["draw_call_sites"] == [] and d["steps"] == 0,
}
res = {"ok": all(cases.values()), "cases": cases, "seed": "%08X" % SEED, "extra_allowed": ["%08X" % e for e in EXTRA], "stats5_0": a, "stats5_1": b, "no_stats": c, "no_pickup": d}
json.dump(res, open(os.path.join(HERE, "lc5_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-50s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
