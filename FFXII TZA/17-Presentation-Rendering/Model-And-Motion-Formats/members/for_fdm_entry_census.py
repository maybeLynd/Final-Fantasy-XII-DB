"""@FOR / @FDM entry census — SWE2-DATA, UQ-218 FDM-FOR slice.

Runs the structural claims in fdm-and-for-entries.md over every .cm in the
archive: @FOR header fields, keyed 0xE0-stride record table, u16 index-list
tail bounds; @FDM key-table at +0x32 and the three {u32 n, u16[n]} list
offsets with -1 sentinels.

    FF12_VBF=<archive> python for_fdm_entry_census.py
"""
import sys, os, io, struct, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
from census_format_magics import load_index

BLOCK = 0x10000
f = io.open(os.environ["FF12_VBF"], "rb")
names, blocks = load_index(f)

def read_all(p):
    sb, size, off = names[p]
    n = (size + BLOCK - 1) // BLOCK
    out = b""
    f.seek(off)
    for i in range(n):
        cs = blocks[sb + i] or BLOCK
        exp = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        c = f.read(cs)
        if cs != exp:
            c = zlib.decompress(c)
        out += c
    return out

def entries(p):
    d = read_all(p)
    var, clen, cnt = struct.unpack_from("<III", d, 4)
    base = 0x40 if var == 1 else 0x30
    for i in range(cnt):
        o = base + struct.unpack_from("<I", d, base + i * 4)[0]
        yield d[o:o + 4], o, d

for_files = 0
for_recbase = collections.Counter()
for_thresh = collections.Counter()
for_keys_seq = 0
for_keys_other = []
for_tail_ok = 0
for_tail_bad = []
for_w34 = collections.Counter()
fdm_files = 0
fdm_keyoff = collections.Counter()
fdm_lists_ok = 0
fdm_lists_bad = []
fdm_keyseq = collections.Counter()

for p in [q for q in names if q.lower().endswith(".cm")]:
    for tag, o, d in entries(p):
        if tag == b"@FOR":
            elen = struct.unpack_from("<I", d, o + 8)[0]
            e = d[o:o + elen]
            for_files += 1
            rc = e[0x30]
            rb = struct.unpack_from("<H", e, 0x38)[0]
            for_recbase[rb] += 1
            for_w34[struct.unpack_from("<H", e, 0x34)[0]] += 1
            for_thresh[(e[0x3A], e[0x3B])] += 1
            ok = True
            for i in range(rc):
                r = e[rb + i * 0xE0:rb + (i + 1) * 0xE0]
                if len(r) < 0xE0 or r[0] != i + 1:
                    ok = False
            if ok:
                for_keys_seq += 1
            else:
                for_keys_other.append(p)
            bad = False
            for i in range(rc):
                r = e[rb + i * 0xE0:]
                for k in range(3):
                    off = struct.unpack_from("<H", r, 0x08 + k * 2)[0]
                    n = struct.unpack_from("<H", r, 0x10 + k * 2)[0]
                    if off and off + 2 * n > elen:
                        bad = True
            if bad:
                for_tail_bad.append(p)
            else:
                for_tail_ok += 1
        elif tag == b"@FDM":
            elen = struct.unpack_from("<I", d, o + 8)[0]
            e = d[o:o + elen]
            fdm_files += 1
            kt = struct.unpack_from("<H", e, 0x32)[0]
            fdm_keyoff[kt] += 1
            offs = struct.unpack_from("<III", e, 0x34)
            ok = True
            for off in offs:
                if off == 0xFFFFFFFF:
                    continue
                if off + 4 > elen:
                    ok = False
                    break
                n = struct.unpack_from("<I", e, off)[0]
                if off + 4 + 2 * n > elen or n > 0x400:
                    ok = False
                    break
            if ok:
                fdm_lists_ok += 1
            else:
                fdm_lists_bad.append((p, offs))
            n = struct.unpack_from("<I", e, kt)[0]
            ks = struct.unpack_from("<%dI" % n, e, kt + 4)
            fdm_keyseq[all(ks[i + 1] - ks[i] == 1 for i in range(n - 1))] += 1

print("@FOR files:", for_files)
print("  rec base u16@0x38:", dict(for_recbase))
print("  tableA u16@0x34:", dict(for_w34))
print("  (thresh count, cap) @0x3A/0x3B:", dict(for_thresh))
print("  rec keys = 1..count:", for_keys_seq, "exceptions:", len(for_keys_other), for_keys_other)
print("  u16 lists in bounds:", for_tail_ok, "bad:", len(for_tail_bad))
print("@FDM files:", fdm_files)
print("  key-table u16@0x32:", dict(fdm_keyoff))
print("  {u32 n, u16[n]} lists (or -1) ok:", fdm_lists_ok, "bad:", len(fdm_lists_bad), fdm_lists_bad[:4])
print("  keys strictly sequential:", dict(fdm_keyseq))
