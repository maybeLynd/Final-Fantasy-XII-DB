#!/usr/bin/env python3
"""scan_descriptor_flag_bits.py - which bits of a descriptor's +0xFC are ever set, TIED to a descriptor.

NAMED `scan_` AND NOT `check_` ON PURPOSE: run_gates.py collects `check_*`, and this takes about
five minutes because it rebuilds the call graph and runs a fixpoint taint. It answers a question
once rather than guarding an invariant every run.

WHY NOT AN IMAGE-WIDE SWEEP. Sweeping every `mov/or [reg+0xFC], imm` in the image reports bit 3
set at 18 sites - and every one of them is an unrelated object that also happens to have a field
at +0xFC. That is attribution by displacement with no tie to the type, which is the error
EVIDENCE-STANDARD addendum bw exists to name. The 0xFC displacement is shared by hundreds of
structures.

SO THIS REUSES THE DESCRIPTOR TAINT from check_default_instance_writers.py: seed every register
provably holding one of the known descriptor addresses, propagate through moves, frame spills,
pointer arithmetic and ARGUMENT SLOTS across direct calls to a fixpoint, and only then look at
`[tainted + 0xFC]`.

THE QUESTION IT ANSWERS. PCluster::create tests `[desc+0xFC] & 8` at 0063A99A and, when set,
prints "Class '%s' has no default constructor and cannot be allocated with PCluster::create()".
RTTI marks 35 of the 315 classes `PClassDescriptorWithoutDefaultConstructor` /
`...HeaderWithoutDefaultConstructor`. Is bit 3 how that mark reaches the runtime?

CONTROLS - the probe must find the flag writes this project has already established, all of
which are in functions that RECEIVE the descriptor as an argument:
    bit 1   `or [desc+0xFC], 2`            in every class's descriptor constructor
    bit 29  `or [desc+0xFC], 0x20000000`   0063BC49, "default pointer handed out"
    bit 30  `or [desc+0xFC], 0x40000000`   006363E0 / 00639465
    bit 31  `or [desc+0xFC], 0x80000000`   00639C55, "default buffer built"
A run that misses any of those has not shown it can see a flag write at all, and its silence on
bit 3 would mean nothing.

WHAT IT MEASURED, 2026-09-19 (OPUS). All four controls found. The bits ever set on a descriptor:

    bit 1   315 sites   `or 2` in every class's descriptor constructor
    bit 27    1 site    00639EEF, inside 00639C80
    bit 28    1 site    0063A0E2, inside 00639C80 - and 00639CB4 CLEARS 27 and 28 together
    bit 29    1 site    0063BC49, the default pointer handed out
    bit 30    1 site    00639465
    bit 31    1 site    00639C55, the default buffer has been built

    BIT 3: NEVER SET ON ANY DESCRIPTOR-TIED PATH.

So PCluster::create's refusal arm - `test byte [r8+0xFC], 8` at 0063A99A, printing "Class '%s'
has no default constructor and cannot be allocated with PCluster::create()" - CANNOT FIRE in this
build. That is the third arm of this machinery found disarmed, after 00639A60's
construct-and-compare (slot +0x50 returns false on all 315) and the "position dependant
constructor" diagnostic that depends on it.

AND IT CORRECTED A FIGURE THE UNTIED SWEEP GAVE. An image-wide scan reports bit 30 set at two
sites, 006363E0 and 00639465. Only 00639465 is descriptor-tied; 006363E0 writes some other
object's +0xFC. The same untied scan reports bit 3 set at 18 sites, every one of them an
unrelated structure that also has a field at that displacement.

THE READS ARE THE SIBLING SCRIPT, scan_descriptor_flag_reads.py, and the two together give the
verdict a write census alone cannot: only bits 1, 30 and 31 are BOTH written and read. Bits 0 and
3 are read and never written (dead arms); bits 27, 28 and 29 are written and never read
(discarded results).

THE BOUNDARY, unchanged from the taint this reuses: indirect calls are not followed, nor is a
descriptor parked in memory and reloaded with no lea on the path. The negative is "no
descriptor-tied path sets bit 3", not "no instruction anywhere sets it".
"""
import collections
import sys

sys.path.insert(0, "C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts")
import check_default_instance_writers as W  # noqa: E402
import capstone  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG  # noqa: E402

X = capstone.x86
FLAG = 0xFC


def flag_writes(img, entry, seed_regs, seed_values=None):
    """every `<op> [tainted+0xFC], imm` in one body, using the same CFG may-taint."""
    t = W.Taint(img)
    starts, blocks, succ = t._blocks(entry)
    if not starts:
        return [], set()
    out, forwards = [], set()
    size = img.sizes.get(entry, 0)
    state = {starts[0]: frozenset(seed_regs)}
    work = collections.deque([starts[0]])
    rounds = 0
    while work and rounds < 20000:
        rounds += 1
        b = work.popleft()
        regs = set(state[b])
        for i in blocks[b]:
            m = i.mnemonic
            if (i.operands and i.operands[0].type == X86_OP_MEM
                    and i.operands[0].value.mem.disp == FLAG
                    and not i.operands[0].value.mem.index
                    and W.norm(i.operands[0].value.mem.base) in regs
                    and m in ("or", "and", "mov", "xor", "bts", "btr")):
                if len(i.operands) > 1 and i.operands[1].type == X86_OP_IMM:
                    out.append((i.address, m, i.operands[1].imm & 0xFFFFFFFF))
                else:
                    out.append((i.address, m, None))
            v = W.lea_value(i)
            if v is not None:
                d = W.norm(i.operands[0].reg)
                if seed_values and v in seed_values:
                    regs.add(d)
                else:
                    regs.discard(d)
                continue
            if m == "mov" and len(i.operands) == 2 and i.operands[0].type == X86_OP_REG:
                d = W.norm(i.operands[0].reg)
                s = i.operands[1]
                if s.type == X86_OP_REG and W.norm(s.reg) in regs:
                    regs.add(d)
                else:
                    regs.discard(d)
                continue
            if m in ("call", "jmp") and i.operands and i.operands[0].type == X86_OP_IMM:
                tgt = i.operands[0].imm
                if not (entry <= tgt < entry + size) and tgt in img.sizes:
                    for k, ar in enumerate(W.ARG_REGS):
                        if ar in regs:
                            forwards.add((tgt, k + 1))
                if m == "call":
                    regs -= W.VOLATILE
                continue
            if m == "call":
                regs -= W.VOLATILE
                continue
            try:
                _r, w = i.regs_access()
            except capstone.CsError:
                w = []
            for r in w:
                regs.discard(W.norm(r))
        for s in succ[b]:
            prev = state.get(s)
            new = frozenset(regs)
            if prev is None or (prev | new) != prev:
                state[s] = new if prev is None else (prev | new)
                work.append(s)
    return out, forwards


def main():
    img = W.Image()
    descs = W.store_descriptors(W.G.DB) | set(W.enumerate_descriptors(img))
    print("descriptor seed set: %d" % len(descs))

    hosts = [e for e in img.sizes
             if any(W.lea_value(i) in descs for i in img.body(e) if i.mnemonic == "lea")]
    writes, seen, work = [], set(), collections.deque()
    for e in hosts:
        w, f = flag_writes(img, e, set(), seed_values=descs)
        writes += [(e,) + x for x in w]
        for g in f:
            if g not in seen:
                seen.add(g)
                work.append((g[0], g[1], 0))
    while work:
        f, slot, d = work.popleft()
        w, fw = flag_writes(img, f, {W.ARG_REGS[slot - 1]})
        writes += [(f,) + x for x in w]
        if d >= 12:
            continue
        for g in fw:
            if g not in seen:
                seen.add(g)
                work.append((g[0], g[1], d + 1))
    print("bodies seeded by a lea of a descriptor : %d" % len(hosts))
    print("(callee, arg slot) pairs reached       : %d" % len(seen))
    print("flag writes tied to a descriptor       : %d" % len(writes))
    print()

    bits = collections.defaultdict(set)
    forms = collections.Counter()
    for host, addr, m, v in writes:
        forms[(m, hex(v) if v is not None else "reg")] += 1
        if v is None or m in ("and", "btr"):
            continue
        if m == "bts":
            bits[v].add(addr)
            continue
        if m in ("or", "mov", "xor"):
            for b in range(32):
                if v >> b & 1:
                    bits[b].add(addr)
    print("write forms:", dict(forms.most_common(10)))
    print()
    print("BITS EVER SET ON A DESCRIPTOR'S +0xFC:")
    for b in sorted(bits):
        print("   bit %-2d : %3d site(s)   e.g. %s"
              % (b, len(bits[b]), " ".join("%08X" % a for a in sorted(bits[b])[:4])))
    print()
    ok = True
    for b, what in ((1, "or 2, descriptor constructors"),
                    (29, "0063BC49 default pointer handed out"),
                    (30, "006363E0 / 00639465"),
                    (31, "00639C55 default buffer built")):
        hit = b in bits
        ok = ok and hit
        print("CONTROL bit %-2d %-38s %s" % (b, what, "FOUND" if hit else "MISSING"))
    print()
    if not ok:
        print("A CONTROL IS MISSING -> the bit-3 result below is not reportable.")
    print("BIT 3, which PCluster::create tests before refusing to allocate: %s"
          % ("SET at %d site(s)" % len(bits[3]) if 3 in bits
             else "NEVER SET on any descriptor-tied path"))


if __name__ == "__main__":
    main()
