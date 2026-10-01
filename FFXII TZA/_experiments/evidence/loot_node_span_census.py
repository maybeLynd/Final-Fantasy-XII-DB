"""WorldLootPickupNode's two 4-byte spans, re-censused with both addressing forms.

S-33's types cell is PARTIAL and only eight bytes of this type are unobserved - +0x0C and +0x5C,
four bytes each. Both rows say "no censused access". Two instrument defects found today bear on
that, and this pool is exactly the shape they affect:

  * the fixed-address tracker kept a stale value through a partial-register write and dropped
    register-register ADD (ASTRA-CONTRA-OPUS-AQ18-SCANNER-PARTIAL-ALIASES);
  * BLIND SPOT 11 - a census that looks for code FORMING a global's address cannot see the
    image-base idiom, `lea r14,[rip-X]` then a displacement that is an image OFFSET. The pool is
    a .bss array at a FIXED address, which is precisely the case that idiom serves.

The pool is `ARRAY 0x02EC0FA0 stride=0x60 count=10`, so accesses are indexed and a fixed-address
census cannot resolve them exactly. This reports INDEXED hits by their offset within the stride,
which is the question the two spans actually ask.

CONTROL: the same pass must find the fields this type already declares - slotIndex at +0x00,
state at +0x04, materialiseStamp at +0x08. A zero at +0x0C and +0x5C means nothing until those
come back.
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

POOL, STRIDE, COUNT = 0x02EC0FA0, 0x60, 10
IMAGE_BASE = 0x120000
LO, HI = POOL, POOL + STRIDE * COUNT

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

hits = collections.defaultdict(list)     # offset-in-stride -> [(site, fn, kind, form, text)]
for fn, n in fns:
    if n <= 0 or n > 1 << 18:
        continue
    body = img.read(fn, n)
    if not body:
        continue
    reg, form = {}, {}
    for ins in md.disasm(body, fn):
        m, ops = ins.mnemonic, ins.operands
        for op in ops:
            if op.type != X.X86_OP_MEM or m == "lea":
                continue
            mm = op.mem
            base, f = None, "direct"
            if mm.base == X.X86_REG_RIP:
                base = ins.address + ins.size
            elif mm.base:
                cb = C.get(ins.reg_name(mm.base))
                base = reg.get(cb) if cb else None
                f = form.get(cb, "direct")
            elif not mm.index:
                base = 0
            if not isinstance(base, int):
                continue
            addr = base + mm.disp
            # an indexed walk over the pool: the base lands in it, the element is not fixed
            if LO <= addr < HI:
                acc = getattr(op, "access", 0)
                kind = ("w" if acc & 2 else "") + ("r" if acc & 1 else "") or "r"
                tag = f + ("+indexed" if mm.index else "")
                # ATTRIBUTE THE ACCESS TO EVERY BYTE IT COVERS, not just its starting offset.
                # The first version bucketed by start only, and the pool initialiser zeroes
                # state (+0x04) and materialiseStamp (+0x08) with ONE qword store at +0x04 -
                # so a declared field read as "not found" was simply being written by a wider
                # neighbour. A control that fails for that reason is a bucketing defect, not
                # a reach defect, and the difference decides whether the zeros below mean
                # anything.
                for b in range(max(1, op.size)):
                    hits[(addr - POOL + b) % STRIDE].append(
                        (ins.address, fn, kind, tag, "%s %s" % (m, ins.op_str)))

        dst, val, f = None, NOVAL, "direct"
        if m == "lea" and ops[0].type == X.X86_OP_REG:
            dst = C.get(ins.reg_name(ops[0].reg)); s = ops[1].mem
            if s.base == X.X86_REG_RIP and not s.index:
                val = ins.address + ins.size + s.disp
                if val == IMAGE_BASE: f = "imagebase"
            elif s.base and not s.index:
                cb = C.get(ins.reg_name(s.base)); v = reg.get(cb) if cb else None
                val = v + s.disp if isinstance(v, int) else None
                f = form.get(cb, "direct")
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
                f = form.get(cs_, "direct")
            elif m == "mov" and o1.type == X.X86_OP_IMM:
                val = o1.imm
            elif o1.type == X.X86_OP_IMM and m in ("add", "sub"):
                v = reg.get(dst); f = form.get(dst, "direct")
                val = (v + o1.imm * (1 if m == "add" else -1)) if isinstance(v, int) else None
            elif o1.type == X.X86_OP_REG and m in ("add", "sub"):
                cs_ = C.get(ins.reg_name(o1.reg))
                v, w = reg.get(dst), (reg.get(cs_) if cs_ else None)
                val = v + w * (1 if m == "add" else -1) if isinstance(v, int) and isinstance(w, int) else None
        for rg in ins.regs_access()[1]:
            c = KILL.get(ins.reg_name(rg))
            if c: reg[c] = None; form.pop(c, None)
        if m == "call":
            for v in VOL: reg[v] = None; form.pop(v, None)
        if dst and val is not NOVAL:
            reg[dst] = val
            if isinstance(val, int): form[dst] = f
            else: form.pop(dst, None)

print("pool %08X stride 0x%X count %d  (%08X..%08X)" % (POOL, STRIDE, COUNT, LO, HI))
print("\nACCESSES BY OFFSET WITHIN THE STRIDE")
print("%-8s %-6s %s" % ("offset", "count", "sites"))
for off in sorted(hits):
    l = hits[off]
    print("  +0x%02X   %-4d  %s" % (off, len(l),
          ", ".join("%08X[%s/%s]" % (s, k, f) for s, _fn, k, f, _t in l[:4])))
print("\nCONTROL - the three declared fields must appear:")
for off, nm in ((0x00, "slotIndex"), (0x04, "state"), (0x08, "materialiseStamp")):
    print("   +0x%02X %-18s %d access(es)  %s" % (off, nm, len(hits.get(off, [])),
          "FOUND" if hits.get(off) else "NOT FOUND - the census reaches nothing and the result below is void"))
print("\nTHE TWO OPEN SPANS:")
for off, nm in ((0x0C, "unobservedSpan000C"), (0x5C, "unobservedTail005C")):
    l = hits.get(off, [])
    print("   +0x%02X %-20s %d access(es)" % (off, nm, len(l)))
    for s, fn, k, f, t in l[:8]:
        print("        %08X in %08X [%s] {%s}  %s" % (s, fn, k, f, t))
forms = collections.Counter(f for l in hits.values() for *_a, f, _t in [(*e,) for e in l])
print("\nby addressing form:", dict(collections.Counter(e[3] for l in hits.values() for e in l)))
