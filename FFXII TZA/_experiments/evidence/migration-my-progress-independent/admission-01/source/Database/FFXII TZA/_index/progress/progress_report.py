#!/usr/bin/env python3
"""progress_report.py -- the route to L1+L2, generated from exported inputs.

FRONTIER-REQ-SWE2-DATA-PROGRESS-ROUTE-REPORT (2026-09-27 directive), SWE2-DATA.
Repaired under FRONTIER-REQ-SWE2-DATA-PROGRESS-REPAIR-CKPT10 (checkpoint 10).

Reads ONLY the exported database set (OPEN-QUESTIONS, L2-VERDICTS,
CONTRADICTIONS.tsv, the batch-K transfer record, COVERAGE*, PROGRAM-STATE,
SYSTEM-MATRIX, PARITY-STATUS, TEAM.json, progress.config.json). No Tools/ or
Temp input *content* dependency: instruments are imported when present
(check_questions' status classifier, transfer_audit's obligation check) and the
report says which engine produced each number; a vendored fallback classifier
keeps the generator runnable standalone. Instrument *versions* are part of the
fingerprint: a check_questions.py or transfer_audit.py edit forces regeneration.

Outputs (staged atomically, committed as one generation; a failed run leaves
the last good set and marks snapshot.json INCOMPLETE):
  Database/FFXII TZA/PROGRESS.md        - brief summary, identity, freshness
  _index/progress/snapshot.json         - machine-readable state
  _index/progress/snapshot.md           - the route, human-readable
  _index/progress/crosswalk.md          - deduplicated obligation route
  _index/progress/metrics.md            - numerators/denominators/sources
  _index/progress/history.jsonl         - one line per SUCCESSFUL generation

Modes:
  generate   always regenerate (fails INCOMPLETE on missing/mid-build-moved
             inputs; nothing is published on failure)
  auto       regenerate only if the input fingerprint moved OR the output set
             is incoherent OR a .dirty mark is present; else stamps checked_at
             and reports UNCHANGED (the controller cadence hook)
  check      verify the output set exists, carries the live fingerprint
             coherently, and every stamped member agrees (CURRENT/STALE/
             INCOMPLETE/MISSING, exit 0/1/2)
  status     print the one-line state

Checkpoint-10 repair contract (asserted by test_progress_report.py):
  * terminal-sequence evidence comes from accepted receipts -- PROGRAM-STATE's
    declared `final_audits N / 30` counter plus AUDIT-LOG complete-run entries;
    `AUDIT-PASS*` files are per-round evidence documents, reported separately
    and never summed as passes (the two AUDIT-PASS13-ROUND* files are two
    rounds of one historical pass, not 2/30);
  * a LIVE cell counts toward MET only where its own text cites the governing
    L2 ruling that accepts it; bare LIVE is reported as LIVE-UNRULED;
  * reviewers resolve from actual assignment/receipt fields
    (reviewer/recipient/reviewed_by) -- never `requester`; absent identity is
    UNKNOWN;
  * accepted answers, dispositions, withdrawals, transfers, new debt and
    reopened work are separate counters; WITHDRAWN is never counted as learned;
  * the route is a deduplicated union of page / register / carrier / coverage /
    transfer obligations, each row carrying owner, reviewer, dependency,
    evidence, missing discriminator, next action and acceptance;
  * transferred required work stays visible as a completion obligation;
  * values the inputs cannot produce are UNMEASURED; proxies are labelled;
  * parity is read from PARITY-STATUS.md and is UNMEASURED when the ledger is
    absent or unparseable -- never implied PASS;
  * history.jsonl records successful publications only, one row per fingerprint
    (a duplicate trigger does not double-record);
  * `.dirty` forces regeneration even when the fingerprint is unchanged; the
    marker is consumed by the watchdog only after a successful run.
"""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent          # _index/progress/
DB = HERE.parents[1]                            # Database/FFXII TZA/
ROOT = DB.parents[1]                            # repo root
PARSER_VERSION = 4                              # bump on any parse-rule change

REQUIRED_INPUTS = [                             # missing -> INCOMPLETE
    "_index/OPEN-QUESTIONS.md",
    "_index/UNIDENTIFIED-OPEN-QUESTIONS.md",
    "_index/L2-VERDICTS.md",
    "_index/CONTRADICTIONS.tsv",
    "_index/candidates/register-triage/batch-K-scope-rulings.md",
    "_index/COVERAGE.md",
    "_index/COVERAGE-DIMENSIONS.md",
    "_index/PROGRAM-STATE.md",
    "_index/SYSTEM-MATRIX.md",
    "_index/_inbox/TEAM.json",
    "_index/progress/progress.config.json",
    # terminal_audit() consumed AUDIT-LOG.md unfingerprinted since 2026-09-28
    # - an edit to the receipted complete-run headings left the fingerprint
    # unmoved (CKPT10R2 C2). Consumed sources are fingerprinted, all of them.
    "_index/AUDIT-LOG.md",
]
OPTIONAL_INPUTS = [                             # missing -> UNMEASURED, not INCOMPLETE
    "_index/PARITY-STATUS.md",
    # FABLE's dated transition list for the route (commit, row, from, to,
    # record). A dated record, not current state; consumed for route links.
    "_index/candidates/fable-route-links-0927/fable-register-transitions.tsv",
]
INPUTS = REQUIRED_INPUTS + OPTIONAL_INPUTS      # fingerprint covers all

OUT_DIR = HERE
SNAP_JSON = OUT_DIR / "snapshot.json"
SNAP_MD = OUT_DIR / "snapshot.md"
CROSS_MD = OUT_DIR / "crosswalk.md"
MET_MD = OUT_DIR / "metrics.md"
HIST = OUT_DIR / "history.jsonl"
PROGRESS = DB / "PROGRESS.md"
DIRTY = OUT_DIR / ".dirty"
CONFIG = OUT_DIR / "progress.config.json"


class ProgressError(Exception):
    """A generation cannot be honestly produced; the named cause is published
    into snapshot.json as an INCOMPLETE state and the last-good set is kept."""


# ---------------------------------------------------------------- OQ status
# The status vocabulary and classification order are vendored from
# check_questions.py (verbatim rule, with attribution) so the generator does
# not depend on a Tools/ path; when that module IS importable it is used
# instead and a test asserts the two agree row for row.
OQ_CLOSED = ("ANSWERED", "CLOSED", "RECOVERED", "RESOLVED", "IDENTIFIED",
             "CONFIRMED", "ALREADY ANSWERED")
OQ_BLOCKED = ("STILL OPEN", "BLOCKED")
OQ_WITHDRAWN = ("WITHDRAWN", "DISSOLVED", "SUPERSEDED", "NOT A DEFECT",
                "NOT A QUESTION")
# OEB (FRONTIER ruling 2026-09-27, batch-K extension): the class-3 terminal
# state, closed for the gate but unanswered in fact - NOT a synonym of NAS.
# Vendored in parity with check_questions.py's NO_ADMISSIBLE += (line ~90).
OQ_NO_ADMISSIBLE = ("NO ADMISSIBLE SOURCE", "OUT OF EVIDENCE BOUNDARY")
OQ_PARTIAL = ("ADVANCED", "PARTIAL", "PARTLY", "SHARPENED", "BOUNDED",
              "CHARACTERISED", "REVISED", "SUPPORTED", "IN PROGRESS", "LEANS",
              "VALUES ANSWERED", "LOCATION ANSWERED", "ANSWERED STRUCTURALLY",
              "THE FILE IS IDENTIFIED")
OQ_BARE = {"OPEN": "OPEN", "BLOCKED": "BLOCKED", "IN PROGRESS": "PARTIAL",
           "PARTIAL": "PARTIAL", "CLOSED": "ANSWERED", "ANSWERED": "ANSWERED"}
CELL = re.compile(r"(?<!\\)\|")
LEAD_STRUCK = re.compile(r"^\s*~~(.+?)~~\s*", re.S)


def _vendored_classify(rest):
    """Port of check_questions.classify - see that file's comments for the
    measured hazards this ordering exists to defeat."""
    cells = [c.strip() for c in CELL.split(rest) if c.strip() != ""]
    if cells and cells[-1] in OQ_BARE:
        return OQ_BARE[cells[-1]], cells
    lead = LEAD_STRUCK.sub("", cells[-1]).lstrip("*~ \t").upper()[:48] \
        if len(cells) >= 2 else ""
    for group, verdict in ((OQ_BLOCKED, "BLOCKED"), (OQ_NO_ADMISSIBLE, "ANSWERED"),
                           (OQ_WITHDRAWN, "WITHDRAWN"), (OQ_CLOSED, "ANSWERED"),
                           (OQ_PARTIAL, "PARTIAL")):
        for k in group:
            if lead.startswith(k):
                return verdict, cells
    if lead.startswith("OPEN"):
        return "OPEN", cells
    body = " ".join(cells)
    for m in re.finditer(r"\*\*([^*]{2,}?)\*\*", body):
        tok = m.group(1).upper().lstrip()[:48]
        for k in OQ_BLOCKED:
            if tok.startswith(k):
                return "BLOCKED", cells
        for k in OQ_CLOSED:
            if tok.startswith(k):
                return "ANSWERED", cells
        for k in OQ_PARTIAL:
            if tok.startswith(k):
                return "PARTIAL", cells
        if tok.startswith("OPEN"):
            return "OPEN", cells
    # A row with a question and NO answer cell is genuinely open.
    if len(cells) < 2:
        return "OPEN", cells
    # A known-length row whose lead word the vocabulary does not know is
    # unreadable, not open - UNKNOWN keeps the two apart.
    return "UNKNOWN", cells


def _classifier():
    """Prefer the live instrument; fall back to the vendored port.
    Returns (fn, engine_name)."""
    try:
        sys.path.insert(0, str(ROOT / "Database" / "Tools" / "analysis-kit"
                                 / "gfz-scripts"))
        import check_questions  # noqa
        return check_questions.classify, "check_questions.classify"
    except Exception:
        return _vendored_classify, "vendored-port-v%d" % PARSER_VERSION


OQ_ALL_LEADS = (OQ_NO_ADMISSIBLE + OQ_WITHDRAWN + OQ_CLOSED
                + OQ_PARTIAL + OQ_BLOCKED)


def _lead_keyword(cells):
    """The status cell's matched lead keyword (e.g. NO ADMISSIBLE SOURCE,
    SUPERSEDED, ANSWERED) - what classify() keyed on. Needed because the
    ANSWERED verdict merges true answers with approved dispositions (NAS/OEB)
    and WITHDRAWN merges superseded / not-a-question / dissolved / other -
    a report must keep them separate."""
    if len(cells) < 2:
        return ""
    lead = LEAD_STRUCK.sub("", cells[-1]).lstrip("*~ \t").upper()[:64]
    for k in OQ_ALL_LEADS:
        if lead.startswith(k):
            return k
    if lead.startswith("OPEN"):
        return "OPEN"
    return ""


# ------------------------------------------------------------------ parsers
def parse_questions(path, classify):
    """OPEN-QUESTIONS rows -> {id, status, lead, owner_doc, question_first_line,
    status_text}."""
    out = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^\|\s*(~~)?([A-Z]+-\d+(?:/[a-z]|[a-z])?)(~~)?\s*\|(.*)$",
                     line)
        if not m:
            continue
        rid, rest = m.group(2), m.group(4)
        verdict, cells = classify(rest)
        owner = cells[1] if len(cells) > 2 else ""
        q = re.sub(r"\s+", " ", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1",
                                       cells[0]))[:110]
        status_text = re.sub(
            r"\s+", " ", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1",
                                cells[-1]))[:160] if cells else ""
        out.append({"id": rid, "status": verdict, "lead": _lead_keyword(cells),
                    "owner": owner.strip("*` "), "question": q,
                    "status_text": status_text})
    return out


VERDICT_WORD = re.compile(
    r"^[\s*~`(]*\b(N/A|NOT MET|SCOPE-SHORT|PARTIAL|MIXED|MET|LIVE|UNSCORED|"
    r"PENDING|BLOCKED)\b")


def _cell_verdict(cell):
    m = VERDICT_WORD.match(cell.strip())
    return m.group(1) if m else "UNSCORED"


LIVE_RULING = re.compile(
    r"(?i)(?:criterion[\s\S]{0,40}?ruling|ruling[\s~`*]*\d{4}-\d{2}-\d{2})")


def live_accepted(cell_text):
    """A LIVE cell counts as satisfied only where the cell's own text cites the
    governing ruling that accepts it (e.g. 'Criterion: `runtime` ruling
    2026-09-25'). Bare LIVE - including the words 'no ruling' - is unruled and
    never folds into MET."""
    return bool(LIVE_RULING.search(cell_text))


def parse_verdicts(path):
    """L2-VERDICTS.md per-system table ->
    [{system, name, contract..script_data (verdict words), l2, gap,
      cell_text: {dimension: raw cell}}]."""
    rows = []
    if not path.exists():
        return rows
    in_table = False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if re.match(r"^\|\s*system\s*\|\s*contract\s*\|", line):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|") or re.match(r"^\|[-\s|]+\|?$", line):
            if rows or re.match(r"^\|[-\s|]+\|?$", line):
                continue
        cells = [c for c in CELL.split(line)]
        cells = [c.strip() for c in cells]
        if len(cells) < 7 or not re.match(r"(\*\*)?S-\d+", cells[1]):
            continue
        name = re.sub(r"\*\*", "", cells[1])
        sid = name.split()[0]
        sysname = name[len(sid):].strip()
        rows.append({
            "system": sid, "name": sysname,
            "contract": _cell_verdict(cells[2]), "types": _cell_verdict(cells[3]),
            "relationships": _cell_verdict(cells[4]),
            "runtime": _cell_verdict(cells[5]),
            "script_data": _cell_verdict(cells[6]),
            "l2": _cell_verdict(cells[7]) if len(cells) > 7 else "UNSCORED",
            "gap": re.sub(r"\s+", " ", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1",
                          re.sub(r"\*\*", "", cells[8])))[:160]
            if len(cells) > 8 else "",
            "cell_text": {"contract": cells[2], "types": cells[3],
                          "relationships": cells[4], "runtime": cells[5],
                          "script_data": cells[6]},
        })
    return rows


def dim_satisfied(v, dim):
    """Whether one L2 cell is satisfied: MET, N/A doesn't count toward MET but
    isn't a blocker, and LIVE counts only when its cell text cites the ruling."""
    code = v[dim]
    if code == "MET":
        return True
    if code == "LIVE":
        return live_accepted(v.get("cell_text", {}).get(dim, ""))
    return False


def parse_contradictions(path):
    rows = 0
    kinds = Counter()
    if not path.exists():
        return {"rows": 0, "kinds": {}, "engine": "missing"}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if parts[0] == "id" or len(parts) < 3:
            continue
        rows += 1
        kinds[parts[2]] += 1
    # every ledger row is a resolved disposition; an OPEN kind would count here
    return {"rows": rows, "kinds": dict(kinds), "engine": "tsv-parse"}


def _reviewer_of(t):
    """Reviewer resolves from actual assignment/receipt fields only --
    `reviewer`, `recipient`, `reviewed_by` -- never `requester`/`requested_by`.
    A task carrying none has UNKNOWN."""
    for k in ("reviewer", "recipient", "reviewed_by"):
        v = t.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return "UNKNOWN"


def parse_board(path):
    """TEAM.json -> identity + open package list."""
    try:
        b = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"identity": None, "open": [], "counts": {}, "tasks": []}
    tasks = b.get("tasks", [])
    open_tasks = [t for t in tasks if t.get("status") in
                  ("READY", "ACTIVE", "BLOCKED")]
    counts = Counter(t.get("status") for t in tasks)
    # prerequisite ordering: a task is ordered after its unfinished deps
    done = {t["id"] for t in tasks if t.get("status") == "DONE"}
    def unfinished_deps(t):
        return sum(1 for d in t.get("dependencies", []) if d not in done)
    def prio(t):
        p = str(t.get("priority", "P9"))
        return int(p[1:]) if p.startswith("P") and p[1:].isdigit() else 9
    open_sorted = sorted(open_tasks,
                         key=lambda t: (unfinished_deps(t), prio(t),
                                        t.get("status") != "ACTIVE",
                                        t.get("id", "")))
    pk = []
    for t in open_sorted:
        blocked_by = [d for d in t.get("dependencies", []) if d not in done]
        disc = "external/runtime" if t.get("kind") == "runtime" else \
               "blocked by " + ",".join(blocked_by) if blocked_by else \
               "waiting-review" if t.get("kind") == "contradiction" else \
               "research"
        evidence = t.get("known_evidence") or t.get("description") \
            or t.get("note") or t.get("summary") or ""
        pk.append({"id": t.get("id"), "kind": t.get("kind"),
                   "status": t.get("status"), "priority": t.get("priority"),
                   "owner": t.get("assigned_to") or t.get("agent") or "UNASSIGNED",
                   "reviewer": _reviewer_of(t),
                   "target": str(t.get("target", ""))[:140],
                   "acceptance": str(t.get("completion", ""))[:140],
                   "evidence": str(evidence)[:160],
                   "blocked_by": blocked_by, "discriminator": disc})
    return {"identity": {"revision": b.get("revision"),
                         "epoch": b.get("recovery_epoch"),
                         "phase": b.get("phase")},
            "open": pk, "counts": dict(counts),
            "total": len(tasks), "tasks": tasks}


def parse_transfers(db):
    """transfer_audit obligations: (problems, checked) via the instrument."""
    try:
        sys.path.insert(0, str(ROOT / "Database" / "Tools" / "analysis-kit"
                                 / "gfz-scripts"))
        import transfer_audit
        problems, checked = transfer_audit.audit(str(db),
                                                 str(db / "_index/_inbox/TEAM.json"))
        return {"engine": "transfer_audit.audit", "obligations": len(checked),
                "untracked": len(problems), "problems": problems[:20]}
    except Exception as e:
        return {"engine": "UNMEASURED (%s)" % type(e).__name__,
                "obligations": None, "untracked": None, "problems": []}


def parse_route_links(db):
    """FABLE's dated transition record (fable-route-links-0927 TSV):
    commit / row / from / to / record. A dated transition list, NOT current
    state - consumed so the route can cite where rows went. Rows whose TSV
    'row' field fails the register-id pattern are parse hazards carried in
    `dropped` rather than silently discarded."""
    p = (db / "_index" / "candidates" / "fable-route-links-0927"
         / "fable-register-transitions.tsv")
    rec = {"source": "_index/candidates/fable-route-links-0927/",
           "tsv": p.name if p.exists() else None,
           "dated_record": True,
           "transitions": 0, "to_counts": {}, "moved": [], "dropped": 0}
    if not p.exists():
        rec["state"] = "UNMEASURED"
        return rec
    for line in p.read_text(encoding="utf-8",
                            errors="replace").splitlines()[1:]:
        f = line.split("\t")
        if len(f) < 5 or not re.match(r"^[A-Z]+-\d+(/[a-z]|[a-z])?$", f[1]):
            if line.strip():
                rec["dropped"] += 1
            continue
        rec["transitions"] += 1
        to = f[3].strip().upper()
        rec["to_counts"][to] = rec["to_counts"].get(to, 0) + 1
        if to in ("SUPERSEDED", "NO ADMISSIBLE SOURCE",
                  "OUT OF EVIDENCE BOUNDARY"):
            rec["moved"].append({"row": f[1], "commit": f[0],
                                 "from": f[2].strip(), "to": to,
                                 "record": f[4].strip()})
    rec["state"] = "CURRENT"
    return rec


def _git_tracked(db):
    """Set of db-relative posix paths known to the index (one git call);
    None when git cannot answer."""
    try:
        prefix = os.path.relpath(str(db), str(ROOT)).replace(os.sep, "/")
        if prefix.startswith(".."):
            return None
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z", "--", prefix],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=30).stdout
        return set(x[len(prefix) + 1:] for x in out.split("\0")
                   if x.startswith(prefix + "/"))
    except Exception:
        return None


def parse_page_boxes(db):
    """Unticked checkbox obligations the register never counts.

    check_questions.read_boxes enumerates every `- [ ]`/`- [x]` block;
    the UNTICKED subset is split three ways:

      * no_id     - page-local residue naming no register row. The class
                    OPUS's structural-obligations census (2026-09-28)
                    measured as invisible to the gate's questions
                    dimension. These stay page-local work-items, not
                    register questions - but they are COUNTED here.
      * closed_id - boxes naming only rows the register already records
                    as closed (ANSWERED/WITHDRAWN). Mis-marked residue:
                    the row is closed for the gate yet the box still
                    reads as pending work.
      * open_id   - boxes naming a live (OPEN/PARTIAL/BLOCKED/UNKNOWN)
                    row - honest pending residue already counted via
                    its row.

    UNMEASURED when the instrument or register is unreadable - a missing
    reader must not read as zero obligations."""
    try:
        sys.path.insert(0, str(ROOT / "Database" / "Tools" / "analysis-kit"
                                 / "gfz-scripts"))
        import check_questions
        boxes = check_questions.read_boxes(str(db))
        reg, _dupes = check_questions.read_table(str(db))
        tracked = _git_tracked(db)
    except Exception as e:
        return {"engine": "UNMEASURED (%s)" % type(e).__name__}
    closed = ("ANSWERED", "WITHDRAWN")
    out = {"engine": "check_questions.read_boxes",
           "no_id": 0,
           "no_id_untracked": 0 if tracked is not None else None,
           "closed_id": 0, "open_id": 0}
    for rel, _line, ticked, ids, _text in boxes:
        if ticked:
            continue
        if not ids:
            out["no_id"] += 1
            if tracked is not None and rel not in tracked:
                out["no_id_untracked"] += 1
        elif any(reg.get(i, "OPEN") not in closed for i in ids):
            out["open_id"] += 1
        else:
            out["closed_id"] += 1
    return out


def count_system_docs(db):
    """system: frontmatter docs per top-level category (program_coverage rule:
    non-index documents carrying a `system:` key)."""
    per_cat = Counter()
    total = 0
    for dp, dns, fns in os.walk(db):
        rel = os.path.relpath(dp, db).replace(os.sep, "/")
        top = rel.split("/")[0]
        if top.startswith("_") or top == ".":
            continue
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            try:
                head = open(os.path.join(dp, fn), encoding="utf-8",
                            errors="replace").read(4000)
            except OSError:
                continue
            if re.search(r"^system\s*:", head, re.M):
                per_cat[top] += 1
                total += 1
    return {"total": total, "per_category": dict(per_cat)}


def terminal_audit(db):
    """Terminal-sequence evidence from ACCEPTED RECEIPTS, not filenames.

    Receipted sources:
      * PROGRAM-STATE.md's declared `final_audits N / 30` -- the protocol's own
        counter (its Recording rule: one AUDIT-LOG entry per complete run);
      * AUDIT-LOG.md complete-run headings (a run is logged only when all
        thirty passes complete clean);
      * `AUDIT-PASS*` documents are round-evidence artefacts, counted
        separately and NEVER summed as passes -- AUDIT-PASS13-ROUND1/ROUND2
        are two rounds of one historical pass.
    """
    declared = None
    ps = db / "_index" / "PROGRAM-STATE.md"
    if ps.exists():
        m = re.search(r"final_audits[^0-9]*(\d+)\s*/\s*30",
                      ps.read_text(encoding="utf-8", errors="replace"))
        if m:
            declared = int(m.group(1))
    receipts = 0
    al = db / "_index" / "AUDIT-LOG.md"
    if al.exists():
        receipts = len(re.findall(
            r"^#+.*(?:final[- ]audit|thirty[- ]pass).*(?:complete|clean) run",
            al.read_text(encoding="utf-8", errors="replace"),
            flags=re.M | re.I))
    artefacts = 0
    for d in (db, db / "_index"):
        if d.exists():
            artefacts += sum(1 for f in d.iterdir()
                             if re.match(r"AUDIT-PASS", f.name))
    return {"final_audits_declared": declared,
            "audit_log_complete_runs": receipts,
            "audit_pass_artefacts": artefacts,
            "required_consecutive": 30}


def parity_status(db):
    """Parity certification from PARITY-STATUS.md ('N of M pilots certified').
    Absent or unparseable -> UNMEASURED; never implied PASS."""
    p = db / "_index" / "PARITY-STATUS.md"
    if not p.exists():
        return {"label": "UNMEASURED", "certified": None, "of": None}
    m = re.search(r"(\d+)\s+of\s+(\d+)\s+pilots certified",
                  p.read_text(encoding="utf-8", errors="replace"))
    if not m:
        return {"label": "UNMEASURED", "certified": None, "of": None}
    return {"label": "%s of %s pilots certified" % (m.group(1), m.group(2)),
            "certified": int(m.group(1)), "of": int(m.group(2))}


# --------------------------------------------------------------- fingerprint
def _sha(path):
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _doc_signature(db):
    """Hash the consumed document surface: each non-index document's path
    plus the first 4000 bytes (the frontmatter window) - INCLUDING root-level
    documents such as the AUDIT-PASS* artefacts terminal_audit() consumes
    (CKPT10R2 C2: every consumed source is fingerprinted; the generated
    PROGRESS.md is the only exclusion). A document appearing, disappearing,
    or frontmatter-editing moves the fingerprint."""
    h = hashlib.sha256()
    for dp, dns, fns in os.walk(db):
        rel = os.path.relpath(dp, db).replace(os.sep, "/")
        top = rel.split("/")[0]
        if top.startswith("_"):
            continue
        for fn in sorted(fns):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            # PROGRESS.md is a generated OUTPUT - hashing it would make the
            # fingerprint self-referential (every commit would invalidate it).
            if os.path.abspath(p) == os.path.abspath(str(PROGRESS)):
                continue
            try:
                with open(p, "rb") as f:
                    head = f.read(4000)
            except OSError:
                head = b""
            h.update(os.path.relpath(p, db).replace(os.sep, "/").encode())
            h.update(b"\x00")
            h.update(head)
            h.update(b"\x00")
    return h.hexdigest()


def fingerprint(db):
    """Coherent input capture. Covers: parser version, this file's sha, the
    config sha, every input sha (MISSING marker when absent), the consumed
    document tree, every consumed instrument's sha (external classifier +
    transfer audit + generator versions), and the board revision/epoch."""
    h = hashlib.sha256()
    h.update(("parser=%d" % PARSER_VERSION).encode())
    h.update((_sha(HERE / "progress_report.py") or "-").encode())
    for rel in INPUTS:
        h.update(rel.encode())
        h.update((_sha(db / rel) or "MISSING").encode())
    h.update(b"docs:")
    h.update(_doc_signature(db).encode())
    for name in ("check_questions.py", "transfer_audit.py"):
        h.update(name.encode())
        h.update((_sha(ROOT / "Database" / "Tools" / "analysis-kit"
                       / "gfz-scripts" / name) or "MISSING").encode())
    try:
        j = json.loads((db / "_index/_inbox/TEAM.json")
                       .read_text(encoding="utf-8"))
        h.update(str(j.get("revision")).encode())
        h.update(str(j.get("epoch", j.get("recovery_epoch"))).encode())
    except Exception:
        h.update(b"board:unreadable")
    return h.hexdigest()


def missing_inputs(db):
    """Required inputs absent from the database tree -> the run is INCOMPLETE.
    Optional inputs are fingerprinted (so their appearance/disappearance
    regenerates) but never block."""
    return [rel for rel in REQUIRED_INPUTS if not (db / rel).exists()]


def input_problems(db):
    """(missing, invalid) required inputs. A present-but-empty or unparseable
    required input is INVALID: "missing or invalid required evidence cannot
    become zero CURRENT work" (CKPT10R2 C3) - an empty file is never a
    schema-valid register. A *cleared* register still parses: a .tsv keeps
    its header, a .md keeps a heading or table, TEAM.json keeps "tasks" - so
    the test is structural, never "has rows"."""
    missing, invalid = [], []
    for rel in REQUIRED_INPUTS:
        p = db / rel
        if not p.exists():
            missing.append(rel)
            continue
        try:
            if p.stat().st_size == 0:
                invalid.append("%s (empty file)" % rel)
                continue
            if rel.endswith(".json"):
                j = json.loads(p.read_text(encoding="utf-8"))
                if rel.endswith("TEAM.json") and \
                        not isinstance(j.get("tasks"), list):
                    invalid.append("%s (no 'tasks' list)" % rel)
            else:
                text = p.read_text(encoding="utf-8",
                                   errors="replace")
                if not text.strip():
                    invalid.append("%s (whitespace only)" % rel)
                elif rel.endswith(".tsv") \
                        and "\t" not in text and "|" not in text:
                    # a .tsv with no delimiter on any line is truncated or
                    # misnamed - a cleared register still keeps its header
                    invalid.append("%s (no delimiter structure)" % rel)
        except (OSError, ValueError):
            invalid.append("%s (unreadable or unparseable)" % rel)
    return missing, invalid


def git_head():
    try:
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse",
                               "--short=9", "HEAD"], capture_output=True,
                              text=True, timeout=15).stdout.strip()
    except Exception:
        return "unknown"


# ------------------------------------------------------------------- deltas
def history_append(counters, fp):
    """Record a SUCCESSFUL publication only -- one row per fingerprint; a
    duplicate trigger for the same generation does not double-record, and a
    failed candidate never reaches this function."""
    rec = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "fp": fp[:16], **counters}
    try:
        last = None
        if HIST.exists():
            for line in HIST.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    last = line
        if last and json.loads(last).get("fp") == rec["fp"]:
            return rec
        with open(HIST, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    except OSError:
        pass
    return rec


def deltas(counters):
    """vs previous entry and vs first entry >=24h / >=7d old."""
    prev, d24, d7 = None, None, None
    now = datetime.now(timezone.utc)
    try:
        lines = HIST.read_text(encoding="utf-8").strip().splitlines()
    except OSError:
        lines = []
    for line in lines:
        try:
            rec = json.loads(line)
            age = (now - datetime.fromisoformat(rec["ts"])).total_seconds()
        except (ValueError, KeyError):
            continue
        prev = rec
        if age >= 86400 and d24 is None:
            d24 = rec
        if age >= 7 * 86400 and d7 is None:
            d7 = rec
    def diff(a, b):
        if not a or not b:
            return None
        keys = set(a) | set(b)
        out = {}
        for k in keys - {"ts", "fp"}:
            if isinstance(a.get(k), (int, float)) and isinstance(b.get(k), (int, float)):
                dv = b[k] - a[k]
                if dv:
                    out[k] = dv
        return out or {}
    return {"vs_prior": diff(prev, counters) if prev else None,
            "over_24h": diff(d24, counters) if d24 else None,
            "over_7d": diff(d7, counters) if d7 else None}


# ------------------------------------------------------------------- build
def build(db):
    """Build the snapshot from a coherent input capture.

    Fails ProgressError before publishing anything when a required input is
    missing (INCOMPLETE -- last-good set retained) or when an input moved
    between the pre-build and post-build captures (mid-build move)."""
    missing, invalid = input_problems(db)
    if missing or invalid:
        raise ProgressError(
            "INCOMPLETE - " + "; ".join(
                (["required input(s) missing: " + ", ".join(missing)]
                 if missing else []) +
                (["required input(s) invalid: " + ", ".join(invalid)]
                 if invalid else [])))
    fp0 = fingerprint(db)

    classify, engine = _classifier()
    oq = parse_questions(db / "_index/OPEN-QUESTIONS.md", classify)
    oq_st = Counter(r["status"] for r in oq)
    unid = parse_questions(db / "_index/UNIDENTIFIED-OPEN-QUESTIONS.md", classify)
    unid_st = Counter(r["status"] for r in unid)
    verdicts = parse_verdicts(db / "_index/L2-VERDICTS.md")
    dims = ["contract", "types", "relationships", "runtime", "script_data"]
    dim_counts = {d: Counter(v[d] for v in verdicts) for d in dims}
    # satisfied per dimension: MET plus LIVE only where the cell cites its
    # governing ruling; bare LIVE is counted apart and never folds into MET.
    dim_met = {d: sum(1 for v in verdicts if dim_satisfied(v, d)) for d in dims}
    dim_live_unruled = {d: sum(1 for v in verdicts
                               if v[d] == "LIVE" and not dim_satisfied(v, d))
                        for d in dims}
    l2_counts = Counter(v["l2"] for v in verdicts)
    board = parse_board(db / "_index/_inbox/TEAM.json")
    transfers = parse_transfers(db)
    page_boxes = parse_page_boxes(db)
    contra = parse_contradictions(db / "_index/CONTRADICTIONS.tsv")
    docs = count_system_docs(db)
    term = terminal_audit(db)
    parity = parity_status(db)
    links = parse_route_links(db)
    reopened = sum(1 for t in board.get("tasks", [])
                   if re.search(r"reopen", str(t.get("note", "") or "")
                                + str(t.get("checkpoint", "") or ""), re.I)
                   and str(t.get("status", "")).upper() in ("READY", "ACTIVE"))

    # GAP B (FABLE-NOTICE-SWE2DATA-ROUTE-LINKS-AND-TWO-CLASSIFIER-GAPS):
    # classify() merges approved dispositions into ANSWERED and merges several
    # disposition classes into WITHDRAWN - right for a closed-or-not gate,
    # wrong for a learned-state report. Split by the row's lead keyword.
    n_answered = oq_st.get("ANSWERED", 0)
    n_nas = sum(1 for r in oq
                if r["status"] == "ANSWERED"
                and r["lead"] == "NO ADMISSIBLE SOURCE")
    n_oeb = sum(1 for r in oq
                if r["status"] == "ANSWERED"
                and r["lead"] == "OUT OF EVIDENCE BOUNDARY")
    withdrawn = [r for r in oq + unid if r["status"] == "WITHDRAWN"]
    withdrawn_kinds = Counter(
        r["lead"] if r["lead"] in OQ_WITHDRAWN else "OTHER/DUPLICATE"
        for r in withdrawn)
    # Superseded rows carry moved residue - required work living elsewhere.
    # They stay closed for the gate but remain listed in the route.
    superseded = [r for r in withdrawn if r["lead"] == "SUPERSEDED"]

    counters = {
        "oq_open": oq_st.get("OPEN", 0), "oq_partial": oq_st.get("PARTIAL", 0),
        "oq_blocked": oq_st.get("BLOCKED", 0),
        # accepted answers EXCLUDE approved dispositions (NAS/OEB) - those are
        # closed for the gate but unanswered in fact, counted separately.
        "oq_answered": n_answered - n_nas - n_oeb,
        "oq_disposition_nas": n_nas,          # approved disposition, not learned
        "oq_disposition_oeb": n_oeb,          # OUT OF EVIDENCE BOUNDARY, class 3
        "oq_withdrawn": oq_st.get("WITHDRAWN", 0),  # never counted as learned
        "withdrawn_superseded": withdrawn_kinds.get("SUPERSEDED", 0),
        "withdrawn_not_a_question": withdrawn_kinds.get("NOT A QUESTION", 0),
        "withdrawn_not_a_defect": withdrawn_kinds.get("NOT A DEFECT", 0),
        "withdrawn_dissolved": withdrawn_kinds.get("DISSOLVED", 0),
        "withdrawn_other": sum(v for k, v in withdrawn_kinds.items()
                               if k in ("WITHDRAWN", "OTHER/DUPLICATE")),
        "oq_unknown": oq_st.get("UNKNOWN", 0),
        "unid_open": unid_st.get("OPEN", 0),
        "unid_partial": unid_st.get("PARTIAL", 0),
        "l2_systems": len(verdicts), "l2_met": l2_counts.get("MET", 0),
        "l2_cells_satisfied": sum(dim_met.values()),
        "l2_live_unruled": sum(dim_live_unruled.values()),
        "tasks_open": len(board["open"]),
        "debt_ready": board["counts"].get("READY", 0),
        "reopened": reopened,
        "transfers_untracked": transfers["untracked"] if transfers["untracked"] is not None else -1,
        "page_obligations": page_boxes.get("no_id", -1)
            if page_boxes.get("no_id") is not None else -1,
        "page_boxes_closed_id": page_boxes.get("closed_id", -1),
        "contra_rows": contra["rows"],
        "system_docs": docs["total"],
        "final_audits": term["final_audits_declared"] if term["final_audits_declared"] is not None else -1,
        "audit_pass_artefacts": term["audit_pass_artefacts"],
        "parity_certified": parity["certified"] if parity["certified"] is not None else -1,
    }
    snap = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "identity": {"git_head": git_head(),
                     "board": board["identity"]},
        "freshness": {"state": "CURRENT",
                      "fingerprint": fp0,
                      "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        "engines": {"oq_classifier": engine,
                    "transfers": transfers["engine"],
                    "page_boxes": page_boxes["engine"],
                    "parser_version": PARSER_VERSION,
                    "generator_sha256": _sha(HERE / "progress_report.py"),
                    "config_sha256": _sha(CONFIG)},
        "levels": {
            "L1_modding_grade": {
                "open_questions": {k: v for k, v in sorted(oq_st.items())},
                "open_questions_dispositions": {
                    "accepted_answers": n_answered - n_nas - n_oeb,
                    "no_admissible_source": n_nas,
                    "out_of_evidence_boundary": n_oeb,
                    "withdrawn_by_lead": dict(
                        sorted(withdrawn_kinds.items())),
                    "note": "ANSWERED merges learned answers with approved "
                            "dispositions; NAS and OEB are closed for the gate "
                            "but unanswered in fact. WITHDRAWN merges "
                            "superseded / not-a-question / dissolved / other - "
                            "the lead column keeps them apart."},
                "unidentified_open_questions": {k: v for k, v in sorted(unid_st.items())},
                "system_documents": docs,
                "terminal_audit": term,
            },
            "L2_reconstruction_grade": {
                "systems_scored": len(verdicts),
                "per_dimension": {d: dict(dim_counts[d]) for d in dims},
                "per_dimension_satisfied": dim_met,
                "per_dimension_live_unruled": dim_live_unruled,
                "verdict_column": dict(l2_counts),
                "systems": verdicts,
            },
            "residual_required_knowledge": {
                "oq_open_ids": [r["id"] for r in oq if r["status"] == "OPEN"],
                "oq_partial_ids": [r["id"] for r in oq if r["status"] == "PARTIAL"],
                "oq_blocked_ids": [r["id"] for r in oq if r["status"] == "BLOCKED"],
                "oq_open_rows": [r for r in oq
                                 if r["status"] in ("OPEN", "PARTIAL", "BLOCKED")],
                # Superseded rows are closed for the gate but their residue
                # moved to a named carrier - required work still owned
                # elsewhere. Listed (not reopened) so the route keeps them.
                "superseded_residue_rows": [
                    {"id": r["id"], "owner": r["owner"],
                     "status_text": r["status_text"]} for r in superseded],
                "contradictions": contra,
            },
            "terminal_certification": {
                "final_audits_declared": term["final_audits_declared"],
                "audit_log_complete_runs": term["audit_log_complete_runs"],
                "audit_pass_artefacts": term["audit_pass_artefacts"],
                "required_consecutive": 30,
                "note": "FINAL-AUDIT-PROTOCOL: thirty consecutive passes from "
                        "pass 1; the count is the PROGRAM-STATE receipted "
                        "counter plus AUDIT-LOG complete-run entries - "
                        "AUDIT-PASS* files are per-round evidence documents, "
                        "never terminal passes. L2 verdicts all-MET and "
                        "OPEN-QUESTIONS empty are preconditions tracked above."},
            "parity": parity,
            "L3": "excluded by directive - out of scope",
        },
        "transfers": transfers,
        "page_boxes": page_boxes,
        "route_links": links,
        "packages": board["open"],
        "board_counts": board["counts"], "board_total": board["total"],
        "board_task_count": board.get("total", 0),
    }
    d = deltas(counters)
    snap["deltas"] = d

    # Coherency: every consumed input is re-captured; if anything moved during
    # the build, this generation is aborted and nothing is published.
    if fingerprint(db) != fp0:
        raise ProgressError(
            "INCOMPLETE - an input moved during generation; "
            "aborted, prior generation retained")
    return snap, counters


# ------------------------------------------------------------------ writers
def _atomic_write(path, text):
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, str(path))
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _output_paths(db):
    return [SNAP_JSON, SNAP_MD, CROSS_MD, MET_MD, PROGRESS]


def _plan(snap):
    return [(SNAP_JSON, json.dumps(snap, indent=1) + "\n"),
            (SNAP_MD, _snapshot_md(snap)),
            (CROSS_MD, _crosswalk_md(snap)),
            (MET_MD, _metrics_md(snap)),
            (PROGRESS, _progress_md(snap))]


def _semantics_sha(snap):
    """sha256 over the snapshot's semantic payload - every field except the
    volatile meta (generated_at / freshness / semantics_sha256 itself). The
    fingerprint proves WHICH inputs produced the generation; this proves the
    PUBLISHED CONTENTS are still what that generation committed - a wiped
    levels/packages section is tamper even when the fp field survives
    (CKPT10R2 C1)."""
    payload = {k: v for k, v in snap.items()
               if k not in ("generated_at_utc", "freshness",
                            "semantics_sha256")}
    return hashlib.sha256(json.dumps(payload, sort_keys=True,
                                   default=str).encode("utf-8")).hexdigest()


def _semantic_problems(snap):
    """snapshot.json semantic binding check (CKPT10R2 C1): the recorded
    semantics_sha256 must exist and recompute to the same value. An absent
    field is treated as tamper/incomplete, not legacy-silent."""
    recorded = snap.get("semantics_sha256")
    if not recorded:
        return ["snapshot.json carries no semantics_sha256"]
    if _semantics_sha(snap) != recorded:
        return ["snapshot.json semantic contents altered "
                "(semantics_sha256 mismatch)"]
    return []


def _verify_outputs(snap):
    """Problems in the committed set: missing/empty members, a stamped member
    not carrying this generation's fingerprint, or (when the snapshot records
    per-output content hashes) a member whose bytes differ from what the
    generation committed - a tampered or mixed set."""
    fp = snap["freshness"]["fingerprint"]
    problems = list(_semantic_problems(snap))
    for p in _output_paths(DB):
        if not p.exists() or p.stat().st_size == 0:
            problems.append("%s missing or empty" % p.name)
    recorded = snap.get("outputs") or {}
    cid = snap.get("commit_id")
    for p in (SNAP_MD, CROSS_MD, MET_MD, PROGRESS):
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if p.name in recorded:
            if hashlib.sha256(p.read_bytes()).hexdigest() \
                    != recorded[p.name]:
                problems.append("%s content does not match the committed "
                                "generation" % p.name)
        elif fp[:12] not in text:
            problems.append("%s does not carry fp %s" % (p.name, fp[:12]))
        if cid and ("commit:** `%s`" % cid) not in text:
            problems.append("%s does not carry commit %s"
                            % (p.name, cid))
    if SNAP_JSON.exists():
        try:
            j = json.loads(SNAP_JSON.read_text(encoding="utf-8"))
            if j.get("freshness", {}).get("fingerprint") != fp:
                problems.append("snapshot.json fingerprint drift")
        except ValueError:
            problems.append("snapshot.json unreadable")
    return problems


def write_all(snap, counters, db):
    """Commit one generation coherently: render the four text outputs, record
    their content sha256 in the snapshot (so a hand-edit or a foreign write is
    detectable, not merely a missing stamp), stage every output to a sibling
    temp file, then replace members -- the fingerprint-bearing snapshot.json
    LAST, so a mid-commit failure leaves the published set carrying the PRIOR
    fingerprint (a coherent last-good set or a detectably mixed one), never a
    silent mix. History records the publication only after the committed set
    verifies complete."""
    # C4b (AUDIT-SPEC ckpt10_exec): same-input re-publications produce
    # byte-identical outputs unless each commit carries a unique id - stamp
    # one into every member so a mid-commit failure leaves a detectably
    # mixed set even when the inputs (and fp) never moved.
    snap["commit_id"] = hashlib.sha256(os.urandom(16)).hexdigest()[:16]
    texts = [(SNAP_MD, _snapshot_md(snap)), (CROSS_MD, _crosswalk_md(snap)),
             (MET_MD, _metrics_md(snap)), (PROGRESS, _progress_md(snap))]
    snap["outputs"] = {p.name: hashlib.sha256(t.encode("utf-8")).hexdigest()
                       for p, t in texts}
    # C1: bind the semantic payload (levels/packages/transfers/counters/
    # outputs-map/commit-id) to this committed generation. Recorded last so
    # the hash covers the outputs map as well.
    snap["semantics_sha256"] = _semantics_sha(snap)
    plan = texts + [(SNAP_JSON, json.dumps(snap, indent=1) + "\n")]
    tmps = []
    try:
        for path, text in plan:
            fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp_")
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            tmps.append((tmp, path))
        # stamp-bearing snapshot commits last
        ordered = [t for t in tmps if t[1] != SNAP_JSON] + \
                  [t for t in tmps if t[1] == SNAP_JSON]
        for tmp, path in ordered:
            os.replace(tmp, str(path))
    except BaseException:
        for tmp, _ in tmps:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        raise ProgressError(
            "publication commit failed - the set may be mixed; "
            "snapshot.json still carries the prior generation's fingerprint")
    problems = _verify_outputs(snap)
    if problems:
        raise ProgressError("output set incomplete after commit: "
                            + "; ".join(problems))
    history_append(counters, snap["freshness"]["fingerprint"])
    gen = snap["generated_at_utc"]
    ident = snap["identity"]
    print("wrote PROGRESS.md + _index/progress/{snapshot.json,snapshot.md,"
          "crosswalk.md,metrics.md} @ %s head=%s board=%s fp=%s" %
          (gen, ident["git_head"], ident["board"],
           snap["freshness"]["fingerprint"][:10]))


def write_incomplete(err, db=None):
    """A failed generation: snapshot.json alone reports INCOMPLETE with the
    named cause (missing inputs / mid-build move / commit failure); every other
    output keeps its last-good content and history records nothing."""
    last_fp = None
    try:
        if SNAP_JSON.exists():
            last_fp = json.loads(SNAP_JSON.read_text(
                encoding="utf-8")).get("freshness", {}).get("fingerprint")
    except Exception:
        pass
    _m, _i = input_problems(db or DB)
    snap = {"generated_at_utc": datetime.now(timezone.utc)
            .isoformat(timespec="seconds"),
            "identity": {"git_head": git_head()},
            "freshness": {"state": "INCOMPLETE", "reason": str(err),
                          "fingerprint": last_fp or "none",
                          "checked_at_utc": datetime.now(timezone.utc)
                          .isoformat(timespec="seconds"),
                          "missing": _m, "invalid": _i},
            "engines": {"parser_version": PARSER_VERSION}}
    _atomic_write(SNAP_JSON, json.dumps(snap, indent=1) + "\n")


def _hdr(snap, title):
    return ("<!-- GENERATED by _index/progress/progress_report.py parser v%d - "
            "do not hand-edit -->\n"
            "# %s\n\n**as of (UTC):** %s · **source identity:** git `%s`, board "
            "rev `%s` epoch `%s` · **freshness:** `%s` (fp `%s`)\n\n"
            % (snap["engines"]["parser_version"], title,
               snap["generated_at_utc"], snap["identity"]["git_head"],
               (snap["identity"]["board"] or {}).get("revision"),
               (snap["identity"]["board"] or {}).get("epoch"),
               snap["freshness"]["state"], snap["freshness"]["fingerprint"][:12])
            + ((" · **commit:** `%s`" % snap["commit_id"])
               if snap.get("commit_id") else ""))


def _progress_md(snap):
    l1 = snap["levels"]["L1_modding_grade"]
    l2 = snap["levels"]["L2_reconstruction_grade"]
    q = l1["open_questions"]
    uq = l1["unidentified_open_questions"]
    t = snap["transfers"]
    term = l1["terminal_audit"]
    lines = [_hdr(snap, "PROGRESS - route to L1+L2 (generated)"),
             "Detail lives in [`_index/progress/`](_index/progress/): "
             "[snapshot.md](_index/progress/snapshot.md) (the route), "
             "[crosswalk.md](_index/progress/crosswalk.md) (obligation route), "
             "[metrics.md](_index/progress/metrics.md) (numerators/sources), "
             "[snapshot.json](_index/progress/snapshot.json) (machine), "
             "[history.jsonl](_index/progress/history.jsonl) (deltas).\n"]
    lines.append("| leg | state | source |")
    lines.append("|---|---|---|")
    dis = l1["open_questions_dispositions"]
    lines.append("| L1 open questions | OPEN %d · PARTIAL %d · BLOCKED %d "
                 "(of %d scored; accepted answers %d, approved dispositions "
                 "%d [%d NAS / %d OEB - closed for the gate, unanswered in "
                 "fact], withdrawn %d - withdrawn is not learned) | "
                 "OPEN-QUESTIONS.md |"
                 % (q.get("OPEN", 0), q.get("PARTIAL", 0), q.get("BLOCKED", 0),
                    sum(q.values()), dis["accepted_answers"],
                    dis["no_admissible_source"]
                    + dis["out_of_evidence_boundary"],
                    dis["no_admissible_source"],
                    dis["out_of_evidence_boundary"], q.get("WITHDRAWN", 0)))
    lines.append("| L1 unidentified-OQ residue | OPEN %d · PARTIAL %d | "
                 "UNIDENTIFIED-OPEN-QUESTIONS.md |"
                 % (uq.get("OPEN", 0), uq.get("PARTIAL", 0)))
    lines.append("| L1 system documents | %d docs carrying `system:` over %d "
                 "categories | tree walk (program_coverage rule - proxy) |"
                 % (l1["system_documents"]["total"],
                    len(l1["system_documents"]["per_category"])))
    lines.append("| L2 verdicts | **%d MET of %d systems**; blocking dims: "
                 "types %d, runtime %d · LIVE-unruled cells %d | L2-VERDICTS.md |"
                 % (l2["verdict_column"].get("MET", 0), l2["systems_scored"],
                    l2["systems_scored"] - l2["per_dimension_satisfied"]["types"],
                    l2["systems_scored"] - l2["per_dimension_satisfied"]["runtime"],
                    sum(l2["per_dimension_live_unruled"].values())))
    tr = ("UNMEASURED" if t["obligations"] is None else
          "%d obligations, %d untracked" % (t["obligations"], t["untracked"]))
    lines.append("| transfers (batch-K) | %s | transfer_audit |" % tr)
    pb = snap["page_boxes"]
    if pb.get("no_id") is None:
        pbs = "UNMEASURED"
    else:
        pbs = ("**%d page-local** (no register id%s), **%d closed-row**, "
               "%d live-row unticked" % (
                   pb["no_id"],
                   "" if pb["no_id_untracked"] is None else
                   ", %d on untracked pages" % pb["no_id_untracked"],
                   pb["closed_id"], pb["open_id"]))
    lines.append("| page-box obligations | %s | %s |" % (pbs, pb["engine"]))
    openk = {k: v for k, v in snap["board_counts"].items()
             if k in ("READY", "ACTIVE", "BLOCKED")}
    lines.append("| board packages | %d open (%s) | TEAM.json |"
                 % (len(snap["packages"]), ", ".join(
                     "%s %d" % (k, v) for k, v in sorted(openk.items()))))
    declared = term["final_audits_declared"]
    lines.append("| terminal certification | declared `final_audits` **%s / "
                 "30** (PROGRAM-STATE receipt) · AUDIT-LOG complete runs %d · "
                 "AUDIT-PASS* round artefacts %d (evidence docs, not passes) | "
                 "FINAL-AUDIT-PROTOCOL |"
                 % (declared if declared is not None else "UNMEASURED",
                    term["audit_log_complete_runs"],
                    term["audit_pass_artefacts"]))
    lines.append("| parity | %s | PARITY-STATUS.md |"
                 % snap["levels"]["parity"]["label"])
    d = snap.get("deltas") or {}
    if any(d.get(k) for k in ("vs_prior", "over_24h", "over_7d")):
        lines.append("\n**deltas** (keyed counters): prior `%s` · 24h `%s` · "
                     "7d `%s`\n" % (d.get("vs_prior"), d.get("over_24h"),
                                     d.get("over_7d")))
    lines.append("\n*L3 is out of scope by directive. No blended score is "
                 "computed; every number above names its source. For ETAs: "
                 "none is given - throughput is tracked in history.jsonl and "
                 "no reliable rate is claimed.*\n")
    return "".join(l + "\n" if not l.endswith("\n") else l for l in lines)


def _snapshot_md(snap):
    l2 = snap["levels"]["L2_reconstruction_grade"]
    out = [_hdr(snap, "Progress snapshot - the L1/L2 route")]
    out.append("\n## Level separation\n\n")
    out.append("| requirement | measured | of | note |\n|---|---:|---:|---|\n")
    q = snap["levels"]["L1_modding_grade"]["open_questions"]
    out.append("| L1 - OPEN-QUESTIONS empty | %d open/partial/blocked | %d | "
               "%s |\n" % (q.get("OPEN", 0) + q.get("PARTIAL", 0) +
                           q.get("BLOCKED", 0), sum(q.values()),
                           ", ".join("%s %d" % (k, v) for k, v in
                                     sorted(q.items()))))
    for d in ("contract", "types", "relationships", "runtime", "script_data"):
        c = l2["per_dimension"][d]
        sat = l2["per_dimension_satisfied"][d]
        note = ", ".join("%s %d" % (k, v) for k, v in sorted(c.items()))
        unruled = l2["per_dimension_live_unruled"].get(d, 0)
        if unruled:
            note += " (%d LIVE unruled - not counted)" % unruled
        out.append("| L2 - %s | %d satisfied | %d | %s |\n"
                   % (d, sat, l2["systems_scored"], note))
    out.append("| L2 - verdict column | %d MET | %d | %s |\n"
               % (l2["verdict_column"].get("MET", 0), l2["systems_scored"],
                  ", ".join("%s %d" % (k, v) for k, v in
                            sorted(l2["verdict_column"].items()))))
    out.append("\n## Residual required knowledge (L1/L2)\n\n")
    res = snap["levels"]["residual_required_knowledge"]
    out.append("- OPEN: %s\n" % ", ".join(res["oq_open_ids"]))
    out.append("- PARTIAL: %s\n" % ", ".join(res["oq_partial_ids"]))
    out.append("- BLOCKED: %s\n\n" % ", ".join(res["oq_blocked_ids"]))
    pb = snap["page_boxes"]
    out.append("## Page-box obligations (uncounted by the register)\n\n")
    if pb.get("no_id") is None:
        out.append("UNMEASURED - %s\n\n" % pb["engine"])
    else:
        out.append("| class | count |\n|---|---:|\n")
        out.append("| unticked boxes naming no register id "
                   "(page-local residue) | **%d** |\n" % pb["no_id"])
        if pb["no_id_untracked"] is not None:
            out.append("| - of which on untracked (uncommitted) pages | %d |\n"
                       % pb["no_id_untracked"])
        out.append("| unticked boxes of closed register rows "
                   "(mis-marked residue) | **%d** |\n" % pb["closed_id"])
        out.append("| unticked boxes of live rows (honest pending) | %d |\n"
                   % pb["open_id"])
        out.append("\n*instrument: %s - the register counts rows; this is "
                   "the surface it cannot see.*\n\n" % pb["engine"])
    out.append("## Per-system L2 cells\n\n| system | contract | types | rel | "
               "runtime | script/data | L2 | gap |\n|---|---|---|---|---|---|---|---|\n")
    for v in l2["systems"]:
        out.append("| %s %s | %s | %s | %s | %s | %s | %s | %s |\n"
                   % (v["system"], v["name"][:40], v["contract"], v["types"],
                      v["relationships"], v["runtime"], v["script_data"],
                      v["l2"], v["gap"][:80].replace("|", "\\|")))
    return "".join(out)


def _crosswalk_md(snap):
    """The deduplicated obligation route: page (open questions), register
    (untracked batch-K transfers), coverage (unsatisfied L2 cells), and board
    packages/carriers -- one row per obligation carrying owner / reviewer /
    dependency / evidence / missing discriminator / next action / acceptance."""
    out = [_hdr(snap, "Obligation route - deduplicated finishable work")]
    out.append("\n*Ordered by unfinished-dependency count, then priority, "
               "then ACTIVE-before-READY. Every row carries owner, reviewer, "
               "dependency, evidence, a missing discriminator, a next action "
               "and an acceptance; fields the source cannot produce are "
               "UNMEASURED, never blank.*\n\n")
    out.append("| order | id | kind | status | pri | owner | reviewer | "
               "dependency | evidence | missing | next action / acceptance |\n"
               "|---:|---|---|---|---|---|---|---|---|---|\n")
    for i, p in enumerate(snap["packages"], 1):
        dep = ",".join(p["blocked_by"]) or "-"
        missing = "none"
        if p["owner"] in (None, "", "UNASSIGNED"):
            missing = "owner"
        elif not p["evidence"]:
            missing = "evidence"
        out.append("| %d | `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n"
                   % (i, p["id"], p["kind"], p["status"], p["priority"],
                      p["owner"], p["reviewer"], dep,
                      (p["evidence"] or "MISSING").replace("|", "\\|"),
                      missing,
                      (p["acceptance"] or p["target"]).replace("|", "\\|")))
    out.append("\n## Transferred obligations (never complete, never vanish)\n\n")
    t = snap["transfers"]
    if t["obligations"] is None:
        out.append("UNMEASURED - transfer_audit unavailable: %s\n" % t["engine"])
    else:
        out.append("%d batch-K obligations checked, %d untracked.\n"
                   % (t["obligations"], t["untracked"]))
        out.append("| register obligation | owner | reviewer | evidence | "
                   "next action | acceptance |\n|---|---|---|---|---|---|\n")
        for p in t["problems"]:
            rid = str(p).split(":")[0]
            out.append("| %s | UNMEASURED | UNKNOWN | %s | resolve the "
                       "audited transfer | a DONE task or accepted receipt "
                       "closes it |\n"
                       % (rid.replace("|", "\\|"),
                          str(p)[:160].replace("|", "\\|")))
    out.append("\n## Coverage obligations (unsatisfied L2 cells)\n\n")
    l2 = snap["levels"]["L2_reconstruction_grade"]
    out.append("| system | cell | verdict | evidence | next action | "
               "acceptance |\n|---|---|---|---|---|---|\n")
    for v in l2["systems"]:
        for d in ("contract", "types", "relationships", "runtime",
                  "script_data"):
            code = v[d]
            if code in ("MET", "N/A") or dim_satisfied(v, d):
                continue
            ev = v.get("cell_text", {}).get(d, "")[:120] or "MISSING"
            tag = "LIVE (unruled - not satisfied)" if code == "LIVE" else code
            out.append("| %s | %s | %s | %s | satisfy the cell under its "
                       "criterion | cell reaches MET or ruling-cited LIVE |\n"
                       % (v["system"], d, tag, ev.replace("|", "\\|")))
    res = snap["levels"]["residual_required_knowledge"]
    out.append("\n## Page obligations (open questions)\n\n")
    out.append("| id | status | owner doc | evidence / question | next "
               "action |\n|---|---|---|---|---|\n")
    for r in res["oq_open_rows"]:
        out.append("| %s | %s | %s | %s | answer or withdraw the row |\n"
                   % (r["id"], r["status"], r["owner"].replace("|", "\\|"),
                      r["question"].replace("|", "\\|")))
    out.append("\n## Superseded rows - residue moved to a carrier "
               "(closed for the gate, residue still required elsewhere)\n\n")
    sr = res.get("superseded_residue_rows", [])
    if not sr:
        out.append("None at this fingerprint.\n")
    else:
        out.append("| id | owner doc | status text (names the carrier / "
                   "ruling) |\n|---|---|---|\n")
        for r in sr:
            out.append("| %s | %s | %s |\n"
                       % (r["id"], r["owner"].replace("|", "\\|"),
                          r["status_text"].replace("|", "\\|")))
    out.append("\n## Route links - dated transition record\n\n")
    rl = snap.get("route_links", {})
    if rl.get("state") != "CURRENT":
        out.append("UNMEASURED - `%s` not present at this fingerprint. "
                   "Transitions are a dated record, not current state.\n"
                   % rl.get("source", "route-links record"))
    else:
        out.append("`%s` - %d transitions (%s)%s. A dated list, not current "
                   "state; register rows above carry the live status.\n\n"
                   % (rl["source"], rl["transitions"],
                      ", ".join("%s %d" % (k, v) for k, v in
                                sorted(rl["to_counts"].items())),
                      " - %d parse-hazard rows dropped" % rl["dropped"]
                      if rl.get("dropped") else ""))
        if rl.get("moved"):
            out.append("| row | commit | from | to | record |\n"
                       "|---|---|---|---|---|\n")
            for m in rl["moved"]:
                out.append("| %s | `%s` | %s | %s | `%s` |\n"
                           % (m["row"], m["commit"], m["from"], m["to"],
                              m["record"]))
    return "".join(out)


def _metrics_md(snap):
    out = [_hdr(snap, "Metrics - numerator/denominator/formula/source")]
    eng = snap["engines"]
    out.append("\nformula/parser version `%d`; classifier `%s`; transfers `%s`; "
               "page-boxes `%s`\n\n"
               % (eng["parser_version"], eng["oq_classifier"], eng["transfers"],
                  eng.get("page_boxes", "n/a")))
    out.append("| metric | numerator | denominator | formula | source |\n"
               "|---|---:|---:|---|---|\n")
    q = snap["levels"]["L1_modding_grade"]["open_questions"]
    tot = sum(q.values())
    dis = snap["levels"]["L1_modding_grade"]["open_questions_dispositions"]
    rows = [
        ("open questions", q.get("OPEN", 0), tot, "classify(status)==OPEN",
         "OPEN-QUESTIONS.md"),
        ("partial questions", q.get("PARTIAL", 0), tot, "classify(status)==PARTIAL",
         "OPEN-QUESTIONS.md"),
        ("blocked questions", q.get("BLOCKED", 0), tot, "classify(status)==BLOCKED",
         "OPEN-QUESTIONS.md"),
        ("accepted answers (learned)",
         dis["accepted_answers"], tot,
         "classify==ANSWERED and lead not in (NAS, OEB)", "OPEN-QUESTIONS.md"),
        ("approved dispositions - NO ADMISSIBLE SOURCE",
         dis["no_admissible_source"], tot,
         "lead==NO ADMISSIBLE SOURCE; closed for the gate, unanswered in fact",
         "OPEN-QUESTIONS.md"),
        ("approved dispositions - OUT OF EVIDENCE BOUNDARY",
         dis["out_of_evidence_boundary"], tot,
         "lead==OUT OF EVIDENCE BOUNDARY (class-3 terminal); not a synonym of "
         "NAS", "OPEN-QUESTIONS.md"),
        ("withdrawn (never counted as learned)", q.get("WITHDRAWN", 0), tot,
         "classify(status)==WITHDRAWN", "OPEN-QUESTIONS.md"),
        ("  withdrawn - SUPERSEDED (residue moved to a carrier)",
         dis["withdrawn_by_lead"].get("SUPERSEDED", 0), tot,
         "lead==SUPERSEDED", "OPEN-QUESTIONS.md + UNIDENTIFIED"),
        ("  withdrawn - NOT A QUESTION / NOT A DEFECT",
         dis["withdrawn_by_lead"].get("NOT A QUESTION", 0)
         + dis["withdrawn_by_lead"].get("NOT A DEFECT", 0), tot,
         "lead in (NOT A QUESTION, NOT A DEFECT)", "registers"),
        ("  withdrawn - DISSOLVED (false premise)",
         dis["withdrawn_by_lead"].get("DISSOLVED", 0), tot,
         "lead==DISSOLVED", "registers"),
        ("  withdrawn - other (WITHDRAWN/duplicate)",
         dis["withdrawn_by_lead"].get("WITHDRAWN", 0)
         + dis["withdrawn_by_lead"].get("OTHER/DUPLICATE", 0), tot,
         "remaining leads", "registers"),
    ]
    l2 = snap["levels"]["L2_reconstruction_grade"]
    for d in ("contract", "types", "relationships", "runtime", "script_data"):
        sat = l2["per_dimension_satisfied"][d]
        rows.append(("L2 %s cells satisfied" % d, sat, l2["systems_scored"],
                     "MET plus LIVE only where the cell cites its governing "
                     "ruling", "L2-VERDICTS.md"))
    rows.append(("L2 cells LIVE but unruled",
                 sum(l2["per_dimension_live_unruled"].values()),
                 l2["systems_scored"] * 5,
                 "LIVE without a ruling citation - not satisfied",
                 "L2-VERDICTS.md"))
    t = snap["transfers"]
    rows.append(("transfer obligations tracked",
                 (t["obligations"] - t["untracked"]) if t["obligations"] is not None else "UNMEASURED",
                 t["obligations"] if t["obligations"] is not None else "UNMEASURED",
                 "transfer_audit (problems, checked)", "batch-K-scope-rulings.md"))
    c = snap["levels"]["residual_required_knowledge"]["contradictions"]
    rows.append(("contradiction-ledger dispositions", c["rows"], c["rows"],
                 "all ledger kinds are resolved dispositions", "CONTRADICTIONS.tsv"))
    pb = snap["page_boxes"]
    if pb.get("no_id") is None:
        rows.append(("page-box obligations (no register id)", "UNMEASURED",
                     "UNMEASURED", "instrument absent", pb["engine"]))
    else:
        rows.append(("page-box obligations (no register id)", pb["no_id"],
                     pb["no_id"],
                     "unticked - [ ] boxes naming no question id; "
                     "page-local residue", "check_questions.read_boxes"))
        rows.append(("  of which on untracked pages",
                     pb["no_id_untracked"]
                     if pb["no_id_untracked"] is not None else "UNMEASURED",
                     pb["no_id"], "git ls-files split", "index"))
        rows.append(("unticked boxes of closed rows (mis-marked)",
                     pb["closed_id"], pb["closed_id"] + pb["open_id"],
                     "unticked and every named id is ANSWERED/WITHDRAWN",
                     "read_boxes + register"))
    rows.append(("board packages open", len(snap["packages"]), snap["board_total"],
                 "status in READY/ACTIVE/BLOCKED", "TEAM.json"))
    rows.append(("new debt (READY tasks)",
                 snap["board_counts"].get("READY", 0), snap["board_total"],
                 "status==READY", "TEAM.json"))
    term = snap["levels"]["L1_modding_grade"]["terminal_audit"]
    rows.append(("final_audits (receipted counter)",
                 term["final_audits_declared"]
                 if term["final_audits_declared"] is not None else "UNMEASURED",
                 30, "declared `final_audits N / 30` in PROGRAM-STATE plus "
                 "AUDIT-LOG complete-run entries", "PROGRAM-STATE.md"))
    rows.append(("AUDIT-PASS* round artefacts (not terminal passes)",
                 term["audit_pass_artefacts"], "-",
                 "filename count - per-round evidence documents only",
                 "_index/AUDIT-PASS*"))
    rows.append(("parity certified",
                 snap["levels"]["parity"]["certified"]
                 if snap["levels"]["parity"]["certified"] is not None
                 else "UNMEASURED",
                 snap["levels"]["parity"]["of"]
                 if snap["levels"]["parity"]["of"] is not None else "UNMEASURED",
                 "'N of M pilots certified' line", "PARITY-STATUS.md"))
    for name, n, d_, f, src in rows:
        out.append("| %s | %s | %s | `%s` | `%s` |\n" % (name, n, d_, f, src))
    out.append("\nNo blended percentage is produced. UNMEASURED marks an "
               "unavailable denominator. No ETA is claimed.\n")
    return "".join(out)


# -------------------------------------------------------------------- modes
def check(db):
    """Assert the published output set is current AND coherent: snapshot exists
    and is not INCOMPLETE, its fingerprint equals the live capture, and every
    output member exists, is non-empty and carries that fingerprint. Exit
    0 CURRENT / 1 STALE / 2 MISSING-or-INCOMPLETE."""
    if not SNAP_JSON.exists():
        print("MISSING: no snapshot")
        return 2
    try:
        snap = json.loads(SNAP_JSON.read_text(encoding="utf-8"))
    except ValueError as e:
        print("INCOMPLETE: snapshot.json unreadable: %s" % e)
        return 2
    fr = snap.get("freshness", {})
    if fr.get("state") == "INCOMPLETE":
        print("INCOMPLETE: last generation failed: %s" % fr.get("reason"))
        return 2
    missing, invalid = input_problems(db)
    if missing or invalid:
        print("INCOMPLETE: " + "; ".join(
            (["required input(s) missing: " + ", ".join(missing)]
             if missing else []) +
            (["required input(s) invalid: " + ", ".join(invalid)]
             if invalid else [])))
        return 2
    cur = fingerprint(db)
    if fr.get("fingerprint") != cur:
        print("STALE: generated %s, fp %s vs current %s"
              % (snap.get("generated_at_utc"),
                 str(fr.get("fingerprint"))[:12], cur[:12]))
        return 1
    problems = _verify_outputs(snap)
    if problems:
        print("INCOMPLETE: output set not coherent - " + "; ".join(problems))
        return 2
    print("CURRENT: generated %s, fp %s, all %d outputs coherent"
          % (snap["generated_at_utc"], cur[:12], len(_output_paths(db))))
    return 0


def auto(db):
    """The scheduled entry point: skip only when the fingerprint is unchanged
    AND the published set is coherent AND no .dirty mark is present. A forced
    or moved generation publishes atomically; a failure keeps the last-good
    set and exits nonzero (the watchdog consumes .dirty only on success)."""
    dirty = DIRTY.exists()
    if SNAP_JSON.exists() and not dirty:
        try:
            snap = json.loads(SNAP_JSON.read_text(encoding="utf-8"))
        except ValueError:
            snap = None
        if snap and snap.get("freshness", {}).get("state") != "INCOMPLETE" \
                and snap["freshness"]["fingerprint"] == fingerprint(db) \
                and not _verify_outputs(snap):
            snap["freshness"]["checked_at_utc"] = \
                datetime.now(timezone.utc).isoformat(timespec="seconds")
            _atomic_write(SNAP_JSON, json.dumps(snap, indent=1) + "\n")
            print("UNCHANGED (fp %s); checked_at stamped"
                  % snap["freshness"]["fingerprint"][:12])
            return 0
    try:
        snap, counters = build(db)
        write_all(snap, counters, db)
    except ProgressError as e:
        write_incomplete(e, db)
        print(str(e))
        return 1
    except Exception as e:
        write_incomplete(e, db)
        print("generation failed: %s" % e)
        return 1
    # A successful generation/publication discharges the dirty mark - whoever
    # runs it. (The watchdog does the same for its own invocation.)
    if dirty:
        try:
            DIRTY.unlink()
        except OSError:
            pass
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["generate", "auto", "check", "status"])
    ap.add_argument("--db", default=str(DB))
    a = ap.parse_args()
    db = Path(a.db)
    if a.mode == "check":
        sys.exit(check(db))
    if a.mode == "status":
        if not SNAP_JSON.exists():
            print("no snapshot"); return
        snap = json.loads(SNAP_JSON.read_text(encoding="utf-8"))
        if snap.get("freshness", {}).get("state") == "INCOMPLETE":
            print("INCOMPLETE: %s" % snap["freshness"].get("reason")); return
        q = snap["levels"]["L1_modding_grade"]["open_questions"]
        l2 = snap["levels"]["L2_reconstruction_grade"]
        print("as-of %s | OQ open %d partial %d | L2 MET %d/%d | tasks open %d | fp %s"
              % (snap["generated_at_utc"], q.get("OPEN", 0), q.get("PARTIAL", 0),
                 l2["verdict_column"].get("MET", 0), l2["systems_scored"],
                 len(snap["packages"]), snap["freshness"]["fingerprint"][:12]))
        return
    if a.mode == "auto":
        sys.exit(auto(db))
    # generate
    try:
        snap, counters = build(db)
        write_all(snap, counters, db)
    except ProgressError as e:
        write_incomplete(e, db)
        print(str(e))
        sys.exit(1)
    except Exception as e:
        write_incomplete(e, db)
        print("generation failed: %s" % e)
        sys.exit(1)
    try:
        DIRTY.unlink()
    except OSError:
        pass


if __name__ == "__main__":
    main()
