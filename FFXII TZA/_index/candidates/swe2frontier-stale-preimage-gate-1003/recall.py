"""recall.py COMMIT... - replay the gate over every touched text file of known stale-sweep commits."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
import check_stale_preimage as S
R = r"C:\Users\Kristian\source\repos\XIIOnline"
for c in sys.argv[1:]:
    _, subj = S.git(R, "log", "-1", "--format=%h %s", c)
    _, names = S.git(R, "show", "--format=", "--name-only", c)
    paths = [p for p in names.splitlines() if p.endswith((".md", ".tsv", ".py"))]
    hits = []
    for p in paths:
        for f in S.replay(R, c, p):
            hits.append("%s <- %s (%s) gone %d/%d restored %d" % (p.split("/")[-1], f["commit"], f["subject"][:45], f["gone"], f["added"], f["restored"]))
    print("== %s | %d files | %d flagged" % (subj.strip()[:90], len(paths), len(hits)))
    for h in hits:
        print("   " + h)
