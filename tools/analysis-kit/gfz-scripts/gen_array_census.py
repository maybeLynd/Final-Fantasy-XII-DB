#!/usr/bin/env python3
"""gen_array_census.py - census for an `ARRAY` at a static address, reached through a register.

THE GAP THIS FILLS WAS DEMONSTRATED, NOT ASSUMED. `gen_static_census.py` censuses a record at a
fixed address by resolving RIP-relative operands. Run against `ActorManagerSlot`
(`ARRAY 0x02098E10 stride=0x288 count=5`) with the counts the store's own evidence records, it
**failed its control and refused to write**: `+0x00` wanted 11 and got 60, `+0x12` wanted 1 and got
0. That is not a bug in it - those counts were gathered from accesses through a BASE REGISTER, and
one `ActorManagerSlot` row says so outright (*"FOLDED-BASE ACCESS"*). A RIP-relative scan and a
register scan see different populations of the same table.

Six `.bss` `ARRAY` types have no census at all for exactly this reason. This is the register half:

    lea  rB, [rip -> ADDR]          rB = the array base
    imul rI, rC, <stride>           rI = i * stride, when the stride exceeds x86's scale limit
    lea  rE, [rB + rI]              rE = element i
    ...  [rE + disp]                an access at element-relative `disp`

and, because the two halves belong in one census, RIP-relative operands landing inside the table are
recorded too, as `rip` rather than `reg`.

ELEMENT vs OFFSET. `[rB + disp]` with a constant `disp` addresses element `disp // stride` at offset
`disp % stride`. That is only true when the base register really holds element 0, which is why the
base is seeded from a `lea` of the table address and dropped the moment anything else writes it.

    python gen_array_census.py --type ActorManagerSlot --control 0x0=11,0x12=1,0x14=2
    python gen_array_census.py --type SpawnGroupLedger --out <path>

FLOW-SENSITIVITY, added 2026-09-22 (FRONTIER, per OPUS-REQ-FRONTIER-SHARED-CENSUS-
WALKS-LINEARLY-NO-CFG). The per-function walk now runs a dataflow fixpoint over the
control-flow graph with a union join, instead of reading instructions in address
order: a base/element/index register killed on one arm no longer stays dead past the
merge, which made every negative the linear pass produced unsound. Instructions no
resolved edge reaches - jump-table arms - are still visited, seeded from the union of
indirect-jump exit states. Two adjacent defects fixed in the same pass: a write to a
register now clears its `mul` entry (stale multipliers survived before), and `call`
clears `mul` for the volatile registers alongside the tracked sets.
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
R_ARRAY = re.compile(r"^ARRAY\s+(0x[0-9A-Fa-f]+)(?:\s*\+\s*(0x[0-9A-Fa-f]+))?\s+"
                     r"stride=(0x[0-9A-Fa-f]+|\d+)\s+count=(\d+)")


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
                for alt in f[12].split("|"):
                    m = R_ARRAY.match(alt.strip())
                    if m:
                        return (int(m.group(1), 0) + (int(m.group(2), 0) if m.group(2) else 0),
                                int(m.group(3), 0), int(m.group(4)))
    return None


MULCAP = 8   # a register's candidate multipliers cap here; past it the key drops


def scan(base, stride, count, blob, tva, sizes, names, md):
    span = stride * count
    rows = []
    seen_rows = set()   # (fn, site, disp, kind) - the fixpoint revisits instructions

    def rec(fn, site, d, kind, txt, how):
        k = (fn, site, d, kind)
        if k in seen_rows:
            return
        seen_rows.add(k)
        rows.append((fn, names.get(fn, ""), site, d, kind, txt, how))

    def joinst(A, B):
        mul = dict(A[3])
        for k, v in B[3].items():
            u = (mul.get(k, frozenset()) | v)
            if len(u) <= MULCAP:
                mul[k] = u
            else:
                mul.pop(k, None)
        return (A[0] | B[0], A[1] | B[1], A[2] | B[2],
                {k: frozenset(v) for k, v in mul.items()})

    def xfer(ins, st, fn):
        bases, elems, idxs = set(st[0]), set(st[1]), set(st[2])
        mul = {k: set(v) for k, v in st[3].items()}
        rn, ops, m = ins.reg_name, ins.operands, ins.mnemonic
        if not (m.startswith("nop") or m.startswith("prefetch")):
            # RIP-relative operand landing inside the table -> record directly
            for oi, op in enumerate(ops):
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    t = ins.address + ins.size + op.mem.disp
                    if base <= t < base + span and m != "lea":
                        d = (t - base) % stride
                        rec(fn, ins.address, d,
                            RT.op_kind(ins, op, oi), m + " " + ins.op_str, "rip")

            done = False
            # seed: lea rB, [rip -> base]
            if m == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM \
                    and ops[1].mem.base == X86_REG_RIP:
                t = ins.address + ins.size + ops[1].mem.disp
                if t == base:
                    bases.add(rn(ops[0].reg)); done = True
                elif base < t < base + span and (t - base) % stride == 0:
                    elems.add(rn(ops[0].reg)); done = True

            # INDEX REGISTERS ARE TRACKED BY THEIR MULTIPLIER, not by "is a multiple
            # of stride". `SpawnGroupLedger` (stride 0x18) is why. The compiler does
            # not `imul` by 24; it writes `lea rcx, [rdx + rdx*2]` -- a multiply by
            # THREE -- and lets the addressing mode's scale of 8 supply the rest. A
            # rule that only knew `imul` and `shl` could not see it, and the type came
            # back with zero accesses through every route while its own field evidence
            # cites thirteen sites. Strides of 24, 40 and 72 are all built this way.
            if not done and m == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM \
                    and ops[1].mem.base and ops[1].mem.index \
                    and ops[1].mem.base == ops[1].mem.index and ops[1].mem.disp == 0:
                src = rn(ops[1].mem.base)
                mul[rn(ops[0].reg)] = {(1 + ops[1].mem.scale) * v
                                       for v in mul.get(src, {1})}
                done = True
            if not done and m == "imul" and len(ops) == 3 \
                    and ops[2].type == X86_OP_IMM and ops[2].imm > 0:
                mul[rn(ops[0].reg)] = {ops[2].imm * v
                                       for v in mul.get(rn(ops[1].reg), {1})}
                if stride and ops[2].imm % stride == 0:
                    idxs.add(rn(ops[0].reg))
                done = True
            if not done and m == "shl" and len(ops) == 2 \
                    and ops[1].type == X86_OP_IMM:
                mul[rn(ops[0].reg)] = {(1 << ops[1].imm) * v
                                       for v in mul.get(rn(ops[0].reg), {1})}
                done = True
            if not done and m in ("movsxd", "movsx", "movzx") and len(ops) == 2 \
                    and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG:
                mul[rn(ops[0].reg)] = set(mul.get(rn(ops[1].reg), {1}))
                done = True

            if not done and m == "lea" and len(ops) == 2 \
                    and ops[1].type == X86_OP_MEM:
                mem, dst = ops[1].mem, rn(ops[0].reg)
                bn = rn(mem.base) if mem.base else None
                inm = rn(mem.index) if mem.index else None
                if bn in bases and (inm in idxs
                                    or (mem.index and mem.scale
                                        and any(v * mem.scale == stride
                                                for v in mul.get(inm, {1})))):
                    elems.add(dst)
                elif bn in elems and mem.index == 0 and 0 <= mem.disp < stride:
                    elems.add(dst)
                elif bn in idxs and inm in bases:
                    elems.add(dst)
                else:
                    for s in (bases, elems, idxs):
                        s.discard(dst)
                    mul.pop(dst, None)
                done = True

            if not done:
                # record accesses off a tracked register
                for oi, op in enumerate(ops):
                    if op.type != X86_OP_MEM or op.mem.base in (0, X86_REG_RIP):
                        continue
                    bn = rn(op.mem.base)
                    d = None
                    if bn in elems and 0 <= op.mem.disp < stride:
                        d = op.mem.disp
                    elif bn in bases and 0 <= op.mem.disp < span:
                        d = op.mem.disp % stride
                    if d is None:
                        continue
                    rec(fn, ins.address, d,
                        RT.op_kind(ins, op, oi),
                        m + " " + ins.op_str, "reg")

            if ins.group(CS_GRP_CALL):
                for s in (bases, elems, idxs):
                    for v in list(s):
                        if v in VOLATILE:
                            s.discard(v)
                for v in VOLATILE:
                    mul.pop(v, None)
            elif not done and m == "mov" and len(ops) == 2 \
                    and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG:
                d_, s_ = rn(ops[0].reg), rn(ops[1].reg)
                for st2 in (bases, elems, idxs):
                    if s_ in st2:
                        st2.add(d_)
                        break
                else:
                    for st2 in (bases, elems, idxs):
                        st2.discard(d_)
                    mul.pop(d_, None)
            elif not done and ops and ops[0].type == X86_OP_REG:
                n2 = rn(ops[0].reg)
                for s in (bases, elems, idxs):
                    s.discard(n2)
                mul.pop(n2, None)
        return (frozenset(bases), frozenset(elems), frozenset(idxs),
                {k: frozenset(v) for k, v in mul.items()})

    EMPTY = (frozenset(), frozenset(), frozenset(), {})
    for fn in sorted(sizes):
        body = blob[fn - tva:fn - tva + sizes[fn]]
        if not body:
            continue
        try:
            ins_list = list(md.disasm(body, fn))
        except Exception:
            continue
        insns = {i.address: i for i in ins_list}
        order = sorted(insns)
        if not order:
            continue
        nxt = {order[i]: order[i + 1] for i in range(len(order) - 1)}
        succ = {}; ind = []
        for a in order:
            ins = insns[a]; ops = ins.operands; m = ins.mnemonic; s = []
            fall = nxt.get(a)
            if m == "jmp" and len(ops) == 1 and ops[0].type == X86_OP_IMM:
                if ops[0].imm in insns:
                    s = [ops[0].imm]
            elif m == "jmp":
                ind.append(a)
            elif (m.startswith("j") or m in ("loop", "loope", "loopne")) \
                    and len(ops) == 1 and ops[0].type == X86_OP_IMM:
                if ops[0].imm in insns:
                    s.append(ops[0].imm)
                if fall:
                    s.append(fall)
            elif m.startswith("ret") or m in ("ud2", "int3", "iret", "iretq", "iretd"):
                pass
            elif fall:
                s = [fall]
            succ[a] = s
        IN = {fn: EMPTY}; OUT = {}
        wl = collections.deque([fn]); onwl = {fn}; visited = set()
        while True:
            while wl:
                a = wl.popleft(); onwl.discard(a)
                st = IN.get(a)
                if st is None:
                    continue
                visited.add(a)
                ns = xfer(insns[a], st, fn)
                OUT[a] = ns
                for s in succ[a]:
                    j = joinst(IN.get(s, EMPTY), ns)
                    if IN.get(s) != j:
                        IN[s] = j
                        if s not in onwl:
                            wl.append(s); onwl.add(s)
            heads = []
            prev = True
            for a in order:
                if a not in visited:
                    if prev:
                        heads.append(a)
                    prev = False
                else:
                    prev = True
            if not heads:
                break
            base_st = EMPTY
            srcs = [a for a in ind if a in OUT] or list(OUT)
            for a in srcs:
                base_st = joinst(base_st, OUT[a])
            for h in heads:
                IN[h] = joinst(IN.get(h, EMPTY), base_st)
                if h not in onwl:
                    wl.append(h); onwl.add(h)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True)
    ap.add_argument("--control", default=None, help="offset=count pairs, e.g. 0x0=11,0x12=1")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    rt = route_for(a.type)
    if not rt:
        print("no ARRAY route for %s" % a.type)
        return 2
    base, stride, count = rt
    raw, tva, tvs, tpr = load_text()
    blob = raw[tpr:tpr + tvs]
    sizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    rows = scan(base, stride, count, blob, tva, sizes, names, md)
    seen, out = set(), []
    for x in rows:
        k = (x[2], x[3])
        if k not in seen:
            seen.add(k)
            out.append(x)
    out.sort(key=lambda x: (x[3], x[2]))
    per = collections.Counter(x[3] for x in out)
    via = collections.Counter(x[6] for x in out)
    print("%s: ARRAY %08X stride 0x%X count %d" % (a.type, base, stride, count))
    print("  %d distinct access(es) at %d distinct offset(s)   (%s)"
          % (len(out), len(per), ", ".join("%s %d" % kv for kv in sorted(via.items()))))

    ok = True
    if a.control:
        print()
        print("  CONTROL - each offset must show exactly the declared count")
        for part in a.control.split(","):
            o, c = part.split("=")
            o, c = int(o, 0), int(c)
            got = per.get(o, 0)
            good = got == c
            ok = ok and good
            print("    +0x%03X  want %3d  got %3d   %s" % (o, c, got, "ok" if good else "MISMATCH"))
        print("  %s" % ("control passes" if ok else "CONTROL FAILED - not writing"))

    if a.out and (ok or not a.control):
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
            for fn, nm, site, d, kind, txt, how in out:
                fh.write("%08X\t%s\t%08X\t0x%X\t%s\t%s\tarray %08X %s\t\n"
                         % (fn, nm, site, d, kind, txt, base, how))
        print("  wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
