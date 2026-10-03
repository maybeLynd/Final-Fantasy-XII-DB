"""check_s22_recipes.py - FABLE, 2026-10-03, on SWE2-AUDIT-SPEC's L2 expansion (S-22, stale section 13).

Claim checked: CONTRACT-weapon-recipes.md section 13 reads "None. No experiment executes this resolver." Two
recorded native replays execute it (and the RW-5 gate's two steps). This check:
  - reads the resolver's extent at the bytes: the loop's hook site 003863D0 lies in 00385F60's chained .pdata (S1);
  - reads what each recorded result asserts (R*), and asserts the committed list's cut-short from the record (R3);
  - re-runs both packages from a temp copy and compares every result file's md5 with the committed one (RR*).
Controls:
  C1 (sensitivity, stale text): the old "no experiment executes this resolver" must FAIL against the record.
  C2 (sensitivity, reading): "the committed path runs every slot of the second list" predicts called == committed
      for recipes 6 and 2; on the record it must FAIL.
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

DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CAND = os.path.abspath(os.path.join(HERE, ".."))
RES = os.path.join(CAND, "s22-opus-replay-recipe-resolver")
SWG = os.path.join(CAND, "s22-opus-replay-severe-weather-gate")
fails = 0
REPLAYS = {
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
    tmp = tempfile.mkdtemp(prefix="fable_l2exp_s22r_")
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


def expected_prefix(committed, flags):
    """What the loop must call if it stops right after the first step that leaves the flag at 1."""
    for k, f in enumerate(flags):
        if f == 1:
            return committed[:k + 1]
    return committed


def main():
    head = os.popen('git -C "%s" rev-parse --short HEAD' % DB).read().strip()
    print("check_s22_recipes.py  HEAD %s" % head)
    img = Img.load()

    pd = img.pdata(0x003863D0)
    ents, ok = img.pdata_cover(0x00385F60, pd[1])
    call = next(img.cs.disasm(img.read(0x003863D0, 8), 0x003863D0, 1))
    report(ok and all(r == 0x00385F60 for _, _, _, r in ents) and call.mnemonic == "call" and "0x1dda5c0" in call.op_str,
           "S1 the hook site 003863D0 (call [rbx+rax*8+0x1DDA5C0]) lies in the resolver 00385F60 (chained .pdata)",
           " ".join("%08X-%08X" % (a, b) for a, b, _, _ in ents))

    r = json.load(open(os.path.join(RES, "result.json")))
    res = r["results"]
    report(r["ok"] is True and res["RW1_table_extent_static"]["pass_"] and res["RW2_RW4_static"]["pass_"],
           "R1 recorded: RW-1 extent and RW-2/RW-4 decode pass (static, read from the mapped image)",
           "next qword %s" % res["RW1_table_extent_static"]["next_qword"])
    report(res["RW2_committed_list_only"]["pass_"] is True and res["RW2_committed_list_only"]["failing"] == [],
           "R2 recorded and ASSERTED in the package: the committed path calls only the second list (39 calls none)",
           res["RW2_committed_list_only"]["note"][:90])
    cases = res["cases"]
    done = {k: c for k, c in cases.items() if c["ok"]}
    good = all(c["slots_called"] == expected_prefix(c["committed"], c["flag_after_each"]) for c in done.values())
    cut = {k: c for k, c in done.items() if 1 in c["flag_after_each"]}
    report(good and sorted(cut) == ["2", "6"] and cut["6"]["slots_called"] == [3, 4] and cut["2"]["slots_called"] == [20, 30, 32, 40],
           "R3 asserted here from the record: every completed run calls its committed list up to the first step leaving [02AEDFB8]=1",
           "completed %s; cut short: 6 -> %s, 2 -> %s" % (sorted(done, key=int), cut.get("6", {}).get("slots_called"),
                                                         cut.get("2", {}).get("slots_called")))
    report(res["loop_early_exit_observed"]["pass_"] is True and "observed" in res["loop_early_exit_observed"]["note"],
           "R4 the package's own early-exit case is a recorded observation (literal pass), not an assertion",
           res["loop_early_exit_observed"]["note"][:70])
    c25 = cases.get("25", {})
    report(c25.get("ok") is False and c25.get("slots_called") == [29] and c25.get("stopped_at") == ["0000001C"],
           "R5 not covered: recipe 25 (bow) stops in its first committed slot 29 at an unplanted read (0x1C)",
           "ok %s called %s stopped_at %s" % (c25.get("ok"), c25.get("slots_called"), c25.get("stopped_at")))

    s = json.load(open(os.path.join(SWG, "result.json")))
    st = s["steps"]
    want = {"clear_class2": (80, 50), "bit4_class2": (100, 100), "clear_class1": (100, 100), "clear_class0": (100, 100),
            "others_set_class2": (80, 50), "bit4_class1": (100, 100)}
    got = {k: (st["step35"][k][1], st["step36"][k][1]) for k in want}
    report(s["ok"] is True and got == want and all(st[x][k][0] for x in st for k in st[x]),
           "R6 recorded and asserted: RW-5 gate on steps 35/36 (+0x1A bit 0x04 clear and class 2 scale 100 -> 80 / 50)",
           json.dumps(got))

    called_any = any(c["slots_called"] for c in cases.values())
    report(called_any and ok, "C1 sensitivity: OLD 'no experiment executes this resolver' is FALSE",
           "recorded steps called through 003863D0 in %d of %d cases" % (sum(1 for c in cases.values() if c["slots_called"]), len(cases)))
    every = all(cut[k]["slots_called"] == cut[k]["committed"] for k in cut)
    report(not every, "C2 sensitivity: 'the committed path runs every slot' predicts called == committed for 6 and 2; FALSE",
           "6: %d of %d, 2: %d of %d" % (len(cut["6"]["slots_called"]), len(cut["6"]["committed"]),
                                          len(cut["2"]["slots_called"]), len(cut["2"]["committed"])))

    rerun_replays()
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
