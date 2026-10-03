#!/usr/bin/env python3
"""xcheck.py - SWE2-ORACLE execution cross-check of AUDIT-SEM's six L2 systems (OPUS-REQ-ORACLE-L2-CROSSCHECK-1003).

For every replay package the six runtime cells cite, in a same-depth sandbox copy (`_index/_xc_sandbox/`, ignored;
the repository copies are never run or written):
  R  reproduce   run each driver; the produced result file must equal the published one byte-for-byte
  C  coverage    run it again under gfz-scripts/execcov (b742fa6c9, review 701804391): every catalogue entry the run
                 touched, classed returned/faulted (executed) or stubbed/scripted (NOT executed), and the count of
                 blocks outside the image (harness-planted code). A "stub-free" claim is contradicted by a stubbed or
                 scripted catalogue entry, not by out-of-image import stubs, which are reported separately
  M  mutation    for each one-byte mutation of a load-bearing instruction named in the cells (MUTS below), run the
                 driver under mutshim/: KILLED (the harness reports a failure), CHANGED-BUT-PASS (its result changes
                 but it still passes: an observation, not a judgement), INVISIBLE (byte-identical result although the
                 patched instruction executed), NOT-REACHED (it never executed in this driver)
Prints one line per check; writes xcheck.tsv. Requires system Python 3.14 / unicorn 2.1.4.
usage: xcheck.py [--only PKG ...] [--jobs N]
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(CAND, "..", "..", "..", ".."))
SANDBOX = os.path.join(os.path.dirname(CAND), "_xc_sandbox")
EXECCOV = os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts", "execcov")
MUTSHIM = os.path.join(HERE, "mutshim")
CAT = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
PY = sys.executable
EVID = os.path.join(ROOT, "Database", "FFXII TZA", "_experiments", "evidence")
EVSANDBOX = os.path.join(ROOT, "Database", "FFXII TZA", "_experiments", "_cov_runs")   # ignored (execcov's)
SIBLINGS = ["s29-opus-replay-inventory-rebase", "s21-opus-replay-applier-stub-free", "s33-opus-replay-op1-real"]

# system -> [(package, driver, result file)]
RUNS = {
    "S-02": [("s02-opus-replay-world-tick-stub-free", "check.py", "result.json"),
             ("s02-opus-replay-world-tick-stub-free", "wt6.py", "wt6_result.json"),
             ("s02-opus-replay-stop-apply-stub-free", "check.py", "result.json")],
    "S-13": [("s13-opus-replay-record-pool-stub-free", "check.py", "result.json"),
             ("s13-opus-replay-record-pool-stub-free", "residuals.py", "residuals_result.json")],
    "S-28": [("s28-opus-replay-five-slot-maps", "check.py", "result.json"),
             ("s28-opus-replay-five-slot-maps", "check_block.py", "result_block.json"),
             ("s28-opus-replay-five-slot-maps", "check_focus.py", "result_focus.json"),
             ("s28-opus-replay-five-slot-maps", "check_roster.py", "result_roster.json"),
             ("s28-opus-replay-slot-map-writers", "check.py", "result.json")],
    "S-43": [("s43-opus-replay-save-image-pipeline", "check.py", "result.json")],
    "S-36": [("s36-opus-replay-request-router", "check.py", "result.json"),
             ("s36-opus-replay-request-router", "r45.py", "r45_result.json"),
             ("s36-opus-replay-arbiter-input-gate", "check.py", "result.json"),
             ("s36-opus-replay-widget-ctor", "check.py", "result.json")],
    "S-49": [("s49-opus-replay-lighting-slot-zeros", "check.py", "result.json"),
             ("evidence:phyre-header-exec", "check.py", "result.json"),
             ("evidence:class-descriptor-dtor-exec", "check.py", "result.json")],
}
# system -> [(label, instruction va, patched byte va, orig, new, what the mutation breaks)]
MUTS = {
    "S-02": [("SS2-polarity", 0x226339, 0x22633B, 0x43, 0x42, "cmovae->cmovb: the exemption polarity of SS-2"),
             ("tick-cmovns", 0x314088, 0x314089, 0x49, 0x48, "cmovns->cmovs in the tick prologue (00314088)")],
    "S-13": [("init-jb", 0x2668EA, 0x2668EA, 0x72, 0x73, "jb->jae after cmp eax,0xa (00266530 init)"),
             ("bind-cmovne", 0x26C8FA, 0x26C8FC, 0x45, 0x44, "cmovne->cmove in the manager bind 0026C8C0")],
    "S-28": [("binder-magic-je", 0x233C53, 0x233C53, 0x74, 0x75, "je->jne on the 0x05071901 magic test (BS-2)"),
             ("refresher-base", 0x3266D4, 0x3266D7, 0x48, 0x4A, "slot-map base +0x5A48 -> +0x5A4A (refresher)"),
             ("reach-mode1-arm", 0x3269D2, 0x3269D2, 0, 0, "reach only: refresher mode-1 arm 003269D2 (CON-169 SM-5)"),
             ("reach-mode2-arm", 0x326991, 0x326991, 0, 0, "reach only: refresher mode-2 arm 00326991 (CON-169 SM-5)")],
    "S-43": [("clear-count", 0x2EF577, 0x2EF578, 0xCD, 0xCC, "loop count 0xACD -> 0xACC (SV-2 backup copy)"),
             ("crc-span", 0x583F8C, 0x583F8F, 0xE2, 0xE1, "CRC span +0xE200 -> +0xE100 (SV CRC placement)")],
    "S-36": [("R5-drain-bit", 0x2E0C93, 0x2E0C95, 0x07, 0x06, "R-5 drain guard keeps bit 1 instead of bit 0")],
    "S-49": [("ladder-6", 0x59A421, 0x59A422, 0x06, 0x07, "header failure code 6 -> 7"),
             ("ladder-9", 0x59A3E2, 0x59A3E4, 0xB5, 0xB4, "header failure code 9 -> 8"),
             ("reach-005847E0", 0x5847E0, 0x5847E0, 0, 0, "reach only: descriptor deleting destructor 005847E0 (I2)")],
}
FAIL = re.compile(r"\bFAIL(?:ED|S)?\b(?!\s*0\b)")


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None


def src_of(pkg):
    return os.path.join(EVID, pkg[9:]) if pkg.startswith("evidence:") else os.path.join(CAND, pkg)


def sandbox(pkg):
    dst = os.path.join(EVSANDBOX, "xc-" + pkg[9:]) if pkg.startswith("evidence:") else os.path.join(SANDBOX, pkg)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src_of(pkg), dst, ignore=shutil.ignore_patterns("__pycache__"))
    return dst


def prepare():
    os.makedirs(SANDBOX, exist_ok=True)
    gi = os.path.join(SANDBOX, ".gitignore")
    if not os.path.exists(gi):
        open(gi, "w").write("# SWE2-ORACLE L2 cross-check sandbox - scratch, never published\n*\n")
    for s in SIBLINGS:
        if not os.path.exists(os.path.join(SANDBOX, s)):
            shutil.copytree(os.path.join(CAND, s), os.path.join(SANDBOX, s),
                            ignore=shutil.ignore_patterns("__pycache__"))


def run(pkg, drv, res, env_extra, timeout=3600):
    d = sandbox(pkg)
    out_res = os.path.join(d, res)
    if os.path.exists(out_res):
        os.remove(out_res)                     # the run must produce it
    env = dict(os.environ, **env_extra)
    p = subprocess.run([PY, drv], cwd=d, env=env, capture_output=True, timeout=timeout)
    so = p.stdout.decode("utf8", "replace")
    return dict(rc=p.returncode, out=so, err=p.stderr.decode("utf8", "replace")[-1500:],
                md5=md5(out_res), fails=len(FAIL.findall(so)), result=open(out_res, "rb").read() if
                os.path.exists(out_res) else None)


def catalogue():
    names = {}
    for ln in open(CAT, encoding="utf8").read().splitlines()[1:]:
        f = ln.split("\t")
        names[f[0].lower()] = f[1]
    return names


def one(system, pkg, drv, res, names):
    rows = []
    pub = md5(os.path.join(src_of(pkg), res))
    base = run(pkg, drv, res, {})
    ok = base["md5"] == pub and base["rc"] == 0
    rows.append((system, pkg, drv, "R reproduce", "PASS" if ok else "FAIL",
                 "rc %d, result md5 %s vs published %s, %d FAIL tokens" % (
                     base["rc"], (base["md5"] or "none")[:8], (pub or "none")[:8], base["fails"])))
    fd, cov = tempfile.mkstemp(suffix=".json"); os.close(fd); os.remove(cov)
    c = run(pkg, drv, res, {"PYTHONPATH": EXECCOV, "EXECCOV_OUT": cov, "EXECCOV_FUNCTIONS": CAT})
    if os.path.exists(cov):
        cr = json.load(open(cov)); os.remove(cov)
        ent = cr.get("entries", {})
        bad = sorted((e, k) for e, k in ent.items() if k in ("stubbed", "scripted"))
        ex = sum(1 for k in ent.values() if k in ("returned", "faulted", "returned+faulted"))
        rows.append((system, pkg, drv, "C coverage", "STUB-FREE" if not bad else "NOT STUB-FREE",
                     "%d entries executed; stubbed/scripted: %s; %d blocks outside the image (harness-planted); "
                     "receipt under the shim %s" % (
                         ex, ", ".join("%s %s (%s)" % (e.upper(), names.get(e, "?"), k) for e, k in bad) or "none",
                         cr.get("blocks_outside_image", 0),
                         "reproduced" if c["md5"] == pub else "DIFFERS")))
    else:
        rows.append((system, pkg, drv, "C coverage", "NO-RECORD", "rc %d %s" % (c["rc"], c["err"][-200:])))
    for lab, ins, pa, o, n, what in MUTS.get(system, []):
        fd, st = tempfile.mkstemp(suffix=".json"); os.close(fd); os.remove(st)
        m = run(pkg, drv, res, {"PYTHONPATH": MUTSHIM, "XC_MUT": "%x:%x:%x:%x" % (ins, pa, o, n), "XC_OUT": st})
        s = json.load(open(st)) if os.path.exists(st) else {}
        if os.path.exists(st):
            os.remove(st)
        if o == n:
            v = "REACHED" if s.get("hits") else "NOT-REACHED"
        elif not s.get("hits"):
            v = "NOT-REACHED"
        elif m["rc"] != base["rc"] or m["fails"] > base["fails"] or m["md5"] is None:
            v = "KILLED"
        elif m["md5"] != base["md5"]:
            v = "CHANGED-BUT-PASS"
        else:
            v = "INVISIBLE"
        rows.append((system, pkg, drv, "M %s" % lab, v, "%s; patched %d emu_start(s), site executed %d time(s); "
                     "rc %d, FAIL tokens %d->%d, result %s" % (
                         what, s.get("applied", 0), s.get("hits", 0), m["rc"], base["fails"], m["fails"],
                         "identical" if m["md5"] == base["md5"] else ("absent" if m["md5"] is None else "changed"))))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    prepare()
    names = catalogue()
    todo = [(s, p, d, r) for s, lst in RUNS.items() for p, d, r in lst
            if not a.only or p in a.only or s in a.only]
    # one package's drivers share a sandbox dir: run per package serially, packages in parallel
    by_pkg = {}
    for t in todo:
        by_pkg.setdefault(t[1], []).append(t)
    allrows = []
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for rows in ex.map(lambda ts: sum((one(*t, names) for t in ts), []), by_pkg.values()):
            for r in rows:
                print("%-5s %-38s %-14s %-22s %-16s %s" % r, flush=True)
            allrows += rows
    order = list(RUNS)
    allrows.sort(key=lambda r: (order.index(r[0]), r[1], r[2]))
    with open(os.path.join(HERE, "xcheck.tsv"), "w", newline="\n") as f:
        f.write("system\tpackage\tdriver\tcheck\tverdict\tdetail\n")
        for r in allrows:
            f.write("\t".join(r) + "\n")
    print("rows %d -> xcheck.tsv" % len(allrows))


if __name__ == "__main__":
    main()
