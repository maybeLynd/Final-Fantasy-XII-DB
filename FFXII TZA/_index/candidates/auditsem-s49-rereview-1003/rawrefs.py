"""Function-list-independent reference scan of .text for one data address: rip-relative (any instruction whose
decoded rip operand lands in [T, T+W)), image-base-relative disp32 (T-0x120000 with a non-rip base) and abs64.
Prints each site with its instruction and an R/W/lea classification.  usage: rawrefs.py HEXADDR [width]"""
import struct, sys
sys.path.insert(0, r'C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts')
import retool
R = retool.R
T = int(sys.argv[1], 16)
W = int(sys.argv[2]) if len(sys.argv) > 2 else 4
LO, HI = 0x121000, 0x8C1800
blob = R.at(LO, HI - LO)
hits = {}
for p in range(0, len(blob) - 4):
    disp = struct.unpack_from('<i', blob, p)[0]
    va = LO + p
    ok = False
    for k in (0, 1, 2, 4):
        if T - 8 <= va + 4 + k + disp < T + W:
            ok = True
            break
    ibr = (T - 0x120000 - 8) <= disp < (T - 0x120000 + W)
    if not (ok or ibr):
        continue
    for back in range(1, 11):
        s = va - back
        try:
            i = next(iter(R.md.disasm(R.at(s, 16), s)))
        except StopIteration:
            continue
        if not (i.address < va < i.address + i.size):
            continue
        for k, op in enumerate(i.operands):
            if op.type == 3:
                if op.mem.base == retool.RIP:
                    g = i.address + i.size + op.mem.disp
                elif op.mem.base != 0 and op.mem.disp == disp:
                    g = 0x120000 + op.mem.disp if ibr else None
                else:
                    g = None
                if g is not None and T <= g < T + W:
                    kind = 'lea' if i.mnemonic == 'lea' else ('W' if k == 0 and i.mnemonic not in ('cmp', 'test', 'push', 'bt') else 'R')
                    if i.mnemonic in ('inc', 'dec', 'add', 'sub', 'xadd') and k == 0:
                        kind = 'RW'
                    hits[i.address] = (kind, '%s %s' % (i.mnemonic, i.op_str), 'base=%s' % ('rip' if op.mem.base == retool.RIP else 'reg'))
# abs64
for p in range(0, len(blob) - 8):
    v = struct.unpack_from('<Q', blob, p)[0]
    if T <= v < T + W:
        hits.setdefault(LO + p, ('abs64', 'raw qword', ''))
sz = retool.sizes()
for a in sorted(hits):
    f = retool.func_of(a, sz)
    print('%08X %-5s %-45s %s fn=%s' % (a, hits[a][0], hits[a][1], hits[a][2], ('%08X' % f) if f else 'UNLISTED'))
from collections import Counter
print('total', len(hits), Counter(v[0] for v in hits.values()))
