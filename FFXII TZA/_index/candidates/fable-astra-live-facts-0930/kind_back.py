import os, re
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch")
g = {}; exec(open("disw.py").read().split("fn = int")[0], g)
funcs, off, d = g["funcs"], g["off"], g["d"]
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
SITES = {0x0025C4F4:"eax",0x0025C5B9:"eax",0x0025C669:"eax",0x0025D005:"r14",0x0025D0B5:"r14",0x0025D182:"r14",0x0025D2E0:"r15",
         0x0025D39B:"ebx",0x00266CD2:"r14",0x00268BDB:"r15",0x00269700:"r15",0x00269766:"r15",0x002699AB:"esi",0x00269B71:"ecx",0x00269C0D:"eax"}
FAM = {"eax":"(r|e)ax|al","ebx":"(r|e)bx|bl","ecx":"(r|e)cx|cl","esi":"(r|e)si|sil","r14":"r14d?|r14b","r15":"r15d?|r15b"}
fl = sorted(funcs)
for s, r in sorted(SITES.items()):
    fn = max(f for f in fl if f <= s)
    ins = [i for i in md.disasm(bytes(d[off(fn):off(fn)+funcs[fn]]), fn) if i.address < s]
    rx = re.compile(r"^(%s)\b" % FAM[r])
    w = [i for i in ins if rx.match(i.op_str) and i.mnemonic not in ("cmp","test","push") ]
    last = w[-3:] if w else []
    print("%08X arg5=%s | %s" % (s, r, " ; ".join("%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in last)))
