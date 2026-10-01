"""ctrl590.py - SWE2-AUDIT-SPEC: the save menu's slot-header table is also held at [ctrl + 0x590].
00583040 builds the menu's create parameter at rsp+0x30 (+0x18 = [ctrl+0x590], 005831D0/005831D7), and the handler
0057FE80 copies param+0x18 into [widget+0x1C0] (0057FF1C/0057FF20). The OPUS census (sd_slot_header_reads.py) seeds
HDR only as a load of [MENU + 0x1C0]. This lists every 8-byte load of [reg + 0x590] in functions that also read the
controller global 02CA99B8, or that lie in the save UI module 0057C000-00586000, and follows the loaded register
linearly (until it is overwritten) for memory accesses through it, printing their displacements and widths, and the
field they hit mod 0xA0.
"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_REG
import capstone
CTRL = 0x02CA99B8
refs, _ = tk.rip_refs(CTRL, CTRL + 8)
ctrl_fns = set(tk.owner(x.address)[0] for x, k, t in refs)
dr, _ = tk.disp_refs(0x590, 0x591)
loads = []
for x, k, v in dr:
    f = tk.owner(x.address)[0]
    if f is None: continue
    if not (f in ctrl_fns or 0x0057C000 <= f < 0x00586000): continue
    if x.mnemonic == "mov" and x.operands[0].type == X86_OP_REG and x.operands[1].type == X86_OP_MEM and x.operands[1].size == 8:
        loads.append((f, x))
    else:
        print("other +0x590 access %08X %s %s  in %s" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address)))
print("8-byte loads of [reg+0x590] in CTRL-reading or save-module functions: %d" % len(loads))
FAM = lambda r: {"rax": "a", "eax": "a", "rbx": "b", "ebx": "b", "rcx": "c", "ecx": "c", "rdx": "d", "edx": "d", "rsi": "si", "esi": "si", "rdi": "di", "edi": "di", "rbp": "bp", "ebp": "bp"}.get(r, r.rstrip("d"))
for f, x in loads:
    reg = tk.md.reg_name(x.operands[0].reg)
    body = tk.fdis(f)
    idx = next(i for i, y in enumerate(body) if y.address == x.address)
    uses = []
    for y in body[idx + 1: idx + 60]:
        for op in y.operands:
            if op.type == X86_OP_MEM and (FAM(tk.md.reg_name(op.mem.base) or "") == FAM(reg) or FAM(tk.md.reg_name(op.mem.index) or "") == FAM(reg)):
                uses.append("%08X %s %s (+%#x mod A0 = %#x, w%d)" % (y.address, y.mnemonic, y.op_str, op.mem.disp, op.mem.disp % 0xA0, op.size))
        if y.mnemonic in ("ret", "jmp"): break
        try:
            _, w = y.regs_access()
        except capstone.CsError:
            w = []
        if any(FAM(tk.md.reg_name(r)) == FAM(reg) for r in w):
            if y.operands and y.operands[0].type == X86_OP_REG and y.mnemonic in ("mov", "lea", "add", "imul", "movsxd"):
                uses.append("%08X %s %s (register redefined/derived)" % (y.address, y.mnemonic, y.op_str))
            break
    print("%08X %s %s  in %s" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address)))
    for u in uses[:8]: print("    " + u)
