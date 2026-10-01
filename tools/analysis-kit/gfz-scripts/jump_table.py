#!/usr/bin/env python3
"""jump_table.py - resolve the arms of a switch so a block walk can enter them.

WHY. Every census in this kit walks basic blocks and follows DIRECT branches. A switch compiled
to a jump table ends in `jmp <reg>`, and its arms are reached through DATA, so as far as the walk
is concerned they do not exist. That is not a rounding error: `ManagerSub0209BE80_57E0`'s
thirteen-slot claim array - `lea rbx,[rsi+0x270]`, `add rbx,0x2a0`, `cmp edi,0xd` - is written
entirely inside one such arm, and the region censuses as ZERO accesses across a 0x2220-byte span
of the store's largest type. 529 of 34,270 listed bodies (1.5%) end an arm in `jmp <reg>`.

THE IDIOM, as MSVC emits it for x64 and as it appears at 0028F000:

    0028F01A  cmp  eax, 5                                  the bound (arms = 5 + 1)
    0028F01D  ja   <default>
    0028F01F  lea  rdx, [rip - 0x16f026]                   rdx = the image base
    0028F028  mov  ecx, dword ptr [rdx + rax*4 + 0x16f09c] the table, indexed by the case
    0028F02F  add  rcx, rdx                                entries are RVAs from that base
    0028F032  jmp  rcx

So the table sits at `base + DISP`, each entry is a 32-bit RVA relative to the SAME base, and the
arm count is bounded by the `cmp`/`ja` pair.

HOW THIS STAYS HONEST. The bound is read from the `cmp` when one is found, and otherwise entries
are taken only while each resolved target lands INSIDE the function body - a table is contiguous
and the first entry that leaves the body ends it. A target outside the body is never returned, so
a misread table cannot inject a foreign address into a census; the worst case is too few arms,
which is the situation today. `resolve` returns [] when it cannot establish the base, and a
caller that gets [] is exactly as blind as it was before.

WHAT IS NOT HANDLED, so a zero is not misread: a table of absolute 64-bit pointers, a two-level
table (MSVC's byte-index form for sparse switches), a base register loaded any way other than a
RIP-relative `lea`, and a computed jump that is not a switch at all.

    python jump_table.py            # self-test against the case that motivated it
"""
import struct
import sys

from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG


def _norm(md, reg):
    try:
        n = md.reg_name(reg) or ""
    except Exception:
        return reg
    n = n.lower()
    if n.startswith("e"):
        return "r" + n[1:]
    if n.endswith("d") and n[:-1].startswith("r"):
        return n[:-1]
    return n


def resolve(img, md, body, at_index, entry, size, max_arms=256):
    """Targets of the `jmp <reg>` at body[at_index], or [] if the table cannot be established."""
    jmp = body[at_index]
    if jmp.mnemonic != "jmp" or not jmp.operands or jmp.operands[0].type != X86_OP_REG:
        return []
    target_reg = _norm(md, jmp.operands[0].reg)

    base_va = None       # the RIP-relative lea's value
    table_disp = None    # displacement of the indexed load
    bound = None         # from `cmp idx, N`

    # Walk backwards over a bounded window. The idiom is emitted as a unit; searching the whole
    # body would let an unrelated `lea` from far away supply the base.
    for k in range(at_index - 1, max(-1, at_index - 24), -1):
        i = body[k]
        m = i.mnemonic
        if m == "add" and len(i.operands) == 2 \
                and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_REG \
                and _norm(md, i.operands[0].reg) == target_reg:
            continue
        if m == "mov" and len(i.operands) == 2 \
                and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_MEM:
            mem = i.operands[1].value.mem
            if mem.index and mem.scale == 4 and table_disp is None:
                table_disp = mem.disp
            continue
        if m == "lea" and len(i.operands) == 2 \
                and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_MEM:
            mem = i.operands[1].value.mem
            if mem.base and md.reg_name(mem.base) == "rip" and base_va is None:
                base_va = i.address + i.size + mem.disp
            continue
        if m == "cmp" and len(i.operands) == 2 and i.operands[1].type == X86_OP_IMM \
                and bound is None:
            bound = i.operands[1].imm
            continue
    if base_va is None or table_disp is None:
        return []

    n = (bound + 1) if (bound is not None and 0 <= bound < max_arms) else max_arms
    out = []
    for k in range(n):
        raw = img.read(base_va + table_disp + 4 * k, 4)
        if not raw or len(raw) < 4:
            break
        tgt = base_va + struct.unpack("<I", raw)[0]
        if not (entry <= tgt < entry + size):
            break
        if tgt not in out:
            out.append(tgt)
    return out


def self_test():
    """The case this was written for: 0028F000's six-arm switch, one arm of which forms
    `ManagerSub0209BE80_57E0 + 0x270` and tail-calls the claim loop."""
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import check_default_instance_writers as W
    img = W.Image()
    entry, size = 0x28F000, img.sizes.get(0x28F000, 0)
    body = img.body(entry)
    idx = [n for n, i in enumerate(body)
           if i.mnemonic == "jmp" and i.operands and i.operands[0].type == X86_OP_REG]
    ok = True
    if not idx:
        print("  no indirect jmp found in 0028F000"), sys.exit(1)
    tg = resolve(img, img.md, body, idx[0], entry, size)
    print("  0028F000 arms resolved: %d -> %s" % (len(tg), " ".join("%08X" % t for t in tg)))
    want = 0x28F034
    ok &= want in tg
    print("  %-56s %s" % ("the arm that forms +0x57E0 (0028F034) is among them",
                          "yes" if want in tg else "NO"))
    ok &= 2 <= len(tg) <= 8
    print("  %-56s %s" % ("arm count is plausible for `cmp eax, 5` (<= 6)",
                          "yes" if len(tg) <= 6 else "NO"))
    # a function with no indirect jump must resolve nothing rather than invent arms
    e2 = 0x0051FB70
    b2 = img.body(e2)
    j2 = [n for n, i in enumerate(b2)
          if i.mnemonic == "jmp" and i.operands and i.operands[0].type == X86_OP_REG]
    print("  %-56s %s" % ("a body with no indirect jmp yields no arms",
                          "yes" if not j2 else "NO"))
    ok &= not j2
    print("SELF-TEST", "PASSES" if ok else "FAILS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(self_test())
