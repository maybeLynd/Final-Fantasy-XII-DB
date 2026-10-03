"""S-14: execute the definition installer 0023A570 (CONTRACT-battle-unit-construction.md) end to end with its REAL callees - the
reset 00236A60, the rekey 00322050 / 003220E0, the party install, the pulse reset 002FEAB0 - over the shipped battle_pack tables,
and test I1..I4, I7 and I8 (OPUS, 2026-09-25, block 333).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. The gap this answers: "the reset is a stub". world.py (block 318/319's
builder, Session; UCRT rand bridge from block 332) supplies the image, the IAT traps and the named bridges. No application stub
and no stop boundary. shipped_pack.py binds the battle_pack tables by shipped code (the heap-6 binders skipped).
Fixtures: four idle objects (the convention of the world's nine), the unit pool [0208E688] / [0208E6A0] (stride 0xF50) holding
the installed unit, the unit's +0x10 handle object (a zeroed block: the rekey resolves through q[unit+0x10], and its generation
bump 002659D0 has no null guard - EXP-151), the unit's flag qword and the master flag d[02089300].
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
INSTALL, RESET, REKEY, PULSE, TRACK = 0x23A570, 0x236A60, 0x322050, 0x2FEAB0, 0x328FF0
W.ALLOWED |= {0x16D6A0} | W.closure(INSTALL) | SP.allowed(W)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
made, skipped = SP.bind(W, S)
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
POOL, HANDLE, MASTER = 0x76280000, 0x76290000, 0x2089300
STATS_BLOCK = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF190, 8)))[0]
TRACKED = 0x2EC1380

ev = {}
for a, nm, regs in ((RESET, "reset", (UC_X86_REG_RCX,)), (REKEY, "rekey", (UC_X86_REG_RCX,)), (PULSE, "pulse", (UC_X86_REG_RCX,)),
                    (TRACK, "track", (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8))):
    def on(u, addr, n, _, nm=nm, regs=regs):
        ev.setdefault(nm, []).append(["%X" % (u.reg_read(x) & 0xFFFFFFFF) for x in regs])
    uc.hook_add(UC_HOOK_CODE, on, begin=a, end=a)


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def unit(flags=0, stats=0):
    uc.mem_write(POOL, bytes(0xF50 * 2))
    uc.mem_write(HANDLE, bytes(0x100))
    w(POOL, "<Q", flags)
    w(POOL + 0x10, "<Q", HANDLE)
    w(POOL + 0x698, "<Q", stats)
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", 2)


def install(uid, master=1):
    w(MASTER, "<I", master)
    ev.clear()
    ok = S.call(INSTALL, POOL, uid)
    return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- I4 / I8: party installs over the shipped party rows ----
party = {}
for row in (0, 3, 5):
    unit()
    w(POOL + 0xEAC, "<QQ", 0x1111111111111111, 0x2222222222222222)
    ok, v = install(row)
    party[row] = {"ok": ok, "returned": v, "stats": "%X" % r(POOL + 0x698, "<Q")[0], "want": "%X" % (STATS_BLOCK + 8 + row * 0x1C8),
                  "spawn_6A0": "%X" % r(POOL + 0x6A0, "<Q")[0], "flags": "%016X" % r(POOL, "<Q")[0],
                  "EAC": "%X" % r(POOL + 0xEAC, "<Q")[0], "EB4": "%X" % r(POOL + 0xEB4, "<Q")[0],
                  "reset": len(ev.get("reset", [])), "pulse": ev.get("pulse", [])}
p_ok = all(v["ok"] and v["returned"] == 1 and v["stats"] == v["want"] and v["spawn_6A0"] == "0" and int(v["flags"], 16) >> 2 & 1
           and v["EAC"] == "0" and v["EB4"] == "2222222222222222" and v["reset"] == 1 and len(v["pulse"]) == 1 for v in party.values())
record("I4_I8_party_install", p_ok, rows=party,
       note="ids 0x0000 / 0x0003 / 0x0005: the installer returns 1, +0x698 = q[02EBF190] + 8 + row*0x1C8 (the shipped party rows), "
            "+0x6A0 = 0, flag bit 2 set; the reset runs once and the pulse reset 002FEAB0 zeroes exactly the qword at +0xEAC "
            "(+0xEB4 survives)")

# ---- I2: the reset precedes the master-enable rejection ----
ALL = 0xFFFFFFFFFFFFFFEB                                       # all ones except bit 2 (would read an old id first) and bit 4
unit(flags=ALL, stats=STATS_BLOCK + 8)                         # (00236A6F: gates the cleanup call 003105D0 - off here)
w(POOL + 0xEAC, "<Q", 0x3333333333333333)
ok, v = install(0, master=0)
i2 = {"ok": ok, "returned": v, "flags_after": "%016X" % r(POOL, "<Q")[0], "EAC_after": "%X" % r(POOL + 0xEAC, "<Q")[0],
      "reset": len(ev.get("reset", [])), "pulse": len(ev.get("pulse", [])), "stats_after": "%X" % r(POOL + 0x698, "<Q")[0]}
record("I2_reset_then_master_reject", ok and v == 0 and i2["reset"] == 1 and i2["pulse"] == 0 and i2["EAC_after"] == "3333333333333333"
       and i2["flags_after"] != "%016X" % ALL, result=i2,
       note="master flag 0: the reset runs (flags masked to %s), then the installer returns 0; +0xEAC survives because only the success "
            "path's pulse reset clears it" % i2["flags_after"])

# ---- I1: a class above 1 clears bit 26 only, and returns 0 ----
unit(flags=ALL, stats=STATS_BLOCK + 8)
ok, v = install(0x0203)
reset_flags = None
f_after = r(POOL, "<Q")[0]
i1 = {"ok": ok, "returned": v, "flags_after": "%016X" % f_after, "rekey": ev.get("rekey", []), "bit26": f_after >> 26 & 1,
      "bit42": f_after >> 42 & 1}
record("I1_other_class_clears_bit26", ok and v == 0 and i1["bit26"] == 0 and len(i1["rekey"]) == 1, result=i1,
       note="class 2 (id 0x0203): the rekey runs (a nonzero class byte), then the class dispatch clears bit 26 and returns 0 - class 2 "
            "can rekey and then fail (I3)")

# ---- I3: rekey selection ----
rk = {}
for label, uid, old in (("class 0, fresh unit", 0x0003, None), ("class 0, old id 0x0005", 0x0003, 0x0005),
                        ("class 0, old id = incoming", 0x0003, 0x0003), ("teardown 0xFFFF, old id 0x0005", 0xFFFF, 0x0005)):
    if old is None:
        unit()
    else:
        st = STATS_BLOCK + 8 + 5 * 0x1C8
        unit(flags=1 << 2, stats=st)
        w(st + 4, "<H", old)
    ok, v = install(uid)
    rk[label] = {"ok": ok, "returned": v, "rekey_calls": len(ev.get("rekey", []))}
record("I3_rekey_selection", rk["class 0, fresh unit"]["rekey_calls"] == 0 and rk["class 0, old id 0x0005"]["rekey_calls"] == 1
       and rk["class 0, old id = incoming"]["rekey_calls"] == 0 and all(v["ok"] for v in rk.values()), cases=rk,
       note="class byte 0: no rekey for a fresh unit or when the saved old id equals the incoming one; a different saved old id rekeys")

# ---- I7: tracked-HP registration is conditional ----
unit()
uc.mem_write(TRACKED, b"\xAA" * 0x60)
install(0x0003)
tr = {"calls": ev.get("track", []), "table_changed": bytes(uc.mem_read(TRACKED, 0x60)) != b"\xAA" * 0x60}
record("I7_party_path_registers_nothing", tr["calls"] == [] and not tr["table_changed"], result=tr,
       note="a party install makes NO 00328FF0 call and leaves the tracked table 02EC1380 untouched; I7's conditional write belongs to "
            "the enemy path, which this harness does not reach (its tables are not in battle_pack)")

json.dump({"ok": allok, "bound": made, "not_bound": skipped, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
