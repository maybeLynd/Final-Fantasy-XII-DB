"""nearcall_imm.py IMM[,IMM..] API[,API..] : every call to one of the APIs (listed functions, linear decode) whose
preceding 16 instructions contain the immediate/displacement IMM anywhere in an operand (mov/lea/add/sub/cmp).
Catches computed ids such as `lea r8d, [rsi + 0x9a]` that a constant tracker misses. --control via argv[3] sites."""
import sys, struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM
imms = {int(x, 16) for x in sys.argv[1].split(",")}; apis = {int(x, 16) for x in sys.argv[2].split(",")}
ctrl = [int(x, 16) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else []
exec(open("peek.py").read())
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
hits = []
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: f, n, sz = int(p[0], 16), p[1], int(p[2])
    except (ValueError, IndexError): continue
    o = off(f)
    if o is None: continue
    win = []
    for ins in md.disasm(d[o:o + sz], f):
        if ins.mnemonic == "call" and ins.op_str.startswith("0x") and int(ins.op_str, 16) in apis:
            for w in win[-16:]:
                for op in w.operands:
                    v = op.imm if op.type == X86_OP_IMM else (op.mem.disp if op.type == X86_OP_MEM and w.reg_name(op.mem.base) != "rip" else None)
                    if v in imms: hits.append((ins.address, f, n, w.address, w.mnemonic, w.op_str))
        win.append(ins)
for h in hits: print("%08X  [%08X %s]  <- %08X %s %s" % h)
fails = sum(1 for c in ctrl if c not in {h[0] for h in hits})
for c in ctrl: print("CONTROL %08X:" % c, "FAIL" if c not in {h[0] for h in hits} else "PASS")
print("FAILS", fails)
