"""Falsification pass 1 on CONTRACT-actor-storage-record-initialisation (OPUS, 2026-09-29), from the shipping image.

  S0  section 2: 00266530 is 1,439 B and its only caller is 002679F0
  S1  AR-1: 002679F0 calls memset before its first call to 00266530
  S2  AR-3: 00266530 reads byte +0x03 of the record three times and never writes it
  S3  (REFUTES AR-4's ordering) the index store `mov word ptr [rbx], r10w` is at 002665EB, after the stores to +0x14, +0xEC and
      +0xF5 and the calls 00266AD0 and 00266BD0 - it is not the first field written
  S4  AR-5: the highest offset the body stores through the record ends at 0x11C; it stores nothing in +0x60..+0xB7 or
      +0xC0..+0xEB itself; 003DB580 (called at 002667D7) writes +0x88, +0x24, +0x89 and +0x60
"""
import collections, io, os
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


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[p[1]] = int(p[0], 16)
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")
callers = collections.defaultdict(set)
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    for x in md.disasm(code, fa):
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            callers[T(x)].add(fa)
dis = lambda fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa))
F = 0x00266530
b = dis(F)

check("S0", sizes[F] == 1439 and callers[F] == {0x002679F0}, "%d B; callers %s" % (sizes[F], sorted("%08X" % c for c in callers[F])))
al = dis(0x002679F0)
first_init = next(i for i, x in enumerate(al) if x.mnemonic == "call" and T(x) == F)
ms = [i for i, x in enumerate(al[:first_init]) if x.mnemonic == "call" and T(x) == names.get("memset")]
check("S1", bool(ms), "memset before the first 00266530 call: %s" % bool(ms))
# the record register: the first store of a word at displacement 0
st = [x for x in b if x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "and", "or", "movss", "movups", "movaps", "xor", "inc")
      and x.operands[0].mem.base not in (0, X86_REG_RIP) and x.reg_name(x.operands[0].mem.base) not in ("rsp", "rbp")]
first = st[0] if st else None
rec = first.reg_name(first.operands[0].mem.base) if first else None
rd3 = [S(x) for x in b if any(o.type == X86_OP_MEM and o.mem.disp == 3 and x.reg_name(o.mem.base) == rec for o in x.operands[1:])]
wr3 = [S(x) for x in st if x.operands[0].mem.disp == 3 and x.reg_name(x.operands[0].mem.base) == rec]
check("S2", len(rd3) == 3 and not wr3, "record register %s; reads of +0x03 %s; writes %s" % (rec, rd3, wr3 or "none"))
rs = [x for x in st if x.reg_name(x.operands[0].mem.base) == rec]
idx = next(x for x in rs if x.operands[0].mem.disp == 0 and x.operands[0].size == 2)
before = [S(x) for x in rs if x.address < idx.address]
calls_before = ["%08X" % T(x) for x in b if x.mnemonic == "call" and x.address < idx.address]
check("S3", idx.address == 0x002665EB and S(idx) == "mov word ptr [rbx], r10w" and before[:3] == ["and byte ptr [rbx + 0x14], 0x7f", "mov qword ptr [rbx + 0xec], r13",
      "mov byte ptr [rbx + 0xf5], 0xff"] and calls_before[:2] == ["00266AD0", "00266BD0"],
      "(REFUTES 'the first field written is +0x00') the index store %s is at %08X, after %d record stores %s and the calls %s"
      % (S(idx), idx.address, len(before), before[:3], calls_before))
rs = [x for x in st if x.reg_name(x.operands[0].mem.base) == rec]
top = max(x.operands[0].mem.disp + x.operands[0].size for x in rs)
gap = [S(x) for x in rs if 0x60 <= x.operands[0].mem.disp < 0xB8 or 0xC0 <= x.operands[0].mem.disp < 0xEC]
c = dis(0x003DB580)
cw = sorted({x.operands[0].mem.disp for x in c if x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith("mov") and x.operands[0].mem.base not in (0, X86_REG_RIP)})
check("S4", top == 0x11C and not gap and any(x.address == 0x002667D7 and T(x) == 0x003DB580 for x in b) and {0x24, 0x60, 0x88, 0x89} <= set(cw),
      "extent 0x%X; own stores in the two spans: %s; 003DB580 writes +%s" % (top, gap or "none", [hex(d) for d in cw if d in (0x24, 0x60, 0x88, 0x89)]))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
