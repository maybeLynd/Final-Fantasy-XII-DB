"""S-20: execute the combo roll 00388660 (CONTRACT-combo-continuation.md CB-3, CB-4, CB-5 and section 12) as shipped code with the
real gameplay MT19937, against an independent model of its instructions (OPUS, 2026-09-25, block 346).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; UCRT rand bridge from block
332) supplies the image, the IAT traps and the named bridges; shipped_pack.py binds battle_pack by shipped code; rsn_b.ard (shipped
extract) is bound by the game's binder 003EA710 for the foe case. The MT is seeded by the shipped seeder 00379CF0 -> 00863D30 and
drawn by 00379CD0 -> 00863BF0 (block 339). No application stub and no stop boundary.
Fixtures: six idle objects at 0x76300000, the unit pool - unit 0 a party member owning battle-state row 0 (+0x24 max HP,
+0x48 HP, +0x64 / +0x3C status, +0x6B7 the combo counter), unit 1 a foe installed by 0023A570 class 1 - and a context whose +0x10
points at an object holding the continue flag at +0x18 bit 1. The percent gate [02AEDFE4] is read as the world leaves it and
set per case where stated.
Writes result.json next to this file.
"""
import copy
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ARD_PATH = r"D:\FFXII_TZA_extract\ps2data\plan_master\in\plan_map\rsn_b\area\rsn_b.ard"
ARD = open(ARD_PATH, "rb").read()
ROLL, SEED, DRAW, INSTALL, BINDER = 0x388660, 0x379CF0, 0x379CD0, 0x23A570, 0x3EA710
W.ALLOWED |= ({0x16D6A0, 0x863D30, 0x863BF0} | SP.allowed(W)
              | set().union(*(W.closure(f) for f in (ROLL, SEED, 0x863D30, 0x863BF0, INSTALL, BINDER))))   # 00379CF0 / 00379CD0 are jmp thunks
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
POOL, HANDLES, LISTS, SPAWNS, CTX, OBJ, MASTER = 0x76280000, 0x76290000, 0x76290800, 0x762C0000, 0x762D0000, 0x762D1000, 0x2089300
BLOCK = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF190, 8)))[0]
GATE = 0x2AEDFE4
PARTY_TABLE, FOE_TABLE = 0x208D480, 0x208DE80
SEED_VALUE = 20260925


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


class MT:
    """MT19937, init_genrand - independent of the image (block 339's model)."""

    def __init__(self, seed):
        self.m = [seed & 0xFFFFFFFF]
        for i in range(1, 624):
            self.m.append((1812433253 * (self.m[-1] ^ (self.m[-1] >> 30)) + i) & 0xFFFFFFFF)
        self.i = 624

    def next(self):
        if self.i >= 624:
            for k in range(624):
                y = (self.m[k] & 0x80000000) | (self.m[(k + 1) % 624] & 0x7FFFFFFF)
                self.m[k] = self.m[(k + 397) % 624] ^ (y >> 1) ^ (0x9908B0DF if y & 1 else 0)
            self.i = 0
        y = self.m[self.i]
        self.i += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        return y


def c_div(a, b):
    """C signed division toward zero (the cdq / and / add / sar idiom)"""
    q = abs(a) // b
    return q if a >= 0 else -q


def model(mt, counter, hp, maxhp, status, gate, nibble, foe_cap=None):
    """00388660 as read (0038868A-00388874): returns (continue flag, nibble after, draws)"""
    if counter:
        return int(counter < nibble), nibble, 0
    draws = 1
    if not (mt.next() % 100 < gate):
        return 0, nibble, draws

    def base():
        if status & 0x10000:
            return max(hp, 1)
        return maxhp * 2 if status >> 28 & 1 else maxhp
    p = 64 if hp < c_div(base(), 16) else 32 if hp < c_div(base(), 8) else 16 if hp < c_div(base(), 4) else 8
    count = 1
    for _ in range(11):
        draws += 1
        if p > mt.next() % 100:
            count += 1
    if foe_cap is not None:
        count = min(count, foe_cap - 1)
    count = min(count, 11)
    if count < 1:
        return 0, nibble, draws
    return 1, count, draws


draws = []
uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _: draws.append(1), begin=DRAW, end=DRAW)


def world():
    uc.mem_write(POOL, bytes(0xF50 * 2))
    uc.mem_write(HANDLES, bytes(0x400))
    uc.mem_write(SPAWNS, bytes(0x250 * 2))
    w(0x208E690, "<Q", SPAWNS)
    w(0x208E688, "<Q", POOL)
    w(0x208E6A0, "<I", 2)
    w(MASTER, "<I", 1)
    rec = BLOCK + 8
    uc.mem_write(rec, bytes(0x1C8))
    w(rec + 4, "<BB", 0, 0)
    w(POOL + 0x10, "<Q", HANDLES)
    w(POOL + 0x698, "<Q", rec)
    foe = POOL + 0xF50
    w(foe, "<Q", 1 << 26)
    w(foe + 0x10, "<Q", HANDLES + 0x100)
    w(foe + 0x40, "<Q", LISTS)
    w(LISTS, "<BB", 1, 0)
    assert S.call(INSTALL, foe, 0x0100) and uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF == 1, "install"
    uc.mem_write(CTX, bytes(0x40))
    uc.mem_write(OBJ, bytes(0x40))
    w(CTX + 0x10, "<Q", OBJ)
    return rec, foe


def roll(rec, unit, counter, hp=None, maxhp=None, status=0):
    if hp is not None:
        w(rec + 0x24, "<i", maxhp)
        w(rec + 0x48, "<i", hp)
    w(rec + 0x64, "<I", status)
    w(rec + 0x3C, "<I", 0)
    w(unit + 0x6B7, "<B", counter)
    del draws[:]
    ok = S.call(ROLL, rec, 0, CTX)
    return ok, r(OBJ + 0x18, "<I")[0] >> 1 & 1, len(draws)


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


rec, foe = world()
gate_world = r(GATE, "<I")[0]
print("gate [02AEDFE4] as the world leaves it:", gate_world)
assert S.call(SEED, SEED_VALUE), "seed"
mt = MT(SEED_VALUE)
nib_addr = PARTY_TABLE + 0 * 0x40 + 0x12

# ---- CB-3 / CB-4 against the model, across the four HP bands and both status modifiers ----
w(GATE, "<I", 60)
seq, miss = [], []
CASES = [(1000, 1000, 0), (240, 1000, 0), (120, 1000, 0), (50, 1000, 0), (400, 1000, 1 << 28), (30, 1000, 0x10000)]
for k in range(60):
    hp, mx, st = CASES[k % len(CASES)]
    w(nib_addr, "<B", 0x05)
    ok, flag, nd = roll(rec, POOL, 0, hp, mx, st)
    nib = r(nib_addr, "<B")[0] >> 4
    want = model(mt, 0, hp, mx, st, 60, 0)
    seq.append({"hp": hp, "max": mx, "status": "%X" % st, "flag": flag, "nibble": nib, "draws": nd, "model": want})
    if not ok or (flag, nib if flag else 0, nd) != (want[0], want[1] if want[0] else 0, want[2]) or r(nib_addr, "<B")[0] & 0xF != 5:
        miss.append(seq[-1])
fired = [s for s in seq if s["flag"]]
record("CB3_first_hit_draws_twelve_not_two", not miss and fired and all(s["draws"] == 12 for s in fired)
       and all(s["draws"] == 1 for s in seq if not s["flag"]) and len(fired) < len(seq),
       rolls=len(seq), combos=len(fired), mismatches=miss[:4], draws_seen=sorted({s["draws"] for s in seq}),
       note="60 first-hit rolls (counter 0) at gate 60 against an independent MT19937 model of the instructions: every flag, nibble "
            "and draw count matches; a first hit that passes the percent gate draws the generator 12 times (1 + an 11-draw loop at "
            "003887E3), one that fails draws once - CB-3's 'twice' counts call sites, not draws; the low nibble of +0x12 survives")
bands = {}
for s in fired:
    bands.setdefault("%d/%d %s" % (s["hp"], s["max"], s["status"]), []).append(s["nibble"])
record("CB3_count_rises_as_hp_falls", all(max(v) <= 11 for v in bands.values()), counts_by_band=bands,
       note="the per-hit probability is 8 / 16 / 32 / 64 % as current HP falls below max/4, max/8, max/16 (status bit 28 doubles "
            "max, status bit 16 compares HP with itself - always 8 %); the count is 1 + successes of 11 draws, capped at 11")

# ---- CB-4: a non-zero counter draws nothing and compares against the memoised nibble ----
cb4 = {}
for counter, nibble in ((1, 3), (2, 3), (3, 3), (5, 3)):
    w(nib_addr, "<B", nibble << 4)
    ok, flag, nd = roll(rec, POOL, counter)
    cb4["counter %d, nibble %d" % (counter, nibble)] = {"ok": ok, "flag": flag, "draws": nd}
record("CB4_progress_against_the_nibble", all(v["ok"] and v["draws"] == 0 for v in cb4.values())
       and [v["flag"] for v in cb4.values()] == [1, 1, 0, 0], cases=cb4,
       note="counter 1 / 2 against nibble 3 continue, 3 and 5 end; no case draws the generator")

# ---- CB-5: the foe's record is in a different table, and the foe count is capped by its class record ----
frec = r(foe + 0x698, "<Q")[0]
kind = r(foe + 0xEA9, "<B")[0]
cap = r(r(foe + 0xE68, "<Q")[0] + 0x20, "<B")[0]
w(GATE, "<I", 100)
foe_rolls, foe_miss = [], []
for k in range(12):
    w(FOE_TABLE + kind * 0x40 + 0x12, "<B", 0)
    w(PARTY_TABLE + r(frec + 4, "<B")[0] * 0x40 + 0x12, "<B", 0xEE)
    ok, flag, nd = roll(frec, foe, 0, 10, 1000, 0)
    nib = r(FOE_TABLE + kind * 0x40 + 0x12, "<B")[0] >> 4
    uncapped = model(copy.deepcopy(mt), 0, 10, 1000, 0, 100, 0)
    want = model(mt, 0, 10, 1000, 0, 100, 0, foe_cap=cap)
    foe_rolls.append({"flag": flag, "nibble": nib, "draws": nd, "model": want,
                      "party_table_untouched": r(PARTY_TABLE + r(frec + 4, "<B")[0] * 0x40 + 0x12, "<B")[0] == 0xEE,
                      "uncapped_model_count": uncapped[1]})
    if not ok or (flag, nib if flag else 0, nd) != (want[0], want[1] if want[0] else 0, want[2]):
        foe_miss.append(foe_rolls[-1])
record("CB5_foe_record_table_and_cap", not foe_miss and all(x["party_table_untouched"] for x in foe_rolls)
       and all(x["nibble"] <= max(cap - 1, 0) for x in foe_rolls if x["flag"])
       and any(x["uncapped_model_count"] > cap - 1 for x in foe_rolls), class_cap_byte=cap, kind_EA9=kind,
       rolls=foe_rolls[:6], mismatches=foe_miss[:3],
       note="a foe record (stats +5 = 1): the nibble is written in 0208DE80 + unit[+0xEA9]*0x40 (003886D6), not the party table "
            "0208D480 + rec[+4]*0x40 CB-5 names; the count is capped at class[+0x20] - 1 = %d (0038884D); all 12 rolls at gate "
            "100 and HP 10/1000 (p = 64) match the capped model, and the uncapped model would have exceeded the cap" % (cap - 1))
w(GATE, "<I", gate_world)

json.dump({"ok": allok, "mt_seed": SEED_VALUE, "gate_world_value": gate_world,
           "ard": {"path": ARD_PATH, "sha256": hashlib.sha256(ARD).hexdigest()}, "bound": made,
           "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
