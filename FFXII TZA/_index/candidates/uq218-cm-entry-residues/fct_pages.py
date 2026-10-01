"""@FCT payload: are the 4 clutBytes-sized pages distinct palettes, and what do they look like?
Per page: fraction of colours that are grey (max-min of RGB <= 8), mean luminance, equality to page 0.
Control: page 0 of a known file vs the same bytes read by the 005044D0 formula with mode 0."""
import struct, os, collections
from lib import *
C = collections.Counter
grey = collections.defaultdict(list); lum = collections.defaultdict(list); sat = collections.defaultdict(list)
eq0 = C(); npal = 0
for p in cm_files():
    d, es = cm_entries(p)
    tags = {t: o for t, o in es}
    if '@FCT' not in tags:
        continue
    e = entry(d, tags['@FCT'])
    n = struct.unpack_from('<I', e, 0xC)[0]
    for i in range(n):
        gs, clut, rrw, pages, rrh, tid, off = struct.unpack_from('<HHBBHII', e, 0x30 + i * 16)
        if off + 4 * clut > len(e):
            continue
        npal += 1
        pg = [e[off + k * clut: off + (k + 1) * clut] for k in range(4)]
        for k in range(4):
            cols = [pg[k][j:j + 4] for j in range(0, clut, 4)]
            g = sum(1 for c in cols if max(c[:3]) - min(c[:3]) <= 8) / len(cols)
            l = sum((c[0] * 299 + c[1] * 587 + c[2] * 114) / 1000 for c in cols) / len(cols)
            s = sum(max(c[:3]) - min(c[:3]) for c in cols) / len(cols)
            grey[k].append(g); lum[k].append(l); sat[k].append(s)
            eq0[(k, pg[k] == pg[0])] += 1
print('palettes measured', npal)
for k in range(4):
    gl = grey[k]
    print('page', k, 'mean grey-fraction %.3f' % (sum(gl) / len(gl)),
          'pages >=0.95 grey', sum(1 for x in gl if x >= 0.95),
          'mean luminance %.1f' % (sum(lum[k]) / len(lum[k])),
          'mean chroma %.1f' % (sum(sat[k]) / len(sat[k])))
print('page == page0:', sorted(eq0.items()))
