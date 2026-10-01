"""S-48: execute CONTRACT-authored-command-ramp-channels.md's six entries - the reset 003B6890, the four setters (003B6A90
class 0x0D, 003B69B0 0x0E, 003B6A10 0x0F, 003B6950 0x10) and the per-tick advance 003B5890 - as shipped code in one persistent
world, and test its section 2/3/4 properties (OPUS, 2026-09-25, block 321).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's world builder, plus Session: build once,
call many) - no application stub, imports only through named bridges. ONE ALLOCATION IS REPLACED BY A FIXTURE: the reset
allocates the 0x8C00-byte table (160 x 0xE0) from engine heap 6 (003B68A7 0036C1D0, 003B68B1 0036A100); that heap belongs to
the engine's boot and is not built, and its allocator halts (0036C000: jmp 0036C000). So [02B40528] is planted to a 0x8C00
buffer and 003B6890 takes its own already-allocated path and runs its reset body.
Writes result.json next to this file.
"""
import json
import os
import struct

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
RESET, ADVANCE = 0x3B6890, 0x3B5890
SET = {"0D": 0x3B6A90, "0E": 0x3B69B0, "0F": 0x3B6A10, "10": 0x3B6950}
TABLE_CELL, GATE = 0x2B40528, 0x2B40524
W.ALLOWED |= {0x16D6A0}
for f in (RESET, ADVANCE) + tuple(SET.values()):
    W.ALLOWED |= W.closure(f)
S = W.Session(FX["fixes"], FX["inits"])
TABLE = 0x76380000                              # inside the fixture region
S.uc.mem_write(TABLE, bytes(0x8C00))
S.uc.mem_write(TABLE_CELL, struct.pack("<Q", TABLE))


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def rdf(a):
    return struct.unpack("<f", bytes(S.uc.mem_read(a, 4)))[0]


def rec(slot):
    return TABLE + slot * 0xE0


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-32s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# the reset
S.uc.mem_write(TABLE, b"\xFF" * 0x8C00)
ok = S.call(RESET)
en = [S.uc.mem_read(rec(i) + 0x40, 1)[0] & 1 for i in range(160)]
record("reset_003B6890", ok, enable_bits_after=sum(en), gate=struct.unpack("<I", bytes(S.uc.mem_read(GATE, 4)))[0],
       note="the reset runs to its return over the planted table")


def fresh(slot, gen=0x12):
    S.uc.mem_write(rec(slot), bytes(0xE0))
    S.uc.mem_write(rec(slot) + 0x10, struct.pack("<I", (gen << 8) | slot))
    return (gen << 8) | slot


# 1. the identity guard writes nothing
sid = fresh(7)
before = bytes(S.uc.mem_read(rec(7), 0xE0))
wrong = (0x99 << 8) | 7
S.uc.mem_write(0x76390000, struct.pack("<ff", 3.0, 4.0))
okg = all(S.call(SET[k], wrong, 10, 0x76390000, xmm={2: 5.0}) for k in SET)
record("P1_identity_guard_writes_nothing", okg and bytes(S.uc.mem_read(rec(7), 0xE0)) == before,
       note="a wrong generation in the id: all four setters return with the record byte-identical")

# 2. steps == 0 is immediate and clears the counter (single channel 0x0E: counter +0x01, value +0x70, delta +0x74)
sid = fresh(9)
S.call(SET["0E"], sid, 50, 0, xmm={2: 100.0})
c_mid = S.uc.mem_read(rec(9) + 1, 1)[0]
S.call(SET["0E"], sid, 0, 0, xmm={2: 7.5})
p2 = c_mid == 50 and S.uc.mem_read(rec(9) + 1, 1)[0] == 0 and rdf(rec(9) + 0x70) == 7.5
record("P2_steps_zero_is_immediate", p2, counter_mid=c_mid, value_after=rdf(rec(9) + 0x70),
       note="an in-flight 50-step ramp is cancelled: counter 0, value = target")

# 3. the delta, and the value is never clamped: run a 3-step ramp to its end through the advance
sid = fresh(11)
S.uc.mem_write(rec(11) + 0x40, bytes([1, 0]))
S.uc.mem_write(GATE, struct.pack("<I", 0))
S.uc.mem_write(rec(11) + 0x70, struct.pack("<f", 0.0))
S.call(SET["0E"], sid, 3, 0, xmm={2: 1.0})
delta = rdf(rec(11) + 0x74)
recip = f32(f32(1.0) / 3.0)
want_mul = f32(f32(1.0 - 0.0) * recip)
want_div = f32(1.0 / 3.0)
vals = []
for _ in range(4):
    S.call(ADVANCE)
    vals.append(rdf(rec(11) + 0x70))
final_exact = vals[2]
p3 = delta == want_mul and S.uc.mem_read(rec(11) + 1, 1)[0] == 0 and vals[2] == vals[3]
record("P3_delta_and_no_clamp", p3, delta=repr(delta), reciprocal_product=repr(want_mul), true_quotient=repr(want_div),
       values=[repr(v) for v in vals], note="delta = (target - value) * (1/steps); after 3 ticks the counter is 0 and the value "
                                            "stays where the additions left it (%r vs target 1.0)" % final_exact)

# 3b. a landing that is NOT exact (0 -> 0.1 in 3 steps), and the delta formula: reciprocal product vs true quotient (0 -> 0.3)
def ramp(slot, target, steps, ticks):
    sid = fresh(slot)
    S.uc.mem_write(rec(slot) + 0x40, bytes([1, 0]))
    S.uc.mem_write(rec(slot) + 0x70, struct.pack("<f", 0.0))
    S.call(SET["0E"], sid, steps, 0, xmm={2: target})
    d = rdf(rec(slot) + 0x74)
    for _ in range(ticks):
        S.call(ADVANCE)
    return d, rdf(rec(slot) + 0x70), S.uc.mem_read(rec(slot) + 1, 1)[0]


d01, v01, c01 = ramp(19, f32(0.1), 3, 5)
d03, v03, c03 = ramp(21, f32(0.3), 3, 0)
mul03, div03 = f32(f32(0.3) * f32(1.0 / 3)), f32(f32(0.3) / 3)
record("P3b_inexact_landing_and_reciprocal", v01 != f32(0.1) and c01 == 0 and d03 == mul03 and d03 != div03,
       landing_0p1=[repr(d01), repr(v01), c01], delta_0p3=repr(d03), reciprocal_product=repr(mul03), true_quotient=repr(div03),
       note="0 -> 0.1 in 3 steps ends at %r, not 0.1 (no clamp); the 0 -> 0.3 delta is the RECIPROCAL product %r, not the "
            "quotient %r the contract's (target - value) / steps gives" % (v01, mul03, div03))

# 4. a paused slot (or the global gate) does not accumulate
sid = fresh(13)
S.uc.mem_write(rec(13) + 0x40, bytes([1, 1]))                 # enabled, paused
S.uc.mem_write(rec(13) + 0x70, struct.pack("<f", 0.0))
S.call(SET["0E"], sid, 4, 0, xmm={2: 8.0})
S.call(ADVANCE)
paused = (S.uc.mem_read(rec(13) + 1, 1)[0], rdf(rec(13) + 0x70))
S.uc.mem_write(rec(13) + 0x41, bytes([0]))
S.uc.mem_write(GATE, struct.pack("<I", 1))
S.call(ADVANCE)
gated = (S.uc.mem_read(rec(13) + 1, 1)[0], rdf(rec(13) + 0x70))
S.uc.mem_write(GATE, struct.pack("<I", 0))
S.call(ADVANCE)
running = (S.uc.mem_read(rec(13) + 1, 1)[0], rdf(rec(13) + 0x70))
record("P4_paused_does_not_accumulate", paused == (4, 0.0) and gated == (4, 0.0) and running == (3, 2.0),
       paused=paused, global_gate=gated, running=running, note="paused or globally gated: counter and value unchanged; then one step")

# 5. counters are bytes: 255 steps
sid = fresh(15)
S.call(SET["0E"], sid, 255, 0, xmm={2: 255.0})
record("P5_byte_counter", S.uc.mem_read(rec(15) + 1, 1)[0] == 255, note="steps 255 stores 255 in the byte counter")

# section 3: the advance order 0, 2, 1, 3, 0x43 and the channel layout (pair channels get two components)
sid = fresh(17)
S.uc.mem_write(rec(17) + 0x40, bytes([1, 0]))
S.uc.mem_write(0x76390000, struct.pack("<ff", 10.0, 20.0))
S.call(SET["0D"], sid, 2, 0x76390000)
S.call(SET["0F"], sid, 2, 0x76390000)
S.call(SET["10"], sid, 2, 0, xmm={2: 6.0})
S.call(SET["0E"], sid, 2, 0, xmm={2: 4.0})
S.uc.mem_write(rec(17) + 0x43, bytes([2]))
S.uc.mem_write(rec(17) + 0x9C, struct.pack("<f", 0.5))
S.call(ADVANCE)
lay = {"c00": S.uc.mem_read(rec(17), 1)[0], "v50": rdf(rec(17) + 0x50), "v54": rdf(rec(17) + 0x54),
       "c02": S.uc.mem_read(rec(17) + 2, 1)[0], "v58": rdf(rec(17) + 0x58), "v5C": rdf(rec(17) + 0x5C),
       "c01": S.uc.mem_read(rec(17) + 1, 1)[0], "v70": rdf(rec(17) + 0x70), "c03": S.uc.mem_read(rec(17) + 3, 1)[0],
       "v78": rdf(rec(17) + 0x78), "c43": S.uc.mem_read(rec(17) + 0x43, 1)[0], "v98": rdf(rec(17) + 0x98)}
lay_ok = lay == {"c00": 1, "v50": 5.0, "v54": 10.0, "c02": 1, "v58": 5.0, "v5C": 10.0, "c01": 1, "v70": 2.0, "c03": 1, "v78": 3.0,
                 "c43": 1, "v98": 0.5}
record("S2_S3_channel_layout", lay_ok, after_one_tick=lay,
       note="classes 0x0D/0x0F drive pairs +0x50/+0x54 and +0x58/+0x5C, 0x0E +0x70, 0x10 +0x78; the fifth channel (+0x43, +0x98) "
            "advances with no setter")
json.dump({"ok": allok, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
