"""con185_186.py - SWE2-AUDIT-SPEC (batch-8 review, 2026-09-29). Independent re-derivation of CON-185 and CON-186.

CON-185: 001EC680's body; its raw callers (E8/E9 rel32, 0F 8x jcc, abs64/rva32); whether 0026B750 calls the pusher thunk
         001EC6A0 without it; the number of 01F832B0-relative reads in 001CD0E0 (rip form and image-base form).
CON-186: every reference to the two switches 02B3F53C / 02B3F540 image-wide, and which function each lies in.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
import b8dis  # noqa: E402

print("== CON-185")
b8dis.dump(0x001EC680, 0x001EC6A0)
print("callers of 001EC680: rel32", T.rel32_callers(0x001EC680), "jcc", T.jcc_callers(0x001EC680), "data", T.data_refs(0x001EC680))
print("callers of 001EC6A0 (pusher thunk): rel32", T.rel32_callers(0x001EC6A0), "jcc", T.jcc_callers(0x001EC6A0))
for c in [int(x.split()[0], 16) for x in T.rel32_callers(0x001EC6A0)]:
    print("  -- window before %08X" % c)
    b8dis.dump(c - 0x18, c + 5)
# 001CD0E0: reads of the counter array 01F832B0 in either addressing form, over its body (to its first ret run)
ins = T.dis_func(0x001CD0E0, 0x4000)
end = ins[-1].address + ins[-1].size
print("001CD0E0 decoded to %08X (%d insns)" % (end, len(ins)))
n = 0
for i in ins:
    for m, sz in T.mem_ops(i):
        if m.base == T.X86_REG_RIP and 0x01F832B0 <= i.address + i.size + m.disp < 0x01F832B0 + 0x40:
            n += 1; print("  rip  %08X %s %s" % (i.address, i.mnemonic, i.op_str))
        elif m.base != T.X86_REG_RIP and 0x01F832B0 - T.IB <= m.disp < 0x01F832B0 - T.IB + 0x40:
            n += 1; print("  base %08X %s %s" % (i.address, i.mnemonic, i.op_str))
print("001CD0E0 counter-array accesses:", n)

print("== CON-186")
for cell in (0x02B3F53C, 0x02B3F540):
    r = T.rip_refs(cell, cell + 4) + T.imagebase_refs(cell, cell + 4)
    print("%08X: %d refs" % (cell, len(r)))
    for h in r:
        print("   %08X  %s %s (%dB)" % h)
b8dis.dump(0x003AED70, 0x003AEDC0)
print("---")
b8dis.dump(0x003AEF90, 0x003AEFC0)
