"""qid_gap.py - FABLE measurement (2026-09-30): question-ID references the two green checkers do not cover.
(A) front-matter `status:` lines and checkbox lines citing an id-shaped token XX-N whose prefix the register uses but
    whose exact id has no register row;
(B) TICKED checkboxes that carry no register id at all (nothing ties their closure to a row).
Positive control: a synthetic line with an unregistered GR-999 must be flagged by (A)."""
import io, os, re, sys, collections
import os as _o; DB = _o.path.normpath(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "..", ".."))
DB = _o.path.dirname(DB)
reg = io.open(os.path.join(DB, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8").read()
ids = set(re.findall(r"^\| ([A-Z][A-Z0-9]{0,6}-\d{1,4}[a-z]?) \|", reg, re.M))
prefixes = collections.Counter(i.split("-")[0] for i in ids)
TOK = re.compile(r"(?<![A-Za-z0-9_/-])([A-Z][A-Z0-9]{0,6})-(\d{1,4}[a-z]?)(?![0-9A-Za-z])")
def unreg(line):
    out = []
    for p, n in TOK.findall(line):
        if prefixes.get(p, 0) >= 3 and "%s-%s" % (p, n) not in ids: out.append("%s-%s" % (p, n))
    return out
assert unreg("- [x] closes GR-999 (control)") == ["GR-999"], "control failed"
A, B = [], []
skip = ("_experiments", "_inbox", "candidates", "progress", "_types", "AUDIT-LOG", "ADDRESS-INDEX", "OPEN-QUESTIONS")
for root, dirs, files in os.walk(DB):
    dirs[:] = [d for d in dirs if d not in ("_experiments", "_inbox", "candidates", "progress", "_types", "archive")]
    for fn in files:
        if not fn.endswith(".md") or any(s in fn for s in skip): continue
        p = os.path.join(root, fn); rel = os.path.relpath(p, DB)
        for ln, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
            s = line.strip()
            isbox = re.match(r"^[-*] \[[ xX]\]", s)
            if s.startswith("status:") or isbox:
                for u in unreg(s): A.append((rel, ln, u, s[:110]))
            if isbox and s[3] in "xX":
                if not any("%s-%s" % t in ids for t in TOK.findall(s)): B.append((rel, ln, s[:110]))
print("register ids: %d, prefixes used >=3 times: %d" % (len(ids), sum(1 for v in prefixes.values() if v >= 3)))
print("(A) unregistered ids in status/box lines: %d (distinct %d)" % (len(A), len(set(a[2] for a in A))))
for a in A[:60]: print("  %s:%d  %s  | %s" % a)
print("(B) ticked boxes with no register id: %d in %d files" % (len(B), len(set(b[0] for b in B))))
for b in B[:25]: print("  %s:%d | %s" % b)
