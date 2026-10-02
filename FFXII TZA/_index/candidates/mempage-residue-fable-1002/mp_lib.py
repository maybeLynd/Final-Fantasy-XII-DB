"""mp_lib.py - shared, read-only image helpers for the mempage-residue-fable-1002 scripts (FABLE, 2026-10-02).

Image: Database/Tools/work/exe/FFXII_TZA.exe (sha256 checked below); canonical addresses = PE ImageBase 0x120000 + RVA.
Function list: Database/Tools/work/graph/functions.tsv (entry, name, body_bytes).

Instruments:
  raw_index(targets)  - every E8/E9 rel32, 0F 80..8F rel32 and EB/70..7F rel8 in .text whose target is in `targets`,
                        independent of the function list; each hit is then checked for decode alignment inside its
                        owner function (a byte coincidence is reported, not counted).
  decode(fn)          - capstone (detail) instructions of one listed body; section-aware file offsets.
  all_functions()     - every listed body.
  mem_writes(ins)     - (operand, width) for each memory operand the instruction WRITES (capstone access flags),
                        so a store's width is the operand size, never the next field's offset.
"""
import bisect, hashlib, os, struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_AC_WRITE, CS_AC_READ
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
DBROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))          # .../Database
EXE = os.path.join(DBROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(DBROOT, "Tools", "work", "graph", "functions.tsv")
EDGES = os.path.join(DBROOT, "Tools", "work", "graph", "edges.tsv")
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"

d = open(EXE, "rb").read()
assert hashlib.sha256(d).hexdigest() == SHA, "exe hash mismatch"
_pe = struct.unpack_from("<I", d, 0x3C)[0]
_nsec = struct.unpack_from("<H", d, _pe + 6)[0]
_opt = struct.unpack_from("<H", d, _pe + 20)[0]
BASE = struct.unpack_from("<Q", d, _pe + 24 + 24)[0]
assert BASE == 0x120000
SECS = []
for _i in range(_nsec):
    _o = _pe + 24 + _opt + _i * 40
    SECS.append((d[_o:_o + 8].rstrip(b"\0").decode(), struct.unpack_from("<I", d, _o + 12)[0],
                 struct.unpack_from("<I", d, _o + 8)[0], struct.unpack_from("<I", d, _o + 20)[0],
                 struct.unpack_from("<I", d, _o + 16)[0]))
TEXT = [s for s in SECS if s[0] == ".text"][0]
TEXT_VA, TEXT_SZ = BASE + TEXT[1], TEXT[2]


def off(addr):
    """file offset of an image address, section-aware; None past raw data (zero-initialised tail)."""
    r = addr - BASE
    for _n, va, vs, ro, rs in SECS:
        if va <= r < va + vs:
            return ro + (r - va) if r - va < rs else None
    return None


funcs, names = {}, {}
for _line in open(FUNCS, encoding="utf-8", errors="replace"):
    _p = _line.rstrip("\n").split("\t")
    try:
        _e = int(_p[0], 16)
    except ValueError:
        continue
    funcs[_e] = int(_p[2]); names[_e] = _p[1]
STARTS = sorted(funcs)


def owner(a):
    i = bisect.bisect_right(STARTS, a) - 1
    if i >= 0 and STARTS[i] <= a < STARTS[i] + funcs[STARTS[i]]:
        return STARTS[i]
    return None


md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
_cache = {}


def decode(fn):
    if fn not in _cache:
        o = off(fn)
        _cache[fn] = list(md.disasm(d[o:o + funcs[fn]], fn)) if o is not None else []
    return _cache[fn]


def all_functions():
    return [e for e in STARTS if funcs[e] > 0 and TEXT_VA <= e < TEXT_VA + TEXT_SZ]


def raw_index(targets):
    """{target: [(site, form, owner_or_None, aligned_bool)]} from a byte scan of .text."""
    targets = set(targets)
    base = off(TEXT_VA)
    blob = d[base:base + TEXT_SZ]
    hits = {t: [] for t in targets}
    n = len(blob)
    for i in range(n - 1):
        b0 = blob[i]
        t = None
        if b0 in (0xE8, 0xE9) and i + 5 <= n:
            t = TEXT_VA + i + 5 + struct.unpack_from("<i", blob, i + 1)[0]; form = "call" if b0 == 0xE8 else "jmp"
            if t in targets: hits[t].append((TEXT_VA + i, form))
        if b0 == 0x0F and i + 6 <= n and 0x80 <= blob[i + 1] <= 0x8F:
            t = TEXT_VA + i + 6 + struct.unpack_from("<i", blob, i + 2)[0]
            if t in targets: hits[t].append((TEXT_VA + i, "jcc32"))
        if (b0 == 0xEB or 0x70 <= b0 <= 0x7F):
            t = TEXT_VA + i + 2 + struct.unpack_from("<b", blob, i + 1)[0]
            if t in targets: hits[t].append((TEXT_VA + i, "jmp8" if b0 == 0xEB else "jcc8"))
    out = {}
    for t, lst in hits.items():
        res = []
        for site, form in lst:
            o = owner(site)
            aligned = False
            if o is not None:
                for x in decode(o):
                    if x.address == site:
                        aligned = x.op_str == hex(t) and (x.mnemonic.startswith("j") or x.mnemonic == "call")
                        break
            res.append((site, form, o, aligned))
        out[t] = res
    return out


def rip_target(x, op):
    return x.address + x.size + op.mem.disp


def mem_writes(x):
    """[(op, width)] memory operands this instruction writes."""
    out = []
    for op in x.operands:
        if op.type == X86_OP_MEM and (op.access & CS_AC_WRITE):
            out.append((op, op.size))
    return out


def mem_reads(x):
    out = []
    for op in x.operands:
        if op.type == X86_OP_MEM and (op.access & CS_AC_READ):
            out.append((op, op.size))
    return out


def reg_name(r):
    return md.reg_name(r) if r else ""


def head_sha():
    import subprocess
    try:
        return subprocess.check_output(["git", "-C", DBROOT, "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "?"


def imports():
    """{iat_slot_address: (dll, name)} from the PE import directory."""
    rva, _size = struct.unpack_from("<II", d, _pe + 24 + 112 + 8)
    res = {}
    o = off(BASE + rva)
    while True:
        oft, _ts, _fc, name_rva, ft = struct.unpack_from("<IIIII", d, o)
        if name_rva == 0:
            break
        dll = d[off(BASE + name_rva):].split(b"\0")[0].decode()
        k = 0
        while True:
            thunk = struct.unpack_from("<Q", d, off(BASE + (oft or ft)) + 8 * k)[0]
            if thunk == 0:
                break
            nm = ("#%d" % (thunk & 0xFFFF)) if thunk >> 63 else d[off(BASE + (thunk & 0x7FFFFFFF)) + 2:].split(b"\0")[0].decode()
            res[BASE + ft + 8 * k] = (dll, nm)
            k += 1
        o += 20
    return res


def import_thunks(wanted):
    """{thunk_address: name} for every 6-byte `jmp qword ptr [rip+X]` in .text whose slot imports a name in `wanted`."""
    imp = imports()
    slots = {a: n for a, (dll, n) in imp.items() if n in wanted}
    base = off(TEXT_VA)
    blob = d[base:base + TEXT_SZ]
    out = {}
    i = blob.find(b"\xff\x25")
    while i != -1:
        if i + 6 <= len(blob):
            t = TEXT_VA + i + 6 + struct.unpack_from("<i", blob, i + 2)[0]
            if t in slots:
                out[TEXT_VA + i] = slots[t]
        i = blob.find(b"\xff\x25", i + 1)
    return out
