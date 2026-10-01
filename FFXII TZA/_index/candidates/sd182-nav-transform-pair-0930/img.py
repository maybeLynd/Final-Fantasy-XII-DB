"""img.py - shared image helpers (ORACLE, 2026-09-30): PE mapping, .pdata chain-root extents, raw E8/E9 rel32 index,
rip-relative target from the decoded operand (never from op_str text)."""
import bisect, io, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP

# the record folder is Database/FFXII TZA/_index/candidates/<record>/; the image is Database/Tools/work/exe/
EXE = os.environ.get("FFXII_EXE") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                  "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"))
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData),
         s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + rawsz:
            return raw + (va - start)
    raise ValueError("%08X" % va)


def sec(name):
    return [s for s in SECS if s[0] == name][0]


def rd(va, n):
    return blob[OFF(va):OFF(va) + n]


def u32(va):
    return struct.unpack("<I", rd(va, 4))[0]


def dis(va, n):
    return list(md.disasm(rd(va, n), va))


def ripmem(x):
    """rip-relative memory target of a decoded instruction, or None."""
    for o in x.operands:
        if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP:
            return x.address + x.size + o.mem.disp
    return None


# .pdata: RUNTIME_FUNCTION (begin, end, unwind). Chained unwind info (flag 4) points to the parent function entry.
_p = sec(".pdata")
PDATA = []
for k in range(0, _p[4] // 12):
    b, e, u = struct.unpack("<III", blob[_p[3] + 12 * k:_p[3] + 12 * k + 12])
    if b == 0:
        break
    PDATA.append((BASE + b, BASE + e, BASE + u))
PDATA.sort()
_ps = [p[0] for p in PDATA]


def _root(entry):
    b, e, u = entry
    seen = 0
    while seen < 64:
        seen += 1
        uo = OFF(u)
        ver_fl = blob[uo]; ncodes = blob[uo + 2]
        if (ver_fl >> 3) & 4:  # UNW_FLAG_CHAININFO
            off = uo + 4 + 2 * ((ncodes + 1) & ~1)
            b2, e2, u2 = struct.unpack("<III", blob[off:off + 12])
            b, e, u = BASE + b2, BASE + e2, BASE + u2
        else:
            return (b, e, u)
    return (b, e, u)


ROOTS = {}   # root begin -> list of fragments (begin,end)
FRAG_ROOT = {}
for ent in PDATA:
    r = _root(ent)
    ROOTS.setdefault(r[0], []).append((ent[0], ent[1]))
    FRAG_ROOT[ent[0]] = r[0]


def owner(va):
    """chain-root function entry owning va, via .pdata fragment."""
    j = bisect.bisect_right(_ps, va) - 1
    if j >= 0 and PDATA[j][0] <= va < PDATA[j][1]:
        return FRAG_ROOT[PDATA[j][0]]
    return None


def fragments(root):
    return sorted(ROOTS.get(root, []))


def fn_ins(root):
    out = []
    for b, e in fragments(root):
        out += dis(b, e - b)
    return out


TX = sec(".text")
T0, TR, TN = TX[1], TX[3], TX[4]
_CALLIDX = None


def calls_to(target):
    """raw rel32 E8/E9 sites whose target is `target`."""
    t = blob[TR:TR + TN]
    res = []
    for m in re.finditer(rb"[\xe8\xe9]", t[:-4]):
        o = m.start()
        if T0 + o + 5 + struct.unpack("<i", t[o + 1:o + 5])[0] == target:
            res.append((T0 + o, "call" if t[o] == 0xE8 else "jmp"))
    return res


def pr(ins, f=sys.stdout):
    for x in ins:
        t = ripmem(x)
        f.write("%08X  %-7s %s%s\n" % (x.address, x.mnemonic, x.op_str, ("   ; [%08X]" % t) if t else ""))
