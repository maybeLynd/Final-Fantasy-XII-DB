"""DD owner read, version-stamps page: the call chains the new section 5b states, checked against the raw call index
(SWE2-DATA 2026-09-30), static. Every edge is a raw rel32 call/jmp/jcc site in .text (function-list independent), and
the 'only caller' statements are the complete raw caller sets.
Controls: C1 the sweep finds the finaliser's call of the persistent-flag gate (00583D60 -> 0032A8A0), a site the
parent page cites; C2 an absent edge is not reported (00584210 does not call 002370C0 directly).
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, owner, secs, BASE  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


t = [s for s in secs if s[0] == ".text"][0]
name, va, vs, ro, rs = t
blob = d[ro:ro + rs]
calls = {}
for p in range(len(blob) - 6):
    b0 = blob[p]
    if b0 in (0xE8, 0xE9):
        tg = BASE + va + p + 5 + struct.unpack_from("<i", blob, p + 1)[0]
        calls.setdefault(tg, []).append(BASE + va + p)
    elif b0 == 0x0F and 0x80 <= blob[p + 1] <= 0x8F:
        tg = BASE + va + p + 6 + struct.unpack_from("<i", blob, p + 2)[0]
        calls.setdefault(tg, []).append(BASE + va + p)


def callers(tg):
    return sorted({(s, owner(s)) for s in calls.get(tg, []) if owner(s)})


def edge(src, dst):
    return [s for s, f in callers(dst) if f == src]


EDGES = [
    ("load: lifecycle handler -> normaliser", 0x00582860, 0x00584210),
    ("load: lifecycle handler -> load-mode bit setter", 0x00582860, 0x00238A30),
    ("load: lifecycle handler -> restore mark", 0x00582860, 0x00285E60),
    ("load: restore mark -> guard", 0x00285E60, 0x00233C10),
    ("guard -> reinitialise", 0x00233C10, 0x00237DF0),
    ("reinitialise -> inventory/authored init", 0x00237DF0, 0x0023AF50),
    ("authored init -> zero-and-stamp", 0x0023AF50, 0x002370C0),
    ("save: header init -> 0x58 constant", 0x00253A80, 0x002EF2A0),
    ("save: header init -> 0x60 constant", 0x00253A80, 0x00235E90),
    ("save: finaliser -> bit-12 reader", 0x00583D60, 0x00236760),
    ("control C1: finaliser -> persistent-flag gate", 0x00583D60, 0x0032A8A0),
]
for label, a, b in EDGES:
    e = edge(a, b)
    print("   %-48s %08X -> %08X at %s" % (label, a, b, " ".join("%08X" % x for x in e) or "-"))
    check("E " + label, bool(e))
only = {0x00584210: {0x00582860}, 0x002EF2A0: {0x00253A80}, 0x00235E90: {0x00253A80}}
for tg, want in only.items():
    got = {f for s, f in callers(tg)}
    check("O %08X's complete raw caller set is %s" % (tg, " ".join("%08X" % x for x in sorted(want))), got == want,
          " ".join("%08X" % x for x in sorted(got)))
g = {f for s, f in callers(0x00233C10)}
print("   guard 00233C10 raw callers: %s" % " ".join("%08X" % x for x in sorted(g)))
check("O guard callers are 00280140, 00285E60, 0036FCC0, 00394130 (the page's list)",
      g == {0x00280140, 0x00285E60, 0x0036FCC0, 0x00394130})
check("C2 control: no direct 00584210 -> 002370C0 edge is reported", not edge(0x00584210, 0x002370C0))
print("FAILS %d" % FAILS)
