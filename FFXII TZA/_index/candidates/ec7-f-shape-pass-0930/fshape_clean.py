"""fshape_clean.py X OUT.tsv - OPUS's f_shapes buckets over check_dispositions' frontier on the clean export X."""
import collections, os, sys
X, OUT = sys.argv[1], sys.argv[2]
DB = os.path.join(X, "Database", "FFXII TZA")
sys.path.insert(0, os.path.join(X, "Database", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, os.path.join(DB, "_index", "candidates", "f-frontier-shapes-0930"))
import check_dispositions as CD
import f_shapes as F
sizes = CD.load_functions()
r = CD.evaluate(DB, sizes)
fr = sorted(r["frontier_set"])
uc1 = CD.uc1_band.frontier_starts()
cnt = collections.Counter()
with open(OUT, "w", encoding="utf-8", newline="\n") as o:
    o.write("entry\tbucket\tbytes\tuc1\n")
    for a in fr:
        n = sizes[a]
        b, _ = F.bucket(a, n)
        u = "uc1" if a in uc1 else ""
        cnt[(b, u)] += 1
        o.write("%08X\t%s\t%d\t%s\n" % (a, b, n, u))
print("frontier %d (refused rows %d)" % (len(fr), r["families_refused"]))
for (b, u), v in sorted(cnt.items(), key=lambda kv: -kv[1]):
    print("  %-12s %-4s %5d" % (b, u, v))
