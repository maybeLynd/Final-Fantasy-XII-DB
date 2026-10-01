"""rc4_derived.py - RC-4's remaining step: does any store reach the capture machine's state word at +0xDAC through a
pointer derived at another offset? OPUS, 2026-09-30. Static. Reads only.

Every function in the catalogue is run through the value-flow engine of k14_actorflow.py (registers, own stack,
lea/add offsets, switch tables), seeded with its entry registers and callee-saved registers as roots. A pointer loaded
from memory is its own root. Calls do not descend. They apply a one-level summary instead: a function whose return
value is an entry register plus a constant (a getter handing out `obj + K`) makes the caller's rax that register's
value plus K.

For every store, the effective offset from its root is the root offset plus the instruction's displacement. The census
lists every store whose written bytes cover root + 0xDAC (the machine's state word):
  DIRECT   the instruction's own displacement is 0xDAC or reaches it (the form rc4_census already covers);
  DERIVED  the root offset is not 0 - the pointer was formed at another offset (the RC-4 question);
  INDEXED  the root offset is unknown (pointer + index) and the displacement is at most 0xDAC; listed only in
           functions that also touch +0xDAC or +0xDB8 directly (the machine's fields), since without types every
           indexed store in the image would qualify.
Controls: DIRECT must include the machine's four stores (00187891, 001878B3, 001878D5, 001878E5) and the
constructor's (00185020); DERIVED is then read against the values stored.
"""
import collections, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K  # noqa: E402
from capstone import x86 as X  # noqa: E402

R = K.R
TARGET = 0xDAC
MACHINE = {0x00187891, 0x001878B3, 0x001878D5, 0x001878E5, 0x00185020}


class Census(K.Analysis):
    def __init__(self, getters):
        super().__init__()
        self.getters = getters
        self.hits = []
        self.touch = set()
        self.cur_ret = None

    def summary(self, f, ctx, depth, stack):
        return (K.UNK, ())

    def call(self, f, st, i, t, depth, stack, caller_writes):
        g = self.getters.get(t)
        rv = K.UNK
        if g is not None:
            reg, k = g
            v = st.r.get(reg, K.UNK)
            rv = K.add(v, k) if v is not K.UNK else K.UNK
        for r in K.VOLATILE:
            st.r[r] = K.UNK
        st.r["rax"] = rv if rv is not K.UNK else K.vs(("R%08X" % t, 0))
        return st

    def store(self, f, i, st, addr, size, val):
        op = i.operands[0] if i.operands else None
        disp = op.mem.disp if op is not None and op.type == X.X86_OP_MEM else None
        if disp is not None and disp <= TARGET < disp + size:
            self.touch.add(f)
        if addr is not K.UNK:
            for b, o in addr:
                if b is None or b in ("SP", "CSP") or str(b).startswith("G"):
                    continue
                if o is not None and o <= TARGET < o + size:
                    kind = "DIRECT" if disp is not None and disp <= TARGET < disp + size else "DERIVED"
                    self.hits.append((kind, f, i.address, "%s %s" % (i.mnemonic, i.op_str), K.desc(addr), K.desc(val)))
                elif o is None and disp is not None and 0 <= disp <= TARGET and op.mem.index != 0:
                    self.hits.append(("INDEXED", f, i.address, "%s %s" % (i.mnemonic, i.op_str), K.desc(addr), K.desc(val)))
        o = K.sp_off(addr)
        if o is not None:
            for k in [k for k in st.s if k < o + size and o < k + 8 and k != o]:
                del st.s[k]
            if size == 8:
                st.s[o] = val
            else:
                st.s.pop(o, None)
        elif addr is K.UNK or any(b == "SP" for b, _ in addr):
            st.s.clear()


def entry_ctx():
    return tuple(sorted((r, K.vs(("%s@e" % r, 0))) for r in ("rcx", "rdx", "r8", "r9")))


def run_one(an, f):
    an.memo.clear()
    ctx = dict(entry_ctx())
    # callee-saved registers are roots as well
    res = an.run(f, ctx, 0, (f,))
    return res


def main():
    fns = sorted(K.ext)
    # pass 1: getters - functions whose return value is an entry register plus a constant
    getters = {}
    g_an = Census({})
    for f in fns:
        try:
            ret, _ = run_one(g_an, f)
        except Exception:
            continue
        if ret is not K.UNK and len(ret) == 1:
            (b, o), = ret
            if isinstance(b, str) and b.endswith("@e") and o is not None and 0 < o <= TARGET:
                getters[f] = (b[:-2], o)
    print("getters handing out entry + K (0 < K <= 0xDAC): %d" % len(getters))
    an = Census(getters)
    errors = 0
    for f in fns:
        try:
            run_one(an, f)
        except Exception:
            errors += 1
    direct = [h for h in an.hits if h[0] == "DIRECT"]
    derived = sorted(set(h for h in an.hits if h[0] == "DERIVED"))
    indexed = sorted(set(h for h in an.hits if h[0] == "INDEXED" and h[1] in an.touch))
    found = MACHINE & set(h[2] for h in direct)
    print("%s  control: DIRECT includes the machine's and the constructor's stores: %d of %d (%s)" % (
        "PASS" if found == MACHINE else "FAIL", len(found), len(MACHINE), " ".join("%08X" % a for a in sorted(MACHINE - found)) or "all"))
    print("functions analysed: %d (errors %d); DIRECT %d, DERIVED %d, INDEXED in +0xDAC/+0xDB8 functions %d" % (
        len(fns), errors, len(set(h[2] for h in direct)), len(derived), len(indexed)))
    for h in derived + indexed:
        print("  %-8s %08X %08X %-44s base %-24s value %s" % h)
    with io.open(os.path.join(HERE, "rc4_derived.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("kind\tfunction\taddress\tinstruction\tbase\tvalue\n")
        for h in sorted(set(an.hits)):
            o.write("%s\t%08X\t%08X\t%s\t%s\t%s\n" % h)
    return 0 if found == MACHINE else 1


if __name__ == "__main__":
    sys.exit(main())
