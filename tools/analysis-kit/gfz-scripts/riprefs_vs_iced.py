#!/usr/bin/env python3
"""riprefs_vs_iced.py - control for work/h78/rip_data_refs.tsv (the global_refs source) against iced-x86.

OPUS, 2026-09-24. Each row names a site and a rip-relative target with kind read/write/addr/other.
The file has no read-modify-write class. This re-decodes every site with iced, finds the operand
whose effective address is the row's target, and tabulates (instruction class, file kind, iced
access). Measurement only.
    python riprefs_vs_iced.py --iced <dir> [--out rows.tsv]
"""
import argparse, collections, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iced", required=True)
    ap.add_argument("--refs", default=os.path.join(HERE, "..", "..", "work", "h78", "rip_data_refs.tsv"))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    sys.path.insert(0, a.iced)
    import iced_x86 as I
    import check_default_instance_writers as W
    A = I.OpAccess
    amap = {A.READ: "read", A.COND_READ: "read", A.WRITE: "write", A.COND_WRITE: "write",
            A.READ_WRITE: "rw", A.READ_COND_WRITE: "rw", A.NO_MEM_ACCESS: "addr", A.NONE: "addr"}
    img = W.Image()
    fac = I.InstructionInfoFactory()
    fmt = I.Formatter(I.FormatterSyntax.INTEL)
    c = collections.Counter(); ex = {}; bad = []
    n = 0
    for ln in io.open(a.refs, encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        if len(p) < 4 or p[0] == "function_entry":
            continue
        n += 1
        site, tgt, kind = int(p[3], 16), int(p[1], 16), p[2]
        b = img.read(site, 16)
        ins = I.Decoder(64, b, ip=site).decode()
        info = fac.info(ins)
        got = None
        for oi in range(ins.op_count):
            if ins.op_kind(oi) == I.OpKind.MEMORY and ins.is_ip_rel_memory_operand \
                    and ins.ip_rel_memory_address == tgt:
                got = amap.get(info.op_access(oi), "?")
                break
        if ins.mnemonic == I.Mnemonic.LEA:
            got = "addr"
        if got is None:
            got = "no-rip-operand"
        mn = fmt.format_mnemonic(ins)
        key = (kind, got)
        c[key] += 1
        if kind != got:
            k2 = (mn, kind, got)
            c[k2] += 1
            ex.setdefault(k2, "%08X %s" % (site, fmt.format(ins)))
            bad.append((p[0], p[1], kind, got, p[3], fmt.format(ins)))
    print("rows %d" % n)
    print("file-kind -> iced:")
    for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
        if len(k) == 2:
            print("  %-6s -> %-14s %7d" % (k[0], k[1], v))
    print("disagreements by mnemonic:")
    for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
        if len(k) == 3:
            print("  %-12s %-6s -> %-14s %6d  %s" % (k[0], k[1], k[2], v, ex[k]))
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as f:
            f.write("function_entry\treferenced_address\tkind_file\tkind_iced\tsite\tinstruction\n")
            for r in bad:
                f.write("\t".join(r) + "\n")


if __name__ == "__main__":
    main()
