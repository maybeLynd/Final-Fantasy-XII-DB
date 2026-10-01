#!/usr/bin/env python3
"""check_span_access.py - unobserved spans that are not unobserved.

WHY. Four times now the store has carried an absence claim inherited from a census that could not
see the access: SpawnRecord +0x19 (a taken address), seventeen "no writer" rows (the same class,
measured), eighty-nine Phyre prefixes (the reflection never described them), and
ManagerSingleton0209BE80 +0xB244 - the largest span in the store, claiming "no censused access"
across 23,224 bytes while 99 distinct displacements inside it are touched by 32 functions.

That is a dominant error mode, not four incidents, so it deserves an instrument.

For each declared span this counts the distinct displacements inside its extent that appear as a
based memory operand anywhere in .text, and the functions using them.

THE COLLISION PROBLEM, WHICH IS WHY --min-offset EXISTS AND DEFAULTS HIGH. A displacement is not a
type: `[rcx+0x18]` occurs in hundreds of unrelated structures, so a hit on a small offset means
nothing. A hit on +0xBBC0 is another matter - few objects are that large, and the count of
distinct types that could own it is small. The default floor is 0x400 and the report says plainly
that everything below it was skipped rather than cleared.

A HIT IS A LEAD, NOT A REFUTATION. It says the span's extent contains displacements something
uses, which is a reason to look, not proof that this type is what is being indexed.
"""
import argparse
import collections
import csv
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP

import member_reach_scan as M
import kit_paths as KP  # noqa: E402

DB = KP.DB  # was os.path.join("..", "..", "..", "FFXII TZA") - same defect as the EXE path
# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-offset", type=lambda x: int(x, 0), default=0x400,
                    help="ignore spans starting below this; small displacements collide")
    ap.add_argument("--min-size", type=int, default=64)
    ap.add_argument("--top", type=int, default=20)
    a = ap.parse_args()

    raw = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off = pe + 24 + opt
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        if nm == ".text":
            TVA, TVS, TPR = ib + va, vs, pr
        off += 40
    blob = raw[TPR:TPR + TVS]
    fsizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    disp = collections.defaultdict(set)      # displacement -> functions
    width = collections.defaultdict(set)     # displacement -> access widths seen
    for fn in sorted(fsizes):
        o = fn - TVA
        if not (0 <= o < len(blob)):
            continue
        for i in md.disasm(blob[o:o + fsizes[fn]], fn):
            for op in i.operands:
                if op.type != X86_OP_MEM or op.mem.base in (0, X86_REG_RIP):
                    continue
                # STACK FRAMES ARE NOT OBJECTS, and at these magnitudes they dominate.
                # A function with 4 KB of locals produces `[rsp+0x1090]`, which is
                # indistinguishable from a field at +0x1090 unless the base is checked.
                # This contaminant put ManagerSub0209BE80_8FA0 +0x1088 at 2.98x on the first
                # run; every one of its "hits" was a stack slot or an unrelated object.
                # RSP is unambiguous. RBP is excluded too and that is a judgement: with frame
                # pointer omission RBP is often a general register, so this loses some real
                # hits - preferred to reporting stack slots as fields.
                if op.mem.base in (X86_REG_RSP, X86_REG_RBP):
                    continue
                if op.mem.disp >= a.min_offset:
                    disp[op.mem.disp].add(fn)
                    width[op.mem.disp].add(op.size)
    keys = sorted(disp)

    rows = [r for r in list(csv.reader(io.open(os.path.join(DB, "_types", "fields.tsv"),
                                               encoding="utf-8"), delimiter="\t"))[1:]
            if len(r) > 3]
    import bisect
    out, skipped_small, skipped_low = [], 0, 0
    for r in rows:
        if not r[3].startswith(("unobservedSpan", "unobservedTail", "unread")):
            continue
        if not r[2].isdigit():
            continue
        sz = int(r[2])
        try:
            lo = int(r[1], 16)
        except ValueError:
            continue
        if sz < a.min_size:
            skipped_small += 1
            continue
        if lo < a.min_offset:
            skipped_low += 1
            continue
        hi = lo + sz
        i0 = bisect.bisect_left(keys, lo)
        i1 = bisect.bisect_left(keys, hi)
        ds = keys[i0:i1]
        if not ds:
            continue
        fns = set().union(*(disp[d] for d in ds))
        # WIDTH COHERENCE - the discriminator, learned from two splits and two
        # dismissals. A real record has ONE access width per offset: every offset of
        # ManagerSingleton +0xBBC0 and of the PDeferredLightingBase pointer table did.
        # Where several unrelated objects share a displacement the widths contradict,
        # and overlapping qwords appear - which is what killed +0x1088.
        coh = sum(1 for d in ds if len(width[d]) == 1) / float(len(ds))
        out.append((len(ds), len(fns), r[0], r[1], sz, ds, coh))

    # THE DENSITY BASELINE, and it is the whole difference between a lead and noise.
    # A raw hit count is worthless: offsets near 0x660 are used by hundreds of unrelated
    # structures, so ANY 2,448-byte window there is full of touched displacements. What matters
    # is whether a span is touched MORE than a typical window of its size at its magnitude.
    # Baseline = the fraction of all offsets in the same power-of-two band that are touched.
    def band(x):
        return x.bit_length()
    inband = collections.Counter()
    for d in keys:
        inband[band(d)] += 1
    bandwidth = {b: (1 << b) - (1 << (b - 1)) for b in inband}

    print("spans considered: size >= %d and offset >= 0x%X" % (a.min_size, a.min_offset))
    print("   skipped, too small : %d" % skipped_small)
    print("   skipped, offset too low to be distinctive : %d  <- NOT cleared, just not judged"
          % skipped_low)
    print()
    print("DENSITY BASELINE - fraction of offsets touched, by magnitude band:")
    for b in sorted(inband):
        print("     0x%-7X..0x%-8X  %5d touched of %7d  (%.1f%%)"
              % (1 << (b - 1), (1 << b) - 1, inband[b], bandwidth[b],
                 100.0 * inband[b] / bandwidth[b]))
    print()
    scored = []
    for nd, nf, ty, offs, sz, ds, coh in out:
        lo = int(offs, 16)
        b = band(lo)
        base = inband[b] / float(bandwidth[b])
        expected = base * sz
        enrich = (nd / expected) if expected > 0 else 0.0
        scored.append((enrich, nd, expected, nf, ty, offs, sz, coh))
    print("SPANS RANKED BY ENRICHMENT OVER THAT BASELINE (not by raw hits): %d" % len(scored))
    print("%-30s %-9s %7s %6s %7s %6s %6s"
          % ("type", "offset", "bytes", "disps", "enrich", "coher", "fns"))
    for enrich, nd, exp, nf, ty, offs, sz, coh in sorted(scored, key=lambda x: -x[0])[:a.top]:
        flag = ("  <- LEAD" if enrich >= 2.0 and nd >= 5 and coh >= 0.9
                else "  (enriched but INCOHERENT widths - probably several objects)"
                if enrich >= 2.0 and nd >= 5 else "")
        print("%-30s %-9s %7d %6d %6.2fx %5.0f%% %6d%s"
              % (ty[:30], offs, sz, nd, enrich, 100 * coh, nf, flag))
    print()
    print("A raw hit count is not evidence. Offsets near 0x660 are used by hundreds of unrelated")
    print("structures, so any window there looks busy; enrichment near 1.00x means the span is")
    print("exactly as touched as its neighbourhood, which is what 'no signal' looks like.")
    print("COHERENCE is the discriminator: a real record has ONE access width per offset.")
    print("Both spans split so far scored 100%; both dismissed ones had contradictory")
    print("widths and overlapping qwords. Even a LEAD means read the base register first.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
