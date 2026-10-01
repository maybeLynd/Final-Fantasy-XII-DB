#!/usr/bin/env python3
"""regwrites_vs_iced.py - receiver-overwrite control: reg_tracking.written() against iced-x86.

OPUS, 2026-09-24. A route-seeded census keeps an object in a register until the register is
written; a missed write means accesses through a DIFFERENT object are credited to the tracked
type (receiver overwrite), and a spurious write drops real accesses. This compares, for every
instruction in every listed body, the 64-bit GPRs written per reg_tracking.written() with the
GPRs iced-x86 reports as written (WRITE / COND_WRITE / READ_WRITE / READ_COND_WRITE, sub-registers
folded to their parent). Measurement only; iced is loaded from --iced.

    python regwrites_vs_iced.py --iced <dir holding iced_x86>
"""
import argparse, collections, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

GPR = {"rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"} | {"r%d" % n for n in range(8, 16)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iced", required=True)
    a = ap.parse_args()
    sys.path.insert(0, a.iced)
    import iced_x86 as I
    import check_default_instance_writers as W
    import reg_tracking as RT
    A = I.OpAccess
    WR = {A.WRITE, A.COND_WRITE, A.READ_WRITE, A.READ_COND_WRITE}
    names = {v: k.lower() for k, v in vars(I.Register).items() if isinstance(v, int)}
    # iced names the REX byte registers r8l..r15l; the kit (capstone) calls them r8b..r15b
    names = {v: (k[:-1] + "b" if k.startswith("r") and k.endswith("l") and k[1:-1].isdigit() else k)
             for v, k in names.items()}
    img = W.Image()
    fac = I.InstructionInfoFactory()
    n = 0
    dis = collections.Counter()
    ex = {}
    for entry in sorted(img.sizes):
        size = img.sizes[entry]
        if not 0 < size <= 0x20000:
            continue
        blob = img.read(entry, size)
        if not blob:
            continue
        at = {x.ip: x for x in I.Decoder(64, blob, ip=entry)}
        for i in img.md.disasm(blob, entry):
            ii = at.get(i.address)
            if ii is None or ii.len != i.size:
                continue
            n += 1
            cs = RT.written(i) & GPR
            ic = set()
            for u in fac.info(ii).used_registers():
                if u.access in WR:
                    ic.add(RT.canon(names.get(u.register, "?")))
            ic &= GPR
            if cs != ic:
                key = (i.mnemonic, tuple(sorted(cs - ic)), tuple(sorted(ic - cs)))
                dis[key] += 1
                ex.setdefault(key, "%08X %s %s" % (i.address, i.mnemonic, i.op_str))
    print("instructions %d  disagree %d" % (n, sum(dis.values())))
    print("(mnemonic, only-capstone-kills, only-iced-kills) count example")
    for k, v in sorted(dis.items(), key=lambda kv: -kv[1])[:60]:
        print("  %-14s cs-only=%-18s iced-only=%-18s %7d  %s" % (k[0], ",".join(k[1]), ",".join(k[2]), v, ex[k]))


if __name__ == "__main__":
    main()
