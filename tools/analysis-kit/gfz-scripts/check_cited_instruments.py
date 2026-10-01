#!/usr/bin/env python3
"""check_cited_instruments.py - canonical indexes quoting a tool no peer has.

WHY THIS EXISTS. Two instruments were found in `Database/Tools/work/` on 2026-09-14, each producing
a table that a canonical index quotes as a current figure:

  final_audit_verdicts.py   FINAL-AUDIT-PROTOCOL quotes "27 clean, 1 would fail, 1 PARTIAL, 1 manual"
  gap_shapes.py             TYPE-COVERAGE quotes "PAD 141 / INTERIOR 112 / TAIL 25 / OUTSIZED 2"

`Database/Tools/.gitignore` excludes `work/`, so **both pages were citing a number nobody else could
reproduce.** That is the index-consistency criterion failing through the tooling rather than the
prose, and finding the second one by accident an hour after the first is not a method.

WHAT IS AND IS NOT A DEFECT, because the naive version of this check is almost all noise. A citation
is only a problem when a reader could be expected to RUN the tool and cannot. Three things look
identical to a substring match and are not:

  a tool tracked SOMEWHERE ELSE       the index cites `Reconstruction/Tests/Differential/
                                      diff_angle_wrap.py`; a staging COPY also sits under
                                      `work/OPUS/litsuffix/.../inputs/`.  The cited file is in git.
  a dated log entry                   `AUDIT-LOG.md` records what was run on a date.  A log naming
                                      a scratch tool is the log doing its job, not a broken pointer.
  an attribution                      `EVIDENCE-STANDARD` names ASTRA's probes in a "Who produces
                                      it" column of a hashing-convention table.  That says who
                                      emits a convention; it does not ask anyone to run anything.

THE SWEEP OVER-REPORTED FOUR TIMES, and the numbers matter more than the final one:

  39   naked substring matching - `bp.py` matched `check_ebp.py`, `scan.py` matched
       `record_field_scan.py`, `refs.py` matched `audit_crossrefs.py`
  17   after requiring a word boundary before the name
   5   after asking git whether that BASENAME is tracked anywhere, which cleared every
       `diff_*.py` and `select_generated_adapters.py`
   6   after adding dated-heading and attribution tests - it went UP, because those tests also
       surfaced two mentions the earlier list had never reached

**AND THE LAST STEP IS NOT MECHANICAL, WHICH IS THE REAL FINDING.** The remaining mentions are all
non-defects and no pattern says so:

  `AUDIT-LOG.md:8133`  *"A scratch helper named `dis.py` shadowed the standard library's `dis`"* -
                       prose ABOUT a tool that caused a bug, not a pointer TO a tool.
  `EVIDENCE-STANDARD.md:497`  the four ASTRA probes sit in a table whose COLUMN HEADER is
                       "Who produces it".  The attribution is a property of the column, one row
                       above; no line-scoped test can see it.
  `GOAL-REVISION-2026-09-08.md:105`  the FILENAME carries the date.  `check_index_figures` learned
                       that months-equivalent ago and this tool did not inherit it - now fixed.

So the tool classifies what it can mechanically - tracked elsewhere, dated heading, dated filename,
attribution - and the last step is a **NAMED LIST** (`READ`) of mentions read by hand, each with its
reason, not a pattern.  Anything outside that list is a QUESTION nobody has read yet, which is the
only thing this can honestly report.

**AND THE FIRST ATTEMPT AT THAT LAST STEP WAS WRONG IN A WAY WORTH RECORDING.** I widened the
attribution regex with `named\\s+`` and `shadowed` until the unclassified count reached 0 - patterns
fitted to the three lines I wanted gone.  That is making a metric agree by weakening the test, and
it is worse than a false positive, because those patterns would silently clear FUTURE rows nobody
had read.  Reverted; the readings are named instead.  **Telling a live instruction from a mention is
a reading, and a sweep that reports 39 when the answer is 0 needs a definition, not a tighter
regex.**

CONTROL: the two known instances are asserted by name.  Both now live in the kit, so both must come
back CLEAN - and if either is ever moved back under `work/`, this fails.  A checker whose subject
has been fixed must still be able to prove it would catch the fix being undone.
"""
import argparse
import collections
import io
import os
import re
import subprocess
import sys

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")
WORK = os.path.join(REPO, "Database", "Tools", "work")

# A name, not preceded by anything that would make it the tail of a longer name - and NOW ALSO
# matching a PATH-QUALIFIED citation, which the first version could not see at all.
#
# THE FIRST VERSION WAS A FALSE NEGATIVE AND IT INVALIDATED THIS FILE'S OWN HEADLINE. The lookbehind
# `(?<![\w./-])` was added to stop `bp.py` matching inside `check_ebp.py`, and it worked - but it
# also excluded a preceding `/`, so every citation written as a PATH was invisible:
#
#     "Re-run Tools/work/OPUS/nowriter_claims_blind_census.py to re-test that."   <- not seen
#     "work/OPUS/parent_delta.py recomputes the ..."                              <- not seen
#
# That is the most explicit way anyone cites a tool, and it is exactly the form a checker uses when
# it tells a reader to run something. This file reported "0 unread - the class is closed" on
# 2026-09-14 while blind to it. **A false negative in a gate is worse than a false positive: the
# false positive gets read, the false negative gets believed.**
#
# Found by following an unrelated standing red - check_census_writers names that very tool in its
# own output - rather than by testing this pattern, which is the second time in one day that a
# sweep of mine was corrected by something it was not looking at.
NAME = re.compile(r"(?<![\w-])(?:[\w.\\/-]*[\\/])?([A-Za-z_][\w-]*\.py)\b")
DATED_HEAD = re.compile(r"^#{1,4}\s.*20\d\d-\d\d-\d\d")
# "Who produces it", "produced by", "publishes" - the line credits a tool rather than invoking it.
# DELIBERATELY NARROW. An earlier revision of this file widened it with `named\s+`` and
# `shadowed` until the unclassified count reached 0 - patterns fitted to the three lines I
# wanted gone. That is making a metric agree by weakening the test, which this standard forbids,
# and it is worse here than a false positive because it would silently clear future rows too.
# The three readings live in READ below, named, with their reasons.
ATTRIBUTION = re.compile(r"who produces|produced by|publish(es)?\b|emitted by|its author", re.I)

# A TOOL RECORDING WHERE IT WAS MOVED FROM CITES ITS OWN OLD PATH, and that old path is untracked
# BY CONSTRUCTION - the move is what made it tracked. So doing the right thing (saying plainly
# "this was at Tools/work/OPUS/x.py, which .gitignore excludes") manufactures a hit in the very
# checker that exists to find the wrong thing. Three files carry such a line, all written today
# and all deliberate.
FORMER_NAME = re.compile(r"published into the kit|published \d{4}-\d\d-\d\d from|was named|"
                         r"it lived at|renamed|until 20\d\d-\d\d-\d\d", re.I)

# A TEST THAT CREATES A FILE IS NOT CITING A TOOL. `test_publication_extractors.py` writes
# one.py, single.py, multi.py, late.py, nested.py and broken.py into a temp folder as FIXTURES -
# they are inputs it invents, not instruments anyone is asked to run, and they are untracked
# because they never exist outside that test.
FIXTURE = re.compile(r"\.write_text\(|write_text|tmp_path|/ *'[\w.-]+\.py'|\bfolder\b", re.I)

# AND A CHECKER QUOTING ITS OWN FALSE POSITIVES NAMES THEM. This file's docstring records that
# `bp.py` matched `check_ebp.py` and `refs.py` matched `audit_crossrefs.py`; those names are the
# evidence for a lesson, not pointers.
SELF_QUOTED = re.compile(r"matched|false positive|substring|naked substring", re.I)
# A DOCUMENT NAMED FOR A DATE IS A RECORD OF THAT DATE - `GOAL-REVISION-2026-09-08.md` is the goal
# revision OF that day. check_index_figures established this and this file did not inherit it,
# which is the second time a lesson has had to be learned twice in this kit.
DATED_FILE = re.compile(r"20\d\d-\d\d-\d\d")

# AN INSTRUCTION, WHICH IS THIS FILE'S OWN DEFINITION OF THE DEFECT - applied to KIT sources only.
# An index may point at a tool by naming it; a kit file cannot, because kit files discuss tools
# constantly (this one most of all). What marks an instruction there is an imperative aimed at the
# reader. Both real instances found on 2026-09-14 had one - "Re-run X", "Regenerate with X" - and
# none of the 21 benign kit mentions does.
#
# WINDOWED, because the instruction is split across consecutive print() calls: "Re-run" sat on the
# line BEFORE the path. Two lines either side covers that and reaches no further.
IMPERATIVE = re.compile(r"\b(?:re-?run|regenerate|regen|invoke|execute|run)\b", re.I)
IMPERATIVE_WINDOW = 2

KNOWN_FIXED = ("final_audit_verdicts.py", "gap_shapes.py")

# MENTIONS READ BY HAND ON 2026-09-14 AND FOUND NOT TO BE INSTRUCTIONS. Each is listed so a re-run
# does not re-ask, and each carries the reason so the judgement can be challenged rather than
# inherited. A row NOT in this list is a question nobody has read yet - which is the only thing
# this tool can honestly tell you.
READ = {
    # THE EIGHT KIT LINES THAT QUOTE THE OLD INSTRUCTION WHILE EXPLAINING IT WAS A DEFECT.
    # Each contains a real imperative - "Re-run", "Regenerate with" - because it is QUOTING one.
    # No pattern separates a quotation of an instruction from an instruction, so these are named.
    # If one of these files ever genuinely tells a reader to run an untracked tool again, it will
    # be on a line that is not in this list.
    ("check_cited_instruments.py", "nowriter_claims_blind_census.py"):
        "this file's own docstring and comments, quoting the path-qualified citation it was blind "
        "to - the example that proves the lookbehind bug",
    ("check_cited_instruments.py", "parent_delta.py"):
        "same docstring, the second example of a path-qualified citation going unseen",
    ("check_cited_instruments.py", "dis.py"):
        "the READ table's own key, quoted in source",
    ("check_cited_instruments.py", "arena_alloc_probe.py"):
        "the READ table's own key, quoted in source",
    # AND THE LIST NAMES THE TOOL, SO THE LIST ITSELF IS A MENTION. Adding the entry above
    # created a new hit - this file now mentions `seed_doc_claim_terms.py` on the line that
    # clears it elsewhere. A self-key is self-clearing, so ONE entry closes it and the
    # recursion terminates here rather than going on forever.
    ("check_cited_instruments.py", "seed_doc_claim_terms.py"):
        "the READ table's own key, quoted in source - see the note above",
    ("check_doc_claims.py", "seed_doc_claim_terms.py"):
        "the printed note recording that this line USED to tell readers to run a gitignored file, "
        "and now names the kit tool instead",
    ("check_nowriter_claims.py", "nowriter_claims_blind_census.py"):
        "its own docstring recording the former path it was published from",
    ("gen_doc_claim_terms.py", "seed_doc_claim_terms.py"):
        "its own docstring recording the former path it was published from",
    ("AUDIT-LOG.md", "dis.py"):
        "prose ABOUT a scratch helper that shadowed the stdlib `dis` and broke capstone - a bug "
        "narrative, not a pointer to a tool anyone should run",
    ("EVIDENCE-STANDARD.md", "arena_alloc_probe.py"):
        "sits in a table whose COLUMN HEADER is 'Who produces it' - attribution for a hashing "
        "convention. The header is one row above, so no line-scoped test can see it",
    ("EVIDENCE-STANDARD.md", "arena_init_probe.py"): "same table, same column",
    ("PROVENANCE-TRANSFER.md", "check_stale_absence_after_gn161.py"):
        "the numbered note recording that this ruling USED to back 'It found none' with a gitignored "
        "one-shot, and now cites check_stranded_absence.py instead. Naming the retired tool is what "
        "makes the correction checkable - a reader can diff the two and see they are the same "
        "109-address test - so removing the name to satisfy this checker would cost the provenance "
        "the correction exists to supply. Read 2026-09-14 (OPUS) on AUDITSPEC-REQ-OPUS-STALE-ABSENCE-CITE",
    ("EVIDENCE-STANDARD.md", "cap_policy_probe.py"): "same table, same column",
    ("EVIDENCE-STANDARD.md", "efx_rebase_probe.py"): "same table, same column",
    # The same shape as the AUDITSPEC entry above, and cleared the same way: by making the FACT
    # re-derivable rather than by deleting the name of what produced it.
    # The naming of the tool IS the correction. FABLE's note records that they had attributed the
    # nine duplicate ids to gen_unidentified_questions.py and that the minting is actually
    # register_idless_boxes.py - a correction that cannot be stated without naming both scripts,
    # one of which is gitignored. Removing the name would delete the correction and leave the
    # wrong attribution standing.
    #
    # And the FACT no longer depends on the private tool: the root cause is fixed in the committed
    # kit. check_questions.read_boxes ended a block at six spaces and missed an id written on a
    # two-space continuation (9a275aaa), and could not see an id in bold-with-backticks
    # (bb411fd1). Anyone can now re-derive why the nine were minted without running anything of
    # FABLE's. Read 2026-09-16 (OPUS).
    ("OPEN-QUESTIONS.md", "register_idless_boxes.py"):
        "a correction that names the tool it is correcting - FABLE recording that the minting is "
        "register_idless_boxes.py and NOT gen_unidentified_questions.py, which they had said "
        "earlier. It is provenance and a retraction in one sentence, and the underlying defect is "
        "fixed in the committed kit (9a275aaa, bb411fd1), so the fact stands without the tool.",
    ("OPEN-QUESTIONS.md", "gen_unidentified_questions.py"):
        "the same sentence, naming the script it exonerates. That one IS in the kit.",
    ("OPEN-QUESTIONS.md", "alias_boxes.py"):
        "a DATED PROVENANCE citation, not an instruction: the row records what ran on 2026-09-14 "
        "to measure the alias boxes - 11 in 1,384 checkbox blocks - and rewriting it would falsify "
        "what ran. It was still an unreproducible figure, because Tools/work/FABLE/ is gitignored "
        "and no reader could check it. That is now fixed at the other end: check_alias_boxes.py "
        "(2fbb3210) re-measures the same census from committed data alone - a sweep of checkbox "
        "lines and the register's own verdicts - and at HEAD reports 21 alias boxes in 1,405 "
        "blocks, the figures having moved with the corpus exactly as a dated ratio should. So the "
        "private path stays as the record of what ran, and anyone who doubts the number can now "
        "take it themselves. Read 2026-09-16 (OPUS).",
}


def tracked_basenames():
    out = collections.defaultdict(list)
    r = subprocess.run(["git", "-C", REPO, "ls-files"], capture_output=True, text=True)
    for p in r.stdout.replace("\\", "/").split("\n"):
        if p.endswith(".py"):
            out[p.rsplit("/", 1)[-1]].append(p)
    return out


# SIDE FILES ARE THE THIRD POPULATION, and the sweep reported "closed" while blind to them. A
# canonical candidates file whose header says "Generated by <a gitignored tool>" is the same defect
# as an index quoting one - the reader who wants to regenerate cannot.
#
# EVIDENCE MANIFESTS ARE NOT THAT. `_experiments/evidence/**/manifest.json` records the instrument
# that produced the evidence together with its hash, which is what a manifest is for; repointing one
# at a kit tool would falsify the record of what actually ran. The test is the DIRECTORY, not a
# phrase, because that is a class a reader can check in one command rather than a regex fitted to
# the manifests that exist today.
EVIDENCE_DIR = os.path.join("_experiments", "evidence")


def side_files(db):
    """(display name, path) for every side file the sweep should read. Manifests included, so
    they are COUNTED as provenance rather than silently skipped."""
    out = []
    idx = os.path.join(db, "_index")
    for dirpath, _d, files in os.walk(idx):
        for fn in sorted(files):
            if fn.endswith(".tsv") or fn == "TEAM.json":
                p = os.path.join(dirpath, fn)
                out.append((os.path.relpath(p, db).replace(os.sep, "/"), p))
    ev = os.path.join(db, EVIDENCE_DIR)
    for dirpath, _d, files in os.walk(ev):
        for fn in sorted(files):
            if fn == "manifest.json":
                p = os.path.join(dirpath, fn)
                out.append((os.path.relpath(p, db).replace(os.sep, "/"), p))
    return out


def is_manifest(rel):
    return rel.replace("\\", "/").startswith("_experiments/evidence/") and \
        rel.endswith("manifest.json")


def is_board(rel):
    """The board names work paths in task notes; it is a log, not a publication."""
    return rel.replace("\\", "/").endswith("_inbox/TEAM.json")


def is_baseline(rel):
    """`gate-baseline.tsv` is MACHINE-WRITTEN and its last column quotes each checker's own output
    verbatim. So any checker that reports a path puts that path into the baseline, and then finds
    it there - THIS file's own finding about `check_census_writers` is now recorded in the baseline
    row for THIS file, quoting the path it reported.

    That is a real fixed point and it is not the one closed on 2026-09-14 in the READ table, where
    a self-key cleared itself and the recursion terminated. Here nothing terminates by naming a
    line, because the line is rewritten every time the baseline is refreshed - the only stable thing
    is the FILE, and the file is a record of what tools printed, exactly like an evidence manifest
    or the board. Same class, same reason: rewriting it would falsify the record.
    """
    return rel.replace("\\", "/").endswith("_index/gate-baseline.tsv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    # `run_gates.py` globs `check_*.py` and hands every corpus gate `--db <path>`. This file is
    # named `check_*` and did not accept it, so the runner got an argparse refusal and exit 2 on
    # every run - a checker that crashes every time is noise, and noise trains people to ignore
    # reds. Found by the gate suite the same day the file was published, which is the runner
    # doing its job. The value is used: it names the database root to scan.
    ap.add_argument("--db", default=DB)
    a = ap.parse_args()

    tracked = tracked_basenames()
    kit = {f for f in os.listdir(KIT) if f.endswith(".py")}

    # CONTROL - the two known instances must be in the kit and tracked, or this checker is
    # reporting clean about a subject that has silently regressed.
    for f in KNOWN_FIXED:
        if f not in kit or f not in tracked:
            print("  CONTROL FAILED: %s is not a tracked kit tool. It was moved there on "
                  "2026-09-14 precisely because an index quotes it." % f)
            return 2
    print("  control passed: both known instances are tracked kit tools.")

    idx = os.path.join(a.db, "_index")
    if not os.path.isdir(idx):
        print("no _index at %s" % idx)
        return 2

    # THE KIT ITSELF IS IN SCOPE, and leaving it out was how the one real instance survived.
    # `check_census_writers.py` ended its output with "Re-run
    # Tools/work/OPUS/nowriter_claims_blind_census.py to re-test that" - a checker telling every
    # reader of its findings to run a file `.gitignore` excludes. That is the same defect as an
    # index quoting an untracked tool and arguably worse, because the reader is someone running
    # the gates. Scanning only `_index` could never have seen it.
    sources = [(fn, os.path.join(idx, fn)) for fn in sorted(os.listdir(idx))
               if fn.endswith(".md")]
    kit_sources = {fn for fn in os.listdir(KIT) if fn.endswith(".py")}
    sources += [(fn, os.path.join(KIT, fn)) for fn in sorted(kit_sources)]
    side = side_files(a.db)
    sources += side
    side_names = {fn for fn, _p in side}

    hits, dated, attributed, elsewhere, read = [], 0, 0, 0, 0
    former = fixture = self_quoted = discussed = 0
    manifest = board = 0
    for fn, path in sources:
        if DATED_FILE.search(fn):
            dated += 1
            continue
        in_dated = False
        level = 0
        all_lines = io.open(path, encoding="utf-8", errors="replace").read().splitlines()
        is_kit = fn in kit_sources
        # THE DATED-SECTION RULE IS A MARKDOWN RULE. A `#` line in a TSV is a comment, not a
        # heading: it has no level and nothing closes it, so treating one dated comment as opening
        # a dated section excuses every citation in the file. That is exactly what happened to
        # `_index/candidates/text-gap-citations-250.tsv`, whose line 3 names a gitignored generator
        # and was filed as "a log recording what it ran" because line 3 carries a date.
        is_md = fn.endswith(".md")
        for ln, line in enumerate(all_lines, 1):
            hm = re.match(r"^(#{1,6})\s", line) if is_md else None
            if hm:
                lv = len(hm.group(1))
                if DATED_HEAD.match(line):
                    in_dated, level = True, lv
                elif in_dated and lv <= level:
                    in_dated, level = False, 0
            for nm in sorted(set(NAME.findall(line))):
                if nm in kit:
                    continue
                if tracked.get(nm):
                    elsewhere += 1
                    continue
                if in_dated:
                    dated += 1
                    continue
                if ATTRIBUTION.search(line):
                    attributed += 1
                    continue
                if (fn, nm) in READ:
                    read += 1
                    continue
                if FORMER_NAME.search(line):
                    former += 1
                    continue
                if FIXTURE.search(line):
                    fixture += 1
                    continue
                if SELF_QUOTED.search(line):
                    self_quoted += 1
                    continue
                if fn in side_names and is_manifest(fn):
                    manifest += 1
                    continue
                if fn in side_names and (is_board(fn) or is_baseline(fn)):
                    board += 1
                    continue
                if is_kit:
                    lo = max(0, ln - 1 - IMPERATIVE_WINDOW)
                    near = "\n".join(all_lines[lo:ln + IMPERATIVE_WINDOW])
                    if not IMPERATIVE.search(near):
                        discussed += 1
                        continue
                hits.append((fn, ln, nm, line.strip()[:110]))

    print("\n  cited and tracked elsewhere in the repo : %4d  (a staging copy is not the subject)"
          % elsewhere)
    print("  cited under a DATED heading            : %4d  (a log recording what it ran)" % dated)
    print("  cited as ATTRIBUTION, not an instruction: %4d" % attributed)
    print("  read by hand and cleared, with a reason : %4d" % read)
    print("  a tool naming its OWN former path       : %4d  (the move is what made it"
          % former)
    print("                                                 tracked - see FORMER_NAME)")
    print("  a test creating a fixture, not a tool   : %4d" % fixture)
    print("  a checker quoting its own false positive: %4d" % self_quoted)
    print("  kit prose DISCUSSING a tool, no imperative: %4d  (an index may point"
          % discussed)
    print("                                                  by naming; a kit file"
          " cannot)")
    print("  an EVIDENCE MANIFEST naming its instrument: %4d  (provenance, and"
          % manifest)
    print("                                                 rewriting it would"
          " falsify what ran)")
    print("  a MACHINE-WRITTEN record of what ran    : %4d  (the board's task notes and"
          % board)
    print("                                                 gate-baseline's quoted output -")
    print("                                                 records, like a manifest)")
    print("  UNREAD - a QUESTION, not a defect       : %4d" % len(hits))
    print("\n  Telling a live instruction from a mention is a READING, and the last filter here is")
    print("  a NAMED LIST rather than a pattern for exactly that reason: an earlier revision")
    print("  widened the attribution regex until this count reached 0, which is making a metric")
    print("  agree by weakening the test. The two real instances are fixed and the control above")
    print("  asserts they stay fixed.")
    if hits:
        print("\nMENTIONS OF A TOOL NOT IN THE REPOSITORY, not yet read:")
        for fn, ln, nm, text in hits:
            print("  %s:%d  %s" % (fn, ln, nm))
            print("      %s" % text)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
