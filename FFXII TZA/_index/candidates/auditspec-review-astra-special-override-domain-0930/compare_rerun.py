"""Compare this review's fresh re-runs of the special-action-override-domain packet with its committed outputs.
Run from the repo root. Prints one line per compared file and the differing top-level keys."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent
P = R.parents[2] / "_experiments/evidence/special-action-override-domain"
pairs = [("rerun_domain_result.json", "special-override-domain-result-01.json"),
         ("rerun_control_raw.json", "special-override-control-raw-01.json"),
         ("rerun_constructor_raw.json", "special-override-constructor-raw-01.json")]
for mine, theirs in pairs:
    a = json.loads((R / mine).read_text()); b = json.loads((P / theirs).read_text())
    diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    print("%-28s vs %-42s identical=%s differing_keys=%s" % (mine, theirs, a == b, diff))
    if "ranges" in a:
        print("   ranges=%d instructions=%d" % (len(a["ranges"]), sum(len(s["instructions"]) for s in a["ranges"])))
r = json.loads((R / "rerun_domain_result.json").read_text())
print("controls:", json.dumps(r["controls"]))
print("initializer_words:", r["initializer_words"], "constructor_initial_ae0:", r["constructor_initial_ae0"])
c = json.loads((R / "rerun_control_raw.json").read_text())
print("direct_calls:", json.dumps(c["direct_calls"]), "unresolved:", c["unresolved_candidates"])
print("file_backed_index:", json.dumps(c["file_backed_index"]))
