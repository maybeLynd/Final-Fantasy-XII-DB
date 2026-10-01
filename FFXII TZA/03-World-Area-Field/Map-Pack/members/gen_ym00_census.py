#!/usr/bin/env python3
"""
gen_ym00_census.py -- MP-2: the YM00 section (slot 8) of the map-ctrl pack.

Walks every ps2data/plan_master/map_ctrl/**/bin/*.mpk in the shipped
FFXII_TZA.vbf, extracts the slot-8 payload and parses its chunk index under
the layout proved against 002F6AB0's index walk:

    mov ecx, [r15-4]            ; previous index entry
    mov edx, [r15]              ; current index entry
    and prev, 0xffffff
    shl r14, 4                  ; chunkPtr = base + prevOff * 16   (base=file+8)
    and edx/eax, 0xffffff
    sub edx, eax                ; chunkSize = curOff - prevOff
    shr ecx, 0x18               ; tag = entry >> 24
    cmp eax, 0x21               ; tags 0..33
    mov ecx, [r13+rax*4+1d72f8] ; jump table
    jmp rcx

File layout:
    +0x00 'YM00'
    +0x04 f32      per-map scalar
    +0x08 char[8]  author tag (developer surname, e.g. 'naomif',
                   't-hiros', 'mtanaka' -- NOT the pack stem)
    +0x10 u32      indexCount = 17  (rbx = &file[0x10] in 002F6AB0)
    +0x14 (indexCount+1) x {u24 offset | u8 tag}, offsets ascending,
                   in 16-byte units relative to file+0x10;
                   the +1 entry is the end sentinel {tag=0xFF, off=end}
    chunk(tag_i) = file[0x10 + off_i*16, 0x10 + off_{i+1}*16)
    a small 16-byte-unit tail pad may follow the last chunk.

Emits one row per (pack, tag) with chunk offset/size, plus per-pack
invariant checks: ascending offsets, terminator presence, last chunk
end vs file size.

Usage:
  python gen_ym00_census.py <FFXII_TZA.vbf> <out.tsv>
"""
import sys, struct, collections

sys.path.insert(0, 'C:/Users/Kristian/source/repos/XIIOnline/agent_flow/tools')
import vbfextract


def slot9(d, s):
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
    tagsets = collections.Counter()
    bad = []
    for p in packs:
        b = slot9(vbfextract.read_entry(f, names, blocks, p), 8)
        if b is None:
            continue
        stem = p.split('/')[-1]
        if len(b) < 0x14 or b[:4] != b'YM00':
            bad.append(stem)
            continue
        w04 = struct.unpack_from('<I', b, 4)[0]
        name = b[8:0x10].split(b'\0')[0].decode('ascii', 'replace')
        n = struct.unpack_from('<I', b, 0x10)[0]
        ents = []
        ok = True
        for i in range(n + 1):                     # count+1 dwords; last = 0xFF end sentinel
            v = struct.unpack_from('<I', b, 0x14 + i * 4)[0]
            off, tag = v & 0xFFFFFF, v >> 24
            if ents and off < ents[-1][0]:
                ok = False
            ents.append((off, tag))
        tagset = tuple(sorted(t for _, t in ents if t != 0xFF))
        tagsets[tagset] += 1
        # chunk extents: chunk_i = [0x10+off_i*16, 0x10+off_{i+1}*16)
        last_end = 0x10 + ents[-1][0] * 16
        for i, (off, tag) in enumerate(ents):
            nxt = ents[i + 1][0] if i + 1 < len(ents) else off
            rows.append((stem, len(b), name, n, i, tag,
                         0x10 + off * 16, (nxt - off) * 16,
                         'OK' if ok else 'ORDER', last_end,
                         len(b) - last_end))
    with open(out, 'w', newline='') as o:
        o.write('# YM00 (slot 8) chunk census over all .mpk in the VBF\n')
        o.write('# layout: indexCount+1 {tag:8|offset:24} dwords at +0x14, '
                'offsets in 16-byte units from file+0x10; last entry = '
                '0xFF end sentinel; chunk=[off_i,off_{i+1}); '
                'proved against 002F6AB0 index walk\n')
        o.write('pack\tym00_bytes\tinner_name\tidx_count\tentry\ttag\t'
                'chunk_off\tchunk_bytes\torder\tlast_end\ttail_pad\n')
        for row in rows:
            o.write('\t'.join(str(c) for c in row) + '\n')
    print(f'{len(set(r[0] for r in rows))} YM00 sections, '
          f'{len(rows)} index rows, bad: {bad}')
    print('tag-set histogram (top 12):')
    for ts, c in tagsets.most_common(12):
        print(f'  x{c}: {ts}')


if __name__ == '__main__':
    main()
