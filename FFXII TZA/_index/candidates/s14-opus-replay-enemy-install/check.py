"""S-14: execute the definition installer 0023A570's ENEMY path (class 1, CONTRACT-battle-unit-construction.md I1, I4, I5, I6, I8)
over a shipped area file, with the real spawn-record initializer 0023AC80 (OPUS, 2026-09-25, block 343).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Block 333 ran the installer's party path stub-free; EXP-150 ran the enemy
path over synthetic joins with the spawn initializer scripted. world.py (block 318/319's builder, Session; UCRT rand bridge from
block 332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack by shipped code; the area file
ps2data/plan_master/in/plan_map/rsn_b/area/rsn_b.ard (shipped extract) is bound by the game's own binder 003EA710 (block 342).
No application stub and no stop boundary. Fixtures: four idle objects, the unit pool [0208E688] / [0208E6A0] with the unit
(flag bit 26 = placement, +0x10 a zeroed handle object, +0x40 a spawn index list {1, 0}, +0x57 = 0), a zeroed spawn pool at
q[0208E690] (stride 0x250), the master flag d[02089300] = 1.
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RIP

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ARD_PATH = r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map\rsn_b\area\rsn_b.ard"
ARD = open(ARD_PATH, "rb").read()
INSTALL, BINDER, SPAWN_INIT, TRACK = 0x23A570, 0x3EA710, 0x23AC80, 0x328FF0
W.ALLOWED |= {0x16D6A0} | SP.allowed(W) | W.closure(INSTALL) | W.closure(BINDER)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
for fam in range(15):
    for o in (0x48, 0x50):
        h = struct.unpack("<Q", bytes(uc.mem_read(0x1EEBCC0 + fam * 0x58 + o, 8)))[0]
        if h:
            W.ALLOWED |= {h} | W.closure(h)
made, skipped = SP.bind(W, S)
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
REGION = 0x76400000
uc.mem_map(REGION, (len(ARD) + 0x1000 + 0xFFFF) & ~0xFFFF)
BUF = REGION + 0x1000                                   # 0x1000 into its own zeroed mapping, below 4 GB (block 342)
uc.mem_write(BUF, ARD)
assert S.call(BINDER, BUF), "binder"
POOL, HANDLE, LIST, SPAWNS, MASTER = 0x76280000, 0x76290000, 0x76290800, 0x762C0000, 0x2089300
COUNTERS = 0x2089340 + 0x4014


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def table(slot):
    h = r(slot, "<Q")[0]
    return {"count": r(h + 4, "<I")[0], "stride": r(h + 8, "<H")[0], "rows": r(h + 0xC, "<I")[0]}


DEFS, CLS, BASE, PER = table(0x2EBF120), table(0x2EBF150), table(0x2EBF148), table(0x2EBF140)
ev = {"calls": []}
for a, nm in ((SPAWN_INIT, "spawn init 0023AC80"), (TRACK, "track 00328FF0"), (0x236A60, "reset 00236A60")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev["calls"].append(nm), begin=a, end=a)


def world(spawn_fresh=True):
    uc.mem_write(POOL, bytes(0xF50 * 2))
    uc.mem_write(HANDLE, bytes(0x100))
    w(POOL, "<Q", 1 << 26)
    w(POOL + 0x10, "<Q", HANDLE)
    w(POOL + 0x40, "<Q", LIST)
    w(POOL + 0x57, "<b", 0)
    w(LIST, "<BB", 1, 0)
    if spawn_fresh:
        uc.mem_write(SPAWNS, bytes(0x250 * 4))
    w(0x208E690, "<Q", SPAWNS)
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", 1)
    w(MASTER, "<I", 1)


def install(uid):
    ev["calls"] = []
    ok = S.call(INSTALL, POOL, uid)
    return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))




AREA_BYTE = 0x208D454                                   # the counter row selector read at 0023A7FE
COUNTERS_BASE = 0x2089340 + 0x4014
tracked = []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: tracked.append(["%08X" % u.reg_read(UC_X86_REG_RIP), "%X" % a, v]),
            begin=0x2EC1380, end=0x2EC1380 + 2 * 24 - 1)
counter_w = []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: counter_w.append(["%08X" % u.reg_read(UC_X86_REG_RIP), "%X" % a, v & 0xFFFF]),
            begin=COUNTERS_BASE, end=COUNTERS_BASE + 256 * 64 * 2 - 1)
spawn_w = []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: spawn_w.append(u.reg_read(UC_X86_REG_RIP)),
            begin=SPAWNS, end=SPAWNS + 0x24F)


def row(tab, i):
    return tab["rows"] + i * tab["stride"]


# ---- I1 / I4 / I8: every shipped definition installs on the enemy path ----
rows = {}
for d in range(DEFS["count"]):
    world()
    del spawn_w[:], tracked[:], counter_w[:]
    ok, v = install(0x0100 | d)
    dr = row(DEFS, d)
    ci, bi, li = r(dr, "<H")[0], r(dr + 0x22, "<H")[0], r(dr + 0x24, "<H")[0]
    rows[d] = {"ok": ok, "returned": v, "flags": "%016X" % r(POOL, "<Q")[0],
               "stats_698_is_spawn_80": r(POOL + 0x698, "<Q")[0] == SPAWNS + 0x80, "spawn_6A0": r(POOL + 0x6A0, "<Q")[0] == SPAWNS,
               "E60_is_def_row": r(POOL + 0xE60, "<Q")[0] == dr, "E68_is_class_row": r(POOL + 0xE68, "<Q")[0] == row(CLS, ci),
               "E70_is_base_row": r(POOL + 0xE70, "<Q")[0] == row(BASE, bi), "E78_is_per_level_row": r(POOL + 0xE78, "<Q")[0] == row(PER, li),
               "f6C": r(POOL + 0x6C, "<f")[0], "class_byte_27": r(row(CLS, ci) + 0x27, "<B")[0],
               "spawn_init_writes": len(spawn_w), "calls": list(ev["calls"]), "def_plus3_code": r(dr + 3, "<B")[0] & 3,
               "tracked_writes": list(tracked)}
k = rows.values()
record("I1_I4_enemy_install_every_definition",
       all(v["ok"] and v["returned"] == 1 and v["stats_698_is_spawn_80"] and v["spawn_6A0"] and v["E60_is_def_row"] and v["E68_is_class_row"]
           and v["E70_is_base_row"] and v["E78_is_per_level_row"] and int(v["flags"], 16) >> 2 & 1 and int(v["flags"], 16) >> 26 & 1
           and v["calls"][:2] == ["reset 00236A60", "spawn init 0023AC80"] for v in k), definitions=len(rows), rows=rows,
       note="class 1 (ids 0x0100..0x0115) over all %d definitions of the shipped rsn_b.ard: each returns 1; +0x698 = spawn + 0x80 (the "
            "spawn's embedded stats), +0x6A0 = the spawn, +0xE60 = the definition row, +0xE68 = the [02EBF150] row chosen by def +0, "
            "+0xE70 / +0xE78 = the [02EBF148] / [02EBF140] rows chosen by def +0x22 / +0x24; the reset and the REAL spawn "
            "initializer 0023AC80 run" % len(rows))
record("I8_class1_float_from_byte_27", all(v["f6C"] == float(v["class_byte_27"]) for v in k),
       values=sorted({v["f6C"] for v in k}),
       note="on class 1, unit +0x6C = float(class row byte +0x27) - no x1.5 (that is class 0's +0x2B path)")
# ---- I5: the row bound against the shipped count ----
i5 = {}
for label, uid in (("row = count", 0x0100 | DEFS["count"]), ("row 0xFF", 0x01FF), ("row count - 1", 0x0100 | (DEFS["count"] - 1))):
    world()
    ok, v = install(uid)
    i5[label] = {"ok": ok, "returned": v, "bit26": r(POOL, "<Q")[0] >> 26 & 1, "spawn_init": "spawn init 0023AC80" in ev["calls"]}
record("I5_row_bound_is_the_shipped_count",
       all(x["ok"] for x in i5.values()) and all(i5[k]["returned"] == 0 and i5[k]["bit26"] == 1 and not i5[k]["spawn_init"]
                                                 for k in ("row = count", "row 0xFF"))
       and i5["row count - 1"]["returned"] == 1,
       cases=i5, note="row index = the shipped count (%d) or 0xFF: returns 0 and KEEPS bit 26 - the bound failure at 0023A662 jumps to "
                      "0023A63A, past the bit-26 clear at 0023A633 that only other classes take - with no spawn initialization; "
                      "row count - 1 installs" % DEFS["count"])

# ---- I6: the freshness gate covers the spawn init AND the counter ----
i6 = {}
for label, pre in (("fresh (byte 0 = 0)", 0), ("byte 0 bit 0 set", 1), ("byte 0 bit 2 set", 4), ("byte 0 bit 1 only", 2)):
    world()
    w(SPAWNS, "<B", pre)
    w(SPAWNS + 0x12, "<B", 0xAB)
    del counter_w[:]
    ok, v = install(0x0100)
    i6[label] = {"ok": ok, "returned": v, "spawn_init": "spawn init 0023AC80" in ev["calls"], "counter_writes": list(counter_w),
                 "spawn_12": r(SPAWNS + 0x12, "<B")[0]}
fresh = [i6["fresh (byte 0 = 0)"], i6["byte 0 bit 1 only"]]
stale = [i6["byte 0 bit 0 set"], i6["byte 0 bit 2 set"]]
record("I6_freshness_gate", all(x["ok"] and x["returned"] == 1 for x in i6.values())
       and all(x["spawn_init"] and len(x["counter_writes"]) == 1 and x["spawn_12"] != 0xAB for x in fresh)
       and all(not x["spawn_init"] and not x["counter_writes"] and x["spawn_12"] == 0xAB for x in stale),
       cases=i6, note="byte[spawn] & 5 == 0 (0 or 2): the real initializer runs, one counter word is written and spawn +0x12 takes the "
                      "old count; bit 0 or bit 2 set: neither runs and +0x12 keeps its value - the install still returns 1")

# ---- I7: tracked-HP registration needs a nonzero code - over a second shipped area whose codes are 0 AND 1 ----
# (every rsn_b definition has def+3 & 3 == 0, so rsn_b alone tests only the no-write half)
ARD2_PATH = r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map\bhm_c\area\bhm_c.ard"
ARD2 = open(ARD2_PATH, "rb").read()
REGION2 = 0x76500000
uc.mem_map(REGION2, (len(ARD2) + 0x1000 + 0xFFFF) & ~0xFFFF)
uc.mem_write(REGION2 + 0x1000, ARD2)
assert S.call(BINDER, REGION2 + 0x1000), "binder 2"
DEFS2 = table(0x2EBF120)
i7 = {}
for d in range(DEFS2["count"]):
    world()
    uc.mem_write(0x2EC1380, bytes(2 * 24))
    del tracked[:]
    ok, v = install(0x0100 | d)
    code = r(row(DEFS2, d) + 3, "<B")[0] & 3
    i7[d] = {"ok": ok, "returned": v, "code": code, "slot_EA9": r(POOL + 0xEA9, "<B")[0], "tracked_writes": list(tracked),
             "row0": list(r(0x2EC1380, "<II"))}
codes = sorted({x["code"] for x in i7.values()})
record("I7_tracked_registration_needs_a_code",
       codes == [0, 1] and all(x["ok"] and x["returned"] == 1 for x in i7.values())
       and all(bool(x["tracked_writes"]) == (x["code"] != 0) for x in i7.values())
       and all(x["row0"] == [x["slot_EA9"], 1] for x in i7.values() if x["code"]),
       area={"path": ARD2_PATH, "sha256": hashlib.sha256(ARD2).hexdigest(), "defs": DEFS2["count"]}, codes=codes, defs=i7,
       note="bhm_c.ard (%d definitions, codes 0 and 1): 00328FF0(0, def+3 & 3, unit+0xEA9) writes the tracked table 02EC1380 row 0 "
            "= {slot, code} exactly for the definitions whose code is nonzero, and writes nothing for code 0" % DEFS2["count"])

json.dump({"ok": allok, "ard": {"path": ARD_PATH, "sha256": hashlib.sha256(ARD).hexdigest(), "defs": DEFS["count"]}, "bound": made,
           "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
