#!/usr/bin/env python3
"""gen_phyre_descriptor_vtables.py - each Phyre class's DESCRIPTOR vtable, and what is in it.

RE-KEYED 2026-09-25 (OPUS) - EVERY ROW BEFORE THIS DATE RECORDED THE WRONG TABLE. The descriptor
constructor this tool reads is the `PClassDescriptorAbstract<T>` BASE constructor, and the vtable it
stamps is the base's. The descriptor object's own table is stamped AFTER it returns, by the class's
one static initialiser: `lea rcx,[desc] ; call <Abstract ctor> ; and dword [desc+0xFC], ~2 ;
lea rax,[VT] ; mov [desc], rax` (PAtmospherics: 00164230 -> 00643E80, then 00D5B0C0). The RTTI
Complete Object Locator at [VT-8] settles which is which with no slot numbering at all: the old
column is `PClassDescriptorAbstract<T>` on 315 of 315, and the restamped table is the derived
template RTTI names for the class on 298 of 298 - Concrete 260, WithoutDefaultConstructor 34,
Header 3, HeaderWithoutDefaultConstructor 1. The other 17 (the `ForType-only` rows) are never
restamped, keep the Abstract table as their final one, and keep the `+0xFC` bit 1 that the Abstract
constructor sets and every restamping initialiser clears - so that bit is the abstract-class flag.
Found answering FABLE on PAtmospherics (FABLE-ANSWER-OPUS-SLOT-10-BOTH-RIGHT-DIFFERENT-TABLES...),
whose slot 10 was the Concrete table's and mine the Abstract's.

WHAT MOVED, on the 298 restamped rows: +0x18 and +0x38 differ on all 298, +0x50 on 296, +0x58 on 4;
+0x20/+0x28/+0x30/+0x40/+0x48/+0x60/+0x68 on none. So the controls C1, C2, C4, C5 and C6 below
measured slots the two tables share and stand as written; C3 is re-read by hand on the final table.
**The +0x50 reading below is RETRACTED IN FULL.** On the object's real table +0x50 is the class's
PLACEMENT DEFAULT CONSTRUCTOR - `if (rdx) T::T(rdx); return 1` (PDeferredLightingBase 0063F9A0
calls 006458A0; PAtmospherics 00640280) - on 296 of 315, and the `xor al, al ; ret` stub on 19: the
17 abstract classes and two WithoutDefaultConstructor classes. Nothing a static descriptor's
construction runs reaches 00639A60 - the Abstract constructor's whole forward call closure (14
bodies) never does - so it sees the final table, its construct-and-compare arm IS reachable, and
0063CB80 is not the only builder of default buffers. (PClassDescriptorDynamic's constructor
00632E80 calls 00639A60 directly, but that is another descriptor kind, with bit 0 set.) Everything the old text concluded from "the same stub on all 315"
was concluded from the base class's table.

NOT the class's own vtable. Every Phyre class has a `PClassDescriptorConcrete<T>` object, and
that object has a vtable of its own, installed by the descriptor constructor with
`lea rax,[VT] ; mov [this], rax`. The engine reaches a class's reflection behaviour through it:
`0063C910` and `0063BC00` call slot `+0x60`, `00639A60` calls `+0x50` and `+0x58`, and the member
registrar's last act is a call to `+0x40`.

WHAT IT MEASURED, 2026-09-19 (OPUS), over the 384 descriptor constructors that register a default
buffer - 315 of which yield both a class name and a vtable by a straight-line read:

    +0x40   0062EFD0  on 315 of 315      AttachMember; ONE value
    +0x50   00657140  on 315 of 315      three bytes: `xor al, al ; ret`
    +0x58   121 distinct over 315        THE DESTROY SLOT - shared thunks, not one per class
    +0x60   315 distinct over 315        the class's member registrar, one per class
    +0x18   0063F850  on 315 of 315
    +0x20 / +0x28 / +0x30 / +0x38        315 distinct each - four per-class functions, NAMED
    +0x68   00660570  on 314 of 315

`+0x50` IS THE SAME THREE-BYTE STUB `00657140` (`xor al, al ; ret`) ON ALL 315, AND THAT MUCH IS
MEASURED. `00639A60` calls it with the second scratch buffer and branches on the result, so a
false return on every class means the construct-and-compare arm is UNREACHABLE in this build,
`0063CB80` always builds the buffer - the parent class's default object, then each registered
member's own default, over `0xA5` everywhere else - and the "position dependant constructor"
diagnostic at `00D584A0` can never fire. None of that depends on what the bool means.

WHAT THE BOOL MEANS WAS PUBLISHED WRONG AND IS RETRACTED HERE (OPUS, same day). It was read as
"does this class have a default constructor", from the wording of a diagnostic string nearby, and
the conclusion drawn was that no Phyre class in the image has one. THE ENGINE'S OWN TYPE NAMES
SAY OTHERWISE. Every class carries a descriptor template instantiation in RTTI, and the names
distinguish exactly that property:

    PClassDescriptorConcrete<T>                          260
    PClassDescriptorWithoutDefaultConstructor<T>          34
    PClassDescriptorForType<T> only                       17
    PClassDescriptorHeader<T>                              3
    PClassDescriptorHeaderWithoutDefaultConstructor<T>     1

260 classes the engine calls Concrete have the identical `00657140` stub at `+0x50`, and NO SLOT
IN THE DESCRIPTOR VTABLE SEPARATES THE TWO GROUPS - `+0x18`, `+0x40`, `+0x50` and `+0x68` are
constant across both. So whatever `+0x50` asks, it is not "do you have a default constructor";
the engine answers that question with a template name, and 35 classes are the ones marked without
one. The `descriptor_template` column records it per class.

A string near a call is a hint about the call. A name the compiler emitted for the type is
evidence about the type, and where they disagree the name wins.

`+0x58` IS THE DESTROY SLOT - `00639A60` calls it on both objects it constructs - BUT IT IS STILL
NOT A PER-CLASS DESTRUCTOR COLUMN. 121 distinct values over 315 classes, because the values are
SHARED THUNKS selected by how the class is destroyed:

     86 classes  0061ECF0 and clones, three bytes: `mov al, 1 ; ret`      nothing to destroy
     87 classes  `sub rsp ; mov rcx,rdx ; call <D> ; mov al,1 ; ret`      a direct, non-virtual call
    111 classes  adjust the pointer, then `mov rax,[rcx] ; call [rax+8k]`  the OBJECT's own vtable - slot 0 on
                 0063FC60 (87), slot 3 on 0068C4E0 (23 physics shapes), slot 2 on 00680910 (PScheduler); read as
                 slot 0 for all until 2026-09-28 (OPUS, _index/candidates/phyre-virtual-destroy-slot/virtual_slot.py)
     31 classes  bespoke bodies, 43 to 102 bytes, not reduced

THE CONTROL IS A CROSS-TABULATION AGAINST RTTI (C6 below), and it is what turns a shape into a
reading: whether a class is polymorphic is recorded in Tools/work/rtti/methods.tsv, which has
nothing to do with descriptors.

    dispatch form              has an RTTI vtable    has none
    indirect, through a vtable slot    111               0
    direct call                          0              87
    trivial                              0              86
    bespoke / unreduced                  0              31

Every class destroyed through a vtable has one and every class destroyed directly or not at all
has none. THREE CLASSES ARE COUNTED AS UNREDUCED RATHER THAN VIRTUAL FOR EXACTLY THIS REASON:
PPhysicsRigidBodyBullet (00689FC0), PSamplerStateD3D11 (006132E0) and PScriptableComponent
(0063FC60) make an indirect call while RTTI records no vtable for them. The first two are bespoke
bodies whose indirect call may not be a destructor dispatch at all; the third shares the standard
-8 thunk with 87 others and is the one worth following. None of them is given a `virtual` reading.

The 87 direct-call thunks name a destructor, and those 87 addresses are the `s58_destroy` column.

THE FOUR PER-CLASS SLOTS, each named by a join against an artifact this tool did not produce.

  +0x28  THE CLASS'S SCRIPT-VM OBJECT-POINTER ACCESSOR GETTER. The body is 26 bytes on all 315:
         `mov rcx,rdx ; mov rbx,r8 ; call <X> ; mov [rbx],rax ; ret`. Resolve X in the 747-entry
         address-to-bound-type table on the Script-Object-Accessors page - built from RTTI xrefs,
         not from any vtable - and **314 of 315 are present and the bound type's LEAF NAME EQUALS
         THE CLASS NAME, with 0 mismatches**. That is a name-level agreement between the string
         the descriptor constructor lea's and a table derived from mangled RTTI, and it is what
         makes this a reading rather than a position.
  +0x38  THE DESCRIPTOR'S OWN DELETING DESTRUCTOR. 92 bytes on all 315: install a base vtable at
         [rcx], then `call 00633390` - which the store already names `PClassDescriptor` base
         destructor - with the usual `edx` deleting-flag argument. 315 of 315 make that call.
  +0x20  THE CLASS'S SCRIPT-VM OBJECT PUSH ADAPTER. 297 of 315 are members of the documented
         304-member `object-push-adapters` family, and the size split this tool measures - 21 B
         x194, 31 B x115 - is that family's own documented split of 188 at 21 B and 116 at 31 B.
         Of the rest, 5 and 4 sit in two sibling adapter families and 9 are in none (eight at the
         same 21/31 B, one an 11-byte stub).
  +0x30  THE CLASS'S NULLABLE OBJECT PUSH ADAPTER. 287 of 315 in the 295-member
         `nullable-object-push-adapters` family, 16 and 7 in two documented sibling families, and
         5 are 11-byte stubs.

WHAT THAT CLOSES. Those adapter families are documented as generated code with an open question
attached, in their own words: "NOT dispositioned: the shared implementations they delegate to,
and whatever object or member each adapter names." For every member that sits in a descriptor
vtable, THIS NAMES THE CLASS - 297 of 304 push adapters and 287 of 295 nullable ones.

CONTROLS. Both are against figures this tool did not produce.

  C1  `+0x40` must be `0062EFD0`. member-registration-and-the-recovered-field-schema.md
      established, by a different route, that it is on **1,186 of 1,187** descriptor vtables.
      315 of 315 here. A vtable recovered wrongly would not land on that value.
  C2  `+0x60`, followed through any one-target thunk, must equal the `caller` column that
      phyre-field-schema.tsv records for the same class. That artifact found its callers by
      walking the member registrar's callers and never looked at a vtable, so the two
      derivations are independent. **176 agree, 0 disagree**, over every class the schema
      covers. It read 173 before the four members below were added, which moved three
      classes into the schema - the figure tracks the schema and is not a constant.
  C3  PDeferredLightingBase, read by hand: vtable 00D5A4C8, `+0x50` 00657140, `+0x58` 0063FC60,
      `+0x60` 0063F7E0 -> 006488A0, and `+0x28` 0063F560 -> 0064E220, which the accessor page
      independently calls `PPostProcessing::PDeferredLightingBase *`.
  C4  `+0x28`'s resolved accessor must carry the class's own name: 314 of 315, 0 mismatches.
  C5  `+0x38` must call the `PClassDescriptor` base destructor 00633390: 315 of 315.
  C6  `+0x58`'s dispatch form must agree with RTTI polymorphism - indirect exactly when
      the class has a vtable. 0 disagree, once the three named above are held out as
      unreduced rather than counted as agreements.

AND WHAT C2 WAS WORTH ON THE CLASSES THE SCHEMA DOES NOT COVER. Each of them has a named
registrar, so "the schema is missing them" became a testable claim instead of an open one: count
the member-registrar calls in each registrar body. When this first ran, 142 classes were
uncovered and **139 of the 142 made none** - no reflected members, and the schema was complete
about them. **3 made four between them**, those four were genuinely missing, and they have since
been decoded and added, which is why a run today reports 139 uncovered and 139 registering
nothing. The zero has a control: the same count over the covered classes returns 1 to 9 for
every one of them, so a zero is a real zero and not a decoder that stopped seeing calls.

usage: gen_phyre_descriptor_vtables.py [--out <tsv>] [--check]
"""
import argparse
import collections
import io
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402
import call_graph as CG  # noqa: E402
import check_default_instance_writers as W  # noqa: E402
import gen_phyre_default_buffers as GEN  # noqa: E402

import capstone  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG  # noqa: E402

X = capstone.x86
SLOTS = [0x18, 0x20, 0x28, 0x30, 0x38, 0x40, 0x50, 0x58, 0x60, 0x68]
ATTACH = 0x0062EFD0
FALSE_STUB = 0x00657140                  # `xor al, al ; ret`
ABSTRACT_FLAG = 2                        # desc+0xFC bit 1: set by the Abstract ctor
# C3, read by hand 2026-09-25 on the FINAL table: 001643F0 calls the Abstract ctor 006442E0 on
# 02D34840, clears [02D3493C] bit 1, stamps 00D5A638; +0x50 0063F9A0 placement-constructs through
# 006458A0 and returns 1. (The pre-re-key control read the base table 00D5A4C8 and 00657140.)
CONTROL = ("PDeferredLightingBase", 0x00D5A638, 0x0063F9A0, 0x0063FC60, 0x006488A0, 0x00D5A4C8)
OUT = ("22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/"
       "phyre-class-descriptor-vtable.tsv")

HEADER = """\
# Each Phyre class's DESCRIPTOR vtable - the vtable of the class's descriptor OBJECT, not of the
# class itself - and the slots the reflection machinery calls through it. Generated by
# Tools/analysis-kit/gfz-scripts/gen_phyre_descriptor_vtables.py.
#
# RE-KEYED 2026-09-25 (OPUS). descriptor_vtable is the table the object CARRIES: the one its static
# initialiser stamps after the PClassDescriptorAbstract<T> base constructor returns, or the Abstract
# table itself where no initialiser restamps (the 17 abstract classes). Before this date the column
# held the Abstract base table on all 315 rows. abstract_base_vtable keeps that value; the RTTI
# Complete Object Locator at [vt-8] names both (final_template_rtti), and abstract_flag_cleared says
# whether the initialiser cleared desc+0xFC bit 1, which the Abstract constructor sets.
#
# s50 is the slot 00639A60 calls to DEFAULT-CONSTRUCT an object into the class's default buffer. On
# the carried table it is the class's placement default constructor - `if (rdx) T::T(rdx); return 1`
# - on 296 of 315, and the `xor al, al ; ret` stub 00657140 on 19 (17 abstract, 2 without a default
# constructor). The earlier statement here, that it is that stub on every class and that 00639A60's
# construct-and-compare arm is unreachable, was read from the base table and is withdrawn.
#
# s60 is the class's MEMBER REGISTRAR, one per class, and following it through a single-target
# thunk reproduces phyre-field-schema.tsv's `caller` column on 173 of 173 classes with 0
# disagreements - two independent derivations agreeing.
#
# s58 IS NOT A DESTRUCTOR COLUMN. 121 distinct values over 315 classes is a shared helper, and
# nothing here says what selects between them. s40 is AttachMember on all 315, which is the
# control: the store established 0062EFD0 there on 1,186 of 1,187 descriptor vtables by a
# different route.
#
# s20_family / s30_family name the documented Script-Object-Accessors family each adapter belongs
# to. s28_accessor is the single callee of the 26-byte s28 body, and s28_bound_type is the type
# that page's 747-entry address-to-bound-type table gives for it - on 314 of 315 rows its LEAF
# NAME EQUALS THE `class` COLUMN, with 0 mismatches, which is the control that names these slots.
#
# regcalls is the number of DIRECT calls to 00632960 / 00632A70 in the s60 body. ITS DOMAIN IS
# THOSE TWO CONSTRUCTORS ONLY; it is NOT a member count, and regcalls = 0 does NOT mean the class
# registers no member (2026-09-27, OPUS, on ASTRA's PMeshInstanceSegmentContext sentinel). The
# column is kept unchanged as the historical instrument.
# member_nodes is the wrapper-aware count: calls in the s60 body to ANY of the five member-node
# constructors (MEMBER_CTORS below - scalar, fixed-size, array, enum and dynamic),
# each controlled to install a PClassDataMember* vtable by RTTI. It is >= regcalls on every row;
# 19 classes with regcalls = 0 register 25 array members through 00632A10.
# in_schema says whether phyre-field-schema.tsv carries rows for the class.
# exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
"""


def q(img, a):
    b = img.read(a, 8)
    return struct.unpack("<Q", b)[0] if b else None


def recover(img, h):
    """(class name, descriptor vtable) from one descriptor constructor body."""
    held, this, vt, name = {}, None, None, None
    for i in img.body(h):
        v = W.lea_value(i)
        if v is not None:
            held[W.norm(i.operands[0].reg)] = v
            continue
        if i.mnemonic == "mov" and len(i.operands) == 2:
            d, s = i.operands
            if d.type == X86_OP_REG and s.type == X86_OP_REG:
                dn, sn = W.norm(d.reg), W.norm(s.reg)
                if sn == X.X86_REG_RCX and this is None and i.address - h < 0x20:
                    this = dn
                if sn in held:
                    held[dn] = held[sn]
                else:
                    held.pop(dn, None)
                continue
            if d.type == X86_OP_MEM and s.type == X86_OP_REG:
                mm = d.value.mem
                if (mm.disp == 0 and not mm.index and W.norm(mm.base) == this
                        and W.norm(s.reg) in held):
                    vt = held[W.norm(s.reg)]
                continue
        if i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM:
            if i.operands[0].imm in GEN.CTORS:
                nm = held.get(X.X86_REG_R8)
                if isinstance(nm, int):
                    name = GEN.cstring(img, nm)
            held = {k: x for k, x in held.items() if k not in W.VOLATILE}
            continue
        try:
            _r, w = i.regs_access()
        except capstone.CsError:
            w = []
        for r in w:
            held.pop(W.norm(r), None)
        if i.mnemonic == "call":
            held = {k: x for k, x in held.items() if k not in W.VOLATILE}
    return name, vt


def rip_target(i, op):
    return i.address + i.size + op.mem.disp


def final_stamp(img, h, callers):
    """The table the descriptor object ends up carrying, from the Abstract ctor's callers.

    Each caller that does `lea rcx,[desc] ; call h` and then, within a few instructions,
    `lea reg,[VT] ; mov [desc], reg` RESTAMPS the object - the MSVC derived-constructor shape.
    Returns (vt or None, initialiser, abstract flag cleared, callers seen). None with callers seen
    means no caller restamps, so the base table is the final one; more than one distinct restamp
    is returned as None with the count, and the row is refused rather than guessed.
    """
    stamps, seen = set(), 0
    for c in callers.get(h, ()):
        ins = list(img.body(c))
        for k, i in enumerate(ins):
            if not (i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM
                    and i.operands[0].imm == h):
                continue
            seen += 1
            obj = None
            for p in reversed(ins[max(0, k - 6):k]):
                if (p.mnemonic == "lea" and p.op_str.startswith("rcx,")
                        and p.operands[1].mem.base == X.X86_REG_RIP):
                    obj = rip_target(p, p.operands[1])
                    break
            if obj is None:
                continue
            # The flag word desc+0xFC is edited in either of two forms: `and dword [fc], imm` in
            # place (Concrete), or `mov eax,[fc] ; and/or eax, imm ... ; mov [fc], eax` around the
            # restamp (WithoutDefaultConstructor, Header). Both are followed; `edit` is the net
            # (clear mask, set mask) the initialiser applies.
            held, stamp, clr, st, fcreg, pend = {}, None, 0, 0, None, (0, 0)
            for p in ins[k + 1:k + 16]:
                if p.mnemonic in ("jmp", "ret", "call"):
                    break
                ops = p.operands
                m0 = (len(ops) >= 1 and ops[0].type == X86_OP_MEM
                      and ops[0].mem.base == X.X86_REG_RIP)
                m1 = (len(ops) == 2 and ops[1].type == X86_OP_MEM
                      and ops[1].mem.base == X.X86_REG_RIP)
                if p.mnemonic == "lea" and m1:
                    held[W.norm(ops[0].reg)] = rip_target(p, ops[1])
                elif p.mnemonic == "mov" and m1 and rip_target(p, ops[1]) == obj + 0xFC:
                    fcreg, pend = W.norm(ops[0].reg), (0, 0)
                elif (p.mnemonic in ("and", "or") and ops[1].type == X86_OP_IMM
                      and ((m0 and rip_target(p, ops[0]) == obj + 0xFC)
                           or (ops[0].type == X86_OP_REG and W.norm(ops[0].reg) == fcreg))):
                    imm = ops[1].imm & 0xFFFFFFFF
                    c_, s_ = pend if not m0 else (clr, st)
                    if p.mnemonic == "and":
                        c_, s_ = c_ | (~imm & 0xFFFFFFFF), s_ & imm
                    else:
                        c_, s_ = c_ & ~imm, s_ | imm
                    if m0:
                        clr, st = c_, s_
                    else:
                        pend = (c_, s_)
                elif (p.mnemonic == "mov" and m0 and rip_target(p, ops[0]) == obj + 0xFC
                      and ops[1].type == X86_OP_REG and W.norm(ops[1].reg) == fcreg):
                    clr, st = pend
                elif (p.mnemonic == "mov" and m0 and rip_target(p, ops[0]) == obj
                      and ops[1].type == X86_OP_REG and W.norm(ops[1].reg) in held):
                    stamp = held[W.norm(ops[1].reg)]
            if stamp is not None:
                stamps.add((stamp, c, (clr, st)))
    if len({s[0] for s in stamps}) == 1:
        vt, c, edit = stamps.pop()
        return vt, c, edit, seen
    return None, None, (0, 0), seen if not stamps else -len(stamps)


def fc_edit(edit):
    clr, st = edit
    return " ".join(x for x in (("clear 0x%X" % clr) if clr else "",
                                ("set 0x%X" % st) if st else "") if x) or "none"


def col_class(img, vt):
    """The RTTI Complete Object Locator at [vt-8]: (template, class leaf) or (None, None)."""
    import re as _re
    col = q(img, vt - 8)
    if not col or not (img.base <= col < img.base + 0x3000000):
        return None, None
    sig = img.read(col, 4)
    td = img.read(col + 12, 4)
    if not sig or not td or struct.unpack("<I", sig)[0] != 1:
        return None, None
    nm = (img.read(img.base + struct.unpack("<I", td)[0] + 16, 300) or b"").split(b"\0")[0]
    m = _re.match(r"\.\?AV\?\$(\w+)@V(\w+)@", nm.decode("latin1"))
    return (m.group(1), m.group(2)) if m else (None, None)


def unthunk(img, a, depth=3):
    """follow a small body whose only control transfer is to one target."""
    for _ in range(depth):
        b = img.body(a)
        if not b or img.sizes.get(a, 0) > 64:
            return a
        t = {i.operands[0].imm for i in b
             if i.mnemonic in ("jmp", "call") and i.operands
             and i.operands[0].type == X86_OP_IMM}
        if len(t) != 1:
            return a
        a = t.pop()
    return a


def regcalls(img, f):
    return sum(1 for i in img.body(f)
               if i.mnemonic == "call" and i.operands
               and i.operands[0].type == X86_OP_IMM
               and i.operands[0].imm in (0x00632960, 0x00632A70))


# The member-node constructors: PClassDataMember 00632960, its fixed-size twin 00632A70,
# PClassDataMemberArray 00632A10 (every PArray / PSharray / ArrayDynamic member, the template
# vtable swapped in by the caller), PClassDataMemberEnum 00632BE0 and the
# PClassDataMemberDynamic constructor 00632B30 (00633300 installs the same vtable but is its
# destructor: it drains the annotation list through 006B6700 and frees). Found image-wide as the small bodies that
# install a PClassDataMember* vtable (RTTI) and are called, not tail-jumped (the 701 + 194
# tail-jumps into 00633240 / 006332A0 are destructor restores).
MEMBER_CTORS = (0x00632960, 0x00632A70, 0x00632A10, 0x00632BE0, 0x00632B30)


def member_nodes(img, f):
    return sum(1 for i in img.body(f)
               if i.mnemonic == "call" and i.operands
               and i.operands[0].type == X86_OP_IMM
               and i.operands[0].imm in MEMBER_CTORS)


def rtti_full(img, vt):
    """The full RTTI type-descriptor name behind a vtable, or ''."""
    col = q(img, vt - 8)
    if not col or not (img.base <= col < img.base + 0x3000000):
        return ""
    sig, td = img.read(col, 4), img.read(col + 12, 4)
    if not sig or not td or struct.unpack("<I", sig)[0] != 1:
        return ""
    return (img.read(img.base + struct.unpack("<I", td)[0] + 16, 300) or b"").split(b"\0")[0].decode("latin1")


def installs_member_vtable(img, f):
    for i in img.body(f):
        if i.mnemonic == "lea" and len(i.operands) == 2 and i.operands[1].type == X86_OP_MEM \
                and i.operands[1].mem.base == X.X86_REG_RIP:
            if "PClassDataMember" in rtti_full(img, i.address + i.size + i.operands[1].mem.disp):
                return True
    return False


ACCESSOR_PAGE = ("22-Middleware-PhyreEngine/Script-Object-Accessors/"
                 "phyre-script-object-accessors.md")
ADAPTER_MEMBERS = "22-Middleware-PhyreEngine/Script-Object-Accessors/members"


def bound_types(db):
    """address -> bound type, from the accessor page's two-column table.

    Built from RTTI xrefs by a different author and a different route; nothing in it comes from
    a vtable, which is what makes the name agreement below worth something.
    """
    import re
    out = {}
    pg = io.open(os.path.join(db, ACCESSOR_PAGE), encoding="utf-8").read()
    for m in re.finditer(r"\|\s*`([0-9A-F]{8})`\s*\|\s*`([^`]+)`\s*\|"
                         r"\s*`([0-9A-F]{8})`\s*\|\s*`([^`]+)`\s*\|", pg):
        out[int(m.group(1), 16)] = m.group(2)
        out[int(m.group(3), 16)] = m.group(4)
    return out


def adapter_families(db):
    out = {}
    d = os.path.join(db, ADAPTER_MEMBERS)
    import csv as _csv
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".tsv"):
            continue
        for r in _csv.reader(io.open(os.path.join(d, fn), encoding="utf-8", newline=""),
                             delimiter="	"):
            if not r or r[0].startswith("#"):
                continue
            try:
                out.setdefault(int(r[0], 16), fn[:-4])
            except ValueError:
                pass
    return out


RTTI_METHODS = "Tools/work/rtti/methods.tsv"


def rtti_templates(db):
    """class leaf -> the descriptor template RTTI instantiated for it.

    This is the ENGINE's own statement about default-constructibility, and it is what refuted the
    first reading of slot +0x50.
    """
    import csv as _csv
    import re as _re
    root = os.path.dirname(os.path.dirname(os.path.abspath(db.rstrip("/\\"))))
    path = os.path.join(root, "Tools/work/rtti/classes.tsv")
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(os.path.abspath(db.rstrip("/\\"))),
                            "Tools/work/rtti/classes.tsv")
    order = ["PClassDescriptorWithoutDefaultConstructor",
             "PClassDescriptorHeaderWithoutDefaultConstructor",
             "PClassDescriptorConcrete", "PClassDescriptorHeader"]
    seen = collections.defaultdict(set)
    for r in _csv.reader(io.open(path, encoding="utf-8", newline=""), delimiter="	"):
        if not r:
            continue
        m = _re.match(r"Phyre::(PClassDescriptor\w*)<class ([^>]*)>$", r[0])
        if m:
            seen[m.group(2).split("::")[-1]].add(m.group(1))
    out = {}
    for k, v in seen.items():
        out[k] = next((x for x in order if x in v), "ForType-only")
    return out


def rtti_slot0(db):
    """class leaf names that RTTI records a vtable slot 0 for - i.e. polymorphic classes.

    Read from Tools/work/rtti/methods.tsv, which has nothing to do with descriptors. It is the
    independent side of the +0x58 control.
    """
    import csv as _csv
    root = os.path.dirname(os.path.dirname(os.path.abspath(db.rstrip("/\\"))))
    path = os.path.join(root, RTTI_METHODS)
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(os.path.abspath(db.rstrip("/\\"))), RTTI_METHODS)
    out = set()
    for r in _csv.reader(io.open(path, encoding="utf-8", newline=""), delimiter="	"):
        if not r or r[0] == "address" or len(r) < 3:
            continue
        try:
            if int(r[2]) != 0:
                continue
        except ValueError:
            continue
        # A TEMPLATE INSTANTIATION IS NOT THE CLASS. `split("::")[-1]` on
        # `Phyre::PClassDescriptorAbstract<class Phyre::PGameplay::PScriptableComponent>` returns
        # `PScriptableComponent>` - with the bracket - because the last `::` is INSIDE the
        # template argument. 614 distinct malformed keys over 20,974 rows came out that way.
        # MEASURED YIELD OF FIXING IT: ZERO. A malformed key can only fail to match, never match
        # falsely, and re-running the +0x58 cross-tabulation with template instantiations
        # excluded entirely gives the identical table and the identical three exceptions. It is
        # fixed because the next caller may not be so lucky, not because it changed an answer.
        if "<" in r[1]:
            continue
        out.add(r[1].split("::")[-1])
    return out


def has_indirect_call(img, a):
    return any(i.mnemonic == "call" and i.operands and i.operands[0].type != X86_OP_IMM
               for i in img.body(a))


def sole_call(img, a):
    t = {i.operands[0].imm for i in img.body(a)
         if i.mnemonic in ("call", "jmp") and i.operands
         and i.operands[0].type == X86_OP_IMM}
    return t.pop() if len(t) == 1 else None


def calls_any(img, a, tgt):
    return any(i.mnemonic in ("call", "jmp") and i.operands
               and i.operands[0].type == X86_OP_IMM and i.operands[0].imm == tgt
               for i in img.body(a))


def schema_callers(db):
    import csv
    out = collections.defaultdict(set)
    p = os.path.join(db, "22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/"
                         "phyre-field-schema.tsv")
    for r in csv.reader(io.open(p, encoding="utf-8", newline=""), delimiter="\t"):
        if not r or r[0] == "class_leaf" or r[0].startswith("#") or len(r) < 10:
            continue
        try:
            out[r[0]].add(int(r[9], 16))
        except ValueError:
            pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(G.DB, OUT))
    ap.add_argument("--db", default=G.DB)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    img = W.Image()
    callers, _c, _s = CG.call_maps(G.EXE, G.FUNCS)
    hosts = set()
    for t in GEN.SETTERS:
        hosts |= set(callers.get(t, ()))
    rows, extra, refused = [], {}, []
    for h in sorted(hosts):
        n, base = recover(img, h)
        if not (n and base):
            continue
        fin, init, cleared, seen = final_stamp(img, h, callers)
        if fin is None and seen < 0:
            refused.append((n, h, -seen))
            continue
        vt = fin if fin is not None else base
        rows.append((n, vt, h, [q(img, vt + s) for s in SLOTS]))
        extra[n] = (base, init, cleared, fin is not None)
    rows.sort()
    print("descriptor constructors                   : %d" % len(hosts))
    print("class name + descriptor vtable recovered  : %d" % len(rows))
    print("  restamped by a static initialiser       : %d" % sum(1 for e in extra.values() if e[3]))
    print("  refused - more than one distinct stamp  : %d %s" % (len(refused), refused[:3]))

    # C7 - THE RE-KEY'S OWN CONTROL, from RTTI and nothing this tool computed. The table the Abstract
    # constructor stamps must be PClassDescriptorAbstract<T>; the table the object carries must be
    # the template RTTI instantiated for the class (Abstract itself for the ForType-only rows); both
    # must name the row's class; and the initialiser clears the abstract flag exactly when it
    # restamps.
    tmpl = rtti_templates(a.db)
    c7 = collections.Counter()
    for n, vt, _h, _sl in rows:
        base, _i, edit, restamped = extra[n]
        cleared = bool(edit[0] & ABSTRACT_FLAG)
        bt_, bc = col_class(img, base)
        ft, fc = col_class(img, vt)
        want = tmpl.get(n, "?")
        want = "PClassDescriptorAbstract" if want == "ForType-only" else want
        c7["base Abstract<T>" if (bt_ == "PClassDescriptorAbstract" and bc == n) else "base WRONG"] += 1
        c7["final == RTTI template" if (ft == want and fc == n) else "final WRONG"] += 1
        c7["flag cleared == restamped" if cleared == restamped else "flag MISMATCH"] += 1
    ok7 = not any("WRONG" in k or "MISMATCH" in k for k in c7)
    print("C7 RTTI names both tables, flag tracks it : %s  %s" % ("PASS" if ok7 else "FAIL", dict(c7)))
    fe = collections.Counter((col_class(img, vt)[0], fc_edit(extra[n][2])) for n, vt, _h, _s in rows)
    print("   desc+0xFC edit by the static initialiser, per carried template:")
    for (t, e), v in sorted(fe.items(), key=lambda kv: -kv[1]):
        print("       %-48s %-22s %d" % (t, e, v))
    for k, s in enumerate(SLOTS):
        c = collections.Counter(r[3][k] for r in rows)
        top = c.most_common(1)[0]
        print("  +0x%02X : %3d distinct   most common %08X x%d"
              % (s, len(c), top[0], top[1]))

    i40, i50, i58, i60 = SLOTS.index(0x40), SLOTS.index(0x50), SLOTS.index(0x58), SLOTS.index(0x60)
    ok = all(r[3][i40] == ATTACH for r in rows)
    print("C1 +0x40 is AttachMember 0062EFD0 on all   : %s  (the store: 1,186 of 1,187)"
          % ("PASS" if ok else "FAIL"))
    sch = schema_callers(a.db)
    agree = dis = 0
    for n, vt, _h, sl in rows:
        if n not in sch:
            continue
        if unthunk(img, sl[i60]) in sch[n]:
            agree += 1
        else:
            dis += 1
    print("C2 +0x60 == the schema's caller            : %s  (%d agree, %d disagree)"
          % ("PASS" if dis == 0 and agree else "FAIL", agree, dis))
    ok = ok and dis == 0 and agree
    cn, cvt, c50, c58, c60, cbase = CONTROL
    got = [r for r in rows if r[0] == cn]
    hit = bool(got) and (got[0][1] == cvt and got[0][3][i50] == c50
                         and got[0][3][i58] == c58 and unthunk(img, got[0][3][i60]) == c60
                         and extra[cn][0] == cbase)
    print("C3 PDeferredLightingBase read by hand      : %s" % ("PASS" if hit else "FAIL"))
    ok = ok and hit and ok7 and not refused
    i20, i28, i30, i38 = (SLOTS.index(x) for x in (0x20, 0x28, 0x30, 0x38))
    i58 = SLOTS.index(0x58)
    bt = bound_types(a.db)
    famap = adapter_families(a.db)
    acc = {}
    named = mismatched = 0
    for n, _v, _h, sl in rows:
        t = sole_call(img, sl[i28])
        nm = bt.get(t) if t else None
        acc[n] = (t, nm)
        if nm:
            if nm.rstrip(" *&").split("::")[-1] == n:
                named += 1
            else:
                mismatched += 1
    dtor = sum(1 for _n, _v, _h, sl in rows if calls_any(img, sl[i38], 0x00633390))
    print("C4 +0x28 accessor carries the class name  : %s  (%d named, %d mismatched)"
          % ("PASS" if named and not mismatched else "FAIL", named, mismatched))
    print("C5 +0x38 calls PClassDescriptor dtor      : %s  (%d of %d)"
          % ("PASS" if dtor == len(rows) else "FAIL", dtor, len(rows)))
    ok = ok and named and not mismatched and dtor == len(rows)
    f20 = collections.Counter(famap.get(sl[i20], "(none)") for _n, _v, _h, sl in rows)
    f30 = collections.Counter(famap.get(sl[i30], "(none)") for _n, _v, _h, sl in rows)
    print("   +0x20 adapter families:", dict(f20.most_common(4)))
    print("   +0x30 adapter families:", dict(f30.most_common(4)))

    # +0x58: DESTROY AN INSTANCE. 121 distinct values because they are shared thunks selected
    # by how the class is destroyed, and the cross-tabulation below is the control.
    poly = rtti_slot0(a.db)
    s58 = {}
    for n, _v, _h, sl in rows:
        addr = sl[i58]
        t = sole_call(img, addr)
        ind = has_indirect_call(img, addr)
        if img.sizes.get(addr, 0) == 3:
            s58[n] = ("trivial", None)
        elif t is not None and not ind:
            s58[n] = ("direct", t)
        elif ind and n in poly:
            s58[n] = ("virtual", None)
        else:
            s58[n] = ("unreduced", None)
    tab = collections.Counter((f, n in poly) for n, (f, _t) in s58.items())
    print("   +0x58 destroy form x has an RTTI vtable:")
    for (f, p), c in sorted(tab.items(), key=lambda kv: -kv[1]):
        print("       %-10s %-16s %d" % (f, "RTTI vtable" if p else "no RTTI vtable", c))
    wrong = sum(c for (f, p), c in tab.items() if (f == "virtual") != p and f != "unreduced")
    print("   C6 dispatch form agrees with RTTI polymorphism : %s  (%d disagree)"
          % ("PASS" if wrong == 0 else "FAIL", wrong))
    ok = ok and wrong == 0

    print()
    s50 = collections.Counter()
    for n, _v, _h, sl in rows:
        s50[(col_class(img, _v)[0], "false stub" if sl[i50] == FALSE_STUB else "body")] += 1
    print("+0x50 on the carried table, by the template RTTI names for it:")
    for (t, k), v in sorted(s50.items(), key=lambda kv: -kv[1]):
        print("   %-48s %-10s %d" % (t, k, v))
    print("  -> 00639A60's construct-and-compare arm is reachable wherever +0x50 is a body.")
    miss = [(n, regcalls(img, unthunk(img, sl[i60])), unthunk(img, sl[i60]))
            for n, _v, _h, sl in rows if n not in sch]
    zero = [m for m in miss if m[1] == 0]
    print("classes with no rows in phyre-field-schema     : %d" % len(miss))
    print("  of those, regcalls = 0 (no DIRECT 00632960/00632A70 call; NOT 'registers nothing' - see C8): %d"
          % len(zero))
    for n, c, f in sorted((m for m in miss if m[1]), key=lambda x: -x[1]):
        print("  MISSED: %-42s %d member call(s), registrar %08X" % (n, c, f))
    # C8 - the wrapper-aware member count (2026-09-27, OPUS). Each constructor must install a
    # PClassDataMember* vtable by RTTI; the new count must never fall below the old one; and the
    # named counterexample (ASTRA's sentinel, 005E6860 -> 00632A10) must count exactly one.
    ctor_ok = all(installs_member_vtable(img, c) for c in MEMBER_CTORS)
    nodes = {n: member_nodes(img, unthunk(img, sl[i60])) for n, _v, _h, sl in rows}
    below = [n for n, _v, _h, sl in rows if nodes[n] < regcalls(img, unthunk(img, sl[i60]))]
    sent = nodes.get("PMeshInstanceSegmentContext")
    zero_nodes = [m for m in zero if nodes[m[0]] == 0]
    print("   C8 member constructors install PClassDataMember* vtables : %s" % ("PASS" if ctor_ok else "FAIL"))
    print("   C8 member_nodes >= regcalls on every row                 : %s  (%d below)"
          % ("PASS" if not below else "FAIL", len(below)))
    print("   C8 sentinel PMeshInstanceSegmentContext member_nodes = 1  : %s  (%s)"
          % ("PASS" if sent == 1 else "FAIL", sent))
    print("  of the regcalls-zero registrars, wrapper-aware zero        : %d  (the rest register array members)"
          % len(zero_nodes))
    ok = ok and ctor_ok and not below and sent == 1
    if not ok:
        print("\nA CONTROL FAILED -> the table is not written.")
        return 2
    if a.check:
        return 0
    with io.open(a.out, "w", encoding="utf-8", newline="") as f:
        f.write(HEADER)
        f.write("class\tdescriptor_vtable\tctor_body\t"
                + "\t".join("s%02X" % s for s in SLOTS)
                + "\ts60_unthunked\tregcalls\tin_schema"
                + "\ts20_family\ts28_accessor\ts28_bound_type\ts30_family"
                + "\ts58_form\ts58_destroy\tdescriptor_template"
                + "\tabstract_base_vtable\tstatic_initialiser\tfinal_template_rtti"
                + "\tfc_flag_edit\tmember_nodes\n")
        for n, vt, h, sl in rows:
            t = unthunk(img, sl[i60])
            at, an = acc[n]
            base, init, edit, _r = extra[n]
            f.write("%s\t%08X\t%08X\t%s\t%08X\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%08X\t%s\t%s\t%s\t%d\n"
                    % (n, vt, h, "\t".join("%08X" % (x or 0) for x in sl), t,
                       regcalls(img, t), "yes" if n in sch else "no",
                       famap.get(sl[i20], ""), ("%08X" % at) if at else "",
                       an or "", famap.get(sl[i30], ""),
                       s58[n][0], ("%08X" % s58[n][1]) if s58[n][1] else "",
                       tmpl.get(n, ""), base, ("%08X" % init) if init else "",
                       col_class(img, vt)[0] or "", fc_edit(edit), nodes[n]))
    print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
