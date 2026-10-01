"""S-25: execute the enmity operations (CONTRACT-enmity.md E-1..E-8) as shipped code over foes installed by the shipped
installer 0023A570 from a shipped area file, shipped party rows, and shipped action rows (OPUS, 2026-09-25, block 345).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; UCRT rand bridge from block
332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack (the action rows at registry slot
[02EBF138] included) by shipped code; ps2data/plan_master/in/plan_map/rsn_b/area/rsn_b.ard (shipped extract) is bound by the
game's own binder 003EA710. No application stub and no stop boundary.
Fixtures: six idle objects at 0x76300000 (the world's convention), the unit pool - units 0 and 1 are foes installed by 0023A570
class 1 (each with its own spawn: flag bit 26, +0x10 handle, +0x40 spawn list {1, i}), units 2..4 are party members owning
battle-state rows 0..2 (+4 type) - slot map 0 = {0, 1, 2} with maps 1-4 built by the real refresher 003266C0, a zeroed spawn pool,
the master flag.
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ARD_PATH = r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map\rsn_b\area\rsn_b.ard"
ARD = open(ARD_PATH, "rb").read()
APPLY, WRITE1, PROPAGATE, ADJUST, DECAY, WRITEALL = 0x3216E0, 0x321850, 0x3219D0, 0x321B00, 0x321530, 0x321D30
INSTALL, BINDER, REFRESH = 0x23A570, 0x3EA710, 0x3266C0
W.ALLOWED |= ({0x16D6A0} | SP.allowed(W) | set().union(*(W.closure(f) for f in (APPLY, DECAY, WRITEALL, INSTALL, BINDER, REFRESH))))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
for fam in range(15):
    for o in (0x48, 0x50):
        h = struct.unpack("<Q", bytes(uc.mem_read(0x1EEBCC0 + fam * 0x58 + o, 8)))[0]
        if h:
            W.ALLOWED |= {h} | W.closure(h)
made, skipped = SP.bind(W, S)
IDLE = 0x76300000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
REGION = 0x76400000
uc.mem_map(REGION, (len(ARD) + 0x1000 + 0xFFFF) & ~0xFFFF)
uc.mem_write(REGION + 0x1000, ARD)
assert S.call(BINDER, REGION + 0x1000), "binder"
POOL, HANDLES, LISTS, SPAWNS, MASTER = 0x76280000, 0x76290000, 0x76290800, 0x762C0000, 0x2089300
BLOCK = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF190, 8)))[0]
MAP0 = BLOCK + 0x5A48
NFOE, NPARTY = 2, 3


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def unit(i):
    return POOL + i * 0xF50


def row(i):
    return BLOCK + 8 + i * 0x1C8


def table(slot):
    h = r(slot, "<Q")[0]
    return {"count": r(h + 4, "<I")[0], "stride": r(h + 8, "<H")[0], "rows": r(h + 0xC, "<I")[0]} if h else None


ACTIONS = table(0x2EBF138)
print("actions", ACTIONS, "framelimit scale", r(0x1DFE0B8, "<f")[0])
cands = []
for a in range(ACTIONS["count"]):
    base = ACTIONS["rows"] + a * ACTIONS["stride"]
    p = (r(base + 0x1D, "<B")[0], r(base + 0x1F, "<B")[0], r(base + 0x20, "<B")[0])
    if all(p):
        cands.append((a, p))


def world(foe_status=0):
    uc.mem_write(POOL, bytes(0xF50 * (NFOE + NPARTY)))
    uc.mem_write(HANDLES, bytes(0x800))
    uc.mem_write(SPAWNS, bytes(0x250 * 4))
    w(0x208E690, "<Q", SPAWNS)
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", NFOE + NPARTY)
    w(MASTER, "<I", 1)
    for i in range(NPARTY):
        rec = row(i)
        uc.mem_write(rec, bytes(0x1C8))
        w(rec + 4, "<BB", i, 0)
        u = unit(NFOE + i)
        w(u + 0x10, "<Q", HANDLES + (NFOE + i) * 0x100)
        w(u + 0x698, "<Q", rec)
    uc.mem_write(MAP0, struct.pack("<9H", 0, 1, 2, *[0xFFFF] * 6))
    assert S.call(REFRESH, 0), "refresh"
    for f in range(NFOE):
        u = unit(f)
        w(u, "<Q", 1 << 26)
        w(u + 0x10, "<Q", HANDLES + f * 0x100)
        w(u + 0x40, "<Q", LISTS + f * 0x10)
        w(LISTS + f * 0x10, "<BB", 1, f)
        assert S.call(INSTALL, u, 0x0100 | f) and uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF == 1, "install"
        w(r(u + 0x698, "<Q")[0] + 0x64, "<I", foe_status)


def tab(f):
    """foe f's enmity vector: [timer, entry(id 0), entry(id 1), ...] from BKEI + 0x19"""
    return list(bytes(uc.mem_read(r(unit(f) + 0x6A0, "<Q")[0] + 0x19, 1 + NPARTY)))


def plant(f, entries, timer=0):
    uc.mem_write(r(unit(f) + 0x6A0, "<Q")[0] + 0x19, bytes([timer] + list(entries)))


def action(a):
    return ACTIONS["rows"] + a * ACTIONS["stride"]


calls = []
for a, nm in ((WRITE1, "write 00321850"), (PROPAGATE, "propagate 003219D0"), (ADJUST, "adjust 00321B00"), (WRITEALL, "write-all 00321D30")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: calls.append([nm, u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF]), begin=a, end=a)

results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


A0 = 0
P = (r(action(A0) + 0x1D, "<B")[0], r(action(A0) + 0x1F, "<B")[0], r(action(A0) + 0x20, "<B")[0])

# ---- E-2 / E-4 / E-5: one application of shipped action 0 by party member 0 on foe 0 ----
world()
plant(0, [0, 30, 30])                                  # foe 0 already angry at members 1 and 2
plant(1, [5, 0, 0])                                    # foe 1 holds a grudge against member 0 only
before = {"foe0": tab(0), "foe1": tab(1)}
del calls[:]
ok = S.call(APPLY, unit(NFOE + 0), unit(0), action(A0))
after = {"foe0": tab(0), "foe1": tab(1)}
record("E4_three_parameters_third_negated", ok and [c[0] for c in calls] == ["write 00321850", "propagate 003219D0", "adjust 00321B00"]
       and calls[0][1] == 0 and calls[2][1] == (-P[2]) & 0xFFFFFFFF, parameters=P, calls=[list(c) for c in calls], before=before, after=after,
       note="shipped action 0 (+0x1D / +0x1F / +0x20 = %d / %d / %d): 003216E0 makes exactly three calls - write, propagate, and "
            "adjust with the NEGATED third parameter (edx = -%d)" % (P[0], P[1], P[2], P[2]))
record("E2_threat_is_stored_on_the_target", ok and after["foe0"][1] > before["foe0"][1] and after["foe0"][2] < 30
       and after["foe0"][3] < 30 and after["foe0"][0] == before["foe0"][0], before=before["foe0"], after=after["foe0"],
       note="member 0 hits foe 0: FOE 0's vector gains threat for id 0 (%d -> %d) and its entries for members 1 / 2 fall "
            "(30 -> %d / %d); the timer byte (entry 0 of the vector) is untouched"
            % (before["foe0"][1], after["foe0"][1], after["foe0"][2], after["foe0"][3]))
record("E5_grudge_alone_does_not_propagate", ok and after["foe1"] == before["foe1"], foe1_before=before["foe1"], foe1_after=after["foe1"],
       note="foe 1 already holds %d for member 0 but does NOT gain from the hit on foe 0: with a direct target, 003219D0 also requires "
            "foe 1's list at +0xBC8 (count +0xBC4, 16-byte entries) to hold the target's handle [target+0x10] (00321A82-00321AB4)"
            % before["foe1"][1])
e5 = {}
for label, listed, direct in (("grudge 5, target listed", True, True), ("grudge 0, target listed", False, True),
                              ("grudge 5, null direct target", False, False)):
    world()
    plant(0, [0, 0, 0])
    plant(1, [5 if "grudge 5" in label else 0, 0, 0])
    if listed:
        w(unit(1) + 0xBC4, "<i", 1)
        w(unit(1) + 0xBC8, "<Q", r(unit(0) + 0x10, "<Q")[0])
    if label == "grudge 0, target listed":
        w(unit(1) + 0xBC4, "<i", 1)
        w(unit(1) + 0xBC8, "<Q", r(unit(0) + 0x10, "<Q")[0])
    ok = S.call(PROPAGATE, 0, P[1], unit(0) if direct else 0, 0)
    e5[label] = {"ok": ok, "foe1": tab(1)}
record("E5_propagation_needs_grudge_and_perception", all(v["ok"] for v in e5.values())
       and e5["grudge 5, target listed"]["foe1"][1] > 5 and e5["grudge 0, target listed"]["foe1"] == [0, 0, 0, 0]
       and e5["grudge 5, null direct target"]["foe1"][1] > 5, cases=e5,
       note="003219D0(id 0, %d, target): foe 1 rises only when it already holds a grudge AND lists the direct target's handle; a zero "
            "grudge stays zero even when listed; with a null direct target the list is not consulted" % P[1])

# ---- the write seeds a new grudge vector ----
world()
plant(0, [0, 0, 0])
ok = S.call(WRITE1, unit(0), 0, P[0], 0)
record("first_grudge_seeds_the_vector", ok and tab(0)[1] >= P[0] and tab(0)[2:] == [1, 1], vector=tab(0),
       note="foe 0 holding no grudge, write id 0 += %d: the entry becomes %d (+10 at 0032193A, taken when 00321770 returns 0 - not taken in E-2, where the vector already held 30 / 30) and the zero entries for the other valid ids become 1 "
            "(0032194B-003219A5: the first grudge walks the vector through the class-2 validator)" % (P[0], tab(0)[1]))

# ---- E-3: only a party-class caster generates enmity; only foe-class targets are written ----
world()
plant(0, [0, 0, 0])
plant(1, [0, 0, 0])
del calls[:]
ok_f = S.call(APPLY, unit(1), unit(0), action(A0))      # a foe as the caster
foe_caster = {"calls": list(calls), "foe0": tab(0)}
del calls[:]
ok_p = S.call(WRITE1, unit(NFOE + 1), 0, P[0], 0)        # write aimed at a PARTY unit
party_target = {"calls": list(calls)}
record("E3_class_gates", ok_f and ok_p and foe_caster["calls"] == [] and foe_caster["foe0"] == [0, 0, 0, 0],
       foe_caster=foe_caster, party_target=party_target,
       note="a foe-class caster (stats +5 = 1) makes no call at all (003216E0's gate at 0032170D reads the CASTER's stats +5); a "
            "write aimed at a party unit returns without a table write (003218D0 requires the target's stats +5 == 1)")

# ---- E-8: the acting suppression gates the write ----
e8 = {}
for label, st in (("target status 0", 0), ("target status bit 0", 1), ("target status bit 31", 0x80000000)):
    world(foe_status=st)
    plant(0, [0, 0, 0])
    ok = S.call(WRITE1, unit(0), 0, P[0], 0)
    e8[label] = {"ok": ok, "entry_id0": tab(0)[1]}
record("E8_suppression_gates_the_write", all(v["ok"] for v in e8.values()) and e8["target status 0"]["entry_id0"] > 0
       and e8["target status bit 0"]["entry_id0"] == 0 and e8["target status bit 31"]["entry_id0"] == 0, cases=e8,
       note="00321850 writes id 0's entry for a target with status 0, and writes nothing when the target's status has bit 0 or bit "
            "31 (mask 0x80000003 at 003218AC)")

# ---- E-1 / E-6 / E-7: the decay counts in entry 0 and fires every 30 x FrameLimit-scale calls ----
e6 = {}
for scale in (1.0, 2.0):
    w(0x1DFE0B8, "<f", scale)
    world()
    plant(0, [25, 12, 5])
    fired = []
    for n in range(1, 125):
        del calls[:]
        assert S.call(DECAY, unit(0)), "decay"
        if any(c[0] == "write-all 00321D30" for c in calls):
            fired.append({"call": n, "edx": struct.unpack("<i", struct.pack("<I", [c for c in calls if c[0] == "write-all 00321D30"][0][1]))[0],
                          "vector_after": tab(0)})
    e6[str(scale)] = fired
w(0x1DFE0B8, "<f", 1.0)
one, two = e6["1.0"], e6["2.0"]
record("E6_E7_decay_interval_and_step", [f["call"] for f in one][:4] == [30, 60, 90, 120] and [f["call"] for f in two][:2] == [60, 120]
       and all(f["edx"] == -10 for f in one + two) and one[0]["vector_after"][1:] == [15, 2, 1] and one[1]["vector_after"][1:] == [5, 1, 1]
       and one[2]["vector_after"][1:] == [1, 1, 1],
       scale_1=one[:3], scale_2=two[:2],
       note="the decay fires write-all with edx = -10 on calls 30, 60, 90, 120 at FrameLimit scale 1.0 and on calls 60, 120 at 2.0; "
            "entries 25 / 12 / 5 become 15 / 2 / 1, then 5 / 1 / 1, then 1 / 1 / 1 - a held grudge is FLOORED AT 1, never forgotten "
            "(0032191D-00321923); the counter is byte 0 of the same vector (E-1)")

json.dump({"ok": allok, "ard": {"path": ARD_PATH, "sha256": hashlib.sha256(ARD).hexdigest()}, "actions": ACTIONS,
           "action_parameters_nonzero": len(cands), "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
