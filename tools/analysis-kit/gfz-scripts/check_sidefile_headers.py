"""check_sidefile_headers.py - the prose no gate reads.

FINAL-AUDIT pass 25 turned this up sideways. Checking all 1,224 script verbs against the bundled
ff12-script catalog found **1,224 of 1,224 identical** - and then the file's own provenance header
turned out to be wrong about something else entirely:

    scriptvm-dispatch.tsv, header:
      "The index is APPROXIMATELY the call id ... At least one discontinuity exists and its
       location is unknown (question I-6)."

    OPEN-QUESTIONS.md, I-6:
      "CLOSED 2026-09-07 - there is no discontinuity ... `record N = verb N` holds across all
       1,496 family-0 records."

The register closed the question seven days earlier and the side file still told every reader it was
open.

WHY NOTHING CAUGHT IT. `check_answered_not_established.py:174` walks `if fn.endswith(".md")`, and so
does every other stale-prose gate. **The corpus's side files carry substantial authored prose in `#`
headers - provenance per column, caveats, "do not rely on this row" warnings - and until this
checker no instrument had read a line of it.** A claim is not less load-bearing for living in a TSV
comment; the dispatch header is exactly where a reader is told whether they can trust the table.

TWO THINGS ARE CHECKED, both mechanical.

  QUESTION IDS  a header naming a question the register has since CLOSED, while still describing it
                as open. Naming a closed question to record its history is correct and common, so
                the two are distinguished and the sentence is printed whole.

  STATED COUNTS "1,224 rows", "133 members", "all 404 bodies". A count that no longer matches the
                file is the cheapest defect to find and one of the easiest to create: add three
                rows, forget the header.

THE HARD PART OF THE COUNT TEST IS NOT COUNTING, IT IS KNOWING WHAT THE NUMBER COUNTS. Headers mix
"1,224 rows" (this file) with "CScriptContainerInitializers.cpp, 1,954 entries" (an external
population) in the same sentence shape, so a checker that assumes every number is a row count
reports the catalog's 1,954 as a defect in a 1,224-row file. **Differences are reported as QUESTIONS
with the sentence attached, never as defects**, and this exits 0 on them.

Two measured facts that shaped the implementation and are worth keeping: `members/*.tsv` are bare
address lists with **no column header**, so subtracting one for a header turned every "133 members"
into a 132-row file - 138 of 144 apparent differences were that subtraction alone. And a header is a
PARAGRAPH, not a line: in the one defect this was written for, the id `I-6` sits on a different line
from every word that makes the claim, so a per-line test returns a confident zero.
"""
import argparse, collections, io, os, re, sys

DB_DEFAULT = "Database/FFXII TZA"
QID = re.compile(r"(?<![A-Za-z0-9])([A-Z]{1,4}-\d+[a-z]?)(?![A-Za-z0-9])")
COUNT = re.compile(r"\b(\d{1,3}(?:,\d{3})+|\d{2,6})\s+(rows|entries|functions|members|bodies)\b",
                   re.I)
# the header speaks of the question as STILL OPEN
OPENWORD = re.compile(r"\bunknown\b|\bnot established\b|\bnot known\b|\bunresolved\b|\bopen\b|"
                      r"\bnot verifiable\b|\bnot yet\b|\bat least one\b", re.I)
CLOSEDWORD = re.compile(r"\bCLOSED\b|\bANSWERED\b|\bRESOLVED\b|Established \d{4}", re.I)
# THE REGISTER STATES A VERDICT IN ITS LAST CELL, and that beats prose anywhere in the row.
# UC-1 reads "BLOCKED - vote closed 3-0; independent review ... outstanding": a closed VOTE
# is not a closed QUESTION, and CLOSEDWORD matching "vote closed" made this gate report the
# side file as stale against a question the register still holds open. Added 2026-09-18
# (OPUS), wiring in OPUS-RULING-SIDEFILE-HEADERS-UC1-STALE-IS-A-FALSE-POSITIVE.
#
# A NARROWING: the prose scan still decides every row whose verdict cell says nothing
# recognisable, and is consulted only after the cell.
VERDICT_CLOSED = re.compile(r"^(ANSWERED|WITHDRAWN|SUPERSEDED|DUPLICATE|DISSOLVED|"
                            r"NOT A QUESTION|NO ADMISSIBLE SOURCE|REVISED|CONFIRMED)\b", re.I)
VERDICT_OPEN = re.compile(r"^(OPEN|PARTIAL|BLOCKED)\b", re.I)
ADDRONLY = re.compile(r"^[0-9A-Fa-f]{8}$")


def sidefiles(db):
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in sorted(files):
            if f.endswith(".tsv"):
                yield os.path.join(root, f)


def header_blocks(lines):
    """Contiguous runs of `#` lines, as one unit of prose each."""
    blocks, cur, start = [], [], None
    for n, line in enumerate(lines, 1):
        if line.startswith("#"):
            if start is None:
                start = n
            cur.append(line)
        else:
            if cur:
                blocks.append((start, "\n".join(cur)))
            cur, start = [], None
    if cur:
        blocks.append((start, "\n".join(cur)))
    return blocks


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB_DEFAULT)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    reg = os.path.join(a.db, "_index", "OPEN-QUESTIONS.md")

    status = {}
    for line in io.open(reg, encoding="utf-8", errors="replace"):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        m = QID.match(cells[0].strip("`* "))
        if not m:
            continue
        rest = " ".join(cells[1:])
        # The stated verdict first; the prose scan only when the cell says nothing known.
        cell = cells[-1].strip("`* ") if len(cells) > 1 else ""
        if VERDICT_CLOSED.match(cell):
            state = "CLOSED"
        elif VERDICT_OPEN.match(cell):
            state = "OPEN"
        else:
            state = "CLOSED" if CLOSEDWORD.search(rest) else "OPEN"
        status[m.group(1)] = (state, rest[:200])

    files = list(sidefiles(a.db))
    hdr_lines, hits = 0, []
    agree, differ = 0, []

    for p in files:
        rel = os.path.relpath(p, a.db).replace(os.sep, "/")
        lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
        hdr_lines += sum(1 for l in lines if l.startswith("#"))

        for n, block in header_blocks(lines):
            for qid in sorted(set(QID.findall(block))):
                if qid not in status:
                    continue
                st, ans = status[qid]
                # test the WHOLE block, display a prefix: filtering on a truncated display string
                # cut the evidence off the end of a 29-line header and hid the defect this was
                # written for.
                hits.append((rel, n, qid, st, " ".join(block.split()), ans))

        data = [l for l in lines if l.strip() and not l.startswith("#")]
        if not data:
            continue
        first = data[0].split("\t")[0].strip()
        nrows = len(data) - (0 if ADDRONLY.match(first) else 1)
        for n, line in enumerate(lines, 1):
            if not line.startswith("#"):
                continue
            for m in COUNT.finditer(line):
                if int(m.group(1).replace(",", "")) == nrows:
                    agree += 1
                else:
                    differ.append((rel, n, m.group(1), m.group(2), nrows,
                                   " ".join(line.split())[:120]))

    stale = [h for h in hits if h[3] == "CLOSED" and OPENWORD.search(h[4])
             and not CLOSEDWORD.search(h[4])]
    histor = [h for h in hits if h[3] == "CLOSED" and h not in stale]
    still = [h for h in hits if h[3] == "OPEN"]

    if not a.quiet:
        print("Prose in side-file headers - a population no other gate reads\n")
        print("  side files                : %d" % len(files))
        print("  authored `#` header lines : %d" % hdr_lines)
        print("  questions in the register : %d" % len(status))
        print()
        print("  QUESTION IDS")
        print("      header lines naming a registered question : %d" % len(hits))
        print("      STALE - the register CLOSED it, the header still calls it open : %d"
              % len(stale))
        for rel, n, qid, st, line, ans in stale:
            print("          %s:%d  [%s]" % (rel, n, qid))
            print("              header   %s" % line[:150])
            print("              register %s" % ans[:150])
        print("      names a CLOSED question without calling it open (history, fine) : %d"
              % len(histor))
        print("      names a question the register still has OPEN (fine)             : %d"
              % len(still))
        print()
        print("  STATED COUNTS")
        print("      stated counts found    : %d" % (agree + len(differ)))
        print("      equal to the row count : %d" % agree)
        print("      different              : %d  (a QUESTION - the number may count something"
              " else)" % len(differ))
        for rel, n, stated, unit, nrows, line in differ:
            print("          %s:%d  stated %s %s, file has %d rows" % (rel, n, stated, unit, nrows))
            print("              %s" % line)

    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
