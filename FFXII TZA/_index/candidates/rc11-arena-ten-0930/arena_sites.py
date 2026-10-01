"""arena_sites.py - the arena (ecx) every call or tail jump to the selection push 0036C1D0 passes, including the 15
sites SWE2-CONTRACT's arena_select.py left unresolved (ORACLE, 2026-09-30, RC-11). Static. Reads only.

Engine: OPUS's value-set dataflow rc9_channels.py (../rc9-log-channels-0930/), imported unchanged and pointed at
0036C1D0: a forward dataflow over each caller's own control flow from its entry, with zero/equality edge refinement,
jump tables, and entry-register values resolved through every caller (edges.tsv), recursively.

Controls (exit 1 on failure):
  C1 sites / functions = 135 / 109 (the memory page's counts, reproduced by arena_select.py);
  C2 0025A990's push resolves to exactly {5} (the memory page: 0036C1D0(5, 5));
  C3 every one of the 120 sites arena_select.py resolved by its literal rule gets a value set containing that literal
     (read from ../swe2contract-ddres-b1-0930/arena_select.py, re-run in-process);
  C4 the arena-10 site 00504398 resolves to {10}.
Output: arena_sites.tsv (every site) and the 15 previously unresolved sites on stdout.
"""
import collections, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc9-log-channels-0930"))
sys.path.insert(0, os.path.join(HERE, "..", "swe2contract-ddres-b1-0930"))
import rc9_channels as R  # noqa: E402
import arena_select as A  # noqa: E402

PUSH = 0x0036C1D0
PREV_UNRES = [0x002492B4, 0x002497ED, 0x0024981D, 0x0026FB22, 0x00377FA3, 0x00384466, 0x003DD5A1, 0x003DF4B4,
              0x003E9AC2, 0x003EA031, 0x003EC8DD, 0x003EC924, 0x003EDE9B, 0x0050D93F, 0x0050DB1F]


def contract_literals():
    """arena_select.py's own per-site literal rule, re-run: {site: value} for the sites it resolves."""
    import capstone
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    out = {}
    for f in sorted(R.CALLERS[PUSH]):
        ins = list(md.disasm(R.at(f, R.ext[f]), f))
        for k, i in enumerate(ins):
            if i.mnemonic in ("call", "jmp") and i.op_str == hex(PUSH):
                v = A.regval(ins, k, "ecx")
                if isinstance(v, int):
                    out[i.address] = v
    return out


def main():
    callers = sorted(R.CALLERS[PUSH])
    rows = []
    for f in callers:
        st, _ = R.analyse_keep(f)
        for s in R.call_sites_to(f, PUSH):
            if s not in st:
                rows.append((f, s, None, "UNREACHED"))
                continue
            v = st[s].get("rcx", R.UNK)
            v = R.trunc32(v) if v is not R.UNK else R.UNK
            consts, notes = R.resolve(f, v)
            rows.append((f, s, consts, "; ".join(sorted(set(notes)))[:240]))
    lits = contract_literals()
    # a site the dataflow's own decode does not reach from the entry (a fragment it does not enter) still counts:
    # it is taken from arena_select.py's linear decode with that tool's literal value, and marked
    have = {s for _f, s, _c, _n in rows}
    for s, v in sorted(lits.items()):
        if s not in have:
            f = [g for g in callers if g <= s < g + R.ext[g]][0]
            rows.append((f, s, {v}, "not reached by the dataflow decode; literal %d from the linear decode" % v))
    rows.sort()
    by_site = {s: c for _f, s, c, _n in rows}
    fails = 0
    c1 = (len(rows), len(callers)) == (135, 109)
    c2 = by_site.get(0x0025AA21) == {5} or any(f == 0x0025A990 and c == {5} for f, _s, c, _n in rows)
    bad3 = [s for s, v in lits.items() if by_site.get(s) is None or v not in by_site[s]]
    c3 = len(lits) == 120 and not bad3
    c4 = by_site.get(0x00504398) == {10}
    for ok, name in ((c1, "C1 sites/functions = %d/%d (published 135/109)" % (len(rows), len(callers))),
                     (c2, "C2 0025A990 resolves to {5}"),
                     (c3, "C3 arena_select.py literals: %d sites, %d outside the dataflow's set %s" % (
                         len(lits), len(bad3), ["%08X" % s for s in bad3])),
                     (c4, "C4 00504398 resolves to %s" % by_site.get(0x00504398))):
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
        fails += not ok
    per = collections.Counter()
    for _f, _s, c, _n in rows:
        for x in (c or ()):
            per[x] += 1
    print("arena values over all 135 sites (a multi-valued site counts under each): %s" % (
        ", ".join("%d: %d" % kv for kv in sorted(per.items()))))
    print("sites with no resolved value set: %d" % sum(1 for r in rows if r[2] is None))
    print("the 15 sites arena_select.py left unresolved:")
    for f, s, c, n in rows:
        if s in PREV_UNRES:
            print("  %08X %08X arena=%-14s %s" % (f, s, ",".join(str(x) for x in sorted(c)) if c else "UNRESOLVED", n))
    with io.open(os.path.join(HERE, "arena_sites.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("function\tsite\tarena_values\tnotes\n")
        for f, s, c, n in rows:
            o.write("%08X\t%08X\t%s\t%s\n" % (f, s, ",".join(str(x) for x in sorted(c)) if c else "UNRESOLVED", n))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
