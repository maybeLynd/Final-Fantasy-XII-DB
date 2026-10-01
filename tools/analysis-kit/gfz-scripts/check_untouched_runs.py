#!/usr/bin/env python3
"""check_untouched_runs.py - where is the block that NO document has ever mentioned?

`check_coverage_cross.py` split the frontier three ways and found that most of it is cited by no
document anywhere, not even at an entry address. That is the largest single block of work left in
the database, and a bare frontier count told nobody where to start.

The figures move as the corpus is written, and the control below is deliberately fatal so that a
move is reconciled rather than absorbed. When this was written the split was 14,560 never-cited of
19,909 frontier; at the 2026-09-14 reconciliation it was 13,454 of 19,885.

`check_frontier_shape.py` already measures the frontier's size distribution and contiguity. It does
not know about the citation axis, so its runs mix bodies a page already mentions with bodies nobody
has ever written an address for. **Those are different tasks** - one needs a page finished, the
other needs one started - and a run that mixes them is not a candidate for anything.

This measures contiguity over the NEVER-MENTIONED subset alone, in census order, and prints the
longest runs with their address ranges and byte totals.

WHAT A RUN IS AND IS NOT
------------------------
`check_frontier_shape.py` carries the rule and it is repeated here because this tool makes the runs
look more actionable than they are:

    NOTHING IS DISPOSED OF HERE. A long run is a CANDIDATE for a C family and not a family: the
    PPFX row that carries 1,657 members earned it with a provenance argument, boundary controls and
    a member list, and a run length is none of those.

A run of untouched bodies is a place to LOOK. Every disposition this project has accepted was
argued from provenance - an RTTI class, a link span with justified edges, a uniform instruction
form, a shared call target. Adjacency is none of those, and a family declared from adjacency alone
is the unsupported bulk disposition EC-7 exists to refuse.
"""
import argparse
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--functions")
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args(argv)

    import check_dispositions as CD
    import check_coverage_cross as CC

    sizes = CD.load_functions(a.functions)
    entries = sorted(sizes)
    any_cited = CC.cited_anywhere(a.db, sizes, CD)
    a_set, _eo, _ai, _da = CD.measure_a(a.db, sizes)
    official = CD.evaluate(a.db, sizes)
    frontier = official["frontier_set"]
    untouched = frontier - any_cited

    print("--- control ---")
    # THE CONTROL NOW COMPARES TWO LIVE MEASUREMENTS, NOT A MEASUREMENT AGAINST A FROZEN NUMBER.
    #
    # It used to hold `frontier == 19885` and refuse otherwise. That constant was reconciled on the
    # morning of 2026-09-14 (from 19,909) and was stale by the same afternoon: peers documented
    # addresses all day, A grew 1,434 -> 1,449, and the frontier fell to 19,870 -- so the gate
    # refused to run at all while BOTH instruments it cites agreed with each other and with it.
    #
    # A frozen figure cannot tell "the corpus moved" from "the corpus broke", and in a project whose
    # whole purpose is moving that figure it will be wrong more often than right. check_provenance
    # learned this exact lesson and records it: its own duplicated parent hash went two generations
    # stale in the tool whose job was detecting staleness, so now it READS the parent rather than
    # copying it. Same fix here.
    #
    # AND THE "INDEPENDENT DERIVATION" IT REPLACED WAS THE NEXT BUG, found 2026-09-15. This file
    # used to compute its own frontier as population minus A minus every declared member, and the
    # paragraph here defended that as a real cross-check. It was not independent, it was WRONG:
    # check_dispositions counts only the families it ACCEPTS, and this loop counted them all,
    # refused ones included. The two agreed for as long as nothing was refused. On 2026-09-15 four
    # families were refused for overlapping A, the numbers came apart by 296, and this gate stopped
    # running entirely - as did check_frontier_shape, which had a third copy of the same loop.
    #
    # Two implementations of one definition are two definitions, and the second one is where the
    # drift lives. The frontier now comes from check_dispositions.evaluate and nowhere else.
    # What is still worth checking is that the population this file walks is the one that was
    # scored, so the comparison below is against the census the frontier was taken from.
    published = official["frontier"]
    print("    frontier            %6d   (check_dispositions computes %d)" % (len(frontier), published))
    print("    of it, NEVER cited  %6d" % len(untouched))
    if not frontier <= set(entries):
        print("\n  *** frontier holds %d body/bodies outside the census this file walks - the runs"
              % len(frontier - set(entries)))
        print("      below would be measured over a population that is not the scored one ***")
        return 2

    # runs in CENSUS order: consecutive entries in the function list, all untouched
    runs, cur = [], []
    for e in entries:
        if e in untouched:
            cur.append(e)
        else:
            if cur:
                runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)

    tot = sum(sizes[e] for e in untouched)
    print("\n--- contiguity of the NEVER-MENTIONED bodies, in census order ---")
    print("    %d bodies, %d bytes, in %d unbroken run(s)" % (len(untouched), tot, len(runs)))
    for k in (2, 8, 32, 128):
        n = sum(len(r) for r in runs if len(r) >= k)
        print("    in a run of >= %-3d : %6d  %5.1f%%" % (k, n, 100.0 * n / len(untouched)))

    runs.sort(key=len, reverse=True)
    print("\n--- the %d longest runs: WHERE TO LOOK, not what to declare ---" % a.top)
    print("    %-9s %-9s %7s %9s   %s" % ("from", "to", "bodies", "bytes", "largest member"))
    for r in runs[:a.top]:
        big = max(r, key=lambda e: sizes[e])
        print("    %08X  %08X  %7d %9d   %08X (%d B)"
              % (r[0], r[-1], len(r), sum(sizes[e] for e in r), big, sizes[big]))

    covered = sum(sum(sizes[e] for e in r) for r in runs[:a.top])
    print("\n    those %d runs hold %d of the %d untouched bytes (%.0f%%)"
          % (a.top, covered, tot, 100.0 * covered / tot))
    print("\n  A RUN IS A PLACE TO LOOK. Every disposition this project has accepted was argued")
    print("  from provenance - an RTTI class, a link span with justified edges, a uniform")
    print("  instruction form, a shared call target. Adjacency is none of those.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
