"""S-28: execute CONTRACT-the-five-parallel-slot-maps.md - the initialiser 00329CC0, the refresher 003266C0 and the resolver
0031B9F0 - as shipped code over the shipped tables, and test SM-1..SM-5 and SM-8 (OPUS, 2026-09-25, block 338).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. The S-28 exposure note (block 301): "all of slot-assignment, SM-1..SM-8
and BS-1..BS-5" unexecuted. world.py (block 318/319's builder, Session; named CRT bridges) supplies the image, the IAT traps and
the named bridges; shipped_pack.py binds battle_pack by shipped code. No application stub and no stop boundary.
Fixtures: six idle objects (the world's convention); map 0 selectors planted where a case sets them.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn.x86_const import UC_X86_REG_RAX

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
INIT, REFRESH, RESOLVE = 0x329CC0, 0x3266C0, 0x31B9F0
W.ALLOWED |= {0x16D6A0} | SP.allowed(W) | set().union(*(W.closure(f) for f in (INIT, REFRESH, RESOLVE)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
for fam in range(15):                                   # the inventory handlers the id family table reaches by `jmp rax`
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
SOURCE = 0x1EED260                                    # the authored 9-byte table 00329CE1 addresses


def maps():
    return [list(struct.unpack("<9H", bytes(uc.mem_read(m, 18)))) for m in MAPS]


def run(fn, *args):
    ok = S.call(fn, *args)
    assert ok, (hex(fn), (S.st["bad"] or S.st["faults"])[:2])
    return uc.reg_read(UC_X86_REG_RAX) & 0xFF


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- SM-4 / SM-8: the initialiser, over a zeroed map region and over stale selectors ----
src = bytes(uc.mem_read(SOURCE, 9))
sm4 = {}
for label, fill in (("zeroed maps", 0x00), ("stale selectors 5A5A", 0x5A)):
    uc.mem_write(BLOCK + 0x5A48, bytes([fill]) * 0x60)
    run(INIT)
    m = maps()
    sm4[label] = {"map0": ["%04X" % x for x in m[0]], "maps_1_4_equal_map0": all(m[k] == m[0] for k in range(1, 5)),
                  "word_5AA4": struct.unpack("<I", bytes(uc.mem_read(BLOCK + 0x5AA4, 4)))[0]}
z, s = sm4["zeroed maps"], sm4["stale selectors 5A5A"]
want_z = ["%04X" % (0xFFFF if b == 0xFF else b) for b in src]
record("SM4_SM8_born_identical", z["map0"] == want_z and z["maps_1_4_equal_map0"] and z["word_5AA4"] == src[0]
       and s["maps_1_4_equal_map0"] and s["map0"][1:] == ["5A5A"] * 8, source_table=src.hex(), cases=sm4,
       note="over zeroed maps 00329CC0 writes map 0 from the authored table 01EED260 (0xFF -> FFFF) and copies it into maps 1-4; "
            "+0x5AA4 holds the table's first byte. For a 0xFF table entry it writes FFFF only after releasing the member the OLD "
            "selector names, and skips the write when that old low byte is above 0x27 - a stale 5A5A survives, and is copied")

# ---- SM-5: the refresher - map 3 copied before the clear, maps 2 and 4 from the cleared map 1 ----
sel = [0x0100, 0x0101, 0x0102, 0x0103, 0x0104, 0x0105, 0x0106, 0x0107, 0x0108]
uc.mem_write(MAPS[0], struct.pack("<9H", *sel))
for k in range(1, 5):
    uc.mem_write(MAPS[k], b"\x11" * 18)
ok_r = S.call(REFRESH)
m = maps()
cleared = sel[:4] + [0xFFFF] * 5
sm5 = m[3][:9] == sel and m[1][:4] == sel[:4] and m[1][4:9] == [0xFFFF] * 5 and m[2][:9] == m[1][:9] and m[4][:9] == m[1][:9]
record("SM5_refresh_order", ok_r and sm5, maps_after=[["%04X" % x for x in mm] for mm in m],
       fault=(S.st["faults"] or S.st["bad"] or [None])[0],
       note="map 0 = 0100..0108: afterwards map 3 = map 0 (copied before the clear), map 1 keeps [0..3] and has [4..8] = FFFF, and "
            "maps 2 and 4 equal the cleared map 1")

# ---- SM-1 / SM-2 / SM-3: the resolver ----
uc.mem_write(MAPS[0], struct.pack("<9H", 0x1234, 0xFFFF, 0x00AB, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006))
res = {"class 0 id 0 (0x1234)": run(RESOLVE, 0, 0), "class 0 id 1 (0xFFFF)": run(RESOLVE, 1, 0), "class 0 id 2 (0x00AB)": run(RESOLVE, 2, 0),
       "class 0 id 8": run(RESOLVE, 8, 0), "class 0 id 9 (past the gate)": run(RESOLVE, 9, 0), "class 5": run(RESOLVE, 0, 5),
       "class 3 id 0": run(RESOLVE, 0, 3)}
record("SM1_SM2_SM3_resolver", res["class 0 id 0 (0x1234)"] == 0x34 and res["class 0 id 1 (0xFFFF)"] == 0xFF
       and res["class 0 id 2 (0x00AB)"] == 0xAB and res["class 0 id 8"] == 0x06 and res["class 0 id 9 (past the gate)"] == 0xFF
       and res["class 5"] == 0xFF and res["class 3 id 0"] == (m[3][0] & 0xFF),
       results={k: "%02X" % v for k, v in res.items()},
       note="the resolver returns the LOW byte of the u16 selector (0x1234 -> 34, empty FFFF -> FF); an id past the class-23 gate (9) "
            "and class 5 both return FF through the same epilogue; class 3 reads map 3")

json.dump({"ok": allok, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
