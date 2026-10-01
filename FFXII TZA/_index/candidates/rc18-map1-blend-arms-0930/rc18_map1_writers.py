"""rc18_map1_writers.py - RC-18, part 1: every store that can reach party slot map 1 (block + 0x5A5A .. + 0x5A6B,
nine u16) of the battle-state block whose only published pointer is the global 02EBF190. ORACLE, 2026-09-30. Static.

The flow engine of ../k14-closure-stores-0930/k14_actorflow.py tracks the block as the token "A" (as rc4_flow.py does
for its object):
- roots: every function with a rip-relative load of 02EBF190 (the load yields A), closed over functions that return
  A (their callers become roots);
- A is followed through registers, the stack, lea/add offsets (so `rdi = A + 0x5A48` then `[rdi + 0x12]` is A+0x5A5A),
  switch tables, tail jumps and direct callees under their argument values; memset/memcpy adapters and rep-string
  stores count by destination and length;
- every store whose written bytes can overlap [A+0x5A5A, A+0x5A6C) is listed with its base and value; stores of A
  into non-stack memory (escapes) and indirect calls receiving A (blind spots) are listed.
Positive controls (the two known writers, from the five-maps and battle-state-block pages):
  00326717 / 0032671B  BattleGroup_RefreshFourActorDefinitions copies map 0 into map 1 through r15 = A + 0x5A5A
  00329DF6 / 00329DFD  BattleSlotMap_InitializeMappingClasses copies map 0 into map 1
"""
import collections, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K  # noqa: E402
from capstone import x86 as X  # noqa: E402

R = K.R
GLOBAL = 0x02EBF190
LO, HI = 0x5A5A, 0x5A6C
CONTROL = {0x00326717, 0x0032671B, 0x00329DF6, 0x00329DFD}
K.MAXDEPTH = 8


SSE_STORES = ("movups", "movaps", "movdqu", "movdqa", "movupd", "movapd", "movss", "movsd", "movq", "movd", "movlps",
              "movhps", "movlpd", "movhpd", "movntdq", "movntps", "vmovups", "vmovaps", "vmovdqu", "vmovdqa")


class Flow(K.Analysis):
    """capstone flags the memory destination of the SSE moves (`movups xmmword [r15], xmm0`) as READ, so the base
    engine does not see them as stores; they are handled here before the base step."""
    def __init__(self):
        super().__init__()
        self.hits = []
        self.loose = set()   # call sites passing the block with an unknown offset: (fn, site, target, register)
        self.strided = []   # stores into element k of a C-stride array inside the block: (fn, addr, text, A*C, offset, size)

    def step(self, f, st, i, depth, stack, caller_writes):
        ops = i.operands
        mn = i.mnemonic
        # strided-array refinement: `imul r64, s, C` yields the token IDX<C> (an index times C), and
        # `add r64, r64` of a block pointer A+o with IDX<C> yields A*<C>+o: element k of a C-stride array at A+o.
        if mn == "imul" and len(ops) == 3 and ops[0].type == X.X86_OP_REG and ops[2].type == X.X86_OP_IMM:
            dn, dw = K.fullname(ops[0].reg)
            if dn and dw == 8:
                st.r[dn] = K.vs(("IDX%X" % ops[2].imm, 0))
                return R.branch_targets(i), st, False
        if mn == "add" and len(ops) == 2 and ops[0].type == X.X86_OP_REG and ops[1].type == X.X86_OP_REG:
            dn, dw = K.fullname(ops[0].reg)
            a1, a2 = st.r.get(dn, K.UNK), K.reg(st, ops[1].reg)[0]
            if dn and dw == 8 and a1 is not K.UNK and a2 is not K.UNK:
                for p, q in ((a1, a2), (a2, a1)):
                    if len(q) == 1:
                        (qb, qo), = q
                        if isinstance(qb, str) and qb.startswith("IDX") and qo is not None and                                 all(b == "A" for b, _ in p):
                            st.r[dn] = frozenset(("A*" + qb[3:], None if o is None else o + qo) for b, o in p)
                            return R.branch_targets(i), st, False
        if mn == "call" and ops and ops[0].type == X.X86_OP_IMM:
            for r in ("rcx", "rdx", "r8", "r9"):
                v = st.r.get(r, K.UNK)
                if v is not K.UNK and ("A", None) in v:
                    self.loose.add((f, i.address, ops[0].imm, r))
        if mn == "jmp" and ops and ops[0].type == X.X86_OP_IMM and ops[0].imm in K.ext and not (f <= ops[0].imm < f + K.ext.get(f, 0)):
            for r in ("rcx", "rdx", "r8", "r9"):
                v = st.r.get(r, K.UNK)
                if v is not K.UNK and ("A", None) in v:
                    self.loose.add((f, i.address, ops[0].imm, r))
        if i.mnemonic in SSE_STORES and len(ops) == 2 and ops[0].type == X.X86_OP_MEM and ops[1].type == X.X86_OP_REG:
            self.store(f, i, st, K.memaddr(st, ops[0].mem, i), ops[0].size, K.UNK)
            return R.branch_targets(i), st, False
        return super().step(f, st, i, depth, stack, caller_writes)

    def store(self, f, i, st, addr, size, val):
        if addr is not K.UNK:
            for b, o in addr:
                if b == "A" and (o is None or (o < HI and LO < o + size)):
                    self.hits.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str), K.desc(addr), K.desc(val)))
                elif isinstance(b, str) and b.startswith("A*"):
                    self.strided.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str), b, o, size))
        o = K.sp_off(addr)
        if o is not None:
            for k in [k for k in st.s if k < o + size and o < k + 8 and k != o]:
                del st.s[k]
            if size == 8:
                st.s[o] = val
            else:
                st.s.pop(o, None)
        else:
            if addr is K.UNK or any(b == "SP" for b, _ in addr):
                st.s.clear()
            if hasA(val):
                self.escapes.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str), K.desc(addr)))


def hasA(v):
    """the block or any strided element inside it"""
    return v is not K.UNK and any(isinstance(b, str) and (b == "A" or b.startswith("A*")) for b, _ in v)


_orig_load = K.load_value


def load_value(st, addr):
    if addr is not K.UNK and addr == K.vs(("G%08X" % GLOBAL, 0)):
        return K.vs(("A", 0))
    return _orig_load(st, addr)


K.load_value = load_value


def main():
    roots = []
    for f in sorted(K.ext):
        for i in R.md.disasm(R.at(f, K.ext[f]), f):
            if any(op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP and i.address + i.size + op.mem.disp == GLOBAL
                   for op in i.operands):
                roots.append(f)
                break
    an = Flow()
    done, work, returners = set(), list(roots), set()
    while work:
        f = work.pop()
        if f in done:
            continue
        done.add(f)
        rv, _ = an.summary(f, (), 0, ())
        if hasA(rv) and f not in returners:
            returners.add(f)
            work.extend(sorted(R.CALLERS.get(f, ())))
    for (f, ctx), (rv, _) in list(an.memo.items()):
        if hasA(rv) and f not in returners:
            returners.add(f)
            for c in sorted(R.CALLERS.get(f, ())):
                if c not in done:
                    done.add(c)
                    an.summary(c, (), 0, ())
    print("roots (functions loading %08X): %d; functions returning the block: %s" % (
        GLOBAL, len(roots), " ".join("%08X" % f for f in sorted(returners)) or "none"))
    print("bodies analysed %d, contexts %d; cuts %d, of which carry the block %d" % (
        len(an.fns), len(an.memo), len(an.recursive), sum(1 for c in an.recursive if c[2])))
    hits = sorted(set(an.hits))
    found = CONTROL & set(h[1] for h in hits)
    ok = found == CONTROL
    print("%s  control: the two known writers' map-1 copies found: %d of %d (%s)" % (
        "PASS" if ok else "FAIL", len(found), len(CONTROL), " ".join("%08X" % a for a in sorted(CONTROL - found)) or "all"))
    fns = collections.OrderedDict()
    for h in hits:
        fns.setdefault(h[0], []).append(h)
    print("stores that can overlap A+0x5A5A..A+0x5A6B: %d sites in %d functions" % (len(set(h[1] for h in hits)), len(fns)))
    for f, hs in fns.items():
        print("FUNCTION %08X" % f)
        for h in hs:
            print("  %08X %-44s base %-24s value %s" % (h[1], h[2], h[3], h[4]))
    st = sorted(set(an.strided), key=lambda t: (t[3], t[0], t[1]))
    print("stores into a strided array of the block (A + o + k*C), by array: %d sites" % len(set(t[1] for t in st)))
    grp = collections.OrderedDict()
    for t in st:
        grp.setdefault((t[3], t[4] is None), []).append(t)
    for (b, unk), ts in grp.items():
        offs = sorted(set(t[4] for t in ts if t[4] is not None))
        ends = [t[4] + t[5] for t in ts if t[4] is not None]
        print("  %s  sites %d  element-relative offsets %s .. end %s%s" % (
            b, len(set(t[1] for t in ts)), ("%#x" % offs[0]) if offs else "-", ("%#x" % max(ends)) if ends else "-",
            "  (some offsets unknown)" if unk else ""))
        for t in ts:
            if t[4] is None:
                print("    UNKNOWN-OFFSET %08X %08X %s" % (t[0], t[1], t[2]))
    print("call sites passing the block with an unknown offset (A+?) as an argument: %d" % len(an.loose))
    for t in sorted(an.loose):
        print("  LOOSE %08X %08X -> %08X in %s" % t)
    esc = sorted(set(an.escapes))
    print("escapes of the block pointer into non-stack memory: %d" % len(esc))
    for e in esc:
        print("  ESCAPE %08X %08X %-40s to %s" % e)
    carried = sorted(set(an.indirect))
    print("indirect calls receiving the block: %d" % len(carried))
    for e in carried:
        print("  INDIRECT %08X %08X %-40s args %s" % e)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
