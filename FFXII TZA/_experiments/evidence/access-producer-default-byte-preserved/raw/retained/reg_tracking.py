#!/usr/bin/env python3
"""reg_tracking.py - which registers does an instruction actually WRITE?

THE DEFECT THIS FIXES WAS IN SHIPPED CENSUS OUTPUT, not in theory. Every forward register tracker
in this kit dropped a tracked register with this rule:

    # any write to a held register drops it
    if ins.operands and ins.operands[0].type == X86_OP_REG:
        drop(ins.reg_name(ins.operands[0].reg))

The first operand of an x86 instruction is not necessarily written. `test rbx, rbx`, `cmp rbx, rax`,
`push rbx` and `jmp rbx` all read their first operand and write nothing but flags - and capstone
agrees: `test rbx, rbx`.regs_access() returns writes `['rflags']` and nothing else.

WHY IT MATTERED SO MUCH HERE. The idiom the rule breaks on is the commonest one in this image:

    mov  rbx, qword ptr [rip -> singleton]
    test rbx, rbx                              <- tracking stopped HERE
    je   bail
    cmp  dword ptr [rbx + 0x120], 0            <- never recorded

A singleton is loaded and immediately null-checked, so on that path the tracker discarded the object
at the exact instruction after which the accesses occur, and it did so silently.

HOW MUCH IT COST, MEASURED rather than asserted. Over all eleven PTR-route types the corrected rule
finds 995 distinct accesses against 926 - a factor of 1.07, not a landslide. Two types carry nearly
all of it (LegacyPs2GsTextureContext 6 -> 16, ManagerSingleton0209BE80 202 -> 258); six are
unchanged; and GameSettingConfig goes DOWN by three.

Those three are worth knowing about, because they are not one story. ONE is a false access the old
rule should never have recorded: it read `mov eax, [rax+4]` off an `rax` that `mul rcx` had already
destroyed - `mul` writes rax and rdx implicitly and names neither as operand zero, so the old rule
could not see the clobber. THE OTHER TWO are real accesses this rule now misses, at a branch target
whose fall-through path contains `mov eax, [rax+0x2c]`. Killing the base there is correct per
instruction and wrong per path, because these scanners are a LINEAR SWEEP with no control flow.
Both rules are floors, and neither is sound on branching code.

THE RULE HERE. `capstone`'s `regs_access()` reports the real write set. A write to any part of a
register kills the whole thing for tracking purposes: `mov eax, 1` zeroes the upper half, and
`mov al, 1` leaves a value that is no longer the pointer. Both are a kill, so sub-registers are
normalised to their 64-bit parent.

`regs_access()` raises if capstone was built without the detail tables, so `written()` falls back to
the explicit-operand write flags, which are still far better than "operand zero".
"""
from capstone.x86 import X86_OP_REG

_PARENT = {}
for _q, _parts in {
    "rax": "eax ax al ah", "rbx": "ebx bx bl bh", "rcx": "ecx cx cl ch",
    "rdx": "edx dx dl dh", "rsi": "esi si sil", "rdi": "edi di dil",
    "rbp": "ebp bp bpl", "rsp": "esp sp spl",
    "r8": "r8d r8w r8b", "r9": "r9d r9w r9b", "r10": "r10d r10w r10b",
    "r11": "r11d r11w r11b", "r12": "r12d r12w r12b", "r13": "r13d r13w r13b",
    "r14": "r14d r14w r14b", "r15": "r15d r15w r15b",
}.items():
    _PARENT[_q] = _q
    for _p in _parts.split():
        _PARENT[_p] = _q


def canon(name):
    """The 64-bit register a name belongs to, or the name itself."""
    return _PARENT.get(name, name)


def op_kind(ins, op, oi):
    """'addr', 'w', 'rw' or 'r' for a memory operand - from its ACCESS FLAGS, not its position.

    The same positional shortcut that broke register tracking also mislabels the census output:
    `kind = "w" if oi == 0 else "r"` calls `cmp dword ptr [rbx+0x120], 0` a WRITE, because the
    memory operand comes first. `cmp` and `test` only read. A consumer of the census that believes
    the label concludes the engine stores to a field it merely tests, which is the opposite of what
    the instruction says.

    capstone sets CS_AC_READ (1) / CS_AC_WRITE (2) per operand. `lea` is reported separately
    because its operand is an address computation and is neither read nor written.

    CAPSTONE'S FLAGS ARE THEMSELVES WRONG FOR SOME ENCODINGS, and the field-access index shipped
    238 reversed labels because of it (OPUS, 2026-09-24). Measured over every memory operand in
    the image against iced-x86 (opkind_vs_iced.py), capstone 5.0.7:
      - flags the STORE form of movups/movq/movd/movhps/movhpd/movlpd/vmov*/setcc as READ
        (13,816 movups stores alone);
      - gives `test byte/word/dword ptr [m], reg` NO flag, so the positional fallback called a
        compare a WRITE (477 sites);
      - flags `lock cmpxchg [m]` as READ only; it is read-modify-write;
      - flags nop/prefetch as READ; neither touches the operand architecturally.
    So the mnemonic tables below are consulted FIRST, each taken from the SDM operation of the
    instruction, and the operand flags only for everything else. An operand with no flag after
    that is "?", never a guess: the positional rule is the defect this function exists to remove.
    """
    mn = ins.mnemonic.split()[-1]          # "lock cmpxchg" -> "cmpxchg"
    if mn == "lea" or mn == "nop" or mn.startswith("prefetch"):
        return "addr"
    if mn in _READ_ONLY:
        return "r"
    if mn in _RMW:
        return "rw"
    if mn in _MOVE or mn.startswith("set"):
        return "w" if oi == 0 else "r"
    acc = getattr(op, "access", 0)
    if acc:
        w, r = bool(acc & 2), bool(acc & 1)
        if w and r:
            return "rw"
        if w:
            return "w"
        if r:
            return "r"
    return "?"


# Compares: the memory operand is read wherever it stands; only flags are written.
_READ_ONLY = frozenset("test cmp bt comiss comisd ucomiss ucomisd vcomiss vcomisd vucomiss "
                       "vucomisd ptest vptest outsb outsw outsd".split())
# Atomic exchanges: the memory operand is read and (conditionally) written.
_RMW = frozenset("cmpxchg cmpxchg8b cmpxchg16b xadd xchg".split())
# Pure moves: a memory operand 0 is a destination (written, not read), anywhere else a source.
_MOVE = frozenset(
    "mov movzx movsx movsxd movbe movnti "
    "movups movupd movaps movapd movdqu movdqa movss movsd movq movd "
    "movlps movlpd movhps movhpd movntps movntpd movntdq movntq "
    "pextrb pextrw pextrd pextrq extractps "
    "vmovups vmovupd vmovaps vmovapd vmovdqu vmovdqa vmovss vmovsd vmovq vmovd "
    "vmovlps vmovlpd vmovhps vmovhpd vmovntps vmovntpd vmovntdq vextractps "
    "vpextrb vpextrw vpextrd vpextrq vextractf128 vextracti128".split())


def written(ins):
    """The set of 64-bit register names this instruction writes.

    Flags and non-general registers are returned as capstone names them; callers that track
    general registers simply never hold those.
    """
    try:
        _, w = ins.regs_access()
        out = {canon(ins.reg_name(r)) for r in w}
    except Exception:
        out = set()
        for op in ins.operands:
            if op.type == X86_OP_REG and getattr(op, "access", 0) & 2:
                out.add(canon(ins.reg_name(op.reg)))
    # CAPSTONE'S IMPLICIT-WRITE TABLES ARE WRONG FOR THREE MNEMONICS IN THIS IMAGE, measured
    # against iced-x86 over all 1,775,860 decoded instructions (regwrites_vs_iced.py,
    # 2026-09-24). The first is the dangerous direction - a MISSED kill lets a tracker credit
    # accesses to an object the register no longer holds (receiver overwrite):
    #   cmpxchg        writes rax on failure; capstone omits it          (30 sites)
    #   cmpxchg8b/16b  write rdx:rax on failure                          (same rule)
    #   cdq/cqo/cwd    write rdx only; capstone also kills rax           (1,031 sites)
    #   test           writes flags only; capstone kills rax for `test eax, imm` (208 sites)
    mn = ins.mnemonic.split()[-1]
    if mn == "cmpxchg":
        out.add("rax")
    elif mn in ("cmpxchg8b", "cmpxchg16b"):
        out |= {"rax", "rdx"}
    elif mn in ("cdq", "cqo", "cwd"):
        out.discard("rax")
    elif mn == "test":
        out = {r for r in out if r not in _GPR64}
    return out


_GPR64 = frozenset(set(_PARENT.values()))
