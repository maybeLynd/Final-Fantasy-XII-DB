"""sdx_indep.py - SWE2-AUDIT-SPEC independent helpers for the SD-180/181/23B reviews (2026-09-30).

pefile + capstone over the certified image (sha256 asserted); no retool / kit census. Scan functions follow this lane's
auditspec-review-ov31-type-store-0929/ov31_indep.py (rip disp32 by raw arithmetic then decode; image-base-relative
disp32 with a non-rip base; abs64/rva32 data hits; raw E8/E9; raw 0F 8x jcc) plus DIR64 relocation targets.

Write detection: capstone 5.0.x marks some memory destinations as READ, so a memory operand is classed a WRITE by
mnemonic + first operand (operand 0 is the memory operand and the mnemonic is a store/RMW form), not by op.access.
"""
import array, hashlib, struct
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
TEXT = [(n, v, vs, p, rs) for n, v, vs, p, rs, x in SECS if x]
ALL = [(n, v, vs, p, rs) for n, v, vs, p, rs, x in SECS]
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

NOWRITE = {"cmp", "test", "push", "lea", "prefetcht0", "prefetcht1", "prefetcht2", "prefetchnta", "ucomiss",
           "comiss", "ucomisd", "comisd", "bt", "call", "jmp", "nop"}


def off(va):
    for n, v, vs, p, rs in ALL:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def rd(va, n):
    o = off(va)
    return raw[o:o + n]


def q(va):
    return struct.unpack("<Q", rd(va, 8))[0]


def dis(start, end):
    o = off(start)
    return list(md.disasm(raw[o:o + (end - start)], start))


def one(va):
    return next(md.disasm(rd(va, 16), va, 1))


def txt(i):
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def mem_ops(i):
    for k, op in enumerate(i.operands):
        if op.type == CS_OP_MEM:
            yield k, op.mem, op.size


def is_write(i, k):
    """memory operand k of i is written: it is operand 0 and the mnemonic stores / read-modify-writes it."""
    if k != 0 or i.mnemonic in NOWRITE or i.mnemonic.startswith("j") or i.mnemonic.startswith("cmov"):
        return False
    if len(i.operands) == 1:
        return i.mnemonic in ("inc", "dec", "neg", "not", "pop") or i.mnemonic.startswith("set")
    return True


def rip_refs(lo, hi):
    hits = []
    for n, v, vs, p, rs in TEXT:
        blob = raw[p:p + min(vs, rs)]
        L = len(blob)
        for k0 in range(4):
            n4 = (L - k0) // 4
            arr = array.array("i")
            arr.frombytes(blob[k0:k0 + 4 * n4])
            base = v + k0 + 4
            cands = [k0 + 4 * j for j, d in enumerate(arr) if lo - 4 <= base + 4 * j + d < hi]
            for k in cands:
                d = struct.unpack_from("<i", blob, k)[0]
                for tail in (0, 1, 2, 4):
                    t = v + k + 4 + tail + d
                    if not (lo <= t < hi):
                        continue
                    best = None
                    for back in range(10, 0, -1):
                        if k - back < 0:
                            continue
                        ins = list(md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                        if not ins:
                            continue
                        i = ins[0]
                        if i.address + i.size != v + k + 4 + tail:
                            continue
                        for kk, m, sz in mem_ops(i):
                            if m.base == X86_REG_RIP and lo <= i.address + i.size + m.disp < hi:
                                best = (i.address, i.address + i.size + m.disp, txt(i), sz,
                                        "W" if is_write(i, kk) else ("A" if i.mnemonic == "lea" else "R"))
                        if best:
                            break
                    if best:
                        hits.append(best)
    return sorted(set(hits))


def imagebase_refs(lo, hi):
    """disp32 in [lo-IB, hi-IB) with a non-rip base (the image-base-relative form); window sweep by raw arithmetic."""
    hits = []
    for n, v, vs, p, rs in TEXT:
        blob = raw[p:p + min(vs, rs)]
        L = len(blob)
        for k0 in range(4):
            n4 = (L - k0) // 4
            arr = array.array("I")
            arr.frombytes(blob[k0:k0 + 4 * n4])
            cands = [k0 + 4 * j for j, d in enumerate(arr) if lo - IB <= d < hi - IB]
            for k in cands:
                for back in range(1, 9):
                    if k - back < 0:
                        continue
                    ins = list(md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                    if ins and ins[0].address < v + k < ins[0].address + ins[0].size:
                        i = ins[0]
                        for kk, m, sz in mem_ops(i):
                            if m.base not in (X86_REG_RIP,) and lo - IB <= (m.disp & 0xFFFFFFFF) < hi - IB \
                                    and (m.base != X86_REG_INVALID or m.index != X86_REG_INVALID):
                                hits.append((i.address, IB + (m.disp & 0xFFFFFFFF), txt(i), sz,
                                             "W" if is_write(i, kk) else ("A" if i.mnemonic == "lea" else "R")))
    return sorted(set(hits))


def data_refs(tgt):
    res = []
    for kind, pat in (("abs64", struct.pack("<Q", tgt)), ("rva32", struct.pack("<I", tgt - IB))):
        for n, v, vs, p, rs in ALL:
            blob = raw[p:p + min(vs, rs)]
            k = blob.find(pat)
            while k >= 0:
                res.append((kind, v + k, n))
                k = blob.find(pat, k + 1)
    return res


_RELOC = None


def dir64_targets():
    """{target VA: [slot VA]} for every DIR64 base relocation."""
    global _RELOC
    if _RELOC is None:
        p2 = pefile.PE(EXE, fast_load=True)
        p2.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_BASERELOC"]])
        _RELOC = {}
        for blk in p2.DIRECTORY_ENTRY_BASERELOC:
            for e in blk.entries:
                if e.type == 10:
                    slot = IB + e.rva
                    _RELOC.setdefault(q(slot), []).append(slot)
    return _RELOC


def reloc_in(lo, hi):
    r = dir64_targets()
    return sorted((t, s) for t, ss in r.items() if lo <= t < hi for s in ss)


def rel32_callers(tgt):
    res = []
    for n, v, vs, p, rs in TEXT:
        blob = raw[p:p + min(vs, rs)]
        for opc in (0xE8, 0xE9):
            k = blob.find(bytes([opc]))
            while 0 <= k and k + 5 <= len(blob):
                d = struct.unpack_from("<i", blob, k + 1)[0]
                if v + k + 5 + d == tgt:
                    res.append((v + k, "call" if opc == 0xE8 else "jmp"))
                k = blob.find(bytes([opc]), k + 1)
    return res


def jcc_callers(tgt):
    res = []
    for n, v, vs, p, rs in TEXT:
        blob = raw[p:p + min(vs, rs)]
        k = blob.find(b"\x0f")
        while 0 <= k and k + 6 <= len(blob):
            if 0x80 <= blob[k + 1] <= 0x8F:
                d = struct.unpack_from("<i", blob, k + 2)[0]
                if v + k + 6 + d == tgt:
                    res.append((v + k, "jcc"))
            k = blob.find(b"\x0f", k + 1)
    return res


_PDATA = None


def pdata():
    """sorted [(begin, end)] from .pdata RUNTIME_FUNCTION entries."""
    global _PDATA
    if _PDATA is None:
        d = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
        b = raw[off(IB + d.VirtualAddress):off(IB + d.VirtualAddress) + d.Size]
        _PDATA = sorted((IB + struct.unpack_from("<I", b, k)[0], IB + struct.unpack_from("<I", b, k + 4)[0])
                        for k in range(0, len(b) - 11, 12))
    return _PDATA


def owner(va):
    """the .pdata range containing va (begin, end) or None (chained / leaf entries resolve to their own range)."""
    import bisect
    P = pdata()
    j = bisect.bisect_right(P, (va, 1 << 64)) - 1
    if j >= 0 and P[j][0] <= va < P[j][1]:
        return P[j]
    return None
