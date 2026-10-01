"""Fields declared as scalars that the image indexes as ARRAY ELEMENTS.

`CharacterRenderRecord +0x4C4` was declared `uint16` with no meaning until 2026-09-13. Its readers
index it `[base + i*8 + 0x4C4]`, so it is element 0 of an array whose entries are eight bytes apart -
0x4C4, 0x4CC, 0x4D4 - each of which the store carries as its own separate `uint16` row. An array had
been flattened into per-offset scalars, and nothing in the kit could see it.

THE TEST. Scan every census for a memory operand of the form `[base + index*SCALE + disp]`, which is
an indexed access, and report the displacements where one appears against a field the store declares
as a plain scalar. The SCALE is the array's element stride; when it differs from the declared field's
size, the field is one member of a strided entry rather than the whole entry.

TWO EXCLUSIONS, both learned from this file's own first output. A `lea` computes an address and
accesses nothing - 43 of the 393 indexed operands are leas - and an indexed operand with NO
displacement lands at offset 0, so it is attributed to whatever field starts the type. Together they
produced four false findings, including `BattleUnit.unitFlags`, a named uint64 "indexed at stride 4"
by three leas that have nothing to do with it. 341 real indexed accesses remain.

WHAT A ROW MEANS, AND WHAT IT DOES NOT. A hit says the image computes this address with an index
register. It does NOT say how long the array is - no censused reader here bounds one - and it does not
say the neighbouring rows are its elements, only that they lie where its elements would. Both are
judgements for whoever reads the row; this reports the indexing and stops.

The control is printed first and is the population that makes the report readable: how many indexed
accesses were found at all. If that is zero the pattern is not being matched and every empty finding
below it is a property of this regex.
"""
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_census_widths as ccw
import insn_class

DB = 'Database/FFXII TZA'
FIELDS = os.path.join(DB, '_types', 'fields.tsv')

# [base + index*scale + disp]  - capstone renders the scale as `*N`
INDEXED = re.compile(r'\[\s*[a-z0-9]+\s*\+\s*[a-z0-9]+\s*\*\s*(\d+)\s*(?:\+\s*(0x[0-9a-f]+|\d+))?\s*\]')


def declared():
    per = collections.defaultdict(dict)
    for n, line in enumerate(io.open(FIELDS, encoding='utf-8')):
        if n == 0 or not line.strip():
            continue
        c = line.rstrip('\n').split('\t')
        if len(c) < 6:
            continue
        try:
            per[c[0]][int(c[1], 16)] = (int(c[2]), c[3], c[4])
        except ValueError:
            continue
    return per


decl = declared()
total_indexed = 0
skipped_lea = 0
skipped_nodisp = 0
hits = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))

for tname, fname, sbase, shift, extent in ccw.censused_types():
    path = None
    for root, _d, files in os.walk(DB):
        if fname in files:
            path = os.path.join(root, fname)
            break
    if path is None or tname not in decl:
        continue
    for n, line in enumerate(io.open(path, encoding='utf-8', errors='replace')):
        if n == 0 or not line.strip():
            continue
        c = line.rstrip('\n').split('\t')
        if len(c) < 6:
            continue
        m = INDEXED.search(c[5])
        if not m:
            continue
        # A `lea` COMPUTES an address and accesses nothing, so an indexed lea says where a pointer
        # was built, never that this field is an array element. 43 of the 393 indexed operands are
        # leas. And an indexed operand with NO displacement lands at offset 0, so it is attributed
        # to whatever field starts the type - which is how `BattleUnit.unitFlags`, a named uint64,
        # came to be reported as indexed at stride 4 by three `lea rdx, [rdi + rdx*4]` that have
        # nothing to do with it.
        #
        # This is the SAME mistake the float gate made three times before it was fixed there: a
        # move or an address computation treated as evidence about a type. Fixed in one instrument
        # and reproduced in the next one I wrote, which is why it is written out here rather than
        # silently filtered.
        if insn_class.is_address_only(c[5]):
            skipped_lea += 1
            continue
        if m.group(2) is None:
            skipped_nodisp += 1
            continue
        total_indexed += 1
        try:
            off = int(c[3], 16)
        except ValueError:
            continue
        # Both bounds, through the one implementation: a sub-object access is the parent's
        # displacement minus the shift AND inside the sub-object's own extent. The upper bound
        # was missing here until 2026-09-13.
        if shift:
            off = ccw.rebase(off, shift, extent)
            if off is None:
                continue
        hits[tname][off][int(m.group(1))] += 1

print('--- control: indexed MEMORY ACCESSES across all censuses: %d ---' % total_indexed)
print('    excluded: %d lea address computations, %d indexed operands with no displacement'
      % (skipped_lea, skipped_nodisp))
if not total_indexed:
    print('  CONTROL FAILED: the indexed-operand pattern matched nothing. Everything below is void.')
    sys.exit(2)

print()
rows = []
for tname, offs in hits.items():
    for off, scales in offs.items():
        d = decl[tname].get(off)
        if not d:
            continue
        size, name, ctype = d
        # The expected stride is the ELEMENT size, not the field size. A field declared `uint16[9]`
        # occupies 18 bytes and is indexed at stride 2, and the first version of this check reported
        # all nine of those as findings - twenty of its thirty-three rows were declared arrays being
        # indexed exactly as declared. Comparing a stride against a total size is a category error,
        # and it is the same one this session found in a gap count and a format census: the number
        # was right and the population it was compared against was not.
        m_elems = re.search(r'\[(\d+)\]\s*$', ctype)
        elems = int(m_elems.group(1)) if m_elems else 1
        expected = size // elems if elems and size % elems == 0 else size
        for scale, count in scales.items():
            if scale == expected:
                continue          # indexed exactly as declared
            rows.append((count, tname, off, size, name, ctype, scale, expected))
rows.sort(reverse=True)

PRIM = ('uint', 'int', 'float', 'double', 'byte', 'char', 'bool', 'void', 'u8', 'u16', 'u32', 'u64')


def primitive(ctype):
    base = ctype.split('[')[0].strip().lower()
    return base.startswith(PRIM) or base == 'unresolved'


# A field whose ctype is another TYPE is a nested structure, and an index inside it belongs to that
# structure's own interior rather than to this row. Reporting those as flattened arrays would be
# blaming the container for its contents, so they are separated instead of dropped - a reader may
# still want to know an inner array exists.
flat = [r for r in rows if primitive(r[5])]
nested = [r for r in rows if not primitive(r[5])]

# THE ADJUDICATION IS IN THE ROW. Every one of these eight is already explained in its own
# `meaning` cell - "Element 0 of a STRIDE-4 ARRAY of per-slot summary entries", "element 0 of a
# STRIDE-8 ARRAY of presentation channels" - and this checker read none of it, so the same eight
# were re-derived on every run. That is the FIFTH instrument found this session reporting findings
# the corpus had already decided; the checkers all predate the adjudications and none of them reads
# the data back. Split, so a NEW stride finding is visible instead of buried. 2026-09-14, OPUS.
STRIDE_NOTED = re.compile(r'stride[- ]?\d|STRIDE-\d|\bindexed\b|element \d+ of|member \d+ of',
                          re.I)
_mean = {}
for _n, _line in enumerate(io.open(FIELDS, encoding='utf-8')):
    if _n == 0 or not _line.strip():
        continue
    _c = _line.rstrip("\n").split("\t")
    if len(_c) > 5:
        try:
            _mean[(_c[0], int(_c[1], 16))] = _c[5]
        except ValueError:
            pass
_adj = [r for r in flat if STRIDE_NOTED.search(_mean.get((r[1], r[2]), ''))]
_new = [r for r in flat if r not in _adj]

print('--- declared SCALARS indexed at a stride that is not their size: %d ---' % len(flat))
if _new:
    print('  NOT YET EXPLAINED IN THE ROW - these are the ones to read:')
    for count, tname, off, size, name, ctype, scale, expected in _new:
        print('    %-24s 0x%03X  %-20s %-11s %d B  ->  stride %d, %d site(s)'
              % (tname[:24], off, name[:20], ctype[:11], size, scale, count))
if _adj:
    print("  ALREADY EXPLAINED as an array element in the field's own meaning cell: %d"
          % len(_adj))
    for count, tname, off, size, name, ctype, scale, expected in _adj:
        print('    %-24s 0x%03X  %-20s %-11s %d B  ->  stride %d, %d site(s)  | %s'
              % (tname[:24], off, name[:20], ctype[:11], size, scale, count,
                 _mean.get((tname, off), '')[:58]))

print()
print('--- nested TYPE fields whose interior is indexed: %d - expected, not defects ---' % len(nested))
for count, tname, off, size, name, ctype, scale, expected in nested:
    print('  %-26s 0x%03X  %-22s %-11s element %d B  ->  inner stride %d, %d site(s)'
          % (tname[:26], off, name[:22], ctype[:11], expected, scale, count))

print()
print('  A hit means the image computes the address with an index register at that stride. It does')
print('  NOT establish the array length, and it does not establish that the neighbouring declared')
print('  rows are its elements - only that they lie where its elements would. Both are judgements.')

# THE SPLIT WAS COMPUTED AND THEN THROWN AWAY AT THE EXIT. `sys.exit(1 if rows else 0)` keyed on
# the RAW hits, so the eight rows this file had just classified as ALREADY EXPLAINED still failed
# the gate, and the nested three - printed under a heading that calls them "expected, not defects"
# - failed it too. This is FINAL-AUDIT pass 15's instrument, so that was a pass the terminal gate
# would fail today with a defect count of zero. Half an instrument fix is worth nothing if the
# verdict still comes from the unclassified number. 2026-09-14, OPUS.
#
# CONTROL, every run: blank the stride note on one adjudicated row and confirm it moves to _new.
# A suppression that is not keyed to the note would keep the row suppressed, and then every clean
# exit this gate prints would be unearned.
if _adj:
    _probe = dict(_mean)
    _k = (_adj[0][1], _adj[0][2])
    _probe[_k] = ''
    _still = [r for r in flat if STRIDE_NOTED.search(_probe.get((r[1], r[2]), ''))]
    if len(_still) >= len(_adj):
        print('\n  CONTROL FAILED: clearing a meaning cell did not move its row back to the')
        print('  unexplained list, so the suppression is not keyed to the row. This exit is unproven.')
        sys.exit(2)
    print('\n  control passed: clearing one meaning cell returns its row to the unexplained list.')

if _new:
    print('\n  PASS 15 FAILS: %d indexed scalar(s) with no explanation in their own row.' % len(_new))
    sys.exit(1)
print('\n  %d indexed scalar(s), every one explained in its own `meaning` cell, and %d nested'
      % (len(_adj), len(nested)))
print('  interior(s), which the heading above calls expected. Exiting 0 because nothing is')
print('  UNEXPLAINED - not because nothing was found. A new stride with a silent row fails again.')
sys.exit(0)
