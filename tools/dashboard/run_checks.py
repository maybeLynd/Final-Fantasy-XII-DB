"""run_checks.py - the Evidence & lessons tab's verification checks, run once per dashboard build (2026-09-30).

    python run_checks.py --db "<FFXII TZA>" --out <checks.json> [--workers 4] [--timeout 60]

Runs a CURATED set of the database's own checkers - each one read-only and measured at about 15 s or less - and writes
one JSON record per checker: status, exit code, seconds, ran_at, key numbers and the full output. build_views.py runs it
before a generation begins, so the record becomes a captured, fingerprinted input like goal_gate.json.

STATUS IS FAIL-CLOSED. PASS needs exit 0, some output, and no failure marker. Exit 1 (or a failure marker in the output)
is FAIL. Anything else - a traceback, a timeout, a launch error, an exit code this runner does not know, a checker that
printed nothing - is UNMEASURED with the reason, never PASS. ("Clean" and "scanned nothing" read identically; COVERAGE.md.)

READ-ONLY. Every checker runs with `python -B` (no bytecode written) from the repository root. A checker is on the list
only when its source writes nothing outside a self-test temp folder on the invocation used here. The ones left out are in
EXCLUDED with the reason, and the page names them, so a checker that is not run is never mistaken for one that passed.
"""
import argparse, concurrent.futures, datetime, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE); DBROOT = os.path.dirname(TOOLS); REPO = os.path.dirname(DBROOT)
GS = os.path.join(TOOLS, "analysis-kit", "gfz-scripts")
NOW = lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
OUTPUT_CAP = 200000

# A key number is (label, regex, how): "int" takes group 1 of the first match; "count" counts matches; a third element
# "zero:<regex>" reads 0 when that regex matches and the number's own line is absent (a clean run prints no count line).
# A number that cannot be read is None and the page shows a dash, never 0.
CHECKS = [
    {"id": "contradiction_index", "script": "contradiction_index.py", "args": ["status", "--db", "{db}"],
     "what": "The mistakes ledger is complete: every recorded correction has a written cause and names the instrument that produced the wrong answer.",
     "keys": [("records", r"contradiction records\s*:\s*(\d+)"), ("without a written cause", r"UNSUMMARISED\s*:\s*(\d+)"),
              ("source line gone", r"source missing/unmatched\s*:\s*(\d+)")]},
    {"id": "check_alias_boxes", "script": "check_alias_boxes.py", "args": ["--db", "{db}"],
     "what": "No question is tracked as open under two different ids.",
     "keys": [("alias boxes", r"alias boxes \(two or more ids\)\s*:\s*(\d+)"), ("both ids still open", r"BOTH IDS STILL OPEN\s*:\s*(\d+)")]},
    {"id": "check_arithmetic", "script": "check_arithmetic.py", "args": ["--db", "{db}"],
     "what": "Sums written in the documents' code spans actually compute to what the page says.",
     "keys": [("expressions checked", r"backtick expressions evaluated\s*:\s*(\d+)"), ("do not reproduce", r"expressions that do not reproduce\s*:\s*(\d+)")]},
    {"id": "check_assets", "script": "check_assets.py", "args": ["--db", "{db}"],
     "what": "Every kind of file the game ships has a format sheet, or a declared reason it needs none.",
     "keys": [("formats covered", r"covered:\s*(\d+)\s*/\s*\d+"), ("formats in the archive", r"covered:\s*\d+\s*/\s*(\d+)"),
              ("bucketed", r"bucketed:\s*(\d+)")]},
    {"id": "check_citation_shape", "script": "check_citation_shape.py", "args": ["--db", "{db}"],
     "what": "How strongly each explained function is cited - a report on the heaviest-weighted progress number, not a gate.",
     "keys": [("functions counted", r"bodies counted by engine_explained:\s*(\d+)"), ("cited only once", r"cited exactly once anywhere\s*:\s*(\d+)")]},
    {"id": "check_consistency", "script": "check_consistency.py", "args": ["--db", "{db}"],
     "what": "No address is described two different ways (size, name or caller count) in two documents.",
     "keys": [("documents", r"checked (\d+) documents"), ("disagreements", r"(\d+) disagreement\(s\) to resolve", r"zero:consistent: no address")]},
    {"id": "check_counts", "script": "check_counts.py", "args": ["--db", "{db}"],
     "what": "Where a page states a count just above a table, the table has that many rows (advisory: a nearby number need not be the table's length).",
     "keys": [("documents", r"documents scanned\s*:\s*(\d+)"), ("pairs to eyeball", r"count/table pairs that disagree\s*:\s*(\d+)")]},
    {"id": "check_counts_vs_tables", "script": "check_counts_vs_tables.py", "args": ["--db", "{db}"],
     "what": "Every count-versus-table mismatch has been read by someone and ruled on.",
     "keys": [("candidates", r"candidates:\s*(\d+)"), ("needing a fix", r"needing a fix:\s*(\d+)"), ("untriaged", r"untriaged:\s*(\d+)")]},
    {"id": "check_coverage", "script": "check_coverage.py", "args": ["--db", "{db}"],
     "what": "The coverage index's document count per category matches what is on disk.",
     "keys": [("documents claimed", r"totals: claimed (\d+)"), ("documents on disk", r"totals: claimed \d+\s+actual (\d+)"),
              ("categories off", r"COVERAGE MISMATCH in (\d+) categor", r"zero:COVERAGE consistent")]},
    {"id": "check_doc_self", "script": "check_doc_self.py", "args": ["--db", "{db}"],
     "what": "No document contradicts its own structure (a status that disagrees with the page's own sections).",
     "keys": [("documents", r"scanned (\d+) documents")]},
    {"id": "check_evidence_propagated", "script": "check_evidence_propagated.py", "args": ["--db", "{db}"],
     "what": "Functions a session established are carried into a form the progress numbers count.",
     "keys": [("functions counted", r"\bCOUNTED\b", "count")]},
    {"id": "check_formats", "script": "check_formats.py", "args": ["--db", "{db}"],
     "what": "Every slot of the game's authored-data registry is explained by a document.",
     "keys": [("slots covered", r"covered:\s*(\d+)\s*/\s*\d+"), ("slots", r"covered:\s*\d+\s*/\s*(\d+)")]},
    {"id": "check_gate26", "script": "check_gate26.py", "args": ["--db", "{db}"],
     "what": "Each subsystem contract answers the charter's section-26 questions (owner, inputs, lifetime, invariants...).",
     "keys": [("contracts", r"SCORED AGAINST CHARTER SECTION 26:\s*(\d+)"), ("runtime-validated", r"control passed: (\d+) of \d+ live")]},
    {"id": "check_provenance", "script": "check_provenance.py", "args": ["--db", "{db}"],
     "what": "Every document names the evidence generation it was verified against.",
     "keys": [("documents", r"documents:\s*(\d+)"), ("with no provenance block", r"(\d+)\s+no verified_against block")]},
    {"id": "documented_rule", "script": "{db}/_index/candidates/status-currency-ruling-fable/documented_rule.py", "args": [],
     "what": "Pages ready to move from PARTIAL to DOCUMENTED pass FABLE's status-currency rule (a candidate tool; its self-test runs first).",
     "keys": [("pages judged", r"TALLY .* of (\d+)"), ("ready", r"TALLY .*\bREADY=(\d+)"), ("still partial", r"TALLY .*\bPARTIAL=(\d+)"),
              ("self-test failures", r"^FAILS (\d+)")],
     "fail": r"^FAILS [1-9]"},
]

# Not run at build time, named so that silence is never mistaken for a pass.
EXCLUDED = [
    {"id": "check_links", "why": "slow", "detail": "about 54 s: resolves every relative link across the database and Tools"},
    {"id": "run_gates", "why": "slow", "detail": "runs all ~80 kit checkers against the accepted baseline; many minutes"},
    {"id": "audit_crossrefs", "why": "writes files", "detail": "rewrites the shared, tracked pass22-tripwires.tsv on every run"},
    {"id": "check_address_index", "why": "writes files", "detail": "regenerates the address index into a temp folder and runs git status, which can rewrite the shared git index"},
    {"id": "check_rules_index", "why": "writes files", "detail": "regenerates the rules index into a fixed file in the system temp folder"},
    {"id": "census_archive_formats", "why": "writes files", "detail": "writes the archive format census TSV (the format registry reads its last output instead)"},
]


def key_numbers(spec, out):
    nums = []
    for k in spec.get("keys", []):
        label, rx = k[0], k[1]
        how = k[2] if len(k) > 2 else "int"
        val = None
        if how == "count":
            val = len(re.findall(rx, out, re.M))
        else:
            m = re.search(rx, out, re.M)
            if m:
                val = int(m.group(1))
            elif how.startswith("zero:") and re.search(how[5:], out, re.M):
                val = 0
        nums.append([label, val])
    return nums


def classify(rc, out, err, fail=None):
    """(status, reason). Fail-closed: only exit 0 with output and no failure marker is PASS."""
    if rc is None:
        return "UNMEASURED", err or "did not run"
    if "Traceback (most recent call last)" in (err or ""):
        last = [l for l in err.strip().splitlines() if l.strip()]
        return "UNMEASURED", "crashed: " + (last[-1][:200] if last else "traceback")
    if re.search(r"^CANNOT RUN", out or "", re.M):
        return "UNMEASURED", "the checker says it cannot run"
    if rc not in (0, 1):
        return "UNMEASURED", "exit %s is not a verdict (2 usually means the check itself failed)" % rc
    if not (out or "").strip():
        return "UNMEASURED", "exit %s with no output: a clean run and a run that scanned nothing read the same" % rc
    if fail and re.search(fail, out, re.M):
        return "FAIL", "the output reports a failure (%s)" % fail
    return ("PASS", "exit 0") if rc == 0 else ("FAIL", "exit 1: the checker reports findings")


def run_one(spec, db, timeout=60, python=sys.executable):
    script = spec["script"].replace("{db}", db)
    path = script if os.path.isabs(script) else os.path.join(GS, script)
    args = [a.replace("{db}", db) for a in spec.get("args", [])]
    rec = {"id": spec["id"], "what": spec.get("what", ""), "script": os.path.relpath(path, REPO).replace("\\", "/") if os.path.isabs(path) else path,
           "args": ["<db>" if a == db else a for a in args], "ran_at": NOW()}
    t0 = time.time()
    rc, out, err = None, "", ""
    try:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        r = subprocess.run([python, "-B", path] + args, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout, cwd=REPO, env=env)
        rc, out, err = r.returncode, r.stdout or "", r.stderr or ""
    except subprocess.TimeoutExpired:
        err = "exceeded %d s and was stopped" % timeout
    except OSError as e:
        err = "could not start: %s" % e
    rec["seconds"] = round(time.time() - t0, 1)
    rec["exit"] = rc
    rec["status"], rec["reason"] = classify(rc, out, err, spec.get("fail"))
    rec["numbers"] = key_numbers(spec, out) if rec["status"] != "UNMEASURED" else [[k[0], None] for k in spec.get("keys", [])]
    lines = [l for l in out.strip().splitlines() if l.strip()]
    rec["last_line"] = lines[-1].strip()[:200] if lines else ""
    full = out + (("\n--- stderr ---\n" + err) if err.strip() else "")
    rec["output"] = full if len(full) <= OUTPUT_CAP else full[:OUTPUT_CAP] + "\n... [cut at %d characters]" % OUTPUT_CAP
    return rec


def run_all(db, specs=None, workers=4, timeout=60):
    specs = CHECKS if specs is None else specs
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        recs = list(ex.map(lambda s: run_one(s, db, timeout), specs))
    return {"version": 1, "ran_at": NOW(), "workers": workers, "timeout": timeout, "checks": recs, "excluded": EXCLUDED}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--timeout", type=int, default=60)
    a = ap.parse_args(argv)
    t0 = time.time()
    res = run_all(os.path.abspath(a.db), workers=a.workers, timeout=a.timeout)
    res["seconds"] = round(time.time() - t0, 1)
    tmp = a.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    os.replace(tmp, a.out)
    print("%d checks in %.1f s: %s" % (len(res["checks"]), res["seconds"],
          ", ".join("%s %s" % (c["id"], c["status"]) for c in res["checks"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
