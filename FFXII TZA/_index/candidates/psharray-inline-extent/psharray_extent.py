"""PSharray<T> is not one size: a by-value element is stored inline (OPUS, 2026-09-27).
Distinguishes four things a PSharray row can mean, and checks only the first three:
  native layout      - the object's bytes in memory (V1-V5)
  serialized offsets - the member address is member[+0x48] - classdesc[+0xF4]; the file schema's order is another
                       representation (V6 reads the adjustment in the shared accessor; no file offset is used here)
  ownership flag     - bit 31 of the count keeps a buffer from release; an inline element is never released (V6)
  element semantics  - NOT claimed beyond the D3D11 buffer-creation call's argument shape (V4 is representation)
Checks (static, certified EXE 73461d08...21f8):
  V1 the nine PSharray<T> class descriptors state their instance size to 00632D80: seven 0x10, two 0x50
  V2 the two by-value element classes (PDataBlockBufferD3D11 02D39B40, PIndexDataBlockBufferD3D11 02D39940) are 0x48
  V3 every measured size equals 8 + max(8, sizeof(T)) - header, then a union of T* and one inline T
  V4 0066F970 / 0066FAB0 walk m_buffers of PDataBlockD3D11 / PIndexDataBlockD3D11: count at +0x20 / +0x18, the
     count-1 base is the inline address +0x28 / +0x20, stride i*9*8 = 0x48, and m_dataSize is read at +0x78 / +0x70
  V5 m_buffers + 0x50 is the next registered member of both classes (m_offsetInVertexBuffer +0x70,
     m_offsetInIndexBuffer +0x68) and no registration lies between
  V6 the shared accessor 0063B9B0: count <= 1 -> the address +8 (null at 0); address = member[+0x48] - class[+0xF4];
     the resize 006C7A40 releases the old storage only when it is not the inline address and bit 31 is clear
  S  REGRESSION: the store sizes the by-value pair at 80 bytes with no 64-byte gap after them, PSharray's size cell is
     VARIABLE, and the page no longer states one PSharray size (FAILS before the patch)
  N  NEGATIVE: the tile rule rejects the 0x10 generalisation on a by-value member and keeps the 16-byte pointer members
"""
import json, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(os.path.dirname(DB), "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read(); B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)) if m else None
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok

def r9_before(ins, k):
    """The r9d value set before instruction k: `mov r9d, imm` or `lea r9d, [reg + imm]` with reg zeroed earlier."""
    def full(r): return re.sub(r"^(r\d+)d$", r"\1", re.sub(r"^e(\w\w)$", r"r\1", r))
    zero = set()
    for x in ins[:k]:
        m = re.match(r"(\w+), (\w+)$", x.op_str)
        if x.mnemonic == "xor" and m and m.group(1) == m.group(2): zero.add(full(m.group(1)))
    for x in reversed(ins[:k]):
        if x.op_str.startswith("r9d,") or x.op_str.startswith("r9,"):
            m = re.match(r"r9d?, (0x[0-9a-f]+|\d+)$", x.op_str)
            if x.mnemonic == "mov" and m: return int(m.group(1), 0)
            m = re.match(r"r9d, \[(\w+) \+ (0x[0-9a-f]+)\]$", x.op_str)
            if x.mnemonic == "lea" and m and m.group(1) in zero: return int(m.group(2), 16)
            return None
def desc_size(registrar, desc=None):
    ins = dis(registrar, 0x200)
    for k, x in enumerate(ins):
        if x.mnemonic == "call" and x.op_str == "0x632d80":
            return r9_before(ins, k)

# V1: the nine PSharray<T> class registrars (they register the template's own m_u at +8 through 00632A10, a7=2)
REG = {"005B7AC0": ("PEAVPAnimationClip", 8), "005EFB10": ("I", 4), "005EFE60": ("PEBVPMeshInstanceSegmentStreamBinding", 8),
       "0066A460": ("PEAVPMaterial", 8), "0066A7B0": ("VPDataBlockBufferD3D11", None), "0066AB00": ("VPIndexDataBlockBufferD3D11", None),
       "00698930": ("PEAVPPhysicsShape", 8), "006A84C0": ("PEAVPTriggerReceiverComponent", 8), "006C6560": ("PEAVPMeshInstance", 8)}
harvest = json.load(open(os.path.join(DB, "_index", "candidates", "rm1-array-members", "harvest.json"), encoding="utf-8"))
mu = {r["caller"]: r for r in harvest if r.get("name") == "m_u"}
sizes = {a: desc_size(int(a, 16)) for a in REG}
check("V1 nine PSharray<T> descriptors: seven 0x10, two 0x50",
      set(mu) == set(REG) and all(mu[a]["offset"] == 8 and mu[a]["a7"] == 2 and REG[a][0] in mu[a]["member_class"] for a in REG)
      and sorted(sizes.values()) == [0x10] * 7 + [0x50] * 2 and sizes["0066A7B0"] == sizes["0066AB00"] == 0x50,
      str({a: hex(v) if v else v for a, v in sizes.items()}))

# V2: the element classes' own sizes, from the registrar that leas each descriptor and constructs it
def element_size(desc):
    text = [s for s in SECS if s[0] == b".text"][0]; lo = B + text[2]; hi = lo + text[3]
    for m in re.finditer(rb"\x48\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]", d[off(lo):off(lo) + text[3]]):
        a = lo + m.start(); x = next(cs.disasm(d[off(a):off(a) + 7], a), None)
        if not x or rip(x) != desc: continue
        ins = dis(a, 0x100)
        for k, y in enumerate(ins[:8]):
            if y.mnemonic != "call" or not y.op_str.startswith("0x"): continue
            # either the descriptor constructor itself, or the registrar the caller hands the descriptor to in rcx
            v = r9_before(ins, k) if y.op_str == "0x632d80" else (desc_size(int(y.op_str, 16)) if x.op_str.startswith("rcx,") else None)
            if v: return v
            break
EL = {"VPDataBlockBufferD3D11": element_size(0x2D39B40), "VPIndexDataBlockBufferD3D11": element_size(0x2D39940)}
check("V2 the two by-value elements are 0x48", list(EL.values()) == [0x48, 0x48], str({k: hex(v) if v else v for k, v in EL.items()}))

# V3: size = 8 + max(8, sizeof(T))
pred = {a: 8 + max(8, REG[a][1] if REG[a][1] else EL[REG[a][0]] or 0) for a in REG}
check("V3 every measured size is 8 + max(8, sizeof T)", pred == sizes)

# V4: the engine's own walk over the inline element
def at(a): return next(cs.disasm(d[off(a):off(a) + 16], a))
def v4(fn, dsz, cnt, base, bind, loads):
    ins = dis(fn, 0x140); ops = [(x.mnemonic, x.op_str) for x in ins]
    return (("mov", "edi, dword ptr [rcx + 0x%x]" % dsz) in ops and ("mov", "ebp, dword ptr [rbx + 0x%x]" % cnt) in ops
            and ("lea", "rdx, [rbx + 0x%x]" % base) in ops and ("lea", "rcx, [rax + rax*8]") in ops
            and ("lea", "r9, [rdx + rcx*8]") in ops and ("add", "rsi, 0x48") in ops
            and ("mov", "dword ptr [rsp + 0x28], %d" % bind) in ops and ("call", "qword ptr [r10 + 0x18]") in ops
            and all(at(a).op_str == "eax, dword ptr [rbx + 0x%x]" % cnt for a in loads))
check("V4 0066F970 / 0066FAB0: inline base at +0x28 / +0x20, stride 0x48, m_dataSize +0x78 / +0x70",
      v4(0x66F970, 0x78, 0x20, 0x28, 1, [0x66FA10, 0x66FA4D]) and v4(0x66FAB0, 0x70, 0x18, 0x20, 2, [0x66FB50, 0x66FB8D]))

# V5: the next registered member of both classes is m_buffers + 0x50
schema = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(DB, "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
          "phyre-field-schema.tsv"), encoding="utf-8")][1:]
def regs(cls):
    out = {int(r[3], 16): r[2] for r in schema if r[0] == cls}
    for r in harvest:
        if r.get("cls") == cls: out[r["offset"]] = r["name"]
    return out
ok5 = True; det = []
for cls, mb in (("PDataBlockD3D11", 0x20), ("PIndexDataBlockD3D11", 0x18)):
    rg = regs(cls); after = sorted(o for o in rg if o > mb)
    ok5 &= rg.get(mb) == "m_buffers" and bool(after) and after[0] == mb + 0x50
    det.append("%s m_buffers +0x%x next %s" % (cls, mb, after and "%s +0x%x" % (rg[after[0]], after[0])))
check("V5 m_buffers + 0x50 is the next registration", ok5, "; ".join(det))

# V6: the shared accessor and the resize (ownership)
acc = [(x.mnemonic, x.op_str) for x in dis(0x63B9B0, 0x30)]
rsz = [(x.mnemonic, x.op_str) for x in dis(0x6C7A40, 0xB0)]
check("V6 accessor: inline address at count 1, offset minus class +0xF4; resize spares inline and bit-31 storage",
      acc[:3] == [("mov", "rax, qword ptr [rcx + 0x18]"), ("mov", "ecx, dword ptr [rcx + 0x48]"), ("sub", "ecx, dword ptr [rax + 0xf4]")]
      and ("btr", "ecx, 0x1f") in acc and ("add", "rax, 8") in acc and ("cmove", "rax, rdx") in acc
      and ("lea", "rdi, [rcx + 8]") in rsz and ("cmp", "rbx, rdi") in rsz and ("shr", "eax, 0x1f") in rsz and ("call", "0x584730") in rsz)

# the tile rule, shared by S and N: a by-value PSharray member must be 8 + sizeof(T) wide and leave no gap behind it
def tile_ok(rows, cls, mb, width):
    r = {int(x[1], 16): x for x in rows if x[0] == cls}
    return mb in r and int(r[mb][2]) == width and (mb + 0x10) not in r
F = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")]
ptr_ok = all(any(x[0] == c and int(x[1], 16) == o and x[2] == "16" for x in F)
             for c, o in (("PMeshInstanceSegmentContext", 0x38), ("PPhysicsRigidBodyBase", 0xB0), ("PLODLevel", 0x8)))
syn_bad = [["PDataBlockD3D11", "0x0020", "16"], ["PDataBlockD3D11", "0x0030", "64"]]
syn_good = [["PDataBlockD3D11", "0x0020", "80"]]
check("N the tile rule rejects a 16-byte by-value member and keeps the 16-byte pointer members",
      not tile_ok(syn_bad, "PDataBlockD3D11", 0x20, 0x50) and tile_ok(syn_good, "PDataBlockD3D11", 0x20, 0x50) and ptr_ok)

T = {l.split("\t")[0]: l.rstrip("\r\n").split("\t") for l in open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8")}
page = open(os.path.join(DB, "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                         "member-registration-and-the-recovered-field-schema.md"), encoding="utf-8").read()
live = re.sub(r"~~.*?~~", "", page, flags=re.S)
check("S the store and the page follow the inline extent",
      tile_ok(F, "PDataBlockD3D11", 0x20, 0x50) and tile_ok(F, "PIndexDataBlockD3D11", 0x18, 0x50)
      and T["PSharray"][1].startswith("VARIABLE") and "`PSharray`'s size is `0x10`" not in live)
print("FAILS", fails)
sys.exit(1 if fails else 0)
