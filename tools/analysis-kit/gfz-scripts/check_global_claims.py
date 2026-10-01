# -*- coding: utf-8 -*-
"""Check the database's writer claims about globals against BOTH reference instruments.

`IB-1`. The RIP-relative reference map cannot see a global reached through an image-base register
(`lea r15,[rip-X]` then `[r15+disp]`). `imagebase_refs.py` measured that gap: **636 of 38,161
functions**, 2,027 references, **103 globals written that way that the RIP map shows as having no
writer**. One document had already drawn a false conclusion from it (`DD-1`/`DD-3`).

This sweep asks the follow-up: **which prose claims rest on that gap?**

Two claim shapes are checked, and one is deliberately NOT:

  * ABSENCE  -- "no writer", "never written", "no function writes"  -> contradicted if either
    instrument shows a writer.
  * COUNT    -- "N writers" / "one writer"                          -> contradicted if the combined
    writer set is larger than N.
  * SCOPED   -- "never written BY THIS FUNCTION", "never written THROUGH A RIP-RELATIVE ..." --
    these are correctly bounded statements about one function or one instrument. **They are not
    findings**, and conflating them with the above would manufacture false positives out of the
    database's most careful sentences.

    python check_global_claims.py                 # sweep
    python check_global_claims.py --control       # prove the instrument fires (REQUIRED reading)
"""
import argparse
import collections
import csv
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

_HERE = os.path.dirname(os.path.abspath(__file__))
_WORK = os.path.join(os.path.dirname(os.path.dirname(_HERE)), "work")
DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
RIP = os.path.join(_WORK, "h78", "rip_data_refs.tsv")
IBR = os.path.join(_WORK, "graph", "imagebase_refs.tsv")

ADDR = re.compile(r"\b(0[0-9A-Fa-f]{7})\b")

ABSENCE = re.compile(
    r"no writer|never written|not written|no function writes|nothing writes|unwritten", re.I)
COUNT = re.compile(
    r"\*{0,2}(one|two|three|four|\d+)\*{0,2}\s+writers?\b", re.I)

# Three shapes of QUALIFIED claim, all correct English and all previously flagged as findings.
# Each cost a real false positive on the first sweep, and each is named where it was found:
#
#   scope      "never written BY THIS FUNCTION"            -- true of that function
#   condition  "with it zero, X is not written at all"     -- true under a stated condition
#   restrict   "no writer stores A VTABLE OBJECT into it"  -- about WHAT is written, not whether
#
# Sentences that scope the claim to one function or one instrument are CORRECT, not findings.
# NOTE the word boundaries on `here`. Written once as `here\b`, it matched inside "anyw(here)"
# and silently suppressed the control's own planted claim -- and would have suppressed real
# findings in the sweep the same way. The control is what caught it.
SCOPED = re.compile(
    r"by this func|by this path|on this path|\bhere\b|in this func|through a rip|rip-relative|"
    r"this instrument|by the translator|by this document|in this pass|by that function", re.I)

# A claim guarded by a condition is not a claim of absolute absence.
CONDITIONAL = re.compile(
    r"\bif\b|\bunless\b|\bwhen\b|\bwhile\b|\bwith it (zero|unset|null)|"
    r"\bonce\b|\buntil\b|\bwould\b|\bunder\b", re.I)

# A claim that restricts WHAT is written ("no writer stores <something> into it") is not a claim
# that nothing writes it. Detected as an absence phrase followed by a transitive verb.
RESTRICTED = re.compile(
    r"(no writer|nothing|neither)[^.]{0,80}?"
    r"(stores?|writes?|puts?|places?|installs?|sets?)\s+(a|an|the|any)\s", re.I)

# An absence phrase INSIDE QUOTATION MARKS is someone else's claim being quoted -- most often a
# document quoting its own retracted wording:
#
#   > **OVERTURNED in section 21.** This paragraph said the table has *"no writer anywhere in
#   > `.text`"* ... **All three are false.**
#
# Reporting that as a live claim would indict a document for the correction it already made.
# Quoted spans are stripped before the claim patterns run.
QUOTED = __import__("re").compile(r"[\u201c\u201d\"][^\u201c\u201d\"]{0,400}?[\u201c\u201d\"]")


# "three writers set it to 0x7F" counts a SUBSET, not the writer set.
SUBSET_COUNT = re.compile(r"writers?[^.]{0,40}?(set|write|store)s?\s+it\s+to|"
                          r"writers?[^.]{0,40}?the immediate", re.I)

WORDS = {"one": 1, "two": 2, "three": 3, "four": 4}


def norm(v):
    v = (v or "").strip().lower()
    return (v[2:] if v.startswith("0x") else v).zfill(8)


def load_writers():
    """global -> set of writing functions, from BOTH instruments."""
    w = collections.defaultdict(set)
    src = collections.defaultdict(set)
    if os.path.exists(RIP):
        with io.open(RIP, encoding="utf-8", errors="replace") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if "write" in (r.get("kind") or "").lower():
                    g = norm(r["referenced_address"])
                    w[g].add(norm(r["function_entry"]))
                    src[g].add("rip")
    if os.path.exists(IBR):
        with io.open(IBR, encoding="utf-8", errors="replace") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if r.get("kind") == "write":
                    g = norm(r["global"])
                    if int(g, 16) < 0x00121000:      # base + a runtime offset: indeterminate
                        continue
                    w[g].add(norm(r["function"]))
                    src[g].add("imagebase")
    return w, src


# `_index/` holds append-only logs (AUDIT-LOG, COVERAGE) and ledgers that QUOTE the category
# documents. A finding there is a duplicate of a finding in the page it was copied from, and
# retroactively editing an append-only log would be wrong. Skipped, and counted.
def docs(root):
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("_inbox", "_index")]
        for fn in files:
            if fn.endswith(".md"):
                yield os.path.join(dirpath, fn)


# A markdown line often carries several addresses and a claim about only ONE of them --
# "`A`, `B`, `C`. **`D` is read and never written**" would otherwise indict A, B and C.
# Claims are therefore attributed CLAUSE by clause, not line by line.
CLAUSE = re.compile(r"(?<=[.;])\s+|\s+--\s+|\s*\|\s*")


def check_line(line, writers, src):
    """Return a list of (kind, addr, detail) findings for one line, attributed per clause."""
    out = []
    for clause in CLAUSE.split(line):
        out.extend(_check_clause(clause, writers, src))
    return out


def _nearest_before(spans, pos):
    """The address whose mention most closely PRECEDES `pos`, else the first that follows.

    One clause can carry several addresses with several different counts -- "`A` has 41 writers and
    `B` has 47" -- and attributing every count to every address in the clause indicted a document
    that was right. A claim belongs to the address it follows."""
    before = [(p, a) for p, a in spans if p <= pos]
    if before:
        return max(before)[1]
    return min(spans)[1] if spans else None


def _check_clause(line, writers, src):
    spans = [(m.start(), norm(m.group(1))) for m in ADDR.finditer(line)]
    addrs = [a for _, a in spans]
    line = QUOTED.sub(" ", line)          # a quoted claim is not this document's assertion
    if not addrs:
        return []
    if SCOPED.search(line) or CONDITIONAL.search(line) or RESTRICTED.search(line):
        return []
    out = []
    hit_abs = ABSENCE.search(line)
    m_cnt = None if SUBSET_COUNT.search(line) else COUNT.search(line)
    # Bind each claim to the address it actually follows, not to every address in the clause.
    if hit_abs is not None:
        a = _nearest_before(spans, hit_abs.start())
        addrs = [a] if a else []
    elif m_cnt is not None:
        a = _nearest_before(spans, m_cnt.start())
        addrs = [a] if a else []
    for a in addrs:
        ws = writers.get(a, set())
        if not ws:
            continue
        if hit_abs:
            out.append(("ABSENCE", a, "claimed unwritten; %d writer(s) found (%s)"
                        % (len(ws), "+".join(sorted(src.get(a, ()))))))
        elif m_cnt:
            tok = m_cnt.group(1).lower()
            n = WORDS.get(tok, int(tok) if tok.isdigit() else None)
            if n is not None and len(ws) > n:
                out.append(("COUNT", a, "claims %d writer(s); %d found (%s)"
                            % (n, len(ws), "+".join(sorted(src.get(a, ()))))))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=DB)
    ap.add_argument("--control", action="store_true",
                    help="plant a known-false claim and assert the sweep reports it")
    a = ap.parse_args()

    writers, src = load_writers()
    if not writers:
        print("check_global_claims: no writer data loaded -- every result below would be a dead "
              "scan; refusing to sweep.", file=sys.stderr)
        return 2
    ib_only = sum(1 for g in writers if src[g] == {"imagebase"})
    print("writer evidence: %d globals with >=1 writer  (%d visible ONLY through the image-base "
          "instrument)" % (len(writers), ib_only))

    if a.control:
        # The control DERIVES its subject rather than hardcoding one, so it cannot rot when the
        # reference data is regenerated. It picks a global written ONLY through an image-base
        # register -- exactly the class this sweep exists to catch.
        #
        # Hardcoding it went wrong once already: the first attempt used 01DF1738, which the
        # publisher only ever ADDRESS-TAKES (`lea rbx,[r15+0x1cd1738]`). It has no write row, so
        # the control failed while the code was correct.
        ib_only = sorted(g for g in writers if src[g] == {"imagebase"})
        if not ib_only:
            print("   FAIL  no image-base-only global to plant a control on", file=sys.stderr)
            return 1
        subject = ib_only[0]
        planted = "The global at `%s` has no writer anywhere in the image." % subject.upper()
        got = check_line(planted, writers, src)
        ok1 = any(k == "ABSENCE" and x == subject for k, x, _ in got)
        # And it must NOT fire on a correctly scoped sentence about the same address.
        scoped = "`%s` is read and never written by this function." % subject.upper()
        ok2 = not check_line(scoped, writers, src)
        # And it must not fire on an address with no writers at all.
        unwritten = "01DF1480"
        ok3 = not check_line("`%s` has no writer." % unwritten, writers, src)
        print()
        print("   subject chosen from the data: %s (written only via an image-base register)"
              % subject.upper())
        print()
        print("CONTROL")
        print("   %s  fires on a planted false absence claim" % ("ok  " if ok1 else "FAIL"))
        print("   %s  stays silent on a correctly SCOPED claim" % ("ok  " if ok2 else "FAIL"))
        print("   %s  stays silent where no writer exists (%s)"
              % ("ok  " if ok3 else "FAIL", "01DF1480 genuinely has none"))
        if not (ok1 and ok2 and ok3):
            print()
            print("   the sweep below would be untrustworthy; fix the instrument first.")
            return 1

    print()
    print("SWEEP")
    findings = collections.defaultdict(list)
    n_docs = n_lines = 0
    for path in docs(a.db):
        n_docs += 1
        rel = os.path.relpath(path, a.db).replace(os.sep, "/")
        try:
            text = io.open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        # Markdown wraps prose at ~100 columns, so a sentence -- and its qualifier -- routinely
        # spans two lines. Scanning line by line split "with it zero," from the clause it guards
        # and produced a false positive. Paragraphs are unwrapped before being scanned.
        para, start = [], 1
        for i, line in enumerate(text.split(chr(10)) + [""], 1):
            n_lines += 1
            if line.strip():
                if not para:
                    start = i
                para.append(line)
                continue
            if para:
                joined = " ".join(x.strip() for x in para)
                for kind, addr, detail in check_line(joined, writers, src):
                    findings[kind].append((rel, start, addr, detail, joined.strip()[:130]))
                para = []

    total = sum(len(v) for v in findings.values())
    print("   scanned %d documents, %d lines (excluding _inbox/ and the append-only _index/ logs)"
          % (n_docs, n_lines))
    print("   findings: %d" % total)
    for kind in ("ABSENCE", "COUNT"):
        rows = findings.get(kind, [])
        if not rows:
            continue
        print()
        print("   %s -- %d" % (kind, len(rows)))
        for rel, i, addr, detail, snippet in rows:
            print("      %s:%d" % (rel, i))
            print("         %s  %s" % (addr.upper(), detail))
            print("         | %s" % snippet)
    if not total:
        print()
        print("   No claim in the database is contradicted by the combined writer evidence.")
        print("   With the control passing, that is a real negative.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
