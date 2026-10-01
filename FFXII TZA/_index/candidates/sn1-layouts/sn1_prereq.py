"""sn1_prereq.py - OPUS (Claude Opus 5.5), 2026-09-28. The SN-1 controls' prerequisite interface
(FRONTIER-REQ-OPUS-SN1-NEITHER-PARTITION-PREREQ).

A control that builds on another control's objects must not certify on that control's failure. Until 2026-09-28,
sn1_neither_partition.py ran sn1_variable_binding.py with its sys.exit disabled and its output discarded, and
sn1_variable_binding.py swallowed sn1_q0_domain.py's SystemExit. A failed prerequisite therefore still produced a green
downstream run: with mapctrl's T0 count edited 127 -> 126 in the producer's check T, the producer said FAILS 1 / exit 1
and the wrapper said FAILS 0 / exit 0.

run(path, argv, tags, names) runs the prerequisite UNCHANGED, in process, and returns (module, None) only when ALL hold:
  - the file exists;
  - it runs to its own sys.exit without raising anything else (a syntax error or a crash is a refusal);
  - the exit code is 0;
  - its output is well formed: every line is 'PASS  <tag> ...' or 'FAIL  <tag> ...', and the last line is exactly
    'FAILS 0';
  - it printed no FAIL line, and its PASS tags are exactly `tags`, each once. A missing, extra or repeated check is a
    changed interface: it is refused rather than guessed at;
  - it defines every attribute in `names`.
`line` is the check-line pattern (group 1 PASS/FAIL, group 2 the tag). The default is the SN-1 controls' own
'PASS  <tag> ...' form; a caller running a control with another fixed form (e.g. FABLE's 'PASS <tag>  ...') passes that
form explicitly (sn1-x-oeb-package, 2026-09-28). It never relaxes the other conditions.
Otherwise it returns (None, reason). The caller reports the reason as a FAIL and stops before computing anything from
the prerequisite's objects. The check is on the prerequisite's whole result, not a chosen subset: the callers use
objects that its tables, samples and q0 lookup build, so no narrower dependency set has been justified.
"""
import contextlib, importlib.util, io, os, re, sys

LINE = re.compile(r"^(PASS|FAIL)  (\S+)(?: |$)")


def run(path, argv, tags, names, line=LINE):
    if not os.path.isfile(path):
        return None, "missing: %s" % os.path.basename(path)
    name = "sn1prereq_" + re.sub(r"\W", "_", os.path.splitext(os.path.basename(path))[0])
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    saved, sys.argv = sys.argv, list(argv)
    buf, code = io.StringIO(), "no sys.exit"
    try:
        with contextlib.redirect_stdout(buf):
            spec.loader.exec_module(mod)
    except SystemExit as e:
        code = e.code
    except Exception as e:  # a prerequisite that cannot run is a refusal, never a pass
        return None, "%s raised %s: %s" % (os.path.basename(path), type(e).__name__, e)
    finally:
        sys.argv = saved
    out = buf.getvalue().splitlines()
    base = os.path.basename(path)
    # The configured `line` format decides what a FAIL is; the literal prefixes are a floor. Same defect and same fix as
    # gfz-scripts/prereq.py (ASTRA's A03 REJECT, 2026-09-29): a custom format's recognized FAIL was read as no failure.
    failed = [l[:100] for l in out if (lambda m: bool(m and m.group(1).upper() == "FAIL"))(line.match(l)) or l.startswith(("FAIL ", "FAIL\t"))]
    if code != 0:
        return None, "%s exit %r%s" % (base, code, "; " + " | ".join(failed) if failed else "")
    if not out or out[-1] != "FAILS 0":
        return None, "%s output does not end with 'FAILS 0' (last line %r)" % (base, out[-1][:60] if out else None)
    bad = [l[:60] for l in out[:-1] if not line.match(l)]
    if bad:
        return None, "%s output is malformed: %r" % (base, bad[:3])
    if failed:
        return None, "%s exited 0 but printed FAIL lines: %s" % (base, " | ".join(failed))
    seen = [line.match(l).group(2) for l in out[:-1]]
    if sorted(seen) != sorted(tags):
        return None, "%s checks %s, expected exactly %s" % (base, seen, list(tags))
    miss = [n for n in names if not hasattr(mod, n)]
    if miss:
        return None, "%s does not define %s" % (base, miss)
    return mod, None
