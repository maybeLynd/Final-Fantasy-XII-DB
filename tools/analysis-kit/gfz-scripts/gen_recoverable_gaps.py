"""Regenerate `_types/recoverable-layout-gaps.tsv`: layout gaps that ALREADY have census accesses.

The file existed as a one-off artefact with a `Generated 2026-09-13` line and no generator, so the
first field recovered out of it made it stale with nothing to re-run. That is the failure this
session spent its morning on - eight committed index artefacts found stale - reproduced in a file
about finding things. So the generator now lives here.

WHAT A ROW IS. A declared-layout gap in a censused type, with the count and widths of the census
accesses that land inside it. **Candidates, not fields.** An access inside a gap may be an indexed
read into an array declared elsewhere, so each row has to be read before anything is declared -
`CharacterRenderRecord 0x180` was read on 2026-09-13 and turned out to be a 4x4 affine matrix whose
three zero lanes are written through an integer register, which no row of this file could have said.

The censuses and their cleaning rules are IMPORTED from `check_census_widths`, never restated. A
first version of a different instrument re-declared a sibling's matchers and produced 621 against the
gate's 583 - a decomposition of a corpus that was not quite the one it claimed to explain.
"""
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_census_widths as ccw

DB = 'Database/FFXII TZA'
TYPES = os.path.join(DB, '_types', 'types.tsv')
FIELDS = os.path.join(DB, '_types', 'fields.tsv')
OUT = os.path.join(DB, '_types', 'recoverable-layout-gaps.tsv')
# Verdicts on individual candidate DISPLACEMENTS, keyed (type, displacement). The registry is
# regenerated and cannot carry them; without them a reader cannot tell a displacement nobody has
# looked at from one that was read and REFUSED, which are opposite states. Keyed on displacement
# rather than on the gap because gap boundaries move whenever a neighbour is declared, and a
# ruling about evidence at one offset stays true when the gap around it changes shape.
DISPO = os.path.join(DB, '_types', 'recoverable-layout-gaps-dispositions.tsv')


def _load_dispositions():
    """-> {(type, displacement_int): verdict}. Absent file is not an error: it means nothing has
    been adjudicated yet, and every row then reports OPEN, which is the honest reading."""
    got = {}
    if not os.path.isfile(DISPO):
        return got
    for line in io.open(DISPO, encoding='utf-8', errors='replace'):
        if line.startswith('#') or not line.strip():
            continue
        f = line.rstrip('\n').split('\t')
        if len(f) < 3 or f[1] == 'displacement':
            continue
        try:
            got[(f[0], int(f[1], 16))] = f[2]
        except ValueError:
            continue
    return got


def declared(type_name):
    """(offset, size) rows for one type, from the field store."""
    rows = []
    for n, line in enumerate(io.open(FIELDS, encoding='utf-8')):
        if n == 0 or not line.strip():
            continue
        c = line.rstrip('\n').split('\t')
        if len(c) < 3 or c[0] != type_name:
            continue
        try:
            rows.append((int(c[1], 16), int(c[2])))
        except ValueError:
            continue
    return sorted(rows)


sizes = ccw.type_sizes(TYPES)
tally = collections.Counter()
out = []

for tname, census_file, sbase, shift, extent in ccw.censused_types():
    path = None
    for root, _d, files in os.walk(DB):
        if census_file in files:
            path = os.path.join(root, census_file)
            break
    if path is None:
        tally['census_missing'] += 1
        continue
    if sbase is None:
        per, _dropped = ccw.clean(path, tally)
    else:
        per = ccw.clean_static(path, sbase, sizes.get(tname, 0), tally)
    if shift:
        # A sub-object's offsets are its own; its parent's census records them shifted. This
        # file had the extent clip already - it is the one consumer that copied the good
        # version - and now shares the single implementation with the other three.
        per = dict((ccw.rebase(d, shift, extent), w) for d, w in per.items()
                   if ccw.rebase(d, shift, extent) is not None)
    rows = declared(tname)
    if not rows:
        continue
    total = sizes.get(tname)
    # the gaps: between the end of one declared field and the start of the next, plus the tail
    edges = []
    cursor = 0
    for off, size in rows:
        if off > cursor:
            edges.append((cursor, off))
        cursor = max(cursor, off + size)
    if total and cursor < total:
        edges.append((cursor, total))

    for start, end in edges:
        inside = sorted(d for d in per if start <= d < end)
        if not inside:
            continue
        desc = ' '.join('%X:%s' % (d, '/'.join('%dx%d' % (c, w) for w, c in
                                               sorted(per[d].items())))
                        for d in inside)
        out.append((len(inside), tname, start, end, end - start, desc, inside))

out.sort(key=lambda r: (-r[0], r[1], r[2]))

# A GAP IS DISPOSITIONED ONLY WHEN EVERY DISPLACEMENT INSIDE IT IS. One unruled displacement
# leaves the whole row OPEN - otherwise a gap could be marked settled while carrying evidence
# nobody has read, which is exactly the confusion this column exists to remove.
_dispo = _load_dispositions()
_verdicts = []
for _r in out:
    _seen = [_dispo.get((_r[1], _d)) for _d in _r[6]]
    if all(_seen):
        _verdicts.append('+'.join(sorted(set(_seen))))
    else:
        _verdicts.append('OPEN')
_open = sum(1 for _v in _verdicts if _v == 'OPEN')

store_types = set()
store_fields = collections.Counter()
for _n, _l in enumerate(io.open(FIELDS, encoding='utf-8')):
    if _n == 0 or not _l.strip():
        continue
    store_fields[_l.split('\t')[0]] += 1
for _n, _l in enumerate(io.open(TYPES, encoding='utf-8')):
    if _n == 0 or not _l.strip():
        continue
    store_types.add(_l.split('\t')[0])
_cen = {t for t, _f, _b, _sh, _ex in ccw.censused_types()} & store_types
_cov_t = 100.0 * len(_cen) / max(1, len(store_types))
_cov_f = 100.0 * sum(store_fields[t] for t in _cen) / max(1, sum(store_fields.values()))

# How many uncensused types even record HOW they are reached. This is measured rather than stated,
# because it is the figure that says whether the next census is a script run or a piece of research.
_no_route = _some_route = 0
for _n, _l in enumerate(io.open(TYPES, encoding='utf-8')):
    if _n == 0 or not _l.strip():
        continue
    _c = _l.rstrip('\n').split('\t')
    if _c[0] in _cen:
        continue
    _inst = (_c[3] if len(_c) > 3 else '').strip()
    if not _inst or _inst == 'UNRESOLVED':
        _no_route += 1
    else:
        _some_route += 1

with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('# Layout gaps in censused types that ALREADY have census accesses inside them.\n')
    fh.write('# The evidence exists and no field row was ever written. CANDIDATES, not recovered '
             'fields:\n')
    fh.write('# an access inside a gap may be an indexed read into an array declared elsewhere, so '
             'each\n')
    fh.write('# row must be read before a field is declared. displacement_count is the signal '
             'strength.\n')
    fh.write('#\n')
    fh.write('# THE DENOMINATOR, because the row count below will otherwise be read as the whole\n')
    fh.write('# problem. This instrument can only see types that HAVE an access census: %d of the\n'
             % len(_cen))
    fh.write('# store\'s %d types, %.1f %%. Those types hold %.1f %% of all field rows - they are the\n'
             % (len(store_types), _cov_t, _cov_f))
    fh.write('# big, heavily worked ones - but the remaining %d types produce NO candidates because\n'
             % (len(store_types) - len(_cen)))
    fh.write('# nothing has censused them, and their gaps are INVISIBLE HERE RATHER THAN ABSENT.\n')
    fh.write('# Emptying this file would not mean the layout work is done.\n')
    fh.write('#\n')
    fh.write('# AND THE BOTTLENECK IS NOT TOOLING. Measured 2026-09-13, over the %d uncensused types:\n'
             % (len(store_types) - len(_cen)))
    fh.write('#   %d have NO access route recorded at all - no instance, no chain, nothing saying\n'
             % _no_route)
    fh.write('#     how the record is reached. A census cannot be generated for any of them.\n')
    fh.write('#   %d record something, and they split three ways: reached through a POINTER CHAIN\n'
             % _some_route)
    fh.write('#     (record_field_scan.py), accessed at a STATIC address (gen_static_census.py),\n')
    fh.write('#     or reached through a STATIC POINTER such as *(void**)0x020927C0, which\n')
    fh.write('#     record_field_scan.py --root-global handles as of 2026-09-13.\n')
    fh.write('#   Exactly ONE uncensused type with 5+ fields cites a rip-relative access, so the\n')
    fh.write('#     static generator has no remaining work: BattleFormulaScratch was its population.\n')
    fh.write('# Establishing a route is research, not a script, and it is what stands between this\n')
    fh.write('# file and the rest of the store.\n')
    fh.write('#\n')
    fh.write('#\n')
    fh.write('# THE `disposition` COLUMN, AND WHY AN EMPTY REGISTRY WOULD STILL PROVE NOTHING.\n')
    fh.write('# A row is DISPOSITIONED only when EVERY displacement inside its gap has a verdict in\n')
    fh.write('# recoverable-layout-gaps-dispositions.tsv; one unruled displacement leaves it OPEN.\n')
    fh.write('# REFUSED means the evidence does not describe a field at that offset - the bytes are\n')
    fh.write('# STILL UNACCOUNTED FOR. Dispositioning a row removes a question from the queue, not a\n')
    fh.write('# gap from the layout.\n')
    fh.write('#   rows here: %d   OPEN (not yet read): %d   dispositioned: %d\n'
             % (len(out), _open, len(out) - _open))
    fh.write('#\n')
    fh.write('# Regenerate with gen_recoverable_gaps.py; do not hand-edit.\n')
    fh.write('type\tgap_start\tgap_end\tbytes\tdisplacement_count\tdisplacements_and_widths'
             '\tdisposition\n')
    for (n, tname, start, end, span, desc, _inside), verdict in zip(out, _verdicts):
        fh.write('%s\t0x%04X\t0x%04X\t%d\t%d\t%s\t%s\n'
                 % (tname, start, end, span, n, desc, verdict))

print('%d candidate gap(s) across %d censused type(s) - %.1f %% of the %d types in the store'
      % (len(out), len(_cen), _cov_t, len(store_types)))
for (n, tname, start, end, span, _d, _i), verdict in list(zip(out, _verdicts))[:8]:
    print('   %-28s 0x%04X..0x%04X  %3d bytes  %2d access(es)   %s'
          % (tname, start, end, span, n, verdict))
print('dispositions: %d of %d rows ruled on, %d OPEN (%d verdict(s) on file)'
      % (len(out) - _open, len(out), _open, len(_dispo)))
if tally:
    print('census intake: %s' % dict(tally))
