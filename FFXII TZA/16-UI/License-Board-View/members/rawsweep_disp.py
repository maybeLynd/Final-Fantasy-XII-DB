"""rawsweep_disp.py LO HI DISP[,DISP...]: linear capstone sweep of raw .text bytes in [LO, HI) - listed or not - reporting
every instruction with a memory operand displacement in DISPS. Resynchronises on undecodable bytes by skipping one byte,
and re-anchors at every listed function entry so a bad sync inside data cannot run past a known body start. Marks whether
the instruction lies inside a listed body."""
import sys, struct, bisect
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
disps = set(int(x, 16) for x in sys.argv[3].split(","))
sizes = {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError):
        pass
ks = sorted(sizes)
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(ns):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(), *struct.unpack_from("<IIII", d, o + 8)))


def v2o(v):
    for n, vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs:
            return v - BASE - va + ro


def listed(a):
    i = bisect.bisect_right(ks, a) - 1
    return i >= 0 and ks[i] <= a < ks[i] + sizes[ks[i]]


md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
anchors = [a for a in ks if lo <= a < hi]
a = lo
while a < hi:
    nxt = min([x for x in anchors if x > a] + [hi])
    o = v2o(a)
    progressed = False
    for ins in md.disasm(d[o:o + (nxt - a)], a):
        progressed = True
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.disp in disps and not (op.mem.base and ins.reg_name(op.mem.base) == "rip"):
                print("%08X %-5s %-8s %s" % (ins.address, "list" if listed(ins.address) else "UNLST", ins.mnemonic, ins.op_str))
        a = ins.address + ins.size
    if not progressed or a < nxt and not progressed:
        a += 1
    elif a < nxt:
        a += 1
    else:
        a = nxt
