#!/usr/bin/env python3
"""sweep_route_seeded_census.py - run the route-seeded census over every routed type.

gen_route_seeded_census.py answers the question for one type. This runs it for all of them and
prints the only two outcomes that matter per gap row:

    a gap row the census LANDS IN   -> a refuted absence, to be read and corrected
    a gap row it does NOT land in   -> an absence with a stronger instrument behind it

Both are worth having and neither is a layout. Nothing here splits anything: a displacement is
an observation, and the store has three retractions on this exact type from treating one as a
reading.

SHARED WORK. The per-type tool rescans every function body to find its seed hosts, which is
fine once and wasteful 22 times, so this builds ONE index of rip-relative loads and leas per
function and looks the hosts up. The census itself is unchanged and is imported, not copied -
a sweep that reimplemented the walk could disagree with the single-type tool and nobody would
know which was right.

usage: sweep_route_seeded_census.py [--with-children] [--max-depth 6]
"""
import argparse
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402
import call_graph as CG  # noqa: E402
import check_default_instance_writers as W  # noqa: E402
import gen_route_seeded_census as R  # noqa: E402

from capstone.x86 import X86_OP_MEM, X86_OP_REG  # noqa: E402


def build_index(img):
    """function -> (set of rip-relative LOAD targets, set of lea'd addresses,
    per-function register-lea displacements). lea_disp exists for the
    image-base-relative idiom (`lea rX,[rip->imagebase]` then `lea rY,[rX+disp]`):
    hosts_for() in the single-type tool requires it for STATIC/ARRAY seeds, so a
    sweep index that skipped it would under-seed and silently disagree."""
    loads = collections.defaultdict(set)
    leas = collections.defaultdict(set)
    lea_disp = collections.defaultdict(set)
    mov_disp = collections.defaultdict(set)
    imov = collections.defaultdict(set)
    for e in sorted(img.sizes):
        for i in img.body(e):
            v = W.lea_value(i)
            if v is not None:
                leas[v].add(e)
                continue
            if i.mnemonic == "lea" and len(i.operands) == 2:
                m = i.operands[1].value.mem
                if i.operands[1].type == X86_OP_MEM and not m.index:
                    lea_disp[e].add(m.disp)
                continue
            if (i.mnemonic == "mov" and len(i.operands) == 2
                    and i.operands[0].type == X86_OP_REG
                    and i.operands[1].type == X86_OP_MEM):
                a = W.rip_target(i, i.operands[1])
                if a is not None:
                    loads[a].add(e)
                    continue
                m = i.operands[1].value.mem
                if m.index:
                    imov[e].add((m.scale, m.disp))
                else:
                    mov_disp[e].add(m.disp)
    return loads, leas, lea_disp, mov_disp, imov


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-children", action="store_true")
    ap.add_argument("--max-depth", type=int, default=6)
    ap.add_argument("--db", default=G.DB)
    a = ap.parse_args()

    img = W.Image()
    callers, _c, _s = CG.call_maps(G.EXE, G.FUNCS)
    types, fields, routes = R.store(a.db)
    print("indexing rip-relative loads and leas once for the whole sweep ...")
    loads, leas, lea_disp, mov_disp, imov = build_index(img)
    base_leaders = leas.get(img.base, set())
    print("  %d distinct load targets, %d distinct lea targets" % (len(loads), len(leas)))

    def hosts(rule):
        kind, addr = rule[0], rule[1]
        if kind == "FN":
            return sorted(callers.get(addr, ()))
        if kind == "VTABLE":
            return R.vtable_entries(img, addr)
        delta = addr - img.base
        h = set(loads.get(addr, ()))
        if kind in ("PARRAY", "SLOTPTR"):
            for e in base_leaders:
                if delta in mov_disp.get(e, ()):
                    h.add(e)
        if kind == "SLOTPTR":
            # the common shape leas the table base, then indexes it with disp 0; the
            # BIASED shape leas an enclosing base up to 0x400 below the table and lets
            # the load's displacement finish the address (`lea [T-8]` + `[rB + i*S + 8]`)
            for v, es in leas.items():
                if 0 <= addr - v <= 0x400:
                    h |= es
            stride = rule[3]
            for e, ss in imov.items():
                if (stride, addr) in ss:
                    h.add(e)
            for e in base_leaders:
                if ((stride, delta) in imov.get(e, ())
                        or any(0 <= delta - d <= 0x400 for d in lea_disp.get(e, ()))):
                    h.add(e)
            return sorted(h)
        if kind in ("PTR", "PARRAY", "PTABLE"):
            # PTABLE's seed is the same cell load as PTR - `mov rX,[rip->ADDR]` puts the
            # table's runtime base in a register, then slot loads index it
            return sorted(h)
        h |= set(leas.get(addr, ()))
        for e in base_leaders:
            if delta in lea_disp.get(e, ()):
                h.add(e)
        return sorted(h)

    routed = []
    for name, (size, route, _ctor) in sorted(types.items()):
        rules = R.parse_routes(route)
        if rules:
            routed.append((name, size, route, rules))
    print("types with a route this tool models: %d\n" % len(routed))

    refuted, upheld, nogap = [], [], 0
    orphan_bases = []
    for name, size, route, rules in routed:
        c = R.Census(img, size)
        h = []
        acc, reached = None, 0
        for rule, _text in rules:
            c.stride = rule[3] if rule[0] in ("ARRAY", "PARRAY") else None
            c.parray_off = rule[2] if rule[0] == "PARRAY" else None
            c.derived = None
            if rule[0] in R.DERIVED:
                specs, _fails = R.derive_specs(types, fields, routes, name, rule)
                for rrule, _rtext, spec, _path in specs:
                    c.stride = rrule[3] if rrule[0] in ("ARRAY", "PARRAY") else None
                    c.parray_off = rrule[2] if rrule[0] == "PARRAY" else None
                    c.derived = spec
                    hr = hosts(rrule)
                    h.extend(hr)
                    acc, n = c.run(rrule, hr, a.max_depth, acc)
                    reached += n
                c.derived = None
                continue
            hr = hosts(rule)
            h.extend(hr)
            acc, n = c.run(rule, hr, a.max_depth, acc)
            reached += n
        if acc is None:
            # fail closed, same as the single-type tool: no route yielded a host set,
            # so there is no census to report - not a measured zero
            print("%-34s 0x%-7X %-24s UNSEEDABLE - no route yielded a host set"
                  % (name, size, route))
            continue
        if a.with_children:
            for off, sz, nm, ctype in sorted(fields.get(name, [])):
                base = ctype.strip().rstrip("*").split("[")[0].strip()
                if base not in types or base == name:
                    continue
                crule = R.parse_route(types[base][1])
                if not crule or crule[0] not in R.SEEDABLE:
                    continue
                cc = R.Census(img, types[base][0])
                cc.stride = crule[3] if crule[0] in ("ARRAY", "PARRAY") else None
                cc.parray_off = crule[2] if crule[0] == "PARRAY" else None
                cacc, _r = cc.run(crule, hosts(crule), a.max_depth)
                if cacc is None:
                    continue
                for d, sites in cacc.items():
                    if 0 <= off + d < size:
                        acc[off + d] |= sites
        # GAP ROWS OF EMBEDDED CHILDREN COUNT TOO. The first version of this sweep listed only
        # the routed type's own rows, and on ManagerSingleton0209BE80 that reported "gaps 0" -
        # because both of its unread spans had just been moved inside ManagerSub0209BE80_AB30,
        # an EMBED child with no route of its own. The two spans this instrument had refuted
        # an hour earlier were invisible to the sweep built to look for exactly that.
        rows = list(sorted(fields.get(name, [])))
        for off, sz, nm, ctype in sorted(fields.get(name, [])):
            base = ctype.strip().rstrip("*").split("[")[0].strip()
            if base in types and base != name:
                for co, cs, cn, cct in sorted(fields.get(base, [])):
                    if off + co + cs <= size:
                        rows.append((off + co, cs, "%s.%s" % (base, cn), cct))
        rows.sort()
        gaps = [(o, s, n) for o, s, n, _ct in rows
                if s >= 256 and ("unobserved" in n.lower() or "gap" in n.lower())]
        print("%-34s 0x%-7X %-24s hosts %-4d offsets %-5d gaps %d"
              % (name, size, route, len(h), len(acc), len(gaps)))
        # A BASE IN NO DECLARED ROW IS A CANDIDATE SUB-OBJECT WITH ITS FUNCTIONS ATTACHED.
        # On ManagerSingleton0209BE80 every base resolves, which is what makes a non-resolving
        # one on another type worth a reader's time rather than noise.
        for b, k in R.report_bases(rows, acc, size, limit=0, indent="      BASE "):
            orphan_bases.append((name, b, k))
        if not gaps:
            nogap += 1
        for o, s, n in gaps:
            hit = sorted(d for d in acc if o <= d < o + s)
            tag = "REFUTED" if hit else "upheld "
            (refuted if hit else upheld).append((name, n, o, s, hit))
            print("      %s +0x%-7X %-28s %6d B : %d %s"
                  % (tag, o, n, s, len(hit), " ".join("0x%X" % x for x in hit[:8])))

    print()
    print("=" * 78)
    print("gap rows the census LANDS IN (absence refuted) : %d" % len(refuted))
    for name, n, o, s, hit in refuted:
        print("   %-32s %-26s +0x%-7X %6d B  %d offsets" % (name, n, o, s, len(hit)))
    print("gap rows it does NOT land in (absence upheld)  : %d" % len(upheld))
    print("routed types with no gap row at all            : %d" % nogap)
    print("bases in NO declared row (candidate sub-objects): %d" % len(orphan_bases))
    for name, b, k in orphan_bases:
        print("   %-32s +0x%-7X %d access(es)" % (name, b, k))
    print()
    print("A DISPLACEMENT IS AN OBSERVATION AND A LAYOUT IS A READING. Nothing is split here.")
    print("An upheld zero means 'not reached by a tracked displacement from the routes seeded',")
    print("which does not exclude a wholesale copy or a route form this tool declines to model.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
