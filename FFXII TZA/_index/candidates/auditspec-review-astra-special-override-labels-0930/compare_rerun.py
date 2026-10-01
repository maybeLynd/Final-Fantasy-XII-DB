"""Compare this review's fresh re-runs of the special-action-override-label-binding packet with its committed outputs."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent
P = R.parents[2] / "_experiments/evidence/special-action-override-label-binding"
pairs = [("rerun_label_result.json", "special-override-label-binding-result-02.json"),
         ("rerun_constructor-dependencies_raw.json", "special-override-constructor-dependencies-raw-01.json"),
         ("rerun_formatting-effects_raw.json", "special-override-formatting-effects-raw-01.json"),
         ("rerun_control_raw.json", "special-override-control-raw-01.json"),
         ("rerun_prereq_controls/result.json", "special-override-label-prerequisite-controls-02/result.json")]
for mine, theirs in pairs:
    a = json.loads((R / mine).read_text()); b = json.loads((P / theirs).read_text())
    diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    print("%-40s identical=%s differing_keys=%s" % (mine, a == b, diff))
c = json.loads((R / "rerun_prereq_controls/result.json").read_text())
for k in c["cases"]:
    err = (R / "rerun_prereq_controls" / k["case"] / "stderr.txt").read_text().strip().splitlines()
    print("  case %-20s exit %s created %s passed %s  last stderr: %s" % (k["case"], k["exit_code"], k["result_created"], k["passed"], err[-1][-90:] if err else ""))
