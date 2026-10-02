"""test_upstream_guard.py - the s33 upstream verdict guard, both directions, without the native campaign
(OPUS, 2026-10-01). Prints one line per case and FAILS n; exit 0 only when every case behaves."""
import sys
import types

import upstream_guard as G


def mod(**kw):
    m = types.ModuleType("fake_upstream")
    for k, v in kw.items():
        setattr(m, k, v)
    return m


PASS1 = {"I2": {"pass_": True}, "I3": {"pass_": True}}
CASES = [
    ("positive control: allok True, every case passing", mod(allok=True, results=PASS1), True),
    ("non-empty results with a FAIL, allok False", mod(allok=False, results={"I2": {"pass_": True}, "I3": {"pass_": False}}), False),
    ("allok True but one case failing (inconsistent upstream)", mod(allok=True, results={"I2": {"pass_": False}}), False),
    ("allok missing", mod(results=PASS1), False),
    ("allok truthy but not True (1)", mod(allok=1, results=PASS1), False),
    ("results missing", mod(allok=True), False),
    ("results empty", mod(allok=True, results={}), False),
    ("results malformed (list)", mod(allok=True, results=[("I2", True)]), False),
    ("a case entry malformed (bool, not dict)", mod(allok=True, results={"I2": True}), False),
    ("a case pass_ truthy but not True", mod(allok=True, results={"I2": {"pass_": "yes"}}), False),
]
fails = 0
for label, m, want in CASES:
    ok, why = G.verdict(m)
    good = ok is want
    fails += 0 if good else 1
    print("%-4s %-58s -> %s%s" % ("ok" if good else "FAIL", label, ok, "" if ok else " (%s)" % why))
print("FAILS", fails)
sys.exit(1 if fails else 0)
