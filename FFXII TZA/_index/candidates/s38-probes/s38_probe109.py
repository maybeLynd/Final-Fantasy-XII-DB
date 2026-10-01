import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_experiments\evidence\render-pool-lifecycle-exec")
sys.dont_write_bytecode = True
import check as C
raw, secs = C.load_image()
for case in C.build_cases():
    if case["name"].startswith("aloc-"):
        tr, faults, obs = C.run_case(dict(case), raw, secs)
        ret = obs["ret"]; idx = (ret - C.POOL)//C.STRIDE if ret else None
        print("%-18s ret_idx=%s live=%#x nextFree=%#x faults=%s" % (case["name"], idx, obs["live"], obs["nextFree"], faults))
