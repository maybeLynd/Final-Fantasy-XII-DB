"""S-26: execute the three bodies of CONTRACT-effect-layers.md - mutate 0030E130, rebuild 0030FED0, merge 003847C0 - as shipped
code, and test L-1..L-6 and the section 12 reproduction formula (OPUS, 2026-09-25, block 341).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; UCRT rand bridge from block
332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack by shipped code. No application
stub and no stop boundary. Fixtures: four idle objects, the unit pool [0208E688] / [0208E6A0] with owning units (+0x698 -> the
stats record, +0x10 a zeroed actor), stats records (+4 character index, +5 party 0 / foe 1, +0x50 five equipment words = 0xFFFF,
+0x194 the licence bitmap), an action byte for the merge's second argument.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RIP, UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
MUTATE, REBUILD, MERGE, OWNER = 0x30E130, 0x30FED0, 0x3847C0, 0x31B860
W.ALLOWED |= {0x16D6A0} | SP.allowed(W) | set().union(*(W.closure(f) for f in (MUTATE, REBUILD, MERGE)))
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
POOL, CASTER, TARGET, LONE, ACTORS, CTX, ACTION = 0x76280000, 0x76290000, 0x76291000, 0x76292000, 0x762A0000, 0x762B0000, 0x762B1000
G_OWNER = 0x2EBF188


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def layer(rec, off):
    return int.from_bytes(bytes(uc.mem_read(rec + off, 16)), "little")


def ids(v):
    return [n for n in range(128) if v >> n & 1]


ev = {"writes": [], "entered": set()}
for rec, nm in ((CASTER, "caster"), (TARGET, "target")):
    for off, ln in ((0x68, "mutable"), (0x78, "derived")):
        uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _, nm=nm, ln=ln: ev["writes"].append(
            [nm, ln, "%08X" % u.reg_read(UC_X86_REG_RIP)]), begin=rec + off, end=rec + off + 15)
ev_mode = []                                           # the mutate's fifth argument (mode), read at entry from [rsp + 0x28]
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: ev_mode.append(
    struct.unpack("<I", bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP) + 0x28, 4)))[0]), begin=MUTATE, end=MUTATE)
SIDE = {0x386AE0: "set handler 00386AE0", 0x386A50: "clear handler 00386A50", 0x3112F0: "applier 003112F0",
        0x30EA40: "0030EA40", 0x3279B0: "003279B0", REBUILD: "rebuild 0030FED0", 0x46A790: "0046A790", 0x46A720: "0046A720"}
for a, nm in SIDE.items():
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev["entered"].add(nm), begin=a, end=a)


def reset_ev():
    ev["writes"].clear()
    ev["entered"].clear()
    del ev_mode[:]


def world(target_owned=True, caster_char=0, licences=b"", foe_bits=None):
    """caster and target records in the pool; LONE is a record no unit owns."""
    uc.mem_write(POOL, bytes(0xF50 * 2))
    recs = [(CASTER, caster_char)] + ([(TARGET, 1)] if target_owned else [])
    for rec in (CASTER, TARGET, LONE):
        uc.mem_write(rec, bytes(0x400))
        w(rec + 0x50, "<5H", *[0xFFFF] * 5)
    for i, (rec, ch) in enumerate(recs):
        w(rec + 4, "<BB", ch, 0)
        uc.mem_write(ACTORS + i * 0x1000, bytes(0x1000))
        w(POOL + i * 0xF50 + 0x10, "<Q", ACTORS + i * 0x1000)
        w(POOL + i * 0xF50 + 0x698, "<Q", rec)
        w(POOL + i * 0xF50 + 0x55, "<B", 0x20 + i)
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", len(recs))
    if licences:
        uc.mem_write(CASTER + 0x194, licences)
    w(G_OWNER, "<Q", 0x1111111111111111)


def merge(caster, target, action_byte=0, word5=0x7777):
    uc.mem_write(CTX, b"\xCC" * 0x40)
    w(ACTION, "<B", action_byte)
    ok = S.call(MERGE, CTX, ACTION, caster, target, stack=(word5,))
    return ok, {"flags_caster": "%08X" % r(CTX + 4, "<I")[0], "flags_target": "%08X" % r(CTX + 8, "<I")[0],
                "word_18": "%04X" % r(CTX + 0x18, "<H")[0], "merged": int.from_bytes(bytes(uc.mem_read(CTX + 0x1A, 16)), "little"),
                "g_02EBF188": "%X" % r(G_OWNER, "<Q")[0], "word_0": "%04X" % r(CTX, "<H")[0]}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- L-3 / L-4: the merge is the OR over all 128 ids (id 15 kept clear so L-5 cannot interfere) ----
A = int.from_bytes(bytes((0x5A ^ (i * 37)) & 0xFF for i in range(16)), "little") & ~(1 << 15)
B = int.from_bytes(bytes((0xC3 ^ (i * 91)) & 0xFF for i in range(16)), "little") & ~(1 << 15)
world()
uc.mem_write(CASTER + 0x68, A.to_bytes(16, "little"))
uc.mem_write(CASTER + 0x78, B.to_bytes(16, "little"))
ok, m = merge(CASTER, TARGET)
record("L3_merge_is_the_or_of_both_layers", ok and m["merged"] == A | B and A & ~B and B & ~A,
       only_mutable=len(ids(A & ~B)), only_derived=len(ids(B & ~A)), both=len(ids(A & B)), merged_ids=len(ids(m["merged"])),
       note="caster +0x68 = A, +0x78 = B over all 128 ids (id 15 clear): ctx +0x1A == A | B exactly; bits from either layer are "
            "indistinguishable after it (L-3), so a shared position aliases (L-4)")
w(CASTER + 0x68, "<16s", (1 << 16).to_bytes(16, "little"))
w(CASTER + 0x78, "<16s", bytes(16))
ok1, m1 = merge(CASTER, TARGET)
w(CASTER + 0x68, "<16s", bytes(16))
w(CASTER + 0x78, "<16s", (1 << 16).to_bytes(16, "little"))
ok2, m2 = merge(CASTER, TARGET)
record("L4_alias_bit_16", ok1 and ok2 and m1["merged"] == m2["merged"] == 1 << 16,
       note="bit 16 in the mutable layer (Disease) and bit 16 in the derived layer (Weatherproof) give the SAME merged context")

# ---- L-5: id 15 revocation, and what the merge writes besides the context ----
l5 = {}
for label, owned, tgt, act in (("target owned, action bit5 clear", True, TARGET, 0), ("target not owned", True, LONE, 0),
                               ("target null", True, 0, 0), ("action bit5 set", True, TARGET, 0x20)):
    world(target_owned=owned)
    w(CASTER + 0x68, "<16s", (1 << 15 | 1 << 3).to_bytes(16, "little"))
    w(TARGET + 0x64, "<I", 0x00811000)
    w(LONE + 0x64, "<I", 0x00811000)
    ok, m = merge(CASTER, tgt, act)
    m["id15"] = m["merged"] >> 15 & 1
    m["id3"] = m["merged"] >> 3 & 1
    m["merged"] = "%032X" % m["merged"]
    l5[label] = dict(ok=ok, **m)
k = l5
record("L5_id15_revocation", all(v["ok"] and v["id3"] == 1 for v in k.values())
       and k["target owned, action bit5 clear"]["id15"] == 1 and k["target not owned"]["id15"] == 0
       and k["target null"]["id15"] == 0 and k["action bit5 set"]["id15"] == 0
       and k["target owned, action bit5 clear"]["flags_target"] == "00811000" and k["target not owned"]["flags_target"] == "00810000"
       and k["action bit5 set"]["flags_target"] == "00000000",
       cases=l5, note="id 15 (and 3 as a control) set in the CASTER's mutable layer: kept when the TARGET (4th argument) has an owning "
                      "unit and the action byte's bit 5 is clear; revoked when the target has no owning unit, is null, or bit 5 is set")
record("L5_owner_global_written_by_the_merge",
       all(v["ok"] for v in k.values()) and k["target owned, action bit5 clear"]["g_02EBF188"] == "%X" % POOL.__add__(0xF50)
       and k["target not owned"]["g_02EBF188"] == "0" and k["target null"]["g_02EBF188"] == "1111111111111111",
       word_18={kk: v["word_18"] for kk, v in k.items()},
       note="the merge STORES 0031B860(target) into 02EBF188 (00384870) whenever the target is non-null - the contract's section 5 "
            "lists that global as read, never written here; +0x18 is the owning unit's byte +0x55, 0xFFFF with no owner, and "
            "left 0 (the prologue's clear) with a null target")

# ---- L-2 and the mutate's layer selection ----
modes = {}
for mode, start, layer_off in ((2, 0, 0x68), (3, 0, 0x78), (0, 1, 0x68), (1, 1, 0x78)):
    world()
    n = 40
    if start:
        w(CASTER + layer_off, "<16s", (1 << n).to_bytes(16, "little"))
    before = (layer(CASTER, 0x68), layer(CASTER, 0x78))
    reset_ev()
    ok = S.call(MUTATE, CASTER, n, 0, 0x202, stack=(mode,))
    after = (layer(CASTER, 0x68), layer(CASTER, 0x78))
    touched = ["mutable" if before[0] != after[0] else None, "derived" if before[1] != after[1] else None]
    modes[mode] = {"ok": ok, "layer_changed": [t for t in touched if t], "bit_after": after[0 if layer_off == 0x68 else 1] >> n & 1,
                   "entered": sorted(ev["entered"])}
    reset_ev()
    ok2 = S.call(MUTATE, CASTER, n, 0, 0x202, stack=(mode,))
    modes[mode]["repeat_is_noop"] = ok2 and (layer(CASTER, 0x68), layer(CASTER, 0x78)) == after and not ev["entered"]
record("L2_mutate_takes_the_layer_as_a_parameter",
       all(v["ok"] and v["repeat_is_noop"] for v in modes.values())
       and modes[2]["layer_changed"] == ["mutable"] and modes[2]["bit_after"] == 1
       and modes[3]["layer_changed"] == ["derived"] and modes[3]["bit_after"] == 1
       and modes[0]["layer_changed"] == ["mutable"] and modes[0]["bit_after"] == 0
       and modes[1]["layer_changed"] == ["derived"] and modes[1]["bit_after"] == 0,
       modes={str(kk): v for kk, v in modes.items()},
       note="0030E130(rec, id 40, 0, flags 0x202, mode): mode 2 sets / 0 clears the mutable layer, 3 sets / 1 clears the derived; "
            "the same id, the layer chosen by the caller; a repeat in the reached state writes nothing and runs no side effect")

cross = {}
for label, pre_off, mode in (("set derived while mutable holds it", 0x68, 3), ("set derived, neither holds it", None, 3)):
    world()
    n = 40
    if pre_off:
        w(CASTER + pre_off, "<16s", (1 << n).to_bytes(16, "little"))
    reset_ev()
    ok = S.call(MUTATE, CASTER, n, 0, 0x202, stack=(mode,))
    cross[label] = {"ok": ok, "derived_bit": layer(CASTER, 0x78) >> n & 1, "entered": sorted(ev["entered"])}
record("mutate_side_effects_key_on_the_merged_presence",
       all(v["ok"] and v["derived_bit"] == 1 for v in cross.values())
       and not cross["set derived while mutable holds it"]["entered"] and cross["set derived, neither holds it"]["entered"],
       cases=cross,
       note="setting id 40 in the derived layer writes the layer either way, but the set handler / applier run only when the id "
            "was in NEITHER layer before (0030E27B compares either-layer presence before and after) - a cross-layer coupling")

# ---- L-1 / L-6: the rebuild over shipped tables ----
lic = b"\xFF" * 46
world(licences=lic)
w(CASTER + 0x68, "<16s", (1 << 16 | 1 << 2).to_bytes(16, "little"))
reset_ev()
ok1 = S.call(REBUILD, CASTER, 0)
first = {"ok": ok1, "derived": ids(layer(CASTER, 0x78)), "mutable": ids(layer(CASTER, 0x68)),
         "writes": [x for x in ev["writes"] if x[0] == "caster"], "mutate_modes": sorted(set(ev_mode)), "mutate_calls": len(ev_mode)}
reset_ev()
ok2 = S.call(REBUILD, CASTER, 0)
second = {"ok": ok2, "derived": ids(layer(CASTER, 0x78)), "writes": [x for x in ev["writes"] if x[0] == "caster"],
          "mutate_calls": len(ev_mode)}
stale = min(n for n in range(128) if n not in first["derived"])
w(CASTER + 0x78, "<16s", (layer(CASTER, 0x78) | 1 << stale).to_bytes(16, "little"))
drop = first["derived"][0] if first["derived"] else None
if drop is not None:
    w(CASTER + 0x78, "<16s", (layer(CASTER, 0x78) & ~(1 << drop)).to_bytes(16, "little"))
reset_ev()
ok3 = S.call(REBUILD, CASTER, 0)
third = {"ok": ok3, "derived": ids(layer(CASTER, 0x78)), "mutate_modes": sorted(set(ev_mode)), "mutate_calls": len(ev_mode),
         "stale_id": stale, "dropped_id": drop}
record("L1_rebuild_never_writes_the_mutable_layer",
       ok1 and first["derived"] and first["mutable"] == [2, 16] and all(x[1] == "derived" for x in first["writes"])
       and first["mutate_modes"] == [3],
       first=first,
       note="all 0x169 licence bits set, mutable {2, 16}: the rebuild fills the derived layer from shipped tables and every "
            "write to the caster's +0x68..+0x87 lands in +0x78 - through 0030E130 mode 3, not a store of its own")
record("L6_rebuild_reconciles",
       ok2 and second["derived"] == first["derived"] and not second["writes"] and second["mutate_calls"] == 0
       and ok3 and third["derived"] == first["derived"] and third["mutate_modes"] == [1, 3] and third["mutate_calls"] == 2,
       second=second, third=third,
       note="a second rebuild with unchanged inputs writes nothing and calls the mutate zero times; after planting a stale id and "
            "dropping a desired one, the third rebuild makes exactly two mutate calls - mode 1 clears the stale, mode 3 re-adds")

# ---- the foe source: rec +5 == 1 takes its desired bitmap from the owning unit's +0xE80 ----
world()
FOE_BITS = int.from_bytes(bytes((0x3C ^ (i * 53)) & 0xFF for i in range(16)), "little")
w(CASTER + 5, "<B", 1)
uc.mem_write(POOL + 0xE80, FOE_BITS.to_bytes(16, "little"))
SIDEBLK = 0x762C0000
uc.mem_write(SIDEBLK, bytes(0x100))
w(POOL + 0x6A0, "<Q", SIDEBLK)
w(CASTER + 0x68, "<16s", (1 << 16 | 1 << 2).to_bytes(16, "little"))
reset_ev()
# 002FEF30's foe arm reads the area's unit-definition slot [02EBF150] (an ARD resource this world does not load), so for the foe
# the run ENDS at 002FEF30's entry (a stop boundary, recorded - not a stub); the reconcile precedes it at 00310340-003103A3.
boundary = []


def _stop(u, x, n, _):
    boundary.append({"at": "%08X" % x, "rcx": "%X" % u.reg_read(UC_X86_REG_RCX), "edx": u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF})
    u.emu_stop()


hstop = uc.hook_add(UC_HOOK_CODE, _stop, begin=0x2FEF30, end=0x2FEF30)
S.call(REBUILD, CASTER, 0)
uc.hook_del(hstop)
okf = uc.reg_read(UC_X86_REG_RIP) == 0x2FEF30 and not S.st["faults"] and not S.st["bad"] and len(boundary) == 1 \
    and boundary[0]["rcx"] == "%X" % CASTER
foe = {"ok": okf, "boundary": boundary, "derived_equals_unit_E80": layer(CASTER, 0x78) == FOE_BITS, "mutable": ids(layer(CASTER, 0x68)),
       "desired_ids": len(ids(FOE_BITS)), "mutate_modes": sorted(set(ev_mode)), "mutate_calls": len(ev_mode),
       "mutable_writes": [x for x in ev["writes"] if x[1] == "mutable"]}
record("foe_derived_layer_is_the_unit_E80_bitmap",
       okf and foe["derived_equals_unit_E80"] and foe["mutable"] == [2, 16] and not foe["mutable_writes"]
       and foe["mutate_calls"] == foe["desired_ids"] and foe["mutate_modes"] == [3], foe=foe,
       note="a foe record (+5 = 1, no equipment, no licences): the rebuild's derived layer equals its owning unit's +0xE80 128-bit "
            "bitmap exactly, one mode-3 mutate per id, and the mutable layer is untouched; the run ends at the stop boundary "
            "002FEF30(rec, 0) - its foe arm needs the area's unit-definition slot [02EBF150], not loaded here")

json.dump({"ok": allok, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
