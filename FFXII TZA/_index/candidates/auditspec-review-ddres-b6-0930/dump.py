"""dump.py FUNC [FUNC ...] - decode each .pdata function (all chained ranges), rip targets resolved. Or A-B for a span."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ind as I  # noqa: E402

for arg in sys.argv[1:]:
    if "-" in arg:
        a, b = (int(x, 16) for x in arg.split("-"))
        seq = I.dis(a, b)
        print("=== span %08X-%08X" % (a, b))
    else:
        f = int(arg, 16)
        r = I.func_of(f)
        print("=== %08X root %s ranges %s" % (f, "%08X" % r if r else None,
                                            [("%08X" % x, "%08X" % y) for x, y in I.RANGES.get(r, [])]))
        seq = I.body(r)
    for i in seq:
        s = "%08X  %-8s %s" % (i.address, i.mnemonic, i.op_str)
        for _, op in I.mem_ops(i):
            if op.mem.base == I.X86_REG_RIP:
                s += "   ; -> %08X" % (i.address + i.size + op.mem.disp)
        print(s)
