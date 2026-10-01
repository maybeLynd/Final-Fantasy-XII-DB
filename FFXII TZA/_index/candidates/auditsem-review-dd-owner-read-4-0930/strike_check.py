"""SWE2-AUDIT-SEM (1): does every strike added in the reviewed commit quote real old text? For each .md page the commit
changed (register and inbox excluded), every ~~struck span~~ in the NEW version that was not already struck in the parent
is searched in the parent's text (whitespace normalised). A span not found verbatim is printed with the parent's nearest
line for reading.  Usage: python strike_check.py [COMMIT]   (default: batch 4, 4415dba48)."""
import subprocess, re, difflib, sys
REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
C = sys.argv[1] if len(sys.argv) > 1 else "4415dba48"
def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True).stdout.decode("utf-8", "replace")
files = [f for f in git("show", "--name-only", "--format=", C).splitlines()
         if f.endswith(".md") and "/_index/" not in f]
norm = lambda s: re.sub(r"\s+", " ", s).strip()
tot = bad = 0
for f in files:
    oldraw = git("show", "%s^:%s" % (C, f))
    new = git("show", "%s:%s" % (C, f))
    old = norm(oldraw)
    olds = set(norm(m.group(1)) for m in re.finditer(r"~~(.+?)~~", oldraw, re.S))
    n = 0
    for m in re.finditer(r"~~(.+?)~~", new, re.S):
        span = norm(m.group(1))
        if span in olds or len(span) < 6:
            continue
        tot += 1; n += 1
        if span not in old:
            bad += 1
            best = max((l for l in oldraw.splitlines()), key=lambda l: difflib.SequenceMatcher(None, norm(l), span[:120]).ratio(), default="")
            print("NOT VERBATIM  %s\n   struck: %s\n   parent: %s" % (f.split("/")[-1], span[:260], norm(best)[:260]))
    print("  %-70s new strikes %d" % (f.split("/")[-1], n))
print("commit %s: new struck spans %d, not found verbatim in the parent: %d" % (C, tot, bad))
