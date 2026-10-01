#!/usr/bin/env python3
"""check_bulk_write_lifetime.py - is a type cleared wholesale, and does every span know it?

WHY THIS EXISTS, AND WHY IT IS THE RIGHT SHAPE. `check_span_propagation.py` searches a type's own
page for a span's OFFSET. That finds offset-keyed prose and nothing else, and the miss it produced
is instructive: `BattleUnit` flagged two spans, because two are named in a sentence, while the
actual fact - **the whole 0xF50 unit is memset to zero on both allocate and release** - is about
the OBJECT and mentions no offset at all. It covers all thirty of that type's spans.

A lifetime fact is a property of the type, so the instrument should be too.

METHOD. Every call to `memset` (`00861EC0`) or `memcpy` (`00861EBA`) in a listed body is found, and
the length argument recovered when it is a literal - `mov r8d, imm` in the Win64 third slot, taken
from the nearest preceding setter that is not clobbered. Each length is then matched against the
declared `size` of every type in the store.

TWO TIERS, because a size match is not an attribution:

  ATTRIBUTED - the destination register `rcx` is traced, in the same body, back to the type's own
      route root: a load or store of its `PTR` slot, a `lea` of its `ARRAY`/`STATIC` base, or a
      `lea` of its `EMBED` offset from a parent that was itself traced. This is evidence.

  SIZE MATCH ONLY - the length equals the type's extent but `rcx` could not be tied to it. This is
      a candidate for a human, nothing more. Sizes collide: several unrelated types share 0x100.

WHAT IT DOES NOT CLAIM. A clear proves the bytes have a defined VALUE from that point; it says
nothing about meaning, and no field may be declared from it. A length computed at runtime is
invisible here, so a type reported as never cleared may still be cleared by a variable-length copy
- the `CharacterRenderObject` argument only holds because a literal sweep is exhaustive for THAT
object's 0x668, which was checked separately.

    python check_bulk_write_lifetime.py
    python check_bulk_write_lifetime.py --type BattleUnit
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
BULK = {0x00861EC0: "memset", 0x00861EBA: "memcpy"}
VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
R_PTR = re.compile(r"^PTR\s+(0x[0-9A-Fa-f]+)")
R_BASE = re.compile(r"^(?:ARRAY|STATIC|PARRAY|SLOTPTR)\s+(0x[0-9A-Fa-f]+)")
R_FN = re.compile(r"^FN\s+(0x[0-9A-Fa-f]+)")
SPAN = re.compile(r"^(unobserved|unread)", re.I)


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--type", default=None)
    a = ap.parse_args()

    sizes_of, roots_of = {}, {}
    fn_accessors = set()
    with io.open(os.path.join(a.db, "_types", "types.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if not f or not f[0]:
                continue
            try:
                sz = int(f[1], 0)
            except ValueError:
                continue
            sizes_of[f[0]] = sz
            roots = set()
            for alt in (f[12] if len(f) > 12 else "").split("|"):
                m = R_PTR.match(alt.strip()) or R_BASE.match(alt.strip())
                if m:
                    roots.add(int(m.group(1), 16))
                    continue
                # THE THIRD SEEDING MODE. `PersistentFlagPayload` is `FN 0x002EF640+0x200`
                # and its clear is `call 002EF640` / `lea rcx,[rax+0x200]` / memset - the
                # destination is a CALL RETURN, which neither rip-relative rooting nor
                # parameter seeding can see. The accessor address is the root.
                m = R_FN.match(alt.strip())
                if m:
                    addr = int(m.group(1), 16)
                    roots.add(addr)
                    fn_accessors.add(addr)
            roots_of[f[0]] = roots
    by_size = collections.defaultdict(list)
    for t, s in sizes_of.items():
        by_size[s].append(t)

    spans = collections.defaultdict(list)
    with io.open(os.path.join(a.db, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) >= 9 and SPAN.match(f[3]):
                spans[f[0]].append((f[1], int(f[2]), f[8]))

    raw, tva, tvs, tpr = load_text()
    blob = raw[tpr:tpr + tvs]
    fsizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    ARGREG = ["rcx", "rdx", "r8", "r9"]

    def scan_body(il, fn, found, pre_rooted=None, handoffs=None):
        """One body. `pre_rooted` maps a parameter register to the route it holds on entry."""
        r8 = None                    # last literal placed in r8d/r8
        rooted = dict(pre_rooted or {})
        pend = dict((r, a) for r, a in rooted.items() if r in ARGREG)
        for ins in il:
            rn, ops, mn = ins.reg_name, ins.operands, ins.mnemonic
            # EVERY SEEDING BRANCH MUST `continue`. The clobber loop at the bottom uses
            # RT.written(), which correctly reports that `mov r8d, 0xf50` WRITES r8 - so without
            # the continue it erased the literal on the very instruction that set it, and the
            # scan reported zero bulk writes in an image that contains at least four. The control
            # for that was knowing the BattleUnit pair existed before the tool was run.
            if (mn == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG
                    and ops[1].type == X86_OP_IMM
                    and rn(ops[0].reg) in ("r8d", "r8")):
                r8 = ops[1].imm
                continue
            # route roots: a rip-relative load/store of a slot, or a lea of a base
            if (len(ops) == 2 and ops[1].type == X86_OP_MEM
                    and ops[1].mem.base == X86_REG_RIP and not ops[1].mem.index
                    and ops[0].type == X86_OP_REG and mn in ("mov", "lea")):
                d = rn(ops[0].reg)
                rooted[d] = ins.address + ins.size + ops[1].mem.disp
                if d in ARGREG:
                    pend[d] = rooted[d]
                continue
            if (len(ops) == 2 and ops[0].type == X86_OP_MEM
                    and ops[0].mem.base == X86_REG_RIP and not ops[0].mem.index
                    and ops[1].type == X86_OP_REG and mn == "mov"):
                rooted[rn(ops[1].reg)] = ins.address + ins.size + ops[0].mem.disp
                continue
            if (mn == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG
                    and ops[1].type == X86_OP_REG):
                s_, d = rn(ops[1].reg), rn(ops[0].reg)
                if s_ in rooted:
                    rooted[d] = rooted[s_]
                    if d in ARGREG:
                        pend[d] = rooted[d]
                else:
                    rooted.pop(d, None)
                    pend.pop(d, None)
                continue

            # lea rY, [rX + imm] carries the root: the FN form reaches its object that way.
            if (mn == "lea" and len(ops) == 2 and ops[0].type == X86_OP_REG
                    and ops[1].type == X86_OP_MEM and ops[1].mem.base
                    and ops[1].mem.base != X86_REG_RIP and not ops[1].mem.index):
                src = rn(ops[1].mem.base)
                d = rn(ops[0].reg)
                if src in rooted:
                    rooted[d] = rooted[src]
                    if d in ARGREG:
                        pend[d] = rooted[d]
                else:
                    rooted.pop(d, None)
                    pend.pop(d, None)
                continue

            if ins.group(CS_GRP_CALL):
                if ops and ops[0].type == X86_OP_IMM and ops[0].imm in BULK and r8:
                    found[r8].append((fn, ins.address, BULK[ops[0].imm], rooted.get("rcx")))
                # PARAMETER SEEDING, the fix that made the EMBED census work. A destination that
                # arrives as an argument is invisible to a body-local root, and rcx at a memset
                # is usually exactly that. Record which callee receives the object in which slot.
                elif handoffs is not None and ops and ops[0].type == X86_OP_IMM:
                    for areg, addr in pend.items():
                        handoffs.add((ops[0].imm, ARGREG.index(areg), addr))
                for v in list(rooted):
                    if v in VOLATILE:
                        del rooted[v]
                pend.clear()
                r8 = None
                # the accessor's RETURN VALUE is the object; seed after the volatile drop
                if ops and ops[0].type == X86_OP_IMM and ops[0].imm in fn_accessors:
                    rooted["rax"] = ops[0].imm
                continue
            for w in RT.written(ins):
                rooted.pop(w, None)
                pend.pop(w, None)
                if w in ("r8",):
                    r8 = None

    def body_il(fn):
        o = fn - tva
        if o < 0 or o >= len(blob):
            return None
        b = blob[o:o + fsizes.get(fn, 0)]
        if not b:
            return None
        try:
            return list(md.disasm(b, fn))
        except Exception:
            return None

    found = collections.defaultdict(list)     # size -> [(fn, site, kind, rootaddr or None)]
    handoffs = set()                          # (callee, arg index, route address)
    for fn in sorted(fsizes):
        il = body_il(fn)
        if il:
            scan_body(il, fn, found, None, handoffs)
    print("bodies that pass a route-rooted object into a call: %d handoff(s)" % len(handoffs))

    # PASS 2 - re-scan each receiving callee with that parameter pre-rooted
    seen_pairs = set()
    for callee, argi, addr in sorted(handoffs):
        if (callee, argi, addr) in seen_pairs or callee not in fsizes:
            continue
        seen_pairs.add((callee, argi, addr))
        il = body_il(callee)
        if il:
            scan_body(il, callee, found, {ARGREG[argi]: addr}, None)
    tot = sum(len(v) for v in found.values())
    print("bulk-write calls with a literal length: %d, over %d distinct length(s)"
          % (tot, len(found)))

    rows = []
    for sz, sites in found.items():
        for t in by_size.get(sz, []):
            if a.type and t != a.type:
                continue
            att = [s for s in sites if s[3] is not None and s[3] in roots_of.get(t, ())]
            rows.append((t, sz, sites, att))
    rows.sort(key=lambda x: -(sum(b for _, b, _ in spans.get(x[0], [])) or 0))

    print()
    print("TYPES whose declared size equals a literal bulk-write length: %d" % len(rows))
    print()
    print("%-30s %8s %6s %5s %7s  %s" % ("type", "size", "sites", "attr", "spanB", "verdict"))
    for t, sz, sites, att in rows:
        sb = sum(b for _, b, _ in spans.get(t, []))
        already = sum(1 for _, _, ev in spans.get(t, []) if "LIFETIME" in ev)
        v = ("ATTRIBUTED" if att else "size match only")
        if spans.get(t) and already == len(spans[t]) and att:
            v += " (all spans already carry it)"
        elif att and spans.get(t):
            v += " -> %d of %d span rows LACK a lifetime note" % (len(spans[t]) - already,
                                                                  len(spans[t]))
        print("%-30s %8X %6d %5d %7d  %s" % (t[:30], sz, len(sites), len(att), sb, v))
        for fn, site, kind, root in (att or sites)[:3]:
            print("      %-6s at %08X in %08X %s"
                  % (kind, site, fn, ("root %08X" % root) if root else "rcx not traced"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
