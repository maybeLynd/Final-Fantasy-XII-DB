"""gen_uc1_impact.py - measures what admitting the UC-1 floor would do to every figure the project reports.

PUBLISHED INTO THE KIT 2026-09-14 from `Tools/work/OPUS/uc1_impact.py`, which `.gitignore` excludes.
A canonical candidates file under `_index/candidates/` named it in its header, so the instruction
for reproducing a file this corpus cites pointed at a tool no peer had. Found by extending
`check_cited_instruments.py` to side files - it had been closed over `_index/*.md` and the kit's own
`*.py` and was blind to `.tsv` entirely.

THE BODY BELOW IS THE ORIGINAL, UNCHANGED. Rewriting its paths and defaults while publishing it
would mean the tool in the kit is not the tool that produced the file beside it, and seeing how the
rows were derived is the whole reason for publishing. The only addition is the two lines under this
docstring, which resolve the repository root from `__file__` and change into it so the tool's
repo-relative paths mean what they have always meant, from any working directory.

NAMED `gen_*`, NOT `check_*`: `run_gates.py` globs `check_*.py`, and a generator under that prefix
would run as a gate every suite and rewrite its own output as a side effect of auditing.
"""
import os as _os
import sys as _sys

# The repository root, four levels above this file: gfz-scripts -> analysis-kit -> Tools -> Database
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.dirname(_os.path.abspath(__file__)))))))

# The original module docstring, kept verbatim:
# uc1_impact.py - what a denominator change actually does to every figure, measured.
#
# `OPUS-REQ-AUDITSPEC-UC1-ESTABLISHED-FLOOR` tells the reviewer that *"a denominator change rewrites
# every figure this project reports"* and then does not say by how much. That is a warning where a
# table belongs: a reviewer deciding whether to accept a floor of 34,409 should see what accepting it
# does, and so should anyone who later wonders why the numbers moved.
#
# THREE POPULATIONS, all already argued elsewhere and none decided here:
#
#     34,270   the list, today's denominator
#     34,409   the established floor - the 139 unlisted blocks whose boundary three independent
#              signals agree on (uc1-established-floor-139.tsv)
#     35,572   the ceiling - every unlisted block admitted, boundary established or not
#              (35,579 counting the 7 ambiguous)
#
# WHAT MOVES AND WHAT DOES NOT. The admitted blocks are unlisted code: nothing cites them, nothing
# dispositions them. **Every numerator stays exactly where it is** - they enter only the denominator,
# and therefore only the frontier. So every ratio this project reports gets WORSE, which is the point
# worth putting in front of a reviewer: **the floor is not the flattering subset, and admitting it
# costs percentage points rather than buying them.**
#
# Reads the live figures rather than restating them, so it cannot quote a stale numerator.

import re, subprocess, sys, os

KIT = os.path.join("Database", "Tools", "analysis-kit", "gfz-scripts")
DB = "Database/FFXII TZA"
LIST = 34270
FLOOR = 34409
CEIL = 35572
CEIL_AMB = 35579


def live():
    r = subprocess.run([sys.executable, os.path.join(KIT, "progress.py"), "--db", DB],
                       capture_output=True, text=True)
    t = r.stdout + r.stderr
    m = re.search(r"engine_explained.*?([\d,]+)\s*/\s*([\d,]+)", t)
    cited = int(m.group(1).replace(",", "")) if m else None
    den = int(m.group(2).replace(",", "")) if m else None
    m = re.search(r"A\s+(\d+)\s*\+\s*B\s+(\d+)\s*\+\s*C\s+(\d+)\s*=\s*(\d+)\s+of\s+(\d+)", t)
    A, B, C, disp = (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))) if m \
        else (None,) * 4
    m = re.search(r"frontier\s+(\d+)", t)
    frontier = int(m.group(1)) if m else None
    return cited, den, A, B, C, disp, frontier


def main():
    cited, den, A, B, C, disp, frontier = live()
    if den is None:
        print("could not read the live figures - refusing to print a table from memory")
        return 2
    if den != LIST:
        print("progress.py reports a denominator of %d, not %d - the populations below are stale "
              "and this needs re-deriving before it is shown to anyone" % (den, LIST))
        return 2

    print("UC-1 denominator impact, measured against the live figures\n")
    print("  live numerators (unchanged by any of this):")
    print("      engine_explained cited : %d" % cited)
    print("      EC-7 A / B / C         : %d / %d / %d  = %d declared" % (A, B, C, disp))
    print("      frontier at 34,270     : %d" % frontier)
    print()
    print("  %-34s %10s %10s %10s %10s" % ("", "list", "floor", "ceiling", "ceiling+amb"))
    print("  %-34s %10d %10d %10d %10d" % ("population", LIST, FLOOR, CEIL, CEIL_AMB))
    print("  %-34s %10s %+10d %+10d %+10d" % ("bodies admitted", "-", FLOOR - LIST,
                                              CEIL - LIST, CEIL_AMB - LIST))
    print()
    for label, num in (("engine_explained", cited), ("EC-7 declared surface", disp)):
        print("  %-34s %9.2f%% %9.2f%% %9.2f%% %9.2f%%"
              % (label, 100.0 * num / LIST, 100.0 * num / FLOOR,
                 100.0 * num / CEIL, 100.0 * num / CEIL_AMB))
    print("  %-34s %9.2f  %9.2f  %9.2f  %9.2f"
          % ("  points lost vs list", 0.0,
             100.0 * cited / LIST - 100.0 * cited / FLOOR,
             100.0 * cited / LIST - 100.0 * cited / CEIL,
             100.0 * cited / LIST - 100.0 * cited / CEIL_AMB))
    print()
    print("  %-34s %10d %10d %10d %10d"
          % ("frontier", frontier, frontier + (FLOOR - LIST), frontier + (CEIL - LIST),
             frontier + (CEIL_AMB - LIST)))
    print()
    print("  EVERY NUMERATOR IS UNCHANGED. The admitted blocks are unlisted code: nothing cites")
    print("  them and nothing dispositions them, so they enter the denominator and the frontier")
    print("  and nothing else. Every ratio gets worse.")
    print()
    print("  That is the argument for the floor rather than against it: it is not the flattering")
    print("  subset, and an agent proposing a denominator that costs it percentage points is not")
    print("  proposing it to look better.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
