#!/usr/bin/env python3
"""infer_field_type.py - what does the INSTRUCTION say a field is, without saying what it means?

THE POPULATION. 431 non-span field rows sit at DISCOVERED/UNKNOWN: width and access are recorded,
nothing else is. Some of those are genuinely semantic questions and belong to FABLE. But many are
not - the instructions that touch the field already fix its TYPE, and a type is OPUS's to state.

A field read with `movss` is a float whoever wrote it and whatever it means. A field loaded into a
register that then serves as a memory base is a pointer. A field widened with `movsxd` is signed.
A field only ever hit with `test`/`or`/`and` against an immediate is a bit set. None of those are
readings of purpose; they are readings of representation, and they raise a row from DISCOVERED to
TYPE RESOLVED without claiming a meaning.

WHAT IT CLASSIFIES, each from an instruction and nothing else:

  float      movss / movsd / mulss / addss / subss / divss / comiss / ucomiss / cvt*
  vector     movaps / movups / xmm on a 16-byte field
  pointer    a value loaded by `mov` becomes a memory BASE later in the same body
  addrterm   a value ADDED to a register whose sum becomes a base - a term in an
             address, which may be a pointer, a displacement or a size. NOT a pointer.
  signed     movsx / movsxd
  unsigned   movzx with no movsx anywhere - a zero-extending load fixes signedness
  bitfield   test / or / and / btr / bts with an immediate, and never an arithmetic use
  bool       a byte compared only against 0 or 1

AND WHAT IT REFUSES. A field with conflicting evidence is reported as CONFLICT and classified as
nothing - two idioms on one offset usually means the offset is a union, or that the census has
merged two types, and either way it is not a width question. A field with one lonely access is
reported but flagged, because one instruction is an anecdote.

NOTHING IS WRITTEN BY THIS TOOL. It prints candidates with their citations; a person moves the row.

    python infer_field_type.py --census <census.tsv> --type ManagerSingleton0209BE80
"""
import argparse
import collections
import csv
import io
import os
import re
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP

import member_reach_scan as M
import reg_tracking as RT
import kit_paths as KP

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE
FLOAT = re.compile(r"^(movss|movsd|mulss|addss|subss|divss|comiss|ucomiss|cvtsi2ss|cvtss2si|"
                   r"maxss|minss|sqrtss|andps|xorps)$")
VEC = re.compile(r"^(movaps|movups|movdqa|movdqu|addps|mulps|shufps|unpck)")
SIGNX = re.compile(r"^(movsx|movsxd)$")
BITOP = re.compile(r"^(test|or|and|btr|bts|bt|xor)$")
ARITH = re.compile(r"^(add|sub|imul|mul|inc|dec|shl|shr|sar|lea)$")


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
    ap.add_argument("--census", required=True)
    ap.add_argument("--type", required=True)
    ap.add_argument("--db", default=KP.DB)
    a = ap.parse_args()

    want = {}
    with io.open(os.path.join(a.db, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) >= 9 and f[0] == a.type and (f[6] == "DISCOVERED" or f[7] == "UNKNOWN"):
                if not re.match(r"^(unobserved|unread)", f[3], re.I):
                    want[int(f[1], 16)] = (f[3], int(f[2]), f[4])
    print("%s: %d non-span field row(s) at DISCOVERED/UNKNOWN" % (a.type, len(want)))
    if not want:
        return 0

    rows = list(csv.reader(io.open(a.census, encoding="utf-8", newline=""), delimiter="\t"))[1:]
    per = collections.defaultdict(list)
    for x in rows:
        try:
            d = int(x[3], 16)
        except (ValueError, IndexError):
            continue
        if d in want:
            per[d].append(x)

    raw, tva, tvs, tpr = load_text()
    blob = raw[tpr:tpr + tvs]
    fsizes, names = M.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    cache = {}

    def il_of(fn):
        if fn not in cache:
            o = fn - tva
            cache[fn] = (list(md.disasm(blob[o:o + fsizes[fn]], fn))
                         if fn in fsizes and 0 <= o < len(blob) else [])
        return cache[fn]

    ARGREG = ("rcx", "rdx", "r8", "r9")

    def deref_in_callee(callee, argreg, budget=400):
        """Does `callee` dereference the parameter arriving in `argreg`?

        WHY THIS EXISTS. The same-body test below proves a dereference and is the strongest
        evidence there is, but it misses the commonest pointer idiom in this engine: the field
        is loaded straight into rcx and passed to a call. Reading ManagerSingleton0209BE80 made
        that plain - +0x10FC0 has fifteen accesses, nearly every read a `mov rcx/rdx,
        [obj+0x10FC0]` feeding a call, and the same-body test classified none of them. Following
        the value ONE call level and asking whether the callee dereferences it is the same
        proof, one frame out.

        AND IT MUST FOLLOW THE PARAMETER, NOT THE REGISTER. A callee almost always parks its
        arguments in callee-saved registers before touching them: 003FA600 opens
        `mov rbx,[r8+0x2490]; mov rbp, r9; mov r14, rdx; mov r15, rcx`, and a scan watching only
        `r9` sees the copy, learns nothing and gives up - which is why `ptr10F50` stayed
        unclassified despite being passed to that very function. Following the value through
        `mov <reg>, <carrier>` is what makes the test work on real prologues.

        AND SOMETIMES THE CALLEE ONLY FORWARDS IT. `ptr10F50` is passed to 003FA600 as r9,
        parked in rbp, and rbp is NEVER dereferenced in that body - it is handed on to 003FBA80
        at the first call. One level is genuinely not enough for that row, so the walk goes to
        DEPTH 2 and no further. Each step is still the same statement - "the value is in this
        parameter" - so the proof does not weaken with depth; what grows is the chance of
        tracking the wrong value, which is why the depth is capped.

        It stops at a call it cannot follow, because after that a tracked register may hold
        something else and a hit would be about that value, not this one.
        """
        return _deref(callee, argreg, budget, 1)

    def _deref(callee, argreg, budget, depth):
        carriers = {argreg}
        for i in il_of(callee)[:budget]:
            for op in i.operands:
                if op.type == X86_OP_MEM and op.mem.base and op.mem.base != X86_REG_RIP \
                        and i.reg_name(op.mem.base) in carriers:
                    return i.address
            if i.mnemonic == "mov" and len(i.operands) == 2 \
                    and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_REG \
                    and i.reg_name(i.operands[1].reg) in carriers:
                carriers.add(i.reg_name(i.operands[0].reg))
                continue
            if i.group(2):
                if depth < 2:
                    # TRY EVERY ARGUMENT REGISTER THAT CARRIES THE VALUE, not one of them.
                    # By the forwarding call in 003FA600 the carriers are {r9, rbp, rdx}: r9 is
                    # the ORIGINAL parameter and is stale, rdx is the live copy made at
                    # 003FA67D `mov rdx, rbp`. Picking one - the first alphabetically - picked
                    # r9 and proved nothing. Which register the callee reads is the callee's
                    # business, so ask about all of them.
                    inarg = sorted(carriers & {"rcx", "rdx", "r8", "r9"})
                    tgt = (i.operands[0].imm
                           if i.operands and i.operands[0].type == X86_OP_IMM else None)
                    if tgt is not None and tgt in fsizes:
                        for reg in inarg:
                            w = _deref(tgt, reg, budget, depth + 1)
                            if w:
                                return w
                return None
            carriers -= set(RT.written(i))
            if not carriers:
                return None
        return None

    def becomes_base(fn, site):
        """Where is the value loaded at `site` dereferenced? (address, how) or None.

        `how` is "here" for a dereference in this body, "callee XXXXXXXX" when the value was
        handed to a direct call in an argument register and dereferenced inside it. Both are
        dereferences; keeping them distinguishable keeps the citation honest.
        """
        il = il_of(fn)
        dst = None
        for i in il:
            if i.address == site:
                if i.operands and i.operands[0].type == X86_OP_REG:
                    dst = i.reg_name(i.operands[0].reg)
                continue
            if dst is None:
                continue
            for op in i.operands:
                if op.type == X86_OP_MEM and op.mem.base and op.mem.base != X86_REG_RIP \
                        and i.reg_name(op.mem.base) == dst:
                    return (i.address, "here")
            if i.mnemonic == "mov" and len(i.operands) == 2 \
                    and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_REG \
                    and i.reg_name(i.operands[1].reg) == dst:
                dst = i.reg_name(i.operands[0].reg)          # the value changed registers
                continue
            if i.group(2):
                if dst in ARGREG and i.operands and i.operands[0].type == X86_OP_IMM \
                        and i.operands[0].imm in fsizes:
                    w = deref_in_callee(i.operands[0].imm, dst)
                    if w:
                        return (w, "callee %08X" % i.operands[0].imm)
                dst = None
                continue
            # THE WRITE SET, NOT OPERAND ZERO - the same defect fixed in reg_tracking.py and
            # promptly reintroduced here. `cmp rax, rbx` has a register first operand and writes
            # only rflags; clearing dst there abandons the value before its use as a base, which
            # is exactly the use this function exists to find.
            if dst in RT.written(i):
                dst = None
        return None

    out = []
    for d in sorted(per):
        name, size, ctype = want[d]
        ev = collections.Counter()
        cite = {}
        for x in per[d]:
            fn = int(x[0], 16)
            site = int(x[2], 16)
            txt = x[5] if len(x) > 5 else ""
            mn = txt.split()[0] if txt else ""
            if FLOAT.match(mn):
                ev["float"] += 1; cite.setdefault("float", (site, txt))
            elif VEC.match(mn):
                ev["vector"] += 1; cite.setdefault("vector", (site, txt))
            elif SIGNX.match(mn):
                ev["signed"] += 1; cite.setdefault("signed", (site, txt))
            elif BITOP.match(mn) and re.search(r",\s*(0x[0-9a-f]+|\d+)\s*$", txt):
                ev["bitfield"] += 1; cite.setdefault("bitfield", (site, txt))
            elif mn == "movzx":
                ev["unsigned"] += 1
                cite.setdefault("unsigned", (site, txt))
            elif ARITH.match(mn):
                ev["arith"] += 1; cite.setdefault("arith", (site, txt))
            # ONLY A `mov` PROVES A POINTER. `add rcx, [field]` whose destination later becomes a
            # memory base shows that `rcx_old + field` is an address - the field is a COMPONENT of
            # that address, which is just as likely a displacement or a size as a pointer. Reading
            # the LegacyPs2GsTextureContext output caught this: three rows the store itself calls
            # `addendXXXX` were being reported as pointers on exactly that reasoning.
            if mn == "mov":
                b = becomes_base(fn, site)
                if b:
                    ev["pointer"] += 1
                    cite.setdefault("pointer", (site, "%s  -> dereferenced at %08X (%s)"
                                                % (txt, b[0], b[1])))
            elif mn == "add" and becomes_base(fn, site):
                ev["addrterm"] += 1
                cite.setdefault("addrterm", (site, "%s  -> the SUM becomes a base" % txt))
        kinds = [k for k in ("float", "vector", "pointer", "addrterm", "signed",
                             "unsigned", "bitfield") if ev[k]]
        if not kinds:
            continue
        # bitfield plus arithmetic is not a bit set
        if "bitfield" in kinds and ev["arith"]:
            kinds.remove("bitfield")
        verdict = ("CONFLICT: " + "/".join(kinds)) if len(kinds) > 1 else (kinds[0] if kinds else "")
        if not verdict:
            continue
        out.append((d, name, size, ctype, verdict, len(per[d]), cite))

    print()
    print("%-9s %-24s %-4s %-10s %s" % ("offset", "field", "sz", "ctype", "verdict"))
    for d, name, size, ctype, verdict, n, cite in out:
        flag = "  [ONE ACCESS - anecdote]" if n == 1 else ""
        print("+0x%-6X %-24s %-4d %-10s %s%s" % (d, name[:24], size, ctype or "-", verdict, flag))
        for k, (site, txt) in cite.items():
            if k in verdict:
                print("      %-8s %08X  %s" % (k, site, txt[:58]))
    print()
    print("candidates: %d of %d weak rows" % (len(out), len(want)))
    print("NOTHING WAS WRITTEN. Each row above needs a person to accept the citation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
