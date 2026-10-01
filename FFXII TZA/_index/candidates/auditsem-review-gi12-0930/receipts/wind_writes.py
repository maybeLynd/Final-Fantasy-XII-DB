"""SWE2-AUDIT-SEM: aligned re-decode of every rip reference to 02CA4380..02CA43A0 from its .pdata function root,
classifying each as READ or WRITE, to name the writers of the map-wind block."""
import sys, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\bucket0930")
import img, wrappers as W
sites = [int(l[:8], 16) for l in open("ripref_wind.out.txt") if "->" in l]
roots = sorted({W.root(s) for s in sites})
WR = ("mov","movss","movsd","movups","movaps","movd","movq","add","sub","or","and","inc","dec","xchg","stosd")
writers = {}
for r in roots:
    hi = max(s for s in sites if W.root(s) == r) + 16
    for ins in img.md.disasm(img.rd(r, hi - r), r):
        if "rip" not in ins.op_str:
            continue
        m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", ins.op_str)
        t = ins.address + ins.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if 0x02CA4380 <= t < 0x02CA43A0:
            ops = [o.strip() for o in ins.op_str.split(",")]
            w = ins.mnemonic in WR and "ptr [rip" in ops[0]
            print("%s %08X in %08X  %s %s  -> %08X" % ("WRITE" if w else "read ", ins.address, r, ins.mnemonic, ins.op_str, t))
            if w:
                writers.setdefault(r, []).append(t)
print("writer functions:", {"%08X" % k: sorted({"%08X" % x for x in v}) for k, v in writers.items()})
