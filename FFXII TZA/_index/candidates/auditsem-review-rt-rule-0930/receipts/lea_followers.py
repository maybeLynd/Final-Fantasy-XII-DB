"""SWE2-AUDIT-SEM: for each lea of the registry base, the 40 instructions after it (decoded from the REX byte),
flagging any memory store (write) and any operand displacement 0x3c."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\bucket0930")
import img
leas = [0x002FD18C,0x002FD458,0x002FD8E0,0x002FD980,0x0030090D,0x003047F1,0x00309450,0x003097FB,0x00309B87,0x00309EF5,
        0x00309F68,0x0030A00E,0x0030ADF5,0x0030AE65,0x0030B129,0x0030B2A1,0x0030B31C,0x0030B32D,0x0030B410,0x0030B46B,0x0030B6A9]
WR = ("mov","add","sub","or","and","inc","dec","xchg","movdqu","movups","movaps","movq","movd","xor","not","neg","lock")
for a in leas:
    seq = list(img.md.disasm(img.rd(a - 1, 400), a - 1))[:40]
    first = seq[0]
    out = []
    for ins in seq:
        ops = [o.strip() for o in ins.op_str.split(",")]
        w = ins.mnemonic.split()[0] in WR and ops and "ptr [" in ops[0]
        tag = ("W " if w else "  ") + ("3C " if "0x3c" in ins.op_str else "   ")
        out.append("%s%08X %s %s" % (tag, ins.address, ins.mnemonic, ins.op_str))
        if ins.mnemonic in ("ret", "jmp", "int3"):
            break
    print("== LEA %08X: %s %s" % (a - 1, first.mnemonic, first.op_str))
    for o in out:
        if o.startswith("W") or "3C" in o[:5]:
            print("   ", o)
