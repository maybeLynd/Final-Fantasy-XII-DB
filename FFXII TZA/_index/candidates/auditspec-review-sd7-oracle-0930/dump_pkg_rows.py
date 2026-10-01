"""dump_pkg_rows.py - SWE2-AUDIT-SPEC review helper (2026-09-30). Executes the PACKAGE's sd7_app_pointer_sites.py in a
private namespace (its stdout discarded) and writes every one of its 192 census rows with the class it assigned and the
regval terms it used, to pkg_rows.json in this folder. This is only the package's own census, captured so the
independent sweep (sd7_indep.py) can be compared to it site by site and so the E1 rule can be probed per site.
Nothing in the package folder is written (run with python -B)."""
import contextlib, io, json, os, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "sd7-stored-app-pointer-0930", "sd7_app_pointer_sites.py")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    g = runpy.run_path(PKG, run_name="__pkg__")
out = []
for f, a, ld, obj, terms in g["rows"]:
    if g["e1"](terms):
        c = "E1"
    elif g["e2"](terms):
        c = "E2"
    elif g["e3"](terms):
        c = "E3"
    else:
        ds = g["slot_disps"](f, ld.address, obj) if ld is not None and obj else []
        c = "E4" if [x for x in ds if x[1] >= 31 * 8] else "RESIDUE"
    out.append({"func": "%08X" % f, "site": "%08X" % a, "vtload": ("%08X" % ld.address) if ld is not None else None,
                "obj": obj, "class": c, "terms": sorted([list(map(str, t)) for t in (terms or ())])})
json.dump(out, open(os.path.join(HERE, "pkg_rows.json"), "w"), indent=0)
print("rows", len(out), "last line of package output:", buf.getvalue().strip().splitlines()[-1])
