# FCP tail-section census: sections 0/2/5/6/8/10/18 over all 1,066 .cm @FCP blocks.
# Run: FF12_VBF=<archive> python fcp_tail_sections_census.py
import sys, os, io, struct, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
from census_format_magics import load_index
BLOCK = 0x10000
f = io.open(os.environ["FF12_VBF"], "rb")
names, blocks = load_index(f)
def read_all(p):
    sb, size, off = names[p]; n = (size + BLOCK - 1) // BLOCK
    out = b""; f.seek(off)
    for i in range(n):
        cs = blocks[sb + i] or BLOCK
        exp = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        c = f.read(cs)
        if cs != exp: c = zlib.decompress(c)
        out += c
    return out
def fcp(p):
    d = read_all(p); i = d.find(b"@FCP")
    size = struct.unpack_from("<I", d, i + 8)[0]
    return d[i + 0x30:i + size]

cms = [p for p in names if p.lower().endswith(".cm")]
sec_bytes = collections.defaultdict(list)   # section -> [(file, bytes)]
for p in cms:
    pl = fcp(p)
    offs = list(struct.unpack_from("<19H", pl, 0))
    sp = sorted((o, n) for n, o in enumerate(offs) if o)
    for k, (o, n) in enumerate(sp):
        nxt = sp[k + 1][0] if k + 1 < len(sp) else len(pl)
        sec_bytes[n].append((p, pl[o:nxt]))

def label(p): return p.rsplit("/", 1)[-1]
for n in (2, 6, 18):
    ents = sec_bytes[n]
    print("=== section", n, "present", len(ents), "===")
    print(" sizes:", collections.Counter(len(b) for _, b in ents).most_common(10))
    allzero = sum(1 for _, b in ents if not any(b))
    print(" all-zero:", allzero)
    if n == 6:
        # 16 x 16B records {u32 key, f32, f32, u32}
        keys = collections.Counter(); vals = collections.Counter()
        for _, b in ents:
            for r in range(16):
                key, fa, fb, fc = struct.unpack_from("<IffI", b, r * 16)
                keys[key if key in (0xFFFF, 0) else "id"] += 1
                if key not in (0xFFFF,):
                    vals[(key)] += 1
        print(" record-key value histogram:", vals.most_common(15))
    if n == 18:
        # stride detection
        lanes = collections.Counter()
        nz = 0
        for _, b in ents:
            if any(b): nz += 1
            for i in range(0, len(b), 4):
                lanes[(i % 16, struct.unpack_from("<f", b, i)[0])] += 0
        print(" nonzero sections:", nz)
        # per-16B-lane float pattern on c1004-class
        samp = ents[0][1]
        for i in range(0, min(len(samp), 96), 16):
            print("  lane@%02x" % i, ["%.3g" % struct.unpack_from("<f", samp, i + j)[0] for j in (0, 4, 8, 12)])
    if n == 2:
        nz = sum(1 for _, b in ents if any(b))
        print(" nonzero sections:", nz)
        first = collections.Counter()
        for _, b in ents:
            if len(b) >= 8: first[struct.unpack_from("<I", b, 0)[0]] += 1
        print(" first dword:", first.most_common(10))
