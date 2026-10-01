"""Falsification pass 1 on the-nonempty-prf-registration-and-specialized-relocation (OPUS, 2026-09-29), from the shipping
image. The SECTION-10 executions are carried, not re-run; these checks pin the static clauses the page rests on.

  R1  "Discovery": 00409780 sets both outputs to -1, normalises the name into the scratch at 02B62E20 (00409210), tests
      '@FRP' (0x50524640); version 0 walks children at +0x30 without skipping, version 1 at +0x40 skipping zero slots, each
      offset relative to that fixed table base; the root is tested first; a PRF root match writes offset 0 and leaves the
      index -1, a plain root writes 0 / 0
  R2  00409A60 pads the root and child names (memset to 32) before the mode branch at 00409B95: mode 0 copies into owned
      storage (0051F020 / 0051EF90), mode 1 keeps the tagged source at +0x30
  R3  "Two offsets": 00409FE0 reads the parser offset as the dword at source + align64(size) - 4 (0040A15F / 0040A16A /
      0040A16F)
  R4  "The specialized subtype": 003A9A70 stores the record in the table *(02EBEF78) at its subtype word and calls
      005004C0; 0024ED80 publishes ctx + 0x850 into 02EBEF78 (distinct from + 0x848 and + 0x840); 00500470 makes four
      004304F0 calls at +0x00, +0x10, +0x20, +0x30, and 004304F0 re-encodes the two dwords at +0 and +4 through
      0020E600 / 0020E620 with the delta - eight dwords
  R5  "Movement and repair": 003A9BA0 walks the slots 8..0x17F8 of *(02EBEF78) and, for a nonzero slot, first runs
      005004C0 on slot + delta with the delta, then adds the delta to the slot
  R6  CON-195's consumer (OV-39 box): the configuration table 02B64380 is not left unpopulated - 00409F80 calls its
      populator 0040A230 (00409F84) and the render resource root initialiser 0041E3A0 calls 00409F80 (0041E40B)
"""
import collections, io, os, re, struct
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


F = body(0x00409780)
check("R1", F.get(0x004097AA) == "mov dword ptr [rsi], 0xffffffff" and F.get(0x004097B0) == "mov dword ptr [r9], 0xffffffff"
      and rip_to(0x004097BC, 0x02B62E20) and F.get(0x004097C9) == "call 0x409210" and F.get(0x0040981A) == "cmp dword ptr [r10], 0x50524640"
      and F.get(0x00409840) == "call 0x409c30" and F.get(0x0040984B) == "je 0x4098b1" and F.get(0x00409859) == "lea r11, [r10 + 0x40]"
      and F.get(0x00409865) == "je 0x40987c" and F.get(0x00409867) == "lea ecx, [rax + 0x40]" and F.get(0x0040986D) == "add ecx, r10d"
      and F.get(0x004098A4) == "call 0x409c30" and F.get(0x004098BE) == "lea r11, [r10 + 0x30]" and F.get(0x004098C8) == "add ecx, 0x30"
      and F.get(0x004098C2) == "mov ecx, dword ptr [r11]" and F.get(0x004098C5) == "mov r8, rdi" and F.get(0x004098CD) == "add ecx, r10d"
      and F.get(0x004098B1) == "mov dword ptr [rsi], r9d" and F.get(0x004098B4) == "jmp 0x409912"
      and F.get(0x0040990C) == "mov dword ptr [rsi], r9d" and F.get(0x0040990F) == "mov dword ptr [r14], r9d",
      "-1/-1 at entry; '@FRP'; v0 +0x30 unskipped, v1 +0x40 skipping zero; root first; PRF root -> offset 0, index -1; plain root -> 0/0")
S = body(0x00409A60)
pads = [a for a, t in S.items() if t == "call 0x861ec0"]
check("R2", len(pads) >= 2 and max(pads) < 0x00409B95 and S.get(0x00409B95) == "test ebp, ebp" and S.get(0x00409B9E) == "mov qword ptr [r14 + 0x30], r15"
      and S.get(0x00409BB9) == "call 0x51f020" and S.get(0x00409BD7) == "call 0x51ef90",
      "%d name pads (last %08X) before the mode branch 00409B95; mode 1 keeps the source at +0x30, mode 0 copies" % (len(pads), max(pads)))
E = body(0x00409FE0)
check("R3", E.get(0x0040A15F) == "add eax, 0x3f" and E.get(0x0040A16A) == "and eax, 0xffffffc0" and E.get(0x0040A16F) == "mov edx, dword ptr [rax + r14 - 4]",
      "the parser offset is the dword at source + align64(size) - 4")
A, P, K, Z = body(0x003A9A70), body(0x0024ED80), body(0x00500470), body(0x004304F0)
calls = [(a, t) for a, t in K.items() if t == "call 0x4304f0"]
check("R4", A.get(0x003A9A7A) == "movzx r8d, word ptr [rcx]" and rip_to(0x003A9A97, 0x02EBEF78) and A.get(0x003A9AA1) == "mov qword ptr [r8 + r9*8], rcx"
      and A.get(0x003A9AAD) == "call 0x5004c0"
      and P.get(0x0024EDC7) == "lea rax, [rdx + 0x850]" and rip_to(0x0024EDCE, 0x02EBEF78) and P.get(0x0024EDB9) == "lea rax, [rdx + 0x848]"
      and P.get(0x0024EDAB) == "lea rax, [rdx + 0x840]" and not rip_to(0x0024EDC0, 0x02EBEF78)
      and len(calls) == 4 and K.get(0x00500484) == "lea rcx, [rdi + 0x10]" and K.get(0x0050048F) == "lea rcx, [rdi + 0x20]" and K.get(0x0050049A) == "lea rcx, [rdi + 0x30]"
      and Z.get(0x004304FF) == "mov ecx, dword ptr [rcx]" and Z.get(0x00430512) == "mov dword ptr [rdi], eax" and Z.get(0x0043050F) == "mov ecx, dword ptr [rdi + 4]"
      and Z.get(0x00430527) == "mov dword ptr [rdi + 4], eax" and Z.get(0x00430501) == "call 0x20e600" and Z.get(0x0043050A) == "call 0x20e620"
      and Z.get(0x00430506) == "lea rcx, [rbx + rax]",
      "table *(02EBEF78) = ctx + 0x850; four rebases at +0/+0x10/+0x20/+0x30, each re-encoding two dwords with the delta")
B = body(0x003A9BA0)
check("R5", B.get(0x003A9BAD) == "mov ebx, 8" and rip_to(0x003A9BC0, 0x02EBEF78) and B.get(0x003A9BD1) == "je 0x3a9bec"
      and B.get(0x003A9BD3) == "lea rcx, [rsi + rax]" and B.get(0x003A9BD9) == "call 0x5004c0" and B.get(0x003A9BE8) == "add qword ptr [rbx + rcx], rsi"
      and B.get(0x003A9BF0) == "cmp rbx, 0x1800",
      "specialise slot + delta first (003A9BD9), then add the delta to the slot (003A9BE8)")
C, R_ = body(0x00409F80), body(0x0041E3A0)
check("R6", C.get(0x00409F84) == "call 0x40a230" and R_.get(0x0041E40B) == "call 0x409f80",
      "00409F80 calls the 02B64380 populator 0040A230; 0041E3A0 calls 00409F80 (CON-195)")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
