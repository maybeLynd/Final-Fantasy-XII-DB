"""What the 19,909-body frontier is made of, before anyone proposes how to reduce it.

WHY. The frontier - bodies declared by nothing, neither A nor B nor C - is 58 % of the census and
the largest single population in the database. Every plan for it so far has been a plan for a
NUMBER: "disposition more", "explain more". A number that large is never one kind of thing, and the
EC-7 rule this role holds is that a bulk disposition must be earned per population rather than
applied to a total.

So this measures the shape and proposes nothing. Four cuts, each chosen because it changes what the
right next action would be:

  SIZE        a 6-byte thunk and a 5,000-byte body are not the same work. If the frontier is mostly
              tiny, its headline count overstates the reading left to do; if mostly large, the
              opposite.
  THUNK FLAG  the function list already marks thunks. A thunk forwards and holds no behaviour of its
              own, so a frontier made largely of thunks is a DIFFERENT problem from one made of
              bodies - and the flag is data, not a guess from size.
  NAMED       a body the list names (not `FUN_*`) has been identified by somebody, somewhere, even
              if no page declares it. That is a different starting point from an unnamed one.
  CONTIGUITY  library code arrives in ADDRESS RUNS. A frontier that clusters into long unbroken runs
              has candidate C families in it; one that is evenly scattered through documented code
              does not, and proposing span dispositions for it would be the unsupported bulk
              disposition this role exists to refuse.

Nothing here disposes of anything. The output is the input to that decision, not the decision.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_dispositions as cd
import uc1_band

DB = 'Database/FFXII TZA'
FUNCTIONS = 'Database/Tools/work/graph/functions.tsv'

SIZE_BANDS = [(0, 16, 'thunk-sized'), (17, 64, 'a few instructions'),
              (65, 256, 'small'), (257, 1024, 'substantial'), (1025, 1 << 30, 'large')]


def band(n):
    for lo, hi, label in SIZE_BANDS:
        if lo <= n <= hi:
            return (lo, hi, label)
    return SIZE_BANDS[-1]


def rows(path):
    """entry -> (size, name, is_thunk) straight from the function list."""
    out = {}
    with open(path, encoding='utf-8', errors='replace') as fh:
        head = fh.readline().rstrip('\n').split('\t')
        try:
            i_e, i_n, i_b = head.index('entry'), head.index('name'), head.index('body_bytes')
            i_t = head.index('thunk')
        except ValueError:
            return out
        for line in fh:
            c = line.rstrip('\n').split('\t')
            if len(c) <= max(i_e, i_n, i_b, i_t):
                continue
            try:
                out[int(c[i_e], 16)] = (int(c[i_b]), c[i_n], c[i_t].strip().lower() == 'true')
            except ValueError:
                continue
    return out


def main():
    if not os.path.exists(FUNCTIONS):
        print('  CONTROL FAILED: no function list at %s' % FUNCTIONS)
        return 2
    sizes = cd.load_functions(FUNCTIONS)
    # RESTRICTED TO THE SCORED CENSUS, and the control below is why. The raw list holds 38,161 rows
    # and `load_functions` keeps 34,270 of them - it drops what the census excludes by design. Read
    # naively, this shape came out over 23,800 frontier bodies against the headline's 19,909, and the
    # 3,891 difference was entirely the rows the census never counted. Measuring a population's shape
    # over a wider population than the headline is the defect this session has found six times; here
    # the control caught it before it was published rather than after.
    meta = {e: v for e, v in rows(FUNCTIONS).items() if e in sizes}
    # UC-1 frontier bodies have no functions.tsv row - synthesise their meta
    # (size, UC1-FRONTIER name, not-thunk) from the band, or the coverage
    # control below drops them and the shape describes a subset.
    meta.update({e: v for e, v in uc1_band.meta_rows().items() if e in sizes})
    a_set, entry_only, any_interior, documented_any = cd.measure_a(DB, sizes)
    official = cd.evaluate(DB, sizes)

    # THE frontier, taken from check_dispositions rather than rebuilt here. This used to walk the
    # members files itself, under a comment claiming the definition was "EXACTLY
    # check_dispositions'". It was not, and the gap was invisible precisely because the comment
    # said otherwise: reading members files counts EVERY family, while the headline counts only
    # the ACCEPTED ones. Four families refused for overlapping A kept their ~300 members here, the
    # two frontiers came out 296 apart, and this control - which exists to catch exactly that -
    # fired on its own author. A second implementation of a definition is a second definition.
    claimed = official["claimed_set"]
    frontier = official["frontier_set"] & set(meta)

    print('--- control: functions %d, A %d, claimed by an accepted family %d ---'
          % (len(meta), len(a_set), len(claimed)))
    print('    frontier measured here      : %d' % len(frontier))
    print('    frontier per check_dispositions: %d' % official['frontier'])
    # WHAT THIS CONTROL TESTS NOW. The frontier is no longer rebuilt here, so the two figures can
    # no longer disagree about which bodies are DECLARED - that was the old failure and it is now
    # impossible by construction. What can still differ is coverage of the metadata table: a
    # frontier body with no row in functions.tsv silently drops out of every bucket below, and the
    # shape would then describe a subset while claiming to describe the frontier. A control that
    # cannot fail is not a control, so it now names the population it actually guards.
    if len(frontier) != official['frontier']:
        print('  CONTROL FAILED: %d frontier body/bodies have no metadata row, so the shape below'
              % (official['frontier'] - len(frontier)))
        print('  would describe a subset of the frontier while being read as the whole of it.')
        return 2

    fb = collections.Counter(band(meta[e][0]) for e in frontier)
    tot = sum(fb.values())
    print()
    print('--- by SIZE ---')
    for lo, hi, label in SIZE_BANDS:
        k, v = (lo, hi, label), fb.get((lo, hi, label), 0)
        rng = '%d-%d' % (lo, hi) if hi < (1 << 30) else '%d+' % lo
        print('    %-9s %6d %6.1f%%   %s' % (rng, v, 100.0 * v / max(1, tot), label))

    thunks = sum(1 for e in frontier if meta[e][2])
    named = sum(1 for e in frontier if not meta[e][1].upper().startswith('FUN_'))
    print()
    print('--- by WHAT THE LIST ALREADY KNOWS ---')
    print('    flagged as a THUNK by the function list : %6d  %5.1f%%' % (thunks, 100.0 * thunks / tot))
    print('    carrying a NAME that is not FUN_*       : %6d  %5.1f%%' % (named, 100.0 * named / tot))
    print('    total bytes in the frontier             : %6d' % sum(meta[e][0] for e in frontier))

    # contiguity: how much of the frontier sits in long unbroken runs of frontier bodies
    order = sorted(meta)
    runs, cur = [], 0
    for e in order:
        if e in frontier:
            cur += 1
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    runs.sort(reverse=True)
    for cut in (2, 8, 32, 128):
        n = sum(r for r in runs if r >= cut)
        print('    in an unbroken run of >= %-3d frontier bodies : %6d  %5.1f%%'
              % (cut, n, 100.0 * n / tot))
    print('    longest run: %d bodies' % (runs[0] if runs else 0))

    print()
    print('  THESE RUNS ARE MEASURED OVER THE WRONG POPULATION FOR THE QUESTION BELOW.')
    print('  5,349 of the 19,909 frontier bodies are already MENTIONED by some document, and')
    print('  they bridge the ones that are not. Over the 14,560 nobody has ever written an')
    print('  address for, the frontier SHATTERS: 3,298 runs - MORE runs over FEWER bodies than')
    print('  the 2,236 counted here - and the share in a run of >= 32 falls 44.2% to 15.8%.')
    print('  So span dispositions are substantially LESS worth attempting than the figures')
    print('  above imply. Run check_untouched_runs.py; see EVIDENCE-STANDARD 2026-09-13r.')
    print()
    print('  NOTHING IS DISPOSED OF HERE. A long run is a CANDIDATE for a C family and not a family:')
    print('  the PPFX row that carries 1,657 members earned it with a provenance argument, boundary')
    print('  controls and a member list, and a run length is none of those. What the runs decide is')
    print('  whether span dispositions are worth ATTEMPTING at all - if the frontier were evenly')
    print('  scattered through documented code, they would not be.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
