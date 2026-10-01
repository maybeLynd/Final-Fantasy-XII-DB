"""SWE2-AUDIT-SEM attack on documented_rule.py condition T (86ba479ef): does cited_untracked() see every evidence-path
form the register uses, and avoid false hits? Imports the producer's functions (the code under review) and feeds them
(a) synthetic cells for each path form, (b) the live register, comparing with my own independent extraction."""
import os, re, sys, io, subprocess, collections
HERE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\status-currency-ruling-fable"
sys.path.insert(0, HERE)
import documented_rule as D
DB = D.DB
tracked = D.tracked_paths()
print("tracked paths under _index/candidates + _experiments:", len(tracked))
real = next(p for p in sorted(tracked) if p.startswith("_index/candidates/") and p.count("/") >= 3)
rdir = real.rsplit("/", 1)[0]
cases = [
    ("backticked full", "`%s`" % real, False),
    ("bare dir with slash", "see %s/ for it" % rdir, False),
    ("bare dir no slash", "see %s." % rdir, False),
    ("short candidates/", "(%s)" % real.replace("_index/", ""), False),
    ("markdown link ../", "[r](../%s)" % real.replace("_index/", ""), False),
    ("Database/FFXII TZA prefix", "`Database/FFXII TZA/%s`" % real, False),
    ("ghost dir", "`_index/candidates/zz-ghost-0000/`", True),
    ("ghost file", "`_index/candidates/zz-ghost-0000/x.py`", True),
    ("Tools/work record (gitignored)", "`Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-30-takebacks2.md`", True),
    ("_experiments non-evidence path", "`_experiments/EXP-999-ghost.md`", True),
    ("brace-expansion form", "`_index/candidates/auditsem-review-{rc-residue,rc22-34}-0930/`", False),
    ("dir with a dot in its name", "`_index/candidates/v1.2-ghost`", True),
    ("prose 'candidates/'", "the candidates/ folder", False),
]
for name, cell, expect_bad in cases:
    bad = D.cited_untracked(cell, tracked)
    ok = bool(bad) == expect_bad
    print("%-4s %-34s flagged=%s %s" % ("OK" if ok else "MISS", name, bool(bad), bad))
# live register: my own extraction of every evidence-looking path, then track check
t = io.open(os.path.join(DB, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8", errors="replace").read()
rows = re.findall(r"^\|\s*([A-Z][A-Za-z0-9/\-]*)\s*\|(.*)$", t, re.M)
forms = collections.Counter()
examples = collections.defaultdict(list)
for rid, cell in rows:
    for m in re.finditer(r"Tools/work/[^\s`)|,]+", cell):
        forms["Tools/work"] += 1; examples["Tools/work"].append((rid, m.group(0)))
    for m in re.finditer(r"_index/candidates/[^\s`)|,]*\{", cell):
        forms["brace"] += 1; examples["brace"].append((rid, m.group(0)))
    for m in re.finditer(r"_experiments/(?!evidence/)[^\s`)|,]+", cell):
        forms["_experiments non-evidence"] += 1; examples["_experiments non-evidence"].append((rid, m.group(0)))
print("live register rows:", len(rows), "path forms outside T's pattern:", dict(forms))
for k, v in examples.items():
    print("  %s e.g. %s" % (k, v[:4]))
st = D.evidence_status()
print("T on the live register now: %d rows with untracked evidence %s" % (len(st), sorted(st)[:10]))
