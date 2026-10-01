"""Union two access censuses of one type, refusing if they disagree about any shared site.

WHY A TOOL AND NOT A ONE-LINER. Two censuses of the same type are built by different admission
rules - a route-tracked scan follows a tainted register and drops it the moment anything else writes
it; a chain scan admits every access reached through a fixed pointer hop. Each is narrower than the
other in a different direction, so the union is genuinely more evidence than either. But a union is
only safe if the two AGREE, and "they agree" is a claim that has to be checked rather than assumed:
if the same instruction is filed at two displacements, one of the two has the wrong base and merging
would bake a contamination into the result.

So this refuses to merge on any disagreement, and prints the disagreeing sites. A merge that cannot
fail is not a merge, it is a concatenation.

    merge_census.py <base.tsv> <addition.tsv> --out <merged.tsv>
"""
import argparse
import collections
import io
import sys


def read(path):
    head = None
    rows = []
    for n, line in enumerate(io.open(path, encoding='utf-8', errors='replace')):
        if not line.strip():
            continue
        c = line.rstrip('\n').split('\t')
        if n == 0:
            head = c
            continue
        if len(c) >= 6:
            rows.append(c)
    return head, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base')
    ap.add_argument('addition')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    hb, rb = read(a.base)
    ha, ra = read(a.addition)
    if hb != ha:
        print('HEADERS DIFFER, refusing:')
        print('  base    : %s' % '\t'.join(hb or []))
        print('  addition: %s' % '\t'.join(ha or []))
        return 2

    by_site = {}
    for c in rb:
        by_site[c[2].upper()] = c
    disagree = []
    added = kept = 0
    for c in ra:
        s = c[2].upper()
        if s in by_site:
            if by_site[s][3].lower() != c[3].lower():
                disagree.append((s, by_site[s][3], c[3]))
            kept += 1
        else:
            by_site[s] = c
            added += 1

    print('--- control: base %d rows, addition %d rows ---' % (len(rb), len(ra)))
    print('    shared sites %d, sites only in the addition %d' % (kept, added))
    if disagree:
        print()
        print('REFUSING TO MERGE: %d shared site(s) are filed at different displacements.' % len(disagree))
        for s, x, y in sorted(disagree)[:20]:
            print('    %s  base=%s  addition=%s' % (s, x, y))
        print('  One of the two has the wrong base at these sites. Merging would bake it in.')
        return 1

    out = sorted(by_site.values(), key=lambda c: (c[0].upper(), c[2].upper()))
    with io.open(a.out, 'w', encoding='utf-8', newline='') as fh:
        fh.write('\t'.join(hb) + '\n')
        for c in out:
            fh.write('\t'.join(c) + '\n')
    print()
    print('  no disagreement on any shared site; wrote %d rows to %s' % (len(out), a.out))
    per = collections.Counter(c[3] for c in out)
    print('  distinct displacements in the merged census: %d' % len(per))
    return 0


if __name__ == '__main__':
    sys.exit(main())
