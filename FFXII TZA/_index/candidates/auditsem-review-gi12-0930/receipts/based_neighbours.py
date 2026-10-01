"""SWE2-AUDIT-SEM: for each lea of a base in 02B59C00..02B59D60, follow the loaded register (40 instrs, or until it is
redefined) and print every memory operand through it with the absolute address it names; flag any that land on
02B59D60..02B59D64 and whether that access is a store. Callees receiving the base in rcx/rdx are listed for follow-up."""
import sys, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\bucket0930")
import img
R32 = {"eax":"rax","ebx":"rbx","ecx":"rcx","edx":"rdx","esi":"rsi","edi":"rdi","ebp":"rbp"}
sites = []
for l in open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\gi120930\ripref_below_4k.out.txt"):
    m = re.match(r"([0-9A-F]{8})\s+lea (\w+), .*-> ([0-9A-F]{8})", l)
    if m and int(m.group(3), 16) >= 0x02B59C00:
        sites.append((int(m.group(1), 16), int(m.group(3), 16)))
WR = ("mov","add","sub","or","and","inc","dec","xchg","movdqu","movups","movaps","movq","movd","xor","movss","movsd")
for a, base in sites:
    seq = list(img.md.disasm(img.rd(a - 1, 400), a - 1))
    reg = seq[0].op_str.split(",")[0].strip()
    print("== %08X %s %s   base %08X" % (seq[0].address, seq[0].mnemonic, seq[0].op_str, base))
    for ins in seq[1:40]:
        ops = [o.strip() for o in ins.op_str.split(",")]
        for k, o in enumerate(ops):
            mm = re.search(r"\[" + reg + r"(?: \+ (0x[0-9a-f]+|\d+))?\]", o)
            if mm:
                disp = int(mm.group(1), 0) if mm.group(1) else 0
                addr = base + disp
                w = k == 0 and ins.mnemonic.split()[0] in WR
                flag = "  <<< 02B59D60" if 0x02B59D60 <= addr < 0x02B59D64 else ""
                print("   %s %08X %s %s   -> %08X%s" % ("W" if w else "R", ins.address, ins.mnemonic, ins.op_str, addr, flag))
        if ins.mnemonic == "call":
            print("   C %08X call %s  (base reg %s live? %s)" % (ins.address, ins.op_str, reg, reg in ("rcx", "rdx", "r8", "r9")))
        if ops and ops[0] == reg and ins.mnemonic in ("mov", "lea", "xor", "pop"):
            break
        if ins.mnemonic in ("ret", "jmp"):
            break
