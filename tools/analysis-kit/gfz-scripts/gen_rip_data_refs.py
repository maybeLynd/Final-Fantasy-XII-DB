#!/usr/bin/env python3
"""gen_rip_data_refs.py - producer for work/h78/rip_data_refs.tsv (the global_refs source).

Schema: `function_entry<TAB>referenced_address<TAB>kind<TAB>site` — one row per RIP-relative
memory operand in every function listed in work/graph/functions.tsv, in file order.

WHY THIS PRODUCER EXISTS (SWE2-DATA, 2026-09-26, OPUS-REQ-DATA-GLOBAL-REFS-AND-FIELDS-
DIRECTION). The file's original generator is not recorded anywhere — a fact the request
itself names as missing information — and its direction column was measured wrong by
independent re-decode (riprefs_vs_iced.py, iced-x86 as second decoder, evidence in
_index/candidates/access-direction/): 4,040 stores labelled read (movups 4,013, movq 26,
setns 1), 19 `lock cmpxchg` labelled read, 1,100 read-modify-write sites labelled write,
68 `test` sites labelled other. This producer classifies each operand with
`reg_tracking.op_kind`, the kit's controlled classifier — SDM-grounded mnemonic tables
first (compares read, atomic exchanges read-modify-write, pure moves write operand 0,
lea/nop/prefetch touch nothing), capstone access flags after, `?` never a guess.

kind vocabulary: read | write | rw | addr | other. `rw` is new with this regeneration —
the old file had no read-modify-write class, which is exactly the 1,119-site defect.

    python gen_rip_data_refs.py [--out <path>] [--check]
    --check  compare the emitted rows against the existing file and report the relabel
             census by (old,new) pair and mnemonic; expected: exactly the sites in
             _index/candidates/access-direction/rip-data-refs-vs-iced.tsv.
"""
import argparse
import collections
import csv
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

import kit_paths as KP
import reg_tracking as RT

FUNCS = os.path.join(KP.WORK, "graph", "functions.tsv")
REFS = os.path.join(KP.WORK, "h78", "rip_data_refs.tsv")

_KIND = {"r": "read", "w": "write", "rw": "rw", "addr": "addr", "?": "other"}


def load_sections():
    raw = open(KP.EXE, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    secs = []
    for i in range(ns):
        o = pe + 24 + opt + i * 40
        secs.append((struct.unpack_from("<I", raw, o + 12)[0],      # virtual address
                     struct.unpack_from("<I", raw, o + 8)[0],       # virtual size
                     struct.unpack_from("<I", raw, o + 20)[0]))     # raw offset
    return raw, secs


def va_off(va, secs, base=0x120000):
    r = va - base
    for sva, svs, sro in secs:
        if sva <= r < sva + svs:
            return sro + (r - sva)
    return None


def load_funcs():
    out = []
    with io.open(FUNCS, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 3:
                continue
            try:
                out.append((int(f[0], 16), int(f[2])))
            except ValueError:
                continue
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=REFS)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    raw, secs = load_sections()
    funcs = load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    rows = []
    for entry, size in funcs:
        o = va_off(entry, secs)
        if o is None or size <= 0:
            continue
        for ins in md.disasm(raw[o:o + size], entry):
            for oi, op in enumerate(ins.operands):
                if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
                    continue
                t = ins.address + ins.size + op.mem.disp
                rows.append((entry, t, _KIND[RT.op_kind(ins, op, oi)], ins.address))

    kinds = collections.Counter(r[2] for r in rows)
    print("functions %d  rows %d   (%s)"
          % (len(funcs), len(rows), ", ".join("%s %d" % kv for kv in sorted(kinds.items()))))

    if a.check:
        old = {}
        if os.path.exists(REFS):
            with io.open(REFS, encoding="utf-8", errors="replace") as fh:
                fh.readline()
                for ln in fh:
                    p = ln.rstrip("\n").split("\t")
                    if len(p) >= 4:
                        old[(p[0].upper(), p[1].upper(), p[3].upper())] = p[2]
        same = rel = add = 0
        by_pair = collections.Counter()
        missing = set(old)
        for e, t, k, s in rows:
            key = ("%08X" % e, "%08X" % t, "%08X" % s)
            missing.discard(key)
            ok = old.get(key)
            if ok is None:
                add += 1
            elif ok == k:
                same += 1
            else:
                rel += 1
                by_pair[(ok, k)] += 1
        print("check vs existing: same %d  relabelled %d  added %d  dropped %d"
              % (same, rel, add, len(missing)))
        for (o2, n2), v in sorted(by_pair.items(), key=lambda kv: -kv[1]):
            print("  %-6s -> %-6s %6d" % (o2, n2, v))
        return 0

    with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
        fh.write("function_entry\treferenced_address\tkind\tsite\n")
        for e, t, k, s in rows:
            fh.write("%08X\t%08X\t%s\t%08X\n" % (e, t, k, s))
    print("wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
