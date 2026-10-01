"""Falsification pass 1 on CONTRACT-system-stop-registry (OPUS, 2026-09-29), from the shipping image. Killers first.

  R0  section 2: 00226280 is 952 B and 00226BE0 1,936 B
  R1  SS-1 / SS-3: two all-ones accumulators; the walk from 01FD4410 to 01FD46B0 ANDs [cursor - 0x2B0] and [cursor - 0x10];
      the active bitset 01FD46D4 has zero references in the apply
  R2  SS-4: `js` over a negative fade, first non-negative taken, `cmovg` keeps the smaller, then `mov dword [rax], -1` only on
      that path
  R3  SS-5: `movabs r10, 0x20000000000` and `or r8, r10` stored back to record B for every slot
  R4  SS-6: the apply exits when 01FD46D0 is 0 and clears it at 0022660A; a start ORs the bitset (00226C7A) and sets dirty (00226C87)
  R5  SS-7: `shr rax, 0x1e / not eax / and eax, 2 / or eax, 1` from record A's low dword
  R6  SS-4's note: 00226B30 writes -1 to each record's first qword and 0 to byte +0x14 over 56 records, never +0x10, and sets
      the combined fades (01FD46B0, 01FD46C8) to -1
"""
import io, os
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
B = {fa: list(md.disasm(blob[OFF(fa):OFF(fa) + n], fa)) for fa, n in ((0x00226280, 952), (0x00226BE0, 1936), (0x00226B30, 0x6F))}
I = {x.address: x for b in B.values() for x in b}
at = lambda va: S(I[va]) if va in I else "?"
cell = lambda va: rip(I[va])[0] if va in I and rip(I[va]) else None
run = lambda lo, hi: [S(I[a]) for a in sorted(I) if lo <= a <= hi]

check("R0", sizes[0x00226280] == 952 and sizes[0x00226BE0] == 1936, "%d / %d B" % (sizes[0x00226280], sizes[0x00226BE0]))
check("R1", at(0x002262BA) == "or rdi, 0xffffffffffffffff" and at(0x002262C2) == "or rbx, rdi" and cell(0x002262D7) == 0x01FD4410 and cell(0x00226298) == 0x01FD46B0
      and at(0x002262E4) == "and rdi, qword ptr [rax - 0x2b0]" and run(0x002262E0, 0x002262EB) == ["mov r8, qword ptr [rax - 0x10]", "and rdi, qword ptr [rax - 0x2b0]", "and rbx, r8"]
      and at(0x0022630E) == "add rax, 0x18" and not [x for x in B[0x00226280] if 0x01FD46D4 in rip(x)],
      "all-ones accumulators; 01FD4410..01FD46B0 step 0x18; A at -0x2B0, B at -0x10; 01FD46D4 unread")
check("R2", run(0x002262EE, 0x00226307) == ["mov edx, dword ptr [rax]", "test edx, edx", "js 0x226307", "test ecx, ecx", "jns 0x2262fc", "mov ecx, edx",
                                            "jmp 0x226301", "cmp ecx, edx", "cmovg ecx, edx", "mov dword ptr [rax], 0xffffffff", "or r8, r10"],
      "minimum of the non-negative fades; the -1 reset only on that path")
check("R3", at(0x002262A3) == "movabs r10, 0x20000000000" and run(0x00226307, 0x0022630A) == ["or r8, r10", "mov qword ptr [rax - 0x10], r8"],
      "bit 41 ORed into record B on both paths")
check("R4", cell(0x00226287) == 0x01FD46D0 and at(0x0022628E) == "je 0x226633" and cell(0x0022660A) == 0x01FD46D0 and at(0x0022660A).endswith(", 0")
      and cell(0x00226C7A) == 0x01FD46D4 and at(0x00226C7A).startswith("or dword") and cell(0x00226C87) == 0x01FD46D0 and at(0x00226C87).endswith(", 1"),
      "apply gated and cleared on 01FD46D0; start ORs 01FD46D4 and sets 01FD46D0")
check("R5", at(0x00226C77) == "mov eax, dword ptr [r15]" and at(0x00226C81) == "shr rax, 0x1e" and at(0x00226C85) == "not eax"
      and at(0x00226C8E) == "and eax, 2" and at(0x00226C91) == "or eax, 1", "(~(A >> 30) & 2) | 1")
init = [S(x) for x in B[0x00226B30]]
check("R6", "mov qword ptr [rax], 0xffffffffffffffff" in init and "mov byte ptr [rax + 0x14], 0" in init and "mov ecx, 0x1c" in init
      and cell(0x00226B37) == 0x01FD4160 and cell(0x00226B48) == 0x01FD46B4 and cell(0x00226B56) == 0x01FD46E4
      and "mov dword ptr [rdx - 4], 0xffffffff" in init and not any("+ 0x10]" in s for s in init),
      "56 records (2 x 28, rax not reset); first qword -1, +0x14 = 0, +0x10 untouched; combined fades 01FD46B0 / 01FD46C8 = -1")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
