"""Falsification pass 1 on CONTRACT-battle-action-handler-table (OPUS, 2026-09-29), from the shipping image. Killers first.

  A0  HT-1: 01EEC460 holds 359 qwords: 341 non-null, 18 null, every non-null one inside .text; the qword just past is
      0x0000000400000002
  A1  HT-2: the non-null slots name exactly eight distinct handlers; 002FDDA0 x 249, 002FDA60 x 57, then 25 and 6, and four
      handlers with one id each
  A2  HT-3: the dispatcher tail-jumps with only rcx set (003050F1 `mov rcx, rbx`, 003050FE `jmp rdx`); 002FDDA0 re-reads the id
      at 002FDDB0 (`movzx edx, word ptr [rcx + 0x714]`)
  A3  HT-4: 00305080 and 00301830 both subtract 0x4000 and bound with `cmp ..., 0x166` / `ja` against 01EEC460; the dispatcher
      returns -1 on an empty slot
  A4  HT-6: the dispatcher posts event 0x2001 or 0x2010
"""
import collections, io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

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
B = {fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)) for fa in (0x00305080, 0x00301830, 0x002FDDA0)}
txt = {fa: [S(x) for x in b] for fa, b in B.items()}
text = next(x for x in SECS if x[0] == ".text")
q = lambda va: struct.unpack("<Q", blob[OFF(va):OFF(va) + 8])[0]
TB = 0x01EEC460

# A0
slots = [q(TB + 8 * i) for i in range(359)]
nn = [v for v in slots if v]
check("A0", len(nn) == 341 and slots.count(0) == 18 and all(text[1] <= v < text[1] + text[2] for v in nn) and q(TB + 8 * 359) == 0x0000000400000002,
      "%d non-null, %d null, all in .text; next qword %016X" % (len(nn), slots.count(0), q(TB + 8 * 359)))
# A1
c = collections.Counter(nn).most_common()
check("A1", len(c) == 8 and c[0] == (0x002FDDA0, 249) and c[1] == (0x002FDA60, 57) and [n for _v, n in c[2:]] == [25, 6, 1, 1, 1, 1],
      "%s" % [("%08X" % v, n) for v, n in c])
# A2
d = B[0x00305080]
check("A2", any(x.address == 0x003050F1 and S(x) == "mov rcx, rbx" for x in d) and any(x.address == 0x003050FE and S(x) == "jmp rdx" for x in d)
      and any(x.address == 0x002FDDB0 and S(x) == "movzx edx, word ptr [rcx + 0x714]" for x in B[0x002FDDA0]),
      "tail jmp with only rcx; 002FDDA0 re-reads +0x714")
# A3
def bounds(fa):
    t = txt[fa]
    return any("0xffffc000" in s or "- 0x4000" in s or "0x4000" in s for s in t) and any(s.startswith("cmp") and s.endswith(", 0x166") for s in t) \
        and any(TB in rip(x) for x in B[fa])
check("A3", bounds(0x00305080) and bounds(0x00301830) and any(s in ("or eax, 0xffffffff", "mov eax, 0xffffffff") for s in txt[0x00305080]),
      "both consumers subtract 0x4000, bound at 0x166 and read 01EEC460; the dispatcher returns -1")
# A4
check("A4", any(s.endswith(", 0x2001") for s in txt[0x00305080]) and any(s.endswith(", 0x2010") for s in txt[0x00305080]),
      "events 0x2001 and 0x2010 in the dispatcher")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
