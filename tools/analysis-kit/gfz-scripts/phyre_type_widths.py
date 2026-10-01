#!/usr/bin/env python3
"""phyre_type_widths.py - the width of every Phyre reflection type, from its own descriptor.

WHY A SWEEP AND NOT THREE MORE BY HAND. 269 field rows in the type store declared `size = 0`,
invisible to the sum invariant because zero contributes nothing to it. Three ctypes were resolved
one at a time - `VVector3` and `VVector4` at 0x10, `VPString` at 8 - and each took a different
shape of search. 201 rows remain across many ctypes, so the method is worth writing down.

THE METHOD, and it is the same one that produced the 177 class extents. Every reflection type has
a class descriptor, and the descriptor's constructor is told the instance size:

    <registrar>   mov r9d, <SIZE>            argument 4 -> descriptor +0x38
                  mov dword [rsp+0x20], <A>  argument 5 -> descriptor +0x3C, the alignment
                  lea r8, [rip -> <name>]    argument 3 -> the name, which CHECKS the match
                  lea rcx, [rip -> <descr>]  argument 1 -> the descriptor
                  call 00632D80 / 00632C90

`phyre-field-schema.tsv` already records, per member, the `type_obj` its type resolves to - so the
descriptor address is known and does not have to be guessed.

TWO SHAPES, AND MISSING THE SECOND IS WHY `VPString` LOOKED UNRESOLVABLE. For most types the
`lea` of the descriptor and the `call` to the constructor sit in ONE body. For `PString` they do
not: `00166C90` leas `02E4D630` and calls `006A7190`, and the constructor call is inside THAT.
So the scan follows one level: if a body leas the descriptor and calls a non-constructor, the
callee is searched too, with the descriptor still considered to be in rcx.

AND A THIRD SOURCE, FOR THE SCALARS. The `PType` objects at `01F2Exxx` are INITIALISED data, so
their size is simply readable at `+0x38` with no code involved. That path is the control: it
yields `unsigned int` -> `PUInt32` size 4 and `float` -> `float` size 4, both known-correct, and
any run where those two disagree is a broken run.

WHAT IT DOES NOT DO. It does not write to the store. A width still has to be room-checked against
the next registered member before it is applied - of 23 candidates filled by the naive
"ctype names a type, use that type's size" rule, THIRTEEN were refuted by the next field's
offset, because a Phyre ctype frequently names the POINTED-TO type rather than an inline value.

    python phyre_type_widths.py
"""
import argparse
import collections
import csv
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP

import member_reach_scan as M
import kit_paths as KP

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE
CTOR = (0x00632D80, 0x00632C90)
SCHEMA = os.path.join("22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                      "phyre-field-schema.tsv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--out")
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

    def rdd(x):
        f = fo(x)
        return struct.unpack_from("<I", raw, f)[0] if f is not None else None

    def rds(x):
        f = fo(x)
        if f is None:
            return None
        e = raw.find(b"\x00", f, f + 120)
        s = raw[f:e]
        return s.decode("latin1") if s and all(32 <= c < 127 for c in s) else None

    # type -> descriptor, straight out of the recovered schema
    want = {}
    rows = list(csv.reader(io.open(os.path.join(a.db, SCHEMA), encoding="utf-8", newline=""),
                           delimiter="\t"))
    ci = {k: i for i, k in enumerate(rows[0])}
    cnt = collections.Counter()
    for r in rows[1:]:
        to = r[ci["type_obj"]].strip()
        if not to:
            continue
        try:
            want.setdefault(r[ci["type"]], int(to, 16))
        except ValueError:
            pass
        cnt[r[ci["type"]]] += 1
    desc2ty = {v: k for k, v in want.items()}
    print("reflection types with a descriptor address: %d" % len(want))

    # SOURCE 1 - the descriptor is initialised data, so +0x38 is simply readable
    out = {}
    for ty, d in want.items():
        s = rdd(d + 0x38)
        if s is not None and 0 < s <= 0x10000:
            out[ty] = (s, rdd(d + 0x3C), "initialised data at %08X+0x38" % d, rds(
                struct.unpack_from("<Q", raw, fo(d + 0x30))[0]) if fo(d + 0x30) else None)
    print("  resolved from initialised descriptors: %d" % len(out))

    # SOURCE 2 - follow the registrar, one level deep
    import gen_ptr_census as G
    braw, tva, tvs, tpr = G.load_text()
    blob = braw[tpr:tpr + tvs]
    fsizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    def il(fn):
        o = fn - tva
        return (list(md.disasm(blob[o:o + fsizes[fn]], fn))
                if fn in fsizes and 0 <= o < len(blob) else [])

    def scan(fn, seeded=None):
        """Return (descriptor, size, align, namestr) for each ctor call reached from this body."""
        found = []
        rooted = dict(seeded or {})
        r9 = a5 = r8 = None
        for i in il(fn):
            ops, mn = i.operands, i.mnemonic
            if mn == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM \
                    and ops[1].mem.base == X86_REG_RIP:
                t = i.address + i.size + ops[1].mem.disp
                d = i.reg_name(ops[0].reg)
                if t in desc2ty:
                    rooted[d] = t
                elif d == "r8":
                    r8 = t
                else:
                    rooted.pop(d, None)
                continue
            if mn == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_IMM:
                if i.reg_name(ops[0].reg) in ("r9d", "r9"):
                    r9 = ops[1].imm
                continue
            if mn == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM \
                    and ops[0].mem.base and i.reg_name(ops[0].mem.base) == "rsp" \
                    and ops[0].mem.disp == 0x20 and ops[1].type == X86_OP_IMM:
                a5 = ops[1].imm
                continue
            if mn == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_REG:
                s, d = i.reg_name(ops[1].reg), i.reg_name(ops[0].reg)
                if s in rooted:
                    rooted[d] = rooted[s]
                else:
                    rooted.pop(d, None)
                continue
            if i.group(2) and ops and ops[0].type == X86_OP_IMM:
                tgt = ops[0].imm
                if tgt in CTOR and "rcx" in rooted:
                    found.append((rooted["rcx"], r9, a5, rds(r8) if r8 else None))
                    r9 = a5 = None
                elif "rcx" in rooted and tgt in fsizes and tgt not in CTOR:
                    # THE SECOND SHAPE: the lea is here, the ctor call is in the callee.
                    for x in scan(tgt, {"rcx": rooted["rcx"]}):
                        found.append(x)
                rooted = {k: v for k, v in rooted.items()
                          if k not in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")}
        return found

    seen = set()
    for fn in sorted(fsizes):
        for d, s, al, nm in scan(fn):
            ty = desc2ty.get(d)
            if ty and s and ty not in out:
                out[ty] = (s, al, "registrar %08X" % fn, nm)
            seen.add(d)
    print("  resolved via registrars: %d" % (len(out) - sum(1 for v in out.values()
                                                            if v[2].startswith("initialised"))))

    ctrl = {"unsigned int": 4, "float": 4}
    bad = [k for k, v in ctrl.items() if k in out and out[k][0] != v]
    print()
    print("CONTROL - known scalars: %s"
          % (", ".join("%s=%s" % (k, out[k][0] if k in out else "MISSING") for k in ctrl)))
    print("  %s" % ("OK" if not bad and all(k in out for k in ctrl)
                    else "FAILED - believe nothing below"))
    print()
    print("%-52s %-7s %-6s %s" % ("reflection type", "size", "align", "source / name"))
    for ty in sorted(out, key=lambda t: -cnt[t]):
        s, al, src, nm = out[ty]
        print("%-52s 0x%-5X %-6s %s%s" % (ty[:52], s, al, src, (" name=%r" % nm) if nm else ""))
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write("type\tsize\talign\tsource\tname\tmember_rows\n")
            for ty, (s, al, src, nm) in sorted(out.items()):
                fh.write("%s\t0x%X\t%s\t%s\t%s\t%d\n" % (ty, s, al, src, nm or "", cnt[ty]))
        print("\nwrote %s" % a.out)
    print()
    print("NOTHING WAS WRITTEN TO THE STORE. Room-check each width against the next registered")
    print("member before applying: a Phyre ctype often names the POINTED-TO type, not an inline")
    print("value, and 13 of 23 such candidates were refuted that way.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
