#!/usr/bin/env python3
"""check.py - regression for retiring `level:` from every page's front matter (FABLE ruling rev 49820, extended to
non-contract pages; applied by SWE2-CONTRACT 2026-10-03). Reads the tree it runs in. Ends FAILS <n>.

  P1  no .md page outside the `_` folders declares `level:` in its front matter (contracts and other pages alike);
  S1  sensitivity: the detector flags a synthetic page that declares `level:` in front matter, and ignores a body
      line `level: L1` below the front matter.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
fails = 0


def check(name, ok, detail):
    global fails
    print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    fails += 0 if ok else 1


def declares(text):
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    return end > 0 and re.search(r"^level:", text[:end], re.M) is not None


pages, offenders = 0, []
for root, dirs, files in os.walk(DB):
    rel = os.path.relpath(root, DB).replace("\\", "/")
    if rel != "." and any(s.startswith("_") for s in rel.split("/")):
        continue
    for f in files:
        if f.endswith(".md"):
            pages += 1
            if declares(open(os.path.join(root, f), encoding="utf-8", errors="replace").read()):
                offenders.append(rel + "/" + f)
check("P1 no page declares level:", pages > 500 and not offenders,
      "%d pages scanned, %d declare level: %s" % (pages, len(offenders), offenders[:5]))
check("S1 sensitivity", declares("---\nsystem: x\nlevel: L1\n---\nbody\n")
      and not declares("---\nsystem: x\n---\nlevel: L1\n"), "front-matter key flagged; body line ignored")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
