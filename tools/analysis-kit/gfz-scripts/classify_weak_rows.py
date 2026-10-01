#!/usr/bin/env python3
"""classify_weak_rows.py - what IS the residual, exactly? One taxonomy, so the number stops moving.

THE NUMBER HAS MOVED THREE TIMES IN A DAY and every move was a measurement error, not progress:
378 became 134 when the "non-span" filter was found to miss `unobservedTail`, and 134 became 120
as rows were read. That is a metric nobody should trust, so this replaces the single number with
a taxonomy, because "weak" was hiding five different situations that need five different things.

THE BUCKETS, in order of how much work they actually represent:

  MEASURED ABSENCE     the evidence says, in so many words, that nothing accesses this range -
                       "absence: no access at this displacement in the family". These are not
                       fields awaiting a reading. They are a RESULT: the bytes are proven
                       untouched by the instrument that looked. Counting them as outstanding
                       work overstates the residual.
  DECLARED GAP         "width = declared span, not an instruction access" - the row exists to
                       satisfy the sum invariant and its name is cosmetic. Same story.
  ADDRESS TAKEN ONLY   the only citation is a `lea` at this offset. The address escapes, so no
                       width or representation can be read from the site; it needs the callee.
  MECHANISM ONLY       the citation is a function, not an instruction - an FN route base or a
                       shared accessor. Real evidence about ownership, silent about layout.
  READABLE             there are real accesses and a representation could be read. THIS is the
                       bucket that represents outstanding OPUS work on this frontier.

It writes nothing. The point is to know which bucket a row is in before spending a pass on it.

    python classify_weak_rows.py --db "<db>"
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
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

import member_reach_scan as M
import kit_paths as KP

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE
SPAN = re.compile(r"^(unobserved|unread|pad)", re.I)
ADDR = re.compile(r"\b(00[0-9A-Fa-f]{6})\b")
ABSENCE = re.compile(r"absence:|no access at this displacement|no read at this displacement|"
                     r"none in this range", re.I)
GAPTEXT = re.compile(r"width = declared span, not an instruction access|extent-declared gap", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    a = ap.parse_args()

    raw = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off, secs = pe + 24 + opt, []
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((nm, ib + va, vs, rs, pr))
        off += 40

    def fo(x):
        for nm, va, vs, rs, pr in secs:
            if va <= x < va + vs and (x - va) < rs:
                return pr + (x - va)

    fsizes, _ = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    tp = list(csv.reader(io.open(os.path.join(a.db, "_types", "types.tsv"),
                                 encoding="utf-8", newline=""), delimiter="\t"))
    tci = {k: i for i, k in enumerate(tp[0])}
    parent = {}
    for f in tp[1:]:
        if f and f[0] and len(f) > tci.get("route", 99):
            m = re.match(r"EMBED\s+(\S+)\s+\+0x([0-9A-Fa-f]+)", f[tci["route"]].strip())
            if m:
                parent[f[0]] = (m.group(1), int(m.group(2), 16))

    def chain(t, d=0):
        if d > 6 or t not in parent:
            return 0
        p, o = parent[t]
        return o + chain(p, d + 1)

    rows = []
    with io.open(os.path.join(a.db, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) >= 9 and f[0] and not SPAN.match(f[3]) \
                    and (f[6] in ("DISCOVERED", "") or f[7] == "UNKNOWN"):
                rows.append(f)

    bucket = collections.Counter()
    detail = collections.defaultdict(list)
    for f in rows:
        offv = int(f[1], 16)
        alt = offv + chain(f[0])
        ev = f[8]
        if ABSENCE.search(ev):
            b = "MEASURED ABSENCE"
        elif GAPTEXT.search(ev):
            b = "DECLARED GAP"
        else:
            sites = [int(m.group(1), 16) for m in ADDR.finditer(ev)]
            kinds = set()
            for s in dict.fromkeys(sites)[:8] if False else list(dict.fromkeys(sites))[:8]:
                p = fo(s)
                if p is None:
                    continue
                if s in fsizes:
                    kinds.add("fn")
                i = next(md.disasm(raw[p:p + 16], s), None)
                if i is None:
                    continue
                touches = any(op.type == X86_OP_MEM and op.mem.base
                              and op.mem.base != X86_REG_RIP and op.mem.disp in (offv, alt)
                              for op in i.operands)
                if touches:
                    kinds.add("lea" if i.mnemonic == "lea" else "access")
            if "access" in kinds:
                b = "READABLE"
            elif "lea" in kinds:
                b = "ADDRESS TAKEN ONLY"
            elif "fn" in kinds:
                b = "MECHANISM ONLY"
            elif not sites:
                b = "NO CITATION"
            else:
                b = "OTHER EVIDENCE KIND"
        bucket[b] += 1
        detail[b].append(f)

    print("weak named field rows: %d" % len(rows))
    print()
    order = ["READABLE", "ADDRESS TAKEN ONLY", "MECHANISM ONLY", "OTHER EVIDENCE KIND",
             "MEASURED ABSENCE", "DECLARED GAP", "NO CITATION"]
    for b in order:
        if bucket[b]:
            print("  %-22s %4d" % (b, bucket[b]))
    print()
    print("OUTSTANDING OPUS WORK ON THIS FRONTIER = the READABLE bucket: %d row(s)"
          % bucket["READABLE"])
    print("Everything else is either a measured result (absence, declared gap) or needs a")
    print("DIFFERENT instrument (the callee for an escaped address, ownership for a mechanism).")
    print()
    for b in order:
        if not bucket[b] or b in ("MEASURED ABSENCE", "DECLARED GAP"):
            continue
        print("%s:" % b)
        for f in detail[b][:12]:
            print("   %-34s +0x%-6s sz=%-4s %s" % (f[0][:34], f[1], f[2], f[3][:26]))
        if len(detail[b]) > 12:
            print("   ... %d more" % (len(detail[b]) - 12))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
