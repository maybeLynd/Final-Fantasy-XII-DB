"""S-23: execute the HP write 00300530 (CONTRACT-hp-write-and-lethal-transition.md) with its REAL status transition 0030E360 and
recompute 0030FED0, and attribute every store to the target's +0x48 (OPUS, 2026-09-25, block 334).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. The exposure this answers (block 300, s23-runtime-per-invariant-exposure):
EXP-093 stubbed 0030FED0, which hid a second +0x48 store at 00310508. world.py (block 318/319's builder, Session; UCRT rand
bridge from block 332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack by shipped
code. No application stub and no stop boundary: the caller's flags word selects the presentation-free path the setter itself
offers - bit 1 skips the death credit 00469BB0 (0030059C), bit 4 skips 003283D0 and bit 7 skips the display 0028F1F0
(00300601); 0x50 are I7's target-HP bits. Fixtures: four idle objects, the unit pool [0208E688] / [0208E6A0] with the target's
owning unit (its +0x10 actor a zeroed block), the stats records (+0x48 HP, +0x24 max HP, +0x64 / +0x3C status words).
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RIP

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
HPWRITE, STATUS, RECOMP = 0x300530, 0x30E360, 0x30FED0
W.ALLOWED |= {0x16D6A0} | W.closure(HPWRITE) | SP.allowed(W)
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
POOL, SRC, TGT, ACTORS = 0x76280000, 0x76290000, 0x76291000, 0x762A0000
PRESENTATION = {0x469BB0: "death credit 00469BB0", 0x28F1F0: "display 0028F1F0", 0x3283D0: "003283D0"}
ev = {}
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: ev.setdefault("hp_stores", []).append(["%08X" % u.reg_read(UC_X86_REG_RIP),
                                                                                                  v & 0xFFFFFFFF]),
            begin=TGT + 0x48, end=TGT + 0x4B)
for a, nm in list(PRESENTATION.items()) + [(STATUS, "status 0030E360"), (RECOMP, "recompute 0030FED0")]:
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev.setdefault("entered", []).append(nm), begin=a, end=a)


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def world_units(hp, maxhp=500, status=0):
    uc.mem_write(POOL, bytes(0xF50 * 2))
    for i, st in enumerate((SRC, TGT)):
        uc.mem_write(st, bytes(0x400))
        w(st + 4, "<BB", i, 0)
        uc.mem_write(ACTORS + i * 0x1000, bytes(0x1000))
        w(POOL + i * 0xF50 + 0x10, "<Q", ACTORS + i * 0x1000)
        w(POOL + i * 0xF50 + 0x698, "<Q", st)
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", 2)
    w(TGT + 0x48, "<I", hp)
    w(TGT + 0x24, "<I", maxhp)
    w(TGT + 0x64, "<I", status)


def hp_write(delta, source=SRC, flags=0xD2):
    ev.clear()
    ok = S.call(HPWRITE, TGT, delta & 0xFFFFFFFF, source, flags)
    return ok, {"stores": ev.get("hp_stores", []), "entered": sorted(set(ev.get("entered", []))), "hp_after": r(TGT + 0x48, "<i")[0],
                "ko_bit": r(TGT + 0x64, "<I")[0] & 1}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


cases = {}
for label, hp, delta, src in (("lethal, source present", 100, -150, SRC), ("lethal, null source", 100, -150, 0),
                              ("non-lethal", 100, -30, SRC), ("heal past the cap", 480, 50, SRC)):
    world_units(hp)
    ok, res = hp_write(delta, src)
    cases[label] = dict(ok=ok, **res)
lethal = [cases["lethal, source present"], cases["lethal, null source"]]
record("second_store_on_the_lethal_path", all(c["ok"] and [s[0] for s in c["stores"]] == ["00300749", "00310508"] and c["ko_bit"] == 1
                                              and "recompute 0030FED0" in c["entered"] and not set(c["entered"]) & set(PRESENTATION.values())
                                              for c in lethal), lethal=lethal,
       note="one lethal call of 00300530 stores +0x48 TWICE: its own store at 00300749, then 0030E360 (KO bit 0, mode 3) reaches the "
            "recompute 0030FED0, which stores +0x48 again at 00310508; the KO bit is set and no presentation call runs")
nl, heal = cases["non-lethal"], cases["heal past the cap"]
record("single_store_without_a_status_transition", nl["ok"] and [s[0] for s in nl["stores"]] == ["00300749"] and nl["hp_after"] == 70
       and heal["ok"] and [s[0] for s in heal["stores"]] == ["00300749"] and heal["hp_after"] == 500,
       non_lethal=nl, heal_past_cap=heal,
       note="100 - 30 and 480 + 50 (cap 500): one store each, at 00300749 (70; clamped to 500) - no status transition, no recompute")
record("bound_holds_after_every_store", all(0 <= s[1] <= 500 for c in cases.values() for s in c["stores"]),
       note="every stored value lies in [floor 0, cap 500] - the second store clamps as well")

json.dump({"ok": allok, "bound": made, "not_bound": skipped, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
