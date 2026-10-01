"""t5_argtypes.py - for the hop-3 survivors whose store base is an entry argument, print every raw call site and the
defining instruction of the argument register there, so the argument can be typed (record or not).
python t5_argtypes.py > t5_argtypes.out"""
import json, os
import tk
from capstone.x86 import X86_OP_REG
HERE = os.path.dirname(os.path.abspath(tk.__file__))
IDX = json.load(open(os.path.join(HERE, "..", "pub140-scratch", "tools", "rawcalls.json")))
FAM = {"ecx": "rcx", "edx": "rdx", "ebx": "rbx", "edi": "rdi", "esi": "rsi", "eax": "rax", "r8d": "r8", "r9d": "r9"}
def fam(r): return FAM.get(r, r)
TARGETS = {0x00244DD0: "rcx", 0x002A27F0: "rcx", 0x0032B880: "rcx", 0x0032EC40: "rcx", 0x00380B80: "rcx", 0x00380D30: "rcx",
           0x003AB960: "rdx", 0x003D99B0: "rcx", 0x004FEAD0: "rcx", 0x00519A30: "rcx", 0x0051A320: "rcx", 0x0036BC60: "rbx",
           0x0023A570: "rdi", 0x00300E40: "rcx", 0x0030E360: "rsi", 0x0042DA30: "rbx"}
def slice_at(site, reg):
    fn, how = tk.owner(site)
    if fn is None or tk.fsize(fn) is None: return "unowned"
    ins = tk.fdis(fn); i = next((k for k, y in enumerate(ins) if y.address == site), None)
    if i is None: return "off-boundary"
    want = reg; out = []
    for j in range(i - 1, max(-1, i - 40), -1):
        y = ins[j]
        if y.mnemonic == "call": out.append("(call %08X before)" % y.address); break
        if not y.operands or y.operands[0].type != X86_OP_REG or fam(y.reg_name(y.operands[0].reg)) != want: continue
        if y.mnemonic in ("cmp", "test"): continue
        out.append("%08X %s %s" % (y.address, y.mnemonic, y.op_str))
        if y.mnemonic == "mov" and y.operands[1].type == X86_OP_REG: want = fam(y.reg_name(y.operands[1].reg)); continue
        break
    return " | ".join(out) or "(window)"
for f, reg in TARGETS.items():
    print("%s  (argument register at entry: %s)" % (tk.fname(f), "rcx" if reg not in ("rdx",) else reg))
    ar = "rdx" if reg == "rdx" else "rcx"
    for s in IDX.get("%X" % f, [])[:12]:
        s = int(s, 16)
        print("     %08X in %s: %s" % (s, tk.fname(s), slice_at(s, ar)))
