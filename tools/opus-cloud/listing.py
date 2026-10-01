"""listing.py - the annotated disassembly OPUS's cloud packs carry and its ingest checks against (OPUS, 2026-10-01).

listing(fn) -> (lines, tokens): one line per instruction over the function's functions.tsv extent, with
  - every rip-relative operand resolved ('; -> 01DF0010'),
  - initialized-data targets decoded where it helps ('[f32 1.0]', '[u32 0x00000002]', '[str "Nobody"]'),
  - call / jmp targets marked when they are listed function entries ('; fn'),
and `tokens`, the set of 8-hex-digit addresses the listing shows (the function itself, every instruction address,
every resolved target, every branch target). A cloud row may only name addresses in `tokens`."""
import os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloudlib as cl  # noqa: E402
sys.path.insert(0, cl.KIT)
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402

_d = None
_secs = None
_sizes = None
_md = Cs(CS_ARCH_X86, CS_MODE_64)
RIP = re.compile(r"\[rip ([+-]) (0x[0-9a-f]+|\d+)\]")
HEX = re.compile(r"\b0x([0-9a-f]+)\b")


_base = 0x00120000


def _load():
    global _d, _secs, _sizes, _base
    if _d is not None:
        return
    _d = open(fp.EXE, "rb").read()
    pe = struct.unpack_from("<I", _d, 0x3C)[0]
    nsec = struct.unpack_from("<H", _d, pe + 6)[0]
    opt = struct.unpack_from("<H", _d, pe + 20)[0]
    base = _base = struct.unpack_from("<Q", _d, pe + 24 + 24)[0]
    _secs = []
    for i in range(nsec):
        o = pe + 24 + opt + i * 40
        name = _d[o:o + 8].rstrip(b"\0").decode("ascii", "replace")
        vs, va, rs, pr = struct.unpack_from("<IIII", _d, o + 8)
        _secs.append((name, base + va, vs, pr, rs))
    _sizes = cd.load_functions()


def sizes():
    _load()
    return _sizes


def file_off(va, n=1):
    """file offset of va when [va, va+n) lies in a section's initialized raw data, else None."""
    _load()
    for name, sva, vs, pr, rs in _secs:
        lim = sva + (min(vs, rs) if vs else rs)
        if sva <= va and va + n <= lim:
            return pr + (va - sva)
    return None


def section(va):
    _load()
    for name, sva, vs, pr, rs in _secs:
        if sva <= va < sva + max(vs, rs):
            return name
    return "?"


def _decode(va, width):
    o = file_off(va, 4)
    if o is None:
        return "" if section(va) != "?" else ""
    raw = _d[o:o + 64]
    end = raw.find(b"\0")
    s = raw[:end] if end >= 0 else b""
    if len(s) >= 4 and all(32 <= c < 127 for c in s):
        return ' [str "%s"]' % s.decode("ascii")
    if width == 16:
        fs = struct.unpack_from("<4f", raw, 0)
        if all(x == 0 or 1e-6 < abs(x) < 1e7 for x in fs):
            return " [f32x4 %s]" % ", ".join("%.7g" % x for x in fs)
        return " [u32x4 %s]" % ", ".join("0x%08X" % x for x in struct.unpack_from("<4I", raw, 0))
    if width == 4:
        u = struct.unpack_from("<I", raw, 0)[0]
        f = struct.unpack_from("<f", raw, 0)[0]
        if u and 1e-6 < abs(f) < 1e7:
            return " [f32 %.7g]" % f
        return " [u32 0x%08X]" % u
    if width == 8:
        q = struct.unpack_from("<Q", raw, 0)[0]
        dv = struct.unpack_from("<d", raw, 0)[0]
        if q and 1e-9 < abs(dv) < 1e12:
            return " [f64 %.10g]" % dv
        return " [u64 0x%016X]" % q
    if width == 2:
        return " [u16 0x%04X]" % struct.unpack_from("<H", raw, 0)[0]
    if width == 1:
        return " [u8 0x%02X]" % raw[0]
    return ""


def _width(op_str):
    for k, w in (("xmmword", 16), ("qword", 8), ("dword", 4), ("word", 2), ("byte", 1)):
        if k + " ptr" in op_str:
            return w
    return 0


def listing(fn):
    _load()
    n = _sizes.get(fn)
    if not n:
        return None, set()
    o = file_off(fn, n)
    if o is None:
        return None, set()
    lines, tokens = [], {"%08X" % fn}
    base_regs = set()                      # registers known to hold the image base (lea r, [rip -> 00120000])
    for i in _md.disasm(_d[o:o + n], fn):
        note = ""
        m = RIP.search(i.op_str)
        if not m and base_regs:
            bm = re.search(r"\[(\w+) \+ (?:\w+\*\d+ \+ )?(0x[0-9a-f]+)\]", i.op_str)
            if bm and bm.group(1) in base_regs and int(bm.group(2), 16) >= 0x1000:
                t = _base + int(bm.group(2), 16)
                tokens.add("%08X" % t)
                note = "; image base + %s = %08X" % (bm.group(2), t)
        if m:
            disp = int(m.group(2), 0)
            t = i.address + i.size + (disp if m.group(1) == "+" else -disp)
            tokens.add("%08X" % t)
            note = "; -> %08X" % t
            if t == _base and i.mnemonic == "lea":
                base_regs.add(i.op_str.split(",")[0].strip())
                note += " (image base)"
            if i.mnemonic != "lea" or _width(i.op_str):
                note += _decode(t, _width(i.op_str))
            elif section(t) in (".rdata", ".data"):
                note += _decode(t, 0)
        elif i.mnemonic == "call" or i.mnemonic.startswith("j"):
            h = HEX.fullmatch(i.op_str.strip())
            if h:
                t = int(h.group(1), 16)
                tokens.add("%08X" % t)
                note = "; -> %08X%s" % (t, " fn" if t in _sizes else "")
        for h in HEX.findall(i.op_str):
            if len(h) >= 6:
                tokens.add(("%08X" % int(h, 16))[-8:])
        tokens.add("%08X" % i.address)
        lines.append("%08X  %-8s %s%s" % (i.address, i.mnemonic, i.op_str, ("  " + note) if note else ""))
    return lines, tokens


def boundaries(fn):
    """{address: mnemonic} of the instructions inside the extent."""
    _load()
    n = _sizes.get(fn)
    o = file_off(fn, n)
    return {i.address: i.mnemonic for i in _md.disasm(_d[o:o + n], fn)}
