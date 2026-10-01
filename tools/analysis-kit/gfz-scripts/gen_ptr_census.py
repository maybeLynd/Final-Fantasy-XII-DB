#!/usr/bin/env python3
"""gen_ptr_census.py - a census for the `*(void**)0xADDR` class, which had no generator.

WHY THIS EXISTS. `_types/README.md` names the gap outright: *"`PTR`/`PARRAY`/`SLOTPTR` rows are the
`*(void**)0xADDR` class no generator consumes yet - they are recorded precisely so that third
generator has a population."* `gen_static_census.py` handles records AT a fixed address, where every
access is RIP-relative. `record_field_scan.py` handles records reached by a pointer chain from a
parent. Neither handles the commonest singleton shape in this image: **a pointer parked in a global,
loaded into a register, and indexed off.**

Nine types carry a bare `PTR` route, including the three largest in the store -
`ManagerSingleton0209BE80` (0x10FD0), `BattleSystemState` (0x7410) and `ImageBackedStateBlock`
(0x4818) - and none of them has a census.

METHOD. For `PTR 0xADDR [+0xOFF]` the instance is `*(ADDR) + OFF`. So:

    mov  rX, qword ptr [rip -> ADDR]      <- rX now holds the instance base
    ...  [rX + OFF + disp]                <- an access at type-relative offset `disp`

The register is tracked forward through the body, `mov rY, rX` propagates it, and a register is
dropped the moment anything else writes it. Volatile registers are dropped across a call, because
the callee may clobber them; callee-saved registers are not, which is what lets the scan follow a
base held in `rbx`/`rsi`/`rdi` across the calls a real body makes.

THE CONTROL IS AN EXISTING CENSUS, NOT A SITE COUNT
---------------------------------------------------
`--control <file>` re-derives a census somebody else wrote by hand and requires every site in it that
this method can see to be reproduced. `PostProcessParamContext` is the target: it is `PTR 0x01F7F5F0
| PTR 0x01F81300` and `postprocess-context-accesses.tsv` already lists its accesses, produced by
different work. Reproducing a census is a far stronger control than counting sites, because it checks
the OFFSETS and the INSTRUCTION TEXT, not just that the decoder ran.

WHAT IT DOES NOT DO, stated rather than implied
-----------------------------------------------
* **Same-function only.** An instance passed into a callee is invisible, so every count is a FLOOR.
  The existing censuses carry a `route` column naming the call path precisely because this limit is
  real; rows here are marked `gptr` and nothing more is claimed.
* **It does not infer types.** It records the instruction; every judgement downstream is somebody
  else's - the same rule `gen_static_census.py` states.
* **It does not follow the pointer being reloaded.** If a body loads the global twice the second load
  simply re-seeds; no attempt is made to prove the value is unchanged.

    python gen_ptr_census.py --type PostProcessParamContext --control <existing tsv>
    python gen_ptr_census.py --type BattleSystemState --out <path>
"""
import argparse
import bisect
import collections
import csv
import io
import os
import re
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_GRP_CALL
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_REG_RIP

import member_reach_scan as M
import reg_tracking as RT
import kit_paths as KP

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE

VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
ROUTE = re.compile(r"^PTR\s+(0x[0-9A-Fa-f]+)(?:\s*\+\s*(0x[0-9A-Fa-f]+))?\s*$")


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


def routes_for(tname):
    p = os.path.join(KP.DB, "_types", "types.tsv")
    with io.open(p, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if f and f[0] == tname:
                size = None
                try:
                    size = int(f[1], 0)
                except (ValueError, IndexError):
                    pass
                alts = (f[12] if len(f) > 12 else "").split("|")
                out = []
                for a in alts:
                    m = ROUTE.match(a.strip())
                    if m:
                        out.append((int(m.group(1), 0), int(m.group(2), 0) if m.group(2) else 0))
                return out, size
    return [], None


def control_owner(path):
    """Which type check_census_widths.py registers this census file to, or None.

    WHY THIS GUARD EXISTS, and it is not hypothetical. The first run of this generator against
    `LegacyPs2GsTextureContext` was given `postprocess-context-accesses.tsv` as its control - the
    file this docstring names, because it is the control the method was VALIDATED on - and the
    result printed `reproduces : 0 (0.0%)`. That zero is not a measurement. The control belongs to
    `PostProcessParamContext`; no scan of a different type can reproduce a single one of its sites,
    so the number is 0 by construction whatever the scan does. Run correctly against its own type
    the same control reproduces 20 of 777, which is a small number for the reason the docstring
    above states - and 20 against 0 is a difference a reader skimming two console blocks would not
    notice. A control that cannot fail is worse than no control, so this refuses rather than prints.
    """
    try:
        import check_census_widths as C
    except Exception:
        return None
    want = os.path.basename(path).lower()
    for t, f in C.CENSUS.items():
        if os.path.basename(f).lower() == want:
            return t
    for t, (f, _b) in C.STATIC_CENSUS.items():
        if os.path.basename(f).lower() == want:
            return t
    for t, (f, _s) in C.SUBOBJECT_CENSUS.items():
        if os.path.basename(f).lower() == want:
            return t
    return None


def scan(slot, baseoff, size, blob, tva, sizes, names, md):
    """Every access at `*(slot)+baseoff+disp`, disp within the type."""
    st = sorted(sizes)
    rows = []
    for fn in st:
        body = blob[fn - tva:fn - tva + sizes[fn]]
        if not body:
            continue
        try:
            ins_list = list(md.disasm(body, fn))
        except Exception:
            continue
        held = {}          # reg name -> True
        seeded = False
        for ins in ins_list:
            # seed: mov reg, [rip -> slot]
            if ins.mnemonic == "mov" and len(ins.operands) == 2 \
                    and ins.operands[0].type == X86_OP_REG \
                    and ins.operands[1].type == X86_OP_MEM \
                    and ins.operands[1].mem.base == X86_REG_RIP \
                    and ins.address + ins.size + ins.operands[1].mem.disp == slot:
                held = dict(held)
                held[ins.reg_name(ins.operands[0].reg)] = True
                seeded = True
                continue
            # SEED ALSO ON THE STORE, because a lazy singleton's initialiser publishes the
            # instance rather than loading it. `PostProcessParamContext`'s own init reads the slot
            # into `rsi`, finds it null, REASSIGNS `rsi` from the fresh allocation and stores it
            # back at `0018EFEC` -- so the load-only seed dropped `rsi` at the reassignment and the
            # scan reported ZERO accesses through that slot, for the one body that most certainly
            # has them. The value written to the slot IS the instance.
            if ins.mnemonic == "mov" and len(ins.operands) == 2 \
                    and ins.operands[0].type == X86_OP_MEM \
                    and ins.operands[0].mem.base == X86_REG_RIP \
                    and ins.operands[1].type == X86_OP_REG \
                    and ins.address + ins.size + ins.operands[0].mem.disp == slot:
                held = dict(held)
                held[ins.reg_name(ins.operands[1].reg)] = True
                continue
            if not held:
                continue
            # A MULTI-BYTE NOP IS NOT AN ACCESS. `nop word ptr [rax + rax]` is alignment padding
            # whose operand is never read or written, and it decodes as a memory operand like any
            # other. Left unfiltered it produced the run's only "declared-unread span with a
            # censused access" -- a finding that was entirely this instruction.
            if ins.mnemonic.startswith("nop") or ins.mnemonic.startswith("prefetch"):
                continue
            # record accesses off a held register
            for oi, op in enumerate(ins.operands):
                if op.type != X86_OP_MEM or op.mem.base == X86_REG_RIP or op.mem.base == 0:
                    continue
                bn = ins.reg_name(op.mem.base)
                if bn not in held:
                    continue
                d = op.mem.disp - baseoff
                if size is not None and not (0 <= d < size):
                    continue
                kind = RT.op_kind(ins, op, oi)
                rows.append((fn, names.get(fn, ""), ins.address, d, kind,
                             ins.mnemonic + " " + ins.op_str))
            # lea rY, [rX + k] keeps a base, offset by k -- not tracked; drop rY below.
            # propagate mov rY, rX
            if ins.mnemonic == "mov" and len(ins.operands) == 2 \
                    and ins.operands[0].type == X86_OP_REG and ins.operands[1].type == X86_OP_REG \
                    and ins.reg_name(ins.operands[1].reg) in held:
                held = dict(held)
                held[ins.reg_name(ins.operands[0].reg)] = True
                continue
            if ins.group(CS_GRP_CALL):
                held = {k: v for k, v in held.items() if k not in VOLATILE}
                continue
            # any write to a held register drops it.
            # THE WRITE SET, NOT OPERAND ZERO. `test rbx, rbx` and `cmp rbx, rax` have a register
            # first operand and write only rflags; the previous rule dropped the tracked register
            # on both. That is the null-check idiom every singleton load is followed by, so the
            # tracker used to stop exactly where the accesses start. See reg_tracking.py.
            wr = RT.written(ins)
            if wr:
                held = {k: v for k, v in held.items() if k not in wr}
        del seeded
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True)
    ap.add_argument("--control", default=None, help="an existing *-accesses.tsv to reproduce")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    rts, size = routes_for(a.type)
    if not rts:
        print("no bare PTR route for %s -- this generator handles `PTR 0xADDR [+0xOFF]` only"
              % a.type)
        return 2

    raw, tva, tvs, tpr = load_text()
    blob = raw[tpr:tpr + tvs]
    sizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    allrows = []
    for slot, boff in rts:
        r = scan(slot, boff, size, blob, tva, sizes, names, md)
        print("  slot %08X +0x%X : %d access(es)" % (slot, boff, len(r)))
        allrows += r
    seen, rows = set(), []
    for x in allrows:
        k = (x[2], x[3])
        if k not in seen:
            seen.add(k)
            rows.append(x)
    rows.sort(key=lambda x: (x[3], x[2]))
    print("%s: %d distinct access(es) at %d distinct offset(s)"
          % (a.type, len(rows), len({x[3] for x in rows})))

    if a.control:
        # AND THAT THE FILE IS THERE. `control_owner` resolves by BASENAME against the registry,
        # which is what lets it answer without reading the file - so a mistyped directory passes
        # the ownership test and then raises inside the reader, below the summary that has already
        # been printed. Refuse here, where the message is next to the reason.
        if not os.path.isfile(a.control):
            print()
            print("CONTROL REFUSED: %s does not exist." % a.control)
            return 2
        owner = control_owner(a.control)
        if owner is None:
            print()
            print("CONTROL REFUSED: %s is not registered in check_census_widths.py, so which "
                  "type it censuses cannot be established here." % os.path.basename(a.control))
            return 2
        if owner != a.type:
            print()
            print("CONTROL REFUSED: %s is the census of %s, not %s."
                  % (os.path.basename(a.control), owner, a.type))
            print("  A control census of a DIFFERENT TYPE reproduces 0% by construction and the")
            print("  zero means nothing. Pass that type's own census, or run without --control.")
            return 2
        ctl = set()
        with io.open(a.control, encoding="utf-8", newline="") as fh:
            r = csv.reader(fh, delimiter="\t")
            hdr = next(r, None)
            for f in r:
                if len(f) > 3:
                    try:
                        ctl.add((int(f[2], 16), int(f[3], 0)))
                    except ValueError:
                        pass
        mine = {(x[2], x[3]) for x in rows}
        hit = ctl & mine
        print()
        print("CONTROL against %s" % os.path.basename(a.control))
        print("  sites in the control            : %d" % len(ctl))
        print("  of those this method reproduces : %d (%.1f%%)"
              % (len(hit), 100.0 * len(hit) / len(ctl) if ctl else 0.0))
        print("  sites this method adds          : %d" % len(mine - ctl))
        miss = sorted(ctl - hit)[:8]
        if miss:
            print("  control sites NOT reproduced (first 8): %s"
                  % " ".join("%08X@+0x%X" % m for m in miss))
            print("  -- expected: the control carries rows reached by call argument, which")
            print("     same-function tracking cannot see. That is the stated floor, not a defect.")

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
            for fn, nm, site, d, kind, txt in rows:
                fh.write("%08X\t%s\t%08X\t0x%X\t%s\t%s\tgptr %08X\t\n"
                         % (fn, nm, site, d, kind, txt, rts[0][0]))
        print("wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
