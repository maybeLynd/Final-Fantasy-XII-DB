#!/usr/bin/env python3
"""check_interior_escape.py - does a pointer INTO this object ever escape to memory?

THE MISSING HALF. A pool closure proves which functions hold an object, and scanning those bodies
proves which displacements they touch. Neither answers the question that decides whether "untouched"
means anything: **if a body computes `object + d` and stores that pointer somewhere, every later
read through it is invisible to both.** A span can look untouched across 200 bodies and still be
read every frame through a pointer handed out once.

Two major-system pages close that route by hand and nothing in this kit did it. S-14's battle-unit
page states the result plainly - *"a store of any tainted `unit+d` value into memory, over all 67
bodies. The only displacement that ever escapes is `+0x000` - the unit pointer itself, at
`00302D2A`, `00324957`, `00324DB5`, `00336869`"* - and S-01's boot singleton closes the same route.
This file makes that a repeatable check over any closure the generalised
`gen_actor_arg_closure.py` produces.

WHAT COUNTS AS AN ESCAPE, kept narrow so the answer means something:

  * `lea rX, [R + d]` where R holds the object taints rX with displacement d. `mov rX, R` taints it
    with d = 0.
  * `rax` after `call A` where A is in `--returns` taints with d = 0. AN ACCESSOR THAT RETURNS THE
    OBJECT IS HOW MOST BODIES GET IT, and without this the control reproduced 0 of 4. `--returns` is
    supplied per type and is the one input this check cannot derive: given none, it finds nothing and
    says nothing, so a run without it is not evidence.
  * A store `mov [anything], rX` of a tainted register is an ESCAPE at displacement d - UNLESS the
    destination is frame-derived, which is reported separately as a local buffer. The distinction is
    the whole point: a local array the body fills and hands on is the closure's business, while a
    store into a global or another object is a pointer a later reader can follow.
  * A tainted register passed as a call argument is reported SEPARATELY as a handoff, not as an
    escape - the closure already follows those, and conflating them would double-count the thing
    the closure exists to handle.

WHAT IS NOT FOLLOWED, and each is a hole in the floor rather than a silence:

  * taint through arithmetic other than `lea`, through the stack, or through a second register copy
    chain longer than one hop;
  * stores of a tainted value into a register-indirect address whose base this does not resolve -
    counted, because the escape is real even when its destination is not known;
  * taint that survives a call in a volatile register - `rax`, `rcx`, `rdx`, `r8`-`r11` are dropped
    at every call, which is correct for the ABI but loses a value the callee happens to preserve;
  * nothing, in the frame-address case - that hole is CLOSED. Frame-derived registers are now
    tracked through `lea` and register copies, so `lea r12,[rsp+0x70]` / `lea r12,[r12+rax*8]` /
    `mov [r12], rbx` is reported as a FRAME-LOCAL store rather than an escape. It had to be: in
    003247F0 that is the shape of every store the check finds.

So a reported escape is a fact and an empty report is a FLOOR. The control is S-14: run over the
battle-unit closure it must find `+0x000` escaping and must find it at the sites the page names,
because a check that cannot reproduce a known positive proves nothing by its silence.

CONTROL STATUS: PASSES, at 3 of 4 - and 3 is the ceiling, not a shortfall. The control counts a site
whether it lands in the frame or outside it, because both kinds appear among the four.

CORRECTION, 2026-09-20 (OPUS). THIS BLOCK PREVIOUSLY CLAIMED that the page's list "mixes the two" and
that naming which is which was "this check's contribution over the hand run". THAT IS WRONG, and the
error was mine for reading the CONTRACT's one-line summary instead of the page. `battleunit-slot-pool-
and-actor-class.md` already gives every site a destination AND a reader: `00302D2A` to the global
`022C17A8` with "exactly one body references that global - the one that wrote it"; `00324957` and
`00324DB5` to "`[rsp+0x70]`, a **stack** array of pointers", read by "nobody - the buffer is never
passed to any call in that body"; and `00336869` to `ctx+0xF0`, followed out through 28 bodies to
`+0x698`, `+0x714`, `+0x768`, `+0x76C`, `+0xE68` and nowhere else. The hand run also measured that
every handoff target is a DIRECT call, so no dispatch hatch exists.

WHAT THIS CHECK ACTUALLY ADDS is therefore corroboration and reach, not a distinction the page lacked:
it performs the classification MECHANICALLY over any closure the kit can build, and it INDEPENDENTLY
REPRODUCES the page's result - one body for the global, frame-local for the two in `003247F0`. A
second instrument agreeing with a hand run is worth having. Claiming it saw something the hand run
missed was not. `00336869` lies in
`00336710`, which this closure does not contain, so no amount of tracking reaches it; the other three
are all inside the closure and all reproduce, at exactly one displacement, `+0x000`. That is the
page's conclusion re-derived rather than restated. It got there through two failures worth keeping:
tracking one register instead of a set (the compiler parks the argument immediately), and stopping
when the last tainted register died - which threw away every escape after the object's register was
first reused, and is precisely what hid `00302D2A`, a store of an accessor's return INTO A GLOBAL
0x125A bytes into its body.
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

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_OP_REG
except ImportError:
    sys.stderr.write("check_interior_escape: needs capstone\n")
    raise SystemExit(2)

ARGREGS = ("rcx", "rdx", "r8", "r9")


def scan(img, md, ex, entry, reg, returns=(), slots=()):
    """(escapes, frame-locals, handoffs, decoded) for one body; each list is [(site, disp)]."""
    if entry not in ex:
        return [], [], [], False
    try:
        ins = R.decode(img, md, entry, ex[entry])
    except SystemExit:
        return [], [], [], False
    # THE OBJECT IS A SET OF REGISTERS, NOT ONE REGISTER. The first version tracked only the
    # closure's declared argreg and killed everything when that register was written - which is
    # exactly what a compiler does on entry. `003247F0` opens by parking the argument in a
    # callee-saved register and later restores it with `mov rcx, r14`; killing the taint at the
    # first write to rcx lost the object while r14 still held it, and with it the escape at
    # 00324957. `holds` maps EVERY register currently holding object+d, propagates across copies
    # and `lea`, and each register dies on its own write rather than taking the others with it.
    holds = {reg: 0}
    # FRAME-DERIVED DESTINATIONS, TRACKED RATHER THAN GUESSED AT. Comparing a store's base register
    # against rsp/rbp catches `mov [rsp+0x50], rdi` and misses `lea r12,[rsp+0x70]` /
    # `lea r12,[r12+rax*8]` / `mov [r12], rbx` - which is not a corner case: in 003247F0 that is the
    # shape of EVERY store this check finds, five branches filling ONE local array at +0x70. A store
    # into the current frame is a local collection buffer, not a pointer left where a later reader
    # can find it, and the two must be reported apart or the count means nothing.
    frame = set()
    esc, local, hand = [], [], []
    # NO EARLY EXIT WHEN `holds` EMPTIES. With return-value taint an accessor called later in the
    # body re-seeds the object, so stopping at the first moment nothing is tainted throws away every
    # escape after the object's register is first reused. That is what hid 00302D2A - a store of the
    # accessor's return INTO A GLOBAL, 0x125A bytes into 00301AD0 - and removing the exit is what
    # took the control from 2 of 4 to its 3-of-4 ceiling.
    for i in ins:
        w = set(R.norm64(i.reg_name(x)) for x in i.regs_access()[1])
        taint = holds
        # a store of a tainted register into memory is the escape we are looking for
        if i.mnemonic in ("mov", "movq") and len(i.operands) == 2 \
                and i.operands[0].type == X86_OP_MEM and i.operands[1].type == X86_OP_REG:
            src = R.norm64(i.reg_name(i.operands[1].reg))
            dstb = i.operands[0].mem.base
            dst = R.norm64(i.reg_name(dstb)) if dstb else None
            # A STACK SPILL IS NOT AN ESCAPE, and counting it as one was this file's only "finding".
            # 00311FBB `mov qword ptr [rsp+0x50], rdi` stores a tainted copy into the CURRENT
            # FRAME, and the next instruction is `lea rcx, [rsp+0x40]` building a local record to
            # pass on - a handoff the closure already follows, not a pointer left where a later
            # reader can find it. The escape that matters lands in a global, a heap object or
            # another record; `rsp`/`rbp` destinations are excluded.
            if src in taint:
                if dst in ("rsp", "rbp") or dst in frame:
                    local.append((i.address, taint[src]))
                else:
                    esc.append((i.address, taint[src]))
        # a tainted register in an argument slot is a HANDOFF, which the closure already follows
        rax_taint = None
        if i.mnemonic == "call":
            for a in ARGREGS:
                if a in taint:
                    hand.append((i.address, taint[a]))
            # AN ACCESSOR RETURNING THE OBJECT taints rax. This is how most bodies obtain it, and
            # 00324928 `mov r14, rax` after `call 00236820` is why the four-site control read 0.
            if i.operands and i.operands[0].type != X86_OP_REG \
                    and getattr(i.operands[0], "imm", None) in returns:
                rax_taint = 0
            # a call clobbers the volatile registers, so taint in them does not survive it
            for v in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
                holds.pop(v, None)
        # taint creation: lea rX, [R + d]  /  mov rX, R
        made = None
        # A GLOBAL SLOT HOLDING THE OBJECT is the third way a body obtains one, and for some types it
        # is the ONLY way. BattleSystemState is interior to the save image buffer and reached through
        # *(void**)0x02EBF190, so no accessor returns it and no argument carries it into most bodies:
        # derive_object_accessors admits nothing for it, correctly. `mov rX, [rip+d]` resolving to a
        # listed slot taints rX with d = 0.
        if i.mnemonic == "mov" and len(i.operands) == 2                 and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_MEM                 and i.operands[1].mem.base and i.reg_name(i.operands[1].mem.base) == "rip"                 and not i.operands[1].mem.index                 and (i.address + i.size + i.operands[1].mem.disp) in slots:
            made = (R.norm64(i.reg_name(i.operands[0].reg)), 0)
        elif i.mnemonic == "lea" and len(i.operands) == 2 \
                and i.operands[1].type == X86_OP_MEM and i.operands[1].mem.base \
                and not i.operands[1].mem.index \
                and R.norm64(i.reg_name(i.operands[1].mem.base)) in holds:
            b = R.norm64(i.reg_name(i.operands[1].mem.base))
            made = (R.norm64(i.reg_name(i.operands[0].reg)),
                    holds[b] + i.operands[1].mem.disp)
        elif i.mnemonic == "mov" and len(i.operands) == 2 \
                and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_REG \
                and R.norm64(i.reg_name(i.operands[1].reg)) in holds:
            made = (R.norm64(i.reg_name(i.operands[0].reg)),
                    holds[R.norm64(i.reg_name(i.operands[1].reg))])
        # a frame address propagates through `lea` and a register copy exactly as the object does
        fmade = None
        if i.mnemonic == "lea" and len(i.operands) == 2 and i.operands[1].type == X86_OP_MEM:
            fb = i.operands[1].mem.base
            fbn = R.norm64(i.reg_name(fb)) if fb else None
            if fbn in ("rsp", "rbp") or fbn in frame:
                fmade = R.norm64(i.reg_name(i.operands[0].reg))
        elif i.mnemonic == "mov" and len(i.operands) == 2 \
                and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_REG \
                and R.norm64(i.reg_name(i.operands[1].reg)) in frame:
            fmade = R.norm64(i.reg_name(i.operands[0].reg))
        for d in list(holds):
            if d in w:
                del holds[d]
        frame -= w
        if fmade:
            frame.add(fmade)
        if made:
            holds[made[0]] = made[1]
        if rax_taint is not None:
            holds["rax"] = rax_taint
    return esc, local, hand, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--closure", required=True,
                    help="a TSV from gen_actor_arg_closure.py (function, argreg columns)")
    ap.add_argument("--span", help="lo:hi in hex - report only escapes landing in this span")
    ap.add_argument("--returns", default="",
                    help="comma-separated hex accessors that RETURN this object; without them "
                         "nothing is tainted through a call and the run is not evidence")
    ap.add_argument("--slots", default="",
                    help="comma-separated hex GLOBAL SLOTS holding a pointer to this object; a load "
                         "from one taints the destination. For a type reached only through a global "
                         "- an interior singleton, say - this is the only seeding route there is.")
    a = ap.parse_args()
    ret = set(int(x, 16) for x in a.returns.split(",") if x.strip())
    slot = set(int(x, 16) for x in a.slots.split(",") if x.strip())

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    img = DF.Image(KP.EXE)
    ex = R.extents()
    raw = io.open(a.closure, encoding="utf-8", newline="").read().split("\n")
    head = raw[0].split("\t")
    I = {k: head.index(k) for k in head}
    fns = [(int(c[I["function"]], 16), c[I["argreg"]])
           for c in (l.split("\t") for l in raw[1:] if l.strip())]

    esc_all, loc_all, hand_all, decoded = [], [], [], 0
    for f, reg in fns:
        e, lo_, h, ok = scan(img, md, ex, f, reg, ret, slot)
        if ok:
            decoded += 1
        esc_all.extend((f,) + x for x in e)
        loc_all.extend((f,) + x for x in lo_)
        hand_all.extend((f,) + x for x in h)

    lo = hi = None
    if a.span:
        lo, hi = (int(x, 16) for x in a.span.split(":"))
        esc_all = [x for x in esc_all if lo <= x[2] < hi]
        loc_all = [x for x in loc_all if lo <= x[2] < hi]

    print("INTERIOR-POINTER ESCAPE over %s" % os.path.basename(a.closure))
    print("  closure functions : %d   bodies decoded: %d" % (len(fns), decoded))
    if a.span:
        print("  restricted to span +0x%X..+0x%X" % (lo, hi))
    bydisp = collections.Counter(x[2] for x in esc_all)
    print("  ESCAPES           : %d store(s) at %d distinct displacement(s)"
          % (len(esc_all), len(bydisp)))
    for d, n in sorted(bydisp.items()):
        sites = [x[1] for x in esc_all if x[2] == d]
        print("      +0x%-6X %2d store(s)   %s" % (d, n, " ".join("%08X" % s for s in sites[:6])))
    locdisp = collections.Counter(x[2] for x in loc_all)
    print("  FRAME-LOCAL stores (a local buffer, NOT an escape) : %d at %d displacement(s)"
          % (len(loc_all), len(locdisp)))
    for d, n in sorted(locdisp.items()):
        sites = [x[1] for x in loc_all if x[2] == d]
        print("      +0x%-6X %2d store(s)   %s" % (d, n, " ".join("%08X" % s for s in sites[:6])))
    print("  handoffs (a tainted interior pointer passed as an argument) : %d" % len(hand_all))
    print()
    print("  AN EMPTY REPORT IS A FLOOR. Taint through arithmetic other than `lea` or through the")
    print("  stack is not followed, volatile registers are dropped at every call, and a body whose")
    print("  accessors are absent from --returns is never seeded at all - so silence here can mean")
    print("  only that the check was not told where to look.")
    print()
    # THE CONTROL, AND IT FAILS. S-14's page closed this exact route by hand over 67 bodies and
    # states the answer: the only escaping displacement is +0x000, at 00302D2A, 00324957, 00324DB5
    # and 00336869. Run over the battle-unit closure this file finds the right DISPLACEMENT and
    # ONE of the four SITES. That is not a pass and it is not presented as one.
    if os.path.basename(a.closure).startswith("bu_"):
        # S-14 names four sites. THREE ARE REACHABLE AND ALL THREE MUST REPRODUCE; 00336869 is in
        # 00336710, which this closure does not contain, so it is excluded BY POPULATION rather than
        # forgiven - `f <= site < f + ex[f]` over the closure decides which bucket a site is in, and
        # note that ex[] holds a LENGTH, not an end address.
        KNOWN = {0x302D2A, 0x324957, 0x324DB5}
        OUT_OF_POPULATION = {0x336869}
        got = set(x[1] for x in esc_all) | set(x[1] for x in loc_all)
        found = KNOWN & got
        # THE DISPLACEMENT RULE APPLIES TO ESCAPES ONLY. Unioning the frame-locals in made the
        # control fail on +0x6D4, +0x6D8 and +0xBC0 - which are spills of an interior pointer into
        # the body's OWN frame, not pointers left where a later reader can follow them. A spill is
        # exactly what the page's rule is not about, and counting it broke the rule's own test.
        disps = set(x[2] for x in esc_all)
        print("  CONTROL against S-14's hand-closed route (four sites, all at +0x000):")
        print("      in-population sites reproduced: %d of %d   %s"
              % (len(found), len(KNOWN), " ".join("%08X" % s for s in sorted(found)) or "(none)"))
        print("      excluded by population: %s (body 00336710 is not in this closure)"
              % " ".join("%08X" % s for s in sorted(OUT_OF_POPULATION)))
        if found == KNOWN and disps == {0}:
            print("      PASS - every reachable site reproduced, at exactly one displacement")
            print("      (+0x000), which is the page's conclusion re-derived rather than restated.")
            print("      THIS IS NOT A LICENCE TO READ SILENCE AS ABSENCE on another type: the")
            print("      result depends entirely on --returns, which is supplied by hand.")
            return 0
        if disps - {0}:
            print("      **FAIL - an escape at a displacement the page does not allow**: %s"
                  % " ".join("+0x%X" % d for d in sorted(disps - {0})))
            return 2
        if not ret and not slot:
            print("      NOT A RESULT - no --returns given, so no call return was tainted and this")
            print("      run cannot reproduce anything. Supply the accessors.")
            return 2
        if len(found) != len(KNOWN):
            print("      **FAIL - THIS INSTRUMENT IS WEAKER THAN THE HAND RUN**, and the two")
            print("      mechanisms it cannot see are named rather than left as a gap:")
            print("        1. A POINTER RETURNED BY A CALL is never tainted. 00302D2A stores rax")
            print("           straight from `call 002367A0`, an accessor returning the object. The")
            print("           page seeded by 'tainting the accessor's RETURN VALUE'; this does not.")
            print("        2. 00324957 IS THE SAME CAUSE, TRACED TO THE END. The store is")
            print("           `mov [r13], r14`, and r14 is not the `lea r14,[rdi+0xbc0]` earlier in")
            print("           the body - that value is spilled and never reloaded. 00324928")
            print("           `mov r14, rax` overwrites it with the return of `call 00236820`, an")
            print("           index->unit accessor, so the escape IS at +0x000 as the page says.")
            print("        3. 00336869 is in 00336710, which this closure does not contain at all -")
            print("           a population difference rather than a tracking gap.")
            print("      So an empty or short report here CANNOT be read as 'no escape'. Use it to")
            print("      CONFIRM escapes it does find; do not use its silence to promote a span.")
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
