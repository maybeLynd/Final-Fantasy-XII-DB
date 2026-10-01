"""abi_livein.py - OPUS (Claude Opus 5.5), 2026-09-28. An ABI discriminator for UC-1 body candidates: a Win64 function entry cannot
depend on the incoming value of a NONVOLATILE register (rbx, rbp, rsi, rdi, r12-r15, xmm6-xmm15) - the callee must save it before
use and may only read it to save it. A block whose first touch of such a register (in linear order from the start) is a READ
that is not a save (push, or a store of the register to [rsp + x]) consumes a value its caller never passed, so it is a
continuation of the code before it, not an entry. The linear order is an approximation of the control flow: it can MISS a read
on a branch taken before a write, so a PASS is weak and a FAIL is the signal.

  L  applied to every clean row of the >256 B band and, as a control, to the 99 admitted 65-256 B bodies and the 696 new 1-64 B
     bodies (the populations FABLE ruled on): it reports each failure with the first offending instruction
Usage: python abi_livein.py
"""
import hashlib, io, os, struct, sys
import capstone
from capstone import x86_const as X
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); md.detail = True
NV = {X.X86_REG_RBX: "rbx", X.X86_REG_RBP: "rbp", X.X86_REG_RSI: "rsi", X.X86_REG_RDI: "rdi", X.X86_REG_R12: "r12", X.X86_REG_R13: "r13",
      X.X86_REG_R14: "r14", X.X86_REG_R15: "r15"}
NV.update({getattr(X, "X86_REG_XMM%d" % k): "xmm%d" % k for k in range(6, 16)})
def family(r):
    """map sub-registers (ebx, bx, bl, r12d ...) to the 64-bit nonvolatile they belong to"""
    name = md.reg_name(r)
    for full, nm in NV.items():
        if name == nm: return full
    alias = {"ebx": "rbx", "bx": "rbx", "bl": "rbx", "bh": "rbx", "ebp": "rbp", "bp": "rbp", "bpl": "rbp", "esi": "rsi", "si": "rsi",
             "sil": "rsi", "edi": "rdi", "di": "rdi", "dil": "rdi"}
    for k in range(12, 16):
        for suf in ("d", "w", "b"): alias["r%d%s" % (k, suf)] = "r%d" % k
    tgt = alias.get(name)
    return next((f for f, nm in NV.items() if nm == tgt), None) if tgt else None
def first_livein(v, nb):
    seen = set()
    for x in md.disasm(d[off(v):off(v) + nb], v):
        try: rd, wr = x.regs_access()
        except capstone.CsError: continue
        save = x.mnemonic == "push" or (x.mnemonic in ("mov", "movaps", "movdqa", "movups", "movdqu") and x.operands and x.operands[0].type == X.X86_OP_MEM
                                         and x.operands[0].mem.base == X.X86_REG_RSP)
        zero_idiom = x.mnemonic in ("xor", "pxor", "xorps", "sub", "psubw") and len(x.operands) == 2 and x.operands[0].type == X.X86_OP_REG \
            and x.operands[1].type == X.X86_OP_REG and x.operands[0].reg == x.operands[1].reg
        for r in rd:
            f = family(r)
            if f is not None and f not in seen and not save and not zero_idiom:
                return "%08X %s %s (%s)" % (x.address, x.mnemonic, x.op_str, NV[f])
        for r in wr:
            f = family(r)
            if f is not None: seen.add(f)
        if save:
            for r in rd:
                f = family(r)
                if f is not None: seen.add(f)
        if x.mnemonic in ("ret",): break
    return None
def rows(path, kinds, startcol, endcol, kindcol):
    out = []
    for l in io.open(path, encoding="utf-8"):
        if l.startswith("#") or l.startswith("kind") or l.startswith("start"): continue
        c = l.rstrip("\n").split("\t")
        if c[kindcol] in kinds: out.append((int(c[startcol], 16), int(c[endcol], 16) if endcol is not None else None, c))
    return out
UC = os.path.join(DB, "99-Unresolved-Residual", "Unlisted-Code")
clean = [(int(c[0], 16), int(c[1])) for v, e, c in rows(os.path.join(HERE, "uc1-band-257-up-rows.tsv"), {"clean"}, 0, None, -1)]
a65 = [(v, e - v) for v, e, c in rows(os.path.join(UC, "uc1-applied-population-65-256.tsv"), {"admit-frontier"}, 2, 3, 0)]
a64 = [(v, e - v) for v, e, c in rows(os.path.join(UC, "uc1-applied-population-1-64.tsv"), {"admit-frontier", "split-part"}, 2, 3, 0)]
for name, pop in ((">256 B clean", clean), ("65-256 B admitted", a65), ("1-64 B admitted", a64)):
    bad = [(("%08X" % v), first_livein(v, nb)) for v, nb in pop]
    bad = [b for b in bad if b[1]]
    print("L  %-18s %4d rows, %d read a nonvolatile before writing it%s" % (name, len(pop), len(bad), "" if not bad else ":"))
    for b in bad[:40]: print("     %s  %s" % b)
# sensitivity control: the admissions TSV's own `continuation` rows (code classified as the tail of the body before it)
adm = [l.rstrip("\n").split("\t") for l in io.open(os.path.join(UC, "unlisted-body-admissions.tsv"), encoding="utf-8") if not l.startswith("#")][1:]
cont = [(int(r[0], 16), int(r[1])) for r in adm if r[8] == "continuation"]
fc = sum(1 for v, nb in cont if first_livein(v, nb))
print("C  sensitivity: %d of %d `continuation` rows fail L (one-directional: a fail marks a continuation, a pass proves nothing);"
      " specificity: 0 failures among the 795 admitted bodies above" % (fc, len(cont)))
