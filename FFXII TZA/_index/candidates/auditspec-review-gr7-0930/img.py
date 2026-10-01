"""img.py - SWE2-AUDIT-SPEC minimal loader for the GR-7 review (pefile + capstone; sha256 asserted).
Canonical VAs (image base 0x120000 included). `python img.py dis START END` prints a linear decode."""
import hashlib, struct, sys, os
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "work",
                                   "exe", "FFXII_TZA.exe"))
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "image hash mismatch"
pe = pefile.PE(data=raw, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), IB + s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData,
         bool(s.Characteristics & 0x20000000)) for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def off(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def rd(va, n):
    o = off(va)
    return raw[o:o + n]


u8 = lambda a: rd(a, 1)[0]
u32 = lambda a: struct.unpack("<I", rd(a, 4))[0]
s32 = lambda a: struct.unpack("<i", rd(a, 4))[0]


def dis(start, end):
    o = off(start)
    return list(md.disasm(raw[o:o + (end - start)], start))


def pdata():
    """.pdata function starts (canonical VAs) with their end."""
    for n, v, vs, p, rs, x in SECS:
        if n == ".pdata":
            out = []
            for k in range(0, min(vs, rs) // 12):
                b, e, u = struct.unpack_from("<III", raw, p + 12 * k)
                if b:
                    out.append((IB + b, IB + e))
            return out
    return []


if __name__ == "__main__":
    if sys.argv[1] == "dis":
        for i in dis(int(sys.argv[2], 16), int(sys.argv[3], 16)):
            print("%08X  %-8s %s" % (i.address, i.mnemonic, i.op_str))
