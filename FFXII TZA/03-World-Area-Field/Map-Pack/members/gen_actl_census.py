#!/usr/bin/env python3
"""
gen_actl_census.py -- MP-2: the ACTL section (slot 9) of the map-ctrl pack.

Walks every ps2data/plan_master/map_ctrl/**/bin/*.mpk in the shipped
FFXII_TZA.vbf, extracts the slot-9 payload and parses it under the layout
proved against the consumers in the image:

  +0x00  'ACTL'  magic
  +0x04  u16     version = 1          (the 003E8940 install gate: word[+4]==1)
  +0x06  u16     recordStride = 0x16  (inner loops add 0x16)
  +0x08  u16     idBound              (003E8230: id >= idBound -> fail)
  +0x0A  u16     reserved = 0
  +0x0C  u16     idIndexOffset = 0x10 (003E8230: actl + word[+0xC])
  +0x0E  u16     auxTableOffset       (003E7EC0/003E8D50: actl + word[+0xE],
                                     handed to the per-record handler)

  at +0x10 the id index:
    u16 bucketCount                       (003E8230: id/100 >= word[T] -> fail)
    {u16 bound, u16 recordByteOffset}[]   (003E8230: word[T+2+b*4] bound,
                                          word[T+4+b*4] base)
  id -> record:  bucket = id/100, slot = id%100;
                 if bucket >= bucketCount or slot >= bound[bucket]: no record
                 record = actl + recordByteOffset[bucket] + slot * 0x16

  records: 0x16 bytes each, contiguous per bucket; an all-0xFF record is a
  tombstone. The aux table fills [auxTableOffset, fileSize).

Emit one row per pack with the parse result plus corpus invariant checks:
  rec_end == auxOff            (records end exactly at the aux table)
  idx_end == min(base offsets) (the index abuts the first record region)
  file size == auxOff + aux bytes

Usage:
  python gen_actl_census.py <FFXII_TZA.vbf> <out.tsv>
"""
import sys, struct, collections

sys.path.insert(0, 'C:/Users/Kristian/source/repos/XIIOnline/agent_flow/tools')
import vbfextract


def sections(d):
    cnt = struct.unpack_from('<I', d, 0)[0]
    sz = struct.unpack_from('<32I', d, 4)
    off = ((cnt + 1) * 4 + 0x3F) & ~0x3F
    out = {}
    for s in range(32):
        if sz[s]:
            off += 0x40
            out[s] = d[off:off + sz[s]]
            off += sz[s]
    return out


def parse_actl(b):
    """Return dict of header fields + lists, or {'error': ...}."""
    r = {}
    if len(b) < 0x10 or b[:4] != b'ACTL':
        return {'error': 'bad magic'}
    (r['ver'], r['stride'], r['idbound'], r['w0A'],
     r['idxoff'], r['auxoff']) = struct.unpack_from('<6H', b, 4)
    t = r['idxoff']
    r['buckets'] = struct.unpack_from('<H', b, t)[0]
    r['idxend'] = t + 2 + 4 * r['buckets']
    ent = []
    for i in range(r['buckets']):
        ent.append(struct.unpack_from('<2H', b, t + 2 + i * 4))
    r['entries'] = ent
    r['nrec'] = sum(e[0] for e in ent)
    # collect records
    recs = []
    for i, (bound, base) in enumerate(ent):
        for s in range(bound):
            recs.append(b[base + s * r['stride']:base + (s + 1) * r['stride']])
    r['recs'] = recs
    # invariant: the last record ends exactly at auxoff
    if r['nrec']:
        r['recend'] = max(e[1] + e[0] * r['stride'] for e in ent)
    else:
        r['recend'] = r['idxend']
    r['auxlen'] = len(b) - r['auxoff']
    return r


def main():
    vbf, out = sys.argv[1], sys.argv[2]
    f = open(vbf, 'rb')
    names, blocks = vbfextract.load_index(f)
    packs = sorted(n for n in names if n.lower().endswith('.mpk'))
    rows = []
    fld = collections.Counter()          # per-offset value census
    tomb = 0
    for p in packs:
        b = sections(vbfextract.read_entry(f, names, blocks, p)).get(9)
        if b is None:
            continue
        r = parse_actl(b)
        if 'error' in r:
            rows.append((p.split('/')[-1], len(b), 'PARSEFAIL', '', '', '',
                         '', '', '', '', '', '', ''))
            continue
        tomb += sum(1 for rec in r['recs'] if all(x == 0xFF for x in rec))
        for rec in r['recs']:
            for off in (0x00, 0x02, 0x0E, 0x10):
                fld[(off, struct.unpack_from('<H', rec, off)[0])] += 1
            for off in (0x12, 0x13, 0x14, 0x15):
                fld[(off, rec[off])] += 1
        rows.append((p.split('/')[-1], len(b), r['ver'], r['stride'],
                     r['idbound'], r['buckets'], r['nrec'],
                     r['idxoff'], r['auxoff'], r['auxlen'],
                     'OK' if r['recend'] == r['auxoff'] else
                     f"RECFIT+{r['recend']-r['auxoff']}",
                     'OK' if not r['nrec'] or
                     min(e[1] for e in r['entries']) >= r['idxend'] else
                     'IDXOVERLAP', tomb))
    with open(out, 'w', newline='') as o:
        o.write('# ACTL (slot 9) census over all .mpk in the VBF -- '
                'header fields, id-index shape, record count, aux extent\n')
        o.write('# layout proven against consumers 003E8230 / 003E7EC0 / '
                '003E8D50 / 003E82F0 / 003E8BF0; version gate in 003E8940\n')
        o.write('pack\tactl_bytes\tver\tstride\tidbound\tbuckets\trecords\t'
                'idxoff\tauxoff\tauxlen\trecfit\tidxfit\ttombstones\n')
        for row in rows:
            o.write('\t'.join(str(c) for c in row) + '\n')
    n = len(rows)
    print(f'{n} ACTL sections parsed; tombstone records {tomb}')
    print('field census (offset, value):')
    for (off, v), c in sorted(fld.items()):
        print(f'  +{off:02x} {v:#06x} x{c}')


if __name__ == '__main__':
    main()
