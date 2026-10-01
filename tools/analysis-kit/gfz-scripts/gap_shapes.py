"""gap_shapes.py - the type gaps are not one thing, and the L2 verdict treats them as one.

PUBLISHED INTO THE KIT 2026-09-14 FROM `Tools/work/OPUS/`, WHICH `.gitignore` EXCLUDES.
`TYPE-COVERAGE.md` quotes this table and for a day no peer could reproduce it - the second
instrument found in that state the same day, after `final_audit_verdicts.py`. A canonical index
citing a gitignored tool is the index-consistency defect arriving through the tooling.

THE HEADLINE IN THE OLD DOCSTRING WAS ALSO A FROZEN NUMBER. It said "the 302 type gaps"; 302 was
true on 2026-09-14 morning and is 280 by that afternoon, because 65 fields were declared in
between. A tool that names its own measurement in its title goes stale the first time it works.

RECONSTRUCTION-READINESS-GATE rates "reconstruction-grade types" PARTIAL, and the number behind
that is `types_index.py`'s 302 gaps against 247 types / 1,906 fields. A gap is NOT an error - the
same run reports 0 errors - it is declared-field coverage falling short of the declared extent.

But "gap" covers at least four different situations, and they are worth different amounts:

  PAD-1..7      an interior gap of 1-7 bytes before a field whose alignment explains it. This is
                the compiler, not missing knowledge, and closing it would mean declaring padding
                as if it were a field.
  INTERIOR      an interior gap of 8+ bytes: genuinely unmapped fields inside a struct whose
                surrounding offsets ARE established. Real type frontier, and the cheapest to close
                because both edges are known.
  TAIL          undeclared bytes after the last declared field. The struct's SIZE is established
                and its contents are not - a different claim from an interior hole.
  OUTSIZED      a gap larger than the entire declared part of its type. That is not a hole in a
                model; it is a signal the model may be wrong - two structures conflated, or a
                pointer-to-array read as an inline array.

Counting all four as one number makes a type with seven alignment pads look worse than a type with
one 2,130-byte hole in the middle of it.
"""
import collections
import os
import re
import subprocess
import sys

# Resolved from __file__, not cwd: this now lives IN the kit, and a relative path would only
# work from the repo root. The kit learned that the hard way on 2026-09-14 (check_index_figures).
KIT = os.path.dirname(os.path.abspath(__file__))

r = subprocess.run([sys.executable, os.path.join(KIT, "types_index.py")],
                   capture_output=True, text=True)
lines = (r.stdout + r.stderr).split("\n")

GAP = re.compile(r"^gap\s+(\S+):\s+undeclared\s+(tail|gap)\s+0x([0-9A-Fa-f]+)\.\.0x([0-9A-Fa-f]+)"
                 r"\s+\((\d+) bytes\)(?:\s+before\s+(\S+))?")

# declared extent per type: the highest end offset we see mentioned for it
rows = []
for line in lines:
    m = GAP.match(line.strip())
    if m:
        t, kind, lo, hi, n, before = m.groups()
        rows.append((t, kind, int(lo, 16), int(hi, 16), int(n), before or ""))

print("gap records parsed: %d" % len(rows))
if not rows:
    print("none parsed - has types_index's gap line changed shape?")
    raise SystemExit(2)

# the declared span of each type, approximated by the largest offset it mentions
span = collections.defaultdict(int)
for t, kind, lo, hi, n, before in rows:
    span[t] = max(span[t], hi)

buckets = collections.Counter()
outsized = []
by_type = collections.Counter()
for t, kind, lo, hi, n, before in rows:
    if kind == "tail":
        b = "TAIL"
    elif n >= max(8, span[t] // 2) and n > 64:
        b = "OUTSIZED"
    elif n <= 7:
        b = "PAD-1..7"
    else:
        b = "INTERIOR"
    if b == "OUTSIZED":
        outsized.append((t, lo, hi, n, before))
    buckets[b] += 1
    by_type[(t, b)] += 1

print("\nGAP SHAPES")
for b, c in buckets.most_common():
    print("  %-10s %4d   %5.1f%%" % (b, c, 100.0 * c / len(rows)))

print("\nOUTSIZED - a gap bigger than half the type's declared span, and over 64 bytes.")
print("These are modelling questions, not missing fields:")
for t, lo, hi, n, before in sorted(outsized, key=lambda x: -x[3])[:12]:
    print("  %-34s 0x%03X..0x%03X  %6d bytes  before %s" % (t[:34], lo, hi, n, before or "(tail)"))

print("\nINTERIOR gaps by type - both edges known, cheapest real frontier:")
inter = [(t, c) for (t, b), c in by_type.items() if b == "INTERIOR"]
for t, c in sorted(inter, key=lambda x: -x[1])[:10]:
    print("  %-40s %d" % (t[:40], c))
