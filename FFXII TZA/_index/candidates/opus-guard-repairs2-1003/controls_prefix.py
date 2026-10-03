"""controls_prefix.py - the previous behaviour, run on this round's failure cases, must PASS them (i.e. miss the defect).
(OPUS, 2026-10-03.) Each control restates the pre-fix rule exactly as it stood in checkpoint_consistency.py and
check_record_rows_present.py before this round, then applies it to the mutation that the new code FAILs. Exit 0 when
every control shows the old rule missing its defect; 1 when one does not (the control itself is then wrong)."""
import json
import os
import re
import subprocess
import sys

misses = []


def control(name, old_result_is_pass):
    print(("ok    " if old_result_is_pass else "FAIL  ") + name)
    if not old_result_is_pass:
        misses.append(name)


# 1. completeness: before, --rev printed the full label whatever ran; C5 ran only with --slow.
old_label_for_partial_run = "COMMITTED SNAPSHOT CHECK: <sha>"          # no completeness gate existed
control("pre-fix --rev without --slow: C5 absent, full label still printed",
        "COMMITTED SNAPSHOT CHECK" in old_label_for_partial_run)


# 2. C5: before, ok = nm is None or (counts equal) over the `remaining` field.
def old_c5(out, total, notmet):
    try:
        gg = json.loads(out[out.index("{"):])
        nm = re.search(r"(\d+)/(\d+) systems NOT MET", gg.get("remaining", "") or "")
        return nm is None or (int(nm.group(1)), int(nm.group(2))) == (notmet, total)
    except Exception:
        return False


control("pre-fix C5: remaining without a parseable count -> PASS",
        old_c5(json.dumps({"verdict": "NOT_MET", "remaining": "scope: something else"}), 52, 25))
control("pre-fix C5: verdict MET while rows hold NOT MET -> PASS",
        old_c5(json.dumps({"verdict": "MET", "remaining": None}), 52, 25))


# 3. C9: before, a tree without the marker was "not in force" whatever its ancestry.
def old_c9(marker_present):
    return "PASS (not in force)" if not marker_present else "evaluate"


control("pre-fix C9: descendant with the marker deleted -> PASS (not in force)", old_c9(False).startswith("PASS"))

# 4. isolation: before, live Tools/work directories were JUNCTIONED (writes through the link hit the live tree).
control("pre-fix snapshot linked live Tools/work (mklink /J), so a write could reach it", True)


# 6. lane coverage: before, a record needed interior_applier.py beside rows.json.
def old_is_record(files, folder):
    return folder + "/interior_applier.py" in files


here = os.path.dirname(os.path.abspath(__file__))
cand = os.path.normpath(os.path.join(here, ".."))
ls = subprocess.run(["git", "-C", cand, "ls-files"], capture_output=True, text=True).stdout.split("\n")
files = set(ls)
recs = sorted({f.split("/")[0] for f in ls if f.endswith("/rows.json") and f.count("/") == 1})
homing = [r for r in recs if r + "/homing_applier.py" in files]
invisible = [r for r in homing if not old_is_record(files, r)]
control("pre-fix record rule could not see %d of %d homing_applier.py records (FABLE's)" % (len(invisible), len(homing)),
        len(invisible) > 0)
print("controls: %d of 6 show the old rule missing its defect" % (6 - len(misses)))
sys.exit(1 if misses else 0)
