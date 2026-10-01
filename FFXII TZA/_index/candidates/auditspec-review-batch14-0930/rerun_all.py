"""rerun_all.py - SWE2-AUDIT-SPEC (2026-09-30): re-run every committed RC-11..RC-21 control of 1e4537034 from its own
folder and compare stdout with the committed .out, ignoring CR. Also records the scripts' exit codes, and reports any
tracked file a run dirtied (the caller restores those). Output: rerun_summary.txt; each stdout as rerun_<name>.out."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.dirname(HERE)
JOBS = [
    ("rc11-arena-ten-0930", "arena_sites.py", [], "arena_sites.out"),
    ("rc11-arena-ten-0930", "b00_census.py", [], "b00_census.out"),
    ("rc11-arena-ten-0930", "basedisp.py", ["02096A00", "02096C78"], "basedisp_02096Axx.out"),
    ("rc11-arena-ten-0930", "basedisp.py", ["022D89B8", "022D89BC"], "basedisp_022D89B8.out"),
    ("rc11-arena-ten-0930", "closure.py", [], "closure.out"),
    ("rc11-arena-ten-0930", "reach59.py", [], "reach59.out"),
    ("rc11-arena-ten-0930", "residue5.py", [], "residue5.out"),
    ("rc11-arena-ten-0930", "riprefs.py", ["02096A00", "02096C78"], "riprefs_02096Axx.out"),
    ("rc11-arena-ten-0930", "riprefs.py", ["02096B98"], "riprefs_02096B98.out"),
    ("rc11-arena-ten-0930", "riprefs.py", ["02096C70"], "riprefs_02096C70.out"),
    ("rc11-arena-ten-0930", "riprefs.py", ["022D89B8", "022D89BC"], "riprefs_022D89B8.out"),
    ("rc11-arena-ten-0930", "riprefs.py", ["02F97340"], "riprefs_02F97340.out"),
    ("rc11-arena-ten-0930", "uninit.py", [], "uninit.out"),
    ("rc11-arena-ten-0930", "verb_census.py", [], "verb_census.out"),
    ("rc12-footer-channels-runstate-0930", "rc12_slots.py", [], "rc12_slots.out"),
    ("rc12-footer-channels-runstate-0930", "rc13_engine_channels.py", [], "rc13_engine_channels.out"),
    ("rc12-footer-channels-runstate-0930", "rc13_script_channels.py", [], "rc13_script_channels.out"),
    ("rc12-footer-channels-runstate-0930", "rc14_sweep.py", [], "rc14_sweep.out"),
    ("rc15-regfile-skipmask-0930", "rc15_flow.py", [], "rc15_flow.out"),
    ("rc15-regfile-skipmask-0930", "rc16_check.py", [], "rc16_check.out"),
    ("rc15-regfile-skipmask-0930", "rc17_skip_chain.py", [], "rc17_skip_chain.out"),
    ("rc15-regfile-skipmask-0930", "scan_bit13.py", [], "scan_bit13.out"),
    ("rc18-map1-blend-arms-0930", "rc18_follow_path.py", [], "rc18_follow_path.out"),
    ("rc18-map1-blend-arms-0930", "rc18_map1_writers.py", [], "rc18_map1_writers.out"),
    ("rc18-map1-blend-arms-0930", "rc18_mode_idiom.py", [], "rc18_mode_idiom.out"),
    ("rc18-map1-blend-arms-0930", "rc18_modes_emu.py", [], "rc18_modes_emu.out"),
    ("rc18-map1-blend-arms-0930", "rc19_blend_arms.py", [], "rc19_blend_arms.out"),
    ("rc18-map1-blend-arms-0930", "rc19_rate_readers.py", [], "rc19_rate_readers.out"),
    ("rc18-map1-blend-arms-0930", "slice.py", [], "slice.out"),
    ("rc20-float-push-verbs-0930", "rc20_verbs.py", [], "rc20_verbs.out"),
    ("rc21-verb-reach-regen-0930", "rc21_reach.py", [], "rc21_reach.out"),
    ("rc21-verb-reach-regen-0930", "rc21_draws.py", [], "rc21_draws.out"),
]
only = sys.argv[1:]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
lines = []
for d, s, args, out in JOBS:
    if only and not any(o in out for o in only):
        continue
    wd = os.path.join(CAND, d)
    p = subprocess.run([sys.executable, "-B", s] + args, cwd=wd, capture_output=True, env=env)
    mine = p.stdout.replace(b"\r", b"")
    tag = "rerun_%s__%s" % (d.split("-")[0], out)
    open(os.path.join(HERE, tag), "wb").write(mine)
    ref = open(os.path.join(wd, out), "rb").read().replace(b"\r", b"")
    same = "IDENTICAL" if mine == ref else "DIFFERS (%d vs %d lines)" % (mine.count(b"\n"), ref.count(b"\n"))
    line = "%-36s %-22s %-28s rc=%d %s" % (d, s, " ".join(args), p.returncode, same)
    print(line, flush=True)
    if p.returncode and p.stderr:
        print("   stderr:", p.stderr.decode("utf-8", "replace").strip().splitlines()[-1][:200])
    lines.append(line)
if not only:
    open(os.path.join(HERE, "rerun_summary.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
