"""check_s22_envscaling.py - FABLE, 2026-10-03, on SWE2-AUDIT-SPEC's L2 expansion (S-22, stale section 13).

Claim checked: CONTRACT-environmental-element-scaling.md section 13 reads "None. No experiment executes these four
bodies." Three recorded native replays execute them. This check:
  - re-runs the three packages from a temp copy and compares every result file's md5 with the committed one (RR*);
  - reads what each recorded result does and does not assert (W*);
  - asserts from the recorded 288-combination table the shared environment+terrain multiply that WE-2's 10-02
    correction names, and reads that multiply's single mulss at the bytes (S*).
Controls:
  C1 (sensitivity, reading): the OLD WE-2 wording "multiplied in sequence" predicts 1.2 x 1.2 = 1.44 where an
      environment rule and a terrain rule of one element both hold; on the recorded table that prediction must FAIL.
  C2 (sensitivity, stale text): the old section-13 claim "no experiment executes these four bodies" must FAIL
      against the recorded run (the stage and the getters are in its executed allowed set and it records writes).
Prints PASS/FAIL lines and FAILS N last.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
from capstone.x86 import X86_OP_IMM  # noqa: E402

DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CAND = os.path.abspath(os.path.join(HERE, ".."))
STEPS = os.path.join(CAND, "s22-opus-replay-steps-and-element-scaling")
RES = os.path.join(CAND, "s22-opus-replay-recipe-resolver")
SWG = os.path.join(CAND, "s22-opus-replay-severe-weather-gate")
fails = 0

REPLAYS = {
    "s22-opus-replay-steps-and-element-scaling": {"check.py": {"result.json": "99336e052d1e386d671e9cee2c5b5426"}},
    "s22-opus-replay-recipe-resolver": {"check.py": {"result.json": "a226db98765feb8a1a5447f211c1d194"},
                                        "we1.py": {"we1_result.json": "5680857b37dea30c63e4dbdc9d214019"}},
    "s22-opus-replay-severe-weather-gate": {"check.py": {"result.json": "867bbaf3cc23ce50b3d38778aa27afb0"}},
}


def report(ok, label, detail=""):
    global fails
    print("%s %s: %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        fails += 1


def rerun_replays():
    tmp = tempfile.mkdtemp(prefix="fable_l2exp_s22e_")
    try:
        for name, scripts in REPLAYS.items():
            src = os.path.join(CAND, name)
            dst = os.path.join(tmp, name)
            shutil.copytree(src, dst)
            for script, outs in scripts.items():
                pr = subprocess.run([sys.executable, script], cwd=dst, capture_output=True, text=True)
                for out, rec in outs.items():
                    got = hashlib.md5(open(os.path.join(dst, out), "rb").read()).hexdigest()
                    com = hashlib.md5(open(os.path.join(src, out), "rb").read()).hexdigest()
                    report(pr.returncode == 0 and got == com == rec, "RR %s/%s re-run reproduces %s" % (name, script, out),
                           "exit %d, re-run %s, committed %s, recorded %s" % (pr.returncode, got[:8], com[:8], rec[:8]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    head = os.popen('git -C "%s" rev-parse --short HEAD' % DB).read().strip()
    print("check_s22_envscaling.py  HEAD %s" % head)
    img = Img.load()

    # S1: the shared multiply at the bytes - one mulss in 0038B3E1..0038B42C, reached from the environment test
    # (je 0038B418 at 0038B3F6) and by fall-through from the terrain test (jne past it at 0038B416)
    win = list(img.cs.disasm(img.read(0x0038B3E1, 0x0038B42C - 0x0038B3E1), 0x0038B3E1))
    muls = [i for i in win if i.mnemonic == "mulss"]
    j_env = [i for i in win if i.address == 0x0038B3F6]
    j_ter = [i for i in win if i.address == 0x0038B416]
    ok = (len(muls) == 1 and muls[0].address == 0x0038B420
          and j_env and j_env[0].mnemonic == "je" and j_env[0].operands[0].type == X86_OP_IMM and j_env[0].operands[0].imm == 0x0038B418
          and j_ter and j_ter[0].mnemonic == "jne" and j_ter[0].operands[0].imm == 0x0038B42C
          and win[0].mnemonic == "test" and win[0].op_str == "byte ptr [rcx + 0x13], 2")
    report(ok, "S1 Lightning (bit 0x02): one mulss 0038B420 serves the environment test and the terrain test",
           " | ".join("%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in win if i.mnemonic in ("test", "je", "jne", "mulss", "call")))

    # W*: what the recorded steps-and-element-scaling result asserts
    r = json.load(open(os.path.join(STEPS, "result.json")))["results"]
    report(r["WE4_WE5_bit16_skips_the_stage"]["pass_"] is True, "W1 recorded: WE-4/WE-5 bit-16 skip case passes (asserted in the package)")
    w = r["WE2_WE6_rule_table"]
    report(w["pass_"] is True and set(w["writes"]) <= {"02AEE054", "02EBF188", "02EBF18C"},
           "W2 recorded: WE-6 write set is 02AEE054 + the cached unit pointer 02EBF188", " ".join(w["writes"]))
    t = {el: {(e, wv, tt): m for e, wv, tt, m in rows} for el, rows in w["rule_table_nonneutral"].items()}
    n = 6 * 4 * 3 * 4
    report(len(t) == 6, "W3 recorded: rule table over 6 elements (the run iterates %d combinations; neutral cells are omitted)" % n,
           ", ".join("%s %d" % (k, len(v)) for k, v in t.items()))
    report("rule_table_nonneutral" in w and w["note"].startswith("observed"),
           "W4 the WE-2 table is RECORDED, not asserted: the case's pass flag is the write-set bound only", w["note"][:60])

    shared = {"Lightning": [(0, wv, 0) for wv in range(3)], "Ice": [(2, wv, 2) for wv in range(3)],
              "Earth": [(1, wv, 1) for wv in range(3)], "Water": [(3, 0, 0), (3, 1, 0)]}
    vals = {el: [t[el].get(c) for c in cs] for el, cs in shared.items()}
    report(all(v == 1.2 for vs in vals.values() for v in vs),
           "S2 shared multiply: where an environment and a terrain rule of one element both hold, the factor is 1.2 once",
           "; ".join("%s %s" % (el, vs) for el, vs in vals.items()))
    old = all(abs((v or 0) - 1.44) < 1e-6 for vs in vals.values() for v in vs)
    report(not old, "C1 sensitivity: OLD 'multiplied in sequence' predicts 1.44 in those cells; it is FALSE",
           "prediction holds: %s" % old)
    report(t["Water"].get((3, 2, 0)) == 0.6 and t["Fire"].get((0, 2, 0)) == 0.6,
           "S3 composition across DIFFERENT rules still multiplies (x0.5 x1.2 = 0.6)", "Water e3w2t0 %s, Fire e0w2t0 %s"
           % (t["Water"].get((3, 2, 0)), t["Fire"].get((0, 2, 0))))

    # C2: the old section-13 statement against the recorded run. The stage is called directly (ESCALE = 0x38B220 in
    # the package source) and its writes are recorded; each of the three getters is shown live because the recorded
    # factor varies with the environment, MWeather and terrain class alone.
    srcs = open(os.path.join(STEPS, "check.py"), encoding="utf-8").read()
    called = "PREP, FINAL, ESCALE = 0x38AAF0, 0x38D280, 0x38B220" in srcs and "call(ESCALE" in srcs
    lt = t["Lightning"]; fi = t["Fire"]
    env_live = lt.get((0, 0, 1)) == 1.2 and lt.get((1, 0, 1)) is None      # environment 0 vs 1, terrain 1
    ter_live = lt.get((1, 0, 0)) == 1.2 and lt.get((1, 0, 1)) is None      # terrain 0 vs 1, environment 1
    wea_live = fi.get((1, 2, 1)) == 1.2 and fi.get((1, 1, 1)) is None      # MWeather 2 vs 1
    report(called and bool(w["writes"]) and env_live and ter_live and wea_live,
           "C2 sensitivity: OLD 'no experiment executes these four bodies' is FALSE",
           "stage called %s, writes %s, environment/terrain/MWeather each change the factor: %s/%s/%s"
           % (called, bool(w["writes"]), env_live, ter_live, wea_live))

    # we1: order and read site only, because the planted action row carries only +0x08
    src = open(os.path.join(RES, "check.py"), encoding="utf-8").read()
    planted = [ln.strip() for ln in src.splitlines() if ln.strip().startswith("rows[")]
    w1 = json.load(open(os.path.join(RES, "we1_result.json")))
    report(planted == ["rows[0x20 * action_id + 8] = rid"],
           "W5 we1 plants only the action row's +0x08 (so +0x13 = 0 and no element rule fires on that path)", str(planted))
    report(w1.get("ok") is True and w1.get("live_game") is False and all(w1["cases"].values()) and len(w1["cases"]) == 4,
           "W6 we1 recorded: 4/4 cases pass (WE-1 order and +0x13 read site), live_game false", ", ".join(sorted(w1["cases"])))

    # severe-weather package: WE-3 consumer side
    s = json.load(open(os.path.join(SWG, "result.json")))
    g = s.get("weather_getter") or s.get("results", {}).get("weather_getter")
    report(g is not None and all(v == [True, int(k)] for k, v in g.items()),
           "W7 recorded: 00263E20 returns [02099DAC] verbatim for 0,1,2,5 (WE-3 consumer side)", json.dumps(g))

    rerun_replays()
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
