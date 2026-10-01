#!/usr/bin/env python3
"""check_default_instance_writers.py - does anything write a Phyre class's default buffer?

THE ANSWER IS YES, AND THE STORE SAID NO. Read that first, because this file exists to close a
hole and the hole turned out to be a wrong answer rather than a missing one.

THE QUESTION. Every Phyre object in this build is born by `0063C910`, which does
`rdx = [descriptor+0xC0]; if (rdx) memcpy(instance - [desc+0xF8], rdx, [desc+0x38])`. The FULL
instance size is copied from a per-class buffer, so every byte no member registration covers
comes from there. `phyre-default-instances.tsv` had established that all 173 buffers it records
live in .bss, that NO instruction names any interior byte of any of them, and that no
ADDRESS-TIED path reaches one through `+0xC0`. From that it concluded: "So on static evidence
these buffers are what the loader left: ZERO ... the whole default-instance mechanism is inert in
this build." It also wrote down, honestly, the hole in its own method - a function that RECEIVES
the descriptor as an ARGUMENT is invisible to an address tie, and 0063C910 is exactly such a
function - and closed with "Supported, not proven."

WHAT THIS DOES. A forward interprocedural MAY-taint over control-flow graphs, seeded where a
descriptor value can enter as a constant (a `lea` of one of the known descriptor addresses) and
propagated through register moves, frame spills, pointer arithmetic and ARGUMENT SLOTS across
direct calls and tail jumps, to a fixpoint. Only then does it look at `[tainted + 0xC0]`, and
only then does it follow what a LOAD of that slot returns.

WHAT IT FOUND, 2026-09-19 (OPUS): FIVE WRITES, in TWO builders, and not one of them is a store.

    00639AEC   memset([desc+0xC0], 0xA5, [desc+0x38])        the whole buffer, poison-filled
    00639B8C   memcpy([desc+0xC0], [desc+0xC8], size)        the second construction copied in
    00639C2D   memcpy([desc+0xC0]+off, <member default>, n)  each registered member's own default
    0063CBF8   memcpy([desc+0xC0]-adj, <parent's default>,)  the no-default-constructor arm
    0063CCD9   memcpy([desc+0xC0]+off, <member default>, n)  and its per-member pass

plus two the tool cannot see, through `call qword ptr [rax+0x50]`, an indirect vtable call: the
class default-constructs an object INTO each buffer. `0063CB80` is the arm taken when that call
returns false - the class has no default constructor - and it builds the buffer anyway, out of
the PARENT class's default object plus each registered member's own. `00639A60` then memcmps the
two and, if they differ, prints the engine's own words - "Class '%s' has a position dependant
constructor and should be marked as having no default constructor to avoid usage of the default
buffer" (00D584A0). THE ENGINE CALLS `+0xC0` THE DEFAULT BUFFER. It is built at RUNTIME, once per
class: `00639A60` sets flag bit 31 at its own exit (00639C55) and both callers - `0063C910` and
the default-object getter `0063BC00` - skip the whole preparation when that bit is set.

So the buffers are neither authored into the image nor zero. The negative was sound about what it
measured (no instruction NAMES those bytes - still true, 173 of 173) and wrong about what it
concluded, because the bytes are reached through a pointer.

THE CONTROLS, and what each one is for - EVIDENCE-STANDARD addendum bx: a control tests the
DISCRIMINATOR, not the window it runs in.

  C1  0063C910 must be reached with the descriptor in arg slot 1 and its load at 0063C961
      reported. This is the hole itself, two frames of parameter passing from any lea. IT FAILED
      ON THE FIRST RUN, and the reason is worth keeping: the walk was linear, and 0063A990 holds
      the descriptor in RSI across a branch whose early-return block restores RSI. A control that
      only ever passes has not been asked anything.
  C2  0063DC80 - `mov [rcx+0xC0], rdx; ret` - must be reported as a STORE TO THE SLOT. Separates
      the two kinds: writing the SLOT registers a buffer, writing THROUGH it fills one.
  C3  THE DISCRIMINATOR. 02CF9970 is PDeferredLightingBase's default BUFFER, not a descriptor. It
      is lea'd at 00644341 and handed to the same 0063DC80 in arg slot 2, beside a real descriptor
      in slot 1. Seeded alone it must produce ZERO findings, or the tool is keyed on the
      displacement rather than the tie - addendum bw.
  C4  00639AEC must be reported as handing the buffer to memset. THIS CONTROL DID NOT EXIST AT
      FIRST, and its absence is the lesson of the whole exercise: C1, C2 and C3 all passed while
      the tool reported ZERO writers, because it only recognised a direct `mov [reg+disp], x`
      through the loaded pointer and every real write here is performed by a callee. Three
      controls proved it could REACH the evidence and TELL IT APART from a lookalike. None asked
      whether it could RECOGNISE it.

AND C4 WAS NOT THE END OF IT. With C4 passing the tool reported three writes; there are five. The
other two are in 0063CB80 and were reached only by READING it: one destination is derived with
`sub` and one buffer pointer moves between registers with `mov`, and the tracker propagated the
DESCRIPTOR through both while dropping the BUFFER. A control proves an instrument finds the case
you thought of. It cannot tell you the case you did not.

WHAT A NEGATIVE FROM THIS IS STILL WORTH. The fixpoint does not follow indirect calls, a
descriptor parked in memory and reloaded with no lea on the path, or anything entering from
outside the image. The middle one is measurable, so it is measured and printed: every store of a
tainted descriptor into non-frame memory, and every data-section qword equal to a known
descriptor address.

usage: check_default_instance_writers.py [--db <root>] [--max-depth 12] [--verbose]
"""
import argparse
import collections
import csv
import io
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402

import capstone  # noqa: E402
import jump_table as JT  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG  # noqa: E402

X = capstone.x86

DESC_CTORS = (0x00632D80, 0x00632C90)
ARG_REGS = [X.X86_REG_RCX, X.X86_REG_RDX, X.X86_REG_R8, X.X86_REG_R9]
VOLATILE = {X.X86_REG_RAX, X.X86_REG_RCX, X.X86_REG_RDX, X.X86_REG_R8, X.X86_REG_R9,
            X.X86_REG_R10, X.X86_REG_R11}
SLOT_OFF = 0xC0

CONTROL_C1 = (0x0063C910, 1, 0x0063C961)
CONTROL_C2 = (0x0063DC80, 1, 0x0063DC80)
CONTROL_C3 = 0x02CF9970
CONTROL_C4 = (0x00639AEC, 0x00861EC0, 1)

# A CALLEE THAT WRITES WHAT IT IS GIVEN. The first version of this tool looked only for a STORE
# through the pointer a `[desc+0xC0]` load returns, passed all three of its controls, and
# reported zero writers - while 00639AEC hands that exact pointer to memset. A write performed
# by a callee is a write. These are the ones this image resolves by name; anything else that
# receives the pointer is reported unclassified, because "not on my list" is not "harmless".
WRITE_CALLEES = {0x00861EC0: ("memset", 1), 0x00861EBA: ("memcpy", 1)}
READ_CALLEES = {0x00861ED2: ("memcmp", 0)}


def parent64():
    """sub-register -> its 64-bit parent.

    Not decoration. A previous census in this kit missed every teardown it was built to find
    because `xor edi,edi` writes EDI and the store it fed was `mov [slot],rdi`, and the two were
    compared as different registers.
    """
    m = {}
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    for full, parts in (
        (X.X86_REG_RAX, (X.X86_REG_EAX, X.X86_REG_AX, X.X86_REG_AL, X.X86_REG_AH)),
        (X.X86_REG_RBX, (X.X86_REG_EBX, X.X86_REG_BX, X.X86_REG_BL, X.X86_REG_BH)),
        (X.X86_REG_RCX, (X.X86_REG_ECX, X.X86_REG_CX, X.X86_REG_CL, X.X86_REG_CH)),
        (X.X86_REG_RDX, (X.X86_REG_EDX, X.X86_REG_DX, X.X86_REG_DL, X.X86_REG_DH)),
        (X.X86_REG_RSI, (X.X86_REG_ESI, X.X86_REG_SI, X.X86_REG_SIL)),
        (X.X86_REG_RDI, (X.X86_REG_EDI, X.X86_REG_DI, X.X86_REG_DIL)),
        (X.X86_REG_RBP, (X.X86_REG_EBP, X.X86_REG_BP, X.X86_REG_BPL)),
        (X.X86_REG_RSP, (X.X86_REG_ESP, X.X86_REG_SP, X.X86_REG_SPL)),
        (X.X86_REG_R8, (X.X86_REG_R8D, X.X86_REG_R8W, X.X86_REG_R8B)),
        (X.X86_REG_R9, (X.X86_REG_R9D, X.X86_REG_R9W, X.X86_REG_R9B)),
        (X.X86_REG_R10, (X.X86_REG_R10D, X.X86_REG_R10W, X.X86_REG_R10B)),
        (X.X86_REG_R11, (X.X86_REG_R11D, X.X86_REG_R11W, X.X86_REG_R11B)),
        (X.X86_REG_R12, (X.X86_REG_R12D, X.X86_REG_R12W, X.X86_REG_R12B)),
        (X.X86_REG_R13, (X.X86_REG_R13D, X.X86_REG_R13W, X.X86_REG_R13B)),
        (X.X86_REG_R14, (X.X86_REG_R14D, X.X86_REG_R14W, X.X86_REG_R14B)),
        (X.X86_REG_R15, (X.X86_REG_R15D, X.X86_REG_R15W, X.X86_REG_R15B)),
    ):
        m[full] = full
        for p in parts:
            m[p] = full
    del md
    return m


P64 = parent64()


def norm(r):
    return P64.get(r, r)


class Image(object):
    def __init__(self):
        self.blob, self.base, self.secs = G.load_pe(G.EXE)
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.md.detail = True
        self.sizes, self.names = {}, {}
        f = io.open(G.FUNCS, encoding="utf-8", errors="replace")
        f.readline()
        for line in f:
            p = line.split("\t")
            try:
                e = int(p[0], 16)
            except (ValueError, IndexError):
                continue
            if p[1].startswith(("Unwind@", "Catch_All@")):
                continue
            try:
                self.sizes[e] = int(p[2])
            except (ValueError, IndexError):
                continue
            self.names[e] = p[1]
        self._body = {}

    def off(self, va):
        r = va - self.base
        for nm, sva, vs, ra, rs in self.secs:
            if sva <= r < sva + max(vs, rs):
                o = r - sva
                if o < rs:
                    return ra + o, nm
        return None, None

    def read(self, va, n):
        o, _nm = self.off(va)
        if o is None:
            return None
        return self.blob[o:o + n]

    def body(self, entry):
        if entry in self._body:
            return self._body[entry]
        n = self.sizes.get(entry, 0)
        out = []
        if 0 < n <= 0x20000:
            b = self.read(entry, n)
            if b:
                out = list(self.md.disasm(b, entry))
        self._body[entry] = out
        return out


def rip_target(i, op):
    if op.type != X86_OP_MEM:
        return None
    m = op.value.mem
    if m.base == X.X86_REG_RIP and m.index == 0:
        return i.address + i.size + m.disp
    return None


def lea_value(i):
    """the constant address a `lea rX, [...]` puts in rX, or None."""
    if i.mnemonic != "lea" or len(i.operands) != 2:
        return None
    d, s = i.operands
    if d.type != X86_OP_REG or s.type != X86_OP_MEM:
        return None
    m = s.value.mem
    if m.index:
        return None
    if m.base == X.X86_REG_RIP:
        return i.address + i.size + m.disp
    if m.base == 0:
        return m.disp
    return None


def enumerate_descriptors(img):
    """every address handed to a class-descriptor constructor as arg 1.

    This is the descriptor population as the IMAGE defines it, not as the store records it: the
    store's 330-row parent chain is a COVERAGE of this set, and reading the coverage as the
    population is a mistake this project has already published and corrected once.
    """
    import call_graph as CG
    callers, _callees, _sites = CG.call_maps(G.EXE, G.FUNCS)
    out = {}
    for ctor in DESC_CTORS:
        for c in callers.get(ctor, ()):
            held = {}
            for i in img.body(c):
                v = lea_value(i)
                if v is not None:
                    held[norm(i.operands[0].reg)] = v
                    continue
                if (i.mnemonic == "mov" and len(i.operands) == 2
                        and i.operands[0].type == X86_OP_REG
                        and i.operands[1].type == X86_OP_REG):
                    src = held.get(norm(i.operands[1].reg))
                    if src is not None:
                        held[norm(i.operands[0].reg)] = src
                    else:
                        held.pop(norm(i.operands[0].reg), None)
                    continue
                if (i.mnemonic == "call" and i.operands
                        and i.operands[0].type == X86_OP_IMM
                        and i.operands[0].imm == ctor):
                    v = held.get(X.X86_REG_RCX)
                    if v is not None:
                        out.setdefault(v, (c, i.address))
                    held = {k: x for k, x in held.items() if k not in VOLATILE}
                    continue
                try:
                    _r, w = i.regs_access()
                except capstone.CsError:
                    w = []
                for r in w:
                    held.pop(norm(r), None)
                if i.mnemonic == "call":
                    held = {k: x for k, x in held.items() if k not in VOLATILE}
    return out


def store_descriptors(db):
    got = set()
    for rel, col in (
        ("22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/"
         "phyre-class-parent-chain.tsv", 1),
        ("22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/"
         "phyre-default-instances.tsv", 1),
    ):
        p = os.path.join(db, rel)
        if not os.path.exists(p):
            continue
        for r in csv.reader(io.open(p, encoding="utf-8", newline=""), delimiter="\t"):
            if not r or r[0].startswith("#") or len(r) <= col:
                continue
            v = r[col].strip()
            try:
                got.add(int(v, 16))
            except ValueError:
                pass
    return got


def default_instances(db):
    out = {}
    p = os.path.join(db, "22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/"
                         "phyre-default-instances.tsv")
    for r in csv.reader(io.open(p, encoding="utf-8", newline=""), delimiter="\t"):
        if not r or r[0].startswith("#") or len(r) < 5:
            continue
        try:
            out[int(r[2], 16)] = (r[0], int(r[4], 16))
        except ValueError:
            pass
    return out

class Taint(object):
    """forward taint of descriptor-valued locations over one function's CONTROL-FLOW GRAPH.

    A LINEAR WALK IS WRONG HERE AND THE CONTROL SAID SO. The first version of this class walked
    the body in address order, and control C1 failed: 0063A990 holds the descriptor in RSI across
    a branch, and the EARLY-RETURN block at 0063A9C0 does `mov rsi,[rsp+0x58]` to restore the
    caller's RSI. In address order that kill lands before the real path resumes at 0063A9CB, so
    the taint was dead by the time the descriptor was handed to 0063C910 - the one call the whole
    tool exists to see. Nothing about the finding was wrong; the traversal was.

    So this is a proper MAY-analysis: basic blocks, union at every merge, iterate to a fixpoint.
    May is the right direction for an ABSENCE claim - it over-approximates what could hold a
    descriptor, so a finding of nothing is a finding about every path, not about one path. The
    same over-approximation means a POSITIVE has to be read by hand before it is believed.

    Locations tracked: 64-bit registers, RSP-relative frame slots, and separately the registers
    holding what a `[descriptor+0xC0]` LOAD returned - the buffer pointer, which is the only thing
    a store can go through to reach a default instance.

    FRAME SLOTS ARE KEYED BY THE RAW DISPLACEMENT, not by a normalised frame offset. Two slots at
    the same displacement either side of a `sub rsp` are therefore conflated. That is another
    over-approximation and it is stated rather than fixed, because it errs the same safe way.
    """

    def __init__(self, img):
        self.img = img

    def _blocks(self, entry):
        body = self.img.body(entry)
        if not body:
            return [], {}, {}
        size = self.img.sizes.get(entry, 0)
        inside = lambda a: entry <= a < entry + size          # noqa: E731
        at = {i.address: n for n, i in enumerate(body)}
        leaders = {body[0].address}
        # SWITCH ARMS ARE BLOCKS TOO. A `jmp <reg>` reaches its arms through a jump table, so a
        # walk that follows only direct branches never enters any of them - and one such arm is
        # where ManagerSub0209BE80_57E0's thirteen-slot claim array is written, which is why a
        # 0x2220-byte span of the store's largest type censused as ZERO accesses. jump_table.py
        # reads the table and returns only targets INSIDE this body, so a misread cannot inject
        # a foreign address into a census; the worst case is the blindness that was there before.
        arms = {}
        for n, i in enumerate(body):
            if i.mnemonic == "jmp" and i.operands and i.operands[0].type == X86_OP_REG:
                t = JT.resolve(self.img, self.img.md, body, n, entry, size)
                if t:
                    arms[i.address] = t
                    leaders.update(t)
        for n, i in enumerate(body):
            m = i.mnemonic
            if m == "ret" or m.startswith("ret"):
                if n + 1 < len(body):
                    leaders.add(body[n + 1].address)
            elif m == "jmp" or (m[0] == "j" and m != "jmp"):
                if i.operands and i.operands[0].type == X86_OP_IMM and inside(i.operands[0].imm):
                    leaders.add(i.operands[0].imm)
                if n + 1 < len(body):
                    leaders.add(body[n + 1].address)
        starts = sorted(a for a in leaders if a in at)
        blocks = {}
        for k, s in enumerate(starts):
            e = starts[k + 1] if k + 1 < len(starts) else None
            blocks[s] = [i for i in body[at[s]:] if e is None or i.address < e]
        succ = {}
        for s, ins in blocks.items():
            if not ins:
                succ[s] = []
                continue
            last = ins[-1]
            m = last.mnemonic
            nxt = []
            fall = last.address + last.size
            if m == "ret" or m.startswith("ret") or m == "int3":
                pass
            elif m == "jmp":
                if last.operands and last.operands[0].type == X86_OP_IMM \
                        and inside(last.operands[0].imm):
                    nxt.append(last.operands[0].imm)
                elif last.address in arms:
                    nxt.extend(arms[last.address])
            elif m[0] == "j":
                if last.operands and last.operands[0].type == X86_OP_IMM \
                        and inside(last.operands[0].imm):
                    nxt.append(last.operands[0].imm)
                if fall in blocks:
                    nxt.append(fall)
            else:
                if fall in blocks:
                    nxt.append(fall)
            succ[s] = [x for x in nxt if x in blocks]
        return starts, blocks, succ

    def run(self, entry, seed_regs, seed_values=None):
        starts, blocks, succ = self._blocks(entry)
        if not starts:
            return set(), set(), set(), set(), set()
        size = self.img.sizes.get(entry, 0)
        inside = lambda a: entry <= a < entry + size          # noqa: E731
        forwards, slot_access, mem_escape, writers = set(), set(), set(), set()
        buf_escapes = set()
        state = {starts[0]: (frozenset(seed_regs), frozenset(), frozenset())}
        work = collections.deque([starts[0]])
        rounds = 0
        while work and rounds < 20000:
            rounds += 1
            b = work.popleft()
            regs, slots, buf = (set(x) for x in state[b])
            for i in blocks[b]:
                m = i.mnemonic
                # A register that RECEIVES the +0xC0 pointer on this very instruction must not
                # then be cleared by the same instruction's own kill. The first version did
                # exactly that - `mov rcx,[rdi+0xC0]` added RCX to the buffer set and the mov
                # rule removed it two lines later - and control C4 reported zero hand-offs while
                # the next instruction handed RCX to memset.
                just_buf = set()

                for oi, o in enumerate(i.operands):
                    if o.type != X86_OP_MEM:
                        continue
                    mm = o.value.mem
                    if mm.index or mm.disp != SLOT_OFF or norm(mm.base) not in regs:
                        continue
                    if oi == 0 and m.startswith("mov"):
                        slot_access.add((i.address, "store", i.op_str))
                    else:
                        slot_access.add((i.address, "load", i.op_str))
                        if (m in ("mov", "add") and len(i.operands) == 2 and oi == 1
                                and i.operands[0].type == X86_OP_REG):
                            # `add rsi, [desc+0xC0]` at 00639B19 makes RSI point INTO the
                            # buffer just as surely as a mov does. A derived pointer is the
                            # pointer.
                            buf.add(norm(i.operands[0].reg))
                            just_buf.add(norm(i.operands[0].reg))

                if buf and i.operands and i.operands[0].type == X86_OP_MEM:
                    mm = i.operands[0].value.mem
                    if norm(mm.base) in buf or norm(mm.index) in buf:
                        writers.add((i.address, "%s %s" % (m, i.op_str)))
                    elif (len(i.operands) == 2 and i.operands[1].type == X86_OP_REG
                            and norm(i.operands[1].reg) in buf):
                        buf_escapes.add((i.address, None, 0, "%s %s" % (m, i.op_str)))

                if (m == "mov" and len(i.operands) == 2
                        and i.operands[0].type == X86_OP_MEM
                        and i.operands[1].type == X86_OP_REG
                        and norm(i.operands[1].reg) in regs):
                    mm = i.operands[0].value.mem
                    if norm(mm.base) == X.X86_REG_RSP and not mm.index:
                        slots.add(mm.disp)
                    else:
                        mem_escape.add((i.address, "%s %s" % (m, i.op_str)))

                # A POINTER DERIVED FROM THE BUFFER IS THE BUFFER. 00639A60 forms the adjusted
                # instance pointer with `lea r12,[rsi+rax]` where RAX holds the +0xC0 load, and
                # later reaches a member's slot with `add rcx, r12`. Neither is a mov, and
                # without these two rules the per-member default copy at 00639C2D is invisible.
                if m == "lea" and len(i.operands) == 2 and i.operands[0].type == X86_OP_REG                         and i.operands[1].type == X86_OP_MEM:
                    mm = i.operands[1].value.mem
                    if norm(mm.base) in buf or norm(mm.index) in buf:
                        buf.add(norm(i.operands[0].reg))
                        just_buf.add(norm(i.operands[0].reg))
                # ARITHMETIC ON A BUFFER POINTER LEAVES A BUFFER POINTER. 0063CB80 forms the
                # destination of its memcpy as `add r12,[desc+0xC0]` then `mov rcx,r12` then
                # `sub rcx,rax` - adjusting past the parent sub-object - and the SUB is what
                # killed the taint before this rule existed, hiding a whole second builder.
                if m in ("add", "sub") and len(i.operands) == 2                         and i.operands[0].type == X86_OP_REG:
                    d0 = norm(i.operands[0].reg)
                    s1 = i.operands[1]
                    if d0 in buf or (s1.type == X86_OP_REG and norm(s1.reg) in buf):
                        buf.add(d0)
                        just_buf.add(d0)

                v = lea_value(i)
                if v is not None:
                    d = norm(i.operands[0].reg)
                    if seed_values and v in seed_values:
                        regs.add(d)
                    else:
                        regs.discard(d)
                    buf.discard(d)
                    continue
                if m == "mov" and len(i.operands) == 2 and i.operands[0].type == X86_OP_REG:
                    d = norm(i.operands[0].reg)
                    s = i.operands[1]
                    if s.type == X86_OP_REG and norm(s.reg) in buf:
                        # THE BUFFER POINTER MOVES BETWEEN REGISTERS TOO. Without this the
                        # descriptor taint propagated through `mov` and the buffer taint did
                        # not, so 0063CB80's `mov rcx,r12` dropped it one instruction before
                        # the memcpy that is the whole point.
                        buf.add(d)
                        just_buf.add(d)
                    if s.type == X86_OP_REG and norm(s.reg) in regs:
                        regs.add(d)
                        continue
                    if (s.type == X86_OP_MEM and not s.value.mem.index
                            and norm(s.value.mem.base) == X.X86_REG_RSP
                            and s.value.mem.disp in slots):
                        regs.add(d)
                        continue
                    regs.discard(d)
                    if d not in just_buf:
                        buf.discard(d)
                    continue
                if m in ("call", "jmp") and i.operands and i.operands[0].type == X86_OP_IMM:
                    tgt = i.operands[0].imm
                    if not inside(tgt) and tgt in self.img.sizes:
                        for k, ar in enumerate(ARG_REGS):
                            if ar in regs:
                                forwards.add((tgt, k + 1))
                            if ar in buf:
                                buf_escapes.add((i.address, tgt, k + 1, i.op_str))
                    if m == "call":
                        regs -= VOLATILE
                        buf -= VOLATILE
                    continue
                if m == "call":
                    regs -= VOLATILE
                    buf -= VOLATILE
                    continue
                try:
                    _r, w = i.regs_access()
                except capstone.CsError:
                    w = []
                for r in w:
                    regs.discard(norm(r))
                    if norm(r) not in just_buf:
                        buf.discard(norm(r))

            out = (frozenset(regs), frozenset(slots), frozenset(buf))
            for s in succ[b]:
                prev = state.get(s)
                if prev is None:
                    state[s] = out
                    work.append(s)
                else:
                    merged = tuple(a | b2 for a, b2 in zip(prev, out))
                    if merged != prev:
                        state[s] = merged
                        work.append(s)
        return forwards, slot_access, mem_escape, writers, buf_escapes

def fixpoint(img, seeds, maxdepth):
    """seeds: {function_entry: set(arg_slot | 0 for 'lea inside this body')}"""
    t = Taint(img)
    state = collections.defaultdict(set)
    for f, slots in seeds.items():
        state[f] |= slots
    work = collections.deque((f, s, 0) for f, ss in seeds.items() for s in ss)
    accesses, escapes, writers, handoffs = [], [], [], []
    seen_edge = set()
    depth_cut = 0
    while work:
        f, slot, d = work.popleft()
        regs = set()
        if slot == 0:
            regs = None      # handled by the caller's own lea scan; see seed_from_leas
        else:
            regs = {ARG_REGS[slot - 1]}
        if regs is None:
            continue
        fwd, acc, esc, wr, besc = t.run(f, regs)
        for a in acc:
            accesses.append((f, slot) + a)
        for a in esc:
            escapes.append((f, slot) + a)
        for a in wr:
            writers.append((f, slot) + a)
        for a in besc:
            handoffs.append((f, slot) + a)
        if d >= maxdepth:
            depth_cut += 1
            continue
        for (g, gslot) in fwd:
            if (g, gslot) in seen_edge:
                continue
            seen_edge.add((g, gslot))
            state[g].add(gslot)
            work.append((g, gslot, d + 1))
    return state, accesses, escapes, writers, handoffs, depth_cut


def seed_from_leas(img, values):
    """functions whose body lea's one of `values`, and the (callee, arg slot) pairs they feed.

    Uses the same CFG walk as everything else. An earlier linear version of this step is what
    control C1 caught: a taint killed on a not-taken branch never reached the call it was
    supposed to.
    """
    seeds = collections.defaultdict(set)
    t = Taint(img)
    hosts = []
    for e in img.sizes:
        b = img.body(e)
        if not b or not any(lea_value(i) in values for i in b if i.mnemonic == "lea"):
            continue
        hosts.append(e)
        fwd = t.run(e, set(), seed_values=values)[0]
        for g, slot in fwd:
            seeds[g].add(slot)
    return seeds, hosts


def data_holding(img, values):
    """data-section qwords whose value is one of `values`.

    A descriptor parked in memory can be reloaded with no lea anywhere on the path, which is the
    one reload route a forward taint from leas cannot see. Counting them is what turns "no writer
    found" into "no writer found, and here is the size of what this method cannot reach".
    """
    hits = []
    vs = set(values)
    for nm, sva, vsz, ra, rs in img.secs:
        if nm in (".text", ".pdata", ".reloc", ".rsrc"):
            continue
        n = min(rs, vsz) & ~7
        chunk = img.blob[ra:ra + n]
        for o in range(0, n - 7, 8):
            q = struct.unpack_from("<Q", chunk, o)[0]
            if q in vs:
                hits.append((img.base + sva + o, q, nm))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=G.DB)
    ap.add_argument("--max-depth", type=int, default=12)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    img = Image()
    img_desc = enumerate_descriptors(img)
    st_desc = store_descriptors(a.db)
    descs = set(img_desc) | st_desc
    print("descriptors from the image (arg1 of %s): %d"
          % ("/".join("%08X" % c for c in DESC_CTORS), len(img_desc)))
    print("descriptors recorded in the store          : %d" % len(st_desc))
    print("union used as the seed set                 : %d   (store-only %d, image-only %d)"
          % (len(descs), len(st_desc - set(img_desc)), len(set(img_desc) - st_desc)))
    print()

    seeds, hosts = seed_from_leas(img, descs)
    print("bodies that lea a descriptor               : %d" % len(hosts))
    print("direct (callee, arg slot) pairs from those : %d" % sum(len(v) for v in seeds.values()))
    state, acc, esc, wr, hand, cut = fixpoint(img, seeds, a.max_depth)
    print("functions reached with a descriptor arg    : %d  (depth cut at %d: %d paths)"
          % (len(state), a.max_depth, cut))
    print()

    loads = [x for x in acc if x[3] == "load"]
    stores = [x for x in acc if x[3] == "store"]
    print("accesses to [descriptor + 0xC0]            : %d load, %d store"
          % (len(loads), len(stores)))
    print("direct stores through a +0xC0 load        : %d" % len(wr))
    for f, slot, addr, txt in sorted(set(wr), key=lambda x: x[2]):
        print("    %08X in %08X arg%d   %s" % (addr, f, slot, txt))
    if not wr:
        print("    none")
    print()

    hand_u = sorted(set(hand), key=lambda x: x[2])
    confirmed = [h for h in hand_u if h[3] in WRITE_CALLEES
                 and h[4] == WRITE_CALLEES[h[3]][1]]
    readonly = [h for h in hand_u if h[3] in READ_CALLEES]
    other = [h for h in hand_u if h not in confirmed and h not in readonly]
    print("THE BUFFER POINTER HANDED TO SOMETHING ELSE : %d site(s)" % len(hand_u))
    print("  WRITES BY A CALLEE (the finding)          : %d" % len(confirmed))
    for f, slot, addr, tgt, k, txt in confirmed:
        print("    %08X in %08X arg%d  ->  %08X %s, arg%d  =  A WRITE"
              % (addr, f, slot, tgt, WRITE_CALLEES[tgt][0], k))
    print("  reads by a callee                         : %d" % len(readonly))
    for f, slot, addr, tgt, k, txt in readonly:
        print("    %08X in %08X arg%d  ->  %08X %s, arg%d"
              % (addr, f, slot, tgt, READ_CALLEES[tgt][0], k))
    print("  unclassified hand-offs                    : %d" % len(other))
    for f, slot, addr, tgt, k, txt in other[:20]:
        print("    %08X in %08X arg%d  ->  %s arg%d   %s"
              % (addr, f, slot, ("%08X" % tgt) if tgt else "memory", k, txt))
    print()

    # ---- controls -----------------------------------------------------------------
    ok = True
    c1f, c1slot, c1addr = CONTROL_C1
    hit = any(f == c1f and slot == c1slot and addr == c1addr and kind == "load"
              for f, slot, addr, kind, _t in loads)
    print("C1 reach-the-hole   %08X arg%d load at %08X   %s"
          % (c1f, c1slot, c1addr, "PASS" if hit else "FAIL"))
    ok = ok and hit
    c2f, c2slot, c2addr = CONTROL_C2
    hit2 = any(f == c2f and slot == c2slot and addr == c2addr
               for f, slot, addr, kind, _t in stores)
    print("C2 slot-store seen  %08X arg%d store at %08X  %s"
          % (c2f, c2slot, c2addr, "PASS" if hit2 else "FAIL"))
    ok = ok and hit2
    c4a, c4t, c4k = CONTROL_C4
    hit4 = any(addr == c4a and tgt == c4t and k == c4k
               for _f, _s, addr, tgt, k, _t in hand)
    print("C4 callee-write     %08X hands the buffer to %08X arg%d          %s"
          % (c4a, c4t, c4k, "PASS" if hit4 else "FAIL"))
    ok = ok and hit4
    s3, _h3 = seed_from_leas(img, {CONTROL_C3})
    _st3, acc3, _esc3, wr3, hand3, _c3 = fixpoint(img, s3, a.max_depth)
    hit3 = not acc3 and not wr3 and not hand3
    print("C3 discriminator    %08X (a BUFFER, not a descriptor) -> %d accesses, %d writers  %s"
          % (CONTROL_C3, len(acc3), len(wr3), "PASS" if hit3 else "FAIL"))
    ok = ok and hit3
    print()
    if not ok:
        print("A CONTROL FAILED -> the negative below is not reportable. C1 failing means the")
        print("tool cannot see a parameter-passed descriptor, which is the entire hole.")
    print()

    # ---- the boundary this method cannot cross, measured --------------------------
    print("THE RELOAD ROUTE, measured rather than assumed:")
    print("  tainted descriptors stored into non-frame memory : %d" % len(esc))
    for f, slot, addr, txt in esc[:12]:
        print("      %08X in %08X arg%d  %s" % (addr, f, slot, txt))
    dh = data_holding(img, descs)
    print("  data qwords equal to a known descriptor address  : %d" % len(dh))
    for addr, val, nm in dh[:12]:
        print("      %08X in %-8s -> %08X" % (addr, nm, val))
    print()
    inst = default_instances(a.db)
    print("default instances on record: %d" % len(inst))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
