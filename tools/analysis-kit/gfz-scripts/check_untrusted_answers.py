"""The register rows that say ANSWERED and nothing else: what are they, and can they be settled?

WHY. `progress.py` classifies a register cell of exactly `**ANSWERED**` as UNTRUSTED - "state
inferred from prose by the merge script" - and counts it NEITHER as closed nor as open. 296 rows
sit there. They are invisible to `questions_closed` in both directions: if they are genuinely
answered the score understates, and if they are open the denominator does.

A number that is excluded from both halves of a ratio is the one place a metric cannot be
self-correcting, so it is worth knowing what is actually in there before anyone proposes counting
them. This measures; it does not reclassify anything.

THE TEST. For each untrusted row, look for the same question id ELSEWHERE in the database - the
per-document sections that the register mirrors. Three outcomes:

  ANSWERED ELSEWHERE   a document carries the same id with real substance after its verdict. The
                       register row is a stale mirror and the answer already exists.
  OPEN ELSEWHERE       a document carries the id in an UNTICKED checkbox. ONE OF THE TWO IS STALE
                       and which one requires reading both - the first version of this file
                       asserted the register was the thin one, and all three of the actual cases
                       ran the other way: the document answered the question in its own prose and
                       nobody ticked the box the scorer counts.
  NOWHERE              the id appears only in the register. **THE LABEL IS WRONG AND IS KEPT
                       ONLY BECAUSE THE OUTPUT KEY IS PUBLISHED.** This test looks OUTSIDE the
                       register, so it cannot see an answer written INSIDE the row - and on
                       2026-09-13 all nine of these turned out to carry a full attributed answer
                       in their Question or Owner-document cell, with the thin `**ANSWERED**`
                       only in the Status column. J-A's owner cell gives `+0x04` as a uint32 row
                       count read at 120 sites; EZ-6 names its single reader 003122F4 and adds a
                       correction. Read NOWHERE as "no support outside the register", never as
                       "nothing supports it".

The third outcome is the interesting one: it is the population that would have to be worked rather
than reconciled.
"""
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import progress as pr

DB = 'Database/FFXII TZA'
REG = os.path.join(DB, '_index', 'OPEN-QUESTIONS.md')
ID = re.compile(r'^[A-Z]{1,3}-\d+$')


def untrusted_ids(text):
    """The ids whose only verdict is a bare `**ANSWERED**`, using progress.py's own classifier."""
    out = []
    for line in text.split('\n'):
        if not line.startswith('|') or pr.REG_SEP.match(line):
            continue
        cells = [c for c in pr.REG_CELL.split(line.strip().strip('|'))]
        if len(cells) < 2 or cells[0].strip().lower() in ('id', 'id '):
            continue
        vs = [pr._verdict(c) for c in cells[1:]]
        if 'open' in vs or 'closed' in vs:
            continue
        if 'untrusted' in vs:
            out.append((cells[0].strip().strip('*` '), line))
    return out


def main():
    if not os.path.exists(REG):
        print('  CONTROL FAILED: no register at %s' % REG)
        return 2
    text = io.open(REG, encoding='utf-8', errors='replace').read()
    rows = untrusted_ids(text)
    print('--- control: register rows classified UNTRUSTED by progress.py: %d ---' % len(rows))
    if not rows:
        # AN EMPTY PILE IS THE SUCCESS CONDITION, AND THIS USED TO REFUSE ON IT. The old branch
        # exited 2 saying "if progress.py still reports untrusted rows, this parser disagrees with
        # it and THAT is the finding" - while never asking progress.py anything. It asserted a
        # cross-check it did not run, which is the same defect EVIDENCE-STANDARD 15bk names for
        # absence claims: the negative has to be checked with the scan that was actually run. So
        # when the pile is empty the classifier is put to a CONSTRUCTED POSITIVE CONTROL. If a
        # bare `**ANSWERED**` cell still comes back untrusted and a cell carrying evidence prose
        # does not, then zero means zero; if it does not, the parser is broken and the zero is
        # worth nothing - which is the only reading that deserves a refusal. 2026-09-15, OPUS.
        probe = ('| id | verdict |\n| --- | --- |\n'
                 '| ZZ-1 | **ANSWERED** |\n'
                 '| ZZ-2 | **ANSWERED** 2026-01-01, see 00-Engine/foo.md - the field is a count. |\n')
        got = [i for i, _l in untrusted_ids(probe)]
        if got != ['ZZ-1']:
            print('  CONTROL FAILED: on a constructed register the classifier returned %r, want'
                  " ['ZZ-1']." % (got,))
            print('  A bare **ANSWERED** must read untrusted and an evidence-bearing cell must not,')
            print('  so the zero above says nothing about the register.')
            return 2
        print('  positive control passed: a constructed bare **ANSWERED** still reads UNTRUSTED,')
        print('  and an evidence-bearing cell does not. No register row is left whose only verdict')
        print('  is a state inferred from prose by the merge script.')
        return 0

    # Every other document, indexed by the ids it mentions with a verdict of its own.
    #
    # BOTH SHAPES, because the first version of this check scanned only TABLE ROWS and reported 293
    # of 296 as appearing nowhere - which would have been an artefact of the scan, not a fact about
    # the corpus. The per-document questions `progress.py` counts are CHECKBOX items (`- [ ]` /
    # `- [x]`) in prose, not table rows, so a table-only scan cannot see the place most answers
    # live. A measurement whose population is defined by what the instrument happens to parse is the
    # defect this session has now found five times.
    elsewhere = collections.defaultdict(list)
    mentions = collections.defaultdict(list)
    for p in pr.docs(DB):
        if os.path.abspath(p) == os.path.abspath(REG):
            continue
        t = io.open(p, encoding='utf-8', errors='replace').read()
        rel = os.path.relpath(p, DB)
        for line in t.split('\n'):
            s = line.strip()
            m = re.match(r'^-\s*\[([ x])\]\s*(.*)$', s)
            if m:
                for qid in re.findall(r'\b([A-Z]{1,3}-\d+)\b', m.group(2)[:160]):
                    elsewhere[qid].append(('closed' if m.group(1) == 'x' else 'open', rel))
                continue
            for qid in re.findall(r'\b([A-Z]{1,3}-\d+)\b', s):
                mentions[qid].append(rel)
            if not line.startswith('|'):
                continue
            cells = [c for c in pr.REG_CELL.split(line.strip().strip('|'))]
            if len(cells) < 2:
                continue
            qid = cells[0].strip().strip('*` ')
            if not ID.match(qid):
                continue
            vs = [pr._verdict(c) for c in cells[1:]]
            v = ('open' if 'open' in vs else 'closed' if 'closed' in vs
                 else 'untrusted' if 'untrusted' in vs else 'unstated')
            elsewhere[qid].append((v, os.path.relpath(p, DB)))

    tally = collections.Counter()
    fams = collections.Counter()
    nowhere = []
    disagree = []
    for qid, line in rows:
        fams[re.sub(r'-\d+$', '', qid)] += 1
        hits = elsewhere.get(qid, [])
        if not hits:
            if mentions.get(qid):
                tally['MENTIONED IN PROSE ONLY'] += 1
            else:
                tally['NOWHERE'] += 1
                nowhere.append(qid)
        elif any(v == 'closed' for v, _ in hits):
            tally['ANSWERED ELSEWHERE'] += 1
        elif any(v == 'open' for v, _ in hits):
            tally['OPEN ELSEWHERE'] += 1
            disagree.append((qid, [d for v, d in hits if v == 'open'][:1]))
        else:
            tally['MENTIONED, NO VERDICT'] += 1

    print()
    print('--- where each untrusted id stands OUTSIDE the register ---')
    for k in ('ANSWERED ELSEWHERE', 'OPEN ELSEWHERE', 'MENTIONED, NO VERDICT',
              'MENTIONED IN PROSE ONLY', 'NOWHERE'):
        if tally[k]:
            print('  %-22s %4d' % (k, tally[k]))

    if disagree:
        print()
        print('--- THE REGISTER SAYS ANSWERED AND A DOCUMENT SAYS OPEN: %d ---' % len(disagree))
        print('    These are not thin rows. One of the two is STALE - read both before deciding')
        print('    which. Every case measured so far ran the same way: the document answered the')
        print('    question in its own prose and left the checkbox unticked.')
        for qid, where in disagree[:20]:
            print('      %-8s open in %s' % (qid, where[0] if where else '?'))

    print()
    print('--- untrusted rows by id family (top 15) ---')
    for k, v in fams.most_common(15):
        print('  %-8s %4d' % (k, v))

    print()
    print('  NOTHING IS RECLASSIFIED HERE. An id answered elsewhere still needs its register row')
    print('  filled in by whoever owns that question, and a row that is NOWHERE needs the work')
    print('  doing. The point of the measurement is that those are different queues.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
