"""Falsification pass 1 on the-external-source-owner-and-borrowed-view-lifetime.md (OPUS, 2026-09-29), from the image.

  E0  sections 1-2: owners at 02B581A0 + (group * 16 + index) * 0x1C; 003DD790 resets one group of 16 - handle+state qword,
      route byte +0x0D, group byte +0x0C, index word +0x0E, and the group's pending mask at 02B58A60 + group * 4 - leaving
      +0x08 and +0x10..+0x1B untouched
  E1  section 2: the armer 003DDA20 accepts state 0 only, writes +0x08 (its third argument) and state 2, and ORs the pending bit
  E2  section 3: 003DDA70's descriptor - file offset (+0x18) at +0, low32(owner) at +8, completion 003DD850 at +0x10, null at
      +0x18 - then 0032E620, then state 3 with the return unused
  E3  section 4: 003DD380 sweeps exactly 16 records: state 1 -> free, clear handle+state and +0x0D; state 3 -> state 5 only;
      state 4 -> dispose (0041E490), then free (00369800), then the same clears
  E4  section 4: 003DD850 unpins (0036D170) first; state 5 -> dispose, free, clear only the state dword; any other state ->
      register (0041E580) and state 4 with no test of the result; the owner arrives as `mov edi, ecx` (low 32 bits)
  E5  section 4: 003DD740 returns the handle only for state 4
  E6  section 5: 0032E370 calls the completion only when its callback is set and the requested length is -1
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
B = {fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)) for fa in (0x003DD790, 0x003DDA20, 0x003DDA70, 0x003DD380, 0x003DD850, 0x003DD740, 0x0032E370)}
txt = {fa: [S(x) for x in b] for fa, b in B.items()}
cell = lambda fa, va: rip(next(x for x in B[fa] if x.address == va))[0]

# E0
check("E0", cell(0x003DD790, 0x003DD79D) == 0x02B581A0 + 0x0D and "imul rax, r8, 0x1c0" in txt[0x003DD790] and "cmp edx, 0x10" in txt[0x003DD790]
      and txt[0x003DD790][7:11] == ["mov word ptr [rax + 1], dx", "inc edx", "mov qword ptr [rax - 0xd], r10", "mov byte ptr [rax], r10b"]
      and "mov byte ptr [rax - 1], cl" in txt[0x003DD790] and cell(0x003DD790, 0x003DD7C9) == 0x02B58A60
      and not any(("[rax - 5]" in s) or ("[rax + 3]" in s) for s in txt[0x003DD790]),
      "base %08X (+0x0D); 16 records of 0x1C per group (0x1C0); +0x00 qword, +0x0C group, +0x0D route, +0x0E index; mask %08X" % (cell(0x003DD790, 0x003DD79D) - 0x0D, cell(0x003DD790, 0x003DD7C9)))
# E1
a = txt[0x003DDA20]
check("E1", cell(0x003DDA20, 0x003DDA34) == 0x02B581A0 and "cmp dword ptr [rax + rcx + 4], 0" in a and "mov dword ptr [rax + rcx + 8], r8d" in a
      and "mov dword ptr [rax + rcx + 4], 2" in a and cell(0x003DDA20, 0x003DDA47) == 0x02B58A60 and "or dword ptr [r8 + r9*4], eax" in a,
      "state 0 only; +0x08 = arg 3; state 2; pending bit ORed at 02B58A60")
# E2
s2 = txt[0x003DDA70]
check("E2", "mov edx, dword ptr [rbx + 0x18]" in s2 and "mov dword ptr [rsp + 0x30], edx" in s2 and "mov dword ptr [rsp + 0x38], ebx" in s2
      and cell(0x003DDA70, 0x003DDA83) == 0x003DD850 and "mov qword ptr [rsp + 0x40], rcx" in s2 and "mov qword ptr [rsp + 0x48], 0" in s2
      and s2[s2.index("call 0x32e620") + 1] == "mov dword ptr [rbx + 4], 3",
      "descriptor at rsp+0x30: offset, low32(owner), 003DD850, null; state 3 written right after 0032E620, its return unread")
# E3
s3 = txt[0x003DD380]
check("E3", "mov esi, 0x10" in s3 and "add rbx, 0x1c" in s3 and cell(0x003DD380, 0x003DD39E) == 0x02B581A4
      and s3[s3.index("mov ecx, dword ptr [rbx]") + 1:s3.index("mov ecx, dword ptr [rbx]") + 7] == ["sub ecx, 1", "je 0x3dd3e0", "sub ecx, 2", "je 0x3dd40f", "cmp ecx, 1", "jne 0x3dd3f0"]
      and "call 0x41e490" in s3 and "call 0x369800" in s3 and s3.index("call 0x41e490") < s3.index("call 0x369800")
      and "mov byte ptr [rbx + 9], bpl" in s3 and "mov qword ptr [rbx - 4], rbp" in s3 and "mov dword ptr [rbx], 5" in s3,
      "16 records; 1 -> free + clears; 3 -> 5; 4 -> dispose then free + clears; others untouched")
# E4
s4 = txt[0x003DD850]
check("E4", s4[3:6] == ["mov edi, ecx", "mov ecx, dword ptr [rdi]", "call 0x36d170"] and "cmp dword ptr [rdi + 4], 5" in s4
      and s4.index("call 0x41e490") < s4.index("call 0x369800") < s4.index("mov dword ptr [rdi + 4], 0")
      and "call 0x41e580" in s4 and s4[s4.index("call 0x41e580") + 2] == "mov dword ptr [rdi + 4], 4"
      and not any(s.startswith("test eax") for s in s4[s4.index("call 0x41e580"):]),
      "owner = low32 (mov edi, ecx); unpin first; 5 -> dispose, free, state 0; else register, state 4, result untested")
# E5
check("E5", "cmp dword ptr [rax + rcx + 4], 4" in txt[0x003DD740] and "mov eax, dword ptr [rax + rcx]" in txt[0x003DD740] and cell(0x003DD740, 0x003DD743) == 0x02B581A0,
      "handle returned only for state 4")
# E6
s6 = txt[0x0032E370]
check("E6", s6[2:10] == ["mov rax, qword ptr [rcx + 0x40]", "mov rbx, rcx", "test rax, rax", "je 0x32e394", "cmp dword ptr [rcx + 0x28], -1", "jne 0x32e394",
                         "mov rdx, qword ptr [rcx + 0x70]", "xor r8d, r8d"] and "call rax" in s6,
      "completion only when +0x40 is set and the length +0x28 is -1")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
