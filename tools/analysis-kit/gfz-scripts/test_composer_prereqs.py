"""test_composer_prereqs.py - the two composers' explicit prerequisite contracts, through their own entry points
(OPUS, 2026-09-29; FRONTIER-REQ-OPUS-COMPOSER-PREREQ-REPAIRS; matrix A03). Each composer runs as a subprocess; its
prerequisite is redirected to a broken scratch copy through the composer's documented override variable.

check_gap_debt.py (data contract: import exit 0, CENSUS a non-empty dict)
  G0  valid: the real check_census_widths.py -> the composer's normal report ("DECLARED GAP ROWS"), no PREREQUISITE FAILED
  G1  the prerequisite exits 2 at import           -> composer exit 2, PREREQUISITE FAILED, no report
  G2  CENSUS half-built (an empty dict)            -> exit 2, PREREQUISITE FAILED
  G3  the prerequisite raises at import            -> exit 2, PREREQUISITE FAILED
check_route_collisions_control.py (data contract: exits 0/1, contained() callable)
  R0  valid: the real check_route_span_overlaps.py -> exit 0, CONTROL PASSES
  R1  the prerequisite exits 2                     -> exit 2, PREREQUISITE FAILED, no CONTROL line
  R2  exit 1 (findings) with contained() present   -> accepted: the control runs its cases (a findings exit is not broken)
  R3  contained() missing                          -> exit 2, PREREQUISITE FAILED
"""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0
def check(tag, ok, text=""):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
T = tempfile.mkdtemp(prefix="cpq_")
def broken(name, body):
    p = os.path.join(T, name); open(p, "w", encoding="utf-8").write(body); return p
def run(script, var=None, src=None):
    env = dict(os.environ)
    if var: env[var] = src
    r = subprocess.run([sys.executable, os.path.join(HERE, script)], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=900)
    return r.returncode, r.stdout
V = "GAP_DEBT_CENSUS_SOURCE"
rc, out = run("check_gap_debt.py")
check("G0", "DECLARED GAP ROWS" in out and "PREREQUISITE FAILED" not in out, "valid: exit %d with its report" % rc)
for tag, body in (("G1", "import sys\nsys.exit(2)\n"), ("G2", "CENSUS = {}\n"), ("G3", "CENSUS = {'a': 1}\nraise RuntimeError('half way')\n")):
    rc, out = run("check_gap_debt.py", V, broken(tag + ".py", body))
    check(tag, rc == 2 and "PREREQUISITE FAILED" in out and "DECLARED GAP ROWS" not in out, "exit %d: %s" % (rc, out.strip().splitlines()[-1][:110] if out.strip() else ""))
V = "ROUTE_OVERLAPS_SOURCE"
rc, out = run("check_route_collisions_control.py")
check("R0", rc == 0 and "CONTROL PASSES" in out, "valid: exit %d" % rc)
real = open(os.path.join(HERE, "check_route_span_overlaps.py"), encoding="utf-8").read()
cases = (("R1", "import sys\nsys.exit(2)\n", 2, False),
         ("R2", real.replace("sys.exit(1 if overlap else 0)", "sys.exit(1)"), 0, True),
         ("R3", real.replace("def contained(", "def _renamed_contained("), 2, False))
for tag, body, want, runs in cases:
    if tag != "R1" and body == real:
        check(tag, False, "ERROR: the fixture edit did not apply"); continue
    rc, out = run("check_route_collisions_control.py", V, broken(tag + ".py", body))
    ok = rc == want and (("CONTROL PASSES" in out) == runs) and (("PREREQUISITE FAILED" in out) == (not runs))
    check(tag, ok, "exit %d: %s" % (rc, out.strip().splitlines()[-1][:110] if out.strip() else ""))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
