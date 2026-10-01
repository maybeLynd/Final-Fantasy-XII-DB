"""The two extensionless archive entries: ps2data/square_ff12/ff12config and ps2data/debglobal.bin/file1.

Read-only over FFXII_TZA.vbf (set FF12_VBF) and the executable (set FF12_EXE).
1. Prints both files' sizes and nonzero bytes, and the FF12CONFIG bytes 00408C30 copies (file offset -> global).
2. Searches .text for RIP-relative references to the two path literals "PS2Data/SQUARE_FF12/FF12CONFIG"
   and "PS2Data\\DebGlobal.bin": every 4-byte displacement d at file offset o with VA(o) + 4 + k + d == target
   for k in 0..4 (the instruction bytes after the displacement), reported per target. Positive controls: the
   FF12CONFIG literal (referenced by 00408C88) and the double at 00D22C50 next to the DebGlobal literal
   (referenced by 0051E03C).
FABLE, 2026-09-13.
"""
import sys, os, io, struct, zlib
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
    assert len(out) == size
    return out


none = sorted(p for p in names if "." not in p.rsplit("/", 1)[-1])
print("control: extensionless entries:", len(none), "(published 2):", none)
for p in none:
    d = read_all(p)
    if p.endswith("file1"):
        print(p, len(d), "bytes; as 16-byte NUL-padded strings:", [d[i:i + 16].split(bytes(1))[0].decode("latin1") for i in range(0, len(d), 16)])
    else:
        print(p, len(d), "bytes; nonzero:", [(hex(i), d[i]) for i in range(len(d)) if d[i]][:40])
cfg = read_all("ps2data/square_ff12/ff12config")
COPY = [(0x02, 1, "02B62DA8", 3), (0x03, 1, "02B62DA9", 0), (0x04, 1, "02B62DAA", 0), (0x06, 1, "02B62DAC", 0),
        (0x08, 1, "02B62DAE", 0), (0x09, 1, "02B62DAF", 1), (0x0A, 2, "02B62DB4", 0), (0x0C, 1, "02B62DB0", 0),
        (0x0D, 1, "02B62DB1", 0), (0x0E, 1, "02B62DB2", 0), (0x0F, 1, "02B62DB3", 0), (0x10, 1, "02B62DB6", 0),
        (0x11, 1, "02B62DB7", 0), (0x12, 1, "02B62DB8", 0), (0x15, 1, "02B62DBB", None), (0x16, 1, "02B62DBC", 0)]
for off, w, g, dflt in COPY:
    v = cfg[off] if w == 1 else struct.unpack_from("<H", cfg, off)[0]
    print("  file +0x%02X (%s) -> %s : shipped %d, default from 00408BA0 %s" % (off, "u8" if w == 1 else "u16", g, v, dflt))
copied = set()
for off, w, g, dflt in COPY:
    copied.update(range(off, off + w))
print("  nonzero bytes not copied:", [hex(i) for i in range(len(cfg)) if cfg[i] and i not in copied])

exe = open(os.environ["FF12_EXE"], "rb").read()
pe = struct.unpack_from("<I", exe, 0x3C)[0]
nsec = struct.unpack_from("<H", exe, pe + 6)[0]; opt = struct.unpack_from("<H", exe, pe + 20)[0]
base = struct.unpack_from("<Q", exe, pe + 24 + 24)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + 40 * i
    nm = exe[o:o + 8].rstrip(b"\0"); vs, va, rs, ra = struct.unpack_from("<IIII", exe, o + 8)
    secs.append((nm, va, vs, rs, ra))


def va_of(off):
    for nm, va, vs, rs, ra in secs:
        if ra <= off < ra + rs:
            return base + va + off - ra


def off_of(v):
    for nm, va, vs, rs, ra in secs:
        if va <= v - base < va + rs:
            return ra + v - base - va


targets = {}
for lit in (b"PS2Data/SQUARE_FF12/FF12CONFIG\0", b"PS2Data\\DebGlobal.bin\0"):
    targets[lit.decode().rstrip("\0")] = va_of(exe.find(lit))
targets["control: double at 00D22C50"] = 0x00D22C50
text = [s for s in secs if s[0] == b".text"][0]
tva = base + text[1]; traw = text[4]; tsize = text[3]
disp = memoryview(exe)[traw:traw + tsize]
for name, tgt in targets.items():
    hits = []
    for k in range(5):
        for o in range(0, tsize - 4):
            d = struct.unpack_from("<i", disp, o)[0]
            if tva + o + 4 + k + d == tgt:
                hits.append(tva + o)
    print("RIP-relative candidates for %s at %08X: %d %s" % (name, tgt, len(hits), ["%08X" % h for h in sorted(set(hits))[:6]]))
