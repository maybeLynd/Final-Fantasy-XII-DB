"""Offline dry run of publish_correction_gate's text rules on apply.py's planned edits (no git diff, no repo writes).

Builds each planned page's unified diff with difflib (git's hunk shape), then runs the gate's own
find_correction_hunks / EXEC_CLAIM / strike-provenance rule, and its record regexes on consumer-check.md.
"""
import difflib, io, os, re, sys
KIT = r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts"
sys.path.insert(0, KIT)
sys.path.insert(0, r"C:/x/p22/drafts")
import publish_correction_gate as g
import apply as ap

ROOT = r"C:/x/p22b"
HEAD_ROOT = r"C:/Users/Kristian/source/repos/XIIOnline"
problems = []
exec_hits = []
for rel, draft, last in ap.EDITS:
    page = ap.load_page(ROOT, HEAD_ROOT, rel, problems)
    p = ap.plan_page(rel, draft, last, r"C:/x/p22/drafts", page, problems)
    old, new = p["diff"]
    diff = "\n".join(difflib.unified_diff(old.split("\n"), new.split("\n"), "a/" + rel, "b/" + rel, n=3, lineterm=""))
    hits = g.find_correction_hunks(diff)
    removed = g._norm(" ".join(l[1:] for l in diff.splitlines()
                               if l.startswith("-") and not l.startswith("---"))).replace("**", "")
    unq = [m.group(1) for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")
           for m in re.finditer(r"~~(.+?)~~", l)
           if len(g._norm(m.group(1))) > 8 and g._norm(m.group(1)).replace("**", "") not in removed]
    ex = [a for _, added in hits for a in added if g.EXEC_CLAIM.search(a)]
    exec_hits += ex
    print("%-90s correction hunks %d, unquoted strikes %d, exec-claim lines in correction hunks %d"
          % (rel[-90:], len(hits), len(unq), len(ex)))
    for a in ex:
        print("    EXEC:", a[:140])
print("problems:", problems)
rec = io.open(r"C:/x/p22/drafts/consumer-check.md", encoding="utf-8").read()
print("record: consumer word %s, agreement token %s, AFFECTED match %s, pending/routed %s"
      % (bool(re.search("consumer", rec, re.I)), bool(g.AGREE.search(rec)), bool(g.AFFECTED.search(rec)),
         g.record_pending(rec)))
decl = set()
for m in re.finditer(r"(?im)^.*\baffected\b[^\n]*", rec):
    for p in re.finditer(r"[\w./\\-]+\.(?:md|tsv)", m.group(0)):
        decl.add(p.group(0))
    if g.EXEC_CLAIM.search(m.group(0)):
        print("  EXEC on affected line:", m.group(0)[:120])
touched = {"Database/FFXII TZA/" + r for r, _, _ in ap.EDITS} | {"Database/FFXII TZA/" + ap.RECORD}
names = {t.rsplit("/", 1)[-1] for t in touched}
for d in sorted(decl):
    ok = d in touched or d.rsplit("/", 1)[-1] in names or any(t.endswith("/" + d) for t in touched)
    print("  declared %-100s %s" % (d[-100:], "touched" if ok else "NOT TOUCHED -> gate would refuse"))
print("receipt tokens:", [m.group(1) for m in g.RECEIPT.finditer(rec)])
print("exec_needed (correction hunks):", bool(exec_hits))
