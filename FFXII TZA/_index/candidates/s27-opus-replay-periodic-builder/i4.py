"""S-27 I-3 / I-4 as corrected on 2026-09-25 (OPUS, 2026-09-26): attribute every READ and WRITE of the stats block to the stage
whose call frame is live, over block 310's harness (check.py, imported: it runs its own six cases first, unchanged).

I-3 (corrected): stage 1 (003848E0) zeroes all 320 bytes +0x08..+0x147 of the result record through memset, then plants
its sentinels. I-4 (corrected): stage 3 is the only body that READS the effect-slot timers +0x17C; stage 2 is the only one
that reaches the duration / beat pair +0xBC / +0x13C; no stage writes the stats block.

Attribution is by call frame, not by 'last stage entered': on a stage's entry its return address is recorded, and reaching
that address hands attribution back to the builder (stage 0). Reads are hooked on the stats block only; the hook is added
after check.py's runs, so the translation cache is flushed first (uc.ctl_flush_tb()).
Evidence class: NATIVE-REPLAY (unicorn), live_game false; the same single memset import bridge as block 310, no application
stub. Writes i4_result.json.
"""
import collections
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RSP

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc = C.uc
frames = []                 # stack of (stage, return address)
acc = collections.defaultdict(lambda: collections.defaultdict(set))   # stage -> kind -> set of stats offsets


def cur():
    return frames[-1][0] if frames else 0


def on_code(u, a, n, _):
    if frames and a == frames[-1][1]:
        frames.pop()
    if a in C.STAGES:
        ret = struct.unpack("<Q", bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP), 8)))[0]
        frames.append((C.STAGES[a], ret))


def on_read(u, ac, a, n, v, _):
    for i in range(n):
        acc[cur()]["r"].add(a + i - C.STATS)


def on_write(u, ac, a, n, v, _):
    for i in range(n):
        acc[cur()]["w"].add(a + i - C.STATS)


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_READ, on_read, begin=C.STATS, end=C.STATS + 0x7FF)
uc.hook_add(UC_HOOK_MEM_WRITE, on_write, begin=C.STATS, end=C.STATS + 0x7FF)
uc.ctl_flush_tb()


def span(lo, n):
    return set(range(lo, lo + n))


DUR, BEAT, SLOT = span(0xBC, 4 * 32), span(0x13C, 2 * 32), span(0x17C, 2 * 32)
scen = {
    "effect_slots": dict(w68=bytes([0xFF] * 8), slots={0: 5, 1: 1, 2: 0, 3: 7}, erows={3: 0, 9: 1, 20: 2, 30: 0xFF}, ecount=64),
    "regen_beat": dict(w3c=1 << 0x19, beat={0x19: 10}, srows={0x19: 4}, frame=1),
    "beat_and_slots": dict(w3c=1 << 0x19, beat={0x19: 25}, srows={0x19: 4}, w68=bytes([0xFF] * 8), slots={0: 5, 1: 1},
                           erows={3: 0, 9: 1}, ecount=64),
    "empty": dict(),
}
out, ok_all = {}, True
for name, kw in scen.items():
    frames.clear()
    acc.clear()
    C.world(**kw)
    ok = C.run()
    rec = bytes(uc.mem_read(C.RESULT, C.RSIZE))
    per = {str(s): {k: sorted(v) for k, v in d.items()} for s, d in acc.items()}
    slot_readers = sorted(s for s, d in acc.items() if d["r"] & SLOT)
    pair_readers = sorted(s for s, d in acc.items() if d["r"] & (DUR | BEAT))
    stage_writers = sorted(s for s, d in acc.items() if s and d["w"])
    out[name] = {"returned": ok, "slot_readers": slot_readers, "dur_beat_readers": pair_readers,
                 "stages_writing_stats": stage_writers, "per_stage": per}
    ok_all &= ok
cases = {
    "I4_only_stage3_reads_the_effect_slot_timers": all(set(v["slot_readers"]) <= {3} for v in out.values())
        and out["effect_slots"]["slot_readers"] == [3],
    "I4_only_stage2_reaches_the_duration_beat_pair": all(set(v["dur_beat_readers"]) <= {2} for v in out.values())
        and out["regen_beat"]["dur_beat_readers"] == [2],
    "I4_no_stage_writes_the_stats_block": all(not v["stages_writing_stats"] for v in out.values()),
}
# I-3 (corrected), from this file's own empty-world run: stage 1's memset of exactly 0x140 bytes at result + 8, no 0xCC fill
# left in +0x08..+0x147, and the sentinel runs (32 dwords from +0x5C, 32 words from +0xDC) all -1
frames.clear(); acc.clear(); C.world(); ok_e = C.run()
rec = bytes(uc.mem_read(C.RESULT, C.RSIZE))
ms = [m for m in C.state["memset"] if m[1] == C.RESULT + 8]
cases["I3_stage1_zeroes_all_320_bytes_then_plants_sentinels"] = bool(
    ok_e and ms and ms[0][0] == 1 and ms[0][2] == 0 and ms[0][3] == 0x140
    and 0xCC not in rec[0x08:0x148]
    and all(struct.unpack_from("<i", rec, 0x5C + 4 * k)[0] == -1 for k in range(32))
    and all(struct.unpack_from("<h", rec, 0xDC + 2 * k)[0] == -1 for k in range(32)))
out["I3_empty_world"] = {"returned": ok_e, "memset": ms, "cc_left_in_08_147": rec[0x08:0x148].count(0xCC)}
res = {"ok": bool(ok_all and all(cases.values())), "cases": cases, "scenarios": out}
json.dump(res, open(os.path.join(HERE, "i4_result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-56s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
