#!/usr/bin/env python3
"""data_xref_scan.py - find every instruction that references a data address, offline.

Two blind spots this exists to defeat
-------------------------------------
**1. This binary does not address globals RIP-relative.** It loads the image base into a register
once and then uses `[reg + index*8 + disp]`, where `disp` is the address minus `0x00120000`:

    0032FB87  lea  r14, [rip - 0x20fb8e]          ; r14 = 0x00120000
    0032FB9B  mov  [r14 + rcx*8 + 0x21a6da8], rdx ; = 0x022C6DA8[rcx]

A RIP-relative xref scan therefore returns **zero hits for globals that are demonstrably
referenced**. Verified: a RIP-only scan of the 63-slot authored-data registry found 0 of 63 slots
referenced, and 0 hits for a control address read out of a disassembly by hand.

**2. Linear sweep across `.text` desynchronises.** `.text` contains data and padding; a sweep from
the section start loses instruction alignment and silently never decodes large stretches. The same
control returned 0 under linear sweep and 1 when disassembly started at the function entry.

So this disassembles **from every function entry in `functions.tsv`**, bounded by the recorded body
size, and matches memory operands by absolute address in either form.

A control is mandatory, not optional
------------------------------------
`--control <va>` re-runs the scan for an address the caller already knows is referenced. **If the
control returns zero the scan is broken and the result is refused**, because "no references" and
"my instrument cannot see references" produce identical output — which is how the first two
versions of this scan produced confident nonsense.

`sections_of` reports RAW sizes - do not build a data-section filter on it
--------------------------------------------------------------------------
This script matches by absolute address and never asks "is this a data section", so it is not
affected. A CALLER that adds such a filter is. `.data`'s raw size ends at `0x01F7E400` while its
virtual extent runs far past it, and the uninitialised globals worth scanning for - the shared
scratch at `022D8F30`, the transform workbench at `02EBEFC0` - live in that BSS tail. A filter
built on raw sizes discards exactly them: measured 2026-09-19 (OPUS), a three-group overlap scan
reported **one** address per group until the filter was rebuilt on `VirtualSize`, after which it
reported nine, ten and nine. Parse `VirtualSize` from the section table, and assert a known data
address passes the filter before trusting any absence.

Indexed access hides per-slot references
----------------------------------------
`[r14 + rax*8 + arrayBase]` references an ENTIRE ARRAY in one instruction. For a table like the
registry, expect hits on the array base rather than on individual slots, and **read an absence of
per-slot hits as an addressing mode, never as an unused slot.**

Usage
-----
    python data_xref_scan.py --exe <exe> --funcs <functions.tsv> --addr 0x02EBF130 \
        --control 0x022C6DA8
    python data_xref_scan.py ... --range 0x02EBF008 0x02EBF1F8
    python data_xref_scan.py --self-test
"""
import argparse
import collections
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
IMAGE_BASE = 0x120000


def sections_of(blob):
    import ext_string_probe as P
    return P.sections(blob)


def entries(path, limit=0):
    """(va, size) for every non-funclet function in functions.tsv."""
    out = []
    for n, line in enumerate(io.open(path, encoding="utf-8", errors="replace")):
        if n == 0:
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) < 3 or p[1].startswith(("Unwind@", "Catch_All@")):
            continue
        try:
            out.append((int(p[0], 16), int(p[2])))
        except ValueError:
            pass
        if limit and len(out) >= limit:
            break
    return out


def scan(blob, secs, funcs, wanted):
    """wanted: set of absolute VAs -> {va: [(insn_va, mnemonic, op_str, func_va)]}"""
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_REG_RIP

    def off(va):
        for _n, ro, sz, v in secs:
            if v <= va < v + sz:
                return ro + (va - v)
        return None

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    out = collections.defaultdict(list)
    for fva, fsize in funcs:
        o = off(fva)
        if o is None or fsize <= 0:
            continue
        for i in md.disasm(blob[o:o + fsize], fva):
            for op in i.operands:
                if op.type != X86_OP_MEM:
                    continue
                d = op.mem.disp
                if op.mem.base == X86_REG_RIP:
                    ea = i.address + i.size + d
                elif d > 0x100000:
                    # image-base-register form; also covers [reg+index*scale+disp]
                    ea = IMAGE_BASE + d
                else:
                    continue
                if ea in wanted:
                    out[ea].append((i.address, i.mnemonic, i.op_str, fva))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe")
    ap.add_argument("--funcs")
    ap.add_argument("--addr", action="append", default=[])
    ap.add_argument("--range", nargs=2, metavar=("LO", "HI"))
    ap.add_argument("--stride", type=lambda s: int(s, 0), default=8)
    ap.add_argument("--control", help="a VA known to be referenced; the scan is refused without it")
    ap.add_argument("--limit-funcs", type=int, default=0)
    ap.add_argument("--show", type=int, default=8)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not (a.exe and a.funcs):
        return ap.error("--exe and --funcs required")

    wanted = set(int(x, 0) for x in a.addr)
    if a.range:
        lo, hi = int(a.range[0], 0), int(a.range[1], 0)
        wanted |= set(range(lo, hi + 1, a.stride))
    ctrl = int(a.control, 0) if a.control else None
    if ctrl:
        wanted.add(ctrl)
    if not wanted:
        return ap.error("--addr or --range required")

    blob = io.open(a.exe, "rb").read()
    secs = sections_of(blob)
    funcs = entries(a.funcs, a.limit_funcs)
    print("scanning %d function bodies for %d address(es)" % (len(funcs), len(wanted)))
    res = scan(blob, secs, funcs, wanted)

    if ctrl:
        n = len(res.get(ctrl, []))
        print("CONTROL %08X: %d reference(s)" % (ctrl, n))
        if n == 0:
            print("\n  ** CONTROL RETURNED ZERO - THE SCAN IS BROKEN AND THE RESULT IS REFUSED. **")
            print("  'no references' and 'cannot see references' look identical; do not report"
                  "\n  this run as evidence of absence.")
            return 2
        print("  control passes - absence below is meaningful\n")

    found = {k: v for k, v in res.items() if k != ctrl}
    print("addresses with at least one reference: %d of %d"
          % (len(found), len(wanted) - (1 if ctrl else 0)))
    for ea in sorted(found):
        rows = found[ea]
        fns = sorted({r[3] for r in rows})
        print("\n  %08X  %d ref(s) in %d function(s)" % (ea, len(rows), len(fns)))
        for iva, mn, ops, fva in rows[:a.show]:
            print("      %08X  %-7s %-46s  [fn %08X]" % (iva, mn, ops[:46], fva))
        if len(rows) > a.show:
            print("      ... %d more" % (len(rows) - a.show))
    return 0


def self_test():
    ok = True
    rows = entries.__doc__ is not None
    if not rows:
        print("SELF-TEST FAILED: missing docstring"); ok = False
    # the addressing rule: disp above 0x100000 with a non-RIP base is image-base-relative
    if IMAGE_BASE + 0x21A6DA8 != 0x022C6DA8:
        print("SELF-TEST FAILED: image-base arithmetic"); ok = False
    if not ok:
        return 1
    print("self-test ok: image-base displacement arithmetic correct "
          "(0x120000 + 0x21A6DA8 = 0x022C6DA8, the control read out of FUN_0032fb70 by hand)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
