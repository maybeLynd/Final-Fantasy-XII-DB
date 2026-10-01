"""S-32: execute the gil setter 00254EE0, the getter 00253690 and its thunk 00309BF0, and the console writer 003058B0
(CONTRACT-gil-storage-and-movement.md GL-1..GL-5) as shipped code, with the meter 00316A50 real (OPUS, 2026-09-25, block 347).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; UCRT rand bridge from block
332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack by shipped code. No application
stub and no stop boundary. Fixtures: six idle objects at 0x76300000 (the world's convention): [02092758] is the game state holding
gil at +8, [020927C0] the block the meter's counters live in.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RIP

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
SET, GET, GET_THUNK, DEBUG_MAX, METER = 0x254EE0, 0x253690, 0x309BF0, 0x3058B0, 0x316A50
W.ALLOWED |= ({0x16D6A0, SET, GET} | SP.allowed(W) | set().union(*(W.closure(f) for f in (SET, GET, GET_THUNK, DEBUG_MAX))))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
made, skipped = SP.bind(W, S)
IDLE = 0x76300000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
STATE, COUNTERS = IDLE + 4 * 0x20000, IDLE + 5 * 0x20000
GIL = STATE + 8


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


ev = {"meter": [], "gil_stores": [], "counter_writes": []}
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: ev["meter"].append([u.reg_read(UC_X86_REG_RCX) & 0xFF, u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF]),
            begin=METER, end=METER)
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: ev["gil_stores"].append(["%08X" % u.reg_read(UC_X86_REG_RIP), v & 0xFFFFFFFF]),
            begin=GIL, end=GIL + 3)
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: ev["counter_writes"].append(["+%X" % (a - COUNTERS), n, v & 0xFFFFFFFF]),
            begin=COUNTERS, end=COUNTERS + 0x1FFFF)


def put(old, arg, fn=SET):
    w(GIL, "<i", old)
    for k in ev:
        ev[k] = []
    ok = S.call(fn, arg & 0xFFFFFFFF) if fn == SET else S.call(fn)
    return {"ok": ok, "stored": r(GIL, "<i")[0], "meter": list(ev["meter"]), "stores": list(ev["gil_stores"]),
            "counter_writes": list(ev["counter_writes"])}


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


CAP = 99999999
g1 = {}
for old, arg in ((100, -5), (100, 0), (100, CAP), (100, CAP + 1), (100, 0x7FFFFFFF), (100, -0x80000000), (0, 12345)):
    g1["old %d, set %d" % (old, arg)] = put(old, arg)
want = {"old 100, set -5": 0, "old 100, set 0": 0, "old 100, set 99999999": CAP, "old 100, set 100000000": CAP,
        "old 100, set 2147483647": CAP, "old 100, set -2147483648": 0, "old 0, set 12345": 12345}
record("GL1_clamp_in_the_setter", all(v["ok"] and v["stored"] == want[k] and [s[0] for s in v["stores"]] == ["00254F1F"] for k, v in g1.items()),
       cases={k: {"stored": v["stored"], "stores": v["stores"], "meter": v["meter"]} for k, v in g1.items()},
       note="every write lands once at 00254F1F, clamped to [0, 99,999,999]: -5 -> 0, 100,000,000 -> 99,999,999, 0x7FFFFFFF -> "
            "99,999,999, -0x80000000 -> 0")

g2 = {"gain 100 -> 250": put(100, 250), "spend 250 -> 100": put(250, 100), "zero 400 -> 400": put(400, 400)}
record("GL2_GL4_meter_kind_and_zero_delta", g2["gain 100 -> 250"]["meter"] == [[6, 150]] and g2["spend 250 -> 100"]["meter"] == [[7, 150]]
       and g2["zero 400 -> 400"]["meter"] == [] and [s[0] for s in g2["zero 400 -> 400"]["stores"]] == ["00254F1F"]
       and g2["zero 400 -> 400"]["stored"] == 400, cases=g2,
       note="a gain meters kind 6 with |delta|, a spend kind 7 with |delta|; a zero delta calls no meter and STILL stores")
g3 = put(0, 200000000)
record("GL3_delta_before_clamp", g3["meter"] == [[6, 200000000]] and g3["stored"] == CAP, case=g3,
       note="old 0, set 200,000,000: the meter records a gain of 200,000,000 while 99,999,999 is stored")
g2d = put(5, 0, fn=DEBUG_MAX)
record("GL2_console_writer_is_metered", g2d["ok"] and g2d["meter"] == [[6, CAP - 5]] and g2d["stored"] == CAP, case=g2d,
       note="Debug_SetGilToMaximum 003058B0 (`mov ecx, 99,999,999; jmp 00254EE0`) from 5: metered as a gain of 99,999,994, like "
            "any other writer")

w(GIL, "<i", 4242)
ok_a = S.call(GET)
va = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
ok_b = S.call(GET_THUNK)
vb = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
thunk = bytes(uc.mem_read(GET_THUNK, 5))
record("GL5_two_getter_entries", ok_a and ok_b and va == vb == 4242 and thunk[0] == 0xE9
       and (GET_THUNK + 5 + struct.unpack("<i", thunk[1:])[0]) == GET, getter=va, thunk_value=vb, thunk_bytes=thunk.hex(),
       note="00253690 and the 5-byte thunk 00309BF0 (`jmp 00253690`) both return the stored 4242")

g_wrap = put(100, -0x80000000)
record("delta_wraps_to_a_metered_gain", g_wrap["ok"] and g_wrap["meter"] == [[6, 2147483548]] and g_wrap["stored"] == 0, case=g_wrap,
       note="old 100, set -2,147,483,648: `sub edx, [rax+8]` wraps to +0x7FFFFF9C, so the write is METERED AS A GAIN (kind 6) of "
            "2,147,483,548 while 0 is stored - GL-4's 'a negative one ... kind 7' does not hold at the 32-bit edge")

uc.mem_write(COUNTERS + 0x3848, bytes(0x40))
sat = []
for old, arg in ((0, 1000000000), (0, 1500000000), (500, 200)):
    v = put(old, arg)
    sat.append({"old": old, "set": arg, "meter": v["meter"], "gain_counter": r(COUNTERS + 0x3860, "<I")[0],
                "spend_counter": r(COUNTERS + 0x3864, "<I")[0]})
record("meter_counters_accumulate_and_saturate", [x["gain_counter"] for x in sat] == [1000000000, 0x7FFFFFFF, 0x7FFFFFFF]
       and [x["spend_counter"] for x in sat] == [0, 0, 300], steps=sat,
       note="from zeroed counters: gains of 1,000,000,000 and 1,500,000,000 leave the kind-6 counter at [020927C0]+0x3860 at "
            "1,000,000,000 then 0x7FFFFFFF (saturated, not wrapped); a spend of 300 lands in the kind-7 counter at +0x3864")

meter_effect = {k: v["counter_writes"] for k, v in (("gain", g2["gain 100 -> 250"]), ("spend", g2["spend 250 -> 100"]),
                                                     ("gain 200,000,000", g3))}
record("meter_counters_observed", all(meter_effect.values()), writes=meter_effect,
       note="the real meter 00316A50 writes the counter block [020927C0] on each metered write; the offsets and values are recorded "
            "(their meaning is not claimed)")

json.dump({"ok": allok, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
