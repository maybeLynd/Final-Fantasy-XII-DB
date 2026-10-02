"""check_page_neighbours.py PAGE... [--vs-stripped] - pass-22 UNACCOUNTED NEIGHBOUR hits of one page, working tree vs HEAD, in seconds
(OPUS, 2026-10-02). PAGE is relative to "FFXII TZA/".

Re-implements audit_crossrefs.py's per-document loop (same functions.tsv, edges.tsv, aliases, substrate and hub
rules, crossing-section accounting, R6 far ends and registry dispositions) for the pages named, so a publisher can see
which NEW hits an edit adds before paying for check_publish_neighbours.py's two worktree audits (about 9 minutes).
--vs-stripped compares against the same page with its OPUS interior-citation sections cut (from the
first such heading to the end), to measure what published sections added. It is a preview, not the gate: run check_publish_neighbours.py on the batch before publishing.

Prints, per page and subsystem: the working-tree hit count, the HEAD hit count and every hit that is new (subject
address, direction, far end). Exit 1 when any page has a new hit.
"""
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DBROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DOCS = os.path.join(DBROOT, "FFXII TZA")
KIT = HERE
GRAPH = os.path.join(DBROOT, "Tools", "work", "graph")
sys.path.insert(0, KIT)
import audit_crossrefs as ac  # noqa: E402


def hits(text, rel, fn, callers, callees, dispositioned):
    folder_low = rel.lower()
    xlow = "".join(m.group(0) for m in ac.CROSSING_SECTION.finditer(ac.body_text(text))).lower()
    cited = sorted(ac.cited_addresses(text))
    doc_lines = text.split("\n")
    upper = [ln.upper() for ln in doc_lines]
    control_only = {c for c in cited
                    if [i for i, ln in enumerate(upper) if c in ln]
                    and all(re.search(r"\bcontrol\b", doc_lines[i], re.I)
                            for i, ln in enumerate(upper) if c in ln)}
    cited = [c for c in cited if c not in control_only]
    far_ends = set()
    spans = [m.span() for m in ac.CROSSING_SECTION.finditer(text)]
    if spans:
        outside = text
        for lo, hi in reversed(spans):
            outside = outside[:lo] + outside[hi:]
        oc = ac.cited_addresses(outside)
        for c in cited:
            if c in oc:
                continue
            near = {x.upper() for x in callers.get(c, ())} | {x.upper() for x in callees.get(c, ())}
            if near & oc:
                far_ends.add(c)
    seen = {}
    for addr in cited:
        if addr not in fn or addr in far_ends:
            continue
        if ac.is_substrate(fn.get(addr)) or len(callers.get(addr, ())) > ac.HUB_FANIN:
            continue
        for direction, table in (("caller", callers), ("callee", callees)):
            for other in table.get(addr, ()):
                if ac.is_substrate(fn.get(other)):
                    continue
                sub = ac.subsystem_of(fn.get(other))
                if not sub or sub in ac.SUBSTRATE or ac.doc_accounts_for(xlow, folder_low, sub):
                    continue
                seen.setdefault(sub, set()).add((addr, direction, other))
    return {s: h for s, h in seen.items() if (rel, s) not in dispositioned}


def main():
    pages = [a for a in sys.argv[1:] if not a.startswith("--")]
    fn = ac.load_functions(os.path.join(GRAPH, "functions.tsv"))
    ac.register_ledger_aliases({v["owner"] for v in fn.values()})
    ac.register_domain_aliases({d.split(".")[0] for v in fn.values() for d in v["domains"]})
    callers, callees = ac.load_edges(os.path.join(GRAPH, "edges.tsv"))
    dispositioned, _u = ac.load_dispositions(DOCS)
    bad = 0
    for rel in pages:
        work = io.open(os.path.join(DOCS, *rel.split("/")), encoding="utf-8").read()
        if "--vs-stripped" in sys.argv:  # baseline = this page without its OPUS interior-citation sections
            i = work.find("## Interior citations for the entry-cited functions (OPUS")
            head = work[:i] if i > 0 else work
        else:
            head = subprocess.run(["git", "-C", DBROOT, "show", "HEAD:Database/FFXII TZA/" + rel], capture_output=True,
                                  text=True, encoding="utf-8", errors="replace").stdout
        w = hits(work, rel, fn, callers, callees, dispositioned)
        h = hits(head, rel, fn, callers, callees, dispositioned) if head else {}
        print("==", rel)
        for sub in sorted(set(w) | set(h)):
            new = sorted(w.get(sub, set()) - h.get(sub, set()))
            if new or sub not in h:
                bad += 1 if new else 0
            tag = "NEW" if new else "same"
            print("  %-28s work %4d  head %4d  %s" % (sub, len(w.get(sub, ())), len(h.get(sub, ())), tag))
            for a, d, o in new[:12]:
                print("      + %s %s %s" % (a, d, o))
            if len(new) > 12:
                print("      + ... %d more" % (len(new) - 12))
    print("PAGES WITH NEW HITS" if bad else "NO NEW HITS", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
