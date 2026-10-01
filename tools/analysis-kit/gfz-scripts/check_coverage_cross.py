#!/usr/bin/env python3
"""check_coverage_cross.py - the completion surface on BOTH axes at once.

This database measures "explained" two independent ways and had never tabulated them together:

    CITATION      `engine_explained` - some document cites an address inside this body
    DECLARATION   EC-7 - a declared B/C family claims this body as a class

Crossing just one corner of them - the entry-only citations against the families - showed that
**half** of the largest stated gap in the project was already counted as explained elsewhere
(EVIDENCE-STANDARD addendum 2026-09-13p). This runs the same cross over the whole population,
and answers what neither measure can answer alone: what does each contribute that the other does
not, and **how much of the engine is touched by neither?**

THE 57% IS NOT A COMPLETION FIGURE, AND THIS TOOL WILL NOT CALL IT ONE
---------------------------------------------------------------------
The union of the two measures covers ~57.5% of the census. That number must never be quoted as
progress. The two axes have completely different bars: `A` requires a DOCUMENTED page to cite
inside the body, a declared family requires a falsifiable class claim, and the citation axis at its
weakest requires only that *some* document mention an address - which is the entire reason the
entry-only qualifier exists. **A union of a strong measure and a weak one inherits the weak bar.**

What the union IS good for is its complement. The bodies that NO document cites and NO family
claims are touched by nothing at all, and that number is not published anywhere else.
"""
import argparse
import bisect
import io
import sys

HERE = __file__.rsplit("/", 1)[0] if "/" in __file__ else "."
sys.path.insert(0, HERE)


def cited_anywhere(db, sizes, CD):
    """Every body some document cites inside - engine_explained's own measure."""
    entries = sorted(sizes)
    out = set()
    for p in CD.docs(db):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        for h in CD.CITE.findall(t):
            v = int(h, 16)
            i = bisect.bisect_right(entries, v) - 1
            if i < 0:
                continue
            e = entries[i]
            if e <= v < e + sizes[e]:
                out.add(e)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--functions")
    a = ap.parse_args(argv)

    import check_dispositions as CD
    import uc1_band
    sizes = CD.load_functions(a.functions)
    pop = set(sizes)
    any_cited = cited_anywhere(a.db, sizes, CD)
    a_set, entry_only, _ai, _da = CD.measure_a(a.db, sizes)
    dec = set()
    for doc, parts in CD.parse_families(a.db):
        if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
            continue
        try:
            dec.update(CD.read_members(doc, parts[2]))
        except (IOError, OSError, ValueError):
            pass

    # THE CONTROL IS FATAL. A cross-tabulation whose marginals do not reproduce the published
    # figures is measuring some other population, and would be far more convincing than it
    # deserves. check_frontier_shape.py refuses to print percentages for the same reason.
    print("CONTROL - marginals against the published figures")
    print("  population              %6d" % len(pop))
    _uc1 = uc1_band.frontier_starts() & pop
    if _uc1:
        print("      post-2026-09-28: %d listed + %d UC-1 frontier"
              % (len(pop) - len(_uc1), len(_uc1)))
    print("  cited anywhere, any doc %6d" % len(any_cited))
    print("  declared B/C/D          %6d" % len(dec))
    print("  A                       %6d" % len(a_set))
    # THE CONSTANTS ARE GONE, AND WHAT REPLACES THEM IS STRONGER, NOT WEAKER. 2026-09-14 (OPUS).
    #
    # This used to require `len(pop) == 34270 and len(dec) == 12951 and len(a_set) == 1410`. But
    # all three are computed HERE, from CD.load_functions, CD.measure_a and CD.parse_families --
    # the same code path check_dispositions itself uses. So the test compared check_dispositions
    # against a frozen copy of itself, and could never detect the thing the note below it feared,
    # "measuring some other population": both sides agree by construction. What it actually
    # detected was that the corpus had moved since someone last edited the line, and it fired
    # constantly -- A went 1,410 -> 1,434 -> 1,443 -> 1,444 inside a single day of ordinary
    # documentation work, refusing to print the table each time.
    #
    # A control that goes red whenever the project makes progress teaches people to bump it, and a
    # fatal control that is bumped on sight is decoration. These invariants hold however far the
    # corpus moves, and still fail loudly on a real partition defect:
    #
    #   * every band is a subset of the census population -- a body counted in a band but absent
    #     from the census IS the "some other population" case, stated directly;
    #   * A is a subset of cited-anywhere, because A MEANS an interior citation from a documented
    #     page, so an A body that no document cites is a contradiction inside the measurement.
    #
    # UC-1 2026-09-28: the band's frontier bodies are frontier BY RULING - a
    # family declaration naming one is refused in evaluate, so it cannot count
    # as declared here either, and a mechanical cite cannot make one A.
    dec -= uc1_band.frontier_starts()
    # A family member that is `remove-listed` (007EE7F0, adjudicated a false
    # entry) is a STALE DECLARATION - evaluate refuses it - not a partition
    # defect. Named, counted, excluded.
    stale_dec = dec - pop
    dec &= pop
    if stale_dec:
        print("      (%d declared member(s) fall outside the post-break"
              " population - stale declarations, e.g. %08X)"
              % (len(stale_dec), sorted(stale_dec)[0]))
    bad = []
    if not a_set <= pop:
        bad.append("A has %d body(s) outside the census population" % len(a_set - pop))
    if not dec <= pop:
        bad.append("declared B/C/D has %d body(s) outside the census population" % len(dec - pop))
    if not any_cited <= pop:
        bad.append("cited-anywhere has %d body(s) outside the census population"
                   % len(any_cited - pop))
    if not a_set <= any_cited:
        bad.append("%d body(s) are counted in A but cited by no document at all"
                   % len(a_set - any_cited))
    if bad:
        print("\n  *** THE PARTITION IS NOT INTERNALLY CONSISTENT ***")
        for b in bad:
            print("      %s" % b)
        print("  Refusing to print the table: a cross-tabulation over a population it does not")
        print("  agree with would be far more convincing than it deserves.")
        return 2
    print("  -> partition consistent (every band inside the population; A inside cited)")

    print("\nTHE CROSS")
    print("  %-31s %9s %9s %9s" % ("", "declared", "not", "total"))
    for label, s in (("A  cited INSIDE, DOCUMENTED", a_set),
                     ("entry-only, DOCUMENTED", entry_only),
                     ("cited, but neither of those", any_cited - a_set - entry_only),
                     ("NOT cited by any document", pop - any_cited)):
        d = len(s & dec)
        print("  %-31s %9d %9d %9d" % (label, d, len(s) - d, len(s)))
    print("  %-31s %9d %9d %9d" % ("TOTAL", len(dec), len(pop - dec), len(pop)))

    # A and declared must not intersect: the gate refuses a family member measured as A.
    print("\n  INVARIANT  A and declared are disjoint: %s (%d overlap)"
          % ("holds" if not (a_set & dec) else "*** VIOLATED ***", len(a_set & dec)))

    union = any_cited | dec
    print("\n  cited only, no family    %6d   the citation axis's unique reach" % len(any_cited - dec))
    print("  family only, never cited %6d   EC-7's unique reach" % len(dec - any_cited))
    print("  both                     %6d" % len(any_cited & dec))
    print("  TOUCHED BY EITHER        %6d  (%.2f%% - NOT a completion figure, see the docstring)"
          % (len(union), 100.0 * len(union) / len(pop)))
    print("  TOUCHED BY NEITHER       %6d  (%.2f%%)" % (len(pop - union),
                                                        100.0 * len(pop - union) / len(pop)))

    frontier = pop - (a_set | dec)
    print("\n  THE FRONTIER DECOMPOSED - %d bodies that A and the families both miss:" % len(frontier))
    print("    no document mentions them at all %6d" % len(frontier - any_cited))
    print("    entry-only mention               %6d" % len(frontier & entry_only))
    print("    cited some other way             %6d" % len(frontier & (any_cited - entry_only)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
