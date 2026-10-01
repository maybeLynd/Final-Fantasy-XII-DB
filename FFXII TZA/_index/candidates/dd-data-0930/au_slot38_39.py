"""DD owner read, sound-variant-selection page (SD-23): the virtual call sites through Sound-family capability slots 38
(+0x130) and 39 (+0x138) in the audio span 007A0000..00800000 (SWE2-DATA 2026-09-30), static.
Every listed function in the span is disassembled; a site is 'call/jmp qword ptr [reg + 0x130 | 0x138]'.
Control: the same scan for slot 43 (+0x158) must find the stepper 007BD120's call, the select entry the pages cite.
Limit: a site that loads the slot into a register first, or code outside the span, is not seen.
"""
import os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import funcs, dis, names  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


hits = collections.defaultdict(list)
for f in sorted(funcs):
    if not (0x007A0000 <= f < 0x00800000):
        continue
    try:
        b = dis(f)
    except Exception:
        continue
    for x in b:
        m = re.fullmatch(r"qword ptr \[r\w+ \+ (0x130|0x138|0x158)\]", x.op_str)
        if x.mnemonic in ("call", "jmp") and m:
            hits[m.group(1)].append((x.address, f))
for k in ("0x130", "0x138"):
    print("slot %s (+%s): %d sites" % ("38" if k == "0x130" else "39", k, len(hits[k])))
    for a, f in hits[k]:
        print("   %08X in %08X %s" % (a, f, names.get(f, "")))
check("C slot 43 (+0x158) scan finds the stepper 007BD120's call", any(f == 0x007BD120 for a, f in hits["0x158"]),
      "%d slot-43 sites" % len(hits["0x158"]))
print("FAILS %d" % FAILS)
