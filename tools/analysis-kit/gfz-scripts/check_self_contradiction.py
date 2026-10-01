#!/usr/bin/env python3
"""check_self_contradiction.py - an absence claim refuted by the same document, elsewhere.

Why this exists
---------------
Three findings across two falsification passes on 2026-09-02 were the same shape, and it is a shape
no existing checker looks for: **a claim contradicted by the document's own adjacent section.**

  * `vbf-archive-and-st2e-tables.md` declared a "complete" set of forty authored tables and then
    spent §7 analysing `word.bin`, which is not in it -- along with four other files.
  * `the-largest-unclassified-functions.md` §13 stated that the region at `022D94B0` has **no writer
    anywhere in `.text`** and is "built at run time through a computed pointer rather than a literal
    address" -- while **§12, one section earlier, documents a setter writing that same region through
    literal RIP addresses.** Eight of the sixteen referencing functions write to it.
  * The same document's §14 wrote down that a `0xB` is a bound on a *second argument* and then titled
    the subsection "an 11-entry table", carrying 11 into its summary diagram. The table has 32
    entries.

`check_consistency.py` compares a document against OTHER documents. `check_answered_not_established.py`
compares a document against the ledger. **Nothing compares a document against itself**, which is
where a heavily-sectioned document is weakest: the correction is written where it is discovered and
the original claim stays where it was.

What it does
------------
Finds present-tense ABSENCE claims about writes -- "no writer", "nothing writes it", "all sixteen
only read", "is never written" -- and records the addresses in the same sentence. Then it searches
the rest of the SAME document for a positive write claim about one of those addresses: a setter, a
constructor, "writes", "zeroes", "stores".

A hit means one of the two statements is wrong, or they are scoped differently and neither says so.

What it does NOT do
-------------------
It only handles absence-of-write, because that is the one where the vocabulary on both sides is
narrow enough to match mechanically. The §14 case -- a value correctly described as a bound and then
reused as a count -- needs the numbers tied to an identifier, and this does not attempt it.

An address is the join key, so a claim scoped by name only ("the descriptor table is never written")
is invisible to it. That is a real limit: the check works because our documents cite addresses.

Usage
-----
    python check_self_contradiction.py --db "Database/FFXII TZA"
    python check_self_contradiction.py --db "Database/FFXII TZA" --self-test
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dispositions as DISP  # noqa: E402

# `\b` fails after `0x` -- see verify_doc_addresses.py. repos-c9, 2026-09-04.
ADDR = re.compile(r"(?<![0-9A-Fa-fx.])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Fa-f])")

# A STRUCTURE FIELD: `+0x18`, `actor+0x03`, `ctx+0xD0`. Not an address, and this checker joins
# on addresses - see the subject resolution in claims().
FIELD = re.compile(r"\+\s?0x[0-9A-Fa-f]{1,4}(?![0-9A-Fa-f])")

# Present-tense claims that nothing writes.
#
# `only read` is NOT in this list, and that omission is the whole lesson from the first run.
# "`022CB726` ... is read only by `003603C0` and written by three functions" scopes the READER set;
# it is not an absence-of-write claim, and matching it made the checker report a sentence that
# states both halves correctly in one breath.  **"only read by X" and "only read" are different
# claims and one substring covers both.**  Requiring an explicit no-write phrase costs recall and
# buys the check its right to be believed.
NO_WRITE = re.compile(
    r"\b(no writer|no writers|nothing writes|never written|not written|never initiali[sz]es|"
    r"read-only|no function writes|nothing stores|never stored)\b", re.I)

# Positive claims that something does.
DOES_WRITE = re.compile(
    r"\b(setter|constructor|writes?|wrote|zeroe?s|stores?|initiali[sz]es|assigns?|"
    r"populates?|fills?)\b", re.I)

# A write verb under a negation is not a writer.  The first run reported a line reading "never
# initialises either: mapping the whole frame of `00234AF0`" as positive evidence of a write,
# because the verb matched and the `never` three words earlier did not.  A verb is not a claim.
NEGATED = re.compile(
    r"\b(no|not|never|nothing|none|neither|nor|without|cannot|can't|does not|do not|"
    r"doesn't|don't|fails? to)\b[^.;]{0,40}?\b(setter|constructor|writes?|wrote|zeroe?s|"
    r"stores?|initiali[sz]es|assigns?|populates?|fills?)\b", re.I)

# A claim SCOPED to one function, one path or one instrument is correct English and correct
# analysis -- it is NOT a contradiction. "`022D9138` is read and never written BY THIS FUNCTION"
# sat two lines from a table naming its two image-wide writers, and this checker reported the
# document against itself. All three shapes below are ported from check_global_claims.py, where
# each cost a false positive before it was recognised.
SCOPED = re.compile(
    r"by this func|by this path|on this path|\bhere\b|in this func|through a rip|rip-relative|"
    r"this instrument|by the translator|by this document|in this pass|by that function|"
    r"at this address|in this section|at this site|at this call site|on this line", re.I)
# "at this site" added 2026-09-15 (OPUS). The list is an enumeration of scoping IDIOMS, not a
# closed vocabulary, and it already carried "at this address" and "in this section" - the same
# construction with a different noun. It was found by scoping a real finding: the map-screens page
# said of one row that "the global is read, not written", which is true of that instruction and
# false of the global, and the repair names both the site AND the writer elsewhere. The repair was
# still reported, because the idiom it used was missing rather than because anything was ambiguous.
# A gate that only accepts the scoping words it happens to list teaches authors to write for the
# regex instead of for the reader.

# A claim guarded by a condition is not a claim of absolute absence.
CONDITIONAL = re.compile(
    r"\bif\b|\bunless\b|\bwhen\b|\bwhile\b|\bwith it (zero|unset|null)|\bunder\b", re.I)

# An absence phrase inside quotation marks is a claim being QUOTED -- most often a document
# quoting its own retracted wording in order to correct it.
QUOTED = re.compile(u"[“”\"][^“”\"]{0,400}?[“”\"]")

# Past-tense / retracted framing is legitimate: a correction SHOULD say both things.
HISTORICAL = re.compile(
    r"\b(was|were|had been|previously|originally|superseded|retracted|corrected|"
    r"this (?:row|claim|section) (?:said|read)|until pass|no longer)\b", re.I)

# An absence claim ATTRIBUTED to another party is a report, not an assertion: "the widget contract
# SS5 **CLAIMED** `0208EA28` has no writer" states the contract's position, and the document goes on
# to refute it (OPUS-CONTRA-SPAWN-0208EA28, 2026-09-13).
#
# **This is deliberately NOT in HISTORICAL**, which `writers()` also consults: the first cut put it
# there and silenced 60-odd positive write lines corpus-wide, because a sentence like "asserted
# **only** where a single function writes the whole set" is a perfectly good write claim that merely
# contains the verb.  An attribution verb disqualifies an ABSENCE claim; it says nothing about a
# write claim.  Applied in `claims()` only.
#
# Recall cost, stated rather than hidden: a document that quotes an absence claim, ENDORSES it, and
# then contradicts it is invisible to this check.  That shape is not in the corpus; the reporting
# shape is.
ATTRIBUTED = re.compile(r"\b(claimed|asserted|argued|declared|according to)\b", re.I)


def sentence_around(lines, i, phrase):
    """The logical SENTENCE containing `phrase` on physical line `i`, joined across wrapping.

    Markdown hard-wraps prose at about a hundred characters, mid-sentence. Every frame guard
    above -- QUOTED, HISTORICAL, SCOPED, CONDITIONAL -- was written to read a sentence, and each
    was being handed a wrapped fragment instead, so a claim whose attribution sat on the previous
    line and whose refutation sat on the next one read as a bare present-tense assertion. Both of
    this checker's standing hits on 2026-09-13 were that defect and neither was a document error
    (OPUS-CONTRA-SPAWN-0208EA28, OPUS-EVSTD-01F83530).

    The join stops at a blank line, a heading, a list-item start or a table row, so it never runs
    two independent claims together -- which would hide a real contradiction behind a neighbour's
    "was".
    """
    def joinable(s):
        t = s.strip()
        return t and not t.startswith(("#", ">", "|", "```", "- ", "* ", "+ "))

    lo = i
    while lo > 0 and joinable(lines[lo - 1]) and joinable(lines[lo]):
        lo -= 1
    hi = i
    while hi + 1 < len(lines) and joinable(lines[hi + 1]) and joinable(lines[hi]):
        hi += 1
    block = " ".join(x.strip() for x in lines[lo:hi + 1])
    parts = re.split(r"(?<=[.;])\s+", block)
    for part in parts:
        if phrase.lower() in part.lower():
            return part
    return block


def claims(text):
    """(line_no, {address}) for each present-tense, UNSCOPED no-write claim.

    The claim is attributed to the address it FOLLOWS, not to every address on the line. A line
    reading "`A` is never written ... its two writers are `B` and `C`" states one absence and two
    presences; indicting B and C for it reported a correct sentence as a contradiction. That was
    4 of this checker's 5 standing hits on 2026-09-08.

    The MATCH and the address stay line-scoped; only the frame guards read the surrounding
    sentence (see sentence_around)."""
    out = []
    lines = text.split("\n")
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith(("#", ">")):
            continue
        bare = QUOTED.sub(" ", line)
        m = NO_WRITE.search(bare)
        if not m:
            continue
        # INVARIANT: the frame is never NARROWER than the physical line the guards used to read.
        # Dropping that invariant traded two false positives for four: a register table row is one
        # line holding a claim AND its disposition, and narrowing to the sentence around "no
        # writer" cut the disposition off, so four `OPEN-QUESTIONS.md` rows that the 2026-09-08
        # pass had already dispositioned by hand came back. Frame = line UNION sentence, so a claim
        # can only ever be suppressed more by this change, never less, and no new hit can appear.
        frame = QUOTED.sub(" ", line + " " + sentence_around(lines, n - 1, m.group(0)))
        if (HISTORICAL.search(frame) or SCOPED.search(frame) or CONDITIONAL.search(frame)
                or ATTRIBUTED.search(frame)):
            continue
        spans = [(x.start(), x.group(1).upper()) for x in ADDR.finditer(bare)]
        if not spans:
            continue
        # A CLAIM ABOUT A FIELD IS NOT A CLAIM ABOUT AN ADDRESS, and this checker joins on
        # addresses only. ED-5 reads "nothing on that tree writes `actor+0x03` (no writer in the
        # 80-reader census outside the carver)". The subject is a STRUCTURE FIELD, which ADDR
        # cannot match, so the nearest-preceding-address rule reached back past it into an earlier
        # clause and indicted `0026C120` - which that row names as a CALL TARGET, "calls
        # 0026C120(actor, 0)". The row says nothing about writes to 0026C120 at all, so nothing
        # could refute it, and the hit cost a disposition and two agents' reading time
        # (FABLE-ANSWER-OPUS-ED5-UQ101, signed 2026-09-15).
        #
        # So the subject is resolved against BOTH vocabularies, and if the nearer one is a field
        # the claim is skipped rather than reassigned. This checker's own docstring already says an
        # address is the join key and a claim scoped by name only is invisible to it; a claim
        # scoped by FIELD is the same limit, now honoured instead of papered over with a guess.
        # It can only ever remove hits. OPUS, 2026-09-15.
        fields = [(x.start(), x.group(0)) for x in FIELD.finditer(bare)]
        before = [(pos, addr) for pos, addr in spans if pos <= m.start()]
        near_field = max([f for f in fields if f[0] <= m.start()], default=None)
        if before and near_field and near_field[0] > max(before)[0]:
            continue                      # the field sits between the address and the claim
        if not before and near_field:
            continue                      # a field subject and no address before it at all
        subject = max(before)[1] if before else min(spans)[1]
        out.append((n, {subject}))
    return out


def writers(text):
    """address -> [(line_no, line)] for lines making a positive write claim."""
    idx = collections.defaultdict(list)
    for n, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith(">"):
            continue
        if (not DOES_WRITE.search(line) or NO_WRITE.search(line)
                or NEGATED.search(line) or HISTORICAL.search(line)):
            continue
        for m in ADDR.finditer(line):
            # The address must be the SUBJECT of the write, not merely present in the line.  The
            # first run reported "`02091098` has exactly one writer image-wide | 1 WRITE
            # (`00249FC0`), 3 READs (`00249C60`, ...)" as evidence that `00249C60` is written --
            # it is in the READ list of a sentence about a different address.  **An address in a
            # line about writing is not an address being written.**  Cheap guard: drop an
            # occurrence sitting in a READ context.
            before = line[max(0, m.start() - 24):m.start()]
            if re.search(r"\bREADs?\b|\bread by\b|\bread from\b", before, re.I):
                continue
            # Same guard, the other grammar: an address governed by a preposition is an OPERAND of
            # the sentence's verb, not its target.  "the appender `lea`s the entry's own address,
            # compresses it AGAINST `01F83530` and stores the result IN THE OBJECT" is a read of
            # `01F83530` and a store somewhere else, and it was reported as a write to it
            # (OPUS-EVSTD-01F83530, 2026-09-13).  A store target is named directly or with `to` /
            # `into`, never with `against` / `from` / `relative to`.
            # The trailing class absorbs the markdown that always sits between the preposition and
            # the address: a backtick, a quote, an opening bracket, `0x`.
            if re.search(r"\b(against|from|out of|relative to|compared to|compared with|"
                         r"based on|derived from|by way of|versus|vs\.?)"
                         r"[\s`'\"(\[]*(?:0x)?$", before, re.I):
                continue
            idx[m.group(1).upper()].append((n, line.strip()))
    return idx


def scan(text, rel, out):
    w = writers(text)
    for n, addrs in claims(text):
        for a in sorted(addrs):
            for wn, wline in w.get(a, []):
                if abs(wn - n) <= 2:
                    continue          # same passage: a sentence qualifying itself, not a conflict
                out.append((rel, n, wn, a, wline))
                break


SELF_TEST_BAD = (
    "## 12\nThe setter `0039AF70` writes the region through literal RIP addresses.\n"
    + "\n" * 20 +
    "## 13\nThere is no writer anywhere in `.text` for `0039AF70` - all sixteen only read.\n")
SELF_TEST_OK = (
    "## 12\nThe setter `0039AF70` writes the region through literal RIP addresses.\n"
    + "\n" * 20 +
    "## 13\nThis section previously said there was no writer for `0039AF70`; that was wrong.\n")

# --- added 2026-09-13 with the sentence-frame and operand-preposition guards ------------------
#
# The first two are the shapes that were being reported wrongly. The THIRD is the control that
# matters: a genuine contradiction whose absence claim is ALSO hard-wrapped. If the sentence join
# had bought its precision by blinding the check to wrapped prose, this case would go silent, and
# the two above would prove nothing.

# Reported claim: the attribution is on the line BEFORE and the refutation on the line AFTER.
SELF_TEST_ATTRIBUTED = (
    "## 5\nThe setter `0039AF70` writes the slot during initialisation.\n"
    + "\n" * 20 +
    "## 9\nThe widget contract section 5 CLAIMED\n"
    "`0039AF70` has no writer, remains null for the process lifetime, and must be passed\n"
    "as null in reconstruction. The native initializer contradicts that argument.\n")

# The address is an operand of the verb, not its target: read here, stored elsewhere.
SELF_TEST_OPERAND = (
    "## 4\nThe appender `lea`s the entry's own address, compresses it against `0039AF70`\n"
    "and stores the result in the object.\n"
    + "\n" * 20 +
    "## 8\nAnd `0039AF70` has no writer: two references image-wide and both are reads.\n")

# CONTROL: a real contradiction, wrapped exactly as the two above are. Must still fire.
SELF_TEST_WRAPPED_REAL = (
    "## 6\nThe setter `0039AF70` writes the region through literal RIP addresses.\n"
    + "\n" * 20 +
    "## 11\nThe region is built at run time through a computed pointer, so\n"
    "`0039AF70` has no writer anywhere in `.text` and all sixteen referencing\n"
    "functions only ever load from it.\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        cases = (("live contradiction", SELF_TEST_BAD, 1),
                 ("recorded retraction", SELF_TEST_OK, 0),
                 ("another document's claim, reported", SELF_TEST_ATTRIBUTED, 0),
                 ("address as operand, stored elsewhere", SELF_TEST_OPERAND, 0),
                 ("CONTROL: real contradiction, wrapped", SELF_TEST_WRAPPED_REAL, 1))
        failed = 0
        for name, text, want in cases:
            got = []
            scan(text, "<%s>" % name, got)
            mark = "ok " if len(got) == want else "FAIL"
            if len(got) != want:
                failed += 1
            print("  %s  %-38s fired %d, want %d" % (mark, name, len(got), want))
        if failed:
            print("SELF-TEST FAILED: %d case(s)" % failed)
            return 1
        print("self-test ok: %d cases, including the wrapped-prose control" % len(cases))
        return 0

    if not a.db:
        return ap.error("--db required unless --self-test")

    # POPULATION, narrowed 2026-09-08 after dispositioning a full run by hand.
    #
    # The first run reported 7 hits in 5 documents. **One warranted an edit.** The other six were
    # the instrument, not the corpus:
    #
    #   2 in `_index/_inbox/` -- peer handoff notes, which `COVERAGE.md` explicitly does not count
    #                            as documents. They are raw transcripts of another session's work
    #                            and are not maintained for internal consistency.
    #   1 in `AUDIT-LOG.md`   -- an append-only chronological log, where the refuting line came
    #                            LATER and therefore supersedes. Flagging it inverts the record.
    #   3 in `OPEN-QUESTIONS.md` -- rows that QUOTE an absence claim in order to state a question
    #                            about it, each already naming the instrument it is scoped to.
    #
    # So `_inbox` is excluded outright, and for an append-only ledger a hit counts only when the
    # ABSENCE claim is the later line. **`OPEN-QUESTIONS.md` is deliberately NOT exempted**: its
    # three hits were dispositioned by hand and recorded, because a blanket exemption on the
    # question ledger would silently hide a real contradiction filed as a question. This session
    # already deleted one heuristic that reported zero while possibly being broken; a rule that
    # cannot be checked is worse than a hit that has to be read.
    APPEND_ONLY = ("AUDIT-LOG.md",)

    out = []
    skipped_inbox = 0
    superseded = 0
    for root, _d, files in os.walk(a.db):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, a.db)
            if "_inbox" in rel.replace(chr(92), "/").split("/"):
                skipped_inbox += 1
                continue
            hits = []
            scan(io.open(p, encoding="utf-8", errors="replace").read(), rel, hits)
            if fn in APPEND_ONLY:
                keep = [h for h in hits if h[1] > h[2]]      # absence line after the write line
                superseded += len(hits) - len(keep)
                hits = keep
            out.extend(hits)

    # DISPOSITIONS, which this gate did not have. Its false positives were recorded as prose in the
    # comments above - "three hits were dispositioned by hand" - which no run can check and no
    # reviewer can find, so every run re-adjudicated them by hand. FINAL-AUDIT pass 24 makes that
    # untenable: thirty consecutive runs would mean thirty re-readings of the same non-defects.
    #
    # A row suppresses a finding only when an INDEPENDENT reviewer signed it and the evidence is
    # byte-for-byte what was judged; the subject carries the address and both line numbers, and the
    # hash covers both quoted lines. Reword either one and the disposition LAPSES and the finding
    # returns, reported as a lapse rather than as news. dispositions.py holds the mechanism and its
    # 13 controls. OPUS, 2026-09-15.
    reg = DISP.Registry(a.db, "check_self_contradiction.py")
    kept = []
    for rel, n, wn, addr, wline in out:
        # SUBJECT IS path::address, WITHOUT LINE NUMBERS. Corrected 2026-09-16 on
        # FABLE-CONTRA-OPUS-A-LINE-KEYED-DISPOSITION-GOES-INVISIBLE-RATHER-THAN-LAPSING. This read
        # `...::%d::%d` % (n, wn), and the one disposition this gate owns was keyed on lines 2048 and
        # 2838 of OPEN-QUESTIONS.md. Both moved +24 when rows were inserted ABOVE them - ED-5 to
        # 2072, UQ-101 to 2862 - so the subject could never match again and the row went INVISIBLE:
        # never applied, never lapsed, never reported, because report() can only describe lookups
        # that happened. dispositions.py's own docstring had already reasoned this out for
        # check_banned_evidence - "a line number is not stable across an edit above it" - and this
        # gate inherited the problem that comment was written to avoid.
        #
        # THE DIVISION OF LABOUR IS THE POINT: the SUBJECT says WHICH finding, and the EVIDENCE HASH
        # says whether it still reads the same. Line numbers belong to neither - they are an index
        # into the file, not a property of the claim. Dropping them costs nothing, because the hash
        # over `wline` already lapses the row loudly the moment the sentence itself changes.
        subject = "%s::%s" % (rel.replace("\\", "/"), addr)
        if not reg.suppressed(subject, wline):
            kept.append((rel, n, wn, addr, wline))
    out = kept

    print("population: every .md under the database root, EXCLUDING %d file(s) in _inbox/"
          % skipped_inbox)
    for line in reg.report():
        print(line)
    if superseded:
        print("           %d hit(s) in an append-only log where the refutation came later"
              % superseded)
    print()
    if not out:
        print("no document asserts that an address is never written and then writes it")
        return 0

    print("ABSENCE CLAIMS REFUTED BY THE SAME DOCUMENT")
    print("Each is a QUESTION: the two statements may be differently scoped -- but if they are,")
    print("neither of them says so, and a reader has no way to tell which one to believe.\n")
    by = collections.defaultdict(list)
    for rel, n, wn, addr, wline in out:
        by[rel].append((n, wn, addr, wline))
    for rel in sorted(by):
        print("  %s" % rel)
        for n, wn, addr, wline in by[rel]:
            print("      line %d says %s is never written; line %d:" % (n, addr, wn))
            print("        %s" % wline[:110])
        print()
    print("%d contradiction(s) in %d document(s)" % (len(out), len(by)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
