"""tk.py - shared helpers for the takeback censuses (FABLE reader, 2026-09-29). Read-only on the image.

Independent of the function list where it matters:
  rip_refs(lo, hi)      raw sweep of ALL .text bytes for rip-relative disp32 resolving into [lo,hi); each candidate is
                        verified by decoding an instruction that starts 1..12 bytes before the disp and whose rip memory
                        operand is that disp. Unverified raw hits are returned too (flag 'raw-only').
  disp_refs(lo, hi)     raw sweep of ALL .text bytes for a disp32 value in [lo,hi) (image-base-relative forms), verified
                        the same way (a memory operand with a non-rip base or index and that displacement).
  reloc_ptrs(lo, hi)    every DIR64 relocation whose target qword lies in [lo,hi) (stored absolute pointers, any section).
  raw_q(lo, hi)         unaligned raw qword scan of the whole file for values in [lo,hi) (backup for reloc_ptrs).
  owner(a)              listed function containing a, else the .pdata range containing it, else None.
  dis(start, end)       capstone detail decode of [start,end).
"""
import struct, bisect, array
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = {}
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode()
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs[nm] = (va + BASE, vs, rs, ro)
def off(addr):
    for nm, (va, vs, rs, ro) in secs.items():
        if va <= addr < va + vs:
            r = addr - va
            return ro + r if r < rs else None      # virtual tail past SizeOfRawData -> zero-initialised, no file bytes
    return None
def sec_of(addr):
    for nm, (va, vs, rs, ro) in secs.items():
        if va <= addr < va + vs: return nm
    return None
def u32(a): o = off(a); return None if o is None else struct.unpack_from("<I", d, o)[0]
def u64(a): o = off(a); return None if o is None else struct.unpack_from("<Q", d, o)[0]
TVA, TVS, TRS, TRO = secs[".text"]
names = {}; flist = []
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: e = int(p[0], 16); sz = int(p[2])
    except (ValueError, IndexError): continue
    names[e] = p[1]; flist.append((e, sz))
flist.sort(); fstarts = [e for e, _ in flist]
# .pdata ranges
PVA, PVS, PRS, PRO = secs[".pdata"]
pdata = []
for k in range(0, PVS - 11, 12):
    b, e, u = struct.unpack_from("<III", d, PRO + k)
    if b == 0: break
    pdata.append((b + BASE, e + BASE))
pdata.sort(); pstarts = [b for b, _ in pdata]
def owner(a):
    i = bisect.bisect_right(fstarts, a) - 1
    if i >= 0 and flist[i][0] <= a < flist[i][0] + flist[i][1]: return flist[i][0], "listed"
    j = bisect.bisect_right(pstarts, a) - 1
    if j >= 0 and pdata[j][0] <= a < pdata[j][1]: return pdata[j][0], "pdata"
    return None, "none"
def fname(a):
    o, how = owner(a)
    if o is None: return "unlisted"
    return "%08X %s%s" % (o, names.get(o, "?"), "" if how == "listed" else " [pdata]")
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
def dis(start, end):
    o = off(start)
    return list(md.disasm(d[o:o + (end - start)], start))
def fsize(e):
    i = bisect.bisect_left(fstarts, e)
    return flist[i][1] if i < len(flist) and flist[i][0] == e else None
def fdis(e):
    return dis(e, e + fsize(e))
def _decode_at(a):
    o = off(a)
    if o is None: return None
    for x in md.disasm(d[o:o + 16], a): return x
    return None
def _verify(dpos, want_rip, dispval):
    """find an instruction starting 1..12 bytes before dpos whose memory operand disp field sits at dpos."""
    out = []
    for back in range(1, 13):
        s = dpos - back
        x = _decode_at(s)
        if x is None: continue
        if x.disp_offset != back or x.disp_size != 4: continue
        for k, op in enumerate(x.operands):
            if op.type != X86_OP_MEM: continue
            isrip = op.mem.base != 0 and x.reg_name(op.mem.base) == "rip"
            if want_rip != isrip: continue
            if want_rip:
                out.append((x, k))
            elif (op.mem.disp & 0xFFFFFFFF) == (dispval & 0xFFFFFFFF):
                out.append((x, k))
    return out
def _words():
    blob = d[TRO:TRO + min(TVS, TRS)]
    for al in range(4):
        n = (len(blob) - al) // 4
        arr = array.array("i"); arr.frombytes(blob[al:al + n * 4])
        yield al, arr
_bcache = {}
def boundaries(a):
    """instruction starts of the linear decode of the owner (listed function or .pdata range) of a"""
    o, how = owner(a)
    if o is None: return None
    if o not in _bcache:
        if how == "listed": end = o + fsize(o)
        else: end = pdata[bisect.bisect_right(pstarts, a) - 1][1]
        oo = off(o); _bcache[o] = set(x.address for x in md.disasm(d[oo:oo + end - o], o))
    return _bcache[o]
def _pick(cands):
    """keep decodes that start on the owner's instruction boundary; unowned: keep the earliest start, flagged via attribute"""
    if not cands: return cands
    b = boundaries(cands[0][0].address)
    if b is not None:
        on = [(x, k) for x, k in cands if x.address in b]
        return on
    m = min(x.address for x, k in cands)
    return [(x, k) for x, k in cands if x.address == m]
def rip_refs(lo, hi):
    """returns list of (insn_addr, insn, opindex, target, owner) plus raw-only list of (disp_pos, target)"""
    cands = []
    for al, arr in _words():
        base = TVA + al + 4
        for idx, v in enumerate(arr):
            p = base + idx * 4          # end of disp field
            for imm in (0, 1, 2, 4):
                t = p + imm + v
                if lo <= t < hi: cands.append((p - 4, imm, t))
    hits = {}; raw = []
    for dpos, imm, t in cands:
        vs = _verify(dpos, True, 0)
        good = [(x, k) for x, k in vs if x.address + x.size + x.operands[k].mem.disp == t]
        good = _pick(good)
        if good:
            for x, k in good: hits[x.address] = (x, k, t)
        else: raw.append((dpos, t))
    raw = [(p, t) for p, t in raw if not any(a <= p < a + hits[a][0].size for a in hits)]
    return [hits[a] for a in sorted(hits)], raw
def disp_refs(lo, hi):
    cands = []
    for al, arr in _words():
        base = TVA + al
        for idx, v in enumerate(arr):
            if lo <= (v & 0xFFFFFFFF) < hi: cands.append((base + idx * 4, v & 0xFFFFFFFF))
    hits = {}; raw = []
    for p, v in cands:
        vs = _pick(_verify(p, False, v))
        if vs:
            for x, k in vs: hits[x.address] = (x, k, v)
        else: raw.append((p, v))
    return [hits[a] for a in sorted(hits)], raw
def relocs():
    RVA_, RVS, RRS, RRO = secs[".reloc"]
    k = RRO; end = RRO + RVS
    while k < end:
        page, size = struct.unpack_from("<II", d, k)
        if size == 0: break
        for j in range(8, size, 2):
            e = struct.unpack_from("<H", d, k + j)[0]
            if e >> 12 == 10: yield page + (e & 0xFFF) + BASE
        k += size
def reloc_ptrs(lo, hi):
    out = []
    for a in relocs():
        q = u64(a)
        if q is not None and lo <= q < hi: out.append((a, q))
    return out
def raw_q(lo, hi):
    out = []
    for nm, (va, vs, rs, ro) in secs.items():
        blob = d[ro:ro + min(vs, rs)]
        for i in range(len(blob) - 7):
            if blob[i + 3] == 0 and blob[i + 4] == 0 and blob[i + 5] == 0 and blob[i + 6] == 0 and blob[i + 7] == 0:
                q = struct.unpack_from("<Q", blob, i)[0]
                if lo <= q < hi: out.append((va + i, q, nm))
    return out
WRITE_MN = ("mov", "movzx", "movsx", "or", "and", "xor", "add", "sub", "inc", "dec", "bts", "btr", "btc", "neg", "not",
            "adc", "sbb", "shl", "shr", "sar", "rol", "ror", "xchg", "cmpxchg", "xadd", "stos", "movs")
def is_store(x, k):
    """operand k of x is a memory destination that is written"""
    mn = x.mnemonic
    if k != 0: return mn in ("xchg", "xadd", "cmpxchg")
    if x.operands[0].type != X86_OP_MEM: return False
    if mn in ("lea", "bt", "nop", "push", "call", "jmp", "clflush"): return False
    if mn.startswith(("cmp", "test", "ucomis", "comis", "vucomis", "vcomis", "j", "prefetch")): return False
    return True
def memsize(x, k): return x.operands[k].size

def abs_refs(lo, hi):
    """dword values in [lo,hi) inside .text that decode as an instruction's imm32 or disp32 (absolute-VA forms);
    only decodes on the owner's instruction boundary are kept (unowned: earliest start)."""
    from capstone.x86 import X86_OP_IMM
    cands = []
    for al, arr in _words():
        base = TVA + al
        for idx, v in enumerate(arr):
            if lo <= (v & 0xFFFFFFFF) < hi: cands.append((base + idx * 4, v & 0xFFFFFFFF))
    hits = {}; raw = []
    for p, v in cands:
        got = []
        for back in range(1, 13):
            x = _decode_at(p - back)
            if x is None or x.address + x.size < p + 4: continue
            ok = False
            if x.disp_offset == back and x.disp_size == 4:
                ok = any(op.type == X86_OP_MEM and (op.mem.base == 0 or x.reg_name(op.mem.base) != "rip") and (op.mem.disp & 0xFFFFFFFF) == v for op in x.operands)
            if not ok and x.imm_offset == back and x.imm_size in (4, 8):
                ok = any(op.type == X86_OP_IMM and (op.imm & 0xFFFFFFFF) == v for op in x.operands)
            if ok: got.append((x, 0))
        got = _pick(got)
        if got:
            for x, k in got: hits[x.address] = (x, v)
        else: raw.append((p, v))
    return [hits[a] for a in sorted(hits)], raw
