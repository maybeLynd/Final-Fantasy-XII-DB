"""img45.py - SWE2-AUDIT-SPEC independent image loader for the GR-4/GR-5 review (2026-09-30).

pefile + capstone over the certified image (sha256 asserted). Canonical VAs (image base 0x120000 already included).
Nothing from the reviewed package or the kit is imported here.
"""
import hashlib, struct, os
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


def off(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def rd(va, n):
    o = off(va)
    return raw[o:o + n] if o is not None else None


def q(va):
    return struct.unpack("<Q", rd(va, 8))[0]


def d32(va):
    return struct.unpack("<I", rd(va, 4))[0]


def dis(start, end):
    o = off(start)
    return list(md.disasm(raw[o:o + (end - start)], start))


def text_secs():
    return [(n, v, vs, p, rs) for n, v, vs, p, rs, x in SECS if x]


def pdata():
    """(begin, end) of every .pdata RUNTIME_FUNCTION, canonical VAs"""
    for n, v, vs, p, rs, x in SECS:
        if n == ".pdata":
            out = []
            for k in range(0, min(vs, rs), 12):
                b, e, u = struct.unpack_from("<III", raw, p + k)
                if b:
                    out.append((IB + b, IB + e))
            return out
    return []


def relocs():
    """set of VAs carrying a DIR64 relocation"""
    pe2 = pefile.PE(data=raw, fast_load=True)
    pe2.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_BASERELOC"]])
    s = set()
    for blk in getattr(pe2, "DIRECTORY_ENTRY_BASERELOC", []):
        for e in blk.entries:
            if e.type == 10:
                s.add(IB + e.rva)
    return s


import numpy as _np
_TX = {}


def _text_np():
    if not _TX:
        n, v, vs, p, rs = text_secs()[0]
        b = _np.frombuffer(raw[p:p + min(vs, rs)], dtype=_np.uint8)
        L = len(b)
        d = _np.zeros(L, dtype=_np.int64)
        d[:L - 3] = (b[:L - 3].astype(_np.int64) | (b[1:L - 2].astype(_np.int64) << 8) |
                     (b[2:L - 1].astype(_np.int64) << 16) | (b[3:L].astype(_np.int64) << 24))
        d = _np.where(d >= 1 << 31, d - (1 << 32), d)
        _TX.update(v=v, b=b, d=d, L=L)
    return _TX


def raw_rel32_sites(target):
    """E8/E9 and 0F 8x rel32 sites whose destination is target (raw byte scan of .text)"""
    t = _text_np()
    v, b, d, L = t["v"], t["b"], t["d"], t["L"]
    idx = _np.arange(L, dtype=_np.int64)
    out = []
    m1 = _np.zeros(L, dtype=bool)
    m1[:L - 5] = ((b[:L - 5] == 0xE8) | (b[:L - 5] == 0xE9)) & (v + idx[:L - 5] + 5 + d[1:L - 4] == target)
    for k in _np.nonzero(m1)[0]:
        out.append((v + int(k), "E8" if b[k] == 0xE8 else "E9"))
    m2 = _np.zeros(L, dtype=bool)
    m2[:L - 6] = (b[:L - 6] == 0x0F) & (b[1:L - 5] >= 0x80) & (b[1:L - 5] <= 0x8F) & (v + idx[:L - 6] + 6 + d[2:L - 4] == target)
    for k in _np.nonzero(m2)[0]:
        out.append((v + int(k), "0F%02X" % b[k + 1]))
    return sorted(out)


def disp_candidates(lo, hi, ib=0x120000):
    """offsets k in .text where the dword at k is a rip disp (next-ip + d in [lo,hi), tail imm 0..4) or an
    image-base-relative disp (d + ib in [lo,hi))"""
    t = _text_np()
    v, d, L = t["v"], t["d"], t["L"]
    idx = _np.arange(L, dtype=_np.int64)
    m = (d + ib >= lo) & (d + ib < hi)
    kinds = {int(k): "ib" for k in _np.nonzero(m)[0]}
    for tail in (0, 1, 2, 4):
        g = v + idx + 4 + tail + d
        for k in _np.nonzero((g >= lo) & (g < hi))[0]:
            kinds.setdefault(int(k), "rip")
    return kinds


def abs64_sites(lo, hi):
    """every 8-byte-aligned or unaligned qword in any section whose value is in [lo, hi]"""
    out = []
    lob, hib = lo, hi
    for n, v, vs, p, rs, x in SECS:
        blob = raw[p:p + min(vs, rs)]
        for k in range(0, len(blob) - 7):
            val = struct.unpack_from("<Q", blob, k)[0]
            if lob <= val <= hib:
                out.append((n, v + k, val))
    return out
