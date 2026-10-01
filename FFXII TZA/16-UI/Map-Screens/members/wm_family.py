"""wm_family.py: the world map menu widget family. Members = functions with a rip reference to the singleton 02B457E0,
plus functions called ONLY from members (closure). Prints per member: size, name, frontier flag, callers outside the
family, and widget field displacements read/written through the singleton pointer."""
import json, collections, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
GFZ = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, GFZ)
import check_dispositions as cd
import frontier_census as fc
import data_xref_scan as dxs
import call_graph as cg

GRAPH = os.path.join(GFZ, "..", "..", "work", "graph")
FUNCS = os.path.join(GRAPH, "functions.tsv")
EXE = os.path.abspath(os.path.join(GFZ, "..", "..", "work", "exe", "FFXII_TZA.exe"))
DB = cd.DEFAULT_DB

sizes, names = {}, {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError): pass
ks = sorted(sizes)
front = fc.frontier_set(DB, sizes)          # the live frontier; was arch_frontier.txt + c_frontier.txt

# seed: every FUN_-named body holding a reference to the singleton (was tools/ripscan.py)
blob = open(EXE, "rb").read()
secs = dxs.sections_of(blob)
funcs = dxs.entries(FUNCS)
res = dxs.scan(blob, secs, funcs, set(range(0x02B457E0, 0x02B457E8)))
seed = {fva for rows in res.values() for (_iva, _mn, _op, fva) in rows
        if names.get(fva, "").startswith("FUN_")}

# call graph rebuilt from the EXE + functions.tsv, calls AND tail jumps (was tools/rawcalls.json;
# edges.tsv alone would do for calls but drops tail jumps - 0037ED70 jmp 0037EB90 is a member edge)
callers, callees, _sites = cg.call_maps(EXE, FUNCS)

fam = set(seed)
while True:
    add = set()
    for f in fam:
        for c in callees[f]:
            if c not in fam and c in sizes and callers[c] and callers[c] <= fam: add.add(c)
    if not add: break
    fam |= add
print("seed", len(seed), "closure", len(fam), "frontier", len(fam & front), "bytes", sum(sizes[f] for f in fam))
ext = {}
for f in sorted(fam):
    xc = sorted(c for c in callers[f] if c not in fam)
    if xc: ext[f] = xc
print("members called from outside the family:", len(ext))
for f, xc in ext.items():
    print("  %08X %-45s <- %s" % (f, names.get(f, "")[:45], ", ".join("%08X %s" % (c, names.get(c, "")[:30]) for c in xc[:5])))
print("closure-only members (no singleton ref):", " ".join("%08X" % f for f in sorted(fam - seed)))
json.dump({"seed": sorted("%08X" % f for f in seed), "family": sorted("%08X" % f for f in fam)}, open(os.path.join(HERE, "wm_family.json"), "w"))
