"""sweep.py N - replay check_stale_preimage over the last N commits (each touched .md/.tsv/.py file, at most 40 per
commit) and print every commit the gate would have refused. Read-only."""
import os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
import check_stale_preimage as S
R = r"C:\Users\Kristian\source\repos\XIIOnline"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 150
_, out = S.git(R, "log", "--no-merges", "-n", str(N), "--format=%h")
commits = out.split()
flag, files_seen = [], 0
for c in commits:
    _, names = S.git(R, "show", "--format=", "--name-only", c)
    paths = [p for p in names.splitlines() if p.endswith((".md", ".tsv", ".py")) and "/_inbox/" not in p][:40]
    for p in paths:
        files_seen += 1
        for f in S.replay(R, c, p):
            flag.append((c, p, f))
            print("FLAG %s %s <- reverts %s (%s) gone %d/%d restored %d | e.g. %r" % (
                c, p.split("/")[-1], f["commit"], f["subject"][:50], f["gone"], f["added"], f["restored"], f["example"][:80]), flush=True)
print("SWEEP: %d commits, %d (commit, file) pairs, %d flagged" % (len(commits), files_seen, len(flag)))
