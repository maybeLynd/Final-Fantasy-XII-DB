"""softedges_check.py - FABLE's re-check of the image and asset facts its SOFTEDGES consumption restates
(ASTRA returns reviewed by SWE2-AUDIT-SPEC at d5f06584e). Decodes each cited instruction with capstone and compares
its text; checks the shipped PhyreText asset's hash, length and the softEdges record bytes. Prints PASS/FAIL, FAILS n.
Sensitivity: every check compares against an exact expected decode or byte string, so a wrong address, a wrong
section mapping or a different asset fails. The two string reads ("softEdges", "m_els") go through the same
section-aware offset function as the instruction reads. The textColor / alphaThreshold size controls are the
reviewer's (fe_controls.out) and are not repeated here."""
import hashlib, os, struct, sys
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
ASSET = "D:/FFXII_TZA_extract/gamedata/d3d11/artdata/shaders/phyretext.fx.phyre"
BASE = 0x120000

data = open(EXE, "rb").read()
pe = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, pe + 6)[0]
optsz = struct.unpack_from("<H", data, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + optsz + 40 * i
    vsz, va, rsz, raw = struct.unpack_from("<IIII", data, o + 8)
    secs.append((va, vsz, raw, rsz))
def off(a):
    r = a - BASE
    for va, vsz, raw, rsz in secs:
        if va <= r < va + max(vsz, rsz): return raw + r - va
    raise ValueError(hex(a))
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
def ins(a):
    i = next(md.disasm(data[off(a):off(a) + 16], a))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()
def cstr(a):
    o = off(a); return data[o:data.index(b"\0", o)].decode("latin-1")

fails = 0
def check(name, ok, got=""):
    global fails
    print("%s %s %s" % ("PASS" if ok else "FAIL", name, got))
    if not ok: fails += 1

# field extent (5bbbe5528): the constructor's route and the copy's destination
for a, want in [(0x1D03C6, "add rcx, 8"), (0x1EA3DC, "mov rsi, rcx"), (0x1EA5C1, "lea r10, [rsi + 0x118]")]:
    got = ins(a); check("%08X %s" % (a, want), got == want, "-> " + got)
got = ins(0x1D03CA); check("001D03CA call 001EA3C0", got == "call 0x1ea3c0", "-> " + got)
got = ins(0x1EA5AD); tgt = 0x1EA5AD + 7 + struct.unpack_from("<i", data, off(0x1EA5AD) + 3)[0]
check("001EA5AD lea rdx -> \"softEdges\"", got.startswith("lea rdx") and cstr(tgt) == "softEdges", "-> %08X %r" % (tgt, cstr(tgt)))
# pointer keys (a50f9dea4): the guard's polarity and the 32-bit address arithmetic
for a, want in [(0x59ECDE, "cmp eax, 1"), (0x59ECE1, "sete al"), (0x59ED3F, "lea eax, [rdx + rbx]"), (0x59ED42, "add rax, r13")]:
    got = ins(a); check("%08X %s" % (a, want), got == want, "-> " + got)
# member boundaries (7a524fda9) and preassignment (451897b9d)
for a, want in [(0x60EFF8, "test r8d, r8d"), (0x59CC84, "movsxd rdx, ecx"), (0x59CD14, "mov qword ptr [rdx], r13")]:
    got = ins(a); check("%08X %s" % (a, want), got == want, "-> " + got)
got = cstr(0xD32DC0); check("00D32DC0 \"m_els\"", got == "m_els", "-> %r" % got)

# the shipped asset
b = open(ASSET, "rb").read()
h = hashlib.sha256(b).hexdigest()
check("asset length 44,634", len(b) == 44634, str(len(b)))
check("asset sha256 f67d4492...a767a4cf", h.startswith("f67d4492") and h.endswith("a767a4cf"), h[:8] + "..." + h[-8:])
rec = b[29328:29341]
check("softEdges record at 29328", rec.hex() == "0000400100a0000800b8000000", rec.hex())
check("softEdges record size word 8", struct.unpack_from("<H", rec, 7)[0] == 8, str(struct.unpack_from("<H", rec, 7)[0]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
