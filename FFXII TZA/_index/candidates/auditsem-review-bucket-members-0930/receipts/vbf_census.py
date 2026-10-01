"""SWE2-AUDIT-SEM independent census of .bin/.dat entries in the installed VBF.
Reads the archive index with agent_flow/tools/vbfextract.py's loader and decompresses
only the first block of each .bin/.dat entry to take its leading 4 bytes.
Output: vbf_bin_dat.tsv (path, ext, size, lead4hex) + a summary on stdout."""
import sys, os, zlib, collections, hashlib
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools")
import vbfextract as V
VBF = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vbf_bin_dat.tsv")

def first_bytes(f, names, blocks, path, n=64):
    sb, size, off = names[path]
    if size == 0:
        return b""
    nblocks = (size + V.BLOCK - 1) // V.BLOCK
    csize = blocks[sb] or V.BLOCK
    expected = V.BLOCK if nblocks > 1 else size
    f.seek(off)
    data = f.read(csize)
    if csize != expected:
        try:
            data = zlib.decompressobj().decompress(data)
        except zlib.error:
            pass
    return data[:n]

with open(VBF, "rb") as f:
    names, blocks = V.load_index(f)
    print("total entries", len(names))
    rows = []
    for p in sorted(names):
        ext = os.path.splitext(p)[1].lower()
        if ext not in (".bin", ".dat"):
            continue
        sb, size, off = names[p]
        fb = first_bytes(f, names, blocks, p)
        rows.append((p, ext[1:], size, fb[:4].hex()))
with open(OUT, "w", encoding="utf-8", newline="\n") as o:
    o.write("path\text\tsize\tlead4\n")
    for r in rows:
        o.write("%s\t%s\t%d\t%s\n" % r)
c = collections.Counter(r[1] for r in rows)
print("by ext", dict(c))
for e in ("bin", "dat"):
    sig = collections.Counter(r[3] for r in rows if r[1] == e)
    print(e, "distinct lead4:", len(sig))
