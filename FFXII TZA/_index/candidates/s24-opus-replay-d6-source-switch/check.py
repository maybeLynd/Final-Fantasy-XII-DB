"""S-24 D-6 (OPUS, 2026-09-26): 'One authored boolean gates a base term and its matching equipment term together'
(CONTRACT-stat-derivation.md D-6), executed on the foe path of 002FEF30 with shipped data and shipped items.

Evidence class: NATIVE-REPLAY (unicorn), live_game false. World: block 342's (probe.py: world.py Session, battle_pack bound
by shipped code, rsn_b.ard bound by the game's binder 003EA710). No application stub, no stop boundary.
Fixtures: definition 0 of rsn_b (it ships +0x15 = 3); its +0x15 bits 0/1 are set per case in the bound copy and restored;
a real weapon and a real shield from the shipped item table (classified by 0031E9A0), equipped in the foe record's first
equipment word; the level span is 50 (0 -> 50), or 2 for the growth-column case.
Output bytes (found by differential, probe run): +0x2E attack, +0x32 parry, +0x33 block, +0x34 magick evade.
Cases:
 W  bit 0 clear: the weapon adds exactly its row +0x1A to attack and +0x1D to parry; bit 0 set: it adds nothing to either.
 S  bit 1 clear: the shield adds exactly its row +0x18 to block and +0x19 to magick evade; bit 1 set: nothing to either.
 X  each bit leaves the other kind alone: bit 1 set keeps the weapon's terms, bit 0 set keeps the shield's.
 C  the .ard base row's +0x2D / +0x2E / +0x02 / +0x03 feed attack / parry / block / magick evade only while the matching bit
    is set (+1 on each column moves each output by +1 with the bit set, and by 0 with it clear); a +1 on the growth row's
    +0x2E moves parry by the level span.
Writes result.json.
"""
import json
import os

import probe as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {"attack": 0x2E, "parry": 0x32, "block": 0x33, "mevade": 0x34}
n_items, kinds = P.items_by_kind()


def pick(kind, a, b):
    for iid, hx in kinds[kind]:
        row = bytes.fromhex(hx)
        if 0 < row[a] < 30 and 0 < row[b] < 30:
            return iid, row[a], row[b]


WPN, SHD = pick(1, 0x1A, 0x1D), pick(2, 0x18, 0x19)
NONE = (0xFFFF,) * 5
ok, _ = P.foe(0, 0, 50)
DEF, BASE, GROWTH = P.cap["def"], P.cap["base"], P.cap["growth"]
ORIG = P.r(DEF + 0x15, "<B")[0]


def run(bits, equip=NONE, hi=50, bump=None):
    P.w(DEF + 0x15, "<B", (ORIG & ~3) | bits)
    saved = []
    for row, off in (bump or []):
        v = P.r(row + off, "<B")[0]
        saved.append((row, off, v))
        P.w(row + off, "<B", v + 1)
    ok, b = P.foe(0, 0, hi, equip)
    for row, off, v in saved:
        P.w(row + off, "<B", v)
    P.w(DEF + 0x15, "<B", ORIG)
    return ok, {k: b[o] for k, o in OUT.items()}


def delta(a, b):
    return {k: b[k] - a[k] for k in OUT}


res, cases = {}, {}
eqW, eqS = (WPN[0],) + (0xFFFF,) * 4, (SHD[0],) + (0xFFFF,) * 4
allok = True
for bits in (0, 1, 2, 3):
    o0, n0 = run(bits)
    ow, nw = run(bits, eqW)
    os_, ns = run(bits, eqS)
    allok &= o0 and ow and os_
    res["bits%d" % bits] = {"none": n0, "weapon_delta": delta(n0, nw), "shield_delta": delta(n0, ns)}
W_ON = {"attack": WPN[1], "parry": WPN[2], "block": 0, "mevade": 0}
S_ON = {"attack": 0, "parry": 0, "block": SHD[1], "mevade": SHD[2]}
ZERO = dict.fromkeys(OUT, 0)
cases["W_bit0_clear_weapon_adds_its_row_terms"] = res["bits0"]["weapon_delta"] == W_ON and res["bits2"]["weapon_delta"] == W_ON
cases["W_bit0_set_weapon_adds_nothing"] = res["bits1"]["weapon_delta"] == ZERO and res["bits3"]["weapon_delta"] == ZERO
cases["S_bit1_clear_shield_adds_its_row_terms"] = res["bits0"]["shield_delta"] == S_ON and res["bits1"]["shield_delta"] == S_ON
cases["S_bit1_set_shield_adds_nothing"] = res["bits2"]["shield_delta"] == ZERO and res["bits3"]["shield_delta"] == ZERO
cases["X_each_bit_leaves_the_other_kind_alone"] = res["bits1"]["shield_delta"] == S_ON and res["bits2"]["weapon_delta"] == W_ON

cols = [(BASE, 0x2D), (BASE, 0x2E), (BASE, 0x02), (BASE, 0x03)]
_, b3 = run(3)
_, b3c = run(3, bump=cols)
_, b0 = run(0)
_, b0c = run(0, bump=cols)
_, g3 = run(3, hi=2)
_, g3c = run(3, hi=2, bump=[(GROWTH, 0x2E)])
_, g0 = run(0, hi=2)
_, g0c = run(0, hi=2, bump=[(GROWTH, 0x2E)])
res["columns"] = {"bits3_base_bump": delta(b3, b3c), "bits0_base_bump": delta(b0, b0c),
                  "bits3_growth2E_bump_span2": delta(g3, g3c), "bits0_growth2E_bump_span2": delta(g0, g0c)}
cases["C_base_columns_feed_the_outputs_only_with_the_bit_set"] = (res["columns"]["bits3_base_bump"] == dict.fromkeys(OUT, 1)
                                                                 and res["columns"]["bits0_base_bump"] == ZERO)
cases["C_growth_column_is_scaled_by_the_level_span"] = (res["columns"]["bits3_growth2E_bump_span2"] == {"attack": 0, "parry": 2, "block": 0, "mevade": 0}
                                                        and res["columns"]["bits0_growth2E_bump_span2"] == ZERO)
out = {"ok": bool(allok and all(cases.values())), "cases": cases, "runs": res, "ard_sha256": P.ARD_SHA,
       "definition": {"index": 0, "shipped_plus15": ORIG, "row": "%X" % DEF, "base_row": "%X" % BASE, "growth_row": "%X" % GROWTH},
       "weapon": {"id": "%04X" % WPN[0], "row+1A": WPN[1], "row+1D": WPN[2]},
       "shield": {"id": "%04X" % SHD[0], "row+18": SHD[1], "row+19": SHD[2]},
       "item_rows": n_items, "kinds": {str(k): len(v) for k, v in kinds.items()}}
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-62s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
