"""Known-answer controls and defect-sensitive mutants for every uq218 instrument. Prints PASS/FAIL per check."""
import struct, os, collections
from lib import *
fails = 0
def check(name, ok, detail=''):
    global fails
    print(('PASS ' if ok else 'FAIL ') + name + ('  ' + str(detail) if detail else ''))
    if not ok:
        fails += 1

# --- exe reader (section-aware): constants the pages cite
check('exe .rdata 008F30E4 == 0.01f', abs(f32(0x008F30E4) - 0.01) < 1e-9, f32(0x008F30E4))
# fdm-and-for-entries.md calls this 9.99e7; the bytes are 20 BC BE 4C = 1.0e8 exactly (first run FAILED on 9.99e7)
check('exe .rdata 00D10824 == 1.0e8f (page says 9.99e7)', rd(0x00D10824, 4) == bytes.fromhex('20bcbe4c'), f32(0x00D10824))
check('exe string 00D122F0 == "chara\\h"', rd(0x00D122F0, 8) == b'chara\\h\x00', rd(0x00D122F0, 8))
check('exe .text 0016D6A0 is ret 0 (C2 00 00)', rd(0x0016D6A0, 3) == b'\xc2\x00\x00', rd(0x0016D6A0, 3).hex())

def load(name):
    p = [f for f in cm_files() if os.path.basename(f) == name + '.cm'][0]
    d, es = cm_entries(p)
    return d, {t: o for t, o in es}

# --- FTE parser: hand-decoded m1283 / g0116 records (hex dumps in notes.md)
d, t = load('m1283')
e = entry(d, t['@FTE'])
rec = struct.unpack_from('<IHHHHHHIIII', e, 0x40)
check('FTE m1283 rec0 known answer', rec == (0x8000, 256, 128, 0x13, 0x80, 0x40, 0, 0, 0x8000, 0x60, 0x6D005030), [hex(x) for x in rec])
d, t = load('g0116')
e = entry(d, t['@FTE'])
recs = [struct.unpack_from('<IHHHHHHIIII', e, 0x40 + i * 0x20) for i in range(3)]
check('FTE g0116 3 records, stride 0x20, dataOff 0xA0/0x80A0/0x100A0', [r[9] for r in recs] == [0xA0, 0x80A0, 0x100A0])
# mutant: stride 0x1C must break contiguity
bad = [struct.unpack_from('<IHHHHHHIIII', e, 0x40 + i * 0x1C) for i in range(3)]
check('FTE mutant stride 0x1C breaks the dataOff chain', [r[9] for r in bad] != [0xA0, 0x80A0, 0x100A0])
# FCT known answer g0116: ids equal FTE ids, pages 4, payload offs 0x60/0x1060/0x2060
f = entry(d, t['@FCT'])
fr = [struct.unpack_from('<HHBBHII', f, 0x30 + i * 16) for i in range(3)]
check('FCT g0116 known answer', [(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in fr] ==
      [(0x2000, 0x400, 16, 4, 16, 0x67000740 + i, 0x60 + 0x1000 * i) for i in range(3)], fr)
# 005044D0 formula control: entry + off + mode*clut ; mode 3 page of rec0 == bytes at 0x60+0xC00
check('FCT 005044D0 formula page3 addr', 0x60 + 3 * 0x400 == 0xC60)
# grey metric sensitivity: planted grey palette vs page0 of g0116 rec0
def greyfrac(b):
    cols = [b[j:j + 4] for j in range(0, len(b), 4)]
    return sum(1 for c in cols if max(c[:3]) - min(c[:3]) <= 8) / len(cols)
planted = bytes(sum(([v, v, v, 0x80] for v in range(256)), []))
check('grey metric: planted grey palette -> 1.0', greyfrac(planted) == 1.0)
g0 = greyfrac(f[0x60:0x460]); g3 = greyfrac(f[0x60 + 0xC00:0x60 + 0x1000])
check('grey metric distinguishes g0116 page0 from page3', g3 > 0.95 and g0 < g3, (round(g0, 3), round(g3, 3)))

# --- FDM/FTR join: mutant (FTR count instead of +0x38) must not match everywhere
same = mut = tot = 0
for p in cm_files():
    dd, es = cm_entries(p)
    tt = {a: b for a, b in es}
    if '@FDM' not in tt:
        continue
    ftr = entry(dd, tt['@FTR']); fdm = entry(dd, tt['@FDM'])
    nk = struct.unpack_from('<I', fdm, struct.unpack_from('<H', fdm, 0x32)[0])[0]
    tot += 1
    same += nk == struct.unpack_from('<I', ftr, 0x38)[0]
    mut += nk == struct.unpack_from('<I', ftr, 0x0C)[0]
check('FDM keys == FTR +0x38 in every FDM file', same == tot, (same, tot))
check('mutant FDM keys == FTR count (+0x0C) is NOT universal', mut < tot, (mut, tot))

# --- FTR parent link: mutant (low 12 bits as parent) must fail the topological test
ok = mbad = n_all = 0
for p in cm_files():
    dd, es = cm_entries(p)
    tt = {a: b for a, b in es}
    e = entry(dd, tt['@FTR'])
    n = struct.unpack_from('<I', e, 0xC)[0]
    for i in range(n):
        ro = struct.unpack_from('<I', e, 0x40 + 4 * i)[0] >> 12
        link = struct.unpack_from('<I', e, ro)[0]
        if (link & 0xFFF000) == 0xFFF000:
            continue
        n_all += 1
        ok += ((link >> 12) & 0xFFF) < i
        mbad += (link & 0xFFF) < i
check('FTR bits 12-23 parent < own index (all non-roots)', ok == n_all, (ok, n_all))
check('mutant: low 12 bits as parent is NOT topological', mbad < n_all, (mbad, n_all))

# --- FEF: negative control - EFX magic absent at +0x30 of @FTE entries
neg = 0
for p in cm_files()[:200]:
    dd, es = cm_entries(p)
    for a, b in es:
        if a == '@FTE' and dd[b + 0x30:b + 0x37] == b'EFX0010':
            neg += 1
check('negative: no @FTE entry carries EFX0010 at +0x30 (first 200 files)', neg == 0)
print('FAILS', fails)
