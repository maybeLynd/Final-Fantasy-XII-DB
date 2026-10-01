"""collect.py - for every live SD row whose id is answered/narrowed in a commit subject since 2026-09-30, collect:
the commit, its subject (the author's own one-line answer), the record README(s) it added under _index/candidates/,
the record's scripts, and whether each script re-runs to FAILS 0. Writes incorp/plan.tsv. Read-only on the DB."""
import subprocess, re, io, os, sys
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline")
OQ = "Database/FFXII TZA/_index/OPEN-QUESTIONS.md"
CELL = re.compile(r"(?<!\\)\|")
live = {}
for l in io.open(OQ, encoding="utf-8").read().split("\n"):
    m = re.match(r"^\| (SD-\d+) \|", l)
    if not m: continue
    st = [c.strip() for c in CELL.split(l)[1:-1]][-1]
    if re.match(r"^\**(OPEN|PARTIAL)", st.lstrip("~ ")): live[m.group(1)] = st[:40]
log = subprocess.run(["git", "log", "--since=2026-09-30T00:00", "--format=%h\t%s"], capture_output=True, text=True,
                     encoding="utf-8", errors="replace").stdout.splitlines()
rows = []
for rid in sorted(live, key=lambda x: int(x.split("-")[1])):
    for h in log:
        sha, subj = h.split("\t", 1)
        if not re.search(r"\b%s\b" % rid, subj) or not re.search(r"answered|narrowed|typed", subj, re.I): continue
        if "adopt the orphaned" in subj: continue
        files = subprocess.run(["git", "show", "--name-only", "--format=", sha], capture_output=True, text=True).stdout.split("\n")
        recs = sorted({os.path.dirname(f) for f in files if "/_index/candidates/" in f and f.endswith("README.md")})
        scripts = [f for f in files if "/_index/candidates/" in f and f.endswith(".py")]
        verdict = "answered" if re.search(r"\b%s\b[^-]*answered|answered[^-]*\b%s\b" % (rid, rid), subj) else \
                  ("narrowed" if "narrowed" in subj.lower() else "answered")
        # re-run each script from its own directory
        res = []
        for s in scripts:
            r = subprocess.run([sys.executable, os.path.basename(s)], cwd=os.path.dirname(s), capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=900)
            fm = re.findall(r"FAILS (\d+)", r.stdout)
            res.append("%s:%s" % (os.path.basename(s), fm[-1] if fm else ("rc%d" % r.returncode)))
        rows.append((rid, sha, verdict, subj.split(" - ", 1)[1] if " - " in subj else subj, ";".join(recs), ",".join(res)))
        break
os.makedirs("Database/Tools/work/FABLE/incorp", exist_ok=True)
with io.open("Database/Tools/work/FABLE/incorp/plan.tsv", "w", encoding="utf-8") as f:
    for r in rows: f.write("\t".join(r) + "\n")
for r in rows: print("%-7s %s %-8s recs=%d checks=%s | %s" % (r[0], r[1], r[2], len(r[4].split(";")) if r[4] else 0, r[5][:60], r[3][:70]))
print("rows:", len(rows))
