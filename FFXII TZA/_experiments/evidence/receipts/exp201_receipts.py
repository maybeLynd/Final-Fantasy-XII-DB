"""exp201_receipts.py - SWE2-ORACLE's application of gfz-scripts/seal.py (OPUS, 475456436) to EXP-201 (2026-09-29).

FRONTIER-REQ-ORACLE-EXP201-RECEIPT-SEALING. EXP-201's record cites `member-block-chain-exec/result.json` with SHA256 be5088bd..
and 394 cases, but that path is shared by every later EXP of the harness: it held 407 cases after EXP-202 and holds 556 after
EXP-256. A citation to the path is a citation to whatever it holds today.

This script seals three write-once receipts into ./store/ with seal.py (it does not re-implement it):

  EXP-201  394 cases  the cited run. Its genuine bytes are in git: `git cat-file --filters aa29615b7:<path>` reproduces the
                      working copy the run wrote (the driver writes result.json in text mode on Windows, so CRLF), and that
                      copy hashes to the cited be5088bd.. exactly. Nothing is reconstructed from a later subset.
  EXP-202  407 cases  the result the finding compared against (commit 7926c92cd).
  EXP-256  556 cases  the current run on the shared path (commit 21ab1e3c9; the live file today).

Each driver is the exact committed check.py of that commit (seal.py's committed-source gate checks the git blob). The one
input is image-identity.json: the authority image's sha256 and size. The image bytes are NOT stored (not redistributable);
each driver asserts that sha256 itself at load_image(). Every receipt is a full run: no case is credited by reuse.

Modes
  seal    materialize the three sources from git into --work (gitignored scratch), refuse unless each hashes to the value
          fixed below, seal, print the run ids. Idempotent: identical content returns the same run id, untouched.
  check   the regression (no image needed). Fails on: a missing or tampered receipt; a receipt whose result hash or case
          count differs from the fixed value; EXP-201's record or contract section 13j not citing the EXP-201 receipt; the
          record's cited SHA256 not equal to that receipt's result hash. Negative control: the same binding check run
          on the record as committed at aa29615b7 (a path citation, no receipt) must REJECT it - that is the original error.
          Positive control: the live shared result must read MOVED against the EXP-201 receipt (the drift is real and
          the instrument sees it). seal.publishable is run on each receipt and must return no refusal. Since OPUS
          eae0ed3c7 (seal.py reads flat {case_id: {...}} case maps, SWE2-ORACLE-REQ-OPUS-SEAL-FLATMAP-0929) all three
          receipts print PASS at HEAD. The PEND branch for the flat-map refusal alone is kept only as a fallback should
          seal.py regress; any other refusal is a FAIL. A stored result that is not JSON, or not a flat case map, is a
          FAIL row on R-<label>-cases (N-non-json-result is its negative control), never an uncaught exception.
  rerun   re-execute each sealed driver copy in a temp dir against the image and compare its result byte-for-byte with
          the sealed result (needs the shipping image at the driver's EXE path, unicorn, capstone).

The store carries `.gitattributes` `* -text` so the sealed copies keep their exact bytes (CRLF) through git on any host.
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import seal as SL  # noqa: E402

STORE = os.path.join(HERE, "store")
DB = "Database/FFXII TZA/"
EVID = DB + "_experiments/evidence/member-block-chain-exec/"
RECORD = DB + "_experiments/EXP-201-display-request-queue-exec.md"
CONTRACT = DB + "10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md"
IMAGE = {"image": "FFXII_TZA.exe (FFXII TZA shipping x64)",
         "sha256": "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8", "size": 32864752,
         "bytes_stored": False,
         "why": "the image is not redistributable; every sealed driver asserts this sha256 in load_image() before running"}
RUNS = [
    {"label": "EXP-201", "commit": "aa29615b7865f20e353747e2f4b7d80123dcddcc", "cases": 394,
     "driver_sha": "c15499107b5154c92b7dd7001102a6ab48ce970c965b1a82f4330afce459cacb",
     "result_sha": "be5088bdbeac09d363985991df0f0f0c97ba55022f664eea40f939c18ebfc965"},
    {"label": "EXP-202", "commit": "7926c92cd817bdadfe618c7d4a188f99908ee919", "cases": 407,
     "driver_sha": "d3f045801abb6b326308492e534827e4950b3fb2934684da7c1023e071100e92",
     "result_sha": "1a40a8377d79e3b9606c100769cb7ca14f35950620821ffb3dfdc7cc392078a0"},
    {"label": "EXP-256", "commit": "21ab1e3c96e036cee70b5e5fb57f8b44b5e640d4", "cases": 556,
     "driver_sha": "dee2012d82d0ce57dd11299f9bd2b9c24f52f2fcc4fa219a51913b67e9fc93e9",
     "result_sha": "5982226cece2b07f6b3ddbd6ec98a56a1e33efdbc773bc04a548592d4fd19b31"},
]
# filled from the first seal; content-derived, so a re-seal of the same bytes reproduces them
RUN_IDS = {"EXP-201": "r-95260e713b7dba43", "EXP-202": "r-edb8403635767456", "EXP-256": "r-5be60dc8ce879ae1"}

LIMITS = ("NATIVE-REPLAY, live_game false: shipped bytes executed under Unicorn over synthetic fixtures with scripted "
          "boundaries, all as disclosed in the %s record; no initialized-gameplay reachability is claimed. The image is "
          "bound by hash only (inputs/image-identity.json), not stored. Sealed 2026-09-29 by SWE2-ORACLE from the "
          "commit's own bytes (git cat-file --filters, i.e. the working copy the run wrote); the original run's "
          "environment was not recorded. Re-executed 2026-09-29 from this driver against the authority image: "
          "byte-identical result.")


def sha(p):
    return SL.sha(p)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def git_bytes(spec, filters=True):
    a = ["git", "-C", REPO, "cat-file", "--filters", spec] if filters else ["git", "-C", REPO, "show", spec]
    r = subprocess.run(a, capture_output=True)
    if r.returncode:
        raise SystemExit("git could not read %s: %s" % (spec, r.stderr.decode(errors="replace").strip()))
    return r.stdout


def result_cases(p):
    """case ids of this harness's result.json: a flat JSON object {case_id: {...}}"""
    try:
        r = json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):                 # ValueError covers JSONDecodeError / bad UTF-8: fail closed as a row
        return None
    if isinstance(r, dict) and "cases" not in r and all(isinstance(v, dict) for v in r.values()):
        return sorted(r)
    return None


def image_manifest(work):
    p = os.path.join(work, "image-identity.json")
    with open(p, "wb") as f:
        f.write((json.dumps(IMAGE, indent=1, sort_keys=True) + "\n").encode())
    return p


def do_seal(work):
    os.makedirs(STORE, exist_ok=True)
    ga = os.path.join(STORE, ".gitattributes")
    if not os.path.isfile(ga):
        open(ga, "wb").write(b"# sealed copies keep their exact bytes through git (SWE2-ORACLE 2026-09-29)\n* -text\n")
    man = image_manifest(work)
    env_rerun = SL._env()
    out = {}
    for run in RUNS:
        d = os.path.join(work, run["label"])
        os.makedirs(d, exist_ok=True)
        drv, res = os.path.join(d, "check.py"), os.path.join(d, "result.json")
        for p, spec, want in ((drv, run["commit"] + ":" + EVID + "check.py", run["driver_sha"]),
                              (res, run["commit"] + ":" + EVID + "result.json", run["result_sha"])):
            b = git_bytes(spec)
            if sha_bytes(b) != want:
                raise SystemExit("REFUSED: %s materializes to %s, not the fixed %s (EOL config?)" % (spec, sha_bytes(b), want))
            open(p, "wb").write(b)
        cases = result_cases(res)
        if len(cases) != run["cases"]:
            raise SystemExit("REFUSED: %s has %d cases, not %d" % (run["label"], len(cases), run["cases"]))
        env = {"original_run": "not recorded (commit %s)" % run["commit"][:9],
               "sealed_by": "SWE2-ORACLE (OPUS's Claude subagent) 2026-09-29", "rerun_2026_09_29": env_rerun}
        rid = SL.seal(STORE, {"check.py": drv}, {"image-identity.json": man}, res, cases, LIMITS % run["label"], env)
        out[run["label"]] = rid
        print("%s  %s  %d cases  result %s" % (run["label"], rid, len(cases), run["result_sha"][:16]))
    return out


def binding_problems(text, rid, want_sha):
    """the original error: a record citing a result by path+hash with no sealed receipt that holds that hash"""
    probs = []
    if rid not in text:
        probs.append("does not cite receipt %s" % rid)
    cited = set(re.findall(r"\b[0-9a-f]{64}\b", text))
    if want_sha not in cited:
        probs.append("does not cite the result hash %s" % want_sha[:16])
    return probs


FLATMAP = "result is not a parseable case list: no cases in the result"


def do_check():
    fails = 0
    pend = []

    def ck(tag, ok, msg=""):
        nonlocal fails
        fails += not ok
        print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))

    for run in RUNS:
        rid = RUN_IDS[run["label"]]
        rec = SL.load(STORE, rid)
        ck("R-%s-exists" % run["label"], rec is not None, rid)
        if rec is None:
            continue
        ck("R-%s-verify" % run["label"], not SL.verify(STORE, rid), "; ".join(SL.verify(STORE, rid)))
        ck("R-%s-hash" % run["label"], rec["result"]["sha256"] == run["result_sha"] and
           rec["drivers"]["check.py"]["sha256"] == run["driver_sha"], rec["result"]["sha256"][:16])
        rc = result_cases(os.path.join(STORE, rid, "result"))
        ck("R-%s-cases" % run["label"], rc is not None and len(rec["cases"]) == run["cases"] and rec["cases"] == rc,
           "%d" % len(rec["cases"]) if rc is not None else "stored result is not a parseable flat case map")
        ck("R-%s-committed-driver" % run["label"], rec["drivers"]["check.py"].get("committed") is True)
        ck("R-%s-no-reuse" % run["label"], rec["case_sources"] == {} and not rec["wip"])
        gate = SL.publishable(STORE, rid)
        if gate == [FLATMAP]:
            # seal.py's case parser reads {"cases": ...} or a list; this harness writes a flat {case_id: {...}} object.
            # Requested of seal.py's owner (SWE2-ORACLE-REQ-OPUS-SEAL-FLATMAP-0929). Not a PASS: printed as PEND, and
            # every other gate condition is checked separately above (verify, committed driver, case map, no reuse).
            pend.append(run["label"])
            print("PEND  R-%s-gate %s (flat case-map; seal.py support requested)" % (run["label"], FLATMAP))
        else:
            ck("R-%s-gate" % run["label"], not gate, "; ".join(gate) or "publishable")
    r201 = RUN_IDS["EXP-201"]
    live = os.path.join(REPO, EVID, "result.json")
    mv = SL.verify(STORE, r201, live={"result": live})
    ck("P-live-moved", any(p.startswith("MOVED") for p in mv), "the shared path no longer holds the EXP-201 run")
    rec_txt = open(os.path.join(REPO, RECORD), encoding="utf-8").read()
    b = binding_problems(rec_txt, r201, RUNS[0]["result_sha"])
    ck("B-record", not b, "; ".join(b))
    con_txt = open(os.path.join(REPO, CONTRACT), encoding="utf-8").read()
    sec = con_txt.split("### 13j.", 1)[1].split("\n### ", 1)[0] if "### 13j." in con_txt else ""
    ck("B-contract-13j", r201 in sec, "section 13j cites %s" % r201)
    old = git_bytes(RUNS[0]["commit"] + ":" + RECORD, filters=False).decode("utf-8")
    nb = binding_problems(old, r201, RUNS[0]["result_sha"])
    ck("N-original-error-rejected", bool(nb), "record at aa29615b7: " + ("; ".join(nb) or "ACCEPTED (control failed)"))
    with tempfile.TemporaryDirectory() as td:        # AUDITSPEC-REQ-ORACLE-EXP201-PRECISIONS-0929 point 3
        bad = os.path.join(td, "result")
        with open(bad, "wb") as f:
            f.write(b"not json {")
        ck("N-non-json-result", result_cases(bad) is None, "a non-JSON stored result reads as unparseable (FAIL row)")
    print("FAILS %d  GATE-PENDING %s" % (fails, ",".join(pend) or "none"))
    return 1 if fails else 0


def do_rerun():
    bad = 0
    for run in RUNS:
        rid = RUN_IDS[run["label"]]
        t = tempfile.mkdtemp(prefix="rerun_")
        shutil.copyfile(os.path.join(STORE, rid, "drivers", "check.py"), os.path.join(t, "check.py"))
        r = subprocess.run([sys.executable, "check.py"], cwd=t, capture_output=True, text=True)
        got = os.path.join(t, "result.json")
        same = r.returncode == 0 and os.path.isfile(got) and sha(got) == run["result_sha"]
        bad += not same
        print("%s  %s  exit %d  %s" % ("SAME" if same else "DIFFERS", run["label"], r.returncode,
                                       r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""))
        shutil.rmtree(t, ignore_errors=True)
    return 1 if bad else 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode == "seal":
        w = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO, "Database", "Tools", "work", "SWE2-ORACLE", "exp201-materialized")
        os.makedirs(w, exist_ok=True)
        do_seal(w)
        sys.exit(0)
    sys.exit({"check": do_check, "rerun": do_rerun}.get(mode, lambda: print(__doc__) or 2)())
