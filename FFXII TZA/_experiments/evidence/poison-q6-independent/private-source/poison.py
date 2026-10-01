"""S-27 stage 2's damage, Sap, duration, Stop and HP-Critical arms, executed (OPUS, 2026-09-29, FABLE-REQ-OPUS-POISON-ARM-REPLAY
for PKG-GP-STATUS-POISON Q6).

Block 310's harness (check.py, imported unchanged: its six cases run first and result.json is rewritten identically) drove
Regen only. This drives 00385DF0 through the arms its README lists as not covered. The expected values are the status-write
page's stage-2 table (the-status-write-and-its-side-effects.md, 00386C70 stage 2); a mismatch is the finding.

Record fields read (00386C70, read from the image 2026-09-29): HP delta +0x24 (dword), flag A +0x2C, flag C +0x140, apply
mask +0x54, remove mask +0x58, per-status duration +0x5C+4s, beat +0xDC+2s. Stats fields planted: present words +0x3C
(word 2) and +0x64 (word 1), durations +0xBC+4s, beats +0x13C+2s, max HP +0x24, current HP +0x48.

Evidence class: NATIVE-REPLAY (unicorn), live_game false; the same single memset import bridge as block 310, no application
stub. Writes poison_result.json.
"""
import json
import os
import struct

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
uc = C.uc
POISON, SAP, STOP, DISEASE, BUBBLE, CRIT = 8, 10, 3, 16, 28, 29


def case(w3c=0, w64=0, beat=None, dur=None, maxhp=1000, hp=500):
    C.world(w3c=w3c, w64=w64, beat=beat, dur=dur, srows={POISON: 3, SAP: 3, STOP: 3, 20: 3})
    uc.mem_write(C.STATS + 0x24, struct.pack("<i", maxhp))
    uc.mem_write(C.STATS + 0x48, struct.pack("<i", hp))
    uc.mem_write(C.G_MODES, struct.pack("<I", 0))   # check.py case F leaves the stage-4 drain modes at 3 (image data, not
    uc.mem_write(C.G_CLOCK, struct.pack("<I", 1))   # the WORLD block world() clears); off, and a clock that is no multiple
    ok = C.run()
    rd = lambda fmt, off: struct.unpack(fmt, bytes(uc.mem_read(C.RESULT + off, struct.calcsize(fmt))))[0]
    return {"ran": ok, "faults": C.state["faults"], "outside": C.state["bad"][:3], "rng_draws": len(C.state["rng"]),
            "hp_delta": rd("<i", 0x24), "flagA": rd("<I", 0x2C), "flagC": rd("<I", 0x140), "apply": rd("<I", 0x54),
            "remove": rd("<I", 0x58), "dur20": rd("<i", 0x5C + 4 * 20), "beat8": rd("<h", 0xDC + 2 * POISON)}


B = lambda *bits: sum(1 << b for b in bits)
P = {POISON: 10}                      # a beat of 10 expires this tick (10 - 10 <= 0)
cases = {
    "1_poison_maxhp_1000": (dict(w3c=B(POISON), beat=P), dict(hp_delta=-62, flagA_has=0x140, flagC_has=0x4000)),
    "2_poison_under_bubble": (dict(w3c=B(POISON, BUBBLE), beat=P), dict(hp_delta=-125, flagA_has=0x140, flagC_has=0x4000)),
    "3_poison_under_disease_hp40": (dict(w3c=B(POISON, DISEASE), beat=P, hp=40), dict(hp_delta=-2, flagA_has=0x140, flagC_has=0x4000)),
    "4_poison_maxhp_15_zero_share": (dict(w3c=B(POISON), beat=P, maxhp=15, hp=15), dict(hp_delta=-1, flagA_has=0x140, flagC_has=0x4000)),
    "5a_sap_hp_1": (dict(w3c=B(SAP), beat={SAP: 10}, hp=1), dict(hp_delta=0, flagA_lacks=0x100)),
    "5b_sap_hp_2": (dict(w3c=B(SAP), beat={SAP: 10}, hp=2), dict(hp_delta=-1, flagA_has=0x100)),
    "6a_word1_duration_expires": (dict(w64=B(20), dur={20: 10}), dict(remove_has=B(20), dur20=0)),
    "6b_word1_duration_not_yet": (dict(w64=B(20), dur={20: 11}), dict(remove_lacks=B(20), dur20=1)),
    "7_stop_skips_poison": (dict(w3c=B(STOP, POISON), beat=P), dict(hp_delta=0, flagA_lacks=0x140, flagC_lacks=0x4000, beat8=-1)),
    # the table's "after the loop" row, on the same arm: the HP-Critical line is max HP / 5
    "8_poison_crosses_crit_line": (dict(w3c=B(POISON), beat=P, hp=250), dict(hp_delta=-62, apply_has=B(CRIT))),
    "9_crit_present_above_line": (dict(w3c=B(POISON, CRIT), beat=P, hp=500), dict(hp_delta=-62, remove_has=B(CRIT), apply_lacks=B(CRIT))),
    # the competing reading, tested: the page gates the HP-Critical check on an HP write (flag A bit 8); 00386F78-00386F95
    # read as running it on EVERY call, comparing current HP when there is no write. No statuses at all, so no HP write:
    "10_no_status_hp_below_line": (dict(hp=100), dict(hp_delta=0, flagA_lacks=0x100, apply_has=B(CRIT))),
    "11_no_status_hp_above_line": (dict(hp=500), dict(hp_delta=0, flagA_lacks=0x100, apply_lacks=B(CRIT), remove_lacks=B(CRIT))),
    "12_crit_only_hp_above_line": (dict(w3c=B(CRIT), hp=500), dict(hp_delta=0, flagA_lacks=0x100, remove_has=B(CRIT))),
}


def judge(got, want):
    bad = []
    if not got["ran"] or got["outside"] or got["faults"]:
        bad.append("did not run cleanly")
    for k, v in want.items():
        if k.endswith("_has") and (got[k[:-4]] & v) != v:
            bad.append("%s lacks %#x (is %#x)" % (k[:-4], v, got[k[:-4]]))
        elif k.endswith("_lacks") and got[k[:-6]] & v:
            bad.append("%s has %#x (is %#x)" % (k[:-6], v, got[k[:-6]]))
        elif not k.endswith(("_has", "_lacks")) and got[k] != v:
            bad.append("%s = %r, expected %r" % (k, got[k], v))
    return bad


out, fails = {}, 0
for name, (kw, want) in cases.items():
    got = case(**kw)
    bad = judge(got, want)
    fails += bool(bad)
    out[name] = {"fixture": {k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()}) for k, v in kw.items()},
                 "expected": want, "observed": {k: (hex(v) if k in ("flagA", "flagC", "apply", "remove") else v) for k, v in got.items()},
                 "verdict": "PASS" if not bad else "MISMATCH: " + "; ".join(bad)}
    print("%-5s %-32s %s" % ("PASS" if not bad else "FAIL", name, "; ".join(bad) or "delta %d flagA %#x flagC %#x apply %#x remove %#x"
                             % (got["hp_delta"], got["flagA"], got["flagC"], got["apply"], got["remove"])))
json.dump({"evidence_class": "NATIVE-REPLAY (unicorn), live_game false", "builder": "00385DF0", "stage": "00386C70",
           "cases": out, "fails": fails}, open(os.path.join(HERE, "poison_result.json"), "w", encoding="utf-8"), indent=1, sort_keys=True)
print("FAILS %d" % fails)
