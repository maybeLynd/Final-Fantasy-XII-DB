"""Decode the packed-namespace table.

Layout, read out of the byte-swap routine 0059C180 and confirmed by arithmetic on 169/169 files:

    +0x00 u32  0x01020304 byte-order mark
    +0x04 u32  namespaceSize          (repeats m_packedNamespaceSize)
    +0x08 u32  A                      -- region A, A words
    +0x0C u32  nClasses               -- records of 9 words  (0059A780 swaps these)
    +0x10 u32  nMembers               -- records of 6 words
    +0x14 u32  stringPoolSize
    +0x18 u32  ?
    +0x1C u32  ?
    +0x20      u32[A] | class[9]*nClasses | member[6]*nMembers | char[stringPoolSize]

A column is identified as a string-pool offset only if, over EVERY record in EVERY file, it lands
exactly on the first byte of a NUL-terminated name. One counter-example disqualifies the column.
"""
import os, struct, collections

ROOT = 'D:/FFXII MP Mod/extracted'
files = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if f.lower().endswith('.phyre'):
            files.append(os.path.join(dp, f))
files.sort()

cls_col_ok = [0] * 9
cls_col_bad = [0] * 9
mem_col_ok = [0] * 6
mem_col_bad = [0] * 6
cls_records = 0
mem_records = 0
regionA_ok = regionA_bad = 0
samples = []

for p in files:
    d = open(p, 'rb').read()
    hs, ns = struct.unpack_from('<I', d, 4)[0], struct.unpack_from('<I', d, 8)[0]
    b = d[hs:hs + ns]
    bom, size, A, nC, nM, S, U6, U7 = struct.unpack_from('<8I', b, 0)
    off = 0x20
    regA = struct.unpack_from('<%dI' % A, b, off); off += 4 * A
    cls = [struct.unpack_from('<9I', b, off + 36 * i) for i in range(nC)]; off += 36 * nC
    mem = [struct.unpack_from('<6I', b, off + 24 * i) for i in range(nM)]; off += 24 * nM
    pool = b[off:off + S]

    def name_at(o):
        if not (0 <= o < len(pool)):
            return None
        if o and pool[o - 1] != 0:
            return None                      # not the START of a string
        e = pool.find(b'\0', o)
        if e < 0:
            return None
        s = pool[o:e]
        if not s or not all(32 <= c < 127 for c in s):
            return None
        return s.decode()

    for o in regA:
        if name_at(o) is not None:
            regionA_ok += 1
        else:
            regionA_bad += 1
    for r in cls:
        cls_records += 1
        for i, w in enumerate(r):
            if name_at(w) is not None:
                cls_col_ok[i] += 1
            else:
                cls_col_bad[i] += 1
    for r in mem:
        mem_records += 1
        for i, w in enumerate(r):
            if name_at(w) is not None:
                mem_col_ok[i] += 1
            else:
                mem_col_bad[i] += 1
    if len(samples) < 1:
        samples.append((os.path.basename(p), A, nC, nM, S, U6, U7,
                        [name_at(o) for o in regA],
                        [(r, name_at(r[0]), name_at(r[2])) for r in cls[:6]],
                        [(r, name_at(r[0]), name_at(r[1])) for r in mem[:6]]))

print("files %d   class records %d   member records %d" % (len(files), cls_records, mem_records))
print("region A entries resolving to a pool string: %d ok / %d bad" % (regionA_ok, regionA_bad))
print()
print("class record columns (9 words):")
for i in range(9):
    print("  word %d : %6d resolve / %6d do not %s" % (i, cls_col_ok[i], cls_col_bad[i],
                                                       "   <-- ALWAYS A NAME" if cls_col_bad[i] == 0 else ""))
print("member record columns (6 words):")
for i in range(6):
    print("  word %d : %6d resolve / %6d do not %s" % (i, mem_col_ok[i], mem_col_bad[i],
                                                       "   <-- ALWAYS A NAME" if mem_col_bad[i] == 0 else ""))
print()
n, A, nC, nM, S, U6, U7, ra, cs, ms = samples[0]
print("=== sample: %s   A=%d classes=%d members=%d pool=%d  word6=%d word7=%d ===" % (n, A, nC, nM, S, U6, U7))
print("region A names:", ra)
print("first class records:")
for r, n0, n2 in cs:
    print("   ", r, " w0->", n0, " w2->", n2)
print("first member records:")
for r, n0, n1 in ms:
    print("   ", r, " w0->", n0, " w1->", n1)
