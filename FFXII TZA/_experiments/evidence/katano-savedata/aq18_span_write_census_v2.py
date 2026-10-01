#!/usr/bin/env python3
"""AQ-18 rerun on a REPAIRED tracker. ASTRA falsified v1's instrument; this is the fix.

ASTRA-CONTRA-OPUS-AQ18-SCANNER-PARTIAL-ALIASES executed v1 unchanged against ten
synthetic fixtures with Unicorn recording the truth, and v1 failed five of them.
Its package is ../astra-census-impact/ and it holds v1's bytes, so v1's identity and
its historical output stay reproducible. v1 is kept beside this file, unrepaired.

THE TWO DEFECTS, both confirmed at the instruction level before this was written.

(1) UNSOUND - v1 INVENTED EXACT ADDRESSES. Its register map held 64- and 32-bit names
    only, and its kill path was `c = C.get(name); if c: reg[c] = None`. For `xor al,al`
    capstone reports the written register as `al`, `C.get("al")` is None, the guard is
    false, AND NOTHING IS KILLED - so rax kept a stale `lea` value that the instruction
    had just partly overwritten. v1 then reported the stale address as an exact target.
    Measured: `xor al,al` -> written ['rflags','al'] -> C.get -> [None,None].
    Truth for ASTRA's fixture: `lea rax,[02165176]` then `xor al,al` leaves 02165100,
    which is OUTSIDE the span; v1 reported 02165176, INSIDE it. Same for `xor ax,ax`
    (02160000) and `mov al,90h` (02165190). This is the third direction the absence
    gate calls blind spot 10 - not hiding an access and not inventing one from nothing,
    but MISPLACING a real access onto an address it never touched.

(2) LOSSY - v1 dropped register-register ADD. `add rax,rcx` matched no transfer rule
    and fell to the kill, so a base composed from two registers went unknown even when
    both halves were known. Safe, but it shrinks what the absence covers.

THE REPAIR.
  * DEFAULT-KILL, THEN MODEL. Every register an instruction writes is killed first,
    through an alias map covering all four widths and the legacy high bytes, so a
    partial write can only ever DESTROY a tracked address. A value is re-established
    only where a rule is sound. Defect 1 cannot recur by construction: modelling is
    opt-in, and an 8/16-bit destination is not in the value map, so it never opts in.
  * SOUND CONSTANTS. `xor r,r` -> 0, `mov r,imm` -> imm, and `add`/`sub` of two known
    registers now compose. That recovers both ADD fixtures honestly rather than by
    keeping an unknown base and calling it exact, which ASTRA correctly named unsound.

WHAT IS STILL NOT CLOSED, and v1 had all three too.
  * LINEAR DECODE. Bodies are read first byte to last with branches ignored, so a value
    established on one path is used at a join it may not reach. Constant tracking widens
    the exposure, so every hit is TAGGED with its provenance and the two classes are
    reported apart: `lea` is an address the code itself formed, a constant is one this
    tracker composed. None of ASTRA's ten fixtures test this - all are straight-line.
  * A HIT IS NO LONGER DECISIVE BY ITSELF. v1 said it was. That sentence is withdrawn:
    a hit is a candidate site whose instruction and path must be read.
  * AN ABSENCE STILL HAS A BOUND. A base arriving as an argument or loaded from memory
    is invisible. The unresolved-base count below is that denominator, measured.
"""
import collections
import csv
import io
import os
import sys

KIT = r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts"
sys.path.insert(0, KIT)
import kit_paths as KP, disasm_fn as DF
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import capstone.x86 as X

img = DF.Image(KP.EXE)
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

BUF = 0x02164280                 # 002EF640's constant
PAYLOAD = BUF + 0x200            # 0x02164480
LO, HI = PAYLOAD + 0xCF6, PAYLOAD + 0x1000
REC_LO, REC_HI = PAYLOAD, PAYLOAD + 0x1538

GPR = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "r8", "r9",
       "r10", "r11", "r12", "r13", "r14", "r15"]

# VALUE MAP - names that may CARRY a tracked value. 64- and 32-bit only: a 32-bit write
# zero-extends, and every value this tracker holds is an image address below 2^32, so a
# 32-bit destination reproduces it exactly. Narrower destinations are deliberately absent.
C = {}
for g in GPR:
    C[g] = g
    if g[1].isdigit(): C[g + "d"] = g
    else: C["e" + g[1:]] = g

# KILL MAP - every alias of every register, all four widths plus the legacy high bytes.
# This is the half v1 was missing, and it is why v1 could keep a stale address.
KILL = dict(C)
_LOW = {"rax": "a", "rbx": "b", "rcx": "c", "rdx": "d"}
for g in GPR:
    if g[1].isdigit():
        for suf in ("w", "b"): KILL[g + suf] = g
    elif g in _LOW:
        s = _LOW[g]
        for n in (s + "x", s + "l", s + "h"): KILL[n] = g
    else:                                     # rsi/rdi/rbp -> si, sil / di, dil / bp, bpl
        KILL[g[1:]] = g
        KILL[g[1:] + "l"] = g

# NARROW MAP - an 8/16-bit destination MERGES into the register instead of replacing it.
# name -> (canonical, mask, shift). Modelling the merge exactly is what turns ASTRA's three
# misplaced fixtures into three CORRECT addresses rather than merely three safe losses:
# `lea rax,[02165176]` then `mov al,90h` really does leave 02165190, and that is computable.
NARROW = {}
for g in GPR:
    if g[1].isdigit():
        NARROW[g + "b"] = (g, 0xFF, 0)
        NARROW[g + "w"] = (g, 0xFFFF, 0)
    elif g in _LOW:
        s = _LOW[g]
        NARROW[s + "l"] = (g, 0xFF, 0)
        NARROW[s + "h"] = (g, 0xFF, 8)          # the legacy high byte, bits 8..15
        NARROW[s + "x"] = (g, 0xFFFF, 0)
    else:
        NARROW[g[1:] + "l"] = (g, 0xFF, 0)
        NARROW[g[1:]] = (g, 0xFFFF, 0)


def merge(v, new, mask, shift):
    """Exact x86 semantics for a narrow write into a wider register."""
    return (v & ~(mask << shift)) | ((new & mask) << shift)


VOL = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")
ARGS = ("rcx", "rdx", "r8", "r9")
NOVAL = object()                 # "this instruction modelled no value", distinct from None

fns = []
for r in csv.DictReader(io.open(os.path.join(KP.WORK, "graph", "functions.tsv"),
                                encoding="utf-8", newline=""), delimiter="\t"):
    fns.append((int(r["entry"], 16), int(r["body_bytes"])))

span_hits, record_hits, indexed_into = [], [], []
resolved_sites = 0
unresolved_base_sites = 0        # the absence's measured denominator
arg_carriers = collections.Counter()
for fn, n in fns:
    if n <= 0 or n > 1 << 18:
        continue
    reg, prov, a, end = {}, {}, fn, fn + n
    while a < end:
        b = img.read(a, 16)
        if not b:
            break
        ins = next(md.disasm(b, a), None)
        if ins is None:
            break
        m, ops = ins.mnemonic, ins.operands

        # ---- resolve memory operands against the PRE-instruction state
        for op in ops:
            if op.type != X.X86_OP_MEM or m == "lea":
                continue
            mm = op.mem
            base, src = None, "lea"
            if mm.base == X.X86_REG_RIP:
                base = ins.address + ins.size
            elif mm.base:
                cb = C.get(ins.reg_name(mm.base))
                base = reg.get(cb) if cb else None
                src = prov.get(cb, "lea")
            elif mm.disp and not mm.index:
                base = 0                       # absolute [disp32]
            if not isinstance(base, int):
                if mm.base or mm.index:
                    unresolved_base_sites += 1
                continue
            addr = base + mm.disp
            resolved_sites += 1
            acc = getattr(op, "access", 0)
            kind = ("w" if acc & 2 else "") + ("r" if acc & 1 else "") or "r"
            if mm.index:
                if REC_LO <= addr < REC_HI or (addr <= LO and addr + 0x1538 > LO):
                    indexed_into.append((ins.address, fn, addr, kind, m, ins.op_str))
                continue
            if LO <= addr < HI:
                span_hits.append((ins.address, fn, addr, kind, m, ins.op_str, src))
            elif REC_LO <= addr < REC_HI:
                record_hits.append((ins.address, fn, addr, kind))

        if m == "call":
            for r_ in ARGS:
                v = reg.get(r_)
                if isinstance(v, int) and REC_LO <= v < REC_HI:
                    arg_carriers[(ops[0].imm if ops and ops[0].type == X.X86_OP_IMM else 0)] += 1

        # ---- decide the modelled result from the PRE-instruction state
        dst, val, src = None, NOVAL, "lea"
        if m == "lea" and ops[0].type == X.X86_OP_REG:
            dst = C.get(ins.reg_name(ops[0].reg)); s = ops[1].mem
            if s.base == X.X86_REG_RIP and not s.index:
                val = ins.address + ins.size + s.disp
            elif s.base and not s.index:
                cb = C.get(ins.reg_name(s.base)); v = reg.get(cb) if cb else None
                val = v + s.disp if isinstance(v, int) else None
                src = prov.get(cb, "lea")
            elif not s.base and not s.index:
                val = s.disp
            else:
                val = None
        elif m in ("xor", "mov") and ops and ops[0].type == X.X86_OP_REG \
                and ins.reg_name(ops[0].reg) in NARROW:
            # a NARROW destination merges into a value we already hold, and only then
            dn = ins.reg_name(ops[0].reg)
            canon, mask, shift = NARROW[dn]
            prior = reg.get(canon)
            o1 = ops[1] if len(ops) > 1 else None
            if isinstance(prior, int) and o1 is not None:
                if m == "mov" and o1.type == X.X86_OP_IMM:
                    dst, val = canon, merge(prior, o1.imm, mask, shift)
                    src = prov.get(canon, "lea")
                elif m == "xor" and o1.type == X.X86_OP_REG \
                        and ins.reg_name(o1.reg) == dn:
                    dst, val = canon, merge(prior, 0, mask, shift)
                    src = prov.get(canon, "lea")
        elif m in ("add", "sub", "xor", "mov") and ops and ops[0].type == X.X86_OP_REG:
            dst = C.get(ins.reg_name(ops[0].reg))
            o1 = ops[1] if len(ops) > 1 else None
            if o1 is None:
                dst = None
            elif m == "xor" and o1.type == X.X86_OP_REG:
                # the zero idiom only, and only when both names are the same register
                if dst and C.get(ins.reg_name(o1.reg)) == dst:
                    val, src = 0, "const"
            elif m == "mov" and o1.type == X.X86_OP_REG:
                cs_ = C.get(ins.reg_name(o1.reg))
                val = reg.get(cs_) if cs_ else None
                src = prov.get(cs_, "lea")
            elif m == "mov" and o1.type == X.X86_OP_IMM:
                val, src = o1.imm, "const"
            elif o1.type == X.X86_OP_IMM and m in ("add", "sub"):
                v = reg.get(dst) if dst else None
                src = prov.get(dst, "lea")
                val = (v + o1.imm * (1 if m == "add" else -1)) if isinstance(v, int) else None
            elif o1.type == X.X86_OP_REG and m in ("add", "sub"):
                cs_ = C.get(ins.reg_name(o1.reg))
                v, w = (reg.get(dst) if dst else None), (reg.get(cs_) if cs_ else None)
                if isinstance(v, int) and isinstance(w, int):
                    val = v + w * (1 if m == "add" else -1)
                    src = "const" if "const" in (prov.get(dst), prov.get(cs_)) else "lea"
                else:
                    val = None

        # ---- DEFAULT KILL: anything written, through ANY alias. This is defect 1's fix.
        for rg in ins.regs_access()[1]:
            c = KILL.get(ins.reg_name(rg))
            if c:
                reg[c] = None; prov.pop(c, None)
        if m == "call":
            for v in VOL:
                reg[v] = None; prov.pop(v, None)
            if ops and ops[0].type == X.X86_OP_IMM and ops[0].imm == 0x2EF640:
                reg["rax"], prov["rax"] = BUF, "lea"

        # ---- then re-establish only what a sound rule produced
        if dst and val is not NOVAL:
            reg[dst] = val
            if isinstance(val, int): prov[dst] = src
            else: prov.pop(dst, None)
        a += ins.size

lea_hits = [h for h in span_hits if h[6] == "lea"]
const_hits = [h for h in span_hits if h[6] == "const"]

print("payload base %08X   contested span %08X..%08X (%d bytes)"
      % (PAYLOAD, LO, HI, HI - LO))
print("memory operands resolved to an absolute address anywhere: %d" % resolved_sites)
print("memory operands whose base register was NOT known: %d" % unresolved_base_sites)
if resolved_sites + unresolved_base_sites:
    print("  -> this tracker resolves %.1f%% of register-based memory operands"
          % (100.0 * resolved_sites / (resolved_sites + unresolved_base_sites)))
print("\nACCESSES INSIDE THE CONTESTED SPAN: %d  (%d code-formed, %d tracker-composed)"
      % (len(span_hits), len(lea_hits), len(const_hits)))
for site, fn, addr, kind, m, ops_, src in sorted(span_hits):
    print("  %08X in %08X  ->  payload+0x%04X  [%s]  {%s}  %s %s"
          % (site, fn, addr - PAYLOAD, kind, src, m, ops_))
print("\nCONTROL - accesses elsewhere in the same 0x1538 record: %d at %d distinct offsets"
      % (len(record_hits), len({h[2] for h in record_hits})))
for site, fn, addr, kind in sorted(record_hits)[:14]:
    print("  %08X in %08X  ->  payload+0x%04X  [%s]" % (site, fn, addr - PAYLOAD, kind))
print("\nLIMIT - calls handed a pointer into this record as an argument: %d site(s), "
      "%d distinct callees" % (sum(arg_carriers.values()), len(arg_carriers)))
for t, c in arg_carriers.most_common(8):
    print("  callee %08X  %d site(s)" % (t, c))
print("\nBLIND SPOT - INDEXED accesses whose known base lands in or before this record,")
print("             so the exact address is not fixed and the span cannot be excluded")
print("             for them: %d" % len(indexed_into))
for site, fn, addr, kind, m, ops_ in sorted(indexed_into)[:14]:
    print("  %08X in %08X  base -> payload+0x%04X  [%s]  %s %s"
          % (site, fn, addr - PAYLOAD, kind, m, ops_))
