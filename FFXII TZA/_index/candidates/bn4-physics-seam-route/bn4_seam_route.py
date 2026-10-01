"""BN-4 narrowing control (OPUS, 2026-09-27): how the Bullet seam 006883A0 can be entered.

Static, original EXE 73461d... only.  Asserts:
 S1  006883A0 is named by exactly two image qwords, both slot +0x70 of a PPhysicsWorld class-DESCRIPTOR vtable
     (PClassDescriptorAbstract / PClassDescriptorConcrete<PPhysicsWorld>); no rel32 or RIP-relative reference.
 S2  slot +0x70 is the per-class hook most classes leave as the stub 005C5230 (>= 290 of the 315 descriptor tables).
 S3  no class RTTI names PPhysicsWorld itself, so an instance exists only through reflection (descriptor default
     buffer or a created/loaded object), never through a native constructor that installs a class vtable.
 S4  every image reference to the PPhysicsWorld descriptor 02E494D0 is followed by a registration, type-signature,
     type-check, default-instance, descriptor ctor/dtor or atexit call - none by a create/construct call.
Mutant M1: a synthetic third qword naming 006883A0 inside another vtable is detected by S1's scan.
"""
import hashlib, pathlib, struct, sys, collections
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = pathlib.Path(__file__).resolve().parent
DB = HERE.parents[2]
EXE = DB.parent / "Tools" / "work" / "exe" / "FFXII_TZA.exe"
VTT = DB / "22-Middleware-PhyreEngine" / "Reflection-And-Class-Metadata" / "members" / "phyre-class-descriptor-vtable.tsv"
RTTI = DB / "22-Middleware-PhyreEngine" / "Reflection-And-Class-Metadata" / "members" / "rtti-class-vtables.tsv"
raw = EXE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
pe = pefile.PE(data=raw, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
def at(va, n, buf=raw): o = pe.get_offset_from_rva(va - IB); return buf[o:o + n]
def q(va, buf=raw): return struct.unpack("<Q", at(va, 8, buf))[0]
def rtti(vt):
    col = q(vt - 8); td = struct.unpack("<I", at(col + 12, 4))[0] + IB
    return at(td + 16, 200).split(b"\0")[0].decode()
SEAM, DESC = 0x6883A0, 0x2E494D0
text = next(s for s in pe.sections if s.Name.startswith(b".text"))
TV, TO, TL = IB + text.VirtualAddress, text.PointerToRawData, text.Misc_VirtualSize

def qword_refs(buf, tgt):
    out, pat = [], struct.pack("<Q", tgt); i = buf.find(pat)
    while i != -1: out.append(IB + pe.get_rva_from_offset(i)); i = buf.find(pat, i + 1)
    return out
def code_refs(tgt):
    tb = raw[TO:TO + TL]; out = []
    for p in range(len(tb) - 6):
        if tb[p] in (0xE8, 0xE9) and TV + p + 5 + struct.unpack_from("<i", tb, p + 1)[0] == tgt: out.append(("rel32", TV + p))
        if (tb[p] & 0xC7) == 0x05:
            d = struct.unpack_from("<i", tb, p + 1)[0]
            for imm in (0, 1, 4):
                if TV + p + 5 + imm + d == tgt: out.append(("riprel", TV + p)); break
    return out
def vtable_of(slot):
    s = slot
    while 0x121000 <= q(s - 8) < 0x8C3000: s -= 8
    return s

# S1
qs = qword_refs(raw, SEAM)
S1 = [(("%08X" % x), "%08X" % vtable_of(x), x - vtable_of(x), rtti(vtable_of(x))) for x in qs]
assert len(S1) == 2 and all(o == 0x70 and "PPhysicsWorld@PPhysics" in n and "PClassDescriptor" in n for _, _, o, n in S1), S1
cr = code_refs(SEAM)
assert cr == [], cr
# M1: plant a third qword in a copy (inside another descriptor table slot) -> detected
mut = bytearray(raw); o = pe.get_offset_from_rva(0xD70BC8 + 0x78 - IB); mut[o:o + 8] = struct.pack("<Q", SEAM)
assert len(qword_refs(bytes(mut), SEAM)) == 3
# S2
rows = [l.rstrip("\r\n").split("\t") for l in VTT.read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
iv = rows[0].index("descriptor_vtable")
c = collections.Counter(q(int(r[iv], 16) + 0x70) for r in rows[1:])
assert c[0x5C5230] >= 290, c.most_common(3)
# S3
names = [l.split("\t")[0] for l in RTTI.read_text(encoding="utf-8").splitlines() if "\t" in l and not l.startswith("#")]
assert not any(n in ("PPhysicsWorld", ".?AVPPhysicsWorld@PPhysics@Phyre@@") for n in names)
# S4
md = Cs(CS_ARCH_X86, CS_MODE_64)
ALLOWED = {0x690950: "descriptor ctor", 0x808B90: "atexit", 0x63E2E0: "type check", 0x684080: "adapter thunk",
           0x632960: "member registration", 0x6388C0: "by-name registration", 0x632FB0: "method caller node",
           0x63BC00: "default instance", 0x6B1600: "signature table", 0x6301F0: "signature table",
           0x630180: "signature table", 0x633390: "descriptor dtor", 0x639450: "registration finaliser"}
refs = [a for k, a in code_refs(DESC)]
seen = collections.Counter()
for a in refs:
    ins = list(md.disasm(at(a - 2, 64), a - 2))   # the modrm byte sits after a REX + opcode
    nxt = next((i for i in ins[1:8] if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x")), None)
    t = int(nxt.op_str, 16) if nxt else None
    if t is None: seen["parent-chain compare (no call)"] += 1; continue
    assert t in ALLOWED, "%08X -> %08X is not a known non-creating call" % (a, t)
    seen[ALLOWED[t]] += 1
assert len(refs) == 29, len(refs)
print("S1 seam = PPhysicsWorld descriptor slot +0x70 only:", [(v, n.split("@")[0]) for _, v, _, n in S1])
print("S2 slot +0x70 stub on", c[0x5C5230], "descriptor tables; S3 no class RTTI for PPhysicsWorld")
print("S4 29 descriptor references:", dict(seen))
print("M1 planted qword detected; PASS")
