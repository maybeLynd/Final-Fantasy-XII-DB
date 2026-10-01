#!/usr/bin/env python3
"""Does a STATIC route's extent actually hold the object, or only a pointer to it?

THE DEFECT THIS EXISTS TO CATCH. `STATIC 0xADDR` in the route grammar means "one instance at a
fixed address", and `gen_static_census.py` consumes it by reading `size` bytes there. `PTR 0xADDR`
means the instance is at `*(ADDR)`. Get the two confused and a generator censuses the wrong memory
- for a heap singleton whose slot sits in the .bss tail it censuses zeros and reports the type as
empty, with nothing in the output to say the base was wrong.

THE DISCRIMINATOR IS MECHANICAL, NOT LEXICAL. Three lexical selectors for semantic classes were
built here on 2026-09-19 and all three failed their controls (1/7, 0/3, 1/2), so this reads
instructions:

  * a real STATIC object is touched at INTERIOR displacements - ADDR+4, ADDR+0x20, ... - and at
    mixed widths, because a struct has fields of different sizes;
  * a pointer slot is touched at ADDR ONLY and always 8 bytes wide, because the only thing anyone
    does with it is load it, compare it against zero and store the allocation back.

TWO CONTROLS, both required to fire or the output is discarded:
  * STATIC positive - Mt19937State (0x02EB3870, 0x9C4). A Mersenne Twister state is a 624-word
    array walked by index; it MUST show interior targets.
  * PTR positive - ManagerSingleton0209BE80 (0x0209BE80). It MUST show the slot only, at width 8.

AND A WARNING THIS TOOL EARNED ON ITS FIRST RUN. Both controls passed and the verdict for
EffectPresetSingleton01F82C80 was still WRONG - reported OBJECT SHAPE on 185 targets, when the row
is a heap singleton whose slot holds nothing but a pointer. The cause was not the discriminator; it
was the WINDOW. A STATIC route's extent is `addr .. addr+size`, and if the row's base is wrong that
extent is an arbitrary stretch of memory, so every unrelated global inside it counts as `interior`
and manufactures the OBJECT verdict. GameSettingConfig's own route address 0x01F82D20 lay 0xA0
bytes inside the claimed 0xF778 extent.

  >> A CONTROL TESTS THE DISCRIMINATOR. IT DOES NOT TEST THE WINDOW THE DISCRIMINATOR IS APPLIED
  >> TO. For a row whose base is in doubt, the extent derived from that base is in doubt with it,
  >> and the evidence it gathers is circular.

Hence `other routes in extent`: any STATIC extent containing another declared route address is not
a credible extent, and the verdict for that row is withheld rather than reported.

WHAT THIS SWEEP CANNOT SEE, stated so `NOT NAMED BY ANY INSTRUCTION` is not misread as unused. It
finds RIP-relative operands and the image-base-relative idiom. It does NOT find an object reached
through a root pointer already in a register. RenderModelInstanceContainer is the worked example:
both its route addresses score zero here and BOTH ARE CORRECT - it is embedded at +0xF0 of the
static render resource root 022C6F30 and cached at root+0xDA0, and 0041E3A0 does exactly
`lea rax,[rsi+0xF0]` / `mov [rsi+0xDA0], rax` with the root in rsi. The root itself IS named, by
`lea` in six functions. So a zero here is a statement about this instrument's reach and nothing
else, and an embedded or chained object should be expected to score zero.

usage: check_static_vs_ptr_routes.py [--src <db root>]
"""
import collections
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402

import capstone  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_REG_RIP  # noqa: E402

SRC = G.DB
if "--src" in sys.argv:
    SRC = sys.argv[sys.argv.index("--src") + 1]

CONTROL_STATIC = "Mt19937State"
# keyed by INSTANCE, not by type name (2026-09-27, OPUS): Mt19937State gained a second static route (01F7F600), and a
# name-keyed verdict let that window overwrite the control's own 02EB3870 - the control failed and the whole table was
# discarded although the discriminator still separated the known cases
CONTROL_STATIC_ADDR = 0x02EB3870
CONTROL_PTR = "ManagerSingleton0209BE80"


def parse_routes(path):
    rows = list(csv.reader(io.open(path, encoding="utf-8", newline=""), delimiter="\t"))
    h = rows[0]
    iR, iT, iS = h.index("route"), h.index("type"), h.index("size")
    out = []
    for r in rows[1:]:
        route = (r[iR] or "").strip()
        if not route:
            continue
        for alt in route.split("|"):
            p = alt.split()
            if not p or p[0] not in ("STATIC", "PTR"):
                continue
            if "+" in p[1]:                      # PTR 0xADDR+0xOFF - the slot is still p[1] head
                addr = int(p[1].split("+")[0], 16)
            else:
                addr = int(p[1], 16)
            try:
                size = int(r[iS], 16) if r[iS].lower().startswith("0x") else None
            except ValueError:
                size = None
            out.append((r[iT], p[0], addr, size))
    return out


def main():
    types_tsv = os.path.join(SRC, "_types", "types.tsv")
    routes = parse_routes(types_tsv)
    d, base, secs = G.load_pe(G.EXE)

    # one window per route: STATIC gets its whole declared extent, PTR gets 8 bytes at the slot
    windows = []
    for name, kind, addr, size in routes:
        hi = addr + (size if (kind == "STATIC" and size) else 8)
        windows.append((name, kind, addr, size, hi))

    funcs = []
    f = io.open(G.FUNCS, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.split("\t")
        try:
            sz = int(p[2])
            if 0 < sz <= 0x20000:
                funcs.append((int(p[0], 16), sz))
        except (ValueError, IndexError):
            pass

    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    # target -> (widths, funcs)
    tgt_w = collections.defaultdict(set)
    tgt_f = collections.defaultdict(set)
    lo_all = min(w[2] for w in windows)
    hi_all = max(w[4] for w in windows)

    for entry, size in funcs:
        r = entry - base
        blob = None
        for nm, sva, vs, ra, rs in secs:
            if nm == ".text" and sva <= r < sva + max(vs, rs):
                o = r - sva
                if o < rs:
                    blob = d[ra + o: ra + o + size]
                break
        if not blob:
            continue
        holders = set()
        for i in md.disasm(blob, entry):
            if i.mnemonic == "lea" and len(i.operands) == 2:
                dst, src = i.operands
                if (src.type == X86_OP_MEM and src.value.mem.base == X86_REG_RIP
                        and i.address + i.size + src.value.mem.disp == base):
                    holders.add(dst.value.reg)
                    continue
            if holders:
                _rd, wr = i.regs_access()
                holders -= set(wr)
            for o in i.operands:
                if o.type != X86_OP_MEM:
                    continue
                tgt = None
                if o.value.mem.base == X86_REG_RIP:
                    tgt = i.address + i.size + o.value.mem.disp
                elif holders and o.value.mem.base in holders and o.value.mem.disp:
                    tgt = base + o.value.mem.disp
                if tgt is not None and lo_all <= tgt < hi_all:
                    tgt_w[tgt].add(o.size)
                    tgt_f[tgt].add(entry)

    print("routes examined: %d  (%d STATIC, %d PTR)"
          % (len(windows), sum(1 for w in windows if w[1] == "STATIC"),
             sum(1 for w in windows if w[1] == "PTR")))
    print()
    verdicts = {}
    rowsout = []
    for name, kind, addr, size, hi in sorted(windows, key=lambda w: (w[1], w[0])):
        tgts = sorted(t for t in tgt_w if addr <= t < hi)
        interior = [t for t in tgts if t != addr]
        widths = set()
        for t in tgts:
            widths |= tgt_w[t]
        at_slot = sorted(tgt_w.get(addr, ()))
        # a SCALAR static is one target at the base whose width IS the declared size - it has no
        # interior to show and it is not a pointer slot, so neither of the two main tests applies
        scalar = (kind == "STATIC" and size and size <= 8 and tgts == [addr]
                  and at_slot == [size])
        shape = ("SCALAR STATIC" if scalar
                 else "POINTER-SLOT SHAPE" if (tgts and not interior and at_slot == [8])
                 else "OBJECT SHAPE" if interior
                 else "NOT NAMED BY ANY INSTRUCTION" if not tgts
                 else "MIXED")
        verdicts[(name, addr)] = shape
        rowsout.append((kind, name, addr, len(tgts), len(interior),
                        sorted(widths), shape))

    all_route_addrs = sorted({w[2] for w in windows})
    print("%-7s %-40s %-10s %6s %8s %7s  %-14s %s"
          % ("route", "type", "addr", "tgts", "interior", "others", "widths", "shape"))
    for kind, name, addr, nt, ni, ws, shape in rowsout:
        hi = addr + (dict((w[0], w[3]) for w in windows).get(name) or 8)
        others = sum(1 for a in all_route_addrs if addr < a < hi)
        flag = ""
        if kind == "STATIC" and others:
            shape = "EXTENT NOT CREDIBLE"
            verdicts[(name, addr)] = shape
            flag = ("   <<< %d OTHER ROUTE ADDRESS(ES) INSIDE THE EXTENT - verdict withheld, the "
                    "base is in doubt" % others)
        elif kind == "STATIC" and shape == "POINTER-SLOT SHAPE":
            flag = "   <<< ROUTE SAYS STATIC, BYTES SAY PTR"
        elif kind == "PTR" and shape == "OBJECT SHAPE":
            flag = "   <<< ROUTE SAYS PTR, BYTES SAY STATIC"
        print("%-7s %-40s %08X %6d %8d %7d  %-14s %s%s"
              % (kind, name, addr, nt, ni, others,
                 ",".join(str(w) for w in ws), shape, flag))

    print()
    cs = verdicts.get((CONTROL_STATIC, CONTROL_STATIC_ADDR))
    cp = next((v for (n, a), v in sorted(verdicts.items()) if n == CONTROL_PTR), None)
    ok_s = cs == "OBJECT SHAPE"
    ok_p = cp == "POINTER-SLOT SHAPE"
    print("CONTROL  %-40s expect OBJECT SHAPE       got %-20s %s"
          % (CONTROL_STATIC, cs, "PASS" if ok_s else "FAIL"))
    print("CONTROL  %-40s expect POINTER-SLOT SHAPE got %-20s %s"
          % (CONTROL_PTR, cp, "PASS" if ok_p else "FAIL"))
    if not (ok_s and ok_p):
        print()
        print("A CONTROL FAILED -> THE TABLE ABOVE IS DISCARDED. The discriminator has not shown")
        print("it can separate the two shapes on cases whose answer is already known, so it says")
        print("nothing about the cases whose answer is not.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
