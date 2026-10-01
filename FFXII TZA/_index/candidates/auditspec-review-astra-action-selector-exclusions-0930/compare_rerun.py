"""compare_rerun.py - SWE2-AUDIT-SPEC: compare this folder's fresh re-runs with the packet's committed results/raws,
and the re-run control receipts (built in the session scratchpad) with the packet's committed receipts, ignoring the
fields that name paths/interpreters (argv, adapted_checker_sha256, which embed the output location)."""
import json, os, sys
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
P = os.path.join(ROOT, "Database", "FFXII TZA", "_experiments", "evidence", "action-selector-local-exclusions")
R = os.path.dirname(os.path.abspath(__file__))
S = sys.argv[1]
pairs = [("action-category-seven-result-01.json", "rerun_action-category-seven-result.json"),
         ("special-fallback-byte-result-01.json", "rerun_special-fallback-byte-result.json"),
         ("action-availability-gates-raw-01.json", "rerun_action-availability-gates-raw.json"),
         ("spattack-leaves-and-guard-raw-01.json", "rerun_spattack-leaves-and-guard-raw.json"),
         ("special-selection-dispatch-raw-02.json", "rerun_special-selection-dispatch-raw.json")]
for a, b in pairs:
    x = json.load(open(os.path.join(P, a))); y = json.load(open(os.path.join(R, b)))
    print("%-42s %s %s" % (a, "identical" if x == y else "DIFF", [k for k in set(x) | set(y) if x.get(k) != y.get(k)]))
for d in ("category-controls", "fallback-controls"):
    x = json.load(open(os.path.join(P, d, "receipt.json"))); y = json.load(open(os.path.join(S, d, "receipt.json")))
    strip = lambda cs: [{k: v for k, v in c.items() if k not in ("argv", "adapted_checker_sha256")} for c in cs]
    print("%-42s driver %s checker %s cases %s" % (d, x["driver_sha256"] == y["driver_sha256"],
                                                   x["original_checker_sha256"] == y["original_checker_sha256"],
                                                   "identical" if strip(x["cases"]) == strip(y["cases"]) else "DIFF"))
    for c in y["cases"]:
        err = open(os.path.join(S, d, c["case"], "stderr.txt")).read().strip().splitlines()
        print("   %-28s exit=%d result=%s passed=%s  %s" % (c["case"], c["exit_code"], c["result_exists"],
                                                          c["control_passed"], (err[-1] if err else "")[:110]))
    pos = json.load(open(os.path.join(S, d, "positive", "result.json")))
    ref = json.load(open(os.path.join(P, d, "positive", "result.json")))
    keep = lambda r: {k: v for k, v in r.items() if k not in ("driver_sha256",)}
    print("   positive result vs committed positive result (driver hash excluded):",
          "identical" if keep(pos) == keep(ref) else "DIFF")
