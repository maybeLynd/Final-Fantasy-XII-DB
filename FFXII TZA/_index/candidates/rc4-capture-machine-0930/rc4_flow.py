"""rc4_flow.py - RC-4, the interprocedural half: follow the render object from every place it is obtained into
everything that runs with it, and list every store that can reach its state word +0xDAC. OPUS, 2026-09-30. Static.

The render object is `new(0xDD8)` built by 00184F20 in 00189000 and published only in the global 01F7F598
(00189067). The flow engine of k14_actorflow.py tracks it as the token "A":
- roots: every function with a rip-relative load of 01F7F598 (the load yields A), and the constructor 00184F20 with
  rcx = A;
- A is followed through registers, the stack, offsets (lea/add), switch tables, and into direct callees under the
  argument values they receive (a pointer handed out as A + K reaches the callee as A + K);
- every store whose written bytes can cover A + 0xDAC is listed with the value stored, and every store of A itself
  into non-stack memory (an escape: a later load from there would be another root) is listed.
Control: the machine's four stores and the constructor's (00187891, 001878B3, 001878D5, 001878E5, 00185020) must be
found, which requires following A from the global through the frame routine into the machine.
"""
import collections, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K  # noqa: E402
from capstone import x86 as X  # noqa: E402

R = K.R
GLOBAL = 0x01F7F598
TARGET = 0xDAC
MACHINE = {0x00187891, 0x001878B3, 0x001878D5, 0x001878E5, 0x00185020}
K.MAXDEPTH = 12


class Flow(K.Analysis):
    def __init__(self):
        super().__init__()
        self.hits = []

    def export(self, v, st):
        """Only the object's own flow matters here: an argument that cannot carry it enters the callee as UNKNOWN,
        so callees are analysed once per object-carrying argument pattern, not once per distinct pointer."""
        v = K.Analysis.export(self, v, st)
        return v if K.has_actor(v) else K.UNK

    def store(self, f, i, st, addr, size, val):
        if addr is not K.UNK:
            for b, o in addr:
                if b == "A" and (o is None or o <= TARGET < o + size):
                    self.hits.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str), K.desc(addr), K.desc(val)))
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
            if K.has_actor(val):
                self.escapes.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str), K.desc(addr)))


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
    an.summary(0x00184F20, (("rcx", K.vs(("A", 0))),), 0, ())
    # roots to a fixpoint: a function whose return value can be the object (the getter 00189120 is
    # `mov rax, [01F7F598]; ret`) makes every caller of it a root as well
    done, work, returners = set(), list(roots), set()
    while work:
        f = work.pop()
        if f in done:
            continue
        done.add(f)
        rv, _ = an.summary(f, (), 0, ())
        if K.has_actor(rv) and f not in returners:
            returners.add(f)
            work.extend(sorted(R.CALLERS.get(f, ())))
    # every analysed context that returns the object also makes its callers roots
    for (f, ctx), (rv, _) in list(an.memo.items()):
        if K.has_actor(rv) and f not in returners:
            returners.add(f)
            for c in sorted(R.CALLERS.get(f, ())):
                if c not in done:
                    done.add(c)
                    an.summary(c, (), 0, ())
    roots = sorted(done)
    print("functions returning the object: %s" % " ".join("%08X" % f for f in sorted(returners)))
    found = MACHINE & set(h[1] for h in an.hits)
    print("%s  control: the machine's and the constructor's stores found through the flow: %d of %d (%s)" % (
        "PASS" if found == MACHINE else "FAIL", len(found), len(MACHINE),
        " ".join("%08X" % a for a in sorted(MACHINE - found)) or "all"))
    print("roots (functions loading %08X): %d; bodies analysed %d, contexts %d; cuts %d, of which carry the object %d" % (
        GLOBAL, len(roots), len(an.fns), len(an.memo), len(an.recursive), sum(1 for c in an.recursive if c[2])))
    hits = sorted(set(an.hits))
    other = [h for h in hits if h[1] not in MACHINE]
    print("stores that can cover +0xDAC: %d distinct; beyond the five known: %d" % (len(set(h[1] for h in hits)), len(set(h[1] for h in other))))
    for h in hits:
        print("  %s %08X %08X %-40s base %-20s value %s" % ("KNOWN" if h[1] in MACHINE else "OTHER", *h))
    esc = sorted(set(an.escapes))
    print("escapes of the object pointer into non-stack memory: %d" % len(esc))
    for e in esc:
        print("  ESCAPE %08X %08X %-40s to %s" % e)
    carried = sorted(set(an.indirect))
    print("indirect calls receiving the object: %d" % len(carried))
    for e in carried:
        print("  INDIRECT %08X %08X %-40s args %s" % e)
    return 0 if found == MACHINE else 1


if __name__ == "__main__":
    sys.exit(main())
