"""builders.py - UQ-47 / UQ-46: the 66 hub-called builders; which call none of memset / 008631D0 / 008631E0;
what those do instead (stores by offset into their object, other callees); and each object's store extent."""
import struct, sys, collections, os
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
HELPERS = {0x861EC0: "memset", 0x8631D0: "hdr", 0x8631E0: "reg"}
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((BASE + va, vs, ro, rs))
def off(a):
    for va, vs, ro, rs in secs:
        if va <= a < va + rs: return ro + (a - va)
sizes = {}; names = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
def ins(f): return list(md.disasm(d[off(f):off(f) + sizes[f]], f))
def riptarget(x, op): return x.address + x.size + op.mem.disp
# hubs: (object, builder) pairs
pairs = []
for hub in (0x37DF90, 0x37E0F0):
    last_lea = None
    for x in ins(hub):
        if x.mnemonic == "lea" and x.operands[0].type == X86_OP_REG and x.reg_name(x.operands[0].reg) == "rcx" and x.operands[1].type == X86_OP_MEM and x.reg_name(x.operands[1].mem.base) == "rip":
            last_lea = riptarget(x, x.operands[1])
        if x.mnemonic == "call" and x.operands[0].type == X86_OP_IMM:
            pairs.append((hub, last_lea, x.operands[0].imm)); last_lea = None
print("hub calls:", len(pairs), " by hub:", collections.Counter(h for h, _, _ in pairs))
band = [(h, o, b) for h, o, b in pairs if 0x480000 <= b < 0x500000 or b in sizes and (o is not None)]
# per builder census
rows = []
for hub, obj, b in pairs:
    if b not in sizes: continue
    callees = collections.Counter(); stores = []; other = []
    objregs = {"rcx"}          # the object pointer arrives in rcx; follow plain register copies of it
    for x in ins(b):
        if x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[0].type == X86_OP_REG and x.operands[1].type == X86_OP_REG:
            dst, src = x.reg_name(x.operands[0].reg), x.reg_name(x.operands[1].reg)
            if src in objregs: objregs.add(dst)
            elif dst in objregs: objregs.discard(dst)
        elif x.operands and x.operands[0].type == X86_OP_REG and x.mnemonic not in ("cmp", "test", "push") and len(x.operands) >= 1:
            dst = x.reg_name(x.operands[0].reg)
            if dst in objregs and dst != "rcx" and x.mnemonic != "mov":
                objregs.discard(dst)
        if x.mnemonic == "call" and x.operands[0].type == X86_OP_IMM:
            callees[x.operands[0].imm] += 1
            objregs -= {"rax", "rdx", "r8", "r9", "r10", "r11"}   # volatile across the call; rcx is too
            objregs.discard("rcx")
        if x.mnemonic.startswith("mov") and x.operands and x.operands[0].type == X86_OP_MEM:
            m = x.operands[0].mem
            base = x.reg_name(m.base) if m.base else ""
            if base == "rip":
                stores.append(("abs", riptarget(x, x.operands[0]), x.operands[0].size))
            elif base in objregs and not m.index:
                stores.append((base, m.disp, x.operands[0].size))
    h = {HELPERS[c] for c in callees if c in HELPERS}
    others = {c: k for c, k in callees.items() if c not in HELPERS}
    # store extent relative to a base register (the object is passed in rcx; builders often move it to rbx/rdi)
    rel = [(s[1], s[2]) for s in stores if s[0] != "abs"]
    ext = max((o + w for o, w in rel), default=0)
    absr = [s for s in stores if s[0] == "abs"]
    rows.append((hub, obj, b, sizes[b], sorted(h), others, len(rel), ext, len(absr), stores))
none = [r for r in rows if not r[4]]
print("builders with a body:", len(rows), " calling none of the three:", len(none))
print()
print("%-8s %-8s %-8s %5s %-14s %5s %6s %5s  %s" % ("hub", "object", "builder", "size", "helpers", "stores", "extent", "abs", "other callees"))
for hub, obj, b, sz, h, others, nrel, ext, nabs, st in sorted(rows, key=lambda r: (r[0], r[1] or 0)):
    if h: continue
    oc = " ".join("%08X%s" % (c, "x%d" % k if k > 1 else "") for c, k in sorted(others.items()))
    print("%08X %08X %08X %5d %-14s %5d %6X %5d  %s" % (hub, obj or 0, b, sz, ",".join(h) or "-", nrel, ext, nabs, oc[:60]))
print()
print("=== the same for ALL builders (for UQ-46: store extent vs memset size) ===")
for hub, obj, b, sz, h, others, nrel, ext, nabs, st in sorted(rows, key=lambda r: (r[0], r[1] or 0)):
    print("%08X %08X %08X %5d %-14s %5d %6X %5d" % (hub, obj or 0, b, sz, ",".join(h) or "-", nrel, ext, nabs))
if len(sys.argv) > 1 and sys.argv[1] == "--dump":
    for hub, obj, b, sz, h, others, nrel, ext, nabs, st in rows:
        if h: continue
        print("\n--- %08X (object %08X, %d B)" % (b, obj or 0, sz))
        for x in ins(b): print("  %08X  %-8s %s" % (x.address, x.mnemonic, x.op_str))
