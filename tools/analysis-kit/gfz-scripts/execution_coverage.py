#!/usr/bin/env python3
"""execution_coverage.py — run every sealed Unicorn evidence suite under the
execcov shim and aggregate function-level execution coverage.

OPUS-REQ-ORACLE-EXECUTION-COVERAGE-INSTRUMENT-0929-R.

For each evidence dir containing check.py + result.json where check.py imports
unicorn, the driver:

  1. records md5(result.json) — the run's sealed receipt,
  2. re-runs `python check.py` with PYTHONPATH=<execcov shim dir> and
     EXECCOV_OUT=<out>/runs/<name>.json,
  3. verifies the rewritten result.json is byte-identical (receipt reproduced;
     a mismatch is reported and the original restored),
  4. folds the coverage JSON into runs/<name>.json (run, receipt, status) and
     runs/<name>.tsv (entry, class),

then writes execution-coverage.tsv: entry, name, owner, executed (yes/NOT),
runs_executed, runs_observed, classes, run ids, receipt ids, mutated_runs.
Only runs whose receipt reproduced (status ok) contribute.

then seals the output (SEAL.json) on a full sweep or --aggregate-only.

usage: execution_coverage.py [--jobs N] [--dirs DIR [DIR...]] [--list]
       [--out <candidate dir>] [--timeout SECONDS] [--aggregate-only]

Run it with the interpreter the suites were sealed under (system Python 3.14,
unicorn 2.1.4); the analysis venv's unicorn 2.1.0 rejects mt-twist-simd-exec's
SIMD instructions.
"""
import argparse, glob, hashlib, json, os, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
EVID = os.path.join(ROOT, "Database", "FFXII TZA", "_experiments", "evidence")
SANDBOX = os.path.join(ROOT, "Database", "FFXII TZA", "_experiments",
                       "_cov_runs")
SHIM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "execcov")
CAT = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
OUT = os.path.join(ROOT, "Database", "FFXII TZA", "_index", "candidates",
                   "oracle-execution-coverage-1002")
PY = sys.executable
EXECUTED = ("returned", "faulted", "returned+faulted")  # shim's executed classes

# Write-once suites assert their own outputs absent ('preserve prior run'
# style). They cannot re-run in place; they re-run in a same-depth sandbox so
# `Path(__file__).parents[N]` anchors (e.g. the vendored-unicorn insert) keep
# resolving.
FILE_EXISTS = re.compile(r"FileExistsError: .*?File exists: '([^']+)'")
SIBLING = re.compile(r"""HERE\.parent\s*/\s*['"]([^'"/\\]+)['"]""")
WRITE_ONCE = re.compile(r"assert\s+not\s+\(HERE/|assert\s+not\s+\w+\.exists\(\)")


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def suites():
    for d in sorted(os.listdir(EVID)):
        dd = os.path.join(EVID, d)
        chk, res = os.path.join(dd, "check.py"), os.path.join(dd, "result.json")
        if not (os.path.isdir(dd) and os.path.exists(chk) and os.path.exists(res)):
            continue
        try:
            src = open(chk, encoding="utf8", errors="replace").read()
        except OSError:
            continue
        if "unicorn" not in src or "emu_start" not in src:
            continue
        yield d, dd, src


def sandbox_copy(name, dd):
    sb = os.path.join(SANDBOX, name)
    if os.path.exists(sb):
        shutil.rmtree(sb)
    shutil.copytree(dd, sb, ignore=shutil.ignore_patterns("__pycache__"))
    for pat in ("result.json", "manifest.json", "disassembly.txt", "*.bin"):
        for f in glob.glob(os.path.join(sb, pat)):
            os.remove(f)
    # sibling suites a harness imports from (EXP-040: HERE.parent/'EXP-032-...')
    src = open(os.path.join(dd, "check.py"), encoding="utf8",
               errors="replace").read()
    for sib in set(SIBLING.findall(src)):
        s_src, s_dst = os.path.join(EVID, sib), os.path.join(SANDBOX, sib)
        if os.path.isdir(s_src) and not os.path.exists(s_dst):
            shutil.copytree(s_src, s_dst,
                            ignore=shutil.ignore_patterns("__pycache__"))
    return sb


def invoke(dd, env, timeout, check_py):
    p = subprocess.run([PY, check_py], cwd=dd, env=env,
                       capture_output=True, timeout=timeout)
    return p.returncode, p.stderr.decode("utf8", "replace")


def run_one(name, dd, src, outdir, timeout):
    runs = os.path.join(outdir, "runs")
    os.makedirs(runs, exist_ok=True)
    res = os.path.join(dd, "result.json")
    cov = os.path.join(runs, name + ".cov.json")
    orig_bytes = open(res, "rb").read()
    rec = {"run": name, "receipt_md5": hashlib.md5(orig_bytes).hexdigest(),
           "status": "ok"}
    env = dict(os.environ, PYTHONPATH=SHIM, EXECCOV_OUT=cov,
               EXECCOV_FUNCTIONS=CAT)
    t0 = time.time()
    cwd, chk = dd, "check.py"
    try:
        rc, err = invoke(cwd, env, timeout, chk)
        if rc != 0 and not (WRITE_ONCE.search(src) or "FileExistsError" in err):
            # suites with repo-relative inputs must run from the root; some
            # mask the FileNotFoundError (status-write-execution: KeyError
            # 'w64' from its catch), so retry on any failure
            rc, err = invoke(ROOT, env, timeout, os.path.join(dd, "check.py"))
        if rc != 0 and (WRITE_ONCE.search(src) or "FileExistsError" in err):
            cwd = sandbox_copy(name, dd)
            rec["sandboxed"] = True
            rc, err = invoke(cwd, env, timeout, "check.py")
            # exclusive-create outputs beyond the default list (EXP-040's
            # full-disassembly.txt): drop the named sandbox file and re-run
            for _ in range(12):
                m = FILE_EXISTS.search(err) if rc != 0 else None
                if not m:
                    break
                victim = os.path.abspath(m.group(1).replace("\\\\", "\\"))
                if not victim.startswith(os.path.abspath(cwd) + os.sep):
                    break
                os.remove(victim)
                rc, err = invoke(cwd, env, timeout, "check.py")
            if rc != 0 and "FileNotFoundError" in err:
                rc, err = invoke(ROOT, env, timeout,
                                 os.path.join(cwd, "check.py"))
            if rc == 0:
                # write-once suite: the sandbox-produced receipt must match
                produced = os.path.join(cwd, "result.json")
                if os.path.exists(produced):
                    now = md5(produced)
                    if now != rec["receipt_md5"]:
                        rec["status"] = "receipt_mismatch"
                        rec["new_receipt_md5"] = now
                else:
                    rec["status"] = "no_receipt_produced"
                rec["elapsed_s"] = round(time.time() - t0, 1)
                rec["rc"] = rc
                _fold(name, cov, runs, rec)
                return rec
        rec["elapsed_s"] = round(time.time() - t0, 1)
        rec["rc"] = rc
        if rc != 0:
            rec["status"] = "rc%d" % rc
            rec["stderr_tail"] = err[-2000:]
    except subprocess.TimeoutExpired:
        rec["status"] = "timeout"
    now = md5(res)
    if now != rec["receipt_md5"]:
        rec["status"] = "receipt_mismatch"
        rec["new_receipt_md5"] = now
        with open(res, "wb") as f:   # restore the sealed receipt
            f.write(orig_bytes)
    _fold(name, cov, runs, rec)
    return rec


def _fold(name, cov, runs, rec):
    covrec = {}
    if os.path.exists(cov):
        covrec = json.load(open(cov))
        rec.update({k: covrec[k] for k in
                    ("instrument", "catalogue", "exe_sha256", "emu_starts",
                     "unique_blocks", "blocks_in_image", "blocks_outside_image",
                     "patched_blocks") if k in covrec})
        rec["classes"] = {}
        for e, c in covrec.get("entries", {}).items():
            rec["classes"][c] = rec["classes"].get(c, 0) + 1
        # executed = the shipped body ran: returned or faulted only
        rec["entries_executed"] = sum(rec["classes"].get(c, 0)
                                      for c in EXECUTED)
        mut = set(covrec.get("mutated", []))
        with open(os.path.join(runs, name + ".tsv"), "w") as f:
            f.write("entry\tclass\tmutated\n")
            for e, c in sorted(covrec.get("entries", {}).items()):
                f.write("%s\t%s\t%s\n" % (e, c, "yes" if e in mut else ""))
    else:
        rec["status"] = rec["status"] if rec["status"] != "ok" else "no_cov_out"
    with open(os.path.join(runs, name + ".json"), "w") as f:
        json.dump(rec, f, indent=1, sort_keys=True)
    if os.path.exists(cov):
        os.remove(cov)


def aggregate(outdir):
    runs = os.path.join(outdir, "runs")
    cat = {}
    for ln in open(CAT, encoding="utf8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) > 3:
            cat[f[0]] = (f[1], f[3])
    rows = {}
    receipts = {}
    for fn in sorted(os.listdir(runs)):
        if not fn.endswith(".json"):
            continue
        rec = json.load(open(os.path.join(runs, fn)))
        name = rec["run"]
        receipts[name] = rec["receipt_md5"]
        tsv = os.path.join(runs, name + ".tsv")
        if not os.path.exists(tsv):
            continue
        if rec.get("status") != "ok":
            continue        # an unreproduced receipt seals nothing
        for ln in open(tsv).read().splitlines()[1:]:
            e, c, m = (ln.split("\t") + [""])[:3]
            r = rows.setdefault(e, {"runs": [], "exec": [], "classes": set(),
                                    "rcpts": [], "mut": 0})
            r["runs"].append(name)
            r["classes"].add(c)
            if c in EXECUTED:
                r["exec"].append(name)
                r["rcpts"].append(rec["receipt_md5"])
                r["mut"] += m == "yes"
    with open(os.path.join(outdir, "execution-coverage.tsv"), "w") as f:
        f.write("entry\tname\towner\texecuted\truns_executed\truns_observed"
                "\tclasses\trun_ids_executed\treceipt_ids\tmutated_runs\n")
        for e in sorted(rows, key=lambda x: int(x, 16)):
            nm, ow = cat.get(e.upper(), ("", ""))
            r = rows[e]
            f.write("%s\t%s\t%s\t%s\t%d\t%d\t%s\t%s\t%s\t%d\n" % (
                e.upper(), nm, ow, "yes" if r["exec"] else "NOT",
                len(r["exec"]), len(r["runs"]),
                "|".join(sorted(r["classes"])), "|".join(r["exec"]),
                "|".join(sorted(set(r["rcpts"]))), r["mut"]))
    return rows, receipts


def seal(outdir):
    """SEAL.json: instrument/engine/catalogue identities + sha256 of every
    record, so a later reader can tell a re-generated record from this one."""
    def sha(p):
        return hashlib.sha256(open(p, "rb").read()).hexdigest()
    import unicorn as _u   # the real engine: this process has no shim
    files = {}
    for dp, _dn, fns in os.walk(outdir):
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, outdir).replace(os.sep, "/")
            # the checker's own .out is written while it verifies the seal
            if rel != "SEAL.json" and not rel.endswith(".out"):
                files[rel] = sha(p)
    me = os.path.abspath(__file__)
    rec = {
        "request": "OPUS-REQ-ORACLE-EXECUTION-COVERAGE-INSTRUMENT-0929-R",
        "evidence_class": "NATIVE-REPLAY (isolated original-code execution; "
                          "never live reachability)",
        "python": sys.version.split()[0], "unicorn": _u.__version__,
        "instrument": {
            "execution_coverage.py": sha(me),
            "execcov/sitecustomize.py": sha(os.path.join(SHIM,
                                                        "sitecustomize.py")),
            "execcov/unicorn/__init__.py": sha(os.path.join(
                SHIM, "unicorn", "__init__.py"))},
        "catalogue_md5": md5(CAT),
        "files": dict(sorted(files.items())),
    }
    with open(os.path.join(outdir, "SEAL.json"), "w") as f:
        json.dump(rec, f, indent=1)
    return len(files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--dirs", nargs="*", default=None)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--aggregate-only", action="store_true")
    a = ap.parse_args()
    # suites run with cwd = their own dir: a relative --out would send each
    # cov record there, and a failed atexit write still exits 0 (no_cov_out)
    a.out = os.path.abspath(a.out)
    os.makedirs(os.path.join(a.out, "runs"), exist_ok=True)
    if a.aggregate_only:
        rows, receipts = aggregate(a.out)
        print("aggregate: %d entries across %d runs" % (len(rows), len(receipts)))
        print("sealed %d files" % seal(a.out))
        return
    todo = [t for t in suites()
            if a.dirs is None or t[0] in a.dirs]
    if a.list:
        for n, d, s in todo:
            print(n)
        print("%d suites" % len(todo))
        return
    fails = []
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for rec in ex.map(lambda t: run_one(t[0], t[1], t[2], a.out, a.timeout),
                          todo):
            line = "%-52s %-16s entries=%s runs=%s" % (
                rec["run"], rec["status"], rec.get("entries_executed", "-"),
                rec.get("emu_starts", "-"))
            if rec["status"] != "ok":
                fails.append(line)
            print(line, flush=True)
    rows, receipts = aggregate(a.out)
    print("aggregate: %d entries across %d runs" % (len(rows), len(receipts)))
    if a.dirs is None:
        print("sealed %d files" % seal(a.out))
    print("FAILS %d" % len(fails))
    for l in fails:
        print(" ", l)


if __name__ == "__main__":
    main()
