"""S-03: the battle runtime mode word's setters, reset, getters and save round trip executed as shipped code - the part of
CONTRACT-battle-runtime-mode.md that EXP-098 (the ladder composition, zero scripted boundaries) left unexecuted (OPUS, 2026-09-26).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. World: block 348's (probe.py: world.py Session, battle_pack bound by
shipped code - which also builds the battle state block [02EBF190]). No application stub.
STOP BOUNDARY (recorded, not stubbed): 0035C620, where the bit-0 setter tail-jumps after writing the bit; it reads +0x28 of a
null object in this world. The bit-0 write and the tail call's argument are asserted before it.
Cases:
 L  the ladder over all 16 values of the low nibble (field bit 15 as the bound tables leave it): the result is a priority -
    3 -> 5, 2 -> 4, 1 -> 2, 0 -> 1 else 0 (invariants 1/2); bits 4..31 set change nothing.
 P  the bit-3 and bit-2 setters: one write that sets / clears exactly the bit; no write when the bit already equals the argument.
 Z  the bit-0 setter: the same one write, then a tail jump to 0035C620 with edx = the new flags word; no write and no jump
    when equal.
 C  the bit-1 (chocobo) setter: enable writes flags |= 2, +0x5AE0 |= 0xC and +0x5AE4 = 180.0f and nothing else; disable writes
    flags &= ~2, calls 002E73C0(actor of roster slot 3, 3) and zeroes +0x5AEC; no effect when equal.
 R  the reset 0030DA10 zeroes +0x5B04 and +0x5B08.
 G  the bit getters return each bit; the mode getters 003072C0 / 00307280 / 00303EC0 return ladder()==4 / ==5 / ==2.
 S  the save pair: 002EF3C0 writes state +0x5AE0..+0x5AEF to rec +0x08, state +0x5AD0..+0x5ADF to rec +0x18 and the flags word
    to rec +0x28; 002EF410 restores +0x5AE0.. and the flags word, and +0x5AD0.. only when rec +0x18 bit 1 is set.
Writes result.json.
"""
import json
import os
import struct

import probe as P
from unicorn.x86_const import UC_X86_REG_RDX as RDX

HERE = os.path.dirname(os.path.abspath(__file__))
uc, S, STATE, w, r, call = P.uc, P.S, P.STATE, P.w, P.r, P.call
P.W.ALLOWED.discard(0x35C620)
F = STATE + 0x5B04
res, cases = {}, {}


def model(fl):
    fl &= 0xF
    return 5 if fl & 8 else 4 if fl & 4 else 2 if fl & 2 else fl & 1


# L
lad = []
for fl in range(16):
    for hi in (0, 0xFFFFFFF0):
        w(F, "<I", fl | hi)
        ok, v, _ = call(P.LADDER)
        lad.append([fl, hi != 0, ok, v])
cases["L_ladder_is_a_priority_over_the_low_nibble"] = all(ok and v == model(fl) for fl, _, ok, v in lad)
res["ladder"] = lad

# P / Z
pz = {}
for fn, bit, nm in ((P.SET3, 3, "bit3"), (P.SET2, 2, "bit2"), (P.SET0, 0, "bit0")):
    w(F, "<I", 0xA0)                                  # unrelated high bits must survive
    on = call(fn, 1); f_on = r(F, "<I")[0]; w_on, e_on = list(P.flag_writes), list(P.entered); rdx_on = uc.reg_read(RDX) & 0xFFFFFFFF
    again = call(fn, 1); w_again, e_again = list(P.flag_writes), list(P.entered)
    off = call(fn, 0); f_off = r(F, "<I")[0]; w_off, e_off = list(P.flag_writes), list(P.entered); rdx_off = uc.reg_read(RDX) & 0xFFFFFFFF
    pz[nm] = {"on": [f_on, w_on, e_on, on[2], rdx_on], "again": [w_again, e_again], "off": [f_off, w_off, e_off, off[2], rdx_off]}
    good = f_on == 0xA0 | (1 << bit) and w_on == [0xA0 | (1 << bit)] and w_again == [] and e_again == [] \
        and f_off == 0xA0 and w_off == [0xA0]
    if nm == "bit0":
        # the world stops at the boundary's entry before any other hook runs; the tail call's edx (the new flags word) is read there
        good = good and on[2] == ["0035C620"] and off[2] == ["0035C620"] and rdx_on == 0xA1 and rdx_off == 0xA0   # edx = the new flags word
    else:
        good = good and e_on == [] and e_off == [] and on[0] and off[0]
    cases["%s_setter_one_write_none_when_equal" % ("Z" if nm == "bit0" else "P_" + nm)] = good
res["setters"] = pz

# C
uc.mem_write(STATE + 0x5AD0, bytes(0x40))
w(F, "<I", 0)
w(STATE + 0x5AE0, "<Q", 0x1)
w(STATE + 0x5AEC, "<I", 0x77)
before = bytes(uc.mem_read(STATE + 0x5AD0, 0x40))
en = call(P.SET1, 1)
after_en = bytes(uc.mem_read(STATE + 0x5AD0, 0x40))
f_en, e_en = r(F, "<I")[0], list(P.entered)
again = call(P.SET1, 1); w_again = list(P.flag_writes)
dis = call(P.SET1, 0)
f_dis, e_dis = r(F, "<I")[0], list(P.entered)
changed_en = sorted({i for i in range(0x40) if before[i] != after_en[i]})
c = {"enable": {"flags": f_en, "5AE0": "%X" % r(STATE + 0x5AE0, "<I")[0], "5AE4": struct.unpack("<f", after_en[0x14:0x18])[0],
                "bytes_changed_in_5AD0_block": ["+0x%X" % (0x5AD0 + i) for i in changed_en], "entered": e_en},
     "again_writes": w_again, "disable": {"flags": f_dis, "5AEC": r(STATE + 0x5AEC, "<I")[0], "entered": e_dis}}
cases["C_chocobo_enable_sets_bit_ride_time_and_sequence_bits"] = en[0] and f_en == 2 and c["enable"]["5AE0"] == "D" \
    and c["enable"]["5AE4"] == 180.0 and set(changed_en) <= set(range(0x10, 0x18)) | {0x34, 0x35, 0x36, 0x37} and e_en == []
cases["C_chocobo_disable_clears_bit_calls_roster_slot3_and_zeroes_5AEC"] = dis[0] and f_dis == 0 and c["disable"]["5AEC"] == 0 \
    and [e[0] for e in e_dis][:1] == ["002E73C0"] and e_dis[0][2] == 3 and w_again == []
res["chocobo"] = c

# R
w(F, "<I", 0xF); w(STATE + 0x5B08, "<I", 0x1234)
okr = call(P.RESET)
cases["R_reset_zeroes_5B04_and_5B08"] = okr[0] and r(F, "<I")[0] == 0 and r(STATE + 0x5B08, "<I")[0] == 0

# G
g = []
for fl in range(16):
    w(F, "<I", fl)
    bits = [call(fn)[1] & 0xFF for fn in (P.GET0, P.GET1, P.GET2, P.GET3)]
    modes = [call(fn)[1] & 0xFF for fn in (P.IS4, P.IS5, P.IS2)]
    g.append([fl, bits, modes])
cases["G_bit_getters_and_mode_getters"] = all(b == [fl & 1, fl >> 1 & 1, fl >> 2 & 1, fl >> 3 & 1]
                                              and m == [int(model(fl) == 4), int(model(fl) == 5), int(model(fl) == 2)] for fl, b, m in g)
res["getters"] = g

# S
REC = 0x76700000
uc.mem_map(REC, 0x1000)
uc.mem_write(REC, bytes(0x40))
blockA = bytes(range(0x10, 0x20))            # +0x5AE0..+0x5AEF
blockB = bytes([0x02] + list(range(0x41, 0x50)))   # +0x5AD0..+0x5ADF, first byte bit 1 set
uc.mem_write(STATE + 0x5AE0, blockA); uc.mem_write(STATE + 0x5AD0, blockB); w(F, "<I", 0x6)
okc = call(P.CAPTURE, REC)
rec = bytes(uc.mem_read(REC, 0x30))
cap_ok = okc[0] and rec[8:0x18] == blockA and rec[0x18:0x28] == blockB and struct.unpack_from("<I", rec, 0x28)[0] == 6
uc.mem_write(STATE + 0x5AE0, bytes(0x10)); uc.mem_write(STATE + 0x5AD0, bytes(0x10)); w(F, "<I", 0)
okrs = call(P.RESTORE, REC)
rest_on = [bytes(uc.mem_read(STATE + 0x5AE0, 0x10)) == blockA, bytes(uc.mem_read(STATE + 0x5AD0, 0x10)) == blockB, r(F, "<I")[0], okrs[2]]
uc.mem_write(REC + 0x18, bytes([0x00]))       # rec +0x18 bit 1 clear: the 5AD0 block must stay as it is
uc.mem_write(STATE + 0x5AE0, bytes(0x10)); uc.mem_write(STATE + 0x5AD0, b"\x99" * 0x10); w(F, "<I", 0)
okrs2 = call(P.RESTORE, REC)
rest_off = [bytes(uc.mem_read(STATE + 0x5AE0, 0x10)) == blockA, bytes(uc.mem_read(STATE + 0x5AD0, 0x10)) == b"\x99" * 0x10, r(F, "<I")[0], okrs2[0]]
res["save"] = {"capture_rec_hex": rec.hex(), "restore_bit1_set": rest_on, "restore_bit1_clear": rest_off}
cases["S_capture_layout_5AE0_at_rec8_5AD0_at_rec18_flags_at_rec28"] = cap_ok
cases["S_restore_puts_back_5AE0_and_flags_and_5AD0_only_with_rec18_bit1"] = rest_off[0] and rest_off[1] and rest_off[2] == 6 and rest_off[3] \
    and rest_on[0] and rest_on[1] and rest_on[2] == 6

out = {"ok": all(cases.values()), "cases": cases, "state_block": "%X" % STATE, **res}
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-70s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
