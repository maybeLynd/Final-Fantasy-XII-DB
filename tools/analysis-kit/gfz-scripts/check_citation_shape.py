#!/usr/bin/env python3
"""check_citation_shape.py - the 0.55-weight dimension, audited for the first time.

`engine_explained` counts a body as explained when SOME document cites an address inside it. That is
55% of the headline - more than every other dimension combined - and the measure has never been
examined for what it actually admits.

Two things it does not distinguish, and both are testable:

  1. WHO IS CITING. A citation from a STUB or a PARTIAL page counts exactly as much as one from a
     DOCUMENTED page. check_dispositions already reports 8,794 bodies cited by a DOCUMENTED page
     against engine_explained's ~10,715, so roughly 1,900 are carried by pages that do not claim to
     be finished.

  2. HOW MUCH. One address mentioned once in a table counts exactly as much as a body dissected
     across a whole section. A dimension that cannot tell those apart is measuring reach.

Neither is a defect on its own: a PARTIAL page can explain a function perfectly, and a short function
can be explained in one line. The point is that nothing has ever said how much of the 31% rests on
each shape, so nobody can tell whether the number is a floor or a ceiling.
"""
import bisect, collections, io, os, re, sys

sys.path.insert(0, 'Database/Tools/analysis-kit/gfz-scripts')
import progress as pr
import check_dispositions as CD

DB = 'Database/FFXII TZA'
sizes = CD.load_functions(None)
entries = sorted(sizes)

# body -> {status: citation count}, and how many distinct pages cite it
per_body = collections.defaultdict(collections.Counter)
pages_per_body = collections.defaultdict(set)
status_of = {}
for p in pr.docs(DB):
    t = io.open(p, encoding='utf-8', errors='replace').read()
    m = re.search(r"^status:\s*(\S+)", CD.frontmatter(t), re.M)
    st = m.group(1) if m else 'NONE'
    rel = os.path.relpath(p, DB)
    status_of[rel] = st
    for h in CD.CITE.findall(t):
        v = int(h, 16)
        i = bisect.bisect_right(entries, v) - 1
        if i < 0:
            continue
        e = entries[i]
        if e <= v < e + sizes[e]:
            per_body[e][st] += 1
            pages_per_body[e].add(rel)

cited = set(per_body)
print("bodies counted by engine_explained: %d   (progress.py publishes ~10,715)" % len(cited))
print()

print("--- 1. THE STRONGEST STATUS THAT CITES EACH BODY ---")
# AUDITED is STRONGER than DOCUMENTED and REOPENED weaker than PARTIAL; the first
# version of this list omitted both and fell through to alphabetical order, which put
# NONE above PARTIAL. Ranked explicitly now.
RANK = ['AUDITED', 'DOCUMENTED', 'CONTRACT', 'PARTIAL', 'REOPENED', 'STUB', 'NONE']
best = {}
for e, c in per_body.items():
    for s in RANK:
        if c.get(s):
            best[e] = s
            break
    else:
        best[e] = sorted(c)[0]
bs = collections.Counter(best.values())
for s, n in bs.most_common():
    print("    %-12s %6d  %5.1f%%" % (s, n, 100.0 * n / len(cited)))
# AUDITED is a STRONGER status than DOCUMENTED, not a weaker one. Counting it among the
# unfinished was the second half of the same rank bug.
FINISHED = {'AUDITED', 'DOCUMENTED'}
nondoc = sum(n for s, n in bs.items() if s not in FINISHED)
print("    -> %d bodies (%.1f%%) are carried ONLY by pages that do not claim to be finished"
      % (nondoc, 100.0 * nondoc / len(cited)))

print("\n--- 2. HOW MANY TIMES EACH BODY IS CITED, ANYWHERE ---")
tot = collections.Counter()
for e, c in per_body.items():
    n = sum(c.values())
    tot['1 citation' if n == 1 else
         '2' if n == 2 else
         '3-5' if n <= 5 else
         '6-20' if n <= 20 else '21+'] += 1
for k in ('1 citation', '2', '3-5', '6-20', '21+'):
    if tot[k]:
        print("    %-12s %6d  %5.1f%%" % (k, tot[k], 100.0 * tot[k] / len(cited)))

once = [e for e in cited if sum(per_body[e].values()) == 1]
print("\n--- 3. THE THINNEST SHAPE: cited exactly ONCE, by a non-DOCUMENTED page ---")
thin = [e for e in once if best[e] != 'DOCUMENTED']
print("    cited exactly once anywhere             : %6d  (%.1f%% of the dimension)"
      % (len(once), 100.0 * len(once) / len(cited)))
print("    of those, by a non-DOCUMENTED page only : %6d  (%.1f%%)"
      % (len(thin), 100.0 * len(thin) / len(cited)))
print("    their total bytes                       : %6d" % sum(sizes[e] for e in thin))
big = sorted(thin, key=lambda e: -sizes[e])[:6]
print("    the largest of them:")
for e in big:
    print("      %08X %6d B  cited once by %s"
          % (e, sizes[e], sorted(pages_per_body[e])[0][:58]))
