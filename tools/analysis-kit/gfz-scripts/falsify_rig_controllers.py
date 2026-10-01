"""Falsification pass 1 on the-rig-of-seventeen-controllers (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  R0  sizes: 003E1350 629, 003E1610 629, 003E00C0 1,631, 0042EE90 254, 0042DD90 186, 004718D0 31, 00471640 27, 004716A0 290,
      00471150 220, 002E8570 110, 002EDF30 89, 002EE0D0 91, 002EDE70 91, 00428F80 82, 00421D20 70, 002EDDC0 95, 0042BDE0 230,
      00518F50 418, 0051A890 140, 00513150 108, 00515FE0 486
  R1  section 3: both switches bound n by `cmp edx, 0x10` / ja and jump through a 17-entry RVA table (003E15C8 off, 003E1888 on);
      index 4's arm is the plain exit in both, and every other index's arm is distinct
  R2  section 3: each timed service (002E85E0, 002E8B80, 002ED320) divides by [01DFE0BC] and tail-jumps to the setter that
      stores at +0x640 (002EDF30), +0x644 (002EE130), +0x648 (002EDED0);
      the lip-flap wrapper 0042DD90 reads the rig at +0x94 and tests record +0x304 bit 6
  R3  section 3: 0042EE90 tests +0x290 bit 1, the byte +0x40B, and subtracts [01DFE0BC]; 00428F80 walks the list headed at +0x48800
  R4  section 5: 003E00C0 reads 02B59D68 at 003E0680 and the rig bytes +0x63 and +0x5F
  R5  section 5: 004716A0 reads the cycle 01F223B0, the rise curve 01F22590 and the settle curve 01F22670 (image base plus
      displacement) and the 01DFE0BC time base; 00471150 reads the curves 01F22130 / 01F22170 and the heading +0x124
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
body = lambda fa: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)]
txt = lambda fa: [S(x) for x in body(fa)]
rips = lambda fa: {r for x in body(fa) for r in rip(x)}

SZ = {0x003E1350: 629, 0x003E1610: 629, 0x003E00C0: 1631, 0x0042EE90: 254, 0x0042DD90: 186, 0x004718D0: 31, 0x00471640: 27,
      0x004716A0: 290, 0x00471150: 220, 0x002E8570: 110, 0x002EDF30: 89, 0x002EE0D0: 91, 0x002EDE70: 91, 0x00428F80: 82,
      0x00421D20: 70, 0x002EDDC0: 95, 0x0042BDE0: 230, 0x00518F50: 418, 0x0051A890: 140, 0x00513150: 108, 0x00515FE0: 486}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("R0", not bad, "mismatches %s" % bad if bad else "all twenty-one sizes as cited")


def table(fa, tab):
    rv = struct.unpack("<17I", blob[OFF(tab):OFF(tab) + 68])
    return [BASE + r for r in rv]


offt, ont = table(0x003E1350, 0x003E15C8), table(0x003E1610, 0x003E1888)
O, N = {x.address: S(x) for x in body(0x003E1350)}, {x.address: S(x) for x in body(0x003E1610)}
exit_off = [a for a, s in O.items() if s == "ret"]
check("R1", O.get(0x003E1350) == "cmp edx, 0x10" and O.get(0x003E1353, "").startswith("ja ") and N.get(0x003E1610) == "cmp edx, 0x10"
      and offt[4] not in offt[:4] + offt[5:] and ont[4] not in ont[:4] + ont[5:] and len(set(offt[:4] + offt[5:])) == 16 and len(set(ont[:4] + ont[5:])) == 16
      and any(O.get(a) == "ret" for a in range(offt[4], offt[4] + 12)) and any(N.get(a) == "ret" for a in range(ont[4], ont[4] + 12)),
      "off index 4 -> %08X (%s ...), on index 4 -> %08X (%s ...); the other sixteen distinct in both" %
      (offt[4], O.get(offt[4]), ont[4], N.get(ont[4])))
tm = {f: txt(f) for f in (0x002EDF30, 0x002EE130, 0x002EDED0)}
st = {f: [s for s in t if any("+ 0x%x]" % d in s for d in (0x640, 0x644, 0x648)) and s.startswith("mov")] for f, t in tm.items()}
LW = txt(0x0042DD90)
svc = {0x002E85E0: 0x002EDF30, 0x002E8B80: 0x002EE130, 0x002ED320: 0x002EDED0}
pair = all(0x01DFE0BC in rips(sv) and any(x.mnemonic == "divss" for x in body(sv)) and "jmp 0x%x" % se in txt(sv) for sv, se in svc.items())
check("R2", pair and any("0x640" in s for s in st[0x002EDF30]) and any("0x644" in s for s in st[0x002EE130])
      and any("0x648" in s for s in st[0x002EDED0]) and any("+ 0x94]" in s for s in LW) and any("+ 0x304]" in s for s in LW),
      "each timed service divides by [01DFE0BC] and tail-jumps to its setter (%s); stores %s; the wrapper reads +0x94 and +0x304"
      % (pair, {("%08X" % f): v for f, v in st.items()}))
CD, SP = txt(0x0042EE90), txt(0x00428F80)
check("R3", any("+ 0x290]" in s for s in CD) and any("+ 0x40b]" in s for s in CD) and 0x01DFE0BC in rips(0x0042EE90) and any("0x48800" in s for s in SP),
      "countdown gates +0x290 / +0x40B, subtracts 01DFE0BC; the phase walks +0x48800")
F = {x.address: x for x in body(0x003E00C0)}
check("R4", 0x02B59D68 in rip(F[0x003E0680]) and any("+ 0x63]" in S(x) for x in F.values()) and any("+ 0x5f]" in S(x) for x in F.values()),
      "%s; rig bytes +0x63 and +0x5F read" % S(F[0x003E0680]))
# the curves are addressed as image base (a register loaded with 00120000) plus a large displacement
based = lambda fa: {BASE + o.mem.disp for x in body(fa) for o in x.operands if o.type == X86_OP_MEM and o.mem.base != X86_REG_RIP and o.mem.disp > 0x1000000}
check("R5", {0x01F223B0, 0x01F22590, 0x01F22670} <= based(0x004716A0) and 0x01DFE0BC in rips(0x004716A0) and BASE in rips(0x004716A0)
      and {0x01F22130, 0x01F22170} <= based(0x00471150)
      and any("+ 0x124]" in s for s in txt(0x00471150)),
      "Float bob base-relative tables %s and 01DFE0BC; controller-12 tables %s and heading +0x124"
      % (sorted("%08X" % a for a in based(0x004716A0)), sorted("%08X" % a for a in based(0x00471150))))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
