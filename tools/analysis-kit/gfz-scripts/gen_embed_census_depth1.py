#!/usr/bin/env python3
"""gen_embed_census_depth1.py - a census for `EMBED Parent +0xOFF`, following the lea handoff.

THE SHAPE NO GENERATOR COVERS. `ManagerSub0209BE80_8FA0` is `EMBED ManagerSingleton0209BE80
+0x8FA0`, 0x1130 bytes, and **99% of it is declared span**. It is not accessed through the parent's
base register at all. The parent's constructor computes its address once and hands it away:

    00291750  ...
    002917AA  lea rcx, [rdi + 0x8fa0]      rdi = the singleton, rcx = THIS SUB-OBJECT
    002917B1  call <initialiser>
    002917B6  lea rcx, [rdi + 0x8fa0]      and again, to a second one
    002917BD  call <initialiser>

Every field of the sub-object is then touched off `rcx` INSIDE those callees, at displacements
relative to the sub-object, not the parent. A parent census sees one `lea` and nothing else, which
is exactly what "99% unexplained" was recording.

METHOD, three seeds rather than one.

  A. Track the PARENT from its `PTR` slot, seeding on both the load and the store (a lazy
     singleton's initialiser publishes the object instead of loading it).
  B. Inside that walk, `lea rX, [parent + OFF]` seeds rX as the SUB-OBJECT base, and a parent-
     relative access whose displacement falls inside `[OFF, OFF+size)` is recorded as a
     sub-object access at `disp - OFF`. Both are the same object by construction.
  C. When a sub-object base reaches an argument register and a DIRECT call follows, the callee is
     re-scanned with that parameter register seeded - the same one-level rule as
     `gen_ptr_census_depth1.py`, and the same reason: one level is what the argument registers
     establish, and a second would need the value to survive another frame.

THE CHAIN IS WALKED, AND THE SCOPE WAS MEASURED BEFORE IT WAS WIDENED. Of the store's 26 `EMBED`
types, a one-level resolver reached 7. Composing the offsets up a chain of `EMBED`s to the first
`PTR` reaches 10: `ManagerSub00A0Entry` is `EMBED ManagerSub0209BE80_00A0 +0x20`, whose parent is
`EMBED ManagerSingleton0209BE80 +0xA0`, so the element sits at `singleton + 0xC0`. The remaining 16
have `ARRAY`/`PARRAY`/`CHAIN`/`DYNAMIC` parents and are NOT handled - deliberately: they hold 118
unexplained bytes between them and are already 0-5% unexplained, while the three types the chain
walk adds hold 518. Widening further would be work spent where there is nothing to find.

An array element type carries `stride`/`count` from its own row, and a parent-relative access is
attributed **modulo the stride**, so element 7's field `+0x10` is recorded at `+0x10` rather than
at `0x710`. A `lea` onto any element boundary seeds the sub-object, not only element 0.

CONTROLS AND LIMITS. Counts are floors, as every census here is. Only direct calls are followed.
Register writes come from `reg_tracking.written()`, so `test`/`cmp`/`push` no longer end tracking
and implicit writes like `mul`'s to rax/rdx do. Indexed operands ARE recorded, with the scale
reported, because an embedded array is walked with an index and discarding those is how a large
interior stays invisible.

    python gen_embed_census_depth1.py --type ManagerSub0209BE80_8FA0
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
import reg_tracking as RT
import kit_paths as KP

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE
VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
ARGREG = ["rcx", "rdx", "r8", "r9"]
R_EMBED = re.compile(r"^EMBED\s+(\w+)\s*\+\s*(0x[0-9A-Fa-f]+)")
R_PTR = re.compile(r"^PTR\s+(0x[0-9A-Fa-f]+)(?:\s*\+\s*(0x[0-9A-Fa-f]+))?")


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


def rows_by_type(db):
    out = {}
    with io.open(os.path.join(db, "_types", "types.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if f and f[0]:
                out[f[0]] = f
    return out


R_SC = re.compile(r"stride=(0x[0-9A-Fa-f]+|\d+)(?:\s+count=(\d+))?")


def _to_ptr(name, T, acc, depth, seen):
    """Walk an EMBED chain up to a PTR slot, summing the offsets. Returns (slot, total_off, path)."""
    if name in seen or depth > 6:
        return None
    row = T.get(name)
    if not row or len(row) < 13:
        return None
    for alt in row[12].split("|"):
        m = R_PTR.match(alt.strip())
        if m:
            return int(m.group(1), 16), acc, [name]
    for alt in row[12].split("|"):
        m = R_EMBED.match(alt.strip())
        if m:
            r = _to_ptr(m.group(1), T, acc + int(m.group(2), 16), depth + 1, seen + (name,))
            if r:
                return r[0], r[1], [name] + r[2]
    return None


def resolve(tname, T):
    """(PTR slot, offset from the slot's object, size, chain, stride, count).

    THE CHAIN IS WALKED, NOT ASSUMED ONE LEVEL DEEP. `ManagerSub00A0Entry` is
    `EMBED ManagerSub0209BE80_00A0 +0x20 stride=0x100 count=64`, and that parent is itself
    `EMBED ManagerSingleton0209BE80 +0xA0`. Only by composing `0xA0 + 0x20` does the element land
    at `singleton + 0xC0`, and only then can a scan seeded on the singleton see it. Stopping at
    one level left three types - 518 of the 636 unexplained bytes among the EMBED types this tool
    could not previously reach - permanently invisible.

    `stride`/`count` come from THIS type's own EMBED row when it is an array element, so an access
    is attributed modulo the stride rather than treated as a single record.
    """
    row = T.get(tname)
    if not row or len(row) < 13:
        return None
    try:
        size = int(row[1], 0)
    except ValueError:
        return None
    for alt in row[12].split("|"):
        m = R_EMBED.match(alt.strip())
        if not m:
            continue
        r = _to_ptr(m.group(1), T, int(m.group(2), 16), 0, (tname,))
        if not r:
            continue
        slot, off, path = r
        stride = count = None
        sc = R_SC.search(alt)
        if sc:
            stride = int(sc.group(1), 0)
            count = int(sc.group(2)) if sc.group(2) else None
        return slot, off, size, " -> ".join([tname] + path), stride, count
    return None


def record(rows, fn, names, ins, op, oi, d, scale, idxname):
    rows.append((fn, names.get(fn, ""), ins.address, d, RT.op_kind(ins, op, oi),
                 ins.mnemonic + " " + ins.op_str, scale, idxname))


def walk(md, il, size, rows, fn, names, slot=None, emb_off=None,
         sub_seed=None, call_out=None, par_seed=None, parent_pend=False,
         stride=None, count=None):
    """Track the parent (via `slot` or `par_seed`) and the sub-object simultaneously.

    `parent_pend` switches what `call_out` collects: with it set, the pairs recorded are the calls
    that receive the PARENT in an argument register (used to find the constructor); otherwise they
    are the calls that receive the SUB-OBJECT.
    """
    par = set(par_seed or ())
    sub = set(sub_seed or ())
    pend = {}
    if parent_pend:
        for p in par:
            if p in ARGREG:
                pend[p] = True
    for ins in il:
        rn, ops, mn = ins.reg_name, ins.operands, ins.mnemonic
        if mn.startswith("nop") or mn.startswith("prefetch"):
            continue

        if slot is not None and mn == "mov" and len(ops) == 2:
            if ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM \
                    and ops[1].mem.base == X86_REG_RIP and not ops[1].mem.index \
                    and ins.address + ins.size + ops[1].mem.disp == slot:
                par.add(rn(ops[0].reg))
                continue
            if ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_REG \
                    and ops[0].mem.base == X86_REG_RIP and not ops[0].mem.index \
                    and ins.address + ins.size + ops[0].mem.disp == slot:
                par.add(rn(ops[1].reg))
                continue

        # the handoff: lea rX, [parent + emb_off]  -> rX is the sub-object.
        # For an ARRAY element type, any element base counts: the displacement must land on an
        # element boundary inside the array, not only on element 0.
        if emb_off is not None and mn == "lea" and len(ops) == 2 \
                and ops[1].type == X86_OP_MEM and ops[1].mem.base \
                and ops[1].mem.base != X86_REG_RIP and not ops[1].mem.index \
                and rn(ops[1].mem.base) in par:
            rel = ops[1].mem.disp - emb_off
            hit = (rel == 0) if not stride else \
                  (0 <= rel < stride * (count or 1) and rel % stride == 0)
            if hit:
                d = rn(ops[0].reg)
                sub.add(d)
                if d in ARGREG:
                    pend[d] = True
                continue

        for oi, op in enumerate(ops):
            if op.type != X86_OP_MEM or not op.mem.base or op.mem.base == X86_REG_RIP:
                continue
            bn = rn(op.mem.base)
            ix = rn(op.mem.index) if op.mem.index else ""
            if bn in sub:
                if 0 <= op.mem.disp < size:
                    record(rows, fn, names, ins, op, oi, op.mem.disp, op.mem.scale, ix)
            elif bn in par and emb_off is not None:
                rel = op.mem.disp - emb_off
                if stride:
                    # an ARRAY element: attribute modulo the stride, so element 7's field +0x10
                    # is recorded at +0x10 and not at 0x710.
                    if 0 <= rel < stride * (count or 1):
                        d = rel % stride
                        if d < size:
                            record(rows, fn, names, ins, op, oi, d, op.mem.scale, ix)
                elif 0 <= rel < size:
                    record(rows, fn, names, ins, op, oi, rel, op.mem.scale, ix)

        if mn == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and ops[1].type == X86_OP_REG:
            s, d = rn(ops[1].reg), rn(ops[0].reg)
            if s in sub:
                sub.add(d)
                if d in ARGREG:
                    pend[d] = True
            elif s in par:
                par.add(d)
                sub.discard(d)
                pend.pop(d, None)
                if parent_pend and d in ARGREG:
                    pend[d] = True
            else:
                par.discard(d)
                sub.discard(d)
                pend.pop(d, None)
            continue

        if ins.group(CS_GRP_CALL):
            if call_out is not None and ops and ops[0].type == X86_OP_IMM:
                for a in list(pend):
                    call_out.add((ops[0].imm, ARGREG.index(a)))
            par -= VOLATILE
            sub -= VOLATILE
            pend.clear()
            continue

        for w in RT.written(ins):
            par.discard(w)
            sub.discard(w)
            pend.pop(w, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True)
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--out")
    a = ap.parse_args()

    T = rows_by_type(a.db)
    r = resolve(a.type, T)
    if not r:
        print("no EMBED route resolving to a parent PTR slot for %s" % a.type)
        return 2
    slot, emb_off, size, chain, stride, count = r
    raw, tva, tvs, tpr = load_text()
    blob = raw[tpr:tpr + tvs]
    sizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    print("%s: size 0x%X at PTR %08X +0x%X%s"
          % (a.type, size, slot, emb_off,
             ("  stride 0x%X count %s" % (stride, count)) if stride else ""))
    print("  chain: %s" % chain)

    def body_of(fn):
        o = fn - tva
        if o < 0 or o >= len(blob):
            return None
        b = blob[o:o + sizes.get(fn, 0)]
        if not b:
            return None
        try:
            return list(md.disasm(b, fn))
        except Exception:
            return None

    # PASS 0 - WHERE THE PARENT GOES. The handoff that matters is not in a body that loads the
    # singleton; it is in the CONSTRUCTOR, which receives the parent as an argument:
    #     0028F8DE  call 00291750          with rcx = the object
    #     002917AA  lea  rcx, [rdi+0x8fa0] inside it, rdi being that parameter
    # A scan that only seeds the parent from its global slot has an empty parent set in 00291750
    # and therefore never sees the lea. So first find every (callee, argument index) at which the
    # PARENT is passed, then walk those callees with the parent seeded from that parameter.
    parent_callees = set()
    for fn in sorted(sizes):
        il = body_of(fn)
        if il:
            walk(md, il, size, [], fn, names, slot=slot, emb_off=None,
                 call_out=parent_callees, parent_pend=True)
    print("  PASS 0 functions receiving the parent as an argument: %d" % len(parent_callees))

    rows, callees = [], set()
    for fn in sorted(sizes):
        il = body_of(fn)
        if il:
            walk(md, il, size, rows, fn, names, slot=slot, emb_off=emb_off,
                 call_out=callees, stride=stride, count=count)
    # and again inside the bodies that receive the parent, with it seeded from the parameter
    for callee, argi in sorted(parent_callees):
        il = body_of(callee)
        if il:
            walk(md, il, size, rows, callee, names, emb_off=emb_off,
                 par_seed={ARGREG[argi]}, call_out=callees, stride=stride, count=count)

    p1 = len({(x[2], x[3]) for x in rows})
    print("  PASS 1 (parent body, via lea or parent-relative) : %d access(es) at %d offset(s)"
          % (p1, len({x[3] for x in rows})))
    print("  PASS 2 callee/arg pairs                          : %d" % len(callees))

    before = len(rows)
    for callee, argi in sorted(callees):
        if callee not in sizes:
            continue
        o = callee - tva
        b = blob[o:o + sizes[callee]]
        if not b:
            continue
        try:
            il = list(md.disasm(b, callee))
        except Exception:
            continue
        walk(md, il, size, rows, callee, names, sub_seed={ARGREG[argi]})
    print("  PASS 2 added                                     : %d raw row(s)"
          % (len(rows) - before))

    seen, out = set(), []
    for x in rows:
        k = (x[2], x[3])
        if k not in seen:
            seen.add(k)
            out.append(x)
    out.sort(key=lambda x: (x[3], x[2]))
    kinds = collections.Counter(x[4] for x in out)
    nidx = sum(1 for x in out if x[7])
    print()
    print("  TOTAL: %d access(es) at %d offset(s)  (%s)  indexed: %d"
          % (len(out), len({x[3] for x in out}),
             ", ".join("%s %d" % kv for kv in sorted(kinds.items())), nidx))
    print("  functions contributing: %d" % len({x[0] for x in out}))
    for fn, nm, site, d, kind, txt, sc, ix in out[:20]:
        print("    +0x%-5X %08X in %08X %-4s %s" % (d, site, fn, kind, txt[:50]))
    if len(out) > 20:
        print("    ... %d more" % (len(out) - 20))

    if a.out and out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write("function\tname\tsite\tdisp\tkind\tinstruction\tscale\tindex\troute\n")
            for fn, nm, site, d, kind, txt, sc, ix in out:
                # `parent` never existed - the route tuple unpacks to `slot`, and this line
                # raised NameError for every type that reached it. Because the crash happens
                # AFTER the summary is printed and only when `--out` is given, every EMBED
                # census in a sweep came back as a 0-row file while the console showed the
                # accesses being found. Silent empty output from a tool that says it found
                # something is the worst shape of failure, so: `slot`, formatted as the
                # summary line above already formats it.
                fh.write("%08X\t%s\t%08X\t0x%X\t%s\t%s\t%s\t%s\tembed-d1 %08X+0x%X\n"
                         % (fn, nm, site, d, kind, txt, sc, ix, slot, emb_off))
        print("  wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
