"""S-32: execute the level advance 0030C650 (CONTRACT-level-advance-and-growth.md LU-1..LU-4, LU-7, LU-8) as shipped code over the
shipped party growth rows, with the real gameplay MT (OPUS, 2026-09-25, block 348).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; UCRT rand bridge from block
332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack (the growth rows at [02EBF130] and
the level table [02EBF108]) by shipped code; rsn_b.ard (shipped extract) is
bound by the game's binder 003EA710 so the kind-1 case's final-level rebuild can read its area rows. The MT is seeded by the shipped seeder 00379CF0 -> 00863D30 and drawn by 00379CD0.
No application stub. STOP BOUNDARIES (recorded, never stubbed): the message poster 0046AB10 (reached from the level-up poster
0046A690, event 4, as in block 344) and, for the owner case, the first forwarding call 0035D8C0 (not reached here) - the presentation calls
lead into UI / audio this world does not build.
Fixtures: six idle objects at 0x76300000, battle-state row 0 as the stats record (+4 character, +5 kind, +8 HP, +0xC MP,
+0x10..+0x1C floats, +0x1C2 level), optionally a unit 0 owning it.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RIP, UC_X86_REG_RDX

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ADVANCE, SEED, DRAW, BINDER = 0x30C650, 0x379CF0, 0x379CD0, 0x3EA710
ARD_PATH = r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map\rsn_b\area\rsn_b.ard"
ARD = open(ARD_PATH, "rb").read()
W.ALLOWED |= ({0x16D6A0, 0x863D30, 0x863BF0} | SP.allowed(W) | set().union(*(W.closure(f) for f in (ADVANCE, SEED, 0x863D30, 0x863BF0, BINDER))))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
made, skipped = SP.bind(W, S)
IDLE = 0x76300000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
REGION = 0x76400000                                   # the foe-kind rebuild (002FEF30's foe arm) reads the area slots: bind rsn_b
uc.mem_map(REGION, (len(ARD) + 0x1000 + 0xFFFF) & ~0xFFFF)
uc.mem_write(REGION + 0x1000, ARD)
assert S.call(BINDER, REGION + 0x1000), "binder"
POOL, HANDLES = 0x76280000, 0x76290000
BLOCK = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF190, 8)))[0]
REC = BLOCK + 8


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


SITES = {0x30C730: "HP 002F9A60", 0x30C746: "MP 002F9B20", 0x30C75B: "float", 0x30C771: "float", 0x30C787: "float", 0x30C79D: "float",
         0x30C7CE: "rebuild 0030FED0", 0x30C7E4: "poster 0046A690", 0x30C815: "forward 0035D8C0", DRAW: "MT draw"}
ev = {"sites": [], "boundary": []}
for a, nm in SITES.items():
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev["sites"].append(nm), begin=a, end=a)
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: ev["sites"].append("level store"), begin=0x30C7BB, end=0x30C7BB)
BOUNDARIES = {0x46AB10: "poster 0046AB10", 0x35D8C0: "forward 0035D8C0"}


def _stop(u, x, n, _):
    ev["boundary"].append({"at": BOUNDARIES[x], "edx": u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF})
    u.emu_stop()


for a in BOUNDARIES:
    uc.hook_add(UC_HOOK_CODE, _stop, begin=a, end=a)


def advance(level, target, flags=0, kind=0, owner=False, seed=None):
    uc.mem_write(REC, bytes(0x1C8))
    w(REC + 4, "<BB", 0, kind)
    w(REC + 8, "<ih", 500, 50)
    w(REC + 0x10, "<4f", 10.0, 10.0, 10.0, 10.0)
    w(REC + 0x1C2, "<B", level)
    uc.mem_write(POOL, bytes(0xF50))
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", 1 if owner else 0)
    if owner:
        w(POOL + 0x10, "<Q", HANDLES)
        w(POOL + 0x698, "<Q", REC)
    if seed is not None:
        assert S.call(SEED, seed), "seed"
    ev["sites"], ev["boundary"] = [], []
    ok = S.call(ADVANCE, REC, target, flags)
    at_boundary = uc.reg_read(UC_X86_REG_RIP) in BOUNDARIES and not S.st["faults"] and not S.st["bad"]
    return {"returned": ok, "at_boundary": at_boundary, "boundary": list(ev["boundary"]), "level": r(REC + 0x1C2, "<B")[0],
            "hp": r(REC + 8, "<i")[0], "mp": r(REC + 0xC, "<h")[0], "floats": [round(x, 3) for x in r(REC + 0x10, "<4f")],
            "counts": {k: ev["sites"].count(k) for k in sorted(set(SITES.values()) | {"level store"})}, "order": list(ev["sites"])}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# flags bit 1 SUPPRESSES notification (0030C660-0030C676: r13 = ~(flags >> 1) & 1); ebx = notify AND final level (0030C6A3-0030C6C9)
QUIET = 2

# ---- LU-3: four levels, notification suppressed, no owner - the whole body to its return ----
a = advance(10, 14, flags=QUIET, seed=4537)
c = a["counts"]
record("LU3_three_cadences", a["returned"] and a["level"] == 14 and c["level store"] == 4 and c["HP 002F9A60"] == 4 and c["MP 002F9B20"] == 4
       and c["float"] == 16 and c["rebuild 0030FED0"] == 1 and c["poster 0046A690"] == 0 and c["forward 0035D8C0"] == 0, result=a,
       note="level 10 -> target 14, flags 2 (notification suppressed), no owning unit: 0030C650 returns with level 14; per level "
            "HP, MP and four float growth calls (4 / 4 / 16), the derived rebuild once (final level), no presentation")

# ---- LU-8: the growth draws the MT inside the loop; same seed same stats, other seed other stats ----
b = advance(10, 14, flags=QUIET, seed=4537)
d = advance(10, 14, flags=QUIET, seed=91)
one = advance(10, 11, flags=QUIET, seed=4537)
record("LU8_growth_is_rolled", b["returned"] and (b["hp"], b["mp"], b["floats"]) == (a["hp"], a["mp"], a["floats"])
       and (d["hp"], d["mp"]) != (a["hp"], a["mp"]) and a["counts"]["MT draw"] == 8 and one["counts"]["MT draw"] == 2,
       seed_4537=[a["hp"], a["mp"]], repeat=[b["hp"], b["mp"]], seed_91=[d["hp"], d["mp"]],
       draws_4_levels=a["counts"]["MT draw"], draws_1_level=one["counts"]["MT draw"],
       note="the same seed reproduces HP / MP exactly (%s), another seed changes them (%s); four levels draw the generator 8 times "
            "(HP and MP once each per level, the floats never), one level twice" % ([a["hp"], a["mp"]], [d["hp"], d["mp"]]))

# ---- LU-4: a non-zero kind advances the level with no growth, and posts nothing ----
f = advance(10, 14, flags=QUIET, kind=1, seed=4537)
fn = advance(10, 14, flags=0, kind=1, seed=4537)
record("LU4_nonzero_kind_bare_increment", f["returned"] and f["level"] == 14 and f["counts"]["HP 002F9A60"] == 0
       and f["counts"]["float"] == 0 and (f["hp"], f["mp"], f["floats"]) == (500, 50, [10.0] * 4) and f["counts"]["MT draw"] == 0
       and fn["returned"] and fn["counts"]["poster 0046A690"] == 0,
       result={k: f[k] for k in ("returned", "level", "hp", "mp", "floats", "counts")}, notify_on={k: fn[k] for k in ("returned", "at_boundary", "boundary", "counts")},
       note="kind 1: the level reaches 14 through four bare increments; no growth call, no draw, HP / MP / floats untouched; with "
            "notification on it still returns without the poster (0030C7DB)")

# ---- LU-1 / LU-2: the 99 guards and monotonicity ----
g = {"98 -> 120": advance(98, 120, flags=QUIET, seed=4537), "99 -> 120": advance(99, 120, flags=QUIET, seed=4537),
     "20 -> 10": advance(20, 10, flags=QUIET, seed=4537), "20 -> 20": advance(20, 20, flags=QUIET, seed=4537)}
record("LU1_LU2_cap_and_monotonic", all(v["returned"] for v in g.values()) and g["98 -> 120"]["level"] == 99
       and g["98 -> 120"]["counts"]["level store"] == 1 and g["99 -> 120"]["level"] == 99 and g["99 -> 120"]["counts"]["level store"] == 0
       and g["20 -> 10"]["level"] == 20 and g["20 -> 10"]["order"] == [] and g["20 -> 20"]["order"] == [],
       cases={k: {"level": v["level"], "counts": v["counts"]} for k, v in g.items()},
       note="98 -> 120 stores 99 once; 99 -> 120 stores nothing; 20 -> 10 and 20 -> 20 return before the loop with no call")

# ---- LU-7: the level-up poster does not need an owner ----
h = advance(10, 14, flags=0, seed=4537)
record("LU7_poster_runs_without_an_owner", h["at_boundary"] and h["boundary"][0]["at"] == "poster 0046AB10" and h["boundary"][0]["edx"] == 4
       and h["counts"]["poster 0046A690"] == 1 and h["counts"]["rebuild 0030FED0"] == 1 and h["counts"]["level store"] == 4
       and a["returned"] and a["counts"]["poster 0046A690"] == 0, result={k: h[k] for k in ("boundary", "level", "counts")},
       note="flags 0 (notification on), NO owning unit: after four levels and the rebuild, 0046A690 (0030C7E4, before the owner test "
            "at 0030C7ED) posts event 4 and the run ends at the poster boundary; only flags bit 1 makes an unowned record silent")

import hashlib
json.dump({"ok": allok, "ard": {"path": ARD_PATH, "sha256": hashlib.sha256(ARD).hexdigest()}, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
