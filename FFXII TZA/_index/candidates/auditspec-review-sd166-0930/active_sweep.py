"""active_sweep.py - SWE2-AUDIT-SPEC (2026-09-30): every operand that reaches the active-arena dword 022D89BC, the
push map 022D89A8 (15 bytes), the mask 022D89B8 and the save stack 022D89C0..022D89D0+, in both forms:
  rip-relative (arena_ix.rip_refs over 022D89A8..022D8A60) and image-base-relative (arena_ix.ib_refs of disp = VA - IB,
  plus every disp32 that lands in the window through a non-rip base, found by a raw 4-byte search per candidate disp).
Positive controls (must appear): the push's `[rax + rbx + 0x21b89a8]` read at 0036C272 (image-base form), the rip write
at 00369D73, and the push's image-base save-stack stores.
"""
import collections, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-sd164-167-0930"))
import arena_ix as X  # noqa: E402

LO, HI = 0x022D89A8, 0x022D8A60
rr = X.rip_refs(LO, HI)
print("rip-relative operands into %08X..%08X: %d" % (LO, HI, len(rr)))
for s, m, o, w, k in rr:
    i = X.ins1(s)
    t = [i.address + i.size + op.mem.disp for op in i.operands if op.type == X.CS_OP_MEM and op.mem.base == X.X86_REG_RIP][0]
    print("  %08X -> %08X %-5s %-6s %-46s root=%08X" % (s, t, k, m, o, X.root(s) or 0))
ib = []
for va in range(LO, HI):
    for h in X.ib_refs(va - X.IB):
        ib.append((va, h))
print("image-base-form operands (non-rip base, disp = VA - 0x120000) into the window: %d" % len(ib))
for va, (s, m, o, w, k) in ib:
    print("  %08X  disp->%08X %-5s %-6s %-46s root=%08X" % (s, va, k, m, o, X.root(s) or 0))
ctl = {s for s, m, o, w, k in rr} | {h[0] for va, h in ib}
print("controls: 0036C272 %s, 00369D73 %s" % (0x0036C272 in ctl, 0x00369D73 in ctl))
wr = sorted(set((X.root(s) or s) for s, m, o, w, k in rr if k == "W" and
                X.ins1(s).address + X.ins1(s).size + [op.mem.disp for op in X.ins1(s).operands if op.type == X.CS_OP_MEM][0] == 0x022D89BC))
wr2 = sorted(set((X.root(h[0]) or h[0]) for va, h in ib if va == 0x022D89BC and h[4] == "W"))
print("functions writing 022D89BC: rip %s; image-base %s" % (["%08X" % a for a in wr], ["%08X" % a for a in wr2]))
