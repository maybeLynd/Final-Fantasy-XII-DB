"""rename_check.py [--root REPO] - regression for FABLE family ruling R4 (SWE2-EC7, 2026-09-29).

The generated-family row formerly named CxxObjectLifecycle.ConditionalTeardownReturnTrue is renamed
Phyre.PClassDescriptorConcrete.PlacementCtorConditionalReturnTrue, and the "destroy" reading of its bodies is
corrected on the object-construction page. This check FAILS on the old reading, so it rejects a regression:

  R1  no function_families row is named with the old name; exactly one row carries the new name, and
      check_dispositions accepts it with its declared count;
  R2  every member of that row is RTTI-exclusive slot 10 (+0x50) of a Phyre::PClassDescriptorConcrete<T> vtable
      (rtti/methods.tsv) - the fact the rename rests on;
  R3  all 28 bodies carrying the GFZ tag of the old name are slot 10 of a Phyre class-descriptor vtable
      (PClassDescriptorConcrete or PClassDescriptorWithoutDefaultConstructor) - the population the BQ-25
      section describes;
  R4  outside history (_experiments/, _index/_inbox/, _index/candidates/) every line of a database page that
      names the old family name either carries a strike (~~) or says it was renamed;
  R5  the object-construction page states the "conditional destroy-and-report-success virtual" reading only
      struck, and names slot 10 of the class descriptor.

Control: run with --root on a checkout before the rename (a clean HEAD extract) and it must FAIL R1 and R5.
Prints one line per check and "FAILS n"; exit 1 when n > 0.
"""
import argparse, collections, csv, io, os, re, sys

OLD = "CxxObjectLifecycle.ConditionalTeardownReturnTrue"
NEW = "Phyre.PClassDescriptorConcrete.PlacementCtorConditionalReturnTrue"
ap = argparse.ArgumentParser()
ap.add_argument("--root", default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                               "..", "..", "..", "..", "..")))
a = ap.parse_args()
ROOT = a.root
DB = os.path.join(ROOT, "Database", "FFXII TZA")
WORK = os.path.join(r"C:\Users\Kristian\source\repos\XIIOnline", "Database", "Tools", "work")  # gitignored inputs
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as CD

fails = []
def check(name, ok, detail):
    print("%-3s %s  %s" % (name, "ok  " if ok else "FAIL", detail))
    if not ok:
        fails.append(name)

rows = CD.parse_families(DB)
old_rows = [(d, p) for d, p in rows if p and p[0].strip() == OLD]
new_rows = [(d, p) for d, p in rows if p and p[0].strip() == NEW]
sizes = CD.load_functions()
r = CD.evaluate(DB, sizes)
acc = {}
for x in r.get("accepted", []):
    try:
        acc[x[0]] = x
    except Exception:
        pass
acc_names = set()
for x in r.get("accepted", []):
    s = x[0] if isinstance(x, (list, tuple)) else str(x)
    acc_names.add(s)
members = []
if len(new_rows) == 1:
    d, p = new_rows[0]
    members = CD.read_members(d, p[2])
new_acc = any(NEW in str(s) for s in acc_names)
check("R1", not old_rows and len(new_rows) == 1 and new_acc and len(members) == int(new_rows[0][1][3]) if new_rows else False,
      "old-name rows %d, new-name rows %d, accepted %s, members %d" % (len(old_rows), len(new_rows), new_acc, len(members)))

app = collections.defaultdict(list)
for row in csv.DictReader(open(os.path.join(WORK, "rtti", "methods.tsv"), encoding="utf-8", errors="replace"), delimiter="\t"):
    try:
        app[int(row["address"], 16)].append((row["class"], row["slot"]))
    except (ValueError, TypeError):
        pass
def slot10(m, templates):
    ap_ = app.get(m, [])
    return bool(ap_) and all(s == "10" and c.startswith(templates) for c, s in ap_)
bad = [m for m in members if not slot10(m, ("Phyre::PClassDescriptorConcrete<",))]
check("R2", bool(members) and not bad, "%d members, %d not RTTI-exclusive PClassDescriptorConcrete slot 10 %s" % (
    len(members), len(bad), ["%08X" % m for m in bad[:3]]))

tagged = [int(l.split("\t", 1)[0], 16) for l in open(os.path.join(WORK, "graph", "functions.tsv"), encoding="utf-8", errors="replace")
          if ("GFZ.V121.CodeDomain." + OLD) in l.split("\t")[-1]]
k = collections.Counter(("Concrete" if slot10(t, ("Phyre::PClassDescriptorConcrete<",)) else
                         "WithoutDefaultConstructor" if slot10(t, ("Phyre::PClassDescriptorWithoutDefaultConstructor<",)) else "other")
                        for t in tagged)
check("R3", len(tagged) == 28 and k["other"] == 0, "%d GFZ-tagged bodies: %s" % (len(tagged), dict(k)))

offenders = []
for p in CD.docs(DB):
    rel = os.path.relpath(p, DB).replace("\\", "/")
    if rel.startswith(("_experiments/", "_index/_inbox/", "_index/candidates/")):
        continue
    t = io.open(p, encoding="utf-8", errors="replace").read()
    if OLD not in t:
        continue
    for n, line in enumerate(t.splitlines(), 1):
        if OLD in line and "~~" not in line and not re.search(r"\brenamed\b", line, re.I):
            offenders.append("%s:%d" % (rel, n))
check("R4", not offenders, "unannotated old-name lines outside history: %d %s" % (len(offenders), offenders[:3]))

OC = os.path.join(DB, "24-Compiler-And-CRT-Runtime", "Cxx-Runtime-Families", "object-construction-destruction-and-static-lifetime.md")
t = io.open(OC, encoding="utf-8", errors="replace").read()
claim = re.compile(r"conditional\s+destroy-and-report-success\s+virtual")
spans = [(m.start(), m.end()) for m in re.finditer(r"~~[^~]+~~", t)]
unstruck = [m.start() for m in claim.finditer(t) if not any(a <= m.start() < b for a, b in spans)]
names_slot = bool(re.search(r"slot 10 \(`?\+0x50`?\)", t))
check("R5", not unstruck and names_slot, "unstruck destroy reading %d, page names slot 10 (+0x50): %s" % (len(unstruck), names_slot))

print("FAILS %d" % len(fails))
sys.exit(1 if fails else 0)
