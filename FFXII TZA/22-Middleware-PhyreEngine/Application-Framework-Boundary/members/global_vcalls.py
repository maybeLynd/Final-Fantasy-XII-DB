"""global_vcalls.py GLOBAL: for every function reading the qword GLOBAL (an object pointer), follow the loaded register
within the next 12 instructions (through one `mov reg2, reg` copy and one vtable load `mov r, [reg]`) to indirect calls
`call/jmp [vt + disp]`, and print slot number, call site, containing function, and the byte/int argument setup of
edx/dl and r8 in the preceding instructions. Linear and intra-block only: a register overwritten before the call ends
the track. Reports every read site, including ones where no slot call was followed."""
import sys, struct, bisect
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
G = int(sys.argv[1], 16)
sizes, names = {}, {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError):
        pass
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(ns):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(), *struct.unpack_from("<IIII", d, o + 8)))
text = [s for s in secs if s[0] == ".text"][0]


def v2o(v):
    for n, vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs:
            return v - BASE - va + ro


md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
n, vs, va, rs, ro = text
for e in sorted(sizes):
    if not (BASE + va <= e < BASE + va + vs):
        continue
    o = v2o(e)
    if o is None:
        continue
    ins = list(md.disasm(d[o:o + sizes[e]], e))
    for i, x in enumerate(ins):
        if x.mnemonic != "mov" or len(x.operands) != 2 or x.operands[1].type != X86_OP_MEM:
            continue
        m = x.operands[1].mem
        if not (m.base and x.reg_name(m.base) == "rip" and x.address + x.size + m.disp == G):
            continue
        objs = {x.reg_name(x.operands[0].reg)}
        vts = set()
        found = False
        for y in ins[i + 1:i + 14]:
            ops = y.operands
            if y.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG:
                dst = y.reg_name(ops[0].reg)
                if ops[1].type == X86_OP_REG and y.reg_name(ops[1].reg) in objs:
                    objs.add(dst); continue
                if ops[1].type == X86_OP_MEM and ops[1].mem.base and y.reg_name(ops[1].mem.base) in objs and ops[1].mem.disp == 0:
                    vts.add(dst); continue
                objs.discard(dst); vts.discard(dst)
            if y.mnemonic in ("call", "jmp") and ops and ops[0].type == X86_OP_MEM and ops[0].mem.base and y.reg_name(ops[0].mem.base) in vts:
                j = ins.index(y)
                args = [z for z in ins[max(0, j - 6):j] if z.op_str.startswith(("edx", "dl", "rdx", "r8", "xmm1"))]
                print("slot %2d  call %08X  in %08X %-40s args: %s" % (ops[0].mem.disp // 8, y.address, e, names[e][:40],
                      " ; ".join("%s %s" % (z.mnemonic, z.op_str) for z in args)))
                found = True
                break
            if y.mnemonic in ("call", "ret"):
                break
        if not found:
            print("read     %08X  in %08X %-40s (no slot call followed)" % (x.address, e, names[e][:40]))
