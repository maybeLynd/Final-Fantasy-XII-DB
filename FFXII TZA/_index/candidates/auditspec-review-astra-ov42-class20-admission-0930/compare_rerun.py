"""compare_rerun.py - SWE2-AUDIT-SPEC: JSON-compare this folder's fresh re-runs with the packet's committed files.
Usage: python compare_rerun.py PACKET_DIR  (pairs listed below; a pair whose rerun file is absent is reported)."""
import json, os, sys
R = os.path.dirname(os.path.abspath(__file__))
P = sys.argv[1]
PAIRS = {
    "ov42-special-action-preconditions": [
        ("special-admission-result-01.json", "rerun_special-admission-result.json"),
        ("special-admission-raw-01.json", "rerun_special-admission-raw.json"),
        ("special-loader-raw-01.json", "rerun_special-loader-raw.json"),
        ("selector-callers-raw-01.json", "rerun_selector-callers-raw.json"),
        ("action-selectors-01/result.json", "rerun_action-selectors-result.json")],
    "ov42-class20-action-admission": [
        ("class20-admission-result-01.json", "rerun_class20-admission-result.json"),
        ("action-admission-guards-raw-01.json", "rerun_action-admission-guards-raw.json"),
        ("special-admission-callers-raw-01.json", "rerun_special-admission-callers-raw.json")],
}[os.path.basename(os.path.normpath(P))]
for a, b in PAIRS:
    fb = os.path.join(R, b)
    if not os.path.exists(fb):
        print("%-40s rerun file absent" % a); continue
    x = json.load(open(os.path.join(P, a))); y = json.load(open(fb))
    print("%-40s %s %s" % (a, "identical" if x == y else "DIFF", [k for k in set(x) | set(y) if x.get(k) != y.get(k)]))
