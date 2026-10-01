"""Which dimension actually blocks certification for each subsystem, read off PARITY-STATUS.md.

PROGRAM-STATE says nothing is parity certified because "INTEGRATION and FULL-SUBSYSTEM are NOT
COVERED by every pilot". That was written on 2026-09-08 against 6 pilots. It is a UNIVERSAL claim over
a population that has since grown to 43, so it has to be re-established rather than carried forward -
the same rule this database applies to every other universal.

Prints, per subsystem, the non-`n/a` dimensions that are not covered; a subsystem with an empty list
would be certifiable on coverage grounds. Reads the generated matrix, so it cannot disagree with it.
"""
import io, re, collections

P = 'Database/FFXII TZA/_index/PARITY-STATUS.md'
lines = io.open(P, encoding='utf-8').read().split('\n')

hdr = next(l for l in lines if l.startswith('| dimension |') and '`' in l)
cols = [c.strip().strip('`') for c in hdr.strip('|').split('|')][1:]

DIMS = ('CALCULATION', 'STRUCTURAL', 'STATE-TRANSITION', 'CONTRACT', 'EDGE-CASE', 'SERIALIZATION',
        'RNG', 'TIMING', 'INTEGRATION', 'PRESENTATION', 'FULL-SUBSYSTEM')
grid = {}
for l in lines:
    if not l.startswith('| **'):
        continue
    cells = [c.strip() for c in l.strip('|').split('|')]
    name = cells[0].strip('*')
    if name not in DIMS or name in grid:
        continue
    vals = [c.strip('*').strip() for c in cells[1:]]
    if len(vals) != len(cols):
        continue
    grid[name] = vals
missing = [d for d in DIMS if d not in grid]
assert not missing, 'dimension rows not parsed: %s' % missing

blockers = {}
for j, sub in enumerate(cols):
    blockers[sub] = [d for d in DIMS if grid[d][j] == 'no']

# the claim under test
uni = [d for d in ('INTEGRATION', 'FULL-SUBSYSTEM')
       if all(grid[d][j] == 'no' for j in range(len(cols)))]
print('subsystems: %d' % len(cols))
print('dimensions NOT COVERED by *every* subsystem: %s' % (', '.join(uni) or 'none'))
for d in ('INTEGRATION', 'FULL-SUBSYSTEM', 'TIMING', 'PRESENTATION'):
    cov = [cols[j] for j in range(len(cols)) if grid[d][j] == 'yes']
    print('   %-15s covered by %d: %s' % (d, len(cov), ', '.join(cov) or '-'))
print()
certifiable = [s for s in cols if not blockers[s]]
print('subsystems with no uncovered dimension: %s' % (', '.join(certifiable) or 'none'))
print()
freq = collections.Counter()
for s in cols:
    for d in blockers[s]:
        freq[d] += 1
print('how often each dimension is the blocker:')
for d, c in freq.most_common():
    print('   %-15s blocks %d of %d' % (d, c, len(cols)))
print()
fewest = sorted(cols, key=lambda s: len(blockers[s]))[:6]
print('closest to certification:')
for s in fewest:
    print('   %-22s %d blocker(s): %s' % (s, len(blockers[s]), ', '.join(blockers[s])))
