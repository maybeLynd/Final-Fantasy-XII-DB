"""t5_basedefs.py - for every W & H store listed in t5_regfile_h<N>.out, print the defining instruction chain of its base
register (linear backward slice inside the function, max 60 instructions, following reg<-reg moves), so each store
can be typed: the record itself (an entry argument, a getter return, a table entry [pool+8+i*8]) or a sub-object loaded
from a field.  python t5_basedefs.py t5_regfile_h2.out > t5_basedefs_h2.out"""
import sys, re
import tk
from capstone.x86 import X86_OP_REG, X86_OP_MEM
FAM = {}
for r64, subs in {"rax": "eax ax al", "rbx": "ebx bx bl", "rcx": "ecx cx cl", "rdx": "edx dx dl", "rsi": "esi si sil",
                  "rdi": "edi di dil", "rbp": "ebp bp bpl", "rsp": "esp sp spl"}.items():
    FAM[r64] = r64
    for s in subs.split(): FAM[s] = r64
for n in range(8, 16):
    for suf in ("", "d", "w", "b"): FAM["r%d%s" % (n, suf)] = "r%d" % n
def fam(r): return FAM.get(r, r)
cur = None; rows = []
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"^  ([0-9A-F]{8}) ", line)
    if m: cur = int(m.group(1), 16); continue
    m = re.match(r"^       ([0-9A-F]{8}) .*base=(\w+)", line)
    if m and cur is not None and cur != 0x0025E4C0: rows.append((cur, int(m.group(1), 16), m.group(2)))
for fn, site, base in rows:
    ins = tk.fdis(fn); i = next(k for k, y in enumerate(ins) if y.address == site)
    want = fam(base); chain = []
    for j in range(i - 1, max(-1, i - 60), -1):
        y = ins[j]
        if y.mnemonic == "call" and want in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
            chain.append("%08X %s %s  <- call result/clobber" % (y.address, y.mnemonic, y.op_str)); break
        if not y.operands or y.operands[0].type != X86_OP_REG or fam(y.reg_name(y.operands[0].reg)) != want: continue
        if y.mnemonic in ("cmp", "test", "push"): continue
        chain.append("%08X %s %s" % (y.address, y.mnemonic, y.op_str))
        if y.mnemonic == "mov" and y.operands[1].type == X86_OP_REG:
            want = fam(y.reg_name(y.operands[1].reg)); continue
        break
    else:
        chain.append("(entry value of %s)" % want)
    y = ins[i]
    print("%s  %08X %s %s\n      base %s: %s" % (tk.fname(fn), site, y.mnemonic, y.op_str, base, " | ".join(chain)))
