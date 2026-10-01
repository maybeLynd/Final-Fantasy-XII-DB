"""Every .mh in the archive: the PS2 movie seek index, measured from the bytes.

Read-only over FFXII_TZA.vbf (set FF12_VBF). Hypothesis tested on all files: a 0x18-byte header
('.mhe', u8 kind, u8, u16, u16 width?, u16 height?, u32 total, u32 frameCount, u32 entryCount)
followed by entryCount 12-byte entries {u32 offset, u32 frame, u32 flags}, ending at the file end;
offsets and frames non-decreasing; the last offset below the total.
Also, from the executable (set FF12_EXE): occurrences of the magic and of the kind-28 path array's
.mh entries, and the matching .webm for each .mh stem.
Positive control: the extension census lists 43 .mh entries.
FABLE, 2026-09-12.
"""
import sys, os, io, re, struct, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../Tools/analysis-kit/gfz-scripts"))
from census_format_magics import load_index

BLOCK = 0x10000
f = io.open(os.environ["FF12_VBF"], "rb")
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
    return out


paths = sorted(p for p in names if p.lower().endswith(".mh"))
print("control: .mh entries:", len(paths), "(published 43)")
C = collections.Counter
ok = C(); kinds = C(); b5 = C(); dims = C(); flags = C(); first = C(); monot = C(); below = C(); ratio = []
webm = {p.split("/")[-1][:-5].lower() for p in names if p.lower().endswith(".webm")}
has_webm = C()
for p in paths:
    d = read_all(p)
    magic, k, u5, w6, w8, wa, total, frames, count = struct.unpack_from("<4sBBHHHIII", d, 0)
    ok["size == 0x18 + 12*count" if len(d) == 0x18 + 12 * count and magic == b".mhe" else "mismatch"] += 1
    kinds[k] += 1; b5[u5] += 1; dims[(w8, wa)] += 1
    ents = [struct.unpack_from("<III", d, 0x18 + 12 * i) for i in range(count)]
    for e in ents:
        flags[e[2]] += 1
    first[ents[0][1] if ents else None] += 1
    monot["offsets and frames non-decreasing" if all(ents[i][0] <= ents[i + 1][0] and ents[i][1] <= ents[i + 1][1] for i in range(len(ents) - 1)) else "not monotonic"] += 1
    below["last offset < total" if ents and ents[-1][0] < total else "not below"] += 1
    if ents and ents[-1][1]:
        ratio.append(round(frames / ents[-1][1], 2))
    stem = p.split("/")[-1][:-3].lower()
    has_webm["a .webm with this stem exists" if stem in webm else "no .webm with this stem"] += 1
print(dict(ok), "; +0x04:", dict(kinds), "; +0x05:", dict(b5), "; +0x08/+0x0A:", dict(dims))
print("entry flags:", dict(flags), "; first entry frame:", dict(first), dict(monot), dict(below))
print("frameCount / last entry frame (min, max):", min(ratio), max(ratio))
print(dict(has_webm))
exe = open(os.environ["FF12_EXE"], "rb").read()
print("'.mhe' in the executable:", exe.count(b".mhe"), "; as a dword:", exe.count(struct.pack("<I", 0x65686D2E)))
print(".mh path strings in the executable:", len(re.findall(rb"movie_finish\\[a-z]{2}\\[A-Za-z_0-9]+\.mh\x00", exe, re.I)))
