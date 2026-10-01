#!/usr/bin/env python3
"""check_parity_current.py - PARITY-STATUS.md against what its own generator produces now.

WHY THIS EXISTS. PARITY-STATUS.md says "GENERATED - do not hand-edit" and names parity_status.py.
Nothing checked that the committed file still matches what that generator produces, so the file
could drift from the harnesses it reports on and no gate would notice - the same shape as
COVERAGE-DIMENSIONS quoting 1,389 named fields for a day while every gate passed, which is why
check_surface_figures.py was written.

The goal's own instruction for this surface is "regenerate from clean HEAD; do not choose 7 or 13 by
hand", and a generated file nobody re-generates is exactly how a hand-chosen number survives.

WHAT IT DOES. Runs parity_status.py to a temporary path and diffs it against the committed file,
ignoring trailing whitespace only. A difference means the committed file is stale - or that someone
edited it by hand, which the file's own header forbids.

WHAT IT DOES NOT DO. It does not run the differential harnesses (parity_status.py --run). It checks
that the REPORT matches its generator against the current tree, not that the harnesses still pass;
those are the pilots' own business and take far longer than a gate should.

usage: check_parity_current.py [--db DB]
"""
import argparse
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DEFAULT_DB = os.path.join(ROOT, "Database", "FFXII TZA")


def norm(text):
    return [l.rstrip() for l in text.replace("\r\n", "\n").split("\n")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    a = ap.parse_args()

    committed = os.path.join(a.db, "_index", "PARITY-STATUS.md")
    if not os.path.exists(committed):
        print("PARITY-STATUS.md not found at %s" % committed)
        return 1

    gen = os.path.join(HERE, "parity_status.py")
    tmp = os.path.join(tempfile.mkdtemp(prefix="parity-check-"), "PARITY-STATUS.md")
    r = subprocess.run([sys.executable, gen, "--out", tmp], capture_output=True, text=True, cwd=ROOT)
    # parity_status.py is a GATE as well as a generator: it exits non-zero while any declaration
    # problem stands, and six do. A non-zero exit therefore says nothing about whether it produced
    # the report - only the file's existence does. Treating its exit code as failure made this
    # checker refuse to compare anything on its first run.
    if not os.path.exists(tmp):
        print("the generator produced no file, so nothing is asserted about the committed one:")
        print("  " + ((r.stderr or r.stdout or "").strip().splitlines() or ["(no output)"])[-1][:120])
        return 2
    print((r.stdout or "").strip().splitlines()[-1][:120])

    want = norm(io.open(tmp, encoding="utf-8", errors="replace").read())
    have = norm(io.open(committed, encoding="utf-8", errors="replace").read())
    if want == have:
        print("PARITY-STATUS.md matches its generator")
        return 0

    diffs = [i for i in range(max(len(want), len(have)))
             if (want[i] if i < len(want) else None) != (have[i] if i < len(have) else None)]
    print()
    print("PARITY-STATUS.md IS STALE: %d line(s) differ from the generator" % len(diffs))
    for i in diffs[:8]:
        print("  line %d" % (i + 1))
        print("    committed: %s" % ((have[i] if i < len(have) else "<missing>")[:100]))
        print("    generator: %s" % ((want[i] if i < len(want) else "<missing>")[:100]))
    return 1


if __name__ == "__main__":
    sys.exit(main())
