"""uq218 helpers: section-aware exe reads, disasm-cache access, .cm corpus walker."""
import os, struct, glob, bisect
import pefile

SCR = os.path.dirname(os.path.abspath(__file__))
Y1P = os.path.join(os.path.dirname(SCR), 'y1p_all.txt')
EXE = os.path.join(SCR, '..', '..', '..', '..', 'Tools', 'work', 'exe', 'FFXII_TZA.exe')   # repo-relative from _index/candidates/<record>
CORPUS = r'D:/FFXII_TZA_extract/ps2data/obj_finish/in'

_pe = None
_data = None
def pe():
    global _pe, _data
    if _pe is None:
        _pe = pefile.PE(EXE, fast_load=True)
        _data = open(EXE, 'rb').read()
    return _pe

def va2off(va):
    p = pe()
    base = p.OPTIONAL_HEADER.ImageBase
    rva = va - base
    for s in p.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            d = rva - s.VirtualAddress
            if d >= s.SizeOfRawData:
                return None  # virtual tail, zero-init
            return s.PointerToRawData + d
    raise ValueError(hex(va))

def rd(va, n):
    o = va2off(va)
    if o is None:
        return b'\0' * n
    pe()
    return _data[o:o + n]

def u32(va): return struct.unpack('<I', rd(va, 4))[0]
def u16(va): return struct.unpack('<H', rd(va, 2))[0]
def f32(va): return struct.unpack('<f', rd(va, 4))[0]
def u64(va): return struct.unpack('<Q', rd(va, 8))[0]

_lines = None
def lines():
    global _lines
    if _lines is None:
        _lines = open(Y1P, encoding='utf-8', errors='replace').read().splitlines()
    return _lines

_idx = None
def func_lines(func):
    """all cache lines whose FUNC column == func (hex string, 8 upper)"""
    func = func.upper().rjust(8, '0')
    out = []
    for l in lines():
        if l[9:17] == func:
            out.append(l)
    return out

def cm_files():
    fs = sorted(glob.glob(CORPUS + '/**/*.cm', recursive=True))
    return fs

def find_entries(b):
    """Return dict tag->list of (off) for '@Fxx' tags in blob, validated by kind/len fields."""
    res = {}
    i = 0
    n = len(b)
    while True:
        j = b.find(b'@F', i)
        if j < 0 or j + 16 > n:
            break
        tag = b[j:j + 4]
        if all(0x41 <= c <= 0x5A for c in tag[2:4]):
            res.setdefault(tag.decode('ascii'), []).append(j)
        i = j + 1
    return res

def cm_entries(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'@FRP', path
    var, clen, cnt = struct.unpack_from('<III', d, 4)
    base = 0x40 if var == 1 else 0x30
    out = []
    for i in range(cnt):
        o = base + struct.unpack_from('<I', d, base + i * 4)[0]
        out.append((d[o:o + 4].decode('latin1'), o))
    return d, out

def entry(d, o):
    elen = struct.unpack_from('<I', d, o + 8)[0]
    return d[o:o + elen]
