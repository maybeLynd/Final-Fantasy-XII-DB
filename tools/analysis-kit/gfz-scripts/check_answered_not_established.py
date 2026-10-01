#!/usr/bin/env python3
"""check_answered_not_established.py - find documents that contradict themselves about a question.

Why this exists
---------------
Proposed by a parallel session on 2026-09-02 after finding that
`worldactor-scriptvm-interpreter.md` ticked BF-2 answered in section 7, ANSWERED it in section 10,
and still said "What FUN_0025D740 does is not established. BF-2." in section 4.  The same morning,
`character-render-object.md` said "reads: 13" and "reads within the first 12 instructions: 12 of 12"
two lines apart.

**Append-only correction sections make this the characteristic defect of a heavily-revised
document**: the correction is written where it was discovered, and the original statement stays
where it was.  No reader compares section 4 with section 10, and neither does any other checker --
`check_questions.py` compares the ledger against the CHECKBOXES, not against the prose.

The rule is narrow and cheap: associate a negative phrase with a currently ANSWERED id in the
same Markdown paragraph, list item or table row. Balanced struck-through history is excluded.

What it does NOT do
-------------------
Negative phrases must fit on one physical line, although the id may be on another line of the
same block. Multiple propositions in a block can still produce an unrelated advisory. And a
document may legitimately say "X was not established until pass 3" -- past tense about its own
history is not a defect.  Hits are QUESTIONS, not defects; the output says so.

THE MEASURED GAP (2026-09-13, four instances in one day)
--------------------------------------------------------
The rule needs the id and the negative phrase **in the same block**. Four stale statements found
by hand that day all sit in a *different* block from the answer that retired them, and three of
them **name no id at all**, so none is reachable:

  the-return-value-adapter-family.md   "the OwnedBufferResetAdapter family of 46 is still unread"
                                       -- a paragraph below DF-1, which read that family in full
  the-return-value-adapter-family.md   evidence row "not established" -- no id in the row; DF-4
                                       had been ANSWERED in another section
  the-count-clock-and-bank-recipes.md  "the rows' names are not in this database" -- the paragraph
                                       immediately after the FU-1 block that names all six
  the-action-definition-row.md         struct sketch "+0x34 u16 nameId (= row index)" -- not even
                                       a negative phrase: a stale POSITIVE restatement of a field
                                       its own field map had corrected fifty lines above

So the defect is broader than this gate's rule: **an append-only correction strands whatever
restated the old fact, anywhere in the document, phrased either way.** Closing it needs a
different association than id-in-the-same-block -- most cheaply, a shared distinctive token (an
address, a back-ticked identifier) between an ANSWERED block and a claim elsewhere in the same
document, which is the heuristic `check_novelty_claims.py` uses across documents. Not built here:
recorded so the next attempt starts from four real cases rather than a guess.

Usage
-----
    python check_answered_not_established.py --db "Database/FFXII TZA"
    python check_answered_not_established.py --db "Database/FFXII TZA" --self-test
"""
import argparse
import collections
import io
import os
import re
import sys
import tempfile
from pathlib import Path
import check_questions as questions

# Present-tense statements that the thing is still unknown.
NEGATIVE = re.compile(
    r"\b(is not established|are not established|not yet established|remains? unknown|"
    r"is unknown|are unknown|is not known|are not known|remains? unresolved|is unresolved|"
    r"has not been established|have not been established|is not proven|are not proven)\b", re.I)

# Past-tense / historical framing is legitimate: "was not established until pass 3".
HISTORICAL = re.compile(r"\b(was not established|were not established|had not been established|"
                        r"until pass|previously|originally|earlier version|this row (?:said|read))\b",
                        re.I)

SELF_TEST_LEDGER = "| BF-2 | what it does | **ANSWERED 2026-09-02** it is the pop helper |\n"
SELF_TEST_DOC_BAD = "What `FUN_0025D740` does is not established. **BF-2.**\n"
SELF_TEST_DOC_OK = "What `FUN_0025D740` does was not established until pass 3. **BF-2.**\n"


# A DATED ANSWER MARKER: the corpus's correction convention, which preserves the original claim and
# appends the answer beneath it. All three parts are required, and the DATE is the load-bearing one
# - "this is answered" in prose is a claim, a dated marker is a correction record. Without the date
# any sentence containing the word would excuse a document from contradicting itself.
ANSWER_VERB = re.compile(r"\b(?:answered|identity established|established|resolved|closed)\b",
                         re.I)
ISO_DATE = re.compile(r"\b20\d\d-\d\d-\d\d\b")


def carries_dated_answer(window, qid):
    """Does this text record an answer FOR THIS ID, with a date? -> bool."""
    return bool(ANSWER_VERB.search(window) and ISO_DATE.search(window)
                and re.search(r"\b" + re.escape(qid) + r"\b", window))


def answered_ids(db):
    """Current canonical statuses, never an ANSWERED word in historical prose."""
    table, duplicates = questions.read_table(db)
    if duplicates or not table:
        raise ValueError("question ledger has duplicate IDs or no parsed rows")
    return {qid for qid, status in table.items() if status == "ANSWERED"}


def blocks(text):
    """Line-numbered paragraphs/list items; preserve line positions in struck history."""
    clean = re.sub(r"~~.*?~~", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)
    lines = clean.split("\n")
    start = 0
    for i, line in enumerate(lines):
        plain = re.sub(r"^\s*(?:>\s*)*", "", line)
        boundary = not plain.strip() or plain.startswith('#')
        item = re.match(r"^\s*(?:[-+*]|\d+[.)])\s+|^\s*\|", plain)
        if boundary or item:
            if start < i:
                yield start, lines[start:i]
            start = i + 1 if boundary else i
    if start < len(lines):
        yield start, lines[start:]


def scan(ids, text, rel, out):
    # Materialised, because a block is now judged together with the one IMMEDIATELY BELOW IT: the
    # correction convention appends the answer as its own paragraph, so it lands in the next block.
    bl = list(blocks(text))
    for bi, (start, lines) in enumerate(bl):
        window = "\n".join(lines)
        # ADJACENT ONLY - the next block must begin within one line of this one ending, so nothing
        # but a blank line separates them. A dated answer three sections further down is about
        # something else and must not reach back to excuse this claim.
        below = ""
        if bi + 1 < len(bl):
            nstart, nlines = bl[bi + 1]
            if nstart - (start + len(lines)) <= 1:
                below = "\n".join(nlines)
        # A physical-line window borrowed IDs from adjacent bullets/headings.
        # Hard-wrapped text stays together, but separate Markdown blocks do not.
        # Ambiguity must be judged over ALL ids present, not just answered ones.  Filtering to
        # answered first made an adjacent OPEN id invisible, so a sentence plainly belonging to the
        # open question looked like it belonged to the closed one -- which is how loot-drops line 440
        # (AE-7 named, AE-12 owning) kept reporting.
        all_ids = set(re.findall(r"\b(" + questions.QID + r")\b", window))
        if len(all_ids) != 1:
            continue
        qid = all_ids.pop()
        # A window that AFFIRMS the answer is not contradicting it.  gambit-evaluation reads
        # "Z-11 is answered by this ... (whether 0x01DFE0B0 belongs to the same structure is not
        # established)" -- the negative is a residual sub-question about a DIFFERENT address, and
        # the document is agreeing with the ledger, not disputing it.
        if re.search(re.escape(qid) + r"\s+(?:is\s+)?(?:ANSWERED|answered|CLOSED|closed)", window):
            continue
        # THE CONVENTION: claim preserved, dated answer appended here or directly underneath.
        if carries_dated_answer(window, qid) or carries_dated_answer(below, qid):
            continue
        if qid not in ids:
            continue
        for n, line in enumerate(lines, start + 1):
            m = NEGATIVE.search(line)
            if not m or HISTORICAL.search(line):
                continue
            quoted = re.findall(r"[\"“][^\"”\n]{0,300}[\"”]", line)
            if any(m.group(0) in q for q in quoted):
                continue
            out.append((rel, n, qid, line.strip()))


def _adjacency_control():
    """The adjacent-answer rule must excuse the convention and nothing else. -> bool."""
    cases = [
        # (this block, the block below, qid, should it still flag?)
        ("What X is for is not established - `DK-2`.", "", "DK-2", True),
        ("What X is for is not established - `DK-2`.",
         "*Answered 2026-09-14 (FABLE), DK-2:* it is a thing.", "DK-2", False),
        # no date: a claim, not a correction record
        ("What X is for is not established - `DK-2`.",
         "*Answered (FABLE), DK-2:* it is a thing.", "DK-2", True),
        # dated answer for a DIFFERENT id must not excuse this one
        ("What X is for is not established - `DK-2`.",
         "*Answered 2026-09-14 (FABLE), DK-9:* it is a thing.", "DK-2", True),
        # a date with no answer verb is just a dated sentence
        ("What X is for is not established - `DK-2`.",
         "Sampled 2026-09-14, DK-2 remains the open half.", "DK-2", True),
    ]
    ok = True
    for here, below, qid, should_flag in cases:
        excused = carries_dated_answer(here, qid) or carries_dated_answer(below, qid)
        if excused == should_flag:
            print("  CONTROL FAILED: %r / %r -> excused=%s" % (here[:32], below[:32], excused))
            ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    # RUN FIRST, ALWAYS. The adjacent dated-answer rule excuses 7 of the 10 hits this file used to
    # print; if its control does not hold, every one of those exclusions is unsupported and the
    # honest output is no output.
    if not _adjacency_control():
        print("THE ADJACENT-ANSWER CONTROL DID NOT FIRE - the exclusions below are unsupported.")
        return 2

    if a.self_test:
        with tempfile.TemporaryDirectory() as scratch:
            folder = Path(scratch) / '_index'
            folder.mkdir()
            (folder / 'OPEN-QUESTIONS.md').write_text(SELF_TEST_LEDGER, encoding='utf-8')
            ids = answered_ids(scratch)
        if "BF-2" not in ids:
            print("SELF-TEST FAILED: ledger parse found no ANSWERED ids")
            return 1
        bad, ok = [], []
        scan(ids, SELF_TEST_DOC_BAD, "<bad>", bad)
        scan(ids, SELF_TEST_DOC_OK, "<ok>", ok)
        if len(bad) != 1 or len(ok) != 0:
            print("SELF-TEST FAILED: bad=%d (want 1) ok=%d (want 0)" % (len(bad), len(ok)))
            return 1
        print("self-test ok: fires on the present-tense contradiction, silent on the historical one")
        print("           and the adjacency control holds: a dated answer for the SAME id"
              " in this block or the one directly")
        print("           below excuses it; an undated one, one for another id, and a "
              "dated line with no answer verb do not")
        return 0

    if not a.db:
        return ap.error("--db required unless --self-test")

    ids = answered_ids(a.db)
    if not ids:
        print("No current ANSWERED ids; no answered-question comparisons made.")
        return 2

    out = []
    for root, _d, files in os.walk(a.db):
        if "_index" in root.split(os.sep):
            continue          # the ledger states both sides by design; _inbox is staging
        for fn in files:
            if fn.endswith(".md"):
                p = os.path.join(root, fn)
                scan(ids, io.open(p, encoding="utf-8").read(), os.path.relpath(p, a.db), out)

    print("%d answered id(s) in the ledger" % len(ids))
    if not out:
        print("no document contradicts the ledger about an answered question")
        return 0
    # THE ADJUDICATION EXISTS AND THIS CHECKER DID NOT READ IT.
    # `_index/candidates/answered-but-called-unknown.tsv` was built for exactly this output and
    # carries a verdict per (document, line, id): ANNOTATED where the page already records the
    # answer inline, ANNOTATED-ELSEWHERE where it records it with the original preserved,
    # DIFFERENT-SUBJECT where the page's sentence and the register's answer name disjoint
    # addresses. Every row is decided. Re-printing all of them as open questions on every run is
    # how a registry stops being read. 2026-09-14, OPUS.
    adj = {}
    reg = os.path.join(a.db, "_index", "candidates", "answered-but-called-unknown.tsv")
    try:
        for l in io.open(reg, encoding="utf-8"):
            if l.startswith("#") or not l.strip():
                continue
            c = l.rstrip("\n").split("\t")
            # KEYED ON (document, id), NOT the line number. Keying on the line makes the registry
            # go stale the moment anything above the row is edited - and it did, immediately:
            # adding `transfers_to` to 103 documents pushed their frontmatter down four lines and
            # five adjudicated rows came back "not yet adjudicated". A verdict is about a claim,
            # not about where the claim sits in the file.
            if len(c) >= 4:
                adj[(c[0].replace("\\", "/"), c[2])] = c[3]
    except OSError:
        pass                      # the registry is optional; without it every row is reported

    settled, fresh = [], []
    for rel, n, qid, line in out:
        v = adj.get((rel.replace("\\", "/"), qid))
        (settled if v and v != "UNADJUDICATED" else fresh).append((rel, n, qid, line, v))

    print("\nDOCUMENTS THAT STILL CALL AN ANSWERED QUESTION UNKNOWN")
    print("Each is a QUESTION, not a defect: check whether the sentence is stale or")
    print("whether the ledger closed the id too early.\n")
    if fresh:
        print("  NOT YET ADJUDICATED - no row in answered-but-called-unknown.tsv:\n")
        by = collections.defaultdict(list)
        for rel, n, qid, line, _v in fresh:
            by[rel].append((n, qid, line))
        for rel in sorted(by):
            print("  %s" % rel)
            for n, qid, line in by[rel]:
                print("      line %d  [%s]  %s" % (n, qid, line[:110]))
            print()
    if settled:
        print("  ALREADY ADJUDICATED in the registry: %d" % len(settled))
        c = collections.Counter(v for _r, _n, _q, _l, v in settled)
        for k, v in c.most_common():
            print("      %-22s %d" % (k, v))
        print()
    return 1 if fresh else 0


if __name__ == "__main__":
    sys.exit(main())
