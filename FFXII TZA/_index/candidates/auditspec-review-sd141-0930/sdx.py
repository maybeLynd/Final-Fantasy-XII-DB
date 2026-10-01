"""sdx.py - SWE2-AUDIT-SPEC independent census helpers (SD-126/127/141/169 reviews, 2026-09-30).

pefile + capstone + numpy over the certified image (sha256 asserted). Written without retool.py / the `pe` module the
reviewed packages use. Addresses are canonical VAs (image base 0x120000 included - never added again).

  window(lo, hi, span)  every instruction in .text whose memory operand STARTS in [lo - span, hi), in all encodings:
                        rip-relative (raw disp32 arithmetic, tails 0/1/2/4, confirmed by decode), image-base-relative
                        (disp32 = target - 0x120000 with ANY non-rip base and/or index, incl. index-only and
                        base+index forms), and absolute disp32 (disp32 = VA itself, with or without registers). Each hit carries the
                        access width and whether [start, start + width) covers [lo, hi).
  relocs()              DIR64 / HIGHLOW relocation sites -> target VA (the stored-pointer route).
  data_refs(lo, hi)     raw abs64 / abs32 / rva32 values in [lo, hi) in every section (unrelocated scan).
  rip_leas()            every rip-relative lea in .text (raw 8D /r mod=00 rm=101 scan, confirmed by decode).
  rel32(tgt) / jcc(tgt) raw E8/E9 and 0F 8x callers.
  pdata / root(va)      .pdata extents and chained-unwind root.
Nothing here writes a file.
"""
import bisect, hashlib, os, struct
import numpy as np
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM, CS_OP_IMM
from capstone.x86 import X86_REG_RIP, X86_REG_INVALID

EXE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "image hash mismatch"
pe = pefile.PE(data=raw, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
assert IB == 0x120000
SECS = [(s.Name.rstrip(b"\0").decode(), IB + s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData,
         bool(s.Characteristics & 0x20000000)) for s in pe.sections]
TEXT = [x for x in SECS if x[5]]
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def off(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def sec(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + vs:
            return n
    return None


def rd(va, n):
    o = off(va)
    return raw[o:o + n] if o is not None else None


def one(va):
    o = off(va)
    r = list(md.disasm(raw[o:o + 15], va, 1))
    return r[0] if r else None


def txt(va):
    i = one(va)
    return "%s %s" % (i.mnemonic, i.op_str) if i else "(nodecode)"


def mem_ops(i):
    for op in i.operands:
        if op.type == CS_OP_MEM:
            yield op.mem, op.size


def _confirm(blob, v, k, tail, want):
    """decode starts 1..10 bytes before the disp32 at blob[k]; return instructions (longest first) that contain the disp
    at the displacement position and satisfy want(i, mem, size)."""
    got = []
    for back in range(10, 0, -1):
        if k - back < 0:
            continue
        ins = list(md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
        if not ins:
            continue
        i = ins[0]
        if not (i.address < v + k and v + k + 4 <= i.address + i.size):
            continue
        if tail is not None and i.address + i.size != v + k + 4 + tail:
            continue
        for m, sz in mem_ops(i):
            if want(i, m, sz):
                got.append((i, m, sz))
        if got:
            # a REX byte (40..4F) borrowed from the previous instruction's tail: if the decode one byte later is valid and
            # reads the same (mnemonic + operands), the REX is redundant - keep the later start (linear-decode boundary)
            while blob[got[0][0].address - v] & 0xF0 == 0x40:
                a = got[0][0].address + 1
                j = list(md.disasm(blob[a - v:a - v + 15], a, 1))
                if not j or j[0].address + j[0].size != got[0][0].address + got[0][0].size or                         (j[0].mnemonic, j[0].op_str) != (got[0][0].mnemonic, got[0][0].op_str):
                    break
                got = [(j[0], [mm for mm, z in mem_ops(j[0])][0], got[0][2])]
            return got
    return got


def window(lo, hi, span=64):
    """see module doc. Returns sorted list of dicts."""
    hits = {}
    for n, v, vs, p, rs, x in TEXT:
        blob = raw[p:p + min(vs, rs)]
        L = len(blob)
        a8 = np.frombuffer(blob, dtype=np.uint8)
        for k0 in range(4):
            n4 = (L - k0) // 4
            arr = np.frombuffer(blob, dtype="<i4", count=n4, offset=k0).astype(np.int64)
            pos = k0 + 4 * np.arange(n4, dtype=np.int64)
            # rip-relative: target = VA(disp) + 4 + tail + d
            base = v + pos + 4
            for tail in (0, 1, 2, 4):
                t = base + tail + arr
                for k in pos[(t >= lo - span) & (t < hi)].tolist():
                    for i, m, sz in _confirm(blob, v, k, tail,
                                             lambda i, m, sz: m.base == X86_REG_RIP):
                        s = i.address + i.size + m.disp
                        if lo - span <= s < hi:
                            hits[(i.address, "rip")] = (i, s, sz, "rip")
            # image-base-relative (disp = target - IB, any non-rip base/index) and absolute disp32 (= VA, no regs)
            for form, delta in (("ibrel", IB), ("abs32", 0)):
                t = arr + delta
                for k in pos[(t >= lo - span) & (t < hi)].tolist():
                    d = struct.unpack_from("<i", blob, k)[0]
                    if form == "ibrel":
                        w = lambda i, m, sz, d=d: m.base != X86_REG_RIP and m.disp == d and \
                            (m.base != X86_REG_INVALID or m.index != X86_REG_INVALID)
                    else:
                        w = lambda i, m, sz, d=d: m.base != X86_REG_RIP and m.disp == d
                    for i, m, sz in _confirm(blob, v, k, None, w):
                        hits[(i.address, form)] = (i, d + delta, sz, form)
    out = []
    for (a, form), (i, s, sz, f) in sorted(hits.items()):
        m = [mm for mm, z in mem_ops(i)][0]
        indexed = m.index != X86_REG_INVALID
        w = max(sz, 1)
        out.append(dict(addr=a, form=form, mn=i.mnemonic, op=i.op_str, start=s, width=sz, lea=i.mnemonic == "lea",
                        indexed=indexed, covers=(s < hi and s + w > lo) and i.mnemonic != "lea",
                        base=i.reg_name(m.base) if m.base else None, index=i.reg_name(m.index) if m.index else None))
    return out


_REL = None


def relocs():
    """{site VA: (type, target VA)} for every base relocation (type 10 DIR64, type 3 HIGHLOW)."""
    global _REL
    if _REL is not None:
        return _REL
    dd = pe.OPTIONAL_HEADER.DATA_DIRECTORY[5]
    o0 = off(IB + dd.VirtualAddress)
    o, end, res = o0, o0 + dd.Size, {}
    while o < end:
        page, size = struct.unpack_from("<II", raw, o)
        if size == 0:
            break
        for j in range((size - 8) // 2):
            e = struct.unpack_from("<H", raw, o + 8 + 2 * j)[0]
            typ, ofs = e >> 12, e & 0xFFF
            site = IB + page + ofs
            if typ == 10:
                q = rd(site, 8)
                res[site] = (10, struct.unpack("<Q", q)[0] if q and len(q) == 8 else None)
            elif typ == 3:
                q = rd(site, 4)
                res[site] = (3, struct.unpack("<I", q)[0] if q and len(q) == 4 else None)
        o += size
    _REL = res
    return res


def relocs_into(lo, hi):
    return sorted((s, t) for s, (typ, t) in relocs().items() if t is not None and lo <= t < hi)


def data_refs(lo, hi):
    """unrelocated raw scan: every aligned-or-not qword / dword whose value lies in [lo, hi) (abs64, abs32) or whose
    value + IB lies in it (rva32), in every section's raw data."""
    res = []
    for n, v, vs, p, rs, x in SECS:
        blob = raw[p:p + min(vs, rs)]
        L = len(blob)
        for k0 in range(8):
            n8 = (L - k0) // 8
            if n8 > 0:
                q = np.frombuffer(blob, dtype="<u8", count=n8, offset=k0)
                for j in np.nonzero((q >= lo) & (q < hi))[0].tolist():
                    res.append(("abs64", v + k0 + 8 * j, int(q[j]), n))
        for k0 in range(4):
            n4 = (L - k0) // 4
            d = np.frombuffer(blob, dtype="<u4", count=n4, offset=k0).astype(np.int64)
            for kind, delta in (("abs32", 0), ("rva32", IB)):
                for j in np.nonzero((d + delta >= lo) & (d + delta < hi))[0].tolist():
                    res.append((kind, v + k0 + 4 * j, int(d[j]) + delta, n))
    return sorted(set(res), key=lambda r: (r[1], r[0]))


def rip_leas(lo=None, hi=None):
    """every rip-relative lea in .text: (site, dest register, target). Raw scan for [REX] 8D modrm(mod 00, rm 101)."""
    out = []
    for n, v, vs, p, rs, x in TEXT:
        blob = raw[p:p + min(vs, rs)]
        a = np.frombuffer(blob, dtype=np.uint8)
        idx = np.nonzero((a[:-6] == 0x8D) & ((a[1:-5] & 0xC7) == 0x05))[0]
        for k in idx.tolist():
            d = struct.unpack_from("<i", blob, k + 2)[0]
            for back in (1, 0):  # with REX, or without
                s = k - back
                if s < 0:
                    continue
                if back == 1 and not (0x40 <= blob[s] <= 0x4F):
                    continue
                t = v + k + 6 + d
                if lo is not None and not (lo <= t < hi):
                    break
                i = list(md.disasm(blob[s:s + 7], v + s, 1))
                if i and i[0].mnemonic == "lea" and i[0].address + i[0].size == v + k + 6:
                    out.append((v + s, i[0].op_str.split(",")[0], t))
                    break
    return out


def rel32(tgt):
    res = []
    for n, v, vs, p, rs, x in TEXT:
        blob = raw[p:p + min(vs, rs)]
        a = np.frombuffer(blob, dtype=np.uint8)
        for opc in (0xE8, 0xE9):
            for k in np.nonzero(a[:-5] == opc)[0].tolist():
                if v + k + 5 + struct.unpack_from("<i", blob, k + 1)[0] == tgt:
                    res.append((v + k, "call" if opc == 0xE8 else "jmp"))
    return res


def jcc(tgt):
    res = []
    for n, v, vs, p, rs, x in TEXT:
        blob = raw[p:p + min(vs, rs)]
        a = np.frombuffer(blob, dtype=np.uint8)
        for k in np.nonzero((a[:-6] == 0x0F) & (a[1:-5] >= 0x80) & (a[1:-5] <= 0x8F))[0].tolist():
            if v + k + 6 + struct.unpack_from("<i", blob, k + 2)[0] == tgt:
                res.append((v + k, "jcc"))
    return res


_dd = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
_o = off(IB + _dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", raw, _o + 12 * k) for k in range(_dd.Size // 12))
PST = [e[0] for e in PD]
FUNC_STARTS = set(IB + e[0] for e in PD)


def pdata_of(va):
    rva = va - IB
    j = bisect.bisect_right(PST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    return PD[j]


_CHAIN = None


def chain_end(va):
    """end of the last .pdata chunk that shares va's chained-unwind root (a function split into chunks)."""
    global _CHAIN
    if _CHAIN is None:
        _CHAIN = {}
        for e in PD:
            r = root(IB + e[0])
            if r is not None:
                _CHAIN[r] = max(_CHAIN.get(r, 0), IB + e[1])
    r = root(va)
    e = pdata_of(va)
    return max(_CHAIN.get(r, 0), IB + e[1]) if e else None


def root(va):
    e = pdata_of(va)
    if e is None:
        return None
    while True:
        uo = off(IB + e[2])
        fl = raw[uo] >> 3
        cnt = raw[uo + 2]
        if not (fl & 4):
            return IB + e[0]
        e = struct.unpack_from("<III", raw, uo + 4 + ((cnt + 1) & ~1) * 2)


_ARGS = ("rcx", "rdx", "r8", "r9")
_VOL = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")


def _full(i, r):
    """64-bit name of a GPR id (capstone), or None."""
    n = i.reg_name(r)
    if n is None:
        return None
    m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", "esp": "rsp",
         "ax": "rax", "bx": "rbx", "cx": "rcx", "dx": "rdx", "si": "rsi", "di": "rdi", "bp": "rbp", "sp": "rsp",
         "al": "rax", "bl": "rbx", "cl": "rcx", "dl": "rdx", "sil": "rsi", "dil": "rdi", "bpl": "rbp", "spl": "rsp"}
    if n in m:
        return m[n]
    for p in ("r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"):
        if n == p or n in (p + "d", p + "w", p + "b"):
            return p
    return n


def track_entry(func, reg, base, limit=None, max_ins=4000):
    """as track(), but start at a callee's entry with `reg` holding `base` (one level of hand-on)."""
    return track(func, limit, max_ins, start=(reg, base))


def track(site, limit=None, max_ins=4000, start=None):
    """linear, NOT flow-aware candidate walk: from the rip lea at `site`, track which GPRs hold (target + offset)
    through mov-copies, lea [r + d] and add/sub imm; any other write kills. Records every memory operand based or
    indexed on a tracked register (with offset + disp and width), every call made while a tracked register sits in an
    argument register (handed-on base), and every store of a tracked register to memory. Volatile registers die at a
    call. Stops at the .pdata end of the site's entry (or `limit`), or at ret/jmp-out."""
    if start is None:
        i0 = one(site)
        m0 = [m for m, z in mem_ops(i0)][0]
        tgt = i0.address + i0.size + m0.disp
        regs = {_full(i0, i0.operands[0].reg): 0}
        skip = i0.size
    else:
        regs = {start[0]: 0}
        tgt = start[1]
        skip = 0
    e = pdata_of(site)
    end = limit or ((chain_end(site)) if e else site + 0x800)
    o = off(site)
    acc, calls, stores = [], [], []
    n, far = 0, site
    for i in md.disasm(raw[o + skip:o + (end - site)], site + skip):
        n += 1
        if n > max_ins:
            break
        ops = i.operands
        if e is None:  # no .pdata extent: stop at a ret / int3 past every forward branch seen (leaf extent walk)
            if (i.group(1) or i.group(7)) and ops and ops[0].type == CS_OP_IMM and site <= ops[0].imm < end:
                far = max(far, ops[0].imm)
            if i.mnemonic in ("ret", "int3") and i.address >= far:
                break
        # memory operands through a tracked register
        for op in ops:
            if op.type == CS_OP_MEM:
                b, x = _full(i, op.mem.base) if op.mem.base else None, _full(i, op.mem.index) if op.mem.index else None
                if b in regs or x in regs:
                    via = b if b in regs else x
                    acc.append((i.address, "%s %s" % (i.mnemonic, i.op_str), tgt + regs[via] + (op.mem.disp if b in regs else 0),
                                op.size, x is not None, i.mnemonic == "lea"))
        if i.mnemonic == "call":
            live = {r: regs[r] for r in _ARGS if r in regs}
            if live:
                calls.append((i.address, i.op_str, {r: "%08X" % (tgt + v) for r, v in live.items()}))
            for r in _VOL:
                regs.pop(r, None)
            continue
        if i.mnemonic == "ret" or (i.mnemonic == "jmp" and ops and ops[0].type == CS_OP_IMM and not (site <= ops[0].imm < end)):
            if i.mnemonic == "jmp":
                live = {r: regs[r] for r in _ARGS if r in regs}
                if live:
                    calls.append((i.address, "tail " + i.op_str, {r: "%08X" % (tgt + v) for r, v in live.items()}))
            continue  # linear: keep walking (other paths continue past)
        if len(ops) >= 2 and ops[0].type == 1:  # REG destination
            d = _full(i, ops[0].reg)
            src = ops[1]
            if i.mnemonic == "mov" and src.type == 1 and _full(i, src.reg) in regs and i.reg_name(ops[0].reg).startswith("r"):
                regs[d] = regs[_full(i, src.reg)]
                continue
            if i.mnemonic == "lea" and src.type == CS_OP_MEM and src.mem.base and _full(i, src.mem.base) in regs \
                    and not src.mem.index:
                regs[d] = regs[_full(i, src.mem.base)] + src.mem.disp
                continue
            if i.mnemonic in ("add", "sub") and d in regs and src.type == CS_OP_IMM:
                regs[d] += src.imm if i.mnemonic == "add" else -src.imm
                continue
            if i.mnemonic in ("cmp", "test"):
                continue
            if d in regs:
                regs.pop(d)
        elif len(ops) >= 2 and ops[0].type == CS_OP_MEM and ops[1].type == 1 and _full(i, ops[1].reg) in regs:
            stores.append((i.address, "%s %s" % (i.mnemonic, i.op_str)))
        else:
            for r in i.regs_access()[1]:
                fr = _full(i, r)
                if fr in regs and i.mnemonic not in ("push", "cmp", "test"):
                    regs.pop(fr)
    return tgt, acc, calls, stores


def fmt(h):
    return "%08X %-5s %-8s %-44s start %08X w%-2d%s%s%s" % (
        h["addr"], h["form"], h["mn"], h["op"], h["start"], h["width"], " COVERS" if h["covers"] else "",
        " indexed" if h["indexed"] else "", " lea" if h["lea"] else "")
