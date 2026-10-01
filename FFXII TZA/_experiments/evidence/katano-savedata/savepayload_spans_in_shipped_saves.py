"""SavePayload's four unobserved spans read from the sixteen SHIPPED saves, not from the code.

A code census answers "does any instruction resolve here". For a SERIALISED FORMAT that is the
weaker question: the bytes themselves are shipped, and the game's own VBF carries sixteen saves at
ps2data/image/ff12/katano/ff12savedataNN.sav. The AQ18 row already used them for one span; these
are the other four, which together are 12,000 bytes - the largest single non-Phyre structural debt
in the store.

THE MAPPING, from the save-image page: image offset = payload offset + 0x200 (payload +0x1044 is
image +0x1244). IT DOES NOT REACH EVERY SPAN, and that is a result rather than an obstacle: the
full saves are 57,864 bytes (0xE208), while SavePayload is 0x56490, so a span can sit past the end
of the on-disk image entirely.

CONTROL, because a read that silently returns zeros looks exactly like a span that is zero: the
area id at image +0x1244 must come back DISTINCT per file. That is the same control the AQ18 row
used, and it catches a decode that produced nothing.
"""
import collections, io, os, struct, sys, zlib

KIT = r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts"
sys.path.insert(0, KIT)
from census_format_magics import load_index

VBF = os.environ.get("FF12_VBF") or \
    r"D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FFXII_TZA.vbf"
BLOCK = 0x10000
PAY2IMG = 0x200
SPANS = [("unobservedSpan1538",  0x1538, 2760),
         ("unobservedSpanC818",  0xC818, 6120),
         ("unobservedSpanE004",  0xE004,   60),
         ("unobservedTail5589C", 0x5589C, 3060)]

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
    return out


paths = sorted(p for p in names if p.lower().endswith(".sav"))
print("control: .sav entries in the archive: %d (published 16)" % len(paths))
saves = [(os.path.basename(p), read_all(p)) for p in paths]

areas = {}
for nm, b in saves:
    areas[nm] = struct.unpack_from("<I", b, 0x1244)[0] if len(b) >= 0x1248 else None
distinct = len({v for v in areas.values() if v is not None})
print("control: area id at image +0x1244 is distinct in %d of %d readable files"
      % (distinct, sum(1 for v in areas.values() if v is not None)))
print("         sample:", ", ".join("%s=%08X" % (n, v) for n, v in list(areas.items())[:5] if v is not None))
if distinct < 3:
    sys.exit("CONTROL FAILED - the files did not decode; every result below would be meaningless")
print()

for nm, off, ln in SPANS:
    lo = off + PAY2IMG
    hi = lo + ln
    print("%-22s payload+0x%05X -> image 0x%05X..0x%05X (%d bytes)" % (nm, off, lo, hi, ln))
    inside = outside = partial = 0
    nonzero_files = []
    bytesets = collections.Counter()
    for fname, b in saves:
        if len(b) <= lo:
            outside += 1
            continue
        chunk = b[lo:hi]
        if len(chunk) < ln:
            partial += 1
        else:
            inside += 1
        nz = sum(1 for x in chunk if x)
        if nz:
            nonzero_files.append((fname, nz, len(chunk)))
        bytesets.update(set(chunk))
    print("    files fully covering it: %d   partially: %d   ending before it: %d"
          % (inside, partial, outside))
    if inside == 0 and partial == 0:
        print("    -> NOT ON DISK in any shipped save. This span is in-memory payload only.")
    elif not nonzero_files:
        print("    -> ZERO in every file that covers it (%d files). No shipped save uses these bytes."
              % (inside + partial))
    else:
        print("    -> NONZERO in %d file(s):" % len(nonzero_files))
        for fname, nz, tot in nonzero_files[:6]:
            print("         %-22s %d of %d bytes nonzero" % (fname, nz, tot))
        print("       distinct byte values seen across all files: %d" % len(bytesets))
    print()
