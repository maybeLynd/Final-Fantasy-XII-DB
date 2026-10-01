"""ind.py - SWE2-AUDIT-SPEC review worker library (2026-09-30). pefile + capstone only; no kit or package tool.

Loads the certified image (sha256 asserted), and gives:
  off(va) section-aware file offset (None past SizeOfRawData = zero-initialised virtual tail)
  dis(a, b) linear decode; ins(a) one instruction; txt(i)
  pdata: FUNCS (sorted begin VAs of .pdata roots, chained entries folded), fext(f) -> (begin, end) of the root's
         own primary range, func_of(va) -> the .pdata root that owns va (chain-followed)
  body(f) decode of every .pdata range whose chain root is f (sorted), so split functions are complete
  calls_to(t) raw E8 / E9 / 0F 8x rel32 sites whose target is t (decoded to confirm), image-wide over .text
  relocs() set of DIR64 relocation site VAs; abs64_refs(lo, hi) relocated qwords whose value is in [lo, hi)
  rip_refs(lo, hi) / ib_refs(lo, hi) rip-relative and image-base-relative (disp32 = target - 0x120000) operands
  is_write(i, op) capstone 5 marks some SSE stores as READ: a write is decided by mnemonic + first operand
Addresses are canonical VAs (image base 0x120000 included).
"""
import array, bisect, hashlib, struct
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
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def off(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def rd(va, n):
    o = off(va)
    return None if o is None else raw[o:o + n]


def dis(a, b):
    o = off(a)
    return list(md.disasm(raw[o:o + (b - a)], a))


def ins(a):
    o = off(a)
    return next(md.disasm(raw[o:o + 16], a, 1))


def txt(i):
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def mem_ops(i):
    for k, op in enumerate(i.operands):
        if op.type == CS_OP_MEM:
            yield k, op


WRITE_MN = ("mov", "movups", "movaps", "movdqa", "movdqu", "movq", "movd", "movss", "movsd", "movlps", "movhps",
            "movlpd", "movhpd", "movnti", "stosq", "add", "sub", "and", "or", "xor", "inc", "dec", "neg", "not", "adc",
            "sbb", "shl", "shr", "sar", "rol", "ror", "bts", "btr", "btc", "xchg", "cmpxchg", "xadd", "setne", "sete",
            "movzx", "movsx")


def is_write(i, k):
    """memory operand k of i is written: first operand of a store/RMW form (never a cmp/test/bt/lea/push)."""
    if k != 0:
        return False
    m = i.mnemonic
    if m in ("cmp", "test", "bt", "lea", "push", "call", "jmp", "nop", "prefetcht0", "prefetcht1", "prefetchnta") or \
            m.startswith("cmov") or m.startswith("j") or m.startswith("ucomis") or m.startswith("comis"):
        return False
    if m.startswith("set") or m.startswith("mov") or m in WRITE_MN or m.startswith("vmov"):
        return True
    return len(i.operands) >= 2  # generic two-operand RMW with memory first


# ---- .pdata
_dd = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
_o = off(IB + _dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", raw, _o + 12 * k) for k in range(_dd.Size // 12))
_ST = [e[0] for e in PD]


def _root_entry(e):
    while True:
        uo = off(IB + e[2])
        fl = raw[uo] >> 3
        cnt = raw[uo + 2]
        if not (fl & 4):
            return e
        e = struct.unpack_from("<III", raw, uo + 4 + ((cnt + 1) & ~1) * 2)


ROOT_OF = {}
RANGES = {}
for e in PD:
    r = _root_entry(e)
    ROOT_OF[IB + e[0]] = IB + r[0]
    RANGES.setdefault(IB + r[0], []).append((IB + e[0], IB + e[1]))
FUNCS = sorted(RANGES)


def entry_of(va):
    rva = va - IB
    j = bisect.bisect_right(_ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    return PD[j]


def func_of(va):
    e = entry_of(va)
    return None if e is None else ROOT_OF[IB + e[0]]


def body(f):
    out = []
    for a, b in sorted(RANGES[f]):
        out += dis(a, b)
    return out


# ---- raw call index (E8, E9, 0F 80..8F) over executable sections, decoded to confirm
_CALLIDX = None


def _build_calls():
    global _CALLIDX
    idx = {}
    for n, v, vs, p, rs in TEXT:
        blob = raw[p:p + min(vs, rs)]
        L = len(blob)
        for k0 in range(4):
            cnt = (L - k0) // 4
            arr = array.array("i")
            arr.frombytes(blob[k0:k0 + 4 * cnt])
            for j, d in enumerate(arr):
                k = k0 + 4 * j  # disp starts at k
                if k >= 1 and blob[k - 1] in (0xE8, 0xE9):
                    idx.setdefault(v + k + 4 + d, []).append((v + k - 1, "E8" if blob[k - 1] == 0xE8 else "E9"))
                if k >= 2 and blob[k - 2] == 0x0F and 0x80 <= blob[k - 1] <= 0x8F:
                    idx.setdefault(v + k + 4 + d, []).append((v + k - 2, "JCC"))
    _CALLIDX = idx


def calls_to(t, confirm=True):
    if _CALLIDX is None:
        _build_calls()
    out = []
    for s, kind in _CALLIDX.get(t, []):
        if confirm:
            try:
                i = ins(s)
            except StopIteration:
                continue
            if i.size not in (5, 6) or not i.operands or i.operands[0].type != 2 or i.operands[0].imm != t:
                continue
            f = func_of(s)
            # boundary confirm: s must be an instruction start in its owner's linear decode
            if f is not None and s not in {x.address for x in body(f)}:
                kind += "?straddle"
        out.append((s, kind))
    return sorted(out)


# ---- relocations
_REL = None


def relocs():
    global _REL
    if _REL is None:
        pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_BASERELOC"]])
        s = set()
        for blk in getattr(pe, "DIRECTORY_ENTRY_BASERELOC", []):
            for e in blk.entries:
                if e.type == 10:
                    s.add(IB + e.rva)
        _REL = s
    return _REL


def abs64_refs(lo, hi):
    out = []
    for a in relocs():
        b = rd(a, 8)
        if b is None:
            continue
        v = struct.unpack("<Q", b)[0]
        if lo <= v < hi:
            out.append((a, v))
    return sorted(out)


def _back_decode(blob, v, k, want):
    best = None
    for back in range(12, 0, -1):
        if k - back < 0:
            continue
        got = list(md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
        if not got:
            continue
        i = got[0]
        if not (i.address < v + k < i.address + i.size):
            continue
        if want(i):
            best = i
            break
    return best


def rip_refs(lo, hi):
    hits = {}
    for n, v, vs, p, rs in TEXT:
        blob = raw[p:p + min(vs, rs)]
        L = len(blob)
        for k0 in range(4):
            cnt = (L - k0) // 4
            arr = array.array("i")
            arr.frombytes(blob[k0:k0 + 4 * cnt])
            base = v + k0 + 4
            for j, d in enumerate(arr):
                if not (lo - 8 <= base + 4 * j + d < hi):
                    continue
                k = k0 + 4 * j

                def want(i, k=k):
                    for _, op in mem_ops(i):
                        if op.mem.base == X86_REG_RIP and lo <= i.address + i.size + op.mem.disp < hi:
                            # the disp must be the dword at k
                            return True
                    return False
                i = _back_decode(blob, v, k, want)
                if i is not None:
                    hits[i.address] = i
    return [hits[a] for a in sorted(hits)]


def ib_refs(lo, hi):
    """disp32 in [lo-IB, hi-IB) with a non-rip base: the image-base-relative form."""
    hits = {}
    for n, v, vs, p, rs in TEXT:
        blob = raw[p:p + min(vs, rs)]
        L = len(blob)
        for k0 in range(4):
            cnt = (L - k0) // 4
            arr = array.array("I")
            arr.frombytes(blob[k0:k0 + 4 * cnt])
            for j, d in enumerate(arr):
                if not (lo - IB <= d < hi - IB):
                    continue
                k = k0 + 4 * j

                def want(i):
                    for _, op in mem_ops(i):
                        if op.mem.base not in (X86_REG_RIP,) and (op.mem.disp & 0xFFFFFFFF) == struct.unpack_from("<I", blob, k)[0]:
                            return True
                    return False
                i = _back_decode(blob, v, k, want)
                hits[v + k] = i
    return sorted(hits.items())
