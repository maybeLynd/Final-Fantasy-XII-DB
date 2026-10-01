#!/usr/bin/env python3
"""check_taken_address_writes.py - the field write a displacement sweep cannot see.

WHY THIS EXISTS. `SpawnRecord +0x19` was swept four times by four instruction forms and came back
unwritten every time. It is written, by `BattleEnmity_UpdatePeriodicDecay`:

    00321553  mov   rax, qword ptr [rcx + 0x6A0]   ; the record, reached NOT by its own route
    00321569  lea   rdi, [rax + 0x19]              ; the address is TAKEN
    003215AC  mov   byte ptr [rdi], cl             ; ... and the write has displacement ZERO

**Every sweep keyed on the displacement `0x19` is blind to that store**, because by the time the
write happens the offset is gone - it was consumed by the `lea`. This measures how much room that
leaves: how many struct fields in this image are written through an address taken by a `lea` and
stored at displacement zero.

WHAT IT IS AND IS NOT. It is an intra-function def-use walk: find `lea reg, [base + disp]` with a
struct-sized displacement, then look forward in the same body for a store through that register at
displacement zero, stopping at any redefinition of it. That is deliberately conservative - it will
miss a taken address that crosses a call or is spilled - so **the number it reports is a FLOOR**.
It is not a claim that every hit is an undocumented field; it is the size of the blind spot.

The AL-8 site is the positive control. If the sweep does not find `003215AC`, its total means
nothing.
"""
import argparse
import collections
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import (X86_OP_MEM, X86_OP_REG, X86_REG_RIP, X86_REG_RBX,
                          X86_REG_RBP, X86_REG_RDI, X86_REG_RSI, X86_REG_R12,
                          X86_REG_R13, X86_REG_R14, X86_REG_R15)

# MS x64: these survive a call, so a call does NOT kill a taken address held in one.
# Getting this wrong made the first run miss its own control - the AL-8 address lives in
# RDI across `call 00307CE0`.
CALLEE_SAVED = {X86_REG_RBX, X86_REG_RBP, X86_REG_RDI, X86_REG_RSI,
                X86_REG_R12, X86_REG_R13, X86_REG_R14, X86_REG_R15}

import member_reach_scan as M
import kit_paths as KP  # noqa: E402

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE
CONTROL = 0x003215AC


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-disp", type=lambda x: int(x, 0), default=1)
    ap.add_argument("--max-disp", type=lambda x: int(x, 0), default=0x2000,
                    help="above this a displacement is more likely a table than a field")
    ap.add_argument("--window", type=int, default=40,
                    help="instructions to look ahead for the store")
    a = ap.parse_args()

    raw = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off = pe + 24 + opt
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        if nm == ".text":
            TVA, TVS, TPR = ib + va, vs, pr
        off += 40
    blob = raw[TPR:TPR + TVS]
    fsizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    hits, bydisp = [], collections.Counter()
    for fn in sorted(fsizes):
        o = fn - TVA
        if not (0 <= o < len(blob)):
            continue
        ins = list(md.disasm(blob[o:o + fsizes[fn]], fn))
        for n, i in enumerate(ins):
            if i.mnemonic != "lea" or len(i.operands) != 2:
                continue
            dst, src = i.operands
            if dst.type != X86_OP_REG or src.type != X86_OP_MEM:
                continue
            if src.mem.base in (0, X86_REG_RIP) or src.mem.index:
                continue
            d = src.mem.disp
            if not (a.min_disp <= d <= a.max_disp):
                continue
            reg = dst.reg
            guarded = False
            # walk forward for a store through reg at displacement zero
            for j in ins[n + 1:n + 1 + a.window]:
                w = j.operands[0] if j.operands else None
                # A CMOV into reg is the null-guard idiom (`cmove rdi, rsi` with rsi = 0): the
                # register still holds the taken address on the path that matters, so the chain
                # continues and the hit is marked guarded.
                if w is not None and w.type == X86_OP_REG and w.reg == reg \
                        and j.mnemonic.startswith("cmov"):
                    guarded = True
                    continue
                # any other redefinition kills the chain
                if w is not None and w.type == X86_OP_REG and w.reg == reg \
                        and j.mnemonic not in ("cmp", "test"):
                    break
                # a call kills a VOLATILE register only
                if j.mnemonic == "call" and reg not in CALLEE_SAVED:
                    break
                if w is not None and w.type == X86_OP_MEM and w.mem.base == reg \
                        and not w.mem.index and w.mem.disp == 0 \
                        and j.mnemonic.startswith("mov"):
                    hits.append((fn, i.address, d, j.address,
                                 "%s %s" % (j.mnemonic, j.op_str), guarded))
                    bydisp[d] += 1
                    break

    print("lea-taken field addresses written at displacement zero: %d sites" % len(hits))
    print("distinct displacements involved                       : %d" % len(bydisp))
    print("distinct functions                                    : %d"
          % len({h[0] for h in hits}))
    print()
    ctrl = [h for h in hits if h[3] == CONTROL]
    print("POSITIVE CONTROL - the AL-8 write at %08X: %s" % (CONTROL, "FOUND" if ctrl else
          "NOT FOUND -> this sweep is broken and its total means nothing"))
    if ctrl:
        fn, lea, d, st, txt, g = ctrl[0]
        print("   %s  lea at %08X disp +0x%X, store at %08X: %s"
              % (names.get(fn, "%08X" % fn), lea, d, st, txt))
    print()
    print("   of %d sites, %d pass through a CMOV null-guard like the control's"
          % (len(hits), sum(1 for h in hits if h[5])))
    print()
    print("the most common displacements taken this way:")
    for d, n in bydisp.most_common(15):
        print("   +0x%-5X %4d site(s)" % (d, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
