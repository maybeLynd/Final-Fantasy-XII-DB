"""FTE size fields + cross-file id sharing; FCT id sharing and the 10 short-span records."""
import struct, os, collections, hashlib
from lib import *
C = collections.Counter
rel = C(); ex = []
ids = collections.defaultdict(set)      # id -> set(payload hash)
idfiles = collections.defaultdict(set)
pids = collections.defaultdict(set)
pidfiles = collections.defaultdict(set)
short = []
fct_fte_n = C()
for p in cm_files():
    d, es = cm_entries(p)
    base = os.path.basename(p)[:-3]
    tags = {t: o for t, o in es}
    fte_ids = []
    if '@FTE' in tags:
        e = entry(d, tags['@FTE'])
        n = struct.unpack_from('<I', e, 0xC)[0]
        for i in range(n):
            b0, w, h, fmt, rrw, rrh, dpsm, f10, dbytes, doff, tid = struct.unpack_from('<IHHHHHHIIII', e, 0x40 + i * 0x20)
            bpp = 8 if fmt == 0x13 else 4
            nat = w * h * bpp // 8
            rel[('dbytes==rrw*rrh*4', dbytes == rrw * rrh * 4)] += 1
            rel[('dbytes==w*h*bpp/8', dbytes == nat)] += 1
            rel[('b0%0x2000==0', b0 % 0x2000 == 0)] += 1
            rel[('b0>=dbytes', b0 >= dbytes)] += 1
            rel[('b0==roundup(dbytes,0x2000)', b0 == (dbytes + 0x1FFF) // 0x2000 * 0x2000)] += 1
            rel[('b0==dbytes', b0 == dbytes)] += 1
            rel[('rrw', rrw)] += 1
            if b0 != dbytes and len(ex) < 12:
                ex.append((base, i, hex(fmt), w, h, rrw, rrh, hex(b0), hex(dbytes)))
            h_ = hashlib.md5(e[doff:doff + dbytes]).hexdigest()
            ids[tid].add(h_)
            idfiles[tid].add(base)
            fte_ids.append(tid)
    if '@FCT' in tags:
        e = entry(d, tags['@FCT'])
        n = struct.unpack_from('<I', e, 0xC)[0]
        recs = [struct.unpack_from('<HHBBHII', e, 0x30 + i * 16) for i in range(n)]
        fct_fte_n[(len(fte_ids), n)] += 1
        for i, (gs, clut, rrw, pages, rrh, tid, off) in enumerate(recs):
            nxt = recs[i + 1][6] if i + 1 < n else len(e)
            if nxt - off != 4 * clut:
                short.append((base, i, hex(tid), hex(clut), rrw, rrh, hex(off), hex(nxt - off), [hex(r[5]) for r in recs]))
            pids[tid].add(hashlib.md5(e[off:off + 4 * clut]).hexdigest())
            pidfiles[tid].add(base)
for k, v in sorted(rel.items(), key=str):
    print(k, v)
print('b0 != dbytes examples', ex)
shared = [t for t in idfiles if len(idfiles[t]) > 1]
print('FTE distinct ids', len(ids), 'ids in >1 file', len(shared),
      'of which identical payload in every file', sum(1 for t in shared if len(ids[t]) == 1))
print('  sample shared', [(hex(t), sorted(idfiles[t])[:4], len(ids[t])) for t in shared[:8]])
difs = [t for t in shared if len(ids[t]) > 1]
print('  shared ids with differing payload', len(difs), [(hex(t), sorted(idfiles[t])[:6]) for t in difs[:8]])
pshared = [t for t in pidfiles if len(pidfiles[t]) > 1]
print('FCT distinct ids', len(pids), 'in >1 file', len(pshared), 'identical 4-page payload', sum(1 for t in pshared if len(pids[t]) == 1))
print('FCT short-span records', len(short))
for s in short:
    print('  ', s)
print('(FTE count, FCT count) where differ', sorted(((k, v) for k, v in fct_fte_n.items() if k[0] != k[1]), key=lambda kv: -kv[1])[:20])
