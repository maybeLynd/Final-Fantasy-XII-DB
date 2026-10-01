#!/usr/bin/env python3
"""check_imagebase_relative_refs.py - the address that is never written down but is used anyway.

WHY THIS EXISTS. The combat step table at 0x01EFA5C0 was declared unreachable by indexed dispatch
on the strength of two true observations: there is no `lea` to 0x01EFA5C0 anywhere in the image,
and the literal never appears as a 4- or 8-byte constant. Both hold. The conclusion did not:

    003859E2  lea  r12, [rip - 0x2659e9]            ; r12 = 00120000, the IMAGE BASE
    003859FF  call qword ptr [r12 + rax*8 + 0x1dda5c0]

0x00120000 + 0x01DDA5C0 = 0x01EFA5C0. The table's address is never FORMED - the image base sits
in a register and the *file-relative* offset rides in the instruction's displacement. A sweep for
the address as a constant cannot see this, and on this binary it is an ordinary idiom rather than
a curiosity.

SO ANY CLAIM OF THE SHAPE "X never appears as a constant, therefore nothing computes it" is
unsound here, and this measures how much room that leaves. For every based-or-indexed memory
operand whose displacement, ADDED TO THE IMAGE BASE, lands inside a data section, it reports the
resulting address - the reference a constant-sweep is blind to.

    python check_imagebase_relative_refs.py                 # how common is the idiom
    python check_imagebase_relative_refs.py --target 0x01EFA5C0   # who computes this address
"""
import argparse
import collections
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

import member_reach_scan as M
import kit_paths as KP  # noqa: E402

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", help="a VA; report every site that computes it this way")
    ap.add_argument("--min-disp", type=lambda x: int(x, 0), default=0x10000,
                    help="ignore small displacements, which are struct offsets not file offsets")
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
        if nm == ".text":
            TVA, TVS, TPR = ib + va, vs, pr
        off += 40
    blob = raw[TPR:TPR + TVS]
    fsizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    def sect(x):
        for nm, va, vs, rs, pr in secs:
            if va <= x < va + vs:
                return nm
        return None

    target = int(a.target, 0) if a.target else None
    hits, bysect, bymn = [], collections.Counter(), collections.Counter()
    for fn in sorted(fsizes):
        o = fn - TVA
        if not (0 <= o < len(blob)):
            continue
        for i in md.disasm(blob[o:o + fsizes[fn]], fn):
            for op in i.operands:
                if op.type != X86_OP_MEM or op.mem.base == X86_REG_RIP:
                    continue
                if not op.mem.base and not op.mem.index:
                    continue
                d = op.mem.disp
                if d < a.min_disp:
                    continue
                va = ib + d
                s = sect(va)
                if s is None or s == ".text":
                    continue
                if target is not None and va != target:
                    continue
                hits.append((fn, i.address, "%s %s" % (i.mnemonic, i.op_str), va, s))
                bysect[s] += 1
                bymn[i.mnemonic] += 1

    print("image base %08X; a displacement >= 0x%X added to it that lands in a DATA section is"
          % (ib, a.min_disp))
    print("an image-base-relative reference - invisible to any sweep for the address as a value.")
    print()
    if target is not None:
        print("sites computing %08X this way: %d" % (target, len(hits)))
        for fn, at, t, va, s in hits:
            print("   %08X %-34s %08X  %s" % (fn, names.get(fn, "")[:34], at, t[:60]))
        if not hits:
            print("   none")
        return 0
    print("total such operands: %d" % len(hits))
    print("   by section : %s" % dict(bysect.most_common()))
    print("   by mnemonic: %s" % dict(bymn.most_common(8)))
    print()
    tgt = collections.Counter(h[3] for h in hits)
    print("distinct addresses reached this way: %d" % len(tgt))
    print("the most-referenced, with the function that reaches them:")
    for va, n in tgt.most_common(12):
        f = next(h for h in hits if h[3] == va)
        print("   %08X  %-3d site(s)  %-9s e.g. %08X %s"
              % (va, n, sect(va), f[1], names.get(f[0], "")[:30]))
    print()
    print("EVERY ONE of these is an address some page could truthfully say 'never appears as a")
    print("constant' about. That sentence does not mean nothing reaches it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
