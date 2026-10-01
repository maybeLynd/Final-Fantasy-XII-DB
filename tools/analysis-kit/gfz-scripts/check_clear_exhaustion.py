#!/usr/bin/env python3
"""check_clear_exhaustion.py - is a type cleared ANYWHERE, by any length?

WHY THIS EXISTS. `check_bulk_write_lifetime.py` finds clears whose length is a LITERAL. That is
half the population. `MessageWindowRecord` is cleared by `memset(block, 0, size)` with the length
in a register, and no literal sweep can ever see it - the only way through was reading the
allocation path by hand. Having done that by hand four times (`CharacterRenderObject`,
`LegacyPs2GsTextureContext`, `CharacterRenderSystemTail`, `BootSingleton01F7F598`), the procedure
is stable enough to write down.

THE PROCEDURE, which is an exhaustion rather than a search. A type's spans are UNDEFINED only if
every one of these is negative:

  1. the allocator named in `allocation_site` makes no `memset`/`memcpy` call - of ANY length;
  2. nor does any callee one level below it;
  3. the constructor named in `ctor` makes none, nor its callees one level down;
  4. no literal bulk write whose length equals the type's declared size exists anywhere.

Check 1-3 are the ones that matter, and they are deliberately length-blind: a clear hiding behind
a register is exactly what check 4 alone would miss. If ANY of them is positive the type is a
CANDIDATE FOR ZERO and a human reads the site; only an all-negative type is reported as a
candidate for UNDEFINED, and even then the verdict is written by a person, because "no clear on
these four routes" is not the same as "no clear".

WHAT IT CANNOT DO. It reads the addresses out of the `allocation_site` and `ctor` prose, so a type
whose columns name no address is skipped and said to be skipped. It follows one call level, like
every other instrument here. And an interior type is only as well-served as its parent: the
containment argument that settled the eleven `ManagerSub*` types is not automated here.

    python check_clear_exhaustion.py
    python check_clear_exhaustion.py --type BootSingleton01F7F598
"""
import argparse
import collections
import csv
import io
import os
import re
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_REG

import member_reach_scan as M
import kit_paths as KP

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE
BULK = {0x00861EC0: "memset", 0x00861EBA: "memcpy"}
ADDR = re.compile(r"\b(00[0-9A-Fa-f]{6})\b")
SPAN = re.compile(r"^(unobserved|unread)", re.I)


def load_text():
    raw = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    base = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off = pe + 24 + opt
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        if nm == ".text":
            return raw, base + va, vs, pr
        off += 40
    raise SystemExit("no .text")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--type", default=None)
    ap.add_argument("--all-spans", action="store_true",
                    help="include spans that already carry a verdict. THIS IS THE CONTROL: "
                         "replaying the four types settled by hand is the only way to know "
                         "the procedure reproduces a known answer instead of merely running.")
    a = ap.parse_args()

    types = {}
    with io.open(os.path.join(a.db, "_types", "types.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if not f or not f[0] or len(f) < 7:
                continue
            try:
                sz = int(f[1], 0)
            except ValueError:
                continue
            types[f[0]] = (sz, f[4], f[6] if len(f) > 6 else "", f[5] if len(f) > 5 else "")

    spans = collections.defaultdict(list)
    with io.open(os.path.join(a.db, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) >= 9 and SPAN.match(f[3]) and (a.all_spans or "LIFETIME" not in f[8]):
                spans[f[0]].append(int(f[2]))

    raw, tva, tvs, tpr = load_text()
    blob = raw[tpr:tpr + tvs]
    fsizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    cache = {}

    def il_of(fn):
        if fn not in cache:
            o = fn - tva
            if o < 0 or o >= len(blob) or fn not in fsizes:
                cache[fn] = []
            else:
                try:
                    cache[fn] = list(md.disasm(blob[o:o + fsizes[fn]], fn))
                except Exception:
                    cache[fn] = []
        return cache[fn]

    def bulk_and_callees(fn):
        b, c = [], set()
        for i in il_of(fn):
            if i.group(2) and i.operands and i.operands[0].type == X86_OP_IMM:
                t = i.operands[0].imm
                if t in BULK:
                    b.append((i.address, BULK[t]))
                else:
                    c.add(t)
        return b, c

    # one pass for every literal bulk length in the image
    lit = collections.defaultdict(list)
    for fn in sorted(fsizes):
        r8 = None
        for i in il_of(fn):
            if (i.mnemonic == "mov" and len(i.operands) == 2
                    and i.operands[0].type == X86_OP_REG
                    and i.reg_name(i.operands[0].reg) in ("r8d", "r8")
                    and i.operands[1].type == X86_OP_IMM):
                r8 = i.operands[1].imm
                continue
            if i.group(2):
                if (i.operands and i.operands[0].type == X86_OP_IMM
                        and i.operands[0].imm in BULK and r8):
                    lit[r8].append((fn, i.address))
                r8 = None

    rows = []
    for t, (sz, alloc, dtor, ctor) in sorted(types.items()):
        if a.type and t != a.type:
            continue
        if not spans.get(t):
            continue
        addrs = set()
        for col in (alloc, ctor):
            for m in ADDR.finditer(col or ""):
                v = int(m.group(1), 16)
                if v in fsizes:
                    addrs.add(v)
        if not addrs:
            rows.append((t, sz, sum(spans[t]), len(spans[t]), None, "SKIPPED - no address in "
                         "allocation_site/ctor"))
            continue
        pos = []
        for fn in sorted(addrs):
            b, cs = bulk_and_callees(fn)
            if b:
                pos.append((fn, b[0][1], b[0][0], "direct"))
            for c in sorted(cs):
                b2, _ = bulk_and_callees(c)
                if b2:
                    pos.append((c, b2[0][1], b2[0][0], "callee of %08X" % fn))
        nlit = len(lit.get(sz, []))
        if pos:
            v = "CANDIDATE ZERO - %s at %08X (%s)" % (pos[0][1], pos[0][2], pos[0][3])
        elif nlit:
            v = "CANDIDATE ZERO - %d literal clear(s) of 0x%X elsewhere" % (nlit, sz)
        else:
            v = "CANDIDATE UNDEFINED - no clear on any of the four routes"
        rows.append((t, sz, sum(spans[t]), len(spans[t]), bool(pos), v))

    rows.sort(key=lambda x: -x[2])
    print("types with unanswered spans: %d" % len(rows))
    print()
    print("%-30s %7s %6s %5s  %s" % ("type", "size", "spanB", "rows", "verdict"))
    for t, sz, sb, nr, _, v in rows:
        print("%-30s %7X %6d %5d  %s" % (t[:30], sz, sb, nr, v))
    print()
    c = collections.Counter(v.split(" - ")[0] for _, _, _, _, _, v in rows)
    print("summary: %s" % dict(c))
    print()
    print("A CANDIDATE IS NOT A VERDICT. Every row above needs the site read before anything is")
    print("written to the store; this narrows which sites to read, and nothing more.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
