"""rerun.py - SWE2-AUDIT-SPEC re-run of 3198ee367's receipts: the five rip_refs.py windows the batch-1 README now
records, and counter_access.py. Each output goes to rerun_<name>.out here and is compared with the committed .out
ignoring CR. Run from anywhere; each script runs from its own directory."""
import subprocess, sys, os
C = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates"
HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
jobs = [("b1", "rip_refs.py", ["02064ACC", "02064AD0"], "rip_refs_02064ACC.out"),
        ("b1", "rip_refs.py", ["02CB8084", "02CB8088"], "rip_refs_02CB8084.out"),
        ("b1", "rip_refs.py", ["01F832B0", "01F832C8"], "rip_refs_01F832B0.out"),
        ("b1", "rip_refs.py", ["00369D30"], "rip_refs_00369D30.out"),
        ("b1", "rip_refs.py", ["02CB7FD0", "02CB843C"], "rip_refs_block.out"),
        ("b4", "counter_access.py", [], "counter_access.out")]
for b, script, args, ref in jobs:
    d = os.path.join(C, "swe2contract-ddres-%s-0930" % b)
    p = subprocess.run([sys.executable, script] + args, cwd=d, capture_output=True, text=True, env=env)
    name = "rerun_" + ref
    open(os.path.join(HERE, name), "w", encoding="utf-8", newline="\n").write(p.stdout)
    want = open(os.path.join(d, ref), encoding="utf-8").read().replace("\r", "")
    print("%-24s %-22s exit=%d %s" % (ref, " ".join(args) or "-", p.returncode,
                                     "IDENTICAL" if p.stdout.replace("\r", "") == want else "DIFFERENT"))
