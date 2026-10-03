"""census_s31.py - FABLE, 2026-10-03: every write into the 46-byte licenceOwnedBits window, by displacement.

Window: record-relative displacements 0x194..0x1C1 (BattleStatsRecord +0x194, 46 bytes) and block-relative
0x19C..0x1C9 (the same bytes of record 0 addressed from the battle-state block, *(02EBF190) + 8 + 0x194), every access
width, base-only and base+index forms (rawref.disp_sweep).  A hit is kept when it WRITES (capstone's write access, or
a store-shaped mnemonic with memory in first position).

Route filter: a .pdata function is "on a record route" when its root references 02EBF190 (the block pointer every
party-record path loads) or is a function of 08-Combat-Formula/Battle-Stats-Record/battle-stats-record-accesses.tsv.
Writes whose base register is rsp are stack frames and are dropped.  Hits outside .pdata are re-decoded from their
leaf's start (after the CC padding before them); only those on a real instruction boundary are kept, with their
callers' roots, so the census can show that none of them is on a route.

What this cannot see, stated: bulk copies (memset / memcpy / rep stos of a whole record or of the block, and the save
image load that fills the block) - those are named by reading, in section.txt.
"""
import csv
import io
import os
import struct

from rawref import text_refs, disp_sweep, decode_fn  # noqa: F401
from capstone import CS_AC_WRITE

HERE = os.path.dirname(os.path.abspath(__file__))
TSV = os.path.join(HERE, "..", "..", "..", "08-Combat-Formula", "Battle-Stats-Record", "battle-stats-record-accesses.tsv")
STORE = ("mov", "movups", "movdqu", "movaps", "movdqa", "movq", "movd", "movsd", "movss", "or", "and", "xor", "add",
         "sub", "inc", "dec", "bts", "btr", "btc", "adc", "sbb", "neg", "not", "shl", "shr", "sar", "rol", "ror")


def root_of(img, va):
    pd = img.pdata(va)
    if pd is None:
        return None
    b = pd[0]
    po = img.off(img.base + img.exc_rva)
    n = img.exc_size // 12
    for _ in range(16):
        rva = b - img.base
        lo, hi, ent = 0, n - 1, None
        while lo <= hi:
            m = (lo + hi) // 2
            bb, ee, uu = struct.unpack_from("<III", img.d, po + m * 12)
            if rva < bb:
                hi = m - 1
            elif rva >= ee:
                lo = m + 1
            else:
                ent = (bb, ee, uu)
                break
        if ent is None:
            return b
        ui = img.off(img.base + ent[2])
        fl = img.d[ui] >> 3
        cnt = img.d[ui + 2]
        if not (fl & 4):
            return img.base + ent[0]
        b = struct.unpack_from("<I", img.d, ui + 4 + ((cnt + 1) & ~1) * 2)[0] + img.base
    return b


def leaf_boundary(img, site):
    p = site
    while p > site - 0x400 and img.read(p - 1, 1)[0] != 0xCC:
        p -= 1
    for ci in img.cs.disasm(img.read(p, site - p + 16), p):
        if ci.address == site:
            return ci
        if ci.address > site:
            return None
    return None


def is_write(r):
    text = r[1]
    mn, _, ops = text.partition(" ")
    return bool(r[3] & CS_AC_WRITE) or (mn in STORE and ops.startswith(("byte", "word", "dword", "qword", "xmmword")))


def census(img):
    route = set()
    for lo, hi in ((0x02EBF190, 0x02EBF198), (0x02EBF038, 0x02EBF040), (0x02EBF1A0, 0x02EBF200)):
        refs, _ = text_refs(img, lo, hi)
        for r in refs:
            rt = root_of(img, r["site"])
            if rt:
                route.add(rt)
    for row in csv.DictReader(io.open(TSV, encoding="utf-8"), delimiter="\t"):
        try:
            rt = root_of(img, int(row["function"], 16))
        except ValueError:
            continue
        if rt:
            route.add(rt)
    hits = {}
    for d in range(0x194, 0x1CA):
        for r in disp_sweep(img, d):
            if is_write(r):
                hits[r[0]] = r
    out = {"route": [], "leaf": [], "index": [], "total": len(hits), "stack": 0}
    for a in sorted(hits):
        r = hits[a]
        if "[rsp" in r[1]:
            out["stack"] += 1
            continue
        disp_ok = (0x194 <= _disp(r[1]) <= 0x1C1) or (0x19C <= _disp(r[1]) <= 0x1C9)
        if not disp_ok:
            continue
        if r[5] == "PDATA":
            rt = root_of(img, a)
            if rt in route:
                out["route"].append((a, r[1], rt))
            elif INDEXED.search(r[1]):
                out["index"].append((a, r[1], rt, r[2]))
        else:
            ci = leaf_boundary(img, a)
            if ci is None:
                continue
            # find the leaf start and its callers' roots
            p = a
            while img.read(p - 1, 1)[0] != 0xCC:
                p -= 1
            callers = [root_of(img, x["site"]) for x in text_refs(img, p)[0]]
            if any(c in route for c in callers if c):
                out["route"].append((a, r[1], p))
            else:
                out["leaf"].append((a, r[1], ["%08X" % c for c in callers if c]))
    return out, route


import re as _re
INDEXED = _re.compile(r"\[(\w+) \+ (\w+)(\*\d)? \+ 0x")


def _disp(text):
    import re
    m = re.search(r"\+ (0x[0-9a-f]+)\]", text)
    return int(m.group(1), 16) if m else -1
