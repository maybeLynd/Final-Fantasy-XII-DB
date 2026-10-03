"""nprecheck.py PKGDIR REL ANCHOR - pass-22 neighbour pre-check of a staged host contract (generic form of
fable-l2exp-s16-mech-1003/neighbour_precheck.py). Inserts PKGDIR/section.txt before the line ANCHOR in the HEAD blob
of REL and prints every NEW unaccounted neighbour hit. Writes nothing."""
import io
import os
import subprocess
import sys

PKG, REL, ANCHOR = sys.argv[1], sys.argv[2], sys.argv[3]
DB = os.path.abspath(os.path.join(PKG, "..", "..", ".."))
REPO = os.path.abspath(os.path.join(DB, "..", ".."))
KIT = os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts")
sys.path.insert(0, KIT)
import check_page_neighbours as cpn  # noqa: E402
ac = cpn.ac

head = subprocess.run(["git", "-C", REPO, "show", "HEAD:Database/FFXII TZA/" + REL], capture_output=True).stdout.decode(
    "utf-8").replace("\r\n", "\n")
block = io.open(os.path.join(PKG, "section.txt"), encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")
i = head.index("\n" + ANCHOR + "\n") + 1
staged = head[:i].rstrip("\n") + "\n\n" + block + "\n\n" + head[i:]

fn = ac.load_functions(os.path.join(cpn.GRAPH, "functions.tsv"))
ac.register_ledger_aliases({v["owner"] for v in fn.values()})
ac.register_domain_aliases({d.split(".")[0] for v in fn.values() for d in v["domains"]})
callers, callees = ac.load_edges(os.path.join(cpn.GRAPH, "edges.tsv"))
dispositioned, _u = ac.load_dispositions(cpn.DOCS)
w = cpn.hits(staged, REL, fn, callers, callees, dispositioned)
h = cpn.hits(head, REL, fn, callers, callees, dispositioned)
new_total = 0
print("== %s (staged vs HEAD)" % REL)
for sub in sorted(set(w) | set(h)):
    new = sorted(w.get(sub, set()) - h.get(sub, set()))
    new_total += len(new)
    print("  %-30s staged %4d  head %4d  %s" % (sub, len(w.get(sub, ())), len(h.get(sub, ())),
                                                 "NEW %d" % len(new) if new else "same"))
    for a, d, o in new:
        print("      + %s %s %s" % (a, d, o))
print("NEW HITS %d" % new_total)
