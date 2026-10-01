"""Every .ta in the archive, checked against what the parser 001A8BA0 and the loop 001A7D50 / 001A9770 assume.

Read-only over FFXII_TZA.vbf (set FF12_VBF). Checks:
  * separators: the parser advances strlen(token) + 2 after each sscanf("%s") (001A8C8F), so a
    one-byte separator would eat the next token's first character -- are all separators CRLF?
  * one un-numbered token (frame 0) and "_pic_N" tokens (frame N, decimal after "_pic_", 001A8EB1)
  * the loader requests <map>_anime_0, _1, ... and stops at the first missing index -- are the
    shipped indices contiguous from 0 per map directory?
  * every listed path: does it name a .dds.phyre that exists in the archive (case-insensitive), either
    directly or through the logical -> physical pairs of shared/phyremaps.txt, which the parser's
    remap lookup 001A9940 is built from (its path string 008F6530)?
Positive control: the extension census in ASSET-FORMATS.md lists 45 .ta entries.
FABLE, 2026-09-12.
"""
import sys, os, io, re, zlib, collections
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


tas = sorted(p for p in names if p.lower().endswith(".ta"))
print("control: .ta entries in the archive index:", len(tas), "(published 45)")
remap = {}
pm = read_all("gamedata/d3d11/artdata/shared/phyremaps.txt").split()
for i in range(0, len(pm) - 1, 2):
    remap[pm[i].decode("ascii", "replace").lower()] = pm[i + 1].decode("ascii", "replace").lower()
print("phyremaps.txt: %d tokens, %d pairs" % (len(pm), len(remap)))
C = collections.Counter
direct = mapped = 0
seps = C(); frames = C(); base = C(); contiguous = 0; missing = []; dirs = C(); tokens = 0
per_map = collections.defaultdict(list)
for p in tas:
    d = read_all(p)
    other_ws = re.sub(rb"\r\n", b"", d)
    seps["only CRLF between tokens" if not re.search(rb"[\r\n\t ]", other_ws) else "other whitespace present"] += 1
    seps["ends with CRLF" if d.endswith(b"\r\n") else "no trailing CRLF"] += 1
    toks = d.split()
    tokens += len(toks)
    m = re.match(r"(.*)/([a-z0-9]+)_anime_(\d+)_d3d11\.ta$", p)
    per_map[(m.group(1), m.group(2))].append(int(m.group(3)))
    nums = []; nb = 0
    for t in toks:
        s = t.decode("ascii")
        k = re.search(r"_pic_(\d+)", s)
        if k:
            nums.append(int(k.group(1)))
        else:
            nb += 1
        key = s.lower()
        if key.lstrip("/") in lower:
            direct += 1
        elif key in remap and remap[key].lstrip("/") in lower:
            mapped += 1
        else:
            missing.append((p, s))
        dirs["listed path is under this map's tex/ folder" if s.lower().startswith("/gamedata/d3d11/" + m.group(1)[len("gamedata/d3d11/"):].lower() + "/tex/") else "elsewhere"] += 1
    base[nb] += 1
    contiguous += sorted(nums) == list(range(1, len(nums) + 1))
    frames[len(toks)] += 1
print("separators:", dict(seps))
print("tokens:", tokens, "; frames per file:", sorted(frames.items()))
print("un-numbered (frame 0) tokens per file:", dict(base), "; files whose _pic_ numbers are exactly 1..n:", contiguous)
print("listed paths:", dict(dirs), "; present as listed:", direct, "; present through phyremaps.txt:", mapped, "; unresolved:", len(missing), missing[:5])
print("maps:", len(per_map), "; with more than one list:", {k[1]: sorted(v) for k, v in per_map.items() if len(v) > 1})
print("anime indices contiguous from 0 in every map:", all(sorted(v) == list(range(len(v))) for v in per_map.values()))
