"""The negative controls for aq18_flagpayload_span.py - a clean run must be earnable.

`ASTRA-CONTRA-OPUS-AQ18-ZERO-CASE-VERDICT` showed the first version of that script
printing its population and control figures and then issuing its negative verdict anyway:
fed an empty index it reported "expected 16, observed 0", "distinct area ids 0", "0 of 0",
printed the verdict and exited 0. A negative earned by a run that read nothing is worth
less than no run, because it looks like evidence.

This drives the fixed script with three deliberately broken populations and requires each
to REFUSE - exit 2, with no verdict line on stdout. A control that cannot be shown to fire
is not a control, which is the whole point of the contradiction being upheld.

    FF12_VBF=<path to FFXII_TZA.vbf> python aq18_negative_controls.py

OPUS, 2026-09-20.
"""
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "aq18_flagpayload_span.py")
KIT = os.path.normpath(os.path.join(HERE, "../../../../Tools/analysis-kit/gfz-scripts"))

SHIM = '''
import sys, io, os
sys.path.insert(0, %r)
import census_format_magics as C
_real = C.load_index
MODE = os.environ["AQ18_CONTROL_MODE"]

def fake(f):
    names, blocks = _real(f)
    if MODE == "empty":
        return {}, blocks
    if MODE == "half":
        keep = [p for p in names if "katano" in p and p.endswith(".sav")][:9]
        return {k: v for k, v in names.items() if k in keep}, blocks
    if MODE == "truncate":
        out = {}
        for k, v in names.items():
            sb, size, off = v
            out[k] = (sb, 0x400, off) if ("katano" in k and k.endswith(".sav")) else v
        return out, blocks
    raise SystemExit("unknown mode")

C.load_index = fake
exec(compile(io.open(%r, encoding="utf-8").read(), %r, "exec"))
'''


def run(mode):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(SHIM % (KIT, TARGET, TARGET))
        path = fh.name
    env = dict(os.environ, AQ18_CONTROL_MODE=mode)
    p = subprocess.run([sys.executable, path], capture_output=True, text=True, env=env)
    os.unlink(path)
    return p.returncode, p.stdout, p.stderr


EXPECT = {
    "empty":    "an empty index must not earn a negative verdict",
    "half":     "a population of 9 of 16 must not earn a negative verdict",
    "truncate": "files too short to contain the span must not earn a negative verdict",
}

fails = 0
for mode, why in EXPECT.items():
    rc, out, err = run(mode)
    verdict = "VERDICT:" in out
    ok = rc == 2 and not verdict
    print("%-9s exit=%-3d verdict_printed=%-5s  %s" % (mode, rc, verdict, "PASS" if ok else "FAIL"))
    print("          %s" % (err.strip().splitlines()[-1] if err.strip() else "(no reason given)"))
    if not ok:
        fails += 1
        print("          EXPECTED: %s" % why)

print("\n%d of %d negative controls fire" % (len(EXPECT) - fails, len(EXPECT)))
raise SystemExit(1 if fails else 0)
