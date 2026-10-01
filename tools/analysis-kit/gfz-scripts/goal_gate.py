#!/usr/bin/env python3
"""goal_gate.py -- the database completion gate, as a check rather than a narrative.

Why this exists. Twice (2026-09-20, 2026-09-21) a /goal evaluator returned met=true on
lanes whose own transcripts reported unfinished research -- "continuous substantive
work" read as completion. This script is the smallest READ-ONLY verification of the
goal's actual condition, so a Stop hook can veto a false success with the concrete
unmet obligation attached. It verifies accepted evidence; it does not invent semantic
acceptance, and it introduces no L3 prerequisite -- the goal is L1+L2.

What it checks, mapped to the goal's own requirements:

    scope        whole-game population sealed: verify_GFZ_PARENT/residual_addrs.txt
                 holds zero residual addresses and the function list exists.
    provenance   check_provenance.py green: every doc verified_against the certified
                 parent, per FINAL-AUDIT-PROTOCOL's fourth precondition.
    verdicts     every S-id in _index/important-subsystems.tsv has a row in
                 _index/L2-VERDICTS.md whose verdict cell reads MET.
    questions    check_questions.py reports OPEN=0, BLOCKED=0, PARTIAL=0 and the
                 register/page cross-check consistent. PARTIAL is a residue, not a
                 close -- it counts as unmet until a row is genuinely answered or
                 carries an accepted disposition.
    transfers    every disposition that closed a register row by transferring
                 its obligation (batch-K class-1 SUPERSEDED-onto-instrument,
                 class-2 NOT-A-QUESTION-onto-carrier) still has a live,
                 completion-visible destination: the named file exists, the
                 carrier task is on the board with an owner. A transferred
                 obligation whose destination evaporates is unread work with
                 no owner; verdicts being MET does not cover it.
    contradictions  _index/CONTRADICTIONS.tsv carries no row whose kind is OPEN,
                 FILED, or anything outside the resolved set.
    families     the four families a receipt-only acceptance used to miss
                 (OPUS notice 2026-09-29): P idless unticked page boxes, DD
                 undocumented documents, DA documents without a falsification
                 pass, F undispositioned functions. Read from the current
                 dashboard generation's captured requirement_facts; missing,
                 failed or >6h-stale facts are UNMET.
    acceptance   the COMMITTED _index/AUDIT-LOG.md (read via `git show HEAD:...`,
                 so a self-written uncommitted certificate does not count) records
                 a complete clean run of all thirty passes naming a program state;
                 that state must be an ancestor of HEAD with no database drift
                 since (`git diff` over "Database/FFXII TZA" excluding AUDIT-LOG.md
                 and _index/_inbox, which is where the receipt itself lives).

Missing, malformed or stale evidence is NOT_MET. A marker, a clean board, an empty
queue or a claimed percentage is not consulted -- only the records above.

Usage:  goal_gate.py [--db <path>] [--json]

Output contract (consumed by goal_gate_hook.py and lane prompts):

    DB_GOAL=NOT_MET
    remaining=<the first unmet obligation, concretely>
    next=<an eligible action for it>
    detail=<one line per check>

Exit 0 = MET, 1 = NOT_MET, 2 = the check itself failed (callers should treat as
NOT_MET -- fail closed).
"""
import argparse, collections, json, os, re, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402

IDX = os.path.join("_index")
RESOLVED_CONTRA_KINDS = {"CORRECTED", "WITHDRAWN", "RETRACTED", "SUPERSEDED", "OVERTURNED"}

# An AUDIT-LOG line counts as a terminal receipt when it reads as a complete clean
# run of the thirty passes AND names a program state as a hex commit. FINAL-AUDIT-
# PROTOCOL: "One AUDIT-LOG.md entry per complete run of all thirty, naming the
# program state." No stricter format is imposed -- this matches whatever wording
# the run records, but requires all of: the thirty-pass claim, a completion word,
# and a commit token.
RECEIPT_CLAIM = re.compile(r"(?i)(thirty|30)[ -]?(pass|passes)|all thirty|final[ -]audit")
RECEIPT_DONE = re.compile(r"(?i)complete|clean|streak|30/30|passed")
HEXTOKEN = re.compile(r"\b[0-9a-f]{7,40}\b")

# Paths excluded from receipt-freshness drift: the receipt lives in AUDIT-LOG.md
# and the control plane lives in _index/_inbox; neither is audited content.
DRIFT_EXCLUDE = [":(exclude)Database/FFXII TZA/_index/AUDIT-LOG.md",
                 ":(exclude)Database/FFXII TZA/_index/_inbox"]


def _git(root, *args):
    return subprocess.run(["git", "-C", root] + list(args),
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=60)


def _head(root):
    r = _git(root, "rev-parse", "HEAD")
    return r.stdout.strip() if r.returncode == 0 else None


def check_scope(db, root):
    resid = os.path.join(root, "Database", "Tools", "work",
                         "verify_GFZ_PARENT", "residual_addrs.txt")
    funcs = os.path.join(root, "Database", "Tools", "work", "graph", "functions.tsv")
    if not os.path.isfile(funcs):
        return False, "no function list at Database/Tools/work/graph/functions.tsv", \
            "regenerate the certified function population before completion can be evaluated"
    if not os.path.isfile(resid):
        return False, "no residual ledger at verify_GFZ_PARENT/residual_addrs.txt", \
            "run the certified-parent verification to produce the residual ledger"
    n = sum(1 for l in open(resid, encoding="utf-8", errors="replace") if l.strip())
    if n:
        return False, "%d unresolved residual address(es) in verify_GFZ_PARENT" % n, \
            "disposition the residual addresses"
    return True, "population sealed, 0 residual", ""


def check_provenance(root):
    tool = os.path.join(KP.GFZ_SCRIPTS, "check_provenance.py")
    r = subprocess.run([sys.executable, tool, "--db", KP.DB],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=300)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()
        last = tail[-1][:200] if tail else "no output"
        return False, "check_provenance not green: %s" % last, \
            "re-verify stale/missing provenance stamps against the certified parent"
    return True, "every doc verified against the certified parent", ""


VERDICT_ROW = re.compile(r"^\|\s*\*?\*?(S-\d+)\b.*\|", re.M)


def check_verdicts(db, root):
    reg = os.path.join(db, IDX, "important-subsystems.tsv")
    verd = os.path.join(db, IDX, "L2-VERDICTS.md")
    if not os.path.isfile(reg):
        return False, "system registry missing (important-subsystems.tsv)", "restore the registry"
    if not os.path.isfile(verd):
        return False, "no per-system verdict record (L2-VERDICTS.md)", \
            "score every registered system against the five L2 requirements"
    ids = []
    for l in open(reg, encoding="utf-8", errors="replace"):
        m = re.match(r"^(S-\d+)\t", l)
        if m:
            ids.append(m.group(1))
    # The verdict cell width is read off the table's own header rather than
    # hardcoded: any other table in the document can carry an S-id in its
    # first column, and last-match-wins over those rows silently re-reads a
    # contract-scope or count cell as the verdict (nine systems were scored
    # from the wrong table this way). The verdict column is a controlled
    # vocabulary; a leading MET token counts, its basis belongs in the
    # binding-gap cell.
    lines = open(verd, encoding="utf-8", errors="replace").read().splitlines()
    width = None
    for l in lines:
        if re.match(r"^\|\s*system\b", l, re.I) and "binding gap" in l:
            width = len([c for c in re.split(r"(?<!\\)\|", l) if c.strip()])
    if width is None:
        return False, "verdict table header not found in L2-VERDICTS.md", \
            "restore the verdict table's header row (system .. binding gap)"
    verdicts = {}
    for l in lines:
        m = re.match(r"^\|\s*(?:\*\*)?(S-\d+)\b([^|]*)\|(.*)$", l)
        if not m:
            continue
        cells = [c.strip().strip("*").strip() for c in re.split(r"(?<!\\)\|", m.group(3))]
        cells = [c for c in cells if c]
        if len(cells) == width - 1:
            verdicts[m.group(1)] = cells[-2]  # verdict is the cell before binding gap
    missing = [s for s in ids if s not in verdicts]
    if missing:
        return False, "no verdict row for %s" % ", ".join(missing[:6]), \
            "score %s in L2-VERDICTS.md" % missing[0]
    unmet = [(s, verdicts[s]) for s in ids if not re.match(r"^MET\b", verdicts[s])]
    if unmet:
        return False, "%d/%d systems NOT MET (first: %s)" \
            % (len(unmet), len(ids), unmet[0][0]), \
            "close the binding gap recorded for %s" % unmet[0][0]
    return True, "all %d registered systems verdict MET" % len(ids), ""


def check_questions(db):
    tool = os.path.join(KP.GFZ_SCRIPTS, "check_questions.py")
    r = subprocess.run([sys.executable, tool, "--db", db],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=300)
    out = r.stdout
    counts = {}
    for k in ("OPEN", "BLOCKED", "PARTIAL"):
        m = re.search(r"^\s+%s\s+(\d+)" % k, out, re.M)
        counts[k] = int(m.group(1)) if m else None
    if any(v is None for v in counts.values()):
        # A nonzero exit only means "findings" -- the instrument still prints
        # its counts. A run with no parseable counts is the actual failure.
        return False, "check_questions output unreadable", "inspect the register directly"
    if "questions consistent" not in out:
        return False, "register and page checklists disagree", \
            "reconcile OPEN-QUESTIONS.md with document checklists"
    m = re.search(r"QUESTION LEDGER INCONSISTENT.*", out)
    if m:
        return False, "question ledger malformed: %s" % m.group(0).strip(), \
            "repair the malformed register row"
    # an ANSWERED row resting on evidence nobody can fetch is not closed (AUDITSPEC-REQ-OPUS-ANSWERED-ROW-EVIDENCE-
    # TRACKED-0930); a missing line means an older check_questions, which fails closed like any unreadable count
    m = re.search(r"ANSWERED rows citing untracked or missing evidence\s*:\s*(\d+)(.*)", out)
    if not m:
        return False, "check_questions does not report untracked evidence", "update check_questions.py"
    if int(m.group(1)):
        return False, "ANSWERED rows cite untracked or missing evidence: %s%s" % (m.group(1), m.group(2).strip()[:120]), \
            "publish the cited _index/candidates records"
    bad = {k: v for k, v in counts.items() if v}
    if bad:
        return False, "questions outstanding: " + \
            ", ".join("%s=%d" % kv for kv in bad.items()), \
            "resolve or carry an accepted disposition for every register row"
    return True, "question register closed and consistent", ""


def check_transfers(db):
    """Disposition transfers keep their destinations live.

    transfer_audit.py verifies every class-1 SUPERSEDED row's named
    instrument file exists and every class-2 carrier task is on the board
    with an owner. A missing audit, a malformed record, or one dead
    destination is a failure - this is the all-L2-MET-but-one-unread case.
    """
    tool = os.path.join(KP.GFZ_SCRIPTS, "transfer_audit.py")
    board = os.path.join(db, IDX, "_inbox", "TEAM.json")
    r = subprocess.run([sys.executable, tool, "--db", db, "--board", board],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=120)
    tail = (r.stdout + r.stderr).strip().splitlines()
    if r.returncode == 2 or not tail:
        return False, "transfer audit did not run cleanly", \
            "restore transfer_audit.py and the batch-K record"
    first = next((l for l in tail if l.startswith("untracked:")), None)
    if r.returncode != 0 or first:
        return False, first.replace("untracked: ", "") if first else \
            "transfer audit failed: %s" % tail[-1][:160], \
            "restore a completion-visible destination (file or owned task)"
    return True, tail[-1].strip(), ""


def check_contradictions(db):
    path = os.path.join(db, IDX, "CONTRADICTIONS.tsv")
    if not os.path.isfile(path):
        return False, "CONTRADICTIONS.tsv missing", "restore the contradiction ledger"
    open_rows, unknown = [], []
    for l in open(path, encoding="utf-8", errors="replace"):
        if l.startswith("#") or not l.strip():
            continue
        cells = l.rstrip("\n").split("\t")
        if len(cells) < 3 or cells[0] == "id":
            continue
        kind = cells[2].strip().upper()
        if kind in RESOLVED_CONTRA_KINDS:
            continue
        (open_rows if kind in ("OPEN", "FILED") else unknown).append(cells[0])
    if unknown:
        return False, "unrecognised contradiction kinds on %s" % ", ".join(unknown), \
            "disposition or correctly classify %s" % unknown[0]
    if open_rows:
        return False, "unresolved contradictions: %s" % ", ".join(open_rows), \
            "disposition %s" % open_rows[0]
    return True, "every contradiction carries a resolved disposition", ""


# A requirement-facts generation older than this no longer measures the live
# database (the controller rebuilds it on every board change, debounced to
# 300s, plus a 30-min reconcile - six hours stale means the pipeline is dead).
FAMILY_FACT_STALE_S = 6 * 3600
FAMILY_GATED = ("P", "DD", "DA", "F")


def check_families(root):
    """The four families the gate used to be blind to (OPUS notice
    OPUS-NOTICE-FRONTIER-GATE-BLIND-TO-FOUR-FAMILIES): P page obligations,
    DD documented documents, DA falsification passes, F function
    dispositions. Read the requirement facts captured by the newest
    committed dashboard generation (requirements.collect is the reader; the
    gate consumes its fresh output rather than re-walking the corpus inside
    a Stop hook). Missing, failed or stale facts are NOT_MET - a family the
    instrument cannot measure is not a met family.
    """
    store = os.path.join(root, "Database", "Tools", "work", "dashboard")
    try:
        gen = json.loads(open(os.path.join(store, "CURRENT"),
                              encoding="utf-8").read())["generation"]
        fp = os.path.join(store, gen, "inputs", "requirement_facts")
        facts = json.load(open(fp, encoding="utf-8"))
    except Exception as e:
        return False, "no requirement-family facts (CURRENT generation unreadable: %s)" % e, \
            "run a dashboard generation so P/DD/DA/F requirements are measured"
    try:
        age = time.time() - os.path.getmtime(fp)
    except OSError:
        age = FAMILY_FACT_STALE_S + 1
    if age > FAMILY_FACT_STALE_S:
        return False, "requirement facts are stale (%.0fh old, generation %s)" \
            % (age / 3600.0, gen), "refresh the dashboard generation"
    if facts.get("failed"):
        return False, "requirement collection failed: %s" \
            % sorted(facts["failed"]), "repair the failing readers"
    unmet = collections.Counter(
        x["f"] for x in facts.get("facts", [])
        if x.get("f") in FAMILY_GATED and not x.get("ok"))
    if unmet:
        first = sorted(unmet)[0]
        return False, "requirement families unmet: " + ", ".join(
            "%s=%d" % kv for kv in sorted(unmet.items())), \
            "close the %s family's open obligations" % first
    return True, "P/DD/DA/F requirement families fully met", ""


def check_acceptance(root):
    """Terminal receipts: committed AUDIT-LOG entry recording a complete clean
    thirty-pass run, pinned to a program state that still covers HEAD."""
    head = _head(root)
    if not head:
        return False, "cannot resolve HEAD", "run inside the repository"
    r = _git(root, "show", "HEAD:Database/FFXII TZA/_index/AUDIT-LOG.md")
    if r.returncode != 0:
        return False, "AUDIT-LOG.md not readable at HEAD", "restore the audit log"
    receipt_commits = []
    for l in r.stdout.splitlines():
        if RECEIPT_CLAIM.search(l) and RECEIPT_DONE.search(l):
            receipt_commits += [h for h in HEXTOKEN.findall(l) if len(h) >= 7]
    if not receipt_commits:
        return False, "no committed receipt of a complete clean thirty-pass run", \
            "run the final-audit streak and record it in AUDIT-LOG.md"
    for cand in reversed(receipt_commits):
        c = _git(root, "rev-parse", "--verify", "--quiet", cand + "^{commit}")
        if c.returncode != 0:
            continue
        anc = _git(root, "merge-base", "--is-ancestor", cand, "HEAD")
        if anc.returncode != 0:
            continue
        drift = _git(root, "diff", "--quiet", cand, "HEAD", "--",
                     "Database/FFXII TZA", *DRIFT_EXCLUDE)
        if drift.returncode == 0:
            return True, "terminal receipt at %s covers HEAD %s" % (cand, head[:9]), ""
        return False, "terminal receipt %s is stale: database changed since" % cand, \
            "re-run the thirty-pass streak against current state"
    return False, "receipt's named program state is not an ancestor of HEAD", \
        "re-record the receipt against the audited commit"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--root", default=KP.ROOT)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    checks = [
        ("scope", lambda: check_scope(a.db, a.root)),
        ("provenance", lambda: check_provenance(a.root)),
        ("verdicts", lambda: check_verdicts(a.db, a.root)),
        ("questions", lambda: check_questions(a.db)),
        ("transfers", lambda: check_transfers(a.db)),
        ("contradictions", lambda: check_contradictions(a.db)),
        ("families", lambda: check_families(a.root)),
        ("acceptance", lambda: check_acceptance(a.root)),
    ]
    detail, remaining, nxt, met = [], None, None, True
    for name, fn in checks:
        try:
            ok, rem, nx = fn()
        except Exception as e:  # a broken check is an unmet check - fail closed
            ok, rem, nx = False, "%s check failed: %s" % (name, e), \
                "restore the %s check" % name
        detail.append("%s: %s -- %s" % (name, "OK" if ok else "UNMET", rem))
        if not ok and remaining is None:
            remaining, nxt = rem, nx
        met = met and ok

    verdict = "MET" if met else "NOT_MET"
    if a.json:
        print(json.dumps({"verdict": verdict, "remaining": remaining,
                          "next": nxt, "detail": detail}, indent=1))
    else:
        print("DB_GOAL=%s" % verdict)
        if remaining:
            print("remaining=%s" % remaining)
            print("next=%s" % nxt)
        for d in detail:
            print("detail=%s" % d)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
