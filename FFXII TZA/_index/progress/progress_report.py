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
the last good set UNTOUCHED - snapshot.json included - and records the
failure in the store's LAST-FAILURE.json, which `check` reports):
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
             coherently, every stamped member agrees, and live bytes equal
             the CURRENT generation's manifest (CURRENT/STALE/INCOMPLETE/
             MISSING, exit 0/1/2)
  status     print the one-line state
  export <z> export exactly the CURRENT pinned generation to a verified ZIP
  verify-zip <z> label a ZIP VERIFIED/UNVERIFIED (a hand-made or
             generation-mixed ZIP is never CURRENT)

Checkpoint-10 R3 repair contract (asserted by test_progress_report.py):
  * consumed sources are fingerprinted over their COMPLETE bytes - a page
    reader consumes whole bodies, so a checkbox past the frontmatter window
    still moves the fingerprint;
  * input validation splits MISSING / EMPTY / INVALID - a legitimately
    empty required file is reported as empty, never conflated with
    malformed nonempty text;
  * page-only obligations are rows, not just counts: file + line anchor,
    stable locator, requirement text, owner, reviewer, discriminator and
    the deduplication links to any register ids the box names;
  * publications run through gfz-scripts/generation.py - one .partial
    generation is committed atomically into the store CURRENT pointer and
    the live outputs become a verified copy of it, so the whole last
    COMPLETE generation survives any failure; the source preimage is
    rechecked at the final cutover;
  * export is exactly one generation: `export <zip>` pins CURRENT,
    verifies every member against its manifest, and `verify-zip` labels a
    hand-made or generation-mixed ZIP UNVERIFIED, never CURRENT;

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
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent          # _index/progress/
DB = HERE.parents[1]                            # Database/FFXII TZA/
ROOT = DB.parents[1]                            # repo root
PARSER_VERSION = 7                              # bump on any parse-rule change

# The coherent-generation store (OPUS's generation.py, adopted under
# OPUS-REQ-DATA-ADOPT-GENERATION-LIB): each publication is one generation -
# declared input snapshots + outputs + MANIFEST.json - and the live files are
# a verified copy of CURRENT. The store lives in the ignored work tree; its
# generations carry full input snapshots and are self-verifying on export.
WORK = ROOT / "Database" / "Tools" / "work"
STORE_ROOT = WORK / "progress-generations"
# The last failed attempt, kept OUT of the live output set (2026-10-03, SWE2-DATA): until then a failure
# replaced snapshot.json with a 447-byte INCOMPLETE stub, which broke the coherent last-good set write_all
# promises and every reader of `levels` (the dashboard's My Progress read PARTIAL). Resolved at call time
# from STORE_ROOT so a fixture's rebound store gets its own file.
LAST_FAILURE_NAME = "LAST-FAILURE.json"
# The consumed document tree's preimage (relpath + full sha256 per doc),
# written just before a build begins and declared as a generation input so a
# committed generation/export carries exactly what the docs hashed to.
DOCSIG = WORK / "progress-doc-signature.txt"
GEN = None
try:
    sys.path.insert(0, str(ROOT / "Database" / "Tools" / "analysis-kit"
                             / "gfz-scripts"))
    import generation as GEN  # noqa: E401
except Exception:
    GEN = None

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
    """A generation cannot be honestly produced; the named cause is recorded
    in LAST-FAILURE.json and the last-good set - snapshot.json included - is
    kept untouched."""


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
        lead = _lead_keyword(cells)
        # v5 (OPUS-NOTICE-DATA-REPORTER-UNKNOWN-ROW, SWE2-DATA 2026-09-30): a row whose ID cell
        # is struck (`~~CH-2~~`) is withdrawn by the strike. check_questions' QID pattern does
        # not match a struck id, so it never scores these rows; this reporter does, and one of
        # them (CH-2, "STRUCK 2026-09-07 - FILED IN ERROR") has a lead the vocabulary does not
        # know, which made it the dashboard's single UNKNOWN. Only an unreadable struck row is
        # reclassified - a struck row with a known lead keeps its class.
        if verdict == "UNKNOWN" and m.group(1) and m.group(3):
            verdict, lead = "WITHDRAWN", "STRUCK"
        owner = cells[1] if len(cells) > 2 else ""
        q = re.sub(r"\s+", " ", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1",
                                       cells[0]))[:110]
        status_text = re.sub(
            r"\s+", " ", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1",
                                cells[-1]))[:160] if cells else ""
        out.append({"id": rid, "status": verdict, "lead": lead,
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


_CHORE_ID = re.compile(r"-(PUB|PUBLISH|CHECKPOINT)-")


def _is_chore(t):
    """A board task that is a coordination step, not a knowledge obligation
    (FABLE CROSSWALK-MEANINGS R6, DASHBOARD-MEANINGS §2 'board tasks are not
    packages'): publication leases (`@publication` resource or `-PUB-` id) and
    checkpoint chores. They are still reported - under the chores section,
    never inside the deduplicated route."""
    if any(isinstance(r, dict) and r.get("key") == "@publication"
           for r in t.get("resources", [])):
        return True
    return bool(_CHORE_ID.search(str(t.get("id", ""))))


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
        disc = "chore:coordination" if _is_chore(t) else \
               "external/runtime" if t.get("kind") == "runtime" else \
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
    # R5 (CROSSWALK-MEANINGS): a work item's reviewer is the ASSIGNEE of the
    # review request that names it - join each package id to the review tasks
    # whose target / dependencies / reviews record name it. The requester is
    # still never a reviewer; the named review assignment is.
    reviewer_for = {}
    for rt in tasks:
        rv_agent = rt.get("assigned_to") or rt.get("agent")
        if not rv_agent:
            continue
        if not isinstance(rt.get("reviews"), dict) \
                and "-REVIEW-" not in str(rt.get("id", "")):
            continue
        hay = json.dumps([rt.get("target"), rt.get("dependencies"),
                          rt.get("question"), rt.get("reviews")])
        for p in pk:
            if p["id"] and p["id"] in hay:
                reviewer_for.setdefault(p["id"], rv_agent)
    for p in pk:
        if p["reviewer"] == "UNKNOWN":
            p["reviewer"] = reviewer_for.get(p["id"], "UNKNOWN")
    return {"identity": {"revision": b.get("revision"),
                         "epoch": b.get("recovery_epoch"),
                         "phase": b.get("phase")},
            "open": pk, "counts": dict(counts),
            "total": len(tasks), "tasks": tasks}


def _transfer_rows(db):
    """One route row per batch-K transferred obligation (CROSSWALK-MEANINGS
    R1 - 'N obligations checked' is a check result, not the debt). The ruling
    record itself is the source: class-1 rows went to a named measuring
    instrument (destination owner = that page's declared owner); class-2 rows
    went to a named carrier task (destination owner = the task's board
    owner)."""
    p = (db / "_index" / "candidates" / "register-triage"
         / "batch-K-scope-rulings.md")
    rows = []
    if not p.exists():
        return rows
    carrier_owner = {}
    try:
        b = json.loads((db / "_index/_inbox/TEAM.json")
                       .read_text(encoding="utf-8"))
        for t in b.get("tasks", []):
            carrier_owner[t.get("id")] = (
                t.get("assigned_to") or t.get("agent") or "UNASSIGNED")
    except Exception:
        pass
    cls = None
    seen = set()
    text = p.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        m = re.match(r"^##\s+Class\s+(\d)", line)
        if m:
            cls = int(m.group(1))
            continue
        if not line.startswith("|") or cls not in (1, 2):
            continue
        cells = [c.strip() for c in CELL.split(line) if c.strip()]
        if not cells or cells[0] == "row" or re.match(r"^[-\s]+$", cells[0]):
            continue
        rid = cells[0]
        if not re.match(r"^[A-Z]+-\d+", rid) or rid in seen:
            continue
        seen.add(rid)
        if cls == 1:
            dest = cells[-1].strip("`")
            pm = re.search(r"([\w./-]+\.(?:md|tsv|csv|py))", dest)
            owner = _page_owner(db, pm.group(1)) if pm else "UNKNOWN"
            action = "population now measured by the named instrument"
        else:
            dest = (cells[1] if len(cells) > 1 else "").strip("`")
            owner = carrier_owner.get(dest, "UNKNOWN")
            action = "residue carried by the named board task"
        rows.append({"id": rid, "locator": "register:%s" % rid,
                     "transfer_class": cls, "destination": dest[:140],
                     "destination_owner": owner, "next_action": action})
    # Extension rulings below the two canonical tables transfer more rows as
    # `- **ID** - <ruling text>` bullets. Each such bullet whose text names a
    # class-1 closure, a SUPERSEDED-onto destination, or a residue route is a
    # transferred obligation too (R1: every transferred row listed).
    bullets = re.split(r"(?m)^-\s+(?=\*\*[A-Z]+-\d)", text)
    for blk in bullets:
        m = re.match(r"\*\*([A-Z]+-\d+[a-z]?)\*\*\s*[-\u2014]?\s*(.*)",
                     blk.lstrip("- "), re.S)
        if not m:
            continue
        rid, btext = m.group(1), m.group(2)
        if rid in seen or not re.search(
                r"(?i)class.1|superseded onto|residue routes|routed to|"
                r"carrier", btext):
            continue
        seen.add(rid)
        pm = re.search(r"`([^`\n]+\.(?:md|tsv|csv|py))`", btext)
        tm = re.search(r"`([A-Z][A-Z0-9]*(?:-[A-Z0-9]+){2,})`", btext)
        if pm:
            dest, owner = pm.group(1), _page_owner(db, pm.group(1))
        elif tm:
            dest = tm.group(1)
            owner = carrier_owner.get(dest, "UNKNOWN")
        else:
            dest, owner = "see ruling record", "UNKNOWN"
        c1 = bool(re.search(r"(?i)class.1", btext))
        rows.append({"id": rid, "locator": "register:%s" % rid,
                     "transfer_class": 1 if c1 else "ext",
                     "destination": dest[:140],
                     "destination_owner": owner,
                     "next_action": "routed per the extension ruling - the "
                                    "named carrier keeps the residue"})
    return rows


def parse_transfers(db):
    """transfer_audit obligations: (problems, checked) via the instrument,
    plus one listed row per transferred obligation (R1)."""
    try:
        sys.path.insert(0, str(ROOT / "Database" / "Tools" / "analysis-kit"
                                 / "gfz-scripts"))
        import transfer_audit
        problems, checked = transfer_audit.audit(str(db),
                                                 str(db / "_index/_inbox/TEAM.json"))
        return {"engine": "transfer_audit.audit", "obligations": len(checked),
                "untracked": len(problems), "problems": problems[:20],
                "checked_ids": list(checked), "rows": _transfer_rows(db)}
    except Exception as e:
        return {"engine": "UNMEASURED (%s)" % type(e).__name__,
                "obligations": None, "untracked": None, "problems": [],
                "checked_ids": [], "rows": []}


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
    reader must not read as zero obligations.

    CKPT10R3: every unticked box is also published as an OBLIGATION ROW in
    `obligations` carrying file + line anchor, a stable locator, the
    requirement text, the page's declared owner (UNKNOWN when the page
    declares none), reviewer UNKNOWN, a discriminator and the explicit
    dedup links to whatever register ids the box names - a box with no
    register id or a file the index cannot see never waives the work; the
    class column keeps page-local / mis-marked-closed / live-row residue
    populations distinct."""
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
           "closed_id": 0, "open_id": 0, "obligations": []}
    owners = {}
    for rel, line, ticked, ids, text in boxes:
        if ticked:
            continue
        if not ids:
            out["no_id"] += 1
            cls = "page-local"
            if tracked is not None and rel not in tracked:
                out["no_id_untracked"] += 1
                cls = "page-local-untracked"
        elif any(reg.get(i, "OPEN") not in closed for i in ids):
            out["open_id"] += 1
            cls = "live-row-residue"
        else:
            out["closed_id"] += 1
            cls = "mis-marked-closed"
        if rel not in owners:
            owners[rel] = _page_owner(db, rel)
        out["obligations"].append({
            "file": rel,
            "anchor": "%s#L%d" % (rel, line),
            "locator": "register:" + ",".join(ids) if ids
                       else "page:%s#L%d" % (rel, line),
            "requirement": re.sub(r"\s+", " ", str(text or ""))[:140]
                           or "MISSING",
            "owner": owners[rel],
            "reviewer": "UNKNOWN",
            "class": cls,
            "named_ids": list(ids),
            "dedup": ["register:%s" % i for i in ids] or ["none"],
            "discriminator":
                "untracked page - the index cannot see it"
                if cls == "page-local-untracked"
                else "no register row - page-local" if cls == "page-local"
                else "names %s (%s)" % (",".join(ids), cls)})
    return out


def _page_owner(db, rel):
    """The owning page's declared owner from frontmatter (`owner_layer:` or
    `owner:`), else UNKNOWN - ownership is never guessed."""
    try:
        head = open(db / rel, encoding="utf-8", errors="replace").read(3000)
    except OSError:
        return "UNKNOWN"
    m = re.search(r"^(?:owner_layer|owner)\s*:\s*(.+)$", head, re.M)
    if not m:
        return "UNKNOWN"
    return m.group(1).strip().strip("`") or "UNKNOWN"


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


_PKG_STAGES = ["research", "evidence-ready", "review", "repair",
               "incorporation", "accepted-and-incorporated", "dispositioned"]


def completion_packages(db):
    """Completion packages by stage (DASHBOARD-MEANINGS §2: board tasks are
    not packages - packages carry the stage vocabulary of
    _index/completion-packages/README.md). Each PKG-*.md declares its stage
    on the `**stage.**` line (the earliest non-adjacent item stage). Absent
    directory or field -> UNMEASURED, never zero."""
    d = db / "_index" / "completion-packages"
    rec = {"engine": "pkg stage scan", "packages": [], "by_stage": {},
           "state": "UNMEASURED"}
    if not d.is_dir():
        rec["engine"] = "UNMEASURED (no _index/completion-packages)"
        return rec
    for f in sorted(d.glob("PKG-*.md")):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        m = re.search(r"\*\*stage\.\*\*\s*`?([A-Za-z][\w-]*)", text)
        stage = m.group(1) if m else "UNMEASURED"
        if stage not in _PKG_STAGES:
            stage = "UNMEASURED"
        rec["packages"].append({"id": f.stem, "stage": stage})
        rec["by_stage"][stage] = rec["by_stage"].get(stage, 0) + 1
    rec["state"] = "CURRENT"
    return rec


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


def _doc_preimage(db):
    """Full preimage of the consumed document surface: one
    'relpath<TAB>sha256<TAB>size' line per .md under the database root
    (excluding _* dirs), INCLUDING root-level documents such as the
    AUDIT-PASS* artefacts terminal_audit() consumes. Hashes cover COMPLETE
    file bytes - the page readers (read_boxes, doc counts) consume whole
    bodies, so an edit deep in a document, e.g. an unticked box past byte
    4000, must invalidate the fingerprint (CKPT10R3: the frontmatter window
    alone was not the consumed surface). PROGRESS.md is a generated OUTPUT -
    hashing it would make the fingerprint self-referential."""
    lines = []
    for dp, dns, fns in os.walk(db):
        rel = os.path.relpath(dp, db).replace(os.sep, "/")
        top = rel.split("/")[0]
        if top.startswith("_"):
            continue
        for fn in sorted(fns):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            if os.path.abspath(p) == os.path.abspath(str(PROGRESS)):
                continue
            r = os.path.relpath(p, db).replace(os.sep, "/")
            try:
                raw = open(p, "rb").read()
                lines.append("%s\t%s\t%d" % (
                    r, hashlib.sha256(raw).hexdigest(), len(raw)))
            except OSError:
                lines.append("%s\tUNREADABLE\t-1" % r)
    lines.sort()
    return lines


def _doc_signature(db):
    """Signature over the consumed document tree's full preimage. write_all()
    commits the same preimage into the generation store, so a committed
    generation/export carries exactly what every consumed document hashed
    to."""
    h = hashlib.sha256()
    for ln in _doc_preimage(db):
        h.update(ln.encode("utf-8"))
        h.update(b"\n")
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
    for name in ("check_questions.py", "transfer_audit.py", "generation.py"):
        h.update(name.encode())
        h.update((_sha(ROOT / "Database" / "Tools" / "analysis-kit"
                       / "gfz-scripts" / name) or "MISSING").encode())
    # completion-packages are consumed content (stage counts land in
    # PROGRESS.md); they live under _index so the doc preimage skips them.
    pd = db / "_index" / "completion-packages"
    if pd.is_dir():
        for f in sorted(pd.glob("PKG-*.md")):
            h.update(f.name.encode())
            h.update((_sha(f) or "MISSING").encode())
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


def input_states(db):
    """Per-declared-input structural state (CKPT10R3): ``missing`` is absent;
    ``empty`` is a zero-byte file - reported as a DISTINCT state from
    ``invalid`` (nonempty but unreadable/unparseable text) so the report can
    never conflate "legitimately empty" with "malformed". ``present`` parses
    for the input's class - a *cleared* register still parses (a .tsv keeps
    its header, TEAM.json keeps "tasks"), so the test is structural, never
    "has rows". Optional inputs get states too; only required states block."""
    states = {}
    for rel in INPUTS:
        p = db / rel
        if not p.exists():
            states[rel] = {"state": "missing"}
            continue
        try:
            if p.stat().st_size == 0:
                states[rel] = {"state": "empty"}
                continue
            if rel.endswith(".json"):
                j = json.loads(p.read_text(encoding="utf-8"))
                if rel.endswith("TEAM.json") and \
                        not isinstance(j.get("tasks"), list):
                    states[rel] = {"state": "invalid",
                                   "reason": "no 'tasks' list"}
                else:
                    states[rel] = {"state": "present"}
            else:
                text = p.read_text(encoding="utf-8", errors="replace")
                if not text.strip():
                    states[rel] = {"state": "invalid",
                                   "reason": "whitespace only"}
                elif rel.endswith(".tsv") \
                        and "\t" not in text and "|" not in text:
                    # a .tsv with no delimiter on any line is truncated or
                    # misnamed - a cleared register still keeps its header
                    states[rel] = {"state": "invalid",
                                   "reason": "no delimiter structure"}
                else:
                    states[rel] = {"state": "present"}
        except (OSError, ValueError):
            states[rel] = {"state": "invalid",
                           "reason": "unreadable or unparseable"}
    return states


def input_problems(db):
    """(missing, invalid) required inputs. A present-but-empty or unparseable
    required input is INVALID: "missing or invalid required evidence cannot
    become zero CURRENT work" (CKPT10R2 C3) - an empty file is never a
    schema-valid register, but it is reported as the EMPTY state, distinct
    from malformed nonempty text (CKPT10R3; input_states keeps the split)."""
    missing, invalid = [], []
    for rel, st in input_states(db).items():
        if rel not in REQUIRED_INPUTS:
            continue
        if st["state"] == "missing":
            missing.append(rel)
        elif st["state"] == "empty":
            invalid.append("%s (empty file)" % rel)
        elif st["state"] == "invalid":
            invalid.append("%s (%s)" % (rel, st["reason"]))
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
    pkgs = completion_packages(db)
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
        "completion_packages": pkgs,
        # DASHBOARD-MEANINGS §1: every emitted measure declares its axis, so a
        # consumer can never merge axes into one blended state. A measure the
        # adapter cannot decide emits UNMEASURED, never a zero.
        "meanings": {
            "vocabulary": "DASHBOARD-MEANINGS s1 axes + s2 outcomes",
            "populations": {
                "oq_register": "s2 obligation outcomes - separate counts, "
                               "never summed",
                "unidentified_oq": "s2 obligation outcomes - separate "
                                   "register, never merged",
                "page_boxes": "s2 obligations - page-local/register/"
                              "closed-row populations stay distinct",
                "transfers": "s2 TRANSFERRED - residue moved with the row",
                "l2_verdicts": "scoped-L2 verdicts - not s1 behavior, not "
                               "DB_GOAL",
                "system_documents": "inventory-adjacent proxy "
                                    "(program_coverage rule) - not system "
                                    "coverage",
                "board_tasks": "coordination load - not packages, not "
                               "obligations",
                "completion_packages": "s2 completion-package stages",
                "terminal": "receipt axis - declared final_audits receipt, "
                            "never artefact counts",
                "parity": "execution axis - certified pilots",
                "route_links": "dated transition record - not current "
                               "state",
            }},
        "packages": board["open"],
        "board_counts": board["counts"], "board_total": board["total"],
        "board_task_count": board.get("total", 0),
        "reopened": reopened,
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


def _atomic_write_bytes(path, data):
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp_")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
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


def _gen_inputs(db):
    """Every consumed input declared to the generation store
    (OPUS-REQ-DATA-ADOPT-GENERATION-LIB): the configured inputs keyed by
    their exported relative path, the instruments that produced the verdicts,
    this generator, and the document-tree preimage. TEAM.json is `volatile`:
    the board is rewritten every few seconds during fleet activity, so a
    mid-commit move is drift - the generation binds the snapshot bytes it
    captured - rather than a refused commit (the reporter's own fingerprint
    check already aborts a build whose inputs moved)."""
    ins = {}
    for rel in INPUTS:
        ins["in:%s" % rel] = {"path": str(db / rel),
                              "required": rel in REQUIRED_INPUTS}
    ins["in:_index/_inbox/TEAM.json"]["volatile"] = True
    gfz = ROOT / "Database" / "Tools" / "analysis-kit" / "gfz-scripts"
    for name in ("check_questions.py", "transfer_audit.py", "generation.py"):
        ins["instrument:%s" % name] = {"path": str(gfz / name),
                                       "required": False}
    ins["generator:progress_report.py"] = {"path": str(HERE
                                                      / "progress_report.py"),
                                           "required": False}
    ins["preimage:doc-signature.txt"] = {"path": str(DOCSIG),
                                         "required": True}
    return ins


def _prune_generations(store, keep=8):
    """Bound the store: keep CURRENT plus the newest `keep` generations -
    each generation snapshots every input, so retention must be finite.
    `.rejected` candidates are diagnosis data and are never touched."""
    try:
        cur = store.current_id()
        gens = sorted(d for d in os.listdir(store.root)
                      if re.match(r"^g\d{8}T\d{6}Z-.", d))
        for g in gens[:-keep]:
            if g != cur:
                shutil.rmtree(os.path.join(store.root, g),
                              ignore_errors=True)
    except OSError:
        pass


def write_all(snap, counters, db):
    """Commit one generation coherently through generation.py: render the
    outputs into a `.partial` build directory; the store re-fingerprints
    every declared input at commit (a moved source refuses the generation,
    FAILURE.json records it, CURRENT keeps the last COMPLETE generation);
    then the live outputs become a verified copy of the committed
    generation's outputs - fingerprint-bearing snapshot.json LAST, so a
    mid-copy failure leaves the set carrying the PRIOR fingerprint
    (a coherent last-good set or a detectably mixed one), never a silent
    mix. History records the publication only after the committed set
    verifies complete."""
    if GEN is None:
        raise ProgressError("generation library unavailable "
                            "(Database/Tools/analysis-kit/gfz-scripts/"
                            "generation.py)")
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
    plan = [(p.name, t) for p, t in texts]
    plan.append((SNAP_JSON.name, json.dumps(snap, indent=1) + "\n"))
    # Final cutover re-check: an input moved between build() and publication
    # aborts - the store's commit does the same for declared inputs; this
    # covers the document tree those inputs describe.
    if fingerprint(db) != snap["freshness"]["fingerprint"]:
        raise ProgressError(
            "INCOMPLETE - an input moved between build and commit; "
            "aborted, prior generation retained")
    # The document preimage is committed INTO the generation so its exports
    # carry exactly what the consumed documents hashed to.
    docpre = "\n".join(_doc_preimage(db)) + "\n"
    DOCSIG.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_bytes(DOCSIG, docpre.encode("utf-8"))
    store = GEN.Store(str(STORE_ROOT))
    states = input_states(db)
    validated = {}
    for rel in INPUTS:
        st = states.get(rel, {})
        if rel in REQUIRED_INPUTS and st.get("state") != "present":
            validated["in:%s" % rel] = "schema: %s" % (
                st.get("reason") or st.get("state"))
    try:
        build_ = store.begin(_gen_inputs(db), generator={
            "name": "progress_report.py",
            "sha256": _sha(HERE / "progress_report.py"),
            "parser": PARSER_VERSION})
        for name, text in plan:
            with open(build_.output_path(name), "w", encoding="utf-8",
                      newline="\n") as f:
                f.write(text)
        # Recheck the document preimage at the commit edge - a source moved
        # after begin() must refuse the generation even though the declared
        # inputs did not move.
        if "\n".join(_doc_preimage(db)) + "\n" != docpre:
            store._fail(build_,
                        "document tree moved during the build")
        gid = store.commit(build_, [n for n, _ in plan],
                           validated=validated)
    except GEN.GenerationError as e:
        raise ProgressError("generation commit failed: %s" % e)
    man, gdir, probs = store.open_current()
    if probs or not man or man.get("generation") != gid:
        raise ProgressError("committed generation does not open clean: %s"
                            % "; ".join(probs or ["CURRENT moved"]))
    # Verified copy-out: the live outputs are a byte-exact copy of the
    # committed generation, snapshot.json last.
    dest = {"snapshot.json": SNAP_JSON, "snapshot.md": SNAP_MD,
            "crosswalk.md": CROSS_MD, "metrics.md": MET_MD,
            "PROGRESS.md": PROGRESS}
    order = ["snapshot.md", "crosswalk.md", "metrics.md", "PROGRESS.md",
             "snapshot.json"]
    try:
        for name in order:
            data = open(os.path.join(gdir, "outputs", name), "rb").read()
            _atomic_write_bytes(dest[name], data)
    except BaseException as e:
        raise ProgressError(
            "publication copy failed (%s) - the live set may be mixed; "
            "generation %s is intact and the store still serves it"
            % (e, gid))
    problems = _verify_outputs(snap)
    if problems:
        raise ProgressError("output set incomplete after commit: "
                            + "; ".join(problems))
    history_append(counters, snap["freshness"]["fingerprint"])
    _prune_generations(store)
    gen = snap["generated_at_utc"]
    ident = snap["identity"]
    print("wrote PROGRESS.md + _index/progress/{snapshot.json,snapshot.md,"
          "crosswalk.md,metrics.md} @ %s head=%s board=%s fp=%s gen=%s" %
          (gen, ident["git_head"], ident["board"],
           snap["freshness"]["fingerprint"][:10], gid))


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
    rec = {"failed_at_utc": datetime.now(timezone.utc)
           .isoformat(timespec="seconds"),
           "git_head": git_head(), "state": "INCOMPLETE", "reason": str(err),
           "live_snapshot_fingerprint": last_fp or "none",
           "missing": _m, "invalid": _i,
           "parser_version": PARSER_VERSION,
           "note": "the live output set is the prior generation, untouched"}
    # The live outputs - snapshot.json included - are NOT written: they stay the
    # last coherent generation, and `check` reports this record beside them.
    Path(STORE_ROOT).mkdir(parents=True, exist_ok=True)
    _atomic_write(last_failure_path(), json.dumps(rec, indent=1) + "\n")


def last_failure_path():
    return Path(STORE_ROOT) / LAST_FAILURE_NAME


def last_failure(snap=None):
    """The recorded failed attempt if it is newer than the live snapshot's
    generation, else None."""
    try:
        rec = json.loads(last_failure_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    gen = (snap or {}).get("generated_at_utc") or ""
    return rec if rec.get("failed_at_utc", "") > gen else None


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


# Where the project goes after the database, and who decides: the charter's
# section 0 is the human authority, PROJECT-LIFECYCLE.json its machine twin.
# Linked relative to PROGRESS.md (Database/FFXII TZA/).
LIFECYCLE_LINE = (
    "\n*Lifecycle: the project is in its DATABASE phase; L1+L2 is the "
    "database goal and L3 is not a prerequisite for it. What follows, and "
    "who authorizes it, is set by [RECONSTRUCTION-CHARTER.md section 0]"
    "(../../RECONSTRUCTION-CHARTER.md#0-project-lifecycle-user-directive-2026-10-02) "
    "(machine-readable twin: `_index/workflow/PROJECT-LIFECYCLE.json`). "
    "Parity pilots run now are database-phase evidence probes: they test "
    "whether a database claim or contract is sufficient, they do not start "
    "reconstruction, and pilot counts are not a completion score.*\n")


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
    lines.append("| L2 verdicts (**scoped** L2 - not whole-database "
                 "completion; per-system open obligations are in the route) | "
                 "**%d MET of %d systems**; blocking dims: "
                 "types %d, runtime %d · LIVE-unruled cells %d | L2-VERDICTS.md |"
                 % (l2["verdict_column"].get("MET", 0), l2["systems_scored"],
                    l2["systems_scored"] - l2["per_dimension_satisfied"]["types"],
                    l2["systems_scored"] - l2["per_dimension_satisfied"]["runtime"],
                    sum(l2["per_dimension_live_unruled"].values())))
    # DASHBOARD-MEANINGS §4: DB_GOAL sits beside scoped L2 so the 52/52 cannot
    # read as completion. The gate itself (goal_gate.py, whole-tree walk) is
    # too heavy for this adapter, but the terminal receipt is a fingerprinted
    # input: while declared final_audits < 30 the goal verdict cannot be MET,
    # so NOT_MET here is derived, not re-run. If the receipt ever reads 30 the
    # line reports UNMEASURED until goal_gate.py is run again.
    fg = term["final_audits_declared"]
    goal_state = ("NOT_MET - declared `final_audits` %s / 30; "
                  "`goal_gate.py` is the instrument of record" % fg) \
        if isinstance(fg, int) and fg < 30 else \
        "UNMEASURED - run goal_gate.py (declared receipt no longer forces a verdict)"
    lines.append("| DB_GOAL (whole-database goal gate) | **%s** | "
                 "PROGRAM-STATE.md receipt |" % goal_state)
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
    # DASHBOARD-MEANINGS §4: board tasks measure coordination load, not
    # remaining knowledge - the line is renamed so it cannot read as the
    # completion count, and completion packages are shown separately by stage.
    lines.append("| open board tasks (coordination load) | %d open (%s) | "
                 "TEAM.json |"
                 % (len(snap["packages"]), ", ".join(
                     "%s %d" % (k, v) for k, v in sorted(openk.items()))))
    # §2 obligation outcomes - separate counts, never summed into one total.
    wiq = pb.get("closed_id") if pb.get("closed_id") is not None else None
    lines.append("| obligation outcomes (separate, never summed) | ANSWERED "
                 "%d · DISPOSITIONED %d (NAS %d / OEB %d) · WITHDRAWN %d · "
                 "TRANSFERRED %s · REOPENED %d · WAITING-INTEGRATION %s "
                 "(mis-marked closed-row boxes) | registers + batch-K + "
                 "read_boxes |"
                 % (dis["accepted_answers"],
                    dis["no_admissible_source"]
                    + dis["out_of_evidence_boundary"],
                    dis["no_admissible_source"],
                    dis["out_of_evidence_boundary"],
                    q.get("WITHDRAWN", 0),
                    "UNMEASURED" if t["obligations"] is None
                    else t["obligations"],
                    snap.get("reopened", 0),
                    "UNMEASURED" if wiq is None else wiq))
    cpk = snap.get("completion_packages", {})
    if cpk.get("state") != "CURRENT":
        lines.append("| completion packages | UNMEASURED - %s | "
                     "_index/completion-packages/ |" % cpk.get("engine"))
    else:
        lines.append("| completion packages by stage | %s | "
                     "_index/completion-packages/ |"
                     % (", ".join("%s %d" % (k, v) for k, v in
                                  sorted(cpk["by_stage"].items()))
                        or "none"))
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
    # The lifecycle authority beside the L3 line (user context refresh v3 /
    # addendum; FABLE-REQ-DATA-CONTEXT-REFRESH-MIRROR-PROGRESS-1003). Static
    # text: the generator does not read the lifecycle JSON, so it adds no
    # input to the fingerprint.
    lines.append(LIFECYCLE_LINE)
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


_OQ_REL_LINK = re.compile(r"\]\((\.\./)")

def _oq_link_rebase(text):
    """OQ cells carry markdown links written relative to _index/OPEN-QUESTIONS.md
    (depth 1); crosswalk.md lives one level deeper (_index/progress/), so every
    `../` target emitted here needs one more step or it breaks (check_links)."""
    return _OQ_REL_LINK.sub(r"](../../", text)


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
    obligs = [p for p in snap["packages"]
              if p.get("discriminator") != "chore:coordination"]
    chores = [p for p in snap["packages"]
              if p.get("discriminator") == "chore:coordination"]
    for i, p in enumerate(obligs, 1):
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
    if chores:
        # R6 (CROSSWALK-MEANINGS): publish/checkpoint chores are coordination
        # steps - listed, but outside the route's obligation ordering.
        out.append("\n## Coordination chores (board tasks, not completion "
                   "obligations)\n\n")
        out.append("| id | status | owner |\n|---|---|---|\n")
        for p in chores:
            out.append("| `%s` | %s | %s |\n"
                       % (p["id"], p["status"], p["owner"]))
    out.append("\n## Transferred obligations (never complete, never vanish)\n\n")
    t = snap["transfers"]
    if t["obligations"] is None:
        out.append("UNMEASURED - transfer_audit unavailable: %s\n" % t["engine"])
    else:
        out.append("%d batch-K obligations checked, %d untracked.\n"
                   % (t["obligations"], t["untracked"]))
        # R1 (CROSSWALK-MEANINGS): every transferred obligation is a row -
        # '0 untracked' is the audit's verdict, not the end of the debt.
        if t.get("rows"):
            out.append("| register obligation | class | destination | "
                       "destination owner | next action |\n"
                       "|---|---|---|---|---|\n")
            prob_by_id = {}
            for p in t["problems"]:
                prob_by_id[str(p).split(":")[0].strip()] = p
            for r in t["rows"]:
                state = prob_by_id.pop(r["id"], None)
                out.append("| `%s` | %s | %s | %s | %s |\n"
                           % (r["id"], r["transfer_class"],
                              ("UNTRACKED - " + str(state)[:100] if state
                               else r["destination"]).replace("|", "\\|"),
                              r["destination_owner"], r["next_action"]))
            for rid, p in prob_by_id.items():
                out.append("| `%s` | - | UNTRACKED: %s | UNMEASURED | resolve "
                           "the audited transfer |\n"
                           % (rid.replace("|", "\\|"),
                              str(p)[:120].replace("|", "\\|")))
        else:
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
    # R3 (CROSSWALK-MEANINGS): the register's owner-doc cell is often blank;
    # the owning page is derivable from the unticked box that names the row.
    page_of = {}
    for ob in (snap.get("page_boxes") or {}).get("obligations") or []:
        for i in ob.get("named_ids", []):
            page_of.setdefault(i, ob["file"])
    out.append("\n## Page obligations (open questions)\n\n")
    out.append("| id | status | owner doc | evidence / question | next "
               "action |\n|---|---|---|---|---|\n")
    for r in res["oq_open_rows"]:
        # Only a register-sourced owner cell is written relative to
        # _index/OPEN-QUESTIONS.md and needs the rebase. The naming-page
        # fallback is built here already relative to _index/progress/, so
        # rebasing it as well gave ../../../ (9 broken links, FABLE's final
        # audit pass 29; fixed 2026-10-03, SWE2-DATA).
        if r["owner"]:
            owner = _oq_link_rebase(r["owner"])
        else:
            pf = page_of.get(r["id"])
            owner = ("[%s](../../%s)" % (pf, pf)) if pf else "UNKNOWN"
        out.append("| %s | %s | %s | %s | answer or withdraw the row |\n"
                   % (r["id"], r["status"],
                      owner.replace("|", "\\|"),
                      r["question"].replace("|", "\\|")))
    pb = snap["page_boxes"]
    out.append("\n## Page-box obligations (per unticked checkbox)\n\n")
    if pb.get("no_id") is None:
        out.append("UNMEASURED - %s\n" % pb["engine"])
    elif not pb.get("obligations"):
        out.append("None at this fingerprint.\n")
    else:
        out.append("*One row per unticked box. `page-local` boxes name no "
                   "register row (and never waive the work); "
                   "`mis-marked-closed` boxes name only closed rows; "
                   "`live-row-residue` boxes name a live row already "
                   "counted above - the class column keeps the three "
                   "populations distinct.*\n\n")
        out.append("| anchor | class | requirement | owner | reviewer | "
                   "dedup links | discriminator |\n"
                   "|---|---|---|---|---|---|---|\n")
        for o in pb["obligations"]:
            out.append("| `%s` | %s | %s | %s | %s | %s | %s |\n" % (
                o["anchor"], o["class"],
                o["requirement"].replace("|", "\\|"),
                o["owner"], o["reviewer"],
                ", ".join(o["dedup"]).replace("|", "\\|"),
                o["discriminator"].replace("|", "\\|")))
    out.append("\n## Dispositioned rows - residue moved to a carrier "
               "(closed for the gate, residue still required elsewhere)\n\n")
    sr = res.get("superseded_residue_rows", [])
    # R4 (CROSSWALK-MEANINGS): a SUPERSEDED row that is a duplicate or a split
    # carries NO residue of its own - the survivor row(s) carry it. Only a
    # carrier-bearing supersession stays in the residue table, with the
    # carrier as its own column.
    disp, dups = [], []
    for r in sr:
        st = r["status_text"]
        m = re.search(r"(?i)duplicate of\s+`?([A-Z]+-\d+[a-z]?)", st)
        if m:
            dups.append((r, "duplicate", m.group(1)))
            continue
        m = re.search(r"(?i)split into\s+(.+?)(?:\(|\.\s|$)", st)
        if m:
            surv = ", ".join(re.findall(r"[A-Z]+-\d+[a-z]?", m.group(1)))
            dups.append((r, "split", surv or "see status text"))
            continue
        disp.append(r)
    if not disp:
        out.append("None at this fingerprint.\n")
    else:
        out.append("| id | owner doc | carrier | status text |\n"
                   "|---|---|---|---|\n")
        for r in disp:
            st = r["status_text"]
            cm = (re.search(r"(?i)carrier[:\s`]+([A-Za-z][\w-]+)", st)
                  or re.search(r"(?i)superseded by\s+`?([A-Z]+-\d+[a-z]?)", st))
            out.append("| %s | %s | %s | %s |\n"
                       % (r["id"],
                          _oq_link_rebase(r["owner"] or "UNKNOWN")
                              .replace("|", "\\|"),
                          cm.group(1) if cm else "see status text",
                          _oq_link_rebase(st).replace("|", "\\|")))
    if dups:
        out.append("\n### Duplicates and splits - no residue of their own "
                   "(the survivor row carries it)\n\n")
        out.append("| id | owner doc | kind | survivor(s) | status text |\n"
                   "|---|---|---|---|---|\n")
        for r, kind, surv in dups:
            out.append("| %s | %s | %s | %s | %s |\n"
                       % (r["id"],
                          _oq_link_rebase(r["owner"] or "UNKNOWN")
                              .replace("|", "\\|"), kind, surv,
                          _oq_link_rebase(r["status_text"])
                              .replace("|", "\\|")))
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
    lf = last_failure(snap)
    if lf:
        print("NOTE: the last generation attempt failed at %s (%s); the live set is the"
              " prior generation %s, untouched" % (lf.get("failed_at_utc"), lf.get("reason"),
                                                  snap.get("generated_at_utc")))
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
    # Generation coherence: when the store exists, the live outputs must be
    # the CURRENT generation's committed bytes - a hand-assembled or
    # generation-mixed set is INCOMPLETE, never CURRENT (CKPT10R3/export).
    if GEN and os.path.isfile(os.path.join(str(STORE_ROOT), "CURRENT")):
        man, gdir, gprobs = GEN.Store(str(STORE_ROOT)).open_current()
        if gprobs:
            print("INCOMPLETE: store CURRENT does not open clean: %s"
                  % "; ".join(gprobs))
            return 2
        for name, meta in man["outputs"].items():
            lp = {"snapshot.json": SNAP_JSON, "snapshot.md": SNAP_MD,
                  "crosswalk.md": CROSS_MD, "metrics.md": MET_MD,
                  "PROGRESS.md": PROGRESS}.get(name)
            if lp is None or not lp.exists() \
                    or hashlib.sha256(lp.read_bytes()).hexdigest() \
                    != meta["sha256"]:
                print("INCOMPLETE: live %s differs from generation %s"
                      % (name, man["generation"]))
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
            # checked_at goes to a sidecar, NOT the member: snapshot.json
            # must stay byte-identical to the committed generation's output.
            # The sidecar lives beside the doc preimage (the ignored work
            # tree) - it is a receipt, not an output.
            DOCSIG.parent.mkdir(parents=True, exist_ok=True)
            _atomic_write(DOCSIG.parent / "progress-checked-at.json",
                          json.dumps(
                {"checked_at_utc": datetime.now(timezone.utc)
                 .isoformat(timespec="seconds"),
                 "fingerprint": snap["freshness"]["fingerprint"]}) + "\n")
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
    ap.add_argument("mode", choices=["generate", "auto", "check", "status",
                                     "export", "verify-zip"])
    ap.add_argument("target", nargs="?",
                    help="ZIP path for export / verify-zip")
    ap.add_argument("--db", default=str(DB))
    a = ap.parse_args()
    db = Path(a.db)
    if a.mode in ("export", "verify-zip"):
        # Export is exactly one pinned generation (EXPORT-COHERENT-
        # GENERATION): export() opens CURRENT verified, writes manifest +
        # outputs + input snapshots, re-opens the ZIP and checks every
        # member against the manifest before renaming it live. verify_zip()
        # labels a hand-made or generation-mixed ZIP UNVERIFIED - a member
        # produced by a later generation than the declared snapshot is
        # detected, never called CURRENT.
        if not a.target:
            ap.error("%s needs a ZIP path" % a.mode)
        if GEN is None:
            print("generation library unavailable")
            sys.exit(2)
        if a.mode == "verify-zip":
            label, info = GEN.verify_zip(a.target)
            print(label, json.dumps(info))
            sys.exit(0 if label == "VERIFIED" else 1)
        try:
            gid = GEN.Store(str(STORE_ROOT)).export(a.target)
            print("EXPORTED %s -> %s" % (gid, a.target))
            sys.exit(0)
        except GEN.GenerationError as e:
            print("REFUSED: %s" % e)
            sys.exit(1)
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
