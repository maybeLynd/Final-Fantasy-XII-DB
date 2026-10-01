#!/usr/bin/env python3
"""Every in-place widget construction site, with the EXTENT the caller asks for.

WHY THIS IS THE ONE MEASUREMENT THAT MATTERS NOW. The sized-by-argument ctype rule
(SWE2-FRONTIER, 2026-09-19) spells an embedded widget as the bare ctype and requires THE ROW'S
OWN WIDTH TO CARRY THE EXTENT. Every embedded instance the store evidences has a FLOOR - the
highest offset anybody was seen to touch - and a floor is not an extent. Declaring one as the
other is exactly what that rule's error message guards against.

A widget's size is not inferred. IT IS AN ARGUMENT. `00245000` is the in-place constructor:
`rcx` is caller-owned storage, `edx` is the size, `r8` is the handler, and its fifth argument
is always 1, which sets bit 14 of `+0x40` meaning storage the widget does not own - i.e. an
EMBEDDED widget rather than a pool slot. `002465F0` is the sized initialiser it wraps. So the
extent of an embedded instance is readable at its construction site:

    0029849E   lea rcx, [rsi+0xc0] ; mov edx, 0x4c0 ; call 00245000

gives offset 0xC0 and extent 0x4C0 in one read. This tool recovers that pair at every site.

METHOD, AND ITS ONE HONEST LIMIT. Function bodies are decoded from the entries in
graph/functions.tsv rather than by a linear sweep of .text, so no recovered operand comes from
a desynchronised stream. Inside each body the scan keeps the last-written value of rcx and edx
and reports them at the call. IT REPORTS ONLY WHAT IT SAW WRITTEN IN THAT BODY: where the size
arrives as a parameter rather than a literal, the tool says UNRESOLVED-ARG instead of guessing.
The store already counts four such sites at the factory (`rbx*2 + 0xF0`, `rdi*8 + 0x100`,
`max(0x188, edx)`, and a branch picking 0x1F8 or 0x278) - a computed size is a real answer
about the code and must not be flattened into a number.

THREE RULES WERE TRIED AND THEY ARE EXHAUSTED - recorded so the next person does not rebuild
them expecting more. (1) FORWARDER: a body that never writes rcx passes its own first argument
through; bound _8FA0 to 0x1110 via the single-caller wrapper 002BE450. (2) ARG0 ALIAS: a body
that SAVES rcx into a register and restores it is forwarding just as much; bound _AB30 to
0x61F0. (3) ONE BACKWARD STEP: where rcx comes from a register, take that register's last
definition in the same body and accept only a plain `lea base+disp`; this yielded exactly ONE
further site (002D5F5E in 002D5EB0, storage rdi+0xC0, extent 0xC0) and refused two whose source
is a stack load or an `add`.

So three rules produced three bindings. The sites that remain do not share another peephole
shape - their storage arrives from a field load, a computed address, or a caller several frames
up - and resolving them needs real backward dataflow rather than a fourth pattern that happens
to fit a few. A fourth rule fitted to the residue would be curve-fitting, not analysis.

    python scan_widget_inplace_extents.py --self-test
    python scan_widget_inplace_extents.py
"""
import argparse
import csv
import io
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_widget_census import load_image  # noqa: E402

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM
except ImportError:
    sys.exit("capstone is required")

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")

INPLACE = 0x245000       # rcx = storage, edx = size, r8 = handler, 5th arg 1 (not owned)
SIZED = 0x2465F0         # the sized initialiser 00245000 wraps
FACTORY = 0x244F50       # allocates; ecx = requested size, 0 rewritten to 0xC0

R32 = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esp": "rsp", "ebp": "rbp",
       "esi": "rsi", "edi": "rdi", "r8d": "r8", "r9d": "r9", "r10d": "r10", "r11d": "r11",
       "r12d": "r12", "r13d": "r13", "r14d": "r14", "r15d": "r15"}


def norm(md, reg):
    n = md.reg_name(reg)
    return R32.get(n, n)


def entries():
    out = []
    with io.open(FUNCS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            try:
                out.append((int(r["entry"], 16), int(r["body_bytes"] or 0)))
            except (ValueError, KeyError):
                continue
    return out


def scan(md, raw, fo, code, targets):
    """(site, target, rcx_base, rcx_disp, size) for every call to a target."""
    hits = []
    for entry, nb in code:
        off = fo(entry)
        if off is None or nb <= 0:
            continue
        rcx = None          # ("lea", base_reg, disp) or ("mov", src_reg, None)
        edx = None          # int literal, or None
        wrote_rcx = False   # has this body written rcx at all before the call?
        # ARG0 ALIASES. rcx on entry IS the function's first argument. A body that saves it
        # (`mov rsi, rcx`) and later restores it (`mov rcx, rsi`) is still constructing at its
        # OWN argument - offset 0 of whatever the caller passed - and that is a forwarder just
        # as much as one that never touches rcx. Tracked explicitly rather than assumed: an
        # alias is dropped the moment anything else writes that register.
        arg0 = {"rcx"}
        for i in md.disasm(raw[off:off + nb], entry):
            m = i.mnemonic
            ops = i.operands
            if m == "call" and ops and ops[0].type == X86_OP_IMM and ops[0].imm in targets:
                fwd = (not wrote_rcx) or ('rcx' in arg0)
                hits.append((i.address, ops[0].imm, rcx, edx, entry, not fwd))
                rcx = edx = None
                continue
            if len(ops) == 2 and ops[0].type == X86_OP_REG:
                d = norm(md, ops[0].reg)
                if d == "rcx":
                    wrote_rcx = True
                    if not (m == "mov" and ops[1].type == X86_OP_REG
                            and norm(md, ops[1].reg) in arg0):
                        arg0.discard("rcx")
                    else:
                        arg0.add("rcx")
                    if m == "lea" and ops[1].type == X86_OP_MEM:
                        mem = ops[1].mem
                        base = md.reg_name(mem.base) if mem.base else None
                        rcx = ("lea", base, mem.disp) if not mem.index else None
                    elif m == "mov" and ops[1].type == X86_OP_REG:
                        rcx = ("mov", md.reg_name(ops[1].reg), None)
                    else:
                        rcx = None
                elif d == "rdx":
                    edx = ops[1].imm if (m == "mov" and ops[1].type == X86_OP_IMM) else None
                    arg0.discard("rdx")
                else:
                    if (m == "mov" and ops[1].type == X86_OP_REG
                            and norm(md, ops[1].reg) in arg0):
                        arg0.add(d)
                    else:
                        arg0.discard(d)
            elif m in ("xor",) and len(ops) == 2 and ops[0].type == X86_OP_REG:
                if norm(md, ops[0].reg) == "rdx" and ops[1].type == X86_OP_REG \
                        and norm(md, ops[1].reg) == "rdx":
                    edx = 0
    return hits



def callers_rcx(md, raw, fo, code, target):
    """Every caller of `target`, with rcx as that caller set it."""
    out = []
    for entry, nb in code:
        off = fo(entry)
        if off is None or nb <= 0:
            continue
        rcx = None
        for i in md.disasm(raw[off:off + nb], entry):
            ops = i.operands
            if (i.mnemonic == "call" and ops and ops[0].type == X86_OP_IMM
                    and ops[0].imm == target):
                out.append((i.address, entry, rcx))
            elif len(ops) == 2 and ops[0].type == X86_OP_REG                     and norm(md, ops[0].reg) == "rcx":
                if i.mnemonic == "lea" and ops[1].type == X86_OP_MEM:
                    mem = ops[1].mem
                    rcx = (("lea", md.reg_name(mem.base) if mem.base else None, mem.disp)
                           if not mem.index else None)
                elif i.mnemonic == "mov" and ops[1].type == X86_OP_REG:
                    rcx = ("mov", md.reg_name(ops[1].reg), None)
                else:
                    rcx = None
    return out


def resolve_forwarders(md, raw, fo, code, hits):
    """A site whose body never writes rcx FORWARDS its caller's storage.

    That is the shape 002BE450 has - six instructions, `mov edx, 0x1110`, `call 00245000`, and
    rcx never touched - and it is the only reason the 0x1110 extent could be bound to
    singleton+0x8FA0 at all. Generalised here: for every in-place site whose containing body
    never writes rcx, the storage is that body's OWN first argument, so its callers supply it.
    A forwarder with exactly ONE caller resolves to a single offset; one with several is
    reported with all of them, because a widget built at two different offsets by two callers
    is a real answer and must not be collapsed.
    """
    out = []
    for site, tgt, rcx, size, entry, wrote in sorted(hits):
        if tgt != INPLACE or wrote or size is None:
            continue
        cs = callers_rcx(md, raw, fo, code, entry)
        leas = [(a, e, r) for a, e, r in cs if r and r[0] == "lea"]
        out.append((site, entry, size, cs, leas))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    raw, secs = load_image()

    def fo(x):
        for _nm, va, vs, rs, pr in secs:
            if va <= x < va + vs and (x - va) < rs:
                return pr + (x - va)
        return None

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    code = entries()

    if a.self_test:
        # The documented site must come back exactly: 0029849E lea rcx,[rsi+0xc0]; mov edx,0x4c0
        hits = scan(md, raw, fo, [(e, n) for e, n in code if 0x298000 <= e <= 0x299000],
                    {INPLACE})
        got = [h for h in hits if h[0] == 0x29849E]
        print("self-test: site 0029849E ->", got or "NOT FOUND")
        ok = bool(got) and got[0][2] and got[0][2][2] == 0xC0 and got[0][3] == 0x4C0
        print("self-test %s" % ("PASSES" if ok else
                                "FAILS - the documented lea/mov pair was not recovered"))
        return 0 if ok else 1

    hits = scan(md, raw, fo, code, {INPLACE, SIZED, FACTORY})
    named = {INPLACE: "00245000 in-place", SIZED: "002465F0 sized", FACTORY: "00244F50 factory"}
    by = {t: [] for t in named}
    for site, tgt, rcx, size, _e, _w in hits:
        by[tgt].append((site, rcx, size))

    print("Widget construction sites, by entry point")
    for t, lst in by.items():
        print("  %-22s %4d site(s)" % (named[t], len(lst)))
    print()
    print("IN-PLACE SITES - these are the embedded instances, and the pair to read is")
    print("(offset into the parent, extent asked for):")
    lit = unres = 0
    for site, rcx, size in sorted(by[INPLACE]):
        if rcx and rcx[0] == "lea" and size is not None:
            lit += 1
            print("  %08X  storage = %s + 0x%-6X  extent 0x%-6X" %
                  (site, rcx[1], rcx[2], size))
        else:
            unres += 1
    print()
    print("  %d site(s) give both the offset and a literal extent" % lit)
    print("  %d site(s) do NOT - storage or size arrives as a parameter, reported as" % unres)
    print("     UNRESOLVED-ARG rather than guessed:")
    for site, rcx, size in sorted(by[INPLACE]):
        if not (rcx and rcx[0] == "lea" and size is not None):
            print("  %08X  storage = %-22s extent %s" %
                  (site, (("%s + 0x%X" % (rcx[1], rcx[2])) if rcx and rcx[0] == "lea"
                          else ("<%s>" % (rcx[1] if rcx else "unknown"))),
                   ("0x%X" % size) if size is not None else "UNRESOLVED-ARG"))

    print()
    print("FORWARDERS RESOLVED BY THEIR CALLERS. A body that never writes rcx passes its own")
    print("first argument straight through, so the storage comes from one level up:")
    res = resolve_forwarders(md, raw, fo, code, hits)
    bound = 0
    for site, entry, size, cs, leas in res:
        if len(leas) == 1:
            bound += 1
            _a, _e, r = leas[0]
            print("  %08X in %08X  extent 0x%-6X  <- %s + 0x%X  (1 caller)"
                  % (site, entry, size, r[1], r[2]))
        else:
            print("  %08X in %08X  extent 0x%-6X  <- %d caller(s), %d with a literal lea%s"
                  % (site, entry, size, len(cs), len(leas),
                     "" if cs else " - NO caller found, so the storage is unknowable here"))
            for _a, e, r in leas:
                print("        from %08X: %s + 0x%X" % (e, r[1], r[2]))
    print()
    print("  %d forwarder(s) bind an extent to exactly one storage offset" % bound)
    return 0


if __name__ == "__main__":
    sys.exit(main())
