"""Falsification pass 1 on fef-and-motion-entries (OPUS, 2026-09-29), from the shipping image and the installed archive's own
index. Rows check the page as corrected by this pass (CON-195; CON-196 corrects a consumer). The .cm/.ca census
(members/fef_motion_entry_census.py) and FABLE's embedded-EFX sweep are carried, not re-run.

  F0  the binder 00504940 (called from 00504F00 at 00505026) passes dword[obj+0x44] and @FEF + 0x30 to 0016D6A0 at 005049BD;
      0016D6A0 is C2 00 00 (ret 0)
  F1  0041E580 is `mov rcx, [rcx + 0xD90]; jmp 00409FE0`, reached from exactly 002E4DB4, 002E4EFA, 003DC371, 003DD8AB
  F2  00409FE0: the @FEF tag lookup (edx 0x46454640) gates the path; the last five name characters fold into an index of
      the table 02B64380 (first char x 1280, Horner x10, bias -0x1A0A); a NULL row writes to address 0 (0040A135)
  F3  CON-195: the table's populator 0040A230 is NOT unreferenced. 00409F80 calls it (00409F84) and tail-jumps 0051FB70;
      0041E3A0 (the render resource root's initialiser) calls 00409F80 at 0041E40B, on the start-up chain
      0017D000 -> 0017D4C0 -> 0022A0B0 -> 003325C0 -> 003325D0 -> 0041E3A0 (each link a direct call). So the rows are
      filled at start-up, not NULL (static reading; execution in a shipped session is not observed here)
  F4  the populator stores exactly 144 rip-relative .rdata strings, every one a `PS2Data\\obj_finish\\in\\...\\<stem>.cm`
      path, and every one of those paths is an entry of the installed archive (its header, read now)
  F5  CON-196 (a consumer): those 144 values are .rdata strings - no lea target is in .text
"""
import io, os, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
sys.path.insert(0, os.path.join(ROOT, "Tools", "dashboard"))
import vbf_index  # noqa: E402  (ASTRA's A17 header parser)
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


def section(va):
    return next((n for n, start, size, _r, _z in SECS if start <= va < start + size), "?")


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
body = lambda fa, n=None: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + (n or sizes[fa])], fa)]
A = lambda fa, n=None: {x.address: (S(x), rip(x)) for x in body(fa, n)}
text = next(x for x in SECS if x[0] == ".text")
traw = blob[text[3]:text[3] + text[4]]


def callers(t):
    return sorted(text[1] + k for k in range(len(traw) - 5)
                  if traw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", traw, k + 1)[0] == t)


def eq(m, a, t, target=None):
    g = m.get(a)
    return g is not None and g[0] == t and (target is None or target in g[1])


Bd = A(0x00504940)
check("F0", eq(Bd, 0x005049BD, "call 0x16d6a0") and blob[OFF(0x0016D6A0):OFF(0x0016D6A0) + 3] == b"\xc2\x00\x00"
      and 0x00505026 in callers(0x00504940), "binder -> 0016D6A0 (ret 0) at 005049BD; called from 00505026")
T = A(0x0041E580, 12)
check("F1", eq(T, 0x0041E580, "mov rcx, qword ptr [rcx + 0xd90]") and eq(T, 0x0041E587, "jmp 0x409fe0")
      and callers(0x0041E580) == [0x002E4DB4, 0x002E4EFA, 0x003DC371, 0x003DD8AB], "thunk and its four callers")
R = A(0x00409FE0)
check("F2", eq(R, 0x0040A0A4, "mov edx, 0x46454640") and eq(R, 0x0040A0B4, "je 0x40a1c9") and eq(R, 0x0040A118, "shl rcx, 8")
      and eq(R, 0x0040A100, "lea rdx, [rcx - 0x1a0a]") and eq(R, 0x0040A11C, "lea rsi, [rip + 0x275a25d]", 0x02B64380)
      and eq(R, 0x0040A135, "mov dword ptr [0], esi"), "@FEF gate, the fold, the table, the null trap")
chain = [(0x0040A230, 0x00409F84), (0x00409F80, 0x0041E40B), (0x0041E3A0, 0x0033263C), (0x003325D0, 0x003325C7),
         (0x003325C0, 0x0022A401), (0x0022A0B0, 0x0017D5CC), (0x0017D4C0, 0x0017D01F)]
links = {("%08X" % tgt): (site in callers(tgt)) for tgt, site in chain}
P9 = A(0x00409F80, 18)
check("F3", all(links.values()) and eq(P9, 0x00409F84, "call 0x40a230") and eq(P9, 0x00409F8D, "jmp 0x51fb70"),
      "CON-195: the populator is called at 00409F84; chain up to 0017D000 %s" % links)
Pb = body(0x0040A230)
lea = [t for x in Pb if x.mnemonic == "lea" for t in rip(x)]
movs = [x for x in Pb if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rip")]
strs = []
for t in lea:
    o = OFF(t); strs.append(blob[o:o + 160].split(b"\0")[0].decode("latin-1"))
names, _rec = vbf_index.archive_index(vbf_index.DEFAULT_ARCHIVE)
low = {n.lower() for n in names}
inarc = [s for s in strs if s.replace("\\", "/").lower() in low]
check("F4", len(lea) == 144 and len(movs) == 144 and all(s.startswith("PS2Data\\obj_finish\\in\\") and s.endswith(".cm") for s in strs)
      and len(inarc) == 144, "144 stores of obj_finish .cm paths; %d of 144 are entries of the installed archive" % len(inarc))
check("F5", {section(t) for t in lea} == {".rdata"}, "CON-196: every stored value is an .rdata string (sections %s)" % sorted({section(t) for t in lea}))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
