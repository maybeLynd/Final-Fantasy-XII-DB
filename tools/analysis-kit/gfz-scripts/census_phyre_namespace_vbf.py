"""Census the packed namespace of every shipped .phyre file -- the whole archive, not a sample.

`census_phyre_namespace.py` walks `D:/FFXII MP Mod/extracted`, which holds a 169-file development
extract. The shipped corpus is the 35,984 `.phyre` members of `FFXII_TZA.vbf`; this script reads
each one straight out of the archive (in-memory SRYK index + per-entry decompress, same loader as
`agent_flow/tools/vbfextract.py`) and runs the structural census the CONTRACT-phyre-packed-namespace
§14 items needed:

  * NS-2: header words +0x18 / +0x1C   -> zero in 35,984/35,984
  * NS-3: member word w5               -> the fixed-array bound (nonzero in 21,459/2,192,621)
  * NS-1: class word w7                -> a per-class flags word, constant per class name
  * NS-5: corpus scope                 -> BOM and the size equation close in 35,984/35,984
  * class w4/w5/w6/w8                  -> zero in all 684,244 shipped records

Usage:
    python census_phyre_namespace_vbf.py [--vbf <archive>]
"""
import struct, collections, os, sys, zlib, json

DEFAULT_VBF = os.environ.get('FFXII_VBF', r"D:\Final Fantasy XII The Zodiac Age\FFXII_TZA.vbf")


def load_index(f):
    magic, headerLen = struct.unpack("<4sI", f.read(8))
    assert magic == b"SRYK"
    (numFiles,) = struct.unpack("<Q", f.read(8))
    entries_off = 0x10 + numFiles * 16
    f.seek(entries_off)
    raw = f.read(0x20 * numFiles)
    entries = []
    for i in range(numFiles):
        sb, sb2, size, off, noff = struct.unpack_from("<IIQQQ", raw, i * 0x20)
        entries.append((sb, size, off, noff))
    strtab_off = entries_off + 0x20 * numFiles
    f.seek(strtab_off)
    (strLen,) = struct.unpack("<I", f.read(4))
    strtab = f.read(strLen)
    blocklist_off = strtab_off + strLen
    f.seek(blocklist_off)
    bl_raw = f.read(headerLen - blocklist_off)
    blocks = struct.unpack("<%dH" % (len(bl_raw) // 2), bl_raw)
    names = {}
    for i, (sb, size, off, noff) in enumerate(entries):
        end = strtab.index(b"\0", noff)
        names[strtab[noff:end].decode()] = (sb, size, off)
    return names, blocks


def read_entry(f, names, blocks, path):
    sb, size, off = names[path]
    f.seek(off)
    out = bytearray()
    todo = size
    while todo > 0:
        n = min(todo, 0x10000)
        clen = blocks[sb]
        sb += 1
        chunk = f.read(clen)
        out += zlib.decompress(chunk) if clen < n else chunk
        todo -= n
    return bytes(out)


def main():
    vbf = sys.argv[sys.argv.index('--vbf') + 1] if '--vbf' in sys.argv else DEFAULT_VBF
    f = open(vbf, 'rb')
    names, blocks = load_index(f)
    phyre = sorted(p for p in names if p.endswith('.phyre'))
    print('%d .phyre entries of %d archive members' % (len(phyre), len(names)))

    u6 = collections.Counter(); u7 = collections.Counter()
    w5v = collections.Counter(); w7v = collections.Counter()
    cw0 = {4: collections.Counter(), 5: collections.Counter(), 6: collections.Counter(), 8: collections.Counter()}
    cname_w7 = collections.defaultdict(set)
    mname_w5 = collections.defaultdict(set)
    w5_recs = []
    bom_ok = size_ok = mismatch = parse_fail = 0
    nC_tot = nM_tot = 0

    for idx, p in enumerate(phyre):
        if idx % 6000 == 0:
            print('...', idx, flush=True)
        try:
            d = read_entry(f, names, blocks, p)
            hs, ns = struct.unpack_from('<I', d, 4)[0], struct.unpack_from('<I', d, 8)[0]
            b = d[hs:hs + ns]
            bom, size, A, nC, nM, S, U6, U7 = struct.unpack_from('<8I', b, 0)
            if bom == 0x01020304: bom_ok += 1
            u6[U6] += 1; u7[U7] += 1
            off = 0x20 + 4 * A
            cls = [struct.unpack_from('<9I', b, off + 36 * i) for i in range(nC)]; off += 36 * nC
            mem = [struct.unpack_from('<6I', b, off + 24 * i) for i in range(nM)]; off += 24 * nM
            pool = b[off:off + S]
            if 0x20 + 4 * A + 36 * nC + 24 * nM + S == size: size_ok += 1
            else: mismatch += 1
            nC_tot += nC; nM_tot += nM

            def nm(o):
                e = pool.find(b'\0', o)
                return pool[o:e].decode(errors='replace') if 0 <= o < len(pool) and e >= 0 else '?'

            for c in cls:
                for wi in (4, 5, 6, 8):
                    if c[wi]: cw0[wi][c[wi]] += 1
                if c[7]:
                    w7v[c[7]] += 1
                    cname_w7[nm(c[2])].add(c[7])
            for m in mem:
                if m[5]:
                    w5v[m[5]] += 1
                    mname_w5[nm(m[0])].add(m[5])
                    w5_recs.append((p, nm(m[0]), m[5]))
        except Exception:
            parse_fail += 1

    print('bom_ok %d  size_ok %d  mismatch %d  parse_fail %d' % (bom_ok, size_ok, mismatch, parse_fail))
    print('classes %d  members %d' % (nC_tot, nM_tot))
    print('U6(+0x18): %s   U7(+0x1C): %s' % (dict(u6), dict(u7)))
    print('member w5 nonzero: %d %s' % (sum(w5v.values()), dict(w5v.most_common(20))))
    print('class  w7 nonzero: %d %s' % (sum(w7v.values()), dict(w7v.most_common(20))))
    for wi in (4, 5, 6, 8):
        print('class  w%d nonzero: %s' % (wi, dict(cw0[wi].most_common(8))))
    multi7 = {k: v for k, v in cname_w7.items() if len(v) > 1}
    multi5 = {k: v for k, v in mname_w5.items() if len(v) > 1}
    print('class names with >1 distinct w7 : %d %s' % (len(multi7), list(multi7.items())[:8]))
    print('member names with >1 distinct w5: %d %s' % (len(multi5), list(multi5.items())[:8]))


if __name__ == '__main__':
    main()
