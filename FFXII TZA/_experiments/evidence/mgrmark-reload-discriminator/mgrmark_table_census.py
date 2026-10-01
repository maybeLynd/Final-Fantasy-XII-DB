"""Every access to the manager-mark table 022C6D20, found WITHOUT assuming an addressing form.

WHY THIS INSTRUMENT AND NOT A GREP. The claim this replaces - "022C6D20[m] has no clear
anywhere in the image" - was false, and it was false for a specific reason ASTRA named: the
queries behind it looked for RIP-relative operands, relocations and bulk fills, and the actual
clear is none of those. It is `mov byte [rdi + r14 + 0x21a6d20], bpl`, where r14 is the image
base materialised by `lea r14,[rip-0x20edc2]` and the displacement is therefore an IMAGE
OFFSET, not an address. A census that searched for the address could never have found it.

Re-stating the claim from another narrow query would repeat the mistake, so this resolves the
effective address the way the code does, with the register tracker repaired under
ASTRA-CONTRA-OPUS-AQ18-SCANNER-PARTIAL-ALIASES: default-kill through a full-width alias map,
then model only sound transfers, so a `lea` of the image base into any register is followed
wherever it goes and a partial write can only destroy a tracked value. Both addressing forms
fall out of the same pass, along with any third form nobody has thought of.

REPORTED SEPARATELY, because they answer different questions:
  EXACT   - the whole address is fixed. A clear or a set of one known entry.
  INDEXED - the base is known and lands in the window but the index is not. This is the
            normal shape for a per-entry mark and is where the real accesses live.
"""
import csv, io, os, sys

KIT = r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts"
sys.path.insert(0, KIT)
import kit_paths as KP, disasm_fn as DF
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import capstone.x86 as X

img = DF.Image(KP.EXE)
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

TABLE = 0x022C6D20
WIN = 0x400                       # extent unknown; a window, reported by offset
PTRTAB = 0x022C6C00               # the 8-byte sibling the disposal path nulls alongside

GPR = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "r8", "r9",
       "r10", "r11", "r12", "r13", "r14", "r15"]
C = {}
for g in GPR:
    C[g] = g
    if g[1].isdigit(): C[g + "d"] = g
    else: C["e" + g[1:]] = g
KILL = dict(C)
_LOW = {"rax": "a", "rbx": "b", "rcx": "c", "rdx": "d"}
for g in GPR:
    if g[1].isdigit():
        KILL[g + "w"] = g; KILL[g + "b"] = g
    elif g in _LOW:
        s = _LOW[g]
        for n in (s + "x", s + "l", s + "h"): KILL[n] = g
    else:
        KILL[g[1:]] = g; KILL[g[1:] + "l"] = g
VOL = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
NOVAL = object()

fns = []
for r in csv.DictReader(io.open(os.path.join(KP.WORK, "graph", "functions.tsv"),
                                encoding="utf-8", newline=""), delimiter="\t"):
    fns.append((int(r["entry"], 16), int(r["body_bytes"])))

exact, indexed, ptr_sites = [], [], []
for fn, n in fns:
    if n <= 0 or n > 1 << 18:
        continue
    reg, a, end = {}, fn, fn + n
    body = img.read(fn, n)
    if not body:
        continue
    for ins in md.disasm(body, fn):
        m, ops = ins.mnemonic, ins.operands
        for op in ops:
            if op.type != X.X86_OP_MEM or m == "lea":
                continue
            mm = op.mem
            base = None
            if mm.base == X.X86_REG_RIP:
                base = ins.address + ins.size
            elif mm.base:
                cb = C.get(ins.reg_name(mm.base))
                base = reg.get(cb) if cb else None
            elif not mm.index:
                base = 0
            if not isinstance(base, int):
                continue
            # an index register that itself holds a tracked value adds into the address
            extra = 0
            if mm.index:
                ci = C.get(ins.reg_name(mm.index))
                v = reg.get(ci) if ci else None
                if isinstance(v, int):
                    extra = v * (mm.scale or 1)
            addr = base + mm.disp + extra
            acc = getattr(op, "access", 0)
            kind = ("w" if acc & 2 else "") + ("r" if acc & 1 else "") or "r"
            fixed = not mm.index or extra
            for tgt, lst in ((TABLE, exact if fixed else indexed),
                             (PTRTAB, ptr_sites)):
                if tgt <= addr < tgt + WIN:
                    lst.append((ins.address, fn, addr - tgt, kind, m, ins.op_str))
                    break

        dst, val = None, NOVAL
        if m == "lea" and ops[0].type == X.X86_OP_REG:
            dst = C.get(ins.reg_name(ops[0].reg)); s = ops[1].mem
            if s.base == X.X86_REG_RIP and not s.index:
                val = ins.address + ins.size + s.disp
            elif s.base and not s.index:
                cb = C.get(ins.reg_name(s.base)); v = reg.get(cb) if cb else None
                val = v + s.disp if isinstance(v, int) else None
            elif not s.base and not s.index:
                val = s.disp
            else:
                val = None
        elif m in ("add", "sub", "xor", "mov") and ops and ops[0].type == X.X86_OP_REG:
            dst = C.get(ins.reg_name(ops[0].reg))
            o1 = ops[1] if len(ops) > 1 else None
            if o1 is None or dst is None:
                dst = None
            elif m == "xor" and o1.type == X.X86_OP_REG:
                if C.get(ins.reg_name(o1.reg)) == dst: val = 0
            elif m == "mov" and o1.type == X.X86_OP_REG:
                cs_ = C.get(ins.reg_name(o1.reg)); val = reg.get(cs_) if cs_ else None
            elif m == "mov" and o1.type == X.X86_OP_IMM:
                val = o1.imm
            elif o1.type == X.X86_OP_IMM and m in ("add", "sub"):
                v = reg.get(dst)
                val = (v + o1.imm * (1 if m == "add" else -1)) if isinstance(v, int) else None
            elif o1.type == X.X86_OP_REG and m in ("add", "sub"):
                cs_ = C.get(ins.reg_name(o1.reg))
                v, w = reg.get(dst), (reg.get(cs_) if cs_ else None)
                val = (v + w * (1 if m == "add" else -1)) if isinstance(v, int) and isinstance(w, int) else None

        for rg in ins.regs_access()[1]:
            c = KILL.get(ins.reg_name(rg))
            if c: reg[c] = None
        if m == "call":
            for v in VOL: reg[v] = None
        if dst and val is not NOVAL:
            reg[dst] = val

print("manager-mark table %08X, window %d bytes; sibling pointer table %08X" % (TABLE, WIN, PTRTAB))
for lbl, lst in (("EXACT (whole address fixed)", exact),
                 ("INDEXED (base known, index not) - the per-entry accesses", indexed)):
    print("\n%s: %d" % (lbl, len(lst)))
    for site, fn, off, kind, m, ops_ in sorted(lst):
        print("  %08X in %08X  ->  table+0x%03X  [%s]  %s %s" % (site, fn, off, kind, m, ops_))
print("\nSIBLING pointer table %08X: %d" % (PTRTAB, len(ptr_sites)))
for site, fn, off, kind, m, ops_ in sorted(ptr_sites):
    print("  %08X in %08X  ->  ptrtab+0x%03X  [%s]  %s %s" % (site, fn, off, kind, m, ops_))
