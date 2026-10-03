"""rawref.py - FABLE, 2026-10-03: raw reference index over the certified image (numpy + capstone).

Finds every byte-level reference to a target VA range [lo, hi) in .text, in five forms:
  E8/E9 rel32 (call/jmp), 0F 80..8F rel32 (jcc), EB / 70..7F rel8 (short jmp/jcc),
  rip-relative disp32 (any instruction; imm tail 0/1/2/4 bytes tried),
  [reg + RVA] image-base-relative disp32 (disp == target - image base),
and pointer-sized constants in .rdata/.data (8-byte VA, 4-byte VA or 4-byte RVA, aligned 4).
Every .text candidate is CONFIRMED by decoding its containing .pdata function linearly and finding an instruction
whose operand resolves to the target; a candidate outside .pdata is decoded from 64 bytes back (best effort) and
tagged NOPDATA.  A census built on this sees thunks and unlisted code that a function-list census misses.

Uses rvlib.Img (found by walking up to _index/candidates/fable-review-astra-ov42-caller-quotient-bound-1002).
"""
import os
import sys

import numpy as np

_here = os.path.dirname(os.path.abspath(__file__))
_rv = os.path.join(_here, "..", "fable-review-astra-ov42-caller-quotient-bound-1002")
sys.path.insert(0, os.path.abspath(_rv))
from rvlib import Img, Body  # noqa: E402,F401
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP  # noqa: E402


def sec(img, name):
    for n, va, vs, ra, rs in img.secs:
        if n == name:
            return img.base + va, vs, ra, rs
    raise KeyError(name)


_TEXT = {}


def text_array(img):
    k = id(img)
    if k not in _TEXT:
        va, vs, ra, rs = sec(img, ".text")
        n = min(vs, rs)
        _TEXT[k] = (va, np.frombuffer(img.d[ra:ra + n], dtype=np.uint8))
    return _TEXT[k]


def _i32(a, n):
    # int32 at every offset 0..n-1 (n = len(a) - 3)
    return (a[0:n].astype(np.int64) | (a[1:n + 1].astype(np.int64) << 8) | (a[2:n + 2].astype(np.int64) << 16)
            | (a[3:n + 3].astype(np.int64) << 24)).astype(np.uint32).astype(np.int32).astype(np.int64)


_FUNC_CACHE = {}


def decode_fn(img, va):
    """Linear decode of the .pdata function holding va: {addr: capstone insn}. None when va is outside .pdata."""
    pd = img.pdata(va)
    if pd is None:
        return None, None
    if pd not in _FUNC_CACHE:
        s, e = pd
        out = {}
        for ci in img.cs.disasm(img.read(s, e - s), s):
            out[ci.address] = ci
        _FUNC_CACHE[pd] = out
    return pd, _FUNC_CACHE[pd]


def _single(img, va):
    """One instruction decoded at va (no stream context), or None."""
    for ci in img.cs.disasm(img.read(va, 16), va):
        return ci
    return None


def _spanning(img, ins, site, first_back, pred):
    """The instruction that spans `site` and satisfies pred.  With a .pdata decode (ins is a dict) the linear decode
    decides the boundary.  Outside .pdata (ins is None) every start site-back is tried on its own, and the first that
    spans the site and satisfies pred is accepted (pred is a full operand match, so a misaligned decode is rejected
    unless it resolves to the same target)."""
    if ins is not None:
        for back in range(first_back, 15):
            ci = ins.get(site - back)
            if ci is not None and site - back + ci.size > site:
                return ci if pred(ci) else None
        return None
    # outside .pdata: the EARLIEST start that spans and matches (a REX or other prefix byte belongs to the instruction)
    for back in range(14, first_back - 1, -1):
        ci = _single(img, site - back)
        if ci is not None and site - back + ci.size > site and pred(ci):
            return ci
    return None


def _resolves(img, ci, lo, hi):
    """Does instruction ci reference [lo, hi)? Returns a short form tag or None."""
    m = ci.mnemonic
    for op in ci.operands:
        if op.type == X86_OP_IMM and (m == "call" or m.startswith("j")):
            t = op.imm & 0xFFFFFFFFFFFFFFFF
            if lo <= t < hi:
                return "call" if m == "call" else ("jmp" if m == "jmp" else "jcc")
        if op.type == X86_OP_MEM:
            mm = op.mem
            if mm.base == X86_REG_RIP:
                t = ci.address + ci.size + mm.disp
                if lo <= t < hi:
                    return "rip"
            elif mm.base != 0 or mm.index != 0:
                t = img.base + (mm.disp & 0xFFFFFFFF)
                if mm.disp > 0 and lo <= t < hi:
                    return "basrel"
        if op.type == X86_OP_IMM and m != "call" and not m.startswith("j"):
            v = op.imm & 0xFFFFFFFFFFFFFFFF
            if lo <= v < hi:
                return "immva"
    return None


def text_refs(img, lo, hi=None):
    """All confirmed .text references to [lo, hi). Returns list of dicts (site, insn text, form, func, status)."""
    hi = lo + 1 if hi is None else hi
    tva, a = text_array(img)
    n = len(a) - 3
    d = _i32(a, n)
    pos = np.arange(n, dtype=np.int64) + tva
    cands = set()
    # rel32 branch forms: opcode at p-1 (E8/E9) or p-2 (0F 8x); target = p + 4 + disp
    t = pos + 4 + d
    hit = np.nonzero((t >= lo) & (t < hi))[0]
    for i in hit:
        if i >= 1 and a[i - 1] in (0xE8, 0xE9):
            cands.add(int(tva + i - 1))
        if i >= 2 and a[i - 2] == 0x0F and 0x80 <= a[i - 1] <= 0x8F:
            cands.add(int(tva + i - 2))
    # rip-relative: target = p + 4 + L + disp for imm tails L
    for L in (0, 1, 2, 4):
        t = pos + 4 + L + d
        for i in np.nonzero((t >= lo) & (t < hi))[0]:
            cands.add(("rip", int(tva + i)))
    # image-base-relative disp32 / imm32 VA
    for i in np.nonzero(((d + img.base) >= lo) & ((d + img.base) < hi))[0]:
        cands.add(("rip", int(tva + i)))
    for i in np.nonzero((d >= lo) & (d < hi))[0]:
        cands.add(("rip", int(tva + i)))
    # rel8 forms
    b8 = a[1:n + 1].astype(np.int8).astype(np.int64)
    t8 = pos + 2 + b8
    for i in np.nonzero((t8 >= lo) & (t8 < hi))[0]:
        if a[i] == 0xEB or 0x70 <= a[i] <= 0x7F:
            cands.add(int(tva + i))
    found = {}
    unconfirmed = []
    for c in sorted(cands, key=lambda x: x[1] if isinstance(x, tuple) else x):
        site = c[1] if isinstance(c, tuple) else c
        pd, ins = decode_fn(img, site)
        status = "PDATA" if ins is not None else "NOPDATA"
        hitins = _spanning(img, ins, site, 0, lambda ci: _resolves(img, ci, lo, hi))
        if hitins is None:
            if status == "PDATA" and not isinstance(c, tuple):
                unconfirmed.append(site)
            continue
        found[hitins.address] = {
            "site": hitins.address, "text": (hitins.mnemonic + " " + hitins.op_str).strip(),
            "form": _resolves(img, hitins, lo, hi), "func": pd[0] if pd else None, "status": status}
    return sorted(found.values(), key=lambda r: r["site"]), unconfirmed


def data_refs(img, lo, hi=None, secs=(".rdata", ".data")):
    """Aligned pointer constants (8-byte VA, 4-byte VA, 4-byte RVA) in the file-backed part of secs."""
    hi = lo + 1 if hi is None else hi
    out = []
    for s in secs:
        va, vs, ra, rs = sec(img, s)
        n = min(vs, rs)
        b = np.frombuffer(img.d[ra:ra + (n // 8) * 8], dtype=np.uint64)
        for i in np.nonzero((b >= lo) & (b < hi))[0]:
            out.append((s, int(va + i * 8), "va64", int(b[i])))
        w = np.frombuffer(img.d[ra:ra + (n // 4) * 4], dtype=np.uint32).astype(np.int64)
        for i in np.nonzero(((w >= lo) & (w < hi)) | (((w + img.base) >= lo) & ((w + img.base) < hi)))[0]:
            out.append((s, int(va + i * 4), "u32", int(w[i])))
    return out


def fmt_ref(r):
    return "%08X  %-6s %-8s fn=%s  %s" % (r["site"], r["form"], r["status"],
                                           ("%08X" % r["func"]) if r["func"] else "--------", r["text"])


def disp_sweep(img, disp, width=None):
    """Every confirmed .text instruction with a memory operand whose displacement == disp (disp32 encodings, and
    disp8 when -128 <= disp < 128).  width: keep only operands of that byte size.  Returns list of (site, text, size, rw)."""
    tva, a = text_array(img)
    n = len(a) - 3
    cands = set()
    if -128 <= disp < 128:
        for i in np.nonzero(a.astype(np.int8).astype(np.int64)[:n] == disp)[0]:
            cands.add(int(tva + i))
    d = _i32(a, n)
    for i in np.nonzero(d == disp)[0]:
        cands.add(int(tva + i))
    out = {}
    for site in sorted(cands):
        pd, ins = decode_fn(img, site)
        st = "PDATA" if ins is not None else "NOPDATA"

        def match(ci):
            return any(op.type == X86_OP_MEM and op.mem.disp == disp and op.mem.base != X86_REG_RIP
                       and (width is None or op.size == width) for op in ci.operands)
        ci = _spanning(img, ins, site, 1, match)
        if ci is not None:
            for op in ci.operands:
                if op.type == X86_OP_MEM and op.mem.disp == disp and op.mem.base != X86_REG_RIP:
                    out[ci.address] = (ci.address, (ci.mnemonic + " " + ci.op_str).strip(), op.size,
                                       op.access, pd[0] if pd else None, st)
                    break
    return [out[k] for k in sorted(out)]
