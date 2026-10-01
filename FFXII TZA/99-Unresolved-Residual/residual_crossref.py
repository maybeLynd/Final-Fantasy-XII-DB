"""residual_crossref.py — which of the unresolved residual functions are cited by pages OTHER than the residual pages,
and whether any citation lands strictly inside the body (interior). Writes residual-crossref.tsv beside this script.
Run from the repository root: python "Database/FFXII TZA/99-Unresolved-Residual/residual_crossref.py"
Inputs: Database/Tools/work/verify_GFZ_PARENT/residual_addrs.txt - the ROLE-named directory, which
tracks the certified parent and survives a checkpoint advance (the bare work/verify/ alias is a
GN160-era snapshot that went stale silently; repointed 2026-09-16, OPUS-REQ-SWE2-EC7-RESIDUAL-
CROSSREF-STALE) - Database/Tools/work/graph/functions.tsv, every .md under the
database except _index/_inbox/_experiments, the-unresolved-158.md, this folder's README.md (the ledger's own index,
which audits the residual dump rather than documenting a function; excluded 2026-09-13 after SWE2-AUDIT-SEM's review) and
the Unowned-Code-Census folder.
CITATION FORM LIMIT: only backticked bare 8-hex addresses (`0XXXXXXX`) are read. 0x-prefixed, unbackticked and FUN_-style
forms, and name-only citations, are not. SWE2-AUDIT-SEM's broad sweep found one genuine cite of that kind (in the README,
now excluded by rule) and two false ones (a range bound, a rip displacement)."""
import re, glob, os, bisect, collections
ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.dirname(ROOT)
TOOLS = os.path.join(os.path.dirname(DB), "Tools")
res = []
for l in open(os.path.join(TOOLS, "work", "verify_GFZ_PARENT", "residual_addrs.txt")):
    m = re.match(r"\s*(?:0x)?([0-9A-Fa-f]{6,8})\b", l)
    if m: res.append(int(m.group(1), 16))
sizes = {}
for l in open(os.path.join(TOOLS, "work", "graph", "functions.tsv"), encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
ks = sorted(sizes)
def own(a):
    i = bisect.bisect_right(ks, a) - 1
    return ks[i] if i >= 0 and ks[i] <= a < ks[i] + sizes[ks[i]] else None
R = set(res)
entry = collections.defaultdict(set); interior = collections.defaultdict(set)
for p in glob.glob(os.path.join(DB, "**", "*.md"), recursive=True):
    rp = os.path.relpath(p, DB).replace("\\", "/")
    if rp.startswith("_") or rp.endswith("the-unresolved-158.md") or rp == "99-Unresolved-Residual/README.md" or "Unowned-Code-Census" in rp: continue
    txt = open(p, encoding="utf-8", errors="replace").read()
    for m in set(re.findall(r"`(0[0-9A-Fa-f]{7})`", txt)):
        a = int(m, 16)
        if a in R: entry[a].add(rp)
        else:
            o = own(a)
            if o in R: interior[o].add(rp)
out = os.path.join(ROOT, "residual-crossref.tsv")
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write("address\tsize\tinterior_cited\tpages\n")
    for a in sorted(R):
        ent, inn = entry.get(a, set()), interior.get(a, set())
        pages = sorted(ent | inn)
        f.write("%08X\t%d\t%s\t%s\n" % (a, sizes.get(a, 0), "yes" if inn else "no", "; ".join(pages)))
cited = [a for a in R if entry.get(a) or interior.get(a)]
print("residual", len(R), "cited elsewhere", len(cited), "interior-cited", sum(1 for a in R if interior.get(a)), "->", out)
