#!/usr/bin/env python3
"""field_access_index.py - a (type, offset) -> accessor index over every route-seedable type.

F-6. "every writer of this field" is charter §7's first example query and the only one whose
blocker is a missing PASS, not missing prose: `global_refs` is address-keyed, so it names every
writer of a global, but `obj->field` is `[reg+disp]` with the object identified only by
dataflow. The route-seeded census already does the base-register resolution; this sweep runs it
over EVERY type whose route it models and writes one consolidated index beside fields.tsv.

    field_access_index.py [--max-depth 6]
                          [--out "Database/FFXII TZA/_types/field-access-index.tsv"]

THE INDEX IS OBSERVATIONS, NOT A LAYOUT. `disp` is a displacement the census saw touched and
`kind` the instruction's access kind (r/w/addr); whether a displacement is a field boundary is
a reading the store makes separately. `base` records the in-hand object offset at the access, so
a touch at absolute `disp` reached as [base+x] with base != 0 is a NESTED access - a field of a
sub-object - not a field of this object at disp. `zeroclear` flags stores of a provably-zero
register: the bytes are cleared, nothing about field boundaries follows.

COVERAGE IS STATED, NOT IMPLIED. Only routes the census models are swept (PTR / FN+delta /
STATIC / ARRAY+stride / PARRAY+stride / SLOTPTR, plus the derived CHAIN/EMBED/RELOFF
alternatives whose parent chain resolves to a seedable root). A derived child records its own
window out of the root walk - `disp`/`base` are child-relative with the embed offset already
removed, so a `BattleStatsRecord` row at `disp 0` is the stats record's own first field whether
the access came through `BattleUnit +0x698` or `SpawnRecord +0x80`. DYNAMIC, unrouted types,
and chains with no seedable root produce NO rows - and a type's absence from the index means
the instrument did not run, never that its fields are unwritten. The run prints the
denominator per route kind.

SHARED WALK, NOT A COPY. The census is gen_route_seeded_census.Census, imported; a sweep that
reimplemented it could disagree with the single-type tool and nobody would know which was right.
The host index is ONE pass over the image (a per-rule rescan is fine once, wasteful 134 times)
and, unlike sweep_route_seeded_census.py's, it also recognises the image-base-relative lea
idiom - `lea rX,[rip->imagebase]` then `lea rY,[rX + rva]` - that hosts_for() requires for
STATIC/ARRAY seeds. The two instruments must agree, so this index uses the hosts_for() rule.

usage as a query: `grep -P "^TYPE\\t" field-access-index.tsv | awk -F'\\t' '$4=="w" || $4=="rw"'`
  - writers are `w` AND `rw` (1,740 read-modify-write rows at the 2026-09-24 regeneration;
    `$4=="w"` alone silently omits every atomic/cmpxchg writer)
"""
import argparse
import collections
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402
import call_graph as CG  # noqa: E402
import check_default_instance_writers as W  # noqa: E402
import gen_route_seeded_census as R  # noqa: E402
import kit_paths as KP  # noqa: E402

from capstone.x86 import X86_OP_MEM, X86_OP_REG  # noqa: E402

DEFAULT_OUT = os.path.join(KP.ROOT, "Database", "FFXII TZA", "_types",
                           "field-access-index.tsv")


def build_index(img):
    """One pass over every function body -> per-route-kind host lookup.

    loads[a]   functions that `mov rX, [rip->a]`
    leas[a]    functions that `lea rX, [a]` (absolute or rip-relative constant)
    lea_disp   per function, the displacements of register-based non-indexed leas,
               for the image-base-relative idiom: a function with img.base in
               leas AND (addr - img.base) in lea_disp is a STATIC/ARRAY host.
    """
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
    ap.add_argument("--max-depth", type=int, default=6)
    ap.add_argument("--db", default=G.DB)
    ap.add_argument("--out", default=DEFAULT_OUT)
    a = ap.parse_args()

    img = W.Image()
    callers, _c, _s = CG.call_maps(G.EXE, G.FUNCS)
    types, fields, routes = R.store(a.db)
    print("indexing rip-relative loads and leas once for the whole sweep ...")
    loads, leas, lea_disp, mov_disp, imov = build_index(img)
    base_leaders = leas.get(img.base, set())
    print("  %d load targets, %d lea targets, %d functions with register leas"
          % (len(loads), len(leas), len(lea_disp)))

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

    skipped = collections.Counter()
    swept = 0
    rows_out = []
    for name, (size, route, _ctor) in sorted(types.items()):
        rules = R.parse_routes(route)
        if not rules:
            skipped[route.split("|")[0].strip().split()[0] if route else "NONE"] += 1
            continue
        swept += 1
        c = R.Census(img, size)
        acc, reached = None, 0
        for rule, _text in rules:
            c.stride = rule[3] if rule[0] in ("ARRAY", "PARRAY") else None
            c.parray_off = rule[2] if rule[0] == "PARRAY" else None
            c.derived = None
            if rule[0] in R.DERIVED:
                # a chain alternative: run the resolved ROOT route's hosts and let the
                # derived emit gate pull this type's window out of root coordinates
                specs, fails = R.derive_specs(types, fields, routes, name, rule)
                for rrule, _rtext, spec, _path in specs:
                    c.stride = rrule[3] if rrule[0] in ("ARRAY", "PARRAY") else None
                    c.parray_off = rrule[2] if rrule[0] == "PARRAY" else None
                    c.derived = spec
                    acc, n = c.run(rrule, hosts(rrule), a.max_depth, acc)
                    reached += n
                c.derived = None
                if not specs:
                    skipped["%s-unresolved" % rule[0]] += 1
                continue
            acc, n = c.run(rule, hosts(rule), a.max_depth, acc)
            reached += n
        for entry, site, d, base, kd, insn, z in c.rows:
            rows_out.append((name, d, base, kd, entry, site, insn,
                             "zeroclear" if z else ""))
    rows_out.sort(key=lambda r: (r[0], r[1], r[4], r[5]))

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with io.open(a.out, "w", encoding="utf-8", newline="") as f:
        f.write("type\tdisp\tbase\tkind\tfunction\tsite\tinstruction\tnote\n")
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for name, d, base, kd, entry, site, insn, note in rows_out:
            w.writerow((name, "0x%X" % d, "0x%X" % base, kd,
                        "%08X" % entry, "%08X" % site, insn, note))

    kinds = collections.Counter(r[3] for r in rows_out)
    tset = {r[0] for r in rows_out}
    print("\nswept %d types -> %d access rows over %d types with any touch"
          % (swept, len(rows_out), len(tset)))
    print("kinds: " + "  ".join("%s %d" % kv for kv in sorted(kinds.items())))
    print("unseedable by route kind:")
    for k, n in skipped.most_common():
        print("  %-8s %d" % (k, n))
    print("wrote %s" % a.out)


if __name__ == "__main__":
    main()
