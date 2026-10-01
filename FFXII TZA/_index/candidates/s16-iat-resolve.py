"""Resolve IAT slots to (dll, name) from the PE import directory. usage: iat.py VA [VA...]"""
import struct
import sys

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
raw = open(EXE, "rb").read()
pe = struct.unpack_from("<I", raw, 0x3C)[0]
base = struct.unpack_from("<Q", raw, pe + 48)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs = []
off = pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va, max(vs, rs), ra))
    off += 40


def r2o(rva):
    for va, sz, ra in secs:
        if va <= rva < va + sz:
            return ra + rva - va
    raise KeyError(hex(rva))


imp_rva, imp_sz = struct.unpack_from("<II", raw, pe + 24 + 112 + 8)   # data directory 1 (PE32+)
slots = {}
d = r2o(imp_rva)
while True:
    oft, ts, fc, name, ft = struct.unpack_from("<IIIII", raw, d)
    if not (oft or name or ft):
        break
    dll = raw[r2o(name):raw.index(b"\0", r2o(name))].decode()
    th = r2o(oft or ft)
    i = 0
    while True:
        e = struct.unpack_from("<Q", raw, th + 8 * i)[0]
        if e == 0:
            break
        if e >> 63:
            nm = "#%d" % (e & 0xFFFF)
        else:
            o = r2o(e & 0x7FFFFFFF) + 2
            nm = raw[o:raw.index(b"\0", o)].decode()
        slots[base + ft + 8 * i] = (dll, nm)
        i += 1
    d += 20
print("image base %X, %d IAT slots" % (base, len(slots)))
for a in sys.argv[1:]:
    va = int(a, 16)
    print("%08X -> %s" % (va, slots.get(va, "NOT AN IAT SLOT")))
