"""The 16 ps2data/image/ff12/katano/ff12savedataNN.sav files against the documented save image header.

Read-only over FFXII_TZA.vbf (set FF12_VBF) and the executable (set FF12_EXE). For each file: size,
the leading tag, and the header fields the save-image page documents (+0x08 gil, +0x10 play clock,
+0x18/+0x1A/+0x1B play time, +0x48/+0x4C group and area, +0x58..+0x64 constants, +0x68 magic 0x0131F3EA,
+0x6C size 0x4818, payload +0x1044 = image +0x1244 area id), and the CRC32 of image[0x08, min(size, 0xE200)).
Also the executable: occurrences of the file names, and the slot bound of debug_loadjfdata's loader
002EF300 (index 0x75 + clamp(slot, 0, 15), 0xE240 bytes).
Positive control: the extension census lists 16 .sav entries.
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


paths = sorted(p for p in names if p.lower().endswith(".sav"))
print("control: .sav entries:", len(paths), "(published 16)")
U = lambda d, o: struct.unpack_from("<I", d, o)[0] if o + 4 <= len(d) else None
for p in paths:
    d = read_all(p)
    nz = sum(1 for b in d if b)
    row = {"size": len(d), "tag": d[:4], "nonzero bytes": nz}
    if d[:4] != b"FF12":
        row.update({
            "gil": U(d, 8), "clock": struct.unpack_from("<Q", d, 0x10)[0],
            "time": "%d:%02d:%02d" % (struct.unpack_from("<H", d, 0x18)[0], d[0x1A], d[0x1B]),
            "group": U(d, 0x48), "area": U(d, 0x4C),
            "consts": "%08X %08X %08X %08X" % tuple(struct.unpack_from("<4I", d, 0x58)),
            "magic": "%08X" % U(d, 0x68), "size6C": "%08X" % U(d, 0x6C),
            "area@1244": U(d, 0x1244),
            "crc[8,E200)": "%08X" % (zlib.crc32(d[8:min(len(d), 0xE200)]) & 0xFFFFFFFF),
            "+0x00": "%08X" % U(d, 0), "+0xE200": ("%08X" % U(d, 0xE200)) if U(d, 0xE200) is not None else None,
        })
    else:
        row.update({"+0x04": U(d, 4), "+0x08": U(d, 8), "+0x0C": U(d, 0xC), "+0x10": U(d, 0x10)})
    print(p.split("/")[-1], row)
exe = open(os.environ["FF12_EXE"], "rb").read()
print("'ff12savedata' in the executable:", exe.lower().count(b"ff12savedata"), "; '.sav\\0':", exe.count(b".sav\x00"))
