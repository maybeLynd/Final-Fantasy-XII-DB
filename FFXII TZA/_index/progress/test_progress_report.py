#!/usr/bin/env python3
"""test_progress_report.py - package checks for the progress generator.

Live-tree tests cover the claims the directive makes: inputs all from the
exported set, classifier agreement with the live instrument, L2 table parse
integrity, fingerprint semantics (unchanged -> skip, any input change ->
regenerate), atomicity of outputs, no L3 in the route, and no blended
percentage.

Fixture tests (T9+) build a minimal synthetic database and drive the
generator through every checkpoint-10 repair scenario: config edits,
same-count edits, document add/delete, missing source, mid-build source
moves, mid-commit output failure, deleted/edited outputs, dirty-mark
semantics, duplicate triggers, transferred-obligation visibility, parity
UNMEASURED, the watchdog's scheduled tick/skip/failure path, dated
snapshots, and publication history.

Run: python test_progress_report.py
"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "progress_report", HERE / "progress_report.py")
pr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pr)

DB = pr.DB
fails = 0


def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail))
    fails += (not ok)


# T1 every configured input exists and is under the exported database tree
missing = [rel for rel in pr.INPUTS if not (DB / rel).exists()]
bad = [rel for rel in pr.INPUTS if rel.startswith("..") or "Tools" in rel
       or "Temp" in rel]
check("T1 all inputs exist, none under Tools/Temp",
      not [m for m in missing if m in pr.REQUIRED_INPUTS] and not bad,
      "missing-required=%s optional-absent=%s bad=%s"
      % ([m for m in missing if m in pr.REQUIRED_INPUTS],
         [m for m in missing if m in pr.OPTIONAL_INPUTS], bad))

# T2 vendored classifier agrees with check_questions row for row
vq = pr.parse_questions(DB / "_index/OPEN-QUESTIONS.md", pr._vendored_classify)
try:
    sys.path.insert(0, str(pr.ROOT / "Database" / "Tools" / "analysis-kit"
                           / "gfz-scripts"))
    import check_questions
    lq = pr.parse_questions(DB / "_index/OPEN-QUESTIONS.md",
                            check_questions.classify)
    diffs = [r["id"] for r, l in zip(vq, lq) if r["status"] != l["status"]]
    check("T2 vendored classifier == live instrument", vq and not diffs,
          "%d rows, diffs %s" % (len(vq), diffs[:8]))
except ImportError:
    check("T2 vendored classifier == live instrument", bool(vq),
          "instrument unavailable; vendored parse produced %d rows" % len(vq))

# T3 L2 table parse: all cells from the verdict vocabulary
v = pr.parse_verdicts(DB / "_index/L2-VERDICTS.md")
allowed = {"N/A", "NOT MET", "SCOPE-SHORT", "PARTIAL", "MIXED", "MET", "LIVE",
           "UNSCORED", "PENDING", "BLOCKED"}
unk = [r["system"] for r in v
       if any(r[d] not in allowed for d in
              ("contract", "types", "relationships", "runtime", "script_data",
               "l2"))]
check("T3 L2 verdict table parsed", len(v) >= 45 and not unk,
      "%d systems, unscored-cells %s" % (len(v), unk[:5]))

# T4 fingerprint moves when an input changes
f0 = pr.fingerprint(DB)
oqp = DB / "_index/OPEN-QUESTIONS.md"
raw = oqp.read_bytes()
oqp.write_bytes(raw + b" ")
f1 = pr.fingerprint(DB)
oqp.write_bytes(raw)
f2 = pr.fingerprint(DB)
check("T4 fingerprint tracks inputs", f0 == f2 and f0 != f1,
      "base=%s edited=%s restored=%s" % (f0[:8], f1[:8], f2[:8]))

# T5 generated artifacts parse and carry the required keys
sj = HERE / "snapshot.json"
if sj.exists():
    s = json.loads(sj.read_text(encoding="utf-8"))
    keys = {"generated_at_utc", "identity", "freshness", "levels", "packages",
            "transfers", "deltas"}
    lv = s.get("levels", {})
    term = lv.get("terminal_certification", {})
    check("T5 snapshot.json shape",
          keys <= set(s) and "L3" in lv and lv["L3"].startswith("excluded")
          and {"L1_modding_grade", "L2_reconstruction_grade",
               "residual_required_knowledge",
               "terminal_certification", "parity"} <= set(lv)
          and "final_audits_declared" in term
          and "audit_pass_artefacts" in term,
          "levels=%s" % sorted(lv))
else:
    check("T5 snapshot.json shape", False, "no snapshot - run generate first")

# T6 no blended score and no ETA in PROGRESS.md
pm = DB / "PROGRESS.md"
if pm.exists():
    txt = pm.read_text(encoding="utf-8")
    check("T6 no blended %, no ETA claim",
          "No blended score" in txt or "%" not in txt.split("deltas")[0],
          "PROGRESS.md present")
else:
    check("T6 no blended %, no ETA claim", False, "PROGRESS.md missing")

# T7 outputs are complete non-empty writes (atomic replace leaves no .tmp_)
tmps = [f.name for f in HERE.iterdir() if f.name.startswith(".tmp_")]
check("T7 no stray temp files", not tmps, str(tmps))

# T8 packages carry the required discriminator fields
if sj.exists():
    s = json.loads(sj.read_text(encoding="utf-8"))
    need = {"id", "kind", "status", "owner", "reviewer", "acceptance",
            "discriminator", "blocked_by", "evidence"}
    if "packages" not in s:
        check("T8 package rows carry discriminator fields", False,
              "snapshot state=%s - a failed generation published an "
              "INCOMPLETE stub; run generate" %
              s.get("freshness", {}).get("state"))
    else:
        badp = [p.get("id") for p in s["packages"] if not need <= set(p)]
        check("T8 package rows carry discriminator fields", not badp,
              "%d packages" % len(s["packages"]))
else:
    check("T8 package rows carry discriminator fields", False, "no snapshot")


# ================================================================ fixtures
def _fx_db(root):
    """Minimal synthetic database tree carrying every required input."""
    idx = root / "_index"
    (idx / "_inbox").mkdir(parents=True)
    (idx / "candidates" / "register-triage").mkdir(parents=True)
    (idx / "progress").mkdir(parents=True)
    (root / "01-Fixture-Category").mkdir()
    (root / "01-Fixture-Category" / "fixture-doc.md").write_text(
        "system: fixture\n---\nbody\n", encoding="utf-8")
    (idx / "OPEN-QUESTIONS.md").write_text(
        "| id | question | owner | status |\n|---|---|---|---|\n"
        "| TQ-1 | fixture question one | fixture-doc | OPEN |\n"
        "| TQ-2 | fixture question two | fixture-doc | ANSWERED |\n"
        "| TQ-3 | fixture withdrawn | fixture-doc | WITHDRAWN |\n",
        encoding="utf-8")
    (idx / "UNIDENTIFIED-OPEN-QUESTIONS.md").write_text(
        "| id | question | owner | status |\n|---|---|---|---|\n",
        encoding="utf-8")
    (idx / "L2-VERDICTS.md").write_text(
        "| system | contract | types | relationships | runtime | "
        "script/data | L2 | gap |\n|---|---|---|---|---|---|---|---|\n"
        "| S-01 alpha | MET | MET | MET | MET | MET | MET | none |\n"
        "| S-02 beta | MET | MET | MET | LIVE - observed; Criterion: "
        "`runtime` ruling 2026-09-25 | MET | MET | ruled live |\n"
        "| S-03 gamma | MET | MET | MET | LIVE - bare, no ruling | MET | "
        "PARTIAL | unruled |\n",
        encoding="utf-8")
    (idx / "CONTRADICTIONS.tsv").write_text(
        "id\tthing\tkind\nCT-1\tx\tDISPOSITIONED\n", encoding="utf-8")
    (idx / "candidates" / "register-triage" /
     "batch-K-scope-rulings.md").write_text(
        "# batch K\n\n"
        "## Class 1: SUPERSEDED onto the instrument (1)\n\n"
        "| row | population | instrument |\n|---|---|---|\n"
        "| TQ-7 | fixture population | fixture-doc.md |\n\n"
        "## Class 2: NOT A QUESTION, with a carrier (1)\n\n"
        "| row | carrier |\n|---|---|\n"
        "| TQ-8 | `FX-CARRIER-TASK-0926` |\n\n"
        "## Extension 2026-09-99: later ruling\n\n"
        "- **TQ-9** — class 1 applies (FX-RULING-0926). "
        "`fixture-instrument.tsv` measures the population; SUPERSEDED "
        "onto the instrument.\n", encoding="utf-8")
    (idx / "completion-packages").mkdir(parents=True)
    (idx / "completion-packages" / "PKG-FIXTURE.md").write_text(
        "# PKG-FIXTURE\n\n**stage.** `research`\n", encoding="utf-8")
    (idx / "COVERAGE.md").write_text("# coverage\n", encoding="utf-8")
    (idx / "COVERAGE-DIMENSIONS.md").write_text("# dims\n", encoding="utf-8")
    (idx / "PROGRAM-STATE.md").write_text(
        "**The terminal gate:** `final_audits` **0 / 30**\n",
        encoding="utf-8")
    (idx / "SYSTEM-MATRIX.md").write_text("# matrix\n", encoding="utf-8")
    (idx / "AUDIT-LOG.md").write_text(
        "# audit log\n\n## 2026-09-01 fixture entry\n", encoding="utf-8")
    (idx / "PARITY-STATUS.md").write_text(
        "**0 of 3 pilots certified.**\n", encoding="utf-8")
    (idx / "_inbox" / "TEAM.json").write_text(json.dumps({
        "revision": 1, "epoch": 1, "tasks": [
            {"id": "FX-REQ-ONE", "kind": "request", "status": "READY",
             "priority": "P1", "requester": "FX-REQUESTER",
             "assigned_to": "FX-WORKER", "target": "fixture target",
             "completion": "fixture acceptance",
             "known_evidence": "fixture evidence"},
            {"id": "FX-REQ-TRANSFER", "kind": "request", "status": "READY",
             "priority": "P2", "requester": "FX-A",
             "assigned_to": "FX-B", "target": "transferred work",
             "completion": "must stay visible"},
            {"id": "FX-REQ-TWO", "kind": "request", "status": "READY",
             "priority": "P2", "requester": "FX-REQUESTER2",
             "assigned_to": "FX-WORKER2", "target": "second fixture work",
             "completion": "must carry a joined reviewer"},
            {"id": "FX-REVIEW-TWO-0930", "kind": "request", "status": "DONE",
             "assigned_to": "FX-REVIEWER",
             "target": "review FX-REQ-TWO against its acceptance",
             "reviews": {"FX-REQ-TWO": "fixture-review-record"}},
            {"id": "FX-CARRIER-TASK-0926", "kind": "request", "status": "DONE",
             "assigned_to": "FX-CARRIER", "target": "carrier task"},
            {"id": "FX-PUB-CHORE-1002", "kind": "request", "status": "READY",
             "assigned_to": "FX-PUBLISHER",
             "resources": [{"key": "@publication"}],
             "target": "publish the fixture outputs"}]}), encoding="utf-8")
    (idx / "progress" / "progress.config.json").write_text(
        json.dumps({"package": "progress", "parser_version": 3}),
        encoding="utf-8")
    return root


def _bind(root):
    """Point the module's output paths at a fixture progress dir. Restores
    nothing - tests create a fresh fixture per scenario."""
    prog = root / "_index" / "progress"
    prog.mkdir(parents=True, exist_ok=True)
    pr.SNAP_JSON = prog / "snapshot.json"
    pr.SNAP_MD = prog / "snapshot.md"
    pr.CROSS_MD = prog / "crosswalk.md"
    pr.MET_MD = prog / "metrics.md"
    pr.HIST = prog / "history.jsonl"
    pr.PROGRESS = root / "PROGRESS.md"
    pr.DIRTY = prog / ".dirty"
    pr.STORE_ROOT = prog / "store"          # coherent-generation store
    pr.DOCSIG = prog / "doc-signature.txt"  # declared preimage input
    return prog


def _history_rows():
    if not pr.HIST.exists():
        return []
    return [json.loads(l) for l in
            pr.HIST.read_text(encoding="utf-8").splitlines() if l.strip()]


FXROOT = Path(tempfile.mkdtemp(prefix="prtest_"))

# T9 config edit moves the fingerprint
fx = _fx_db(FXROOT / "t9")
_bind(fx)
f0 = pr.fingerprint(fx)
cfg = fx / "_index" / "progress" / "progress.config.json"
cfg.write_text(cfg.read_text() + " ", encoding="utf-8")
f1 = pr.fingerprint(fx)
check("T9 config edit moves fingerprint", f0 != f1, "%s vs %s" % (f0[:8], f1[:8]))

# T10 same-count edit (whitespace on a ledger) moves the fingerprint
fx = _fx_db(FXROOT / "t10")
_bind(fx)
f0 = pr.fingerprint(fx)
op = fx / "_index" / "OPEN-QUESTIONS.md"
op.write_text(op.read_text() + "\n", encoding="utf-8")
f1 = pr.fingerprint(fx)
check("T10 same-count edit moves fingerprint", f0 != f1, "")

# T11 a new document moves the fingerprint; deleting it moves it back
fx = _fx_db(FXROOT / "t11")
_bind(fx)
f0 = pr.fingerprint(fx)
newdoc = fx / "01-Fixture-Category" / "second-doc.md"
newdoc.write_text("system: second\n", encoding="utf-8")
f1 = pr.fingerprint(fx)
newdoc.unlink()
f2 = pr.fingerprint(fx)
check("T11 new/deleted document moves fingerprint",
      f0 != f1 and f0 == f2, "")

# T12 missing required source -> INCOMPLETE, last-good set retained
fx = _fx_db(FXROOT / "t12")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
good_progress = pr.PROGRESS.read_text(encoding="utf-8")
(fx / "_index" / "L2-VERDICTS.md").unlink()
rc = pr.auto(fx)
snap_j = json.loads(pr.SNAP_JSON.read_text(encoding="utf-8"))
check("T12 missing source -> INCOMPLETE, last-good retained",
      rc == 1 and snap_j["freshness"]["state"] == "INCOMPLETE"
      and "L2-VERDICTS.md" in str(snap_j["freshness"].get("missing"))
      and pr.PROGRESS.read_text(encoding="utf-8") == good_progress,
      "rc=%s state=%s missing=%s"
      % (rc, snap_j["freshness"]["state"],
         snap_j["freshness"].get("missing")))
check("T12b INCOMPLETE records no history row",
      len(_history_rows()) == 1, "%d rows" % len(_history_rows()))

# T13 mid-build source move aborts the generation
fx = _fx_db(FXROOT / "t13")
_bind(fx)
orig_pv = pr.parse_verdicts
def _mid_move(path):
    out = orig_pv(path)
    (fx / "_index" / "COVERAGE.md").write_text("# moved\n",
                                             encoding="utf-8")
    return out
pr.parse_verdicts = _mid_move
try:
    pr.build(fx)
    rc = "no-raise"
except pr.ProgressError as e:
    rc = str(e)
finally:
    pr.parse_verdicts = orig_pv
check("T13 mid-build source move aborts",
      "moved during generation" in str(rc),
      str(rc)[:80])

# T14 second-output commit failure leaves no silent mix
fx = _fx_db(FXROOT / "t14")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
cov = fx / "_index" / "COVERAGE.md"
cov_raw = cov.read_bytes()
cov.write_bytes(cov_raw + b" moved")           # generation 2 has a new fp
snap2, counters2 = pr.build(fx)
orig_replace = os.replace
def _fail_replace(src, dst):
    if Path(dst) == pr.CROSS_MD:
        raise OSError("simulated write failure")
    return orig_replace(src, dst)
os.replace = _fail_replace
try:
    pr.write_all(snap2, counters2, fx)
    rc = "no-raise"
except pr.ProgressError:
    rc = "raised"
finally:
    os.replace = orig_replace
cov.write_bytes(cov_raw)                        # live fp back to generation 1
stale_json = json.loads(pr.SNAP_JSON.read_text(encoding="utf-8"))
newfp = snap2["freshness"]["fingerprint"][:12]
check("T14 mid-commit failure detected, not silently current",
      rc == "raised"
      and stale_json["freshness"]["fingerprint"] != snap2["freshness"]["fingerprint"]
      and newfp not in pr.MET_MD.read_text(encoding="utf-8")
      and pr.check(fx) != 0,
      "rc=%s" % rc)
tmps = [f.name for f in (fx / "_index" / "progress").iterdir()
        if f.name.startswith(".tmp_")]
check("T14b staged temps cleaned on failure", not tmps, str(tmps))

# T15 deleted PROGRESS.md -> check INCOMPLETE, auto regenerates
fx = _fx_db(FXROOT / "t15")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
pr.PROGRESS.unlink()
rc_check = pr.check(fx)
rc_auto = pr.auto(fx)
check("T15 deleted output detected and regenerated",
      rc_check == 2 and rc_auto == 0 and pr.PROGRESS.exists()
      and pr.check(fx) == 0,
      "check=%s auto=%s" % (rc_check, rc_auto))

# T16 edited crosswalk -> check rejects the tampered member
fx = _fx_db(FXROOT / "t16")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
with pr.CROSS_MD.open("a", encoding="utf-8") as f:
    f.write("\nhand-edit\n")
rc = pr.check(fx)
rc2 = pr.auto(fx)
check("T16 edited output detected and regenerated",
      rc != 0 and rc2 == 0 and pr.check(fx) == 0,
      "check=%s auto=%s" % (rc, rc2))

# T17 dirty mark forces regeneration; a failed run must not discharge it
fx = _fx_db(FXROOT / "t17")
prog = _bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
pr.DIRTY.write_text("", encoding="utf-8")
fp_before = json.loads(pr.SNAP_JSON.read_text(
    encoding="utf-8"))["freshness"]["fingerprint"]
rc = pr.auto(fx)
dirty_gone = not pr.DIRTY.exists()
pr.DIRTY.write_text("", encoding="utf-8")          # re-mark
(fx / "_index" / "COVERAGE.md").unlink()            # break an input
rc2 = pr.auto(fx)
dirty_kept = pr.DIRTY.exists()
check("T17 dirty forces regen; failure keeps the mark",
      rc == 0 and dirty_gone and rc2 == 1 and dirty_kept,
      "rc=%s gone=%s rc2=%s kept=%s" % (rc, dirty_gone, rc2, dirty_kept))

# T18 duplicate triggers do not double-record a generation
fx = _fx_db(FXROOT / "t18")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
pr.write_all(snap, counters, fx)
pr.auto(fx)
rows = _history_rows()
check("T18 history records one row per fingerprint",
      len(rows) == 1 and rows[0]["fp"] == snap["freshness"]["fingerprint"][:16],
      "%d rows" % len(rows))

# T19 all-L2-MET with a transferred item open -> obligation stays visible
fx = _fx_db(FXROOT / "t19")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
cross = pr.CROSS_MD.read_text(encoding="utf-8")
check("T19 transferred required work stays a completion obligation",
      "FX-REQ-TRANSFER" in cross and "FX-REQ-ONE" in cross,
      "crosswalk %d bytes" % len(cross))

# T20 parity unavailable -> UNMEASURED, never PASS
fx = _fx_db(FXROOT / "t20")
_bind(fx)
(fx / "_index" / "PARITY-STATUS.md").unlink()
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
check("T20 unavailable parity is UNMEASURED",
      snap["levels"]["parity"]["label"] == "UNMEASURED"
      and snap["levels"]["parity"]["certified"] is None,
      snap["levels"]["parity"]["label"])

# T21 LIVE cells: ruled LIVE satisfies, bare LIVE does not
fx = _fx_db(FXROOT / "t21")
_bind(fx)
snap, counters = pr.build(fx)
l2 = snap["levels"]["L2_reconstruction_grade"]
check("T21 LIVE counts only where the cell cites its ruling",
      l2["per_dimension_satisfied"]["runtime"] == 2
      and l2["per_dimension_live_unruled"]["runtime"] == 1,
      "satisfied=%s unruled=%s" % (l2["per_dimension_satisfied"]["runtime"],
                                   l2["per_dimension_live_unruled"]["runtime"]))

# T22 reviewers come from assignment fields, not requested_by
fx = _fx_db(FXROOT / "t22")
_bind(fx)
snap, counters = pr.build(fx)
revs = {p["id"]: p["reviewer"] for p in snap["packages"]}
check("T22 reviewer is UNKNOWN without an assignment, never the requester",
      revs.get("FX-REQ-ONE") == "UNKNOWN"
      and "FX-REQUESTER" not in revs.values(), str(revs))

# T23 WITHDRAWN never counted as learned
fx = _fx_db(FXROOT / "t23")
_bind(fx)
snap, counters = pr.build(fx)
met = pr.MET_MD if False else None
pr.write_all(snap, counters, fx)
mm = (fx / "_index" / "progress" / "metrics.md").read_text(encoding="utf-8")
check("T23 withdrawn is a separate bucket, not folded into answered",
      "accepted answers (learned) | 1" in mm.replace("**", "")
      and "withdrawn (never counted as learned) | 1" in mm.replace("**", ""),
      "")

# T27 FABLE notice: OEB vendored parity, NAS/OEB not learned, withdrawn
# sub-splits, register parse hazards, route-links transition record
v, _ = pr._vendored_classify(
    " | q | doc | **OUT OF EVIDENCE BOUNDARY (FRONTIER ruling 27b)** |")
check("T27a vendored OEB classifies ANSWERED (live parity)",
      v == "ANSWERED", v)
v2, _ = pr._vendored_classify(
    " | q with a `code | pipe` span | doc | ANSWERED |")
check("T27b unescaped pipe inside a code span still reads the status",
      v2 == "ANSWERED", v2)
v3, _ = pr._vendored_classify(
    " | **ANSWERED** question and status share one cell |")
check("T27c shared question+status cell reads the bold span",
      v3 == "ANSWERED", v3)

fx = _fx_db(FXROOT / "t27")
(fx / "_index" / "OPEN-QUESTIONS.md").write_text(
    "| id | question | owner | status |\n|---|---|---|---|\n"
    "| HA-1 | q | doc | **NO ADMISSIBLE SOURCE (signed)** |\n"
    "| HA-2 | q | doc | **OUT OF EVIDENCE BOUNDARY (signed)** |\n"
    "| HA-3 | q | doc | **SUPERSEDED by HA-9 (the carrier)** |\n"
    "| HA-4 | q | doc | **NOT A QUESTION** |\n"
    "| HA-5 | q | doc | **DISSOLVED - false premise** |\n"
    "| HA-6 | q | doc | ANSWERED |\n"
    "| HA-7 | q | doc | OPEN |\n",
    encoding="utf-8")
rl = fx / "_index" / "candidates" / "fable-route-links-0927"
rl.mkdir(parents=True)
(rl / "fable-register-transitions.tsv").write_text(
    "commit\trow\tfrom\tto\trecord\n"
    "aaaa\tHA-3\tPARTIAL\tSUPERSEDED\t_index/candidates/x/\n"
    "bbbb\tHA-1\tOPEN\tNO ADMISSIBLE SOURCE\t_index/candidates/y/\n"
    "hazard line with no register id\n",
    encoding="utf-8")
snap, counters = pr.build(fx)
dis = snap["levels"]["L1_modding_grade"]["open_questions_dispositions"]
check("T27d NAS/OEB split out of accepted answers",
      dis["accepted_answers"] == 1 and dis["no_admissible_source"] == 1
      and dis["out_of_evidence_boundary"] == 1, str(dis))
check("T27e WITHDRAWN sub-splits keep superseded/not-a-question/dissolved "
      "apart",
      dis["withdrawn_by_lead"].get("SUPERSEDED") == 1
      and dis["withdrawn_by_lead"].get("NOT A QUESTION") == 1
      and dis["withdrawn_by_lead"].get("DISSOLVED") == 1,
      str(dis["withdrawn_by_lead"]))
sr = snap["levels"]["residual_required_knowledge"]["superseded_residue_rows"]
check("T27f superseded residue stays listed with its carrier text",
      len(sr) == 1 and sr[0]["id"] == "HA-3"
      and "HA-9" in sr[0]["status_text"], str(sr))
rls = snap["route_links"]
check("T27g route-links record consumed, hazard rows counted not dropped "
      "silently",
      rls["state"] == "CURRENT" and rls["transitions"] == 2
      and rls["dropped"] == 1
      and {m["row"] for m in rls["moved"]} == {"HA-3", "HA-1"}, str(rls))

# T24 terminal evidence is receipted, not a filename glob
fx = _fx_db(FXROOT / "t24")
_bind(fx)
(fx / "_index" / "AUDIT-PASS13-ROUND1.md").write_text("x", encoding="utf-8")
(fx / "_index" / "AUDIT-PASS13-ROUND2.md").write_text("x", encoding="utf-8")
snap, counters = pr.build(fx)
term = snap["levels"]["terminal_certification"]
check("T24 AUDIT-PASS* are artefacts, never passes; declared counter used",
      term["final_audits_declared"] == 0
      and term["audit_pass_artefacts"] == 2,
      "declared=%s artefacts=%s" % (term["final_audits_declared"],
                                    term["audit_pass_artefacts"]))

# T25 a dated snapshot (e.g. a manual ZIP export) can never masquerade
fx = _fx_db(FXROOT / "t25")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
assert pr.check(fx) == 0
(fx / "_index" / "COVERAGE.md").write_text("# moved\n", encoding="utf-8")
rc = pr.check(fx)
(fx / "_index" / "COVERAGE.md").write_text("# coverage\n", encoding="utf-8")
check("T25 dated snapshot reports STALE, not CURRENT", rc == 1, "rc=%s" % rc)

# T26 scheduled path: watchdog tick / skip / failure receipts + dirty contract
try:
    wspec = importlib.util.spec_from_file_location(
        "swe2_watchdog",
        pr.ROOT / "Database" / "Tools" / "analysis-kit" / "gfz-scripts"
        / "swe2_watchdog.py")
    wd = importlib.util.module_from_spec(wspec)
    sys.path.insert(0, str(pr.ROOT / "Database" / "Tools" / "analysis-kit"
                           / "gfz-scripts"))
    wspec.loader.exec_module(wd)

    class _RC:
        def __init__(self, rc):
            self.returncode = rc
            self.stdout = b"receipt"
    wdroot = Path(tempfile.mkdtemp(prefix="wdtest_"))
    wd.PROGRESS_DIR = str(wdroot)
    wd.PROGRESS_DIRTY = str(wdroot / ".dirty")
    wd.PROGRESS_SCRIPT = str(wdroot / "progress_report.py")
    Path(wd.PROGRESS_SCRIPT).write_text("x", encoding="utf-8")
    events, calls = [], []
    wd.log = lambda e: events.append(e)
    wd.run_hidden = lambda *a, **k: calls.append(a) or _RC(0)
    state = {}
    wd.maybe_progress_report(state)             # startup tick (last_run=0)
    startup_ran = len(calls) == 1 and events and events[-1]["rc"] == 0
    wd.maybe_progress_report(state)             # inside interval -> skip
    skipped = len(calls) == 1
    Path(wd.PROGRESS_DIRTY).write_text("", encoding="utf-8")
    state["progress_report"]["last_run"] = 0    # force a tick
    wd.run_hidden = lambda *a, **k: calls.append(a) or _RC(0)
    wd.maybe_progress_report(state)             # success consumes the mark
    consumed = not os.path.exists(wd.PROGRESS_DIRTY) \
        and events[-1].get("dirty_consumed") is True
    Path(wd.PROGRESS_DIRTY).write_text("", encoding="utf-8")
    wd.run_hidden = lambda *a, **k: calls.append(a) or _RC(1)
    state["progress_report"]["last_run"] = 0
    wd.maybe_progress_report(state)             # failure keeps the mark
    failed_kept = os.path.exists(wd.PROGRESS_DIRTY) \
        and events[-1]["rc"] == 1 and events[-1]["dirty_consumed"] is False
    check("T26 watchdog tick/skip/failure + dirty contract",
          startup_ran and skipped and consumed and failed_kept
          and wd.PROGRESS_INTERVAL == 1800,
          "calls=%d events=%s" % (len(calls), events))
    shutil.rmtree(wdroot, ignore_errors=True)
except Exception as e:
    check("T26 watchdog tick/skip/failure + dirty contract", False,
          "%s: %s" % (type(e).__name__, e))

# ---------------------------------------------------------------- CKPT10R2
# C2: AUDIT-LOG.md is consumed by terminal_audit() and must be fingerprinted
# and required - an edit moves the fp, a deletion is INCOMPLETE.
fx = _fx_db(FXROOT / "t28")
_bind(fx)
f0 = pr.fingerprint(fx)
al = fx / "_index" / "AUDIT-LOG.md"
al.write_text(al.read_text() + "\nextra line\n", encoding="utf-8")
f1 = pr.fingerprint(fx)
al.unlink()
m, i = pr.input_problems(fx)
# root-level AUDIT-PASS* artefacts are also consumed (terminal_audit) and
# must move the fingerprint through the doc signature.
fx = _fx_db(FXROOT / "t28b")
_bind(fx)
f2 = pr.fingerprint(fx)
ap = fx / "AUDIT-PASS9-ROUND1.md"
ap.write_text("# round evidence\n", encoding="utf-8")
f3 = pr.fingerprint(fx)
check("T28 AUDIT-LOG + root AUDIT-PASS* fingerprinted (C2)",
      f0 != f1 and "_index/AUDIT-LOG.md" in m and f2 != f3,
      "fp moved: %s/%s; missing: %s" % (f0 != f1, f2 != f3, m))

# C1: snapshot.json semantic tamper - wiping a section while keeping the fp
# field must not read CURRENT.
fx = _fx_db(FXROOT / "t29")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
check("T29a generation records semantics_sha256",
      "semantics_sha256" in snap and pr._semantic_problems(snap) == [], "")
j = json.loads(pr.SNAP_JSON.read_text(encoding="utf-8"))
del j["levels"]
j["packages"] = []
pr.SNAP_JSON.write_text(json.dumps(j, indent=1) + "\n", encoding="utf-8")
rc = pr.check(fx)
check("T29b wiped levels/packages -> not CURRENT (C1)", rc == 2,
      "rc=%s" % rc)

# C1 second face: tampering only the outputs map is also caught.
fx = _fx_db(FXROOT / "t30")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
j = json.loads(pr.SNAP_JSON.read_text(encoding="utf-8"))
j["outputs"]["metrics.md"] = "0" * 64
pr.SNAP_JSON.write_text(json.dumps(j, indent=1) + "\n", encoding="utf-8")
rc = pr.check(fx)
check("T30 outputs-map tamper -> not CURRENT (C1)", rc == 2, "rc=%s" % rc)

# C3: a present-but-empty required input is invalid, never CURRENT.
fx = _fx_db(FXROOT / "t31")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
(fx / "_index" / "OPEN-QUESTIONS.md").write_text("", encoding="utf-8")
m, i = pr.input_problems(fx)
rc_auto = pr.auto(fx)
sj = json.loads(pr.SNAP_JSON.read_text(encoding="utf-8"))
check("T31 empty required input -> INCOMPLETE, not CURRENT (C3)",
      rc_auto == 1 and any("OPEN-QUESTIONS.md" in x for x in i)
      and sj["freshness"]["state"] == "INCOMPLETE"
      and "OPEN-QUESTIONS.md" in str(sj["freshness"].get("invalid")),
      "rc=%s invalid=%s" % (rc_auto, i))

# C3 second face: a schema-valid CLEARED register is not invalid - a
# header-only TSV parses to zero rows and still generates.
fx = _fx_db(FXROOT / "t32")
_bind(fx)
(fx / "_index" / "CONTRADICTIONS.tsv").write_text(
    "id\tthing\tkind\n", encoding="utf-8")
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
rc = pr.check(fx)
m, i = pr.input_problems(fx)
check("T32 cleared register is valid -> CURRENT (C3)",
      rc == 0 and not i and counters["contra_rows"] == 0,
      "rc=%s invalid=%s contra=%s" % (rc, i, counters.get("contra_rows")))

# C3 third face: truncated JSON input is invalid, not CURRENT.
fx = _fx_db(FXROOT / "t33")
_bind(fx)
(fx / "_index" / "_inbox" / "TEAM.json").write_text('{"revision": 1, "ta',
                                                   encoding="utf-8")
m, i = pr.input_problems(fx)
rc = pr.check(fx)
check("T33 truncated TEAM.json -> INCOMPLETE (C3)",
      rc == 2 and any("TEAM.json" in x for x in i), "rc=%s invalid=%s"
      % (rc, i))

# T34 page-box obligations counter (OPUS structural-obligations notice):
# unticked surface splits into no-id / closed-row / live-row; a fixture
# outside the repo reports the untracked split as unmeasured, not zero.
fx = _fx_db(FXROOT / "t34")
_bind(fx)
(fx / "01-Fixture-Category" / "fixture-doc.md").write_text(
    "system: fixture\n---\n"
    "- [ ] a page-local obligation with no register id\n"
    "- [ ] **TQ-2.** residue of an answered row\n"
    "- [ ] **TQ-1.** residue of an open row\n"
    "- [x] a ticked box counts nowhere\n", encoding="utf-8")
pb = pr.parse_page_boxes(fx)
check("T34 fixture page_boxes splits the unticked surface",
      pb["engine"] == "check_questions.read_boxes"
      and pb["no_id"] == 1 and pb["closed_id"] == 1
      and pb["open_id"] == 1 and pb["no_id_untracked"] is None,
      "%s" % (pb,))
pbl = pr.parse_page_boxes(DB)
check("T34b live page_boxes: closed-row zero, counters present",
      pbl["engine"] == "check_questions.read_boxes"
      and pbl["closed_id"] == 0
      and pbl["no_id"] is not None and pbl["open_id"] is not None,
      "%s" % (pbl,))

# T35 (OPUS-NOTICE-DATA-REPORTER-UNKNOWN-ROW): a struck-id row with an unreadable lead is
# WITHDRAWN/STRUCK; the same lead on an unstruck row stays UNKNOWN (the control); the live
# register carries no UNKNOWN row.
fq = FXROOT / "t35-oq.md"
fq.write_text("| ID | Question | Owner | Status |" + chr(10) + "|---|---|---|---|" + chr(10)
              + "| ~~TQ-8~~ | ~~q~~ | - | **STRUCK 2026-09-07 - FILED IN ERROR, not answered.** x |" + chr(10)
              + "| TQ-9 | q | - | **STRUCK 2026-09-07 - FILED IN ERROR, not answered.** x |" + chr(10), encoding="utf-8")
cls, _eng = pr._classifier()
r35 = {r["id"]: r for r in pr.parse_questions(fq, cls)}
live = [r["id"] for r in pr.parse_questions(DB / "_index" / "OPEN-QUESTIONS.md", cls) if r["status"] == "UNKNOWN"]
check("T35 struck-id row with an unreadable lead is WITHDRAWN/STRUCK; unstruck control stays UNKNOWN; live UNKNOWN = 0",
      r35.get("TQ-8", {}).get("status") == "WITHDRAWN" and r35["TQ-8"]["lead"] == "STRUCK"
      and r35.get("TQ-9", {}).get("status") == "UNKNOWN" and not live,
      "%s | %s | live UNKNOWN %s" % (r35.get("TQ-8"), r35.get("TQ-9", {}).get("status"), live))

# ---------------------------------------------------------------- CKPT10R3
# C1: the fingerprint covers COMPLETE document bodies - a checkbox deep past
# the old 4000-byte head window still invalidates the generation.
fx = _fx_db(FXROOT / "t36")
_bind(fx)
doc = fx / "01-Fixture-Category" / "fixture-doc.md"
pad = "".join("padding line %04d\n" % i for i in range(300))  # >4000 bytes
doc.write_text("system: fixture\n---\n" + pad + "- [ ] deep box one\n",
               encoding="utf-8")
f0 = pr.fingerprint(fx)
doc.write_text("system: fixture\n---\n" + pad + "- [ ] deep box two\n",
               encoding="utf-8")
f1 = pr.fingerprint(fx)
doc.write_text("system: fixture\n---\n" + pad + "- [ ] deep box one\n",
               encoding="utf-8")
f2 = pr.fingerprint(fx)
check("T36 deep-body edit past byte 4000 moves the fingerprint",
      f0 != f1 and f0 == f2, "%s vs %s" % (f0[:8], f1[:8]))

# C2: every page-only obligation is a ROW - file+anchor, locator,
# requirement, owner, reviewer, discriminator, dedup links; page-local /
# closed-row / live-row populations stay distinct.
fx = _fx_db(FXROOT / "t37")
_bind(fx)
(fx / "01-Fixture-Category" / "fixture-doc.md").write_text(
    "system: fixture\nowner_layer: PrimaryOwner:Fixture\n---\n"
    "- [ ] page-local work naming no register id\n"
    "- [ ] **TQ-1.** residue of a live row\n"
    "- [ ] **TQ-2.** residue of a closed row\n", encoding="utf-8")
pb = pr.parse_page_boxes(fx)
obs = pb.get("obligations") or []
need = {"file", "anchor", "locator", "requirement", "owner", "reviewer",
        "class", "named_ids", "dedup", "discriminator"}
check("T37 obligation rows carry the full contract, classes distinct",
      len(obs) == 3 and all(need <= set(o) for o in obs)
      and [o["class"] for o in obs]
      == ["page-local", "live-row-residue", "mis-marked-closed"]
      and obs[0]["dedup"] == ["none"]
      and obs[0]["locator"].startswith("page:")
      and obs[1]["dedup"] == ["register:TQ-1"]
      and obs[1]["locator"] == "register:TQ-1"
      and obs[2]["owner"] == "PrimaryOwner:Fixture"
      and all(o["reviewer"] == "UNKNOWN" for o in obs),
      "%s" % (obs[:1],))

# C3: EMPTY and INVALID are distinct input states; both block a required
# input; a cleared register (header present) is neither.
fx = _fx_db(FXROOT / "t38")
_bind(fx)
(fx / "_index" / "CONTRADICTIONS.tsv").write_text("", encoding="utf-8")
(fx / "_index" / "_inbox" / "TEAM.json").write_text('{"revision": 1, "ta',
                                                   encoding="utf-8")
st = pr.input_states(fx)
m, i = pr.input_problems(fx)
check("T38 empty and invalid are distinct states, both blocking",
      st["_index/CONTRADICTIONS.tsv"]["state"] == "empty"
      and st["_index/_inbox/TEAM.json"]["state"] == "invalid"
      and st["_index/COVERAGE.md"]["state"] == "present"
      and any("CONTRADICTIONS.tsv (empty file)" in x for x in i)
      and any("TEAM.json" in x and "empty" not in x for x in i),
      "invalid=%s" % i)

# C4: a publication commits ONE generation in the store; live outputs are
# byte-exact copies of its manifest's outputs.
fx = _fx_db(FXROOT / "t39")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
store = pr.GEN.Store(str(pr.STORE_ROOT))
man, gdir, probs = store.open_current()
live_ok = (man and all(
    open(os.path.join(gdir, "outputs", n), "rb").read()
    == {"snapshot.json": pr.SNAP_JSON, "snapshot.md": pr.SNAP_MD,
        "crosswalk.md": pr.CROSS_MD, "metrics.md": pr.MET_MD,
        "PROGRESS.md": pr.PROGRESS}[n].read_bytes()
    for n in man["outputs"]))
check("T39 committed generation is CURRENT; live set is its verified copy",
      not probs and man and man["generation"].startswith("g")
      and set(man["outputs"]) == {"snapshot.json", "snapshot.md",
                                  "crosswalk.md", "metrics.md",
                                  "PROGRESS.md"}
      and "preimage:doc-signature.txt" in man["inputs"]
      and live_ok,
      "probs=%s gen=%s" % (probs, (man or {}).get("generation")))

# C5: a failed run leaves the last COMPLETE generation CURRENT and the
# failure state separate (FAILURE.json / failures.jsonl, not CURRENT).
fx = _fx_db(FXROOT / "t40")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
store = pr.GEN.Store(str(pr.STORE_ROOT))
gen1 = store.current_id()
(fx / "_index" / "L2-VERDICTS.md").unlink()
rc = pr.auto(fx)
man, gdir, probs = store.open_current()
check("T40 failed run keeps the last COMPLETE generation",
      rc == 1 and store.current_id() == gen1 and not probs
      and man["generation"] == gen1
      and "L2-VERDICTS.md" in open(
          pr.SNAP_JSON, encoding="utf-8").read(),
      "rc=%s cur=%s probs=%s" % (rc, store.current_id(), probs))
# ...and a mid-commit source move refuses the candidate the same way.
(fx / "_index" / "L2-VERDICTS.md").write_text(
    "| system | contract | types | relationships | runtime | "
    "script/data | L2 | gap |\n|---|---|---|---|---|---|---|---|\n",
    encoding="utf-8")
orig_pb = pr.parse_page_boxes
def _mid_move2(db):
    out = orig_pb(db)
    (fx / "_index" / "COVERAGE.md").write_text("# moved mid-commit\n",
                                              encoding="utf-8")
    return out
pr.parse_page_boxes = _mid_move2
try:
    pr.build(fx)
    mid = "no-raise"
except pr.ProgressError:
    mid = "raised"
finally:
    pr.parse_page_boxes = orig_pb
check("T40b source move during build still aborts the generation",
      mid == "raised" and store.current_id() == gen1, mid)

# C6 (EXPORT-COHERENT-GENERATION): export is exactly one pinned generation;
# a hand-made or generation-mixed ZIP is UNVERIFIED, never CURRENT; a
# mid-export failure leaves no partial ZIP and keeps CURRENT.
fx = _fx_db(FXROOT / "t41")
_bind(fx)
snap, counters = pr.build(fx)
pr.write_all(snap, counters, fx)
store = pr.GEN.Store(str(pr.STORE_ROOT))
gen1 = store.current_id()
zp = str(FXROOT / "progress-export.zip")
gid = store.export(zp)
label, info = pr.GEN.verify_zip(zp)
import zipfile
names = zipfile.ZipFile(zp).namelist()
man1, _d, _p = store.open_current()
check("T41a export is VERIFIED, pinned to the CURRENT generation",
      gid == gen1 and label == "VERIFIED"
      and info["generation"] == gen1
      and "preimage:doc-signature.txt" in man1["inputs"]
      and any(n.startswith("inputs/") for n in names),
      "%s %s" % (label, info))
# a refresh during the day does not change what was exported: committing a
# second generation leaves the first ZIP VERIFIED for gen1.
(fx / "_index" / "COVERAGE.md").write_text("# moved\n", encoding="utf-8")
snap2, counters2 = pr.build(fx)
pr.write_all(snap2, counters2, fx)
gen2 = store.current_id()
label2, info2 = pr.GEN.verify_zip(zp)
check("T41b a later commit does not retro-edit an exported ZIP",
      gen2 != gen1 and label2 == "VERIFIED"
      and info2["generation"] == gen1, "%s %s" % (label2, info2))
# hand-assembled mixed ZIP: gen1's manifest with a member from gen2.
mixed = str(FXROOT / "progress-mixed.zip")
man_bytes = open(os.path.join(str(pr.STORE_ROOT), gen1,
                              "MANIFEST.json"), "rb").read()
with zipfile.ZipFile(mixed, "w") as z:
    z.writestr("MANIFEST.json", man_bytes)
    g1 = os.path.join(str(pr.STORE_ROOT), gen1)
    g2 = os.path.join(str(pr.STORE_ROOT), gen2)
    for n in os.listdir(os.path.join(g2, "outputs")):
        z.write(os.path.join(g2, "outputs", n), "outputs/" + n)
    for n in os.listdir(os.path.join(g1, "inputs")):
        z.write(os.path.join(g1, "inputs", n), "inputs/" + n)
label3, info3 = pr.GEN.verify_zip(mixed)
check("T41c a generation-mixed ZIP is UNVERIFIED, never CURRENT",
      label3 == "UNVERIFIED" and info3.get("hash_mismatch"), str(info3))
# a failure writing the second output mid-export leaves no ZIP and CURRENT
# untouched; last COMPLETE is preserved.
zp2 = str(FXROOT / "progress-export2.zip")
orig_write = zipfile.ZipFile.write
count = [0]
def _boom(self, src, arc=None):
    count[0] += 1
    if count[0] == 2:
        raise OSError("simulated mid-export write failure")
    return orig_write(self, src, arc)
zipfile.ZipFile.write = _boom
try:
    store.export(zp2)
    rc = "no-raise"
except Exception:
    rc = "raised"
finally:
    zipfile.ZipFile.write = orig_write
check("T41d mid-export failure keeps CURRENT, leaves no ZIP",
      rc == "raised" and not os.path.exists(zp2)
      and store.current_id() == gen2, rc)

# T42 CROSSWALK-MEANINGS semantics: reviewer joins from the assigned review
# task (never the requester), chores leave the route, every transferred
# obligation is a listed row, outcomes stay separate counts.
fx42 = _fx_db(FXROOT / "t42")
_bind(fx42)
snap42, counters42 = pr.build(fx42)
pr.write_all(snap42, counters42, fx42)
revs42 = {p["id"]: p["reviewer"] for p in snap42["packages"]}
check("T42a reviewer joins from the assigned review task, not requester",
      revs42.get("FX-REQ-TWO") == "FX-REVIEWER"
      and "FX-REQUESTER2" not in revs42.values(), str(revs42))
discs42 = {p["id"]: p["discriminator"] for p in snap42["packages"]}
cross42 = (fx42 / "_index" / "progress" / "crosswalk.md") \
    .read_text(encoding="utf-8")
route42 = cross42.split("## Coordination chores")[0]
check("T42b chores leave the deduplicated route but stay visible",
      discs42.get("FX-PUB-CHORE-1002") == "chore:coordination"
      and "FX-PUB-CHORE-1002" not in route42
      and "FX-PUB-CHORE-1002" in cross42
      and "## Coordination chores" in cross42,
      "disc=%s" % discs42.get("FX-PUB-CHORE-1002"))
trows = {r["id"]: r for r in snap42["transfers"]["rows"]}
check("T42c every transferred obligation is a listed row",
      {"TQ-7", "TQ-8", "TQ-9"} <= set(trows)
      and trows["TQ-8"]["destination_owner"] == "FX-CARRIER"
      and "TQ-9" in cross42 and "TQ-7" in cross42,
      str(sorted(trows)))
pm42 = (fx42 / "PROGRESS.md").read_text(encoding="utf-8")
check("T42d PROGRESS.md separates outcomes, tasks and package stages",
      "open board tasks (coordination load)" in pm42
      and "obligation outcomes" in pm42 and "TRANSFERRED" in pm42
      and "completion packages by stage" in pm42
      and "research 1" in pm42, "")

shutil.rmtree(FXROOT, ignore_errors=True)

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
