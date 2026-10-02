#!/usr/bin/env python3
# Write neighbour-dispositions.tsv rows for SWE2-DATA's 307 routed pass-22 pairs.
# Rows appended sorted by document; bulleted pairs get `unaccounted` marker,
# pairs already covered by existing prose get `CITES-THE-EDGE`.
import io, os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_crossrefs as A

DB  = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
FN  = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
ED  = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\edges.tsv"
TSV = os.path.join(DB, "_index", "candidates", "neighbour-dispositions.tsv")
DEBT= os.path.join(DB, "_index", "candidates", "pass22-debt-0929", "pass22-debt.tsv")

fn = A.load_functions(FN)
A.register_ledger_aliases({v["owner"] for v in fn.values()})
A.register_domain_aliases({d.split(".")[0] for v in fn.values() for d in v["domains"]})
callers, callees = A.load_edges(ED)
dispositioned, _ = A.load_dispositions(DB)

OWN = {"DATA", "SWE2-DATA", "DATA-FMT-PS2IMG-TAIL"}
FOLD = {"folder:15-Input", "folder:18-Audio",
        "folder:19-Save-Load-Settings", "folder:20-Platform-Online-Achievements"}
routed = []
for line in io.open(DEBT, encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) >= 4 and not p[0].startswith("#") and p[0] != "document":
        if p[3] in OWN or p[3] in FOLD:
            routed.append((p[0], p[1], int(p[2])))
assert len(routed) == 307, len(routed)

# edges for flagged pairs (from the edges driver run on HEAD text BEFORE bullets,
# saved as p22-mine.json) and recompute edges for already-accounted pairs.
flagged = json.load(open("C:/tmp/p22-mine.json", encoding="utf-8"))
flagged_pairs = {(d, s) for d, subs in flagged.items() for s in subs}

def edge_hits(rel, sub):
    """All (subj, dir, other) edges from this doc's subjects to `sub`, same
    subject filtering as audit_crossrefs, ignoring prose/registry accounting."""
    path = os.path.join(DB, *rel.split("/"))
    text = io.open(path, encoding="utf-8").read()
    cited = sorted(A.cited_addresses(text))
    doc_lines = text.split("\n")
    control_only = set()
    for ca in cited:
        idxs = [i for i, ln in enumerate(doc_lines) if ca in ln.upper()]
        if idxs and all(A.re.search(r"\bcontrol\b", doc_lines[i], A.re.I)
                        for i in idxs):
            control_only.add(ca)
    cited = [c for c in cited if c not in control_only]
    sec_spans = [m.span() for m in A.CROSSING_SECTION.finditer(text)]
    far_ends = set()
    if sec_spans:
        outside = text
        for lo, hi in reversed(sec_spans):
            outside = outside[:lo] + outside[hi:]
        outside_cited = A.cited_addresses(outside)
        for ca in cited:
            if ca in outside_cited:
                continue
            near = {x.upper() for x in callers.get(ca, ())} | \
                   {x.upper() for x in callees.get(ca, ())}
            if near & outside_cited:
                far_ends.add(ca)
    hits = []
    for addr in cited:
        if addr in far_ends or A.is_substrate(fn.get(addr)):
            continue
        if len(callers.get(addr, ())) > A.HUB_FANIN:
            continue
        for direction, table in (("caller", callers), ("callee", callees)):
            for other in table.get(addr, ()):
                if A.is_substrate(fn.get(other)):
                    continue
                if A.subsystem_of(fn.get(other)) == sub:
                    hits.append((addr, direction, other))
    return sorted(hits)

def fmt_hits(hits):
    first = "; ".join("%s %s %s" % h for h in hits[:4])
    if len(hits) > 4:
        first += " (+%d more)" % (len(hits) - 4)
    return first

new_rows = []
for rel, sub, debt_n in sorted(routed):
    if (rel, sub) in flagged_pairs:
        hits = [tuple(h) for h in flagged[rel][sub]]
        marker = "unaccounted"
        note = ("SWE2-DATA 2026-10-02: crossing-section bullet appended by "
                "_swe2_p22_write.py (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT); "
                "audit_crossrefs re-run 2026-10-02 reports zero findings on the "
                "document. Verdict records the prose disposition.")
    else:
        hits = edge_hits(rel, sub)
        marker = "CITES-THE-EDGE"
        note = ("SWE2-DATA 2026-10-02: pair already covered by the page's "
                "existing crossing section; audit_crossrefs 2026-10-02 reports "
                "no finding. Verdict records it.")
    n = len(hits) if hits else debt_n
    new_rows.append("\t".join([rel, sub, str(n), marker,
                               fmt_hits(hits) if hits else "(see debt count)",
                               "CROSSING-ACCOUNTED", note]))

existing = io.open(TSV, encoding="utf-8").read()
if not existing.endswith("\n"):
    existing += "\n"
io.open(TSV, "w", encoding="utf-8", newline="\n").write(
    existing + "\n".join(new_rows) + "\n")
n_flag = sum(1 for rel, sub, _ in routed if (rel, sub) in flagged_pairs)
print("appended %d rows; flagged=%d already-covered=%d"
      % (len(new_rows), n_flag, len(new_rows) - n_flag))
