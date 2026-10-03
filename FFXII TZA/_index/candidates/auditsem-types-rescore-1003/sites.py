"""Print the instruction at each named site, decoded from its function's start (aligned)."""
import sys
sys.path.insert(0, r'C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts')
import retool
R = retool.R
sz = retool.sizes()
for s in sys.argv[1:]:
    a = int(s, 16)
    f = retool.func_of(a, sz)
    if f is None:
        print(s, 'UNLISTED'); continue
    for i in R.md.disasm(R.at(f, a - f + 16), f):
        if i.address == a:
            g = ''
            for op in i.operands:
                if op.type == 3 and op.mem.base == retool.RIP:
                    g = ' -> %08X' % (i.address + i.size + op.mem.disp)
            print('%08X %s %s%s  (fn %08X)' % (a, i.mnemonic, i.op_str, g, f))
            break
        if i.address > a:
            print(s, 'not an instruction boundary'); break
