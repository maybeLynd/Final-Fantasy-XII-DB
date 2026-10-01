"""The ch/in ATEL control modules (btlctrl, ctrl, evctrl, mapctrl) x (.sbn, .msb, .dbg), and whether this build can name them.

Read-only over FFXII_TZA.vbf (set FF12_VBF) and the executable (set FF12_EXE). For every file: size,
md5, the leading u32 fields; for .sbn the block table (u32 count, u32 offset[count]) checked for
ascending in-bounds offsets and each block's two leading u32; printable-text runs (the embedded
ATEL source text and symbol names). For the executable: occurrences of each module stem as a path
component, of '.sbn' / '.msb' / '.dbg' terminated by NUL, and of the ATEL extension table strings.
Positive control: the extension census lists 8 entries of each extension.
FABLE, 2026-09-12.
"""
import sys, os, io, re, struct, zlib, hashlib, collections
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


for ext in ("sbn", "msb", "dbg"):
    paths = sorted(p for p in names if p.lower().endswith("." + ext))
    print("== .%s: %d entries" % (ext, len(paths)))
    digests = collections.defaultdict(list)
    for p in paths:
        d = read_all(p)
        md5 = hashlib.md5(d).hexdigest()[:12]
        digests[p.split("/")[-1]].append((p.split("/")[3], md5))
        text = [m.group().decode() for m in re.finditer(rb"[\x20-\x7e]{6,}", d)]
        row = "%-28s %7d B  md5 %s  head %s  text runs %d" % ("/".join(p.split("/")[3:]), len(d), md5, d[:16].hex(" "), len(text))
        if ext == "sbn":
            n = struct.unpack_from("<I", d, 0)[0]
            offs = list(struct.unpack_from("<%dI" % n, d, 4))
            good = offs[0] == 4 * (n + 1) and offs == sorted(offs) and offs[-1] < len(d)
            lead = [struct.unpack_from("<II", d, o) for o in offs]
            row += "  blocks %d at %s ok=%s lead %s" % (n, [hex(o) for o in offs], good, lead)
        print(row)
        if ext == "dbg":
            print("    first text runs:", text[:6])
        if ext == "sbn":
            inc = [t for t in text if t.startswith("#include") or t.startswith("#macro")]
            print("    #include/#macro lines:", len(inc), inc[:3])
    print("  ch copy == in copy for every module:", all(len(set(m for _, m in v)) == 1 for v in digests.values()))
exe = open(os.environ["FF12_EXE"], "rb").read()
for stem in (b"btlctrl", b"evctrl", b"mapctrl", b"systemctrl"):
    print("executable: %r occurs %d times" % (stem, exe.lower().count(stem)))
print("executable: path component '\\\\ctrl.' occurs", len(re.findall(rb"[\\/]ctrl\.", exe, re.I)), "times")
for e in (b".sbn\x00", b".msb\x00", b".dbg\x00"):
    print("executable: %r occurs %d times" % (e, exe.count(e)))
m = exe.find(b"bin\x00dbg\x00sbn\x00msb\x00msf\x00fnt\x00cam\x00")
print("executable: ATEL extension table 'bin dbg sbn msb msf fnt cam' present at file offset", hex(m) if m >= 0 else None)
