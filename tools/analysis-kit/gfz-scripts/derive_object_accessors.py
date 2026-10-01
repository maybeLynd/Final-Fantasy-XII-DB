#!/usr/bin/env python3
"""Derive, rather than guess, which functions RETURN a given object.

check_interior_escape.py needs `--returns`. Supplying it by hand is the one input that is not
evidence, and the whole escape result depends on it. But the closure already knows every member and
the register each one takes the object in, so the accessors are derivable FROM THE SAME DATA:

    call A                      <- candidate: does A return the object?
    ... rax reaches argreg a ...
    call B                      <- B is a closure member whose declared argreg IS a

then A's return value was accepted AS THE OBJECT by a function already proved to take it there. This
is a second fixed point over the closure, not a new kind of evidence.

THE OBVIOUS FAILURE and the guard against it: a function returning a DIFFERENT object that happens to
reach an overloaded member. So a candidate is admitted only with CONFIRMATIONS FROM >= 2 DISTINCT
BODIES, and every admitted accessor is printed with its sites so a reader can reject one.

Only d == 0 counts. An interior pointer `object+d` passed onward says nothing about what A returned.

THE BLIND SPOT, AND IT IS THE AWKWARD ONE. A confirmation requires the return value to be PASSED
ONWARD to a closure member. An accessor whose return is only ever STORED - never passed - therefore
has no confirmation site and is never admitted. `002367A0` is exactly that: its return is stored
straight into a global at `00302D2A`, which is the single true escape in S-14's battle-unit closure.
So this derivation is structurally blind to the accessor whose only observed use IS the escape the
escape check exists to find, and running the two together without noticing would quietly lose it.

That is a floor, not a silence: a derived set is a STARTING POINT to be added to by hand, and the
escape check must be told which accessors were derived and which were supplied. Do not read "the
derivation found no more" as "there are no more".

A SECOND BLIND SPOT, FOUND BY USING THE RESULT (2026-09-20). The battle-unit run ADMITTED
`0020E600`, and it is not an accessor for anything. Its whole body is ten bytes -
`mov eax,ecx / add rax,[rip->01F83530] / ret` - the engine's UNIVERSAL BASE-RELATIVE REFERENCE
DECODER, which the store already documents on `ActorWaitSlot.targetRef` as "resolves it as
arg + *(01F83530)". It returns a pointer into a shared arena and what type lives there depends
entirely on the offset handed to it; the same function serves the loot tier code at `00319A86`.
The >= 2 distinct bodies rule cannot catch this, because a universal decoder legitimately feeds
many consumers in many bodies - the guard is aimed at accidents, and this is not an accident.
`is_universal_decoder` below flags the shape so it cannot be admitted silently.

THREE INDEPENDENT SOURCES NOW AGREE ON `0020E600`, which is worth recording because the guard was
written from one of them. (1) Its ten bytes: `mov eax,ecx / add rax,[rip->01F83530] / ret`. (2) The
type store, on `ActorWaitSlot.targetRef`: "a BASE-RELATIVE reference to another actor record, not a
pointer and not a handle: 0020E600 resolves it as arg + *(01F83530)". (3) EXP-075, which stubbed it
in an isolated run and named it in its own words an "opaque-token resolver". None of the three was
produced with this guard in view. **The published
escape results were not affected** - the battle-unit escape came from the hand-supplied `002367A0`
and the control passed - but they could have been, and a set that admits a decoder would taint
every span it is used to clear.

CONTROL: over `bu_closure.tsv` this must re-derive `00236820`, which was identified by hand from
`00324923 call 00236820` / `00324928 mov r14, rax` / `0032493E mov rcx, rax` / `00324941 call
002FFEF0`. It does. It does NOT re-derive `002367A0`, for the reason above, and that is expected
rather than a defect to be tuned away.
"""
import argparse
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP          # noqa: E402
import disasm_fn as DF          # noqa: E402
import resolve_switch_arms as R  # noqa: E402

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG

VOLATILE = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")


def target(i):
    """the immediate target of a direct call, or None."""
    if i.mnemonic != "call" or not i.operands:
        return None
    if i.operands[0].type == X86_OP_REG:
        return None
    return getattr(i.operands[0], "imm", None)


def is_universal_decoder(img, md, ex, entry):
    """A tiny `base + arg` resolver, which is not an accessor for any one type.

    `0020E600` is the case that taught this: ten bytes, no call, no branch, and a single
    `add r64, [rip+X]` that adds a shared arena base to its argument. Everything it returns is "a
    pointer into that arena", so admitting it as type T's accessor would seed the escape check with
    every consumer of the arena. Shape, not address, so a sibling decoder is caught too.
    """
    if entry not in ex or ex[entry] > 24:
        return False
    try:
        ins = R.decode(img, md, entry, ex[entry])
    except SystemExit:
        return False
    adds_base = False
    for i in ins:
        if i.mnemonic in ("call", "jmp") or i.mnemonic.startswith("j"):
            return False
        if i.mnemonic == "add" and len(i.operands) == 2                 and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_MEM                 and i.operands[1].mem.base and i.reg_name(i.operands[1].mem.base) == "rip":
            adds_base = True
    return adds_base


def sweep(img, md, ex, entry, members):
    """confirmations found in one body: [(callee, site)]."""
    if entry not in ex:
        return []
    try:
        ins = R.decode(img, md, entry, ex[entry])
    except SystemExit:
        return []
    origin = {}          # reg -> the call whose return value it still holds (d == 0 only)
    out = []
    for i in ins:
        t = target(i)
        if i.mnemonic == "call":
            for a in ("rcx", "rdx", "r8", "r9"):
                if a in origin and t in members and members[t] == a:
                    out.append((origin[a], i.address))
            for v in VOLATILE:
                origin.pop(v, None)
            if t is not None:
                origin["rax"] = t
            continue
        made = None
        if i.mnemonic == "mov" and len(i.operands) == 2 \
                and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_REG:
            src = R.norm64(i.reg_name(i.operands[1].reg))
            if src in origin:
                made = (R.norm64(i.reg_name(i.operands[0].reg)), origin[src])
        w = set(R.norm64(i.reg_name(x)) for x in i.regs_access()[1])
        for d in list(origin):
            if d in w:
                del origin[d]
        if made:
            origin[made[0]] = made[1]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--closure", required=True)
    ap.add_argument("--min-bodies", type=int, default=2)
    a = ap.parse_args()

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    img = DF.Image(KP.EXE)
    ex = R.extents()
    raw = io.open(a.closure, encoding="utf-8", newline="").read().split("\n")
    head = raw[0].split("\t")
    I = {k: head.index(k) for k in head}
    rows = [c for c in (l.split("\t") for l in raw[1:] if l.strip())]
    members = {int(c[I["function"]], 16): c[I["argreg"]] for c in rows}

    hits = collections.defaultdict(list)   # callee -> [(body, site)]
    for f in members:
        for callee, site in sweep(img, md, ex, f, members):
            hits[callee].append((f, site))

    print("ACCESSOR DERIVATION over %s" % os.path.basename(a.closure))
    print("  closure members: %d" % len(members))
    print("  candidates with >=1 confirmation: %d" % len(hits))
    admitted = []
    for callee, sites in sorted(hits.items()):
        bodies = set(b for b, _ in sites)
        decoder = is_universal_decoder(img, md, ex, callee)
        if decoder:
            mark = "REFUSED - universal base-relative decoder, not a type's accessor"
        elif len(bodies) >= a.min_bodies:
            mark = "ADMITTED"
            admitted.append(callee)
        else:
            mark = "rejected (1 body)"
        print("    %08X  %2d confirmation(s) in %2d body(ies)  %s"
              % (callee, len(sites), len(bodies), mark))
        for b, s in sites[:3]:
            print("         body %08X site %08X" % (b, s))
    print()
    print("  --returns %s" % ",".join("%X" % c for c in admitted))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
