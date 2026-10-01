"""Falsification pass 1 on CONTRACT-resource-request-queue (OPUS, 2026-09-30), from the shipping image. SECTION-02/-09's
executions and EXP-146 are carried, not re-run; these checks pin the static clauses the contract states.

  Q1  sections 2 and 10: 0032E620 stores the kind and index telemetry (022C51D8 / 022C51DC) before rejecting a negative
      index with 0xFFFFFFFF; the gate is 003EB0D0; the gated branch copies a 0x28-byte descriptor, sets its local +4 to
      0x80000 and +0x20 to 0, and - for a nonzero id only - clears slot +0x50, sets cap +0x30 = 0x80000, word +0x22 = 1,
      remaining +0x34 = the byte count and the first part to the signed minimum of count and 0x80000
  Q2  I3 / I4 / I6: 0032E870 loops pump (0032E070) -> in-flight getter (0046DFE0) -> pacer (0035EA30) while the free head
      022C51D0 is null; the id is (counter << 6) + (slot +0x58 & 0x3F) with the counter at 01EED498 reset to 1 above
      0xFFFFFF by a signed cmovg; the file offset is cdq / and 0x7ff / add / and 0xfffff800
  Q3  section 3: the requester consumes descriptor +0 (offset), +8 (argument, to +0x60), +0x10/+0x18 (to +0x40/+0x48),
      clears +0x50 rather than copying +0x20, writes state 1, the kind byte, word +0x22 = 0, +0x5C = 0, +0x38 = +0x70 =
      the destination, +0x24 the 32-bit index, +0x28 the byte count and the accumulator +0 = 0; the descriptor and flag
      arrive at entry rsp + 0x28 / + 0x30
  Q4  I2 / section 2: 0032E990 takes its flag in ECX and the slot from the free head, advancing the head (0032E9B5) - a
      null head faults at [+0x10]; 0032EC40 pushes the slot on the free head (0032ECBE) and marks its id -1, clearing
      nothing else
  Q5  section 10: 0032E370 calls the done callback with success 0 only when the callback is nonnull and the byte count is
      -1; kind 0xFF frees the sign-extended +0x24 path through 003697F0; otherwise it returns with rax still the callback
"""
import io, os, re
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
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


def body(fa):
    return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}


def rip_to(a, target):
    x = next(md.disasm(blob[OFF(a):OFF(a) + 16], a))
    m = re.search(r"rip ([+-]) 0x([0-9a-f]+)", x.op_str)
    return m is not None and x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) == target


R = body(0x0032E620)
check("Q1", rip_to(0x0032E634, 0x022C51D8) and rip_to(0x0032E63D, 0x022C51DC) and R.get(0x0032E64C) == "jns 0x32e656"
      and R.get(0x0032E64E) == "or eax, 0xffffffff" and R.get(0x0032E656) == "call 0x3eb0d0"
      and R.get(0x0032E684) == "movsd xmm0, qword ptr [rax + 0x20]" and R.get(0x0032E6CC) == "mov dword ptr [rsp + 0x34], 0x80000"
      and R.get(0x0032E6D6) == "mov qword ptr [rsp + 0x50], r14" and R.get(0x0032E6E7) == "je 0x32e738"
      and R.get(0x0032E6FF) == "mov qword ptr [rcx + 0x50], r14" and R.get(0x0032E703) == "mov dword ptr [rcx + 0x30], 0x80000"
      and R.get(0x0032E70A) == "mov word ptr [rcx + 0x22], 1" and R.get(0x0032E710) == "mov dword ptr [rcx + 0x34], eax"
      and R.get(0x0032E718) == "jl 0x32e721" and R.get(0x0032E71A) == "mov dword ptr [rcx + 0x28], 0x80000",
      "telemetry before the negative-index refusal; gated local +4 = 0x80000, +0x20 = 0; nonzero id: cap, chunk word, remaining, signed first part")
A = body(0x0032E870)
check("Q2", rip_to(0x0032E88D, 0x022C51D0) and A.get(0x0032E8AA) == "call 0x32e070" and A.get(0x0032E8AF) == "call 0x46dfe0"
      and A.get(0x0032E8B6) == "call 0x35ea30" and rip_to(0x0032E8BB, 0x022C51D0) and A.get(0x0032E8C3) == "je 0x32e8a2"
      and rip_to(0x0032E90D, 0x01EED498) and A.get(0x0032E924) == "and eax, 0x3f" and A.get(0x0032E927) == "shl ecx, 6"
      and A.get(0x0032E92A) == "add eax, ecx" and A.get(0x0032E935) == "cmp edx, 0xffffff" and A.get(0x0032E93F) == "cmovg edx, r12d"
      and A.get(0x0032E8FB) == "cdq" and A.get(0x0032E8FC) == "and edx, 0x7ff" and A.get(0x0032E90B) == "add eax, edx"
      and A.get(0x0032E913) == "and eax, 0xfffff800",
      "pump -> in-flight -> pacer while the free head is null; id = counter << 6 + slot; signed wrap to 1; offset toward zero to 0x800")
check("Q3", A.get(0x0032E8C5) == "mov ecx, dword ptr [rsp + 0x68]" and A.get(0x0032E8CE) == "mov rcx, qword ptr [rsp + 0x60]"
      and A.get(0x0032E8DB) == "mov eax, dword ptr [rcx]" and A.get(0x0032E8DD) == "mov r8, qword ptr [rcx + 0x10]"
      and A.get(0x0032E8E1) == "mov r9, qword ptr [rcx + 0x18]" and A.get(0x0032E8E5) == "mov r11d, dword ptr [rcx + 8]"
      and A.get(0x0032E951) == "mov qword ptr [r10 + 0x40], r8" and A.get(0x0032E955) == "mov qword ptr [r10 + 0x48], r9"
      and A.get(0x0032E959) == "mov qword ptr [r10 + 0x50], 0" and A.get(0x0032E961) == "mov dword ptr [r10 + 0x60], r11d"
      and A.get(0x0032E93B) == "mov byte ptr [r10 + 0x20], r12b" and A.get(0x0032E943) == "mov byte ptr [r10 + 0x21], r14b"
      and A.get(0x0032E969) == "mov word ptr [r10 + 0x22], 0" and A.get(0x0032E974) == "mov dword ptr [r10 + 0x5c], 0"
      and A.get(0x0032E94D) == "mov qword ptr [r10 + 0x38], rdi" and A.get(0x0032E970) == "mov qword ptr [r10 + 0x70], rdi"
      and A.get(0x0032E902) == "mov dword ptr [r10 + 0x24], ebp" and A.get(0x0032E92C) == "mov dword ptr [r10 + 0x28], esi"
      and A.get(0x0032E97C) == "mov qword ptr [r10], 0" and not any("[rcx + 0x20]" in t for t in A.values()),
      "descriptor +0/+8/+0x10/+0x18 consumed, +0x20 never read, +0x50 cleared; state 1, kind, fields as stated")
F, C = body(0x0032E990), body(0x0032EC40)
check("Q4", F.get(0x0032E99A) == "mov r9d, ecx" and rip_to(0x0032E990, 0x022C51D0) and F.get(0x0032E99D) == "mov rax, qword ptr [rdx + 0x10]"
      and rip_to(0x0032E9B5, 0x022C51D0) and F[0x0032E9B5].endswith("rax")
      and rip_to(0x0032ECBE, 0x022C51D0) and C[0x0032ECBE].endswith("rcx") and C.get(0x0032ECC5) == "mov dword ptr [rcx + 0x64], 0xffffffff"
      and not any(t.startswith(("mov byte ptr [rcx + 0x20]", "mov word ptr [rcx + 0x20]", "mov qword ptr [rcx + 0x40]")) for t in C.values()),
      "flag in ECX, slot from the free head, head advanced; recycle pushes on the free head, id -1, nothing else cleared")
E = body(0x0032E370)
check("Q5", E.get(0x0032E376) == "mov rax, qword ptr [rcx + 0x40]" and E.get(0x0032E380) == "je 0x32e394"
      and E.get(0x0032E382) == "cmp dword ptr [rcx + 0x28], -1" and E.get(0x0032E386) == "jne 0x32e394" and E.get(0x0032E38C) == "xor r8d, r8d"
      and E.get(0x0032E394) == "cmp byte ptr [rbx + 0x21], 0xff" and E.get(0x0032E39A) == "movsxd rcx, dword ptr [rbx + 0x24]"
      and E.get(0x0032E3A3) == "jmp 0x3697f0" and E.get(0x0032E3AD) == "ret",
      "done(arg, dest, 0) only for a nonnull callback with bytes == -1; kind 0xFF frees the sign-extended path; rax otherwise the callback")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
