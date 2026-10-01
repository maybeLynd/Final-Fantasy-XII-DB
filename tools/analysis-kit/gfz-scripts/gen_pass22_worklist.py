#!/usr/bin/env python3
"""gen_pass22_worklist.py - pass 22's findings ordered by what READING ONE FUNCTION would settle.

Pass 22 is the only audit pass still failing, so its unaccounted document x subsystem pairs are the
last completion blocker. There are ~900 of them across ~235 documents, and the existing ranked file
orders them BY DOCUMENT - which is the order you need if you are going to fix documents one at a
time, and the wrong order if you are going to read functions.

THE FINDINGS CONCENTRATE ON A FEW NEIGHBOURS. Measured 2026-09-14: the top 20 neighbour functions
appear in 33.9% of the pairs, the top 50 in 50.0%, the top 100 in 61.9%. That is because a shared
entry point - a sound request, an id-validity query - is called from every corner of the image, so
every document citing one of its callers inherits its subsystem as a neighbour it never mentions.

So this file answers ONE question: **if you read exactly one more function, which one settles the
most pairs?** Each row is a neighbour function with the pairs it appears in, the documents and
subsystems affected, and whether it is already named in the corpus.

WHAT A ROW IS NOT. It is not a disposition and not a finding count. Reading the function tells you
what the RELATIONSHIP is; each affected document's owner still decides whether that relationship
matters to their page. `the-shared-neighbours-pass-22-keeps-finding.md` is what a row becomes when
it is done: six functions read, 130 pairs given an explanation to point at, and not one other
page edited.

FAN-IN IS PRINTED BESIDE EACH ROW because `audit_crossrefs` excludes >100-caller functions as hubs
when they are the SUBJECT of a document and not when they are the NEIGHBOUR. A row at 99 or 71
callers is doing what a hub does while passing the test; whether that exclusion should be symmetric
is routed to SWE2-FRONTIER and FABLE, not decided here.
"""
import argparse
import collections
import importlib.util
import io
import os
import re
import sys

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")
GRAPH = os.path.join(REPO, "Database", "Tools", "work", "graph")
OUT = os.path.join(DB, "_index", "candidates", "pass22-neighbour-worklist.tsv")
ADDR = re.compile(r"(0[0-9A-Fa-f]{7})")


def load_audit():
    spec = importlib.util.spec_from_file_location("ac", os.path.join(KIT, "audit_crossrefs.py"))
    ac = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ac)
    return ac


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--functions", default=os.path.join(GRAPH, "functions.tsv"))
    ap.add_argument("--edges", default=os.path.join(GRAPH, "edges.tsv"))
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--top", type=int, default=120)
    a = ap.parse_args()

    # A WORKLIST THAT RE-LISTS DISPOSITIONED WORK SENDS SOMEBODY TO DO IT TWICE. The first version
    # ranked the raw finding rule and ignored the registry, so 0020E600's rows reappeared the day
    # after 32 of them were dispositioned. Verdicted pairs are subtracted and counted separately.
    done = set()
    ac = load_audit()
    fn = ac.load_functions(a.functions)
    ac.register_ledger_aliases({v["owner"] for v in fn.values()})
    ac.register_domain_aliases({d.split(".")[0] for v in fn.values() for d in v["domains"]})
    callers, callees = ac.load_edges(a.edges)
    regp = os.path.join(a.db, "_index", "candidates", "neighbour-dispositions.tsv")
    if os.path.isfile(regp):
        for line in io.open(regp, encoding="utf-8", errors="replace"):
            if line.startswith("#") or not line.strip():
                continue
            f = line.rstrip(chr(10)).split(chr(9))
            if len(f) >= 6 and f[5].strip():
                done.add((f[0].strip().replace("\\", "/"), f[1].strip()))

    # THE FINDING RULE IS THE AUDIT'S OWN, re-walked here rather than parsed out of its report,
    # because the report samples four edges per finding and the question here is about ALL of them.
    by_neigh = collections.defaultdict(set)
    pairs = set()
    for root, _d, files in os.walk(a.db):
        top = os.path.relpath(root, a.db).split(os.sep)[0]
        if not re.match(r"^\d\d-", top):
            continue
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, a.db).replace(os.sep, "/")
            text = io.open(p, encoding="utf-8", errors="replace").read()
            low, folder = text.lower(), rel.lower()
            cited = {x.upper() for x in ADDR.findall(text)} & set(fn)
            for addr in cited:
                if ac.is_substrate(fn.get(addr)):
                    continue
                if len(callers.get(addr, ())) > ac.HUB_FANIN:
                    continue
                for table in (callers, callees):
                    for other in table.get(addr, ()):
                        sub = ac.subsystem_of(fn.get(other))
                        if not sub or sub in ac.SUBSTRATE:
                            continue
                        if ac.doc_accounts_for(low, folder, sub):
                            continue
                        if (rel, sub) in done:
                            continue
                        by_neigh[other.upper()].add((rel, sub))
                        pairs.add((rel, sub))

    rank = sorted(by_neigh.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    # THE COVERAGE OF THE TOP N IS A UNION, NOT A SUM. One pair can name several neighbours, so
    # adding the rows' counts double-counts: the first version of this line reported the top 120
    # rows as naming 1,411 of 880 pairs. A coverage figure larger than its own population is the
    # tell, and it was in this file's own output.
    covered = set()
    for _addr, ps in rank[:a.top]:
        covered |= ps
    lines = [
        "# FINAL-AUDIT pass 22, ordered by what READING ONE FUNCTION would settle.",
        "#",
        "# Generated by gen_pass22_worklist.py. Each row is a NEIGHBOUR function and the",
        "# document x subsystem pairs that name it. Reading the function explains the",
        "# relationship for every one of them at once; it does not disposition any of them,",
        "# because each affected page's owner decides whether the edge matters there.",
        "#",
        "# %d unaccounted pairs over %d distinct neighbour functions." % (len(pairs), len(by_neigh)),
        "# The rows below cover %d of those pairs - a UNION, because one pair can name several"
        % len(covered),
        "# neighbours and adding the row counts would double-count it.",
        "# fan_in is the neighbour's caller count: audit_crossrefs drops >%d-caller functions as"
        % ac.HUB_FANIN,
        "# hubs when they are the SUBJECT and not when they are the NEIGHBOUR, so a row near that",
        "# threshold is behaving like a hub while passing the test.",
        "#",
        "address\tpairs\tdocuments\tsubsystems\tfan_in\tsize\tname\towner",
    ]
    for addr, ps in rank[:a.top]:
        rec = fn.get(addr, {})
        docs = len({d for d, _s in ps})
        subs = sorted({s for _d, s in ps})
        lines.append("%s\t%d\t%d\t%s\t%d\t%s\t%s\t%s"
                     % (addr, len(ps), docs, ",".join(subs)[:60], len(callers.get(addr, ())),
                        rec.get("body_bytes", ""), rec.get("name", ""), rec.get("owner", "")))
    io.open(a.out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("wrote %s" % a.out)
    print("  %d OPEN pairs over %d neighbours; %d pair(s) already carry a registry verdict and are"
          % (len(pairs), len(by_neigh), len(done)))
    print("  not listed - a worklist that re-lists dispositioned work sends somebody to do it twice.")
    print("  The top %d rows cover %d of the open pairs (%.1f%%)."
          % (min(a.top, len(rank)), len(covered), 100.0 * len(covered) / max(1, len(pairs))))
    for addr, ps in rank[:10]:
        rec = fn.get(addr, {})
        print("    %s  %3d pairs  fan-in %4d  %s"
              % (addr, len(ps), len(callers.get(addr, ())), (rec.get("name") or "")[:44]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
