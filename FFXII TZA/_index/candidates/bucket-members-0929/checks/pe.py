"""Shared read-only helpers for agentA scripts: section-aware image reads of the shipping EXE.
Image base 0x120000 is already inside every canonical address used here."""
import struct, hashlib, os
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000
EXTRACT = "D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok"
LANGS = ["us", "de", "es", "fr", "it", "ch", "cn", "kr", "in", "in_sdver"]

d = open(EXE, "rb").read()
assert hashlib.sha256(d).hexdigest() == SHA, "EXE hash mismatch"
_pe = struct.unpack_from("<I", d, 0x3C)[0]
_nsec = struct.unpack_from("<H", d, _pe + 6)[0]
_opt = struct.unpack_from("<H", d, _pe + 20)[0]
secs = []
for i in range(_nsec):
    o = _pe + 24 + _opt + i * 40
    name = d[o:o + 8].rstrip(b"\0").decode()
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, va, vs, ro, rs))


def off(addr):
    """file offset of image address, or None (also None for the virtual tail past SizeOfRawData)."""
    r = addr - BASE
    for name, va, vs, ro, rs in secs:
        if va <= r < va + max(vs, rs):
            if r - va >= rs:
                return None
            return ro + (r - va)
    return None


def section(addr):
    r = addr - BASE
    for name, va, vs, ro, rs in secs:
        if va <= r < va + max(vs, rs):
            return name
    return None


def u64(a):
    o = off(a)
    return None if o is None else struct.unpack_from("<Q", d, o)[0]


def u32(a):
    o = off(a)
    return None if o is None else struct.unpack_from("<I", d, o)[0]


def cstr(a, n=200):
    o = off(a)
    if o is None:
        return None
    e = d.find(b"\0", o, o + n)
    return d[o:e].decode("latin-1")


funcs = {}
names = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try:
        e = int(p[0], 16)
    except (ValueError, IndexError):
        continue
    funcs[e] = int(p[2]); names[e] = p[1]
starts = sorted(funcs)


def owner(a):
    import bisect
    i = bisect.bisect_right(starts, a) - 1
    if i >= 0 and starts[i] <= a < starts[i] + funcs[starts[i]]:
        return starts[i]
    return None


md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def dis(fn, size=None):
    size = size or funcs[fn]
    return list(md.disasm(d[off(fn):off(fn) + size], fn))


def text_range():
    for name, va, vs, ro, rs in secs:
        if name == ".text":
            return BASE + va, BASE + va + vs, ro


def ins_at(addr):
    """decode the single instruction that starts at addr"""
    o = off(addr)
    for x in md.disasm(d[o:o + 16], addr):
        return x
    return None


def raw_rip_refs(lo, hi):
    """Function-list-independent sweep: every .text position p whose int32 at p, taken as a rip displacement for an
    instruction ending at p+4+k (k in 0,1,2,4 trailing immediate bytes), lands in [lo, hi). Each candidate is then
    confirmed by decoding from p-1..p-7 and requiring an instruction that spans p and resolves to the same target.
    Returns sorted list of (instruction address, mnemonic, op_str, target)."""
    import struct as _s
    t0, t1, ro = text_range()
    blob = d[ro:ro + (t1 - t0)]
    out = set()
    for p in range(len(blob) - 4):
        disp = _s.unpack_from("<i", blob, p)[0]
        for k in (0, 1, 2, 4):
            tgt = t0 + p + 4 + k + disp
            if lo <= tgt < hi:
                for back in range(7, 0, -1):  # longest decoding first keeps REX prefixes
                    s = t0 + p - back
                    x = ins_at(s)
                    if x is None or x.address + x.size != t0 + p + 4 + k:
                        continue
                    if "rip" not in x.op_str:
                        continue
                    out.add((x.address, x.mnemonic, x.op_str, tgt))
                    break
    return sorted(out)


_dcache = {}
def containing_ins(a):
    """instruction covering byte a: from the owning listed function's linear disassembly when there is one,
    else by back-scanning 1..7 bytes (shortest first). Returns (insn, 'listed'|'unlisted') or (None, why)."""
    fn = owner(a)
    if fn is not None:
        if fn not in _dcache:
            _dcache[fn] = dis(fn)
        for x in _dcache[fn]:
            if x.address <= a < x.address + x.size:
                return x, "listed"
        return None, "listed-no-boundary"
    for back in range(1, 8):
        x = ins_at(a - back)
        if x is not None and x.address < a < x.address + x.size:
            return x, "unlisted"
    return None, "unlisted-no-decode"
