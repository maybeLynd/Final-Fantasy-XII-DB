"""test_gate_close.py [PUBLISH_PATHS_SH] - run the carrier gate's embedded Python from publish_paths.sh (default: the kit's) against fixture roots:
plan open -> the carrier is reported; plan CLOSED -> nothing; plan missing -> reported (fail closed);
a 'plan_state: CLOSED' mention inside prose (not its own line) -> still reported."""
import os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
SH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts", "publish_paths.sh")
sh = open(SH, encoding="utf-8").read()
i = sh.index('carrier_hit="$(python - "$root" "${TEAM_AGENT:-}" "$@" <<\'PYEOF\'')
body = sh[sh.index("\n", i) + 1: sh.index("\nPYEOF", i)]
CAR = "00-Engine-Core-Runtime/X.md"
fails = 0
def run(plan):
    root = tempfile.mkdtemp()
    cand = os.path.join(root, "Database", "FFXII TZA", "_index", "candidates")
    os.makedirs(cand)
    open(os.path.join(cand, "overlay-drop-census-2026-09-25.tsv"), "w", encoding="utf-8").write("file\tsections\n" + CAR + "\tS05\n")
    if plan is not None:
        open(os.path.join(cand, "overlay-publication-plan.md"), "w", encoding="utf-8").write(plan)
    out = subprocess.run([sys.executable, "-", root, "FABLE", "Database/FFXII TZA/" + CAR], input=body,
                         capture_output=True, text=True).stdout.strip()
    return out
for name, plan, want_hit in (("open", "# plan\n\nstill in force\n", True),
                             ("closed", "# plan\n\nplan_state: CLOSED\n", False),
                             ("missing", None, True),
                             ("prose mention", "# plan\n\nthe line `plan_state: CLOSED` closes it\n", True)):
    hit = bool(run(plan))
    ok = hit == want_hit
    fails += 0 if ok else 1
    print("%-14s %-4s carrier reported=%s" % (name, "PASS" if ok else "FAIL", hit))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
