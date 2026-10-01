#!/usr/bin/env python3
"""contract_state_dossier.py - everything needed to declare an undeclared contract-named address.

OPUS, 2026-09-25, companion to contract_named_state_census.py. For each UNDECLARED row of the census
TSV (optionally filtered by a contract substring), prints: every rip-relative access to the address
and the 16 bytes after it (width, direction by reg_tracking.op_kind, instruction, function), whether
the address lies in initialised .data or BSS and its image bytes, and the contract lines that name
it. Read-only; it declares nothing.

    contract_state_dossier.py [--contract SUBSTR] [--span 16]
"""
import argparse
import collections
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402
import check_default_instance_writers as W  # noqa: E402
import reg_tracking as RT  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_REG_RIP  # noqa: E402

CENSUS = "_index/candidates/contract-named-state-census.tsv"
RAW_END = 0x01F7E400                       # .data raw extent: below is file-backed, above is BSS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", default="")
    ap.add_argument("--span", type=int, default=16)
    a = ap.parse_args()
    rows = [r for r in csv.DictReader(io.open(os.path.join(G.DB, CENSUS), encoding="utf-8"), delimiter="\t")
            if r["class"] == "UNDECLARED" and a.contract in r["contract"]]
    want = {}
    for r in rows:
        want.setdefault(int(r["address"], 16), set()).add(r["contract"])
    img = W.Image()
    hits = collections.defaultdict(list)
    for e, n in img.sizes.items():
        if not 0 < n <= 0x20000:
            continue
        for i in img.md.disasm(img.read(e, n), e):
            for k, op in enumerate(i.operands):
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    t = i.address + i.size + op.mem.disp
                    for v in want:
                        if v <= t < v + a.span:
                            hits[v].append((t, op.size, RT.op_kind(i, op, k), i.address, e,
                                            "%s %s" % (i.mnemonic, i.op_str)))
    for v in sorted(want):
        where = "initialised .data" if v < RAW_END else "BSS"
        b = img.read(v, 16) if v < RAW_END else b""
        print("=" * 100)
        print("%08X  %s %s" % (v, where, ("bytes " + b.hex(" ")) if b else ""))
        for c in sorted(want[v]):
            print("  named by %s" % c)
            for ln in io.open(os.path.join(G.DB, c), encoding="utf-8", errors="replace"):
                if "%08X" % v in ln:
                    print("    | " + ln.strip()[:260])
                    break
        for t, sz, kd, ia, e, txt in sorted(hits[v])[:40]:
            print("  +%-3X w%-2d %-4s %08X in %08X %-22s %s" % (t - v, sz, kd, ia, e,
                                                          img.names.get(e, "")[:22], txt[:70]))
        if len(hits[v]) > 40:
            print("  ... %d more" % (len(hits[v]) - 40))
    return 0


if __name__ == "__main__":
    sys.exit(main())
