"""arena_ix.py - SWE2-AUDIT-SPEC independent image index for the arena-allocator reviews (SD-164..168, 2026-09-30).

pefile + capstone + numpy over the certified image (sha256 asserted); no retool / regval / package code.
Addresses are canonical VAs (image base 0x120000 included).

  off(va), rd(va, n), dis(a, b), ins1(a), txt(a)
  rel32(tgt_set)   -> {tgt: [(site, 'call'|'jmp'|'jcc')]}   raw E8 / E9 / 0F 8x rel32 over every executable section,
                                                             kept only when the bytes decode to that instruction there
  dir64(tgt_set)   -> {tgt: [slot]}                          DIR64 relocation slots whose qword equals a target
  rva32(tgt)       -> [va]                                   raw 4-byte (tgt - IB) occurrences in every section
  rip_refs(lo, hi) -> [(site, mnem, op_str, width, kind)]    rip-relative operands resolving into [lo, hi)
  ib_refs(disp)    -> [(site, mnem, op_str, width, kind)]    memory operands with a non-rip base and displacement == disp
  root(va)         -> .pdata chain root (function start) of a site, or None
kind is 'W' when the memory operand is operand 0 of a writing mnemonic, 'lea', or 'R'.
"""
import bisect, hashlib, struct
import numpy as np
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM
from capstone.x86 import X86_REG_RIP, X86_REG_INVALID

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "image hash mismatch"
pe = pefile.PE(data=raw, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), IB + s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData,
         bool(s.Characteristics & 0x20000000)) for s in pe.sections]
TEXT = [s for s in SECS if s[5]]
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
WRITERS = ("mov", "and", "or", "xor", "add", "sub", "inc", "dec", "set", "xchg", "stos", "cmpxchg", "not", "neg", "shl",
           "shr", "sar", "rol", "ror", "bts", "btr", "btc", "adc", "sbb", "pop")


def off(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def rd(va, n):
    o = off(va)
    return raw[o:o + n] if o is not None else None


def dis(a, b):
    return list(md.disasm(rd(a, b - a), a))


def ins1(a):
    return next(md.disasm(rd(a, 16), a, 1))


def txt(a):
    i = ins1(a)
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def kind_of(i, k):
    if i.mnemonic == "lea":
        return "lea"
    if k == 0 and i.mnemonic.startswith(WRITERS) and not i.mnemonic.startswith(("movzx", "movsx")):
        return "W"
    return "R"


def rel32(tgts):
    tgts = set(tgts)
    out = {t: [] for t in tgts}
    ta = np.array(sorted(tgts), dtype=np.int64)
    for n, v, vs, p, rs, x in TEXT:
        blob = raw[p:p + min(vs, rs)]
        L = len(blob)
        for k0 in range(4):
            arr = np.frombuffer(raw, dtype="<i4", count=(L - k0) // 4, offset=p + k0).astype(np.int64)
            pos = k0 + 4 * np.arange(len(arr), dtype=np.int64)
            tgt = v + pos + 4 + arr
            for j in np.nonzero(np.isin(tgt, ta))[0]:
                q = int(pos[j])
                t = int(tgt[j])
                if q >= 1 and blob[q - 1] in (0xE8, 0xE9):
                    i = next(md.disasm(blob[q - 1:q + 4], v + q - 1, 1), None)
                    if i and i.size == 5:
                        out[t].append((v + q - 1, "call" if blob[q - 1] == 0xE8 else "jmp"))
                if q >= 2 and blob[q - 2] == 0x0F and 0x80 <= blob[q - 1] <= 0x8F:
                    i = next(md.disasm(blob[q - 2:q + 4], v + q - 2, 1), None)
                    if i and i.size == 6:
                        out[t].append((v + q - 2, "jcc"))
    return out


_RELOC = None


def relocs():
    global _RELOC
    if _RELOC is None:
        pe2 = pefile.PE(data=raw, fast_load=True)
        pe2.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_BASERELOC"]])
        m = {}
        for blk in pe2.DIRECTORY_ENTRY_BASERELOC:
            for e in blk.entries:
                if e.type == 10:
                    va = IB + e.rva
                    b = rd(va, 8)
                    if b and len(b) == 8:
                        m.setdefault(struct.unpack("<Q", b)[0], []).append(va)
        _RELOC = m
    return _RELOC


def dir64(tgts):
    r = relocs()
    return {t: sorted(r.get(t, [])) for t in tgts}


def rva32(tgt):
    pat, res = struct.pack("<I", tgt - IB), []
    for n, v, vs, p, rs, x in SECS:
        blob = raw[p:p + min(vs, rs)]
        k = blob.find(pat)
        while k >= 0:
            res.append((v + k, n))
            k = blob.find(pat, k + 1)
    return res


def _decode_back(p, v, k, blob, pred):
    for back in range(10, 0, -1):
        if k - back < 0:
            continue
        i = next(md.disasm(blob[k - back:k - back + 15], v + k - back, 1), None)
        if not i or not (i.address < v + k and v + k + 4 <= i.address + i.size):
            continue
        for j, op in enumerate(i.operands):
            if op.type == CS_OP_MEM and pred(i, op):
                return (i.address, i.mnemonic, i.op_str, op.size, kind_of(i, j))
    return None


def rip_refs(lo, hi):
    hits = set()
    for n, v, vs, p, rs, x in TEXT:
        blob = raw[p:p + min(vs, rs)]
        L = len(blob)
        for k0 in range(4):
            arr = np.frombuffer(raw, dtype="<i4", count=(L - k0) // 4, offset=p + k0).astype(np.int64)
            pos = k0 + 4 * np.arange(len(arr), dtype=np.int64)
            for tail in (0, 1, 2, 4):
                t = v + pos + 4 + tail + arr
                for j in np.nonzero((t >= lo) & (t < hi))[0]:
                    k = int(pos[j])
                    h = _decode_back(p, v, k, blob, lambda i, op: op.mem.base == X86_REG_RIP and lo <= i.address + i.size + op.mem.disp < hi)
                    if h:
                        hits.add(h)
    return sorted(hits)


def ib_refs(disp):
    pat, hits = struct.pack("<i", disp), set()
    for n, v, vs, p, rs, x in TEXT:
        blob = raw[p:p + min(vs, rs)]
        k = blob.find(pat)
        while k >= 0:
            h = _decode_back(p, v, k, blob, lambda i, op: op.mem.base not in (X86_REG_RIP,) and op.mem.disp == disp
                             and not (op.mem.base == X86_REG_INVALID and op.mem.index == X86_REG_INVALID and False))
            if h:
                hits.add(h)
            k = blob.find(pat, k + 1)
    return sorted(hits)


_dd = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
_o = off(IB + _dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", raw, _o + 12 * k) for k in range(_dd.Size // 12))
PST = [e[0] for e in PD]


def pentry(va):
    rva = va - IB
    j = bisect.bisect_right(PST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    return PD[j]


def root(va):
    e = pentry(va)
    if e is None:
        return None
    while True:
        uo = off(IB + e[2]); fl = raw[uo] >> 3; cnt = raw[uo + 2]
        if not (fl & 4):
            return IB + e[0]
        e = struct.unpack_from("<III", raw, uo + 4 + ((cnt + 1) & ~1) * 2)


def pend(va):
    """end VA of the .pdata range containing va"""
    e = pentry(va)
    return IB + e[1] if e else None


def fdis(f):
    """decode the .pdata range that starts at (or contains) f"""
    e = pentry(f)
    return dis(IB + e[0], IB + e[1])
