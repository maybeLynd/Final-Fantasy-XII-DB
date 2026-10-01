#!/usr/bin/env python3
"""FINAL-AUDIT-PROTOCOL pass 7 - tier presence: every claim in the Evidence section cites a tier.

Pass 7 fails if any claim has none. Before this, pass 7 was one of the eighteen with no instrument,
which means the only way to run it was to open 395 documents and read every Evidence table.

WHY THE OBVIOUS IMPLEMENTATION IS WRONG, AND HOW I KNOW
-------------------------------------------------------
The obvious version finds the Evidence section and reads the LAST column of each table row. A
survey of the corpus before writing a line of it says that would be wrong in two separate ways:

  1. NOT EVERY EVIDENCE TABLE PUTS THE TIER LAST. Taking the last cell yields values like
     '054, 058, 05C' (x14), 'data' (x12) and 'yes' (x6) - those are offset lists and kinds from
     tables with a different column layout. An instrument that scored those as tiers would report
     a corpus full of exotic tier names it had invented itself. The tier column is therefore
     located BY ITS HEADER, and a table with no tier header is reported as exactly that rather
     than guessed at.
  2. THE TIER VOCABULARY IS NOT ONE VOCABULARY. 1247 rows say '1', 794 say 'PROVEN', and the rest
     spread over '2'..'11', 'UNKNOWN', 'PROVEN (static)', '1 + 9', 'VERY HIGH'. Pass 7 asks
     whether a tier is CITED, not whether it is the right one - re-judging the tier is pass 8.
     So this checker deliberately does NOT validate the value against a vocabulary; it only
     distinguishes 'a tier is stated' from 'nothing is stated'. Conflating the two would make
     every non-numeric tier a pass-7 failure and would be a checker inventing its own standard.

  And one population trap: 140 of 395 documents have no Evidence section at all. Most are indexes,
  readmes and stubs that are not making claims. Judging those as failures would bury the real
  finding, so status is reported alongside and the summary separates documents that OWE an
  evidence section from documents that do not.

PLACEHOLDERS COUNT AS MISSING. A tier cell holding '-', '—', '?', 'TBD' or 'n/a' is a claim with
no tier wearing a dash, and pass 7's attack is precisely that.

Usage:
    python check_tier_presence.py --db "Database/FFXII TZA"
    python check_tier_presence.py --self-test
"""
import argparse
import io
import os
import re
import sys
import collections

SKIP_DIRS = {'_index', '_experiments', '_inbox', 'members', 'candidates'}
EVIDENCE_HEAD = re.compile(r'^##\s*\d*\.?\s*Evidence\s*$', re.M | re.I)
NEXT_HEAD = re.compile(r'^##\s', re.M)
TIER_HEAD = re.compile(r'\btiers?\b', re.I)
PLACEHOLDER = {'', '-', '--', '---', '—', '–', '?', 'tbd', 'n/a', 'na', 'none', 'todo'}
# Statuses that make claims and therefore owe an Evidence section.
OWES = ('DOCUMENTED', 'COMPLETE', 'AUDITED', 'VALIDATED', 'PARTIAL', 'REOPENED')


def split_row(line):
    """Cells of a markdown table row, or None if the line is not one.

    A SEPARATOR IS NOT A NON-ROW. `|---|---|` returns the empty list, not None: treating it as
    "not part of a table" splits every table in two between its header and its body, so the
    header is never seen with its own data. The self-test caught exactly that, on 9 of 12 cases,
    before this instrument was ever pointed at the corpus.
    """
    s = line.strip()
    if not s.startswith('|'):
        return None
    if set(s) <= set('|-: '):          # the ---|---|--- separator
        return []
    return [c.strip() for c in s.strip('|').split('|')]


def tables_in(body):
    """Yield (header_cells, [data_rows]) for each markdown table in a block of text."""
    rows, cur = [], []
    for line in body.splitlines():
        cells = split_row(line)
        if cells is None:
            if cur:
                rows.append(cur)
                cur = []
            continue
        if cells == []:                # the separator: stays inside the table
            continue
        cur.append(cells)
    if cur:
        rows.append(cur)
    for tbl in rows:
        if len(tbl) >= 2:
            yield tbl[0], tbl[1:]
        elif tbl:
            yield tbl[0], []


def status_of(text):
    m = re.search(r'^status:\s*(.+)$', text, re.M)
    return m.group(1).strip() if m else ''


def evidence_block(text):
    m = EVIDENCE_HEAD.search(text)
    if not m:
        return None
    rest = text[m.end():]
    nxt = NEXT_HEAD.search(rest)
    return rest[:nxt.start()] if nxt else rest


def section_tier(block):
    """A tier stated once in the section's PROSE, covering every claim under it.

    THE CORPUS PUTS THE TIER IN TWO PLACES AND THE FIRST VERSION OF THIS CHECKER COULD ONLY SEE
    ONE. Reading two flagged documents showed `**Tier 1**, and a two-session result:` and
    `**Tier 1 - structural, and verified by two independent implementations.**` opening their
    Evidence sections, above tables with no tier column. The tier is cited; it is simply cited
    once for the section instead of once per row. Scoring those as untiered claims would have
    reported ~90 documents for a defect that is a layout difference - the same error as reading
    the last column and calling a width a tier.
    """
    m = re.search(r'(?:^|[^A-Za-z])tiers?\b[\s:*_-]*([0-9]+|PROVEN|UNKNOWN|HIGH|VERY HIGH)',
                  block[:1200], re.I)
    return m.group(1) if m else None


GAP_WORDS = re.compile(
    r'not\s+established|not\s+measured|not\s+determined|not\s+proven|not\s+read|'
    r'not\s+observed|not\s+traced|not\s+recovered|not\s+identified|not\s+resolved|'
    r'nothing\s+runs\s+live|nothing\s+observed|no\s+runtime|'
    r'\bunknown\b|\bunproven\b|\bopen\b|\bnone\s+yet\b|\bno\s+evidence\b|\buntested\b',
    re.I)
# A row struck through, or saying so, is a RETRACTED claim - not an untiered one. Pass 24 owns
# retractions; pass 7 must not count a corrected claim as a missing tier, or the corpus would be
# penalised for having fixed something.
WITHDRAWN = re.compile(r'~~|\bwithdrawn\b|\bretracted\b|\boverturned\b|\bsuperseded\b', re.I)
CLAIM_HEAD = re.compile(r'\bclaims?\b|\bfinding\b|\bassertion\b', re.I)


def declares_gap(row, tier_idx):
    """Is this row an explicit NON-claim rather than an untiered claim?

    A row reading `| What the unread callees do | **not established** | - | UNKNOWN |` has no tier
    because there is nothing to tier. That is the document declaring a gap, which is the OPPOSITE
    of the defect pass 7 hunts - an assertion slipping through with no tier attached. Counting it
    as a failure would punish exactly the honesty the evidence standard asks for, so it is counted
    apart and shown, never silently exempted.
    """
    for i, cell in enumerate(row):
        if i == tier_idx:
            continue
        if GAP_WORDS.search(cell):
            return True
    return False


def audit_doc(text):
    """Return (verdict, detail, n_rows, n_missing) for one document's Evidence section."""
    block = evidence_block(text)
    if block is None:
        return 'NO-EVIDENCE-SECTION', '', 0, 0, 0, 0, 0
    tbls = [t for t in tables_in(block)]
    if not tbls:
        return 'NO-TABLE', '', 0, 0, 0, 0, 0
    sect = section_tier(block)
    total = missing = gaps = aux = withdrawn = 0
    notier = 0
    details = []
    for head, data in tbls:
        idx = next((i for i, h in enumerate(head) if TIER_HEAD.search(h)), None)
        if idx is None:
            # NOT EVERY TABLE UNDER THE EVIDENCE HEADING IS A CLAIM TABLE. The corpus puts
            # supporting data there too - `Subsystem/Edges/Disposition`, `Offset/A/B/delta`,
            # `Address/Body/Non-Audio callers/In the 174?`. Those rows are not claims and have no
            # business carrying a tier; reading them as untiered claims turned 23 documents into
            # a finding that was mostly my own parser. A table is judged only if it announces
            # claims - a claim/finding/assertion column - or states a tier for the section.
            if not any(CLAIM_HEAD.search(h) for h in head):
                aux += len(data)
                continue
            notier += 1
            total += len(data)
            if sect is None:
                missing += len(data)
                if data:
                    details.append('claim table with columns %s has no tier column and the '
                                   'section states none (%d rows)'
                                   % ('/'.join(h or '?' for h in head), len(data)))
            continue
        for row in data:
            if any(WITHDRAWN.search(c) for c in row):
                # A retracted claim is not a live claim, so it leaves the denominator too -
                # counting it would let a page look better or worse for having corrected itself.
                withdrawn += 1
                continue
            total += 1
            cell = row[idx] if idx < len(row) else ''
            if cell.strip().strip('*`').lower() in PLACEHOLDER:
                if declares_gap(row, idx):
                    gaps += 1
                elif sect is None:
                    missing += 1
                    claim = (row[0] if row else '')[:60]
                    details.append('no tier: %s' % claim)
                else:
                    notier += 1
    if total == 0:
        return 'NO-CLAIM-ROWS', '', 0, 0, 0, aux, withdrawn
    if missing:
        return 'MISSING', '; '.join(details[:4]), total, missing, gaps, aux, withdrawn
    if gaps and not notier:
        return 'DECLARED-GAPS', '%d row(s) state no tier because they state no claim' % gaps, \
               total, 0, gaps, aux, withdrawn
    if notier:
        # Every claim is tiered, but only because the SECTION states one. Reported apart from OK
        # because "one tier for the whole section" and "a tier per claim" are different promises,
        # and pass 8 - re-judging each tier against its own evidence - can only work on the second.
        return 'SECTION-TIER-ONLY', 'section states tier %s' % sect, total, 0, gaps, aux, withdrawn
    return 'OK', '', total, 0, gaps, aux, withdrawn


def self_test():
    """Known positives and negatives. A checker that has never been shown a defect it must
    catch is a checker nobody has reason to believe."""
    cases = [
        # (text, expected verdict, note)
        ("## 8. Evidence\n\n| Claim | Evidence | Tier |\n|---|---|---|\n| a | b | 1 |\n",
         'OK', 'a stated numeric tier passes'),
        ("## 8. Evidence\n\n| Claim | Evidence | Tier |\n|---|---|---|\n| a | b | PROVEN |\n",
         'OK', 'a non-numeric tier is still a stated tier - judging it is pass 8, not pass 7'),
        ("## 8. Evidence\n\n| Claim | Evidence | Tier |\n|---|---|---|\n| a | b |  |\n",
         'MISSING', 'an empty tier cell is the defect pass 7 exists to find'),
        ("## 8. Evidence\n\n| Claim | Evidence | Tier |\n|---|---|---|\n| a | b | - |\n",
         'MISSING', 'a dash is a missing tier wearing a dash'),
        ("## 8. Evidence\n\n| Claim | Evidence | Tier |\n|---|---|---|\n| a | b | — |\n",
         'MISSING', 'an em dash likewise'),
        ("## 8. Evidence\n\n| Claim | Evidence |\n|---|---|\n| a | b |\n",
         'MISSING', 'no tier column AND no section tier is claims with no tier'),
        ("## 8. Evidence\n\n**Tier 1**, and a two-session result:\n\n"
         "| claim | re-verified result |\n|---|---|\n| a | b |\n",
         'SECTION-TIER-ONLY',
         'a tier stated ONCE in the section prose covers the rows under it - the corpus does this'),
        ("## 8. Evidence\n\n**Tier 1 - structural.**\n\n"
         "| Claim | Evidence | Tier |\n|---|---|---|\n| a | b |  |\n",
         'SECTION-TIER-ONLY', 'an empty cell under a stated section tier inherits it'),
        ("## 8. Evidence\n\nNo tier word anywhere here.\n\n"
         "| Claim | Evidence | Tier |\n|---|---|---|\n| a | b | 1 |\n| c | d |  |\n",
         'MISSING', 'without a section tier, an empty cell is still the pass-7 defect'),
        ("## 8. Evidence\n\n| Type | Offsets | Width |\n|---|---|---|\n| a | 054, 058 | 4 |\n",
         'NO-CLAIM-ROWS',
         'no claim column and no tier column: supporting data under the heading, not judged'),
        ("## 8. Evidence\n\n| Claim | Offsets | Width |\n|---|---|---|\n| a | 054, 058 | 4 |\n",
         'MISSING',
         'but a CLAIM table whose last column is a width is still untiered - the width must '
         'never be read as a tier'),
        ("## 8. Evidence\n\n| Claim | Evidence | Tier |\n|---|---|---|\n"
         "| ~~a~~ **withdrawn** | b |  |\n",
         'NO-CLAIM-ROWS',
         'a struck-through row is a RETRACTED claim, not an untiered one - pass 24 owns those'),
        ("## 8. Evidence\n\n| Claim | Evidence | Tier |\n|---|---|---|\n"
         "| what the callees do | **not established** | - |\n",
         'DECLARED-GAPS', 'a row declaring a gap is the opposite of the pass-7 defect'),
        ("## 8. Evidence\n\nProse only, no table.\n",
         'NO-TABLE', 'prose evidence is not a claim table'),
        ("## 7. Evidence\n\n| Claim | Evidence | Tier |\n|---|---|---|\n| a | b | 1 |\n",
         'OK', 'the section number varies across the corpus'),
        ("## 8. Evidence\n\n| Claim | Evidence | Tier |\n|---|---|---|\n| a | b | 1 |\n\n"
         "## 9. Related\n\n| x | y | z |\n|---|---|---|\n| 1 | 2 | 3 |\n",
         'OK', 'a table in the NEXT section must not be pulled in'),
        ("# no evidence heading at all\n\nsome prose\n",
         'NO-EVIDENCE-SECTION', 'absent section is reported, not scored as a pass'),
        ("## 8. Evidence\n\n| Claim | Evidence | Tier |\n|---|---|---|\n| a | b | 1 |\n| c | d |  |\n",
         'MISSING', 'one bad row among good ones still fails the document'),
    ]
    bad = 0
    for i, (text, want, note) in enumerate(cases, 1):
        got = audit_doc(text)[0]
        ok = got == want
        if not ok:
            bad += 1
        print("  %-4s case %2d  want %-20s got %-20s  %s"
              % ('ok' if ok else 'FAIL', i, want, got, note))
    print("\nself-test: %d of %d cases pass" % (len(cases) - bad, len(cases)))
    return 1 if bad else 0


def mutation_control(db):
    """Prove the checker can still FAIL, on real documents, after all its refinements.

    THIS EXISTS BECAUSE THE CORPUS RESULT IS ZERO, AND I AM THE ONE WHO TUNED IT THERE. The first
    run reported 222 untiered claims across 87 documents. Reading the rows turned that into 0, in
    four steps - a tier stated once in section prose, auxiliary tables under the Evidence heading,
    rows declaring a gap, rows struck through. Each step was a category the corpus really makes,
    and each was driven by reading the text rather than by wanting a smaller number. But a zero
    produced by four rounds of my own narrowing is exactly the shape of a checker tuned until it
    agrees with me, and the protocol's own caution says to run a known-positive before believing
    a zero.

    So: take real documents that currently pass, inject one untiered claim into each, and require
    the verdict to flip. If any mutant survives, the zero above means nothing.
    """
    live = []
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in files:
            if f.endswith('.md'):
                p = os.path.join(root, f)
                t = io.open(p, encoding='utf-8', errors='replace').read()
                if audit_doc(t)[0] == 'OK':
                    live.append((p, t))
    live.sort()
    sample = live[::max(1, len(live) // 12)][:12]
    mutants = [
        ("| a claim with no tier at all | some evidence |  |\n", 'MISSING',
         'empty tier cell'),
        ("| a claim with a dash for a tier | some evidence | - |\n", 'MISSING',
         'dash tier'),
        ("| a claim with an em dash | some evidence | — |\n", 'MISSING',
         'em dash tier'),
    ]
    bad = 0
    run = 0
    print("MUTATION CONTROL - inject an untiered claim into documents that currently pass")
    for p, text in sample:
        block = evidence_block(text)
        rows = [ln for ln in block.splitlines() if ln.strip().startswith('|')]
        if len(rows) < 3:
            continue
        anchor = rows[-1]
        for inject, want, label in mutants:
            mutated = text.replace(anchor, anchor + "\n" + inject.rstrip("\n"), 1)
            got = audit_doc(mutated)[0]
            run += 1
            if got != want:
                bad += 1
                print("   SURVIVED  %-52s %-14s got %s"
                      % (os.path.basename(p)[:52], label, got))
    print("   %d mutants injected, %d caught, %d SURVIVED" % (run, run - bad, bad))
    if bad:
        print("   -> THE ZERO ABOVE IS NOT TRUSTWORTHY. The checker cannot see a defect it must.")
    else:
        print("   -> the checker still fails on a real untiered claim, so the zero is a real"
              " negative")
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--self-test", action="store_true", dest="self_test")
    ap.add_argument("--list", action="store_true", help="print every MISSING document's detail")
    ap.add_argument("--mutation-control", action="store_true", dest="mutation",
                    help="inject untiered claims into passing documents and require a failure")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.db:
        return ap.error("--db or --self-test required")
    if a.mutation:
        return mutation_control(a.db)

    docs = []
    for root, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in files:
            if f.endswith('.md'):
                docs.append(os.path.join(root, f))
    docs.sort()

    verdicts = collections.Counter()
    missing_docs = []
    owes_no_section = []
    rows_total = rows_missing = rows_gaps = rows_aux = rows_wd = 0
    for p in docs:
        text = io.open(p, encoding='utf-8', errors='replace').read()
        st = status_of(text)
        v, detail, n, miss, gp, ax, wd = audit_doc(text)
        verdicts[v] += 1
        rows_total += n
        rows_missing += miss
        rows_gaps += gp
        rows_aux += ax
        rows_wd += wd
        rel = os.path.relpath(p, a.db).replace(os.sep, '/')
        if v == 'MISSING':
            missing_docs.append((rel, st, miss, n, detail))
        elif v in ('NO-EVIDENCE-SECTION', 'NO-TABLE') and st.upper().startswith(OWES):
            owes_no_section.append((rel, st, v))

    print("FINAL-AUDIT-PROTOCOL pass 7 - tier presence")
    print("  documents scanned            : %d" % len(docs))
    for v in ('OK', 'SECTION-TIER-ONLY', 'DECLARED-GAPS', 'MISSING', 'NO-TABLE',
              'NO-CLAIM-ROWS', 'NO-EVIDENCE-SECTION'):
        print("    %-24s : %d" % (v, verdicts[v]))
    print("  claim rows with a tier column: %d" % rows_total)
    print("  claim rows with NO tier      : %d" % rows_missing)
    print("  rows untiered because they DECLARE A GAP (not a defect): %d" % rows_gaps)
    print("  rows in AUXILIARY tables under the heading (not claims, not judged): %d" % rows_aux)
    print("  rows WITHDRAWN / struck through (pass 24 owns those): %d" % rows_wd)

    if missing_docs:
        print("\n  DOCUMENTS WITH AT LEAST ONE UNTIERED CLAIM: %d" % len(missing_docs))
        for rel, st, miss, n, detail in (missing_docs if a.list else missing_docs[:25]):
            print("    %-62s %-12s %d/%d" % (rel[:62], st[:12], miss, n))
            if a.list and detail:
                print("        %s" % detail[:200])
        if not a.list and len(missing_docs) > 25:
            print("    ... %d more (use --list)" % (len(missing_docs) - 25))

    print("\n  A DOCUMENT MAKING CLAIMS OWES AN EVIDENCE SECTION. Documents whose status is one of")
    print("  %s but that have no evidence table: %d" % ('/'.join(OWES), len(owes_no_section)))
    for rel, st, v in owes_no_section[:20] if not a.list else owes_no_section:
        print("    %-62s %-12s %s" % (rel[:62], st[:12], v))
    if not a.list and len(owes_no_section) > 20:
        print("    ... %d more (use --list)" % (len(owes_no_section) - 20))

    print("\n  PASS 7 ASKS WHETHER A TIER IS CITED, NOT WHETHER IT IS EARNED - that is pass 8.")
    print("  No tier VALUE is judged here, and 'PROVEN' is as much a stated tier as '1'.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
