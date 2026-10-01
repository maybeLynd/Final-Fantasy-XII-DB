# scratch_sel2.py <selector.py> <outdir> [args...] - run a members selector with its write targets
# redirected to <outdir>. Same as ../scratch_sel.py but also rewrites single-quoted 'w' opens.
# Env NOUC1=1 strips UC-1 frontier bodies from the census (emulates the UC-1 exclusion patch).
import sys, os, re
sel, outd = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
os.makedirs(outd, exist_ok=True)
src = open(sel, encoding="utf-8").read()
n = 0
def rw(m):
    global n
    n += 1
    return 'open(os.path.join(%r, os.path.basename(%s)), %s' % (outd, m.group(1), m.group(2))
src2 = re.sub(r'open\((os\.path\.join\([^()]*\)),\s*(["\']w["\'])', rw, src)
src2 = re.sub(r'open\(([A-Za-z_]\w*),\s*(["\']w["\'])', rw, src2)
src2 = src2.replace("__file__", repr(sel))
if os.environ.get("UC1IN"):
    # R1 test 2: re-run the selector WITH the UC-1 frontier bodies in its population - undo only the selector's own
    # UC-1 exclusion (the check_dispositions A set is untouched).
    k = src2.count("uc1_band.frontier_starts()")
    if ":" in os.environ["UC1IN"]:      # UC1IN=LO:HI - include only the UC-1 bodies inside [LO, HI)
        lo, hi = [int(x, 16) for x in os.environ["UC1IN"].split(":")]
        src2 = src2.replace("uc1_band.frontier_starts()",
                            "{_x for _x in uc1_band.frontier_starts() if not (%d <= _x < %d)}" % (lo, hi))
    else:
        src2 = src2.replace("uc1_band.frontier_starts()", "set()")
    print("[scratch_sel3] UC1IN: selector UC-1 exclusion undone at %d site(s)" % k, flush=True)
if "import os" not in src2:
    src2 = "import os\n" + src2
print("[scratch_sel2] redirected %d write(s) to %s" % (n, outd), flush=True)
if os.environ.get("NOUC1"):
    sys.path.insert(0, os.environ.get("KIT", r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts"))
    import check_dispositions as _cd, uc1_band as _u
    _orig = _cd.load_functions
    def _lf(path=None):
        s = _orig(path)
        f = _u.frontier_starts()
        print("[scratch_sel2] NOUC1: stripped %d UC-1 frontier bodies from the census" % len(f & set(s)), flush=True)
        return {k: v for k, v in s.items() if k not in f}
    _cd.load_functions = _lf
sys.argv = [sel] + sys.argv[3:]
code = compile(src2, sel, "exec")
g = {"__name__": "__main__", "__file__": sel}
exec(code, g)
