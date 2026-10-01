import sys, struct
sys.path.insert(0, r'C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools')
import vbfextract as V
f = open(r'D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf', 'rb'); names, blocks = V.load_index(f)
H = lambda b, o: struct.unpack_from('<H', b, o)[0]
get = lambda s: V.read_entry(f, names, blocks, [p for p in names if p.lower().endswith(s)][0])
mr = get('ch/common/map_ref.bin'); base = struct.unpack_from('<i', mr, 4)[0]
print('map_ref size', len(mr), 'hdr', mr[:8].hex(' '), 'rows', (len(mr) - base) // 8)
for loc in ('us', 'de', 'it'):
    lm = get(loc + '/worldmap/menumap_location.bin'); cm = get(loc + '/worldmap/menumap_common.bin')
    o = H(cm, 8); groups = [cm[o + 4 + 8 * i] for i in range(struct.unpack_from('<I', cm, o)[0])]
    same = nxt = seven = tot = dsame = dnxt = dtot = 0
    for i in range(lm[9]):
        r = H(lm, 0xA + 2 * i); A, B, C, D = lm[r:r + 4]
        for e in range(A):
            g = H(mr, base + 8 * H(lm, r + 4 + 24 * e + 12) + 6); tot += 1
            same += g == groups[i]; nxt += g == groups[(i + 1) % 48]; seven += g == groups[(i + 7) % 48]
        d0 = r + 4 + 24 * (A + B) + 20 * C + 8
        for e in range(D):
            g = H(mr, base + 8 * H(lm, d0 + 4 * e + 2) + 6); dtot += 1
            dsame += g == groups[i]; dnxt += g == groups[(i + 1) % 48]
    print(loc, 'A same', same, '/', tot, 'ctl next', nxt, 'ctl +7', seven, '| D+2 same', dsame, '/', dtot, 'ctl next', dnxt)
