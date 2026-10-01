#!/usr/bin/env python3
"""opkind_vs_iced.py - whole-image control for reg_tracking.op_kind against a second decoder.

OPUS, 2026-09-24. The field-access index labels each memory operand r / w / rw / addr through
reg_tracking.op_kind, which trusts capstone's per-operand access flags. Those flags are wrong for
some encodings (capstone 5.0.7: `movups [m], xmm` is flagged READ; `test byte ptr [m], sil` has
no flag at all and falls to the positional rule, which calls it a WRITE).

This script decodes EVERY listed function body once with capstone and once with iced-x86, whose
InstructionInfoFactory states the access of each explicit operand from Intel's semantics, and
tabulates every (mnemonic, operand-index) where the two disagree. It is a MEASUREMENT, not a
dependency: iced is loaded from a path given on the command line, the kit never imports it.

    python opkind_vs_iced.py --iced <dir holding iced_x86> [--out disagreements.tsv]

Disagreement is reported per mnemonic with one example site; the verdict of which decoder is
right is the reader's, checked against the SDM for each mnemonic that appears.
"""
import argparse
import collections
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iced", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--kind", default="reg_tracking",
                    help="module providing op_kind (default: the kit's reg_tracking)")
    a = ap.parse_args()
    sys.path.insert(0, a.iced)
    import iced_x86 as I  # noqa: E402
    from capstone.x86 import X86_OP_MEM  # noqa: E402
    import check_default_instance_writers as W  # noqa: E402
    RT = __import__(a.kind)

    A = I.OpAccess
    amap = {A.READ: "r", A.COND_READ: "r", A.WRITE: "w", A.COND_WRITE: "w",
            A.READ_WRITE: "rw", A.READ_COND_WRITE: "rw", A.NO_MEM_ACCESS: "addr",
            A.NONE: "addr"}   # nop: no architectural access, which op_kind calls addr
    img = W.Image()
    fac = I.InstructionInfoFactory()
    stats = collections.Counter()
    dis = collections.Counter()
    ex = {}
    n_mem = 0
    for entry in sorted(img.sizes):
        size = img.sizes[entry]
        if not 0 < size <= 0x20000:
            continue
        blob = img.read(entry, size)
        if not blob:
            continue
        dec = I.Decoder(64, blob, ip=entry)
        iced_at = {}
        for ins in dec:
            iced_at[ins.ip] = ins
        for i in img.md.disasm(blob, entry):
            ops = list(i.operands)
            for oi, o in enumerate(ops):
                if o.type != X86_OP_MEM:
                    continue
                n_mem += 1
                cs = RT.op_kind(i, o, oi)
                ii = iced_at.get(i.address)
                if ii is None or ii.len != i.size:
                    stats["iced-desync"] += 1
                    continue
                info = fac.info(ii)
                if oi >= ii.op_count:
                    stats["iced-fewer-operands"] += 1
                    continue
                if ii.op_kind(oi) not in (I.OpKind.MEMORY, I.OpKind.MEMORY_ESRDI,
                                          I.OpKind.MEMORY_ESEDI, I.OpKind.MEMORY_SEG_RSI,
                                          I.OpKind.MEMORY_SEG_ESI, I.OpKind.MEMORY_SEG_RDI,
                                          I.OpKind.MEMORY_SEG_DI, I.OpKind.MEMORY_SEG_EDI):
                    stats["iced-operand-not-memory"] += 1
                    continue
                ic = amap.get(info.op_access(oi), "?")
                if i.mnemonic == "lea":
                    ic = "addr"
                if cs == ic:
                    stats["agree"] += 1
                    continue
                stats["disagree"] += 1
                key = (i.mnemonic, oi, cs, ic)
                dis[key] += 1
                if key not in ex:
                    ex[key] = "%08X %s %s" % (i.address, i.mnemonic, i.op_str)
    print("memory operands %d" % n_mem)
    for k, v in sorted(stats.items()):
        print("  %-26s %d" % (k, v))
    print("\ndisagreements  (mnemonic, operand, op_kind, iced)  count  example")
    for k, v in sorted(dis.items(), key=lambda kv: -kv[1]):
        print("  %-12s op%d  %-4s -> %-4s  %6d  %s" % (k[0], k[1], k[2], k[3], v, ex[k]))
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as f:
            f.write("mnemonic\toperand\top_kind\ticed\tcount\texample\n")
            for k, v in sorted(dis.items(), key=lambda kv: -kv[1]):
                f.write("%s\t%d\t%s\t%s\t%d\t%s\n" % (k[0], k[1], k[2], k[3], v, ex[k]))


if __name__ == "__main__":
    main()
