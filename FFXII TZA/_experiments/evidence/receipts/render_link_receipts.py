"""render_link_receipts.py - SWE2-ORACLE's application of gfz-scripts/seal.py (OPUS, 475456436) to ASTRA's committed
render-review link-closure runs (2026-10-03; Claude stand-in operating SWE2-ORACLE).

ASTRA-REQ-ORACLE-SEAL-COMMITTED-RENDER-LINK-1003 and ASTRA-REQ-ORACLE-SEAL-RENDER-PATH-CONTROL-1003. They follow
SWE2-ORACLE's disposition 76bf92900, which found the earlier runs unsealable (drivers under ignored work/; no case ids).
ASTRA committed the drivers (88d435193, c7319b1b8) and re-ran from the tracked copies. This seals three write-once
receipts into ./store/ with seal.py. It does not re-implement it.

  PREP   drivers-v2/prepare.py                          15 cases  prepared-committed-01/result.json
  CTRL   drivers-v2/control.py + drivers-v2/prepare.py   3 cases  controls-committed-01/result.json
         (the controls execute prepare.py; each case's driver_sha256 must be the sealed prepare.py)
  PATH   render-review-path-launcher/launch.py + drivers-v2/control-publisher-path.py + drivers-v2/publisher-driver.py
                                                        2 cases  publisher-path-control-committed-02.json
         a labelled synthetic private invocation: no claim, board or database write, no FF12 execution credit

Each driver's sha256 is fixed below to the identity ASTRA named, and each must be a committed blob (seal.publishable
re-checks it). PREP's inputs are the old manifest and the referent origins its result names. The run's status, stdout
and stderr hashes go into the receipt's environment record (outside the run id, kept for provenance).

NOT SEALED, and this script refuses to seal it: the first committed path-control run (committed-path-controls-01, and
render-review-path-launcher/failed-committed-path-01.*) is INVALID_BEFORE_TEST (exit 1, no result file). The check
mode's negative control asserts that seal() refuses it. These receipts certify delivery prerequisites only: the
reviewer script and output copies stay payload (FABLE's corroboration, not ASTRA executions), and nothing here is
independent scientific acceptance.

Modes
  seal    seal the three receipts (idempotent: identical content returns the same run id, untouched); print run ids
  check   regression: each receipt exists, verify() is intact, publishable() returns nothing, its result hash and case
          ids equal the fixed values, the cross-identities hold (CTRL cases name the sealed prepare.py, PATH names the
          sealed controller and producer); negative control: sealing the invalid run 01 is refused
"""
import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import seal  # noqa: E402

STORE = os.path.join(HERE, "store")
EV = os.path.join(REPO, "Database", "FFXII TZA", "_experiments", "evidence")
D2 = os.path.join(EV, "render-review-link-closure", "drivers-v2")
LAUNCH = os.path.join(EV, "render-review-path-launcher", "launch.py")
W = os.path.join(REPO, "Database", "Tools", "work", "ASTRA", "runtime-residue-method-retriage",
                 "render-review-link-closure")
OLD_MANIFEST = os.path.join(EV, "render-review-phase-qualification", "manifest.json")

DRIVERS = {  # name -> (path, sha256 ASTRA named in its request)
    "prepare.py": (os.path.join(D2, "prepare.py"), "d10cae7b1f4459cf695f0218b9b3a13822a1147d8eda3284a13f8bb80f5e5654"),
    "control.py": (os.path.join(D2, "control.py"), "2cf69ccb1ad3cfd8127db1dc75d6afdb585ebe3cce808ad512246bccd49de84a"),
    "control-publisher-path.py": (os.path.join(D2, "control-publisher-path.py"),
                                  "aae9e61c9cbe59097a3af5a897a361127404abc840d907899a8a18fb7d953699"),
    "publisher-driver.py": (os.path.join(D2, "publisher-driver.py"),
                            "5c1b458faeafcc4b206d30ba1ce660ceebd0e8dc54834f974931445490a6eb18"),
    "launch.py": (LAUNCH, "e9d22fdd227b884ddca02981d53750fc3c951b837aaff51c9260c7475909bf2a"),
}
RUNS = {
    "PREP": dict(drivers=["prepare.py"], result=os.path.join(W, "prepared-committed-01", "result.json"),
                 run="committed-prepare-01", ncases=15,
                 limitations=["offline publication closure; no game execution and no new scientific result",
                              "the reviewer scripts/outputs in additions[] are payload (FABLE corroboration), not ASTRA "
                              "executions", "not independent scientific acceptance"]),
    "CTRL": dict(drivers=["control.py", "prepare.py"], result=os.path.join(W, "controls-committed-01", "result.json"),
                 run="committed-controls-01", ncases=3,
                 limitations=["three actual CLI refusal controls of prepare.py (missing referent, conflicting library, "
                              "changed old member); each must exit 1 with no output",
                              "not independent scientific acceptance"]),
    "PATH": dict(drivers=["launch.py", "control-publisher-path.py", "publisher-driver.py"],
                 result=os.path.join(W, "publisher-path-control-committed-02.json"),
                 run="committed-path-controls-02", ncases=2,
                 limitations=["labelled synthetic private invocation: no actual claim, board or database write",
                              "no FF12 execution credit", "the failed first run (committed-path-controls-01) is "
                              "INVALID_BEFORE_TEST and is not sealed or promoted by this receipt",
                              "not independent scientific acceptance"]),
}
INVALID = os.path.join(W, "publisher-path-control-committed-01.json")   # never written: the run failed before test


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def case_ids(p):
    return [c["id"] for c in json.load(open(p, encoding="utf-8"))["cases"]]


def run_env(run):
    env = seal._env()
    env["run_artifacts"] = {}
    for ext in ("status.json", "stdout", "stderr"):
        p = os.path.join(W, "%s.%s" % (run, ext))
        env["run_artifacts"][ext] = {"sha256": sha(p), "size": os.path.getsize(p)} if os.path.exists(p) else None
    st = json.load(open(os.path.join(W, run + ".status.json"), encoding="utf-8"))
    env["run_status"] = {k: st.get(k) for k in ("driver_sha256", "interpreter_sha256", "terminal", "exit", "exception")}
    return env


def preflight(name, spec):
    probs = []
    for d in spec["drivers"]:
        p, want = DRIVERS[d]
        if sha(p) != want:
            probs.append("%s: driver %s sha256 %s != named %s" % (name, d, sha(p)[:12], want[:12]))
        blob, ok = seal.git_committed(p)
        if not ok:
            probs.append("%s: driver %s is not a committed blob (%s)" % (name, d, blob))
    st = json.load(open(os.path.join(W, spec["run"] + ".status.json"), encoding="utf-8"))
    if not (st.get("terminal") is True and st.get("exit") == 0 and st.get("exception") is None):
        probs.append("%s: run status is not terminal exit 0: %s" % (name, {k: st.get(k) for k in ("terminal", "exit")}))
    if st.get("driver_sha256") != DRIVERS[spec["drivers"][0]][1]:
        probs.append("%s: run status names driver %s, not the sealed one" % (name, str(st.get("driver_sha256"))[:12]))
    r = json.load(open(spec["result"], encoding="utf-8"))
    if len(r["cases"]) != spec["ncases"]:
        probs.append("%s: %d cases, expected %d" % (name, len(r["cases"]), spec["ncases"]))
    if name == "PREP" and r.get("driver_sha256") != DRIVERS["prepare.py"][1]:
        probs.append("PREP: result names a different prepare.py")
    if name == "CTRL":
        if r.get("controller_sha256") != DRIVERS["control.py"][1]:
            probs.append("CTRL: result names a different control.py")
        for c in r["cases"]:
            if c.get("driver_sha256") != DRIVERS["prepare.py"][1]:
                probs.append("CTRL %s: ran a different prepare.py" % c["id"])
            if not (c.get("exit") == 1 and c.get("diagnostic_observed") and c.get("result_absent")
                    and c.get("output_absent")):
                probs.append("CTRL %s: not a clean refusal" % c["id"])
    if name == "PATH":
        if r.get("controller_sha256") != DRIVERS["control-publisher-path.py"][1]:
            probs.append("PATH: result names a different controller")
        if r.get("producer_sha256") != DRIVERS["publisher-driver.py"][1]:
            probs.append("PATH: result names a different producer")
        if not r.get("status", "").endswith("PASS"):
            probs.append("PATH: status %s" % r.get("status"))
    return probs


def inputs_for(name):
    if name != "PREP":
        return {}
    r = json.load(open(RUNS["PREP"]["result"], encoding="utf-8"))
    ins = {"old-manifest.json": OLD_MANIFEST}
    for a in r["additions"]:
        for o in a.get("origins", []):
            # short stored names (deep paths hit MAX_PATH): <review dir minus its fixed prefix/suffix>__<file>
            d, f = o["path"].rsplit("/", 2)[-2:]
            short = d.replace("fable-review-astra-render-", "").replace("-1002", "")
            ins["%s__%s" % (short, f)] = os.path.join(REPO, o["path"])
    return ins


def do_seal():
    out = {}
    for name, spec in RUNS.items():
        probs = preflight(name, spec)
        if probs:
            print("REFUSED %s:" % name)
            for p in probs:
                print("  " + p)
            out[name] = None
            continue
        rid = seal.seal(STORE, {d: DRIVERS[d][0] for d in spec["drivers"]}, inputs_for(name), spec["result"],
                        case_ids(spec["result"]), spec["limitations"], environment=run_env(spec["run"]))
        out[name] = rid
        print("%s %s" % (name, rid))
    return out


FIXED = {}   # filled after the first seal: name -> (run id, result sha256)
FIXED_FILE = os.path.join(HERE, "render_link_receipts.ids.json")


def do_check():
    fails = []
    fixed = json.load(open(FIXED_FILE, encoding="utf-8"))

    def chk(n, ok, d):
        print("%-24s %s %s" % (n, "PASS" if ok else "FAIL", d))
        if not ok:
            fails.append(n)
    for name, spec in RUNS.items():
        rid, rsha = fixed[name]["run_id"], fixed[name]["result_sha256"]
        rec = seal.load(STORE, rid)
        chk("R-%s-exists" % name, rec is not None, rid)
        if rec is None:
            continue
        v = seal.verify(STORE, rid)
        chk("R-%s-verify" % name, not v, "intact" if not v else v[0])
        p = seal.publishable(STORE, rid)
        chk("R-%s-publishable" % name, not p, "no refusal" if not p else p[0])
        chk("R-%s-result" % name, rec["result"]["sha256"] == rsha and len(rec["cases"]) == spec["ncases"],
            "%s, %d cases" % (rec["result"]["sha256"][:12], len(rec["cases"])))
        chk("R-%s-drivers" % name, sorted(rec["drivers"]) == sorted(spec["drivers"]) and all(
            rec["drivers"][d]["sha256"] == DRIVERS[d][1] for d in spec["drivers"]), ", ".join(sorted(rec["drivers"])))
    # negative control: the invalid first path-control run has no result and must not be sealable
    try:
        seal.seal(os.path.join(HERE, ".neg-control-never-created"), {d: DRIVERS[d][0] for d in RUNS["PATH"]["drivers"]},
                  {}, INVALID, ["missing-review-stops-before-writes"], ["negative control"])
        refused = False
    except ValueError as e:
        refused = "missing" in str(e)
    chk("N-invalid-run-01", refused and not os.path.exists(INVALID)
        and not os.path.isdir(os.path.join(HERE, ".neg-control-never-created")),
        "seal() refuses committed-path-controls-01 (no result file)")
    print("FAILS %d" % len(fails))
    return len(fails)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode == "seal":
        ids = do_seal()
        if all(ids.values()):
            json.dump({n: {"run_id": ids[n], "result_sha256": sha(RUNS[n]["result"])} for n in RUNS},
                      open(FIXED_FILE, "w", encoding="utf-8"), indent=1)
            print("ids written")
        sys.exit(0 if all(ids.values()) else 1)
    sys.exit(1 if do_check() else 0)
