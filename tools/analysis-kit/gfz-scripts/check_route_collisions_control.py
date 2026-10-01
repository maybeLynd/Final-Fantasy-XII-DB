#!/usr/bin/env python3
"""Control for check_route_span_overlaps' sparse-SLOTPTR containment rule (that checker was
check_route_collisions.py until ffe018a49 gave the name to a different check; re-pointed 2026-09-27, OPUS).

The rule was added on SWE2-STRUCT-REQ-OPUS-SPARSE-SLOTPTR-SPAN-MODEL, and a rule that turns a
reported defect into a pass has to be shown to still refuse. Every expectation below was checked
against fields.tsv BEFORE being written down - the first draft of this control asserted that
ActorManagerSlot +0x30 is a 4-byte handle and it is `resolvedUnitPtr`, a declared void*, so the
checker was right and the control was wrong.

Nine cases: two shapes that must be accepted, seven that must be refused.
"""
import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# THE PREREQUISITE, an explicit data contract since 2026-09-29 (FRONTIER-REQ-OPUS-COMPOSER-PREREQ-REPAIRS, matrix A03):
# check_route_span_overlaps runs its whole check at import and exits 1 when the store has overlaps - findings, which do not
# stop this control using its contained() rule; exit 2 / any other code, a crash, or a missing contained() is a broken
# prerequisite and stops the control. Before, every SystemExit was swallowed. ROUTE_OVERLAPS_SOURCE overrides the file
# (tests only).
import prereq  # noqa: E402
_src = os.environ.get("ROUTE_OVERLAPS_SOURCE") or os.path.join(HERE, "check_route_span_overlaps.py")
m, _why = prereq.run(_src, [sys.argv[0]], names=("contained",), exits=(0, 1),
                     validate=lambda mod: None if callable(mod.contained) else "contained is not callable")
if _why:
    print("PREREQUISITE FAILED: %s - the control does not run" % _why)
    sys.exit(2)

AB, AS, AC = 0x02098E10, 0x288, 5
ARR = (AB, AB + AS * AC, "ActorManagerSlot", "ARRAY", AS, AC)


def slot(off, stride=AS, count=AC, name="Probe"):
    b = AB + off
    return (b, b + stride * (count - 1) + 8, name, "SLOTPTR", stride, count)


CASES = [
 ("cells on +0x08 recordPool, a declared void*      [the real route]", slot(0x08, name="ActorRecordPool"), True),
 ("cells on +0x30 resolvedUnitPtr, also a void*     [second true case]", slot(0x30), True),
 ("cells on +0x28 slotIndex, declared 4B uint32", slot(0x28), False),
 ("cells on +0x10 slotFlags, declared 1B uint8", slot(0x10), False),
 ("cells on +0x2C unobservedSpan002C, a declared gap", slot(0x2C), False),
 ("cells at +0x287, an offset the type does not declare", slot(0x287), False),
 ("cells running past the array end (count 9)", slot(0x08, count=9), False),
 ("cells at differing element offsets (stride 0x289)", slot(0x08, stride=0x289), False),
 ("a DENSE slotptr (stride 8) is not containment", slot(0x08, stride=8), False),
]


def main():
    print("\nCONTROL for the sparse-SLOTPTR containment rule\n")
    bad = 0
    for label, sp, expect in CASES:
        got, why = m.contained(sp, ARR)
        if got != expect:
            bad += 1
        print("%s %-58s -> %-5s %s" % ("ok  " if got == expect else "FAIL", label, got, why[:62]))
    print()
    if bad:
        print("CONTROL FAILED on %d of %d" % (bad, len(CASES)))
        return 1
    print("CONTROL PASSES: the rule accepts a cell landing on a declared 8-byte pointer and")
    print("refuses every other shape - wrong width, wrong type, a gap, an undeclared offset,")
    print("cells outside the array, cells at inconsistent element offsets, and the dense case.")
    return 0


sys.exit(main())
