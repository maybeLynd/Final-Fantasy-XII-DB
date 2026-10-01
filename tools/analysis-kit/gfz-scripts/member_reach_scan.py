#!/usr/bin/env python3
"""member_reach_scan.py - which bodies provably take THIS object, and what do they touch?

THE SET OF BODIES IS THE WHOLE PROBLEM, and getting it wrong is silent. The first version of this
scan took every listed body in a class's address neighbourhood - for `CharacterRenderObject`,
the 108 bodies in `[001F4000, 001FC000)` - and reported accesses at `+0x80`, `+0xA8`, `+0x1C0`,
`+0x1E0` and more. Every one was worthless. Most bodies in that range take some OTHER object in
`rcx`, so what they touched was their own first argument. **Address adjacency is not membership**,
and the corpus already refuses that inference for fields; it is no better for methods.

So the set is built rather than assumed. THREE SEEDING SHAPES, and choosing the wrong one is the
single most expensive mistake this tool can make - each of them has now hidden a real finding:

    --vtable    every slot of the vtable, plus every body that INSTALLS it (found per-body).
                `CharacterRenderObject`'s constructor is not a slot, and it held the answer.
    --accessor  the CALLERS of an accessor, with its RETURN VALUE tainted, plus the accessor
                bodies themselves. `BattleUnit` had a third accessor nobody had seeded.
    --slot      every body that LOADS a singleton's pointer slot.

**--accessor and --slot are not interchangeable, and the counts tell you which to use.**
`BootSingleton01F7F598` has THREE slot loaders against 117 callers of its one-instruction accessor,
so seeding from its slot sees almost nothing - that is exactly how 160 of its bytes sat
"unobserved". (Four bodies *reference* that slot; the fourth only `cmp`s it against zero and never
loads it, so it is not a seed. Reference and load are different counts and this tool wants the
load.) `ManagerSingleton0209BE80` has no accessor at all and 136 loaders, so there the slot
IS the seed. Count both before trusting either.

    closure  when a member body hands `this` ITSELF - displacement 0 - to a callee in `rcx`,
             that callee's `rcx` is the same object, so it joins the set.

A handoff at a NON-zero displacement is recorded and never followed: `lea rcx,[this+0x118]` makes
the callee's `rcx` a sub-object whose offsets are relative to that, not to `this`.

FOUR things are reported, because a census keyed on direct displacements sees only the first, and
because the other three are what decide how much a silence is worth:

    DIRECT    [this+disp]
    HANDOFF   lea reg,[this+disp] ; ... ; call F    with reg still in an argument register
    ESCAPE    a this+disp value STORED INTO MEMORY - the route a register closure cannot follow
    INDIRECT  a handoff whose target is not a literal - virtual dispatch, which the closure stops at

**A HANDOFF IS AN UPPER BOUND, NOT A FACT.** What is recorded is an object-tainted value sitting
in an argument register at a call; whether the callee *reads* that register is a different
question. `CharacterRenderObject` has three calls to an unbound import thunk (`008C2CC8`, whose
stored value is not a valid address in this image) that appear as `+0x000` handoffs purely because
nothing had overwritten `rcx`. Use handoffs to rule things IN; never to count them.

**A span reported as untouched is only as strong as those last two.** `BattleUnit`'s `+0x298`
(1016 bytes) is untouched with **no indirect handoffs at all** and exactly one escaping
displacement - `+0x000`, whose four sites are a write-only global, a stack array never passed to
a call, and a solver context that reads the unit at five offsets outside the span - so that
negative is exhaustive over static routes. `CharacterRenderObject`'s six spans are untouched too,
but that closure **does** hand `this` to `qword ptr [r10+0x98]` and friends, so its negative is
bounded by vtable slots nobody has resolved. Same word, very different claims.

WHAT IT FOUND FIRST TIME OUT, and the trap inside it. On `CharacterRenderObject` the constructor
turned out to zero-fill `+0x78..+0x38F` as ONE 792-byte unit, which accounted for 776 of that
type's 894 unknown bytes as one region instead of two gaps. The scan ALSO reported nine offsets at
an exact `0x10` stride inside it - `+0x88` through `+0x108` - and **those are not nine fields**.
They are the unrolled copy's `movups` displacements. Stride, count and alignment all looked like
corroboration for a lattice of 16-byte elements that does not exist. A tool that reports
displacements will hand you the material for a fictional layout; this docstring is the warning
that ships with it.

THREE MECHANISM NOTES, each of which was a wrong answer first:

* **The accessor BODIES are members too.** Pool mode seeds from an accessor's *callers*, which
  leaves the accessors themselves out - and on `BattleUnit` that omitted
  `BattleUnit_AllocateSlotAndBindActor`, the one body most likely to write a back-pointer into the
  actor record, i.e. exactly the route an unreachability claim has to rule out. They are added to
  the member set explicitly now. The hole was found by reading `check_absence_claims.py`'s warning
  about `UQ-339`, an unrelated wrong *"nothing reads this"* claim, and asking what the analogous
  blind spot was here.

* **Find vtable installers per body, never by sweeping `.text`.** A linear disassembly from
  `00121000` desynchronises on the first padding or data run and then decodes garbage. It reported
  ZERO installers for a class whose own store row says "installed by the constructor". Every
  listed body starts on a real instruction, so disassembling from each entry stays in sync.
* **RBX/RBP/RSI/RDI/R12-R15 survive a call.** Clearing all taint at a call hid the largest
  unexplained span in another type entirely; the control for that lives in `arg_extent_scan.py`.

    python member_reach_scan.py --self-test
    python member_reach_scan.py --vtable 0x00903B68 --size 0x668
    python member_reach_scan.py --vtable 0x00903B68 --size 0x668 --gaps 0x80:144,0x118:632
    python member_reach_scan.py --accessor 0x00189120 --size 0xDD8
    python member_reach_scan.py --slot 0x0209BE80 --size 0x10000
"""
import argparse
import bisect
import collections
import os
import struct
import sys

import kit_paths as KP
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import (X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP, X86_REG_RAX, X86_REG_RCX,
                          X86_REG_RDX, X86_REG_R8, X86_REG_R9, X86_REG_RBX, X86_REG_RBP,
                          X86_REG_RSI, X86_REG_RDI, X86_REG_R12, X86_REG_R13, X86_REG_R14,
                          X86_REG_R15)

import capstone.x86 as _x86
import check_literal_citations as CLC   # the PE reader, already controlled
import reg_tracking as RT  # noqa: E402  (access direction: op_kind)

FUNCS = os.path.join(KP.WORK, "graph", "functions.tsv")
NONVOL = frozenset((X86_REG_RBX, X86_REG_RBP, X86_REG_RSI, X86_REG_RDI,
                    X86_REG_R12, X86_REG_R13, X86_REG_R14, X86_REG_R15))
ARGREGS = (X86_REG_RCX, X86_REG_RDX, X86_REG_R8, X86_REG_R9)

# Set to a list by --census-out; each direct access appends its instruction.
CENSUS = None


#: SUB-REGISTER ALIASING. A write to `eax` clears `rax`, and a taint map keyed on the 64-bit id
#  does not see it unless told. Missing this produced a FALSE ESCAPE that read as a real route:
#  in `SaveSlotTransaction_StateMachine`, `00581DCA call 002EF640` taints rax with the save buffer,
#  `00581E06 xor eax, eax` zeroes it, and `00581E0E mov qword ptr [rdi], rax` then stores ZERO into
#  the buffer - which the scan reported as the buffer pointer escaping to memory. Following it as a
#  route cost a round. Capstone exposes no parent lookup, so the map is built once here.
_PARENT = {}
for _wide, _parts in (
        (X86_REG_RAX, ("EAX", "AX", "AL", "AH")), (X86_REG_RBX, ("EBX", "BX", "BL", "BH")),
        (X86_REG_RCX, ("ECX", "CX", "CL", "CH")), (X86_REG_RDX, ("EDX", "DX", "DL", "DH")),
        (X86_REG_RSI, ("ESI", "SI", "SIL")), (X86_REG_RDI, ("EDI", "DI", "DIL")),
        (X86_REG_RBP, ("EBP", "BP", "BPL")),
        (X86_REG_R8, ("R8D", "R8W", "R8B")), (X86_REG_R9, ("R9D", "R9W", "R9B")),
        (X86_REG_R12, ("R12D", "R12W", "R12B")), (X86_REG_R13, ("R13D", "R13W", "R13B")),
        (X86_REG_R14, ("R14D", "R14W", "R14B")), (X86_REG_R15, ("R15D", "R15W", "R15B"))):
    _PARENT[_wide] = _wide
    for _nm in _parts:
        _r = getattr(_x86, "X86_REG_" + _nm, None)
        if _r is not None:
            _PARENT[_r] = _wide


def _wide_reg(r):
    """The 64-bit register a write to `r` clobbers."""
    return _PARENT.get(r, r)


def load_funcs():
    sizes, names = {}, {}
    for line in open(FUNCS, encoding="utf-8", errors="replace"):
        f = line.rstrip("\n").split("\t")
        if len(f) > 2 and len(f[0]) == 8:
            try:
                sizes[int(f[0], 16)] = int(f[2])
                names[int(f[0], 16)] = f[1]
            except ValueError:
                pass
    return sizes, names


def scan_body(img, md, va, size, objsize):
    """A body whose `rcx` on entry IS the object. -> direct, handoff, passes_this, escapes"""
    return _walk(img, md, va, size, objsize, {X86_REG_RCX: 0}, None)


def slot_loaders(img, sizes, slot):
    """Bodies containing `mov reg, [rip -> slot]`. The seed for a singleton reached by its slot."""
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    out = set()
    for a in sorted(sizes):
        _s, b = img.at(a, sizes[a])
        if not b:
            continue
        for i in md.disasm(b, a):
            ops = i.operands
            if i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP:
                if i.address + i.size + ops[1].mem.disp == slot:
                    out.add(a)
                    break
    return out


def run_slot(img, sizes, slot, objsize):
    """Seed from the bodies that LOAD a singleton's pointer slot.

    THE THIRD SEEDING SHAPE, and it is not interchangeable with the second. Some singletons are
    reached through a one-instruction accessor and almost never by loading the slot
    (`BootSingleton01F7F598`: three loaders against 117 accessor callers - reading the slot alone
    missed 160 bytes). Others have no accessor at all and are loaded everywhere
    (`ManagerSingleton0209BE80`: 136 loaders). **Check which before trusting either.**
    """
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    seed = slot_loaders(img, sizes, slot)
    members = set(seed)
    work = list(seed)
    direct = collections.Counter()
    handoff = collections.defaultdict(set)
    escapes = collections.defaultdict(set)
    reached = []
    while work:
        fn = work.pop()
        if fn not in sizes:
            continue
        if fn in seed:
            d, h, pt, e = _walk(img, md, fn, sizes[fn], objsize, {}, None, slot=slot)
        else:
            d, h, pt, e = scan_body(img, md, fn, sizes[fn], objsize)
        direct.update(d)
        for o, cs in h.items():
            handoff[o] |= cs
        for o, cs in e.items():
            escapes[o] |= cs
        for c in pt:
            if c not in members and c in sizes:
                members.add(c)
                reached.append(c)
                work.append(c)
    return sorted(seed), set(), reached, members, direct, handoff, escapes


def _walk(img, md, va, size, objsize, seed_taint, accessors, slot=None):
    """The shared walk.

    `seed_taint` starts it. `accessors`, when given, re-seeds `rax` after a call to one of them,
    which is how a POOLED type is entered - the object arrives as a return value, not an argument.

    Returns four things, and the last two exist because the first two cannot answer
    "does anything read this span?" on their own:

        direct       {off: count}        [obj+disp]
        handoff      {off: {target}}     lea obj+disp into an argument register at a call
        passes_this  {callee}            a DIRECT call receiving the object itself - the closure
        escapes      {off: {site}}       obj+disp STORED INTO MEMORY

    ESCAPES ARE THE THIRD ROUTE and neither of the first two can see it: a closure follows
    registers, so an address written into another structure leaves its world entirely. On
    `BattleUnit` the only escaping displacement was `+0x000`, the object pointer itself, at four
    sites that all turned out to be dead ends - which is what let a 1016-byte span be called
    unread rather than merely unobserved.

    INDIRECT TARGETS ARE THE FOURTH, and the caller must look at them: a `handoff` target that is
    not a `0x…` literal is an indirect or virtual call, and `passes_this` cannot follow it. The two
    types this was built on differ exactly here - `BattleUnit` has **none**, so its closure is
    complete, while `CharacterRenderObject` passes `this` to `qword ptr [r10+0x98]` and friends,
    so its negative is bounded by whatever those vtable slots resolve to. **A silence from a
    closure with indirect handoffs in it is a much weaker result than the same silence without.**
    """
    _n, b = img.at(va, size)
    if not b:
        return {}, {}, set(), {}
    direct = collections.Counter()
    handoff = collections.defaultdict(set)
    escapes = collections.defaultdict(set)
    passes_this = set()
    tainted = dict(seed_taint)
    argonly = {}          # produced by `add reg, imm`: usable as a CALL ARGUMENT, never as a base
    for i in md.disasm(b, va):
        m, ops = i.mnemonic, i.operands
        if m == "call":
            for r in ARGREGS:
                if r in tainted:
                    handoff[tainted[r]].add(i.op_str)
                elif r in argonly:
                    handoff[argonly[r]].add(i.op_str)
            direct_target = None
            if ops and ops[0].type != X86_OP_MEM:
                try:
                    direct_target = int(i.op_str, 16)
                except ValueError:
                    direct_target = None
            if tainted.get(X86_REG_RCX) == 0 and direct_target is not None:
                passes_this.add(direct_target)
            tainted = {r: d for r, d in tainted.items() if r in NONVOL}
            argonly = {r: d for r, d in argonly.items() if r in NONVOL}
            if accessors is not None and direct_target in accessors:
                tainted[X86_REG_RAX] = 0
            continue
        # A TAIL JMP PASSES ARGUMENTS AND NEVER RETURNS, so it is a handoff and this used to miss
        # every one of them. `ManagerSingleton0209BE80` is wired almost entirely with 19-byte
        # thunks - load the slot, `add rcx, <child offset>`, `jmp <handler>` - and there are 43.
        # Reporting only `call` sites made two of its children look ownerless when `_8FA0` in fact
        # has fourteen owners, and that wrong claim reached a published contract. The caveat was in
        # this docstring at the time; a documented blind spot is still a blind spot.
        if m == "jmp":
            # A JMP INSIDE THIS BODY IS A LOCAL BRANCH, NOT A TAIL CALL. Recording every one of
            # them as a handoff inflates the count for any body with a loop: `00289F50` jumps to
            # its own `0028A054` while rcx is tainted, and that appeared as a handoff of
            # `ManagerSub0209BE80_5380+0x36A` to a function that does not exist.
            _t = None
            if ops and ops[0].type != X86_OP_MEM:
                try:
                    _t = int(i.op_str, 16)
                except ValueError:
                    _t = None
            if _t is not None and va <= _t < va + size:
                continue
            for r in ARGREGS:
                if r in tainted:
                    handoff[tainted[r]].add(i.op_str + " (tail)")
                elif r in argonly:
                    handoff[argonly[r]].add(i.op_str + " (tail)")
            if tainted.get(X86_REG_RCX) == 0 and ops and ops[0].type != X86_OP_MEM:
                try:
                    passes_this.add(int(i.op_str, 16))
                except ValueError:
                    pass
            continue
        if m == "ret":
            continue
        # `add reg, imm` ONLY COUNTS AS ADDRESS ARITHMETIC WHEN A TAIL JMP FOLLOWS IT IMMEDIATELY,
        # which is the thunk shape: `mov rcx,[rip->slot]` / `add rcx, <child>` / `jmp handler`.
        #
        # Taking it generally - as the first version of this did - manufactures fields. A register
        # that held the object is freely reused as a scratch index: in
        # `BattleUnit_RebuildPerceptionCandidateCache`, `00324D9C add rax, 0x375` then
        # `00324DA2 lea rax,[rdi + rax*4]` uses it as an ELEMENT INDEX, and carrying the taint
        # through invented an access at `unit+0x375` - inside the very span whose emptiness this
        # tool had been used to establish. One line, one phantom field, in the worst possible place.
        # So the add is held pending and committed only if the very next instruction is that jmp.
        if m == "add" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[0].reg in tainted \
                and ops[1].type == X86_OP_IMM:
            argonly[ops[0].reg] = tainted[ops[0].reg] + ops[1].imm
            del tainted[ops[0].reg]
            continue
        if m == "add" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[0].reg in argonly                 and ops[1].type == X86_OP_IMM:
            argonly[ops[0].reg] += ops[1].imm
            continue
        if slot is not None and m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP:
            if i.address + i.size + ops[1].mem.disp == slot:
                tainted[ops[0].reg] = 0
                continue
        if m in ("mov", "movq") and len(ops) == 2 and ops[0].type == X86_OP_MEM:
            if ops[1].type == X86_OP_REG and ops[1].reg in tainted:
                escapes[tainted[ops[1].reg]].add("%08X" % i.address)
        # A LEA THAT DOES NOT DERIVE FROM THE OBJECT STILL OVERWRITES ITS DESTINATION. The kill
        # loop below skips `lea` (so `lea rax,[rax+0x10]` can retarget rax), which meant a
        # completely unrelated `lea rax,[rip - 0x461DF7]` left the stale taint in place: the jump
        # table it then indexed was reported as an indexed access into the save buffer at
        # `+0x461E20`. Propagate when the base is tainted, CLEAR otherwise.
        if m == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM:
            base = ops[1].mem.base
            if base in tainted and ops[1].mem.index == 0:
                tainted[ops[0].reg] = tainted[base] + ops[1].mem.disp
            else:
                _w = _wide_reg(ops[0].reg)
                tainted.pop(_w, None)
                argonly.pop(_w, None)
            continue
        if m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG:
            if ops[1].type == X86_OP_REG and ops[1].reg in tainted:
                tainted[ops[0].reg] = tainted[ops[1].reg]
                continue
        for oi, op in enumerate(ops):
            if op.type == X86_OP_MEM and op.mem.base in tainted and op.mem.base != X86_REG_RIP:
                off = tainted[op.mem.base] + op.mem.disp
                if 0 <= off < objsize:
                    direct[off] += 1
                    # THE INSTRUCTION, NOT ONLY THE COUNT. This scan proves the strongest member
                    # set in the kit - 195 bodies for BootSingleton01F7F598 against the 3 a
                    # slot-seeded census finds - and then reported each offset as a bare tally.
                    # A tally cannot say whether a field is a float, a pointer or signed, so the
                    # richest census here could not feed infer_field_type.py at all. Recording
                    # the instruction costs nothing and closes that.
                    if CENSUS is not None:
                        CENSUS.append((va, i.address, off,
                                       RT.op_kind(i, op, oi),
                                       i.mnemonic + " " + i.op_str))
        # register kills from the shared policy (reg_tracking.written), lea excluded as before (OPUS 2026-09-28)
        if m != "lea":
            _wn = RT.written(i)
            for _k in [k for k in tainted if RT.canon(i.reg_name(k)) in _wn]:
                tainted.pop(_k, None)
            for _k in [k for k in argonly if RT.canon(i.reg_name(k)) in _wn]:
                argonly.pop(_k, None)
    return direct, handoff, passes_this, escapes


def scan_body_after_accessor(img, md, va, size, accessors, objsize):
    """A POOLED type has no vtable to enumerate, so the object is seeded from its ACCESSOR's
    RETURN VALUE instead: after `call BattleUnit_GetBySlotIndex`, rax IS a BattleUnit.

    Same four outputs as scan_body. The volatile-register rule is the one that matters everywhere
    else in this file: rax is clobbered by the next call, so the taint has to die there unless it
    was copied into a callee-saved register first - which is exactly what these bodies do.
    """
    return _walk(img, md, va, size, objsize, {}, accessors)


def installers_of(img, sizes, vtable):
    """Bodies that form the vtable's address. PER BODY - a linear .text sweep desynchronises."""
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    out = set()
    for a in sorted(sizes):
        _s, body = img.at(a, sizes[a])
        if not body:
            continue
        for i in md.disasm(body, a):
            for op in i.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    if i.address + i.size + op.mem.disp == vtable:
                        out.add(a)
    return out


def slots_of(img, vtable, cap=64):
    _n, vt = img.at(vtable, 8 * cap)
    out = []
    for i in range(cap):
        q = struct.unpack_from("<Q", vt, i * 8)[0]
        sec, _x = img.at(q, 1) if q else (None, None)
        if sec != ".text":
            break
        out.append(q)
    return out


def run_pool(img, sizes, accessors, objsize):
    """Seed from the CALLERS of a pooled type's accessor, tainting its return value."""
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    import call_graph as G
    callers, _ce, _si = G.call_maps(CLC.EXE, FUNCS)
    seed = set()
    for a in accessors:
        seed |= set(callers.get(a, ()))
    # THE ACCESSOR BODIES THEMSELVES ARE MEMBERS. Seeding from an accessor's CALLERS leaves the
    # accessor out, and on BattleUnit that omitted `BattleUnit_AllocateSlotAndBindActor` - the one
    # body most likely to write a back-pointer into the actor record, i.e. exactly the route an
    # unreachability claim has to rule out. Found by asking what the blind spot was after reading
    # a warning about an unrelated wrong "nothing reads this" claim.
    direct = collections.Counter()
    handoff = collections.defaultdict(set)
    escapes = collections.defaultdict(set)
    members = set(seed) | set(accessors)
    work = list(members)
    reached = []
    while work:
        fn = work.pop()
        if fn not in sizes:
            continue
        if fn in seed:
            d, h, pt, e = scan_body_after_accessor(img, md, fn, sizes[fn], accessors, objsize)
        else:
            d, h, pt, e = scan_body(img, md, fn, sizes[fn], objsize)
        direct.update(d)
        for off, cs in h.items():
            handoff[off] |= cs
        for off, cs in e.items():
            escapes[off] |= cs
        for c in pt:
            if c not in members and c in sizes:
                members.add(c)
                reached.append(c)
                work.append(c)
    return sorted(seed), set(), reached, members, direct, handoff, escapes


def run(img, sizes, vtable, objsize, skip_installers=False):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    seed = slots_of(img, vtable)
    inst = set() if skip_installers else installers_of(img, sizes, vtable)
    members = set(seed) | inst
    work = list(members)
    direct = collections.Counter()
    handoff = collections.defaultdict(set)
    escapes = collections.defaultdict(set)
    reached = []
    while work:
        fn = work.pop()
        if fn not in sizes:
            continue
        d, h, pt, e = scan_body(img, md, fn, sizes[fn], objsize)
        direct.update(d)
        for off, cs in h.items():
            handoff[off] |= cs
        for off, cs in e.items():
            escapes[off] |= cs
        for c in pt:
            if c not in members and c in sizes:
                members.add(c)
                reached.append(c)
                work.append(c)
    return seed, inst, reached, members, direct, handoff, escapes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vtable", type=lambda s: int(s, 0))
    ap.add_argument("--slot", type=lambda s: int(s, 0),
                    help="a .data pointer slot for a singleton with no accessor; the seed is "
                         "every body that LOADS it")
    ap.add_argument("--accessor", default="",
                    help="comma-separated accessor entries for a POOLED type with no vtable; "
                         "the seed is their callers and the taint is the RETURN value")
    ap.add_argument("--size", type=lambda s: int(s, 0), help="the object's size, e.g. 0x668")
    ap.add_argument("--gaps", default="", help="off:len,off:len - spans to report on")
    ap.add_argument("--exe", default=CLC.EXE)
    ap.add_argument("--census-out",
                    help="write every DIRECT access as a TSV of "
                         "function/name/site/disp/kind/instruction - the format "
                         "infer_field_type.py reads, so the closure's census can "
                         "be typed instead of merely counted")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    global CENSUS
    if a.census_out:
        CENSUS = []

    img = CLC.Image(a.exe)
    sizes, names = load_funcs()

    if a.self_test:
        ok = True
        seed, inst, reached, members, direct, handoff, esc = run(img, sizes, 0x00903B68, 0x668)
        checks = [
            ("vtable 00903B68 has 31 slots", len(seed) == 31, len(seed)),
            ("the ctor 001F4DA0 is found as an installer", 0x001F4DA0 in inst, sorted(inst)),
            ("the member set closes at 46 bodies", len(members) == 46, len(members)),
            ("the three known out-vector handoffs are rediscovered",
             all(o in handoff for o in (0x3B0, 0x3C0, 0x3D0)), None),
            ("the ctor's unrolled copy shows +0x88 at a 0x10 stride",
             all(o in direct for o in range(0x88, 0x109, 0x10)), None),
            ("nothing touches the +0x420 span (96 B)",
             not any(0x420 <= o < 0x480 for o in direct), None),
        ]
        for label, good, got in checks:
            ok = ok and good
            print("  %-55s %s%s" % (label, "ok" if good else "BROKEN",
                                    "" if good or got is None else "  got %r" % (got,)))
        # the negative control: a linear .text sweep is what NOT to do, and it is why the
        # per-body installer search exists. 0 installers would mean the sweep bug is back.
        print("  %-55s %s" % ("installers found at all (a sweep would report 0)",
                              "ok" if inst else "BROKEN"))
        ok = ok and bool(inst)
        # POOL MODE, controlled against BattleUnit (0xF50, *(0208E688) + slot*0xF50), which has no
        # vtable at all. The control is one the store established independently: the acquire-side
        # reset hands `unit+0x200` to the two navigation fill helpers. If the accessor seeding or
        # the return-value taint is broken, that handoff does not appear.
        pseed, _pi, _pr, pmem, pdirect, phand, pesc = run_pool(
            img, sizes, {0x00236820, 0x00234480, 0x002367A0}, 0xF50)
        pchecks = [
            ("pool seed: the three accessors have 50 callers", len(pseed) == 50, len(pseed)),
            ("pool closure reaches 63 bodies", len(pmem) == 63, len(pmem)),
            ("+0x200 is handed to BOTH navigation fill helpers",
             "0x3839f0" in phand.get(0x200, set()) and "0x3839c0" in phand.get(0x200, set()),
             sorted(phand.get(0x200, ()))),
            ("+0x000 unitFlags is read directly", pdirect.get(0x000, 0) > 0, pdirect.get(0x000)),
            # The two checks that decide what an untouched span is worth. BattleUnit and
            # CharacterRenderObject differ here, and the difference is the whole point.
            ("pool: the only escaping displacement is +0x000",
             set(pesc) == {0x000}, sorted("+0x%03X" % o for o in pesc)),
            ("pool: its four escape sites are the known ones",
             pesc.get(0x000) == {"00302D2A", "00324957", "00324DB5", "00336869"},
             sorted(pesc.get(0x000, ()))),
            # NO INDIRECT HANDOFFS - and this control has been wrong in both directions.
            # It first asserted none; following tail jumps appeared to break it, because the
            # closure walked into `malloc` and reported its tail jump to an import thunk. That
            # walk was itself a sub-register artifact: a 32-bit write did not clear the 64-bit
            # taint, so a dead register still looked like the object. With aliasing handled the
            # closure does not reach malloc at all and the original assertion is correct again.
            # The lesson is not "the first answer was right" - it is that a control weakened to
            # accommodate a tool bug hides the bug instead of catching it.
            ("pool: NO indirect handoffs, so that closure is complete",
             not any(t for ts in phand.values() for t in ts if not t.startswith("0x")),
             sorted(t for ts in phand.values() for t in ts if not t.startswith("0x"))),
            ("pool: the +0x298 span is still empty after the tail-jmp change",
             not any(0x298 <= o < 0x690 for o in pdirect), None),
            ("vtable: indirect handoffs DO exist, so that one is not",
             any(t for ts in handoff.values() for t in ts if not t.startswith("0x")), None),
            ("vtable: every escape is a stack store, not a structure",
             set(esc) == {0x000, 0x008, 0x030, 0x058, 0x390},
             sorted("+0x%03X" % o for o in esc)),
            ("pool: the accessor bodies are members",
             {0x00234480, 0x00236820, 0x002367A0} <= pmem, None),
        ]
        # SLOT MODE, and the pair of numbers that says why it is not interchangeable with pool
        # mode. ManagerSingleton0209BE80 has no accessor and 136 loaders, so the slot IS the seed.
        # BootSingleton01F7F598 has four loaders against 117 accessor callers, so seeding from its
        # slot sees almost nothing - which is exactly how 160 bytes of it stayed "unobserved".
        sseed, _si, _sr, smem, _sd, shand, _se = run_slot(img, sizes, 0x0209BE80, 0x10000)
        boot_loaders = slot_loaders(img, sizes, 0x01F7F598)
        for label, good, got in (
            ("slot: 0209BE80 has 136 loaders", len(sseed) == 136, len(sseed)),
            ("slot: its closure reaches 143 bodies", len(smem) == 143, len(smem)),
            ("slot: ManagerSub _00A0 is handed to 003F8EC0",
             "0x3f8ec0" in shand.get(0xA0, set()), sorted(shand.get(0xA0, ()))),
            ("slot: ManagerSub _A0D0 is handed to 003F80D0",
             "0x3f80d0" in shand.get(0xA0D0, set()), sorted(shand.get(0xA0D0, ()))),
            # THIS CONTROL USED TO ASSERT THE OPPOSITE, and asserting it is how the blind spot
            # survived: it read "_7EA0 is NOT handed - it is a tail jmp, correctly unseen", which
            # made a green self-test confirm the gap instead of catching it. Tail jumps are
            # handoffs; `0028C870` is one and must now be seen.
            ("slot: _7EA0 IS handed, by tail jmp, to 0028C870",
             any(t.startswith("0x28c870") for t in shand.get(0x7EA0, ())),
             sorted(shand.get(0x7EA0, ()))),
            ("slot: _8FA0 has tail-jmp owners (it was called ownerless once)",
             any("(tail)" in t for t in shand.get(0x8FA0, ())), len(shand.get(0x8FA0, ()))),
            ("slot: +0xAA60 is memset - an owned region outside every declared child",
             any(t.startswith("0x861ec0") for t in shand.get(0xAA60, ())),
             sorted(shand.get(0xAA60, ()))),
            # THREE, not four. A fourth body references that slot with `cmp qword ptr [rip],0`
            # and never loads it - a reference is not a load, and the seed needs the load.
            ("slot vs accessor: 01F7F598 has only 3 loaders, so its slot is the WRONG seed",
             len(boot_loaders) == 3, len(boot_loaders)),
        ):
            ok = ok and good
            print("  %-55s %s%s" % (label, "ok" if good else "BROKEN",
                                    "" if good or got is None else "  got %r" % (got,)))
        for label, good, got in pchecks:
            ok = ok and good
            print("  %-55s %s%s" % (label, "ok" if good else "BROKEN",
                                    "" if good or got is None else "  got %r" % (got,)))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    accessors = set(int(x, 0) for x in a.accessor.split(",") if x.strip())
    if a.size is None or (a.vtable is None and not accessors and a.slot is None):
        ap.error("--size plus one of --vtable / --accessor / --slot is required (or --self-test)")

    gaps = []
    for part in [p for p in a.gaps.split(",") if p.strip()]:
        off, ln = part.split(":")
        gaps.append((int(off, 0), int(ln, 0)))

    if a.slot is not None:
        seed, inst, reached, members, direct, handoff, escapes = run_slot(img, sizes, a.slot, a.size)
        print("singleton slot %08X: %d body(ies) load it" % (a.slot, len(seed)))
    elif accessors:
        seed, inst, reached, members, direct, handoff, escapes = run_pool(img, sizes, accessors, a.size)
        print("pooled type, accessor(s) %s: %d caller(s) seeded"
              % (", ".join("%08X" % x for x in sorted(accessors)), len(seed)))
    else:
        seed, inst, reached, members, direct, handoff, escapes = run(img, sizes, a.vtable, a.size)
        print("vtable %08X: %d slot(s); %d installer(s): %s"
              % (a.vtable, len(seed), len(inst),
                 ", ".join("%08X %s" % (x, names.get(x, "")) for x in sorted(inst)) or "-"))
    print("member bodies PROVED: %d (%d seed + %d reached by a this-in-rcx handoff)"
          % (len(members), len(seed) + len(inst), len(reached)))
    print("  reached: %s" % ", ".join("%08X" % x for x in sorted(reached)))
    print()
    if gaps:
        print("=== declared gap spans ===")
        for base, n in gaps:
            dh = sorted(o for o in direct if base <= o < base + n)
            hh = sorted(o for o in handoff if base <= o < base + n)
            print("  %04X +%-5d %s" % (base, n, "STILL UNOBSERVED" if not dh and not hh else
                                       "%d direct, %d handoff" % (len(dh), len(hh))))
            for o in dh:
                print("      DIRECT  +0x%03X  x%d" % (o, direct[o]))
            for o in hh:
                print("      HANDOFF +0x%03X  -> %s" % (o, ", ".join(sorted(handoff[o]))[:76]))
        print()
    print("=== every handoff (lea this+d into an argument register) ===")
    for o in sorted(handoff):
        print("  +0x%03X -> %s" % (o, ", ".join(sorted(handoff[o]))[:80]))
    print()
    print("=== ESCAPES: a this+d value stored INTO MEMORY ===")
    for o in sorted(escapes):
        print("  +0x%03X at %s" % (o, ", ".join(sorted(escapes[o]))[:74]))
    if not escapes:
        print("  none")
    print()
    indirect = {o: [t for t in ts if not t.startswith("0x")] for o, ts in handoff.items()}
    indirect = {o: v for o, v in indirect.items() if v}
    print("=== INDIRECT handoffs: the closure STOPS at each of these ===")
    for o in sorted(indirect):
        print("  +0x%03X -> %s" % (o, ", ".join(sorted(indirect[o]))[:74]))
    if not indirect:
        print("  none - every handoff target is a direct call, so the closure is complete")
    print()
    print("HOW MUCH AN 'UNOBSERVED' SPAN IS WORTH depends on the two sections above. With no")
    print("indirect handoffs and every escape followed to a dead end, an untouched span is unread")
    print("by every static route. With virtual dispatch in the list it is merely unobserved.")
    print()
    print("A DISPLACEMENT IS NOT A FIELD. An unrolled copy reports a perfectly regular stride;")
    print("on CharacterRenderObject that was nine phantom 16-byte elements inside one memset.")
    if CENSUS is not None:
        seen, out = set(), []
        for fn, site, off, kind, txt in CENSUS:
            if (site, off) in seen:
                continue
            seen.add((site, off))
            out.append((fn, site, off, kind, txt))
        out.sort(key=lambda x: (x[2], x[1]))
        cols = ["function", "name", "site", "disp", "kind", "instruction", "route", "note"]
        with open(a.census_out, "w", encoding="utf-8", newline="") as fh:
            fh.write("\t".join(cols) + "\n")
            for fn, site, off, kind, txt in out:
                fh.write("\t".join(("%08X" % fn, names.get(fn, ""), "%08X" % site,
                                    "0x%X" % off, kind, txt, "reach-closure", "")) + "\n")
        print()
        print("wrote %s - %d distinct access(es) at %d offset(s), instruction text included"
              % (a.census_out, len(out), len({x[2] for x in out})))
    return 0


if __name__ == "__main__":
    sys.exit(main())
