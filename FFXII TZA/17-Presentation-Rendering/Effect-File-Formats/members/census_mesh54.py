"""Kind-0x54 effect mesh record census + element-type-0x05 slot usage.

Loader model (00436D00, verified against disassembly):
  record stream entry: {u16 key, u8 kind, u8 sub} at chunk+0xC, payload at chunk+0x10
  payload: u8 flags @0, pad @1, then 8 u16 counts @2..+0x10
    +2  tri      -> +0x10
    +4  quad     -> +0x12
    +6  c14      -> +0x14 positions, 16B each, w forced 1.0
    +8  c16      -> +0x16 vectors, 16B each
    +0xA c18     -> +0x18 4-byte entries
    +0xC c1A     -> +0x1A 8-byte entries
    +0xE c1C     -> +0x1C id bytes -> kind-0x52 handles
    +0x10 c1E    -> +0x1E 20-byte inline records (capacity 0x140 = 16)
  arrays in order: pos, vec, 4B, 8B, 20B, [if flags&1: idx1, idx2 of
  (6*tri + 8*quad) bytes each], (tri+quad) prim bytes, c1C id bytes.
  Payload is padded so the record stream stays 16-byte aligned.
"""
import struct, glob, os, math, sys
from collections import Counter, defaultdict

ROOT = r'Database/Tools/work/DATA/mesh54/fx_all'
OUT = os.path.dirname(os.path.abspath(__file__))


def f32(b):
    return struct.unpack('<f', b)[0]


def main():
    files = sorted(glob.glob(ROOT + '/**/*.*', recursive=True))
    files = [p for p in files if p.lower().endswith(('.efx', '.efb'))]
    rows = []          # per 0x54 record
    bad_records = []   # size-control failures
    el05 = []          # (file, chunk_off, chunk_type, nslots_filled, mode, ids)
    el_types = Counter()
    el800_sub = Counter()
    link_ok = link_noids = link_partial = 0
    chunk_types = Counter()
    kind_hist = Counter()
    files_with_54 = set()
    files_seen = 0
    padvals = Counter()

    for path in files:
        d = open(path, 'rb').read()
        rel = os.path.relpath(path, ROOT).replace('\\', '/')
        files_seen += 1
        subs54 = set()
        file_el05 = []
        cur = 0x10
        while cur + 8 <= len(d):
            ln, flag, typ = struct.unpack('<IHH', d[cur:cur + 8])
            if ln < 8 or cur + ln > len(d):
                break
            if flag == 0x100:
                chunk_types[typ] += 1
                if typ == 0xB00:
                    # record stream: u32 streamLen @+8, records @+0xC
                    key, kind, sub = struct.unpack('<HBB', d[cur + 0xC:cur + 0x10])
                    kind_hist[kind] += 1
                    if kind == 0x54 and key == 0:
                        subs54.add(sub)
                    if kind == 0x54:
                        files_with_54.add(rel)
                        p = d[cur + 0x10:cur + ln]
                        flags = p[0]
                        tri, quad, c14, c16, c18, c1A, c1C, c1E = \
                            struct.unpack('<8H', p[2:0x12])
                        size = (0x12 + 16 * c14 + 16 * c16 + 4 * c18
                                + 8 * c1A + 20 * c1E)
                        if flags & 1:
                            size += 2 * (6 * tri + 8 * quad)
                        size += (tri + quad) + c1C
                        avail = len(p)
                        diff = avail - size
                        ok = 0 <= diff < 16 and (size + diff) % 16 == 0
                        padvals[diff] += 1
                        if not ok:
                            bad_records.append((rel, hex(cur), size, avail))
                        rows.append((rel, cur, key, sub, flags, tri, quad,
                                     c14, c16, c18, c1A, c1C, c1E, size,
                                     avail, ok, p))
                elif typ == 0x800:
                    # 0x800 handler 003A9730: publishes chunk+0x10 into the
                    # 320-slot table via 02EBEF90; +0xE is the sub-record
                    # SUBTYPE (bounded <=8 by the 00442460 rebase ladder).
                    # Different record class from elements.
                    el800_sub[d[cur + 0xE]] += 1
                elif typ == 0xA00:
                    # 0xA00 handler 003A9A70: publishes chunk+0x10 into the
                    # 768-slot table via 02EBEF78; +0xE is the element TYPE
                    # byte (0..0xD1). The published record is the element:
                    # +0x570 = 32 authored slot id bytes, +0x590 = mode byte,
                    # +0x5A0 = 32 resolved handles (setup 00538DB0, walk
                    # 00449AB0). Ids resolve via 003AA280(key=0, kind=0x54,
                    # sub=id).
                    et = d[cur + 0xE]
                    el_types[et] += 1
                    if et == 0x05:
                        rec = d[cur + 0x10:cur + ln]
                        ids = rec[0x570:0x590]
                        filled = sum(1 for b in ids if b)
                        file_el05.append((rel, cur, typ, filled,
                                          rec[0x590], ids))
            cur += ln
        # per-file linkage: element slot ids -> same-file kind-0x54 subs
        for e in file_el05:
            ids = [b for b in e[5] if b]
            if not ids:
                link_noids += 1
            elif all(b in subs54 for b in ids):
                link_ok += 1
            else:
                link_partial += 1
        el05.extend(file_el05)

    # ---- write per-record TSV ----
    with open(os.path.join(OUT, 'mesh54-records.tsv'), 'w') as f:
        f.write('file\toffset\tkey\tsub\tflags\ttri\tquad\tc14\tc16\tc18'
                '\tc1A\tc1C\tc1E\tsize\tavail\tok\n')
        for r in rows:
            f.write('%s\t0x%x\t0x%04x\t0x%02x\t0x%02x\t%d\t%d\t%d\t%d\t%d'
                    '\t%d\t%d\t%d\t%d\t%d\t%d\n'
                    % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7],
                       r[8], r[9], r[10], r[11], r[12], r[13], r[14],
                       1 if r[15] else 0))

    # ---- element type-0x05 TSV ----
    with open(os.path.join(OUT, 'mesh54-element05.tsv'), 'w') as f:
        f.write('file\tchunk_off\tchunk_type\tslots_filled\tmode_0x590\tids\n')
        for e in el05:
            f.write('%s\t0x%x\t0x%x\t%d\t0x%02x\t%s\n'
                    % (e[0], e[1], e[2], e[3], e[4] & 0xFF, e[5].hex()))

    # ---- aggregate stats ----
    print('files seen:', files_seen)
    print('files with kind-0x54 records:', len(files_with_54))
    print('kind-0x54 records:', len(rows))
    print('size control: exact-fit-16-aligned =',
          sum(1 for r in rows if r[15]), ' bad =', len(bad_records))
    print('pad histogram:', dict(sorted(padvals.items())))
    print('record-kind histogram (0xB00 first records):',
          {hex(k): v for k, v in sorted(kind_hist.items())})
    print('chunk types (flag 0x100):',
          {hex(k): v for k, v in sorted(chunk_types.items())})

    # +0x16 vs +0x14, +0x18 vs +0x1A
    diff_16 = [(r[0], hex(r[1]), r[7], r[8]) for r in rows if r[8] != r[7]]
    diff_1A = [(r[0], hex(r[1]), r[9], r[10]) for r in rows if r[10] != r[9]]
    print('records with c16 != c14:', len(diff_16))
    for t in diff_16[:20]: print('  ', t)
    print('records with c1A != c18:', len(diff_1A))
    for t in diff_1A[:20]: print('  ', t)

    # max c1E vs capacity 16 (0x140/20)
    mx = max(r[12] for r in rows)
    over = [r for r in rows if r[12] > 16]
    print('max c1E (inline 20B records):', mx,
          ' capacity 16; over-capacity records:', len(over))

    # flags distribution
    print('flags histogram:', dict(Counter(r[4] for r in rows)))
    print('sub histogram:', dict(Counter(r[3] for r in rows)))

    # ---- value distributions ----
    # +0x24 (c16 x 16B vectors): unit-length normals?
    # +0x28 (c18 x 4B): byte quads / colours?
    # +0x2C (c1A x 8B): float pairs / UVs?
    vec_unit = vec_nonunit = vec_zero = 0
    vec_w = Counter()
    q4 = Counter()
    q4_alpha = Counter()
    uv_range = Counter()
    uv_nan = 0
    pos_w = Counter()
    for r in rows:
        p = r[16]
        flags = r[4]
        tri, quad, c14, c16, c18, c1A, c1C, c1E = r[5:13]
        o = 0x12
        pos = p[o:o + 16 * c14]; o += 16 * c14
        for i in range(c14):
            pos_w[pos[i * 16 + 12:i * 16 + 16]] += 1
        vec = p[o:o + 16 * c16]; o += 16 * c16
        for i in range(c16):
            x, y, z, w = struct.unpack('<4f', vec[i * 16:i * 16 + 16])
            n = x * x + y * y + z * z
            if n == 0:
                vec_zero += 1
            elif abs(n - 1.0) < 1e-3:
                vec_unit += 1
            else:
                vec_nonunit += 1
            vec_w[vec[i * 16 + 12:i * 16 + 16]] += 1
        b4 = p[o:o + 4 * c18]; o += 4 * c18
        for i in range(c18):
            q = b4[i * 4:i * 4 + 4]
            q4[q] += 1
            q4_alpha[q[3]] += 1
        b8 = p[o:o + 8 * c1A]; o += 8 * c1A
        for i in range(c1A):
            u, v = struct.unpack('<2f', b8[i * 8:i * 8 + 8])
            if math.isnan(u) or math.isnan(v):
                uv_nan += 1
                continue
            for t in (u, v):
                if 0.0 <= t <= 1.0: uv_range['0..1'] += 1
                elif -1.0 <= t <= 2.0: uv_range['-1..2'] += 1
                elif abs(t) < 1e6: uv_range['large-float'] += 1
                else: uv_range['huge'] += 1
        o += 20 * c1E
        if flags & 1:
            o += 2 * (6 * tri + 8 * quad)
        o += tri + quad + c1C

    print()
    print('--- +0x24 vector stats (c16 entries, 16B each) ---')
    print('unit-length:', vec_unit, ' non-unit:', vec_nonunit,
          ' zero:', vec_zero)
    print('w-field top:', [(k.hex(), v) for k, v in vec_w.most_common(8)])
    print('--- +0x20 position w-field (file-side, before loader forces 1.0) ---')
    print([(k.hex(), v) for k, v in pos_w.most_common(8)])
    print('--- +0x28 4-byte entries ---')
    print('distinct:', len(q4), ' top:', [(k.hex(), v) for k, v in q4.most_common(10)])
    print('byte-3 (alpha?) histogram top:', dict(q4_alpha.most_common(10)))
    print('--- +0x2C 8-byte entries (float pairs) ---')
    print(uv_range, 'nan:', uv_nan)

    # ---- element 0x05 summary ----
    print()
    print('--- element type-0x05 (0xA00 chunks only; +0xE = type) ---')
    print('0x800 sub-record subtype histogram:',
          {hex(k): v for k, v in sorted(el800_sub.items())})
    print('element type histogram (0xA00):', {hex(k): v for k, v in
                                            sorted(el_types.items())})
    f05 = sorted(set(e[0] for e in el05))
    print('files using element type 0x05:', len(f05))
    print('type-0x05 elements:', len(el05))
    print('slots-filled histogram (of 32):',
          dict(sorted(Counter(e[3] for e in el05).items())))
    print('mode byte +0x590 histogram:',
          dict(sorted(Counter(e[4] & 0xFF for e in el05).items())))
    print('id->same-file kind-0x54-sub linkage: all-match =', link_ok,
          ' no-ids =', link_noids, ' partial =', link_partial)
    print('id byte histogram:', dict(sorted(
        Counter(b for e in el05 for b in e[5] if b).items())))
    for e in el05[:15]:
        print('  ', e[0], hex(e[1]), 'type 0x%04x' % e[2],
              'slots', e[3], 'mode 0x%02x' % (e[4] & 0xFF))
    for b in bad_records[:10]:
        print('BAD', b)


if __name__ == '__main__':
    main()
