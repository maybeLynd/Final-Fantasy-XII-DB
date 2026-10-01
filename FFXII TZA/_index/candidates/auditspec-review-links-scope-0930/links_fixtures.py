"""links_fixtures.py - SWE2-AUDIT-SPEC sensitivity fixtures for check_links.py's 145ac7e3b scope corrections.

Builds a fixture tree under C:\\t\\auditspec\\links-fx with one REAL broken (or real resolving) link per exempted
shape, runs a COPY of the post-fix checker (145ac7e3b) and of the pre-fix checker (145ac7e3b^) with --raw --db, and
prints for every case whether each version reports it. Nothing in the repository is written or modified.
Case ids:  A* captures, B* code spans, C* percent-decoding.  expect = what a rendered-Markdown reader would see.
"""
import os, shutil, subprocess, sys, urllib.parse
REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
KIT = "Database/Tools/analysis-kit/gfz-scripts"
BASE = r"C:\t\auditspec"
TOOLS = {"post": os.path.join(BASE, "links-tool-post"), "pre": os.path.join(BASE, "links-tool-pre")}
FX = os.path.join(BASE, "links-fx")

def git_show(rev, path):
    return subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (rev, path)], capture_output=True).stdout

for tag, rev in (("post", "145ac7e3b"), ("pre", "145ac7e3b^")):
    d = TOOLS[tag]; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for f in ("check_links.py", "head_scope.py", "kit_paths.py"):
        open(os.path.join(d, f), "wb").write(git_show(rev, KIT + "/" + f))

shutil.rmtree(FX, ignore_errors=True)
def w(rel, text):
    p = os.path.join(FX, *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)

# (target token, file, line, expect_broken_in_rendered_markdown, description)
CASES = [
 ("A1-missing.md", "_experiments/evidence/pkg/run-01/README.md", "[r](A1-missing.md)", True,
  "authored README inside a run-NN subdirectory (not a capture)"),
 ("A2-missing.md", "_experiments/evidence/pkg/retained/page.md", "[r](A2-missing.md)", True,
  "true capture in retained/ (broken in its new location)"),
 ("A3-missing.md", "_experiments/evidence/pkg/README.md", "[r](A3-missing.md)", True,
  "package-level README (control: must stay judged)"),
 ("B1-missing.md", "b.md", "``a`b`` then [real](B1-missing.md) and `c`", True,
  "double-backtick span with an inner backtick, then a real link on the line"),
 ("B2-missing.md", "b.md", "`x` [real](B2-missing.md) `vtbl[0](y)`", True,
  "real link between a plain span and a span containing ]( (balanced)"),
 ("B3-missing.md", "b.md", "[`f](x`](B3-missing.md)", True,
  "link whose code-span label itself contains ]("),
 ("B4-missing.md", "b.md", "`[notalink](B4-missing.md)`", False,
  "whole link inside a code span (Markdown renders code, not a link)"),
 ("B5-missing.md", "b.md", "odd ` tick [real](B5-missing.md) then `code](y)`", False,
  "unbalanced tick: CommonMark pairs the same backticks, so this is code"),
 ("B6-missing.md", "b.md", "```a`` [real](B6-missing.md) ``b](c``", False,
  "unmatched ``` run; the two `` runs pair around the link, so CommonMark renders code (not a link)"),
 ("C1%20missing.md", "c.md", "[p](C1%20missing.md)", True,
  "%20 target whose decoded file is missing, raw-named file present"),
 ("C2%20ok.md", "c.md", "[p](C2%20ok.md)", False,
  "%20 target whose decoded file exists (L5 shape)"),
 ("C3%2F..%2Fc3.md", "c.md", "[p](C3%2F..%2Fc3.md)", True,
  "%2F-encoded traversal: raw path missing, decoded path exists"),
 ("C4-plain-missing.md", "c.md", "[p](C4-plain-missing.md)", True, "plain control"),
]
for tok, f, line, exp, desc in CASES:
    p = os.path.join(FX, *f.split("/"))
    prev = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    w(f, prev + line + "\n")
w("C1%20missing.md", "raw-named file exists; decoded 'C1 missing.md' does not\n")
w("C2 ok.md", "decoded file exists\n")
w("c3.md", "decoded traversal target exists\n")

res = {}
for tag, d in TOOLS.items():
    r = subprocess.run([sys.executable, "-B", os.path.join(d, "check_links.py"), "--db", FX, "--raw"],
                       capture_output=True, text=True)
    res[tag] = r.stdout
    r2 = subprocess.run([sys.executable, "-B", os.path.join(d, "check_links.py"), "--db", FX],
                        capture_output=True, text=True)
    print("%s checker rc=%d; BROKEN lines=%d; %s" % (tag, r.returncode, r.stdout.count("BROKEN\t"),
          [l for l in r2.stdout.splitlines() if "captures not judged" in l]))
print("%-18s %-7s %-7s %-7s  %s" % ("case", "expect", "pre", "post", "shape"))
hidden = 0
for tok, f, line, exp, desc in CASES:
    def rep(tag):
        toks = {tok, urllib.parse.unquote(tok)}   # post-fix prints the decoded target
        return any(l.startswith("BROKEN\t") and l.split("\t")[-1] in toks for l in res[tag].splitlines())
    pre, post = rep("pre"), rep("post")
    flag = "HIDDEN" if exp and not post else ("FALSE+" if post and not exp else "")
    hidden += flag == "HIDDEN"
    print("%-18s %-7s %-7s %-7s  %s %s" % (tok[:18], exp, pre, post, desc, flag))
print("real broken links the post-fix checker does not report: %d" % hidden)
