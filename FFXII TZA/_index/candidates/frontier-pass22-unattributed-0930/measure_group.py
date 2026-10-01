"""measure_group.py <creator-regex> - pass-22 findings at HEAD (audit enumeration, HEAD registry, R6 tripwire-only pairs
excluded) for the pages pass22-debt.tsv attributes to the matching creating lane."""
import io, re, sys
import os
REC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REC)
import pass22_neighbour_bullets as cb

pat = re.compile(sys.argv[1])
pages = sorted({l.split("\t")[0] for l in cb.head("_index/candidates/pass22-debt-0929/pass22-debt.tsv").splitlines()
                if not l.startswith("#") and l.count("\t") >= 3 and pat.search(l.rstrip().split("\t")[3])})
fn, callers, callees, disp = cb.setup()
tot = 0
for rel in pages:
    t = cb.head(rel)
    if not t:
        print("GONE", rel)
        continue
    cb.TRIPWIRE_PAIRS.clear()
    h = cb.page_hits(rel, t, fn, callers, callees, disp)
    f = {s: v for s, v in h.items() if (rel, s) not in cb.TRIPWIRE_PAIRS}
    tot += len(f)
    print("%3d %s %s" % (len(f), rel, sorted(f)))
print("GROUP PAIRS AT HEAD", tot, "on", len(pages), "pages")
