"""SWE2-AUDIT-SEM (3): is each SD row (as registered in f7a3292bd) residue the register does not already answer, and is
each named on a page? For every SD row: its hex addresses; the OTHER register rows (at the same commit) that mention
any of them, with the leading status word of their status cell; and the pages (at the same commit, the eight owner
pages) that name the SD id."""
import subprocess, re, collections
REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
C = "f7a3292bd"
def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True).stdout.decode("utf-8", "replace")
reg = git("show", "%s:Database/FFXII TZA/_index/OPEN-QUESTIONS.md" % C)
rows = {}
for l in reg.splitlines():
    m = re.match(r"^\|\s*([A-Z][A-Za-z0-9/\-]*)\s*\|", l)
    if m:
        rows[m.group(1)] = l
def status(l):
    cells = [c.strip() for c in l.split("|")]
    st = cells[-2] if len(cells) >= 3 else ""
    m = re.search(r"(ANSWERED|SUPERSEDED|WITHDRAWN|NO ADMISSIBLE SOURCE|OUT OF EVIDENCE BOUNDARY|OPEN|PARTIAL|NARROWED|BLOCKED)", st)
    return m.group(1) if m else st[:20]
pages = [f for f in git("show", "--name-only", "--format=", C).splitlines() if f.endswith(".md") and "_index" not in f]
ptext = {f.split("/")[-1]: git("show", "%s:%s" % (C, f)) for f in pages}
sd = {k: v for k, v in rows.items() if re.fullmatch(r"SD-\d+", k)}
print("SD rows at %s: %d  %s" % (C, len(sd), sorted(sd, key=lambda s: int(s[3:]))))
for k in sorted(sd, key=lambda s: int(s[3:])):
    addrs = sorted(set(re.findall(r"\b0[0-9A-F]{7}\b", sd[k])))
    others = collections.defaultdict(set)
    for rid, l in rows.items():
        if rid == k or rid.startswith("SD-"):
            continue
        for a in addrs:
            if a in l:
                others[(rid, status(l))].add(a)
    closed = {r: a for r, a in others.items() if r[1] in ("ANSWERED", "SUPERSEDED", "WITHDRAWN")}
    named = [p for p, t in ptext.items() if re.search(r"\b%s\b" % k, t)]
    print("%-6s status %-10s addrs %-3d closed rows sharing an address: %s | named on: %s" % (
        k, status(sd[k]), len(addrs), ", ".join("%s(%s)" % (r[0], ",".join(sorted(a))) for r, a in sorted(closed.items()))[:260] or "-", ", ".join(named) or "NONE"))
