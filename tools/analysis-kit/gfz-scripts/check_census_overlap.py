"""Where two censuses claim the SAME instruction, is the offset difference constant?

THE OBSERVATION THAT PROMPTED IT. `002FF0D3  or dword ptr [rsi + 0x14], ecx` is recorded by three
censuses at three displacements: BattleStatsRecord +0x38, BattleSystemState +0x40, and SavePayload
+0x4E4CC. `rsi` holds one address, so at most one of those is the type whose field is being written -
unless the types NEST, in which case all three are true and are three views of the same bytes.

THE TEST, AND IT IS DECISIVE EITHER WAY. Collect every instruction site that appears in two censuses.
If the two types nest at a fixed position, the difference between the two recorded displacements is
the SAME at every shared site - that difference is the nesting offset. If the difference varies, the
censuses disagree about what the base register holds, and at least one attribution is wrong.

WHAT A CONSTANT DIFFERENCE DOES AND DOES NOT ESTABLISH. It establishes that every access the two
censuses share is consistent with one containing the other at that offset. It does NOT establish the
containment itself - two records reached through the same base with a fixed gap would look identical
here - and it cannot, because nothing in an access census names a type. It says the two censuses are
CONSISTENT, and it names the one offset at which they are. A varying difference is the stronger
result: it is a contradiction, and it names the sites that carry it.

A shared site is not by itself a defect. Displacement censuses are built by matching a base register
through a route, and one function can legitimately touch two records. The finding is the SHAPE of the
overlap, not its existence.
"""
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_census_widths as ccw
import kit_paths as KP  # noqa: E402

DB = os.path.join(KP.ROOT, 'Database', 'FFXII TZA')


def load():
    """(type, shift) -> {site -> set of offsets in THIS type's frame}."""
    per = {}
    for tname, fname, sbase, shift, extent in ccw.censused_types():
        path = None
        for root, _d, files in os.walk(DB):
            if fname in files:
                path = os.path.join(root, fname)
                break
        if path is None or sbase is not None:
            continue                       # a static catalogue is keyed by address, not displacement
        sites = collections.defaultdict(set)
        for n, line in enumerate(io.open(path, encoding='utf-8', errors='replace')):
            if n == 0 or not line.strip():
                continue
            c = line.rstrip('\n').split('\t')
            if len(c) < 6:
                continue
            try:
                site = int(c[2], 16)
                off = int(c[3], 16)
            except ValueError:
                continue
            if shift:
                off = ccw.rebase(off, shift, extent)
                if off is None:
                    continue
            sites[site].add(off)
        if sites:
            per[tname] = (sites, fname)
    return per


MIN_SITES = 5


def main():
    per = load()
    print('--- control: displacement censuses loaded: %d, distinct sites: %d ---'
          % (len(per), len(set().union(*[set(s) for s, _f in per.values()]))))
    if len(per) < 2:
        print('  CONTROL FAILED: fewer than two censuses. Nothing can overlap.')
        return 2
    print()

    names = sorted(per)
    consistent, contradictory, ambiguous, tautological, thin = [], [], [], [], []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared = set(per[a][0]) & set(per[b][0])
            if not shared:
                continue
            deltas = collections.Counter()
            multi = 0
            for s in shared:
                oa, ob = per[a][0][s], per[b][0][s]
                if len(oa) != 1 or len(ob) != 1:
                    multi += 1          # one site filed at two displacements in one census
                    continue
                deltas[next(iter(ob)) - next(iter(oa))] += 1
            if not deltas:
                ambiguous.append((a, b, len(shared), multi))
            elif len(deltas) == 1:
                d, n = deltas.most_common(1)[0]
                # TWO EXCLUSIONS, because an edge can agree without being evidence.
                #
                # SAME FILE. A sub-object census IS its parent's census read at a shift, so
                # "SavePayload = ImageBackedStateBlock + 0x8000" is not a measurement of anything -
                # it is the shift, returned. An edge between two views of one file is a tautology
                # and must not be allowed to hold the closure together.
                #
                # TOO FEW SITES. One delta over two shared sites is what two coincidental matches
                # produce by arithmetic; agreement needs room to fail before it means anything.
                if per[a][1] == per[b][1]:
                    tautological.append((n, a, b, d, per[a][1]))
                elif n < MIN_SITES:
                    thin.append((n, a, b, d))
                else:
                    consistent.append((n, a, b, d, multi))
            else:
                contradictory.append((len(shared), a, b, deltas, multi))

    consistent.sort(reverse=True)
    contradictory.sort(reverse=True)

    print('--- census pairs whose shared sites agree on ONE offset: %d ---' % len(consistent))
    print('    the two percentages are the shared sites as a fraction of EACH census, because a')
    print('    pair where one census is wholly contained in the other reads very differently from')
    print('    a pair that merely touches: containment is what a census DERIVED from another would')
    print('    look like, and that would make the agreement circular.')
    for n, a, b, d, multi in consistent:
        print('  %-24s + %-24s  %3d shared (%5.1f%% of %s, %5.1f%% of %s), %s = %s %+#x%s'
              % (a[:24], b[:24], n, 100.0 * n / len(per[a][0]), a[:12],
                 100.0 * n / len(per[b][0]), b[:12], b, a, d,
                 '   (%d multi-filed)' % multi if multi else ''))

    print()
    print('--- EXCLUDED as tautological: two views of ONE census file: %d ---' % len(tautological))
    for n, a, b, d, fname in tautological:
        print('  %-24s + %-24s  %3d shared in %s, %+#x' % (a[:24], b[:24], n, fname, d))
        print('        Both read the same rows; the offset IS the registered shift, returned.')
    print()
    print('--- EXCLUDED as too thin to fail: fewer than %d shared sites: %d ---'
          % (MIN_SITES, len(thin)))
    for n, a, b, d in thin:
        print('  %-24s + %-24s  %3d shared, would have said %+#x' % (a[:24], b[:24], n, d))
        print('        One delta over %d site(s) is arithmetic, not agreement.' % n)
    print()
    print('--- census pairs whose shared sites DISAGREE: %d ---' % len(contradictory))
    for n, a, b, deltas, multi in contradictory:
        print('  %-26s + %-26s  %3d shared site(s), %d different offsets:'
              % (a[:26], b[:26], n, len(deltas)))
        for d, c in deltas.most_common():
            print('        %+#10x  at %d site(s)' % (d, c))
        print('        NOT consistent with one type containing the other at a fixed offset.')

    if ambiguous:
        print()
        print('--- pairs whose shared sites are all multi-filed, so no offset can be read: %d ---'
              % len(ambiguous))
        for a, b, n, multi in ambiguous:
            print('  %-26s + %-26s  %d shared, %d multi-filed' % (a[:26], b[:26], n, multi))

    # ---- the transitive closure, which is what makes this a claim rather than a table ----------
    #
    # Each pair gives one equation: base(b) - base(a) = d. Taken together they are overdetermined -
    # ten equations over seven unknowns - so they can CONTRADICT each other even though every pair
    # agrees with itself. Propagating one base through the graph and re-deriving every edge is the
    # check: an edge that comes back with a different offset is a contradiction that no pairwise
    # measurement can see. This is the same shape as the pairwise test one level up, and it is worth
    # running for the same reason: agreement between two things is not agreement among all of them.
    adj = collections.defaultdict(list)
    for n, a, b, d, _m in consistent:
        adj[a].append((b, d))
        adj[b].append((a, -d))
    base = {}
    comps = []
    for t in names:
        if t in base or t not in adj:
            continue
        base[t] = 0
        stack = [t]
        comp = [t]
        while stack:
            u = stack.pop()
            for v, d in adj[u]:
                if v not in base:
                    base[v] = base[u] + d
                    comp.append(v)
                    stack.append(v)
        comps.append(sorted(comp, key=lambda x: base[x]))
    inconsistent = [(a, b, d, base[b] - base[a])
                    for _n, a, b, d, _m in consistent if base[b] - base[a] != d]

    print()
    print('--- transitive closure: %d equation(s) over %d base(s) ---' % (len(consistent), len(base)))
    if inconsistent:
        print('  CONTRADICTION. These edges do not survive propagation:')
        for a, b, d, got in inconsistent:
            print('    %s -> %s  measured %+#x, implied by the rest %+#x' % (a, b, d, got))
    else:
        print('  Every edge survives propagation. The %d measurement(s) are mutually consistent,'
              % len(consistent))
        print('  which %d equations over %d unknowns did not have to be.'
              % (len(consistent), len(base)))
    # An edge the closure asserts but no shared site measures. `BattleUnit` and `BattleStatsRecord`
    # land at the same base here, and their two censuses share NOT ONE instruction - the relation is
    # inferred through BattleSystemState, never observed. That is a weaker statement than a measured
    # edge and must not be read as the same thing.
    measured = {frozenset((a, b)) for _n, a, b, _d, _m in consistent}
    for comp in comps:
        for i, a in enumerate(comp):
            for b in comp[i + 1:]:
                if frozenset((a, b)) not in measured:
                    sh = len(set(per[a][0]) & set(per[b][0]))
                    print()
                    print('  INFERRED, NOT MEASURED: %s and %s are placed %+#x apart by the closure,'
                          % (a, b, base[b] - base[a]))
                    print('    and their censuses share %d instruction(s). The relation rests on the'
                          % sh)
                    print('    path through the other types, not on an access either census recorded.')
    for comp in comps:
        if len(comp) < 2:
            continue
        z = base[comp[0]]
        print()
        print('  one frame, offsets relative to %s:' % comp[0])
        prev = None
        for t in comp:
            same = '   SAME BASE as %s' % prev[0] if prev and base[t] == prev[1] else ''
            print('    %+#10x  %s%s' % (base[t] - z, t, same))
            prev = (t, base[t])

    # ---- the measured lattice against what the STORE DECLARES ---------------------------------
    #
    # The lattice is built from instruction overlaps and knows nothing about the field store. The
    # store's type-valued ctypes are built from allocation sites, constructors and pointer writes and
    # know nothing about the lattice. Where both speak about the same pair they must agree, and where
    # the lattice asserts an edge the store declares no embedding for, that edge is carrying weight
    # nothing else supports. This is the check that turns the contaminated edge from an argument into
    # a disagreement between two independent instruments.
    declared_embed = {}
    types_declared = set()
    tpath = os.path.join(DB, '_types', 'types.tsv')
    if os.path.exists(tpath):
        for n, line in enumerate(io.open(tpath, encoding='utf-8')):
            if n and line.strip():
                types_declared.add(line.split('\t')[0])
    fpath = os.path.join(DB, '_types', 'fields.tsv')
    if os.path.exists(fpath):
        for n, line in enumerate(io.open(fpath, encoding='utf-8')):
            if not n or not line.strip():
                continue
            c = line.rstrip('\n').split('\t')
            if len(c) < 6:
                continue
            inner = c[4].split('[')[0].strip()
            if inner in types_declared and inner != c[0]:
                try:
                    declared_embed[(c[0], inner)] = int(c[1], 16)
                except ValueError:
                    pass

    print()
    print('--- the measured lattice against the store\'s DECLARED embeddings ---')
    agree, disagree, unsupported, unseen = [], [], [], []
    for _n, a, b, d, _m in consistent:
        # base(b) - base(a) = d means b's base is LOWER by d, i.e. a sits inside b at +d.
        if (b, a) in declared_embed:
            want = declared_embed[(b, a)]
            (agree if want == d else disagree).append((b, a, d, want))
        elif (a, b) in declared_embed:
            want = declared_embed[(a, b)]
            (agree if want == -d else disagree).append((a, b, -d, want))
        else:
            unsupported.append((a, b, d))
    for (outer, inner), off in sorted(declared_embed.items()):
        if outer in per and inner in per:
            if not any((x[1], x[2]) in ((outer, inner), (inner, outer)) for x in
                       [(n, a, b) for n, a, b, _d, _m in consistent]):
                unseen.append((outer, inner, off))

    for outer, inner, got, want in agree:
        print('  AGREE        %-24s contains %-24s at %+#x, measured and declared'
              % (outer[:24], inner[:24], want))
    for outer, inner, got, want in disagree:
        print('  DISAGREE     %-24s contains %-24s: measured %+#x, declared %+#x'
              % (outer[:24], inner[:24], got, want))
    # An edge with no declaration of its own is not necessarily unsupported: if both its endpoints
    # are already positioned by DECLARED embeddings, the declarations imply its offset and the
    # overlap merely reproduces it - which is corroboration. The edges that matter are the ones
    # attaching a type to the lattice on overlap evidence ALONE, because nothing else can catch them
    # being wrong. That is exactly the shape of the BattleUnit edge.
    dadj = collections.defaultdict(list)
    for (outer, inner), off in declared_embed.items():
        if outer in per and inner in per:
            dadj[outer].append((inner, off))
            dadj[inner].append((outer, -off))
    dbase, dcomp = {}, {}
    for t in sorted(dadj):
        if t in dbase:
            continue
        dbase[t], dcomp[t] = 0, t
        stack = [t]
        while stack:
            u = stack.pop()
            for v, off in dadj[u]:
                if v not in dbase:
                    dbase[v], dcomp[v] = dbase[u] + off, t
                    stack.append(v)
    implied, alone = [], []
    for a, b, d in unsupported:
        if a in dcomp and b in dcomp and dcomp[a] == dcomp[b]:
            # declared bases: a sits at dbase[a] inside the component frame, so the displacement
            # difference the lattice measures should be dbase[a] - dbase[b].
            implied.append((a, b, d, dbase[a] - dbase[b]))
        else:
            alone.append((a, b, d))
    for a, b, d, want in implied:
        ok = 'reproduces it' if d == want else 'CONTRADICTS it (declared %+#x)' % want
        print('  IMPLIED      %-24s and %-24s differ by %+#x; the declared'
              % (a[:24], b[:24], d))
        print('               embeddings already imply that offset and the overlap %s.' % ok)
    for a, b, d in alone:
        print('  OVERLAP ONLY %-24s and %-24s differ by %+#x, and NO declaration'
              % (a[:24], b[:24], d))
        print('               positions either type. Nothing but this overlap holds the edge up.')
    for outer, inner, off in unseen:
        print('  UNSEEN       %-24s declares %-24s at %+#x and the two censuses share no'
              % (outer[:24], inner[:24], off))
        print('               instruction, so the lattice cannot check it. Not a disagreement.')
    print('  %d agree with a declaration, %d disagree, %d implied by declarations, %d held up by the'
          % (len(agree), len(disagree), len(implied), len(alone)))
    print('  overlap alone, %d declared but unmeasurable.' % len(unseen))

    print()
    print('  A constant difference says the two censuses are CONSISTENT with nesting at that offset.')
    print('  It does not establish the nesting: nothing in an access census names a type. A varying')
    print('  difference is the stronger result - it is a contradiction, and the sites are named.')
    print('  TWO TYPES AT THE SAME BASE are not thereby one type: a record and its own first member')
    print('  share an address. What the closure establishes is that they are not INDEPENDENT, and')
    print('  that a layout claim about one is a layout claim about the other.')
    return 1 if (contradictory or inconsistent) else 0


if __name__ == '__main__':
    sys.exit(main())
