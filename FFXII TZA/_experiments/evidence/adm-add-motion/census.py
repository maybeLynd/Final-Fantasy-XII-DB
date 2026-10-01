"""Every .adm in the archive, walked exactly as AddMotion_ParseFile (001BE1A0) walks it.

Read-only over FFXII_TZA.vbf (set FF12_VBF). Stream: i16 trackCount; per track 8 bytes
{u8, u8, u16, u16 groupCount, u16 keyCount} (001BE260-001BE290 store them at +6, +7, +0, +4, +2);
per group a 28-byte record (001BE2E0-001BE30C) followed by keyCount 28-byte records (001BE340-001BE373).
Checks that the walk ends exactly at the file size, and reports the field values seen, the 28-byte
records read as f32 in the byte positions the parser copies as 8-byte and 4-byte pieces, and the
add_motion_list.txt entries against the shipped files.
Positive control: the extension census lists 39 .adm entries.
FABLE, 2026-09-12.
"""
import sys, os, io, struct, zlib, collections
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


C = collections.Counter


def mc(c, n):
    """most_common with a deterministic tie-break (count descending, then key)."""
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


paths = sorted(p for p in names if p.lower().endswith(".adm"))
print("control: .adm entries:", len(paths), "(published 39)")
exact = 0; tracks = C(); b0 = C(); b1 = C(); w2 = C(); groups = C(); keys = C()
g4 = C(); k0 = C(); gfloat = []; kfloat = []
for p in paths:
    d = read_all(p); pos = 0
    n = struct.unpack_from("<h", d, pos)[0]; pos += 2; tracks[n] += 1
    for t in range(n):
        a, b, c, m, k = struct.unpack_from("<BBHHH", d, pos); pos += 8
        b0[a] += 1; b1[b] += 1; w2[c] += 1; groups[m] += 1; keys[k] += 1
        for g in range(m):
            rec = d[pos:pos + 28]; pos += 28
            g4[struct.unpack_from("<I", rec, 0x18)[0]] += 1
            gfloat.append(struct.unpack_from("<7f", rec, 0))
            for q in range(k):
                kr = d[pos:pos + 28]; pos += 28
                k0[struct.unpack_from("<I", kr, 0)[0]] += 1
                kfloat.append(struct.unpack_from("<7f", kr, 0))
    exact += pos == len(d)
print("walk ends at the file size:", exact, "of", len(paths))
print("tracks per file:", sorted(tracks.items()))
print("track byte0:", sorted(b0.items()), "; byte1:", sorted(b1.items()))
print("track word2 (top):", mc(w2, 12))
nz = [v for v in w2 if v]
print("track word2 non-zero:", sum(w2[v] for v in nz), "tracks, range", min(nz), "..", max(nz), "; distinct values:", len(nz))
print("groupCount:", sorted(groups.items()), "; keyCount:", sorted(keys.items()))
print("group record +0x18 u32 (top):", mc(g4, 6), "; key record +0x00 u32 (top):", mc(k0, 6))
print("group record as 7 f32, first three:", [tuple(round(x, 3) for x in r) for r in gfloat[:3]])
print("key record as 7 f32, first three:", [tuple(round(x, 3) for x in r) for r in kfloat[:3]])
lst = [p for p in names if p.lower().endswith("add_motion/add_motion_list.txt")]
if lst:
    txt = read_all(lst[0]).decode("latin1").split()
    shipped = {p.split("/")[-1][:-4].lower() for p in paths}
    print("add_motion_list.txt entries:", len(txt), txt[:8])
    print("  listed with a shipped <name>.adm:", sum(1 for t in txt if t.lower() in shipped),
          "; with <name>_town.adm:", sum(1 for t in txt if t.lower() + "_town" in shipped),
          "; shipped files not listed:", sorted(s for s in shipped if s not in {t.lower() for t in txt} and s[:-5] not in {t.lower() for t in txt}))
