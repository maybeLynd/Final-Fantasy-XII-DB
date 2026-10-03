"""SWE2-DATA review of recent_changes.py (a065b24fa): rule-logic mutations. Each mutated copy is compiled under the live
path (so its imports resolve) and its --self-test must FAIL. Nothing in the repository is written."""
import io, os, subprocess, sys, tempfile
KIT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts"
SRC = open(os.path.join(KIT, "recent_changes.py"), encoding="utf-8").read()
MUTS = [
    ("M0 unmutated (harness control, must PASS)", "def path_category(p):", "def path_category(p):"),
    ("M1 correction without a strike", "if aff != old_aff and struck_correction(repo, c, ctx):", "if aff != old_aff:"),
    ("M2 undated register lead credited", 'ev.append((KNOWN_TARGET[n[0]] if n[1] else "register-undated", rid, detail))',
     'ev.append((KNOWN_TARGET[n[0]], rid, detail))'),
    ("M3 coverage without a knowledge event", "if knowledge and cat in COVERABLE:", "if cat in COVERABLE:"),
    ("M4 repeat acceptance counted as first", "if prior_acceptance(repo, parent, rec, ctx):", "if False:"),
    ("M5 rule f ignores strikes", "and not dir_events \\\n                and not struck_correction(repo, c, ctx):", "and not dir_events:"),
    ("M6 later-accepted record counted unreviewed", "if acc and acc[0] >= c[\"ct\"]:", "if False:"),
    ("M7 rule f without a page section", "            if pages_with_section:\n                emit(\"page-section-record\"",
     "            if True:\n                emit(\"page-section-record\""),
]
HARNESS = r'''
import sys, types
KIT = %r
sys.path.insert(0, KIT)
src = open(sys.argv[1], encoding="utf-8").read()
m = types.ModuleType("recent_changes"); m.__file__ = KIT + r"\recent_changes.py"; sys.modules["recent_changes"] = m; m.__dict__["__name__"] = "__main__"
sys.argv = [m.__file__, "--self-test"]
exec(compile(src, m.__file__, "exec"), m.__dict__)
'''
py = sys.executable
tmp = tempfile.mkdtemp()
h = os.path.join(tmp, "h.py"); open(h, "w").write(HARNESS % KIT)
for name, old, new in MUTS:
    n = SRC.count(old)
    if n != 1:
        print("SKIP %-45s anchor found %d times" % (name, n)); continue
    f = os.path.join(tmp, "m.py"); open(f, "w", encoding="utf-8").write(SRC.replace(old, new))
    r = subprocess.run([py, "-B", h, f], capture_output=True, text=True, cwd=KIT, timeout=900)
    out = r.stdout + r.stderr
    fails = [l.strip() for l in out.splitlines() if l.strip().startswith("FAIL ")]
    tail = [l for l in out.splitlines() if l.startswith("FAILS")]
    print("%-45s rc=%d %s %s" % (name, r.returncode, tail[-1] if tail else "", "| " + fails[0][:70] if fails else ""))
