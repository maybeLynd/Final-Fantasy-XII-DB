"""@FMC sub-record key census — SWE2-DATA, UQ-218 residue (key domain).

Walks every .cm/.ca @FMC entry: per-record key list, sortedness, 0xFFFF
position, key-vs-@FMN-duration join, and the full key histogram.

    FF12_VBF=<archive> python fmc_subkey_census.py
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

def fmc_records(d, off, elen):
    """yield (rkind, [keys]) for each record in the entry."""
    rend = off + elen
    ro, ri = off + 0x30, 0
    rcount = struct.unpack_from("<I", d, off + 0x0C)[0]
    while ro + 6 <= rend and ri < rcount:
        rkind, subc = d[ro], d[ro + 3]
        rlen = struct.unpack_from("<H", d, ro + 4)[0]
        if rlen < 6 or ro + rlen > rend:
            return
        keys = []
        so = ro + 6
        for _ in range(subc):
            if so + 4 > ro + rlen:
                return
            skey, w2 = struct.unpack_from("<HH", d, so)
            keys.append(skey)
            keys_slen = w2 >> 6            # full sub-record span incl. 4-byte head
            so += keys_slen
        yield rkind, keys
        ro += rlen
        ri += 1

key_hist = collections.Counter()
unsorted = dup_key = 0
ffff_last = ffff_mid = no_ffff = rec_total = 0
kind_by_rec = collections.Counter()
key_vs_dur = collections.Counter()
key_max_nonf = 0
op_by_key = collections.defaultdict(collections.Counter)

for p in names:
    if not (p.lower().endswith(".cm") or p.lower().endswith(".ca")):
        continue
    fmn_dur = None
    for tag, off, d in entries(p):
        if tag == b"@FMN":
            fmn_dur = struct.unpack_from("<H", d, off + 0x50)[0]
    for tag, off, d in entries(p):
        if tag != b"@FMC":
            continue
        elen = struct.unpack_from("<I", d, off + 8)[0]
        for rkind, keys in fmc_records(d, off, elen):
            rec_total += 1
            kind_by_rec[rkind] += 1
            for k in keys:
                key_hist[k] += 1
            if not keys:
                no_ffff += 1
                continue
            if keys != sorted(keys):
                unsorted += 1
            if len(set(keys)) != len(keys):
                dup_key += 1
            if keys[-1] == 0xFFFF:
                ffff_last += 1
                if 0xFFFF in keys[:-1]:
                    ffff_mid += 1
                real = keys[:-1]
            else:
                no_ffff += 1
                if 0xFFFF in keys:
                    ffff_mid += 1
                real = [k for k in keys if k != 0xFFFF]
            if real:
                key_max_nonf = max(key_max_nonf, max(real))
                if fmn_dur is not None:
                    key_vs_dur['le' if max(real) <= fmn_dur else 'gt'] += 1
                else:
                    key_vs_dur['no_fmn'] += 1

print("records walked:", rec_total, " kinds:", dict(kind_by_rec))
print("distinct keys:", len(key_hist), " max non-FFFF key:", key_max_nonf)
print("unsorted:", unsorted, " dup:", dup_key)
print("FFFF-last:", ffff_last, " FFFF-mid:", ffff_mid, " no-FFFF:", no_ffff)
print("key<=dur:", dict(key_vs_dur))
print("top keys:", key_hist.most_common(45))
h = collections.Counter()
for k, c in key_hist.items():
    if k != 0xFFFF:
        h[min(k, 9999) // 100 * 100] += c
print("range hist:")
for b in sorted(h):
    print("  %5d-%5d: %d" % (b, b + 99, h[b]))
