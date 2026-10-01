"""shape_clusters.py X OUT - group the frontier's small-shape candidates (tiny-leaf, forwarder, getter-leaf, setter-leaf,
jmp-thunk; UC-1 excluded) on a clean export X by instruction skeleton (mnemonics + operand kinds, constants and
addresses abstracted), and for each skeleton count its census-wide twins by disposition (frontier / A / which family).
Planning census for new-family proposals; declares nothing."""
import collections, os, re, sys
X, OUT = sys.argv[1], sys.argv[2]
DB = os.path.join(X, "Database", "FFXII TZA")
sys.path.insert(0, os.path.join(X, "Database", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, os.path.join(DB, "_index", "candidates", "f-frontier-shapes-0930"))
import check_dispositions as CD
import f_shapes as F
sizes = CD.load_functions()
r = CD.evaluate(DB, sizes)
fr = r["frontier_set"]
uc1 = set(CD.uc1_band.frontier_starts())
a_only = r["explained_set"] - r["claimed_set"]
owner = {}
for doc, p in CD.parse_families(DB):
    try:
        for m in CD.read_members(doc, p[2]): owner.setdefault(m, p[0])
    except Exception: pass
SMALL = {"tiny-leaf", "forwarder", "getter-leaf", "setter-leaf", "jmp-thunk"}
HEX = re.compile(r"0x[0-9a-f]+")
def skel(a):
    ins = list(F.R.md.disasm(F.R.at(a, min(sizes[a], 64)), a))
    out = []
    for i in ins:
        ops = HEX.sub("K", i.op_str)
        if i.mnemonic in ("call", "jmp") or i.mnemonic.startswith("j"):
            ops = "T" if not ops.startswith(("q", "r", "e")) else ops
        out.append(i.mnemonic + " " + ops)
    return " ; ".join(out), ins
cand = {}
for a in fr:
    if a in uc1 or a not in sizes: continue
    b, _ = F.bucket(a, sizes[a])
    if b in SMALL:
        cand[a] = (b, skel(a)[0])
print("small-shape frontier candidates:", len(cand))
by = collections.defaultdict(list)
for a, (b, s) in cand.items(): by[s].append(a)
# census twins for skeletons with >= 2 candidates or any candidate
twins = collections.defaultdict(collections.Counter)
want = set(by)
for a, n in sizes.items():
    if n > 64 or a in uc1: continue
    try: s = skel(a)[0]
    except Exception: continue
    if s not in want: continue
    st = "frontier" if a in fr else ("A" if a in a_only else "family:" + owner.get(a, "?")[:50])
    twins[s][st] += 1
with open(OUT, "w", encoding="utf-8") as o:
    rows = sorted(by.items(), key=lambda kv: -len(kv[1]))
    o.write("candidates\tbucket\tskeleton\tcensus_twins\texamples\n")
    for s, al in rows:
        o.write("%d\t%s\t%s\t%s\t%s\n" % (len(al), cand[al[0]][0], s[:160],
                "; ".join("%s=%d" % kv for kv in twins[s].most_common(4)), " ".join("%08X" % a for a in sorted(al)[:6])))
print("distinct skeletons:", len(by), " with >=3 candidates:", sum(1 for v in by.values() if len(v) >= 3),
      " candidates in those:", sum(len(v) for v in by.values() if len(v) >= 3))
