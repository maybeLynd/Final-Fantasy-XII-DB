"""run_correction_regressions.py - re-run every accepted correction's regression against the current tree (OPUS, 2026-10-03).

WHY (the user's root-cause directive, item 6). Every correction ships a regression that FAILS on the pre-correction text
(EVIDENCE-POLICY; the consumer-check record names it). But a regression ran exactly once - at the correction's own
publish - and never again, so a later edit that restored the old semantics (the expanded L2 audit found such reversions)
passed every gate. This runner discovers every regression the consumer-check records declare and runs them all, now.

DISCOVERY. Each `_index/candidates/*/consumer-check.md` names its regression as a repository path ending in `.py`
(`Database/Tools/...py`, or a candidate record's own `_index/candidates/<rec>/<name>.py`). Each is run with no arguments,
from its own directory, and must exit 0.

RETIREMENT IS EXPLICIT. A regression legitimately superseded by a later accepted correction is listed in
`_index/correction-regressions-retired.tsv` (path, superseding record, reason) - reviewable, never a silent skip. A
listed path that no longer exists, or a retired entry with no superseding record, is itself a failure.

Usage: python run_correction_regressions.py [--jobs N] [--json OUT] [--only SUBSTR]
Exit 0 when every live regression passes; 1 otherwise. --self-test runs the fixtures."""
import concurrent.futures
import io
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DB = os.path.join(ROOT, "Database", "FFXII TZA")
CAND = os.path.join(DB, "_index", "candidates")
RETIRED = os.path.join(DB, "_index", "correction-regressions-retired.tsv")
REF = re.compile(r"(Database/Tools/[A-Za-z0-9_./-]+\.py|(?:Database/FFXII TZA/)?_index/candidates/[A-Za-z0-9_./-]+\.py)")


DECL = re.compile(r"\bRegression\b[^:\n]{0,40}:\**\s*(.+)$", re.I)
# paths may hold exactly one space, in the "FFXII TZA" folder name; anything else with a space is two tokens ("x.py and
# y.py"), and a glob ("`*_check.py`") is a description, not a script
PYTOK = re.compile(r"(?<![*\w])`?((?:Database/FFXII TZA/)?[A-Za-z0-9_./-]*?[A-Za-z0-9_.-]+\.py)`?")


def _declared(line, rec):
    """[(repo path, args)] from one 'Regression:' declaration line. Only the DECLARED regression counts - a script a
    consumer table merely mentions (a dated receipt with a documented FAIL) is not one. Bare names resolve in the
    declaring record's folder; `--db` with no value gets the database path (the declared invocation)."""
    m = DECL.search(line)
    if not m:
        return []
    out = []
    # the declaration ends where the line starts reporting on it ("..., verified at <sha>: FAILS 0. Both `x.py` ...")
    body = re.split(r",\s*verified\b|\.\s+[A-Z]", m.group(1))[0]
    for pm in PYTOK.finditer(body):
        tok = pm.group(1).strip().strip("`")
        if tok.startswith(("Database/", "_index/")):
            rel = tok if tok.startswith("Database/") else "Database/FFXII TZA/" + tok
        elif "/" not in tok:
            rel = "Database/FFXII TZA/_index/candidates/%s/%s" % (rec, tok)
            if not os.path.isfile(os.path.join(CAND, rec, tok)) and os.path.isfile(os.path.join(HERE, tok)):
                rel = "Database/Tools/analysis-kit/gfz-scripts/" + tok        # a shared tool named bare
        else:
            continue
        rest = body[pm.end():].split("(")[0].split(",")[0].split(";")[0]
        args = []
        toks = rest.split()
        i = 0
        while i < len(toks) and toks[i].startswith("--"):
            args.append(toks[i].rstrip(".`"))
            if i + 1 < len(toks) and not toks[i + 1].startswith(("--", "(")) and toks[i + 1][:1] not in "`":
                pass
            i += 1
        if "--db" in args and (args.index("--db") == len(args) - 1):
            args.append(DB)
        out.append((rel, tuple(args)))
    return out


def discover():
    """{(repo-relative path, args): [declaring record, ...]} from every consumer-check record's Regression lines."""
    out = {}
    for rec in sorted(os.listdir(CAND)):
        cc = os.path.join(CAND, rec, "consumer-check.md")
        if not os.path.isfile(cc):
            continue
        for line in io.open(cc, encoding="utf-8", errors="replace"):
            for key in _declared(line, rec):
                out.setdefault(key, []).append(rec)
    return out


def retired():
    out = {}
    if os.path.isfile(RETIRED):
        for l in io.open(RETIRED, encoding="utf-8"):
            if l.strip() and not l.startswith("#"):
                f = l.rstrip("\n").split("\t")
                out[f[0]] = f[1:] + [""] * (2 - len(f[1:]))
    return out


def run_one(key, timeout=300):
    rel, args = key if isinstance(key, tuple) else (key, ())
    p = os.path.join(ROOT, *rel.split("/"))
    if not os.path.isfile(p):
        return rel, "MISSING", 0.0, "the declared regression file does not exist"
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, "-B", p] + list(args), cwd=os.path.dirname(p), capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace")
        tail = ((r.stdout + r.stderr).strip().splitlines() or [""])[-1][:200]
        return rel, "PASS" if r.returncode == 0 else "FAIL", time.time() - t0, tail
    except subprocess.TimeoutExpired:
        return rel, "TIMEOUT", time.time() - t0, "over %ds" % timeout


def main(argv):
    if "--self-test" in argv:
        return _self_test()
    jobs = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 6
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    regs = discover()
    ret = retired()
    res, problems = [], []
    for rel, (sup, why) in sorted(ret.items()):
        if not sup or not os.path.isdir(os.path.join(CAND, sup)):
            problems.append("retired %s names no existing superseding record (%r)" % (rel, sup))
    todo = [k for k in sorted(regs) if k[0] not in ret and (not only or only in k[0])]
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        for key, (rel, st, dt, tail) in zip(todo, ex.map(run_one, todo)):
            res.append({"regression": rel + ("".join(" " + a for a in key[1]) if key[1] else ""), "state": st,
                        "seconds": round(dt, 1), "tail": tail, "records": regs[key]})
    for r in res:
        if r["state"] != "PASS":
            print("%-8s %s  (%s)  <- %s" % (r["state"], r["regression"], r["tail"], ", ".join(r["records"][:3])))
    for p in problems:
        print("RETIRED-BAD", p)
    n = {s: sum(1 for r in res if r["state"] == s) for s in ("PASS", "FAIL", "MISSING", "TIMEOUT")}
    print("CORRECTION REGRESSIONS: %d declared, %d retired, %d run - PASS %d, FAIL %d, MISSING %d, TIMEOUT %d%s" % (
        len(regs), len(ret), len(res), n["PASS"], n["FAIL"], n["MISSING"], n["TIMEOUT"],
        (", retired-list problems %d" % len(problems)) if problems else ""))
    if "--json" in argv:
        json.dump({"results": res, "retired": ret, "problems": problems},
                  io.open(argv[argv.index("--json") + 1], "w", encoding="utf-8"), indent=1)
    bad = n["FAIL"] + n["MISSING"] + n["TIMEOUT"] + len(problems)
    return 1 if bad else 0


def _self_test():
    import tempfile
    fails = []

    def ok(c, w):
        print(("ok   " if c else "FAIL ") + w)
        if not c:
            fails.append(w)
    m = _declared("- **Regression:** Database/Tools/analysis-kit/gfz-scripts/check_questions.py --db (agree).", "r")
    ok(m == [("Database/Tools/analysis-kit/gfz-scripts/check_questions.py", ("--db", DB))],
       "declared regression with its invocation: %s" % m)
    m = _declared("Regression: `sq1_dword0.py` (A1-A5, controls C1-C2)", "rec-9")
    ok(m == [("Database/FFXII TZA/_index/candidates/rec-9/sq1_dword0.py", ())], "bare name resolves in its record: %s" % m)
    m = _declared("| `_index/candidates/bq23-tier6/bq23_tier6.py` (FABLE receipt) | T4 | receipt unchanged |", "r")
    ok(m == [], "a script a consumer table merely mentions is not a declared regression")
    os.makedirs(os.path.join(ROOT, "Database", "Tools", "work"), exist_ok=True)
    d = tempfile.mkdtemp(dir=os.path.join(ROOT, "Database", "Tools", "work"))
    try:
        good = os.path.join(d, "good.py")
        bad = os.path.join(d, "bad.py")
        io.open(good, "w").write("import sys; sys.exit(0)\n")
        io.open(bad, "w").write("print('FAIL the corrected sentence was reverted'); import sys; sys.exit(1)\n")
        rg = os.path.relpath(good, ROOT).replace(os.sep, "/")
        rb = os.path.relpath(bad, ROOT).replace(os.sep, "/")
        if not rg.startswith(".."):
            ok(run_one(rg)[1] == "PASS", "a regression that holds passes")
            ok(run_one(rb)[1] == "FAIL", "a reverted correction fails its regression")
        ok(run_one("Database/Tools/nope/missing_check.py")[1] == "MISSING", "a declared but absent regression is MISSING")
    finally:
        for f in ("good.py", "bad.py"):
            try:
                os.remove(os.path.join(d, f))
            except OSError:
                pass
        os.rmdir(d)
    print("self-test: %d failure(s)" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
