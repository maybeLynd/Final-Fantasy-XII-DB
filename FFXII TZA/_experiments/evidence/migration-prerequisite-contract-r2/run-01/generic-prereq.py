"""prereq.py - checked prerequisite results for controls that build on other controls (OPUS, 2026-09-29).

Workflow migration M1 1a (FF12-WORKFLOW-MIGRATION-20260928-01 section 6; acceptance matrix A03): "Required upstream
failures, nonzero exits, missing/malformed results, timeouts or dependency mismatches cannot become downstream PASS. A
legitimate smaller dependency contract must be explicit and separately validated."

Promoted from `_index/candidates/sn1-layouts/sn1_prereq.py` (reviewed; left unchanged so its acceptance holds). The
defect it exists for: a composer that runs another control with its exit swallowed (`except SystemExit: pass`, or
`sys.exit` rewritten away) and then uses the objects it built. The upstream control says FAIL; the composer says PASS.

    mod, why = prereq.run(path, argv, tags=..., names=..., exits=(0,), validate=None, line=LINE)

It runs `path` unchanged, in process, with `argv`, and returns (module, None) only when EVERY stated condition holds;
otherwise (None, reason). The caller prints the reason as a FAIL and stops before using the module.

  always       the file exists; it runs without raising (a syntax error or crash is a refusal); its exit code is in
               `exits` (a run that ends without sys.exit counts as exit 0, as the process would); it defines every
               name in `names`
  tags=(...)   A TAGGED CONTRACT - the full verdict is required: the output is only check lines matching `line`
               ('PASS  <tag> ...' by default) then exactly 'FAILS 0'; no FAIL line (a lying exit 0 is caught); the
               PASS tags are exactly `tags`, each once (a missing, extra or repeated check is a changed interface)
  tags=None    A DATA CONTRACT - the composer uses objects, not the verdict. This is the "smaller dependency
               contract" and must be explicit: name the exits you accept (e.g. (0, 1) where 1 means findings, not a
               broken run) and pass `validate(module) -> None | reason` that checks the objects you use are complete
  timeout      not enforced in process; a caller that needs one runs the control as a subprocess instead

`python prereq.py --self-test` runs test_prereq.py.
"""
import contextlib, importlib.util, io, os, re, sys

LINE = re.compile(r"^(PASS|FAIL)  (\S+)(?: |$)")


def run(path, argv, tags=None, names=(), exits=(0,), validate=None, line=LINE):
    if tags is None and validate is None and not names:
        raise ValueError("a data contract must name the objects it uses (names=) or validate them (validate=)")
    base = os.path.basename(path)
    if not os.path.isfile(path):
        return None, "missing: %s" % base
    spec = importlib.util.spec_from_file_location("prereq_" + re.sub(r"\W", "_", os.path.splitext(base)[0]), path)
    mod = importlib.util.module_from_spec(spec)
    saved, sys.argv = sys.argv, list(argv)
    buf, code = io.StringIO(), 0
    try:
        with contextlib.redirect_stdout(buf):
            spec.loader.exec_module(mod)
    except SystemExit as e:
        code = 0 if e.code is None else e.code
    except Exception as e:  # a prerequisite that cannot run is a refusal, never a pass
        return None, "%s raised %s: %s" % (base, type(e).__name__, e)
    finally:
        sys.argv = saved
    out = buf.getvalue().splitlines()
    # A FAILURE IS WHAT THE CONFIGURED LINE FORMAT SAYS IS ONE. This was only a literal `startswith("FAIL ")`, so a caller
    # passing a documented custom `line` (e.g. tab-separated) had its recognized FAIL lines read as neither pass nor
    # failure, and the composer passed on an upstream failure (ASTRA REJECT of A03, OPUS-REQ-ASTRA-VERIFY-A03-PREREQ,
    # 2026-09-29). The configured pattern's verdict group now decides; the literal prefixes stay as a floor.
    def _failed(l):
        m = line.match(l)
        return bool(m and m.group(1).upper() == "FAIL") or l.startswith(("FAIL ", "FAIL\t"))
    failed = [l[:100] for l in out if _failed(l)]
    if code not in exits:
        return None, "%s exit %r (accepted: %s)%s" % (base, code, list(exits), "; " + " | ".join(failed[:3]) if failed else "")
    if tags is not None:
        if not out or out[-1] != "FAILS 0":
            return None, "%s output does not end with 'FAILS 0' (last line %r)" % (base, out[-1][:60] if out else None)
        bad = [l[:60] for l in out[:-1] if not line.match(l)]
        if bad:
            return None, "%s output is malformed: %r" % (base, bad[:3])
        if failed:
            return None, "%s exited %r but printed FAIL lines: %s" % (base, code, " | ".join(failed[:3]))
        seen = [line.match(l).group(2) for l in out[:-1]]
        if sorted(seen) != sorted(tags):
            return None, "%s checks %s, expected exactly %s" % (base, seen, list(tags))
    miss = [n for n in names if not hasattr(mod, n)]
    if miss:
        return None, "%s does not define %s" % (base, miss)
    if validate is not None:
        try:
            why = validate(mod)
        except Exception as e:
            why = "validator raised %s: %s" % (type(e).__name__, e)
        if why:
            return None, "%s: %s" % (base, why)
    return mod, None


if __name__ == "__main__" and "--self-test" in sys.argv:
    import subprocess
    sys.exit(subprocess.call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_prereq.py")]))
