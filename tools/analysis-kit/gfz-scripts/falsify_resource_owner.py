"""Falsification pass 1 on the-resource-owner-from-copy-or-borrow-to-disposal.md (OPUS, 2026-09-29), from the image.

  O0  section 1: 003B38B0 builds a stack template at rsp+0x20 with type byte 3, ORs 0x0C into byte 2, and stores source32 and
      offset32 at template +0x860 / +0x864 (rsp + 0x880 / 0x884)
  O1  section 2: the parser 003EDAD0 tests byte 2 mask 4 (`test byte ptr [rax + 2], 4`) - the borrow bit - at two sites
  O2  section 4: the ticket pool is 64 slots of 0x38 at 02EBCD80 (003B37E0: `and eax, 0x3f` / `imul rbx, rax, 0x38`) ending at
      the link cells 02EBDB80 / 88 / 90 that 003B38B0 uses; 003B37E0 compares the WHOLE id (`cmp dword ptr [rbx], ecx`) first
  O3  section 5: 00409D60 finds a match (0051FE30), sweeps render records, then cancels the ticket (003B37E0), tears the row
      down (00409730) and removes the slot (0051FCF0), then looks for the next match
  O4  section 5: 00409730 stores the word at +0, dwords +4 / +0x40 / +0x44 and the qword +0x30 - and never +0x38 (the cache)
"""
import io, os
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
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
B = {fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)) for fa in (0x003B38B0, 0x003EDAD0, 0x003B37E0, 0x00409D60, 0x00409730)}
txt = {fa: [S(x) for x in b] for fa, b in B.items()}

# O0
t0 = txt[0x003B38B0]
check("O0", "mov byte ptr [rsp + 0x20], 3" in t0 and "or byte ptr [rsp + 0x22], 0xc" in t0 and "mov dword ptr [rsp + 0x880], ebp" in t0
      and "mov dword ptr [rsp + 0x884], esi" in t0, "template rsp+0x20: type 3, byte 2 |= 0x0C, +0x860 = source32, +0x864 = offset32")
# O1
m4 = [S(x) for x in B[0x003EDAD0] if S(x) == "test byte ptr [rax + 2], 4"]
check("O1", len(m4) == 2, "003EDAD0 tests byte 2 mask 4 at %d sites" % len(m4))
# O2
base = [t for x in B[0x003B37E0][:10] for t in rip(x)]
links = sorted({t for x in B[0x003B38B0] for t in rip(x)})
check("O2", base == [0x02EBCD80] and "and eax, 0x3f" in txt[0x003B37E0] and "imul rbx, rax, 0x38" in txt[0x003B37E0] and 0x02EBCD80 + 64 * 0x38 == 0x02EBDB80
      and {0x02EBDB80, 0x02EBDB88, 0x02EBDB90} <= set(links)
      and txt[0x003B37E0].index("cmp dword ptr [rbx], ecx") < txt[0x003B37E0].index("mov dword ptr [rbx + 0x30], 0xffffffff"),
      "64 x 0x38 at 02EBCD80 .. 02EBDB80; links %s; whole-id compare before the first write" % ["%08X" % l for l in links])
# O3
order = [T(x) for x in B[0x00409D60] if x.mnemonic in ("call", "jmp") and T(x) not in (None, 0x0020E600, 0x0020E620)]
check("O3", order[0] == 0x0051FE30 and order.index(0x003B37E0) < order.index(0x00409730) < order.index(0x0051FCF0) and order[-1] == 0x0051FE30
      and sum(1 for x in B[0x00409D60] if x.mnemonic == "call" and T(x) in (0x0020E600, 0x0020E620)) > 0,
      "find, render sweep, 003B37E0, 00409730, 0051FCF0, find next: %s" % ["%08X" % o for o in order])
# O4
st = [x for x in B[0x00409730] if x.mnemonic == "mov" and x.operands[0].type == X86_OP_MEM and x.reg_name(x.operands[0].mem.base) == "rdi"]
disp = sorted(x.operands[0].mem.disp for x in st)
check("O4", disp == [0, 4, 0x30, 0x40, 0x44] and 0x38 not in disp, "00409730 stores at +%s; +0x38 untouched" % ["0x%X" % d for d in disp])
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
