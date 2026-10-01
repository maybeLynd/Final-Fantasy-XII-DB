"""SWE2-AUDIT-SEM (3): is each SD row registered by the reviewed commit residue the database did not already answer, and
is each named on its page?  For every new SD row: its hex addresses; the OTHER register rows (at the commit) that mention
any of them with their status word; the candidate folders (at the commit's PARENT, i.e. before the row existed; the
producer's own dd-data-* folder excluded) whose files mention any of them; the changed pages that name the id; and the
row's status word at HEAD (status currency).  Usage: python sd_rows_check.py [COMMIT] (default batch 3, 71af93479)."""
import subprocess, re, collections, sys
REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
C = sys.argv[1] if len(sys.argv) > 1 else "71af93479"
REG = "Database/FFXII TZA/_index/OPEN-QUESTIONS.md"
CAND = "Database/FFXII TZA/_index/candidates"
def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True).stdout.decode("utf-8", "replace")
def rows_of(text):
    r = {}
    for l in text.splitlines():
        m = re.match(r"^\|\s*([A-Z][A-Za-z0-9/\-]*)\s*\|", l)
        if m:
            r[m.group(1)] = l
    return r
def status(l):
    cells = [c.strip() for c in l.split("|")]
    st = cells[-2] if len(cells) >= 3 else ""
    m = re.search(r"(ANSWERED|SUPERSEDED|WITHDRAWN|NO ADMISSIBLE SOURCE|OUT OF EVIDENCE BOUNDARY|OPEN|PARTIAL|NARROWED|BLOCKED)", st)
    return m.group(1) if m else st[:20]
rows = rows_of(git("show", "%s:%s" % (C, REG)))
parent_rows = rows_of(git("show", "%s^:%s" % (C, REG)))
head_rows = rows_of(git("show", "HEAD:%s" % REG))
new = sorted((k for k in rows if re.fullmatch(r"SD-\d+", k) and k not in parent_rows), key=lambda s: int(s[3:]))
pages = [f for f in git("show", "--name-only", "--format=", C).splitlines() if f.endswith(".md") and "/_index/" not in f]
ptext = {f.split("/")[-1]: git("show", "%s:%s" % (C, f)) for f in pages}
print("new SD rows at %s: %d  %s" % (C, len(new), " ".join(new)))
for k in new:
    addrs = sorted(set(re.findall(r"\b0[0-9A-F]{7}\b", rows[k])))
    others = collections.defaultdict(set)
    for rid, l in rows.items():
        if rid == k or rid.startswith("SD-"):
            continue
        for a in addrs:
            if a in l:
                others[(rid, status(l))].add(a)
    cands = collections.defaultdict(set)
    for a in addrs:
        for f in git("grep", "-l", a, "%s^" % C, "--", CAND).splitlines():
            d = f.split(CAND + "/", 1)[-1].split("/")[0]
            if not d.startswith("dd-data-"):
                cands[d].add(a)
    named = [p for p, t in ptext.items() if re.search(r"\b%s\b" % k, t)]
    print("\n%-6s at-commit %-6s HEAD %-8s addrs %s" % (k, status(rows[k]), status(head_rows.get(k, "")) or "MISSING", " ".join(addrs) or "-"))
    print("   register rows sharing an address: %s" % (", ".join("%s[%s](%s)" % (r[0], r[1], ",".join(sorted(a))) for r, a in sorted(others.items())) or "-"))
    print("   candidate folders (at parent) sharing an address: %s" % (", ".join("%s(%s)" % (d, ",".join(sorted(a))) for d, a in sorted(cands.items())) or "-"))
    print("   named on: %s" % (", ".join(named) or "NONE"))
