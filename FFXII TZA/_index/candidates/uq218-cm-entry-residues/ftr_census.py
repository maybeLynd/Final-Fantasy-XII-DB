"""@FTR node records: the link field as PARENT index (00372B15..00372B99: stored at runtime +0x270,
threaded as first-child +0x274 / next-sibling +0x272), and the aux pool vocabulary by flag bit.

Authored: index table at +0x40 ((recOff<<12)|ordinal), record {u32 link, u32 flags, u16 stream...}.
Checks: parent == -1 count per file; parent < own index (topological order); parent < count;
record 0 is a root. Aux pool: which u16 indices the flag bits select (u32 vs f32 use)."""
import struct, os, collections
from lib import *
C = collections.Counter
r = collections.defaultdict(C); ex = collections.defaultdict(list)
maxtail = 0
for p in cm_files():
    d, es = cm_entries(p)
    base = os.path.basename(p)[:-3]
    t = {a: b for a, b in es}
    e = entry(d, t['@FTR'])
    n, n2, aux, tail = struct.unpack_from('<I', e, 0xC)[0], *struct.unpack_from('<III', e, 0x30)
    maxtail = max(maxtail, tail)
    roots = 0
    for i in range(n):
        ix = struct.unpack_from('<I', e, 0x40 + 4 * i)[0]
        ro = ix >> 12
        link, flags = struct.unpack_from('<II', e, ro)
        par = -1 if (link & 0xFFF000) == 0xFFF000 else (link >> 12) & 0xFFF
        r['link low 12 bits'][link & 0xFFF == 0] += 1
        r['link bits 24-31'][link >> 24] += 1
        if par == -1:
            roots += 1
            r['root index'][i] += 1
        else:
            r['parent < own index'][par < i] += 1
            r['parent < count'][par < n] += 1
            if par >= i and len(ex['par']) < 6:
                ex['par'].append((base, i, par))
        r['flag bits'][hex(flags & 0xFFFFFF00)] += 1
        r['flag low byte'][flags & 0xFF] += 1
    r['roots per file'][roots] += 1
    r['count'][min(n, 999)] += 0
    r['nodes total'][0] += n
print('max FTR +0x38', maxtail)
for k, v in r.items():
    print(k, sorted(v.items(), key=lambda kv: -kv[1])[:16])
for k, v in ex.items():
    print('ex', k, v)
