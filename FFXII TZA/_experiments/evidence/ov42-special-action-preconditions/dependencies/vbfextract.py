"""Selective extractor for FFXII_TZA.vbf (SRYK format). Usage:
   python vbfextract.py [--vbf <archive>] <internal-path> <out-file>
   python vbfextract.py [--vbf <archive>] --find <substring>  (list matching paths)

The archive can also be supplied through ``FFXII_VBF``.  The historical install
path remains the final fallback so older research commands continue to work.
"""
import struct, sys, zlib, os

DEFAULT_VBF = r"D:\Final Fantasy XII The Zodiac Age\FFXII_TZA.vbf"
BLOCK = 0x10000

def load_index(f):
    magic, headerLen = struct.unpack("<4sI", f.read(8))
    assert magic == b"SRYK"
    (numFiles,) = struct.unpack("<Q", f.read(8))
    entries_off = 0x10 + numFiles * 16
    f.seek(entries_off)
    raw = f.read(0x20 * numFiles)
    entries = []
    for i in range(numFiles):
        sb, sb2, size, off, noff = struct.unpack_from("<IIQQQ", raw, i * 0x20)
        entries.append((sb, size, off, noff))
    strtab_off = entries_off + 0x20 * numFiles
    f.seek(strtab_off)
    (strLen,) = struct.unpack("<I", f.read(4))
    strtab = f.read(strLen)
    blocklist_off = strtab_off + strLen  # strLen includes its own 4-byte prefix
    f.seek(blocklist_off)
    bl_raw = f.read(headerLen - blocklist_off)
    blocks = struct.unpack("<%dH" % (len(bl_raw) // 2), bl_raw)
    names = {}
    for i, (sb, size, off, noff) in enumerate(entries):
        end = strtab.index(b"\0", noff)
        names[strtab[noff:end].decode()] = (sb, size, off)
    return names, blocks

def read_entry(f, names, blocks, path):
    """Return one decompressed archive entry without creating a temporary file."""
    sb, size, off = names[path]
    nblocks = (size + BLOCK - 1) // BLOCK
    out = bytearray()
    pos = off
    for i in range(nblocks):
        csize = blocks[sb + i]
        expected = BLOCK if i < nblocks - 1 else (size - BLOCK * (nblocks - 1))
        if csize == 0:
            csize = BLOCK
        f.seek(pos)
        data = f.read(csize)
        if csize == expected:      # stored raw
            out += data
        else:
            try:
                out += zlib.decompress(data)
            except zlib.error:
                out += data        # fallback: raw
        pos += csize
    assert len(out) == size, (len(out), size)
    return bytes(out)


def extract(f, names, blocks, path, outpath):
    data = read_entry(f, names, blocks, path)
    with open(outpath, "wb") as o:
        o.write(data)
    size = len(data)
    print("extracted", path, "->", outpath, size, "bytes")

def main(argv):
    vbf = os.environ.get("FFXII_VBF", DEFAULT_VBF)
    if argv[:1] == ["--vbf"]:
        if len(argv) < 3:
            raise SystemExit("--vbf requires an archive path and a command")
        vbf, argv = argv[1], argv[2:]

    if len(argv) == 2 and argv[0] == "--find":
        with open(vbf, "rb") as f:
            names, _ = load_index(f)
        for name, (_, size, _) in names.items():
            if argv[1].lower() in name.lower():
                print(name, size)
        return

    if len(argv) != 2:
        raise SystemExit(__doc__)
    with open(vbf, "rb") as f:
        names, blocks = load_index(f)
        extract(f, names, blocks, argv[0], argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])
