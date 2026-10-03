"""S-28: execute SM-6 / SM-7 of CONTRACT-the-five-parallel-slot-maps.md - the two selector-removal bodies
PartyConfiguration_RemoveSelector00To06 (00328B20) and ...07To25 (003288F0) - as shipped code, and observe what they leave in
map 0, maps 1-4 and the staging pair 022C2580 (OPUS, 2026-09-25, block 340).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session) supplies the image, the IAT
traps and the named bridges; shipped_pack.py binds battle_pack by shipped code. No application stub and no stop boundary.
Fixtures: map 0's selectors, sentinel-filled maps 1-4 and staging; six idle objects (the world's convention).
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
REMOVE_PARTY, REMOVE_GUEST, REFRESH = 0x328B20, 0x3288F0, 0x3266C0
W.ALLOWED |= {0x16D6A0} | SP.allowed(W) | set().union(*(W.closure(f) for f in (REMOVE_PARTY, REMOVE_GUEST, REFRESH)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
for fam in range(15):
    for o in (0x48, 0x50):
        h = struct.unpack("<Q", bytes(uc.mem_read(0x1EEBCC0 + fam * 0x58 + o, 8)))[0]
        if h:
            W.ALLOWED |= {h} | W.closure(h)
made, skipped = SP.bind(W, S)
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
BLOCK = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF190, 8)))[0]
MAPS = [BLOCK + 0x5A48 + 0x12 * k for k in range(5)]
STAGING = 0x22C2580
calls = []
for a, nm in ((0x323540, "00323540"), (0x3261D0, "003261D0"), (REFRESH, "refresh 003266C0")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: calls.append(nm), begin=a, end=a)


def maps():
    return [["%04X" % x for x in struct.unpack("<9H", bytes(uc.mem_read(m, 18)))] for m in MAPS]


def setup(map0):
    uc.mem_write(MAPS[0], struct.pack("<9H", *map0))
    for k in range(1, 5):
        uc.mem_write(MAPS[k], struct.pack("<9H", *[0x0200 + k] * 9))
    uc.mem_write(STAGING, b"\x11" * 0x12)


def remove(fn, mid):
    del calls[:]
    ok = S.call(fn, mid)
    return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


setup([0, 1, 2, 3, 4, 5, 6, 0xFFFF, 0xFFFF])
okp, rp = remove(REMOVE_PARTY, 2)
mp = maps()
staged = ["%04X" % x for x in struct.unpack("<9H", bytes(uc.mem_read(STAGING, 18)))]
cp = list(calls)
setup([0, 1, 2, 3, 0x0C, 0x0D, 0xFFFF, 0xFFFF, 0xFFFF])
okg, rg = remove(REMOVE_GUEST, 0x0C)
mg = maps()
cg = list(calls)
refreshed = lambda m: m[3] == m[0] and m[1][:4] == m[0][:4] and m[1][4:] == ["FFFF"] * 5 and m[2] == m[1] and m[4] == m[1]
record("SM7_removal_refreshes_all_five", okp and rp == 0 and okg and rg == 0 and cp == cg == ["00323540", "003261D0", "refresh 003266C0"]
       and mp[0] == ["0000", "0001", "0003", "FFFF", "0004", "0005", "0006", "FFFF", "FFFF"] and refreshed(mp)
       and mg[0] == ["0000", "0001", "0002", "0003", "000D", "FFFF", "FFFF", "FFFF", "FFFF"] and refreshed(mg),
       party={"calls": cp, "maps": mp, "staging": staged}, guest={"calls": cg, "maps": mg},
       note="removing member 2 (00328B20) or guest 0x0C (003288F0): the entry is cleared in the STAGING copy at 022C2580, 003261D0 "
            "compacts and writes map 0 back (the active part closes up: 0,1,3,FFFF), and the refresher 003266C0 runs - maps 1-4 are "
            "rebuilt at once (map 3 = map 0, maps 1/2/4 = map 0 with [4..8] cleared). No stale window follows a removal")

rej = {}
for label, fn, mid in (("party 9", REMOVE_PARTY, 9), ("party 7", REMOVE_PARTY, 7), ("guest 6", REMOVE_GUEST, 6),
                       ("guest 0x1A", REMOVE_GUEST, 0x1A), ("party 5, not listed", REMOVE_PARTY, 5)):
    setup([0, 1, 2, 3, 4, 0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF])
    before = maps()
    ok, v = remove(fn, mid)
    rej[label] = {"returned": "%X" % v, "maps_unchanged": maps() == before, "calls": list(calls)}
record("SM7_range_and_absence_refused", all(v["returned"] == "FFFFFFFF" and v["maps_unchanged"] and v["calls"] == [] for v in rej.values()),
       cases=rej, note="an id outside the body's range (party 0..6, guest 7..0x19), or one map 0 does not list, returns -1 and writes nothing")

json.dump({"ok": allok, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
