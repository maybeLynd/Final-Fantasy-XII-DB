"""s38lib.py - FABLE, 2026-10-03: shared helpers for the S-38 flag-word package (chained .pdata roots, body decode)."""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, data_refs, disp_sweep, sec  # noqa: E402,F401

_ROOTS = {}


def pdata_roots(img):
    """{root VA: [(begin, end) fragments]} with CHAININFO followed to the chain's first entry."""
    if id(img) in _ROOTS:
        return _ROOTS[id(img)]
    po = img.off(img.base + img.exc_rva)
    ents = []
    for i in range(img.exc_size // 12):
        b, e, u = struct.unpack_from("<III", img.d, po + i * 12)
        ui = img.off(img.base + u)
        fl = img.d[ui] >> 3
        n = img.d[ui + 2]
        root = b
        if fl & 4:
            co = ui + 4 + ((n + 1) & ~1) * 2
            root = struct.unpack_from("<I", img.d, co)[0]
        ents.append((b + img.base, e + img.base, root + img.base))
    first = {}
    for b, e, r in ents:
        first[b] = r
    frags = {}
    for b, e, r in ents:
        seen = 0
        while r in first and first[r] != r and seen < 16:
            r = first[r]
            seen += 1
        frags.setdefault(r, []).append((b, e))
    _ROOTS[id(img)] = frags
    return frags


def root_of(img, va):
    """Chained-.pdata root of the function holding va; None for a leaf outside .pdata."""
    pd = img.pdata(va)
    if pd is None:
        return None
    for r, parts in pdata_roots(img).items():
        if pd in parts:
            return r
    return pd[0]


def leaf_body(img, va, limit=0x200):
    """Linear decode of a leaf outside .pdata from va to the first ret/jmp followed by int3 padding."""
    out = []
    for ci in img.cs.disasm(img.read(va, limit), va):
        out.append(ci)
        if ci.mnemonic in ("ret", "jmp") and img.read(ci.address + ci.size, 1) == b"\xcc":
            break
    return out


def body(img, root):
    """Every instruction of a function: all chained fragments of a .pdata root, or a leaf decode."""
    parts = pdata_roots(img).get(root)
    if parts is None:
        pd = img.pdata(root)
        if pd is None:
            return leaf_body(img, root)
        parts = [pd]
    out = []
    for s, e in sorted(parts):
        out.extend(img.cs.disasm(img.read(s, e - s), s))
    return out


def txt(ci):
    return (ci.mnemonic + " " + ci.op_str).strip()
