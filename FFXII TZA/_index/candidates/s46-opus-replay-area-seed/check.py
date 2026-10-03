"""S-46: execute I4 of CONTRACT-which-generator-serves-which-roll.md - the shared LCG is seeded, once per battle-area initialisation,
with a counter of areas entered since launch - on the shipped area init 002342F0 and draw 00328370 (OPUS, 2026-09-25, block 336).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. The S-46 exposure note (block 295): "One invariant is unexecuted: I4,
the area-count seeding." world.py (block 318/319's builder, Session) supplies the image, the IAT traps and the named bridges;
shipped_pack.py binds battle_pack by shipped code. No application stub.
STOP BOUNDARY (recorded, nothing substituted): 00239960, the first call after the seeding and the battle-flag reset; from there
the area init re-initialises the party's spawn records (0023AC80 -> 00327DE0), S-14 / S-17's machinery, which needs party data
this world does not hold. Fixtures: the master flag d[02089300] per run; six idle objects (the world's convention). The counter
0208E6B0 starts at the image's 0 and is never written by the harness after the world is built.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
AREA, DRAW, SETSTATE = 0x2342F0, 0x328370, 0x328D80
BOUNDARY = 0x239960
COUNTER, LCG, MASTER = 0x208E6B0, 0x22C256C, 0x2089300
W.ALLOWED |= {0x16D6A0, BOUNDARY} | W.closure(AREA) | W.closure(DRAW) | SP.allowed(W)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
made, skipped = SP.bind(W, S)
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
ev = {}


def on_boundary(u, a, n, _):
    ev["stopped_at"] = "00239960"
    u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_boundary, begin=BOUNDARY, end=BOUNDARY)


def rd(a):
    return struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]


def model_draws(state, n):
    out = []
    for _ in range(n):
        s1 = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
        s2 = (s1 * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
        s3 = (s2 * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
        state = s3
        a = ((s1 >> 16) & 0x7FF) << 10
        b = (s2 >> 16) & 0x3FF
        c = (s3 >> 16) & 0x3FF
        out.append(c ^ ((b ^ a) << 10))
    return out


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


runs = []
start = rd(COUNTER)
for master in (1, 1, 0, 1, 1):
    w_lcg_before = rd(LCG)
    uc.mem_write(LCG, struct.pack("<I", 0xDEADBEEF))            # so a skipped seeding is visible
    uc.mem_write(MASTER, struct.pack("<I", master))
    before = rd(COUNTER)
    ev.clear()
    S.call(AREA)
    seeded = rd(LCG)
    draws = []
    for _ in range(3):
        S.call(DRAW)
        draws.append(uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF)
    runs.append({"master": master, "counter_before": before, "counter_after": rd(COUNTER), "lcg_after_area_init": "%X" % seeded,
                 "stopped_at": ev.get("stopped_at"), "draws": draws, "model_draws": model_draws(seeded, 3)})

seq = [r for r in runs if r["master"]]
i4 = (start == 0 and [int(r["lcg_after_area_init"], 16) for r in seq] == [0, 1, 2, 3]
      and [r["counter_after"] for r in seq] == [1, 2, 3, 4]
      and runs[2]["counter_after"] == runs[2]["counter_before"] == 2 and runs[2]["lcg_after_area_init"] == "DEADBEEF"
      and all(r["stopped_at"] == "00239960" for r in seq) and all(r["draws"] == r["model_draws"] for r in runs))
record("I4_area_count_seeding", i4, counter_at_start=start, runs=runs,
       note="from the image's counter 0, each area init with the master flag set seeds the LCG with the PRE-increment count (0, 1, 2, "
            "3) and stores count+1; with the flag clear nothing is seeded or counted; the shipped draw 00328370 then yields exactly the "
            "contract's three-step XOR recurrence from that seed")
twin = model_draws(1, 3) == runs[1]["draws"] and model_draws(2, 3) != runs[1]["draws"]
record("I4_same_count_same_stream", twin, note="the stream depends only on the count: seed 1 reproduces run 2's draws, seed 2 does not")

json.dump({"ok": allok, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
