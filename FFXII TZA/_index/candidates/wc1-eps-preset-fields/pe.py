"""Section-aware PE reader for FFXII_TZA.exe (image base 0x120000). VA -> file offset via section raw sizes."""
import struct
from pathlib import Path
EXE = Path(__file__).resolve().parents[4] / "Tools/work/exe/FFXII_TZA.exe"
BASE = 0x120000
d = open(EXE, "rb").read()
_pe = struct.unpack_from("<I", d, 0x3C)[0]
_n = struct.unpack_from("<H", d, _pe + 6)[0]
_opt = struct.unpack_from("<H", d, _pe + 20)[0]
secs = []
for i in range(_n):
    o = _pe + 24 + _opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(), *struct.unpack_from("<IIII", d, o + 8)))  # name, vsize, va, rawsize, rawofs


def off(va):
    for n, vs, sva, rs, ro in secs:
        if BASE + sva <= va < BASE + sva + vs:
            r = va - BASE - sva
            return ro + r if r < rs else None  # None = virtual tail (zero-initialised)
    raise ValueError("VA %08X outside image" % va)


def sec(va):
    for n, vs, sva, rs, ro in secs:
        if BASE + sva <= va < BASE + sva + vs:
            return n


def rd(va, fmt):
    o = off(va)
    if o is None:
        return struct.unpack(fmt, bytes(struct.calcsize(fmt)))
    return struct.unpack_from(fmt, d, o)


def f32(va): return rd(va, "<f")[0]
def u32(va): return rd(va, "<I")[0]
def u64(va): return rd(va, "<Q")[0]


if __name__ == "__main__":
    import sys
    # control: .rdata tag table string 'scnf' at 01CB4928 per the page
    print("control 01CB4928 (%s) = %r" % (sec(0x01CB4928), d[off(0x01CB4928):off(0x01CB4928) + 44]))
    for a in sys.argv[1:]:
        va = int(a, 16)
        print("%08X %s u32=%08X f32=%g" % (va, sec(va), u32(va), f32(va)))
