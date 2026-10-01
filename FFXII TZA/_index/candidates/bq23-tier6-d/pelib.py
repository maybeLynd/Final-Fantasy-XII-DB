"""Minimal section-aware PE reader + capstone helpers for the regex identification task."""
import struct, re, csv
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

import pathlib as _pl
_ROOT = _pl.Path(__file__).resolve().parents[5]
EXE = str(_ROOT / "Database/Tools/work/exe/FFXII_TZA.exe")
FUNCS = str(_ROOT / "Database/Tools/work/graph/functions.tsv")


class Image:
    def __init__(self, path=EXE):
        self.pe = pefile.PE(path, fast_load=True)
        self.data = open(path, "rb").read()
        self.base = self.pe.OPTIONAL_HEADER.ImageBase
        self.secs = []
        for s in self.pe.sections:
            name = s.Name.rstrip(b"\0").decode()
            self.secs.append((name, s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData))
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = False

    def sec_of(self, va):
        rva = va - self.base
        for name, v, vs, p, ps in self.secs:
            if v <= rva < v + max(vs, ps):
                return name
        return None

    def off(self, va):
        """file offset for a VA; None if outside raw data (virtual tail)."""
        rva = va - self.base
        for name, v, vs, p, ps in self.secs:
            if v <= rva < v + max(vs, ps):
                d = rva - v
                if d >= ps:
                    return None
                return p + d
        return None

    def va_of_off(self, off):
        for name, v, vs, p, ps in self.secs:
            if p <= off < p + ps:
                return self.base + v + (off - p)
        return None

    def read(self, va, n):
        o = self.off(va)
        if o is None:
            return b"\0" * n
        return self.data[o:o + n]

    def q(self, va):
        return struct.unpack("<Q", self.read(va, 8))[0]

    def d(self, va):
        return struct.unpack("<I", self.read(va, 4))[0]

    def cstr(self, va, maxlen=256):
        b = self.read(va, maxlen)
        return b.split(b"\0")[0].decode("latin1")

    def sec_range(self, name):
        for n, v, vs, p, ps in self.secs:
            if n == name:
                return p, p + ps, self.base + v
        raise KeyError(name)

    def disasm(self, va, size):
        return list(self.md.disasm(self.read(va, size), va))


def load_sizes():
    sizes = {}
    with open(FUNCS, newline="") as f:
        r = csv.reader(f, delimiter="\t")
        next(r)
        for row in r:
            try:
                sizes[int(row[0], 16)] = int(row[2])
            except (ValueError, IndexError):
                pass
    return sizes


def rip_target(ins):
    """return absolute target of [rip + X] operand, or None."""
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+|\d+)\]", ins.op_str)
    if not m:
        return None
    disp = int(m.group(2), 0)
    if m.group(1) == "-":
        disp = -disp
    return ins.address + ins.size + disp


def branch_target(ins):
    if ins.mnemonic in ("call", "jmp") or ins.mnemonic.startswith("j"):
        try:
            return int(ins.op_str, 16)
        except ValueError:
            return None
    return None


def rtti(img):
    """Resolve MSVC x64 RTTI: returns dict vtable_va -> (class name, COL va), and name->type descriptor va."""
    data = img.data
    tds = {}
    for m in re.finditer(rb"\.\?A[VU][A-Za-z0-9_@?$<>]+@@\0", data):
        s_off = m.start()
        td_va = img.va_of_off(s_off - 0x10)
        if td_va is None:
            continue
        tds[td_va] = m.group(0)[:-1].decode()
    # COLs: signature=1, then offset, cdOffset, pTypeDescriptor(rva), pClassHierarchy(rva), pSelf(rva)
    rp0, rp1, rva0 = img.sec_range(".rdata")
    cols = {}
    buf = data[rp0:rp1]
    td_rvas = {va - img.base: va for va in tds}
    for i in range(0, len(buf) - 24, 4):
        sig, off_, cdo, ptd, pch, pself = struct.unpack_from("<IIIIII", buf, i)
        if sig == 1 and ptd in td_rvas:
            col_va = rva0 + i
            if pself == col_va - img.base:
                cols[col_va] = (tds[td_rvas[ptd]], off_)
    # vtables: qword == COL va, followed by code pointers
    vt = {}
    col_set = set(cols)
    for i in range(0, len(buf) - 8, 8):
        v = struct.unpack_from("<Q", buf, i)[0]
        if v in col_set:
            vt[rva0 + i + 8] = (cols[v][0], v, cols[v][1])
    # also unaligned (rare) -- skip
    return tds, cols, vt
