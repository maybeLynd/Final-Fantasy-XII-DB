"""Offset-tracked census of SavePayload, whose route is a GETTER RETURN plus 0x200.

The instrument published as gen_offset_tracked_census.py seeds at `mov rX,[rip -> slot]`.
SavePayload is not reached that way: its route is `FN 0x002EF640+0x200` - the payload base is
SaveImage_GetActiveRuntimeBuffer()'s return value plus 0x200. So the seed rule changes and
nothing else does: after `call 002EF640`, RAX carries offset -0x200 relative to the payload
base, and an access at `[rax+0x200+d]` is recorded at payload offset d.

WHAT IS BEING TESTED. Three spans of SavePayload carry the identical sentence "declared gap
span - inside the record by extent, no censused access; semantics open. NOTHING NAMES THESE
BYTES": +0x1538 (2,760 B), +0xC818 (6,120 B) and +0x5589C (3,060 B). On the one type the
offset-tracked census has been run against, two such claims were refuted because the earlier
instrument tracked whether a register held the object rather than what offset it held.

CONTROL: the census must land inside the regions the store already documents - the
PersistentFlagPayload region at +0x0, the battle-state mirror at +0x2008, the
ImageBackedStateBlock region at +0x8000, the BattleSystemState region at +0x4E48C. A census that
finds nothing where the store already knows things has not earned an opinion about the gaps.
"""
import collections
import sys

sys.path.insert(0, "C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts")
import check_default_instance_writers as W  # noqa: E402
import capstone  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG  # noqa: E402

X = capstone.x86
GETTER = 0x002EF640
DELTA = 0x200
SIZE = 0x56490
GAPS = [(0x1538, 2760), (0xC818, 6120), (0x5589C, 3060)]


def walk(img, entry, seed, acc, fwd, seed_getter):
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
            for o in i.operands:
                if o.type != X86_OP_MEM:
                    continue
                mm = o.value.mem
                base = W.norm(mm.base)
                if base not in off or mm.index:
                    continue
                d = off[base] + mm.disp
                if 0 <= d < SIZE:
                    acc[d].add((entry, i.address))
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
                off.pop(d, None)
                continue
            if m in ("call", "jmp") and i.operands and i.operands[0].type == X86_OP_IMM:
                tgt = i.operands[0].imm
                if not (entry <= tgt < entry + size) and tgt in img.sizes:
                    for k, ar in enumerate(W.ARG_REGS):
                        if ar in off:
                            fwd.add((tgt, k + 1, off[ar]))
                if m == "call":
                    off = {k: v for k, v in off.items() if k not in W.VOLATILE}
                    if seed_getter and tgt == GETTER:
                        off[X.X86_REG_RAX] = -DELTA
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
    import check_absence_claims as G
    import call_graph as CG
    callers, _c, _s = CG.call_maps(G.EXE, G.FUNCS)
    hosts = sorted(callers.get(GETTER, ()))
    print("functions calling the getter %08X : %d" % (GETTER, len(hosts)))
    acc = collections.defaultdict(set)
    fwd = set()
    for e in hosts:
        walk(img, e, {}, acc, fwd, True)
    seen = set(fwd)
    work = collections.deque((x[0], x[1], x[2], 0) for x in fwd)
    while work:
        fn, slot, o, d = work.popleft()
        nf = set()
        walk(img, fn, {W.ARG_REGS[slot - 1]: o}, acc, nf, False)
        if d >= 6:
            continue
        for g in nf:
            if g not in seen and len(seen) < 20000:
                seen.add(g)
                work.append((g[0], g[1], g[2], d + 1))
    print("(callee, slot, offset) triples reached  : %d" % len(seen))
    print("distinct payload offsets touched        : %d" % len(acc))
    if acc:
        lo = sorted(acc)
        print("   range 0x%X .. 0x%X" % (lo[0], lo[-1]))
    print()
    import csv
    import io
    rows = [r for r in csv.reader(io.open(G.DB + "/_types/fields.tsv", encoding="utf-8",
                                          newline=""), delimiter="\t")
            if r and r[0] == "SavePayload"]
    regs = sorted((int(r[1], 16), int(r[2]), r[3]) for r in rows)

    def where(d):
        for o, s, n in regs:
            if o <= d < o + s:
                return n
        return "(outside)"
    by = collections.Counter(where(d) for d in acc)
    print("offsets by declared row:")
    for n, c in by.most_common(12):
        print("   %-30s %d" % (n, c))
    print()
    for o, s in GAPS:
        hit = sorted(d for d in acc if o <= d < o + s)
        print("GAP +0x%-6X (%5d B): %d offsets touched %s"
              % (o, s, len(hit), " ".join("0x%X" % x for x in hit[:12])))
    print()
    ctrl = [(0x0, "PersistentFlagPayload region"), (0x2008, "battle-state mirror"),
            (0x8000, "ImageBackedStateBlock region"), (0x4E48C, "BattleSystemState region")]
    for o, n in ctrl:
        r = [x for x in regs if x[0] == o]
        s = r[0][1] if r else 0
        c = sum(1 for d in acc if o <= d < o + s)
        print("CONTROL %-32s %d offsets inside it  %s" % (n, c, "OK" if c else "EMPTY"))


if __name__ == "__main__":
    main()
