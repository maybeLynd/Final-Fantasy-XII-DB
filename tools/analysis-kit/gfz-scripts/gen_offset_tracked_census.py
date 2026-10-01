#!/usr/bin/env python3
"""gen_offset_tracked_census.py - an access census that carries the OFFSET, not just the object.

WHAT THE EXISTING CENSUSES DO AND WHY IT IS NOT ENOUGH. gen_ptr_census_depth1.py seeds at
`mov rX,[0209BE80]` and follows the object into argument-passed callees; gen_ptr_census_ctor.py
seeds at the allocation and follows sub-object constructors. Both track WHETHER a register holds
the object. Neither tracks WHAT OFFSET it holds, so the moment a caller does
`lea rcx,[rdi+0xAB30]` and hands that to a callee, the callee's `[rcx+0x61B0]` is either lost or
mis-based. On ManagerSingleton0209BE80 they report 20 and 21 offsets.

THIS TRACKS THE OFFSET. Registers carry an integer displacement from the object base; `lea` and
`add`/`sub` with an immediate move it; `mov reg,reg` copies it; ARGUMENT SLOTS carry it into
callees, keyed by (function, slot, offset) so the same callee is analysed once per base it is
handed. A LOAD THROUGH A TRACKED POINTER KILLS THE OFFSET - the value read is a different object,
and conflating those is how a census starts attributing other types' displacements to this one,
which this very type has had retracted three times.

WHAT IT MEASURED ON ManagerSingleton0209BE80, 2026-09-19 (OPUS): 326 DISTINCT OFFSETS, against
20 and 21 from the two published censuses. They distribute across the declared rows the way they
should - 94 inside embedded57E0, 56 inside embedded8FA0, 28 in embedded7FB0, 20 in embedded7EA0,
17 in embedded00A0 - which is the shape a correct census of a type with six embedded sub-objects
has, and is itself a sanity signal the raw count is not.

AND IT REFUTES TWO ABSENCE CLAIMS THIS STORE PUBLISHED:

  unobservedSpanAB38 (0xAB38, 1,800 B) - its row reads "no access at any displacement in this
      span by the 136 functions that load the slot". FIFTY-FOUR distinct offsets are accessed.
  unobservedSpanB244 (0xB244, 23,224 B) - "no censused access". TWO offsets are accessed,
      0x10CE0 and 0x10CE8, at three sites in two functions. The other 23,196 bytes stay
      untouched, so the span is not explained - but it is no longer unobserved.

THE TIE IS POSITIVE AND WAS CHECKED BY HAND, because this type is where attribution-by-extent has
already cost three retractions. 00290CF0 forms both bases with `lea rcx,[rbx+0xAB30]` and
`lea rdx,[rbx+0xAA60]` at 00290D96/00290D88, and IN THE SAME BASIC BLOCK reads this type's own
+0x10F60, +0x10F68 and +0x10FA0. Its `rbx` is its first argument, and its only caller 0028E290
loads `*(void**)0x0209BE80` four times. Slot -> 0028E290 -> 00290CF0 -> 00276650, with the offset
carried, and every step read rather than inferred.

CONTROL: the census must reproduce the offsets the published censuses report - 0x5380, 0x57E0,
0x7EA0, 0x8FA0, 0xA09A, 0x10F90. Six of six found. A census that cannot find what the weaker
instruments found has not earned the right to contradict them.

BOUNDARY, unchanged: indirect calls are not followed; an offset that is computed rather than an
immediate displacement is not tracked; and a pointer cached in memory and reloaded is killed
deliberately rather than followed.

usage: gen_offset_tracked_census.py
"""
import collections
import sys

sys.path.insert(0, "C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts")
import check_default_instance_writers as W  # noqa: E402
import capstone  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG  # noqa: E402

X = capstone.x86
SLOT = 0x0209BE80
SPAN = (0xB244, 0xB244 + 23224)
AB30 = 0xAB30
TYPE_SIZE = 0x10FD0


def walk(img, entry, seed, span_hits, acc, stores_ab30, forwards):
    """seed: {reg: offset}. Runs the CFG once per (function, seed) with union merges."""
    t = W.Taint(img)
    starts, blocks, succ = t._blocks(entry)
    if not starts:
        return
    size = img.sizes.get(entry, 0)
    state = {starts[0]: dict(seed)}
    work = collections.deque([starts[0]])
    n = 0
    while work and n < 20000:
        n += 1
        b = work.popleft()
        off = dict(state[b])
        for i in blocks[b]:
            m = i.mnemonic
            # --- accesses through a tracked pointer -------------------------------
            for oi, o in enumerate(i.operands):
                if o.type != X86_OP_MEM:
                    continue
                mm = o.value.mem
                base = W.norm(mm.base)
                if base not in off or mm.index:
                    continue
                d = off[base] + mm.disp
                if 0 <= d < TYPE_SIZE:
                    acc[d].add(i.address)
                    if SPAN[0] <= d < SPAN[1]:
                        span_hits.append((i.address, d, m, i.op_str))
                    if d == AB30 and oi == 0 and m.startswith("mov") and len(i.operands) == 2:
                        src = i.operands[1]
                        so = off.get(W.norm(src.reg)) if src.type == X86_OP_REG else None
                        stores_ab30.append((i.address, i.op_str, so))
            # --- offset arithmetic -------------------------------------------------
            if m == "lea" and len(i.operands) == 2 and i.operands[0].type == X86_OP_REG \
                    and i.operands[1].type == X86_OP_MEM:
                mm = i.operands[1].value.mem
                d = W.norm(i.operands[0].reg)
                if W.norm(mm.base) in off and not mm.index:
                    off[d] = off[W.norm(mm.base)] + mm.disp
                else:
                    off.pop(d, None)
                continue
            if m in ("add", "sub") and len(i.operands) == 2 \
                    and i.operands[0].type == X86_OP_REG:
                d = W.norm(i.operands[0].reg)
                if d in off and i.operands[1].type == X86_OP_IMM:
                    off[d] += i.operands[1].imm if m == "add" else -i.operands[1].imm
                else:
                    off.pop(d, None)
                continue
            if m == "mov" and len(i.operands) == 2 and i.operands[0].type == X86_OP_REG:
                d = W.norm(i.operands[0].reg)
                s = i.operands[1]
                if s.type == X86_OP_REG and W.norm(s.reg) in off:
                    off[d] = off[W.norm(s.reg)]
                    continue
                if s.type == X86_OP_MEM:
                    a = W.rip_target(i, s)
                    if a == SLOT:                      # the singleton slot load: offset 0
                        off[d] = 0
                        continue
                off.pop(d, None)                       # a load through a pointer is NOT this object
                continue
            if m in ("call", "jmp") and i.operands and i.operands[0].type == X86_OP_IMM:
                tgt = i.operands[0].imm
                if not (entry <= tgt < entry + size) and tgt in img.sizes:
                    for k, ar in enumerate(W.ARG_REGS):
                        if ar in off:
                            forwards.add((tgt, k + 1, off[ar]))
                if m == "call":
                    off = {k: v for k, v in off.items() if k not in W.VOLATILE}
                continue
            if m == "call":
                off = {k: v for k, v in off.items() if k not in W.VOLATILE}
                continue
            try:
                _r, w = i.regs_access()
            except capstone.CsError:
                w = []
            for r in w:
                off.pop(W.norm(r), None)
        for s in succ[b]:
            prev = state.get(s)
            if prev is None:
                state[s] = dict(off)
                work.append(s)
            else:
                merged = {k: v for k, v in prev.items() if off.get(k) == v}
                if merged != prev:
                    state[s] = merged
                    work.append(s)


def main():
    img = W.Image()
    acc = collections.defaultdict(set)
    span_hits, stores_ab30 = [], []
    forwards = set()
    hosts = []
    for e in sorted(img.sizes):
        body = img.body(e)
        if not body:
            continue
        if any(i.mnemonic == "mov" and len(i.operands) == 2
               and i.operands[0].type == X86_OP_REG
               and i.operands[1].type == X86_OP_MEM
               and W.rip_target(i, i.operands[1]) == SLOT for i in body):
            hosts.append(e)
    print("functions that load *(void**)%08X : %d" % (SLOT, len(hosts)))
    for e in hosts:
        walk(img, e, {}, span_hits, acc, stores_ab30, forwards)
    seen, work = set(forwards), collections.deque((f[0], f[1], f[2], 0) for f in forwards)
    while work:
        fn, slot, o, d = work.popleft()
        nf = set()
        walk(img, fn, {W.ARG_REGS[slot - 1]: o}, span_hits, acc, stores_ab30, nf)
        if d >= 6:
            continue
        for g in nf:
            if g not in seen and len(seen) < 20000:
                seen.add(g)
                work.append((g[0], g[1], g[2], d + 1))
    print("(callee, slot, offset) triples reached : %d" % len(seen))
    print("distinct offsets touched               : %d" % len(acc))
    lo = sorted(acc)
    print("   lowest  :", " ".join("0x%X" % x for x in lo[:10]))
    print("   highest :", " ".join("0x%X" % x for x in lo[-10:]))
    print()
    ctrl = [0x5380, 0x57E0, 0x7EA0, 0x8FA0, 0xA09A, 0x10F90]
    got = [c for c in ctrl if c in acc]
    print("CONTROL - offsets the published censuses report: %d of %d found  %s"
          % (len(got), len(ctrl), " ".join("0x%X" % c for c in got)))
    print()
    print("STORES INTO +0xAB30: %d" % len(stores_ab30))
    for a, ops, so in stores_ab30:
        print("   %08X  %s   stored value's own offset: %s"
              % (a, ops, ("+0x%X - SINGLETON-DERIVED" % so) if so is not None else "not tracked"))
    if not stores_ab30:
        print("   none - nothing on a tied path writes that field")
    print()
    print("ACCESSES INSIDE 0xB244..0x10CFC: %d" % len(span_hits))
    for a, d, m, ops in span_hits[:20]:
        print("   %08X  +0x%X  %s %s" % (a, d, m, ops))
    if not span_hits:
        print("   none")


if __name__ == "__main__":
    main()
