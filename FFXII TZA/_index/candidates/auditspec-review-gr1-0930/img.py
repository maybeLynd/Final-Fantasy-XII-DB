"""img.py - SWE2-AUDIT-SPEC minimal image loader for the GR-1 review (pefile + capstone only, sha asserted).
Canonical VAs (image base 0x120000 included). `python img.py START END` prints a linear disassembly."""
import hashlib, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "image hash mismatch"
pe = pefile.PE(data=raw, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), IB + s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData,
         bool(s.Characteristics & 0x20000000)) for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def rd(va, n):
    """section-aware read; bytes past SizeOfRawData (inside VirtualSize) read as zero."""
    for _, v, vs, p, rs, _x in SECS:
        if v <= va < v + vs:
            o = va - v
            b = raw[p + o:p + min(o + n, rs)] if o < rs else b""
            return b + b"\0" * (n - len(b))
    return None


def q(a):
    return struct.unpack("<Q", rd(a, 8))[0]


def d32(a):
    return struct.unpack("<i", rd(a, 4))[0]


def dis(a, n=0x100):
    return list(md.disasm(rd(a, n), a))


def pdata():
    """.pdata RUNTIME_FUNCTION begin VAs (sorted, unique)."""
    for n, v, vs, p, rs, x in SECS:
        if n == ".pdata":
            out = set()
            for k in range(0, min(vs, rs) - 11, 12):
                b, e, u = struct.unpack("<III", raw[p + k:p + k + 12])
                if b:
                    out.add((IB + b, IB + e))
            return sorted(out)
    return []


if __name__ == "__main__":
    s, e = int(sys.argv[1], 16), int(sys.argv[2], 16)
    for i in dis(s, e - s):
        print("%08X  %-7s %s" % (i.address, i.mnemonic, i.op_str))
