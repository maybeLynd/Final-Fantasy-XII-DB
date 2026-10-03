"""neighbour_precheck.py - FABLE, 2026-10-03: pass-22 neighbour pre-check of the STAGED host contract (no file written).

Builds the staged page in memory exactly as apply.py would (section.txt before "## 8. Script · resource · event
interactions"), then runs check_page_neighbours.hits() (OPUS's re-implementation of audit_crossrefs' per-document loop)
on HEAD and on the staged text, and prints every NEW unaccounted neighbour hit. A preview, not the gate.
"""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.abspath(os.path.join(DB, "..", ".."))
KIT = os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts")
sys.path.insert(0, KIT)
import check_page_neighbours as cpn  # noqa: E402
ac = cpn.ac

REL = "05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md"
ANCHOR = "## 8. Script · resource · event interactions"
head = subprocess.run(["git", "-C", REPO, "show", "HEAD:Database/FFXII TZA/" + REL], capture_output=True).stdout.decode(
    "utf-8").replace("\r\n", "\n")
block = io.open(os.path.join(HERE, "section.txt"), encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")
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
    print("  %-30s staged %4d  head %4d  %s" % (sub, len(w.get(sub, ())), len(h.get(sub, ())), "NEW %d" % len(new) if new else "same"))
    for a, d, o in new:
        print("      + %s %s %s" % (a, d, o))
print("NEW HITS %d" % new_total)
