"""The stream object's +0x20 region is a BASE sub-object, not a member (OPUS, 2026-09-27), answering the question
how-a-path-is-resolved-to-bytes.md routes to the structural lane: 'Whether +0x20 is a nested member or a base
sub-object'.

  R1 00597970 installs vtable 00D26C90, whose complete-object locator names Phyre::PSerialization::PStreamReaderFile
  R2 that class's RTTI base-class array lists PStreamFile and PStreamFileWin32 at mdisp 0x20 (pdisp -1: not virtual),
     beside PStreamReader / PStream at 0 and PMemoryBase at 8 - the compiler's own record of the layout
  R3 the standalone 0x30-byte constructor 00597930 installs no vtable (no lea of an .rdata address stored to [rcx]):
     the base is non-polymorphic, which is why no second vtable pointer sits at +0x20
  N  negative control: the same parser reads PStream (vtable 00D26C60) as having no base at 0x20
Not claimed: which of PStreamFile / PStreamFileWin32 00597930 constructs (they share the displacement), or the
fields' meaning.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
q = lambda v: struct.unpack_from("<Q", d, off(v))[0]
u = lambda v: struct.unpack_from("<I", d, off(v))[0]
nm = lambda td: d[off(B + td + 0x10):off(B + td + 0x10) + 96].split(b"\0")[0].decode()
def rtti(vt):
    col = q(vt - 8)
    sig, offs, cdoff, tdr, chdr, selfr = struct.unpack_from("<IIIIII", d, off(col))
    s2, attr, nb, bca = struct.unpack_from("<IIII", d, off(B + chdr))
    bases = []
    for k in range(nb):
        tdr2, ncont, mdisp, pdisp, vdisp, battr, chd2 = struct.unpack_from("<IIiiiII", d, off(B + u(B + bca + 4 * k)))
        bases.append((nm(tdr2), mdisp, pdisp))
    return nm(tdr), bases
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
def leas(f, size):
    out = []
    for x in cs.disasm(d[off(f):off(f) + size], f):
        m = re.search(r"rip \+ (0x[0-9a-f]+)", x.op_str)
        if x.mnemonic == "lea" and m: out.append((x.address, x.address + x.size + int(m.group(1), 16)))
        if x.mnemonic == "ret": break
    return out
vts = [v for a, v in leas(0x597970, 0x120)]
cls, bases = rtti(0xD26C90)
check("R1 00597970 installs 00D26C90, PStreamReaderFile", 0xD26C90 in vts and cls == ".?AVPStreamReaderFile@PSerialization@Phyre@@")
at20 = sorted(b for b, md, pd in bases if md == 0x20)
check("R2 PStreamFile and PStreamFileWin32 are bases at mdisp 0x20 (non-virtual)",
      at20 == [".?AVPStreamFile@PSerialization@Phyre@@", ".?AVPStreamFileWin32@PSerialization@Phyre@@"]
      and all(pd == -1 for b, md, pd in bases if md == 0x20), str(bases))
check("R3 00597930 installs no vtable", not leas(0x597930, 0x3B))
c2, b2 = rtti(0xD26C60)
check("N  PStream has no base at 0x20", c2 == ".?AVPStream@PSerialization@Phyre@@" and all(md != 0x20 for b, md, pd in b2), str(b2))
print("FAILS", fails)
sys.exit(1 if fails else 0)
