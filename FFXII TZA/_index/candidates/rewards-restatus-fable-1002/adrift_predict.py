"""adrift_predict.py PAGE... - before re-statusing a page DOCUMENTED, list its citations that sit strictly inside a
function body that is a member of a declared family (check_dispositions would then measure that member A and refuse
the family). Uses check_dispositions' own loaders. Run from Database/. Prints one line per hit and HITS n."""
import bisect, io, os, sys
sys.path.insert(0, "Tools/analysis-kit/gfz-scripts")
import check_dispositions as CD
db = "FFXII TZA"
sizes = CD.load_functions()
if isinstance(sizes, tuple): sizes = sizes[0]
entries = sorted(sizes)
fam = {}
for doc, parts in CD.parse_families(db):
    if len(parts) < 5: continue
    try: members = CD.read_members(doc, parts[2])
    except Exception: continue
    for m in members: fam.setdefault(m, parts[0].strip()[:50])
hits = 0
for p in sys.argv[1:]:
    t = io.open(p, encoding="utf-8", errors="replace").read()
    for h in sorted(set(CD.CITE.findall(t))):
        v = int(h, 16); i = bisect.bisect_right(entries, v) - 1
        if i < 0: continue
        e = entries[i]
        if e < v < e + sizes[e] and e in fam:
            hits += 1; print("%s  %08X inside %08X  family %s" % (os.path.basename(p), v, e, fam[e]))
print("HITS %d" % hits)
