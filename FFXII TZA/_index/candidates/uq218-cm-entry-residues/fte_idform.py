"""FTE texture id (+0x1C) composition census: top byte by directory; low nibble vs record index;
middle 20 bits vs the file number."""
import struct, os, collections, re
from lib import *
C = collections.Counter
top = C(); low = C(); mid = C(); ex = collections.defaultdict(list)
for p in cm_files():
    d, es = cm_entries(p)
    base = os.path.basename(p)[:-3]
    dr = p.replace('\\', '/').split('/in/')[1].split('/')[0]
    tags = {t: o for t, o in es}
    if '@FTE' not in tags:
        continue
    e = entry(d, tags['@FTE'])
    n = struct.unpack_from('<I', e, 0xC)[0]
    m = re.match(r'([a-z]+)(\d+)(?:_(\d+))?', base)
    num = int(m.group(2))
    for i in range(n):
        tid = struct.unpack_from('<I', e, 0x40 + i * 0x20 + 0x1C)[0]
        tb = tid >> 24
        top[(dr, m.group(1), hex(tb), chr(tb) if 0x20 < tb < 0x7f else '')] += 1
        low[(tid & 0xF) == i] += 1
        md = (tid >> 4) & 0xFFFFF
        k = ('mid==filenum', md == num)
        mid[(dr, k[1])] += 1
        if md != num and len(ex[dr]) < 4:
            ex[dr].append((base, i, hex(tid), md))
print('top byte by (dir, prefix):')
for k, v in sorted(top.items()):
    print('  ', k, v)
print('low nibble == record index:', dict(low))
print('mid 20 bits == file number, by dir:', sorted(mid.items()))
for k, v in ex.items():
    print('  ex', k, v)
