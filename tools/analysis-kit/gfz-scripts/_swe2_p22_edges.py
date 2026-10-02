#!/usr/bin/env python3
# Driver: reproduce audit_crossrefs' `seen` neighbour edge map for a named set
# of documents, so crossing-section bullets name the real subjects/far ends.
import io, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_crossrefs as A

DOCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
FN   = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
ED   = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\edges.tsv"

fn = A.load_functions(FN)
A.register_ledger_aliases({v["owner"] for v in fn.values()})
A.register_domain_aliases({d.split(".")[0] for v in fn.values() for d in v["domains"]})
callers, callees = A.load_edges(ED)
dispositioned, _unk = A.load_dispositions(DOCS)

mine = set()
for line in io.open(os.path.join(DOCS, "_index", "candidates", "pass22-debt-0929", "pass22-debt.tsv"), encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) >= 4 and not p[0].startswith("#") and p[0] != "document":
        if p[3] in ("DATA", "DATA-FMT-PS2IMG-TAIL", "SWE2-DATA",
                    "folder:15-Input", "folder:18-Audio",
                    "folder:19-Save-Load-Settings", "folder:20-Platform-Online-Achievements"):
            mine.add(p[0])

out = {}
for rel in sorted(mine):
    path = os.path.join(DOCS, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        continue
    text = io.open(path, encoding="utf-8").read()
    folder_low = rel.lower()
    xlow = "".join(m.group(0) for m in A.CROSSING_SECTION.finditer(
        A.body_text(text))).lower()
    cited = sorted(A.cited_addresses(text))
    if not cited:
        continue
    doc_lines = text.split("\n")
    lines_upper = [ln.upper() for ln in doc_lines]
    control_only = set()
    for ca in cited:
        idxs = [i for i, ln in enumerate(lines_upper) if ca in ln]
        if idxs and all(re.search(r"\bcontrol\b", doc_lines[i], re.I) for i in idxs):
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
    seen = {}
    for addr in cited:
        if addr in far_ends:
            continue
        if A.is_substrate(fn.get(addr)):
            continue
        if len(callers.get(addr, ())) > A.HUB_FANIN:
            continue
        for direction, table in (("caller", callers), ("callee", callees)):
            for other in table.get(addr, ()):
                if A.is_substrate(fn.get(other)):
                    continue
                sub = A.subsystem_of(fn.get(other))
                if not sub or sub in A.SUBSTRATE:
                    continue
                if not A.doc_accounts_for(xlow, folder_low, sub):
                    if (rel, sub) in dispositioned:
                        continue
                    seen.setdefault(sub, []).append((addr, direction, other))
    for sub in seen:
        seen[sub].sort()
    out[rel] = {s: v for s, v in sorted(seen.items())}

json.dump(out, open("C:/tmp/p22-mine.json", "w", encoding="utf-8"), indent=0)
tot = sum(len(v) for v in out.values())
print("docs with findings:", len(out), "pairs:", tot)
for d, subs in out.items():
    print("%3d %s" % (sum(len(v) for v in subs.values()), d))
