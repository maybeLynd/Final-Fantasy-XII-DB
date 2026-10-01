"""Which undescribed field rows can actually be described, and which can only be measured.

WHY THIS IS A KEPT INSTRUMENT AND NOT A COMMAND. `_types/README.md` publishes "832 empty meanings,
215 actionable, 60 informative, 128 measurable". Those numbers came from an ad-hoc script that was
not kept - the identical defect retracted in EVIDENCE-STANDARD 2026-09-13k, where a published
three-way split turned out to reproduce under no population at all. A figure in a README that nobody
can re-derive is a claim with no instrument behind it, and this session has now found two.

So this measures the same thing with its population stated, and it is the file the README should
cite. If its numbers differ from the published ones, the published ones move.

THE SPLIT, AND WHY EACH BOUNDARY IS WHERE IT IS

  EMPTY MEANING          the `meaning` column is blank. An offset, a size and a type say where a
                         field is and how wide; they do not say what it is.
  PHYRE / ENGINE         reflection-imported types give names and offsets and never prose, so their
                         empty meanings are expected and are NOT a gap. Counted separately rather
                         than excluded, because a number that quietly drops two thirds of its
                         population is how the last three miscounts happened.
  IN A CENSUSED TYPE     the evidence exists on disk. Everything else needs research first, which is
                         a different kind of work and a different queue.
  INFORMATIVE            at least one access is arithmetic, a bit operation, a float operation or a
                         plausible float constant - the classes that say what a value IS, per
                         insn_class. These rows can be DESCRIBED from evidence already collected.
  MEASURABLE ONLY        every access is a move or an address computation. Those give a width and
                         nothing else, so the row can be given a size and a citation and not a
                         meaning. Calling these describable would repeat, in miniature, the error
                         the README entry is about.
"""
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_census_widths as ccw
import insn_class

DB = 'Database/FFXII TZA'
FIELDS = os.path.join(DB, '_types', 'fields.tsv')
TYPES = os.path.join(DB, '_types', 'types.tsv')

# A type whose rows come from engine reflection rather than from reading code. Matched on the
# category column, not on the name, because a name test would be a guess about spelling.
PHYRE_MARKS = ('Phyre', 'phyre', 'PRendering', 'sce::', 'UCD3D11', 'D3D')


def phyre_types():
    out = set()
    if not os.path.exists(TYPES):
        return out
    for n, line in enumerate(io.open(TYPES, encoding='utf-8')):
        if not n or not line.strip():
            continue
        c = line.rstrip('\n').split('\t')
        if len(c) > 2 and any(m in c[2] for m in PHYRE_MARKS):
            out.add(c[0])
        elif any(m in c[0] for m in PHYRE_MARKS):
            out.add(c[0])
    return out


def census_kinds():
    """(type, offset) -> Counter of instruction classes, over every census."""
    per = collections.defaultdict(collections.Counter)
    for tname, fname, sbase, shift, extent in ccw.censused_types():
        path = None
        for root, _d, files in os.walk(DB):
            if fname in files:
                path = os.path.join(root, fname)
                break
        if path is None:
            continue
        for n, line in enumerate(io.open(path, encoding='utf-8', errors='replace')):
            if n == 0 or not line.strip():
                continue
            c = line.rstrip('\n').split('\t')
            if len(c) < 6:
                continue
            try:
                off = int(c[3], 16)
            except ValueError:
                continue
            if shift:
                off = ccw.rebase(off, shift, extent)
                if off is None:
                    continue
            per[(tname, off)][insn_class.classify(c[5])] += 1
    return per


INFORMATIVE = ('float', 'int', 'const')

# A MEANING THAT IS ONLY A RATIONALE IS NOT A MEANING, and this guard exists because I broke it.
# On 2026-09-13 a batch of type dispositions - "retyped to float because every access is
# float-class", "held, not retyped" - was appended to the `meaning` column of 28 rows. None of those
# rows says what its field IS; they say why a declared type was or was not changed. This check
# counted them as described and reported the queue falling from 44 to 28 when the honest figure was
# 37. A number that counts edits instead of understanding is the inflation the standing rules forbid,
# so the rationale now lives in the evidence column and this guard reports any that come back.
RATIONALE_ONLY = (
    'retyped from an integral declaration',
    'held, not retyped',
    'the float finding does not survive',
    'the float finding is not supported',
    'type disposition:',
    'width from the instruction, never from the next offset',
)


def rationale_only(meaning):
    """True when the meaning column holds a type/width rationale and nothing about the field."""
    m = meaning.strip().lower()
    return bool(m) and any(m.startswith(k) for k in RATIONALE_ONLY)


def main():
    phyre = phyre_types()
    kinds = census_kinds()
    censused = {t for t, _f, _b, _s, _e in ccw.censused_types()}

    total = empty = rationale = 0
    empty_phyre = empty_game = 0
    in_censused = informative = measurable = no_access = 0
    rows = []
    for n, line in enumerate(io.open(FIELDS, encoding='utf-8')):
        if not n or not line.strip():
            continue
        c = line.rstrip('\n').split('\t')
        if len(c) < 6:
            continue
        total += 1
        if c[5].strip() and not rationale_only(c[5]):
            continue
        if c[5].strip():
            rationale += 1          # counted as UNDESCRIBED, and reported so it stays visible
        empty += 1
        if c[0] in phyre:
            empty_phyre += 1
            continue
        empty_game += 1
        if c[0] not in censused:
            continue
        in_censused += 1
        try:
            off = int(c[1], 16)
        except ValueError:
            continue
        k = kinds.get((c[0], off))
        if not k:
            no_access += 1
            continue
        if any(k[x] for x in INFORMATIVE):
            informative += 1
            rows.append((sum(k[x] for x in INFORMATIVE), c[0], off, c[3], c[4], dict(k)))
        else:
            measurable += 1

    print('--- control: field rows read: %d, of which empty meaning: %d ---' % (total, empty))
    if not total:
        print('  CONTROL FAILED: no rows parsed.')
        return 2
    print('    of those, holding only a TYPE RATIONALE rather than a description: %d' % rationale)
    print('    Phyre / engine-imported (expected, NOT a gap): %d' % empty_phyre)
    print('    GAME types                                   : %d' % empty_game)
    print()
    print('--- of the %d game rows with no meaning ---' % empty_game)
    print('  in a CENSUSED type, so the evidence is already on disk : %d' % in_censused)
    print('    of those, with NO access at that displacement        : %d' % no_access)
    print('    INFORMATIVE - arithmetic, bits, float or a float const: %d   <- describable now'
          % informative)
    print('    MEASURABLE ONLY - moves and address computations      : %d   <- a width, not a meaning'
          % measurable)
    print('  needing research before any of this                    : %d' % (empty_game - in_censused))
    print()
    print('  README currently publishes 215 actionable / 188 with accesses / 60 informative /')
    print('  128 measurable. Where this disagrees, this instrument is the one that can be re-run.')
    print()
    rows.sort(reverse=True)
    print('--- the describable queue, richest evidence first (top 30 of %d) ---' % len(rows))
    for cnt, tname, off, name, ctype, k in rows[:30]:
        print('  %-26s 0x%04X  %-22s %-12s %d informative   %s'
              % (tname[:26], off, name[:22], ctype[:12], cnt,
                 ' '.join('%s=%d' % (a, b) for a, b in sorted(k.items()))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
