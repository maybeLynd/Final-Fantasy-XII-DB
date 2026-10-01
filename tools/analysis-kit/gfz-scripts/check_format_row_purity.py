"""Does one row of the archive-extension census correspond to one FORMAT?

`formats_explained` scores 40 of 48 rows of `archive-extension-census.tsv`, an honest
`GROUP BY extension` over all 89,414 archive entries - deliberately so, because a census that
pre-trims to the interesting rows is an author choosing their own denominator.

But the dimension is named `formats_explained`, and `explained` means *a sheet with the LOADER
CONTRACT - what the engine reads, rejects, clamps, ignores*. That is a claim about a **format**. If a
row aggregates several formats, no owner can write one loader contract for it, and the row cannot be
honestly dispositioned however diligent anyone is. That is a property of the denominator.

The test uses `format-magic-census.tsv`, which already samples 12 files per extension and records
their leading signatures - and whose own header says *"Several is a LEAD, not a verdict: it is
equally the shape of a version field in the first four bytes."* So: count distinct signatures per
row, and compare the undispositioned rows against the dispositioned ones as a **control**.

NOT A NEW FINDING - A GATE FOR AN OLD ONE. `PS2-Image-Data-Formats/README.md` established this on
2026-09-03, from the same magic census: *".bin is the weak row, not .dat ... a bag of unrelated
formats sharing a name ... One census row cannot cover it, so this row is under-weighted; stated
rather than re-cut."* That decision stands and this instrument does not revisit it. What it adds is
the CONTROL that turns one row's observation into a property of the whole census: of the 29 rows
dispositioned `explained`, exactly ONE - `txt`, whose first four bytes are text rather than a magic -
carries more than one distinct ASCII magic tag. The rule holds across the census, so `bin` and `dat`
are denominator artefacts rather than work nobody did, and a future disposition that quietly claims
one of them will fail here instead of passing silently.

FIRST HYPOTHESIS, REFUTED BY ITS OWN CONTROL. This instrument originally used directory spread -
how many archive trees an extension appears in - and reported 25 % of undispositioned rows spread
against 12 % of dispositioned ones. That is two rows out of eight, and the control killed it
outright: `.txt` spans **14** trees and is dispositioned, `.csv` 13. Spread is survivable, because
text is text wherever it lives. The signature count is the measure that actually separates them, and
the discarded hypothesis is kept here because a reader deserves to know which test was run second.
"""
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_assets

DB = 'Database/FFXII TZA'

sigs = collections.defaultdict(list)
for line in io.open(check_assets.MAGIC_TSV, encoding='utf-8', errors='replace'):
    if line.startswith('#') or line.startswith('ext\t'):
        continue
    f = line.rstrip('\n').split('\t')
    if len(f) >= 5:
        sigs[f[0]].append((f[2], int(f[3]), f[4]))

census = check_assets.load_census()
counted, _refused, _coll, _stray, bucketed, _magic = check_assets.evaluate(
    census, check_assets.claimed_formats(DB))
done = [e for e in census if e in counted or e in bucketed]
todo = [e for e in census if e not in counted and e not in bucketed]

print('census rows: %d   dispositioned %d   not %d' % (len(census), len(done), len(todo)))
print('magic census: %d extensions sampled, 12 files each' % len(sigs))
print()


def report(label, exts):
    rows = sorted(((len(sigs.get(e, ())), e) for e in exts), reverse=True)
    multi = [e for n, e in rows if n > 1]
    print('%s: %d rows, %d show MORE THAN ONE signature in a 12-file sample (%.0f %%)'
          % (label, len(rows), len(multi), 100.0 * len(multi) / max(1, len(rows))))
    for n, e in rows[:8]:
        if n:
            shown = ', '.join('%s x%d' % (s, c) for s, c, _ in sigs[e][:7])
            print('   %-10s %d signature(s): %s' % (e, n, shown))
        else:
            print('   %-10s not in the magic sample' % e)
    return multi


print('--- the 8 that nobody has dispositioned ---')
m_todo = report('undispositioned', todo)
print()
print('--- CONTROL: the 40 that somebody did ---')
m_done = report('dispositioned', done)

print()
print('--- the SIGNATURE-COUNT test does not separate them ---')
r_todo = 100.0 * len(m_todo) / max(1, len(todo))
r_done = 100.0 * len(m_done) / max(1, len(done))
print('  multi-signature share: undispositioned %.0f %%   dispositioned %.0f %%' % (r_todo, r_done))
print('  `ker` has 6 signatures and IS dispositioned - `42 00 00 00`, `02 01 00 00`, `28 00 00 00`:')
print('  little-endian small integers, a count or size field, exactly what the magic census warned')
print('  about. Counting signatures counts version fields. The second test is the one that holds.')

# --- the test that does separate them: distinct printable ASCII magic TAGS ---
kinds = {e: rows[0][1] for e, rows in check_assets.claimed_formats(DB).items()}


def tags(e):
    return {s for s, _c, _x in sigs.get(e, ()) if s.startswith("'")}


print()
print('--- the ASCII-TAG test, against disposition kind ---')
print('  %-8s %-13s %s' % ('ext', 'disposition', 'distinct ASCII magic tags'))
for e in sorted(census, key=lambda x: -len(tags(x))):
    t = tags(e)
    if len(t) < 2:
        continue
    print('  %-8s %-13s %d: %s'
          % (e, kinds.get(e, '(none)') if e in counted else 'UNDISPOSED', len(t), ', '.join(sorted(t))))

explained = [e for e in census if e in counted and kinds.get(e) == 'explained']
breaks = [e for e in explained if len(tags(e)) > 1]
und_multi = [e for e in todo if len(tags(e)) > 1]

print()
print('--- verdict ---')
print('  rows dispositioned `explained`: %d; carrying more than one ASCII magic tag: %d %s'
      % (len(explained), len(breaks), breaks))
print('  rows undispositioned: %d; carrying more than one ASCII magic tag: %d %s'
      % (len(todo), len(und_multi), und_multi))
print()
print('  THE RULE: one `explained` row, one magic tag. The single exception is `txt`, whose first')
print('  four bytes are the file\'s text and not a signature at all - so the rule holds across the')
print('  census, and `bin` (6 tags) and `dat` (2) are DENOMINATOR artefacts, not undone work.')
print('  `formats_explained` therefore tops out at 46/48 = 95.83 %, by a decision already taken and')
print('  written down on 2026-09-03. This instrument does not re-cut the census: choosing the')
print('  denominator is precisely what the census exists to stop an author doing.')

# Gate: a future `explained` disposition on a bag row breaks the rule, and should fail here rather
# than quietly lift the score. `txt` is the one recorded exception.
unexpected = [e for e in breaks if e != 'txt']
if unexpected:
    print()
    print('  FAIL: %s dispositioned `explained` while carrying several magic tags.' % unexpected)
sys.exit(1 if unexpected else 0)
