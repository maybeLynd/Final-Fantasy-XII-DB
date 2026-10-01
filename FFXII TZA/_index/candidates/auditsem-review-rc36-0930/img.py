"""SWE2-AUDIT-SEM minimal PE mapper for FFXII_TZA.exe (own code, no producer helper).
Addresses in the database are written as the VA minus 0x140000000 when the image base is 0x140000000,
or as the plain VA otherwise; va() accepts the database form."""
import struct, capstone
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
raw = open(EXE, "rb").read()
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
opt = pe + 24
BASE = struct.unpack_from("<Q", raw, opt + 24)[0]
secs = []
for i in range(nsec):
    o = opt + optsz + 40 * i
    name = raw[o:o + 8].rstrip(b"\0").decode()
    vsz, rva, rsz, rptr = struct.unpack_from("<IIII", raw, o + 8)
    secs.append((name, rva, vsz, rptr, rsz))

def off(a):
    """database address -> file offset (None if not file-backed)."""
    r = a - BASE if a >= BASE else a
    for n, rva, vsz, rp, rs in secs:
        if rva <= r < rva + max(vsz, rs):
            return rp + (r - rva) if r - rva < rs else None
    return None

def rd(a, n):
    o = off(a)
    return raw[o:o + n] if o is not None else None

def sec_of(a):
    r = a - BASE if a >= BASE else a
    for n, rva, vsz, rp, rs in secs:
        if rva <= r < rva + max(vsz, rs):
            return n
    return None

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False

def dis(a, n=40, stop_ret=True):
    out = []
    for ins in md.disasm(rd(a, n * 15), a):
        out.append(ins)
        if len(out) >= n or (stop_ret and ins.mnemonic in ("ret", "int3")):
            break
    return out

def text_range():
    for n, rva, vsz, rp, rs in secs:
        if n == ".text":
            return rva, rva + rs, rp
