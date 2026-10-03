"""ab_audit.py BASE - run audit_crossrefs.py as of commit BASE and as in the working tree on the same docs tree, both
read-only (the tripwire register is not rewritten), and report whether findings, neighbours and tripwires are identical
(OPUS, 2026-10-03; record opus-gate-speedup-1003).

Both copies run with __file__ = the kit path: load_functions applies the UC-1 band only for the kit copy, and a copy
loaded from elsewhere silently skips it (a first A/B here differed by exactly one UC-1 frontier body for that reason)."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))     # Database/
REPO = os.path.dirname(DB)
KIT = os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts")
GRAPH = os.path.join(DB, "Tools", "work", "graph")
DOCS = os.path.join(DB, "FFXII TZA")


def run(src, tag, tmp):
    sys.path.insert(0, KIT)
    spec = importlib.util.spec_from_file_location("audit_" + tag, src)
    m = importlib.util.module_from_spec(spec)
    m.__file__ = os.path.join(KIT, "audit_crossrefs.py")
    spec.loader.exec_module(m)
    m.write_tripwires = lambda *a, **k: None
    out = os.path.join(tmp, tag + ".json")
    old = sys.argv
    sys.argv = ["audit_crossrefs.py", "--docs", DOCS, "--functions", os.path.join(GRAPH, "functions.tsv"),
                "--edges", os.path.join(GRAPH, "edges.tsv"), "--json", out, "--out", out + ".md", "--quiet"]
    t = time.time()
    try:
        m.main()
    finally:
        sys.argv = old
    return json.load(open(out, encoding="utf-8")), time.time() - t


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    tmp = tempfile.mkdtemp(prefix="ab-audit-")
    old_src = os.path.join(tmp, "audit_base.py")
    blob = subprocess.run(["git", "-C", REPO, "show", base + ":Database/Tools/analysis-kit/gfz-scripts/audit_crossrefs.py"],
                          capture_output=True).stdout
    open(old_src, "wb").write(blob)
    a, ta = run(old_src, "base", tmp)
    b, tb = run(os.path.join(KIT, "audit_crossrefs.py"), "work", tmp)
    same = True
    for k in ("findings", "neighbours", "tripwires"):
        eq = a.get(k) == b.get(k)
        same &= eq
        print("%-10s %s  base %d  work %d" % (k, "SAME" if eq else "DIFF", len(a.get(k) or []), len(b.get(k) or [])))
    print("time base %.0fs  work %.0fs" % (ta, tb))
    print("EQUIVALENT" if same else "NOT EQUIVALENT")
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
