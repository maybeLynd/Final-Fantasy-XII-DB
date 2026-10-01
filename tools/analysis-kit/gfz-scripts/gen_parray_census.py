#!/usr/bin/env python3
"""gen_parray_census.py - census for the `PARRAY` and `SLOTPTR` route forms.

`gen_ptr_census.py` finished the bare `PTR` third of the `*(void**)0xADDR` class the route grammar
named. This finishes the other two:

    PARRAY  0xADDR [+0xOFF] stride=0xS   element i at *(ADDR) + OFF + i*S
    SLOTPTR 0xADDR stride=0xS [count=N]  instance i = *(ADDR + i*S), a table OF pointers

**These need element tracking, which the `PTR` scan does not do.** A `PARRAY` element is reached by
adding an index to the array base, and x86 scales stop at 8, so any stride above that - and
`CharacterRenderRecord`'s is `0x740` - is reached by PRE-MULTIPLYING the index and adding a whole
register. `find_indexed_tables.py` established that fact with controls; this relies on it:

    mov  rB, [rip -> ADDR]          rB = the container base
    lea  rE, [rB + 0xOFF]           rE = element 0
    imul rI, rC, 0x740              rI = a byte offset, i * stride
    lea  rE2, [rE + rI]             rE2 = element i
    ...  [rE2 + disp]               an access at element-relative `disp`

So three register sets are carried: bases (`*(ADDR)`), element pointers, and index registers known
to hold a multiple of the stride. A register leaves every set the moment something else writes it.

A `SLOTPTR` is simpler and different in kind: the global is a table of POINTERS, so the instance
comes from a second load - `mov rX, [rip -> ADDR + k*S]` for a constant slot, or `lea rT, [rip ->
ADDR]` then `mov rX, [rT + rI*S]`.

CONTROL, again an existing census rather than a count
-----------------------------------------------------
`CharacterRenderRecord` is `PARRAY 0x022C6F28 stride=0x740 count=160` and already has
`character-render-record-accesses.tsv` from different work. Offsets and instruction text are
checked, not just that the decoder ran - the same standard `gen_ptr_census.py` used, which caught
two real defects there that a site count would have passed.

LIMITS: same-function only, so counts are a FLOOR; an element pointer passed to a callee is
invisible; no type is inferred, only the instruction recorded.

    python gen_parray_census.py --type CharacterRenderRecord --control <existing tsv>
    python gen_parray_census.py --type BattleUnit --out <path>
"""
import argparse
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

R_PARRAY = re.compile(r"^PARRAY\s+(0x[0-9A-Fa-f]+)(?:\s*\+\s*(0x[0-9A-Fa-f]+))?\s+stride=(0x[0-9A-Fa-f]+|\d+)")
R_SLOT = re.compile(r"^SLOTPTR\s+(0x[0-9A-Fa-f]+)\s+stride=(0x[0-9A-Fa-f]+|\d+)(?:\s+count=(\d+))?")


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
            if f and f[0] == tname:
                try:
                    size = int(f[1], 0)
                except (ValueError, IndexError):
                    size = None
                for a in (f[12] if len(f) > 12 else "").split("|"):
                    a = a.strip()
                    m = R_PARRAY.match(a)
                    if m:
                        return ("PARRAY", int(m.group(1), 0),
                                int(m.group(2), 0) if m.group(2) else 0,
                                int(m.group(3), 0), size, None)
                    m = R_SLOT.match(a)
                    if m:
                        # THE COUNT IS LOAD-BEARING, NOT DECORATION. Without it this scan bounded
                        # the pointer table at `stride * 256` and `AuthoredTableHeader`
                        # (SLOTPTR 02EBEF70 stride 8 count 40) reached 02EBF770 -- which contains
                        # 02EBF190, THE BattleSystemState POINTER. Every BattleSystemState access
                        # was attributed to a 32-byte type: 1,461 accesses at 20 offsets, a
                        # nonsense figure that looked like a rich census.
                        return ("SLOTPTR", int(m.group(1), 0), 0,
                                int(m.group(2), 0), size,
                                int(m.group(3)) if m.group(3) else None)
    return (None, 0, 0, 0, None, None)


def drop(sets, name):
    for s in sets:
        s.discard(name)


def scan(kind, slot, boff, stride, size, count, blob, tva, sizes, names, md):
    span = size if size else stride
    rows = []
    for fn in sorted(sizes):
        body = blob[fn - tva:fn - tva + sizes[fn]]
        if not body:
            continue
        try:
            ins_list = list(md.disasm(body, fn))
        except Exception:
            continue
        bases, elems, idxs, tables = set(), set(), set(), set()
        mul = {}
        for ins in ins_list:
            rn = ins.reg_name
            ops = ins.operands
            m = ins.mnemonic

            if m.startswith("nop") or m.startswith("prefetch"):
                continue

            # ---- seeds ------------------------------------------------------
            if m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP:
                tgt = ins.address + ins.size + ops[1].mem.disp
                if kind == "PARRAY" and tgt == slot:
                    bases.add(rn(ops[0].reg))
                    continue
                if kind == "SLOTPTR" and stride and slot <= tgt < slot + stride * (count or 64) \
                        and (tgt - slot) % stride == 0:
                    elems.add(rn(ops[0].reg))       # the loaded POINTER is an instance
                    continue
            if kind == "PARRAY" and m == "mov" and len(ops) == 2 \
                    and ops[0].type == X86_OP_MEM and ops[0].mem.base == X86_REG_RIP \
                    and ops[1].type == X86_OP_REG \
                    and ins.address + ins.size + ops[0].mem.disp == slot:
                bases.add(rn(ops[1].reg))
                continue
            if m == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM \
                    and ops[1].mem.base == X86_REG_RIP \
                    and ins.address + ins.size + ops[1].mem.disp == slot:
                tables.add(rn(ops[0].reg))          # rT = &table (SLOTPTR) or &base cell
                continue
            # SLOTPTR: mov rX, [rT + rI*S]  or  [rT + k*S]
            if kind == "SLOTPTR" and m == "mov" and len(ops) == 2 \
                    and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM \
                    and ops[1].mem.base != 0 and rn(ops[1].mem.base) in tables:
                elems.add(rn(ops[0].reg))
                continue

            # ---- index registers, tracked by MULTIPLIER ----------------------
            # Carried over from gen_array_census.py, where the same omission made
            # `SpawnGroupLedger` return zero accesses against thirteen documented sites. A compiler
            # builds a stride of 24 as `lea r,[x+x*2]` (x3) plus a scale of 8, never as `imul 24`,
            # and `find_indexed_tables.py` established with controls that large strides here are
            # reached by pre-multiplying. Knowing only `imul` and `shl` misses every such form.
            if m == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM \
                    and ops[1].mem.base and ops[1].mem.index \
                    and ops[1].mem.base == ops[1].mem.index and ops[1].mem.disp == 0:
                mul[rn(ops[0].reg)] = (1 + ops[1].mem.scale) * mul.get(rn(ops[1].mem.base), 1)
                continue
            if m == "imul" and len(ops) == 3 and ops[2].type == X86_OP_IMM and ops[2].imm > 0:
                mul[rn(ops[0].reg)] = ops[2].imm * mul.get(rn(ops[1].reg), 1)
                if stride and ops[2].imm % stride == 0:
                    idxs.add(rn(ops[0].reg))
                continue
            if m == "shl" and len(ops) == 2 and ops[1].type == X86_OP_IMM:
                mul[rn(ops[0].reg)] = (1 << ops[1].imm) * mul.get(rn(ops[0].reg), 1)
                if stride and (1 << ops[1].imm) % stride == 0:
                    idxs.add(rn(ops[0].reg))
                continue
            if m in ("movsxd", "movsx", "movzx") and len(ops) == 2 \
                    and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG:
                mul[rn(ops[0].reg)] = mul.get(rn(ops[1].reg), 1)
                continue

            # ---- element pointers -------------------------------------------
            if m == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM:
                mem = ops[1].mem
                bn = rn(mem.base) if mem.base else None
                inm = rn(mem.index) if mem.index else None
                dst = rn(ops[0].reg)
                if kind == "PARRAY":
                    if bn in bases and mem.index == 0 and mem.disp == boff:
                        elems.add(dst)
                        continue
                    if bn in bases and (inm in idxs
                                        or (mem.index and mem.scale
                                            and mul.get(inm, 1) * mem.scale == stride)):
                        elems.add(dst)
                        continue
                    if bn in elems and (inm in idxs or mem.index == 0) and 0 <= mem.disp < stride:
                        elems.add(dst)
                        continue
                    if bn in idxs and inm in (bases | elems):
                        elems.add(dst)
                        continue
                drop((bases, elems, idxs, tables), dst)
                continue
            if m == "add" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_REG:
                d, s = rn(ops[0].reg), rn(ops[1].reg)
                if (d in elems and s in idxs) or (d in idxs and s in elems):
                    elems.add(d)
                    continue
                if d in bases and s in idxs:
                    elems.add(d)
                    continue

            # ---- record accesses ---------------------------------------------
            for oi, op in enumerate(ops):
                if op.type != X86_OP_MEM or op.mem.base in (0, X86_REG_RIP):
                    continue
                bn = rn(op.mem.base)
                d = None
                if bn in elems and 0 <= op.mem.disp < span:
                    d = op.mem.disp
                elif kind == "PARRAY" and bn in bases and boff <= op.mem.disp < boff + span:
                    d = op.mem.disp - boff       # element 0 addressed directly off the base
                if d is None:
                    continue
                kindc = RT.op_kind(ins, op, oi)
                rows.append((fn, names.get(fn, ""), ins.address, d, kindc,
                             m + " " + ins.op_str))

            # ---- invalidation -------------------------------------------------
            if ins.group(CS_GRP_CALL):
                for s in (bases, elems, idxs, tables):
                    for v in list(s):
                        if v in VOLATILE:
                            s.discard(v)
                continue
            if m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_REG:
                d, s = rn(ops[0].reg), rn(ops[1].reg)
                if s in elems:
                    elems.add(d)
                    continue
                if s in bases:
                    bases.add(d)
                    continue
                if s in idxs:
                    idxs.add(d)
                    continue
            if ops and ops[0].type == X86_OP_REG:
                drop((bases, elems, idxs, tables), rn(ops[0].reg))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True)
    ap.add_argument("--control", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    kind, slot, boff, stride, size, count = route_for(a.type)
    if kind is None:
        print("no PARRAY/SLOTPTR route for %s" % a.type)
        return 2
    raw, tva, tvs, tpr = load_text()
    blob = raw[tpr:tpr + tvs]
    sizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    rows = scan(kind, slot, boff, stride, size, count, blob, tva, sizes, names, md)
    seen, out = set(), []
    for x in rows:
        k = (x[2], x[3])
        if k not in seen:
            seen.add(k)
            out.append(x)
    out.sort(key=lambda x: (x[3], x[2]))
    print("%s: %s %08X +0x%X stride 0x%X count %s (table spans %08X..%08X)"
          % (a.type, kind, slot, boff, stride, count,
             slot, slot + stride * (count or 64)))
    print("  %d distinct access(es) at %d distinct offset(s)"
          % (len(out), len({x[3] for x in out})))

    if a.control:
        ctl = set()
        for f in csv.reader(io.open(a.control, encoding="utf-8", newline=""), delimiter="\t"):
            if len(f) > 3:
                try:
                    ctl.add((int(f[2], 16), int(f[3], 0)))
                except ValueError:
                    pass
        mine = {(x[2], x[3]) for x in out}
        hit = ctl & mine
        print("  CONTROL %s: %d sites, reproduced %d (%.1f%%), added %d"
              % (os.path.basename(a.control), len(ctl), len(hit),
                 100.0 * len(hit) / len(ctl) if ctl else 0.0, len(mine - ctl)))
        bad = sorted(mine - ctl)[:6]
        if bad:
            print("  added sites (verify before trusting): %s"
                  % " ".join("%08X@+0x%X" % b for b in bad))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
            for fn, nm, site, d, kc, txt in out:
                fh.write("%08X\t%s\t%08X\t0x%X\t%s\t%s\t%s %08X\t\n"
                         % (fn, nm, site, d, kc, txt, kind.lower(), slot))
        print("  wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
