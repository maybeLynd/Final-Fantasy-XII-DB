"""Re-measure menumap_location.bin under the layout the native accessors use:
record = u8 countA,countB,countC,countD | A[24]*countA | B[24]*countB | C[20]*countC | 8-byte block | D[4]*countD
(003BF430: A at rec+4, B at rec+4+24*countA; 003BFF20 / 003C1070: C at rec+4+24*(A+B), D at C+20*countC+8)."""
import sys, struct, collections, hashlib
sys.path.insert(0, r'C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools')
import vbfextract as V
VBF = r'D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf'
f = open(VBF, 'rb'); names, blocks = V.load_index(f)
ps = sorted(p for p in names if p.replace('\\', '/').lower().endswith('menumap_location.bin'))
H = lambda b, o: struct.unpack_from('<H', b, o)[0]

def walk(b):
    cnt = b[9]; offs = [H(b, 0xA + 2 * i) for i in range(cnt)]
    recs = []
    for i, r in enumerate(offs):
        A, Bn, C, D = b[r:r + 4]
        a0 = r + 4; b0 = a0 + 24 * A; c0 = b0 + 24 * Bn; g = c0 + 20 * C; d0 = g + 8
        end = offs[i + 1] if i + 1 < cnt else len(b)
        recs.append(dict(r=r, A=A, B=Bn, C=C, D=D, a0=a0, b0=b0, c0=c0, g=g, d0=d0, ok=(d0 + 4 * D == end)))
    return recs

for p in ps:
    b = V.read_entry(f, names, blocks, p)
    recs = walk(b)
    print(p.split('/')[-3], len(b), 'records', len(recs), 'walk ok', sum(x['ok'] for x in recs), 'sha', hashlib.sha256(b).hexdigest()[:8])

b = V.read_entry(f, names, blocks, [p for p in ps if '/us/' in p][0])
recs = walk(b)
tot = collections.Counter(); hit = collections.Counter()
g = collections.Counter(); zeroA = 0
def ids_of(x):  # A ids at native +12
    return {H(b, x['a0'] + 24 * e + 12) for e in range(x['A'])}
for i, x in enumerate(recs):
    own = ids_of(x); nxt = ids_of(recs[(i + 1) % len(recs)])
    if x['A'] == 0: zeroA += 1
    g[b[x['g']:x['g'] + 8].hex(' ')] += 1
    for kind, base, n, stride in (('A', x['a0'], x['A'], 24), ('B', x['b0'], x['B'], 24), ('C', x['c0'], x['C'], 20), ('D', x['d0'], x['D'], 4)):
        for e in range(n):
            o = base + stride * e
            tot[kind] += 1
            for off in range(0, stride - 1, 2):
                v = H(b, o + off)
                if v == 0xFFFF: hit[(kind, off, 'FFFF')] += 1
                if v in own and v: hit[(kind, off, 'own-id')] += 1
                if v in nxt and v and v not in own: hit[(kind, off, 'next-only')] += 1
print('entries', dict(tot), 'records with countA 0:', zeroA)
for kind in 'ABCD':
    row = []
    for off in range(0, 24, 2):
        for t in ('FFFF', 'own-id', 'next-only'):
            if hit[(kind, off, t)]: row.append('+%d %s %d' % (off, t, hit[(kind, off, t)]))
    print(kind, '/', tot[kind], ':', '; '.join(row))
print('8-byte block values', g.most_common())
# A/B +0,+2 ranges (coordinate-shaped?)
for kind in ('A', 'B'):
    xs = []; ys = []
    for x in recs:
        base = x['a0'] if kind == 'A' else x['b0']
        for e in range(x[kind]):
            xs.append(H(b, base + 24 * e)); ys.append(H(b, base + 24 * e + 2))
    print(kind, '+0 range', min(xs), max(xs), '+2 range', min(ys), max(ys))
print('record 0 C[0..2] native +0,+2:', [(H(b, recs[0]['c0'] + 20 * e), H(b, recs[0]['c0'] + 20 * e + 2)) for e in range(3)])
print('record 0 A ids +12:', [H(b, recs[0]['a0'] + 24 * e + 12) for e in range(recs[0]['A'])])
print('--- native per-offset profile (us)')
for kind, stride in (('A', 24), ('B', 24), ('C', 20), ('D', 4)):
    for off in range(0, stride, 2):
        vals = []
        for x in recs:
            base = {'A': x['a0'], 'B': x['b0'], 'C': x['c0'], 'D': x['d0']}[kind]
            for e in range(x[kind]): vals.append(H(b, base + stride * e + off))
        z = sum(v == 0 for v in vals); ff = sum(v == 0xFFFF for v in vals)
        nz = [v for v in vals if v not in (0, 0xFFFF)]
        print(kind, '+%d' % off, 'zero', z, 'FFFF', ff, 'other range', (min(nz), max(nz)) if nz else '-', 'distinct', len(set(vals)))
print('records with countB>=1 and countC>=1:', sum(1 for x in recs if x['B'] and x['C']))
# page C+12 (native next C +0) misses = 44? count C entries that are last in record
print('C entries that are last in their record (page +12 reads the block):', sum(1 for x in recs if x['C']))
