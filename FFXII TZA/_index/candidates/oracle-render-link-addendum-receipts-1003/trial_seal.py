"""trial_seal.py - apply the existing seal.py policy to ASTRA's render-review link addendum runs in a SCRATCH store
(ASTRA-REQ-ORACLE-RENDER-LINK-ADDENDUM-1003; SWE2-ORACLE, Claude stand-in). Copies only; ASTRA's files are untouched.
Prints each receipt's publishable() refusals - the exact remediation list."""
import json, os, sys
R = r"C:\Users\Kristian\source\repos\XIIOnline"
sys.path.insert(0, os.path.join(R, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import seal
A = os.path.join(R, "Database", "Tools", "work", "ASTRA", "runtime-residue-method-retriage", "render-review-link-closure")
import tempfile
STORE = tempfile.mkdtemp(prefix="oracle-trial-store-")   # scratch: the trial seals nothing durable
prep = json.load(open(os.path.join(A, "prepared-01", "result.json"), encoding="utf-8"))
ctl = json.load(open(os.path.join(A, "controls-01", "result.json"), encoding="utf-8"))
print("prepared keys:", sorted(prep)[:12])
print("controls case keys:", sorted(ctl["cases"][0]))
# inputs: the referent origins named in the prepared result (the bytes copied into additions)
inputs = {}
for a in prep.get("additions", []):
    for o in a.get("origins", []):
        p = os.path.join(R, o["path"].replace("/", os.sep))
        inputs[o["path"].replace("/", "__")] = p
missing = [p for p in inputs.values() if not os.path.isfile(p)]
print("origin inputs:", len(inputs), "missing:", missing[:3])
cases_prep = ["addendum"]                     # what a declared case list would have to name
rid1 = seal.seal(STORE, {"prepare.py": os.path.join(A, "prepare.py")},
                 {k: v for k, v in inputs.items() if os.path.isfile(v)},
                 os.path.join(A, "prepared-01", "result.json"), cases_prep,
                 "TRIAL - scratch store, not a credit")
rid2 = seal.seal(STORE, {"control.py": os.path.join(A, "control.py"), "prepare.py": os.path.join(A, "prepare.py")},
                 {}, os.path.join(A, "controls-01", "result.json"),
                 [c["case"] for c in ctl["cases"]], "TRIAL - scratch store, not a credit")
for name, rid in (("prepared-01", rid1), ("controls-01", rid2)):
    rec = seal.load(STORE, rid)
    print("==", name, rid, "verify:", seal.verify(STORE, rid) or "intact")
    print("   drivers:", {n: (v["git_blob"], v["committed"]) for n, v in rec["drivers"].items()})
    for p in seal.publishable(STORE, rid):
        print("   REFUSE:", p)

# REMEDIATION SIMULATION: the same runs with the case shape seal._case_ids reads ({"cases": [{"id": ...}]}).
# Temp copies only. Expected: the case-list refusal disappears; only the driver-commit refusals remain.
import shutil
T = tempfile.mkdtemp(prefix="oracle-trial-fix-")
pfix = dict(prep)
pfix["cases"] = [{"id": "old-manifest-76"}] + [
    {"id": "link:%s -> %s" % (l["document"].rsplit("/", 1)[-1], l["target"])} for l in prep["links"]]
cfix = dict(ctl)
cfix["cases"] = [dict(c, id=c["case"]) for c in ctl["cases"]]
pp, cp = os.path.join(T, "prepared-result.json"), os.path.join(T, "controls-result.json")
json.dump(pfix, open(pp, "w", encoding="utf-8"), indent=2)
json.dump(cfix, open(cp, "w", encoding="utf-8"), indent=2)
rid3 = seal.seal(STORE, {"prepare.py": os.path.join(A, "prepare.py")}, {}, pp, [c["id"] for c in pfix["cases"]],
                 "TRIAL fix simulation")
rid4 = seal.seal(STORE, {"control.py": os.path.join(A, "control.py"), "prepare.py": os.path.join(A, "prepare.py")}, {},
                 cp, [c["id"] for c in cfix["cases"]], "TRIAL fix simulation")
for name, rid in (("prepared-with-ids (%d cases)" % len(pfix["cases"]), rid3), ("controls-with-ids", rid4)):
    probs = seal.publishable(STORE, rid)
    print("== FIX", name, rid)
    for p in probs:
        print("   REFUSE:", p)
    print("   remaining refusals all driver-commit:", all("not a committed source" in p for p in probs))
shutil.rmtree(T, ignore_errors=True)
