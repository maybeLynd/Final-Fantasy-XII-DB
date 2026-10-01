#!/usr/bin/env python3
"""uc1_citation_worklist.py - pass 1 of the UC-1 citation-debt worklist (OPUS, 2026-09-25).

SWE2-AUDIT-SPEC's ruling on OPUS-REQ-AUDITSPEC-UNLISTED-CITATION-COST: addresses that pages cite
as functions but that are ABSENT from functions.tsv are a document-integrity debt, because a
containing-function lookup across a missing entry mis-resolves (0016EEC0's behaviour was published
under 0016EFF0 that way). Two passes: (1) provenance classification, (2) mis-attribution check
against the cited body. This is pass 1, read-only.

A cited address qualifies when it is a backticked 8-hex-digit token in a page, lies in .text, is
not a listed entry, is 16-byte aligned, and lies past the previous listed body's end (not interior
to a listed body - those are extent questions, FUNCTION-EXTENT-ERRATA's domain). Pages under
99-Unresolved-Residual/, _index/ and _experiments/evidence/ are excluded: they are the unlisted
population's own pages, not independent citations.

Provenance (pass 1), from the image alone:
  CALLED     a rel32 call/jmp in a listed body targets it
  LEA        a rip-relative lea takes its address
  STORED     an aligned qword anywhere in the image data equals it
  DOC-ONLY   none of the above - the page is the only source of the address

    uc1_citation_worklist.py [--out worklist.tsv]
"""
import argparse
import bisect
import collections
import io
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_default_instance_writers as W  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP  # noqa: E402

TOK = re.compile(r"`(00[0-9A-F]{6})`")
EXCLUDE = ("99-Unresolved-Residual", "_index", "_experiments" + os.sep + "evidence", "_types")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 "..", "..", "..", "FFXII TZA"))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    img = W.Image()
    # CORRECTED 2026-09-25 (OPUS): "listed" means listed in functions.tsv, FUNCLETS INCLUDED.
    # W.Image() loads the 34,270 non-funclet bodies only - the right population for code censuses,
    # the wrong one for "is this address listed". Pass 1 as first published tested against it and
    # reported 22 listed Unwind@/Catch_All@ funclets as unlisted citations.
    import check_absence_claims as G
    listed = dict(img.sizes)
    for line in io.open(G.FUNCS, encoding="utf-8", errors="replace"):
        c = line.split("\t")
        try:
            listed.setdefault(int(c[0], 16), int(c[2]))
        except (ValueError, IndexError):
            pass
    names = {}
    for line in io.open(G.FUNCS, encoding="utf-8", errors="replace"):
        c = line.split("\t")
        if len(c) > 1:
            names[c[0].upper()] = c[1]
    ents = sorted(listed)
    text = [(img.base + s[1], img.base + s[1] + s[2]) for s in img.secs if s[0] == ".text"][0]

    def qualifies(v):
        if not (text[0] <= v < text[1]) or v in listed or v % 16:
            return False
        k = bisect.bisect_right(ents, v) - 1
        return k < 0 or v >= ents[k] + listed[ents[k]]

    cites = collections.defaultdict(list)
    db = os.path.abspath(a.db)
    for root, _d, files in os.walk(db):
        rel = os.path.relpath(root, db)
        if rel.split(os.sep)[0] in ("99-Unresolved-Residual", "_index", "_types") or \
                rel.startswith(os.path.join("_experiments", "evidence")):
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            for n, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
                for m in TOK.finditer(line):
                    v = int(m.group(1), 16)
                    if qualifies(v):
                        cites[v].append((os.path.relpath(p, db).replace(os.sep, "/"), n))
    targets = set(cites)
    called, lea = collections.Counter(), collections.Counter()
    for e in ents:
        n = listed[e]
        if not 0 < n <= 0x20000:
            continue
        b = img.read(e, n)
        if not b:
            continue
        for i in img.md.disasm(b, e):
            if i.mnemonic in ("call", "jmp") or i.mnemonic.startswith("j"):
                if i.operands and i.operands[0].type == X86_OP_IMM and i.operands[0].imm in targets \
                        and not (e <= i.operands[0].imm < e + n):
                    called[i.operands[0].imm] += 1
            elif i.mnemonic == "lea" and len(i.operands) == 2 and i.operands[1].type == X86_OP_MEM \
                    and i.operands[1].mem.base == X86_REG_RIP:
                t = i.address + i.size + i.operands[1].mem.disp
                if t in targets:
                    lea[t] += 1
    stored = collections.Counter()
    blob = img.blob
    for nm, sva, vs, ra, rs in img.secs:
        if nm in (".text", ".pdata", ".reloc", ".rsrc"):
            continue
        seg = blob[ra:ra + rs]
        for off in range(0, len(seg) - 7, 8):
            v = struct.unpack_from("<Q", seg, off)[0]
            if v in targets:
                stored[v] += 1
    rows = []
    for v in sorted(targets):
        cls = ("CALLED" if called[v] else "LEA" if lea[v] else "STORED" if stored[v] else "DOC-ONLY")
        k = bisect.bisect_right(ents, v) - 1
        prev = ents[k] if k >= 0 else None
        rows.append((v, cls, called[v], lea[v], stored[v], prev,
                     names.get("%08X" % prev, img.names.get(prev, "")) if prev else "", len(cites[v]),
                     "; ".join("%s:%d" % c for c in cites[v][:4])))
    c = collections.Counter(r[1] for r in rows)
    print("qualifying cited addresses: %d  %s" % (len(rows), dict(c)))
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("address\tprovenance\tcalled\tlea\tstored\tprev_listed\tprev_name\tcitations\tfirst_citations\n")
            for r in rows:
                f.write("%08X\t%s\t%d\t%d\t%d\t%s\t%s\t%d\t%s\n" % (
                    r[0], r[1], r[2], r[3], r[4], "%08X" % r[5] if r[5] else "", r[6], r[7], r[8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
