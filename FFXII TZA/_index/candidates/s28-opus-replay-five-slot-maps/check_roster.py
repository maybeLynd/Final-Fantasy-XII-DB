"""S-28: execute CONTRACT-party-slot-assignment.md - the per-slot writer 00269C70, the bulk clears 002695A0 / 0026DB30, the pending-
mask consumer 0025BFB0 and the readers 00263750 / 00263770 - as shipped code, and test the slot <-> +0x12 invariant and its
exception (OPUS, 2026-09-25, block 338).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session) supplies the image, the IAT
traps and the named bridges. No application stub and no stop boundary.
Fixtures: four ActorStorageRecords (+0x12 slot, +0x0F state, +0xC0 secondary context - zeroed blocks), the roster array
0209A1F0 and the pending mask [02099ABC] where a case sets them; six idle objects (the world's convention).
Writes result_roster.json next to this file.
"""
import json
import os
import struct

from unicorn.x86_const import UC_X86_REG_RAX

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ASSIGN, CLEAR1, CLEAR2, CONSUME, READ, READ_OR_FOCUS = 0x269C70, 0x2695A0, 0x26DB30, 0x25BFB0, 0x263750, 0x263770
W.ALLOWED |= {0x16D6A0} | set().union(*(W.closure(f) for f in (ASSIGN, CLEAR1, CLEAR2, CONSUME, READ, READ_OR_FOCUS)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
ROSTER, MASK = 0x209A1F0, 0x2099ABC
RECS = [0x76300000 + i * 0x1000 for i in range(5)]
CTX = [0x76310000 + i * 0x1000 for i in range(5)]


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def fresh():
    uc.mem_write(ROSTER, bytes(32))
    for rec, ctx in zip(RECS, CTX):
        uc.mem_write(rec, bytes(0x200))
        uc.mem_write(ctx, bytes(0x400))
        w(rec + 0x12, "<B", 0xFF)
        w(rec + 0x0F, "<B", 3)
        w(rec + 0xC0, "<Q", ctx)


def call(fn, *args):
    ok = S.call(fn, *args)
    assert ok, (hex(fn), (S.st["bad"] or S.st["faults"])[:2])
    return uc.reg_read(UC_X86_REG_RAX)


def roster():
    return [RECS.index(p) if p in RECS else ("-" if p == 0 else "%X" % p) for p in r(ROSTER, "<4Q")]


def slots():
    return [r(rec + 0x12, "<b")[0] for rec in RECS]


def states():
    return [r(rec + 0x0F, "<B")[0] for rec in RECS]


def bijection():
    ro = r(ROSTER, "<4Q")
    ok = all(p == 0 or r(p + 0x12, "<b")[0] == i for i, p in enumerate(ro))
    ok &= all(not (0 <= r(rec + 0x12, "<b")[0] <= 3) or ro[r(rec + 0x12, "<b")[0]] == rec for rec in RECS)
    return ok


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- the per-slot writer: what it maintains and what it does not ----
fresh()
for i in range(4):
    call(ASSIGN, RECS[i], i)
a1 = {"roster": roster(), "slots": slots(), "states": states(), "bijection": bijection()}
call(ASSIGN, RECS[4], 2)                                   # assign record 4 over slot 2's occupant (record 2)
a2 = {"roster": roster(), "slots": slots(), "states": states(), "bijection": bijection(),
      "displaced_ctx_152": r(CTX[2] + 0x152, "<B")[0]}
fresh()
for i in range(4):
    call(ASSIGN, RECS[i], i)
call(ASSIGN, RECS[0], 3)                                   # move record 0 to slot 3 (over record 3)
a3 = {"roster": roster(), "slots": slots(), "states": states(), "bijection": bijection()}
fresh()
for i in range(4):
    call(ASSIGN, RECS[i], i)
call(ASSIGN, 0, 1)                                         # a null actor into slot 1
a4 = {"roster": roster(), "slots": slots(), "bijection": bijection()}
uc.mem_write(ROSTER + 0x38, bytes(8))
call(ASSIGN, RECS[1], 7)                                   # a slot past 3
a5 = {"roster": roster(), "slots": slots(), "states": states(), "roster_7": "%X" % r(ROSTER + 0x38, "<Q")[0]}
record("writer_keeps_its_own_side_only", a1["bijection"] and a1["roster"] == [0, 1, 2, 3] and a1["states"][:4] == [2, 2, 2, 2]
       and a2["roster"][2] == 4 and a2["slots"][4] == 2 and a2["slots"][2] == 2 and a2["states"][2] == 2 and not a2["bijection"]
       and a2["displaced_ctx_152"] == 1
       and a3["roster"] == ["-", 1, 2, 0] and a3["slots"][0] == 3 and a3["slots"][3] == 3 and not a3["bijection"]
       and a4["roster"] == [0, 1, 2, 3]
       and a5["roster"][1] == "-" and a5["slots"][1] == 7 and a5["states"][1] == 3 and a5["roster_7"] == "%X" % RECS[1],
       assign_0_to_3=a1, over_an_occupant=a2, move_record0_to_slot3=a3, null_into_slot1=a4, slot_7=a5,
       note="records 0..3 into slots 0..3: the bijection holds. Assigning over an occupant vacates the INCOMING record's old slot and "
            "resets it, but the DISPLACED occupant keeps +0x12 = its slot and +0x0F = 2 (only its context's +0x152 is set) - the "
            "writer itself breaks the bijection. A null actor stores nothing. Slot 7 passes the sign test and is STORED at "
            "roster[7], past the four-entry array, with +0x12 = 7 and +0x0F = 3")

# ---- the bulk clears break it and repair nothing ----
clr = {}
for label, fn in (("002695A0", CLEAR1), ("0026DB30", CLEAR2)):
    fresh()
    for i in range(4):
        call(ASSIGN, RECS[i], i)
    before = bytes(b"".join(bytes(uc.mem_read(rec, 0x200)) for rec in RECS))
    call(fn)
    after = bytes(b"".join(bytes(uc.mem_read(rec, 0x200)) for rec in RECS))
    clr[label] = {"roster": roster(), "slots_still": slots(), "records_untouched": before == after, "bijection": bijection()}
fresh()
for i in range(4):
    call(ASSIGN, RECS[i], i)
w(MASK, "<I", 1)
call(CONSUME)
clr["0025BFB0 (mask bit 0)"] = {"roster": roster(), "slots_still": slots(), "bijection": bijection()}
for i in range(4):
    call(ASSIGN, RECS[i], i)
w(MASK, "<I", 2)
call(CONSUME)
clr["0025BFB0 (mask bit 1 only)"] = {"roster": roster(), "slots_still": slots()}
record("bulk_clears_break_it", all(v["roster"] == ["-"] * 4 and v["slots_still"][:4] == [0, 1, 2, 3] and not v["bijection"]
                                   for k, v in clr.items() if k in ("002695A0", "0026DB30", "0025BFB0 (mask bit 0)"))
       and clr["002695A0"]["records_untouched"] and clr["0026DB30"]["records_untouched"]
       and clr["0025BFB0 (mask bit 1 only)"]["roster"] == [0, 1, 2, 3], cases=clr,
       note="002695A0, 0026DB30 and 0025BFB0's bit-0 arm zero the roster and touch no record: every former member keeps +0x12 = its "
            "slot, and the bijection is broken until each is assigned again; 0025BFB0 without bit 0 leaves the roster")

# ---- the readers ----
fresh()
for i in range(4):
    call(ASSIGN, RECS[i], i)
rd = {"slot 2": call(READ, 2) == RECS[2], "slot 5": call(READ, 5) & 0xFFFFFFFFFFFFFFFF}
record("readers", rd["slot 2"] and rd["slot 5"] == 0, results={k: str(v) for k, v in rd.items()},
       note="00263750 returns the occupant, NULL past slot 3")

json.dump({"ok": allok, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result_roster.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
