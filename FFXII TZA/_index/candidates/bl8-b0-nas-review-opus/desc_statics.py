"""Static PhyreClassDescriptor objects: rcx at every call of the base ctors 00632D80 / 00632C90, traced back two levels (OPUS scratch)."""
import struct, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, CS_OP_MEM, CS_OP_REG
from capstone.x86 import X86_REG_RIP, X86_REG_RCX
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database"
d = open(DB + r"\Tools\work\exe\FFXII_TZA.exe", "rb").read(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(DB + r"\Tools\work\graph\functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
BODY = {}
def body(f):
    if f not in BODY:
        o = off(f); BODY[f] = list(cs.disasm(d[o:o + sizes[f]], f)) if o is not None and sizes[f] > 0 else []
    return BODY[f]
callers = collections.defaultdict(list)
for f in sizes:
    if not (0x121000 <= f < 0x900000): continue
    for i, x in enumerate(body(f)):
        if x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type == CS_OP_IMM:
            callers[x.operands[0].imm].append((f, i))
def rcx_source(f, i):
    """walk back from instruction i in f: 'S', addr for lea rcx,[rip+X]; 'ARG' if rcx is the entry rcx; None otherwise"""
    xs = body(f); reg = X86_REG_RCX
    for x in reversed(xs[:i]):
        if x.operands and x.operands[0].type == CS_OP_REG and x.operands[0].reg == reg and x.mnemonic in ("lea", "mov"):
            src = x.operands[1]
            if x.mnemonic == "lea" and src.type == CS_OP_MEM and src.mem.base == X86_REG_RIP: return ("S", x.address + x.size + src.mem.disp)
            if x.mnemonic == "mov" and src.type == CS_OP_REG: reg = src.reg; continue
            return None
        if x.mnemonic == "call": return None if reg in (X86_REG_RCX,) else ("ARG?", reg)
    return ("ARG", reg) if reg == X86_REG_RCX else ("ARGREG", reg)
statics = set(); unresolved = collections.Counter()
for ctor in (0x632D80, 0x632C90):
    for f, i in callers[ctor]:
        s = rcx_source(f, i)
        if s and s[0] == "S": statics.add(s[1]); continue
        # rcx came from this function's own rcx (possibly via a saved register): take its callers
        got = False
        for g, j in callers[f]:
            s2 = rcx_source(g, j)
            if s2 and s2[0] == "S": statics.add(s2[1]); got = True
        if not got: unresolved["%08X" % f] += 1
print("descriptor statics", len(statics), "unresolved ctor callers", len(unresolved))
print(" ".join("%08X" % s for s in sorted(statics)[:12]), "...")
print("unresolved sample", list(unresolved)[:15])
open(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "descriptor-statics.txt"), "w").write(",".join("%08X" % s for s in sorted(statics)))
