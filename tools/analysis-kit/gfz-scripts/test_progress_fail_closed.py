"""A dimension progress.py cannot compute must not become a quotable headline.

Run from the repo root:  python Database/Tools/analysis-kit/gfz-scripts/test_progress_fail_closed.py

WHY THIS TEST EXISTS, with the real failure it reproduces. `check_assets.evaluate()` gained a sixth
return value in `79510a96` and `progress.py` unpacked five. The `ValueError` was caught by an
`except Exception` whose comment read "never let a new dimension break the scorer", which printed a
one-line note and left `cov = tot = 0`. The scoring loop then folded a clean `0.0` into OVERALL at
full weight, and the project's headline read **46.69 %** when it was **51.49 %** - understated by
4.80 points, for as long as nobody read the line above the number.

**A crash is loud and costs a re-run. A silently understated headline gets quoted.** The scorer had
been trading the first for the second on purpose.

This test re-creates that exact shape - `evaluate()` returning one value too many - and asserts three
properties. Any one alone is not fail-closed:

  1. no OVERALL PERCENTAGE is printed, so there is no wrong number to quote;
  2. the broken dimension is named, with the weight it carries;
  3. THE EXIT CODE IS NON-ZERO, because that is the only thing an automated chain can check.

Property 3 is here because the first version of the fix printed the refusal and then `return 0`,
which a chain would have read as success. A refusal that exits 0 is not a refusal.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DB = "Database/FFXII TZA"

SHIM = '''
import sys, runpy
sys.path.insert(0, r"{kit}")
import check_assets
_real = check_assets.evaluate
def _broken(*a, **k):
    return tuple(_real(*a, **k)) + ("EXTRA",)   # the 79510a96 shape: one value too many
check_assets.evaluate = _broken
sys.argv = ["progress.py", "--db", r"{db}"]
runpy.run_path(r"{prog}", run_name="__main__")
'''.format(kit=HERE, db=DB, prog=os.path.join(HERE, "progress.py"))


def main():
    fd, path = tempfile.mkstemp(suffix=".py", text=True)
    os.close(fd)
    open(path, "w", encoding="utf-8").write(SHIM)
    try:
        r = subprocess.run([sys.executable, path], cwd=ROOT, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
    finally:
        os.unlink(path)

    out = r.stdout + r.stderr
    fails = []

    headline = [l for l in out.splitlines() if l.strip().startswith("OVERALL")]
    if headline and "UNAVAILABLE" not in headline[0]:
        fails.append("OVERALL printed a percentage: %r" % headline[0].strip()[:80])
    if not headline:
        fails.append("OVERALL line absent entirely - expected an explicit UNAVAILABLE")
    if "REFUSING TO PRINT A HEADLINE" not in out:
        fails.append("no refusal banner naming what could not be computed")
    if "UNAVAIL" not in out:
        fails.append("the broken dimension was not marked UNAVAIL in its own row")
    if r.returncode == 0:
        fails.append("EXIT 0 - a refusal that exits success is not a refusal")

    print("progress.py with a deliberately broken dimension: exit %d" % r.returncode)
    for l in out.splitlines():
        if "OVERALL" in l or "REFUSING" in l or "UNAVAIL" in l:
            print("   %s" % l.strip()[:112])

    # SEPARABILITY, added 2026-09-16 on AUDITSEM-CONTRA-OPUS-SCORER-EXIT-SEPARABILITY.
    # The exit code promises that a BROKEN dimension (3) is distinguishable from a PROVENANCE
    # WARNING (2). That promise was false for as long as it existed, because the warn block
    # returned first and a warning is always present at HEAD - so the case the contract was
    # written for was the one case it did not cover. This asserts the property rather than the
    # code path, so a future reordering fails here instead of silently at a caller.
    warned = "PROVENANCE WARNING" in out
    if warned and r.returncode != 3:
        fails.append("a broken dimension exited %d WITH a provenance warning present - "
                     "3 must outrank 2, or the codes are not separable" % r.returncode)
    if not warned:
        print("   (no provenance warning in this run - the separability case did not arise)")
    else:
        print("   separability: broken + warning -> exit %d (3 required)" % r.returncode)

    if fails:
        print("")
        print("FAILED:")
        for f in fails:
            print("   - %s" % f)
        return 1
    print("")
    print("PASSED: no headline exists to be quoted, the dimension is named, exit is non-zero,")
    print("and a broken dimension outranks a provenance warning.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
