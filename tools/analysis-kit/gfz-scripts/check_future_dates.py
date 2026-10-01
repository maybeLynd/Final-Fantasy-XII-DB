#!/usr/bin/env python3
"""check_future_dates.py - a date attached to a PAST act may not name a day that has not happened.

EVIDENCE-STANDARD addendum 2026-09-14bg rules that "a ratio against a moving denominator must carry
its date". That makes a date label evidence about WHEN a figure was true, and a label ahead of the
day it was written destroys the only thing it was for: two documents dated a day apart may then be
simultaneous, and one dated later may be the earlier reading.

The defect is real and it is large. This checker was written after finding 687 such labels across
259 documents, 244 of them in a heading, a ruling or a measurement stamp - including OPUS's own
transfer stamp, repeated across 243 pages.

WHY A DATE COMPARISON ALONE IS THE WRONG TEST
---------------------------------------------
Six of those 687 are CORRECT. `_inbox/TEAM.md` says ASTRA is "unavailable to about 2026-09-19" - a
staffing window, a date that is SUPPOSED to be in the future, and flagging it would be the checker
telling the truth to shut up. So the test is not "is this date ahead of today". It is:

    does the sentence attach this date to something ALREADY DONE?

  RETROSPECTIVE   ruled, measured, reviewed, closed, published, bound, disassembled, stamped,
                  superseded, withdrawn, recorded, or a bare heading/stamp date  -> RED if future
  PROSPECTIVE     until, by, before, after, reset, deadline, window, unavailable, scheduled,
                  expires, due, pending, "~"                                     -> never red

PROSPECTIVE wins when both appear, because "closed until 2026-09-19" is a window, not a claim that
closing happened. That asymmetry is deliberate and is the only way this stays quiet about the six.

NOT A GATE PASS. Like check_banned_evidence, this is a diagnostic that can run long before the
terminal gate, because a wrong date is cheap to fix today and expensive to trust later.
"""
import argparse
import collections
import datetime
import io
import os
import re
import sys

DATE = re.compile(r"\b(20\d\d)-(\d{2})-(\d{2})\b")

# The date is attached to something already done.
RETRO = re.compile(
    r"\b(?:ruled?|ruling|adjudicat\w*|measur\w*|review\w*|last_reviewed|closed?|publish\w*|"
    r"bound|disassembl\w*|stamp\w*|supersed\w*|withdraw\w*|withdrawn|recorded?|ran|run on|"
    r"as of|dated|established|verified|derived|re-derived|landed|committed)\b", re.I)

# The date names something that has not happened yet, and is therefore allowed to be in the future.
#
# THE MARKER MUST BE NEXT TO THE DATE, not merely on the line. The first version searched the whole
# line and `by` silently swallowed every "*(Ruled by OPUS 2026-09-15)*" stamp in the corpus - 70
# PROSPECTIVE where only 6 are real. A checker whose escape hatch is the word `by` reports nothing.
PROSPECTIVE_NEAR = re.compile(
    r"\b(?:until|till|by|before|after|through|to about|to|no earlier than|not until|"
    r"scheduled for|due|expires?|resumes?|returns?|reopens?|eta)\s*(?:~|about|approx\.?|circa)?\s*$",
    re.I)
# A window word anywhere on the line is enough on its own - "ASTRA runtime queue - temporary
# (ASTRA unavailable until ~2026-09-19 reset)" is a window however it is punctuated.
PROSPECTIVE_LINE = re.compile(
    r"\b(?:unavailable|deadline|usage reset|usage window|\w+ window|staffing|out of office|"
    r"not before|embargo\w*)\b", re.I)
# "this sentence READ 'three' UNTIL 2026-09-15" is a CORRECTION RECORD, not a window: the same word
# `until` bounds a past state. A past-tense verb ahead of the marker demotes it back.
PAST_IDIOM = re.compile(
    r"\b(?:read|said|stood|was|were|had|has said|remained|carried|showed|claimed|listed)\b", re.I)
NEAR = 28   # characters of context before the date that the marker must sit in

# A heading or a parenthetical stamp whose date is the whole point - "## ... - 2026-09-16 (TAG)",
# "*(2026-09-16 - FRONTIER ...)*". These carry no verb and are retrospective by construction.
BARE_STAMP = re.compile(r"^\s*(?:#{1,6}\s|\*?\(\s*20\d\d-\d{2}-\d{2}\b)")

SKIP_DIRS = {".git", "__pycache__", "_templates"}
EXTS = (".md", ".tsv")


# `| `2026-09-19` | 6 |` - a markdown row whose whole first cell is a date and whose second is a
# bare count. The date is the bucket, not a label on an act.
TALLY_ROW = re.compile(r"^\|\s*`?\d{4}-\d{2}-\d{2}`?\s*\|\s*\*{0,2}[\d,]+\*{0,2}\s*\|?\s*$")


def classify(line, at=None):
    """PROSPECTIVE / RETROSPECTIVE / UNMARKED for one future date on one line.

    `at` is the offset of the date; the prospective marker is looked for in the NEAR characters
    before it, so "by 2026-09-19" is a window and "Ruled by OPUS 2026-09-15" is not."""
    if at is None:
        m = DATE.search(line)
        at = m.start() if m else len(line)
    before = line[max(0, at - NEAR):at].rstrip("~ \t(")
    # A DATE THAT IS A TABLE KEY WITH A COUNT IS A TALLY, NOT A STAMP ON AN ACT. EVIDENCE-STANDARD
    # records a past run of THIS checker as a "by date" table, and the row `| `2026-09-19` | 6 |`
    # was the single UNMARKED finding - the document that explains the checker, reported by the
    # checker. The date labels nothing; it is the bucket a count sits in, and a reader asked to
    # judge it has nothing to judge.
    #
    # Third instance of this shape in one day: a fragment quoted by the page about substring
    # accounting, a dots-only link written by the page documenting dots-only links, and now a date
    # tallied by the page tabulating dates. A gate that cannot tell a reference from an assertion
    # will always report the documents whose subject is the distinction. 2026-09-16, OPUS.
    if TALLY_ROW.match(line.strip()):
        return "TALLY"
    if PROSPECTIVE_LINE.search(line):
        return "PROSPECTIVE"
    if PROSPECTIVE_NEAR.search(before):
        # A past-tense verb ahead of the marker makes it a correction record, and the verb is then
        # itself the retrospective marker - not merely a reason to withhold PROSPECTIVE.
        return "RETROSPECTIVE" if PAST_IDIOM.search(line[:at]) else "PROSPECTIVE"
    if RETRO.search(line) or BARE_STAMP.match(line):
        return "RETROSPECTIVE"
    return "UNMARKED"


def sweep(db, today):
    counts = collections.Counter()
    per_date = collections.Counter()
    per_doc = collections.Counter()
    findings = []
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.lower().endswith(EXTS):
                continue
            p = os.path.join(root, fn)
            try:
                text = io.open(p, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            rel = os.path.relpath(p, db).replace("\\", "/")
            for i, line in enumerate(text.splitlines(), 1):
                for m in DATE.finditer(line):
                    try:
                        d = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                    except ValueError:
                        continue          # 2026-13-40 is a typo, not a date; a different check
                    if d <= today:
                        continue
                    kind = classify(line, m.start())
                    counts[kind] += 1
                    per_date[d.isoformat()] += 1
                    if kind not in ("PROSPECTIVE", "TALLY"):
                        per_doc[rel] += 1
                        findings.append((rel, i, d.isoformat(), kind, line.strip()))
    return counts, per_date, per_doc, findings


def self_test():
    """The classifier separates a staffing window from a measurement stamp, or its count is noise."""
    cases = [
        ("### Staffing - ASTRA usage window, unavailable to about 2026-09-19", "PROSPECTIVE"),
        ("# ASTRA runtime queue - temporary (ASTRA unavailable until ~2026-09-19 reset)",
         "PROSPECTIVE"),
        ("adjudicated: OPUS ruling 2026-09-15, _index/PROVENANCE-TRANSFER.md", "RETROSPECTIVE"),
        ("last_reviewed: 2026-09-16", "RETROSPECTIVE"),
        ("## The `008C5760` vtable's no-caller members, bound - 2026-09-16 (NOCALLER)",
         "RETROSPECTIVE"),
        ("*(2026-09-16, FRONTIER - LAYOUT-KEY-READERS.)*", "RETROSPECTIVE"),
        ("was disassembled from the shipping image within its declared extent (2026-09-16)",
         "RETROSPECTIVE"),
        ("the figure holds 2026-09-15 and nothing else", "UNMARKED"),
        # the asymmetry, stated as a case: a retrospective verb inside a window is still a window
        ("the register is closed until 2026-09-19", "PROSPECTIVE"),
        # THE REGRESSION THIS CHECKER WAS REWRITTEN FOR. `by` on the line, nowhere near the date:
        # searching the whole line for it filed every ruling stamp in the corpus as a deadline.
        ("*(Ruled by OPUS 2026-09-15. The schema and the vocabulary are settled here.)*",
         "RETROSPECTIVE"),
        ("measured by Tools/work/OPUS/measure_entry_only_sizes.py on 2026-09-15", "RETROSPECTIVE"),
        # `until` bounding a PAST state, which is a correction record and not a window. Both of the
        # corpus's instances are of exactly this shape and the first classifier let both through.
        ('this sentence read "four of those libraries" until 2026-09-15 above a table of five',
         "RETROSPECTIVE"),
        ("- **ASTRA window (until ~2026-09-19 reset):** not an eligible dependency", "PROSPECTIVE"),
        # A by-date TALLY row: the date is the bucket a count sits in, not a label on an act.
        ("| `2026-09-19` | 6 |", "TALLY"),
        ("| `2026-09-19` | **6** |", "TALLY"),
        # ... but a date key with PROSE beside it is still a claim and must not be excused.
        ("| `2026-09-19` | the day the window closes |", "PROSPECTIVE"),
    ]
    bad = 0
    for text, want in cases:
        got = classify(text)
        if got != want:
            bad += 1
            print("  SELF-TEST FAIL: %r -> %s, wanted %s" % (text, got, want))
    print("self-test: %d of %d cases correct" % (len(cases) - bad, len(cases)))
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list", action="store_true", help="print every finding")
    ap.add_argument("--today", help="override today, as YYYY-MM-DD, to test the sweep")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.db:
        return ap.error("--db or --self-test required")

    today = (datetime.date(*[int(x) for x in a.today.split("-")]) if a.today
             else datetime.datetime.now(datetime.timezone.utc).date())
    counts, per_date, per_doc, findings = sweep(a.db, today)

    print("future-dated labels - a date on a past act, naming a day that has not happened")
    print("  today, UTC: %s\n" % today)
    print("  RETROSPECTIVE %4d   a ruling, measurement or review stamp  <- the finding"
          % counts["RETROSPECTIVE"])
    print("  UNMARKED      %4d   no verb either way; a reader must judge" % counts["UNMARKED"])
    print("  PROSPECTIVE   %4d   a window or deadline - correctly in the future, NOT a finding"
          % counts["PROSPECTIVE"])
    print("  TALLY         %4d   a by-date table row - the date is a bucket, not a label"
          % counts["TALLY"])
    print("\n  in %d document(s), by date:" % len(per_doc))
    for k, v in sorted(per_date.items()):
        print("     %s   %4d" % (k, v))
    if per_doc:
        print("\n  heaviest documents:")
        for k, v in per_doc.most_common(10):
            print("     %4d  %s" % (v, k))
    if a.list:
        for rel, i, d, kind, line in findings:
            print("\n  %s:%d  [%s %s]\n    %s" % (rel, i, d, kind, line[:220]))
    print("\n  CONTROL: the ASTRA staffing window - 'unavailable to about 2026-09-19' - is a date")
    print("  that SHOULD be in the future. If PROSPECTIVE reads 0 while a staffing window is open,")
    print("  the classifier has collapsed and the count above is a count of nothing.")
    return 1 if (counts["RETROSPECTIVE"] or counts["UNMARKED"]) else 0


if __name__ == "__main__":
    sys.exit(main())
