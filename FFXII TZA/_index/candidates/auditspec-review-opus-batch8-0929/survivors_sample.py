"""survivors_sample.py - SWE2-AUDIT-SPEC (batch-8 review, 2026-09-29). One independent sample per surviving page.

B1 (battle-party verbs): 003601B0 / 003601C0 bodies - bit cl of 022CB720 set / cleared.
T0 (action targets): the call at 00304EE2 and the gatherer it names; the gatherer's raw callers.
M3 (monster viewer, a universal negative): the call at 001EBA05, and EVERY raw reference to its target (E8/E9, 0F 8x,
   abs64/rva32, rip lea/mov) - "one call edge, no data reference: mode 0 never requested".
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
import b8dis  # noqa: E402

print("== B1")
b8dis.dump(0x003601B0, 0x003601D0)
print("== T0")
b8dis.dump(0x00304ED0, 0x00304EE7)
g = T.dis(0x00304EE2, count=1)[0]
tgt = g.operands[0].imm
print("gatherer %08X: rel32 %s jcc %s data %s rip %s" % (tgt, T.rel32_callers(tgt), T.jcc_callers(tgt), T.data_refs(tgt),
                                                    T.rip_refs(tgt, tgt + 1)))
print("== M3")
b8dis.dump(0x001EB9F0, 0x001EBA0A)
c = T.dis(0x001EBA05, count=1)[0]
tgt = c.operands[0].imm
print("requester %08X: rel32 %s jcc %s data %s rip %s" % (tgt, T.rel32_callers(tgt), T.jcc_callers(tgt), T.data_refs(tgt),
                                                     T.rip_refs(tgt, tgt + 1)))
