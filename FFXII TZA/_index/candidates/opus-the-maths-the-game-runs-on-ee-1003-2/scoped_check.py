"""scoped_check.py - the committed checker for "scoped row: set-exact" engine_explained rows (SWE2-AUDIT-SPEC ruling
auditspec-ruling-scoped-ee-row-1003, condition 3). Written 2026-10-03 (local-ee-drafter for OPUS); v2 the same day,
answering the independent review tmp/verify_scoped.json (defects D1-D8; v1 kept as scoped_check_v1.py).

For a function it derives, from the image alone:
  CALLS  - every direct call (target VA, or import:Name when the target is an import or a jmp [IAT] thunk), every call
           through a rip-relative pointer (import:Name or ptr:VA), every indirect call by operand ([rax+0x30], rax),
           every tail-jump (jmp to a VA outside the function's extent, or jmp [IAT] / jmp [ptr]), every conditional jump
           leaving the extent (jcc:VA), every jump-table arm outside the extent (tail:VA), and every indirect jmp that
           is not a resolved jump-table dispatch (ijmp:operand).
  STORES - every explicit memory write that is not stack-relative, as width + address expression:
           width b/w/d/q/x/y/t (1/2/4/8/16/32/10 bytes); address = absolute VA for rip-relative and image-base-relative
           forms (with +reg*scale when indexed), else [base+index*scale+disp]. rep movs/stos print as 'rep:<mnemonic>'.

EXTENT AND DECODE (v2, D4/D5). The extent is the .pdata chain of the function (every RUNTIME_FUNCTION whose chain root is
the entry). Code is decoded by RECURSIVE DESCENT from the entry: fall-through, jcc / jmp targets inside the extent and
resolved jump-table arms. A jump table is resolved from its own instructions - `jmp R` after `add R, IB`,
`mov R32, dword [IB + I*4 + T]` (optionally `movzx I, byte [IB + J + B]` for a two-level table), IB loaded by
`lea IB, [rip -> image base]`, and the bound from the nearest `cmp I, imm` + ja/jae/jbe/jb - and its arms become edges
(an arm outside the extent is a tail:VA call). Fail closed: an unresolvable table shape is ijmp:R; an instruction
overlapping another, a jump into a table, or falling off the extent FAILS; and the decoded code plus the resolved
tables plus nop/int3 padding must tile every fragment exactly, so no in-extent code byte goes unread.

STACK AND IMAGE-BASE ALIASES (v2, D1/D2/D3). A register is a stack alias when it holds rsp + constant (`mov r, S` /
`lea r, [S + d]` with S a stack alias, no index), and an image-base register after `lea r, [rip -> image base]`. Both
sets are a MUST dataflow over the instruction-level CFG: the state entering an instruction is the INTERSECTION over its
predecessors (the entry starts with {rsp} / {}), iterated to a fixpoint. Any register write kills the alias of its
64-bit parent (a 32/16/8-bit write included), and a call kills rax, rcx, rdx, r8, r9, r10 and r11. A store whose base is
a stack alias in the state entering it is a stack store and not reported.

WRITE CLASSIFICATION (v2, D6/D7). One classifier, `insn_stores`, used by derive() and by the controls alike. A memory
FIRST operand is a write when the mnemonic is in WRITE, a read when it is in READ, and the function FAILS when it is in
neither (fail closed). A memory operand later in the list is a write only when capstone flags it CS_AC_WRITE and the
mnemonic is in WRITE. pop [mem] is a store; push [mem] is not. maskmovq / maskmovdqu / vmaskmovdqu (an implicit [rdi]
store) FAIL the function.

Usage:
  scoped_check.py --dump FN...            print the derived sets (canonical tokens)
  scoped_check.py --tables FN...          print the resolved jump tables
  scoped_check.py REPORT.json             check every scoped row of an ee report: the sets stated after 'Calls:' and
                                          'Stores:' must equal the derived sets; prints FAILS n
  scoped_check.py --self-test FN          the derived row passes; a row with one call removed and a row with one store's
                                          width changed both fail
  scoped_check.py --controls              instruction controls, synthetic body controls and real body controls, all
                                          through derive()'s own code path; prints CONTROL FAILS n
"""
import json, re, struct, sys
import capstone
from capstone import x86 as X
import pefile

EXE = r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe"
pe = pefile.PE(EXE, fast_load=False)
BASE = pe.OPTIONAL_HEADER.ImageBase
TEXT = next(s for s in pe.sections if s.Name.rstrip(b"\0") == b".text")
TLO, THI = BASE + TEXT.VirtualAddress, BASE + TEXT.VirtualAddress + TEXT.Misc_VirtualSize
IAT = {}
for d in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []):
    for imp in d.imports:
        IAT[imp.address] = (imp.name.decode() if imp.name else "ord%d" % imp.ordinal)
MEM = pe.get_memory_mapped_image()
OVERLAY = {}            # synthetic control bodies: start VA -> bytes (read before the image)


def rd(va, n):
    for lo, b in OVERLAY.items():
        if lo <= va < lo + len(b):
            return b[va - lo:va - lo + n]
    return MEM[va - BASE:va - BASE + n]


# .pdata: begin, end, unwind (RVAs) -> chain roots
PD = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
pdata = []
raw = pe.get_data(PD.VirtualAddress, PD.Size)
for i in range(0, len(raw) - 11, 12):
    b, e, u = struct.unpack_from("<III", raw, i)
    if b:
        pdata.append((b, e, u))


def root_of(entry):
    b, e, u = entry
    seen = 0
    while True:
        ui = pe.get_data(u & ~1, 4)
        flags = ui[0] >> 3
        if not flags & 0x4:
            return b
        cnt = ui[2]
        off = 4 + ((cnt + 1) & ~1) * 2
        pb, pe_, pu = struct.unpack("<III", pe.get_data((u & ~1) + off, 12))
        b, e, u = pb, pe_, pu
        seen += 1
        if seen > 32:
            return b


ROOT = {}
for ent in pdata:
    ROOT.setdefault(root_of(ent), []).append(ent)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
W = {1: "b", 2: "w", 4: "d", 8: "q", 16: "x", 32: "y", 10: "t"}

# ---- register families (D3): every written register kills the alias of its 64-bit parent
REGID = {n[len("X86_REG_"):].lower(): getattr(X, n) for n in dir(X) if n.startswith("X86_REG_")}
PARENT = {}
for fam in (("rax", "eax", "ax", "al", "ah"), ("rbx", "ebx", "bx", "bl", "bh"), ("rcx", "ecx", "cx", "cl", "ch"),
            ("rdx", "edx", "dx", "dl", "dh"), ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"),
            ("rbp", "ebp", "bp", "bpl"), ("rsp", "esp", "sp", "spl")) + tuple(
        ("r%d" % n, "r%dd" % n, "r%dw" % n, "r%db" % n) for n in range(8, 16)):
    for r in fam:
        if r in REGID:
            PARENT[REGID[r]] = REGID[fam[0]]
RSP = X.X86_REG_RSP
VOLATILE = {REGID[r] for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")}


def parent(r):
    return PARENT.get(r, r)


# ---- write classification (D6/D7): explicit lists, fail closed on a memory first operand in neither
WRITE = {
    "mov", "movabs", "movbe", "movnti", "movntq", "movntdq", "movntps", "movntpd", "movss", "movsd", "movsb", "movsw",
    "movsq", "movaps", "movapd", "movups", "movupd", "movdqa", "movdqu", "movq", "movd", "movhps", "movhpd", "movlps",
    "movlpd", "add", "adc", "sub", "sbb", "and", "or", "xor", "not", "neg", "inc", "dec", "shl", "shr", "sal", "sar",
    "rol", "ror", "rcl", "rcr", "shld", "shrd", "xchg", "xadd", "cmpxchg", "cmpxchg8b", "cmpxchg16b", "bts", "btr",
    "btc", "stosb", "stosw", "stosd", "stosq", "insb", "insw", "insd", "pop", "fst", "fstp", "fist", "fistp", "fisttp",
    "fbstp", "fstsw", "fnstsw", "fstcw", "fnstcw", "fstenv", "fnstenv", "fsave", "fnsave", "stmxcsr", "vstmxcsr",
    "fxsave", "fxsave64", "xsave", "xsave64", "xsaveopt", "xsaveopt64", "xsavec", "xsavec64", "xsaves", "xsaves64",
    "sgdt", "sidt", "sldt", "str", "smsw", "pextrb", "pextrw", "pextrd", "pextrq", "vpextrb", "vpextrw", "vpextrd",
    "vpextrq", "extractps", "vextractps", "vextractf128", "vextracti128", "vcvtps2ph", "vmaskmovps", "vmaskmovpd",
    "vpmaskmovd", "vpmaskmovq", "seto", "setno", "setb", "setae", "sete", "setne", "setbe", "seta", "sets", "setns",
    "setp", "setnp", "setl", "setge", "setle", "setg",
    "vmovss", "vmovsd", "vmovaps", "vmovapd", "vmovups", "vmovupd", "vmovdqa", "vmovdqu", "vmovq", "vmovd", "vmovhps",
    "vmovhpd", "vmovlps", "vmovlpd", "vmovntdq", "vmovntps", "vmovntpd"}
READ = {
    "cmp", "test", "bt", "push", "call", "jmp", "nop", "lea", "clflush", "clflushopt", "clwb", "invlpg", "prefetch",
    "prefetcht0", "prefetcht1", "prefetcht2", "prefetchnta", "prefetchw", "fld", "fild", "fbld", "fcom", "fcomp",
    "ficom", "ficomp", "fadd", "fsub", "fsubr", "fmul", "fdiv", "fdivr", "fiadd", "fisub", "fisubr", "fimul", "fidiv",
    "fidivr", "fldcw", "fldenv", "frstor", "fxrstor", "fxrstor64", "xrstor", "xrstor64", "xrstors", "xrstors64",
    "ldmxcsr", "vldmxcsr", "lgdt", "lidt", "lldt", "ltr", "lmsw", "verr", "verw", "ucomiss", "ucomisd", "comiss",
    "comisd", "vucomiss", "vucomisd", "vcomiss", "vcomisd", "ptest", "vptest", "mul", "imul", "div", "idiv", "cmpsb",
    "cmpsw", "cmpsd", "cmpsq", "scasb", "scasw", "scasd", "scasq"}
IMPLICIT_STORE = ("maskmovq", "maskmovdqu", "vmaskmovdqu")


class CheckError(RuntimeError):
    pass


def base_mnemonic(m):
    for p in ("lock ", "rep ", "repe ", "repne ", "repz ", "repnz ", "notrack ", "bnd "):
        if m.startswith(p):
            m = m[len(p):]
    return m


def regname(r):
    return md.reg_name(r) if r else ""


def render(i, op, ib):
    mm = op.mem
    if mm.base == X.X86_REG_RIP:
        return "[%08X]" % (i.address + i.size + mm.disp)
    if mm.base in ib or (mm.index in ib and mm.scale == 1):
        other = mm.index if mm.base in ib else mm.base
        s = "[%08X" % (BASE + mm.disp)
        if other and other != X.X86_REG_INVALID:
            s += "+%s%s" % (regname(other), "*%d" % mm.scale if mm.scale > 1 and other == mm.index else "")
        return s + "]"
    s = "[" + regname(mm.base)
    if mm.index:
        s += "+%s*%d" % (regname(mm.index), mm.scale)
    if mm.disp:
        s += ("+0x%X" % mm.disp) if mm.disp > 0 else ("-0x%X" % -mm.disp)
    return s + "]"


def insn_stores(i, stack, ib):
    """The store tokens of one instruction, given the stack-alias and image-base sets live BEFORE it. Raises
    CheckError for a memory destination it cannot classify (fail closed). Used by derive() and the controls."""
    m = i.mnemonic
    if m.startswith(("rep", "repe", "repne")) and ("stos" in m or "movs" in m):
        return ["rep:" + m.replace(" ", "_")]
    b = base_mnemonic(m)
    if b in IMPLICIT_STORE:
        raise CheckError("%08X %s: implicit [rdi] store" % (i.address, m))
    out = []
    for n, op in enumerate(i.operands):
        if op.type != X.X86_OP_MEM:
            continue
        flagged = bool(op.access & capstone.CS_AC_WRITE)
        if n == 0:
            if b in WRITE:
                write = True
            elif b in READ:
                write = False   # the list decides: capstone 5 flags frstor's source as written, for one
            else:
                raise CheckError("%08X %s %s: memory destination in neither list" % (i.address, m, i.op_str))
        else:
            if flagged and b not in WRITE:
                raise CheckError("%08X %s %s: flagged write on an unlisted mnemonic" % (i.address, m, i.op_str))
            write = flagged
        if not write or b in ("push", "call", "jmp"):
            continue
        if op.mem.base in stack:
            continue
        out.append(W.get(op.size, str(op.size)) + render(i, op, ib))
    return out


# v3 (N1): register writes capstone 5's regs_access() does not report, merged into every kill set
IMPLICIT_WRITES = {
    "cmpxchg": ("rax",), "cmpxchg8b": ("rax", "rdx"), "cmpxchg16b": ("rax", "rdx"), "xlatb": ("rax",),
    "enter": ("rbp",), "leave": ("rbp",), "syscall": ("rcx", "r11"), "sysenter": ("rcx", "r11"),
    "cpuid": ("rax", "rbx", "rcx", "rdx"), "rdtsc": ("rax", "rdx"), "rdtscp": ("rax", "rcx", "rdx"),
    "rdpmc": ("rax", "rdx"), "xgetbv": ("rax", "rdx"), "rdmsr": ("rax", "rdx"), "cwd": ("rdx",), "cdq": ("rdx",),
    "cqo": ("rdx",), "cbw": ("rax",), "cwde": ("rax",), "cdqe": ("rax",), "mul": ("rax", "rdx"), "div": ("rax", "rdx"),
    "idiv": ("rax", "rdx"), "lodsb": ("rax", "rsi"), "lodsw": ("rax", "rsi"), "lodsd": ("rax", "rsi"),
    "lodsq": ("rax", "rsi"), "stosb": ("rdi",), "stosw": ("rdi",), "stosd": ("rdi",), "stosq": ("rdi",),
    "movsb": ("rsi", "rdi"), "movsw": ("rsi", "rdi"), "movsq": ("rsi", "rdi"), "cmpsb": ("rsi", "rdi"),
    "cmpsw": ("rsi", "rdi"), "cmpsd": ("rsi", "rdi"), "cmpsq": ("rsi", "rdi"), "scasb": ("rdi",), "scasw": ("rdi",),
    "scasd": ("rdi",), "scasq": ("rdi",), "loop": ("rcx",), "loope": ("rcx",), "loopne": ("rcx",)}
REP_WRITES = ("rcx",)   # any rep / repe / repne prefix also counts rcx down


def implicit_kills(i):
    m = i.mnemonic
    b = base_mnemonic(m)
    regs = set(IMPLICIT_WRITES.get(b, ()))
    if b == "imul" and len(i.operands) == 1:
        regs |= {"rax", "rdx"}
    if b in ("movsd", "cmpsd") and not (i.operands and all(o.type == X.X86_OP_MEM for o in i.operands)):
        regs -= {"rsi", "rdi"}       # the SSE forms (a register or immediate operand), not the string forms
    elif b == "movsd":
        regs |= {"rsi", "rdi"}
    if m != b and m.startswith(("rep", "repe", "repne", "repz", "repnz")):
        regs |= set(REP_WRITES)
    return {REGID[r] for r in regs}


def written_regs(i):
    """64-bit parents of every register i writes: capstone's report plus the implicit table. A capstone error FAILS
    the function (v3, N2: assuming 'nothing written' would keep aliases alive across unknown effects)."""
    try:
        _, wr = i.regs_access()
    except capstone.CsError as e:
        raise CheckError("%08X %s %s: capstone cannot report its register writes (%s)" % (i.address, i.mnemonic,
                                                                                         i.op_str, e))
    return {parent(r) for r in wr} | implicit_kills(i)


def transfer(i, stack, ib):
    """Alias sets after instruction i (MUST: anything not modelled kills)."""
    ops, m = i.operands, i.mnemonic
    kill = written_regs(i)
    if m == "call":
        kill |= VOLATILE
    kill.discard(RSP)
    new_ib = len(ops) == 2 and m == "lea" and ops[0].type == X.X86_OP_REG and ops[1].type == X.X86_OP_MEM and \
        ops[1].mem.base == X.X86_REG_RIP and i.address + i.size + ops[1].mem.disp == BASE
    new_stack = len(ops) == 2 and ops[0].type == X.X86_OP_REG and parent(ops[0].reg) != RSP and (
        (m == "mov" and ops[1].type == X.X86_OP_REG and ops[1].reg in stack and ops[0].size == 8) or
        (m == "lea" and ops[1].type == X.X86_OP_MEM and ops[1].mem.base in stack and not ops[1].mem.index
         and ops[0].size == 8))
    stack, ib = set(stack) - kill, set(ib) - kill
    if new_ib:
        ib.add(parent(ops[0].reg))
    if new_stack:
        stack.add(parent(ops[0].reg))
    return frozenset(stack), frozenset(ib)


def fragments(fn):
    if fn in SYNTH:
        return SYNTH[fn]
    rva = fn - BASE
    if rva not in ROOT:
        raise CheckError("no .pdata root for %08X" % fn)
    return sorted((BASE + b, BASE + e) for b, e, u in ROOT[rva])


SYNTH = {}              # synthetic control bodies: entry -> fragments


def thunk_name(t):
    """import:Name when t is an import or a jmp [IAT] thunk."""
    if t in IAT:
        return "import:" + IAT[t]
    if TLO <= t < THI:
        ins = next(md.disasm(rd(t, 16), t), None)
        if ins and ins.mnemonic == "jmp" and ins.operands and ins.operands[0].type == X.X86_OP_MEM \
                and ins.operands[0].mem.base == X.X86_REG_RIP:
            slot = ins.address + ins.size + ins.operands[0].mem.disp
            if slot in IAT:
                return "import:" + IAT[slot]
    return "%08X" % t


def decode(a):
    i = next(md.disasm(rd(a, 16), a), None)
    if i is None:
        raise CheckError("undecodable byte at %08X" % a)
    return i


JCC = {"ja", "jae", "jb", "jbe", "je", "jne", "jg", "jge", "jl", "jle", "jo", "jno", "jp", "jnp", "js", "jns", "jrcxz",
       "jecxz", "loop", "loope", "loopne"}
TERMINAL = {"ret", "retf", "int3", "ud2", "hlt", "iretq", "iretd"}


def _writes(i, reg):
    return parent(reg) in written_regs(i)


def resolve_table(lin, k):
    """lin = instructions in address order, lin[k] = 'jmp R'. Returns (arms, data ranges, description) or None."""
    jr = lin[k].operands[0].reg

    def prev_writer(reg, before, limit=12):
        for j in range(before - 1, max(-1, before - 1 - limit), -1):
            if _writes(lin[j], reg):
                return j
        return None

    j_add = prev_writer(jr, k)
    if j_add is None:
        return None
    a = lin[j_add]
    if a.mnemonic != "add" or a.operands[0].type != X.X86_OP_REG or a.operands[1].type != X.X86_OP_REG:
        return None
    ibr = a.operands[1].reg

    def is_ib(reg, before):
        j = prev_writer(reg, before, before)     # the nearest earlier writer in address order, however far back
        if j is None:
            return False
        x = lin[j]
        return x.mnemonic == "lea" and x.operands[1].type == X.X86_OP_MEM and x.operands[1].mem.base == X.X86_REG_RIP \
            and x.address + x.size + x.operands[1].mem.disp == BASE

    if not is_ib(ibr, j_add):
        return None
    j_ld = prev_writer(jr, j_add)
    if j_ld is None:
        return None
    ld = lin[j_ld]
    if ld.mnemonic != "mov" or ld.operands[1].type != X.X86_OP_MEM or ld.operands[1].size != 4:
        return None
    mm = ld.operands[1].mem
    if mm.scale != 4 or not mm.index or not is_ib(mm.base, j_ld):
        return None
    tbl, idx = BASE + mm.disp, mm.index
    two = None
    j_ix = prev_writer(idx, j_ld)
    bound_reg, bound_before = idx, j_ld
    if j_ix is not None:
        x = lin[j_ix]
        if x.mnemonic == "movzx" and x.operands[1].type == X.X86_OP_MEM and x.operands[1].size == 1:
            m2 = x.operands[1].mem
            if m2.scale != 1 or not m2.index or not (m2.base != 0 and is_ib(m2.base, j_ix)):
                return None
            two = BASE + m2.disp
            bound_reg, bound_before = m2.index, j_ix
    # the bound: the nearest cmp on the index (or the register it was copied from) followed by ja/jae/jbe/jb
    regs = {parent(bound_reg)}
    count = None
    for j in range(bound_before - 1, max(-1, bound_before - 14), -1):
        x = lin[j]
        if x.mnemonic in ("mov", "movsxd", "movzx") and x.operands[0].type == X.X86_OP_REG and \
                parent(x.operands[0].reg) in regs and x.operands[1].type == X.X86_OP_REG:
            regs.add(parent(x.operands[1].reg))
            continue
        if x.mnemonic == "cmp" and x.operands[0].type == X.X86_OP_REG and parent(x.operands[0].reg) in regs \
                and x.operands[1].type == X.X86_OP_IMM and j + 1 < len(lin):
            nxt = lin[j + 1].mnemonic
            imm = x.operands[1].imm & 0xFFFFFFFF
            if nxt in ("ja", "jbe"):
                count = imm + 1
            elif nxt in ("jae", "jb"):
                count = imm
            break
    if not count or count > 4096:
        return None
    data = []
    if two is not None:
        idxs = list(rd(two, count))
        data.append((two, two + count))
        n = max(idxs) + 1
    else:
        n = count
    data.append((tbl, tbl + 4 * n))
    arms = [BASE + struct.unpack("<I", rd(tbl + 4 * e, 4))[0] for e in range(n)]
    desc = "table %08X x%d%s at jmp %08X" % (tbl, n, (" via byte table %08X x%d" % (two, count)) if two else "",
                                             lin[k].address)
    return arms, data, desc


TABLES = []             # (desc) of the last derive()
SITES = {}              # token -> (VA, mnemonic) of the lowest-address instruction that produced it (for anchors)


def build(fn):
    """Recursive descent over the extent. Returns (insn by address, successor lists, tables, calls-with-no-state)."""
    frags = fragments(fn)
    inside = lambda a: any(lo <= a < hi for lo, hi in frags)
    insn, succ, owner = {}, {}, {}
    tables, data = [], []
    work = [fn]
    pending_jmps = []
    while work or pending_jmps:
        while work:
            a = work.pop()
            if a in insn:
                continue
            if not inside(a):
                raise CheckError("control reaches %08X outside the extent" % a)
            if a in owner:
                raise CheckError("jump into the middle of the instruction at %08X (%08X)" % (owner[a], a))
            if any(lo <= a < hi for lo, hi in data):
                raise CheckError("control reaches table data at %08X" % a)
            i = decode(a)
            for b in range(a, a + i.size):
                if b in owner or b in insn:
                    raise CheckError("instruction at %08X overlaps %08X" % (a, owner.get(b, b)))
                if any(lo <= b < hi for lo, hi in data):      # v3 (N3): every byte, not only the start
                    raise CheckError("instruction at %08X runs into table data at %08X" % (a, b))
                owner[b] = a
            insn[a] = i
            m, ops, nxt = i.mnemonic, i.operands, a + i.size
            s = []
            if m in TERMINAL:
                pass
            elif m == "jmp":
                if ops[0].type == X.X86_OP_IMM:
                    if inside(ops[0].imm):
                        s.append(ops[0].imm)
                elif ops[0].type == X.X86_OP_REG:
                    pending_jmps.append(a)
            elif m in JCC:
                if inside(ops[0].imm):
                    s.append(ops[0].imm)
                if inside(nxt):
                    s.append(nxt)
                else:
                    raise CheckError("conditional branch at %08X falls off the extent" % a)
            elif m == "call":
                if inside(nxt):
                    s.append(nxt)
            else:
                if not inside(nxt):
                    raise CheckError("%08X %s falls off the extent" % (a, m))
                s.append(nxt)
            succ[a] = s
            work.extend(s)
        # resolve register jmps once the straight-line code before them is decoded
        while pending_jmps:
            a = pending_jmps.pop()
            lin = sorted(insn.values(), key=lambda x: x.address)
            k = next(n for n, x in enumerate(lin) if x.address == a)
            r = resolve_table(lin, k)
            if r is None:
                continue
            arms, dr, desc = r
            data.extend(dr)
            tables.append((a, arms, desc))
            for lo, hi in dr:
                for b in range(lo, hi):
                    if b in owner:
                        raise CheckError("table %08X..%08X overlaps code at %08X" % (lo, hi, owner[b]))
            succ[a] = [t for t in arms if inside(t)]
            work.extend(succ[a])
    # tiling: code + tables + padding must cover every fragment
    for lo, hi in frags:
        a = lo
        while a < hi:
            if a in owner:
                a = owner[a] + insn[owner[a]].size
                continue
            t = next(((dlo, dhi) for dlo, dhi in data if dlo <= a < dhi), None)
            if t:
                a = t[1]
                continue
            i = decode(a)
            if i.mnemonic not in ("nop", "int3") and not (i.mnemonic == "xchg" and i.op_str == "ax, ax"):
                raise CheckError("unread in-extent bytes at %08X (%s %s)" % (a, i.mnemonic, i.op_str))
            a += i.size
    return insn, succ, tables, frags


def derive(fn):
    insn, succ, tables, frags = build(fn)
    inside = lambda a: any(lo <= a < hi for lo, hi in frags)
    TABLES[:] = [d for _, _, d in tables]
    tab = {a: arms for a, arms, _ in tables}
    # MUST dataflow: IN[a] = intersection over predecessors; None = not yet reached (top)
    IN = {fn: (frozenset([RSP]), frozenset())}
    work = [fn]
    while work:
        a = work.pop()
        st = transfer(insn[a], *IN[a])
        for s in succ[a]:
            old = IN.get(s)
            new = st if old is None else (old[0] & st[0], old[1] & st[1])
            if new != old:
                IN[s] = new
                work.append(s)
    calls, stores = {}, {}
    for a in sorted(insn):
        if a not in IN:
            raise CheckError("decoded but unreached %08X" % a)
        i, (stack, ib) = insn[a], IN[a]
        m, ops = i.mnemonic, i.operands
        toks = []
        if m == "call":
            op = ops[0]
            if op.type == X.X86_OP_IMM:
                toks.append(thunk_name(op.imm))
            elif op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
                slot = i.address + i.size + op.mem.disp
                toks.append("import:" + IAT[slot] if slot in IAT else "ptr:%08X" % slot)
            elif op.type == X.X86_OP_MEM:
                toks.append(render(i, op, ib))
            else:
                toks.append(regname(op.reg))
        elif m == "jmp":
            op = ops[0]
            if op.type == X.X86_OP_IMM:
                if not inside(op.imm):
                    toks.append("tail:" + thunk_name(op.imm))
            elif op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
                slot = i.address + i.size + op.mem.disp
                toks.append("tail:" + ("import:" + IAT[slot] if slot in IAT else "ptr:%08X" % slot))
            elif a in tab:
                toks += ["tail:" + thunk_name(t) for t in tab[a] if not inside(t)]
            else:
                toks.append("ijmp:" + (render(i, op, ib) if op.type == X.X86_OP_MEM else regname(op.reg)))
        elif m in JCC:
            if not inside(ops[0].imm):
                toks.append("jcc:" + thunk_name(ops[0].imm))
        for t in toks:
            calls.setdefault(t, (a, m))
        if m == "call" or m == "jmp" or m in JCC:
            continue
        for t in insn_stores(i, stack, ib):
            stores.setdefault(t, (a, m))
    SITES.clear()
    SITES.update(calls)
    SITES.update(stores)
    return sorted(calls), sorted(stores)


def derive_sites(fn):
    c, s = derive(fn)
    return c, s, dict(SITES)


# ---- run compression (exact as a set: a run token expands to every element)
RUN = re.compile(r"^([bwdqxyt])\[([^\]]*?)(0x[0-9A-F]+|[0-9A-F]{8})\.\.(0x[0-9A-F]+|[0-9A-F]{8})/(\d+)\]$")


def split_tok(s):
    """('d', 'rax+', 0x10, '0x%X') for d[rax+0x10]; ('d', '', 0x02064C80, '%08X') for d[02064C80]; else None."""
    m = re.match(r"^([bwdqxyt])\[([0-9A-F]{8})\]$", s)
    if m:
        return m.group(1), "", int(m.group(2), 16), "%08X"
    m = re.match(r"^([bwdqxyt])\[([a-z0-9]+\+)0x([0-9A-F]+)\]$", s)
    if m:
        return m.group(1), m.group(2), int(m.group(3), 16), "0x%X"
    return None


def compress(stores):
    groups, rest = {}, []
    for s in stores:
        k = split_tok(s)
        if k:
            groups.setdefault((k[0], k[1], k[3]), []).append(k[2])
        else:
            rest.append(s)
    out = list(rest)
    singles = {}
    for (w, pre, f), vals in groups.items():
        vals = sorted(set(vals))
        i = 0
        while i < len(vals):
            j = i + 1
            if j < len(vals):
                step = vals[j] - vals[i]
                while j + 1 < len(vals) and vals[j + 1] - vals[j] == step:
                    j += 1
                if j - i + 1 >= 3:
                    out.append("%s[%s%s..%s/%d]" % (w, pre, f % vals[i], f % vals[j], step))
                    i = j + 1
                    continue
            singles.setdefault((w, pre, f), []).append(vals[i])
            i += 1
    for (w, pre, f), vals in singles.items():
        out.append("%s[%s%s]" % (w, pre, ",".join(f % v for v in vals)))
    return sorted(out)


LIST = re.compile(r"^([bwdqxyt])\[([a-z0-9]+\+)?((?:0x[0-9A-F]+|[0-9A-F]{8})(?:,(?:0x[0-9A-F]+|[0-9A-F]{8}))+)\]$")


def expand(tok):
    ml = LIST.match(tok)
    if ml:
        w, pre, vals = ml.group(1), ml.group(2) or "", ml.group(3).split(",")
        return ["%s[%s%s]" % (w, pre, v) for v in vals]
    m = RUN.match(tok)
    if not m:
        return [tok]
    w, pre, a, b, step = m.groups()
    f = "0x%X" if a.startswith("0x") else "%08X"
    lo, hi, st = int(a, 16), int(b, 16), int(step)
    if st <= 0 or (hi - lo) % st:
        return ["BADRUN:" + tok]
    return ["%s[%s%s]" % (w, pre, f % v) for v in range(lo, hi + 1, st)]


# ---- row parsing: 'Calls: a, b, c' and 'Stores: x, y' (tokens separated by ', ', each list ends at ';' or '.' + space or end)
TOK = re.compile(r"`([^`]+)`")


def stated(text):
    def grab(label):
        m = re.search(label + r":\s*(.*?)(?:;\s+[A-Z][a-z]+:|\Z)", text, re.S)
        if not m:
            return None
        return sorted(set(x for tok in TOK.findall(m.group(1)) for x in expand(tok)))
    return grab("Calls"), grab("Stores")


def check_row(fn, text):
    if not text.startswith("Scope:") or "scoped row: set-exact" not in text:
        return ["no Scope:/marker"]
    try:
        c, s = derive(fn)
    except CheckError as e:
        return ["checker refuses the body: %s" % e]
    sc, ss = stated(text)
    errs = []
    if sc is None or ss is None:
        return ["missing Calls:/Stores: list"]
    if sc != c:
        errs.append("calls: missing %s extra %s" % (sorted(set(c) - set(sc)), sorted(set(sc) - set(c))))
    if ss != s:
        errs.append("stores: missing %s extra %s" % (sorted(set(s) - set(ss)), sorted(set(ss) - set(s))))
    return errs


SCOPE = ("Scope: all calls (direct, tail, exit jcc, indirect by operand, imports by name) and all non-stack stores with "
         "widths; branch conditions, arithmetic and order not stated; scoped row: set-exact.")


def fmt_row(fn, scope_head=SCOPE):
    c, s = derive(fn)
    return "%s Calls: %s; Stores: %s" % (scope_head, ", ".join("`%s`" % x for x in c) or "none",
                                         ", ".join("`%s`" % x for x in compress(s)) or "none")


# ---- controls (D8): every control runs through insn_stores / derive, the code the rows are checked with
CONTROLS = {  # one instruction each, stack {rsp}, image base {}: (hex, expected store token)
    "FF4008": "d[rax+0x8]", "830B01": "d[rbx]", "0FAB01": "d[rcx]", "0FBA2905": "d[rcx]", "F30F114204": "d[rdx+0x4]",
    "0F290A": "x[rdx]", "0F110A": "x[rdx]", "F30F7F0A": "x[rdx]", "660F7E00": "d[rax]", "660FD600": "q[rax]",
    "0FC308": "d[rax]", "660F3A160001": "d[rax]", "AA": "b[rdi]", "A4": "b[rdi]", "0F9400": "b[rax]", "8701": "d[rcx]",
    "0FB111": "d[rcx]", "F00FC101": "d[rcx]", "D918": "d[rax]", "DB18": "d[rax]", "F618": "b[rax]", "D120": "d[rax]",
    "0108": "d[rax]", "C5F81100": "x[rax]", "0F1700": "q[rax]", "0F1300": "q[rax]",
    "8F00": "q[rax]",                 # pop qword [rax] (D7)
    "F3AA": "rep:rep_stosb", "F3A4": "rep:rep_movsb", "F348AB": "rep:rep_stosq"}
NOT_STORES = {  # read-only memory destinations (D6) and stack stores
    "3908": "cmp [rax],ecx", "8500": "test [rax],eax", "0FA301": "bt [rcx],eax", "0F4500": "cmovne eax,[rax]",
    "0F2E00": "ucomiss xmm0,[rax]", "0F1808": "prefetcht0 [rax]", "D900": "fld dword [rax]",
    "F720": "mul dword [rax]", "F728": "imul dword [rax]", "F730": "div dword [rax]", "F738": "idiv dword [rax]",
    "A6": "cmpsb", "F3A6": "repe cmpsb", "DE38": "fidivr word [rax]", "DE28": "fisubr word [rax]", "DF20": "fbld [rax]",
    "D920": "fldenv [rax]", "DD20": "frstor [rax]", "0FAE08": "fxrstor [rax]", "0FAE28": "xrstor [rax]",
    "660FAE30": "clwb [rax]", "0F0138": "invlpg [rax]", "FF30": "push qword [rax]", "48890424": "mov [rsp],rax"}
MUST_FAIL = {"660FF7C1": "maskmovdqu xmm0,xmm1 (implicit [rdi] store)", "62F17E487F00": "vmovdqu32 [rax], zmm0 (unlisted)"}

SYN_BASE = 0x10000000


def _table_body(va, straddle=False):
    """cmp ecx,2; ja DEF; lea r10,[rip->image base]; mov eax,[r10+rcx*4+T]; add rax,r10; jmp rax; DEF: ret; int3 pad;
    T (+0x20): three dword arms; +0x2C: mov [rbx+8],eax; ret; +0x30: mov [rbx+0xC],eax; ret.
    Plain: arms +0x2C, +0x30 and 00300000 (outside the extent -> tail:00300000). straddle: arm 0 -> +0x1E, where a
    3-byte 'ret imm16' takes its last byte from the table (must be refused, v3 N3)."""
    b = bytearray()
    b += bytes.fromhex("83F902" "7714")
    b += bytes.fromhex("4C8D15") + struct.pack("<i", BASE - (va + 12))
    b += bytes.fromhex("418B848A") + struct.pack("<I", va + 0x20 - BASE)
    b += bytes.fromhex("4C01D0" "FFE0" "C3" "CCCCCCCCCCCC")
    arms = [va + 0x2C, va + 0x30, 0x00300000] if not straddle else [va + 0x1E, va + 0x30, va + 0x2C]
    b += b"".join(struct.pack("<I", x - BASE) for x in arms)
    b += bytes.fromhex("894308C3" "89430CC3")
    if straddle:
        b[0x1E:0x20] = bytes.fromhex("C200")
    assert len(b) == 0x34
    return bytes(b)


SYN = {  # synthetic bodies: name -> (hex code or builder(va), stores that must appear, stores that must not,
         #                            refusal text that must appear (None: must derive), calls that must appear)
    # D2: a call clobbers rax; mov rax, rsp; call; mov rdi, rax; mov [rdi+8], rbx; ret
    "call-clobber": ("4889E0" "E8" "00000000" "4889C7" "48895F08" "C3", ["q[rdi+0x8]"], [], None, []),
    # D1: test ecx,ecx; je B; lea rdx,[rsp+0x10]; jmp E; B: mov byte [rdx+0xa],1; E: ret
    "cfg-merge": ("85C9" "7407" "488D542410" "EB04" "C6420A01" "C3", ["b[rdx+0xA]"], [], None, []),
    # the same with the store on the stack path: lea rdx,[rsp+0x10]; mov byte [rdx+0xa],1; ret -> no store
    "cfg-stack": ("488D542410" "C6420A01" "C3", [], ["b[rdx+0xA]"], None, []),
    # join of a stack and a non-stack path: test; je J; lea rdx,[rsp+8]; J: mov [rdx],eax; ret -> reported (MUST)
    "cfg-join": ("85C9" "7405" "488D542408" "8902" "C3", ["d[rdx]"], [], None, []),
    # D3: lea rbx,[rsp+8]; mov ebx,ecx; mov [rbx],eax; ret -> reported
    "subreg-kill": ("488D5C2408" "89CB" "8903" "C3", ["d[rbx]"], [], None, []),
    # v3 N1: lea rax,[rsp+8]; lock cmpxchg [rbx],rcx (loads rax on failure); mov [rax],edx; ret -> d[rax] reported
    "cmpxchg-implicit-rax": ("488D442408" "F0480FB10B" "8910" "C3", ["d[rax]", "q[rbx]"], [], None, []),
    # v3 N1: lea rdx,[rsp+8]; cqo (writes rdx); mov [rdx],eax; ret -> reported
    "cqo-implicit-rdx": ("488D542408" "4899" "8902" "C3", ["d[rdx]"], [], None, []),
    # D4/D5: a resolved table with one arm outside the extent and code after the table
    "table-arm-outside": (_table_body, ["d[rbx+0x8]", "d[rbx+0xC]"], [], None, ["tail:00300000"]),
    # v3 N3: an instruction whose last byte is table data
    "table-straddle": (lambda va: _table_body(va, True), [], [], "runs into table data", []),
}


def synth(name):
    va = SYN_BASE + 0x1000 * (1 + sorted(SYN).index(name))
    src = SYN[name][0]
    code = src(va) if callable(src) else bytes.fromhex(src)
    OVERLAY.clear()
    OVERLAY[va] = code + bytes([0xCC]) * 16
    SYNTH[va] = [(va, va + len(code))]
    return va


class _NoRegs:
    """An instruction whose register query fails (v3 N2 control)."""
    address, mnemonic, op_str, operands = 0x1000, "nop", "", []

    def regs_access(self):
        raise capstone.CsError(capstone.CS_ERR_DETAIL)


def controls():
    bad = 0
    for h, want in list(CONTROLS.items()) + [(h, None) for h in NOT_STORES]:
        i = next(md.disasm(bytes.fromhex(h), 0x1000))
        try:
            got = insn_stores(i, frozenset([RSP]), frozenset())
        except CheckError as e:
            got = ["ERROR " + str(e)]
        ok = (want in got) if want else not got
        bad += not ok
        print("%-4s %-36s want %-14s got %s" % ("ok" if ok else "FAIL", i.mnemonic + " " + i.op_str, want, got))
    for h, why in MUST_FAIL.items():
        i = next(md.disasm(bytes.fromhex(h), 0x1000), None)
        try:
            got = insn_stores(i, frozenset([RSP]), frozenset()) if i else "undecodable"
            ok = False
        except CheckError as e:
            got, ok = "refused: %s" % e, True
        bad += not ok
        print("%-4s %-36s must fail      got %s" % ("ok" if ok else "FAIL", why, got))
    for name in sorted(SYN):
        va = synth(name)
        _, must, mustnot, refuse, callsmust = SYN[name]
        try:
            c, st = derive(va)
            got = "calls %s stores %s" % (c, st)
            ok = refuse is None and all(t in st for t in must) and not any(t in st for t in mustnot) and                 all(t in c for t in callsmust)
        except CheckError as e:
            got = "refused: %s" % e
            ok = refuse is not None and refuse in str(e)
        bad += not ok
        print("%-4s synthetic %-26s %s" % ("ok" if ok else "FAIL", name, got))
    try:
        transfer(_NoRegs(), frozenset([RSP]), frozenset())
        ok, got = False, "accepted"
    except CheckError as e:
        ok, got = True, "refused: %s" % e
    bad += not ok
    print("%-4s register query error fails closed (N2): %s" % ("ok" if ok else "FAIL", got))
    OVERLAY.clear()
    # real bodies: the two review sites must yield their stores; the in-extent tables must resolve with no ijmp
    real = [(0x0064A500, "q[rdi+0x8]", 0x0064A5B8), (0x002986E0, "b[rdx+0xA]", 0x00298EA2),
            (0x002986E0, "w[rdx+0x16]", 0x00298EE8)]
    for fn, tok, site in real:
        c, s, sites = derive_sites(fn)
        ok = tok in s and sites.get(tok, (None,))[0] == site
        bad += not ok
        print("%-4s body %08X %-14s at %08X: got %s" % ("ok" if ok else "FAIL", fn, tok, site, sites.get(tok)))
    # the ijmp left after the tables resolve is the epilogue's computed tail call (mov rsp, r11; pops; jmp rax)
    for fn, ij in ((0x0055FB20, []), (0x004A4410, ["ijmp:rax"]), (0x0083B780, []), (0x002001F0, [])):
        c, s = derive(fn)
        ok = bool(TABLES) and [x for x in c if x.startswith("ijmp:")] == ij
        bad += not ok
        print("%-4s tables %08X: %s; ijmp %s" % ("ok" if ok else "FAIL", fn, "; ".join(TABLES),
                                                 [x for x in c if x.startswith("ijmp:")]))
    print("CONTROL FAILS %d" % bad)
    return bad


def main():
    a = sys.argv[1:]
    if a and a[0] == "--controls":
        return 1 if controls() else 0
    if a and a[0] in ("--dump", "--tables"):
        for f in a[1:]:
            c, s = derive(int(f, 16))
            if a[0] == "--tables":
                print(f, "; ".join(TABLES) or "no table")
                continue
            print("%s calls %d stores %d" % (f, len(c), len(s)))
            print("  CALLS ", " ".join(c))
            print("  STORES", " ".join(s))
        return 0
    if a and a[0] == "--self-test":
        fn = int(a[1], 16)
        row = fmt_row(fn)
        ok = check_row(fn, row) == []
        c, s = derive(fn)
        bad1 = row.replace("`%s`, " % c[0], "", 1) if len(c) > 1 else row.replace("`%s`" % c[0], "", 1)
        st = TOK.findall(row.split("Stores:", 1)[1])
        if not st:
            r1 = check_row(fn, bad1)
            print("positive row passes:", ok)
            print("one call removed fails:", bool(r1), r1[:1])
            print("one store width changed fails: n/a (no non-stack store)")
            return 0 if ok and r1 else 1
        w = st[0]
        alt = ("d" if w[0] != "d" else "q") + w[1:]
        bad2 = row.split("Stores:", 1)[0] + "Stores:" + row.split("Stores:", 1)[1].replace("`%s`" % w, "`%s`" % alt, 1)
        r1, r2 = check_row(fn, bad1), check_row(fn, bad2)
        print("positive row passes:", ok)
        print("one call removed fails:", bool(r1), r1[:1])
        print("one store width changed fails:", bool(r2), r2[:1])
        return 0 if ok and r1 and r2 else 1
    rep = json.load(open(a[0], encoding="utf-8"))
    fails = 0
    for r in rep["rows"]:
        if "scoped row: set-exact" not in r["text"]:
            continue
        e = check_row(int(r["fn"], 16), r["text"])
        if e:
            fails += 1
            print("FAIL", r["fn"], e)
        else:
            print("ok  ", r["fn"])
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
