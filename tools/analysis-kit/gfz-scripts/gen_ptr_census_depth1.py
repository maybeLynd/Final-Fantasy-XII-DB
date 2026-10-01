#!/usr/bin/env python3
"""gen_ptr_census_depth1.py - follow a singleton INTO the functions it is passed to.

THE LIMIT THIS REMOVES IS ONE EVERY GENERATOR IN THIS KIT SHARES, and each of them says so in its
own docstring: *"same-function only"*, *"a root passed as an argument is invisible"*. That boundary
is not a detail. `LegacyPs2GsTextureContext` is `PTR 0x0209A670`, 0x240 bytes, and
`gen_ptr_census.py` finds **6 accesses at 4 offsets** - because almost nothing indexes the global
directly. The code loads it once and hands it to a worker:

    0026E29A  mov  rbx, qword ptr [rip -> 0209A670]     the singleton
    ...
              mov  rcx, rbx
              call 002F7380                             the worker does the real work

Every access inside `002F7380` is invisible to a same-function scan, and those are the accesses
that matter. A census that reports 4 offsets for a 576-byte object is not measuring the object; it
is measuring its own reach.

METHOD, in two passes.

  PASS 1, unchanged: find `mov rX, [rip -> ADDR]`, track rX forward, record direct accesses.
  PASS 2, the addition: in the same walk, when a tracked register is moved into an ARGUMENT
          register (rcx, rdx, r8, r9) and a direct call follows before that register is clobbered,
          record the pair (callee, argument index). Then disassemble each callee with the
          corresponding parameter register seeded as the object base, and record its accesses.

WHAT KEEPS PASS 2 HONEST.

  * Only DIRECT calls with an immediate target are followed. An indirect call names no callee.
  * The seed is dropped in the callee exactly as in pass 1 - any write to the register that is not
    a propagating `mov reg, reg` kills it, and a nested call kills the volatiles. A callee that
    overwrites its parameter before using it contributes nothing, which is correct.
  * ONE level. A depth-2 walk would need the argument to survive a second call frame, and nothing
    here establishes that it does. The count remains a FLOOR, as every census here is.
  * A callee reached with the object in two different argument positions from two call sites is
    scanned once per position, and identical (site, offset) pairs are collapsed.

WHAT IT STILL CANNOT SEE: the object stored into another structure and re-read later, an access
through an index register, and any callee that is not in the function list.

    python gen_ptr_census_depth1.py --type LegacyPs2GsTextureContext
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
R_PTR = re.compile(r"^PTR\s+(0x[0-9A-Fa-f]+)(?:\s*\+\s*(0x[0-9A-Fa-f]+))?")
R_FN = re.compile(r"^FN\s+(0x[0-9A-Fa-f]+)\s*\+\s*(0x[0-9A-Fa-f]+)")


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


def route_for(tname, db):
    with io.open(os.path.join(db, "_types", "types.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if f and f[0] == tname and len(f) > 12:
                try:
                    size = int(f[1], 0)
                except ValueError:
                    size = None
                for alt in f[12].split("|"):
                    m = R_PTR.match(alt.strip())
                    if m:
                        return int(m.group(1), 16), int(m.group(2) or "0", 16), size, "PTR"
                    m = R_FN.match(alt.strip())
                    if m:
                        return int(m.group(1), 16), int(m.group(2), 16), size, "FN"
    return None, None, None, None


def body(blob, tva, sizes, fn):
    o = fn - tva
    if o < 0 or o >= len(blob):
        return None
    b = blob[o:o + sizes.get(fn, 0)]
    return b or None


def walk(md, ins_list, seeded, size, off, rows, fn, names, call_out=None, slot=None,
         fn_addr=None):
    """Track `seeded` (a set of register names holding the object base) through one body.

    When `slot` is given the walk ALSO seeds itself, on two instructions:

        mov rX, qword ptr [rip -> slot]     rX now holds the instance
        mov qword ptr [rip -> slot], rX     rX IS the instance - a lazy singleton's initialiser
                                            publishes the object rather than loading it

    The store seed is not an embellishment. Omitting it cost this tool 126 of 258 accesses on
    `ManagerSingleton0209BE80` (132 against the plain generator's 258, 35 offsets against 51),
    because a body that constructs the singleton reassigns the register between the null test and
    the store, so a load-only seed never sees it. `gen_ptr_census.py` learned this already and
    says so in its own comment; this scan simply had not inherited it.
    """
    held = set(seeded)
    pend = {}                      # argreg -> True, set when the object is placed in it
    for ins in ins_list:
        rn, ops, mn = ins.reg_name, ins.operands, ins.mnemonic
        if mn.startswith("nop") or mn.startswith("prefetch"):
            continue

        if slot is not None and mn == "mov" and len(ops) == 2:
            # load form: mov rX, [rip -> slot]
            if ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM \
                    and ops[1].mem.base == X86_REG_RIP and not ops[1].mem.index \
                    and ins.address + ins.size + ops[1].mem.disp == slot:
                held.add(rn(ops[0].reg))
                continue
            # store form: mov [rip -> slot], rX
            if ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_REG \
                    and ops[0].mem.base == X86_REG_RIP and not ops[0].mem.index \
                    and ins.address + ins.size + ops[0].mem.disp == slot:
                held.add(rn(ops[1].reg))
                continue

        for oi, op in enumerate(ops):
            if op.type != X86_OP_MEM or not op.mem.base or op.mem.base == X86_REG_RIP:
                continue
            if op.mem.index:
                continue
            if rn(op.mem.base) not in held:
                continue
            d = op.mem.disp - off
            if 0 <= d < size:
                rows.append((fn, names.get(fn, ""), ins.address, d,
                             RT.op_kind(ins, op, oi),
                             mn + " " + ins.op_str))

        if mn == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and ops[1].type == X86_OP_REG:
            s, d = rn(ops[1].reg), rn(ops[0].reg)
            if s in held:
                held.add(d)
                if d in ARGREG:
                    pend[d] = True
            else:
                held.discard(d)
                pend.pop(d, None)
            continue

        if ins.group(CS_GRP_CALL):
            if call_out is not None and ops and ops[0].type == X86_OP_IMM:
                for a in list(pend):
                    call_out.add((ops[0].imm, ARGREG.index(a)))
            held -= VOLATILE
            pend.clear()
            # THE `FN 0xADDR +0xOFF` ROUTE. The instance is not parked in a global at all - it is
            # whatever an accessor RETURNS. `SavePayload` is `FN 0x002EF640+0x200`, so the base
            # arrives in rax and every field sits at `rax + 0x200 + disp`. The seed therefore
            # happens AFTER the volatile drop above, because this call is precisely what puts the
            # value in rax.
            if fn_addr is not None and ops and ops[0].type == X86_OP_IMM \
                    and ops[0].imm == fn_addr:
                held.add("rax")
            continue

        # THE WRITE SET, NOT OPERAND ZERO - see reg_tracking.py. `test rbx, rbx` writes only
        # rflags, and dropping the base there stops tracking at the null check that precedes
        # every real access to a singleton.
        for r0 in RT.written(ins):
            held.discard(r0)
            pend.pop(r0, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True)
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--out")
    a = ap.parse_args()

    addr, off, size, mode = route_for(a.type, a.db)
    if addr is None or not size:
        print("no PTR or FN route with a size for %s" % a.type)
        return 2
    raw, tva, tvs, tpr = load_text()
    blob = raw[tpr:tpr + tvs]
    sizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    rows = []
    callees = set()
    # PASS 1
    for fn in sorted(sizes):
        b = body(blob, tva, sizes, fn)
        if not b:
            continue
        try:
            il = list(md.disasm(b, fn))
        except Exception:
            continue
        # ONE walk per body, seeding itself on every load AND every store of the slot. The
        # earlier shape here - collect load registers, then re-walk from the first load of each -
        # missed the store form entirely and so missed every body that CONSTRUCTS the singleton.
        walk(md, il, set(), size, off, rows, fn, names, callees,
             slot=(addr if mode == 'PTR' else None),
             fn_addr=(addr if mode == 'FN' else None))

    direct = len({(r[2], r[3]) for r in rows})
    print("%s: %s %08X +0x%X, size 0x%X" % (a.type, mode, addr, off, size))
    print("  PASS 1 (same function)      : %d access(es) at %d offset(s)"
          % (direct, len({r[3] for r in rows})))
    print("  PASS 2 callee/arg pairs     : %d" % len(callees))

    # PASS 2
    before = len(rows)
    for callee, argi in sorted(callees):
        if callee not in sizes:
            continue
        b = body(blob, tva, sizes, callee)
        if not b:
            continue
        try:
            il = list(md.disasm(b, callee))
        except Exception:
            continue
        walk(md, il, {ARGREG[argi]}, size, off, rows, callee, names, None)
    print("  PASS 2 added                : %d raw access row(s)" % (len(rows) - before))

    seen, out = set(), []
    for x in rows:
        k = (x[2], x[3])
        if k not in seen:
            seen.add(k)
            out.append(x)
    out.sort(key=lambda x: (x[3], x[2]))
    kinds = collections.Counter(x[4] for x in out)
    offs = sorted({x[3] for x in out})
    print()
    print("  TOTAL: %d distinct access(es) at %d distinct offset(s)  (%s)"
          % (len(out), len(offs), ", ".join("%s %d" % kv for kv in sorted(kinds.items()))))
    print("  functions contributing: %d" % len({x[0] for x in out}))
    for fn, nm, site, d, kind, txt in out[:20]:
        print("    +0x%-5X %08X in %08X %-4s %s" % (d, site, fn, kind, txt[:52]))
    if len(out) > 20:
        print("    ... %d more" % (len(out) - 20))

    if a.out and out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
            for fn, nm, site, d, kind, txt in out:
                fh.write("%08X\t%s\t%08X\t0x%X\t%s\t%s\tptr-depth1 %08X+0x%X\t\n"
                         % (fn, nm, site, d, kind, txt, addr, off))
        print("  wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
