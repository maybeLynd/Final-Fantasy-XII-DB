"""S-27: the per-unit periodic tick BattleUnit_RunPeriodicCombatMaintenance (00310DB0) executed end to end with NO application
stub - gates, I-1's deadline check, the builder 00385DF0 and the sink 003112F0 - over the world block 319 builds (OPUS,
2026-09-25, block 320).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py / world.json / printf_bridge.py are block 318/319's world
builder (shipped initialisers, nine zero-filled singleton blocks, TEB/TLS, named import bridges only - see world.py); here the
entry is 00310DB0 and ALLOWED is its static closure plus the listed extras. Every run must reach 00310DB0's own ret.
Per-case fixtures (planted data only): the unit (+0x00 flag word, +0x10 a class-3 actor with a position block, +0x698 the stats
block, +0xDD0 the deadline), the stats block (status word +0x3C, beat +0x13C), the tick counter [0208D45C] read by 0032A150,
the global mode [022C2160], and party-slot record 0 at 02098E20 (+0 active, +4..+6 non-zero, +7 = 3) that the readiness
predicate 00265680 requires.
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
assert hashlib.sha256(W.raw).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
ENTRY, BUILDER, SINK, RET_SITE = 0x310DB0, 0x385DF0, 0x3112F0, 0x3112E7
W.TICK = ENTRY
W.ALLOWED = W.closure(ENTRY) | {0x863BF0, 0x866D60, 0x866B90}
for e in FX["extra_allowed"]:
    W.ALLOWED |= W.closure(int(e, 16))
UNIT, STATS, ACTOR, POS = 0x76300000, 0x76310000, 0x76320000, 0x76321000
COUNTER, MODE = 0x208D45C, 0x22C2160
REGEN = 0x19


def tick(stats=True, flags=0, deadline=0, counter=0, mode=0, slot_ready=True, beat=None):
    ev = {"order": [], "sink_args": None, "beat_writers": []}

    def pre(uc):
        uc.mem_write(UNIT, bytes(0x2000))
        uc.mem_write(STATS, bytes(0x2000))
        uc.mem_write(ACTOR, bytes(0x1000))
        uc.mem_write(POS, bytes(0x100))
        uc.mem_write(ACTOR + 3, bytes([0x65]))
        uc.mem_write(ACTOR + 0xB8, struct.pack("<Q", POS))
        uc.mem_write(UNIT + 0x10, struct.pack("<Q", ACTOR))
        uc.mem_write(UNIT, struct.pack("<Q", flags))
        uc.mem_write(UNIT + 0xDD0, struct.pack("<I", deadline))
        if stats:
            uc.mem_write(UNIT + 0x698, struct.pack("<Q", STATS))
        if beat is not None:
            uc.mem_write(STATS + 0x3C, struct.pack("<I", 1 << REGEN))
            uc.mem_write(STATS + 0x13C + 2 * REGEN, struct.pack("<h", beat))
            uc.mem_write(STATS + 0x1C2, bytes([7]))
        uc.mem_write(COUNTER, struct.pack("<I", counter))
        uc.mem_write(MODE, struct.pack("<i", mode))
        uc.mem_write(0x2098E20, bytes([1, 0, 0, 0, 1, 1, 1, 3]) if slot_ready else bytes(8))

    def hook(uc, st):
        def on_code(u, a, n, _):
            if a == BUILDER:
                ev["order"].append("builder")
            elif a == SINK:
                ev["order"].append("sink")
                ev["sink_args"] = ["%X" % u.reg_read(r) for r in (W.UC_X86_REG_RDX, W.UC_X86_REG_R8, W.UC_X86_REG_R9)]
            elif a == 0x310DE4:
                ev["order"].append("recompute+0x24")
            elif a == 0x310DF4:
                ev["order"].append("deadline_check")
        for a in (BUILDER, SINK, 0x310DE4, 0x310DF4):
            uc.hook_add(UC_HOOK_CODE, on_code, begin=a, end=a)

        def on_write(u, ac, a, n, v, _):
            ev["beat_writers"].append(("%08X" % u.reg_read(W.UC_X86_REG_RIP), v & 0xFFFF))
        bt = STATS + 0x13C + 2 * REGEN
        uc.hook_add(UC_HOOK_MEM_WRITE, on_write, begin=bt, end=bt + 1)

    ok, st, uc = W.run(UNIT, 0, FX["fixes"], trace_n=8, inits=FX["inits"], pre_tick=pre, tick_hook=hook)
    return {"ok": ok, "stopped_at": (st["bad"] or st["faults"])[:1], "functions_entered": len(st["entered"]), "order": ev["order"],
            "sink_args_rdx_r8_r9": ev["sink_args"], "flag_word_after": "%X" % struct.unpack("<Q", bytes(uc.mem_read(UNIT, 8)))[0],
            "beat_after": struct.unpack("<h", bytes(uc.mem_read(STATS + 0x13C + 2 * REGEN, 2)))[0], "beat_writers": ev["beat_writers"]}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-36s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


full = tick()
record("full_tick_stub_free", full["ok"] and full["order"] == ["recompute+0x24", "deadline_check", "builder", "sink"]
       and full["sink_args_rdx_r8_r9"] == ["0", "%X" % STATS, "FFFF"], result=full,
       note="gates pass: the recompute, the deadline check, the builder and then the sink 003112F0(result, 0, stats, 0xFFFF, 0) run, "
            "and the tick returns")
# I-1: the deadline check sits after gate 1 and before gates 2-6
exp_set = 0x40000000
a = tick(flags=exp_set, deadline=5, counter=100)
b = tick(flags=exp_set, deadline=500, counter=100)
c = tick(stats=False, flags=exp_set, deadline=5, counter=100)
d = tick(flags=exp_set, deadline=5, counter=100, mode=5)
i1 = (a["ok"] and a["flag_word_after"] == "0" and b["ok"] and b["flag_word_after"] == "40000000"
      and c["ok"] and c["flag_word_after"] == "40000000" and "deadline_check" not in c["order"]
      and d["ok"] and d["flag_word_after"] == "0" and "builder" not in d["order"])
record("I1_deadline_between_gate1_and_gate2", i1, expired=a, not_expired=b, no_stats_block=c, gate2_refuses=d,
       note="expired (deadline 5 < counter 100) clears bit 30; not expired keeps it; with no stats block (gate 1) the check never runs "
            "and the stale bit stays; with gate 2 refusing (mode 5) the check still ran and cleared it")
# the gates refuse the builder
g2 = {m: tick(mode=m) for m in (5, 6)}
g4 = tick(slot_ready=False)
g6 = tick(flags=0x1000000000)
gates = (all(r["ok"] and "builder" not in r["order"] for r in g2.values()) and g4["ok"] and "builder" not in g4["order"]
         and g6["ok"] and "builder" not in g6["order"])
record("gates_refuse_the_builder", gates, mode5=g2[5]["order"], mode6=g2[6]["order"], not_ready=g4["order"], bit36=g6["order"],
       note="global mode 5 or 6, no ready party slot (00265680 = 0) and unit bit 0x1000000000 each end the tick before the builder")
# does the SINK commit the stage values? a Regen beat of 25 counts down by 10 into the result record (block 310); after the
# whole tick the stats block's beat reads...
cm = tick(beat=25)
record("sink_commits_the_beat", cm["ok"] and cm["beat_after"] == 15 and len(cm["beat_writers"]) == 1
       and 0x3115B6 <= int(cm["beat_writers"][0][0], 16) < 0x311610, result=cm,
       note="the stats beat 25 reads 15 after the whole tick, written ONCE, by the sink's copy 003115B6..00311606: the stages computed it "
            "into the record (block 310) and the sink committed it")

json.dump({"ok": allok, "allowed_functions": len(W.ALLOWED), "world": FX, "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
