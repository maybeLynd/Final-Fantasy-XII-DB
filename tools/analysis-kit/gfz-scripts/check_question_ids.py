#!/usr/bin/env python3
"""check_question_ids.py - question ids minted in documents that the register does not have,
and ids that name two different questions.

WHAT NOTHING ELSE CHECKS. `check_questions.py` compares the register table against the per-document
CHECKBOXES and is green. It never asks whether an id a document DEFINES is in the register at all,
or whether the register's row for that id is about the same subject. Both are false today.

FOUND BY WALKING INTO ONE. `BM-3` in the register is *"the remaining 16 bytes of the 40-byte
`ChannelValue` slot"* - PhyreEngine animation channels. `CONTRACT-battle-runtime-mode.md` section 14
defines `BM-3` as *"what `FUN_002E73C0(actor3, 3)` does to the guest slot when the chocobo bit
clears"*. Two questions, one id. "BM" meant *Battle Mode* to one author and something else to the
other, and both minted 1, 2, 3.

WHY IT MATTERS RATHER THAN BEING TIDINESS. The register is the instrument behind `questions_closed`
and behind every section-7 query. An id absent from it is a question nothing can count, close or
find; an id that names two questions makes "answered" ambiguous - closing one closes the other on
paper.

  MINTED-NOT-REGISTERED   a document defines `XX-N` and the register has no such row
  SUBJECT-MISMATCH        both exist and share NO backticked token AND no 8-hex address

THE MISMATCH TEST IS DELIBERATELY WEAK IN THE SAFE DIRECTION. It fires only when BOTH sides carry
identifiers and the two sets are DISJOINT - a document that defines an id in one terse clause with
no code in it cannot trigger it. So it under-reports: `BM-1` does not flag while `BM-2` and `BM-3`
do, and `BM-1` is the same collision. **A clean SUBJECT-MISMATCH count is not evidence that no id
collides**, and the summary says so rather than implying otherwise.

NEITHER CLASS IS FIXED HERE, and that is a routing decision rather than laziness. Adding the missing
ids to the register moves a scored denominator, and renaming a colliding id changes something other
documents cite. Both belong to the register's owner with the measurement in hand.
"""
import argparse
import collections
import io
import os
import re

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")
SKIP = ("_index", "_templates", "_inbox", "_experiments")
ROW = re.compile(r"^\|\s*([A-Z]{1,3}-\d+)\s*\|(.*)$", re.M)
# A DEFINITION, not a mention. "3. **`BM-3`** — ..." or "- **`BM-3`** — ...": the shape a document
# uses when it is MINTING the id, which is the only shape that can create a collision.
DEFS = (re.compile(r"^\s*\d+\.\s+\*\*`([A-Z]{1,3}-\d+)`\*\*\s*[—-]\s*(.+)$", re.M),
        re.compile(r"^\s*[-*]\s+\*\*`([A-Z]{1,3}-\d+)`\*\*\s*[—-]\s*(.+)$", re.M))
TOKEN = re.compile(r"`([^`]{3,40})`")
ADDR = re.compile(r"\b0[0-9A-Fa-f]{7}\b")


def identifiers(text):
    return {t.lower() for t in TOKEN.findall(text)} | {a.lower() for a in ADDR.findall(text)}


def registry(db):
    p = os.path.join(db, "_index", "OPEN-QUESTIONS.md")
    if not os.path.isfile(p):
        return None
    out = {}
    for m in ROW.finditer(io.open(p, encoding="utf-8", errors="replace").read()):
        out.setdefault(m.group(1), m.group(2))
    return out


def definitions(db):
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, db).replace(os.sep, "/")
            text = io.open(p, encoding="utf-8", errors="replace").read()
            for pat in DEFS:
                for m in pat.finditer(text):
                    yield rel, m.group(1), m.group(2)


def control(reg):
    """A constructed registered/matching pair must NOT flag; unregistered and disjoint must."""
    ok = True
    cases = [
        ("ZZ-99", "the thing at `00123456`", None, "MINTED"),
        ("ZZ-98", "the thing at `00123456`", "the thing at `00123456` again", "clean"),
        ("ZZ-97", "the thing at `00123456`", "something about `00ABCDEF` entirely", "MISMATCH"),
        ("ZZ-96", "a terse clause with no identifiers", "something about `00ABCDEF`", "clean"),
    ]
    for qid, doc, row, want in cases:
        if row is None:
            got = "MINTED"
        else:
            d, r = identifiers(doc), identifiers(row)
            got = "MISMATCH" if (d and r and not (d & r)) else "clean"
        if got != want:
            print("  CONTROL FAILED: %s expected %s got %s" % (qid, want, got))
            ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    a = ap.parse_args()
    reg = registry(a.db)
    if reg is None:
        print("CANNOT RUN: no _index/OPEN-QUESTIONS.md under %s" % a.db)
        return 2
    if not control(reg):
        print("\n  THE CONTROL DID NOT FIRE - every verdict below is unsupported.")
        return 2
    print("  control passed: an unregistered id flags, a disjoint pair flags, a matching pair and")
    print("  a token-free definition do not.")

    minted, mismatch, checked = [], [], 0
    for rel, qid, body in definitions(a.db):
        checked += 1
        if qid not in reg:
            minted.append((rel, qid, body.strip()))
            continue
        d, r = identifiers(body), identifiers(reg[qid])
        if d and r and not (d & r):
            mismatch.append((rel, qid, body.strip(), reg[qid].strip()))

    print("\n  register rows                 : %d" % len(reg))
    print("  id DEFINITIONS found in documents : %d" % checked)
    print("\nMINTED-NOT-REGISTERED - a document defines it and the register has no such row: %d"
          % len({q for _r, q, _b in minted}))
    byfile = collections.Counter(r for r, _q, _b in minted)
    for f, n in byfile.most_common():
        ids = sorted({q for r, q, _b in minted if r == f})
        print("    %-64s %s" % (f[:64], ", ".join(ids)))
    print("\nSUBJECT-MISMATCH - both exist and share no identifier at all: %d" % len(mismatch))
    for rel, qid, body, row in mismatch:
        print("    %-7s %s" % (qid, rel[:66]))
        print("        document : %s" % body[:104])
        print("        register : %s" % row[:104])
    if mismatch:
        print("\n  THIS COUNT UNDER-REPORTS AND THAT IS BY DESIGN. The test fires only when BOTH")
        print("  sides carry identifiers and the sets are disjoint, so a collision stated in plain")
        print("  words does not reach it - `BM-1` is the same collision as `BM-2` and `BM-3` and")
        print("  does not appear here. A clean count is not evidence that no id collides.")
    print("\n  NEITHER CLASS IS FIXED HERE. Adding the missing ids moves a scored denominator and")
    print("  renaming a colliding id changes what other documents cite; both are the register")
    print("  owner's call, which is why this reports and routes rather than editing.")
    return 1 if (minted or mismatch) else 0


if __name__ == "__main__":
    raise SystemExit(main())
