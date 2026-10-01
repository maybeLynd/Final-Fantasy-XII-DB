"""nav_mark.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Independent derivation for
ASTRA-REQ-OPUS-NAV-MARK-WRITE-DOMAIN (_experiments/evidence/nav-grid-mark-write-domain/), written without ASTRA's code, and the
NavGridParams consumer update.

  M  the mark fragment of 00392200 (003923D6..0039242E, after the overlap test 004690B0 answers non-zero): cell = row * gridWidth
     ([02AEE060]) + column; byte = id / 8 and bit = id % 8 by the signed idiom (cdq / and 7 / sar 3); the byte at
     [02AEE0A0] + cell * cellBitsetBytes ([02AEE0B8]) + byte gets `bts` of the bit (003923F4..00392412); then the byte
     [02AEE0A8] + cell is incremented (0039242B inc byte). There is no range check on the id inside the fragment
  K  00392200's four callers: 00392170 (one member added, only while [02AEE0BC] < 0x80; id = [02AEE0BC], then the increment) and
     the three phases of the population builder 00392740 (003928B4 ids from the list, 00392957 ids from 0x80, 003929D5 ids 0xA0 + i;
     nav_population.py P). Under stable counts the ids span 0..287 - exactly the 288 bits of a 0x24-byte cell record
  W  the per-cell byte's writers are this increment and two clears - the builder's allocation memset 0039267E and the rebuild's
     memset 003927D9 (gridWidth * gridHeight bytes) - and its three readers 00391394 / 00391882 / 00391BA2 compare it with zero and
     skip the cell. So the byte counts the ids marked into the cell since the last rebuild, as a byte (it wraps at 256)
  Arithmetic, not observed: an id of 288 would set bit 0 of the next cell's first byte; a count of 256 marks would read as 0.
  S  REGRESSION: NavGridParams +0x40 / +0x48 / +0x58 carry the mark rule (FAILS before)
Usage: python nav_mark.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)   # capstone prints small displacements in decimal
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0)) if m else None
A = lambda pairs: all(at(a)[:2] == v for a, v in pairs)
R = lambda a, cell: at(a)[2] == cell
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
m = (A([(0x3923CD, ("call", "0x4690b0")), (0x3923D4, ("je", "0x39242e")), (0x3923DC, ("mov", "eax, r12d")), (0x3923DF, ("cdq", "")),
        (0x3923E0, ("imul", "ecx, edi")), (0x3923E3, ("and", "edx, 7")), (0x3923F0, ("sar", "r8d, 3")), (0x3923FB, ("add", "ecx, ebx")),
        (0x392404, ("add", "ecx, r8d")), (0x39240A, ("movzx", "ecx, byte ptr [r8 + rdx]")), (0x39240F, ("bts", "ecx, eax")),
        (0x392412, ("mov", "byte ptr [r8 + rdx], cl")), (0x39241C, ("imul", "eax, edi")), (0x39241F, ("add", "eax, ebx")), (0x39242B, ("inc", "byte ptr [rcx + rax]"))])
     and R(0x3923D6, 0x2AEE060) and R(0x3923F4, 0x2AEE0A0) and R(0x3923FD, 0x2AEE0B8) and R(0x392416, 0x2AEE060) and R(0x392424, 0x2AEE0A8))
check("M", m, "mark: bts bit id%8 of byte id/8 in cell record (row*width+col)*0x24; then inc the cell's byte; no id range check")
text = next(s for s in SECS if s[0] == b".text"); tlo = B + text[2]; callers = []
for i in range(off(tlo), off(tlo) + text[3] - 5):
    if d[i] == 0xE8 and tlo + i - off(tlo) + 5 + struct.unpack_from("<i", d, i + 1)[0] == 0x392200: callers.append(tlo + i - off(tlo))
k = (callers == [0x3921E3, 0x3928B4, 0x392957, 0x3929D5] and A([(0x39218A, ("cmp", "eax, 0x80")), (0x39218F, ("jge", "0x3921ee")), (0x3921E8, ("inc", "dword ptr [rip + 0x275bece]")),
                                                                   (0x3929BD, ("lea", "ecx, [rsi + 0xa0]")), (0x392917, ("mov", "ebx, ebp")), (0x3927FF, ("mov", "ebp, 0x80"))])
     and R(0x392183, 0x2AEE0BC))
check("K", k, "callers %s: the guarded single add 00392170 and the builder's three id phases (0.., 0x80.., 0xA0..)" % ["%08X" % c for c in callers])
w = (A([(0x391394, ("cmp", "byte ptr [rcx + rax], 0")), (0x391882, ("cmp", "byte ptr [rcx + rax], r12b")), (0x391BA2, ("cmp", "byte ptr [rcx + rax], r12b")),
        (0x3927D9, ("call", "0x861ec0")), (0x39267E, ("call", "0x861ec0"))]) and R(0x3927CF, 0x2AEE0A8) and R(0x391380, 0x2AEE0A8) and R(0x391870, 0x2AEE0A8) and R(0x391B90, 0x2AEE0A8))
check("W", w, "the per-cell byte: written by the mark's inc and the two clears; three readers compare it with zero")
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/nav-population-opus/nav_mark.py"
TAG = "(OPUS, %s; ASTRA nav-grid-mark-write-domain)" % REC
ADD = {"cellBitsetArray": " || THE MARK 2026-09-28 %s M K: 00392200 sets bit (id %% 8) of byte (id / 8) in the record of cell row * gridWidth + column (bts), with no id range check. Its callers' ids span 0..287 under stable counts - exactly the 288 bits of a record; an id of 288 would spill into the next cell's first byte (arithmetic, not observed)" % TAG,
       "cellByteArray": " || A MARK COUNT 2026-09-28 %s M W: each mark also increments this cell's byte (0039242B inc byte), every other site that loads the pointer cell 02AEE0A8 either clears the bytes (003927D9 on rebuild) or compares them with zero, and the allocation memset 0039267E clears them too - so, among the sites that reach the bytes through that cell, the byte counts the ids marked into the cell since the last rebuild; the readers skip a zero cell, i.e. a cell with no marked id. The count wraps at 256, so 256 marks would read as empty (arithmetic, not observed)" % TAG,
       "cellBitsetBytes": " || MATCHES THE ID DOMAINS 2026-09-28 %s K: the population builder's three id phases (0..127, 0x80.., 0xA0 + i) cover 0..287 under stable counts - 288 ids, the 0x24-byte width exactly" % TAG}
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavGridParams" and c[3] in ADD and REC not in c[5]: c[5] += ADD[c[3]]; fl[i] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
F = {cells(l)[3]: cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "NavGridParams"}
check("S", all(ADD[k] in F[k][5] for k in ADD), "NavGridParams +0x40 / +0x48 / +0x58 carry the mark rule")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
