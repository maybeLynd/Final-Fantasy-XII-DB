#!/usr/bin/env python3
"""recent_changes.py - "Recent Meaningful Changes": knowledge progress versus workflow activity.

FABLE-CLASSIFIER-RECENT-CHANGES-1003 (FABLE builds, SWE2-DATA reviews). Design: SWE2-DATA's plan,
`_index/candidates/swe2data-program-state-present-tense-1003/README.md` section (3); vocabulary: the
user's improvement addendum sections 2 and 10 and DASHBOARD-MEANINGS section 6.3 (FABLE's fragment).

WHAT IT DOES. For every commit in a window it derives CANONICAL EVENTS from WHAT changed - a register
row's state, a correction record, an accepted review of an evidence record, a package or type promotion,
an L2 cell, a parity row, or the path class of a commit that carries none of those. Commit size and line
counts are never read. Each event maps to one class through EVENT_CLASS (one table, below); a commit may
carry several events. A changed path that no rule accounts for is reported UNCLASSIFIED, never guessed.

THE RULES (event kind -> class; DATA's table plus FABLE's additions, marked +):
  register-answered      row moved to ANSWERED with a dated lead          NEW FF12 KNOWLEDGE
  register-narrowed      live lead newly NARROWED, dated                   NEW FF12 KNOWLEDGE
  register-superseded    live lead newly SUPERSEDED, dated                 NEW FF12 KNOWLEDGE
  register-undated       the above but no YYYY-MM-DD in the lead           UNCLASSIFIED (DATA requires a dated lead)
  register-new-open      a newly registered OPEN/PARTIAL/BLOCKED row       UNCLASSIFIED (DATA's table has no row)
  register-other         any other state change (PARTIAL, NAS/OEB,         UNCLASSIFIED (DATA's table has no row)
                         WITHDRAWN/NOT A QUESTION, reopen, removal)
  correction-record      a candidates/ record in the correction gate's     CORRECTED / FALSIFIED FF12 CLAIM
                         shape (is_record: consumer + agrees/revised-here/
                         routed-to- + an affected/corrects declaration),
                         new or with changed declarations, AND the same
                         commit adds a new ~~strike~~ to a database .md
                         (DATA: "a struck-and-replaced claim with a
                         correction record"). The record shape alone also
                         covers consumer checks of publishes that strike
                         nothing, so it is not enough on its own.
  evidence-accepted      a review record (REVIEW.md, or a *review* dir's   NEW RUNTIME / ORIGINAL-CODE EVIDENCE
                         README) whose verdict is ACCEPT and whose header
                         cites `_experiments/evidence/<rec>`, the FIRST
                         accepting review of that record in history. The
                         board is not reachable from git (TEAM.json is no
                         longer committed after 2026-10-01), so the review
                         record stands in for DATA's "review task DONE with
                         verdict:ACCEPT". The event is dated at the review.
  evidence-unreviewed    a new evidence record with no accepting review   UNCLASSIFIED
                         from its commit up to HEAD. (+) A record that IS
                         accepted at or after its commit yields no event at
                         the addition; it is counted once, at the review,
                         and the text report lists it under ACTIVITY.
  package-accepted       PKG stage or a work-item stage newly              NEW RECONSTRUCTION-GRADE TYPE / CONTRACT /
                         accepted-and-incorporated                         RELATIONSHIP
  package-other          any other PKG stage move                          UNCLASSIFIED (DATA names acceptance only)
  type-promoted          _types/*.tsv with a readiness column: new rows    NEW RECONSTRUCTION-GRADE TYPE / CONTRACT /
                         or readiness moved UP the KNOWLEDGE-SCHEMA ladder RELATIONSHIP
  l2-met                 an L2-VERDICTS cell newly satisfied (progress_    NEW RECONSTRUCTION-GRADE TYPE / CONTRACT /
                         report.dim_satisfied) or the L2 column newly MET  RELATIONSHIP
  parity-probe           PARITY-STATUS.md table row change                 RECONSTRUCTION / DIFFERENTIAL PROBE
  parity-certification   the "N of M pilots certified" line or a row       INTEGRATION / PARITY EVIDENCE
                         carrying CERTIF changed
  page-section-record    (+) a database page gains a heading (section) in  NEW FF12 KNOWLEDGE
                         the same commit that adds a new candidate record
                         (README + rows.json / apply*.py / *applier*.py,
                         or + a .py control) and strikes nothing -
                         interior-citation, homing and consume-accepted-
                         packet publishes. The brief's "no affected: line"
                         is replaced by "not a correction" (no new strike):
                         FABLE's consume records carry affected: lines as
                         consumer checks while striking nothing.
  review-verdict         (+) a review record that is not a first evidence  WORKFLOW / COORDINATION
                         acceptance (package/interior reviews, REJECTs,
                         repeat reviews): the knowledge it gates is counted
                         at its publish
  tools                  Database/Tools/** (not Tools/work/), _index/      TOOLING / INSTRUMENTATION
                         progress/*.py and progress.config.json
  board                  _index/_inbox/** (TEAM.json, TEAM.md, resume and  WORKFLOW / COORDINATION
                         inbox notes, op files)
  workflow-doc           (+) _index/workflow/** process documents          WORKFLOW / COORDINATION
  generated              PROGRESS.md, _index/progress/* outputs,           GENERATED / BOOKKEEPING ONLY
                         _index/knowledge.sqlite, */generations/*
  residual               anything else                                     UNCLASSIFIED

COVERAGE. In a commit that carries a knowledge-axis event, the accompanying page, register-text,
candidate, experiment-doc and other _index/ edits are covered by it (they are the text of that event).
In a commit without one they are residual -> UNCLASSIFIED, one event per residual category. Paths under
Database/Tools/work/ and outside Database/ are never covered.

PLACEMENT NOTE. DATA's plan diffs the register against the previous committed generation in
progress/history.jsonl. history.jsonl carries counters only (no row ids, no commit), so the row diff runs
per commit from git (parent vs commit, check_questions.classify on each revision's text); the text report
prints history.jsonl's oq_answered delta over the window as a cross-check.

USAGE
  python recent_changes.py [--db DB] [--json OUT] [--out TEXT]      last 24 h and 7 d, ending now
  python recent_changes.py --since 2026-10-01 [--until ...]          one custom window
  python recent_changes.py --range A..B                              one window over a revision range
  python recent_changes.py --self-test
Output contract (agreed with SWE2-FRONTIER for the dashboard adapter): see build_json(). Files are written
to a temp name and renamed at the end; a failed run writes nothing. Exit 0 on success.
"""
import argparse, collections, difflib, importlib.util, io, json, os, re, subprocess, sys, tempfile
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_questions as CQ            # noqa: E402  the register classifier
import publish_correction_gate as PCG   # noqa: E402  the correction record shape

TOOL_VERSION = "1"

# ------------------------------------------------------------------ classes
K_NEW = "NEW FF12 KNOWLEDGE"
K_CORR = "CORRECTED / FALSIFIED FF12 CLAIM"
K_EVID = "NEW RUNTIME / ORIGINAL-CODE EVIDENCE"
K_TYPE = "NEW RECONSTRUCTION-GRADE TYPE / CONTRACT / RELATIONSHIP"
K_PROBE = "RECONSTRUCTION / DIFFERENTIAL PROBE"
K_PARITY = "INTEGRATION / PARITY EVIDENCE"
A_TOOL = "TOOLING / INSTRUMENTATION"
A_WORK = "WORKFLOW / COORDINATION"
A_GEN = "GENERATED / BOOKKEEPING ONLY"
UNCL = "UNCLASSIFIED"
KNOWLEDGE_CLASSES = [K_NEW, K_CORR, K_EVID, K_TYPE, K_PROBE, K_PARITY]
ACTIVITY_CLASSES = [A_TOOL, A_WORK, A_GEN]
ALL_CLASSES = KNOWLEDGE_CLASSES + ACTIVITY_CLASSES + [UNCL]


def axis_of(cls):
    if cls in KNOWLEDGE_CLASSES:
        return "knowledge"
    if cls in ACTIVITY_CLASSES:
        return "activity"
    return "unclassified"


# THE event -> class table. The self-test swaps entries of this table and requires the fixtures to fail.
EVENT_CLASS = {
    "register-answered": K_NEW,
    "register-narrowed": K_NEW,
    "register-superseded": K_NEW,
    "register-undated": UNCL,
    "register-new-open": UNCL,
    "register-other": UNCL,
    "correction-record": K_CORR,
    "evidence-accepted": K_EVID,
    "evidence-unreviewed": UNCL,
    "package-accepted": K_TYPE,
    "package-other": UNCL,
    "type-promoted": K_TYPE,
    "l2-met": K_TYPE,
    "parity-probe": K_PROBE,
    "parity-certification": K_PARITY,
    "page-section-record": K_NEW,
    "page-section-unreviewed": UNCL,
    "section-accepted": K_NEW,
    "review-verdict": A_WORK,
    "tools": A_TOOL,
    "board": A_WORK,
    "workflow-doc": A_WORK,
    "generated": A_GEN,
    "residual": UNCL,
}
# evidence.kind per event kind (the adapter contract). Every UNCLASSIFIED event carries "none".
EVIDENCE_KIND = {
    "register-answered": "register-transition", "register-narrowed": "register-transition",
    "register-superseded": "register-transition", "correction-record": "correction-record",
    "evidence-accepted": "review-accept", "package-accepted": "package-acceptance",
    "type-promoted": "type-promotion", "l2-met": "l2-verdict", "parity-probe": "parity-row",
    "parity-certification": "parity-row", "page-section-record": "review-accept",
    "section-accepted": "review-accept",
    "review-verdict": "path-class", "tools": "path-class", "board": "board",
    "workflow-doc": "path-class", "generated": "generated",
}
EVIDENCE_KINDS = {"register-transition", "correction-record", "review-accept", "package-acceptance",
                  "type-promotion", "l2-verdict", "parity-row", "path-class", "board", "generated",
                  "none"}

# ------------------------------------------------------------------ paths
DBP = "Database/FFXII TZA/"
REGISTER = DBP + "_index/OPEN-QUESTIONS.md"
CAND = DBP + "_index/candidates/"
EVID = DBP + "_experiments/evidence/"
EXPD = DBP + "_experiments/"
TYPES = DBP + "_types/"
PKGD = DBP + "_index/completion-packages/"
L2 = DBP + "_index/L2-VERDICTS.md"
PARITY = DBP + "_index/PARITY-STATUS.md"
INBOX = DBP + "_index/_inbox/"
WORKFLOWD = DBP + "_index/workflow/"
PROGRESSD = DBP + "_index/progress/"
HISTORY = PROGRESSD + "history.jsonl"
PAGE_RE = re.compile(r"^Database/FFXII TZA/\d{2}-[^/]+/")
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

# KNOWLEDGE-SCHEMA.md "The measurement" - the one ordered readiness sequence.
LADDER = ["DISCOVERED", "CLASSIFIED", "SEMANTICALLY IDENTIFIED", "SIGNATURE RESOLVED", "TYPE RESOLVED",
          "DEPENDENCIES RESOLVED", "BEHAVIORALLY UNDERSTOOD", "RUNTIME VALIDATED", "CONTRACT READY",
          "RECONSTRUCTION READY", "IMPLEMENTED", "DIFFERENTIAL TESTED", "PARITY CERTIFIED"]
PKG_STAGES = ["research", "evidence-ready", "review", "repair", "incorporation",
              "accepted-and-incorporated", "dispositioned"]
ACCEPTED_STAGE = "accepted-and-incorporated"


def path_category(p):
    """The single category of a changed path. Categories map to rules, never to classes directly."""
    if not p.startswith("Database/"):
        return "outside-database"
    if p.startswith("Database/Tools/work/"):
        return "tools-work"
    if p.startswith("Database/Tools/"):
        return "generated" if "/generations/" in p else "tools"
    if not p.startswith(DBP):
        return "outside-database"
    if p == DBP + "PROGRESS.md" or p == DBP + "_index/knowledge.sqlite" or "/generations/" in p:
        return "generated"
    if p.startswith(PROGRESSD):
        if p.endswith(".py") or p.endswith("progress.config.json"):
            return "tools"
        return "generated"
    if p.startswith(INBOX):
        return "board"
    if p.startswith(WORKFLOWD):
        return "workflow-doc"
    if p == REGISTER:
        return "register"
    if p.startswith(CAND):
        return "candidate"
    if p.startswith(EVID):
        return "evidence"
    if p.startswith(EXPD):
        return "experiment-doc"
    if p.startswith(TYPES):
        return "types"
    if p.startswith(PKGD):
        return "pkg"
    if p == L2:
        return "l2"
    if p == PARITY:
        return "parity"
    if PAGE_RE.match(p):
        return "page"
    if p.startswith(DBP + "_index/"):
        return "index-other"
    return "db-root"


# residual categories a knowledge-bearing commit covers (its accompanying text)
COVERABLE = {"page", "register", "candidate", "evidence", "experiment-doc", "types", "pkg", "l2",
             "parity", "index-other", "db-root"}

# ------------------------------------------------------------------ repos


class GitRepo:
    """Read-only git access: one `cat-file --batch` process for blobs, plain commands otherwise."""

    def __init__(self, root):
        self.root = root
        self._cat = None
        self._grep_cache = {}
        self._exists_cache = {}

    def _git(self, *args):
        r = subprocess.run(["git", "-C", self.root, "-c", "core.quotepath=false"] + list(args),
                           capture_output=True)
        if r.returncode not in (0, 1):
            raise RuntimeError("git %s failed: %s" % (" ".join(args[:3]),
                                                      r.stderr.decode("utf-8", "replace")[:300]))
        return r.stdout.decode("utf-8", "replace")

    def head(self):
        return self._git("rev-parse", "HEAD").strip()

    def blob(self, rev, path):
        """(blob sha, text) or (None, None) when absent."""
        if rev is None:
            return None, None
        if self._cat is None:
            self._cat = subprocess.Popen(["git", "-C", self.root, "cat-file", "--batch"],
                                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self._cat.stdin.write(("%s:%s\n" % (rev, path)).encode("utf-8"))
        self._cat.stdin.flush()
        hdr = self._cat.stdout.readline().decode("utf-8", "replace").split()
        if len(hdr) < 3 or hdr[1] != "blob":
            return None, None
        size = int(hdr[2])
        data = self._cat.stdout.read(size)
        self._cat.stdout.read(1)
        return hdr[0], data.decode("utf-8", "replace")

    def diff(self, parent, rev, path, context=0):
        return self._git("diff", "-U%d" % context, "--no-color", "--no-ext-diff", parent or EMPTY_TREE,
                         rev, "--", path)

    def exists(self, rev, path):
        """Whether `path` (file or directory) exists at rev."""
        if rev is None:
            return False
        k = (rev, path)
        if k not in self._exists_cache:
            self._exists_cache[k] = bool(self._git("ls-tree", "--name-only", rev, "--",
                                                   path.rstrip("/")).strip())
        return self._exists_cache[k]

    def grep(self, rev, needle, prefix):
        """Paths under prefix at rev whose text contains needle (fixed string)."""
        if rev is None:
            return []
        k = (rev, needle, prefix)
        if k not in self._grep_cache:
            out = self._git("grep", "-l", "-F", "-e", needle, rev, "--", prefix.rstrip("/"))
            self._grep_cache[k] = [ln.split(":", 1)[1] for ln in out.splitlines() if ":" in ln]
        return self._grep_cache[k]

    def commits(self, rev_args):
        """[{sha, parent, ct, subject, changes: [(status, path)]}], oldest first."""
        out = self._git("log", "--no-renames", "--diff-merges=first-parent", "--name-status",
                        "--format=%x01%H%x1f%P%x1f%ct%x1f%s", *rev_args)
        res = []
        for chunk in out.split("\x01")[1:]:
            lines = chunk.split("\n")
            sha, parents, ct, subject = lines[0].split("\x1f", 3)
            changes = []
            for ln in lines[1:]:
                if "\t" in ln:
                    st, p = ln.split("\t", 1)
                    changes.append((st[:1], p))
            res.append({"sha": sha, "parent": parents.split()[0] if parents.strip() else None,
                        "ct": int(ct), "subject": subject, "changes": changes})
        res.reverse()
        return res

    def close(self):
        if self._cat is not None:
            try:
                self._cat.stdin.close()
                self._cat.wait(timeout=10)
            except Exception:
                pass
            self._cat = None


class FakeRepo:
    """In-memory repo for the self-test: blobs keyed (rev, path)."""

    def __init__(self, blobs):
        self.blobs = blobs

    def blob(self, rev, path):
        t = self.blobs.get((rev, path))
        return (None, None) if t is None else ("%s:%s" % (rev, path), t)

    def diff(self, parent, rev, path, context=0):
        a = (self.blobs.get((parent, path)) or "").splitlines()
        b = (self.blobs.get((rev, path)) or "").splitlines()
        return "\n".join(difflib.unified_diff(a, b, "a/" + path, "b/" + path, n=context, lineterm=""))

    def exists(self, rev, path):
        p = path.rstrip("/")
        return any(r == rev and (q == p or q.startswith(p + "/")) for r, q in self.blobs)

    def grep(self, rev, needle, prefix):
        return sorted(q for (r, q), t in self.blobs.items()
                      if r == rev and q.startswith(prefix) and needle in t)


# ------------------------------------------------------------------ register rule
_CLS_CACHE = {}
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
NAS_LEADS = tuple(CQ.NO_ADMISSIBLE)


def _row_entry(rest):
    hit = _CLS_CACHE.get(rest)
    if hit is None:
        state, cells = CQ.classify(rest)
        lead = CQ.live_lead(cells[-1]).lstrip("*~ \t").upper() if len(cells) >= 2 else ""
        if lead.startswith(NAS_LEADS):
            cat = "NAS/OEB"
        elif lead.startswith("SUPERSEDED"):
            cat = "SUPERSEDED"
        elif lead.startswith("NARROWED"):
            cat = "NARROWED"
        else:
            cat = state
        hit = (cat, bool(DATE.search(lead[:96])), lead[:60])
        _CLS_CACHE[rest] = hit
    return hit


def register_rows(text):
    """{row id: (category, dated, lead)} - check_questions.read_table's regex and classifier, on text."""
    out = {}
    for m in re.finditer(r"^\|\s*(%s)\s*\|(.*)$" % CQ.QID, text or "", re.M):
        out[m.group(1)] = _row_entry(m.group(2))
    return out


KNOWN_TARGET = {"ANSWERED": "register-answered", "NARROWED": "register-narrowed",
                "SUPERSEDED": "register-superseded"}


def register_events(old, new):
    """[(kind, row id, detail)] for every row whose category moved."""
    ev = []
    for rid, n in new.items():
        o = old.get(rid)
        if o is not None and o[0] == n[0]:
            continue
        frm = o[0] if o else "absent"
        detail = "%s %s -> %s (%s)" % (rid, frm, n[0], n[2][:40])
        if n[0] in KNOWN_TARGET:
            ev.append((KNOWN_TARGET[n[0]] if n[1] else "register-undated", rid, detail))
        elif o is None:
            ev.append(("register-new-open" if n[0] in ("OPEN", "PARTIAL", "BLOCKED", "UNKNOWN")
                       else "register-other", rid, detail))
        else:
            ev.append(("register-other", rid, detail))
    for rid, o in old.items():
        if rid not in new:
            ev.append(("register-other", rid, "%s %s -> removed" % (rid, o[0])))
    return ev


# ------------------------------------------------------------------ correction / review records
AFFECTED_LINE = re.compile(r"(?im)^[\s>*_`|-]*affected[*_`]*\s*:[^\n]*")


def correction_shape(text):
    """The correction gate's record shape, exactly as publish_correction_gate.is_record tests it
    ('consumer' + an agreement token + an affected/corrects declaration naming a row id or path).
    Returns the sorted declaration lines (explicit `affected:` lines first), or None."""
    if not text or not re.search(r"consumer", text, re.I) or not PCG.AGREE.search(text) \
            or not PCG.AFFECTED.search(text):
        return None
    lines = sorted(m.group(0).strip() for m in AFFECTED_LINE.finditer(text))
    return lines or sorted(m.group(0).strip() for m in PCG.AFFECTED.finditer(text))


def is_review_path(p):
    if not p.startswith(CAND) or not p.endswith(".md"):
        return False
    d, b = p.rsplit("/", 1)
    return b == "REVIEW.md" or ("review" in d[len(CAND):].lower() and b == "README.md")


EVREF = re.compile(r"_experiments/evidence/([A-Za-z0-9_.\-]+)")
# a candidate record named in a review header or a record README: `_index/candidates/<dir>` or `candidates/<dir>`
CANDREF = re.compile(r"candidates/([A-Za-z0-9_.\-]+)")


def review_candidates(text):
    """Candidate packages a review's header block names (its subject), excluding review dirs themselves."""
    head = []
    for i, ln in enumerate((text or "").splitlines()):
        if i > 0 and ln.startswith("## "):
            break
        head.append(ln)
    return sorted({m.group(1).rstrip(".") for m in CANDREF.finditer("\n".join(head))
                   if "review" not in m.group(1)})


def accepted_review_cited(repo, sha, readme_text, ct, ctx):
    """N1 (SWE2-DATA review 33b51c821): a rule-(f) section counts as knowledge only when its record cites an
    independently accepted result: a review record (a *review* candidate dir) whose verdict at `sha` is ACCEPT
    (incl. ACCEPT-WITH-NARROWING), or an evidence record with an accepting review at or before this commit."""
    dirs = [m.group(1).rstrip(".") for m in CANDREF.finditer(readme_text or "")]
    # records link their reviews relatively, as `../<review dir>/REVIEW.md`
    dirs += re.findall(r"\.\./([A-Za-z0-9_.\-]*review[A-Za-z0-9_.\-]*)/REVIEW\.md", readme_text or "")
    for d in dict.fromkeys(dirs):
        if "review" not in d:
            continue
        p = CAND + d + "/REVIEW.md"
        if repo.exists(sha, p) and parse_review(repo.blob(sha, p)[1])[0] == "ACCEPT":
            return p
    for rec in set(m.group(1).rstrip(".") for m in EVREF.finditer(readme_text or "")):
        acc = ctx["accept_index"].get(rec)
        if (acc and acc[0] <= ct) or prior_acceptance(repo, sha, rec, ctx):
            return EVID + rec + "/"
    return None
VERDICT_LINE = re.compile(r"(?im)^[^\n]*\bverdict\b[^\n]*\b(?:ACCEPT|REJECT)[^\n]*")


def parse_review(text):
    """(verdict ACCEPT|REJECT|UNKNOWN, evidence records cited in the header block)."""
    lines = (text or "").splitlines()
    header = []
    for i, ln in enumerate(lines):
        if i > 0 and ln.startswith("## "):
            break
        header.append(ln)
    recs = sorted(set(m.group(1).rstrip(".") for m in EVREF.finditer("\n".join(header))))
    m = VERDICT_LINE.search(text or "")
    if not m:
        return "UNKNOWN", recs
    v = m.group(0).upper()
    if "REJECT" in v:
        return "REJECT", recs
    return "ACCEPT", recs


def evidence_record(p):
    rest = p[len(EVID):]
    return rest.split("/", 1)[0]


# ------------------------------------------------------------------ types / pkg / l2 / parity
def diff_lines(diff):
    """(removed, added, header_added) from a -U0 unified diff; header_added = new line 1's text."""
    rem, add, hdr = [], [], None
    newno = 0
    for ln in diff.splitlines():
        if ln.startswith("@@"):
            m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", ln)
            newno = int(m.group(1)) if m else 0
            continue
        if ln.startswith("+++") or ln.startswith("---") or ln.startswith("diff ") \
                or ln.startswith("index ") or ln.startswith("new file") or ln.startswith("deleted file"):
            continue
        if ln.startswith("+"):
            if newno == 1:
                hdr = ln[1:]
            add.append(ln[1:])
            newno += 1
        elif ln.startswith("-"):
            rem.append(ln[1:])
    return rem, add, hdr


def type_events(repo, c, path, head_headers):
    rem, add, hdr = diff_lines(repo.diff(c["parent"], c["sha"], path))
    header = hdr if hdr is not None else head_headers.get(path)
    if header is None:
        _, t = repo.blob(c["sha"], path)
        header = (t or "").split("\n", 1)[0]
        head_headers[path] = header
    cols = header.split("\t")
    if "readiness" not in cols:
        return None                                   # not a type/field register: residual
    ri = cols.index("readiness")
    ki = [0] + ([cols.index("offset")] if "offset" in cols else [])

    def keyed(lines):
        d = {}
        for ln in lines:
            f = ln.split("\t")
            if ln == header or len(f) <= ri or ln.startswith("#"):
                continue
            d[tuple(f[i] for i in ki)] = f[ri].strip()
        return d
    old, new = keyed(rem), keyed(add)
    added = [k for k in new if k not in old]
    up = [k for k in new if k in old and new[k] in LADDER and old[k] in LADDER
          and LADDER.index(new[k]) > LADDER.index(old[k])]
    if not added and not up:
        return None
    ex = (added + up)[0]
    return "%d new rows, %d readiness promotions (e.g. %s)" % (len(added), len(up), ".".join(ex))


PKG_STAGE_LINE = re.compile(r"\*\*stage\.\*\*\s*`?([A-Za-z][\w-]*)")


def pkg_state(text):
    """{'_package': stage, item id: stage}."""
    out = {}
    if not text:
        return out
    m = PKG_STAGE_LINE.search(text)
    if m:
        out["_package"] = m.group(1)
    col = None
    for ln in text.splitlines():
        if not ln.startswith("|"):
            col = None if not ln.strip() else col
            continue
        cells = [c.strip() for c in CQ.CELL.split(ln.strip().strip("|"))]
        low = [c.lower() for c in cells]
        if "stage" in low and ("item" in low or "#" in low):
            col = low.index("stage")
            continue
        if col is None or len(cells) <= col or re.match(r"^:?-+", cells[0] or "-"):
            continue
        sm = re.match(r"[`*]*([a-z][a-z-]+)", cells[col])
        if sm and sm.group(1) in PKG_STAGES:
            out[cells[0]] = sm.group(1)
    return out


def pkg_events(old_t, new_t, name):
    old, new = pkg_state(old_t), pkg_state(new_t)
    ev = []
    for k, st in new.items():
        if old.get(k) == st:
            continue
        label = name if k == "_package" else "%s %s" % (name, k)
        if st == ACCEPTED_STAGE:
            ev.append(("package-accepted", label, "%s %s -> %s" % (label, old.get(k, "absent"), st)))
        elif k in old or k == "_package":
            ev.append(("package-other", label, "%s %s -> %s" % (label, old.get(k, "absent"), st)))
    return ev


_PR = None


def progress_report_module(db):
    """progress_report.py, imported read-only for parse_verdicts / dim_satisfied."""
    global _PR
    if _PR is None:
        p = os.path.join(db, "_index", "progress", "progress_report.py")
        spec = importlib.util.spec_from_file_location("progress_report_rc", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _PR = mod
    return _PR


class _TextPath:
    def __init__(self, text):
        self.text = text or ""

    def exists(self):
        return True

    def read_text(self, **kw):
        return self.text


L2_DIMS = ("contract", "types", "relationships", "runtime", "script_data")


def l2_events(pr, old_t, new_t):
    def sat(text):
        s = set()
        for v in pr.parse_verdicts(_TextPath(text)):
            for d in L2_DIMS:
                if pr.dim_satisfied(v, d):
                    s.add((v["system"], d))
            if v.get("l2") == "MET":
                s.add((v["system"], "L2"))
        return s
    newly = sorted(sat(new_t) - sat(old_t))
    return [("l2-met", "%s %s" % k, "L2-VERDICTS %s %s newly satisfied" % k) for k in newly]


def parity_events(repo, c):
    rem, add, _ = diff_lines(repo.diff(c["parent"], c["sha"], PARITY))
    rows = [ln for ln in rem + add if ln.startswith("|") and not re.match(r"^\|[-:\s|]+$", ln)]
    cert = [ln for ln in rem + add if re.search(r"pilots certified", ln) or
            (ln.startswith("|") and re.search(r"CERTIF", ln, re.I))]
    ev = []
    if cert:
        ev.append(("parity-certification", PARITY, "certification line/row changed: %s" % cert[-1][:80]))
    if [r for r in rows if r not in cert]:
        ev.append(("parity-probe", PARITY, "%d table row lines changed" % len(rows)))
    return ev


HEADING_ADDED = re.compile(r"(?m)^\+#{1,6}\s+\S")
APPLIER = re.compile(r"(^rows\.json$|apply[^/]*\.py$|applier[^/]*\.py$)")


# ------------------------------------------------------------------ the commit classifier
def classify_commit(repo, c, ctx):
    """Events for one commit: [{kind, class, ref, detail}]. ctx: db, accept_index, head_headers."""
    sha, parent = c["sha"], c["parent"]
    changes = c["changes"]
    events = []
    covered = set()
    notes = []
    cats = collections.defaultdict(list)
    for st, p in changes:
        cats[path_category(p)].append((st, p))

    def emit(kind, ref, detail="", paths=()):
        events.append({"kind": kind, "ref": ref, "detail": detail})
        covered.update(paths)

    # (a) register transitions
    if cats.get("register"):
        _, old_t = repo.blob(parent, REGISTER)
        _, new_t = repo.blob(sha, REGISTER)
        for kind, rid, detail in register_events(register_rows(old_t), register_rows(new_t)):
            emit(kind, rid, detail)
        if any(e["kind"].startswith("register-") for e in events):
            covered.add(REGISTER)

    # (b) correction records, reviews, (f) page-section publishes - candidate dirs
    cand_dirs = collections.defaultdict(list)
    for st, p in cats.get("candidate", []):
        rest = p[len(CAND):]
        cand_dirs[rest.split("/", 1)[0]].append((st, p))
    page_md = [p for st, p in cats.get("page", []) if st in "AM" and p.endswith(".md")]
    pages_with_section = None
    rule_f_done = False
    for d, files in sorted(cand_dirs.items()):
        dir_events = 0
        for st, p in files:
            if st not in "AM" or not p.endswith(".md"):
                continue
            if is_review_path(p):
                _, txt = repo.blob(sha, p)
                verdict, recs = parse_review(txt)
                old_verdict = parse_review(repo.blob(parent, p)[1])[0] if st == "M" else None
                firsts = []
                if verdict == "ACCEPT" and old_verdict != "ACCEPT":
                    for rec in recs:
                        if not repo.exists(sha, EVID + rec):
                            continue
                        if rec in ctx.setdefault("_accepted_in_commit", {}).get(sha, set()):
                            continue
                        if prior_acceptance(repo, parent, rec, ctx):
                            continue
                        firsts.append(rec)
                        ctx["_accepted_in_commit"].setdefault(sha, set()).add(rec)
                for rec in firsts:
                    emit("evidence-accepted", EVID + rec + "/", "first accepting review: %s" % p, [p])
                # N1, second half: a published section counts as knowledge at the review that first ACCEPTs its
                # candidate package (the way evidence-accepted works), not at the author's publish.
                pkgs = []
                if not firsts and verdict == "ACCEPT" and old_verdict != "ACCEPT":
                    pkgs = [k for k in review_candidates(txt) if repo.exists(sha, CAND + k + "/README.md")]
                if pkgs:
                    emit("section-accepted", p, "first accepting review of %s" % ", ".join(pkgs[:3]), [p])
                elif not firsts:
                    emit("review-verdict", p, "%s%s" % (verdict, (" of " + ", ".join(recs)) if recs
                                                        else ""), [p])
                dir_events += 1
                continue
            _, txt = repo.blob(sha, p)
            aff = correction_shape(txt)
            if aff:
                old_aff = correction_shape(repo.blob(parent, p)[1]) if st == "M" else None
                # DATA: "a struck-and-replaced claim WITH a correction record". The gate's record shape
                # alone also covers consumer checks of publishes that strike nothing (measured: FABLE's
                # astra-returns-title record says "nothing is struck"), so the commit must also carry
                # a correction hunk (publish_correction_gate.find_correction_hunks) in a database page.
                if aff != old_aff and struck_correction(repo, c, ctx):
                    emit("correction-record", p, aff[0][:100], [p])
                    dir_events += 1
        # rule f: a new record (README + applier or control script) with a page section in the same
        # commit, and the commit is not a correction
        added = {p.rsplit("/", 1)[1]: p for st, p in files if st == "A"}
        readme = added.get("README.md")
        if readme and any(APPLIER.search(b) or b.endswith(".py") for b in added) and not dir_events \
                and not struck_correction(repo, c, ctx):
            if pages_with_section is None:
                pages_with_section = [p for p in page_md
                                      if HEADING_ADDED.search(repo.diff(parent, sha, p))]
            if pages_with_section:
                # N2: one rule-(f) event per commit - one per candidate directory would be a size proxy
                if not rule_f_done:
                    acc = accepted_review_cited(repo, sha, repo.blob(sha, readme)[1], c["ct"], ctx)
                    if acc:
                        emit("page-section-record", readme, "record %s + section on %s, incorporating the "
                             "accepted %s" % (d, (pages_with_section or ['?'])[0][len(DBP):], acc))
                    else:
                        emit("page-section-unreviewed", readme, "record %s + section on %s; no independently "
                             "accepted result cited - counted when a review accepts it" %
                             (d, (pages_with_section or ['?'])[0][len(DBP):]))
                    rule_f_done = True
                dir_events += 1
        if dir_events:
            covered.update(p for st, p in files)

    # (c) evidence records: new records are counted at their first accepting review
    recs = collections.OrderedDict()
    for st, p in cats.get("evidence", []):
        recs.setdefault(evidence_record(p), []).append((st, p))
    for rec, files in recs.items():
        is_new = any(st == "A" for st, _ in files) and not repo.exists(parent, EVID + rec)
        if not is_new:
            continue
        acc = ctx["accept_index"].get(rec)
        if acc and acc[0] >= c["ct"]:
            notes.append(("evidence-added-accepted", rec, acc[1]))
        elif rec in ctx.get("_accepted_in_commit", {}).get(sha, set()):
            notes.append(("evidence-added-accepted", rec, sha))
        else:
            emit("evidence-unreviewed", EVID + rec + "/", "new evidence record, no accepting review "
                 "from this commit up to HEAD")
        covered.update(p for _, p in files)
    if notes:
        covered.update(p for _, p in cats.get("experiment-doc", []))

    # (d) package stages, type rows, L2 cells
    for st, p in cats.get("pkg", []):
        name = p.rsplit("/", 1)[1]
        if not name.startswith("PKG-"):
            continue
        for kind, ref, detail in pkg_events(repo.blob(parent, p)[1], repo.blob(sha, p)[1],
                                            name[:-3]):
            emit(kind, ref, detail, [p])
    for st, p in cats.get("types", []):
        if p.endswith(".tsv") and st in "AM":
            detail = type_events(repo, c, p, ctx["head_headers"])
            if detail:
                emit("type-promoted", p, detail, [p])
    if cats.get("l2"):
        try:
            pr = progress_report_module(ctx["db"])
        except Exception as e:                                       # pragma: no cover
            pr = None
            ctx.setdefault("warnings", set()).add("L2 rule disabled: progress_report import "
                                                  "failed (%s)" % e)
        if pr is not None:
            for kind, ref, detail in l2_events(pr, repo.blob(parent, L2)[1], repo.blob(sha, L2)[1]):
                emit(kind, ref, detail, [L2])

    # (e) parity rows
    if cats.get("parity"):
        for kind, ref, detail in parity_events(repo, c):
            emit(kind, ref, detail, [PARITY])

    # (g, h, i) path classes - one event per class per commit
    for cat, kind in (("tools", "tools"), ("board", "board"), ("workflow-doc", "workflow-doc"),
                      ("generated", "generated")):
        ps = [p for _, p in cats.get(cat, [])]
        if ps:
            emit(kind, ps[0], "%d path(s)" % len(ps), ps)

    # residual: anything not covered
    knowledge = any(axis_of(ctx["table"][e["kind"]]) == "knowledge" for e in events)
    residual = collections.OrderedDict()
    for st, p in changes:
        if p in covered:
            continue
        cat = path_category(p)
        if knowledge and cat in COVERABLE:
            continue
        residual.setdefault(cat, []).append(p)
    for cat, ps in residual.items():
        emit("residual", ps[0], "%d uncovered %s path(s)" % (len(ps), cat))
    for e in events:
        e["class"] = ctx["table"][e["kind"]]
    return events, notes


def struck_correction(repo, c, ctx):
    """Whether the commit strikes a claim in a database file: a NEW ~~strike~~ pair (the correction gate's
    STRIKE, counted as a multiset of added minus removed lines, as find_correction_hunks does) in a
    changed .md under the database outside _inbox/ and candidates/. No keyword is required: a declared
    correction (affected: record) strikes without one (measured: ac1406035). Cached per commit."""
    cache = ctx.setdefault("_struck", {})
    if c["sha"] not in cache:
        hit = None
        for st, p in c["changes"]:
            if st in "AM" and PCG.DB_MD.match(p) and not p.startswith(CAND):
                rem, add, _ = diff_lines(repo.diff(c["parent"], c["sha"], p))
                new = collections.Counter(m.group(0) for a in add for m in PCG.STRIKE.finditer(a))
                new.subtract(m.group(0) for r in rem for m in PCG.STRIKE.finditer(r))
                if any(v > 0 for v in new.values()):
                    hit = p
                    break
        cache[c["sha"]] = hit
    return cache[c["sha"]]


def prior_acceptance(repo, parent, rec, ctx):
    """True when a review record at `parent` already ACCEPTs evidence record `rec` (header cite)."""
    for q in repo.grep(parent, "_experiments/evidence/" + rec, CAND):
        if not is_review_path(q):
            continue
        v, recs = parse_review(repo.blob(parent, q)[1])
        if v == "ACCEPT" and rec in recs:
            return True
    return False


def build_accept_index(repo, commits):
    """{evidence record: (ct, sha)} - the earliest accepting review among `commits` (oldest first)."""
    idx = {}
    for c in commits:
        for st, p in c["changes"]:
            if st not in "AM" or not is_review_path(p):
                continue
            v, recs = parse_review(repo.blob(c["sha"], p)[1])
            if v != "ACCEPT":
                continue
            for rec in recs:
                if rec not in idx:
                    idx[rec] = (c["ct"], c["sha"])
    return idx


# ------------------------------------------------------------------ run + report
def subject_prefix(s):
    return s.split(":", 1)[0].strip() if ":" in s else ""


def identity_of(s):
    pre = subject_prefix(s)
    if not pre:
        return None
    tok = pre.split()[0]
    return tok if re.match(r"^[A-Za-z0-9][A-Za-z0-9_-]*$", tok) else None


def iso(ts):
    return datetime.fromtimestamp(ts, timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def run(repo, db, commits, accept_commits, table=None):
    """All events for `commits` (oldest first). Returns (events, notes, warnings)."""
    ctx = {"db": db, "head_headers": {}, "table": table or EVENT_CLASS,
           "accept_index": build_accept_index(repo, accept_commits)}
    out, notes = [], []
    for c in commits:
        evs, ns = classify_commit(repo, c, ctx)
        for e in evs:
            e.update({"sha": c["sha"], "ct": c["ct"], "subject": c["subject"]})
            out.append(e)
        for n in ns:
            notes.append({"sha": c["sha"], "ct": c["ct"], "rec": n[1], "accepted_at": n[2]})
    return out, notes, sorted(ctx.get("warnings", ()))


def to_contract_event(e):
    cls = e["class"]
    kind = "none" if cls == UNCL else EVIDENCE_KIND.get(e["kind"], "none")
    return {"class": cls, "axis": axis_of(cls), "at": iso(e["ct"]), "title": e["subject"],
            "identity": identity_of(e["subject"]), "commit": e.get("sha"),
            "evidence": {"kind": kind, "ref": e["ref"]}}


def build_json(head, generated_at, windows, events):
    """The output contract agreed with SWE2-FRONTIER (dashboard adapter)."""
    return {"tool": "recent_changes.py", "version": TOOL_VERSION, "generated_at": generated_at,
            "source_commit": head,
            "windows": {k: {"since": v} for k, v in windows.items()},
            "events": [to_contract_event(e) for e in events]}


CONTRACT_EVENT_KEYS = {"class", "axis", "at", "title", "identity", "commit", "evidence"}


def validate_json(j):
    """Problems with the contract shape (empty list = valid)."""
    bad = []
    for k in ("tool", "version", "generated_at", "source_commit", "windows", "events"):
        if k not in j:
            bad.append("missing top-level key %s" % k)
    for name, w in (j.get("windows") or {}).items():
        if set(w) != {"since"}:
            bad.append("window %s keys %s" % (name, sorted(w)))
    for i, e in enumerate(j.get("events", [])):
        if set(e) != CONTRACT_EVENT_KEYS:
            bad.append("event %d keys %s" % (i, sorted(e)))
            continue
        if e["class"] not in ALL_CLASSES:
            bad.append("event %d class %r" % (i, e["class"]))
        elif e["axis"] != axis_of(e["class"]):
            bad.append("event %d axis %r for %r" % (i, e["axis"], e["class"]))
        ev = e["evidence"]
        if not isinstance(ev, dict) or set(ev) != {"kind", "ref"} or ev.get("kind") not in EVIDENCE_KINDS:
            bad.append("event %d evidence %r" % (i, ev))
        elif e["class"] == UNCL and ev["kind"] != "none":
            bad.append("event %d UNCLASSIFIED with evidence kind %s" % (i, ev["kind"]))
        if not isinstance(e["title"], str) or "\n" in e["title"]:
            bad.append("event %d title" % i)
    return bad


def history_control(repo, head, since_ts, until_ts):
    _, t = repo.blob(head, HISTORY)
    recs = []
    for ln in (t or "").splitlines():
        try:
            r = json.loads(ln)
            ts = datetime.fromisoformat(r["ts"]).timestamp()
        except Exception:
            continue
        recs.append((ts, r))
    before = [r for ts, r in recs if ts <= since_ts]
    inside = [r for ts, r in recs if since_ts < ts <= until_ts]
    if not inside:
        return "history.jsonl: no generation inside the window"
    a = before[-1] if before else inside[0]
    b = inside[-1]
    return ("history.jsonl (generated counters, not a git diff): oq_answered %s -> %s (%+d), "
            "oq_withdrawn %s -> %s, generations %s .. %s" % (
                a.get("oq_answered"), b.get("oq_answered"),
                (b.get("oq_answered") or 0) - (a.get("oq_answered") or 0),
                a.get("oq_withdrawn"), b.get("oq_withdrawn"), a.get("ts"), b.get("ts")))


def text_window(label, since_ts, until_ts, events, notes, commits, control):
    W = []
    evs = [e for e in events if since_ts <= e["ct"] <= until_ts]
    ns = [n for n in notes if since_ts <= n["ct"] <= until_ts]
    cms = [c for c in commits if since_ts <= c["ct"] <= until_ts]
    W.append("=" * 100)
    W.append("WINDOW %s: %s .. %s - %d commits" % (label, iso(since_ts), iso(until_ts), len(cms)))
    W.append("=" * 100)

    def line(e):
        pre = subject_prefix(e["subject"]) or e["subject"][:30]
        return "    %s  %-22s %-36s %-20s %s%s" % (e["sha"][:9], pre[:22], e["class"][:36], e["kind"],
                                                   e["ref"], ("  | " + e["detail"]) if e["detail"] else "")
    W.append("")
    W.append("KNOWLEDGE - canonical events (what the project learned or proved)")
    kn = [e for e in evs if axis_of(e["class"]) == "knowledge"]
    for cls in KNOWLEDGE_CLASSES:
        ce = [e for e in kn if e["class"] == cls]
        W.append("  %-56s %5d events in %4d commits" % (cls, len(ce), len({e["sha"] for e in ce})))
    W.append("  events:")
    for cls in KNOWLEDGE_CLASSES:
        for e in [e for e in kn if e["class"] == cls]:
            W.append(line(e))
    if not kn:
        W.append("    (none)")
    W.append("")
    W.append("ACTIVITY - throughput only; NEVER a knowledge or completion measure")
    W.append("  commits in window: %d" % len(cms))
    W.append("  commits carrying at least one knowledge event: %d" % len({e["sha"] for e in kn}))
    for cls in ACTIVITY_CLASSES:
        ce = [e for e in evs if e["class"] == cls]
        W.append("  %-56s %5d events in %4d commits" % (cls, len(ce), len({e["sha"] for e in ce})))
    acc_in = sum(1 for n in ns if n["accepted_at"] in {c["sha"] for c in cms})
    W.append("  new evidence records added, counted as evidence at their first accepting review: %d "
             "(that review inside this window: %d, after it: %d)" % (len(ns), acc_in, len(ns) - acc_in))
    W.append("")
    un = [e for e in evs if e["class"] == UNCL]
    W.append("UNCLASSIFIED - no rule decides these; listed, never guessed (%d events in %d commits)" % (
        len(un), len({e["sha"] for e in un})))
    by = collections.Counter((e["kind"], e["detail"].split(" ", 2)[-1] if e["kind"] == "residual" else "")
                             for e in un)
    for (k, sub), n in sorted(by.items(), key=lambda x: -x[1]):
        W.append("  %5d  %s%s" % (n, k, (" - " + sub) if sub else ""))
    W.append("  events:")
    for e in un:
        W.append(line(e))
    W.append("")
    W.append("CONTROL  " + control)
    W.append("")
    return W


def write_atomic(path, text):
    d = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".rc-", suffix=".tmp", dir=d)
    try:
        with io.open(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def parse_when(s):
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc).timestamp()
        except ValueError:
            pass
    raise SystemExit("cannot parse time %r (use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ, UTC)" % s)


def git_time(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")


def main_run(args):
    db = os.path.abspath(args.db)
    root = args.root or subprocess.run(["git", "-C", db, "rev-parse", "--show-toplevel"],
                                       capture_output=True, text=True).stdout.strip()
    if not root:
        raise SystemExit("not a git repository: %s" % db)
    repo = GitRepo(root)
    try:
        head = repo.head()
        now = datetime.now(timezone.utc)
        gen_at = now.isoformat(timespec="seconds").replace("+00:00", "Z")
        until = now.timestamp()
        if args.range:
            commits = repo.commits([args.range])
            if not commits:
                raise SystemExit("empty range %s" % args.range)
            wins = [("range", commits[0]["ct"], commits[-1]["ct"])]
            accept_commits = repo.commits(["--since=" + git_time(commits[0]["ct"]), "HEAD", "--",
                                           CAND.rstrip("/")])
        else:
            if args.since:
                since = parse_when(args.since)
                until = parse_when(args.until) if args.until else until
                wins = [("custom", since, until)]
            else:
                wins = [("24h", until - 86400, until), ("7d", until - 7 * 86400, until)]
            lo = min(w[1] for w in wins)
            commits = [c for c in repo.commits(["--since=" + git_time(lo - 1), "--until=" +
                                                git_time(until + 1), "HEAD"])
                       if lo <= c["ct"] <= until]
            accept_commits = repo.commits(["--since=" + git_time(lo - 1), "HEAD", "--",
                                           CAND.rstrip("/")])
        events, notes, warnings = run(repo, db, commits, accept_commits)
        text = ["recent_changes.py v%s - generated %s - HEAD %s" % (TOOL_VERSION, gen_at, head),
                "Classes come from canonical events (EVENT_CLASS); commit size and line counts are never "
                "read. Knowledge and activity are separate axes."]
        for w in warnings:
            text.append("WARNING " + w)
        for label, s, u in wins:
            text += text_window(label, s, u, events, notes, commits, history_control(repo, head, s, u))
        lo = min(w[1] for w in wins)
        j = build_json(head, gen_at, {label: iso(s) for label, s, u in wins},
                       [e for e in events if e["ct"] >= lo])
        bad = validate_json(j)
        if bad:
            raise SystemExit("output contract violated: %s" % "; ".join(bad[:5]))
        out = "\n".join(text) + "\n"
        if args.json:
            write_atomic(args.json, json.dumps(j, indent=1, ensure_ascii=False) + "\n")
        if args.out:
            write_atomic(args.out, out)
        if not args.quiet:
            sys.stdout.buffer.write(out.encode("utf-8", "replace"))
        return 0
    finally:
        repo.close()


# ------------------------------------------------------------------ self-test
def _fixtures():
    """(name, FakeRepo blobs, commit, accept_index, expected class set)."""
    P, R = "p0", "r1"
    reg_hdr = "| id | question | answer |\n|---|---|---|\n"
    pg = DBP + "16-UI/some-page.md"
    fx = []

    def add(name, blobs, changes, expect, accept=None):
        fx.append((name, blobs, {"sha": R, "parent": P, "ct": 1000, "subject": "FABLE: " + name,
                                 "changes": changes}, accept or {}, set(expect)))
    add("register transition -> knowledge",
        {(P, REGISTER): reg_hdr + "| UQ-1 | q | **OPEN** |\n",
         (R, REGISTER): reg_hdr + "| UQ-1 | q | **ANSWERED 2026-10-02 (FABLE)** - x |\n"},
        [("M", REGISTER)], {K_NEW})
    add("register answered + page + index text -> knowledge only (covered)",
        {(P, REGISTER): reg_hdr + "| UQ-1 | q | **OPEN** |\n",
         (R, REGISTER): reg_hdr + "| UQ-1 | q | **ANSWERED 2026-10-02 (FABLE)** - x |\n",
         (P, pg): "# p\n", (R, pg): "# p\nmore\n"},
        [("M", REGISTER), ("M", pg), ("M", DBP + "_index/AUDIT-LOG.md")], {K_NEW})
    add("superseded with dated lead -> knowledge",
        {(P, REGISTER): reg_hdr + "| UQ-2 | q | **OPEN** |\n",
         (R, REGISTER): reg_hdr + "| UQ-2 | q | **SUPERSEDED 2026-10-02 (OPUS)** by UQ-9 |\n"},
        [("M", REGISTER)], {K_NEW})
    add("narrowed with dated lead -> knowledge",
        {(P, REGISTER): reg_hdr + "| UQ-3 | q | **OPEN** |\n",
         (R, REGISTER): reg_hdr + "| UQ-3 | q | **NARROWED 2026-10-02 (OPUS)** to x |\n"},
        [("M", REGISTER)], {K_NEW})
    add("answered without a date -> UNCLASSIFIED",
        {(P, REGISTER): reg_hdr + "| UQ-4 | q | **OPEN** |\n",
         (R, REGISTER): reg_hdr + "| UQ-4 | q | **ANSWERED** - x |\n"},
        [("M", REGISTER)], {UNCL})
    add("new open question registered -> UNCLASSIFIED",
        {(P, REGISTER): reg_hdr, (R, REGISTER): reg_hdr + "| UQ-5 | q | **OPEN** |\n"},
        [("M", REGISTER)], {UNCL})
    add("partly answered -> UNCLASSIFIED (no DATA row)",
        {(P, REGISTER): reg_hdr + "| UQ-6 | q | **OPEN** |\n",
         (R, REGISTER): reg_hdr + "| UQ-6 | q | **PARTLY ANSWERED 2026-10-02 (FABLE)** |\n"},
        [("M", REGISTER)], {UNCL})
    add("board-only -> workflow",
        {}, [("M", INBOX + "TEAM.json"), ("M", INBOX + "FABLE.md")], {A_WORK})
    add("workflow docs -> workflow", {}, [("M", WORKFLOWD + "START-HERE.md")], {A_WORK})
    add("generated-only -> bookkeeping",
        {}, [("M", DBP + "PROGRESS.md"), ("M", PROGRESSD + "snapshot.json"),
             ("M", PROGRESSD + "history.jsonl")], {A_GEN})
    add("tools-only -> tooling",
        {}, [("M", "Database/Tools/analysis-kit/gfz-scripts/x.py"),
             ("M", PROGRESSD + "progress_report.py")], {A_TOOL})
    rec = CAND + "fable-corr-x-1003/README.md"
    add("correction record -> corrected",
        {(R, rec): "# correction\nconsumer check: the page agrees.\n"
                   "- affected: `16-UI/some-page.md` UQ-7\n",
         (P, pg): "# p\nold\n", (R, pg): "# p\n~~old~~ **Corrected 2026-10-02 (FABLE):** new\n"},
        [("A", rec), ("M", pg)], {K_CORR})
    rec3 = CAND + "uq8-consumer-check.md"
    add("keywordless strike + table-shaped consumer record -> corrected",
        {(R, rec3): "# Affected-consumer check - UQ-8 (FABLE)\n| consumer | state |\n|---|---|\n"
                    "| `_index/OPEN-QUESTIONS.md` UQ-8 | revised-here |\n",
         (P, pg): "# p\n| f | returns [0, A) |\n",
         (R, pg): "# p\n| f | ~~returns [0, A)~~ returns A itself at the top |\n"},
        [("A", rec3), ("M", pg)], {K_CORR})
    add("correction-shaped record, nothing struck, page edit -> UNCLASSIFIED",
        {(R, rec): "# correction\nconsumer check: the page agrees.\n"
                   "- affected: `16-UI/some-page.md` UQ-7\n",
         (P, pg): "# p\nold\n", (R, pg): "# p\nold\nnew text\n"},
        [("A", rec), ("M", pg)], {UNCL})
    rec2 = CAND + "astra-returns-x-fable-1002/"
    add("affected record + control + new page section, no accepted result cited -> UNCLASSIFIED (N1)",
        {(R, rec2 + "README.md"): "# returns\naffected: `16-UI/some-page.md`\nconsumer agrees\n",
         (R, rec2 + "check.py"): "print(1)\n",
         (P, pg): "# p\nold\n", (R, pg): "# p\nold\n\n### New subsection (FABLE)\nx\n"},
        [("A", rec2 + "README.md"), ("A", rec2 + "check.py"), ("M", pg)], {UNCL})
    add("unknown path -> UNCLASSIFIED", {}, [("A", "Foo/bar.txt")], {UNCL})
    add("page-only edit -> UNCLASSIFIED",
        {(P, pg): "# p\n", (R, pg): "# p\nx\n"}, [("M", pg)], {UNCL})
    add("tools/work scratch -> UNCLASSIFIED", {}, [("A", "Database/Tools/work/FABLE/x.txt")], {UNCL})
    nr = CAND + "fable-x-cloudint-1002/"
    add("page section + new record, no accepted result cited -> UNCLASSIFIED (N1)",
        {(R, nr + "README.md"): "# interior citations\n", (R, nr + "rows.json"): "[]",
         (P, pg): "# p\n", (R, pg): "# p\n\n## Interior citations (FABLE)\n| a | b |\n"},
        [("A", nr + "README.md"), ("A", nr + "rows.json"), ("M", pg)], {UNCL})
    acc_rv = CAND + "auditspec-review-fable-x-1002/REVIEW.md"
    add("page section + record citing an ACCEPTed review -> knowledge (rule f, N1)",
        {(R, nr + "README.md"): "# consumed\nreviewed: [r](../auditspec-review-fable-x-1002/REVIEW.md)\n",
         (R, nr + "rows.json"): "[]", (R, acc_rv): "# review\n\n## Verdict: ACCEPT\n",
         (P, pg): "# p\n", (R, pg): "# p\n\n## Consumed (FABLE)\n| a | b |\n"},
        [("A", nr + "README.md"), ("A", nr + "rows.json"), ("M", pg)], {K_NEW})
    add("page section + record citing a REJECTed review -> UNCLASSIFIED (N1)",
        {(R, nr + "README.md"): "# consumed\nreviewed: [r](../auditspec-review-fable-x-1002/REVIEW.md)\n",
         (R, nr + "rows.json"): "[]", (R, acc_rv): "# review\n\n## Verdict: REJECT\n",
         (P, pg): "# p\n", (R, pg): "# p\n\n## Consumed (FABLE)\n| a | b |\n"},
        [("A", nr + "README.md"), ("A", nr + "rows.json"), ("M", pg)], {UNCL})
    add("record + section + a NEW strike on the page -> not rule f (N3, kills M5)",
        {(R, nr + "README.md"): "# x\nreviewed: [r](../auditspec-review-fable-x-1002/REVIEW.md)\n",
         (R, nr + "rows.json"): "[]", (R, acc_rv): "# review\n\n## Verdict: ACCEPT\n",
         (P, pg): "# p\nold claim\n", (R, pg): "# p\n~~old claim~~ new claim\n\n## Consumed (FABLE)\nx\n"},
        [("A", nr + "README.md"), ("A", nr + "rows.json"), ("M", pg)], {UNCL})
    add("record + page edit WITHOUT a new section -> not rule f (N3, kills M7)",
        {(R, nr + "README.md"): "# x\nreviewed: [r](../auditspec-review-fable-x-1002/REVIEW.md)\n",
         (R, nr + "rows.json"): "[]", (R, acc_rv): "# review\n\n## Verdict: ACCEPT\n",
         (P, pg): "# p\n", (R, pg): "# p\nmore text\n"},
        [("A", nr + "README.md"), ("A", nr + "rows.json"), ("M", pg)], {UNCL})
    add("first ACCEPT review of a candidate package -> knowledge at the review (N1)",
        {(R, acc_rv): "# review\nPackage: `_index/candidates/fable-x-cloudint-1002/`\n\n## Verdict: ACCEPT\n",
         (R, nr + "README.md"): "# interior citations\n"},
        [("A", acc_rv)], {K_NEW})
    ev = EVID + "sd-1/"
    rv = CAND + "auditspec-review-astra-sd-1-1003/REVIEW.md"
    add("accepting review of an evidence record -> evidence",
        {(R, ev + "README.md"): "x", (P, ev + "README.md"): "x",
         (R, rv): "# review\nPackage: `_experiments/evidence/sd-1/`\n\n## verdict: ACCEPT\n"},
        [("A", rv)], {K_EVID})
    add("repeat review of an already-accepted record -> workflow",
        {(R, ev + "README.md"): "x", (P, ev + "README.md"): "x",
         (P, CAND + "fable-review-sd-1/REVIEW.md"): "# r\nPacket: _experiments/evidence/sd-1/\n## Verdict: ACCEPT\n",
         (R, CAND + "fable-review-sd-1/REVIEW.md"): "# r\nPacket: _experiments/evidence/sd-1/\n## Verdict: ACCEPT\n",
         (R, rv): "# review\nPackage: `_experiments/evidence/sd-1/`\n\n## verdict: ACCEPT\n"},
        [("A", rv)], {A_WORK})
    add("REJECT review of a package -> workflow",
        {(R, rv): "# review\nPackage: `_experiments/evidence/sd-1/`\n\n## verdict: REJECT\n"},
        [("A", rv)], {A_WORK})
    add("new evidence record never reviewed -> UNCLASSIFIED",
        {(R, EVID + "new-2/README.md"): "x"}, [("A", EVID + "new-2/README.md")], {UNCL})
    add("new evidence record accepted later -> no event at the addition",
        {(R, EVID + "new-3/README.md"): "x"},
        [("A", EVID + "new-3/README.md"), ("A", EXPD + "EXP-300-x-exec.md")], set(),
        accept={"new-3": (2000, "later")})
    th = "type\tsize\tcategory\treadiness\n"
    add("type row promoted -> type/contract",
        {(P, TYPES + "types.tsv"): th + "Foo\t0x10\tc\tDISCOVERED\n",
         (R, TYPES + "types.tsv"): th + "Foo\t0x10\tc\tTYPE RESOLVED\n"},
        [("M", TYPES + "types.tsv")], {K_TYPE})
    add("type row evidence-text edit only -> UNCLASSIFIED",
        {(P, TYPES + "types.tsv"): th + "Foo\t0x10\tc\tTYPE RESOLVED\n",
         (R, TYPES + "types.tsv"): th + "Foo\t0x10\td\tTYPE RESOLVED\n"},
        [("M", TYPES + "types.tsv")], {UNCL})
    pk = PKGD + "PKG-GP-X.md"
    pkt = ("**stage.** `%s`\n\n| # | item | kind | locator | owner | reviewer | stage |\n"
           "|---|---|---|---|---|---|---|\n| Q1 | x | claim | p | FABLE | SEM | %s |\n")
    add("package accepted -> type/contract",
        {(P, pk): pkt % ("review", "review"), (R, pk): pkt % ("review", ACCEPTED_STAGE + ": ACCEPT")},
        [("M", pk)], {K_TYPE})
    add("package moved to review -> UNCLASSIFIED",
        {(P, pk): pkt % ("evidence-ready", "evidence-ready"), (R, pk): pkt % ("review", "review")},
        [("M", pk)], {UNCL})
    l2h = ("| system | contract | types | relationships | runtime | script_data | L2 | gap |\n"
           "|---|---|---|---|---|---|---|---|\n")
    add("L2 cell newly MET -> type/contract",
        {(P, L2): l2h + "| **S-1 Foo** | MET | MET | MET | NOT MET | N/A | NOT MET | x |\n",
         (R, L2): l2h + "| **S-1 Foo** | MET | MET | MET | MET | N/A | MET | - |\n"},
        [("M", L2)], {K_TYPE})
    ph = "# Parity\n| dimension | a |\n|---|---|\n"
    add("parity row change -> probe",
        {(P, PARITY): ph + "| **CALCULATION** | no |\n**0 of 45 pilots certified.**\n",
         (R, PARITY): ph + "| **CALCULATION** | **yes** |\n**0 of 45 pilots certified.**\n"},
        [("M", PARITY)], {K_PROBE})
    add("pilots certified moved -> parity evidence",
        {(P, PARITY): ph + "| **CALCULATION** | no |\n**0 of 45 pilots certified.**\n",
         (R, PARITY): ph + "| **CALCULATION** | no |\n**1 of 45 pilots certified.**\n"},
        [("M", PARITY)], {K_PARITY})
    return fx


def _run_fixtures(table, db, verbose):
    fails = 0
    all_events = []
    exercised = set()
    for name, blobs, c, acc, expect in _fixtures():
        repo = FakeRepo(blobs)
        ctx = {"db": db, "head_headers": {}, "table": table, "accept_index": acc}
        _CLS_CACHE.clear()
        evs, _ = classify_commit(repo, c, ctx)
        got = {e["class"] for e in evs}
        exercised.update(e["kind"] for e in evs)
        ok = got == expect
        fails += not ok
        for e in evs:
            e.update({"sha": c["sha"], "ct": c["ct"], "subject": c["subject"]})
        all_events += evs
        if verbose:
            print("  %s  %-66s %s" % ("PASS" if ok else "FAIL", name,
                                      "" if ok else "expected %s got %s (%s)" % (
                                          sorted(expect), sorted(got),
                                          [(e["kind"], e["detail"]) for e in evs])))
    return fails, all_events, exercised


def self_test(db):
    print("recent_changes.py --self-test")
    print("fixtures (live EVENT_CLASS):")
    fails, events, exercised = _run_fixtures(EVENT_CLASS, db, True)
    # JSON contract shape
    j = build_json("0" * 40, "2026-10-03T00:00:00Z", {"24h": "2026-10-02T00:00:00Z",
                                                     "7d": "2026-09-26T00:00:00Z"}, events)
    bad = validate_json(j)
    ok = not bad and len(j["events"]) == len(events) and len(events) > 0
    fails += not ok
    print("  %s  %-66s %s" % ("PASS" if ok else "FAIL", "JSON contract: keys, class list, axis = class",
                              "" if ok else bad[:3]))
    # N2: at most one rule-(f) event per commit, however many candidate records the commit adds
    P2, R2 = "p" * 40, "r" * 40
    pgn = DBP + "16-UI/some-page.md"
    rvn = CAND + "auditspec-review-fable-x-1002/REVIEW.md"
    blobs = {(R2, rvn): "# review\n\n## Verdict: ACCEPT\n", (P2, pgn): "# p\n",
             (R2, pgn): "# p\n\n## A (FABLE)\nx\n\n## B (FABLE)\ny\n"}
    chg = [("M", pgn)]
    for k in range(3):
        d = CAND + "fable-n2-%d-1003/" % k
        blobs[(R2, d + "README.md")] = "# r\nreviewed: [r](../auditspec-review-fable-x-1002/REVIEW.md)\n"
        blobs[(R2, d + "rows.json")] = "[]"
        chg += [("A", d + "README.md"), ("A", d + "rows.json")]
    _CLS_CACHE.clear()
    evs, _ = classify_commit(FakeRepo(blobs), {"sha": R2, "parent": P2, "ct": 1000, "subject": "FABLE: n2",
                                               "changes": chg},
                             {"db": db, "head_headers": {}, "table": EVENT_CLASS, "accept_index": {}})
    nf = sum(1 for e in evs if e["kind"] in ("page-section-record", "page-section-unreviewed"))
    ok = nf == 1
    fails += not ok
    print("  %s  %-66s %s" % ("PASS" if ok else "FAIL", "N2: three records + sections in one commit -> one rule-(f) event",
                              "" if ok else "got %d" % nf))
    broken = dict(j)
    broken["events"] = [dict(j["events"][0], axis="knowledge" if j["events"][0]["axis"] != "knowledge"
                             else "activity")]
    ok = bool(validate_json(broken))
    fails += not ok
    print("  %s  %-66s" % ("PASS" if ok else "FAIL", "JSON validator rejects an axis that does not match"))
    unexercised = sorted(set(EVENT_CLASS) - exercised)
    ok = not unexercised
    fails += not ok
    print("  %s  %-66s %s" % ("PASS" if ok else "FAIL", "every EVENT_CLASS entry is exercised by a fixture",
                              unexercised if unexercised else "(%d kinds)" % len(exercised)))
    # SENSITIVITY: swap two entries of the table; the fixtures must fail.
    print("sensitivity (swapped EVENT_CLASS entries must fail the fixtures):")
    sw = dict(EVENT_CLASS)
    sw["register-answered"], sw["board"] = sw["board"], sw["register-answered"]
    f2, _, _ = _run_fixtures(sw, db, False)
    ok = f2 > 0
    fails += not ok
    print("  %s  %-66s %d fixture(s) fail" % ("PASS" if ok else "FAIL",
                                              "swap register-answered <-> board", f2))
    kinds = sorted(EVENT_CLASS)
    pairs = [(a, b) for i, a in enumerate(kinds) for b in kinds[i + 1:] if EVENT_CLASS[a] != EVENT_CLASS[b]]
    missed = []
    for a, b in pairs:
        sw = dict(EVENT_CLASS)
        sw[a], sw[b] = sw[b], sw[a]
        if _run_fixtures(sw, db, False)[0] == 0:
            missed.append("%s<->%s" % (a, b))
    ok = not missed
    fails += not ok
    print("  %s  %-66s %s" % ("PASS" if ok else "FAIL",
                              "every swap of two differently-classed entries is caught",
                              "%d of %d caught%s" % (len(pairs) - len(missed), len(pairs),
                                                     (" missed: " + ", ".join(missed[:6])) if missed else "")))
    print("FAILS %d" % fails)
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    default_db = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA"))
    ap.add_argument("--db", default=default_db, help="database root (Database/FFXII TZA)")
    ap.add_argument("--root", help="repository root (default: the git toplevel of --db)")
    ap.add_argument("--since", help="custom window start, UTC (YYYY-MM-DD[THH:MM:SSZ])")
    ap.add_argument("--until", help="custom window end, UTC (default now)")
    ap.add_argument("--range", help="revision range A..B (one window)")
    ap.add_argument("--json", help="write the adapter JSON here (atomic)")
    ap.add_argument("--out", help="also write the text report here (atomic)")
    ap.add_argument("--quiet", action="store_true", help="do not print the text report")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test(os.path.abspath(args.db))
    return main_run(args)


if __name__ == "__main__":
    sys.exit(main())
