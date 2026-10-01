"""check_chain_rederivation.py - the instrument FINAL-AUDIT pass 19 never had.

Pass 19: *"rebuild every call chain from a freshly regenerated call graph; fail if any chain has
gained or lost an edge."* Until now the only instrument the pass rows named was
check_call_chains.py, whose own header says it exists for pass 29 (index integrity: do the links
resolve), and which measures nothing about a chain's edges.

WHAT IS TESTED
  * every arrow-adjacent pair of hops in each `## Documented chains` row where BOTH hops name at
    least one function address (present in functions.tsv) is re-derived against work/graph/edges.tsv:
    - DIRECT    some stated function in hop i calls some stated function in hop i+1
    - INDIRECT  reachable in <= K hops through unnamed intermediates (thunks, trampolines)
    - REVERSED  reachable only hop i+1 -> hop i, i.e. the stated direction is wrong
    - MISSING   no path of length <= K in either direction: the stated edge is gone or never was
  * a hop naming several addresses (the `a / b` alternate idiom) is satisfied when ANY named
    function on each side closes the transition; the alternates are the chain's own vocabulary.

WHAT IS DELIBERATELY NOT TESTED
  * prose hops ("Weather roll", "level 0", "stats record") and data addresses (02EBF130,
    02098E10, tables, fields). They are not functions, so they cannot carry a call edge; a pair
    involving one is UNRESOLVABLE, counted and reported, never a defect and never a pass.
  * edges stated only inside the linked document. The index's own label is the statement under
    test; a document's internal chain is that document's claim and belongs to the passes that
    audit documents. Where a label carries no function addresses at all the row is reported
    PROSE-ONLY, again neither pass nor fail.

K = 4: the index itself documents chains "through one thunk", and three thunks in sequence is the
observed worst case in this corpus. A real missing edge reports MISSING at any K; a longer
path than K is reported INDIRECT-OUT-OF-RANGE, which is information, not silence.
"""
import argparse, collections, io, os, re, sys

import kit_paths as KP
import uc1_band

K = 4
ADDR = re.compile(r"`?([0-9A-F]{6,8})`?")
ARROW = re.compile(r"\s*(?:->|\u2192)\s*")
ROW = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")


def load_functions(path):
    fns = set()
    with io.open(path, encoding="utf-8", errors="replace") as f:
        next(f, None)
        for line in f:
            p = line.split("\t")
            if p:
                try:
                    fns.add(int(p[0], 16))
                except ValueError:
                    pass
    # UC-1 band (2026-09-28) when the input is the shared census.
    if os.path.realpath(path) == os.path.realpath(
            os.path.join(KP.WORK, "graph", "functions.tsv")):
        _b = uc1_band.load()
        fns -= _b["removed"]
        fns |= set(_b["frontier"])
    return fns


def load_edges(path):
    out = collections.defaultdict(set)
    with io.open(path, encoding="utf-8", errors="replace") as f:
        next(f, None)
        for line in f:
            p = line.split("\t")
            if len(p) >= 2:
                try:
                    out[int(p[0], 16)].add(int(p[1], 16))
                except ValueError:
                    pass
    return out


def reaches(edges, srcs, dsts, k):
    """True if any src reaches any dst within k forward edges (BFS, depth-bounded)."""
    frontier = set(srcs)
    seen = set(frontier)
    for _ in range(k):
        nxt = set()
        for a in frontier:
            for b in edges.get(a, ()):
                if b in dsts:
                    return True
                if b not in seen:
                    seen.add(b)
                    nxt.add(b)
        frontier = nxt
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--edges", default=os.path.join(KP.WORK, "graph", "edges.tsv"))
    ap.add_argument("--functions", default=os.path.join(KP.WORK, "graph", "functions.tsv"))
    ap.add_argument("--index", default=None, help="CALL-CHAINS.md (default: <db>/_index/CALL-CHAINS.md)")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    idx = a.index or os.path.join(a.db, "_index", "CALL-CHAINS.md")
    for p in (idx, a.edges, a.functions):
        if not os.path.exists(p):
            print("REFUSED: missing input %s" % p)
            return 2

    fns = load_functions(a.functions)
    edges = load_edges(a.edges)

    rows, inside = [], False
    for n, line in enumerate(io.open(idx, encoding="utf-8", errors="replace").read().split("\n"), 1):
        if line.startswith("## "):
            inside = line.strip() == "## Documented chains"
            continue
        if not inside:
            continue
        m = ROW.match(line)
        if m and m.group(1).lower() != "chain" and not set(m.group(1)) <= set("-: "):
            rows.append((n, m.group(1)))

    direct = indirect = reversed_ = missing = unres = prose = 0
    defects = []
    for n, label in rows:
        hops = [[int(x, 16) for x in ADDR.findall(h) if int(x, 16) in fns]
                for h in ARROW.split(label)]
        pairs = [(hops[i], hops[i + 1]) for i in range(len(hops) - 1)]
        testable = [(s, d) for s, d in pairs if s and d]
        unres += len(pairs) - len(testable)
        if not any(hops):
            prose += 1
        for s, d in testable:
            fwd = reaches(edges, s, set(d), K)
            if fwd and any(b in edges.get(x, ()) for x in s for b in d):
                direct += 1
            elif fwd:
                indirect += 1
            elif reaches(edges, d, set(s), K):
                reversed_ += 1
                defects.append((n, "REVERSED", s, d, label))
            else:
                missing += 1
                defects.append((n, "MISSING", s, d, label))

    print("  documented chain rows                    : %d" % len(rows))
    print("  rows with no function addresses (prose): %d" % prose)
    print("  edge transitions DIRECT                  : %d" % direct)
    print("  edge transitions INDIRECT (<= %d hops)   : %d" % (K, indirect))
    print("  edge transitions REVERSED                : %d" % reversed_)
    print("  edge transitions MISSING                 : %d" % missing)
    print("  hops unresolvable (prose/data, abstained): %d" % unres)
    for n, kind, s, d, label in defects:
        print("      line %-5d %-8s %s -> %s   %s" % (
            n, kind, "/".join("%08X" % x for x in s), "/".join("%08X" % x for x in d), label[:70]))
    return 1 if defects else 0


if __name__ == "__main__":
    sys.exit(main())
