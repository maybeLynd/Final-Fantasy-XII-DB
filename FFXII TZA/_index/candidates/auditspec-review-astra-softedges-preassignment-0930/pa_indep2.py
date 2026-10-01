"""SWE2-AUDIT-SPEC preassignment review, part 2:
(a) 00632960 stores of its arg5 (native offset) and owner (+0x18);
(b) every branch in 0059C700 whose target lies in [0059CC38, 0059CD14] and whose source is outside it (re-entry that
    could bypass the r13 zero), and every branch from >= 0059CD14 back into that window;
(c) where 0060F3D0 and 0060F280 are referenced (rip-relative lea/mov, relocated qwords) - callback identity premise."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, r"..\..\..\..\Tools\work\FABLE\takebacks"))
import tk
print("== 00632960 stores")
for x in tk.fdis(0x00632960):
    if x.mnemonic == "mov" and x.op_str.startswith(("qword ptr [rcx", "dword ptr [rcx", "qword ptr [rbx", "dword ptr [rbx", "qword ptr [rdi", "dword ptr [rdi")) or "rsp + 0x" in x.op_str and x.mnemonic == "mov" and x.address < 0x00632990:
        print("  %08X %-6s %s" % (x.address, x.mnemonic, x.op_str))
ins = list(tk.fdis(0x0059C700))
LO, HI = 0x0059CC38, 0x0059CD14
print("== branches into (%08X, %08X] from outside" % (LO, HI))
for x in ins:
    if x.mnemonic.startswith("j") and x.op_str.startswith("0x"):
        t = int(x.op_str, 16)
        if LO < t <= HI and not (LO <= x.address <= HI):
            print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("== indirect jumps in 0059C700:", [("%08X" % x.address, x.op_str) for x in ins if x.mnemonic == "jmp" and not x.op_str.startswith("0x")])
for t in (0x0060F3D0, 0x0060F280):
    rr, raw = tk.rip_refs(t, t + 1)
    print("rip refs -> %08X:" % t, [("%08X" % h[0].address, h[0].mnemonic, tk.fname(h[0].address)) for h in rr])
    print("reloc qwords -> %08X:" % t, ["%08X" % a if isinstance(a, int) else a for a in tk.reloc_ptrs(t, t + 1)][:10])
