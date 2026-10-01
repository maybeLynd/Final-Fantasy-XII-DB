"""Labelled control for falsify_heading_delta.py H8 (OPUS, 2026-09-29): the real script, run unchanged, with ONE intervention -
its read of functions.tsv returns the catalogue with 002E45E0's size set to 40 (the first-fragment reading). Expected: H8 BROKEN,
the process exits 1. Usage: python h8_catalogue_control.py <gfz-scripts dir>"""
import io, runpy, sys, os
D = sys.argv[1]
real = io.open


def patched(path, *a, **k):
    if str(path).replace("\\", "/").endswith("Tools/work/graph/functions.tsv") and "b" not in (a[0] if a else k.get("mode", "r")):
        rows = []
        for line in real(path, *a, **k):
            p = line.split("\t")
            if p[0] == "002E45E0":
                p[2] = "40"; line = "\t".join(p)
            rows.append(line)
        return io.StringIO("".join(rows))
    return real(path, *a, **k)


io.open = patched
sys.argv = [os.path.join(D, "falsify_heading_delta.py")]
try:
    runpy.run_path(sys.argv[0], run_name="__main__")
    code = 0
except SystemExit as e:
    code = e.code
io.open = real
print("CONTROL exit code %s" % code)
sys.exit(0 if code == 1 else 2)
