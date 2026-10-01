"""SavePayload's four unobserved spans, censused with both addressing forms.

12,000 bytes across four rows - the largest single non-Phyre structural debt in the store. The
payload sits at a CONSTANT address (route `FN 0x002EF640+0x200`, and 002EF640 is a two-instruction
leaf returning 0x02164280), so this is decidable over the code rather than over a moment.

WHY RE-RUN SOMETHING THAT HAS BEEN CENSUSED. Two instrument defects found today, both of which
bear directly on a global at a fixed address:

  * The AQ18 tracker kept a stale `lea` value through a partial-register write, so it could
    MISPLACE an access, and it dropped register-register ADD, so it could lose one. Repaired
    under ASTRA-CONTRA-OPUS-AQ18-SCANNER-PARTIAL-ALIASES; the repair alone resolves 6,643 more
    memory operands image-wide.
  * BLIND SPOT 11, found under ASTRA-CONTRA-OPUS-MGRMARK-HAS-CLEAR: a census that looks for code
    FORMING a global's address cannot see the image-base idiom - `lea r14,[rip-X]` materialising
    0x120000, then reaching the global by its image OFFSET as a displacement. That idiom is
    ordinary here: 921 lea sites in 641 bodies, 1,901 accesses. **For a global at a fixed address
    this is precisely the form that would reach it**, which is why this census exists.

So this tracker follows an image-base `lea` into whatever register holds it and resolves both
forms in one pass. Every hit is tagged with which form found it, because a hit only visible to
the image-base form is evidence about the earlier censuses as well as about the span.

REPORTED SEPARATELY: EXACT (whole address fixed) and INDEXED (base known, index not) - a span
reached by a scaled walk is exactly what a fixed-address census cannot exclude.
"""
import csv, io, os, sys, collections

KIT = r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts"
sys.path.insert(0, KIT)
import kit_paths as KP, disasm_fn as DF
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import capstone.x86 as X

img = DF.Image(KP.EXE)
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

IMAGE_BASE = 0x120000
PAYLOAD = 0x02164280 + 0x200               # 0x02164480
SPANS = [("unobservedSpan1538",  0x1538, 2760),
         ("unobservedSpanC818",  0xC818, 6120),
         ("unobservedSpanE004",  0xE004,   60),
         ("unobservedTail5589C", 0x5589C, 3060)]

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

hits = collections.defaultdict(list)       # span name -> [(site, fn, off, kind, form, text)]
resolved = unresolved = 0
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
                if mm.base or mm.index:
                    unresolved += 1
                continue
            extra = 0
            if mm.index:
                ci = C.get(ins.reg_name(mm.index))
                v = reg.get(ci) if ci else None
                if isinstance(v, int):
                    extra = v * (mm.scale or 1)
            addr = base + mm.disp + extra
            resolved += 1
            acc = getattr(op, "access", 0)
            kind = ("w" if acc & 2 else "") + ("r" if acc & 1 else "") or "r"
            fixed = (not mm.index) or extra
            for nm, off, ln in SPANS:
                lo = PAYLOAD + off
                if lo <= addr < lo + ln:
                    hits[nm].append((ins.address, fn, addr - lo, kind,
                                     f if fixed else f + "+indexed", "%s %s" % (m, ins.op_str)))
                    break

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
                cs_ = C.get(ins.reg_name(o1.reg))
                val = reg.get(cs_) if cs_ else None; f = form.get(cs_, "direct")
            elif m == "mov" and o1.type == X.X86_OP_IMM:
                val = o1.imm
            elif o1.type == X.X86_OP_IMM and m in ("add", "sub"):
                v = reg.get(dst); f = form.get(dst, "direct")
                val = (v + o1.imm * (1 if m == "add" else -1)) if isinstance(v, int) else None
            elif o1.type == X.X86_OP_REG and m in ("add", "sub"):
                cs_ = C.get(ins.reg_name(o1.reg))
                v, w = reg.get(dst), (reg.get(cs_) if cs_ else None)
                if isinstance(v, int) and isinstance(w, int):
                    val = v + w * (1 if m == "add" else -1)
                    f = "imagebase" if "imagebase" in (form.get(dst), form.get(cs_)) else f
                else:
                    val = None

        for rg in ins.regs_access()[1]:
            c = KILL.get(ins.reg_name(rg))
            if c: reg[c] = None; form.pop(c, None)
        if m == "call":
            for v in VOL: reg[v] = None; form.pop(v, None)
            if ops and ops[0].type == X.X86_OP_IMM and ops[0].imm == 0x2EF640:
                reg["rax"], form["rax"] = 0x02164280, "direct"
        if dst and val is not NOVAL:
            reg[dst] = val
            if isinstance(val, int): form[dst] = f
            else: form.pop(dst, None)

print("payload base %08X   tracker resolved %d operands, %d unresolved (%.1f%%)"
      % (PAYLOAD, resolved, unresolved, 100.0 * resolved / (resolved + unresolved)))
print()
total = 0
for nm, off, ln in SPANS:
    h = hits[nm]
    total += len(h)
    print("%-22s payload+0x%05X  %5d bytes   ACCESSES: %d" % (nm, off, ln, len(h)))
    for site, fn, d, kind, f, txt in sorted(h)[:12]:
        print("    %08X in %08X  ->  span+0x%04X  [%s]  {%s}  %s" % (site, fn, d, kind, f, txt))
    if len(h) > 12:
        print("    ... and %d more" % (len(h) - 12))
print()
print("TOTAL ACCESSES INTO THE FOUR SPANS: %d" % total)
byform = collections.Counter(f for l in hits.values() for *_x, f, _t in [(*e,) for e in l])
print("by addressing form:", dict(collections.Counter(e[4] for l in hits.values() for e in l)))
