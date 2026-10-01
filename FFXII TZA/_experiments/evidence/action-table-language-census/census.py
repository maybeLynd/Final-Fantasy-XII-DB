"""Which language directories carry action_data.bin, and is battle_pack.bin's +0x3C section the same table?

Data-tier census over FFXII_TZA.vbf (read-only). Set FF12_VBF to the archive path.
Positive control: battle_pack.bin is listed for all nine languages by the same name filter.
FABLE, 2026-09-12.
"""
import sys, os, io, struct, zlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../Tools/analysis-kit/gfz-scripts"))
from census_format_magics import load_index

BLOCK = 0x10000
VBF = os.environ["FF12_VBF"]
f = io.open(VBF, "rb")
names, blocks = load_index(f)


def read_all(path):
    sb, size, off = names[path]
    n = (size + BLOCK - 1) // BLOCK
    out = b""
    f.seek(off)
    for i in range(n):
        csize = blocks[sb + i] or BLOCK
        expected = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        chunk = f.read(csize)
        if csize != expected:
            chunk = zlib.decompress(chunk)
        out += chunk
    assert len(out) == size, (len(out), size)
    return out


def section(buf, d):
    off = struct.unpack_from("<i", buf, d)[0]
    cnt = struct.unpack_from("<I", buf, off + 4)[0]
    stride = struct.unpack_from("<H", buf, off + 8)[0]
    return buf[off + 0x20: off + 0x20 + cnt * stride], cnt, stride, buf[off:off + 0x20]


if __name__ == "__main__":
    print("entries in archive:", len(names))
    cands = sorted(p for p in names if p.endswith("/action_data.bin") or p.endswith("/battle_pack.bin"))
    for p in cands:
        print("listed", p, names[p][1])
    langs = ["ch", "cn", "de", "es", "fr", "in", "it", "kr", "us"]
    secs = {}
    for L in langs:
        bp = read_all("ps2data/image/ff12/test_battle/%s/binaryfile/battle_pack.bin" % L)
        secs[L] = section(bp, 0x3C)
    us = secs["us"][0]
    for L in langs:
        rows, c, s, hdr = secs[L]
        d = [i for i in range(len(rows)) if rows[i] != us[i]]
        print("battle_pack %s +0x3C: magic %r count %d stride %d; differs from us in %d bytes" % (L, hdr[:4], c, s, len(d)))
    for p in [q for q in cands if q.endswith("action_data.bin")]:
        L = p.split("/")[4]
        ad = read_all(p)
        c2 = struct.unpack_from("<I", ad, 4)[0]
        s2 = struct.unpack_from("<H", ad, 8)[0]
        rows = ad[0x20: 0x20 + c2 * s2]
        own = secs[L][0]
        du = [i for i in range(len(rows)) if rows[i] != us[i]]
        do = [i for i in range(len(rows)) if rows[i] != own[i]]
        print("action_data %s: count %d stride %d header==battle_pack section header %s; differs from own battle_pack in %d bytes, from us in %d" % (L, c2, s2, ad[:0x20] == secs[L][3], len(do), len(du)))
        for i in du:
            r = i // 60
            print("   row %d +0x%02X: us word %d, %s byte %02X" % (r, i % 60, struct.unpack_from("<H", us, r * 60 + 0x34)[0], L, rows[i]))
    bad = [(r, struct.unpack_from("<H", us, r * 60 + 0x34)[0]) for r in range(543) if struct.unpack_from("<H", us, r * 60 + 0x34)[0] != r]
    print("us rows whose +0x34 word != row index:", bad)
