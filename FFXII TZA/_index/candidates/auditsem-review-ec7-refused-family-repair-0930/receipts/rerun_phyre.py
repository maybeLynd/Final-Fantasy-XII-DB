"""SWE2-AUDIT-SEM T0 spot-check: select_phyre_module.py for PRendering and PPostProcessing via runpy (no --write),
diffed against the tracked members files."""
import runpy, sys, os
M = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\22-Middleware-PhyreEngine\members"
sys.path.insert(0, M)
for mod, f in (("PRendering", "phyre-prendering.tsv"), ("PPostProcessing", "phyre-ppostprocessing.tsv")):
    sys.argv = [os.path.join(M, "select_phyre_module.py"), mod]
    g = runpy.run_path(sys.argv[0], run_name="__main__")
    sel = sorted(g["members"])
    tr = sorted(int(l.split()[0], 16) for l in open(os.path.join(M, f)) if l.strip() and not l.startswith("#"))
    print("RESULT %-16s selector %4d tracked %4d equal=%s +%s -%s" % (mod, len(sel), len(tr), sel == tr,
          " ".join("%08X" % x for x in sorted(set(sel) - set(tr))[:8]), " ".join("%08X" % x for x in sorted(set(tr) - set(sel))[:8])))
