#!/usr/bin/env python3
"""dispositions.py - a false-positive disposition that CANNOT outlive the evidence it was given for.

WHY. Several gates in this kit suppress findings that were read once and judged false. Today that
suppression lives in three incompatible shapes, and each has a hole:

  * check_doc_claims keys a registry on (source, target, term). Durable, but it does NOT record what
    the claim SAID. Reword either document and the key still matches, so a verdict given about one
    sentence goes on suppressing a different one.
  * check_self_contradiction has no registry at all. Its dispositions are prose in its own source
    comments - "three hits were dispositioned by hand" - which no run can check and no reviewer can
    find.
  * check_links had STRICT_WAIVERS, a dict in the source keyed by (file, target), with a
    requirement id in the value and nothing tying it to the state of the corpus.

FINAL-AUDIT pass 24 is the reason this matters: a terminal streak of thirty runs re-adjudicates the
same false positives thirty times unless they persist, and a disposition that persists while the
evidence moves is worse than none - it is a permanent blindfold with a date on it.

THE THREE PROPERTIES, and each is mechanical rather than advisory:

  1. PERSISTENT. One TSV per database, committed, greppable, diffable. A disposition nobody can find
     is not a decision, it is a memory.
  2. INDEPENDENTLY REVIEWED. Every row carries an author AND a reviewer, and a row whose reviewer
     is its author - or is blank - IS NOT APPLIED. It is reported as awaiting review, which is the
     one state that must not look like a pass. This is EVIDENCE-STANDARD 15bk requirement 4 applied
     to suppression: the same standard the corpus demands of a NO ADMISSIBLE SOURCE ruling.
  3. EVIDENCE CHANGES INVALIDATE. The row stores a sha256 of the exact text the gate showed when
     the verdict was given. The gate recomputes it every run. If the evidence moved, the hash no
     longer matches, the disposition does NOT apply, and the finding comes back - reported as
     LAPSED rather than as new, so a reader can see that a judgement existed and what it was given
     for. This is the property the other three shapes all lack.

WHAT A DISPOSITION IS NOT. It is not a way to close a question, and nothing here writes to the
register. It records that a GATE's finding was read and found not to be a defect. If the finding is
real, the fix is the document.

FILE FORMAT - `_index/candidates/false-positive-dispositions.tsv`, tab separated:

    gate    subject    evidence_sha256    verdict    author    reviewer    dated    reason

  gate      the checker's filename, e.g. check_self_contradiction.py
  subject   a stable key the gate chooses, e.g. "16-UI/foo.md::02CA8F38"
  evidence  sha256 of the normalised evidence text (see `digest`)
  verdict   FALSE-POSITIVE | SCOPED | DUPLICATE  -- why it is not a defect
  author    the identity that read it
  reviewer  a DIFFERENT identity that checked the reading
  dated     YYYY-MM-DD
  reason    one line, in prose, that a stranger can check
  review_record  WHERE THE REVIEW IS RECORDED (column 9, added 2026-10-01). One of:
            `path` or `path#heading text` - a file under the database root; with a fragment, that
            text must occur in the file; or `commit:HASH` - a commit git can resolve here.

  4. A SIGNATURE NEEDS A DURABLE REVIEW. Added 2026-10-01 on FRONTIER-REQ-OPUS-DISPOSITIONS-RECORD-GATE-1001:
     1e76d4dae signed 28 rows in one commit and 8 of them had no committed review anywhere
     (_index/candidates/frontier-verdicts-repair-1001/README.md, ruling 3), yet the gate applied them,
     because it checked only reviewer != author and the hash. A signed row whose review_record is
     empty or does not resolve is UNRECORDED and suppresses nothing.

usage: dispositions.py [--db DB] [--self-test]
"""
import hashlib
import io
import os
import re
import subprocess
import sys

REL = os.path.join("_index", "candidates", "false-positive-dispositions.tsv")
COLUMNS = ["gate", "subject", "evidence_sha256", "verdict", "author", "reviewer", "dated", "reason",
           "review_record"]
VERDICTS = {"FALSE-POSITIVE", "SCOPED", "DUPLICATE"}

APPLIED = "APPLIED"
LAPSED = "LAPSED"            # subject known, evidence moved -- the finding returns
UNREVIEWED = "UNREVIEWED"    # author is the reviewer, or none named -- never applied
UNRECORDED = "UNRECORDED"    # signed, but no durable review record resolves -- never applied


def record_problem(db, rec):
    """None when `rec` resolves to a durable review record under `db`, else why it does not.

    Fails closed: an empty value, a path outside the database root, a missing file, a fragment the
    file does not contain, or a commit git cannot resolve (or no git at all) all refuse.
    """
    rec = (rec or "").strip()
    if not rec:
        return "no review_record"
    if rec.startswith("commit:"):
        h = rec[len("commit:"):].strip()
        if not re.fullmatch(r"[0-9a-fA-F]{7,40}", h):
            return "malformed commit %r" % h
        try:
            r = subprocess.run(["git", "cat-file", "-e", h + "^{commit}"], cwd=db,
                               capture_output=True, timeout=30)
        except (OSError, subprocess.SubprocessError) as e:
            return "git unavailable (%s)" % e.__class__.__name__
        return None if r.returncode == 0 else "commit %s does not resolve" % h
    path, _, frag = rec.partition("#")
    root = os.path.realpath(db)
    full = os.path.realpath(os.path.join(root, path))
    if not (full == root or full.startswith(root + os.sep)):
        return "record %s is outside the database" % path
    if not os.path.isfile(full):
        return "record %s does not exist" % path
    if frag and frag not in io.open(full, encoding="utf-8", errors="replace").read():
        return "record %s does not contain %r" % (path, frag)
    return None


def digest(*parts):
    """A stable hash of the evidence a verdict was given for.

    Whitespace is collapsed so that reflowing a paragraph does not lapse a disposition, but any
    change to the WORDS does. That is the intended sensitivity: the question is whether the thing
    judged is still the thing present.
    """
    norm = "\x1f".join(re.sub(r"\s+", " ", p or "").strip() for p in parts)
    return hashlib.sha256(norm.encode("utf-8", "replace")).hexdigest()[:16]


def path_for(db):
    return os.path.join(db, REL)


_WARNED = set()


def _warn_terminator(p):
    """A file with no final newline will SWALLOW THE NEXT APPENDED ROW, silently.

    The last line of this registry is usually a `#` note, so a plain append lands inside that
    comment and load() skips it. The row is then in the file, suppresses nothing, and is reported
    in no state at all - not APPLIED, not LAPSED, not UNREVIEWED, not ORPHANED. Every other
    failure in this module is loud by construction; this one is not, so it is announced on sight
    rather than when it next costs somebody a verdict. Printed once per process.
    """
    if p in _WARNED:
        return
    _WARNED.add(p)
    print("  MALFORMED: %s does not end with a newline. The next appended row will be glued onto"
          % os.path.basename(p))
    print("  the last line and, if that line is a comment, skipped without a word. Use "
          "dispositions.append().")


def load(db):
    """All rows for `db`, as a list of dicts. A missing file is no rows, not an error."""
    p = path_for(db)
    rows = []
    if not os.path.exists(p):
        return rows
    with open(p, "rb") as _f:
        _b = _f.read()
    if _b and not _b.endswith(b"\n"):
        _warn_terminator(p)
    for n, line in enumerate(io.open(p, encoding="utf-8", errors="replace")):
        if line.startswith("#") or not line.strip():
            continue
        c = line.rstrip("\r\n").split("\t")
        # THE HEADER IS NOT ALWAYS LINE 0: the registry opens with `#` notes, and the old `n == 0` test
        # loaded the header as a row with gate "gate" (harmless to gates, listed by the CLI as a row).
        if c[0].strip() == "gate" and len(c) > 1 and c[1].strip() == "subject":
            continue
        if len(c) < len(COLUMNS):
            c += [""] * (len(COLUMNS) - len(c))
        rows.append(dict(zip(COLUMNS, [x.strip() for x in c])))
    return rows


def append(db, row, verify=True):
    """Append one disposition row and PROVE IT READS BACK. Returns the row as load() sees it.

    `row` is a dict over COLUMNS or a sequence in COLUMNS order. This exists because the obvious
    append is wrong: the file may not end with a newline, and its last line is usually a `#` note,
    so the obvious append makes the new row part of that comment and load() drops it. Three things
    are therefore done here and nowhere else - normalise the terminator, follow the file's own line
    ending, and read the row back before returning. The read-back is the point: an append that
    cannot be read back raises, instead of leaving a verdict that no run will ever consult.

    It does NOT sign anything. A row appended with an empty reviewer is UNREVIEWED and suppresses
    nothing, which is the intended state for a verdict its author has just written.
    """
    if isinstance(row, dict):
        row = dict(row)
        row.setdefault("review_record", "")   # an author's new row has no review yet
        missing = [c for c in COLUMNS if c not in row]
        if missing:
            raise ValueError("append: missing column(s): %s" % ", ".join(missing))
        cells = [str(row[c]) for c in COLUMNS]
    else:
        cells = [str(c) for c in row]
        if len(cells) == len(COLUMNS) - 1:
            cells.append("")
        if len(cells) != len(COLUMNS):
            raise ValueError("append: %d cells, expected %d" % (len(cells), len(COLUMNS)))
    for name, c in zip(COLUMNS, cells):
        if "\t" in c or "\n" in c or "\r" in c:
            raise ValueError("append: %s contains a tab or a newline" % name)
    if not cells[0].strip():
        raise ValueError("append: a row with no gate is a row no gate will consult")
    if cells[0].lstrip().startswith("#"):
        raise ValueError("append: a gate name starting with # would make the row a comment")

    p = path_for(db)
    blob = open(p, "rb").read() if os.path.exists(p) else b""
    eol = "\r\n" if blob.count(b"\r\n") else "\n"
    with io.open(p, "a", encoding="utf-8", newline="") as f:
        if blob and not blob.endswith(b"\n"):
            f.write(eol)
        f.write("\t".join(cells) + eol)

    if not verify:
        return None
    back = [r for r in load(db)
            if r["gate"] == cells[0].strip() and r["subject"] == cells[1].strip()
            and r["evidence_sha256"] == cells[2].strip()]
    if not back:
        raise IOError("append: the row was written to %s and does not read back. Do not assume it "
                      "is there - a row load() cannot see suppresses nothing and is reported in no "
                      "state at all." % p)
    return back[-1]


class Registry(object):
    """The dispositions for one gate, with the state of each lookup recorded for reporting."""

    def __init__(self, db, gate):
        self.gate = gate
        self.db = db
        self.rows = [r for r in load(db) if r["gate"] == gate]
        self.by_subject = {}
        for r in self.rows:
            self.by_subject.setdefault(r["subject"], []).append(r)
        self.applied, self.lapsed, self.unreviewed, self.unrecorded = [], [], [], []
        self._record_memo = {}
        # EVERY SUBJECT THIS RUN ASKED ABOUT. A row whose subject is never asked about is neither
        # APPLIED nor LAPSED nor UNREVIEWED - it is INVISIBLE, because report() can only describe
        # lookups that happened. That is the hole FABLE found in
        # FABLE-CONTRA-OPUS-A-LINE-KEYED-DISPOSITION-GOES-INVISIBLE-RATHER-THAN-LAPSING, and it is
        # general: it bites any gate whose subject encodes something that drifts.
        self.consulted = set()

    def state(self, subject, *evidence):
        """APPLIED, LAPSED, UNREVIEWED or None, recording the lookup for the report."""
        self.consulted.add(subject)
        cands = self.by_subject.get(subject)
        if not cands:
            return None
        want = digest(*evidence)
        # A REVIEWED MATCH WINS OVER AN UNREVIEWED ONE. This loop used to return at the FIRST row
        # whose hash matched, so an unsigned row written earlier shadowed every later row for the
        # same evidence: a second author's row, even once a non-author signed it, could never apply
        # (SWE2-ORACLE, pass-6 dispositions 2026-09-30, reproduced on a copy). Now every matching row
        # is considered and any valid reviewed one applies; only when none is valid is the page
        # UNREVIEWED. OPUS, 2026-09-30.
        matches = [r for r in cands if r["evidence_sha256"] == want]
        signed = [r for r in matches
                  if r["reviewer"] and r["reviewer"] != r["author"] and r["verdict"] in VERDICTS]
        for r in signed:
            # A SIGNATURE IS NOT A REVIEW UNTIL THE REVIEW IS RECORDED (2026-10-01, OPUS, on
            # FRONTIER-REQ-OPUS-DISPOSITIONS-RECORD-GATE-1001): the row must name where.
            if self.record_problem(r) is None:
                self.applied.append((subject, r))
                return APPLIED
        if signed:
            self.unrecorded.append((subject, signed[0], self.record_problem(signed[0])))
            return UNRECORDED
        if matches:
            self.unreviewed.append((subject, matches[0]))
            return UNREVIEWED
        # The subject is known but nothing matches the evidence in front of us.
        self.lapsed.append((subject, cands[0], want))
        return LAPSED

    def record_problem(self, r):
        key = r.get("review_record", "")
        if key not in self._record_memo:
            self._record_memo[key] = record_problem(self.db, key)
        return self._record_memo[key]

    def suppressed(self, subject, *evidence):
        """True only for a reviewed disposition given for exactly this evidence."""
        return self.state(subject, *evidence) == APPLIED

    def report(self):
        """The lines a gate should print. Silence about a lapse is how a blindfold survives."""
        out = []
        if self.applied:
            out.append("  %d finding(s) suppressed by a reviewed disposition:" % len(self.applied))
            for subject, r in self.applied:
                out.append("      %s  %s (%s, reviewed by %s, %s)"
                           % (subject, r["verdict"], r["author"], r["reviewer"], r["dated"]))
        if self.unreviewed:
            out.append("  %d disposition(s) NOT APPLIED - no independent reviewer:"
                       % len(self.unreviewed))
            for subject, r in self.unreviewed:
                out.append("      %s  author %s, reviewer %r" % (subject, r["author"],
                                                                 r["reviewer"]))
        if self.unrecorded:
            out.append("  %d disposition(s) NOT APPLIED - signed, but no durable review record:"
                       % len(self.unrecorded))
            for subject, r, why in self.unrecorded:
                out.append("      %s  author %s, reviewer %s: %s" % (subject, r["author"],
                                                                      r["reviewer"], why))
        if self.lapsed:
            out.append("  %d disposition(s) LAPSED - the evidence moved since the verdict, so the"
                       % len(self.lapsed))
            out.append("  finding is reported again rather than suppressed:")
            for subject, r, now in self.lapsed:
                out.append("      %s  judged %s by %s on %s against evidence %s; now %s"
                           % (subject, r["verdict"], r["author"], r["dated"],
                              r["evidence_sha256"], now))
        # ORPHANED: a row this gate owns that NOTHING ASKED ABOUT this run. Added 2026-09-16 on
        # FABLE-CONTRA-OPUS-A-LINE-KEYED-DISPOSITION-GOES-INVISIBLE-RATHER-THAN-LAPSING. An orphan
        # suppresses nothing, so it is not a blindfold - but it cannot be SEEN to have gone stale
        # either, and the same false positive will be re-adjudicated from scratch with nobody aware
        # a verdict already existed. Over a thirty-run streak that is exactly the cost this registry
        # exists to remove. SILENCE ABOUT A LAPSE IS HOW A BLINDFOLD SURVIVES, and silence about a
        # row nobody looked up is the same silence one step further out.
        orphans = [r for r in self.rows if r["subject"] not in self.consulted]
        if orphans:
            # DORMANT AND MIS-KEYED LOOK IDENTICAL FROM THE ROW AND ARE NOT THE SAME PROBLEM, so
            # they are told apart by whether the gate asked about ANYTHING this run. A clean gate
            # leaves every row unconsulted and none of them is broken; a gate that found findings
            # and still never asked about this subject has a subject that no longer matches.
            if not self.consulted:
                out.append("  %d disposition(s) DORMANT - this gate reported no findings at all"
                           % len(orphans))
                out.append("  this run, so nothing was looked up. The row is not mis-keyed and is")
                out.append("  not suppressing anything; it is a judgement kept in case the finding")
                out.append("  returns. Retire it only when the finding is established as gone:")
            else:
                out.append("  %d disposition(s) ORPHANED - this gate DID report findings but never"
                           % len(orphans))
                out.append("  looked this subject up, so the row can neither apply nor lapse.")
                out.append("  The subject almost certainly encodes something that drifted (a line")
                out.append("  number is not stable across an edit above it); re-key or retire it:")
            for r in orphans:
                out.append("      %s  judged %s by %s on %s"
                           % (r["subject"], r["verdict"], r["author"], r["dated"]))
        return out


def self_test():
    """Both ways on every property, because each failure direction is a different disaster."""
    import tempfile
    db = tempfile.mkdtemp(prefix="disp-")
    os.makedirs(os.path.join(db, "_index", "candidates"))
    ev = "line 416 says 02CA8F38 is never written"
    good = digest(ev)
    rec = "_index/candidates/review-x/REVIEW.md"
    os.makedirs(os.path.join(db, "_index", "candidates", "review-x"))
    io.open(os.path.join(db, rec), "w", encoding="utf-8").write("# Review\n## doc::A signed\n")
    io.open(path_for(db), "w", encoding="utf-8").write(
        "\t".join(COLUMNS) + "\n" +
        "\t".join(["g.py", "doc::A", good, "SCOPED", "OPUS", "FABLE", "2026-09-15", "scoped",
                   rec + "#doc::A signed"]) + "\n" +
        "\t".join(["g.py", "doc::B", good, "SCOPED", "OPUS", "OPUS", "2026-09-15", "self", rec]) + "\n" +
        "\t".join(["g.py", "doc::C", good, "SCOPED", "OPUS", "", "2026-09-15", "none", rec]) + "\n" +
        "\t".join(["g.py", "doc::D", good, "NOT-A-VERDICT", "OPUS", "FABLE", "2026-09-15", "x", rec]) + "\n" +
        # THE RECORD RULE, every way it can fail (2026-10-01): a signature alone never applies.
        "\t".join(["g.py", "doc::R0", good, "SCOPED", "OPUS", "FABLE", "2026-09-30", "8 cells, no record"]) + "\n" +
        "\t".join(["g.py", "doc::R1", good, "SCOPED", "OPUS", "FABLE", "2026-09-30", "missing file",
                   "_index/candidates/review-gone/REVIEW.md"]) + "\n" +
        "\t".join(["g.py", "doc::R2", good, "SCOPED", "OPUS", "FABLE", "2026-09-30", "wrong heading",
                   rec + "#doc::R2 signed"]) + "\n" +
        "\t".join(["g.py", "doc::R3", good, "SCOPED", "OPUS", "FABLE", "2026-09-30", "outside the db",
                   "../outside.md"]) + "\n" +
        "\t".join(["g.py", "doc::R4", good, "SCOPED", "OPUS", "FABLE", "2026-09-30", "bad commit",
                   "commit:not-a-hash"]) + "\n" +
        "\t".join(["g.py", "doc::R5", good, "SCOPED", "OPUS", "FABLE", "2026-09-30", "a file, no fragment",
                   rec]) + "\n")
    io.open(os.path.join(os.path.dirname(db), "outside.md"), "w", encoding="utf-8").write("x\n")
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("  FAIL %-52s got %r, want %r" % (label, got, want))
        else:
            print("  ok   %-52s %r" % (label, got))

    r = Registry(db, "g.py")
    check("reviewed + evidence unchanged -> applied", r.state("doc::A", ev), APPLIED)
    check("reviewed + EVIDENCE CHANGED -> lapsed", r.state("doc::A", ev + " and more"), LAPSED)
    check("author reviewed their own -> not applied", r.state("doc::B", ev), UNREVIEWED)
    check("no reviewer named -> not applied", r.state("doc::C", ev), UNREVIEWED)
    check("unknown verdict word -> not applied", r.state("doc::D", ev), UNREVIEWED)
    check("signed, no review_record -> not applied", r.state("doc::R0", ev), UNRECORDED)
    check("signed, record file missing -> not applied", r.state("doc::R1", ev), UNRECORDED)
    check("signed, heading not in the record -> not applied", r.state("doc::R2", ev), UNRECORDED)
    check("signed, record outside the database -> not applied", r.state("doc::R3", ev), UNRECORDED)
    check("signed, malformed commit -> not applied", r.state("doc::R4", ev), UNRECORDED)
    check("signed, existing record, no fragment -> applied", r.state("doc::R5", ev), APPLIED)
    check("suppressed() is false when unrecorded", r.suppressed("doc::R0", ev), False)
    check("the report names the unrecorded rows", any("no durable review record" in l
                                                      for l in r.report()), True)
    check("a subject with no row -> nothing", r.state("doc::MISSING", ev), None)
    check("suppressed() is true ONLY for applied", r.suppressed("doc::A", ev), True)
    check("suppressed() is false for a lapse", r.suppressed("doc::A", "moved"), False)
    check("suppressed() is false when unreviewed", r.suppressed("doc::B", ev), False)
    check("another gate sees none of it", Registry(db, "other.py").rows, [])
    check("whitespace reflow does NOT lapse a row",
          digest("a  b\n c") == digest("a b c"), True)
    check("a word change DOES lapse a row", digest("a b c") == digest("a b d"), False)
    check("the report names the lapse", any("LAPSED" in l for l in r.report()), True)

    # SHADOWING, both ways (2026-09-30). An unsigned row BEFORE a signed row for the same evidence
    # must not hide the signed one; and two unsigned rows must still read UNREVIEWED, never APPLIED.
    db3 = tempfile.mkdtemp(prefix="disp-shadow-")
    os.makedirs(os.path.join(db3, "_index", "candidates"))
    io.open(os.path.join(db3, "_index", "REVIEW.md"), "w", encoding="utf-8").write("# r\n")
    io.open(path_for(db3), "w", encoding="utf-8").write(
        "\t".join(COLUMNS) + "\n" +
        "\t".join(["g.py", "doc::S", good, "SCOPED", "OPUS", "", "2026-09-30", "unsigned first"]) + "\n" +
        "\t".join(["g.py", "doc::S", good, "SCOPED", "SWE2-ORACLE", "FABLE", "2026-09-30", "signed second",
                   "_index/REVIEW.md"]) + "\n" +
        "\t".join(["g.py", "doc::U", good, "SCOPED", "OPUS", "", "2026-09-30", "unsigned"]) + "\n" +
        "\t".join(["g.py", "doc::U", good, "SCOPED", "SWE2-ORACLE", "SWE2-ORACLE", "2026-09-30", "self"]) + "\n")
    r3 = Registry(db3, "g.py")
    check("a signed row after an unsigned duplicate APPLIES", r3.state("doc::S", ev), APPLIED)
    check("two rows neither validly signed stay UNREVIEWED", r3.state("doc::U", ev), UNREVIEWED)

    # THE TERMINATOR TRAP, REPRODUCED BEFORE IT IS FIXED. A registry whose last line is a `#` note
    # and which does not end with a newline turns the next naive append into part of that comment,
    # where load() drops it without a word. This asserts the trap is real and then that append()
    # survives it - the same both-directions discipline as every check above, because a fix with no
    # demonstration of the failure is a claim rather than a test.
    db2 = tempfile.mkdtemp(prefix="disp-eol-")
    os.makedirs(os.path.join(db2, "_index", "candidates"))
    io.open(path_for(db2), "w", encoding="utf-8", newline="").write(
        "\t".join(COLUMNS) + "\n" +
        "\t".join(["g.py", "doc::A", good, "SCOPED", "OPUS", "FABLE", "2026-09-15", "scoped"]) +
        "\n# a retirement note, and NO trailing newline")
    naive = ["g.py", "doc::EOL", good, "SCOPED", "OPUS", "FABLE", "2026-09-18", "naive append"]
    io.open(path_for(db2), "a", encoding="utf-8", newline="").write("\t".join(naive) + "\n")
    check("a naive append after a comment with no final newline VANISHES",
          [x for x in load(db2) if x["subject"] == "doc::EOL"], [])
    back = append(db2, ["g.py", "doc::EOL2", good, "SCOPED", "OPUS", "", "2026-09-18", "append()"])
    check("append() repairs the terminator and the row reads back",
          back["subject"] if back else None, "doc::EOL2")
    check("append() does not sign: an empty reviewer stays UNREVIEWED",
          Registry(db2, "g.py").state("doc::EOL2", ev), UNREVIEWED)
    try:
        append(db2, ["g.py", "doc::TAB", good, "SCOPED", "OPUS", "", "2026-09-18", "a\treason"])
        check("append() refuses a field containing a tab", "accepted", "ValueError")
    except ValueError:
        check("append() refuses a field containing a tab", "ValueError", "ValueError")
    return ok


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        print("dispositions self-test")
        sys.exit(0 if self_test() else 1)
    db = "Database/FFXII TZA"
    if "--db" in sys.argv:
        db = sys.argv[sys.argv.index("--db") + 1]
    rows = load(db)
    print("%d disposition(s) in %s" % (len(rows), path_for(db)))
    for r in rows:
        if not (r["reviewer"] and r["reviewer"] != r["author"]):
            flag = "   <- NOT APPLIED, no reviewer"
        else:
            why = record_problem(db, r.get("review_record", ""))
            flag = "" if why is None else "   <- NOT APPLIED, unrecorded: %s" % why
        print("  %-28s %-34s %s%s" % (r["gate"], r["subject"], r["verdict"], flag))
