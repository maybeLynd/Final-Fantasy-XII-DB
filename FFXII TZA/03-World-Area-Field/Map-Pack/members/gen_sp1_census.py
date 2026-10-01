#!/usr/bin/env python3
"""
gen_sp1_census.py -- MP-2: the SP1 section (slot 16) of the map-ctrl pack.

Walks every ps2data/plan_master/map_ctrl/**/bin/*.mpk in the shipped
FFXII_TZA.vbf, extracts the slot-16 payload and parses it under the layout
recovered from the consumer bodies:

    003635C0            installer: stores the block at 022BBAF0, clears flags
    00363B40            weather path: word[+0x1A] = offset of
                        {u16 count; i16 idx[]}, each idx bound-checked
                        against dword[+0x04] then reads u32[+0x20 + idx*4]
                        (edx > 0 required) -- the weather-index table
    003638B0            per-emitter play call: [rbx] = index, bound-checked
                        against [rcx+4], reads the same u32[+0x20] table
    003631B0            per-frame emitter walker: iterates a u16 list
                        (bit15 = end marker), each entry &0x7FFF indexes
                        {u16 bound; u16 recordOff[]} -> emitter record
                        (record base = SP1 + off); reads [rec+9]&0x7F
                        shape class (0/1/2 position transforms), [rec+0x38],
                        [rec+0x54], [rec+0x58] floats

Layout:
    +0x00 'SP1\\0'
    +0x04 u32     indexBound   bound for the +0x20 value table (0x20 in samples)
    +0x08 u32     offB         -> region B: {f32 x4, u32 x2, u16 idx-list...}
    +0x0C u32     offC         -> {u16 bound; u16 recordOff[]} emitter index
    +0x10 u32     offD         -> u16 bit15-terminated idx list, then
                                  0x40-stride emitter records
    +0x14..+0x19  zeros
    +0x1A u16     offWeather   -> optional {u16 count; i16 idx[]} list (0=absent)
    +0x1C..+0x1F  zeros
    +0x20 u32[bound] valueTable  index -> SE id (>0 live; <=0 inert)

Emits one row per pack with the header fields, region sizes, the emitter
index's bound/offset census, and invariant flags.

Usage:
  python gen_sp1_census.py <FFXII_TZA.vbf> <out.tsv>
"""
import sys, struct, collections

sys.path.insert(0, 'C:/Users/Kristian/source/repos/XIIOnline/agent_flow/tools')
import vbfextract


def slot16(d, s):
    cnt = struct.unpack_from('<I', d, 0)[0]
    sz = struct.unpack_from('<32I', d, 4)
    off = ((cnt + 1) * 4 + 0x3F) & ~0x3F
    for i in range(32):
        if sz[i]:
            off += 0x40
            if i == s:
                return d[off:off + sz[i]]
            off += sz[i]
    return None


def main():
    vbf, out = sys.argv[1], sys.argv[2]
    f = open(vbf, 'rb')
    names, blocks = vbfextract.load_index(f)
    packs = sorted(n for n in names if n.lower().endswith('.mpk'))
    rows = []
    bad = []
    bounds = collections.Counter()
    for p in packs:
        b = slot16(vbfextract.read_entry(f, names, blocks, p), 16)
        if b is None:
            continue
        stem = p.split('/')[-1]
        if len(b) < 0x20 or b[:4] != b'SP1\0':
            bad.append(stem)
            continue
        # +0x04 is constant 0x20: the listBase argument to 0020E600, i.e. the
        # byte offset of the index-list region, not an SPP1-style bound.
        bound, offB, offC, offD = struct.unpack_from('<4I', b, 4)
        offW = struct.unpack_from('<H', b, 0x1A)[0]
        bounds[bound] += 1
        ok = []
        # region at +0x20 (bound * 4 bytes): the {u32 count; i32 idx[]} lists
        ok.append('T' if bound * 4 + 0x20 <= len(b) else 't')
        # region C: {u16 bound; u16 offs[]}
        cBound = offs_valid = offn = 0
        cmin = cmax = 0
        if offC and offC + 2 <= len(b):
            cBound = struct.unpack_from('<H', b, offC)[0]
            if offC + 2 + cBound * 2 <= len(b):
                offs = struct.unpack_from('<%dH' % cBound, b, offC + 2)
                nz = [o for o in offs if o]
                offn = len(nz)
                if nz:
                    cmin, cmax = min(nz), max(nz)
                    offs_valid = sum(1 for o in nz if o < len(b))
            ok.append('C' if offs_valid == offn else 'c')
        else:
            ok.append('-')
        # region D: u16 list until bit15
        dterm = -1
        if offD and offD < len(b):
            i = offD
            while i + 1 < len(b):
                v = struct.unpack_from('<H', b, i)[0]
                if v & 0x8000:
                    dterm = i
                    break
                i += 2
            ok.append('D' if dterm >= 0 else 'd')
        else:
            ok.append('-')
        # +0x1A: would name an override list (00363B40's SPP1-side read); 0 in
        # the whole corpus -> flag '0'
        wn = -1
        if offW and offW + 2 <= len(b):
            wn = struct.unpack_from('<H', b, offW)[0]
            ok.append('W' if offW + 2 + wn * 2 <= len(b) else 'w')
        elif offW == 0:
            ok.append('0')
        rows.append((stem, len(b), bound, hex(offB), hex(offC), hex(offD),
                     offW, wn, cBound, offn, hex(cmin), hex(cmax),
                     dterm, ''.join(ok)))
    with open(out, 'w', newline='') as o:
        o.write('# SP1 (slot 16) census over all .mpk in the VBF\n')
        o.write('# layout: {+0x04 listBase=0x20 (0020E600 arg); +0x08 offAreas;'
                ' +0x0C offEmitterIndex={u16 bound;u16 off[]};'
                ' +0x10 offEmitters=bit15-u16-prefix+records; +0x1A u16=0 dead;'
                ' +0x20 index-list region {u32 count;i32 idx[]}}\n')
        o.write('# consumers: SP1=003635C0(install)/003631B0(walker);'
                ' SPP1-side bound checks=003638B0/00363B40 (global 022CBAF8)\n')
        o.write('pack\tsp1_bytes\tdword04\toffB\toffC\toffD\toffW\tw_count\t'
                'c_bound\tc_offn\tc_min\tc_max\td_term\tflags\n')
        for row in rows:
            o.write('\t'.join(str(c) for c in row) + '\n')
    print(f'{len(rows)} SP1 sections, bad: {bad}')
    print('idxBound histogram:', dict(bounds))


if __name__ == '__main__':
    main()
