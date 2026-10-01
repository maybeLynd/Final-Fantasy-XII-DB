#!/usr/bin/env python3
"""receiver_flow_census.py - census a type's fields from a function whose arg0 is the object,
FLOW-SENSITIVELY, so that a re-based or reloaded receiver register cannot manufacture fields.

WHY IT EXISTS.  The store's existing censuses harvest `[<reg> + N]` after finding one
`mov <reg>, rcx` in the prologue and treating every later displacement off that register as a
field.  That is unsound, and 002778C0 (BattleMenuWidget2DC0's registered handler) is the worked
counterexample this script was written from:

  002778FC  mov rsi, rcx           <- receiver established
  00278701  mov rsi, [rbp - 0x21]  <- RELOADED from a stack slot; every later [rsi+N] on that
                                      path belongs to whatever that slot holds, not the object
  00278FD2  add rsi, 0x1600        <- RE-BASED
  00278FE3  lea rsi, [rsi+0x1620]  <- re-based again, inside a two-iteration loop

A flat harvest of that body reports 32 displacements including `-0x1620`, which is not a field at
any object.  This script reports 30, and separately reports the 13 sites where the receiver is
the INDEX rather than the base (`mov eax, [rcx + rsi + 0x1618]`) - a shape a base-only scan
cannot see at all, and the shape that proves an array walk.

THREE CONTROLS THIS SCRIPT ENFORCES ON ITSELF.  The first two each changed the 002778C0
answer; the third was added the same day, after the first version of this script was caught
doing the thing it exists to prevent:

* THE EXTENT IS CHECKED AND A BAD ONE IS REFUSED, exit 1, no result.  The extent is the one
  input this census cannot derive for itself, and a short one does not fail - it produces a
  small, clean, confident answer.  `--bytes 3` on a 389-byte body reported "reached 1 of 1
  instructions, 0 distinct receiver displacements" and exited 0.  So: a claimed end that
  falls inside an instruction is refused, and an extent that disagrees with the function
  list is refused until `--allow-extent-mismatch` says the boundary was re-derived from the
  bytes.  The list is NOT an authority - it has been wrong in this store, which is why the
  override exists - but a disagreement is a reason to look rather than to proceed silently.


* THE RECORDING PASS RUNS AFTER CONVERGENCE, never inside the fixpoint.  Recording as the
  worklist runs banks states that a later iteration refutes: 002778C0's two-iteration loop at
  00278FE0 first reaches the head with rsi = object+0x1600 and only on the back edge learns it
  is also object+0x2C20.  Recording early kept the refuted first answer and invented four
  fields.
* EVERY jump table must be supplied, and unreached instructions are REPORTED.  002778C0 has
  four (00279D60/14, 00279DC8/2, 00279DE4/8, 00279E04/7); following only the first leaves 140
  instructions unvisited, and a census over 93% of a body is not a census.

WHAT IT PROVES AND WHAT IT DOES NOT.  It proves which displacements are taken off the object.
It does not prove field widths, extents or meanings, and a displacement reached only through a
register the analysis gave up on is not reported at all rather than guessed.

    receiver_flow_census.py 0x2778C0 --end 0x279D5E --tables 0x277923=0x279D60:14
"""
import argparse
import collections
import io
import os
import struct
import sys

import kit_paths as KP
import disasm_fn as DF
import reg_tracking as RT
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import capstone.x86 as X

G = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
     "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}     # MS x64 caller-saved
TOP = "T"

_C = {}
for _g in G:
    _C[_g] = _g
    if _g[1].isdigit():
        for _s in ("d", "w", "b"):
            _C[_g + _s] = _g
    else:
        _C["e" + _g[1:]] = _g
        _C[_g[1:]] = _g
for _a, _b in [("al", "rax"), ("bl", "rbx"), ("cl", "rcx"), ("dl", "rdx"), ("sil", "rsi"),
               ("dil", "rdi"), ("bpl", "rbp"), ("spl", "rsp"), ("ah", "rax"), ("bh", "rbx"),
               ("ch", "rcx"), ("dh", "rdx")]:
    _C[_a] = _b


def canon(name):
    return _C.get(name)


class Body(object):
    """One function, decoded linearly across a VERIFIED extent."""

    def __init__(self, img, start, end):
        self.img, self.start, self.end = img, start, end
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True
        self.I, self.order = {}, []
        a = start
        while a < end:
            ins = next(self.md.disasm(img.read(a, 16), a), None)
            if ins is None:
                raise SystemExit("undecodable byte at %08X - the extent is wrong" % a)
            self.I[a] = ins
            self.order.append(a)
            a += ins.size
        if a != end:
            # NOT a warning. A claimed end that falls inside an instruction is a wrong
            # extent, and a census over a wrong extent still prints a confident result -
            # `--bytes 3` on a 389-byte body reported "reached 1 of 1 instructions, 0
            # displacements" and exited 0. That is the same shape as a control that is
            # printed but not enforced, which this session had upheld against elsewhere
            # on the very day this script was written. Fail closed.
            raise SystemExit(
                "receiver_flow_census: the claimed end %08X falls INSIDE an instruction "
                "(the last one decoded runs to %08X). The extent is wrong, and a census "
                "over a wrong extent is not a weaker census - it is a confident empty "
                "one. Fix the extent; no result is issued." % (end, a))

    def tail(self):
        t = self.img.read(self.end, 0x100) or b""
        pad = 0
        while pad < len(t) and t[pad] == 0xCC:
            pad += 1
        return pad, t[:16]


def census(body, tables, entry_reg="rcx", seed_globals=(), seed_fields=()):
    """`seed_globals` - VAs whose LOADED VALUE is the object.
    `seed_fields` - abstract field offsets `OFF` where `object = *(<receiver> + OFF)`.

    THE ENTRY-REGISTER MODEL DOES NOT COVER EVERY RECEIVER, and the gap is not exotic. The
    EXP-109 request pump `0032E070` takes no object argument: it loads the pending-list head out
    of the global `022C51C0` inside its own body and works through that. Seeding `rcx` at entry
    describes the caller's rcx, which is not the slot, so every displacement the pump touches
    would be attributed to the wrong object - or, with `rcx` dead at entry, to nothing at all.

    A VA listed in `seed_globals` means `mov <reg>, [rip+disp]` resolving to it makes `<reg>`
    the receiver, exactly as the entry register would. It is the same abstract value from a
    different door.

    An offset listed in `seed_fields` is the third door: a receiver loaded out of a PARENT
    field. `mov <d>, [<b> + <disp>]` fires the seed when `<b>` is a tracked receiver and the
    abstract field address `b + disp` equals a declared offset - `*(R + OFF)` is the child
    object wherever the parent flow reaches that field, whether `b` is the entry register at
    offset 0 or a derived receiver mid-body. CHAIN-routed types take this door; DYNAMIC, FN,
    SLOTPTR, PTR and RELOFF are the same shape in different dress.
    """
    I, START, END = body.I, body.start, body.end
    seed_globals = set(seed_globals)
    seed_fields = set(seed_fields)

    def succs(a):
        ins = I[a]
        nxt = a + ins.size
        m = ins.mnemonic
        if m == "ret":
            return []
        if m == "jmp":
            op = ins.operands[0]
            if op.type == X.X86_OP_IMM:
                return [op.imm] if START <= op.imm < END else []
            return tables.get(a, [])
        if m.startswith("j"):
            op = ins.operands[0]
            t = [nxt]
            if op.type == X.X86_OP_IMM and START <= op.imm < END:
                t.append(op.imm)
            return t
        return [nxt] if nxt < END else []

    def join(s1, s2):
        if s1 is None:
            return dict(s2)
        return {k: (s1.get(k, TOP) if s1.get(k, TOP) == s2.get(k, TOP) else TOP)
                for k in set(s1) | set(s2)}

    st0 = dict((g, TOP) for g in G)
    st0[entry_reg] = ("R", 0)
    state = {START: st0}
    wl = [START]
    while wl:
        a = wl.pop()
        st = state[a]
        ins = I[a]
        m = ins.mnemonic
        ns = dict(st)
        if m == "call":
            for v in VOLATILE:
                ns[v] = TOP
        elif m == "lea" and ins.operands[0].type == X.X86_OP_REG:
            d = canon(ins.reg_name(ins.operands[0].reg))
            src = ins.operands[1].mem
            b = canon(ins.reg_name(src.base)) if src.base else None
            if d:
                ok = b and src.index == 0 and st.get(b, TOP) != TOP
                ns[d] = ("R", st[b][1] + src.disp) if ok else TOP
        elif (m == "mov" and ins.operands[0].type == X.X86_OP_REG
              and ins.operands[1].type == X.X86_OP_REG):
            d = canon(ins.reg_name(ins.operands[0].reg))
            s = canon(ins.reg_name(ins.operands[1].reg))
            if d:
                ns[d] = st.get(s, TOP) if s else TOP
        elif (seed_globals and m == "mov" and ins.operands[0].type == X.X86_OP_REG
              and ins.operands[1].type == X.X86_OP_MEM
              and ins.operands[1].mem.base == X.X86_REG_RIP
              and (ins.address + ins.size + ins.operands[1].mem.disp) in seed_globals):
            d = canon(ins.reg_name(ins.operands[0].reg))
            ns[d] = ("R", 0) if d else TOP
        elif (seed_fields and m == "mov" and ins.operands[0].type == X.X86_OP_REG
              and ins.operands[1].type == X.X86_OP_MEM
              and ins.operands[1].mem.base not in (0, X.X86_REG_RIP)
              and ins.operands[1].mem.index == 0):
            mm = ins.operands[1].mem
            b = canon(ins.reg_name(mm.base))
            v = st.get(b, TOP) if b else TOP
            d = canon(ins.reg_name(ins.operands[0].reg))
            if v != TOP and (v[1] + mm.disp) in seed_fields:
                # A distinct abstract identity, NOT ("R", 0): the child is a different
                # object than the parent it was loaded out of, and giving it the parent's
                # tag would attribute its displacements to the parent - a confident wrong
                # census, worse than none. The tag names the field it came through.
                ns[d] = ("S:%X" % (v[1] + mm.disp), 0) if d else TOP
            elif d:
                ns[d] = TOP
        elif (m in ("add", "sub") and ins.operands[0].type == X.X86_OP_REG
              and ins.operands[1].type == X.X86_OP_IMM):
            d = canon(ins.reg_name(ins.operands[0].reg))
            if d:
                v = st.get(d, TOP)
                ns[d] = ("R", v[1] + ins.operands[1].imm * (1 if m == "add" else -1)) \
                    if v != TOP else TOP
        else:
            for rg in ins.regs_access()[1]:
                c = canon(ins.reg_name(rg))
                if c:
                    ns[c] = TOP
        for s in succs(a):
            if s not in I:
                continue
            j = join(state.get(s), ns)
            if state.get(s) != j:
                state[s] = j
                wl.append(s)

    base_hits = collections.defaultdict(list)
    index_hits = []
    for a in sorted(state):
        st, ins = state[a], I[a]
        for oi, op in enumerate(ins.operands):
            if op.type != X.X86_OP_MEM:
                continue
            # A `lea` does not touch memory - its MEM operand is an ADDRESS BEING TAKEN.
            # Recording it as a read invents an access, and recording `lea rsi,[rsi+0x1620]`
            # as a field at +0x1620 is how the earlier flat census of 002778C0 reported two
            # displacements that no instruction ever loads or stores.  Kept, because an
            # address handed to a callee IS evidence of a sub-object, but kept as its own kind.
            # Read/write comes from reg_tracking.op_kind (mnemonic tables first, capstone
            # flags second, "?" never a guess): capstone's own flags are wrong for some
            # encodings - they called `movups [m], xmm` stores reads and left `test [m], reg`
            # unflagged, which the positional fallback then called a write.
            if ins.mnemonic == "lea":
                kind = "a"
            else:
                kind = RT.op_kind(ins, op, oi)
            mm = op.mem
            cb = canon(ins.reg_name(mm.base)) if mm.base else None
            ci = canon(ins.reg_name(mm.index)) if mm.index else None
            bR = bool(cb) and st.get(cb, TOP) != TOP
            iR = bool(ci) and st.get(ci, TOP) != TOP and mm.scale == 1 and ci != cb
            if bR and not iR:
                base_hits[(st[cb][0], st[cb][1] + mm.disp)].append((a, cb, kind, ins))
            elif iR and not bR:
                index_hits.append((a, st[ci][1], mm.disp, cb, kind, ins, st[ci][0]))
    return state, base_hits, index_hits


def parse_tables(img, specs):
    """--tables <dispatch va>=<table va>:<entry count>; entries are image-base relative."""
    out = {}
    for s in specs or []:
        site, rest = s.split("=", 1)
        va, n = rest.split(":")
        site, va, n = int(site, 16), int(va, 16), int(n)
        out[site] = [img.base + struct.unpack("<I", img.read(va + 4 * i, 4))[0]
                     for i in range(n)]
    return out


def check_extent_against_graph(start, end, allow):
    """Cross-check the caller's extent against the function list, when it lists the entry.

    The extent is the one input this census cannot derive for itself, and it is the input
    that silently ruins the answer: a short one produces a small, clean, confident result
    rather than an error. Where an independent source has an opinion, use it.
    """
    import csv
    path = os.path.join(KP.WORK, "graph", "functions.tsv")
    if not os.path.exists(path):
        return
    for r in csv.DictReader(io.open(path, encoding="utf-8", newline=""), delimiter="\t"):
        try:
            if int(r["entry"], 16) != start:
                continue
        except (ValueError, KeyError):
            continue
        listed = start + int(r["body_bytes"])
        # the chained-tails extent rule (2026-09-30): an adjudicated errata end (uc1_band.errata_extends) is listed too
        import uc1_band
        adjudicated = uc1_band.errata_extends().get(start)
        if listed == end or adjudicated == end or allow:
            return
        raise SystemExit(
            "receiver_flow_census: %08X is a LISTED function whose body ends at %08X, but "
            "the extent given ends at %08X (%+d bytes). The function list is not an "
            "authority - it has been wrong in this store - but a disagreement is a reason "
            "to look, not to proceed silently. Re-derive the boundary from the bytes and "
            "pass --allow-extent-mismatch once you have. No result is issued."
            % (start, listed, end, end - listed))
    return


def main():
    p = argparse.ArgumentParser()
    p.add_argument("start")
    p.add_argument("--end")
    p.add_argument("--bytes", type=int)
    p.add_argument("--tables", action="append")
    p.add_argument("--reg", default="rcx")
    p.add_argument("--seed-global", action="append", dest="seed_global",
                   help="a VA whose LOADED value is the object, for a receiver that arrives "
                        "from a global inside the body rather than in a register at entry")
    p.add_argument("--seed-field", action="append", dest="seed_field",
                   help="an abstract field offset OFF where `object = *(<receiver> + OFF)` - "
                        "a receiver loaded out of a parent field (CHAIN routes and the "
                        "DYNAMIC/FN/SLOTPTR/PTR/RELOFF shapes)")
    p.add_argument("--exe", default=KP.EXE)
    p.add_argument("--allow-extent-mismatch", action="store_true",
                   dest="allow_extent_mismatch",
                   help="proceed although the extent disagrees with the "
                        "function list - only after re-deriving it from the bytes")
    a = p.parse_args()

    img = DF.Image(a.exe)
    start = int(a.start, 16)
    end = int(a.end, 16) if a.end else start + a.bytes
    check_extent_against_graph(start, end, a.allow_extent_mismatch)
    body = Body(img, start, end)
    seeds = [int(g, 16) for g in (a.seed_global or [])]
    fields = [int(g, 16) for g in (a.seed_field or [])]
    state, base, index = census(body, parse_tables(img, a.tables), a.reg, seeds, fields)

    pad, head = body.tail()
    print("BODY %08X..%08X  %d instructions, %d bytes"
          % (start, end, len(body.I), end - start))
    print("  tail: %d int3, then %s" % (pad, head.hex()))
    print("  reached %d of %d instructions%s"
          % (len(state), len(body.I),
             "" if len(state) == len(body.I) else "   <-- UNRESOLVED CONTROL FLOW"))
    groups = collections.defaultdict(dict)
    for (tag, d), sites in base.items():
        groups[tag][d] = sites
    for tag in sorted(groups):
        g = groups[tag]
        label = ("receiver displacements" if tag == "R"
                 else "displacements on the object loaded through *(R+%s)" % tag[2:])
        print("\n%s - %d distinct, %d sites:"
              % (label, len(g), sum(len(v) for v in g.values())))
        for d in sorted(g):
            kinds = sorted(set(k for _, _, k, _ in g[d]))
            print("  +0x%-6X %2d sites  %s" % (d, len(g[d]), "/".join(kinds)))
    if index:
        print("\n%d RECEIVER-AS-INDEX sites (an array walk off the object):" % len(index))
        for site, delta, disp, b, kind, ins, tag in sorted(index):
            print("  %08X  [%s] base=%s  %s+0x%X + 0x%X   %s %s"
                  % (site, kind, b, tag, delta, disp, ins.mnemonic, ins.op_str))
    un = [x for x in body.order if x not in state]
    if un:
        print("\nUNREACHED %d instructions - resolve before trusting the census:" % len(un))
        for x in un[:12]:
            print("  %08X  %s %s" % (x, body.I[x].mnemonic, body.I[x].op_str))


if __name__ == "__main__":
    main()
