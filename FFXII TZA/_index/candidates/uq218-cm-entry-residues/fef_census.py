"""@FEF census: header shape, EFX0010 magic, the EFX file's own size field, and where the entry sits.
Also: does any dword in the file equal the EFX file offset (FEF+0x30) - a candidate for the offset
00409FE0 reads at 0040A16F and hands to 003B38B0 (source, offset)."""
import struct, os, collections
from lib import *
C = collections.Counter
r = collections.defaultdict(C); ex = collections.defaultdict(list)
for p in cm_files():
    d, es = cm_entries(p)
    base = os.path.basename(p)[:-3]
    dr = p.replace('\\', '/').split('/in/')[1].split('/')[0]
    tags = [t for t, o in es]
    fefs = [(t, o) for t, o in es if t == '@FEF']
    if not fefs:
        continue
    r['files_by_dir'][dr] += 1
    r['fef_per_file'][len(fefs)] += 1
    r['position (index in entry table, n entries)'][(tags.index('@FEF'), len(tags))] += 1
    r['is last entry'][tags[-1] == '@FEF'] += 1
    for t, o in fefs:
        e = entry(d, o)
        kind, elen, f0c = struct.unpack_from('<III', e, 4)
        name = e[0x10:0x30].split(b'\0')[0].decode('latin1')
        r['kind'][kind] += 1
        r['+0x0C'][f0c] += 1
        r['name==basename'][name == base] += 1
        r['+0x10..+0x2F past name all zero'][all(x == 0 for x in e[0x10 + len(name):0x30])] += 1
        magic = e[0x30:0x38]
        r['magic@+0x30'][magic] += 1
        f38 = struct.unpack_from('<f', e, 0x38)[0]
        sz = struct.unpack_from('<I', e, 0x3C)[0]
        r['f32@+0x38'][f38] += 1
        r['u32@+0x3C == entryLen-0x30'][sz == elen - 0x30] += 1
        if sz != elen - 0x30 and len(ex['size']) < 6:
            ex['size'].append((base, hex(sz), hex(elen)))
        r['entry ends at file end'][o + elen == len(d)] += 1
        # entry alignment
        r['entry offset % 0x40'][o % 0x40] += 1
        efx = o + 0x30
        hits = [i for i in range(0, len(d) - 3, 4) if struct.unpack_from('<I', d, i)[0] == efx]
        r['dwords equal to EFX file offset'][len(hits)] += 1
        if len(ex['hits']) < 6:
            ex['hits'].append((base, hex(o), [hex(h) for h in hits[:4]], hex(len(d))))
        # second-level: EFX header words
        w = struct.unpack_from('<8I', e, 0x40)
        r['EFX +0x10 dword'][w[0]] += 1
for k, v in r.items():
    print(k, sorted(v.items(), key=lambda kv: -kv[1])[:12])
for k, v in ex.items():
    print('ex', k, v)
