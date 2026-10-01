"""Entry-only citations, bucketed by how big the function is.

WHY. `engine_explained` counts a function as cited if any document names any address in its body;
`A` counts it only if a DOCUMENTED page names an address strictly INSIDE it. 7,384 functions sit
between: cited by a documented page, at the entry address and nowhere else. The scorer calls the
gap a mention and says so, and it also warns that interior citation is a PROXY - "a page can
explain a six-instruction function perfectly while citing only its entry".

Both cautions are right and they pull opposite ways, which is exactly the situation where a
population should be split rather than argued about. **The discriminator is SIZE.** An entry
citation of a 6-byte thunk is the whole function. An entry citation of a 4,000-byte body is a
mention, and no reading of the rules makes it anything else.

So this buckets the entry-only set by function size and prints the same buckets over the A set as a
control. Nothing is reclassified: the point is to say how much of the 7,384 is arguable and how
much is not.

WHAT IT CANNOT DO. Size is a proxy too. A 300-byte function can be a table of `mov`s that one
sentence explains, and a 40-byte one can hide a subtlety. The buckets bound the argument; they do
not settle any individual row.
"""
import bisect
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_dispositions as cd

DB = 'Database/FFXII TZA'
FUNCTIONS = 'Database/Tools/work/graph/functions.tsv'

# Chosen so the first bucket is "an entry citation IS the body" under any reading: MSVC's smallest
# real bodies are 16 bytes with alignment padding, and a jmp thunk is 6.
BUCKETS = [(0, 16, 'a thunk or stub - the entry IS the body'),
           (17, 64, 'a few instructions'),
           (65, 256, 'a small function'),
           (257, 1024, 'a substantial function'),
           (1025, 1 << 30, 'a large body - an entry citation is a mention')]


def bucket(n):
    for lo, hi, label in BUCKETS:
        if lo <= n <= hi:
            return (lo, hi, label)
    return BUCKETS[-1]


def citing_docs(db, targets):
    """For each target entry address, the DOCUMENTED pages that cite it.

    Only documented pages, because that is the population the gap is drawn from - a citation on an
    undocumented page never entered either dimension and listing it here would widen the queue with
    rows that were never counted.
    """
    out = collections.defaultdict(set)
    want = {('%08X' % e) for e in targets} | {('%08x' % e) for e in targets}
    for p in cd.docs(db):
        t = io.open(p, encoding='utf-8', errors='replace').read()
        # ANCHORED ON THE WHOLE LINE, WHICH IS A TRAP NOW THAT A STATUS MAY CARRY A REASON.
        # EVIDENCE-STANDARD addendum 2026-09-14bp rules that a status which is NOT DOCUMENTED
        # must state what is outstanding on the status line. It does not ask DOCUMENTED pages
        # to carry anything - but an author who reads the rule and adds a note to a DOCUMENTED
        # line would silently drop that page out of this gate, with nothing reporting it.
        # Zero pages do that today, so widening the match is a no-op measured now and a
        # landmine removed. The other four status parsers in the kit already tolerate it:
        # three capture the first token or use startswith, and progress.evidence_bearing
        # splits the reason off. This was the only one that did not.
        if not re.search(r'^status:\s*DOCUMENTED\b.*$', cd.frontmatter(t), re.M):
            continue
        rel = os.path.relpath(p, db)
        for h in set(cd.CITE.findall(t)):
            if h.upper() in want or h in want:
                out[int(h, 16)].add(rel)
    return out


def main():
    if '--list' in sys.argv:
        return listing()
    if not os.path.exists(FUNCTIONS):
        print('  CONTROL FAILED: no function list at %s' % FUNCTIONS)
        return 2
    sizes = cd.load_functions(FUNCTIONS)
    a_set, entry_only, any_interior, documented_any = cd.measure_a(DB, sizes)

    print('--- control: functions in the list: %d ---' % len(sizes))
    print('    A (documented page, interior citation)      : %6d' % len(a_set))
    print('    entry-only (documented page, entry address) : %6d' % len(entry_only))
    if not entry_only:
        print('  CONTROL FAILED: no entry-only citations found. Everything below is void.')
        return 2

    eb = collections.Counter(bucket(sizes.get(e, 0)) for e in entry_only)
    ab = collections.Counter(bucket(sizes.get(e, 0)) for e in a_set)
    tot_e, tot_a = sum(eb.values()), sum(ab.values())

    print()
    print('--- the %d ENTRY-ONLY functions, by size ---' % tot_e)
    print('    %-9s %6s %7s   %6s %7s   %s' % ('bytes', 'entry', '%', 'A', '%', 'what that size means'))
    settled = arguable = mention = 0
    for lo, hi, label in BUCKETS:
        k = (lo, hi, label)
        e, a = eb.get(k, 0), ab.get(k, 0)
        rng = '%d-%d' % (lo, hi) if hi < (1 << 30) else '%d+' % lo
        print('    %-9s %6d %6.1f%%   %6d %6.1f%%   %s'
              % (rng, e, 100.0 * e / max(1, tot_e), a, 100.0 * a / max(1, tot_a), label))
        if hi <= 16:
            settled += e
        elif lo >= 1025:
            mention += e
        else:
            arguable += e

    print()
    print('--- what the 7,384-style figure is actually made of ---')
    print('  %6d  functions where AN ENTRY CITATION IS THE WHOLE BODY (<= 16 bytes).' % settled)
    print('          Counting these as "a mention, not an explanation" UNDERSTATES the database.')
    print('  %6d  functions of 17-1024 bytes. ARGUABLE, and a size bucket cannot settle them.' % arguable)
    print('  %6d  functions over 1024 bytes cited at their entry and nowhere else.' % mention)
    print('          For these the scorer is right without qualification: it is a mention.')
    print()
    print('  THIS TOOL ARGUED THE CASE AND THE CASE WAS DECIDED. It used to end "neither dimension')
    print('  is corrected by this - engine_explained keeps counting entry citations and A keeps')
    print('  refusing them". On 2026-09-14 SWE2-AUDIT-SPEC adjudicated the rule (9efc6221) and')
    print('  engine_explained now takes an entry citation ONLY for a body under 128 bytes - which is')
    print('  the size-aware line the buckets below were built to argue for. A still refuses every')
    print('  entry citation, so the two dimensions still differ, but no longer in that way.')
    print()
    print('  SIZE IS A PROXY TOO. A 300-byte table of moves can be explained in one sentence and a')
    print('  40-byte body can hide a subtlety. The buckets bound the argument; they settle no row.')
    return 0


def listing():
    """The large entry-only bodies, as a work queue: biggest first, with who cites them."""
    sizes = cd.load_functions(FUNCTIONS)
    _a, entry_only, _i, _d = cd.measure_a(DB, sizes)
    big = sorted(((sizes.get(e, 0), e) for e in entry_only if sizes.get(e, 0) > 1024), reverse=True)
    print('--- entry-only bodies over 1024 bytes: %d ---' % len(big))
    print('    These are the sub-population where "a mention, not an explanation" needs no')
    print('    qualification: a documented page names the entry of a body this size and nothing')
    print('    inside it. Biggest first, because the cost of leaving one unexplained scales.')
    print()
    who = citing_docs(DB, [e for _s, e in big])
    for size, e in big:
        docs_ = sorted(who.get(e, ()))
        first = docs_[0] if docs_ else '(no DOCUMENTED citer found - re-check)'
        extra = '  +%d more' % (len(docs_) - 1) if len(docs_) > 1 else ''
        print('  %08X  %6d B  %s%s' % (e, size, first[:78], extra))
    print()
    print('  total bytes in this queue: %d' % sum(s for s, _e in big))

    out = None
    for i, arg in enumerate(sys.argv):
        if arg == '--out' and i + 1 < len(sys.argv):
            out = sys.argv[i + 1]
    if out:
        head = [
            '# Entry-only bodies over 1024 bytes - generated by check_entry_only_sizes.py --list --out',
            '# A DOCUMENTED page names the entry of each of these and nothing inside it. That is the one',
            '# slice of the engine_explained / A gap where "a mention, not an explanation" needs no',
            '# qualification - see EVIDENCE-STANDARD addendum 2026-09-13m for the other two slices.',
            '#',
            '# ACCEPTANCE, so this queue cannot be closed by citation alone: a row leaves when a',
            '# DOCUMENTED page cites an address STRICTLY INSIDE the body. That is the bar the A measure',
            '# already uses, check_dispositions checks it, and it CANNOT be met by adding the entry',
            '# address to another page - which is the failure mode a list of addresses invites.',
            '#',
            '# NOT A PRIORITY ORDER. Sorted by size because the cost of leaving one unexplained scales',
            '# with it, but a 1,100-byte dispatcher that unlocks a subsystem outranks a 5,000-byte leaf.',
            'entry\tsize_bytes\tciting_documented_pages',
        ]
        with io.open(out, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(head) + '\n')
            for size, e in big:
                cites = '; '.join(sorted(who.get(e, ()))) or '(none found)'
                fh.write('%08X\t%d\t%s\n' % (e, size, cites))
        print('  wrote %s' % out)
    return 0



if __name__ == "__main__":
    sys.exit(main())
