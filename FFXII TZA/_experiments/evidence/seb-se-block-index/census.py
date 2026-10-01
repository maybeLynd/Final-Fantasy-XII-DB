"""Every .seb in the archive, checked against what SebAudioBank's initialiser 00223AD0 reads.

Read-only over FFXII_TZA.vbf (set FF12_VBF). 00223AD0 reads: +0x08 i16 block id (compared with the
expected id, 00223B53-00223B59), +0x0A i16 entry count (00223B72), +0x10 i32 offset[count] with -1 =
absent (00223B94), and for each present entry the u32 and u8 at (+0x10 + 4*count + offset)
(00223BBA-00223BE8); it copies the first 16 bytes to the bank (00223C76) and then opens
PS2Data/sound/se/sead_data_win/se%03d/se%03d.win.sab for the block id (00223CB1-00223CD5).
Also checks: the magic, +0x0C against the file size, offsets in bounds and ascending, the file name
number against +0x08, and whether the .sab that the id names exists in the archive.
Positive control: the extension census lists 248 .seb entries.
FABLE, 2026-09-12.
"""
import sys, os, io, re, struct, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../Tools/analysis-kit/gfz-scripts"))
from census_format_magics import load_index

BLOCK = 0x10000
f = io.open(os.environ["FF12_VBF"], "rb")
names, blocks = load_index(f)
lower = {p.lower() for p in names}


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
    assert len(out) == size
    return out


paths = sorted(p for p in names if p.lower().endswith(".seb"))
print("control: .seb entries in the archive index:", len(paths), "(published 248)")
C = collections.Counter
magic = C(); count = C(); sizefield = C(); idname = C(); sab = C(); present = C(); ascending = C(); inbounds = C()
first_u32 = C(); first_u8 = C(); w0e = C(); entries = 0; gaps = C()
for p in paths:
    d = read_all(p)
    magic[d[:8]] += 1
    bid, n = struct.unpack_from("<hh", d, 8)
    count[n] += 1
    sizefield["+0x0C == file size" if struct.unpack_from("<I", d, 0xC)[0] == len(d) else "+0x0C != file size"] += 1
    m = re.search(r"se(\d+)\.seb$", p.lower())
    idname["+0x08 == file number" if m and int(m.group(1)) == bid else "differs"] += 1
    sab["the id's se<id>.win.sab exists" if ("ps2data/sound/se/sead_data_win/se%03d/se%03d.win.sab" % (bid, bid)) in lower else "no .win.sab for the id"] += 1
    offs = struct.unpack_from("<%di" % n, d, 0x10)
    base = 0x10 + 4 * n
    live = [o for o in offs if o != -1]
    present[len(live)] += 1
    ascending["ascending" if live == sorted(live) else "not ascending"] += 1
    inbounds["all in bounds" if all(base + o + 5 <= len(d) for o in live) else "out of bounds"] += 1
    for o in live:
        entries += 1
        first_u32[struct.unpack_from("<I", d, base + o)[0] & 0xFF] += 1
        first_u8[d[base + o + 4]] += 1
    first_idx = [i for i, o in enumerate(offs) if o != -1]
    gaps["present entries contiguous from 0" if first_idx == list(range(len(first_idx))) else "sparse"] += 1
print("magic:", {k: v for k, v in magic.items()})
print("entry count +0x0A:", dict(count), "; +0x0C:", dict(sizefield), "; block id:", dict(idname))
print("audio bank:", dict(sab))
print("present entries per file (histogram top):", present.most_common(8), "; total entries:", entries)
print("offsets:", dict(ascending), dict(inbounds), dict(gaps))
print("first byte of each entry's u32 (top):", first_u32.most_common(6), "; its +4 byte (top):", first_u8.most_common(6))
