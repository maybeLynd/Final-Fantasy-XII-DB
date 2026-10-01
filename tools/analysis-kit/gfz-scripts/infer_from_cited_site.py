#!/usr/bin/env python3
"""infer_from_cited_site.py - read a field's representation from the site its OWN EVIDENCE cites.

WHY THIS EXISTS, and it is the opposite approach to the census reader. `infer_field_type.py`
needs a census, and a census needs a route, and over the swept types only 25% of weak rows had
any access in their type's census at all - not because the censuses are thin (GameSettingConfig
has 154 rows and covers none of its weak offsets) but because those particular offsets are not
reachable from the route.

They are not undiscovered, though. They were found by SOMETHING, and that something is usually
named in the row: 122 of 140 unreached weak rows carry at least one hex address in their evidence
column. That address is an instruction. An instruction states a width and often a representation,
and reading it needs no route, no census and no closure.

WHAT IT DOES. For every weak named field whose evidence names an address, disassemble there and:

  * CHECK THE CITATION FIRST. The instruction must reference memory at this row's offset. If it
    does not, nothing is inferred. That is NOT automatically a defect: a great many rows cite a
    FUNCTION rather than an instruction - `SaveImageHeader` cites 002EF640, which is its own FN
    route base, and the D3D11 rows cite 0063C4A0, the Phyre accessor - and citing the owner or
    the mechanism is legitimate. The report therefore separates "the address is a known function
    start" from "the address is an instruction that touches a different offset", and only the
    second is worth chasing.
  * report the ACCESS WIDTH from the operand (byte/word/dword/qword/xmmword) and flag any row
    whose declared size disagrees;
  * classify the representation exactly as the census reader does - float, vector, signed,
    unsigned, bitfield - from the mnemonic and the operand.

WHAT IT DOES NOT DO. It does not chase the value into callees; one cited site is one instruction,
and a single instruction is an anecdote unless several citations agree. Rows whose citations
disagree are reported as CONFLICT and classified as nothing. It writes nothing to the store.

    python infer_from_cited_site.py --db "<db>"
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
SPAN = re.compile(r"^(unobserved|unread|pad)", re.I)
ADDR = re.compile(r"\b(00[0-9A-Fa-f]{6})\b")
FLOAT = re.compile(r"^(movss|movsd|mulss|addss|subss|divss|comiss|ucomiss|cvtsi2ss|cvtss2si|"
                   r"maxss|minss|sqrtss)$")
VEC = re.compile(r"^(movaps|movups|movdqa|movdqu|addps|mulps|shufps)")
SIGNX = re.compile(r"^(movsx|movsxd)$")
BITOP = re.compile(r"^(test|or|and|btr|bts|bt)$")
ARITH = re.compile(r"^(add|sub|imul|mul|inc|dec|shl|shr|sar)$")
WIDTH = {1: "byte", 2: "word", 4: "dword", 8: "qword", 16: "xmmword"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--type")
    ap.add_argument("--max-sites", type=int, default=6)
    a = ap.parse_args()

    raw = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off, secs = pe + 24 + opt, []
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((nm, ib + va, vs, rs, pr))
        off += 40

    def fo(x):
        for nm, va, vs, rs, pr in secs:
            if va <= x < va + vs and (x - va) < rs:
                return pr + (x - va)

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    fsizes_all, _names_all = M.load_funcs()
    _cache = {}

    def _il(fn):
        if fn not in _cache:
            q = fo(fn)
            _cache[fn] = (list(md.disasm(raw[q:q + fsizes_all[fn]], fn))
                          if fn in fsizes_all and q is not None else [])
        return _cache[fn]

    ARGREG = ("rcx", "rdx", "r8", "r9")

    def _deref_in_callee(callee, argreg, budget=400):
        """Does `callee` dereference the parameter that arrived in `argreg`?

        IT MUST FOLLOW THE PARAMETER, NOT THE REGISTER. A callee almost always parks its
        arguments in callee-saved registers in the prologue before doing anything with them:
        003FA600 opens `mov rbx,[r8+0x2490]; mov rbp, r9; mov r14, rdx; mov r15, rcx`, and a
        scan watching only `r9` sees the copy, learns nothing, and gives up. Following the value
        through `mov <reg>, <carrier>` is what makes the test work on real prologues.

        It still stops at the first CALL, because after that the tracked register may hold
        something else and a hit would be about that value rather than this one.
        """
        carriers = {argreg}
        for i in _il(callee)[:budget]:
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
                return None
            carriers -= set(RT.written(i))
            if not carriers:
                return None
        return None

    def deref_from(site):
        """Is the value loaded at `site` dereferenced - here, or one call level in?

        Same proof the census reader uses, but seeded from the cited site instead of a census
        row, so it works for the rows no route reaches.
        """
        fn = max((f for f in fsizes_all if f <= site < f + fsizes_all[f]), default=None)
        if fn is None:
            return None
        dst = None
        for i in _il(fn):
            if i.address == site:
                if i.operands and i.operands[0].type == X86_OP_REG:
                    dst = i.reg_name(i.operands[0].reg)
                continue
            if dst is None:
                continue
            for op in i.operands:
                if op.type == X86_OP_MEM and op.mem.base and op.mem.base != X86_REG_RIP                         and i.reg_name(op.mem.base) == dst:
                    return (i.address, "here")
            if i.mnemonic == "mov" and len(i.operands) == 2                     and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_REG                     and i.reg_name(i.operands[1].reg) == dst:
                dst = i.reg_name(i.operands[0].reg)
                continue
            if i.group(2):
                if dst in ARGREG and i.operands and i.operands[0].type == X86_OP_IMM                         and i.operands[0].imm in fsizes_all:
                    w = _deref_in_callee(i.operands[0].imm, dst)
                    if w:
                        return (w, "callee %08X" % i.operands[0].imm)
                dst = None
                continue
            if dst in RT.written(i):
                dst = None
        return None


    # AN EMBEDDED TYPE'S ACCESSES ARE OFTEN PARENT-RELATIVE, and its own rows are not. A row of
    # ManagerSub0209BE80_57E0 at +0x192 is reached as `cmp word ptr [rcx+0x5972], 0`, because the
    # sub-object sits at +0x57E0 of its parent and the compiler folded the two displacements. The
    # row names already carry the folded value (`count5972`). Checking only the sub-object-
    # relative displacement reported 12 correct citations as mismatches, so resolve the EMBED
    # chain from types.tsv and accept either displacement.
    embed = {}
    with io.open(os.path.join(a.db, "_types", "types.tsv"), encoding="utf-8", newline="") as fh:
        rr = list(csv.reader(fh, delimiter="	"))
    tci = {k: i for i, k in enumerate(rr[0])}
    parent = {}
    for f in rr[1:]:
        if not f or not f[0] or len(f) <= tci.get("route", 99):
            continue
        m = re.match(r"EMBED\s+(\S+)\s+\+0x([0-9A-Fa-f]+)", f[tci["route"]].strip())
        if m:
            parent[f[0]] = (m.group(1), int(m.group(2), 16))

    def chain(t, depth=0):
        if depth > 6 or t not in parent:
            return 0
        p, o = parent[t]
        return o + chain(p, depth + 1)
    for t in parent:
        embed[t] = chain(t)

    rows = []
    with io.open(os.path.join(a.db, "_types", "fields.tsv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r, None)
        for f in r:
            if len(f) < 9 or not f[0] or SPAN.match(f[3]):
                continue
            if a.type and f[0] != a.type:
                continue
            if f[6] in ("DISCOVERED", "") or f[7] == "UNKNOWN":
                rows.append(f)
    print("weak named field rows considered: %d" % len(rows))

    # the declared size and any stride, so a citation OF THOSE can be recognised as such
    tsize, tstride = {}, {}
    for f in rr[1:]:
        if not f or not f[0]:
            continue
        try:
            tsize[f[0]] = int(f[1], 0)
        except (ValueError, IndexError):
            pass
        if len(f) > tci.get("route", 99):
            m2 = re.search(r"stride=0x([0-9A-Fa-f]+)", f[tci["route"]])
            if m2:
                tstride[f[0]] = int(m2.group(1), 16)

    out, mism, nocite, widthbad, leaonly, otherkind = [], [], [], [], [], []
    for f in rows:
        offv, size = int(f[1], 16), int(f[2])
        alt = offv + embed.get(f[0], 0)
        sites = []
        seen = set()
        for m in ADDR.finditer(f[8]):
            v = int(m.group(1), 16)
            if v not in seen:
                seen.add(v)
                sites.append(v)
        if not sites:
            nocite.append(f)
            continue
        ev, cite, widths, matched = collections.Counter(), {}, set(), 0
        leahit = []
        for s in sites[:a.max_sites]:
            p = fo(s)
            if p is None:
                continue
            i = next(md.disasm(raw[p:p + 16], s), None)
            if i is None:
                continue
            # A `lea` COMPUTES AN ADDRESS AND READS NOTHING. Capstone still reports an operand
            # size for its memory operand - 8 on x64 - and taking that as the field's access
            # width is wrong: `addrTaken26AE` is a 1-byte field whose only citation is
            # `lea r14, [rsi+0x26AE]`, and this check reported it as "declared 1, accessed
            # qword". The lea proves the address is taken and says nothing about the width.
            if i.mnemonic == "lea":
                for op in i.operands:
                    if op.type == X86_OP_MEM and op.mem.base                             and op.mem.base != X86_REG_RIP and op.mem.disp in (offv, alt):
                        leahit.append((s, "%s %s" % (i.mnemonic, i.op_str)))
                continue
            hit = None
            for op in i.operands:
                if op.type == X86_OP_MEM and op.mem.base and op.mem.base != X86_REG_RIP \
                        and op.mem.disp in (offv, alt):
                    hit = op
            if hit is None:
                continue
            matched += 1
            widths.add(hit.size)
            mn, txt = i.mnemonic, "%s %s" % (i.mnemonic, i.op_str)
            if FLOAT.match(mn):
                ev["float"] += 1; cite.setdefault("float", (s, txt))
            elif VEC.match(mn):
                ev["vector"] += 1; cite.setdefault("vector", (s, txt))
            elif SIGNX.match(mn):
                ev["signed"] += 1; cite.setdefault("signed", (s, txt))
            elif mn == "movzx":
                ev["unsigned"] += 1; cite.setdefault("unsigned", (s, txt))
            elif BITOP.match(mn) and any(o.type == X86_OP_IMM for o in i.operands):
                ev["bitfield"] += 1; cite.setdefault("bitfield", (s, txt))
            elif ARITH.match(mn):
                ev["arith"] += 1
            # A PLAIN `mov` FIXES THE WIDTH AND NO IDIOM, which is why most of the READABLE
            # bucket scored nothing. But an 8-byte load whose value is DEREFERENCED is a
            # pointer, and that proof does not need a census either - the cited site is the
            # load, so follow the value from there exactly as the census reader does: within
            # this body, or one call level into a callee that dereferences the parameter.
            elif mn == "mov" and hit.size == 8 and i.operands[0].type == X86_OP_REG:
                w = deref_from(s)
                if w:
                    ev["pointer"] += 1
                    cite.setdefault("pointer", (s, "%s  -> dereferenced at %08X (%s)"
                                                % (txt, w[0], w[1])))
        if not matched and not leahit:
            # NOT EVERY NON-MATCHING CITATION IS WRONG. Several rows are evidenced by something
            # other than a displacement access, and each of those is a legitimate and DIFFERENT
            # kind of evidence that this matcher structurally cannot confirm:
            #   * an IMMEDIATE equal to the type's size or stride - a bulk copy or an array walk.
            #     BattleResultRecord (size 0x148) cites `mov r8d, 0x148`; InputBindingRecord
            #     (stride 0x15C) cites `add rsi, 0x15c`.
            #   * an INDEXED access - `mov dword ptr [r14 + r12 - 0x60], eax` reaches a field
            #     through base+index, and the displacement alone is not comparable.
            #   * a NEGATIVE displacement - the access is through a running or end pointer.
            kind = None
            for x in sites[:a.max_sites]:
                q = fo(x)
                if q is None:
                    continue
                ii = next(md.disasm(raw[q:q + 16], x), None)
                if ii is None:
                    continue
                for op in ii.operands:
                    if op.type == X86_OP_IMM and op.imm in (tsize.get(f[0]), tstride.get(f[0])):
                        kind = "cites the type's size or stride (a bulk copy or an array walk)"
                    if op.type == X86_OP_MEM and op.mem.index:
                        kind = kind or "an INDEXED access; the displacement alone is not comparable"
                    if op.type == X86_OP_MEM and op.mem.disp < 0:
                        kind = kind or "a NEGATIVE displacement; reached through a running pointer"
            if kind:
                otherkind.append((f, kind))
                continue
        if not matched:
            # A `lea` at this row's own offset is a CORRECT citation - the row was discovered
            # because its address is taken, which is exactly what names like `subAddr0342` say.
            # It proves the address is taken and states neither a width nor a representation,
            # so it is neither a defect nor a reading. Its own category.
            (leaonly if leahit else mism).append((f, [x for x, _ in leahit] or sites[:3]))
            continue
        if widths and size not in widths:
            widthbad.append((f, sorted(widths)))
        kinds = [k for k in ("float", "vector", "pointer", "signed", "unsigned", "bitfield") if ev[k]]
        if "bitfield" in kinds and ev["arith"]:
            kinds.remove("bitfield")
        if kinds:
            out.append((f, ("CONFLICT: " + "/".join(kinds)) if len(kinds) > 1 else kinds[0],
                        matched, cite))

    print()
    print("CITATION CHECK - the cited instruction must touch this row's offset")
    print("   rows with no address cited at all            : %d" % len(nocite))
    print("   citation is a `lea` taking THIS field's address: %d   (correct - the row was found"
          % len(leaonly))
    print("        because its address is taken, e.g. the subAddr* rows; states no width)")
    import member_reach_scan as _M
    _fs, _ = _M.load_funcs()
    fnref = [(f, s) for f, s in mism if any(x in _fs for x in s)]
    other = [(f, s) for f, s in mism if not any(x in _fs for x in s)]
    print("   cited address is a FUNCTION start, not an instruction : %d   (legitimate - the row"
          % len(fnref))
    print("        names its owner or the mechanism, e.g. an FN route base or a shared accessor)")
    print("   evidenced by something other than a displacement access: %d   (legitimate - see"
          % len(otherkind))
    print("        below; this matcher structurally cannot confirm these)")
    for f, why in otherkind[:10]:
        print("      %-32s +0x%-5s %-22s %s" % (f[0][:32], f[1], f[3][:22], why))
    print("   cited instruction touches a DIFFERENT offset          : %d   <-- worth chasing"
          % len(other))
    for f, s in other[:10]:
        print("      %-32s +0x%-5s %-22s cited %s"
              % (f[0][:32], f[1], f[3][:22], ",".join("%08X" % x for x in s)))
    print()
    print("WIDTH DISAGREEMENT - declared size vs the cited access width: %d" % len(widthbad))
    for f, w in widthbad[:12]:
        print("      %-32s +0x%-5s %-22s declared %s, accessed %s"
              % (f[0][:32], f[1], f[3][:22], f[2],
                 "/".join(WIDTH.get(x, str(x)) for x in w)))
    print()
    print("REPRESENTATION read from the cited site(s): %d row(s)" % len(out))
    for f, verdict, n, cite in out:
        flag = "  [ONE SITE - anecdote]" if n == 1 else ""
        print("   %-30s +0x%-6s %-22s %-22s%s"
              % (f[0][:30], f[1], f[3][:22], verdict, flag))
        for k, (s, txt) in cite.items():
            if k in verdict:
                print("        %-9s %08X  %s" % (k, s, txt[:56]))
    print()
    print("NOTHING WRITTEN. A citation that does not touch the offset is a defect to fix, not a")
    print("reading to salvage, and a single site is an anecdote.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
