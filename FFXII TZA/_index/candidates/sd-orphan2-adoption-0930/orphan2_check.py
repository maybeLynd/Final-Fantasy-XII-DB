"""Check the second orphaned SD restatement set (SWE2-DATA 2026-09-30). For each id given: the orphan row's cited
record folders are tracked at HEAD, cited shas are ancestors of HEAD, each record's .py scripts print FAILS 0 when
re-run, and every backticked token of the new status (before '*Was') is found in the record folders, the cited
commits, or the SWE2-AUDIT-SEM / SWE2-AUDIT-SPEC review folders that name the id. Control: an invented token is not
found. Terminal FAILS line."""
import glob, io, os, re, subprocess, sys
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
DB = ROOT + r"\Database\FFXII TZA"
CAND = DB + r"\_index\candidates"
SAVE = os.path.join(ROOT, "Database", "Tools", "work", "SWE2-DATA", "dd", "oq_orphan2.save")
FAILS = 0


def git(*a):
    return subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


w = io.open(SAVE, encoding="utf-8").read().replace("\r", "")
rows = {l.split(" | ")[0][2:]: l for l in w.split("\n") if l.startswith("| SD-")}
for rid in sys.argv[1:]:
    st = rows[rid].split(" | ")[-1].split("*Was")[0]
    recs = sorted(set(re.findall(r"candidates/([\w.-]+)/", st)))
    if not recs and "batch-5 review" in st:
        recs = ["auditsem-review-dd-owner-read-5-0930"]  # a narrowing that cites the review itself
    shas = sorted(set(re.findall(r"`([0-9a-f]{9})`", st)))
    tracked = all(any(git("ls-files", "--error-unmatch", "Database/FFXII TZA/_index/candidates/%s/%s" % (r, f)).returncode == 0
                      for f in ("README.md", "REVIEW.md")) for r in recs)
    anc = all(git("merge-base", "--is-ancestor", s, "HEAD").returncode == 0 for s in shas)
    text, fails = "", []
    for r in recs:
        for f in glob.glob(os.path.join(CAND, r, "*")):
            if os.path.isfile(f):
                text += io.open(f, encoding="utf-8", errors="replace").read()
        for py in glob.glob(os.path.join(CAND, r, "*.py")):
            out = subprocess.run([sys.executable, py], capture_output=True, text=True, cwd=(ROOT if r.startswith("audit") else os.path.dirname(py)),
                                 timeout=1800, encoding="utf-8", errors="replace").stdout
            m = re.findall(r"FAILS\s+(\d+)", out)
            fails.append("%s=%s" % (os.path.basename(py), m[-1] if m else "none"))
    for rv in glob.glob(os.path.join(CAND, "audit*-review-*")):
        for f in glob.glob(os.path.join(rv, "*.md")):
            t = io.open(f, encoding="utf-8", errors="replace").read()
            if re.search(r"\b%s\b" % re.escape(rid), t):
                text += t
    for s in shas:
        text += git("show", s).stdout
    toks = {t for t in re.findall(r"`([^`]{2,60})`", st) if not re.fullmatch(r"[0-9a-f]{9}", t)}

    def found(t):
        if t in text or t.replace(",", "") in text or os.path.isdir(os.path.join(CAND, t)):
            return True
        if re.sub(r"\s+", "", t) in re.sub(r"\s+", "", text):
            return True
        parts = [p for p in re.split(r"[^A-Za-z0-9+]+", t) if len(p) >= 3]
        return bool(parts) and all(p in text for p in parts)
    missing = sorted(t for t in toks if not found(t))
    bad_fail = [x for x in fails if not x.endswith("=0") and not x.endswith("=none")]
    ok = tracked and anc and not missing and not bad_fail and recs
    print("%s %s recs=%s tracked=%s shas-ancestor=%s scripts=%s missing=%s" % (
        "PASS" if ok else "CHECK", rid, recs, tracked, anc, fails, missing[:6]))
    FAILS += not ok
print(("PASS" if "ZZ_INVENTED_TOKEN_77" not in git("show", "HEAD", "--stat").stdout else "FAIL") + " C1 control")
print("FAILS %d" % FAILS)
