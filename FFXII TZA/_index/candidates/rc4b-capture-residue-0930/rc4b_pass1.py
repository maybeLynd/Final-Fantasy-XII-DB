"""rc4b_pass1.py - RC-4 residue, pass 1: what the render object stores INTO ITSELF (ORACLE, 2026-09-30). Static.

Runs OPUS's flow (../rc4-capture-machine-0930/rc4_flow.py, on k14_actorflow.py) unchanged, and additionally records every
store whose address is the object at a KNOWN offset (A+K) and whose value is either
  - object-derived (A+K'): a self-pointer field; or
  - a global address (the flow's G<addr> token), which for a .rdata target is a vtable pointer.
It also records every analysed context (function, receiver) and the flow's residue lists. Output: rc4b_pass1.out and
rc4b_selffields.tsv, which pass 2 (rc4b_pass2.py) consumes.
Control: the same five machine and constructor stores as OPUS's control.
"""
import contextlib, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc4-capture-machine-0930"))
import rc4_flow as F  # noqa: E402
K = F.K

SELF = []     # (fn, ins addr, dest offset, value desc)
VT = []       # (fn, ins addr, dest offset, global)
_orig_store = F.Flow.store
holder = {}


def store(self, f, i, st, addr, size, val):
    if addr is not K.UNK and len(addr) == 1 and size == 8:
        (b, o), = addr
        if b == "A" and o is not None and val is not K.UNK:
            if K.has_actor(val):
                SELF.append((f, i.address, o, K.desc(val)))
            elif len(val) == 1 and str(next(iter(val))[0]).startswith("G"):
                VT.append((f, i.address, o, next(iter(val))[0]))
    return _orig_store(self, f, i, st, addr, size, val)


F.Flow.store = store
_init = F.Flow.__init__


def init(self):
    _init(self)
    holder["an"] = self


F.Flow.__init__ = init


def offsets_handed_out(an):
    """Every offset K at which an object-derived pointer A+K crosses a call boundary (an analysed context's argument)
    or is stored as a self-pointer value; K = 0 included."""
    S = set()
    for (f, k) in an.memo:
        for _r, v in k:
            if v is not K.UNK and v is not None:
                for b, o in v:
                    if b == "A" and o is not None:
                        S.add(o)
    for _f, _a, _off, v in SELF:
        for part in v.split(","):
            if part.startswith("A+"):
                S.add(int(part[2:], 16))
            elif part == "A":
                pass
    return S


def main():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = F.main()
    out = buf.getvalue()
    print(out.splitlines()[1])  # the control line
    an = holder["an"]
    with io.open(os.path.join(HERE, "rc4b_selffields.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("kind\tfunction\tinstruction\toffset\tvalue\n")
        for f, a, off, v in sorted(set(SELF)):
            o.write("SELF\t%08X\t%08X\t%#x\t%s\n" % (f, a, off, v))
        for f, a, off, g in sorted(set(VT)):
            o.write("VTBL\t%08X\t%08X\t%#x\t%s\n" % (f, a, off, g))
    print("self-pointer stores at a known offset: %d; global-pointer stores at a known offset: %d" % (len(set(SELF)), len(set(VT))))
    for r in sorted(set(SELF)):
        print("  SELF %08X %08X A%+#x <- %s" % r)
    for r in sorted(set(VT)):
        print("  VTBL %08X %08X A%+#x <- %s" % r)
    ctxs = {}
    for (f, k) in an.memo:
        ctxs.setdefault(f, set()).add(K.desc(dict(k).get("rcx")))
    for f in (0x0018A120, 0x001858A0, 0x00188640, 0x001897C0, 0x00186CD0, 0x00185A90, 0x00189CE0, 0x00185C30, 0x00184AF0,
              0x001F1E80, 0x0060CE50, 0x001F0AD0):
        print("contexts %08X rcx: %s" % (f, sorted(ctxs.get(f, ()))))
    S = offsets_handed_out(an)
    print("offsets K handed out as A+K: %d: %s" % (len(S), " ".join("%#x" % x for x in sorted(S))))
    with io.open(os.path.join(HERE, "rc4b_offsets.txt"), "w", encoding="utf-8") as o:
        o.write(" ".join("%#x" % x for x in sorted(S)))
    return rc


if __name__ == "__main__":
    sys.exit(main())

