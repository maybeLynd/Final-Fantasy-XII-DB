"""seal.py - immutable run receipts for experiments and controls (OPUS, 2026-09-29).

Workflow migration M1 1b (FF12-WORKFLOW-MIGRATION-20260928-01 section 6; acceptance matrix A04). The generic mechanism
behind FRONTIER-REQ-ORACLE-EXP201-RECEIPT-SEALING; ORACLE applies it to its experiments, OPUS to its own controls. It
never edits an experiment's files: it copies what a run consumed and produced into a write-once receipt.

THE DEFECT IT PREVENTS. A cited result file is shared and mutable: EXP-201 cites a 394-case receipt while the shared result
now holds 407 cases; S-15 rewrites S-13's result.json whenever it runs. A citation to a path is a citation to whatever the
path holds today.

A RECEIPT is a directory <store>/<run_id>/ holding copies of the driver(s), the inputs and the raw result, plus RECEIPT.json:
{run_id, sealed_at, drivers/inputs/result: {name: sha256, size}, cases: [ids], case_sources: {case: run_id},
limitations, environment, wip}. run_id = sha256 over the driver, input and result hashes and the sorted case ids, so:
  - a changed run - even one with the same case count - gets a new identity; the old receipt is never touched
  - sealing identical content twice returns the same run_id (idempotent); a different run can never land on an existing id
  - a receipt is staged in <store>/.<id>.partial and renamed into place; an interrupted seal leaves nothing visible

    seal(store, drivers, inputs, result, cases, limitations, environment=None, wip=False, case_sources=None) -> run_id
    verify(store, run_id, live=None) -> problems     ([] = the receipt is intact; `live` also compares live paths: MOVED)
    publishable(store, run_id) -> problems           (the publication gate below)

THE PUBLICATION GATE (publishable):
  - the receipt verifies (every stored copy matches its recorded hash)
  - not WIP (a draft carries no execution credit)
  - every driver's exact bytes were committed (its git blob is in the repository: a truncated or edited working copy is
    refused - parsing alone does not catch a cut that still parses), and every Python driver parses
  - the result is parseable JSON whose case ids are EXACTLY the declared cases (a missing or extra case is refused);
    a result may list cases as {"cases": {id: ...}} or {"cases": [{"id": ...}]} or [{"id": ...}]
  - cumulative reuse: a case credited through case_sources must exist in that source receipt, which must itself be
    publishable, and no case is credited twice
CLI: python seal.py verify <store> <run_id> | publishable <store> <run_id> | list <store> | --self-test
"""
import ast, datetime, hashlib, json, os, platform, shutil, sys, uuid

RECEIPT = "RECEIPT.json"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _files(d):
    """{name: path} from a list of paths (basename) or a dict."""
    if isinstance(d, dict):
        return dict(d)
    out = {}
    for p in d:
        n = os.path.basename(p)
        if n in out:
            raise ValueError("two files named %s; pass a dict of distinct names" % n)
        out[n] = p
    return out


def _env():
    mods = {}
    for m in ("capstone", "pefile", "unicorn"):
        try:
            mods[m] = getattr(__import__(m), "__version__", "present")
        except Exception:
            mods[m] = None
    return {"python": platform.python_version(), "platform": platform.platform(), "modules": mods}


def git_committed(path):
    """(blob, committed): the file's git blob hash and whether that exact blob exists in its repository's object store -
    i.e. these bytes were committed. (None, False) outside a git work tree."""
    import subprocess
    d = os.path.dirname(os.path.abspath(path))
    r = subprocess.run(["git", "-C", d, "hash-object", os.path.abspath(path)], capture_output=True, text=True)
    if r.returncode:
        return None, False
    blob = r.stdout.strip()
    ok = subprocess.run(["git", "-C", d, "cat-file", "-e", blob + "^{blob}"], capture_output=True).returncode == 0
    return blob, ok


def run_id(rec):
    """The run id a receipt's content derives: seal() names the receipt with it, and verify() recomputes it."""
    ident = json.dumps([rec["drivers"], rec["inputs"], rec["result"], rec["cases"], rec["case_sources"], rec["wip"]], sort_keys=True)
    return ("wip-" if rec["wip"] else "r-") + hashlib.sha256(ident.encode()).hexdigest()[:16]


def git_toplevel(path):
    import subprocess
    r = subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(path)), "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def blob_holds(path, blob, repo=None):
    """Whether the recorded git blob exists in the repository the driver was sealed from (the receipt's driver_repos,
    else this script's own) and holds the stored copy's bytes. Line endings are normalised on both sides: git's text
    filters depend on the path's attributes, so re-hashing the copy at the store path is not the same hash."""
    import subprocess
    repo = repo if repo and os.path.isdir(repo) else os.path.dirname(os.path.abspath(__file__))
    if not blob:
        return False
    r = subprocess.run(["git", "-C", repo, "cat-file", "-p", blob + "^{blob}"], capture_output=True)
    if r.returncode:
        return False
    norm = lambda b: b.replace(b"\r\n", b"\n")
    return norm(r.stdout) == norm(open(path, "rb").read())


def seal(store, drivers, inputs, result, cases, limitations, environment=None, wip=False, case_sources=None):
    drivers, inputs = _files(drivers), _files(inputs)
    for n, p in list(drivers.items()) + list(inputs.items()) + [("result", result)]:
        if not os.path.isfile(p):
            raise ValueError("cannot seal: %s is missing (%s)" % (n, p))
    rec = {"drivers": {n: dict(zip(("sha256", "size", "git_blob", "committed"), (sha(p), os.path.getsize(p)) + git_committed(p))) for n, p in drivers.items()},
           "inputs": {n: {"sha256": sha(p), "size": os.path.getsize(p)} for n, p in inputs.items()},
           "result": {"name": os.path.basename(result), "sha256": sha(result), "size": os.path.getsize(result)},
           "cases": sorted(set(cases)), "case_sources": dict(case_sources or {}), "limitations": limitations,
           "environment": environment or _env(), "wip": bool(wip)}
    rid = run_id(rec)
    rec["run_id"] = rid
    # where each driver's blob was found: publishable() re-checks the stored copy there (outside the run-id identity)
    rec["driver_repos"] = {n: git_toplevel(p) for n, p in drivers.items()}
    final = os.path.join(store, rid)
    if os.path.isdir(final):
        return rid                           # identical content: the same receipt, untouched
    os.makedirs(store, exist_ok=True)
    tmp = os.path.join(store, ".%s.%s.partial" % (rid, uuid.uuid4().hex[:6]))
    os.makedirs(os.path.join(tmp, "drivers")); os.makedirs(os.path.join(tmp, "inputs"))
    for sub, files in (("drivers", drivers), ("inputs", inputs)):
        for n, p in files.items():
            shutil.copyfile(p, os.path.join(tmp, sub, n))
    shutil.copyfile(result, os.path.join(tmp, "result"))
    # the copies must be the bytes that were hashed (a file changing while being sealed is refused)
    for sub, recd in (("drivers", rec["drivers"]), ("inputs", rec["inputs"])):
        for n, v in recd.items():
            if sha(os.path.join(tmp, sub, n)) != v["sha256"]:
                shutil.rmtree(tmp, ignore_errors=True); raise ValueError("cannot seal: %s changed while being sealed" % n)
    if sha(os.path.join(tmp, "result")) != rec["result"]["sha256"]:
        shutil.rmtree(tmp, ignore_errors=True); raise ValueError("cannot seal: the result changed while being sealed")
    rec["sealed_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(os.path.join(tmp, RECEIPT), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, sort_keys=True)
    try:
        os.rename(tmp, final)                # never replaces an existing receipt
    except OSError:
        shutil.rmtree(tmp, ignore_errors=True)
        if not os.path.isdir(final):
            raise
    return rid


def load(store, rid):
    p = os.path.join(store, rid, RECEIPT)
    return json.load(open(p, encoding="utf-8")) if os.path.isfile(p) else None


def verify(store, rid, live=None):
    """Problems with the stored receipt (tampered or missing copies); with live={'drivers': {...}, 'inputs': {...},
    'result': path}, also reports each live path that no longer matches as MOVED (the receipt stays valid)."""
    rec = load(store, rid)
    if rec is None:
        return ["no receipt %s" % rid]
    d, probs = os.path.join(store, rid), []
    # the name is the content (AUDITSPEC-REQ-OPUS-SEAL-RUNID-REDERIVE-0929): a result edited and its sha256 re-stamped in
    # RECEIPT.json keeps every copy consistent with the receipt, but the id no longer derives from it
    try:
        derived = run_id(rec)
    except (KeyError, TypeError) as e:
        derived = "unreadable (%s)" % e
    if derived != rid or rec.get("run_id") != rid:
        probs.append("run id %s does not derive from the receipt's content (derives %s; the receipt names %s)" % (
            rid, derived, rec.get("run_id")))
    for sub in ("drivers", "inputs"):
        for n, v in rec[sub].items():
            p = os.path.join(d, sub, n)
            if not os.path.isfile(p) or sha(p) != v["sha256"]:
                probs.append("stored %s/%s does not match the receipt" % (sub, n))
    if not os.path.isfile(os.path.join(d, "result")) or sha(os.path.join(d, "result")) != rec["result"]["sha256"]:
        probs.append("stored result does not match the receipt")
    for sub in ("drivers", "inputs"):
        for n, p in ((live or {}).get(sub) or {}).items():
            if n in rec[sub] and (not os.path.isfile(p) or sha(p) != rec[sub][n]["sha256"]):
                probs.append("MOVED: live %s %s differs from the sealed copy" % (sub, n))
    if (live or {}).get("result") and (not os.path.isfile(live["result"]) or sha(live["result"]) != rec["result"]["sha256"]):
        probs.append("MOVED: the live result differs from the sealed copy")
    return probs


def _case_ids(result_path):
    r = json.load(open(result_path, encoding="utf-8"))
    c = r.get("cases") if isinstance(r, dict) else r
    # The house harness writes a FLAT case map, {case_id: {ok, ret, trace, ...}} (EXP-201 and the other Unicorn results).
    # Accepted when every value is a record (a dict); the exact-match check against the declared cases still applies.
    # 2026-09-29: before this, all three sealed EXP-201 receipts were refused as "no cases" (OPUS's own gate was too narrow).
    if c is None and isinstance(r, dict) and r and all(isinstance(v, dict) for v in r.values()):
        return set(r)
    if isinstance(c, dict):
        return set(c)
    if isinstance(c, list):
        return set(x["id"] for x in c)
    raise ValueError("no cases in the result")


def publishable(store, rid, _seen=None):
    rec = load(store, rid)
    if rec is None:
        return ["no receipt %s" % rid]
    probs = [p for p in verify(store, rid) if not p.startswith("MOVED")]
    if rec.get("wip"):
        probs.append("WIP receipt: no execution credit")
    for n, v in rec["drivers"].items():
        # re-checked, not trusted: the recorded blob must exist in the repository and hold the stored copy's bytes
        if not blob_holds(os.path.join(store, rid, "drivers", n), v.get("git_blob"), (rec.get("driver_repos") or {}).get(n)):
            v = dict(v, committed=False)
            probs.append("driver %s is not a committed source (git blob %s not in the repository): a truncated or unpublished "
                         "working copy carries no execution credit" % (n, v.get("git_blob")))
        if n.endswith(".py"):
            try:
                ast.parse(open(os.path.join(store, rid, "drivers", n), encoding="utf-8").read())
            except (SyntaxError, UnicodeDecodeError, OSError) as e:
                probs.append("driver %s does not parse (truncated?): %s" % (n, e))
    own = set(rec["cases"]) - set(rec["case_sources"])
    try:
        got = _case_ids(os.path.join(store, rid, "result"))
    except (ValueError, KeyError, TypeError, OSError) as e:
        return probs + ["result is not a parseable case list: %s" % e]
    if got != own:
        miss, extra = sorted(own - got), sorted(got - own)
        probs.append("case map mismatch: declared-but-absent %s, present-but-undeclared %s" % (miss[:5], extra[:5]))
    seen = set(_seen or ())
    for c, src in rec["case_sources"].items():
        if c in seen:
            probs.append("case %s credited twice" % c); continue
        seen.add(c)
        srec = load(store, src)
        if srec is None or c not in srec["cases"]:
            probs.append("case %s: source receipt %s does not carry it" % (c, src)); continue
        sp = publishable(store, src, _seen=seen - {c})
        if sp:
            probs.append("case %s: source receipt %s is not publishable (%s)" % (c, src, sp[0]))
    return probs


def main(argv):
    if "--self-test" in argv:
        import subprocess
        return subprocess.call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_seal.py")])
    if len(argv) >= 3 and argv[1] == "list":
        for rid in sorted(os.listdir(argv[2])):
            r = load(argv[2], rid)
            if r: print(rid, r["sealed_at"], "%d cases" % len(r["cases"]), "WIP" if r["wip"] else "")
        return 0
    if len(argv) >= 4 and argv[1] in ("verify", "publishable"):
        probs = (verify if argv[1] == "verify" else publishable)(argv[2], argv[3])
        print("OK" if not probs else "REFUSED: " + "; ".join(probs)); return 0 if not probs else 1
    print(__doc__.split("CLI:")[1].strip()); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
