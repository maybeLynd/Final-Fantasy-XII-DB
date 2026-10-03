"""checkpoint_consistency.py - is this checkpoint's current state self-consistent? (OPUS, 2026-10-03)

The user's directive item 7: a checkpoint must never contain a derived surface that claims CURRENT while its
authoritative dependency has moved (the 2026-10-03 defect: L2-VERDICTS.md 48/52 beside PROGRESS.md 52/52 `CURRENT`).
An explicit STALE is legal; a silent green is not. Each check below compares a current surface with its authoritative
source IN THE SAME TREE and prints PASS / STALE (declared, legal) / FAIL:

  C1 derived bindings      every GENERATION-BINDING.json is CURRENT or declared STALE (derived_binding.py), never
                           FALSE-CURRENT or INCOHERENT
  C2 unbound CURRENT       no tracked derived surface says "**freshness:** `CURRENT`" without a binding beside it
  C3 L2 headline           PROGRESS.md's "N MET of M systems" equals the L2-VERDICTS.md rows of the same tree
  C4 L2 summary blocks     every hand-kept count table in L2-VERDICTS.md ("| contract column | systems |") equals a
                           recount of its rows - a summary that disagrees with its rows is a false current surface
  C5 goal gate             goal_gate.py's verdict and its `verdicts:` detail (count and denominator) equal the rows -
                           ALWAYS run in --rev / --worktree (2026-10-03 hardening: it used to need --slow)
  C6 knowledge mirror      (--worktree) knowledge_db.py check: CURRENT, or STALE reported (fail-closed by design)
  C7 lifecycle consumers   (--worktree) check_lifecycle_consumers.py FAILS 0
  C8 status residue        (--worktree) check_status_residue.py FAILS 0 / UNMAPPED 0

EXACT COMMIT (2026-10-03, the user's directive item 2). `--rev REV` used to return after C1-C4/C9, so an exact commit
was never checked for C5-C8 while the receipt read like a full checkpoint. Now `--rev REV` resolves REV to its SHA,
materializes that commit in a temporary DETACHED git worktree (only `Database/` populated; the shared worktree and its
index are never touched), links the untracked environment inputs the tools read (`Database/Tools/work`: the function
list, the dashboard store, knowledge.sqlite) read-only into it, and runs this checker in full worktree mode there with
the commit's OWN tools (C1-C9). The receipt names the SHA, the materialized tree and the environment inputs' as-of
fingerprints, and prints `COMMITTED SNAPSHOT CHECK: <sha> PASS|STALE|FAIL`. `--worktree` prints
`WORKTREE CHECK: <HEAD sha>+<dirty fingerprint> PASS|STALE|FAIL`. The old committed-only reading survives as
`--rev-partial REV`, labelled PARTIAL (C1-C4, C9): it is never a checkpoint validation.
Cleanup removes the junction first and verifies it is gone before the worktree is removed, so the shared Tools/work can
never be deleted through it; if that fails the temporary tree is left in place and named.

HARDENING (2026-10-03, the user's directive after the guard-repairs return):
  * COMPLETENESS - a full check (--rev, --worktree) must produce exactly C1-C9 (REQUIRED_FULL); a missing check is a
    FAIL and the result is labelled INCOMPLETE, never with the full-checkpoint label. --rev-partial has its own set.
  * C5 FAILS CLOSED - it reads goal_gate's JSON `verdict` AND its `verdicts:` detail line (the authority for the system
    count: `remaining` names only the FIRST unmet check). Unreadable JSON, an unknown verdict, a missing or unparseable
    verdicts line, a wrong count or denominator, or MET while rows hold NOT MET systems -> FAIL.
  * C9 BY LINEAGE - the policy is in force at every revision descended from its commit (git ancestry), not wherever its
    prose marker happens to appear: a descendant without the marker FAILs unless a versioned successor in
    C9_SUCCESSORS is in force. Only a revision that predates the policy commit passes as "not in force".
  * ISOLATED EXTERNAL SNAPSHOT - --rev no longer junctions live Tools/work directories. Only EXTERNAL_INPUTS (the files
    C5-C8 read) are copied into the temporary tree and hashed into the receipt; an undeclared input is simply absent,
    so a checker that needs one fails closed. The label says COMMIT + EXTERNAL SNAPSHOT <digest>, and a before/after
    fingerprint of the live sources proves validation did not modify them.

Usage: python checkpoint_consistency.py [--rev REV | --rev-partial REV | --worktree] [--refresh-mirror] [--json OUT]
(--slow is accepted and ignored: C5 always runs)
Exit 0 when nothing FAILs (STALE allowed), 1 otherwise. --self-test runs the fixtures."""
import collections
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CHECKPOINT_ROOT") or os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
REAL_ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DBREL = "Database/FFXII TZA"
sys.path.insert(0, HERE)
import derived_binding as B  # noqa: E402

FRESH_CURRENT = re.compile(r"\*\*freshness:\*\* `CURRENT`")
HEADLINE = re.compile(r"\*\*(\d+) MET of (\d+) systems\*\*")


# The runtime-exclusion amendment's durable identity (directive item 3): the commit that made it authoritative, the
# marker text that shows it is in force in a tree, and the explicit historical worklist it inherited (the 12 cells
# that excluded material before it existed). A cell leaves the worklist only by being re-read: citing the amendment
# or no longer excluding.
C9_POLICY = {
    "id": "L2-RUNTIME-EXCLUSION-AMENDMENT-1",
    "commit": "ed8a9c03da267369ef7024f358f5304e19ee821e",
    "marker": "an exclusion may not drop registry-subject material",
    "worklist": ["S-05", "S-06", "S-08", "S-11", "S-13", "S-22", "S-23", "S-26", "S-36", "S-37", "S-40", "S-42"],
}
C9_EXCL = re.compile(r"out of (the|this) (runtime )?denominator|outside the (L2 |runtime )?denominator|"
                     r"outside this contract's subject|out of this contract's runtime denominator|"
                     r"static-structure|ruled outside|unreachable from every disclosed|device-gated|"
                     r"not in the denominator|callee-depth|contract-excluded", re.I)


REQUIRED_FULL = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
REQUIRED_PARTIAL = ["C1", "C2", "C3", "C4", "C9"]
# Versioned successors of C9_POLICY (none yet). A successor needs its own id, commit and marker; it is in force at the
# revisions descended from its commit, and only then may C9_POLICY's marker be absent.
C9_SUCCESSORS = []
# The files C5-C8 read outside the commit, relative to Database/Tools/work. `{generation}` is the dashboard generation
# named by dashboard/CURRENT. Anything not listed is not materialized for an exact-commit check.
EXTERNAL_INPUTS = ["graph/functions.tsv", "graph/edges.tsv", "h78/rip_data_refs.tsv", "knowledge/knowledge.sqlite",
                   "verify_GFZ_PARENT/residual_addrs.txt", "dashboard/CURRENT",
                   "dashboard/{generation}/inputs/requirement_facts"]
VERDICTS_LINE = re.compile(r"^verdicts: (OK|UNMET) -- (.*)$")


def completeness(res, required):
    """Required checks that produced no result row."""
    have = {r["check"] for r in res}
    return [c for c in required if c not in have]


def c5_evaluate(output, rows_total, rows_notmet):
    """(status, detail) of goal_gate's JSON against the verdict rows; fails closed on anything unrecognized."""
    try:
        gg = json.loads(output[output.index("{"):])
    except Exception as e:
        return "FAIL", "goal_gate output is not readable JSON (%s)" % type(e).__name__
    verdict = gg.get("verdict")
    if verdict not in ("MET", "NOT_MET"):
        return "FAIL", "goal_gate verdict %r is neither MET nor NOT_MET" % (verdict,)
    lines = [m for d in (gg.get("detail") or []) if isinstance(d, str) for m in [VERDICTS_LINE.match(d)] if m]
    if len(lines) != 1:
        return "FAIL", "goal_gate detail has %d `verdicts:` lines (exactly 1 required)" % len(lines)
    state, text = lines[0].groups()
    if rows_notmet > 0:
        m = re.match(r"(\d+)/(\d+) systems NOT MET\b", text)
        if state != "UNMET" or not m:
            return "FAIL", "rows hold %d NOT MET but goal_gate's verdicts line reads %r" % (rows_notmet, lines[0].group(0))
        if (int(m.group(1)), int(m.group(2))) != (rows_notmet, rows_total):
            return "FAIL", "goal_gate counts %s/%s NOT MET, rows %d/%d" % (m.group(1), m.group(2), rows_notmet, rows_total)
        if verdict != "NOT_MET":
            return "FAIL", "goal_gate verdict MET while rows hold %d NOT MET systems" % rows_notmet
        return "PASS", "goal_gate NOT_MET; verdicts %s/%s NOT MET = rows %d/%d" % (m.group(1), m.group(2), rows_notmet,
                                                                                rows_total)
    m = re.match(r"all (\d+) registered systems verdict MET\b", text)
    if state != "OK" or not m or int(m.group(1)) != rows_total:
        return "FAIL", "rows hold 0 NOT MET of %d but goal_gate's verdicts line reads %r" % (rows_total, lines[0].group(0))
    others_ok = all(d.split(": ", 1)[1].startswith("OK") for d in gg["detail"] if ": " in d)
    if (verdict == "MET") != others_ok:
        return "FAIL", "goal_gate verdict %s disagrees with its own detail lines" % verdict
    return "PASS", "goal_gate %s; verdicts: all %d MET = rows" % (verdict, rows_total)


def c9_lineage(is_descendant, marker_present, successor_in_force):
    """'not-in-force' | 'evaluate' | 'successor' | 'fail-marker-removed'."""
    if not is_descendant:
        return "not-in-force"
    if marker_present:
        return "evaluate"
    return "successor" if successor_in_force else "fail-marker-removed"


def _is_ancestor(root, commit, rev="HEAD"):
    return subprocess.run(["git", "-C", root, "merge-base", "--is-ancestor", commit, rev],
                          capture_output=True).returncode == 0


def _sha256_file(f):
    import hashlib
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_external(work):
    """[(relative path, absolute source)] for EXTERNAL_INPUTS under `work`; raises if one is missing."""
    gen = None
    out = []
    for rel in EXTERNAL_INPUTS:
        if "{generation}" in rel:
            if gen is None:
                gen = json.loads(io.open(os.path.join(work, "dashboard", "CURRENT"), encoding="utf-8").read())["generation"]
            rel = rel.replace("{generation}", gen)
        src = os.path.join(work, *rel.split("/"))
        if not os.path.isfile(src):
            raise RuntimeError("declared external input missing: Database/Tools/work/" + rel)
        out.append((rel, src))
    return out


def materialize_external(pairs, dest_work):
    """Copy each declared input (content and mtime) under dest_work; -> receipt rows with sha256/size/mtime/source."""
    import shutil
    rows = []
    for rel, src in pairs:
        dst = os.path.join(dest_work, *rel.split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        rows.append({"input": "Database/Tools/work/" + rel, "sha256": _sha256_file(src), "bytes": os.path.getsize(src),
                     "mtime": int(os.path.getmtime(src)), "source": "live Tools/work, copied (not linked)"})
    return rows


def live_fingerprint(pairs):
    """(path, size, mtime_ns, sha256) of every live source: compared before/after a run."""
    return [(rel, os.path.getsize(src), os.stat(src).st_mtime_ns, _sha256_file(src)) for rel, src in pairs]


def runtime_cells(text):
    """{system id: runtime cell text} from the L2 verdict table rows."""
    out = {}
    for line in text.splitlines():
        m = re.match(r"^\| \*\*(S-\d+)\*\*", line)
        if m and line.count("|") >= 9:
            out[m.group(1)] = line.split("|")[5].strip()
    return out


def c9_classify(now, at_policy, worklist, verdict):
    """-> (late [(sid, why)], old [sid], cleared [sid]). `verdict` is progress_report._cell_verdict."""
    late, old = [], []
    for sid, cell in sorted(now.items()):
        if verdict(cell) not in ("MET", "LIVE") or not C9_EXCL.search(cell):
            continue
        if "exclusion may not drop" in cell or "exclusion amendment" in cell:
            continue
        if sid not in worklist:
            late.append((sid, "not on the policy worklist"))
        elif cell != at_policy.get(sid):
            late.append((sid, "re-scored since the policy commit without citing the amendment"))
        else:
            old.append(sid)
    cleared = sorted(set(worklist) - set(old) - {s for s, _w in late})
    return late, old, cleared


def _parse_verdicts(text):
    """The L2 table rows via progress_report.parse_verdicts (the generator's own parser, so C3 and C4 cannot disagree
    with the reporter about what a row says)."""
    sys.path.insert(0, os.path.join(ROOT, DBREL, "_index", "progress"))
    import progress_report as P
    import tempfile
    fd, p = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    try:
        io.open(p, "w", encoding="utf-8").write(text)
        from pathlib import Path
        return P.parse_verdicts(Path(p))
    finally:
        os.remove(p)


def summary_tables(text):
    """[(column, {verdict: count}, line_no)] for every '| <column> column | systems |' table in L2-VERDICTS.md."""
    out = []
    lines = text.splitlines()
    for i, l in enumerate(lines):
        m = re.match(r"^\|\s*(\w+) column\s*\|\s*systems\s*\|", l)
        if not m:
            continue
        counts = {}
        for row in lines[i + 2:]:
            if not row.startswith("|"):
                break
            cells = [c.strip() for c in row.strip("|").split("|")]
            if len(cells) < 2:
                continue
            verdict = re.sub(r"[*`]", "", cells[0]).strip()
            n = re.sub(r"[*`]", "", cells[1]).strip()
            if n.isdigit():
                counts[verdict] = int(n)
        out.append((m.group(1).lower(), counts, i + 1))
    return out


def run(rev=None, worktree=False, slow=False, refresh_mirror=False):
    res = []

    def add(cid, status, msg):
        res.append({"check": cid, "status": status, "detail": msg})

    read = B.worktree_reader(ROOT) if worktree else B.git_reader(ROOT, rev=rev or "HEAD")
    # C1
    paths = B.bindings_in(ROOT, rev=None if worktree else (rev or "HEAD"))
    if worktree:
        extra = subprocess.run(["git", "-C", ROOT, "ls-files", "--others", "--exclude-standard"], capture_output=True,
                               text=True).stdout.splitlines()
        paths = sorted(set(paths) | {p for p in extra if p.endswith("/" + B.NAME)})
    bound_dirs = set()
    for p in paths:
        data = read(p)
        if data is None:
            continue
        b = B.load(data)
        s = B.state(b, read)
        bound_dirs.add(os.path.dirname(p))
        st = {"CURRENT": "PASS", "STALE": "STALE"}.get(s["state"], "FAIL")
        add("C1", st, "%s %s%s%s" % (b["surface"], s["state"],
                                       (" moved: " + ", ".join(s["moved"])) if s["moved"] else "",
                                       (" outputs differ: " + ", ".join(s["outputs_bad"])) if s["outputs_bad"] else ""))
    if not paths:
        add("C1", "PASS", "no bindings in this tree")
    # C2
    if worktree:
        g = subprocess.run(["git", "-C", ROOT, "grep", "-l", "-E", r"\*\*freshness:\*\* `CURRENT`", "--", DBREL],
                           capture_output=True, text=True)
    else:
        g = subprocess.run(["git", "-C", ROOT, "grep", "-l", "-E", r"\*\*freshness:\*\* `CURRENT`", rev or "HEAD", "--",
                            DBREL], capture_output=True, text=True)
    unbound = []
    for line in g.stdout.splitlines():
        f = line.split(":", 1)[1] if (not worktree and ":" in line) else line
        d = os.path.dirname(f)
        covered = any(f == o or d == bd for bd in bound_dirs for o in [f])
        # a binding covers the files it names as outputs
        if not covered:
            for p in paths:
                data = read(p)
                if data and f in B.load(data)["outputs"]:
                    covered = True
        if not covered:
            unbound.append(f)
    add("C2", "FAIL" if unbound else "PASS",
        ("claims CURRENT with no binding: " + ", ".join(unbound)) if unbound else "every CURRENT claim is bound")
    # C3 / C4
    l2 = read(DBREL + "/_index/L2-VERDICTS.md")
    prog = read(DBREL + "/PROGRESS.md")
    rows = _parse_verdicts(l2.decode("utf-8")) if l2 else []
    met = sum(1 for r in rows if r["l2"] == "MET")
    if prog is not None and rows:
        ptxt = prog.decode("utf-8")
        m = HEADLINE.search(ptxt)
        stale = "`STALE`" in ptxt.split("\n", 6)[3] if ptxt.count("\n") > 3 else False
        if not m:
            add("C3", "FAIL", "PROGRESS.md has no 'N MET of M systems' headline")
        elif (int(m.group(1)), int(m.group(2))) == (met, len(rows)):
            add("C3", "PASS", "PROGRESS.md %s/%s = L2-VERDICTS rows %d/%d" % (m.group(1), m.group(2), met, len(rows)))
        else:
            add("C3", "STALE" if stale else "FAIL",
                "PROGRESS.md says %s MET of %s, the rows say %d of %d%s" % (
                    m.group(1), m.group(2), met, len(rows), " (labelled STALE)" if stale else " while labelled CURRENT"))
    if l2:
        text = l2.decode("utf-8")
        if not any(col in ("contract", "types", "relationships", "runtime", "l2") for col, _c, _l in summary_tables(text)):
            add("C4", "PASS", "L2-VERDICTS.md carries no hand-kept count table (retired 2026-10-03); nothing to recount")
        for col, counts, ln in summary_tables(text):
            if col not in ("contract", "types", "relationships", "runtime", "l2"):
                continue
            real = collections.Counter(r[col] for r in rows)
            bad = {k: (v, real.get(k, 0)) for k, v in counts.items() if real.get(k, 0) != v}
            add("C4", "FAIL" if bad else "PASS",
                ("L2-VERDICTS.md line %d '%s column' summary disagrees with its rows: %s" % (
                    ln, col, ", ".join("%s says %d, rows %d" % (k, a, b2) for k, (a, b2) in sorted(bad.items()))))
                if bad else "L2-VERDICTS.md line %d '%s column' summary equals its rows" % (ln, col))
    # C9 runtime exclusions are visible (L2-VERDICTS "Amendment — an exclusion may not drop registry-subject material").
    # 2026-10-03 (the user's directive item 3): the policy is ordered by its COMMIT, not by a calendar date. The
    # first version called a cell "old" when its newest date was not after 2026-10-03, so a cell re-scored later the
    # same day passed as historical. Now: a runtime cell that excludes material without citing the amendment is
    # tolerated (STALE, worklist) only if it is on the policy's explicit worklist AND its text is byte-identical to its
    # text at the policy commit; anything else - a new exclusion, a worklist cell re-scored since, a cell not on the
    # worklist - FAILs, whatever date it carries.
    if l2:
        sys.path.insert(0, os.path.join(ROOT, DBREL, "_index", "progress"))
        import progress_report as P
        cells_now = runtime_cells(l2.decode("utf-8"))
        at_policy = subprocess.run(["git", "-C", ROOT, "show", "%s:%s/_index/L2-VERDICTS.md" % (C9_POLICY["commit"], DBREL)],
                                   capture_output=True)
        lineage = c9_lineage(_is_ancestor(ROOT, C9_POLICY["commit"]), C9_POLICY["marker"] in l2.decode("utf-8"),
                             any(_is_ancestor(ROOT, x["commit"]) and x["marker"] in l2.decode("utf-8")
                                 for x in C9_SUCCESSORS))
        if lineage == "not-in-force":
            add("C9", "PASS", "this revision predates the policy commit %s (%s): not yet in force"
                % (C9_POLICY["commit"][:12], C9_POLICY["id"]))
        elif lineage == "fail-marker-removed":
            add("C9", "FAIL", "this revision descends from the policy commit %s but L2-VERDICTS.md no longer carries its "
                "marker and no versioned successor is in force: removing the marker does not disable %s"
                % (C9_POLICY["commit"][:12], C9_POLICY["id"]))
        elif lineage == "successor":
            add("C9", "STALE", "a versioned successor of %s is in force; its evaluation is not implemented here yet"
                % C9_POLICY["id"])
        elif at_policy.returncode != 0:
            add("C9", "FAIL", "policy commit %s unreadable: C9 cannot order cells against it" % C9_POLICY["commit"][:12])
        else:
            late, old, cleared = c9_classify(cells_now, runtime_cells(at_policy.stdout.decode("utf-8")),
                                             C9_POLICY["worklist"], P._cell_verdict)
            pol = "%s @ %s" % (C9_POLICY["id"], C9_POLICY["commit"][:12])
            if late:
                add("C9", "FAIL", "runtime cells exclude material without citing the amendment and are not the "
                    "unchanged historical worklist (%s): %s" % (pol, "; ".join("%s (%s)" % x for x in late)))
            elif old:
                add("C9", "STALE", "historical worklist (%s), unchanged since the policy commit, to be re-read against "
                    "the registry subject: %s%s" % (pol, ", ".join(old),
                                                     (" (cleared: %s)" % ", ".join(cleared)) if cleared else ""))
            else:
                add("C9", "PASS", "no runtime cell excludes material without citing the amendment (%s)" % pol)
    if not worktree:
        return res
    gfz = os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts")   # the checked tree's own tools

    def tool(args, timeout=900):
        r = subprocess.run([sys.executable, "-B"] + args, cwd=gfz, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr)
    # C5 - always (no --slow), fail-closed (c5_evaluate)
    if not rows:
        add("C5", "FAIL", "no verdict rows to compare goal_gate with")
    else:
        rc, out = tool(["goal_gate.py", "--json"])
        st, msg = c5_evaluate(out, len(rows), len(rows) - met)
        add("C5", st, msg)
    # C6 (with --refresh-mirror a STALE mirror is rebuilt through knowledge_db's own guarded build first: a checkpoint
    # refreshes the mirror instead of carrying a stale one forward; no second freshness system)
    rc, out = tool(["knowledge_db.py", "check"])
    if "STALE" in out and refresh_mirror:
        brc, bout = tool(["knowledge_db.py", "build"], timeout=1800)
        add("C6", "PASS" if brc == 0 else "FAIL", "knowledge.sqlite was STALE; rebuilt through the guarded build: %s" % (
            (bout.strip().splitlines() or ["no output"])[-1][:200]))
        rc, out = tool(["knowledge_db.py", "check"])
    if "STALE" in out:
        add("C6", "STALE", "knowledge.sqlite STALE (fails closed): " + "; ".join(
            l.strip() for l in out.splitlines() if "STALE" in l)[:300])
    elif rc == 0:
        add("C6", "PASS", "knowledge.sqlite CURRENT")
    else:
        add("C6", "FAIL", "knowledge_db check exit %d: %s" % (rc, out.strip()[-200:]))
    # C7 / C8
    for cid, script in (("C7", "check_lifecycle_consumers.py"), ("C8", "check_status_residue.py")):
        rc, out = tool([script])
        fails = re.search(r"FAILS (\d+)", out)
        good = rc == 0 and fails is not None and fails.group(1) == "0"
        add(cid, "PASS" if good else "FAIL", "%s: %s" % (script, (out.strip().splitlines() or ["no output"])[-1][:160]))
    return res


def worktree_identity(root=None):
    """HEAD sha + a fingerprint of the uncommitted state (tracked diff and untracked file list) of the worktree."""
    import hashlib
    root = root or ROOT
    head = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    d = subprocess.run(["git", "-C", root, "diff", "HEAD", "--", DBREL], capture_output=True).stdout
    u = subprocess.run(["git", "-C", root, "ls-files", "--others", "--exclude-standard", "--", DBREL],
                       capture_output=True).stdout
    return head, hashlib.sha256(d + b"\0" + u).hexdigest()[:16], bool(d.strip() or u.strip())


def _env_inputs(work):
    """As-of fingerprints of the untracked environment inputs a snapshot borrows from the real tree."""
    import hashlib
    out = {}
    for rel in ("graph/functions.tsv", "knowledge/knowledge.sqlite"):
        f = os.path.join(work, *rel.split("/"))
        if os.path.isfile(f):
            h = hashlib.sha256()
            with open(f, "rb") as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b""):
                    h.update(chunk)
            out[rel] = {"sha256": h.hexdigest(), "bytes": os.path.getsize(f), "mtime": int(os.path.getmtime(f))}
        else:
            out[rel] = None
    return out


def snapshot(rev, slow=True):
    """Run the full checker (C1-C9) against the exact commit `rev` in a temporary detached worktree.
    -> (sha, results, receipt dict)."""
    import tempfile
    sha = subprocess.run(["git", "-C", REAL_ROOT, "rev-parse", "--verify", rev + "^{commit}"], capture_output=True,
                         text=True).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        return rev, [{"check": "C0", "status": "FAIL", "detail": "cannot resolve %r to a commit" % rev}], {}
    # a short root: the deepest evidence paths overflow MAX_PATH under %TEMP% (first run: "Filename too long")
    base = os.environ.get("CHECKPOINT_TMP", "C:\\ck")
    os.makedirs(base, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix=sha[:7] + "-", dir=base)
    tree = os.path.join(tmp, "t")
    work_real = os.path.join(REAL_ROOT, "Database", "Tools", "work")
    work_tree = os.path.join(tree, "Database", "Tools", "work")
    res, receipt, links = [], {"commit": sha, "materialized": tree}, []
    try:
        r = subprocess.run(["git", "-c", "core.longpaths=true", "-C", REAL_ROOT, "worktree", "add", "--no-checkout",
                            "--detach", tree, sha],
                           capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError("git worktree add: " + r.stderr.strip()[-300:])
        # Database/ plus every root-level FILE of the commit: the lifecycle check (C7) reads RECONSTRUCTION-CHARTER.md
        # at the repository root (first full run: C7 FAILed only because the snapshot lacked it - a missing input
        # fails closed, never passes silently)
        top = subprocess.run(["git", "-C", REAL_ROOT, "ls-tree", sha], capture_output=True, text=True).stdout
        root_files = [l.split("\t", 1)[1] for l in top.splitlines() if l.split()[1:2] == ["blob"]]
        r = subprocess.run(["git", "-c", "core.longpaths=true", "-C", tree, "checkout", sha, "--", "Database"]
                           + root_files, capture_output=True, text=True)
        receipt["populated"] = ["Database/"] + root_files
        if r.returncode:
            raise RuntimeError("git checkout Database: " + r.stderr.strip()[-300:])
        got = subprocess.run(["git", "-C", tree, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        if got != sha:
            raise RuntimeError("materialized HEAD %s is not %s" % (got, sha))
        # ISOLATED EXTERNAL SNAPSHOT (2026-10-03 hardening): only the declared EXTERNAL_INPUTS are COPIED into the
        # temporary tree and hashed; nothing is linked, so the run cannot reach or modify the live Tools/work, and a
        # checker that needs an undeclared input finds it absent and fails closed.
        pairs = resolve_external(work_real)
        before = live_fingerprint(pairs)
        receipt["external_inputs"] = materialize_external(pairs, work_tree)
        import hashlib
        receipt["external_snapshot_digest"] = hashlib.sha256(
            "\n".join("%s %s" % (x["input"], x["sha256"]) for x in receipt["external_inputs"]).encode()).hexdigest()
        out = os.path.join(tmp, "result.json")
        env = dict(os.environ, CHECKPOINT_ROOT=tree)
        args = [sys.executable, "-B", os.path.abspath(__file__), "--worktree", "--json", out]
        r = subprocess.run(args, cwd=os.path.join(tree, "Database", "Tools", "analysis-kit", "gfz-scripts"),
                           capture_output=True, text=True, env=env, timeout=7200)
        res = json.load(io.open(out, encoding="utf-8")) if os.path.isfile(out) else [
            {"check": "C0", "status": "FAIL", "detail": "the snapshot run wrote no result: " + (r.stdout + r.stderr)[-300:]}]
        receipt["checker"] = os.path.abspath(__file__)
        after = live_fingerprint(pairs)
        receipt["live_inputs_unchanged"] = before == after
        if before != after:
            # The run read only the COPIES hashed in the receipt (nothing is linked, and the self-test proves a write to
            # a copy cannot reach its original), so a change here is a concurrent writer on the live tree - e.g. the
            # supervised dashboard regenerating CURRENT. The result stays reproducible from the receipt; it is declared
            # STALE against the live source, naming what moved, never silently clean.
            res.append({"check": "C0", "status": "STALE",
                        "detail": "live external input(s) moved during the run (concurrent writer; this result used the "
                                  "copies hashed in the receipt): %s"
                                  % ", ".join(b[0] for b, a in zip(before, after) if b != a)})
    except Exception as e:
        res = res or [{"check": "C0", "status": "FAIL", "detail": "snapshot materialization failed: %s" % e}]
    finally:
        cleaned = not links                    # no junctions are created any more; kept as a fail-safe
        if cleaned:
            subprocess.run(["git", "-C", REAL_ROOT, "worktree", "remove", "--force", tree], capture_output=True)
            subprocess.run(["git", "-C", REAL_ROOT, "worktree", "prune"], capture_output=True)
            try:
                import shutil
                shutil.rmtree(tmp, ignore_errors=True)
            except Exception:
                pass
        else:
            res.append({"check": "C0", "status": "FAIL",
                        "detail": "cleanup refused: a Tools/work junction is still in %s; remove it by hand (rmdir), "
                                  "then git worktree remove" % tree})
        receipt["cleaned"] = cleaned
    return sha, res, receipt


def _self_test():
    fails = []

    def ok(c, w):
        print(("ok   " if c else "FAIL ") + w)
        if not c:
            fails.append(w)
    t = ("| contract column | systems | which |\n|---|---:|---|\n| MET | **47** | x |\n| SCOPE-SHORT | **3** | y |\n"
         "\ntext\n")
    s = summary_tables(t)
    ok(s == [("contract", {"MET": 47, "SCOPE-SHORT": 3}, 1)], "summary table parsed: %s" % s)
    ok(HEADLINE.search("| **48 MET of 52 systems**; x").groups() == ("48", "52"), "PROGRESS headline parsed")
    ok(FRESH_CURRENT.search("· **freshness:** `CURRENT` (fp `x`)") is not None, "CURRENT claim detected")
    ok(FRESH_CURRENT.search("· **freshness:** `STALE` (bound inputs moved") is None, "STALE label is not a CURRENT claim")
    # C9 policy ordering by commit identity, not by date (directive item 3)
    v = lambda c: "MET" if c.startswith("MET") else "NOT MET"
    pol = {"S-05": "MET - device-gated exclusion, scored 2026-10-02", "S-06": "MET - plain"}
    same = dict(pol)
    late, old, cl = c9_classify(same, pol, ["S-05"], v)
    ok(not late and old == ["S-05"], "C9 unchanged worklist cell -> STALE worklist, not FAIL")
    resc = dict(pol, **{"S-05": "MET - device-gated exclusion, re-scored 2026-10-03"})
    late, old, cl = c9_classify(resc, pol, ["S-05"], v)
    ok([x[0] for x in late] == ["S-05"], "C9 SAME-DAY re-score of a worklist cell without the citation -> FAIL "
                                         "(the date-ordered rule called it old)")
    new = dict(pol, **{"S-06": "MET - ruled outside the subject, 2026-10-03"})
    late, old, cl = c9_classify(new, pol, ["S-05"], v)
    ok([x[0] for x in late] == ["S-06"], "C9 a new exclusion on a non-worklist cell, dated the policy day -> FAIL")
    cited = dict(pol, **{"S-05": "MET - device-gated; meets the exclusion amendment (cites it)"})
    late, old, cl = c9_classify(cited, pol, ["S-05"], v)
    ok(not late and not old and cl == ["S-05"], "C9 a re-read cell citing the amendment clears the worklist")
    # completeness (hardening item 1)
    full = [{"check": c, "status": "PASS", "detail": ""} for c in REQUIRED_FULL]
    ok(completeness(full, REQUIRED_FULL) == [], "full C1-C9 result set is complete")
    ok(completeness([r for r in full if r["check"] != "C5"], REQUIRED_FULL) == ["C5"],
       "a result set without C5 is incomplete (named C5)")
    ok(completeness([r for r in full if r["check"] in REQUIRED_PARTIAL], REQUIRED_PARTIAL) == [],
       "the partial set is complete only against the partial requirement")
    # C5 fails closed (hardening item 2): mutations of a real goal_gate --json shape
    def gg(verdict="NOT_MET", vline="verdicts: UNMET -- 25/52 systems NOT MET (first: S-01)", extra=None, raw=None):
        if raw is not None:
            return raw
        d = {"verdict": verdict, "remaining": "25/52 systems NOT MET (first: S-01)", "next": "x",
             "detail": ["scope: OK -- sealed", "provenance: OK -- ok"] + ([vline] if vline else []) + (extra or [])}
        return json.dumps(d)
    ok(c5_evaluate(gg(), 52, 25)[0] == "PASS", "C5 correct control -> PASS")
    ok(c5_evaluate(gg(vline="verdicts: UNMET -- 24/52 systems NOT MET (first: S-01)"), 52, 25)[0] == "FAIL",
       "C5 wrong count -> FAIL")
    ok(c5_evaluate(gg(vline="verdicts: UNMET -- 25/51 systems NOT MET (first: S-01)"), 52, 25)[0] == "FAIL",
       "C5 wrong denominator -> FAIL")
    ok(c5_evaluate(gg(verdict="MET"), 52, 25)[0] == "FAIL", "C5 MET while rows hold NOT MET -> FAIL")
    ok(c5_evaluate(gg(vline="verdicts: UNMET -- some systems are not met"), 52, 25)[0] == "FAIL",
       "C5 NOT_MET with an unparseable count -> FAIL")
    ok(c5_evaluate(gg(vline=None), 52, 25)[0] == "FAIL", "C5 missing verdicts line -> FAIL (was: nm is None -> PASS)")
    ok(c5_evaluate(gg(raw='{"verdict": "NOT_MET", "remaining": '), 52, 25)[0] == "FAIL", "C5 malformed JSON -> FAIL")
    ok(c5_evaluate(gg(raw="no json at all"), 52, 25)[0] == "FAIL", "C5 no JSON -> FAIL")
    ok(c5_evaluate(gg(verdict="MAYBE"), 52, 25)[0] == "FAIL", "C5 unknown verdict -> FAIL")
    ok(c5_evaluate(gg(verdict="NOT_MET", vline="verdicts: OK -- all 52 registered systems verdict MET",
                      extra=["questions: UNMET -- 3 open"]), 52, 0)[0] == "PASS",
       "C5 zero NOT MET rows: verdicts OK, gate NOT_MET for another check -> PASS (explicitly evaluated)")
    ok(c5_evaluate(gg(verdict="NOT_MET", vline="verdicts: OK -- all 52 registered systems verdict MET"), 52, 0)[0]
       == "FAIL", "C5 zero NOT MET rows: NOT_MET although every detail line is OK -> FAIL")
    ok(c5_evaluate(gg(verdict="MET", vline="verdicts: OK -- all 51 registered systems verdict MET"), 52, 0)[0]
       == "FAIL", "C5 zero NOT MET rows: wrong denominator in the OK line -> FAIL")
    # C9 lineage (hardening item 3)
    ok(c9_lineage(False, False, False) == "not-in-force", "C9 before the policy commit, no marker -> not in force")
    ok(c9_lineage(True, False, False) == "fail-marker-removed",
       "C9 descendant of the policy commit with the marker removed -> FAIL (was: PASS 'not in force')")
    ok(c9_lineage(True, True, False) == "evaluate", "C9 descendant with the marker -> evaluated")
    ok(c9_lineage(True, False, True) == "successor", "C9 marker gone but a versioned successor in force -> successor")
    # isolated external snapshot (hardening item 4): copies, not links; the original cannot change through the copy
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        live = os.path.join(d, "live")
        os.makedirs(os.path.join(live, "graph"))
        os.makedirs(os.path.join(live, "undeclared"))
        io.open(os.path.join(live, "graph", "functions.tsv"), "w").write("a\n")
        io.open(os.path.join(live, "undeclared", "x.txt"), "w").write("secret\n")
        pairs = [("graph/functions.tsv", os.path.join(live, "graph", "functions.tsv"))]
        before = live_fingerprint(pairs)
        dest = os.path.join(d, "tree")
        rows_ = materialize_external(pairs, dest)
        io.open(os.path.join(dest, "graph", "functions.tsv"), "w").write("MUTATED\n")
        ok(live_fingerprint(pairs) == before, "a run that rewrites its copied input leaves the live original unchanged")
        ok(not os.path.exists(os.path.join(dest, "undeclared")), "an undeclared input is not materialized")
        ok(not os.path.islink(os.path.join(dest, "graph")) and rows_[0]["sha256"] == before[0][3],
           "inputs are copied (no link) and the receipt hash is the source's")
    print("self-test: %d failure(s)" % len(fails))
    return 1 if fails else 0


def main(argv):
    if "--self-test" in argv:
        return _self_test()
    receipt = {}
    required = REQUIRED_FULL
    if "--rev" in argv:
        sha, res, receipt = snapshot(argv[argv.index("--rev") + 1])
        label = "COMMITTED SNAPSHOT CHECK: %s + EXTERNAL SNAPSHOT %s" % (
            sha, (receipt.get("external_snapshot_digest") or "none")[:16])
    elif "--rev-partial" in argv:
        rev = argv[argv.index("--rev-partial") + 1]
        res = run(rev=rev)
        required = REQUIRED_PARTIAL
        label = "PARTIAL COMMITTED CHECK (C1-C4, C9 only - not a checkpoint validation): %s" % rev
    elif "--worktree" in argv:
        res = run(worktree=True, slow=True, refresh_mirror="--refresh-mirror" in argv)
        head, fp, dirty = worktree_identity()
        receipt = {"head": head, "dirty_fingerprint": fp, "dirty": dirty, "root": ROOT}
        label = "WORKTREE CHECK: %s+%s%s" % (head, fp, " (uncommitted changes)" if dirty else " (clean)")
    else:
        print("usage: --rev REV | --rev-partial REV | --worktree")
        return 2
    missing = completeness(res, required)
    if missing:
        res = res + [{"check": "C0", "status": "FAIL",
                      "detail": "required checks produced no result: %s - not a %s validation" % (
                          ", ".join(missing), "full" if required is REQUIRED_FULL else "partial")}]
        label = "INCOMPLETE (missing %s) - %s" % (",".join(missing), label)
    for r in res:
        print("%-5s %-3s %s" % (r["status"], r["check"], r["detail"]))
    n = collections.Counter(r["status"] for r in res)
    verdict = "FAIL" if n["FAIL"] else "STALE" if n["STALE"] else "PASS"
    checks = sorted({r["check"] for r in res})
    print("%s %s (PASS %d, STALE %d, FAIL %d; checks %s)" % (label, verdict, n["PASS"], n["STALE"], n["FAIL"],
                                                           ",".join(checks)))
    if "--json" in argv:
        out = res if "CHECKPOINT_ROOT" in os.environ else {"label": label, "verdict": verdict, "receipt": receipt,
                                                          "checks": checks, "required": required,
                                                          "checks_equal_required": sorted(set(checks) - {"C0"}) == sorted(required),
                                                          "results": res}
        json.dump(out, io.open(argv[argv.index("--json") + 1], "w", encoding="utf-8"), indent=1)
    return 1 if n["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
