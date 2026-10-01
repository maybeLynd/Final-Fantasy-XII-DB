"""SWE2-AUDIT-SEM: for every rip read of the class-13 descriptor slots 02EBF078..02EBF090 (and neighbours 02EBF070/98),
the next 12 instructions: flag any store whose address register is the register the slot pointer was loaded into."""
import sys, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\bucket0930")
import img
sites = [int(l[:8], 16) for l in open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\rtrule0930\ripref_slots.out.txt") if "->" in l]
WR = ("mov","add","sub","or","and","inc","dec","xchg","movdqu","movups","movq","movd","xor")
n = flagged = 0
for a in sites:
    seq = list(img.md.disasm(img.rd(a - 1, 200), a - 1))[:13]
    ins0 = seq[0]
    ops = [o.strip() for o in ins0.op_str.split(",")]
    if ins0.mnemonic != "mov" or "ptr" in ops[0]:
        print("   (not a load) %08X %s %s" % (ins0.address, ins0.mnemonic, ins0.op_str)); continue
    reg = ops[0]
    n += 1
    for ins in seq[1:]:
        o = [x.strip() for x in ins.op_str.split(",")]
        if ins.mnemonic in WR and o and "ptr [" in o[0] and reg in o[0]:
            flagged += 1
            print("STORE via slot pointer: %08X %s %s   (loaded at %08X into %s)" % (ins.address, ins.mnemonic, ins.op_str, ins0.address, reg))
        if o and o[0] == reg and ins.mnemonic in ("mov", "lea", "xor", "pop"):
            break
print("slot loads examined:", n, " stores through the loaded pointer:", flagged)
