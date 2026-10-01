"""objflow.py - OPUS's reusable object-writer census (2026-09-30): who can write bytes [LO, HI) of one object?

It retargets the value-flow census of `_index/candidates/ov58d-pointer-flow-0930/ov58d_flow.py` (itself built on
k14_actorflow.py: registers, own stack, lea/add offsets, switch tables, callees under their argument values to depth
10, xmm halves, by-reference stack structures, escapes into globals iterated to a fixpoint) at any object that is
reached through a pointer global and/or lives at a static address:

  python -B objflow.py --ptr 0209CC40 --static 0209D490 0209E598 --region 0x1060 0x1098 [--out hits.tsv]

  --ptr G         a qword global holding the object's address (a load of [G] yields object + 0); repeatable
  --static A B    the object is the static range [A, B); a rip-relative address inside it is object + (addr - A)
  --region LO HI  object-relative byte range to report writers of
  --getter F:K    a function whose return value is object + K (repeatable; K may be negative)
  --base A        with --static: the absolute address that is object + 0 (default: the start of the static range), for
                  an object that sits inside a larger static block

Every store whose base is object-derived is classified (ov58d's classes): REGION (a known offset overlapping
[LO, HI)), INDEXED-BELOW (base + a runtime index, base below HI: a non-negative index can reach it), INDEXED-UNKNOWN,
INDEXED-ABOVE / STATE-OTHER (cannot reach it). Escapes, indirect calls and depth cuts are the blind spots and are
printed. A negative is a statement about this census, not proof of absence.
"""
import argparse, collections, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "ov58d-pointer-flow-0930"))
import ov58d_flow as O  # noqa: E402

K = O.K


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ptr", action="append", default=[])
    ap.add_argument("--static", nargs=2)
    ap.add_argument("--region", nargs=2, required=True)
    ap.add_argument("--getter", action="append", default=[])
    ap.add_argument("--base")
    ap.add_argument("--out")
    a = ap.parse_args()
    h = lambda s: int(s, 16) if not s.lower().startswith("0x") else int(s, 0)
    lo, hi = int(a.region[0], 0), int(a.region[1], 0)
    # retarget the census: no registry rows, no record getter, no image getters
    O.LO, O.HI = lo, hi
    O.REG_CELLS.clear()
    O.REG_ROWS = (0, 0)
    O.REC_GETTER = O.IMG_GETTER = O.CAP_GETTER = -1
    O.globals_root.clear()
    O.TABLES.clear()
    ptrs = [h(p) for p in a.ptr]
    for g in ptrs:
        O.globals_root[g] = frozenset([("A", 0)])
    if a.static:
        O.IMG_LO, O.IMG_HI = h(a.static[0]), h(a.static[1])
        O.STATE_ABS = h(a.base) if a.base else O.IMG_LO
    else:
        O.IMG_LO = O.IMG_HI = O.STATE_ABS = 0
    getters = {}
    for gk in a.getter:
        f, k = gk.split(":", 1)
        getters[h(f)] = int(k, 0)
    if getters:
        orig_call = O.Census.call

        def call(self, f, st, i, t, depth, stack, caller_writes):
            if t in getters:
                for r in K.VOLATILE:
                    st.r[r] = K.UNK
                st.r["rax"] = K.vs(("A", getters[t]))
                return st
            return orig_call(self, f, st, i, t, depth, stack, caller_writes)
        O.Census.call = call
    t0 = time.time()
    refs, calls = O.scan()
    for g in ptrs:
        print("pointer %08X: %d rip references (%d loads)" % (g, len(refs.get(g, ())), sum(1 for x in refs.get(g, ()) if x[2])))
    extra = set(c for f in getters for c in calls.get(f, ()))
    for attempt in range(1, 4):
        before, before_t = dict(O.globals_root), set(O.TABLES)
        an, done = fixpoint(refs, calls, extra, t0)
        seen = {}
        for fn, ad, text, where in set(an.escapes):
            w = where.strip("{}").split(",")[0].strip()
            if w.startswith("G") and "?" not in w:
                g, _, off = w[1:].partition("+")
                ga = int(g, 16) + (int(off, 0) if off else 0)
                if ga not in ptrs:
                    seen[ga] = frozenset(an.esc_vals.get(ga) or {("A", None)})
        moved = {g: v for g, v in seen.items() if before.get(g) != v}
        tables = set(an.esc_tables) & set(seen)
        print("pass %d: escape globals %s" % (attempt, ", ".join("%08X%s" % (g, "[table]" if g in tables else "") for g in sorted(seen)) or "none"))
        if not moved and tables == before_t:
            break
        O.globals_root.update(moved)
        O.TABLES.clear()
        O.TABLES.update(tables)
    hits = sorted(set(an.hits))
    by = collections.Counter(x[0] for x in hits)
    print("root functions %d; bodies reached %d (contexts %d); object stores by class: %s (%.0f s)" % (
        len(done), len(an.fns), len(an.memo), dict(sorted(by.items())), time.time() - t0))
    reach = [x for x in hits if x[0] in ("REGION", "INDEXED-BELOW", "INDEXED-UNKNOWN")]
    print("stores that can reach [%#x, %#x): %d in %d functions" % (lo, hi, len(reach), len(set(x[1] for x in reach))))
    for x in reach:
        print("  %-15s %08X %08X %-48s size %d  base %s" % x)
    print("blind spots: escapes %d, indirect calls carrying the object %d, recursion/depth cuts %d" % (
        len(set(an.escapes)), len(set(an.indirect)), sum(1 for r in an.recursive if r[2])))
    for e in sorted(set(an.escapes))[:40]:
        print("  escape %08X %08X %s -> %s" % e)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fo:
            fo.write("class\tfunction\taddress\tinstruction\tsize\tbase\n")
            for x in hits:
                fo.write("%s\t%08X\t%08X\t%s\t%d\t%s\n" % x)
    return reach


def fixpoint(refs, calls, extra, t0):
    an = O.Census()
    done, rounds = set(), 0
    while True:
        rounds += 1
        roots = set(f for g in list(O.globals_root) for f, _, _ in refs.get(g, ()))
        roots |= set(f for g, xs in refs.items() for t in O.TABLES if t <= g < t + O.TABLE_SPAN for f, _, _ in xs)
        if O.IMG_HI > O.IMG_LO:
            roots |= set(f for g, xs in refs.items() if O.IMG_LO <= g < O.IMG_HI for f, _, _ in xs)
        roots |= extra
        roots |= set(c for f in an.state_returners for c in calls.get(f, ()))
        new = sorted(roots - done)
        if not new:
            break
        for f in new:
            try:
                an.summary(f, (), 0, ())
            except Exception as e:  # noqa: BLE001
                print("  error in %08X: %s %r (its stores are a blind spot)" % (f, type(e).__name__, e))
        done |= set(new)
        added = 0
        for fn, ad, text, where in set(an.escapes):
            w = where.strip("{}").split(",")[0].strip()
            if w.startswith("G") and "?" not in w:
                g, _, off = w[1:].partition("+")
                ga = int(g, 16) + (int(off, 0) if off else 0)
                if ga not in O.globals_root:
                    O.globals_root[ga] = frozenset(an.esc_vals.get(ga) or {("A", None)})
                    if ga in an.esc_tables:
                        O.TABLES.add(ga)
                    added += 1
        print("round %d: %d new root functions, %d new escape globals (%.0f s)" % (rounds, len(new), added, time.time() - t0))
    return an, done


if __name__ == "__main__":
    main()
