#!/usr/bin/env python3
"""progress.py - reproducible completion measure for the FFXII TZA engine database.

The mission is "100 % of the engine unlocked, nothing unexplainable", finishing with 30
end-to-end audits once unresolved = 0.  A single percentage hides which of those is lagging,
so this reports the components and a weighted overall.

Deliberately conservative: the dominant term is how much of the engine the database actually
EXPLAINS in prose, not how much the GFZ has classified.  Classification is the instrument;
explanation is the deliverable.
"""
import argparse, bisect, collections, datetime, io, os, re, subprocess, sys
import kit_paths as KP  # noqa: E402
import uc1_band  # noqa: E402

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
FUNCS = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
# verify_GFZ_PARENT, not verify\: Verify-GfzCheckpoint writes its residual and
# coverage dumps to the role-named directory at every certification. The bare
# verify\ tree is the 2026-09-03 pre-GN160 state and goes stale at each advance.
RESID = os.path.join(KP.ROOT, "Database", "Tools", "work", "verify_GFZ_PARENT", "residual_addrs.txt")
COVER = os.path.join(KP.ROOT, "Database", "Tools", "work", "verify_GFZ_PARENT", "coverage.tsv")

# DIMENSIONS THAT COULD NOT BE COMPUTED. Appended to by each evaluator's except handler.
# A non-empty list suppresses the OVERALL number entirely and exits non-zero: the scorer
# must not emit a headline it cannot stand behind, because a headline gets quoted and a
# traceback gets fixed.
BROKEN = []

WEIGHTS = {           # sum to 1.0
    "engine_explained":   0.55,   # the deliverable
    "ledger_resolved":    0.05,   # the instrument  (was 0.20 -- see REWEIGHT below)
    "audit_coverage":     0.15,   # every doc survived a named attack
    "registry_explained": 0.05,   # added 2026-09-03
    "ebp_explained":      0.05,   # added 2026-09-03
    "formats_explained":  0.05,   # added 2026-09-03
    "questions_closed":   0.05,
    "final_audits":       0.05,
}
FINAL_AUDITS_TARGET = 30

# --- 2026-09-03 re-weighting, stated so the headline's drop is not read as a regression ------
#
# Three dimensions were added on the same day and each took 0.05 from `ledger_resolved`, which
# fell 0.20 -> 0.15 -> 0.10 -> 0.05:
#
#     five dimensions  (ledger 0.20)   44.45%
#     + registry_explained (0.15)      39.87%    -4.58
#     + ebp_explained      (0.10)      34.89%    -4.98
#     + formats_explained  (0.05)      ~29.9%    -5.0   (0/48, so it contributes nothing yet)
#
# **`ledger_resolved` is now at its floor and the next new dimension must be funded from
# somewhere else.**  Shaving the same saturated dimension a fourth time would stop being a
# judgement about information content and start being a habit: at 0.05 it is already contributing
# 0.0498 of a possible 0.05, so there is nothing left to take without deleting the dimension --
# and it should NOT be deleted, because a resolved ledger is the precondition for every other
# figure here and a metric that stops watching a finished thing is how it quietly comes undone.
#
# **Not one line of the database changed across those three figures.**  The reasons for taking the
# weight from there rather than from the largest pot:
#
#   * `ledger_resolved` sits at 99.55% and moves 0.003 points per residual.  It is effectively a
#     constant contributing ~0.199 to the headline for work that is finished; a saturated
#     dimension carries no information.
#   * Taking the weight from `engine_explained` instead would have cost only ~0.6 points, because
#     that dimension is at 19.87%.  **The headline can be moved several points by choosing which
#     dimension to shave, without doing any work** -- which is exactly why the choice must be made
#     about the deliverable and never about the resulting number.
#   * The drop is itself the finding: the headline had been partly propped up by a done dimension.
#
# `--show-reweight` prints the old and new figures side by side.
OLD_WEIGHTS = {"engine_explained": 0.55, "ledger_resolved": 0.20, "audit_coverage": 0.15,
               "questions_closed": 0.05, "final_audits": 0.05}


def untracked_docs(db, paths):
    """How many of the documents just measured exist ONLY in the worktree.

    Added 2026-09-16 on FABLE-NOTICE-OPUS-AUDIT-COVERAGE-SHORTFALL-IS-SIX-UNTRACKED-DRAFTS, and the
    reason is worth keeping: audit_coverage read 368/375 and FABLE read that as a seven-document
    lever. SIX of the seven were UNTRACKED files - a producer's package in flight - so acting on the
    number would have meant stamping six of a peer's unpublished drafts. THE METRIC WAS NOT WRONG.
    It measures the worktree, which is what it measures. What was missing is that A READER HAD NO WAY
    TO TELL, and this session hit the same shape four other times: audit_crossrefs reading 34
    findings against a dirty tree and 2 at HEAD, program_coverage counting 328 documents against 327,
    check_surface_figures calling a dirty store 'authoritative', and check_links reporting nothing
    broken at HEAD while a HEAD worktree showed thirty.

    Fails SOFT and reports None: a scorer that refuses to run outside a git checkout is worse than
    one that cannot tell you this.
    """
    try:
        out = subprocess.run(["git", "-C", db, "ls-files", "--error-unmatch", "-z", "--", "."],
                             capture_output=True, text=True, timeout=120)
        if out.returncode != 0:
            return None
        tracked = {os.path.normcase(os.path.abspath(os.path.join(db, p)))
                   for p in out.stdout.split("\0") if p}
    except (OSError, subprocess.SubprocessError):
        return None
    return sum(1 for p in paths if os.path.normcase(os.path.abspath(p)) not in tracked)


def docs(db):
    out = []
    for root, _d, files in os.walk(db):
        top = os.path.relpath(root, db).split(os.sep)[0]
        if not re.match(r"^\d\d-", top):
            continue
        for f in sorted(files):
            if f.endswith(".md") and f != "README.md":
                out.append(os.path.join(root, f))
    return out


# --- the question register -----------------------------------------------------------------
# `docs()` walks only numbered category folders, so `_index/OPEN-QUESTIONS.md` was never opened
# by this scorer at all.  `questions_closed` counted markdown checkboxes in per-document
# sections -- real questions, but not the register the metric is named after: 383 verdict rows
# and 97 staged proposals sat outside both numerator and denominator.
#
# **A metric named after the register that does not read the register.**  Tightening the
# checkbox pattern could never have found it; it was found by restating 15 rows and watching the
# number move by one.
#
# Two judgement calls, both made conservatively, because each moves the number more than the bug:
#
#   PARTLY / PARTIAL / HALF ANSWERED count as OPEN.  A question half answered is a question.
#
#   A verdict cell that is EXACTLY `**ANSWERED**` with nothing after it counts as NEITHER.
#   Those are the merge-derived rows: a script took the longest staging line mentioning an id,
#   and that line is sometimes the answer and sometimes the question.  Counting them would be
#   the metric asserting a check that never ran -- the defect corrected in four fields already.
#   They are reported separately so the size of the untrusted pile stays visible.
REG_DISSOLVED = ("WITHDRAWN", "DISSOLVED", "SUPERSEDED")
REG_CLOSED = ("ANSWERED", "CLOSED", "DONE", "REFUTED",
              "SATISFIED", "MEASURED", "TRIAGED", "BOUNDED", "RESOLVED", "DUPLICATE", "REVISED",
              "CONFIRMED",
              # OPUS ruling 2026-09-15 (EVIDENCE-STANDARD 15bk): a question whose mechanism is
              # established and whose remaining unknown is a designer's name or a designer's
              # intention. No admissible source carries either. It counts closed because no amount
              # of work will move it, and the four requirements that let a row take it - including
              # a reviewer who is not the author - are the guard. Note this DOES move
              # `questions_closed`, which is why the guard is per row and not in this tuple.
              "NO ADMISSIBLE SOURCE",
              # FRONTIER ruling 2026-09-27: class-3 terminal state for rows whose only carrier
              # is outside the admitted evidence base. Counts closed like NAS - same guard,
              # different semantics (lost/excluded artefact, not a fact about people).
              "OUT OF EVIDENCE BOUNDARY")
REG_OPEN = ("PARTLY", "PARTIAL", "HALF", "VERIFIED OPEN", "OPEN", "UNTRIAGED")
REG_SEP = re.compile(r"^\|[\s:\-|]+\|\s*$")
REG_CELL = re.compile(r"(?<!\\)\|")


def _verdict(cell):
    """closed / open / dissolved / unstated / untrusted, from a table cell."""
    c = cell.strip()
    if c == "**ANSWERED**":
        return "untrusted"                     # state inferred from prose by the merge script
    bare = c.replace("*", "").replace("~", "").strip().upper()
    for k in REG_OPEN:                         # partial beats answered: PARTLY ANSWERED is open
        if bare.startswith(k):
            return "open"
    for k in REG_DISSOLVED:                    # a question that should not have been asked
        if bare.startswith(k):
            return "dissolved"
    for k in REG_CLOSED:
        if bare.startswith(k):
            return "closed"
    # A verdict can share the question's cell - `| UQ-214 | Whether X. **ANSWERED ...** |` has
    # no separate verdict cell. check_questions.classify finds it by scanning bold tokens inside
    # the body; doing the same keeps the two readers' verdicts equal on single-cell rows.
    for m in re.finditer(r"\*\*([^*]{2,}?)\*\*", c):
        tok = m.group(1).upper().lstrip()[:48]
        for k in REG_DISSOLVED:
            if tok.startswith(k):
                return "dissolved"
        for k in REG_CLOSED:
            if tok.startswith(k):
                return "closed"
        for k in REG_OPEN:
            if tok.startswith(k):
                return "open"
    return "unstated"


# Same id shape as check_questions' QID - suffixed ids (AR-4a, B-2/c, BI-3c) are real register
# rows and must not be invisible here. Matched against the ORIGINAL-case cell: the lower-case
# suffix is the discriminator and .upper() would erase it.
QID = re.compile(r"^[A-Z]+-\d+(?:/[a-z]|[a-z])?$")


def register(text):
    closed = opened = untrusted = 0
    for line in text.split("\n"):
        if not line.startswith("|") or REG_SEP.match(line):
            continue
        cells = [c for c in REG_CELL.split(line.strip().strip("|"))]
        if len(cells) < 2 or cells[0].strip().lower() in ("id", "id "):
            continue
        vs = [_verdict(c) for c in cells[1:]]
        if "open" in vs:
            opened += 1
        elif "dissolved" in vs:
            continue                           # withdrawn/superseded leaves the denominator
        elif "closed" in vs:
            closed += 1
        elif "untrusted" in vs:
            untrusted += 1
        else:
            opened += 1                        # a row with no verdict at all is an open question
    return closed, opened, untrusted


SELF_TEST = """| ID | Question | Status |
|---|---|---|
| AA-1 | what x is | **ANSWERED** - eight bytes, `return 0`. |
| AA-2 | what y is | **PARTLY ANSWERED** - half of it. |
| AA-3 | what z is | untriaged |
| AA-4 | what w is | **ANSWERED** |
| AA-5 | pipes `a \\| b` in the cell | **CLOSED, premise wrong** |
| AA-6 | nobody wrote a verdict |
"""


def self_test():
    c, o, u = register(SELF_TEST)
    want = (2, 3, 1)
    if (c, o, u) != want:
        print("SELF-TEST FAILED: got closed=%d open=%d untrusted=%d, want %s" % (c, o, u, want))
        return 1
    print("self-test ok: partial reads open, bare **ANSWERED** is untrusted, "
          "escaped pipes do not split a row, a verdictless row is open")
    return 0


# ONE LADDER, NOT TWO VOCABULARIES. The corpus writes a page's maturity two ways - `status:` on
# system documents and `readiness:` on CONTRACT pages - and until 2026-09-14 every tool read one at
# a time. OPUS measured what that cost: 47 of 368 system documents carry no `status:` line at all
# because they are contracts on the `readiness:` ladder, 21 of them at BEHAVIORALLY UNDERSTOOD and
# 13 at CONTRACT READY, and 88 functions were cited INSIDE THE BODY by such a page and by no
# `DOCUMENTED` page - invisible to a gate keyed on `status:` alone.
#
# SWE2-AUDIT-SPEC adjudicated the two ladders into one (9efc6221). A page is evidence-bearing when
# it says DOCUMENTED or AUDITED on the `status:` ladder, or stands at BEHAVIORALLY UNDERSTOOD or
# above on the `readiness:` one. PARTIAL, REOPENED and the lower readiness rungs are not.
READINESS_BEARING = ("BEHAVIORALLY UNDERSTOOD", "CONTRACT READY",
                     "DIFFERENTIAL TESTED", "RUNTIME VALIDATED")
STATUS_BEARING = ("DOCUMENTED", "AUDITED")


def _status_word(head):
    """The page's `status:` as a bare word, or None. A reason after the word is ignored -
    EVIDENCE-STANDARD addendum 2026-09-14bp asks a non-DOCUMENTED status to carry one."""
    m = re.search(r"^status:\s*(.+?)\s*$", head, re.M | re.I)
    if not m:
        return None
    return m.group(1).strip("*`\" ").upper().split(" — ")[0].split(" - ")[0].strip()


def _readiness_bearing(head):
    m = re.search(r"^readiness:\s*(.+?)\s*$", head, re.M | re.I)
    if not m:
        return False
    v = m.group(1).strip("*`\" ").upper()
    return any(v.startswith(r) for r in READINESS_BEARING)


def evidence_bearing(text):
    """DEPTH: is the documented mechanism understood well enough to rebuild?

    ONE LADDER, and it falls through: a page with no bearing `status:` may still be bearing on
    `readiness:`. This is the rule SWE2-AUDIT-SPEC adjudicated (9efc6221) for `engine_explained` and
    the dispositions A test, and FABLE's 2026-09-14 ruling §4 keeps it for exactly those two,
    because they ask about depth.

    NARROWED 2026-09-17 (OPUS), implementing SWE2-AUDIT-SPEC's ruling on
    OPUS-REQ-AUDITSPEC-DEPTH-AXIS-VETO-RULING, which nominated OPUS as implementer:
    AN EXPLICIT NON-BEARING `readiness:` VETOES A BEARING `status:` ON THIS AXIS.
    The reasoning is the reviewer's and is worth keeping next to the code: on a question about
    DEPTH, `readiness:` is the DIRECT answer and `status:` is a PROXY for it, and a proxy must not
    overrule the direct answer when the owner has actually given one. `coverage_documented` already
    applies exactly this direct-field-governs rule for scope, so this makes the two axes consistent
    rather than inventing a rule for one of them. It NARROWS 9efc6221 and does not reverse it:
    the fall-through is untouched, and a page that never answered the depth question is still
    read from `status:` as before. Only the cell where an owner was asked, said NO, and was
    counted YES anyway changes - the cell `depth_axis_split` was built to expose."""
    head = text[:text.find("\n---", 3)] if text.startswith("---") else text[:4000]
    if _READINESS_LINE.search(head):
        # The owner rated depth. Their answer governs, in BOTH directions - this is the whole
        # ruling, and writing it as a single return keeps the veto and the fall-through from
        # drifting apart later.
        return _readiness_bearing(head)
    return _status_word(head) in STATUS_BEARING


_READINESS_LINE = re.compile(r"^readiness:\s*\S", re.M)


def depth_axis_split(heads):
    """HOW MANY PAGES WERE EVER RATED ON THE DEPTH AXIS AT ALL, and how many are counted as bearing
    without having been.

    `evidence_bearing` asks DEPTH and answers it from `status:` when `status:` is enough, returning
    before it ever reads `readiness:`. That is the adjudicated ladder and this does not change it -
    it MEASURES it, because the headline should not be able to hide the size of its own blind spot.
    Measured 2026-09-16 on FABLE's two filings and re-derived with these same predicates: the
    majority of bearing pages reach bearing on `status:` alone, never having been asked about depth.

    Returns (status_only, readiness_only, both, status_over_explicit_no, unrated_nonbearing).
    `status_over_explicit_no` is the case where a page's owner rated depth and said NO, and the
    ladder counted it bearing anyway on `status:` - the only cell where a direct answer to the
    question is being overridden by a proxy for it.
    """
    s_only = r_only = both = veto = unrated_nb = 0
    for head, text in heads:
        s_ok = _status_word(head) in STATUS_BEARING
        r_line = bool(_READINESS_LINE.search(head))
        r_ok = _readiness_bearing(head)
        if s_ok or r_ok:
            if s_ok and not r_line:
                s_only += 1
            elif s_ok and r_line and not r_ok:
                veto += 1
            elif s_ok and r_ok:
                both += 1
            else:
                r_only += 1
        elif not r_line:
            unrated_nb += 1
    return s_only, r_only, both, veto, unrated_nb


def coverage_documented(text):
    """SCOPE COVERAGE: are the page's in-scope questions closed?  A DIFFERENT QUESTION.

    FABLE's 2026-09-14 ruling §4: *"Coverage preconditions read `status:` and are not rescued by
    `readiness:`."*  A mechanism can be BEHAVIORALLY UNDERSTOOD while the page is PARTIAL because
    residual questions remain - that is a true distinction and forbidding the pair would throw it
    away.  So this does NOT fall through when `status:` is present and non-bearing; it falls back to
    `readiness:` only when there is no `status:` line at all, which is the 47 CONTRACT pages.

    OPUS measured 241 of 368 with the fall-through and published it. Under this test it is 234: the
    seven pages carrying `status: PARTIAL` AND `readiness: BEHAVIORALLY UNDERSTOOD` do not count as
    documented until they are reconciled."""
    head = text[:text.find("\n---", 3)] if text.startswith("---") else text[:4000]
    st = _status_word(head)
    if st is not None:
        return st in STATUS_BEARING
    return _readiness_bearing(head)


def merge_questions(db, reg_text):
    """One question counted once. -> (closed, total, shared, disagreed).

    THE TWO HALVES OVERLAP AND THIS SCORER USED TO ADD THEM UP. 396 ids exist both as a page
    checkbox and as a register row, so each was counted twice - in the denominator, and in the
    numerator when closed. Found 2026-09-14 while adjudicating a request to register 387 more
    id-less boxes, which would have taken the double count to 783 without adding one real question.

    WHAT IS AND IS NOT DE-DUPLICATED, because the first version of this went too far. The REGISTER
    KEEPS ITS OWN UNIT: every row is counted, `register()`'s rules unchanged, INCLUDING two rows
    that share an id. One id naming two questions is a real defect - `check_question_ids` reports
    seven of them, and FABLE found `BM-3` is two questions - and a scorer that silently collapsed
    them would hide an integrity defect AND shrink its own denominator. Only the genuine overlap is
    removed: a page checkbox whose id already has a register row is the SAME question written twice.

    A SHARED QUESTION IS CLOSED ONLY IF BOTH SIDES SAY SO. An open box against a closed row counts
    OPEN: `check_questions` exists to find disagreements, and a metric that resolved one in the
    flattering direction would assert a check that never ran.
    """
    import importlib.util
    import os as _os
    kit = _os.path.dirname(_os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("cq", _os.path.join(kit, "check_questions.py"))
    cq = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cq)

    box_state = {}                      # id -> closed, and EVERY box carrying that id must be ticked
    unmatched = []                      # (ticked,) for boxes with no id at all - decided below
    boxes = cq.read_boxes(db)
    for _rel, _line, ticked, ids, _first in boxes:
        for i in (ids or []):
            k = i.upper()
            box_state[k] = box_state.get(k, True) and bool(ticked)

    closed = opened = untrusted = 0
    seen_ids = set()
    reg_verdict = {}                    # id -> the register's verdict, before any box downgrade
    for line in reg_text.split("\n"):
        if not line.startswith("|") or REG_SEP.match(line):
            continue
        cells = [c for c in REG_CELL.split(line.strip().strip("|"))]
        if len(cells) < 2 or cells[0].strip().lower() in ("id", "id "):
            continue
        raw_key = cells[0].strip().strip("`")
        key = raw_key.upper()
        vs = [_verdict(c) for c in cells[1:]]
        if "open" in vs:
            state = "open"
        elif "dissolved" in vs:
            state = "dissolved"
        elif "closed" in vs:
            state = "closed"
        elif "untrusted" in vs:
            state = "untrusted"
        else:
            state = "open"                      # a row with no verdict at all is an open question
        if QID.match(raw_key):
            seen_ids.add(key)
            prev = reg_verdict.get(key)
            reg_verdict[key] = state if prev is None or prev == "closed" else prev
            if state == "closed" and box_state.get(key) is False:
                state = "open"                  # the box says otherwise; a disagreement is open
        if state == "closed":
            closed += 1
        elif state == "open":
            opened += 1
        elif state == "dissolved":
            continue                            # withdrawn/superseded leaves the denominator
        else:
            untrusted += 1

    # Boxes the register already carries are NOT counted again. Everything else is.
    extra_closed = extra_open = 0
    for _rel, _line, ticked, ids, _first in boxes:
        if ids and any(i.upper() in seen_ids for i in ids):
            continue
        if ticked:
            extra_closed += 1
        else:
            extra_open += 1

    shared = len({k for k in box_state if k in seen_ids})
    # A DISAGREEMENT IS THE TWO SIDES DIFFERING, not the box being open. The first version of this
    # counter read "box open" and reported 183 where the real number is 12 - an open box against an
    # open row agrees, and saying otherwise would have handed a peer a population that is not there.
    disagreed = sum(1 for k, v in reg_verdict.items()
                    if k in box_state and v in ("open", "closed")
                    and (v == "closed") != box_state[k])
    return (closed + extra_closed,
            closed + opened + extra_closed + extra_open,
            shared, disagreed)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--final-audits-done", type=int, default=0)
    ap.add_argument("--bar-width", type=int, default=40)
    ap.add_argument("--show-reweight", action="store_true",
                    help="print the pre-2026-09-03 five-dimension overall beside the current one, "
                         "so the re-weighting is visibly not a regression")
    a = ap.parse_args(argv)

    if a.self_test:
        return self_test()

    # --- functions in the program ---------------------------------------------------
    entries, sizes = [], {}
    tags_by_entry = {}
    codedomain_now = 0
    excluded = 0
    for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
        if i == 0:
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) > 2 and not p[1].startswith(("Unwind@", "Catch_All@")):
            try:
                e = int(p[0], 16); entries.append(e); sizes[e] = int(p[2])
                tg = p[8] if len(p) > 8 else ""
                tags_by_entry[e] = tg
                if "GFZ.V121.CodeDomain" in tg:
                    codedomain_now += 1
            except ValueError:
                pass
        elif len(p) > 2:
            excluded += 1
            # The certified `codeDomain=` counts EVERY function, funclets included.  Counting it
            # only over the non-funclet subset produced 24,122 against a ledger 28,009 and reported
            # it as "a mutation is applied but not packed" -- a 3,887-function disagreement that was
            # entirely the exclusion this loop performs.
            #
            # **A cross-check between two counts is only a check when both count the same
            # population.** I built this warning to catch mixed state and its first act was to
            # manufacture some.
            if len(p) > 8 and "GFZ.V121.CodeDomain" in p[8]:
                codedomain_now += 1
    entries.sort()
    # SERIES BREAK 2026-09-28 (OPUS-REQ-DATA-UC1-POPULATION-READERS). The UC-1
    # B bands are applied to the reported population: 34,270 -> 34,269 listed
    # (007EE7F0 removed as a false entry; five extents extended) + 696 frontier
    # (1-64 band) + 99 (65-256 band, OPUS-UC1-POPULATION-CHANGE) = 35,064.
    # Frontier bodies are unexplained by ruling - they join the
    # DENOMINATOR of engine_explained and never its numerator (masked out of
    # `explained` below).  `listed_fn` keeps the certified-census count for
    # `ledger_resolved`: the coverage ledger measures the listed population and
    # the frontier bodies sit outside it entirely.
    listed_fn = len(entries)
    sizes, _band_info = uc1_band.apply(sizes)
    entries = sorted(sizes)
    uc1_frontier = uc1_band.frontier_starts() & set(entries)
    total_fn = len(entries)

    # THE RESIDUAL COMES FROM THE CERTIFIED COVERAGE, NOT FROM THE DERIVED FILE (2026-09-18, OPUS).
    #
    # `residual_addrs.txt` is not a source. `Verify-GfzCheckpoint.ps1` step 4/4 GENERATES it from
    # the `--UNRESOLVED--` section of `coverage.tsv`, entry column only, and then checks its count
    # and SHA against the expected pair. Reading the generated file instead of the thing it is
    # generated from meant the scorer could be wrong in a way the verifier could not be.
    #
    # It was. On 2026-09-18 the scorer reported `ledger_resolved 34240 / 34270` and warned that
    # "the checkpoint has been mutated and not yet re-certified". Both were false:
    #
    #   * `verify_GFZ_PARENT/coverage.tsv` ends AT `--UNRESOLVED--` - an empty section - and its
    #     header says `unresolved=0 pct=100.00000`. Header and body agree.
    #   * `verify_GFZ_PARENT/residual_addrs.txt` held 30 addresses whose set is an EXACT match to
    #     three GN161-era coverage states, one of them `coverage_GN161_0914_STALE.tsv` in the very
    #     same directory. Regenerating from the certified file yields nothing - the generator's own
    #     comment covers the empty-section case.
    #   * `verify_GN162/coverage.tsv` is BYTE-IDENTICAL to the certified one and its companion
    #     `residual_addrs.txt` is 1 byte. That is what the correct pair looks like.
    #   * All 30 carry `GFZ.V121.CodeDomain` in the dump, and none appears anywhere in the
    #     certified coverage. Four independent things said resolved; one derived file said not.
    #
    # The comment fifty lines below already called this "the only figure in the scorer that a
    # mutation can falsify without changing a count it cross-checks". It was right, and the answer
    # is to stop treating a derived artifact as evidence: score from the coverage body, and keep
    # the file as a CROSS-CHECK that says so out loud when it disagrees.
    unresolved = 0
    resid_entries = []
    resid_file_entries = []
    try:
        txt = io.open(RESID, encoding="utf-8", errors="replace").read()
        resid_file_entries = sorted(int(h, 16) for h in set(re.findall(r"[0-9A-Fa-f]{8}", txt)))
    except OSError:
        pass
    cov_section_read = False
    try:
        cov_lines = io.open(COVER, encoding="utf-8", errors="replace").read().splitlines()
        i = cov_lines.index("--UNRESOLVED--")
        cov_section_read = True
        hexes = set()
        for line in cov_lines[i + 1:]:
            m = re.match(r"([0-9A-Fa-f]{8})\b", line.strip())
            if m:
                hexes.add(m.group(1))
        unresolved = len(hexes)
        resid_entries = sorted(int(h, 16) for h in hexes)
    except (OSError, ValueError):
        # No certified coverage, or no `--UNRESOLVED--` marker in it. Fall back to the derived
        # file rather than silently scoring zero unresolved, and say which source was used.
        unresolved = len(resid_file_entries)
        resid_entries = list(resid_file_entries)

    # --- provenance: what state was measured -----------------------------------------
    # A metric is a claim about the database and carries the same burden as a claim about the
    # binary, so this now reports WHAT STATE it measured.  On 2026-09-02 a document was found
    # stale by two functions because it was computed from this dump and said so nowhere; ten
    # tools read the same dump, this scorer among them.
    #
    # The two inputs are produced by different runs -- FUNCS by DumpFullCoverageGraph, RESID by
    # the checkpoint verifier -- so `ledger_resolved` is a ratio ACROSS TWO PROGRAM STATES unless
    # they agree.  `internal=` in the certified header is the shared quantity that decides it.
    #
    # Checked and CLEAN on 2026-09-02: all 158 residual addresses appear in FUNCS and none is an
    # Unwind@/Catch_All@ funclet, so the 158 lie wholly inside the 34,270 denominator.  A residual
    # that WERE a funclet would sit in the numerator and not the denominator; the stray check
    # below is what would catch it.  Recorded because an unrecorded audit did not happen.
    warn = []
    ledger = {}
    try:
        head = io.open(COVER, encoding="utf-8", errors="replace").readline()
        ledger = {k: int(v) for k, v in re.findall(r"(\w+)=(\d+)", head)}
    except OSError:
        warn.append("no certified coverage header - figures are UNVERIFIED against the ledger")
    if ledger.get("internal") and ledger["internal"] != listed_fn + excluded:
        warn.append("FUNCS holds %d functions, certified ledger says internal=%d - the dump is a "
                    "DIFFERENT PROGRAM STATE, not merely older"
                    % (listed_fn + excluded, ledger["internal"]))
    # `ledger.get("unresolved")` is falsy at zero, so this said nothing in the one case that
    # mattered: a header reading `unresolved=0` beside a residual file listing thirty. Compare the
    # key's PRESENCE, not its truthiness.
    if "unresolved" in ledger and ledger["unresolved"] != unresolved:
        warn.append("certified header says unresolved=%d, the `--UNRESOLVED--` section of the same "
                    "file holds %d - that file disagrees with ITSELF"
                    % (ledger["unresolved"], unresolved))
    # THE CROSS-CHECK, now that the derived file is no longer the source. A disagreement is
    # reported as what it is - a stale generated artifact - and never scored from.
    if cov_section_read and sorted(resid_file_entries) != sorted(resid_entries):
        extra = [e for e in resid_file_entries if e not in set(resid_entries)]
        warn.append("residual_addrs.txt lists %d address(es), the certified coverage's own "
                    "`--UNRESOLVED--` section holds %d%s. Verify-GfzCheckpoint GENERATES that file "
                    "from that section, so a difference means the file is left over from an "
                    "earlier checkpoint. SCORED FROM THE COVERAGE; regenerate the file."
                    % (len(resid_file_entries), len(resid_entries),
                       " (e.g. %08X, absent from the section)" % extra[0] if extra else ""))
    if not cov_section_read:
        warn.append("no `--UNRESOLVED--` section in the certified coverage - fell back to the "
                    "DERIVED residual_addrs.txt, which the verifier treats as output, not input")
    # A residual that is now CLASSIFIED in the dump is a residual file the checkpoint has outrun.
    # On 2026-09-03 batch A classified four residual functions; the dump shows all four tagged and
    # `residual_addrs.txt` still lists all four, because the checkpoint has not been packed and
    # re-certified.  `unresolved` is therefore reported as 158 when the project holds 154.
    #
    # **This is the only figure in the scorer that a mutation can falsify without changing a count
    # it cross-checks** -- `internal` and `unresolved` both still matched, so the existing checks
    # stayed quiet while the number was four too high.
    #
    # STILL TRUE, AND NOW IT IS THE RIGHT SUBJECT (2026-09-18). `resid_entries` is read from the
    # certified coverage above, so this fires when the DUMP has outrun the LEDGER - the real
    # "mutated, not re-certified" case the sentence describes. Until today it was reading the
    # generated file, where the same sentence pointed at the wrong artifact entirely.
    classified_resid = [e for e in resid_entries if e in tags_by_entry
                        and "GFZ.V121.CodeDomain" in tags_by_entry[e]]
    if classified_resid:
        warn.append("%d of the %d residual addresses are CLASSIFIED in the dump (e.g. %08X) - the "
                    "checkpoint has been mutated and not yet re-certified, so `unresolved` is that "
                    "many too high" % (len(classified_resid), unresolved, classified_resid[0]))
    if ledger.get("codeDomain") and codedomain_now and ledger["codeDomain"] != codedomain_now:
        warn.append("dump has codeDomain=%d, certified header says %d - a mutation is applied but "
                    "not packed" % (codedomain_now, ledger["codeDomain"]))
    stray = [e for e in resid_entries if e not in sizes]
    if stray:
        warn.append("%d residual address(es) are not non-funclet functions in FUNCS, e.g. %08X - "
                    "they are counted as unresolved but are absent from the denominator"
                    % (len(stray), stray[0]))

    # --- what the database cites ----------------------------------------------------
    # `cited` is the SHIPPED rule - any page, entry counts - kept so the spread can be printed
    # beside the headline rather than replaced by it. `explained` is the adjudicated rule.
    cited = set()
    explained = set()
    _depth_heads = []
    _doc_paths = []
    total_docs = audited = 0
    open_q = closed_q = 0
    for p in docs(a.db):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        _doc_paths.append(p)
        total_docs += 1
        m = re.search(r"^audit:\s*$", t[:t.find("\n---", 3)], re.M)
        if m:
            blk = t[:t.find("\n---", 3)][m.end():]
            # `passes > 0` is NOT sufficient evidence of a falsification pass.  COVERAGE.md records
            # that this counter counts AMENDMENTS -- "a document can read `passes: 8` and have never
            # been attacked once" -- and on 2026-09-02 five documents were found claiming a pass
            # while the audit-debt table listed them as never attacked, with no state fields to
            # decide between the two.  So require the pass to say WHAT PROGRAM STATE it ran against:
            # an amendment bump does not produce `last_pass_state`, and a real pass cannot omit it.
            # This lowers the reported figure.  The figure was wrong, not the documents.
            pm = re.search(r"^\s+passes:\s*(\d+)", blk, re.M)
            sm = re.search(r"^\s+last_pass_state:\s*(\S+)", blk, re.M)
            stamped = (pm and int(pm.group(1)) > 0 and sm and sm.group(1) != "null")
            # A SECOND field name appeared in the corpus and this scorer did not read it.  Eleven
            # documents carry `falsification_passes`, nine of them alongside a stamped `passes`;
            # two use it ALONE, with `passes: 0` and no state -- and this counted both as never
            # attacked while each carries a written falsification-pass section.
            #
            # `falsification_passes` is arguably the better name, since `passes` was established
            # tonight to count AMENDMENTS.  Rather than legislate the name, accept either -- but
            # the new one only WITH A SECTION IN THE BODY, never on the counter alone.  Accepting a
            # bare counter is the original defect: **the whole point is that a number in the
            # frontmatter is a claim, and only the section is evidence.**
            #
            # Third correction to this metric tonight, and the first in the UNDER-counting
            # direction. **A metric drifts both ways, and only one of those feels like a problem.**
            fm = re.search(r"^\s+falsification_passes:\s*(\d+)", blk, re.M)
            has_section = re.search(r"^#{2,3} .*[Ff]alsification pass", t, re.M) is not None
            if stamped or (fm and int(fm.group(1)) > 0 and has_section):
                audited += 1
        open_q += len(re.findall(r"^\s*-\s*\[ \]", t, re.M))
        closed_q += len(re.findall(r"^\s*-\s*\[x\]", t, re.M))
        # `0x`-PREFIXED ADDRESSES WERE INVISIBLE. Found by repos-c9, 2026-09-04, in the citation
        # gate family and confirmed here: the old pattern required a backtick immediately before
        # the leading `0`, so `` `0x0023A570` `` never matched and `` `0023A570` `` did.
        #
        # Measured before fixing: 6,851 functions cited under the old pattern, 6,923 under this
        # one -- **72 functions silently dropped**, worth +0.12 points at weight 0.55. Small in
        # the headline and not small in kind: it is an UNDER-count in the deliverable dimension,
        # and it grows with every sheet written in the `0x` style.
        #
        # `(?:0x)?` is deliberate rather than a lookaround here because the delimiter is a
        # backtick either way. `check_located_not_read.py` line 123 already had the general form,
        # `(?<![0-9A-Fa-f])...(?![0-9A-Fa-f])`, which is correct for unfenced prose.
        bearing = evidence_bearing(t)
        # Collected for depth_axis_split - a measurement of the ladder, not a change to it.
        _depth_heads.append((t[:t.find("\n---", 3)] if t.startswith("---") else t[:4000], t))
        for h in re.findall(r"`(?:0x)?(0[0-9A-Fa-f]{7})`", t):
            v = int(h, 16)
            i = bisect.bisect_right(entries, v) - 1
            if i >= 0 and entries[i] <= v < entries[i] + sizes[entries[i]]:
                e = entries[i]
                cited.add(e)                       # the shipped rule, kept for the spread
                # THE ADJUDICATED RULE (SWE2-AUDIT-SPEC, 2026-09-14, commit 9efc6221), after OPUS
                # measured the three axes and routed the choice rather than making it:
                #   a function counts when an EVIDENCE-BEARING page cites it, and the citation is
                #   strictly INTERIOR or an ENTRY cite of a body under 128 bytes.
                # The size cut is the leaf-helper boundary - `0020E600` is ten bytes and completely
                # explained by naming it, while an entry-only cite of a 512-byte body is a mention.
                if bearing and (v != e or sizes[e] < 128):
                    explained.add(e)

    # UC-1 frontier bodies join the denominator but never the numerator: they
    # are unexplained by ruling (never A/B/C by default, never D), and a
    # mechanical interior cite cannot explain one.  `cited` keeps them - a
    # mention is a mention - so the printed spread can separate the two.
    uc1_cited = cited & uc1_frontier
    explained -= uc1_frontier

    comp = collections.OrderedDict()
    comp["engine_explained"] = (len(explained), total_fn)
    comp["ledger_resolved"] = (listed_fn - unresolved, listed_fn)
    comp["audit_coverage"] = (audited, total_docs)
    reg_path = os.path.join(a.db, "_index", "OPEN-QUESTIONS.md")
    reg_c = reg_o = reg_u = 0
    if os.path.exists(reg_path):
        reg_c, reg_o, reg_u = register(io.open(reg_path, encoding="utf-8",
                                               errors="replace").read())
    # The authored-data pointer registry: 63 slots, re-derived from the registry document's own
    # bounds and stride and cross-checked against the count it states.  Not a plan, a census --
    # see check_formats.py for why a formats metric with an authored denominator is worthless.
    reg_cov = reg_tot = containers = 0
    try:
        import check_formats
        s, e, st, reg_tot = check_formats.derive_population(a.db)
        claims, cont = check_formats.claimed_slots(a.db)
        reg_cov = sum(1 for k in claims if s <= k <= e and (k - s) % st == 0)
        containers = len(cont)
    except Exception as exc:
        # FAIL CLOSED. This used to print a note and leave cov = tot = 0, which the
        # scoring loop folded into OVERALL as a clean 0.0 at full weight - a crash
        # traded for a wrong headline. See BROKEN below.
        BROKEN.append(("registry_explained", "%s" % exc))
        print("  (registry_explained UNAVAILABLE: %s)" % exc)

    # The EBP script container: 14 units -- the container plus 13 section types censused by
    # unpacking all 1,115 us-language scripts.  See check_ebp.py; the population is frozen and
    # `--census` re-verifies it, because a scored denominator that drifts silently is worse than
    # no denominator at all.
    ebp_cov = ebp_tot = 0
    try:
        import check_ebp
        ebp_tot = len(check_ebp.UNITS)
        ebp_cov = sum(1 for u in check_ebp.claimed_units(a.db) if u in check_ebp.UNITS)
    except Exception as exc:
        # FAIL CLOSED. This used to print a note and leave cov = tot = 0, which the
        # scoring loop folded into OVERALL as a clean 0.0 at full weight - a crash
        # traded for a wrong headline. See BROKEN below.
        BROKEN.append(("ebp_explained", "%s" % exc))
        print("  (ebp_explained UNAVAILABLE: %s)" % exc)

    # Shipped file formats: every extension in the archive index, censused over 89,414 entries by
    # `census_archive_formats.py`.  This dimension exists because `engine_explained` is structurally
    # blind to it -- a format nobody documents costs no functions, so Audio could sit at eleven
    # documents and 2,064 owned functions while `.sab` (4,609 files) had one passing mention.
    #
    # `container_format:` stays counted-and-not-scored beside it, and that is not an inconsistency:
    # those formats are not archive entries and still have no census, which was always the stated
    # reason for not scoring them.  The reason was removed for archive formats only.
    # CEILING, and it is deliberate. Two of the 48 rows - `bin` and `dat` - are extensions the game
    # uses for unrelated containers: 12 sampled `.bin` files give SEVEN signatures (`sloc`, `st2e`,
    # `FLAG`, `gmap`, `CCdd`, `hctg`, a bare dword). No single loader contract exists to write, so
    # nobody can honestly disposition them, and `PS2-Image-Data-Formats/README.md` chose on
    # 2026-09-03 to state that rather than re-cut the census - re-cutting is an author choosing
    # their own denominator. **So this dimension tops out at 46/48 = 95.83 %, not 100 %**, and the
    # last two points are not a gap in diligence. `check_format_row_purity.py` keeps it checkable:
    # of the 29 rows dispositioned `explained`, exactly one (`txt`, whose leading bytes are text)
    # carries more than one ASCII magic tag.
    fmt_cov = fmt_tot = 0
    try:
        import check_assets
        census = check_assets.load_census()
        fmt_tot = len(census)
        # SIX, not five. check_assets.evaluate gained `magic_scoped` in 79510a96 and this
        # caller was not updated; the ValueError was swallowed by the except below, so the
        # dimension scored 0/48 at weight 0.05 and OVERALL printed 4.8 points low. Routed by
        # FABLE rather than fixed by them, on this project's rule that one agent does not move
        # the headline. Corrected 2026-09-16 (OPUS).
        counted, _refused, _coll, _stray, bucketed, magic_scoped = check_assets.evaluate(
            census, check_assets.claimed_formats(a.db))
        fmt_cov = len(counted)
        if bucketed:
            print("  formats_explained composition: %d/%d dispositioned = %d explained "
                  "+ %d bucketed; numerator ceiling %d/%d"
                  % (fmt_cov + len(bucketed), fmt_tot, fmt_cov, len(bucketed),
                     fmt_cov, fmt_tot))
    except Exception as exc:
        # FAIL CLOSED. This used to print a note and leave cov = tot = 0, which the
        # scoring loop folded into OVERALL as a clean 0.0 at full weight - a crash
        # traded for a wrong headline. See BROKEN below.
        BROKEN.append(("formats_explained", "%s" % exc))
        print("  (formats_explained UNAVAILABLE: %s)" % exc)

    comp["registry_explained"] = (reg_cov, reg_tot)
    comp["ebp_explained"] = (ebp_cov, ebp_tot)
    comp["formats_explained"] = (fmt_cov, fmt_tot)
    # ONE QUESTION, COUNTED ONCE. The halves overlap - 396 ids are both a page checkbox and
    # a register row - and this line used to add them together. See merge_questions().
    q_closed, q_total, q_shared, q_disagreed = merge_questions(
        a.db,
        io.open(reg_path, encoding="utf-8", errors="replace").read()
        if os.path.exists(reg_path) else "")
    comp["questions_closed"] = (q_closed, q_total)
    comp["final_audits"] = (a.final_audits_done, FINAL_AUDITS_TARGET)

    overall = 0.0
    lost = 0.0
    broken_names = {b[0] for b in BROKEN}
    print("FFXII TZA engine database - completion\n")
    for k, (n, tot) in comp.items():
        # A ZERO DENOMINATOR IS NOT A ZERO SCORE. It means the population could not be
        # derived, so the ratio is undefined; scoring it 0.0 is the silent-zero bug in
        # another hat. final_audits at 0/30 is unaffected - its denominator is 30 and
        # zero completed runs is a true measurement.
        if k in broken_names or not tot:
            if k not in broken_names:
                BROKEN.append((k, "denominator is 0 - population not derived"))
            lost += WEIGHTS[k]
            print("  %-18s [%s] %s   %d / %d   (weight %.2f)"
                  % (k, "?" * a.bar_width, "  UNAVAIL", n, tot, WEIGHTS[k]))
            continue
        r = n / tot
        overall += WEIGHTS[k] * r
        filled = int(round(a.bar_width * r))
        bar = "#" * filled + "." * (a.bar_width - filled)
        print("  %-18s [%s] %6.2f%%   %d / %d   (weight %.2f)"
              % (k, bar, 100 * r, n, tot, WEIGHTS[k]))

    if BROKEN:
        print("\n  %-18s [%s] UNAVAILABLE" % ("OVERALL", "?" * a.bar_width))
        print("\n  REFUSING TO PRINT A HEADLINE: %d dimension(s) could not be computed,"
              " carrying %.2f of the 1.00 weight." % (len(BROKEN), lost))
        for name, why in BROKEN:
            print("      %-20s %s" % (name, why))
        print("  The remaining dimensions sum to %.2f%% of the %.2f weight that did"
              " compute; that is NOT the headline and must not be quoted as one."
              % (100 * overall, 1.0 - lost))
    else:
        filled = int(round(a.bar_width * overall))
        bar = "#" * filled + "." * (a.bar_width - filled)
        print("\n  %-18s [%s] %6.2f%%" % ("OVERALL", bar, 100 * overall))

    if a.show_reweight:
        old = sum(OLD_WEIGHTS[k] * ((n / tot) if tot else 0.0)
                  for k, (n, tot) in comp.items() if k in OLD_WEIGHTS)
        print("\n  RE-WEIGHTING 2026-09-03, on today's numbers:")
        print("    %d dimensions, ledger_resolved at %.2f : %6.2f%%"
              % (len(OLD_WEIGHTS), OLD_WEIGHTS["ledger_resolved"], 100 * old))
        print("    %d dimensions, ledger_resolved at %.2f : %6.2f%%"
              % (len(WEIGHTS), WEIGHTS["ledger_resolved"], 100 * overall))
        print("    difference                          : %+6.2f points" % (100 * (overall - old)))
        print("  The database did not change between those two figures. The 0.05 came out of a")
        print("  dimension sitting at %.2f%% - saturated, and so carrying no information - rather"
              % (100 * comp["ledger_resolved"][0] / comp["ledger_resolved"][1]))
        print("  than out of the largest pot, which would have cost about a tenth as much and")
        print("  flattered the headline for no reason connected to the deliverable.")

    print("\n  %d documents - %d functions cited of %d - %d unresolved"
          % (total_docs, len(cited), total_fn, unresolved))
    print("  population: %s" % uc1_band.describe(_band_info))
    _held = uc1_band.held()
    if _held:
        print("      held (declared uncertainty, never counted): "
              + ", ".join("%08X-%08X" % h for h in _held))
    if uc1_cited:
        print("      (%d UC-1 frontier body/bodies carry an interior citation -"
              " mentions, not explanation)" % len(uc1_cited))
    print("  ledger_resolved keeps the certified-census denominator (%d listed):"
          % listed_fn)
    print("      the coverage ledger measures the listed population; the %d"
          " frontier bodies sit outside it" % len(uc1_frontier))
    # WHICH TREE THESE FIGURES CAME FROM. See untracked_docs' docstring: audit_coverage read
    # 368/375 and six of the seven "unaudited" documents were a peer's UNTRACKED drafts, so the
    # number read as a seven-document lever and was a one-document lever. The metric measures the
    # worktree, which is what it measures; what it could not do was say so.
    _untracked = untracked_docs(a.db, _doc_paths)
    if _untracked is None:
        print("  (could not tell tracked from untracked here - no usable git checkout)")
    elif _untracked:
        print("  %d of those %d documents are UNTRACKED - they exist in this worktree and NOT at"
              % (_untracked, total_docs))
        print("  HEAD, so every figure above counts work nobody else can see. Re-run in a clean")
        print("  detached worktree before quoting any of it as the corpus.")
    else:
        print("  all %d are tracked; no untracked document is inflating these figures" % total_docs)
    # THE SPREAD, PRINTED BESIDE THE HEADLINE BECAUSE THE HEADLINE IS A CHOICE.
    # `engine_explained` was measured three ways in one day and read anywhere from 5.8 % to 41.4 %
    # depending on which pages count and which citations count - a factor of seven on the dimension
    # that carries weight 0.55. SWE2-AUDIT-SPEC chose the rule; this line keeps the alternative
    # visible so nobody has to rediscover that the figure has a shape.
    loose = 100.0 * len(cited) / total_fn if total_fn else 0.0
    tight = 100.0 * len(explained) / total_fn if total_fn else 0.0
    print("  engine_explained spread: %.2f%% under the rule in force (evidence-bearing page, "
          "interior" % tight)
    print("  or an entry cite under 128 B), against %.2f%% if any page and any citation counted."
          % loose)
    # AND THE SAME PRINCIPLE ONE STEP FURTHER: the headline is a choice, and so is the AXIS it reads.
    # `evidence_bearing` asks DEPTH and answers it from `status:` whenever `status:` suffices,
    # returning before `readiness:` is ever read. Measured 2026-09-16 on FABLE's two filings
    # (125 pages below the line never rated, then the symmetric check finding the larger mass ABOVE
    # it): most bearing pages have never been asked about depth at all. This does not change the
    # ladder - OPUS ruled that a change moving weight 0.55 needs independent review first - it
    # stops the number hiding the size of its own blind spot.
    s_only, r_only, r_both, veto, unrated_nb = depth_axis_split(_depth_heads)
    rated = r_only + r_both + veto
    total_pages = s_only + r_only + r_both + veto + unrated_nb
    print("  DEPTH AXIS: %d of %d pages carry a `readiness:` line at all; %d do not."
          % (rated, total_pages, s_only + unrated_nb))
    print("  Of the pages counted BEARING, %d reach it on `status:` ALONE with no readiness line -"
          % s_only)
    print("  never rated on the axis this dimension asks about. %d were rated and rated NOT"
          % veto)
    print("  bearing, and ARE NO LONGER COUNTED BEARING: SWE2-AUDIT-SPEC ruled 2026-09-17 that an")
    print("  explicit non-bearing `readiness:` VETOES a bearing `status:` here, because readiness")
    print("  is the direct answer and status is only a proxy for it. That cell used to be the one")
    print("  place a direct answer was overridden by a proxy, and it is now closed. %d non-bearing"
          % unrated_nb)
    print("  pages were never asked either, and those still fall through to `status:` as before.")
    print("  Rule adjudicated by SWE2-AUDIT-SPEC 2026-09-14 (9efc6221) after OPUS measured the "
          "three")
    print("  axes and routed the choice; the figure fell %.1f points and that is the correction, "
          "not a regression." % (loose - tight))

    # --- EC-7: the A/B/C/D disposition dimension, REPORTED AND NOT WEIGHTED ----------
    #
    # `COMPLETION-PLAN.md` section 3 says outright that a citation count is the wrong measure:
    # *"citing those 11,836 without explaining them would satisfy the metric and betray the
    # mission."*  `check_dispositions.py` implements the policy the plan defines and this line
    # prints it BESIDE `engine_explained` over the same 34,270 bodies.
    #
    # It takes weight from nothing.  Re-weighting the 0.55 dimension is the program-level decision
    # `EC-7` reserves for all three identities; OPUS and FABLE have recorded positions and ASTRA's
    # is outstanding (`OPUS-REQ-ASTRA-DISPOSITION-POSITION`).  Printing it unweighted is what lets
    # the decision be taken on a measured figure instead of an argued one.
    try:
        import check_dispositions as _disp
        _d = _disp.evaluate(a.db, _disp.load_functions())
        # `engine_explained is unchanged` was true until 2026-09-14 and is not now: the
        # scorer applies SWE2-AUDIT-SPEC's adjudicated rule. EC-7 is still REPORTED and
        # NOT WEIGHTED, which is the part that was ever load-bearing here.
        print("  disposition (EC-7, REPORTED AND NOT WEIGHTED - a separate dimension):")
        print("      A %d + B %d + C %d = %d of %d (%.2f%%); D %d held separate; frontier %d"
              % (_d["A"], _d["B"], _d["C"], _d["explained"], _d["total"],
                 100.0 * _d["explained"] / _d["total"], _d["D"], _d["frontier"]))
        print("      %d of the %d functions this scorer counts as cited are cited ONLY at their "
              "entry" % (_d["entry_only"], len(cited)))
        print("      address by an evidence-bearing page - a mention, not an explanation. "
              "Run check_dispositions.py")
        print("      for the attribution; interior citation is a stricter PROXY, not a true count.")
        if _d["families_refused"]:
            print("      %d family declaration(s) REFUSED - run check_dispositions.py"
                  % _d["families_refused"])
    except Exception as _e:                                   # never let a new line break the scorer
        print("  disposition (EC-7): not available - %s" % _e)
    print("  registry: %d of %d authored-data slots explained; %d loose (non-archive) container "
          "formats documented - counted, NOT scored, as those still have no census"
          % (reg_cov, reg_tot, containers))
    print("  ebp:      %d of %d container units explained (1 container + 13 section types censused "
          "over 1,115 scripts)" % (ebp_cov, ebp_tot))
    print("  formats:  %d of %d shipped file formats dispositioned (censused over the archive "
          "index, not chosen)" % (fmt_cov, fmt_tot))
    print("  questions: %d closed / %d open in per-document sections, %d / %d in the register"
          % (closed_q, open_q, reg_c, reg_o))
    print("  %d question(s) appear BOTH as a page checkbox and as a register row; each is counted\n"
          "  ONCE, and %d of them disagree - a ticked box against an open row, or the reverse - and\n"
          "  are counted OPEN" % (q_shared, q_disagreed))
    if reg_u:
        print("  %d register rows read **ANSWERED** with no text - state inferred from prose by "
              "the merge, counted NEITHER way" % reg_u)

    # `engine_explained` counts CITED LISTED FUNCTIONS over LISTED FUNCTIONS.  The function list is
    # an instrument with coverage, not ground truth: on 2026-09-03 a session found a 27-byte
    # function absent from it -- and that function was the ONLY writer of the value its caller
    # census had just reported unwritten.  A citation landing in a gap is silently dropped here,
    # so this metric UNDER-counts by an unmeasured amount.  Printing the gap keeps the name honest.
    span = (entries[-1] + sizes[entries[-1]]) - entries[0]
    covered = sum(sizes[e] for e in entries)
    cur, gapb, gapn = entries[0], 0, 0
    for e in entries:
        if e > cur:
            gapb += e - cur
            gapn += 1
        cur = max(cur, e + sizes[e])
    print("  function list covers %.2f %% of its own span - %d region(s), %d bytes between listed "
          "bodies" % (100.0 * covered / span, gapn, gapb))
    # 2026-09-13: that remainder was classified.  The figures below are the result and they are
    # pinned to the gap total they were derived from -- if the function list is ever regenerated
    # the total moves, the pin fails, and this goes back to saying "unmeasured" rather than
    # quoting a stale number as if it were current.
    if (gapn, gapb) == (31933, 568793):
        print("  of that: 244290 B alignment padding, 59737 B funclet bodies (excluded by design), "
              "38129 B inline jump tables (data), and")
        # ~1308, not the 1471 first published: UC-5 adjudicated 163 of those blocks as continuations
        # of the body before them, not separate functions (2026-09-13, +1 on 2026-09-17 when
        # unlisted_admissions.py's `referenced` dropped the banned .pdata route). The BYTE total is
        # barely touched - 3797 of 244619 is 1.6 % - because those bytes are still unlisted code
        # either way.
        # 2026-09-25 (OPUS): 431 of the blocks were the preceding function's inline jump table -
        # 38129 B of DATA - and one (379 B) now lies inside a listed body; unlisted_admissions.py
        # gives them `table` / `covered` verdicts. 244619 - 38129 - 379 = 206111.
        print("  206111 B of CODE in about 877 blocks that the list does not contain at all - "
              "neither")
        print("  cited nor in the frontier. See 99-Unresolved-Residual/Unlisted-Code/. The "
              "denominator is")
        print("  short by those bodies and has NOT been changed; read every figure above as 'of "
              "the 34270")
        print("  bodies the list contains', not 'of the engine'.")
    else:
        print("  a citation inside a gap is dropped, so engine_explained under-counts by an "
              "unmeasured amount")
        print("  (the 2026-09-13 classification was pinned to 31933 regions / 568793 bytes and no "
              "longer applies)")

    print("\n  measured against")
    for label, path in (("functions", FUNCS), ("residual", RESID), ("ledger", COVER)):
        try:
            ts = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            print("    %-10s %s  %s" % (label, ts.strftime("%Y-%m-%d %H:%M"), os.path.basename(path)))
        except OSError:
            print("    %-10s MISSING  %s" % (label, os.path.basename(path)))
    if ledger:
        print("    ledger says internal=%s codeDomain=%s unresolved=%s"
              % (ledger.get("internal"), ledger.get("codeDomain"), ledger.get("unresolved")))
    if warn:
        print("\n  PROVENANCE WARNINGS - the figures above are measured across mixed state:")
        for w in warn:
            print("    ! %s" % w)
    # A REFUSAL THAT EXITS 0 IS NOT A REFUSAL. The UNAVAILABLE headline above is printed for
    # a human; the exit code is the only thing a chain can check, and it must disagree with
    # success whenever a dimension did not compute. 3 rather than 2 so a broken dimension is
    # separable from a provenance warning.
    #
    # THE ORDER IS THE WHOLE CONTRACT AND IT USED TO BE WRONG. Corrected 2026-09-16 on
    # AUDITSEM-CONTRA-OPUS-SCORER-EXIT-SEPARABILITY: the `warn` block RETURNED 2 before this test
    # ran, so a broken dimension exited 2 whenever a provenance warning was also present - and at
    # HEAD one always is (the dump/header codeDomain mismatch). The separability the comment above
    # promises was therefore false in exactly the case it was written for, and a chain checking
    # `== 3` would have been told a broken dimension was a stale ledger. The warnings still PRINT
    # unconditionally; only the return moved. A BROKEN DIMENSION OUTRANKS A STALE MEASUREMENT,
    # because one means the number is wrong and the other means it is old.
    if BROKEN:
        return 3
    if warn:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
