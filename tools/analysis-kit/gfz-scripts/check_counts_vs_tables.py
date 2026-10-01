#!/usr/bin/env python3
"""check_counts_vs_tables.py - a document that states a count above a table that contradicts it.

EC-5, open since 2026-09-12: *"A document can state a count and tabulate a different one, and no
gate compares them."* `one-word-decides-which-fifteen-subsystems-tick.md` said **"fifteen distinct
masks"** above a table of **fourteen** rows and carried that in plain sight. `check_consistency`
passes, because it compares addresses ACROSS documents and never a number to the table beneath it.

The defect is not cosmetic. The missing row there was the one group reached by `jmp` rather than
`call` - **a call-only census finds fourteen and reports fifteen** - so the mismatch was the only
surviving evidence that an instrument had missed a case.

WHAT THIS CHECKS, narrowly on purpose
-------------------------------------
For every markdown table, the paragraph immediately above it is read for a count phrase: a number
(digits or a spelled-out word) followed closely by a plural noun. If that number disagrees with the
table's data-row count, the pair is reported.

PRECISION OVER RECALL. A gate that cries wolf is a gate people learn to skip, and this one is
looking for a defect that hides in plain sight precisely because everything else about the document
looks right. So it refuses to fire when:

  * the number carries a unit - `B`, `bytes`, `%`, `0x`, `px`, `ms` - it is a measurement, not a count
    of rows;
  * the number is above 200, which is a figure about the engine and not about a table;
  * the table has a totals row, or any row whose first cell is empty or a continuation;
  * the count phrase names something the table plainly is not ("**15 callers**" above a table of
    fields), detected by requiring the plural noun to appear in the table's header or its caption;
  * the table is a key-addresses or evidence table, whose row count is never the subject of the
    sentence above it.

Exit code is 1 when any pair is reported, so it can gate a checkpoint.
"""
import argparse
import io
import os
import re
import sys

WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
         "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
         "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
         "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50}
# The number must not be the tail of a larger one. `1,114 containers` matched as `114` in the first
# version of this and produced four identical false findings in the EBP corpus - the check's own
# first output was a demonstration of the defect class it hunts.
NUMBER = re.compile(r"(?<![\d,])\*{0,2}\b(" + "|".join(WORDS) + r"|\d{1,3})\b\*{0,2}(?![\d,])\s+"
                    r"(?:\*{0,2}[A-Za-z`][\w`/-]*\*{0,2}\s+){0,2}"
                    r"\*{0,2}\b([a-z][a-z-]{3,})s\b", re.I)
UNIT = re.compile(r"\b(?:B|bytes?|%|px|ms|KiB|MiB|GiB)\b|0[xX][0-9A-Fa-f]", re.I)
# Every numeral or number word a reader would take as a count, for the one-count-per-paragraph
# guard. Addresses and hex are excluded: they are names, not quantities.
COUNTABLE = re.compile(r"(?<![\dA-Fa-fx,.])\b(?:" + "|".join(WORDS) + r"|\d{1,3})\b(?![\d,.])",
                       re.I)
SEP = re.compile(r"^\s*\|[\s:\-|]+\|\s*$")
SKIP_HEADER = re.compile(r"\b(?:address|evidence|claim|tier|confidence|key addresses)\b", re.I)


def tables(lines):
    """Yield (header_index, header_cells, data_row_indices)."""
    i = 0
    while i < len(lines) - 1:
        if lines[i].lstrip().startswith("|") and SEP.match(lines[i + 1]):
            hdr = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            j = i + 2
            rows = []
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(j)
                j += 1
            yield i, hdr, rows
            i = j
        else:
            i += 1


def paragraph_above(lines, idx):
    """The last non-blank block of prose before `idx`, or ''."""
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    end = j
    while j >= 0 and lines[j].strip() and not lines[j].lstrip().startswith("|"):
        j -= 1
    return "\n".join(lines[j + 1:end + 1]) if end > j else ""


def check_doc(rel, text, out):
    lines = text.split("\n")
    for hi, hdr, rows in tables(lines):
        if not rows or SKIP_HEADER.search(" ".join(hdr)):
            continue
        body = [lines[r] for r in rows]
        if any(re.match(r"^\s*\|\s*(?:\*{0,2}total|\s*\|)", b, re.I) for b in body):
            continue
        n_rows = len(body)
        para = paragraph_above(lines, hi)
        if not para or para.lstrip().startswith("#"):
            continue
        header_words = " ".join(hdr).lower()
        for m in NUMBER.finditer(para):
            raw, noun = m.group(1).lower(), m.group(2).lower()
            span = para[max(0, m.start() - 12):m.end() + 12]
            if UNIT.search(span):
                continue
            val = WORDS.get(raw, None)
            if val is None:
                try:
                    val = int(raw)
                except ValueError:
                    continue
            if val > 200 or val == n_rows:
                continue
            # A TABLE THAT SUMMARISES AND A TABLE THAT ENUMERATES LOOK IDENTICAL. "83 path-table
            # bases ... collapse into" above four shape rows is correct writing; "fifteen distinct
            # masks" above fourteen rows is EC-5's defect. Nothing in the markup tells them apart -
            # but the ARITHMETIC does. A summary collapses a population by a large factor; a
            # miscount is off by one or two. Reporting only near misses takes the check from 56
            # findings that are almost all summaries to the shape the defect actually has.
            #
            # This is a deliberate loss of recall: a document that states 40 and tabulates 12 when
            # it meant to enumerate is invisible here. That case is indistinguishable from a
            # summary by any rule this gate can apply, and is recorded as the limit rather than
            # papered over.
            if abs(val - n_rows) > 2 or n_rows < 3:
                continue
            # THE NOUN MUST NAME THE TABLE'S ROWS, and the filename is not evidence of that.
            # Matching `rel` too let "1,114 containers" agree with any page whose name contains
            # "container", which is how a count about the corpus was compared to a table about one
            # file. Only the table's own header counts.
            if noun[:5] not in header_words:
                continue
            # A count phrase in a paragraph that also names a DIFFERENT population - "of the 83
            # bases, these 11 fall into three shapes" - is describing a subset, and the row count
            # is not what the sentence claims.
            #
            # Keying this on matches of the full NUMBER pattern was not enough: a paragraph reading
            # "three of those four ... and two more ... five in all" produced exactly one full match
            # and sailed through. The correction I wrote for this gate's own first finding tripped
            # the gate, which is the second time in one session that this check's output has been
            # an instance of its own defect class. Count NUMERALS, not matches.
            if len(COUNTABLE.findall(para)) > 1:
                continue
            out.append((rel, hi + 1, val, noun + "s", n_rows,
                        re.sub(r"\s+", " ", para)[:110]))


def triaged(db):
    """(document, line) pairs a reader has already ruled on, from the candidates file.

    A GATE THAT IS RED ON CANDIDATES IS A GATE PEOPLE LEARN TO SKIP - this file's own docstring
    says so about false positives, and it is just as true of true ones nobody has judged yet. About
    half this check's output is correct writing: a sentence describing a subset of the table below
    it. So the candidates file is the TRIAGE RECORD, its `verdict` column is what a reader decided,
    and the gate goes red only on a mismatch NOBODY HAS LOOKED AT. A verdict of `subset` retires a
    row as correctly written; `fix` leaves it red until the document changes.
    """
    path = os.path.join(db, "_index", "candidates", "count-vs-table-candidates.tsv")
    seen = {}
    if not os.path.isfile(path):
        return seen
    for line in io.open(path, encoding="utf-8", errors="replace"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) >= 6 and f[5].strip():
            # KEYED ON THE CLAIM, NOT ON THE LINE NUMBER. It was (document, line), and on
            # 2026-09-16 FOUR of the twenty rulings were pointing at nothing while this file's own
            # header said "FINAL TALLY, all ten read". The documents had simply grown above the
            # claim: 1266 -> 1299, 528 -> 655, 1911 -> 1914, 300 -> 338. Every one of the four
            # still matched on document, stated count, noun and table_rows - the claim had not
            # changed at all, only its address in the file - so the gate was re-reporting
            # adjudicated work as untriaged and would have gone on doing so after every insertion.
            #
            # Second time this exact defect has been found in the kit today; check_nowriter_claims
            # had it too, and was re-keyed the same way. A judgement keyed to something that is not
            # the thing judged rots silently, because a key that matches nothing looks exactly like
            # a key that was never needed.
            #
            # The tuple carries both numbers, so a NEW mismatch in the same document is only
            # auto-retired if it states the same count over a table of the same size - a different
            # claim of the same shape, which the line number would not have distinguished either
            # once it had drifted.
            seen[(f[0].strip(), f[2].strip(), f[3].strip(), f[4].strip())] = f[5].strip()
    return seen


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--all", action="store_true",
                    help="list every candidate, including the ones already ruled on")
    a = ap.parse_args(argv)
    out = []
    for dirpath, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        for name in sorted(f for f in files if f.endswith(".md")):
            rel = os.path.relpath(os.path.join(dirpath, name), a.db).replace(os.sep, "/")
            text = io.open(os.path.join(dirpath, name), encoding="utf-8",
                           errors="replace").read()
            check_doc(rel, text, out)
    ruled = triaged(a.db)
    fresh, retired, to_fix = [], 0, 0
    for row in out:
        # (document, stated, noun, table_rows) - the claim, matching triaged()
        verdict = ruled.get((row[0], str(row[2]), row[3], str(row[4])))
        if verdict is None:
            fresh.append(row)
        elif verdict.lower().startswith("fix"):
            to_fix += 1
            fresh.append(row)
        else:
            retired += 1
    for rel, line, said, noun, got, para in (out if a.all else fresh):
        v = ruled.get((rel, str(said), noun, str(got)), "")
        print("  %s:%d%s" % (rel, line, ("   [%s]" % v) if v else ""))
        print("     says %d %s, table has %d rows" % (said, noun, got))
        print("     %s" % para)
    print("\n  candidates: %d   ruled correct-as-written: %d   needing a fix: %d   untriaged: %d"
          % (len(out), retired, to_fix, len(fresh) - to_fix))
    if not fresh:
        print("  counts consistent: every mismatch above a table has been read and ruled on")
    return 1 if fresh else 0


if __name__ == "__main__":
    raise SystemExit(main())
