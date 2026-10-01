#!/usr/bin/env python3
"""gen_static_tree_census.py - a census for a STATIC object reached through a root address.

THE GAP THIS FILLS WAS MEASURED, NOT ASSUMED. `RenderModelInstanceContainer` is
`STATIC 0x022C7020`, and **neither that address nor its cached pointer has a single rip-relative
reference in any listed body**. Every other generator here is therefore blind to it:

  * `gen_static_census.py` resolves RIP-relative operands - there are none;
  * `gen_ptr_census.py` seeds on `mov reg, [rip -> slot]` - nothing loads the cache;
  * `gen_array_census.py` seeds on a `lea` of the object's OWN address - nothing `lea`s it either.

The code does this instead:

    lea rsi, [rip -> 022C6F30]        rsi = the render resource ROOT
    lea rax, [rsi + 0xF0]             rax = the container, 0x022C7020
    ...  [rax + disp]                 an access at container-relative `disp`

so the object is never named by an instruction. It is **computed** from a different address. A scan
that only recognises addresses it can read out of an operand cannot see a single access.

WHAT THIS TRACKS. Registers whose ABSOLUTE VALUE is known:

    lea rX, [rip -> A]     rX = A
    lea rY, [rX + d]       rY = A + d          (the whole point)
    add rX, imm            rX = A + imm
    mov rY, rX             rY = A
    anything else writing a tracked register drops it, and a call drops the volatiles.

An access `[rX + d]` where `rX = A` lands in the object when `base <= A + d < base + size`, at
displacement `A + d - base`. **No heuristic is involved**: every tracked value is an address the
image states literally, transformed by constants the instructions state literally.

LIMITS. Same-function only, so the count is a floor. A root passed as an argument is invisible, which
is the same boundary every other generator here has. Nothing is inferred about types; the
instruction is recorded and the judgement is somebody else's.

    python gen_static_tree_census.py --type RenderModelInstanceContainer
"""
import argparse
import collections
import csv
import io
import os
import re
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_GRP_CALL
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP

import member_reach_scan as M
import kit_paths as KP
import reg_tracking as RT  # noqa: E402  (access direction: op_kind)

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE
VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
R_STATIC = re.compile(r"^STATIC\s+(0x[0-9A-Fa-f]+)")


def load_text():
    raw = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    base = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off = pe + 24 + opt
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        if nm == ".text":
            return raw, base + va, vs, pr
        off += 40
    raise SystemExit("no .text")


def route_for(tname):
    p = os.path.join(KP.DB, "_types", "types.tsv")
    with io.open(p, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if f and f[0] == tname and len(f) > 12:
                try:
                    size = int(f[1], 0)
                except ValueError:
                    size = None
                for alt in f[12].split("|"):
                    m = R_STATIC.match(alt.strip())
                    if m:
                        return int(m.group(1), 0), size
    return None, None


def scan(base, size, blob, tva, sizes, names, md):
    rows = []
    for fn in sorted(sizes):
        body = blob[fn - tva:fn - tva + sizes[fn]]
        if not body:
            continue
        try:
            ins_list = list(md.disasm(body, fn))
        except Exception:
            continue
        val = {}                      # reg -> known absolute address
        for ins in ins_list:
            rn, ops, m = ins.reg_name, ins.operands, ins.mnemonic
            if m.startswith("nop") or m.startswith("prefetch"):
                continue

            # record accesses off a register whose absolute value is known
            for oi, op in enumerate(ops):
                if op.type != X86_OP_MEM or op.mem.base in (0, X86_REG_RIP) or op.mem.index:
                    continue
                bn = rn(op.mem.base)
                if bn not in val:
                    continue
                addr = val[bn] + op.mem.disp
                if base <= addr < base + size:
                    rows.append((fn, names.get(fn, ""), ins.address, addr - base,
                                 RT.op_kind(ins, op, oi),
                                 m + " " + ins.op_str))

            # lea rX, [rip -> A]   seeds an absolute value
            if m == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM:
                mem = ops[1].mem
                dst = rn(ops[0].reg)
                if mem.base == X86_REG_RIP and mem.index == 0:
                    val[dst] = ins.address + ins.size + mem.disp
                    continue
                # lea rY, [rX + d]  carries it, which is the whole point
                if mem.base and mem.index == 0 and rn(mem.base) in val:
                    val[dst] = val[rn(mem.base)] + mem.disp
                    continue
                val.pop(dst, None)
                continue
            if m == "add" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_IMM and rn(ops[0].reg) in val:
                val[rn(ops[0].reg)] += ops[1].imm
                continue
            if m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_REG:
                s = rn(ops[1].reg)
                if s in val:
                    val[rn(ops[0].reg)] = val[s]
                else:
                    val.pop(rn(ops[0].reg), None)
                continue
            if ins.group(CS_GRP_CALL):
                for v in list(val):
                    if v in VOLATILE:
                        del val[v]
                continue
            if ops and ops[0].type == X86_OP_REG:
                val.pop(rn(ops[0].reg), None)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    base, size = route_for(a.type)
    if base is None or not size:
        print("no STATIC route with a size for %s" % a.type)
        return 2
    raw, tva, tvs, tpr = load_text()
    blob = raw[tpr:tpr + tvs]
    sizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    rows = scan(base, size, blob, tva, sizes, names, md)
    seen, out = set(), []
    for x in rows:
        k = (x[2], x[3])
        if k not in seen:
            seen.add(k)
            out.append(x)
    out.sort(key=lambda x: (x[3], x[2]))
    kinds = collections.Counter(x[4] for x in out)
    print("%s: STATIC %08X size 0x%X" % (a.type, base, size))
    print("  %d distinct access(es) at %d distinct offset(s)  (%s)"
          % (len(out), len({x[3] for x in out}),
             ", ".join("%s %d" % kv for kv in sorted(kinds.items()))))
    for fn, nm, site, d, kind, txt in out[:12]:
        print("    +0x%-5X %08X in %-8s %-4s %s" % (d, site, "%08X" % fn, kind, txt[:56]))
    if a.out and out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
            for fn, nm, site, d, kind, txt in out:
                fh.write("%08X\t%s\t%08X\t0x%X\t%s\t%s\tstatictree %08X\t\n"
                         % (fn, nm, site, d, kind, txt, base))
        print("  wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
