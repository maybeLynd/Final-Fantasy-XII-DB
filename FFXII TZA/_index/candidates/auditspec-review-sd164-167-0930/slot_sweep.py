"""slot_sweep.py - SWE2-AUDIT-SPEC (2026-09-30): writers of the heap record callback slot +0xA0 (15 records of 0xA8 at
022D7FD0), in every addressing form arena_ix can see:
  (a) rip-relative operands resolving inside the record array, grouped by offset-in-record;
  (b) image-base-relative operands (non-rip base) whose displacement is 0x21B7FD0 + 0xA8*k + j  (j = 0 and 0xA0);
  (c) every memory operand with displacement 0xA0 in the allocator's code block 00369000..0036E000, by kind;
  (d) positive control: the setter's own `mov [rcx+rax+0xa0], rdx` at 0036C5B6 and the boot clear at 00369E36 must appear in (c).
Also: callers of the boot chain (0022A0B0 / 00266D10 / 002EA320), and the callback body's exits.
"""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arena_ix as X  # noqa: E402
from capstone import CS_OP_MEM

LO, N, SZ = 0x022D7FD0, 15, 0xA8
HI = LO + N * SZ
print("record array %08X..%08X" % (LO, HI))

# (a)
ra = X.rip_refs(LO, HI)
by = collections.Counter()
slot = []
for site, m, o, w, k in ra:
    i = X.ins1(site)
    for op in i.operands:
        if op.type == CS_OP_MEM and op.mem.base == X.X86_REG_RIP:
            t = i.address + i.size + op.mem.disp
            j = (t - LO) % SZ
            by[(j, k)] += 1
            if j in range(0xA0, 0xA8):
                slot.append((site, m, o, k, t))
print("(a) rip refs into the array: %d; offset/kind counts: %s" % (len(ra), sorted(by.items())))
print("    rip refs landing on +0xA0..+0xA7 of any record: %d %s" % (len(slot), ["%08X %s %s" % (s, m, o) for s, m, o, k, t in slot]))

# (b)
bh = []
for kk in range(N):
    for j in (0, 0xA0):
        d = (LO - X.IB) + SZ * kk + j
        for h in X.ib_refs(d):
            bh.append((kk, j, h))
print("(b) image-base-form operands with disp = array + 0xA8k (+0 or +0xA0): %d" % len(bh))
for kk, j, h in bh:
    print("    k=%d j=%#x  %08X %s %s width=%d kind=%s root=%s" % (kk, j, h[0], h[1], h[2], h[3], h[4],
                                                                   "%08X" % (X.root(h[0]) or 0)))

# (c)
c = []
for i in X.dis(0x00369000, 0x0036E000):
    for n, op in enumerate(i.operands):
        if op.type == CS_OP_MEM and op.mem.disp == 0xA0:
            c.append((i.address, i.mnemonic, i.op_str, X.kind_of(i, n)))
print("(c) disp 0xA0 operands in 00369000..0036E000: %d" % len(c))
for a, m, o, k in c:
    print("    %08X %-6s %-44s %s root=%s" % (a, m, o, k, "%08X" % (X.root(a) or 0)))
ctl = {a for a, m, o, k in c if k == "W"}
print("(d) control: 0036C5B6 in W set: %s; 00369E36 in W set: %s" % (0x0036C5B6 in ctl, 0x00369E36 in ctl))

r = X.rel32([0x0022A0B0, 0x00266D10, 0x002EA320])
for t in sorted(r):
    print("callers %08X: %s" % (t, ["%08X %s root=%08X" % (s, k, X.root(s) or 0) for s, k in r[t]]))
d = X.dir64([0x0022A0B0, 0x00266D10, 0x002EA320])
print("dir64: %s" % {("%08X" % k): ["%08X" % x for x in v] for k, v in d.items()})
