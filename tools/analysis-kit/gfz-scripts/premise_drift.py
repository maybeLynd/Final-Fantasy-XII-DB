#!/usr/bin/env python3
"""premise_drift.py - register rows citing a figure the owning page retracted.

EC-3 (FABLE): `BQ-14` asked "what are the other twelve objects" from a count of
thirteen that the owning document's own falsification pass had already replaced
with 62 six days earlier. Nothing watched for that shape. This report-only
instrument does: for every OPEN-QUESTIONS row that links its owning page, each
number the row's question text cites is looked up on that page. A number that
appears inside a `~~struck~~` span or on a WITHDRAWN/CORRECTED/REFUTED line is a
retraction candidate -- the page once asserted it and no longer does.

A hit is hand-review material, never a refusal: the page may keep the figure
live elsewhere (both-struck-and-live is reported as a weaker class), and a row
can legitimately quote its own history. Wired into check_questions.py's
CROSS-CHECK block alongside open_claim_drift.py.

Usage: premise_drift.py [--db DBPATH] [--verbose]
"""
import argparse, io, os, re, sys

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                  "..", "..", "..", "FFXII TZA")
REGISTER = "_index/OPEN-QUESTIONS.md"

WORDS = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
         "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
         "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
         "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
         "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
         "eighty": 80, "ninety": 90, "hundred": 100, "thousand": 1000}

RETRACT = re.compile(r"WITHDRAWN|CORRECTED|REFUTED|SUPERSEDED|retract", re.I)
LINK = re.compile(r"\[[^\]]*\]\(([^)]+\.md)\)")
ROW = re.compile(r"^\| ([A-Z][A-Za-z]*-[0-9]+[a-z]?) \| (.*?) \| [^|]* \|\s*$")


def numbers(text):
    """Integers and number-words a reader would call a figure. Code spans,
    hex/address tokens and years are excluded - they are identities, not
    counts."""
    text = re.sub(r"`[^`]*`", " ", text)          # code spans carry addresses
    text = LINK.sub(" ", text)                    # link targets are filenames
    out = set()
    for m in re.finditer(r"(?<![\w.])(\d+)(?![\w.])", text):
        v = int(m.group(1))
        if 2 <= v <= 100000 and not (1990 <= v <= 2099):
            out.add(v)
    for w, v in WORDS.items():
        if re.search(r"(?<![A-Za-z])%s(?![a-z])" % w, text, re.I):
            out.add(v)
    return out


def page_retractions(path):
    """(struck, marked, live) number sets for a page. `struck` = inside a
    ~~...~~ span (they may span lines); `marked` = unstruck text on a line
    carrying a retraction marker (the replacement figure lives there, so it
    is a weaker class); `live` = ordinary text."""
    struck, marked, live = set(), set(), set()
    inside = False
    for line in io.open(path, encoding="utf-8", errors="replace"):
        marked_line = bool(RETRACT.search(line))
        parts = line.split("~~")
        for i, part in enumerate(parts):
            nums = numbers(part)
            if inside:
                struck.update(nums)
            elif marked_line:
                marked.update(nums)
            else:
                live.update(nums)
            if i < len(parts) - 1:
                inside = not inside
    return struck, marked, live


def scan(db):
    """The report, for check_questions and the CLI: (hits, checked, unlinked).
    A hit is (qid, figure, class, owning-page relpath); class is RETRACTED
    (struck and absent from live text - the strong candidate) or struck+live."""
    reg = os.path.join(db, REGISTER)
    pages = {}
    hits, unlinked, checked = [], 0, 0
    for line in io.open(reg, encoding="utf-8", errors="replace"):
        m = ROW.match(line)
        if not m:
            continue
        qid, text = m.groups()
        links = LINK.findall(text)
        if not links:
            unlinked += 1
            continue
        nums = numbers(text)
        if not nums:
            continue
        checked += 1
        for link in links[:1]:                      # first link = owning page
            p = os.path.normpath(os.path.join(db, "_index", link))
            if not os.path.exists(p):
                p = os.path.normpath(os.path.join(db, link))
            if not os.path.exists(p):
                continue
            if p not in pages:
                pages[p] = page_retractions(p)
            struck, marked, live = pages[p]
            # Only the struck class is reported: unstruck text on a CORRECTED
            # line is usually the replacement figure itself, so marked-line
            # collisions are noise, not candidates.
            for v in sorted(nums & struck):
                cls = "RETRACTED" if v not in live else "struck+live"
                hits.append((qid, v, cls, os.path.relpath(p, db)))
    return hits, checked, unlinked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    hits, checked, unlinked = scan(a.db)
    for qid, v, cls, rel in sorted(hits):
        if a.verbose or cls == "RETRACTED":
            print("%-8s %-12s %-5s %s" % (qid, cls, v, rel))
    print("-- %d rows checked; %d premise-drift candidates "
          "(%d retracted-only, %d struck+live); %d rows carry no page link" %
          (checked, len(hits),
           sum(1 for h in hits if h[2] == "RETRACTED"),
           sum(1 for h in hits if h[2] != "RETRACTED"), unlinked))
    return 0


if __name__ == "__main__":
    sys.exit(main())
