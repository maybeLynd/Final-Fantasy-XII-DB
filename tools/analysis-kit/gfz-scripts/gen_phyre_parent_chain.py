#!/usr/bin/env python3
"""gen_phyre_parent_chain.py - each Phyre class's BASE CLASS, and what it explains.

WHY THIS IS THE BIGGEST SINGLE LEVER IN THE TYPE STORE. `member-registration-and-the-recovered-
field-schema.md` section 18 measured that **70.4% of Phyre instance bytes lie below each class's
first registered member**. `PDeferredLightingBase` is the extreme case in the store: 0x41D8 bytes
declared, every named member at 0x40D0 or above, and a single UNKNOWN span of **16,592 bytes** at
offset zero - the largest unknown span in the whole database after ManagerSingleton0209BE80's.

Those low bytes are not a mystery. **They are the base class.** Phyre registers only a class's OWN
members; everything a class inherits is registered against the parent, and the child's schema
starts where the parent's instance ends.

WHERE THE PARENT COMES FROM, read off the constructor rather than guessed:

    00632D80(rcx = descriptor, rdx = sub-object, r8 = name, r9d = size,
             [rsp+0x28] = alignment, [rsp+0x30] = PARENT DESCRIPTOR)

      00632DD1  mov rax, qword ptr [rsp + 0x30]     the 6th argument, as the CALLEE sees it
                                          (the caller writes it at [rsp+0x28]; the call
                                           pushed a return address between the two frames)
      00632DD6  mov qword ptr [rcx + 0x70], rdx
      00632DDA  mov qword ptr [rcx + 0x78], rax     -> +0x78, the parent slot

`CONTRACT-phyre-class-descriptor.md` already documents `+0x78` as *"the parent descriptor, or
null"* and `0063D550` as the rebind that skips when it is null. This reads the value that lands
there, which no file carried.

A FALSE START WORTH RECORDING. The first attempt read the 5th argument of `00632960` and found
`0x40D0` for `PDeferredLightingBase` - exactly its first registered member - which looked like the
base-class prefix size. It is not: `00632960` has **682 callers** and its 5th argument is
distributed as 0x8 (x126), 0x10 (x58), 0x18 (x36)... It is the MEMBER registrar and that argument
is the member's own offset, which `phyre-field-schema.tsv` already carries. One function agreeing
with a hypothesis is not evidence; the distribution over its whole caller set is.

THE CONTROL IS BUILT INTO THE CLAIM, which is why this is worth running at all. If `+0x78` really
is the base class then, for every child with a known parent:

  * `parent.instance_size <= child.instance_size` - a base cannot be larger than what contains it;
  * `child`'s first registered member should sit **at or after** `parent.instance_size`, because a
    child cannot place its own members inside its base;
  * and `PDeferredLightingBase`'s parent should be about `0x40D0` bytes, which is a prediction
    made before the parent is read.

Violations are reported, not suppressed. If the first two fail broadly, the `+0x78` reading is
wrong and the output is discarded.

usage: gen_phyre_parent_chain.py [--out <tsv>]
"""
import argparse
import collections
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402

import capstone  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP  # noqa: E402

X = capstone.x86
CTORS = (0x00632D80, 0x00632C90)
SIZES_TSV = ("22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/"
             "members/phyre-class-instance-sizes.tsv")
SCHEMA_TSV = "22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/phyre-field-schema.tsv"


def load_image():
    d, base, secs = G.load_pe(G.EXE)
    sizes = {}
    f = io.open(G.FUNCS, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.split("\t")
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except (ValueError, IndexError):
            pass
    return d, base, secs, sizes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=G.DB)
    ap.add_argument("--out")
    a = ap.parse_args()

    d, base, secs, fsizes = load_image()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True

    def blob(va, n):
        r = va - base
        for nm, sva, vs, ra, rs in secs:
            if nm == ".text" and sva <= r < sva + max(vs, rs):
                o = r - sva
                if o < rs:
                    return d[ra + o: ra + o + n]
        return None

    # THIS SWEEP COVERS 330 OF THE 409 REFLECTED CLASSES - 81 %. The population is NOT 330 and an
    # earlier version of this comment said it was: AUDIT-LOG 2026-09-13 established 409 by an
    # independent byte-template scan of the adapter family, with 1,185 of 1,185 appearances
    # resolved to a slot-5 complete-object-locator. 400 construction sites are found here and 330
    # of them put a readable class name in r8; the rest are outside what this method sees, which
    # is not a claim that they lack a parent.
    # THE POPULATION IS 400 CONSTRUCTION SITES, NOT THE 177 OF THE SIZE TABLE. That table was
    # built from one registrar shape; sweeping the image for every call to 00632D80/00632C90 and
    # reading the name string out of r8 finds 400 sites, 330 of them named. Using the smaller
    # table as the population left 13 parents pointing at descriptors "not in this set" - every
    # one a real class, and eight of them the same one (PPhysicsShape).
    def cstr(va, n=96):
        r = va - base
        for nm, sva, vs, ra, rs in secs:
            if sva <= r < sva + vs:
                o = r - sva
                if o >= rs:
                    return None
                b = d[ra + o: ra + o + n]
                z = b.find(bytes([0]))
                t = b[:z if z >= 0 else n].decode("ascii", "replace")
                return t if t and all(32 <= ord(ch) < 127 for ch in t) else None
        return None

    want = {}
    for e, n in fsizes.items():
        if n <= 0 or n > 0x8000:
            continue
        b = blob(e, n)
        if not b:
            continue
        lea, r9 = {}, None
        for i in md.disasm(b, e):
            if (i.mnemonic == "lea" and len(i.operands) == 2
                    and i.operands[1].type == X86_OP_MEM
                    and i.operands[1].value.mem.base == X86_REG_RIP):
                lea[i.operands[0].reg] = i.address + i.size + i.operands[1].value.mem.disp
            elif (i.mnemonic == "mov" and len(i.operands) == 2
                  and i.operands[0].type == X86_OP_REG):
                if (i.operands[0].reg in (X.X86_REG_R9D, X.X86_REG_R9)
                        and i.operands[1].type == X86_OP_IMM):
                    r9 = i.operands[1].imm
                if i.operands[1].type == X86_OP_REG and i.operands[1].reg in lea:
                    lea[i.operands[0].reg] = lea[i.operands[1].reg]
                elif i.operands[1].type != X86_OP_MEM:
                    lea.pop(i.operands[0].reg, None)
            if (i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM
                    and i.operands[0].imm in CTORS):
                nm = cstr(lea[X.X86_REG_R8]) if X.X86_REG_R8 in lea else None
                if nm and r9:
                    want[e] = (nm, r9)
                break

    # first registered member offset per class, from the independently recovered schema
    first = {}
    sr = list(csv.reader(io.open(os.path.join(a.db, SCHEMA_TSV), encoding="utf-8", newline=""),
                         delimiter="\t"))
    sh = sr[0]
    ci, oi = sh.index("class_leaf"), sh.index("offset")
    for r in sr[1:]:
        if len(r) <= max(ci, oi):
            continue
        try:
            o = int(r[oi], 16) if r[oi].lower().startswith("0x") else int(r[oi])
        except ValueError:
            continue
        if r[ci] not in first or o < first[r[ci]]:
            first[r[ci]] = o

    # PASS 0: THE DESCRIPTOR IS NOT IN THE REGISTRAR. Most registrars take it as their own
    # parameter - FUN_005A7ED0 opens `mov [rsp+8], rcx` / `mov rbx, rcx` and passes it straight
    # through - so looking for a `lea rcx` inside them recovered 4 of 177. The address is in the
    # registrar's CALLERS, which do `lea rcx,[descriptor]` / `call <registrar>`. Sweeping every
    # function for that pair recovers 177 of 177 with no ambiguity.
    # FOUR THREAD-SAFE-STATIC GUARDS WERE IN THIS MAP AS IF THEY WERE DESCRIPTORS, found
    # 2026-09-20 (OPUS) from ASTRA-CONTRA-OPUS-PHYRE-CORRECTED-DESCRIPTOR-IDENTITY, which was
    # right. The shape, in 00617E60:
    #
    #     lea rcx, [02CF6678]        a 4-byte guard variable
    #     call 008092FC              _Init_thread_header - rcx is dead after this
    #     ...
    #     call <registrar>           and the sweep below read the stale rcx
    #
    # THE OBVIOUS FIX MADE THINGS WORSE AND IS NOT THE ONE HERE. Dropping the caller-saved
    # registers at every call is correct by the ABI, and it took recovery from 330 to 315:
    # it removed the four wrong answers and ELEVEN right ones, because plenty of registrars
    # really do keep the descriptor in rcx across an intervening call. A conservative
    # dataflow rule cannot tell those apart.
    #
    # So the candidate is TESTED INSTEAD OF TRUSTED, on a positive property. The same sweep
    # records, for every rip-relative address that reaches a call in rcx, whether it reaches
    # something that treats it as a descriptor or something that treats it as a guard:
    #   CTORS            write +0x30/+0x38/+0x3C from their own arguments
    #   006388C0         `mov rsi,[rcx+0x30]`, null-check, `movzx ebx,byte ptr [rsi]` - it
    #                    reads +0x30 AS A STRING
    #   0063BC00         reads [rcx+0xd8] and [rcx+0xfc] and dispatches [rcx] -> [rax+0x60]
    #   008092FC         _Init_thread_header - its argument is a 4-byte guard
    # A guard cannot be the first three's argument and a descriptor is not the fourth's.
    # Over the 330 rows this decides ALL of them: 326 descriptors, 4 guards, 0 undecided.
    INIT_THREAD_HEADER = 0x8092FC
    DESC_CONSUMERS = (0x6388C0, 0x63BC00)
    proven_desc, proven_guard = set(), set()

    desc_of, parent_of = {}, {}
    cand = collections.defaultdict(set)
    reg2cls = {e: c for e, (c, _s) in want.items()}
    for e, n in fsizes.items():
        if n <= 0 or n > 0x8000:
            continue
        b = blob(e, n)
        if not b:
            continue
        held = {}
        for i in md.disasm(b, e):
            if (i.mnemonic == "lea" and len(i.operands) == 2
                    and i.operands[1].type == X86_OP_MEM
                    and i.operands[1].value.mem.base == X86_REG_RIP):
                held[i.operands[0].reg] = i.address + i.size + i.operands[1].value.mem.disp
            elif (i.mnemonic == "mov" and len(i.operands) == 2
                  and i.operands[0].type == X86_OP_REG):
                if i.operands[1].type == X86_OP_REG and i.operands[1].reg in held:
                    held[i.operands[0].reg] = held[i.operands[1].reg]
                elif i.operands[1].type != X86_OP_MEM:
                    held.pop(i.operands[0].reg, None)
            if i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM:
                tgt = i.operands[0].imm
                if tgt in reg2cls and X.X86_REG_RCX in held:
                    cand[reg2cls[tgt]].add(held[X.X86_REG_RCX])
                # The same sweep records what each rip-relative address IS, so a candidate
                # can be tested rather than trusted. See is_descriptor below.
                if X.X86_REG_RCX in held:
                    if tgt in CTORS or tgt in DESC_CONSUMERS:
                        proven_desc.add(held[X.X86_REG_RCX])
                    elif tgt == INIT_THREAD_HEADER:
                        proven_guard.add(held[X.X86_REG_RCX])
    def is_guard(a):
        """True only when the address is USED as a thread-safe-static guard and never as a
        descriptor. Both halves matter: rejecting on the guard use alone would drop an
        address that is legitimately both, and nothing here assumes that cannot happen."""
        return a in proven_guard and a not in proven_desc

    rejected = []
    for c, raw in cand.items():
        kept = {a for a in raw if not is_guard(a)}
        if len(raw) != len(kept):
            rejected.append((c, sorted(raw - kept)))
        if len(kept) == 1:
            desc_of[c] = list(kept)[0]
    if rejected:
        sys.stderr.write("gen_phyre_parent_chain: %d class(es) had a GUARD offered as their "
                         "descriptor and it was rejected:\n" % len(rejected))
        for c, bad in sorted(rejected):
            sys.stderr.write("    %-34s rejected %s\n"
                             % (c, " ".join("%#010x" % a for a in bad)))

    # pass 1: the parent descriptor, from caller arg6, per registrar
    for entry, (cls, _sz) in want.items():
        n = fsizes.get(entry)
        if not n:
            continue
        b = blob(entry, n)
        if not b:
            continue
        lea = {}          # register -> most recent rip-relative target
        stack = {}        # stack displacement -> value written
        for i in md.disasm(b, entry):
            if (i.mnemonic == "lea" and len(i.operands) == 2
                    and i.operands[1].type == X86_OP_MEM
                    and i.operands[1].value.mem.base == X86_REG_RIP):
                lea[i.operands[0].reg] = i.address + i.size + i.operands[1].value.mem.disp
            elif (i.mnemonic == "mov" and len(i.operands) == 2
                  and i.operands[0].type == X86_OP_MEM
                  and i.operands[0].value.mem.base == X.X86_REG_RSP):
                disp = i.operands[0].value.mem.disp
                src = i.operands[1]
                if src.type == X86_OP_REG and src.reg in lea:
                    stack[disp] = lea[src.reg]
                elif src.type == X86_OP_IMM:
                    stack[disp] = src.imm
                else:
                    stack.pop(disp, None)
            elif (i.mnemonic == "mov" and len(i.operands) == 2
                  and i.operands[0].type == X86_OP_REG):
                # THE DESCRIPTOR USUALLY ARRIVES IN RCX BY WAY OF ANOTHER REGISTER. The 5-argument
                # form is `lea rbx,[desc]` ... `mov rcx, rbx` / `call 00632C90`, so dropping every
                # register-to-register move recovered 0 descriptors out of 177.
                if i.operands[1].type == X86_OP_REG and i.operands[1].reg in lea:
                    lea[i.operands[0].reg] = lea[i.operands[1].reg]
                elif i.operands[1].type != X86_OP_MEM:
                    lea.pop(i.operands[0].reg, None)
            if (i.mnemonic == "call" and i.operands
                    and i.operands[0].type == X86_OP_IMM and i.operands[0].imm in CTORS):
                if (cls not in desc_of and X.X86_REG_RCX in lea
                        and not is_guard(lea[X.X86_REG_RCX])):
                    desc_of[cls] = lea[X.X86_REG_RCX]
                # ARG 6 IS AT CALLER [rsp+0x28], NOT [rsp+0x30]. The constructor reads it at
                # `mov rax,[rsp+0x30]` (00632DD1) because the call pushed a return address; in
                # the caller's frame arg5 is 0x20 and arg6 is 0x28. Reading 0x30 here found a
                # parent for 12 registrars out of 177, all of them by accident.
                p = stack.get(0x28)
                if p:
                    parent_of[cls] = p
                break

    by_desc = {v: k for k, v in desc_of.items()}
    size_of = {c: s for c, s in want.values()}

    out = []
    for cls in sorted(desc_of):
        pd = parent_of.get(cls)
        pname = by_desc.get(pd) if pd else None
        out.append((cls, "0x%08X" % desc_of[cls], "0x%X" % size_of.get(cls, 0),
                    ("0x%08X" % pd) if pd else "",
                    pname or ("(descriptor not in this set)" if pd else "(no parent / root)"),
                    ("0x%X" % size_of[pname]) if pname in size_of else "",
                    ("0x%X" % first[cls]) if cls in first else ""))

    print("classes with a descriptor address recovered : %d of %d"
          % (len(desc_of), len(want)))
    print("classes carrying a non-null parent          : %d" % len(parent_of))
    print("parents resolved to a class in this set     : %d"
          % sum(1 for r in out if r[4] and not r[4].startswith("(")))
    print()

    # CONTROLS
    bad_size, bad_first, comparable = [], [], 0
    for cls, _da, csz, _pa, pname, psz, fm in out:
        if not psz:
            continue
        comparable += 1
        if int(psz, 16) > int(csz, 16):
            bad_size.append((cls, csz, pname, psz))
        if fm and int(fm, 16) < int(psz, 16):
            bad_first.append((cls, fm, pname, psz))
    print("CONTROL 1  parent.instance_size <= child.instance_size")
    print("           comparable %d | violations %d" % (comparable, len(bad_size)))
    for b in bad_size[:6]:
        print("             %-38s child %-8s parent %-30s %s" % b)
    print("CONTROL 2  child's first registered member >= parent.instance_size")
    print("           comparable %d | violations %d"
          % (sum(1 for r in out if r[5] and r[6]), len(bad_first)))
    for b in bad_first[:6]:
        print("             %-38s first %-8s parent %-30s %s" % b)

    pdl = [r for r in out if r[0] == "PDeferredLightingBase"]
    print()
    print("PREDICTION made before reading: PDeferredLightingBase's parent is about 0x40D0 bytes")
    if pdl:
        print("           got parent %s size %s (its first member is at %s)"
              % (pdl[0][4], pdl[0][5] or "(unknown)", pdl[0][6] or "(unknown)"))
    else:
        print("           PDeferredLightingBase's registrar is not in the size table")

    ok = (not bad_size) and len(bad_first) <= max(1, comparable // 20)
    print()
    if not ok:
        print("CONTROLS FAILED -> the `+0x78 = parent` reading is not supported by the sizes.")
        print("Discard the table; a base class cannot be larger than what contains it.")
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write("# Phyre base-class chain, read from the 6th argument of the class-descriptor\n")
            fh.write("# constructor 00632D80/00632C90, which the ctor stores to descriptor +0x78.\n")
            fh.write("class_leaf\tdescriptor\tinstance_size\tparent_descriptor\tparent_class\t"
                     "parent_instance_size\tfirst_registered_member\n")
            for r in out:
                fh.write("\t".join(r) + "\n")
        print("wrote %s (%d rows)" % (a.out, len(out)))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
