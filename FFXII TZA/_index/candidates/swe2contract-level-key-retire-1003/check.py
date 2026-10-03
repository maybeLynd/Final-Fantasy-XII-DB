#!/usr/bin/env python3
"""check.py - regression for retiring the contract front-matter key `level:` (FABLE ruling 2026-10-03, board note
rev 49820; applied by SWE2-CONTRACT). Reads the tree it runs in. Ends FAILS <n>.

  R1  no production contract (front-matter `contract:`, outside `_` folders) declares `level:` in its front matter;
  R2  _templates/CONTRACT.md has no `level:` key line and carries FABLE's one-line note;
  R3  knowledge_db.py's `contracts` and `reconstruction-ready` queries do not select `level`, and `level-census`
      excludes contracts;
  R4  the field-music contract's §16 carries the parity target its retired level comment held;
  S1  sensitivity: the R1 detector flags a synthetic contract that declares `level:` and passes one that does not,
      and it does not flag a non-contract page that declares one.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KD = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts", "knowledge_db.py"))
fails = 0


def check(name, ok, detail):
    global fails
    print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    fails += 0 if ok else 1


def front_matter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return text[:end] if end > 0 else None


def declares_level(text):
    fm = front_matter(text)
    return bool(fm and re.search(r"^contract:", fm, re.M) and re.search(r"^level:", fm, re.M))


contracts, offenders = 0, []
for root, dirs, files in os.walk(DB):
    rel = os.path.relpath(root, DB).replace("\\", "/")
    if rel != "." and any(s.startswith("_") for s in rel.split("/")):
        continue
    for f in files:
        if f.endswith(".md"):
            t = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            fm = front_matter(t)
            if fm and re.search(r"^contract:", fm, re.M):
                contracts += 1
                if declares_level(t):
                    offenders.append(os.path.join(rel, f))
check("R1 no contract declares level:", contracts >= 100 and not offenders,
      "%d contracts scanned, %d declare level: %s" % (contracts, len(offenders), offenders[:5]))

tp = open(os.path.join(DB, "_templates", "CONTRACT.md"), encoding="utf-8").read()
check("R2 template", not re.search(r"^level:", front_matter(tp) or "", re.M)
      and "Maturity is measured, never declared in front matter (FABLE ruling 2026-10-03)" in tp
      and "Caution on `level:`" not in tp, "level key absent, FABLE's line present, caution gone")

kd = open(KD, encoding="utf-8").read()


def query(name):
    m = re.search(r'"%s": \(True, """(.*?)"""' % re.escape(name), kd, re.S)
    return m.group(1) if m else ""


q1, q2, q3 = query("contracts"), query("reconstruction-ready"), query("level-census")
check("R3 knowledge_db queries", q1 and q2 and q3 and "level" not in q1 and "level" not in q2
      and "is_contract = 0" in q3, "contracts/reconstruction-ready select no level; level-census excludes contracts")

fm_page = open(os.path.join(DB, "18-Audio", "CONTRACT-field-music-selection.md"), encoding="utf-8").read()
s16 = fm_page[fm_page.index("## 16. Parity plan"):]
check("R4 field-music parity target in §16", "calculation parity only" in s16[:600]
      and "Integration is untested" in s16[:600], "carried as prose")

bad = "---\ncontract: x\nscope: family\nlevel: L1\n---\nbody\n"
good = "---\ncontract: x\nscope: family\n---\nbody\n"
page = "---\nsystem: y\nlevel: L1\n---\nbody\n"
check("S1 sensitivity", declares_level(bad) and not declares_level(good) and not declares_level(page),
      "synthetic contract with level flagged; without passes; non-contract page not judged")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
