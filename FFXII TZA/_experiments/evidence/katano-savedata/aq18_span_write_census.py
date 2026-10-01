#!/usr/bin/env python3
"""AQ-18, the part a sample cannot do: does ANY instruction in .text touch the span?

PersistentFlagPayload's route is FN 0x002EF640+0x200, and 002EF640 is a two-instruction
leaf - `lea rax, [02164280]` / `ret`. So the payload is at a CONSTANT ADDRESS, 0x02164480,
and the contested span +0xCF6..+0x1000 is absolute 0x02165176..0x02165480.

That makes an absence claim decidable over the code rather than over a moment, which is
what ASTRA-CONTRA-OPUS-AQ18-AQ19-NEGATIVE-INFERENCE correctly said no sample could give.

THE SWEEP.  Every listed function body is decoded and interpreted forward, tracking which
registers hold a known absolute address: rip-relative `lea` seeds them, register-to-register
moves copy them, `add`/`sub` of an immediate offsets them, a `call` clears the caller-saved
set, and anything else kills the destination.  Every memory operand is then resolved to an
absolute address when its base is known, and reported if it lands in the span.

WHAT THIS CAN AND CANNOT CLOSE, stated before running:
  * A HIT is decisive - the span is touched, and the instruction says read or write.
  * NO HIT is an absence over every access this method can resolve.  It is NOT the same as
    "nothing writes it": an access whose base arrives as a function ARGUMENT, or through a
    pointer loaded from memory, is invisible here.  The sweep therefore also reports HOW
    MANY sites resolve at all, and how many calls receive a span-bearing pointer as an
    argument - because an absence whose denominator is unknown is not a census.
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

C = {}
for g in ["rax","rbx","rcx","rdx","rsi","rdi","rbp","r8","r9","r10","r11","r12","r13","r14","r15"]:
    C[g] = g
    if g[1].isdigit(): C[g + "d"] = g
    else: C["e" + g[1:]] = g
VOL = ("rax","rcx","rdx","r8","r9","r10","r11")
ARGS = ("rcx","rdx","r8","r9")

fns = []
for r in csv.DictReader(io.open(os.path.join(KP.WORK, "graph", "functions.tsv"),
                                encoding="utf-8", newline=""), delimiter="\t"):
    fns.append((int(r["entry"], 16), int(r["body_bytes"])))

span_hits, record_hits, indexed_into = [], [], []
resolved_sites = 0
arg_carriers = collections.Counter()
for fn, n in fns:
    if n <= 0 or n > 1 << 18:
        continue
    reg, a, end = {}, fn, fn + n
    while a < end:
        b = img.read(a, 16)
        if not b:
            break
        ins = next(md.disasm(b, a), None)
        if ins is None:
            break
        m, ops = ins.mnemonic, ins.operands
        # resolve memory operands whose base we know
        for oi, op in enumerate(ops):
            if op.type != X.X86_OP_MEM or m == "lea":
                continue
            mm = op.mem
            base = None
            if mm.base == X.X86_REG_RIP:
                base = ins.address + ins.size
            elif mm.base:
                cb = C.get(ins.reg_name(mm.base))
                base = reg.get(cb) if cb else None
            if not isinstance(base, int):
                continue
            addr = base + mm.disp
            resolved_sites += 1
            acc = getattr(op, "access", 0)
            kind = ("w" if acc & 2 else "") + ("r" if acc & 1 else "") or "r"
            if mm.index:
                # A scaled walk: the base is known but the exact address is not, so this
                # site could reach anywhere at or above `addr`. Counted rather than
                # dropped - an indexed write into the span is exactly what a fixed-address
                # census cannot see, and an absence whose blind spot is unmeasured is not
                # a census.
                if REC_LO <= addr < REC_HI or (addr <= LO and addr + 0x1538 > LO):
                    indexed_into.append((ins.address, fn, addr, kind, m, ins.op_str))
                continue
            if LO <= addr < HI:
                span_hits.append((ins.address, fn, addr, kind, m, ins.op_str))
            elif REC_LO <= addr < REC_HI:
                record_hits.append((ins.address, fn, addr, kind))
        # a call that receives a span-bearing pointer hides the rest of the story
        if m == "call":
            for r_ in ARGS:
                v = reg.get(r_)
                if isinstance(v, int) and REC_LO <= v < REC_HI:
                    arg_carriers[(ops[0].imm if ops and ops[0].type == X.X86_OP_IMM else 0)] += 1
        # transfer
        if m == "lea" and ops[0].type == X.X86_OP_REG:
            d = C.get(ins.reg_name(ops[0].reg)); s = ops[1].mem
            if d:
                if s.base == X.X86_REG_RIP and not s.index:
                    reg[d] = ins.address + ins.size + s.disp
                elif s.base and not s.index:
                    cb = C.get(ins.reg_name(s.base)); v = reg.get(cb) if cb else None
                    reg[d] = v + s.disp if isinstance(v, int) else None
                else:
                    reg[d] = None
        elif m == "mov" and ops[0].type == X.X86_OP_REG and ops[1].type == X.X86_OP_REG:
            d = C.get(ins.reg_name(ops[0].reg)); s = C.get(ins.reg_name(ops[1].reg))
            if d: reg[d] = reg.get(s)
        elif m in ("add", "sub") and ops[0].type == X.X86_OP_REG and ops[1].type == X.X86_OP_IMM:
            d = C.get(ins.reg_name(ops[0].reg)); v = reg.get(d)
            if d: reg[d] = (v + ops[1].imm * (1 if m == "add" else -1)) if isinstance(v, int) else None
        elif m == "call":
            for v in VOL: reg[v] = None
            # 002EF640 returns the buffer in rax - model it, it is the route's own getter
            if ops and ops[0].type == X.X86_OP_IMM and ops[0].imm == 0x2EF640:
                reg["rax"] = BUF
        else:
            for rg in ins.regs_access()[1]:
                c = C.get(ins.reg_name(rg))
                if c: reg[c] = None
        a += ins.size

print("payload base %08X   contested span %08X..%08X (%d bytes)"
      % (PAYLOAD, LO, HI, HI - LO))
print("memory operands resolved to an absolute address anywhere: %d" % resolved_sites)
print("\nACCESSES INSIDE THE CONTESTED SPAN: %d" % len(span_hits))
for site, fn, addr, kind, m, ops_ in sorted(span_hits):
    print("  %08X in %08X  ->  payload+0x%04X  [%s]  %s %s"
          % (site, fn, addr - PAYLOAD, kind, m, ops_))
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