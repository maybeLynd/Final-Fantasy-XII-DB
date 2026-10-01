#!/usr/bin/env python3
"""Rebuild the FULL edge list of pass-22 UNACCOUNTED NEIGHBOUR pairs by reusing audit_crossrefs.py.

Reuses the shipped instrument's own functions (load_functions, register_*_aliases, load_edges,
cited_addresses, body_text, CROSSING_SECTION, is_substrate, subsystem_of, doc_accounts_for,
HUB_FANIN). The per-document loop of check 4 is reproduced from main() line for line, because
main() only prints four sample edges per pair.

Never writes into any docs tree. Reads the export at C:/x/p22/Database/FFXII TZA by default.

usage:
  rebuild_edges.py [--docs DIR] [--pairs fable_pairs.json] [--out edges_full.json]
  rebuild_edges.py --simulate DRAFTDIR     # append each <basename>.crossing.md draft to its page
                                           # (inserted as the page's text would be) and re-run
"""
import argparse
import io
import json
import os
import re
import sys

KIT = r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts"
GRAPH = r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/graph"
sys.path.insert(0, KIT)
import audit_crossrefs as ac  # noqa: E402

# The exact path audit_crossrefs compares against for the UC-1 band (realpath of
# <kit>/../../work/graph/functions.tsv) - so the band applies as it did in the r.json run.
FUNCS = os.path.join(KIT, "..", "..", "work", "graph", "functions.tsv")
EDGES = os.path.join(GRAPH, "edges.tsv")


def setup():
    fn = ac.load_functions(FUNCS)
    ac.register_ledger_aliases({v["owner"] for v in fn.values()})
    ac.register_domain_aliases({d.split(".")[0] for v in fn.values() for d in v["domains"]})
    callers, callees = ac.load_edges(EDGES)
    return fn, callers, callees


def neighbours(rel, text, fn, callers, callees):
    """check 4 of audit_crossrefs.main for one document -> (seen, trip), each {sub: [(addr,dir,other)]}"""
    folder_low = rel.lower()
    xlow = "".join(m.group(0) for m in ac.CROSSING_SECTION.finditer(ac.body_text(text))).lower()
    cited = sorted(ac.cited_addresses(text))
    if not cited:
        return {}, {}, []
    control_only = set()
    doc_lines = text.split("\n")
    lines_upper = [ln.upper() for ln in doc_lines]
    for c in cited:
        idxs = [i for i, ln in enumerate(lines_upper) if c in ln]
        if idxs and all(re.search(r"\bcontrol\b", doc_lines[i], re.I) for i in idxs):
            control_only.add(c)
    cited = [c for c in cited if c not in control_only]
    far_ends = set()
    sec_spans = [m.span() for m in ac.CROSSING_SECTION.finditer(text)]
    if sec_spans:
        outside = text
        for lo, hi in reversed(sec_spans):
            outside = outside[:lo] + outside[hi:]
        outside_cited = ac.cited_addresses(outside)
        for c in cited:
            if c in outside_cited:
                continue
            near = {x.upper() for x in callers.get(c, ())} | {x.upper() for x in callees.get(c, ())}
            if near & outside_cited:
                far_ends.add(c)
    seen, trip = {}, {}
    for addr in cited:
        if addr not in fn:
            continue
        held = addr in far_ends
        if ac.is_substrate(fn.get(addr)):
            continue
        if len(callers.get(addr, ())) > ac.HUB_FANIN:
            continue
        for direction, table in (("caller", callers), ("callee", callees)):
            for other in table.get(addr, ()):
                if ac.is_substrate(fn.get(other)):
                    continue
                sub = ac.subsystem_of(fn.get(other))
                if not sub or sub in ac.SUBSTRATE:
                    continue
                if not ac.doc_accounts_for(xlow, folder_low, sub):
                    (trip if held else seen).setdefault(sub, []).append((addr, direction, other))
    for d in (trip, seen):
        for s in d:
            d[s].sort()
    return seen, trip, sorted(far_ends)


def detail(hits):
    sample = hits[:4]
    d = "; ".join("%s %s %s" % h for h in sample)
    if len(hits) > len(sample):
        d += " (+%d more)" % (len(hits) - len(sample))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default=r"C:/x/p22/Database/FFXII TZA")
    ap.add_argument("--pairs", default=r"C:/x/p22/fable_pairs.json")
    ap.add_argument("--out", default=r"C:/x/p22/drafts/tools/edges_full.json")
    ap.add_argument("--simulate", help="draft dir: insert drafts, then report findings per page")
    a = ap.parse_args()

    pairs = json.load(io.open(a.pairs, encoding="utf-8"))
    fn, callers, callees = setup()
    docs = sorted({p[1] for p in pairs})
    want = {(p[1], p[2]): p[3] for p in pairs}

    if a.simulate:
        import simulate  # sibling module: how a draft is inserted into its page
        total_new = 0
        for rel in docs:
            text = io.open(os.path.join(a.docs, rel), encoding="utf-8").read()
            before, _, _ = neighbours(rel, text, fn, callers, callees)
            new_text = simulate.insert(rel, text, a.simulate)
            after, trip, far = neighbours(rel, new_text, fn, callers, callees)
            print("== %s" % rel)
            print("   before: %s" % ", ".join("%s %d" % (s, len(h)) for s, h in sorted(before.items())))
            print("   after:  %s" % (", ".join("%s %d" % (s, len(h)) for s, h in sorted(after.items())) or "(none)"))
            newsubj = sorted(set(ac.cited_addresses(new_text)) - set(ac.cited_addresses(text)))
            held = [x for x in newsubj if x in far]
            notheld = [x for x in newsubj if x in fn and x not in far]
            print("   new cited functions: %d, held by R6 %d, NOT held (new subjects) %s"
                  % (len([x for x in newsubj if x in fn]), len(held), notheld))
            for s, h in sorted(after.items()):
                if s not in before:
                    print("   NEW PAIR %s %d: %s" % (s, len(h), detail(h)))
                elif len(h) != len(before[s]):
                    print("   PAIR CHANGED %s %d -> %d" % (s, len(before[s]), len(h)))
                if (rel, s) in want:
                    print("   TARGET STILL OPEN %s %d" % (s, len(h)))
                total_new += 1
            for s in sorted(before):
                if s not in after and (rel, s) not in want:
                    print("   NON-TARGET PAIR CLEARED (check it is not a prose-word clear): %s %d"
                          % (s, len(before[s])))
            for s in sorted(before):
                if s not in after and (rel, s) in want:
                    print("   target cleared: %s %d" % (s, len(before[s])))
            new_trip = sorted(set(trip) - set(neighbours(rel, text, fn, callers, callees)[1]))
            if new_trip:
                print("   new tripwire layers (R6-held far ends): %s" % new_trip)
        print("pairs remaining across pages (incl. non-FABLE pairs on the page): %d" % total_new)
        return

    out = {}
    ok = True
    print("page\tlayer\tfinding_edges\trebuilt_edges\tdetail_match")
    for (rel, sub), fdetail in sorted(want.items()):
        text = io.open(os.path.join(a.docs, rel), encoding="utf-8").read()
        seen, _trip, _far = neighbours(rel, text, fn, callers, callees)
        hits = seen.get(sub, [])
        n_find = int(fdetail.split(" ", 1)[0])
        want_detail = fdetail.split("never mentioned: ", 1)[1]
        match = detail(hits) == want_detail
        ok &= (n_find == len(hits)) and match
        print("%s\t%s\t%d\t%d\t%s" % (rel, sub, n_find, len(hits), "yes" if match else "NO"))
        rows = []
        for addr, direction, other in hits:
            r = fn.get(other, {})
            s = fn.get(addr, {})
            rows.append({
                "cited": addr, "cited_name": s.get("name"), "cited_owner": s.get("owner"),
                "cited_bytes": s.get("body_bytes"),
                "direction": direction, "other": other, "other_name": r.get("name"),
                "other_owner": r.get("owner"), "other_domains": r.get("domains"),
                "other_bytes": r.get("body_bytes"),
                "other_callers": len(callers.get(other, ())),
                "other_callees": len(callees.get(other, ())),
                "cited_callers": len(callers.get(addr, ())),
            })
        out["%s|%s" % (rel, sub)] = rows
    with io.open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print("CONTROL: %s" % ("ALL 24 MATCH (count and 4-edge sample)" if ok else "MISMATCH - see rows"))


if __name__ == "__main__":
    main()
