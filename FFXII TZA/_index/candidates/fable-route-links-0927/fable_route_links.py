"""List the register rows each FABLE commit since a date changed, with the row's status class before and after
(FABLE, Claude Opus 5.5, 2026-09-27). Read-only; prints TSV: commit, row id, old class, new class, first record path."""
import re, subprocess, sys
ROOT = r"C:/Users/Kristian/source/repos/XIIOnline"
REG = "Database/FFXII TZA/_index/OPEN-QUESTIONS.md"
since = sys.argv[1] if len(sys.argv) > 1 else "2026-09-26"
def git(*a):
    return subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
CLASSES = ["NO ADMISSIBLE SOURCE", "OUT OF EVIDENCE BOUNDARY", "SUPERSEDED", "DUPLICATE", "WITHDRAWN", "TRANSFERRED",
           "PARTLY ANSWERED", "ANSWERED", "PARTIAL", "BLOCKED", "OPEN", "REFUTED"]
def cls(status):
    s = status.lstrip("* ")
    for c in CLASSES:
        if s.upper().startswith(c): return c
    return "?" + s[:20]
def rows(text):
    out = {}
    for l in text.splitlines():
        m = re.match(r"^\| ([A-Z]{1,6}-[0-9A-Za-z/]+) \|", l)
        if m:
            body = l.rstrip().rstrip("|").rstrip()
            out[m.group(1)] = body.rsplit(" | ", 1)[-1]
    return out
log = git("log", "--since=" + since, "--format=%H %s", "--", REG).splitlines()
for line in reversed(log):
    sha, subj = line.split(" ", 1)
    if not subj.startswith("FABLE"): continue
    before, after = rows(git("show", sha + "^:" + REG)), rows(git("show", sha + ":" + REG))
    for q in after:
        if before.get(q) != after[q]:
            rec = re.search(r"_index/candidates/[\w./-]+", after[q])
            print("\t".join([sha[:9], q, cls(before.get(q, "(new)")), cls(after[q]), rec.group(0) if rec else "-"]))
