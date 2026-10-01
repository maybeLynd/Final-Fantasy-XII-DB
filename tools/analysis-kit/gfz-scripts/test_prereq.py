"""test_prereq.py - valid and rejected prerequisites through prereq.run, plus a composer run through its actual entry
point (a subprocess), for acceptance-matrix A03 (OPUS, 2026-09-29). Disposable fixtures only.

  T1..T9   the tagged contract: valid; FAIL + exit 1; lying exit 0 with a FAIL line; malformed line; extra tag; missing
           tag; missing file; crash; missing name
  D1..D5   the data contract: exit 1 accepted when named (findings); exit 2 rejected; crash rejected; validator rejects
           incomplete data; a contract naming nothing is refused by the API
  C1..C2   a composer script built on prereq.run, run as a subprocess: its prerequisite valid -> exit 0 and PASS;
           the prerequisite changed 127 -> 126 in its count check -> the composer exits 1 with FAIL and never prints PASS
"""
import os, subprocess, sys, tempfile, textwrap
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import prereq  # noqa: E402
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
D = tempfile.mkdtemp(prefix="prereq_")
def script(name, body):
    p = os.path.join(D, name); open(p, "w", encoding="utf-8").write(textwrap.dedent(body)); return p
TAGGED = """
import sys
fails = 0
COUNT = 127
def check(t, ok):
    global fails
    fails += not ok; print("%s  %s x" % ("PASS" if ok else "FAIL", t))
check("A", COUNT == 127)
check("B", True)
DATA = {"n": COUNT}
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
"""
ok = script("ok.py", TAGGED)
r = lambda p, **k: prereq.run(p, [p], **k)
m, why = r(ok, tags=("A", "B"), names=("DATA",)); check("T1", m is not None and why is None and m.DATA["n"] == 127, "valid: %s" % why)
m, why = r(script("f.py", TAGGED.replace("COUNT = 127", "COUNT = 126")), tags=("A", "B")); check("T2", m is None and "exit 1" in why, why)
m, why = r(script("lie.py", TAGGED.replace("COUNT = 127", "COUNT = 126").replace('print("FAILS %d" % fails)\nsys.exit(1 if fails else 0)', 'print("FAILS 0")\nsys.exit(0)')), tags=("A", "B"))
check("T3", m is None and "printed FAIL" in why, why)
m, why = r(script("mal.py", TAGGED.replace('check("B", True)', 'check("B", True)\nprint("note")')), tags=("A", "B")); check("T4", m is None and "malformed" in why, why)
m, why = r(script("extra.py", TAGGED.replace('check("B", True)', 'check("B", True)\ncheck("C", True)')), tags=("A", "B")); check("T5", m is None and "expected exactly" in why, why)
m, why = r(ok, tags=("A", "B", "C")); check("T6", m is None and "expected exactly" in why, why)
m, why = r(os.path.join(D, "nope.py"), tags=("A",)); check("T7", m is None and why.startswith("missing"), why)
m, why = r(script("crash.py", "x = 1/0\n"), tags=("A",)); check("T8", m is None and "ZeroDivisionError" in why, why)
m, why = r(ok, tags=("A", "B"), names=("NOPE",)); check("T9", m is None and "does not define" in why, why)
DATAS = """
import sys
CENSUS = {1: 2, 3: 4}
print("2 disagreements")
sys.exit(%d)
"""
m, why = r(script("d1.py", DATAS % 1), exits=(0, 1), names=("CENSUS",), validate=lambda mm: None if mm.CENSUS else "empty CENSUS")
check("D1", m is not None and m.CENSUS == {1: 2, 3: 4}, "exit 1 (findings) accepted by an explicit data contract: %s" % why)
m, why = r(script("d2.py", DATAS % 2), exits=(0, 1), names=("CENSUS",)); check("D2", m is None and "exit 2" in why, why)
m, why = r(script("d3.py", "CENSUS = {}\nraise RuntimeError('half built')\n"), exits=(0, 1), names=("CENSUS",)); check("D3", m is None and "RuntimeError" in why, why)
m, why = r(script("d4.py", "CENSUS = {}\n"), exits=(0, 1), names=("CENSUS",), validate=lambda mm: None if mm.CENSUS else "empty CENSUS")
check("D4", m is None and "empty CENSUS" in why, why)
try:
    prereq.run(ok, [ok]); refused = False
except ValueError:
    refused = True
check("D5", refused, "a data contract that names nothing is refused")
COMPOSER = """
import os, sys
sys.path.insert(0, %r)
import prereq
up = os.path.join(os.path.dirname(os.path.abspath(__file__)), "up.py")
m, why = prereq.run(up, [up], tags=("A", "B"), names=("DATA",))
if why:
    print("FAIL  P prerequisite: " + why); print("FAILS 1"); sys.exit(1)
print("PASS  P prerequisite clean; n = %%d" %% m.DATA["n"]); print("FAILS 0"); sys.exit(0)
""" % HERE
for tag, body, want in (("C1", TAGGED, 0), ("C2", TAGGED.replace("COUNT = 127", "COUNT = 126"), 1)):
    sub = tempfile.mkdtemp(prefix="prereq_c_", dir=D)
    open(os.path.join(sub, "up.py"), "w", encoding="utf-8").write(textwrap.dedent(body))
    open(os.path.join(sub, "composer.py"), "w", encoding="utf-8").write(textwrap.dedent(COMPOSER))
    p = subprocess.run([sys.executable, os.path.join(sub, "composer.py")], capture_output=True, text=True)
    good = p.returncode == want and (("PASS  P" in p.stdout) == (want == 0)) and (("FAIL  P" in p.stdout) == (want == 1))
    check(tag, good, "composer exit %d (want %d): %s" % (p.returncode, want, p.stdout.strip().splitlines()[0] if p.stdout.strip() else p.stderr[-120:]))
# C3/C4 (ASTRA's A03 REJECT, 2026-09-29): a documented CUSTOM line format, run through the actual composer subprocess.
# The upstream prints a tab-separated FAIL, then a lying 'FAILS 0' and exit 0; the composer must refuse (exit 1, no PASS).
# The same format's PASS positive must still compose.
TAB = r"^(PASS|FAIL)\t(\S+)(?:\t|$)"
TABBED = """
import sys
DATA = {"n": 127}
print("%s\\tA\\trequired check")
print("PASS\\tB\\tother check")
print("FAILS 0")
sys.exit(0)
"""
COMPOSER_TAB = COMPOSER.replace('tags=("A", "B"), names=("DATA",))', 'tags=("A", "B"), names=("DATA",), line=re.compile(%r))' % TAB).replace(
    "import os, sys", "import os, re, sys")
for tag, verdict, want in (("C3", "FAIL", 1), ("C4", "PASS", 0)):
    sub = tempfile.mkdtemp(prefix="prereq_t_", dir=D)
    open(os.path.join(sub, "up.py"), "w", encoding="utf-8").write(textwrap.dedent(TABBED % verdict))
    open(os.path.join(sub, "composer.py"), "w", encoding="utf-8").write(textwrap.dedent(COMPOSER_TAB))
    p = subprocess.run([sys.executable, os.path.join(sub, "composer.py")], capture_output=True, text=True)
    good = p.returncode == want and (("PASS  P" in p.stdout) == (want == 0)) and (("FAIL  P" in p.stdout) == (want == 1))
    check(tag, good, "custom tab format, upstream %s: composer exit %d (want %d): %s" % (
        verdict, p.returncode, want, p.stdout.strip().splitlines()[0] if p.stdout.strip() else p.stderr[-160:]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
